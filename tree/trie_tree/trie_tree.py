from tree.base_tree import Tree, IntNode, TrieNode
import time


class TrieTree(Tree):
    """
    字典树
    """
    def __init__(self):
        self._root = TrieNode(None)
        self.chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
        self.char_to_index = {key: point for point, key in enumerate(self.chars)}
        self.index_to_char = {point: key for point, key in enumerate(self.chars)}

    def _insert(self, word: str):
        """
        插入单词
        :param word: 单词
        :return: value
        """
        self.__put(word)

    def __put(self, word):
        """
        放置一个新的节点
        :param word:单词
        :return: 新的根节点
        """
        current = self._root
        for char in word:
            point = self.char_to_index[char]
            if current.nodes[point]:
                # 经过的单词数量自增
                current.nodes[point].count += 1
                current = current.nodes[point]
            else:
                current.nodes[point] = TrieNode(char)
                current.nodes[point].count = 1
                current = current.nodes[point]
        current.is_end = True
        # 词频自增
        current.word_count += 1

    def _search(self, word: str):
        """
        查询一个单次是否出现过
        :param word:值
        :return: value
        """
        current = self._root
        for char in word:
            # 比较前判断当前节点是否为空
            if current:
                point = self.char_to_index[char]
                current = current.nodes[point]
            else:
                return False
        else:
            # 正常结束后，判定当前节点是否为单次结束节点
            if current and current.is_end:
                return True
        return False

    def count_word(self, word:str):
        """
        计算一个单词在字典中出现的次数
        :param word:
        :return:
        """
        current = self._root
        for char in word:
            # 比较前判断当前节点是否为空
            if current:
                point = self.char_to_index[char]
                current = current.nodes[point]
            else:
                return 0
        else:
            # 正常结束后，判定当前节点是否为单次结束节点
            if current.is_end:
                return current.word_count
        return 0

    def list_by_prefix(self, prefix):
        """
        根据前缀找到所有单词
        :param prefix: 前缀
        """
        current = self._root
        result = []
        for char in prefix:
            if current:
                point = self.char_to_index[char]
                current = current.nodes[point]
            else:
                return []
        else:
            # 正常结束代表找到了指定的前缀
            if current.is_end:
                result.append(prefix)
            self.list(current, prefix, result)
        return result

    def list(self, current, prefix, result):
        """
        从指定节点开始遍历，将单次加入到result中
        :param node: 开始节点
        :param prefix: 前缀
        :param result: 结果
        :return:
        """
        for node in current.nodes:
            if node:
                if node.is_end:
                    result.append(prefix + node.char)
                self.list(node, prefix + node.char, result)

    def forward_split_content(self, content):
        """
        分词,最大前向匹配
        :param content: 文本
        :return:
        """
        start_pointer = 0
        end_pointer = len(content)
        result = []
        while start_pointer < len(content):
            tem_content = content[start_pointer:end_pointer]
            if self.search(tem_content):
                result.append(tem_content)
                start_pointer = end_pointer
                end_pointer = len(content)
            else:
                end_pointer -= 1
            if end_pointer <= start_pointer:
                start_pointer += 1
                end_pointer = len(content)

        return result

    def backward_split_content(self, content):
        """
        分词,最大逆向向匹配
        :param content: 文本
        :return:
        """
        start_pointer = 0
        end_pointer = len(content)
        result = []
        while end_pointer >= 0:
            tem_content = content[start_pointer:end_pointer]
            if self.search(tem_content):
                result.append(tem_content)
                end_pointer = start_pointer
                start_pointer = 0
            else:
                start_pointer += 1
            if start_pointer >= end_pointer:
                start_pointer = 0
                end_pointer -= 1

        return result





if __name__ == '__main__':
    binary_tree = TrieTree()
    nums = [1, 2, 3, 4, 5, 6]
    start = time.time()
    for word in ['a', 'b', 'abc', 'abd', 'bcd', 'abcd', 'efg', 'hii', 'abc', 'bcd', 'bcd']:
        binary_tree.insert(word)
    print(time.time() - start)
    start = time.time()
    # 查找
    assert binary_tree.search('a') is True
    assert binary_tree.search('abd') is True
    assert binary_tree.search('ef') is False
    assert binary_tree.search('ii') is False
    # 统计词频
    assert binary_tree.count_word('abcd') == 1
    assert binary_tree.count_word('abc') == 2
    assert binary_tree.count_word('bcd') == 3
    assert binary_tree.count_word('ii') == 0
    # 获取以指定前缀开始的单词
    print(binary_tree.list_by_prefix('a'))
    print(binary_tree.list_by_prefix('b'))

    # 分词
    print(binary_tree.search('abc'))
    print('最大正向匹配：', binary_tree.forward_split_content('abc a abcd hiikh'))
    print('最大逆向匹配：', binary_tree.backward_split_content('abc a abcd hiikh'))
