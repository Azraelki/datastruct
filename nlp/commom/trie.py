# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2020-01-04 23:46
from typing import Dict, Any, List, Tuple, Union
from nlp.commom.tool import load_dictionary, trie_evaluate_speed


class Node(object):
    """
    节点
    """
    def __init__(self, value=None) -> None:
        self._children = {}
        self._value = value

    def _add_child(self, char, value, overwrite=False):
        """
        添加子节点
        :param char: 子节点字符
        :param value: 子节点值
        :param overwrite: 若已存在，是否覆盖子节点值
        :return: 子节点对象
        """
        child: Node = self._children.get(char)
        if child is None:
            child = Node(value)
            self._children[char] = child
        elif overwrite:
            child._value = value
        return child

    def transit(self, key):
        """
        转移
        :param key: 转移字符
        :return:
        """
        state: Node = self
        for char in key:
            state = state._children.get(char)
            if state is None:
                break
        return state


class Trie(Node):
    """
    字典树
    """
    __name__ = 'Trie'

    def __init__(self, dic: dict):
        super(Trie, self).__init__()
        self.update(dic)

    def __contains__(self, key):
        return self[key] is not None

    def __getitem__(self, key):
        state = self.transit(key)
        if state is None:
            return None
        return state._value

    def __setitem__(self, key, value):
        state = self
        for i, char in enumerate(key):
            if i < len(key) - 1:
                state = state._add_child(char, None, False)
            else:
                state = state._add_child(char, value, True)

    def __delitem__(self, key):
        state = self.transit(key)
        if state is not None:
            state._value = None

    def update(self, dic: Dict[str, Any]):
        """
        更新字典树
        :param dic: 字典
        :return:
        """
        for k, v in dic.items():
            self[k] = v
        return self

    def parse_longest(self, text: str) -> List[Tuple[str, Any, int, int]]:
        """
        最大正向匹配
        :param text:
        :return:
        """
        found = []
        length = len(text)
        i = 0
        while True:
            if i >= length:
                break
            state = self.transit(text[i])
            if state:
                to = i + 1
                end = to
                value = state._value
                for to in range(i + 1, length):
                    state = state.transit(text[to])
                    if not state:
                        break
                    if state._value is not None:
                        value = state._value
                        end = to + 1
                if value is not None:
                    found.append((text[i:end], value, i, end-1))
                    i = end - 1
            i += 1
        return found

    def parse_text(self, text: str) -> List[Tuple[str, Any, int, int]]:
        """
        全切分
        :param text: 文本
        :return:
        """
        found = []
        length = len(text)
        begin = 0
        state = self
        i = begin
        while True:
            if i >= length:
                break
            state = state.transit(text[i])
            if state:
                value = state._value
                if value is not None:
                    found.append((text[begin:i+1], value, begin, i))
            else:
                i = begin
                begin += 1
                state = self
            i += 1
        return found


class TrieDict:

    __name__ = 'TrieDict'

    def __init__(self, dic: dict):
        """
        :param dic: 词典
        """
        self.prefix_trie = Trie({key: key for key in dic})
        self.suffix_trie = Trie({key[::-1]: key for key in dic})

    def __contains__(self, key):
        return self.prefix_trie[key] is not None

    def __getitem__(self, key):
        return self.prefix_trie[key]

    def __setitem__(self, key, value):
        self.prefix_trie[key] = value
        self.suffix_trie[key[::-1]] = value

    def __delitem__(self, key):
        del self.prefix_trie[key]
        del self.suffix_trie[key[::-1]]

    def forward_parse_longest(self, text: str):
        return self.prefix_trie.parse_longest(text)

    def backward_parse_longest(self, text: str):
        founds = self.suffix_trie.parse_longest(text[::-1])
        founds = founds[::-1]
        length = len(text) - 1
        for index, found in enumerate(founds):
            founds[index] = (found[0], found[1], length-found[3], length-found[2])
        return founds

    def parse_longest(self, text: str):
        """
        此处使用逆向最长匹配
        :param text:
        :return:
        """
        return self.backward_parse_longest(text)


if __name__ == '__main__':
    trie = Trie({})
    # 增
    trie['自然'] = 'nature'
    trie['自然人'] = 'human'
    trie['自然语言'] = 'language'
    trie['自语'] = 'talk	to oneself'
    trie['入门'] = 'introduction'
    assert '自然' in trie
    # 删
    trie['自然'] = None
    assert '自然' not in trie
    # 改
    trie['自然语言'] = 'human language'
    assert trie['自然语言'] == 'human language'
    # 查
    assert trie['入门'] == 'introduction'

    # 分词速度评测
    dic = load_dictionary()
    trie = Trie({})
    trie.update({key: key for key in dic})
    text = '江西鄱阳湖干枯，中国最大淡水湖变成大草原'
    print('全切分:', trie.parse_text(text))
    print('最长匹配:', trie.parse_longest(text))
    print('----' * 50)
    print('分词速度评估')
    trie_evaluate_speed(trie, text)
