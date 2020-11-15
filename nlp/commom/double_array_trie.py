# -*- coding:utf-8 -*-
# Author：hankcs
# Date: 2018-05-26 21:16
# 《自然语言处理入门》2.5 双数组字典树
# 配套书籍：http://nlp.hankcs.com/book.php
# 讨论答疑：https://bbs.hankcs.com/

from pyhanlp import *
from typing import Dict, Any, List, Tuple, Union

from nlp.commom.tool import load_dictionary, trie_evaluate_speed


class DoubleArrayTrie:

    __name__ = 'DoubleArrayTrie'

    def __init__(self, dic: dict) -> None:
        m = JClass('java.util.TreeMap')()
        for k, v in dic.items():
            m[k] = v
        DoubleArrayTrie = JClass('com.hankcs.hanlp.collection.trie.DoubleArrayTrie')
        self.dat = DoubleArrayTrie(m)
        self.base = list(self.dat.getBase())
        self.check = list(self.dat.getCheck())
        self.value = list(self.dat.getValueArray(['']))

    @staticmethod
    def char_hash(c) -> int:
        return JClass('java.lang.Character')(c).hashCode()

    def transition(self, c, b) -> int:
        """
        状态转移
        :param c: 字符
        :param b: 初始状态
        :return: 转移后的状态，-1表示失败
        """
        p = self.base[b] + self.char_hash(c) + 1
        if self.base[b] == self.check[p]:
            return p
        else:
            return -1

    def __getitem__(self, key: str):
        b = 0
        for i in range(0, len(key)):  # len(key)次状态转移
            p = self.transition(key[i], b)
            if p is not -1:
                b = p
            else:
                return None

        p = self.base[b]  # 按字符'\0'进行状态转移
        n = self.base[p]  # 查询base
        if p == self.check[p] and n < 0:  # 状态转移成功且对应词语结尾
            index = -n - 1  # 取得字典序
            return self.value[index]
        return None

    def parse_longest(self, text: str) -> List[Tuple[str, Any, int, int]]:
        """
        最大正向匹配
        :param text:
        :return:
        """
        found = []
        searcher = LongestSearcher(text, 0, self.base, self.check, self.value)
        while searcher.next():
            start = searcher.begin
            end = searcher.begin + searcher.length
            found.append((text[start: end], searcher.value, start, end-1))
        return found


class LongestSearcher:
    """
    一个最长搜索工具（注意，当调用next()返回false后不应该继续调用next()，除非reset状态）
    """
    def __init__(self, text: str, offset: int, base, check, values):
        """
        :param text: 文本
        :param offset: 起始下标
        """
        self.begin = offset  # key的起点
        self.length = None  # key的长度
        self.index = None  # key的字典序坐标
        self.value = None # key对应的值
        self.text = text  # 字符串

        self._i = offset  # 上一个字符的下标
        self._text_length = len(text)  # 传入传的长度

        self._base = base
        self._check = check
        self._values = values

    def next(self):
        """
        取出下一个命中输出
        :return: 是否命中，当返回false表示搜索结束，否则使用公开的成员读取命中的详细信息
        """
        self.value = None
        self.begin = self._i
        b = self._base[0]
        n = None
        p = None
        while True:
            if self._i >= self._text_length:  # 指针到头了，将起点往前挪一个，重新开始，状态归零
                return self.value is not None
            p = b + ord(self.text[self._i]) + 1  # 状态转移 p = base[char[i-1]] + char[i] + 1
            if b == self._check[p]:          # base[char[i-1]] == check[base[char[i-1]] + char[i] + 1]
                b = self._base[p]            # 转移成功
            else:
                if self.begin == self._text_length:
                    break
                if self.value is not None:
                    self._i = self.begin + self.length  # // 输出最长词后，从该词语的下一个位置恢复扫描
                    return True
                self._i = self.begin
                self.begin += 1
                b = self._base[0]
            p = b
            n = self._base[p]
            if b == self._check[p] and n < 0:
                self.length = self._i - self.begin + 1
                self.index = -n - 1
                self.value = self._values[self.index]
            self._i += 1
        return False


if __name__ == '__main__':
    dic = {'自然': 'nature', '自然人': 'human', '自然语言': 'language', '自语': 'talk	to oneself', '入门': 'introduction'}
    dat = DoubleArrayTrie(dic)
    assert dat['自然'] == 'nature'
    assert dat['自然语言'] == 'language'
    assert dat['不存在'] is None
    assert dat['自然\0在'] is None

    # 分词速度评测
    dic = load_dictionary()
    trie = DoubleArrayTrie({key: key for key in dic})
    text = '江西鄱阳湖干枯，中国最大淡水湖变成大草原'
    print('最长匹配:', trie.parse_longest(text))
    print('----' * 50)
    print('分词速度评估')
    trie_evaluate_speed(trie, text)

