import json

class Entry:
    """
        记录对象
    """
    def __init__(self, **kwargs):
        """
        :param args:
            key:记录执行的变量
            value:执行变量的值
        """
        self.key = kwargs.get('key')
        self.value = kwargs.get('value')

    def instance_from_str(self, json_str: str):
        """
        通过json字符串序列化对象
        :param json_str: json字符串
        :return:
        """
        json_obj = json.loads(json_str)
        for k, v in json_obj.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def str_from_instance(self):
        """
        将自身转换为json字符串
        :return:
        """



class Log:
    """
    日志对象
    """
    
    def __init__(self, **kwargs):
        """
        :param kwargs:
            term:记录产生的任期
            index:记录的索引
        """
        self.term = kwargs.get('term')
        self.index = kwargs.get('index')
        self.entries = kwargs.get('entries', [])


class RPC:
    """
    RPC对象基类
    """

    def __init__(self, rpc_type: int, **kwargs):
        """
        :param rpc_type: 请求类型，1-日志复制 2-日志复制响应 3-选举 4-选举响应
        :param source_id: 来源ID
        :param target_id: 目标ID
        """
        self.type = rpc_type
        self.source_id = kwargs.get('source_id', None)
        self.target_id = kwargs.get('target_id', None)


class AppendRPC(RPC):
    """
        日志复制RPC对象
    """
    def __init__(self, **kwargs):
        """
        :param args:
            term:leader的任期
            leader_id:leader的my_id
            prev_log_index:leader上条记录的索引
            prev_log_term:leader上条记录的任期
            entries:发送的记录集合，当记录为空时表示为心跳
            leader_commit_index:leader提交的记录的索引
        """
        super(AppendRPC, self).__init__(1)
        self.term = kwargs.get('term', None)
        self.leader_id = kwargs.get('leader_id', None)
        self.prev_log_index = kwargs.get('prev_log_index', None)
        self.prev_log_term = kwargs.get('prev_log_term', None)
        self.leader_commit_index = kwargs.get('leader_commit_index', None)
        self.log = kwargs.get('log', None)


class AppendRPCResult(RPC):
    """
    日志复制请求返回对象
    """

    def __init__(self, **kwargs):
        """
        :param args:
            term:当前节点的任期，用于leader更新自己的任期
            success:false-失败， true-成功
            message:信息
        """
        super(AppendRPCResult, self).__init__(2)
        self.candidate_id = kwargs.get('candidate_id', None)
        self.is_heart_beat = False
        self.term = kwargs.get('term', None)
        self.success = kwargs.get('success', None)


class RequestVoteRPC(RPC):
    """
        投票请求RPC对象
    """
    def __init__(self, **kwargs):
        """
        :param args:
            term:candidate的任期
            candidate_id:candidate的my_id
            last_log_index:candidate最新一条记录的索引
            last_log_term:candidate最新一条记录的任期号
        """
        super(RequestVoteRPC, self).__init__(3)
        self.term = kwargs.get('term', None)
        self.candidate_id = kwargs.get('candidate_id', None)
        self.last_log_index = kwargs.get('last_log_index', None)
        self.last_log_term = kwargs.get('last_log_term', None)


class RequestVoteRPCResult(RPC):
    """
    投票RPC请求返回对象
    """

    def __init__(self, **kwargs):
        """
        :param args:
            term:当前节点的任期，用于candidate更新自己的任期
            vote_granted:false-失去选票 true-获得选票
        """
        super(RequestVoteRPCResult, self).__init__(4)
        self.term = kwargs.get('term', None)
        self.vote_granted = kwargs.get('vote_granted', None)




