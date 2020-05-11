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

    def __repr__(self):
        return str(self.value)


class Tree:
    """
    树的基类
    """
    def __init__(self):
        self._root = None
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
        return self._mid_order(self._root, result)


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
            result.append(node)
            self._mid_order(node.right, result)
        return result

    def find_right_last_node(self, node):
        """
        寻找节点的前驱节点
        :param node:
        :return:
        """
        assert isinstance(node, Node)
        node = node.left
        while node.right:
            node = node.right
        return node

    def find_left_last_node(self, node):
        """
        寻找节点的后继节点
        :param node:
        :return:
        """
        assert isinstance(node, Node)
        node = node.right
        while node.left:
            node = node.left
        return node

    def left_rotate(self, node):
        """
        左旋
        :param node: 不平衡节点
        """
        assert isinstance(node, Node)

    def remove_prev_node(self, node):
        """
        将当前节点的前驱节点和其父节点断开
        :param node:
        :return:
        """
        assert isinstance(node, Node)
        current = node.left
        parent = None
        while current.right:
            parent = current
            current = current.right
        # 当前驱节点不是传入节点的左节点时，将前驱节点的左子树作为父节点的右子树
        if current != node.left:
            parent.right = current.left








