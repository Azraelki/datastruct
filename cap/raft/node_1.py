from cap.raft.node_application import Node

if __name__ == '__main__':
    config = {
        'my_id': 'node_1',
        'address': ('localhost', 8000),
        'nodes': {
            'node_1': ('localhost', 8000),
            'node_2': ('localhost', 8002),
            'node_3': ('localhost', 8003),
            # 'node_4': ('192.168.3.28', 8004),
            # 'node_5': ('192.168.3.28', 8005),
        }
    }
    node = Node(config)
    node.run()
