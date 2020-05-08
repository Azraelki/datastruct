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
        self.value = value
        self.prev = None
        self.next = None


class Tree:
    """
    树的基类
    """
    def __init__(self, root):
        self._root = root
        pass

    def insert(self, value):
        """
        插入一个值
        :param value: 值
        """
        self.__insert(value)

    def search(self, value):
        """
        查询一个节点
        :param value:值
        :return: Node对象
        """
        return self.__search(value)

    def delete(self, value):
        """
        查询一个节点
        :param value:值
        :return: Node对象
        """
        return self.__delete(value)

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
        pass

    def follow_order(self):
        """
        后续遍历
        :return: Node对象列表
        """
        pass

    @abc.abstractmethod
    def __insert(self, value):
        """
        插入一个值
        :param value: 值
        :return: value
        """
        pass

    @abc.abstractmethod
    def __search(self, value):
        """
        查询一个节点
        :param value:值
        :return: value
        """
        pass

    @abc.abstractmethod
    def __delete(self, value):
        """
        查询一个节点
        :param value:值
        :return: value
        """
        pass
