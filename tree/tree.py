import abc


class Node:
    """
    节点对象
        value:值
        prev:前驱节点
        next:后继节点
    """
    def __init__(self, value: int):
        """
        创建节点
        :param value:
        """
        assert isinstance(value, int)
        self.value = value
        self.prev = None
        self.next = None

    def __str__(self):
        return self.value


class Tree:
    """
    树的基类
    """
    def __init__(self):
        pass

    @abc.abstractmethod
    def insert(self, node: Node):
        """
        插入一个节点
        :param node: 节点对象
        :return: int值
        """
        pass

    @abc.abstractmethod
    def search(self, value):
        """
        查询一个节点
        :param value:值
        :return: Node对象
        """
        pass

    @abc.abstractmethod
    def delete(self, value):
        """
        查询一个节点
        :param value:值
        :return: Node对象
        """
        pass

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
