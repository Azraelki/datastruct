import time
import json
import socket
import random
import logging

from multiprocessing import Process

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')


def send():
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servers = [
        ('localhost', 8001),
        ('localhost', 8002),
        ('localhost', 8003)
    ]

    count = 0
    while True:
        addr = random.choice(servers)
        count += 1
        data = {'type': 'client_append', 'entries': [{'key': 'x', 'value': count}], 'address': 'localhost:10000'}
        logging.info('send: {}'.format(data))

        data = json.dumps(data).encode('utf-8')
        cs.sendto(data, addr)

        time.sleep(10)


def recv():
    addr = ('localhost', 10000)
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss.bind(addr)

    while True:
        data, addr = ss.recvfrom(65535)

        data = json.loads(data)
        print('recv: status:' + str(data['index']) + ' has been committed')
        logging.info('status: {}, {} 已经被提交'.format(data['status'], data['index']))


if __name__ == '__main__':
    p1 = Process(target=send, name='send', daemon=True)
    p1.start()
    p2 = Process(target=recv, name='recv', daemon=True)
    p2.start()

    p1.join()
    p2.join()