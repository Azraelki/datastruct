from tree.base_tree import Tree, IntNode
import time

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
        1、删除节点为叶子节点
        2、删除节点有一个子节点
        3、删除节点有两个子节点
        递归更新树的高度，并维持新的平衡
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
                # 获取删除节点的平衡因子
                factor = self.balance_factor(node)
                # 当左子树的高度大于右子树时,将当前节点的前驱节点作为新的节点返回，否则将当前节点的后继节点返回
                if factor >= 0:
                    pre_node = self.find_right_last_node(node)
                    self.remove_prev_node(node)
                    node.value = pre_node.value
                    return node
                else:
                    after_node = self.find_left_last_node(node)
                    self.remove_after_node(node)
                    node.value = after_node.value
                    return node
            elif node.left:
                return node.left
            else:
                return node.right

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



if __name__ == '__main__':
    binary_tree = AverageBinaryTree()
    nums = [1, 2, 3, 4, 5, 6]
    start = time.time()
    for num in range(1, 10001):
        binary_tree.insert(num)
    print(time.time() - start)
    start = time.time()
    for num in range(1, 1001):
        binary_tree.delete(num)
    print(time.time() - start)
    mid = binary_tree.mid_order()
    print(mid)
    for num in range(1, 9001):
        if mid[num - 1].value != 1000 + num:
            print('错误数据：' + str(num))



