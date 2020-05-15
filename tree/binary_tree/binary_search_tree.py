from tree.base_tree import Tree, IntNode
import time

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
        self._root = self.__put(self._root, value)

    def __put(self, node, new_value):
        """
        放置一个新的节点
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
        self._root = self.__delete_node(self._root, value)

    def __delete_node(self, node, value):
        """
        递归删除一个节点
        :param node: 当前节点
        :param value: 删除的值
        :return:
        """
        if node is None:
            return None
        if node.value > value:
            node.left = self.__delete_node(node.left, value)
        elif node.value < value:
            node.right = self.__delete_node(node.right, value)
        elif node.value == value:
            if node.left and node.right:
                prev = self.find_right_last_node(node)
                self.remove_prev_node(node)
                node.value = prev.value
                return node
            elif node.left:
                return node.left
            else:
                return node.right


if __name__ == '__main__':
    binary_tree = BinaryTree()
    nums = [1, 2, 3, 4, 5, 6]
    start = time.time()
    for num in range(1, 1001):
        binary_tree.insert(num)
    print(time.time() - start)
    start = time.time()
    for num in range(1, 101):
        binary_tree.delete(num)
    print(time.time() - start)
    mid = binary_tree.mid_order()
    print(mid)
    for num in range(1, 901):
        if mid[num - 1].value != 100 + num:
            print('错误数据：' + str(num))


