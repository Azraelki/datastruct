from tree.base_tree import Tree, IntNode


class AverageBinaryTree(Tree):
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
        self._root = self.__put(self._root, value)

    def __put(self, node, new_value):
        """

        :param node:
        :param new_node:
        :return: 新的根节点
        """
        # 先将新值插入
        if node is None:
            return IntNode(new_value)
        if node.value > new_value:
            node.left = self.__put(node.left, new_value)
        elif node.value < new_value:
            node.right = self.__put(node.right, new_value)
        else:
            node.value = new_value

        # 更新高度
        node.height = max(self.height(node.left), self.height(node.right)) + 1
        # 平衡因子
        factor = self.balance_factor(node)

        # 判定是否需要右旋
        if factor > 1 and self.balance_factor(node.left) >= 0:
            return self.right_rotate(node)
        # 判定是否需要左旋+右旋
        if factor > 1 and self.balance_factor(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # 判定是否需要左旋
        if factor < -1 and self.balance_factor(node.right) <= 0:
            return self.left_rotate(node)
        # 判定是否需要右旋+左旋
        if factor < -1 and self.balance_factor(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node


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
    binary_tree = AverageBinaryTree()
    nums = [1, 2, 3, 4, 5, 6]
    for num in nums:
        binary_tree.insert(num)
    print(binary_tree.height(binary_tree.search(8)))
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

