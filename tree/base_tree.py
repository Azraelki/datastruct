import abc


class Node:
    """
    节点对象
        value:值
        prev:前驱节点
        next:后继节点
    """
    def __init__(self, value):
        """
        创建节点
        :param value:
        """
        self.value = value
        self.prev = None
        self.next = None
        self.left = None
        self.right = None

    def __str__(self):
        return self.value


class IntNode(Node):
    """
    int类型节点对象
        value:值
        prev:前驱节点
        next:后继节点
    """
    def __init__(self, value: int):
        super(IntNode, self).__init__(value)

    def __str__(self):
        return str(self.value)


class Tree:
    """
    树的基类
    """
    def __init__(self):
        self._root = Node()
        pass

    def insert(self, value):
        """
        插入一个值
        :param value: 值
        """
        self._insert(value)

    def search(self, value):
        """
        查询一个节点
        :param value:值
        :return: Node对象
        """
        return self._search(value)

    def delete(self, value):
        """
        查询一个节点
        :param value:值
        :return: Node对象
        """
        return self._delete(value)

    def pre_order(self):
        """
        先序遍历
        :return: Node对象列表
        """
        pass

    def mid_order(self):
        """
        中序遍历
        :return: Node对象列表
        """
        result = []
        current = self._root.next
        return self._mid_order(current, result)


    def follow_order(self):
        """
        后续遍历
        :return: Node对象列表
        """
        pass

    @abc.abstractmethod
    def _insert(self, value):
        """
        插入一个值
        :param value: 值
        :return: value
        """
        pass

    @abc.abstractmethod
    def _search(self, value):
        """
        查询一个节点
        :param value:值
        :return: value
        """
        pass

    @abc.abstractmethod
    def _delete(self, value):
        """
        查询一个节点
        :param value:值
        :return: value
        """
        pass

    def _mid_order(self, node, result):
        if node:
            self._mid_order(node.left, result)
            result.append(node.value)
            self._mid_order(node.right, result)
        return result

    def find_right_last_node(self, node):
        """
        寻找节点的最右子节点
        :param node:
        :return:
        """
        assert isinstance(node, IntNode)
        while node.right:
            node = node.right
        return node

    def find_left_last_node(self, node):
        """
        寻找节点的最左子节点
        :param node:
        :return:
        """
        assert isinstance(node, IntNode)
        while node.left:
            node = node.left
        return node
