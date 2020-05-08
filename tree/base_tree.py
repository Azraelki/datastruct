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
    def __init__(self, root: int):
        assert isinstance(root, int)
        self._root = root
        pass

    @abc.abstractmethod
    def insert(self, value: int):
        """
        插入一个值
        :param value: 值
        :return: int值
        """
        assert isinstance(value, int)
        pass

    @abc.abstractmethod
    def search(self, value:int):
        """
        查询一个节点
        :param value:值
        :return: 值
        """
        assert isinstance(value, int)
        pass

    @abc.abstractmethod
    def delete(self, value:int):
        """
        查询一个节点
        :param value:值
        :return: 值
        """
        assert isinstance(value, int)
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
