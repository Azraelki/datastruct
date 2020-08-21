import enum
import time
import random

from threading import Timer

from cap.raft.communication import CommunicationManager
from cap.raft.entry_log import Entry, Log,  RequestVoteRPC, RequestVoteRPCResult, AppendRPC, AppendRPCResult

# 定义节点状态枚举类，leader,follower,candidate
State = enum.Enum('State', ('LEADER', 'FOLLOWER', 'CANDIDATE'))


class Node:
    """
        节点类，用于代表一个分布式机器
    """

    def __init__(self, config: dict):
        """
        :param config: 配置字典
            my_id:节点标识
            heart_beat_period:心跳周期，默认为30ms
            min_election_period:最小选举超时时间
        """
        self.config = config
        self.my_id = config.get('my_id', 0)
        self.heart_beat_period = config.get('heart_beat_period', 30)
        self.min_election_period = config.get('min_election_period', 200)

        # 创建通讯管理器
        self.communication_manager = CommunicationManager(config)
        # 创建状态机
        self.state_machine = StateMachine()

        # 创建状态对象，初始化为candidate状态
        self.state = State.CANDIDATE
        # 初始化当前任期为0
        self.current_term = 0
        # 初始化当前轮次投票的节点的my_id,首次启动时默认为None
        self.vote_for = None
        # 初始化选票计数为0
        self.vote_count = 0
        # 初始化多数派数量为0
        self.majority_count = 0
        # 初始化最大提交记录的索引值
        self.last_commit_index = 0
        # 初始化最大执行记录的索引值
        self.last_apply_index = 0

        # 创建下一个要发送的记录列表（leader节点使用，用于记录所有follower的日志复制）
        # 选举结束后初始化，初始值为leader最后一个entry的index+1
        self.next_index = {}

        # 创建一个用于记录每个节点和leader保持一致的最后一个日志记录的索引（leader节点使用，用于记录所有follower的日志复制）
        # 初始值为0
        self.match_index = {}

        # 初始化日志列表
        self.logs = []

        # 选举时间戳
        self.elect_tamp = None

    def start(self):
        """
        启动节点
        :return:
        """
        # 1、检查本地储存的日志并进行恢复
        # 2、启动本地端口监听
        # 3、随机生成选举超时时间，初始化投票信息，发起投票请求
        self.change_state(State.CANDIDATE)
        self.reset_election_period()
        self.elect_cycle()

    def append_request(self, entry_list: list = None):
        """
        角色：leader
        发起日志复制请求
            步骤-1、组装日志对象，组装RPC请求对象，
            步骤-2、将发送的请求添加到自己的日志记录中
            步骤-2、发送日志复制请求
        :param entry_list: 记录列表
        :return:
        """
        log = Log()
        last_term, last_index = self.__get_last_log_term_and_index()
        log.term = self.current_term
        log.index = last_index + 1
        log.entries = entry_list

        rpc = AppendRPC()
        rpc.term = self.current_term
        rpc.leader_id = self.my_id
        rpc.leader_commit_index = self.last_commit_index
        rpc.prev_log_term = last_term
        rpc.prev_log_index = last_index
        rpc.log = log

        self.logs.append(log)
        self.communication_manager.send_to_all(rpc)

    def deal_append_request(self, rpc: AppendRPC):
        """
        角色：follower
        处理日志复制请求
            步骤-1、如果leader的任期小于当前任期，返回错误
            步骤-2、查找match log，判定是否一致,如果一致则追加日志，并返回成功
                步骤2.1、更新自己的commit_index
            步骤-3、否则，日志复制失败，返回错误
        :return:
        """
        self.reset_election_period()

        response = AppendRPCResult()
        response.term = self.current_term
        response.candidate_id = self.my_id

        if rpc.term < self.current_term:
            response.success = False
            response.message = '任期号小于follower节点'
        else:
            pre_log = self.find_log_by_index(rpc.prev_log_index)
            if (rpc.prev_log_index == 0) or (pre_log and pre_log.term == rpc.prev_log_term):
                self.clear_by_match_index(rpc.prev_log_index)
                if rpc.leader_commit_index > self.last_commit_index:
                    self.last_commit_index = min(rpc.leader_commit_index, rpc.prev_log_index)
                if rpc.log:
                    self.logs.append(rpc.log)
                else:
                    response.is_heart_beat = True
                response.success = True
            else:
                response.success = False
                response.message = 'match失败'
        self.communication_manager.send_to(response, rpc.leader_id)

    def deal_append_response(self, rpc: AppendRPCResult):
        """
        角色：leader
        处理日志复制响应
            步骤-1、判断返回的任期号是否大于当前任期号
            步骤-2、判定日志辅助是否成功
            步骤-3、失败重试
        :return:
        """
        self.reset_election_period()

        if rpc.term > self.current_term:
            self.change_state(State.FOLLOWER)
        elif rpc.success:
            if not rpc.is_heart_beat:
                self.next_index[rpc.candidate_id] += 1
                self.match_index[rpc.candidate_id] += 1
                self.update_last_commit_index()
        else:
            print(rpc.message)

            self.next_index[rpc.candidate_id] -= 1
            self.match_index[rpc.candidate_id] = 0 if self.match_index[rpc.candidate_id] <= 0 \
                else self.match_index[rpc.candidate_id] - 1

            new_log = self.find_log_by_index(self.next_index[rpc.candidate_id])
            prev_log = self.find_log_by_index(self.match_index[rpc.candidate_id])
            new_rpc = AppendRPC()
            new_rpc.leader_id = self.current_term
            new_rpc.leader_commit_index = self.last_commit_index
            new_rpc.prev_log_term = prev_log.term if prev_log else None
            new_rpc.prev_log_index = prev_log.index if prev_log else 0
            new_rpc.log = new_log
            self.communication_manager.send_to(new_rpc, rpc.candidate_id)

    def vote_request(self):
        """
        角色：candidate
        发起选举请求
            步骤-1、组装选举请求信息
            步骤-2、向所有机器发送选举请求
        :return:
        """
        print('我是-{},当前的任期号是-{}，我开始选举了'.format(self.my_id, self.current_term))

        self.current_term += 1
        self.reset_vote_count()
        self.reset_majority_count()

        rpc = RequestVoteRPC()
        rpc.term = self.current_term
        rpc.candidate_id = self.my_id
        rpc.last_log_term, rpc.last_log_index = self.__get_last_log_term_and_index()

        self.reset_election_period()
        self.communication_manager.send_to_all(rpc)

    def deal_vote_request(self, rpc: RequestVoteRPC):
        """
        角色：candidate,follower
        处理选举请求
        :param rpc 选举请求对象
            1、选举发起者任期小于当前节点，选举失败
            2、否则，若选举发起者的日志记录至少和自己一样新，则投票给对方，否则选举失败
        :return:
        """
        self.reset_election_period()

        response = RequestVoteRPCResult()
        response.term = self.current_term
        if rpc.term < self.current_term:
            response.vote_granted = False
        else:
            last_log_term, last_log_index = self.__get_last_log_term_and_index()
            if rpc.last_log_term > last_log_term or \
                    (rpc.last_log_term == last_log_term and rpc.last_log_index >= last_log_index):
                response.vote_granted = True
                self.vote_for = rpc.candidate_id
                self.current_term = rpc.term
            else:
                response.vote_granted = False
        self.communication_manager.send_to(response, rpc.candidate_id)

    def deal_vote_response(self, rpc: RequestVoteRPCResult):
        """
        角色：candidate,leader
        :param rpc:选举响应对象
        处理选举响应
            步骤-1、响应任期小于当前任期则忽略
            步骤-2、响应任期大于当前任期，转变为follower
            步骤-3、累加选票，当选票数量大于等于多数派时转换为leader,并发送心跳包
        :return:
        """
        self.reset_election_period()

        if not rpc or rpc.term > self.current_term:
            self.change_state(State.FOLLOWER)
        elif rpc.term == self.current_term and rpc.vote_granted:
            self.vote_count += 1
            if self.vote_count >= self.majority_count and self.state == State.CANDIDATE:
                print('leader is {}'.format(self.my_id))
                self.change_state(State.LEADER)
                _, max_index = self.__get_last_log_term_and_index()
                self.append_request()

    def heart_beat(self):
        """
        角色：leader
        心跳请求,复用日志复制请求，设置传入的entry为空
        :return:
        """
        if self.state == State.LEADER:
            self.append_request()
            timer = Timer(self.heart_beat_period/1000, self.heart_beat, None)
            timer.start()

    def __get_last_log_term_and_index(self):
        """
        获取最近一条日志的任期号和索引号
        :return:(last_log_term, last_log_index)
        """
        last_log_term = 0
        last_log_index = 0
        if self.logs:
            log = self.logs[-1]
            last_log_term = log.term
            last_log_index = log.index
        return last_log_term, last_log_index

    def change_state(self, target_state: State):
        """
        修改自身状态
        :param target_state: 目标状态
        :return:
        """
        self.state = target_state
        if self.state == State.LEADER:
            self.heart_beat()

    def reset_election_period(self):
        """
        重置选举超时时间
        :return:
        """
        self.elect_tamp = time.time()*1000 + self.min_election_period + random.randint(0, self.min_election_period)

    def reset_vote_count(self):
        """
        重置选票技术
        :return:
        """
        self.vote_count = 0

    def reset_majority_count(self):
        """
        重置多数派数量
        :return:
        """
        node_list = self.config.get('node_list', [])
        self.majority_count = len(node_list)/2 + 1

    def find_log_by_index(self, index):
        """
        根据日志索引号日志
        :param index: 日志索引号
        :return:
        """
        result = None
        if self.logs:
            for key, log in enumerate(self.logs):
                if log.index == index:
                    result = log
                    break
        return result

    def clear_by_match_index(self, index):
        """
        根据match index清除之后所有的日志
        :param index: 日志索引号
        :return:
        """
        if index == 0:
            self.logs.clear()
        if self.logs:
            for key, log in enumerate(self.logs):
                if log.index == index:
                    self.logs = self.logs[:key+1]
                    break

    def update_last_commit_index(self):
        """
        角色：leader
        更新last_commit_index
        :return:
        """
        count_dict = {}
        for v in self.match_index.values():
            count_dict[v] += 1
        for k, v in count_dict.items():
            if v > self.majority_count and k > self.last_commit_index:
                prev_last_commit_index = self.last_commit_index
                self.last_commit_index = k
                for log in self.logs:
                    if prev_last_commit_index < log.index <= self.last_commit_index:
                        self.state_machine.apply_entries(log.entries)
                break

    def elect_cycle(self):
        if time.time()*1000 > self.elect_tamp:
            self.change_state(State.CANDIDATE)
            self.vote_request()
            self.reset_election_period()
        else:
            timer = Timer(self.min_election_period/1000, self.elect_cycle, None)
            timer.start()


class StateMachine:
    """
    状态机
    """

    def __init__(self):
        self.state_dict = dict()

    def apply_entry(self, entry: Entry):
        """
        执行一条entry
        :param entry: 记录
        :return:
        """
        self.state_dict[entry.key] = entry.value

    def apply_entries(self, entries: list):
        """
        执行一组操作
        :param entries: 记录列表
        :return:
        """
        for entry in entries:
            self.apply_entry(entry)


if __name__ == '__main__':
    node1 = Node(config={'my_id': 1})
    node2 = Node(config={'my_id': 2})
    node3 = Node(config={'my_id': 3})
    cm = CommunicationManager(None)
    cm.append_node(node1)
    cm.append_node(node2)
    cm.append_node(node3)
    node1.start()
    node2.start()
    node3.start()