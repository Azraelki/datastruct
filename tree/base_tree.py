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
        self.height = 1



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

    def right_rotate(self, node):
        """
        右旋
        :param node: 不平衡节点
        """
        assert isinstance(node, Node)
        left = node.left
        right = left.right
        # 右旋
        left.right = node
        node.left = right

        # 更新变动的两个节点的高度
        node.height = max(self.height(node.left), self.height(node.right)) + 1
        left.height = max(self.height(left.left), self.height(left.right)) + 1
        # 返回旋转后的节点
        return left

    def left_rotate(self, node):
        """
        左旋
        :param node: 不平衡节点
        """
        assert isinstance(node, Node)
        right = node.right
        left = right.left
        # 左
        right.left = node
        node.right = left

        # 更新变动的两个节点的高度
        node.height = max(self.height(node.left), self.height(node.right)) + 1
        right.height = max(self.height(right.left), self.height(right.right)) + 1
        # 返回旋转后的节点
        return right

    def height(self, node):
        """
        获取数数的高度
        :param node:
        :return:
        """
        if node:
            return node.height
        else:
            return 0

    def balance_factor(self, node):
        """
        获取平衡因子
        :param node:
        :return:
        """
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)


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

    def remove_prev_node(self, node):
        """
        删除前驱节点
        :param node:
        :return:
        """
        if node.left is None:
            return
        node = node.left
        while node.right and node.right.right:
            node = node.right
        node.right = None

    def remove_after_node(self, node):
        """
        删除后继节点
        :param node:
        :return:
        """
        if node.right is None:
            return
        node = node.right
        while node.left and node.left.left:
            node = node.left
        node.left = None








