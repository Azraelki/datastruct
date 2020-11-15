# -*- coding:utf-8 -*-
# Author：hankcs
# Date: 2018-05-26 21:16
# 《自然语言处理入门》2.5 双数组字典树
# 配套书籍：http://nlp.hankcs.com/book.php
# 讨论答疑：https://bbs.hankcs.com/

from pyhanlp import *
from typing import Dict, Any, List, Tuple, Union

from nlp.commom.tool import load_dictionary, trie_evaluate_speed


class ACDoubleArrayTrie:

    __name__ = 'ACDoubleArrayTrie'

    def __init__(self, dic: dict) -> None:
        self.segment = JClass('com.hankcs.hanlp.seg.Other.AhoCorasickDoubleArrayTrieSegment')(HanLP.Config.CoreDictionaryPath)

    def parse_longest(self, text: str) -> List[Tuple[str, Any, int, int]]:
        """
        最大正向匹配
        :param text:
        :return:
        """
        found = []
        for term in self.segment.seg(text):
            start = term.offset
            end = start + len(term.word) - 1
            found.append((term.word, None, start, end))
        return found


if __name__ == '__main__':
    # 分词速度评测
    dic = load_dictionary()
    trie = ACDoubleArrayTrie({key: key for key in dic})
    text = '江西鄱阳湖干枯，中国最大淡水湖变成大草原'
    print('最长匹配:', trie.parse_longest(text))
    print('----' * 50)
    print('分词速度评估(內部调用java次数太多，速度很慢)')
    trie_evaluate_speed(trie, text)

