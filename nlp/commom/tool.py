import time
from pyhanlp import *


def load_dictionary():
    """
    加载HanLP中的mini词库
    :return: 一个set形式的词库
    """
    io_util = JClass('com.hankcs.hanlp.corpus.io.IOUtil')
    path = HanLP.Config.CoreDictionaryPath.replace('.txt', '.mini.txt')
    dic = io_util.loadDictionary([path])
    return set(dic.keySet())


def count_single_char(word_list: list):
    """
    统计单字词数量
    :param word_list:
    :return:
    """
    return sum(1 for word in word_list if len(word) == 1)


def evaluate_speed(segment, text, dic, pressure=10000):
    """
    评估分词速度
    :param segment: 分词方法
    :param text: 目标文本
    :param dic: 字典
    :param pressure: 迭代次数
    :return:
    """
    start_time = time.time()
    for i in range(pressure):
        segment(text, dic)
    elapsed_time = time.time() - start_time
    print('{:>18} {:.2f} 万字/秒'.format(segment.__name__, len(text) * pressure / 10000 / elapsed_time))


def trie_evaluate_speed(segment, text, pressure=10000):
    """
    评估分词速度
    :param segment: 分词器
    :param text: 目标文本
    :param dic: 字典
    :param pressure: 迭代次数
    :return:
    """
    start_time = time.time()
    for i in range(pressure):
        segment.parse_longest(text)
    elapsed_time = time.time() - start_time
    print('{:>18} {:.2f} 万字/秒'.format(segment.__name__, len(text) * pressure / 10000 / elapsed_time))


if __name__ == '__main__':
    print(len(load_dictionary()))