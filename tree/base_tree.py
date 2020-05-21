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
        self.parent = None
        self.height = 1
        self.is_red = True


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


class TrieNode(Node):
    """
    字典树类型节点对象
    nodes:子节点列表
    count:经过当前节点的单词数量
    word_count:词频
    is_end:当前节点是否为结束节点(单词结束)
    char:当前节点的字符
    """
    def __init__(self, char):
        self.nodes = [None for x in range(27)]
        self.count = 0
        self.is_end = False
        self.word_count = 0
        if char:
            self.char = char
        else:
            self.char = None

    def __str__(self):
        return str(self.char)

    def __repr__(self):
        return str(self.char)


class BNode(Node):
    """
    int类型节点对象
        value:值
        prev:前驱节点
        next:后继节点
    """
    def __init__(self, value: int=None):
        self.parent = None
        self.values = []
        self.childs = []
        self.left = None
        self.right = None
        if value:
            self.add_val(value)

    def is_leaf(self):
        """判定是否为空节点"""
        if self.childs:
            return False
        return True

    def add_val(self, value: int):
        """添加一个值"""
        self.values.append(value)
        self.values = sorted(self.values)

    def add_child(self, node: Node):
        """添加一个子节点"""
        self.childs.append(node)
        self.childs = sorted(self.childs, key=lambda n: n.values[0])

    def del_value(self, value):
        """删除一个值，并返回他的下标"""
        for k, v in enumerate(self.values):
            if value == v:
                del self.values[k]
                return k
        return None

    def find_value(self, value):
        """查找一个值"""
        for k, v in enumerate(self.values):
            if v == value:
                return k, v
        return None, None

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return str(self.values)


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
        # 当父节点为空时说明节点的前驱节点就是自己的左孩子
        if parent:
            parent.right = current.left
        else:
            node.left = current.left

    def remove_after_node(self, node):
        """
        将当前节点的前驱节点和其父节点断开
        :param node:
        :return:
        """
        assert isinstance(node, Node)
        current = node.right
        parent = None
        while current.left:
            parent = current
            current = current.left
        # 当父节点为空时说明节点的前驱节点就是自己的右孩子
        if parent:
            parent.left = current.right
        else:
            node.right = current.right








