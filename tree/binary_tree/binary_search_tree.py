from tree.base_tree import Tree, IntNode


class BinaryTree(Tree):
    """
    二叉搜索树
    """
    def __init__(self):
        self._root = IntNode(None)

    def _insert(self, value: int):
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

    def _search(self, value: int):
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

    def _delete(self, value: int):
        """
        查询一个节点
        1、删除节点为根节点
            1）、左右子树都不为空
            1）、左子树不为空
            2）、右子树不为空
        2、删除节点为非根节点
            1）、删除节点是父节点的左子树
                1）、左右子树都不为空
                1）、左子树不为空
                2）、右子树不为空
            2）、删除节点是父节点的右子树
                1）、左右子树都不为空
                1）、左子树不为空
                2）、右子树不为空

        :param value:值
        :return: value
        """
        prev = self._root
        current = self._root.next
        is_left = None
        while current:
            if current.value == value:
                if is_left is None:
                    # 当删除节点为根节点时，且有左子树时
                    if current.left:
                        # 找到左子树的最右子节点，将当前节点的右子树作为最右子节点的右节点
                        self.find_right_last_node(current.left).right = current.right
                        # 将根节点设置为当前节点的左节点
                        prev.next = current.left
                    else:
                        # 当无左子树时直接将跟节点设置为当前节点的右节点
                        prev.next = current.right
                elif is_left:
                    # 当前节点为父节点的左子树，且左右子节点不为空时
                    if current.left and current.right:
                        # 找到左子树的最右子节点，将当前节点的右子树作为最右子节点的右节点
                        self.find_right_last_node(current.left).right = current.right
                        # 将父节点左子树设置为当前节点的左节点
                        prev.left = current.left
                    elif current.left:
                        # 当只有左子树时，直接将当前节点的左子树设置为父节点的左子树
                        prev.left = current.left
                    elif current.right:
                        # 当只有右子树时，直接将当前节点的右子树设置为父节点的左子树
                        prev.left = current.right
                    else:
                        prev.left = None
                else:
                    # 当前节点为父节点的右子树，且左右子节点不为空时
                    if current.left and current.right:
                        # 找到左子树的最右子节点，将当前节点的右子树作为最右子节点的右节点
                        self.find_right_last_node(current.left).right = current.right
                        # 将父节点右子树设置为当前节点的左节点
                        prev.right = current.left
                    elif current.left:
                        # 当只有左子树时，直接将当前节点的左子树设置为父节点的右子树
                        prev.right = current.left
                    elif current.right:
                        # 当只有右子树时，直接将当前节点的右子树设置为父节点的右子树
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




if __name__ == '__main__':
    binary_tree = BinaryTree()
    nums = [8, 5, 3, 2, 4, 12, 9]
    for num in nums:
        binary_tree.insert(num)
    print(binary_tree.mid_order())
    print(binary_tree.search(4))
    print(binary_tree.delete(12))
    print(binary_tree.mid_order())
    print(binary_tree.delete(8))
    print(binary_tree.mid_order())
    print(binary_tree.delete(2))
    print(binary_tree.mid_order())
    print(binary_tree.delete(3))
    print(binary_tree.mid_order())
    print(binary_tree.delete(4))
    print(binary_tree.mid_order())
    print(binary_tree.delete(5))
    print(binary_tree.mid_order())
    print(binary_tree.delete(9))
    print(binary_tree.mid_order())
