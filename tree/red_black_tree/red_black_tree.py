from tree.base_tree import Tree, IntNode, Node
import time
import tqdm
import random

class AverageBinaryTree(Tree):
    """
    红黑树
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
        # 涂黑根节点
        self._root.is_red = False

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

        # 当前节点的左节点为红色，右节点为红色
        if self.is_red(node.left) and self.is_red(node.right):
            # 此时满足插入节点是祖父节点的左子树上，插入节点的父节点和叔叔节点为红色，祖父为黑色
            # 此时进行颜色翻转，并把当前节点(祖父节点)作为新的插入节点进行递归处理
            if self.is_red(node.left.left) or self.is_red(node.left.right):
                self.flip_color(node)
            # 此时满足插入节点是祖父节点的右子树上，插入节点的父节点和叔叔节点为红色，祖父为黑色
            # 此时进行颜色翻转，并把当前节点(祖父节点)作为新的插入节点进行递归处理
            if self.is_red(node.right.left) or self.is_red(node.right.right):
                self.flip_color(node)
        # 当前节点的左节点为红色，右节点为黑色
        if self.is_red(node.left) and not self.is_red(node.right):
            # 此时满足插入节点是祖父节点的左子树上，插入节点的父节点是红色，叔叔节点为黑色
            if self.is_red(node.left.right):
                # 如果插入节点为父节点的右子树，先左旋，旋转为插入节点为父节点的左节点
                node.left = self.left_rotate(node.left)
            if self.is_red(node.left.left):
                # 此时满足插入节点为父节点的左子树，将当前节点(祖父节点)进行右旋,父节点替换为当前节点
                node = self.right_rotate(node)
        # 当前节点右节点为红色，左节点为黑色
        if self.is_red(node.right) and not self.is_red(node.left):
            # 此时满足插入节点是祖父节点的右子树上，插入节点的父节点是红色，叔叔节点为黑色
            if self.is_red(node.right.left):
                # 如果插入节点为父节点的左子树，先右旋，旋转为插入节点为父节点的右节点
                node.right = self.right_rotate(node.right)
            if self.is_red(node.right.right):
                # 此时满足插入节点为父节点的右子树，将当前节点(祖父节点)进行左旋,父节点替换为当前节点
                node = self.left_rotate(node)
        return node

    def is_red(self, node):
        """
        判定是否为红色节点
        :param node:
        :return:
        """
        if node:
            return node.is_red
        return False

    def left_rotate(self, node):
        """红黑树的左旋"""
        right = node.right
        # 旋转
        node.right = right.left
        right.left = node
        # 变色
        node.is_red = True
        right.is_red = False
        # 更新高度
        node.height = max(self.height(node.left), self.height(node.right)) + 1
        right.height = max(self.height(right.left), self.height(right.right)) + 1
        return right

    def right_rotate(self, node):
        """红黑树右旋"""
        left = node.left
        # 旋转
        node.left = left.right
        left.right = node
        # 变色
        node.is_red = True
        left.is_red = False
        # 更新高度
        node.height = max(self.height(node.left), self.height(node.right)) + 1
        left.height = max(self.height(left.left), self.height(left.right)) + 1
        return left

    def flip_color(self, node):
        """变色"""
        node.is_red = True
        if node.left:
            node.left.is_red = False
        if node.right:
            node.right.is_red = False

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
                pre_node = self.find_right_last_node(node)
                self.remove_prev_node(node)
                node.value = pre_node.value
                return node
            elif node.left:
                return node.left
            else:
                return node.right

        # 当前节点的左节点为红色，右节点为红色
        if self.is_red(node.left) and self.is_red(node.right):
            # 此时满足插入节点是祖父节点的左子树上，插入节点的父节点和叔叔节点为红色，祖父为黑色
            # 此时进行颜色翻转，并把当前节点(祖父节点)作为新的插入节点进行递归处理
            if self.is_red(node.left.left) or self.is_red(node.left.right):
                self.flip_color(node)
            # 此时满足插入节点是祖父节点的右子树上，插入节点的父节点和叔叔节点为红色，祖父为黑色
            # 此时进行颜色翻转，并把当前节点(祖父节点)作为新的插入节点进行递归处理
            if self.is_red(node.right.left) or self.is_red(node.right.right):
                self.flip_color(node)
            # 当前节点的左节点为红色，右节点为黑色
        if self.is_red(node.left) and not self.is_red(node.right):
            # 此时满足插入节点是祖父节点的左子树上，插入节点的父节点是红色，叔叔节点为黑色
            if self.is_red(node.left.right):
                # 如果插入节点为父节点的右子树，先左旋，旋转为插入节点为父节点的左节点
                node.left = self.left_rotate(node.left)
            if self.is_red(node.left.left):
                # 此时满足插入节点为父节点的左子树，将当前节点(祖父节点)进行右旋,父节点替换为当前节点
                node = self.right_rotate(node)
            # 当前节点右节点为红色，左节点为黑色
        if self.is_red(node.right) and not self.is_red(node.left):
            # 此时满足插入节点是祖父节点的右子树上，插入节点的父节点是红色，叔叔节点为黑色
            if self.is_red(node.right.left):
                # 如果插入节点为父节点的左子树，先右旋，旋转为插入节点为父节点的右节点
                node.right = self.right_rotate(node.right)
            if self.is_red(node.right.right):
                # 此时满足插入节点为父节点的右子树，将当前节点(祖父节点)进行左旋,父节点替换为当前节点
                node = self.left_rotate(node)

        return node


    def remove_prev_node(self, node):
        """删除前驱节点"""
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
        # 将当前节点的左子树的颜色变为黑色,补充被删掉的黑色节点
        if current and not self.is_red(current):
            current.is_red = False








if __name__ == '__main__':
    binary_tree = AverageBinaryTree()
    nums = [1, 2, 3, 4, 5, 6]
    start = time.time()
    result = [num for num in range(1, 10001)]
    random.seed(1)
    while result:
        num = random.choice(result)
        binary_tree.insert(num)
        result.remove(num)
    print(time.time() - start)
    start = time.time()
    print(binary_tree.search(100))
    # for num in range(100, 1001):
    #     binary_tree.delete(num)
    print(time.time() - start)
    mid = binary_tree.mid_order()
    print(mid)
    result = [num for num in range(1, 10001)]
    random.seed(1)
    bar = tqdm.trange(len(mid))
    while result:
        num = random.choice(result)
        binary_tree.delete(num)
        result.remove(num)
        # print(num)
        # print(binary_tree.mid_order())
        bar.update()
    bar.close()
    print('最终结果：', binary_tree.mid_order())

