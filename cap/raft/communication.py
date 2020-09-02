import socket
import json


class CommunicationManager:
    """
    通信器，用于节点间的通信
    """

    def __init__(self, config: dict):
        self.nodes = config.get('nodes', {})
        self.internal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.internal_socket.settimeout(0.5)
        self.internal_socket.bind(('0.0.0.0', config.get('address')[1]))
        self.client_socket = {

        }

    def send_to_all(self, rpc: dict):
        """
        发送信息给所有节点
        :param rpc: 信息
        :return:
        """
        for _my_id in self.nodes:
            self.send_to(rpc, self.nodes[_my_id])

    def send_to(self, rpc: dict, addr: tuple):
        """
        发送RPC到给指定的节点
        :param rpc: 信息
        :param addr: 目标地址和端口
        :return:
        """
        rpc_str = json.dumps(rpc, ensure_ascii=False).encode('utf-8')
        self.internal_socket.sendto(rpc_str, addr)

    def recv(self):
        """
        从绑定的端口接收信息
        :return:
        """
        rpc_str, addr = self.internal_socket.recvfrom(65535)
        return json.loads(rpc_str), addr

    def hold_client(self, address: str, index: int):
        """
        持有客户端
        :param address:
        :param index:
        :return:
        """
        addr = address.split(":")
        self.client_socket[index] = (addr[0], int(addr[1]))

    def release_client(self, key: int):
        """
        释放客户端
        :param key: index
        :return:
        """
        del self.client_socket[key]
