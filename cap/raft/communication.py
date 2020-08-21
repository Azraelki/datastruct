from cap.raft.entry_log import RPC


class CommunicationManager:
    """
    通信器，用于节点间的通信
    """

    def __init__(self, config: dict):
        self.node_dict = {}

    def send_to_all(self, rpc: RPC):
        """
        发送RPC到当前配置的所有文件上
        :param rpc: 请求对象
        :return:
        """
        if rpc.type == 1:
            for node in self.node_dict.values():
                if node.my_id != rpc.leader_id:
                    self.send_to(rpc, node.my_id)
        if rpc.type == 3:
            for node in self.node_dict.values():
                if node.my_id != rpc.candidate_id:
                    self.send_to(rpc, node.my_id)

    def send_to(self, rpc: RPC, my_id: int):
        """
        发送RPC到给指定的节点
        :param rpc: 请求对象
        :param my_id: 目标及其的my_id
        :return:
        """
        if rpc.type == 1:
            self.node_dict[my_id].deal_append_request(rpc)
        elif rpc.type == 2:
            self.node_dict[my_id].deal_append_response(rpc)
        elif rpc.type == 3:
            self.node_dict[my_id].deal_vote_request(rpc)
        elif rpc.type == 4:
            self.node_dict[my_id].deal_vote_response(rpc)

    def append_node(self, node):
        """
        添加一个节点
        :return:
        """
        self.node_dict[node.my_id] = node
        node.communication_manager = self
