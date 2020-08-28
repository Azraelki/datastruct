import enum
import time
import random
import logging
import os
import json

from cap.raft.communication import CommunicationManager
from cap.raft.log_manager import LogManager

# 定义节点状态枚举类，leader,follower,candidate
State = {'LEADER': 'leader', 'FOLLOWER': 'follower', 'CANDIDATE': 'candidate'}
RpcType = {'APPEND': 'append', 'APPEND_RESPONSE': 'append_response', 'VOTE': 'vote', 'VOTE_RESPONSE': 'vote_response', 'CLIENT_APPEND': 'client_append'}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')


class Node:
    """
        节点类，用于代表一个分布式节点
    """

    def __init__(self, config: dict):
        """
        :param config: 配置字典
            my_id:节点标识
            heart_beat_period:心跳周期，默认为30ms
            min_election_period:最小选举超时时间
        """
        self.config = config
        self.my_id = config.get('my_id')
        self.leader_id = None
        self.heart_beat_period = config.get('heart_beat_period', 200)
        self.min_election_period = config.get('min_election_period', 5000)
        # 获取节点列表
        self.nodes = config.get('nodes', {})

        # 创建通讯管理器
        self.communication_manager = CommunicationManager(config)

        # 创建状态机
        self.state_machine = StateMachine()

        # 创建状态对象，初始化为跟随者状态
        self.state = State['FOLLOWER']
        # 初始化当前任期为0
        self.current_term = 0
        # 初始化当前轮次投票的节点的my_id,首次启动时默认为None
        self.vote_for = None
        # 从本地恢复最近的任期号和投票情况
        self.restore()

        # 初始化最大提交记录的索引值
        self.last_commit_index = -1
        # 初始化最大执行记录的索引值
        self.last_apply_index = -1

        # 初始化日志管理器
        self.log_manager = LogManager(self.my_id)

        # 初始化投票信息
        self.vote_count = {_my_id: 0 for _my_id in self.nodes.keys()}

        # 创建下一个要发送的记录列表（leader节点使用，用于记录所有follower的日志复制）
        # 选举结束后初始化，初始值为leader最后一个entry的index+1
        self.next_index = {_my_id: self.log_manager.last_log_index+1 for _my_id in self.nodes.keys()}

        # 创建一个用于记录每个节点和leader保持一致的最后一个日志记录的索引（leader节点使用，用于记录所有follower的日志复制）
        # 初始值为-1
        self.match_index = {_my_id: -1 for _my_id in self.nodes.keys()}

        # 下次选举时间
        self.next_elect_time = 0
        self.reset_election_period()

        # 下次心跳时间
        self.next_heart_beat = 0
        self.reset_heart_beat_period()

    def store(self):
        """
        持久化当前任期及最近一次投票情况
        :return:
        """
        if os.path.exists(self.my_id):
            with open(self.my_id+'/node.json', 'w', encoding='utf-8') as f:
                json.dump({'current_term': self.current_term,
                           'vote_for': self.vote_for,
                           'last_commit_index': self.last_commit_index,
                           'last_apply_index': self.last_apply_index,
                           'state_machine': self.state_machine.state_dict,
                           }, f, ensure_ascii=False, indent=4)

    def restore(self):
        """
        从本地恢复任期及最近一次投票情况
        :return:
        """
        if os.path.exists(self.my_id+'/node.json'):
            with open(self.my_id+'/node.json', 'r', encoding='utf-8') as f:
                node_info = json.load(f)
                if 'current_term' in node_info and 'vote_for' in node_info:
                    self.current_term = node_info.get('current_term')
                    self.vote_for = node_info.get('vote_for')

    def reset_election_period(self):
        """
        重置选举超时时间
        :return:
        """
        self.next_elect_time = time.time()*1000 + self.min_election_period + random.randint(0, self.min_election_period)

    def reset_heart_beat_period(self):
        """
        重置心跳超时时间
        :return:
        """
        self.next_heart_beat = time.time()*1000 + self.heart_beat_period

    def change_state(self, target_state: State):
        """
        修改自身状态
        :param target_state: 目标状态
        :return:
        """
        self.state = target_state

    def append_entries(self, data: dict):
        """
        角色：follower
        日志复制
        :param data:
        :return:
        """
        response = {
            'type': RpcType['APPEND_RESPONSE'],
            'term': self.current_term,
            'source_id': self.my_id,
            'target_id': data['source_id'],
            'is_heart_beat': False,
            'success': False
        }
        # 数据任期小于当前节点任期则直接返回失败
        if data['term'] < self.current_term:
            response['success'] = False
            self.communication_manager.send_to(response, self.nodes[response['target_id']])
            return

        # 设置当前节点leader为source
        self.leader_id = data['leader_id']

        # 当match失败时，返回失败响应，并且删除match_index及之后所有记录
        if data['pre_log_term'] != self.log_manager.get_term_by_index(data['pre_log_index']):
            response['success'] = False
            self.log_manager.delete_logs(data['pre_log_index'])
            self.communication_manager.send_to(response, self.nodes[response['target_id']])
            logging.info('当前角色：【{}】，与leader：【{}】日志【{}】记录不符，记录恢复中'.format(self.state, self.leader_id, data['pre_log_index']))
            return

        log = data.get('log')

        # 当entries为空时则为心跳请求
        if not log or not log.get('entries'):
            response['is_heart_beat'] = True
            response['success'] = True
            logging.info('当前角色：【{}】，接收到来自leader：【{}】 心跳检测'.format(self.state, self.leader_id))
        else:
            # 添加日志，并发送成功响应
            self.log_manager.append_log(log)
            response['success'] = True
            logging.info('当前角色：【{}】，接收到来自leader：【{}】 的日志复制，term:【{}】，index:【{}】'.format(self.state, self.leader_id, log['term'], log['index']))
        self.communication_manager.send_to(response, self.nodes[response['target_id']])

        # 设置节点的最新的commit_index
        if data['leader_commit_index'] > self.last_commit_index:
            self.last_commit_index = min(data['leader_commit_index'], self.log_manager.last_log_index)

    def vote_request(self, data: dict):
        """
        角色: follower
        用于处理vote请求
        :param data:
        :return:
        """
        response = {
            'type': RpcType['VOTE_RESPONSE'],
            'term': self.current_term,
            'source_id': self.my_id,
            'target_id': data['source_id'],
            'vote_granted': False
        }
        # 任期号小于当前任期则放弃投票
        if data['term'] < self.current_term:
            response['vote_granted'] = False
            self.communication_manager.send_to(response, self.nodes[response['target_id']])
            return

        if not self.vote_for or self.vote_for == data['candidate_id']:
            if data['last_log_term'] >= self.log_manager.last_log_term \
                    and data['last_log_index'] >= self.log_manager.last_log_index:
                self.vote_for = data['source_id']
                self.store()
                response['vote_granted'] = True
                self.communication_manager.send_to(response, self.nodes[response['target_id']])
            else:
                # 当前节点的信息比source新时
                self.vote_for = None
                self.store()
                response['vote_granted'] = False
                self.communication_manager.send_to(response, self.nodes[response['target_id']])
        else:
            response['vote_granted'] = False
            self.communication_manager.send_to(response, self.nodes[response['target_id']])

    def redirect(self, data, addr):
        """
        转发信息
        :param data:
        :param addr:
        :return:
        """
        if not data:
            return None
        if data['type'] == RpcType['CLIENT_APPEND']:
            if self.state != State['LEADER']:
                if self.leader_id:
                    self.communication_manager.send_to(data, self.nodes[self.leader_id])
                return None
            else:
                return data

        if data['target_id'] != self.my_id:
            self.communication_manager.send_to(data, self.nodes[data['target_id']])
            return None
        else:
            return data

        return data

    def all_do(self, data: dict):
        """
        所有节点都需执行的操作
        :param data: 信息
        :return:
        """
        # 执行已提交的记录到状态机
        if self.last_commit_index > self.last_apply_index:
            old_value = None
            if 'x' in self.state_machine.state_dict:
                old_value = self.state_machine.state_dict['x']
            for log in self.log_manager.get_logs(self.last_apply_index+1, self.last_commit_index+1):
                self.state_machine.apply_entries(log.get('entries', []))
            logging.info('当前角色：【{}】，leader是：【{}】 ---更新状态机，before:【{}】, after:【{}】---'.format(self.state,
                                                                                             self.leader_id,
                                                                                             old_value,
                                                                                             self.state_machine.state_dict['x']))
            self.last_apply_index = self.last_commit_index

        if not data or data['type'] == RpcType['CLIENT_APPEND']:
            return

        # 更新最新的任期
        if data['term'] > self.current_term:
            logging.info('当前角色：【{}】 ---任期号过小，转变为follower，data.term:【{}】, current_term:【{}】---'.format(self.state, data['term'], self.current_term))
            self.current_term = data['term']
            self.vote_for = None
            self.leader_id = data['source_id']
            self.change_state(State['FOLLOWER'])
            self.store()

    def follower_do(self, data: dict):
        """
        跟随者要做的操作
        :param data: 信息
        :return:
        """
        now = time.time() * 1000
        if data:
            if data['type'] == RpcType['APPEND']:
                # 当接收到leader请求时
                self.append_entries(data)
            elif data['type'] == RpcType['VOTE']:
                # 当接收到candidate请求时
                self.vote_request(data)
            # 重置选举超时时间
            if self.current_term == data['term']:
                self.reset_election_period()
        else:
            if now >= self.next_elect_time:
                # 超过下次选举时间后进入candidate状态，并发送选举请求
                self.reset_election_period()
                self.change_state(State['CANDIDATE'])
                self.current_term += 1
                self.vote_for = self.my_id
                self.store()
                # 初始化投票信息
                self.vote_count = {_my_id: 0 for _my_id in self.nodes.keys()}

    def candidate_do(self, data: dict):
        now = time.time() * 1000

        for target_id in self.nodes.keys():
            count = sum(self.vote_count.values())
            if self.vote_count[target_id] == 0 and target_id != self.my_id and count == 0:
                request = {
                    'type': RpcType['VOTE'],
                    'term': self.current_term,
                    'source_id': self.my_id,
                    'target_id': target_id,
                    'candidate_id': self.my_id,
                    'last_log_term': self.log_manager.last_log_term,
                    'last_log_index': self.log_manager.last_log_index
                }
                self.communication_manager.send_to(request, self.nodes[target_id])
                logging.info(
                    '当前角色：【{}】 ---发送vote请求，source_id:【{}】, target_id:【{}】, current_term:【{}】---'.format(self.state, self.my_id,
                                                                                                target_id, self.current_term))
        self.vote_count[self.my_id] = 1
        if data and data['term'] == self.current_term:
            if data['type'] == RpcType['VOTE_RESPONSE']:
                if data['vote_granted']:
                    self.vote_count[data['source_id']] = 1
                count = sum(self.vote_count.values())
                logging.info(
                    '当前角色：【{}】 ---当前票数：【{}】， current_term:【{}】---'.format(self.state, count, self.current_term))
                # 超过半数时成为leader
                if count > (len(self.vote_count.keys())//2):
                    logging.info(
                        '当前角色：【{}】 ---当前票数：【{}】， 票数达到多数派，当选为【{}】号leader---'.format(self.state, count+1, self.current_term))
                    self.change_state(State['LEADER'])
                    self.vote_for = None
                    self.leader_id = self.my_id
                    self.store()
                    self.next_heart_beat = 0
                    self.next_index = {_my_id: self.log_manager.last_log_index + 1 for _my_id in self.nodes.keys()}
                    self.match_index = {_my_id: -1 for _my_id in self.nodes.keys()}
                    return

            elif data['type'] == RpcType['APPEND_RESPONSE']:
                logging.info(
                    '当前角色：【{}】 ---接收到高任期请求，转变为follower---'.format(self.state))
                # 收到日志复制请求时变为follower
                self.reset_election_period()
                self.change_state(State['FOLLOWER'])
                self.vote_for = None

                self.store()
                return
        else:
            count = sum(self.vote_count.values())
            # 超过半数时成为leader
            if count > (len(self.vote_count.keys()) // 2):
                logging.info(
                    '当前角色：【{}】 ---当前票数：【{}】， 票数达到多数派，当选为【{}】号leader---'.format(self.state, count, self.current_term))
                self.change_state(State['LEADER'])
                self.vote_for = None
                self.leader_id = self.my_id
                self.store()
                self.next_heart_beat = 0
                self.next_index = {_my_id: self.log_manager.last_log_index + 1 for _my_id in self.nodes.keys()}
                self.match_index = {_my_id: -1 for _my_id in self.nodes.keys()}
                return

        if now > self.next_elect_time:
            # 选举超时后开启下一轮选举
            self.reset_election_period()
            self.current_term += 1
            self.vote_for = self.my_id
            self.store()
            # 初始化投票信息
            self.vote_count = {_my_id: 0 for _my_id in self.nodes.keys()}
            logging.info(
                '当前角色：【{}】 ---选举超时，开启下轮选举，任期为【{}】---'.format(self.state, self.current_term))

    def leader_do(self, data: dict):
        """
        leader需做的操作
        :param data: 信息
        :return:
        """
        now = time.time() * 1000
        if now > self.next_heart_beat:
            for target_id in self.next_index.keys():
                if target_id != self.my_id:
                    request = {
                        'type': RpcType['APPEND'],
                        'source_id': self.my_id,
                        'target_id': target_id,
                        'term': self.current_term,
                        'leader_id': self.my_id,
                        'log': self.log_manager.get_log_by_index(self.next_index[target_id]),
                        'pre_log_term': self.log_manager.get_term_by_index(self.next_index[target_id]-1),
                        'pre_log_index': self.next_index[target_id]-1,
                        'leader_commit_index': self.last_commit_index
                    }
                    self.communication_manager.send_to(request, self.nodes[target_id])
                    logging.info(
                        '当前角色：【{}】 ---发送日志复制请求，source_id:【{}】, target_id:【{}】, index:【{}】,current_term:【{}】---'.format(self.state,
                                                                                                            self.my_id,
                                                                                                            target_id,
                                                                                                            self.next_index[target_id],
                                                                                                            self.current_term))
            self.reset_heart_beat_period()

        if data and data['type'] == RpcType['CLIENT_APPEND']:
            log = {
                'term': self.current_term,
                'index': self.log_manager.last_log_index + 1,
                'entries': data['entries']
            }
            # 持有客户端
            self.communication_manager.hold_client(data['address'], log['index'])
            self.log_manager.append_log(log)
            return

        if data and data['term'] == self.current_term:
            if data['type'] == RpcType['APPEND_RESPONSE']:
                if data['success'] and not data['is_heart_beat']:
                    self.match_index[data['source_id']] += self.next_index[data['source_id']]
                    self.next_index[data['source_id']] += 1
                elif not data['success']:
                    self.next_index[data['source_id']] -= 1

        while True:
            N = self.last_commit_index + 1
            count = 0
            self.match_index[self.my_id] = self.log_manager.last_log_index
            for _my_id in self.match_index:
                if self.match_index[_my_id] >= N:
                    count += 1
                if count > len(self.nodes) // 2:
                    self.last_commit_index = N
                    # 释放客户端
                    address = self.communication_manager.client_socket.get(N, None)
                    if address:
                        self.communication_manager.send_to(
                            {'status': 'success', 'index': N}, address)
                        self.communication_manager.release_client(N)
                    break
            else:
                break

    def run(self):
        while True:
            now = time.time()*1000 + 50
            try:
                try:
                    data, addr = self.communication_manager.recv()
                except Exception as e:
                    data, addr = None, None

                data = self.redirect(data, addr)

                self.all_do(data)

                if self.state == State['FOLLOWER']:
                    self.follower_do(data)

                if self.state == State['CANDIDATE']:
                    self.candidate_do(data)

                if self.state == State['LEADER']:
                    self.leader_do(data)

                self.store()

            except Exception as e:
                logging.info(e)
                raise e


class StateMachine:
    """
    状态机
    """

    def __init__(self):
        self.state_dict = dict()

    def apply_entry(self, entry: dict):
        """
        执行一条entry
        :param entry: 记录
        :return:
        """
        self.state_dict[entry['key']] = entry['value']

    def apply_entries(self, entries: list):
        """
        执行一组操作
        :param entries: 记录列表
        :return:
        """
        for entry in entries:
            self.apply_entry(entry)


if __name__ == '__main__':
    config = {
        'my_id': 'node_1',
        'address': ('localhost', 8000),
        'nodes': {
            'node_1': ('localhost', 8000),
            # 'node_2': ('localhost', 8001),
            'node_3': ('localhost', 8002)
        }
    }
    node = Node(config)
    node.run()
