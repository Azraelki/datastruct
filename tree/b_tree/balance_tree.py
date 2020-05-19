from tree.base_tree import Tree, BNode, Node
import time
import random
import tqdm
import math

class BalanceTree(Tree):
    """
    红黑树
    """
    def __init__(self, m=5):
        """
        :param m: 阶数
        """
        self._m = m
        self._root = None

    def _insert(self, value: int):
        """
        插入一个值
        :param value: 值
        :return: value
        """
        self._root = self.__put(self._root, value)
        # 当根节点阶数满时进行拆分
        if len(self._root.values) >= self._m and len(self._root.values)>2:
            self._split(None, self._root)

    def __put(self, node, new_value):
        """
        放置一个新的节点
        :param node:
        :param new_node:
        :return: 新的根节点
        """
        if not node:
            return BNode(new_value)
        # 遍历节点值
        for k, v in enumerate(node.values):
            # 如果当前节点为叶子节点，则直接添加
            if node.is_leaf():
                # 当叶子节点不包含当前值时添加进去
                if new_value not in node.values:
                    node.add_val(new_value)
                break
            else:
                # 当为非叶子节点且当前值小于遍历值时，向下递归
                if new_value < v:
                    node.childs[k] = self.__put(node.childs[k], new_value)
                    break
                # 当前值和插入值一样时不做操作
                elif new_value == v:
                    break
        else:
            # 此时满足新插入的值大于当前节点中所有的值且当前节点不是叶子节点，此时直接递归put当前节点的最大子节点
            node.childs[-1] = self.__put(node.childs[-1], new_value)

        # 1、判定当前节点是否任一节点因为插入导致出现了满阶的情况，如果出现则进行拆分节点
        for k, child in enumerate(node.childs):
            if len(child.values) >= self._m:
                self._split(node, child)
        return node

    def _split(self, parent, child):
        """
        拆分节点
        :param parent: 父节点
        :param child: 当前拆分节点
        :return:
        """
        # 寻找中间节点
        mid = len(child.values) // 2
        current_value = child.values[mid]
        # 生成兄弟节点，此处为后继节点
        right = BNode()
        # 拆分值
        for k, v in enumerate(child.values[mid+1:]):
            right.add_val(v)
        # 拆分子节点
        for k, c in enumerate(child.childs[mid+1:]):
            right.add_child(c)
        child.values = child.values[:mid]
        child.childs = child.childs[:mid+1]

        # 中间值的上升
        if parent:
            parent.add_val(current_value)
            parent.add_child(right)
        else:
            # 当传入的parent为空时说明传入的是根节点
            self._root = BNode()
            self._root.add_val(current_value)
            self._root.add_child(child)
            self._root.add_child(right)

    def _search(self, value: int):
        """
        查询一个节点
        :param value:值
        :return: value
        """
        current = self._root
        while current:
            for k, v in enumerate(current.values):
                if value == v:
                    return v
                if value < v:
                    if not current.is_leaf():
                        current = current.childs[k]
                    else:
                        current = None
                    break
            else:
                if not current.is_leaf():
                    current = current.childs[-1]
                else:
                    current = None
        return None

    def _mid_order(self, node, result):
        """B树中序遍历"""
        if node:
            for k, v in enumerate(node.values):
                if not node.is_leaf():
                    result = self._mid_order(node.childs[k], result)
                result.append(v)
            else:
                if not node.is_leaf():
                    result = self._mid_order(node.childs[-1], result)
        return result

    def _delete(self, value: int):
        """
        删除一个节点
        :param value:值
        :return: value
        """
        self._root = self.__delete_node(self._root, value)
        if not self._root.values and self._root.childs:
            self._root = self._root.childs[0]

    def __delete_node(self, node, value):
        """
        递归删除一个节点
        :param node: 当前节点
        :param value: 删除的值
        :return:
        """
        if not node:
            return None
        # 遍历节点值
        for k, v in enumerate(node.values):
            # 当前节点为叶子节点且值命中时直接删除掉
            if node.is_leaf():
                if value == v:
                    del node.values[k]
                    break
            else:
                if value == v:
                    # 寻找当前节点的后继节点, 并把节点的第一个值赋值到当前节点
                    # print('当前值数量：{},孩子节点数量：{}'.format(len(node.values), len(node.childs)))
                    # print('当前node：{},孩子节点数量：{}'.format(node.values, node.childs))
                    after_node = self.get_after_node(node.childs[k+1])
                    node.values[k] = after_node.values[0]
                    # 将当前后继节点的值替换为当前节点，然后以当前节点的兄弟节点为删除节点开始重新开始递归
                    node.childs[k + 1] = self.__delete_node(node.childs[k+1], after_node.values[0])
                    break
                elif value < v:
                    node.childs[k] = self.__delete_node(node.childs[k], value)
                    break
        else:
            # 当前节点为叶子节点时放弃继续删除，说明在树中不存在
            if not node.is_leaf():
                node.childs[-1] = self.__delete_node(node.childs[-1], value)

        # 1、判定当前节点是否因删除节点导致节点阶数小于限制的阶数,若小于则触发修复动作
        # print('修复前：当前node：{},孩子节点数量：{}'.format(node.values, node.childs))
        for k, child in enumerate(node.childs):
            if len(child.values) < math.ceil(self._m/2)-1:
                self._fill_node(node, child, k)
        # print('修复后：当前node：{},孩子节点数量：{}'.format(node.values, node.childs))
        return node

    def _fill_node(self, parent, child, k):
        """
        修复节点失衡
        :param parent: 父节点
        :param child: 孩子节点
        :param k: 孩子节点所在的下标
        :return:
        """
        # 当前child是parent最后一个孩子时向前找，否则向后找
        if len(parent.childs) > k+1:
            brother = parent.childs[k+1]
            # 当兄弟节点的阶数大于限制阶数时，从兄弟节点借一个作为新的父节点，老的父节点下沉到失衡的节点
            if len(brother.values) > math.ceil(self._m/2) - 1:
                child.add_val(parent.values[k])
                parent.values[k] = brother.values[0]
                if not brother.is_leaf():
                    child.add_child(brother.childs[0])
                    del brother.childs[0]
                del brother.values[0]
            else:
                # 当兄弟节点的阶数小于或等于阶数时，合并两个兄弟节点和父节点
                for v in child.values:
                    brother.add_val(v)
                for c in child.childs:
                    brother.add_child(c)
                # 添加父节点值
                brother.add_val(parent.values[k])
                del parent.values[k]
                del parent.childs[k]
        else:
            brother = parent.childs[k-1]
            # 当兄弟节点的阶数大于最小限制阶数时，从兄弟节点借一个作为新的父节点，老的父节点下沉到失衡的节点
            if len(brother.values) > math.ceil(self._m/2) - 1:
                child.add_val(parent.values[-1])
                parent.values[-1] = brother.values[-1]
                if not brother.is_leaf():
                    child.add_child(brother.childs[-1])
                    del brother.childs[-1]
                del brother.values[-1]
            else:
                # 当兄弟节点的阶数小于或等于阶数时，合并两个兄弟节点和父节点
                # 注意：从兄弟借一个节点的前提为兄弟为叶子节点
                for v in child.values:
                    brother.add_val(v)
                for c in child.childs:
                    brother.add_child(c)
                # 添加父节点值
                brother.add_val(parent.values[-1])
                del parent.values[-1]
                del parent.childs[k]


    def get_after_node(self, node):
        """返回后继节点节点"""
        assert isinstance(node, Node)
        while not node.is_leaf():
            node = node.childs[0]
        return node


if __name__ == '__main__':
    binary_tree = BalanceTree(m=3)
    nums = [1, 2, 3, 4, 5, 6]
    start = time.time()
    result = [num for num in range(1, 10001)]
    random.seed(1)
    while result:
        num = random.choice(result)
        binary_tree.insert(num)
        result.remove(num)
    print(time.time()-start)
    start = time.time()
    print(binary_tree.search(100))
    # for num in range(100, 1001):
    #     binary_tree.delete(num)
    print(time.time()-start)
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
