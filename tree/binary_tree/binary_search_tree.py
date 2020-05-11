from tree.base_tree import Tree, IntNode


class BinaryTree(Tree):
    """
    二叉搜索树
    """
    def __init__(self):
        self._root = None

    def _insert(self, value: int):
        """
        插入一个值
        :param value: 值
        :return: value
        """
        if not self._root:
            self._root = IntNode(value)
            return
        current = self._root
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

    def _search(self, value: int):
        """
        查询一个节点
        :param value:值
        :return: value
        """
        current = self._root
        while current:
            if current.value == value:
                return current
            if current.value > value:
                current = current.left
            else:
                current = current.right
        return None

    def _delete(self, value: int):
        """
        删除一个节点
        1、找到指定节点
        2、找到节点的前驱节点
        3、断开前驱节点和父节点的联系，并将前驱节点的左子树作为其父节点的右子树
        4、将前驱节点的左子树指向删除节点的左子树
        5、将前驱节点的右子树指向删除节点的右子树
        6、建立前驱节点和删除节点父节点的关系
        7、返回指定节点
        :param value:值
        :return: value
        """
        current = self._root
        parent = None
        is_left = True
        if not current:
            return None
        while current:
            if current.value == value:
                if current.left and current.right:
                    # 寻找前驱节点
                    prev = self.find_right_last_node(current)
                    if current.left == prev:
                        # 当前驱节点是删除节点的左节点时，直接将删除节点右子树作为前驱节点的右子树
                        prev.right = current.right
                    else:
                        # 断开前驱节点和父节点的联系，并将前驱节点的左子树作为其父节点的右子树
                        self.remove_prev_node(current)
                        prev.left = current.left
                        prev.right = current.right
                    if parent:
                        if is_left:
                            parent.left = prev
                        else:
                            parent.right = prev
                    else:
                        # 当为跟节点时，直接将跟节点指向前驱节点
                        self._root = prev
                elif current.left:
                    # 只有左子树
                    if parent:
                        if is_left:
                            parent.left = current.left
                        else:
                            parent.right = current.left
                    else:
                        self._root = current.left
                else:
                    # 只有右子树
                    if parent:
                        if is_left:
                            parent.left = current.right
                        else:
                            parent.right = current.right
                    else:
                        self._root = current.right
                return current
            if current.value > value:
                parent = current
                current = current.left
                is_left = True
            else:
                parent = current
                current = current.right
                is_left = False
        return None




if __name__ == '__main__':
    binary_tree = BinaryTree()
    nums = [13, 9, 6, 11, 10,  5, 7, 15, 16, 14]
    for num in nums:
        binary_tree.insert(num)
    print(binary_tree.mid_order())
    print(binary_tree.search(4))
    print(binary_tree.delete(13))
    print(binary_tree.mid_order())
    print(binary_tree.delete(9))
    print(binary_tree.mid_order())
    print(binary_tree.delete(16))
    print(binary_tree.mid_order())
    print(binary_tree.delete(7))
    print(binary_tree.mid_order())
    print(binary_tree.delete(5))
    print(binary_tree.mid_order())
    print(binary_tree.delete(6))
    print(binary_tree.mid_order())
    print(binary_tree.delete(11))
    print(binary_tree.mid_order())
    print(binary_tree.delete(10))
    print(binary_tree.mid_order())
    print(binary_tree.delete(14))
    print(binary_tree.mid_order())
    print(binary_tree.delete(15))
    print(binary_tree.mid_order())


