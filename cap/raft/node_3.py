from cap.raft.node_application import Node

if __name__ == '__main__':
    config = {
        'my_id': 'node_3',
        'address': ('localhost', 8003),
        'nodes': {
            'node_1': ('localhost', 8001),
            'node_2': ('localhost', 8002),
            'node_3': ('localhost', 8003)
        }
    }
    node = Node(config)
    node.run()
