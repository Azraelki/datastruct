from tree.base_tree import Tree, IntNode


class BinaryTree(Tree):
    def __init__(self):
        self._root = IntNode(None)

    def __insert(self, value: int):
        """
        插入一个值
        :param value: 值
        :return: value
        """
        current = self._root.next
        if not current:
            self._root.next = IntNode(value)
            return
        while current:
            if current.value == value:
                return
            if current.value > value:
                if current.left:
                    current = current.left
                else:
                    current.left = IntNode(value)
                    return
            else:
                if current.right:
                    current = current.right
                else:
                    current.right = IntNode(value)
                    return

    def __search(self, value: int):
        """
        查询一个节点
        :param value:值
        :return: value
        """
        current = self._root.next
        while current:
            if current.value == value:
                return current
            if current.value > value:
                current = current.left
            else:
                current = current.right
        return None

    def __delete(self, value: int):
        """
        查询一个节点
        :param value:值
        :return: value
        """
        prev = self._root
        current = self._root.next
        is_left = True
        while current:
            if current.value == value:
                if is_left:
                    if current.left and current.right:
                        self.find_right_last_node(current.left).right = current.right
                        prev.left = current.left
                    elif current.left:
                        prev.left = current.left
                    elif current.right:
                        prev.left = current.right
                    else:
                        prev.left = None
                else:
                    if current.left and current.right:
                        self.find_right_last_node(current.left).right = current.right
                        prev.right = current.left
                    elif current.left:
                        prev.right = current.left
                    elif current.right:
                        prev.right = current.right
                current.left = None
                current.right = None
                return current
            else:
                prev = current
                if current.value > value:
                    is_left = True
                    current = current.left
                else:
                    is_left = False
                    current = current.right
        return None

    def find_right_last_node(self, node):

        pass