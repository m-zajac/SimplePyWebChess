import sys


class StopIterationAfterNodeTraverse(StopIteration):
    pass


class StopIterationBeforeNodeTraverse(StopIteration):
    pass


class DepthFirstNode(object):
    """Generic node for depth-first tree traversal"""

    def __init__(self, data=None, value=None, alghoritm='preorder'):
        self.data = data
        self.nodes = []
        self.value = value
        self.evaluations = 0

        # choose traverse alghoritm
        if alghoritm == 'preorder':
            self.traverse = self.preorder
        else:
            self.traverse = self.postorder

    def addNode(self, node):
        self.nodes.append(node)
        return self

    def preorder(self, parent=None):
        self.evaluate()

        node = None
        try:
            for node in self.nodes:
                self.traverseNode(node)
                self.evaluations += node.evaluations
        except StopIterationBeforeNodeTraverse:
            pass
        except StopIterationAfterNodeTraverse:
            self.evaluations += node.evaluations

        return self

    def postorder(self, parent=None):
        node = None
        try:
            for node in self.nodes:
                self.traverseNode(node)
                self.evaluations += node.evaluations
        except StopIterationBeforeNodeTraverse:
            pass
        except StopIterationAfterNodeTraverse:
            self.evaluations += node.evaluations

        self.evaluate()

        return self

    def traverseNode(self, node):
        node.traverse(self)

    def evaluate(self):
        self.evaluations += 1

    def __str__(self):
        return 'data: ' + str(self.data) + ', ' + str(len(self.nodes)) + ' nodes, value: ' + str(self.value)


class MinNode(DepthFirstNode):
    """Min node for minimax alghoritm"""

    def __init__(self, data=None, value=None):
        super(MinNode, self).__init__(data, value, 'postorder')

    def evaluate(self):
        self.evaluations += 1
        if len(self.nodes) > 0:
            data = self.data
            min_value = sys.maxint
            for node in self.nodes:
                if node.value < min_value:
                    min_value = node.value
                    data = node.data

            self.value = min_value
            self.data = data


class MaxNode(DepthFirstNode):
    """Max node for minimax alghoritm"""

    def __init__(self, data=None, value=None):
        super(MaxNode, self).__init__(data, value, 'postorder')

    def evaluate(self):
        self.evaluations += 1
        if len(self.nodes) > 0:
            data = self.data
            max_value = -sys.maxint
            for node in self.nodes:
                if node.value > max_value:
                    max_value = node.value
                    data = node.data

            self.value = max_value
            self.data = data


class MinABNode(MinNode):
    """Min node for minimax alghoritm with alpha-beta prunning"""

    def __init__(self, data=None, value=None, alpha=-sys.maxint, beta=sys.maxint):
        self.alpha = alpha
        self.beta = beta

        super(MinABNode, self).__init__(data, value)

    def traverseNode(self, node):
        # pass alpha and beta
        node.alpha = self.alpha
        node.beta = self.beta

        # traverse node
        node.traverse(self)

        # update beta
        self.beta = min(self.beta, node.value)

        # alpha cut-off?
        if self.beta <= self.alpha:
            raise StopIterationAfterNodeTraverse


class MaxABNode(MaxNode):
    """Max node for minimax alghoritm with alpha-beta prunning"""

    def __init__(self, data=None, value=None, alpha=-sys.maxint, beta=sys.maxint):
        self.alpha = alpha
        self.beta = beta

        super(MaxABNode, self).__init__(data, value)

    def traverseNode(self, node):
        # pass alpha and beta
        node.alpha = self.alpha
        node.beta = self.beta

        # traverse node
        node.traverse(self)

        # update alpha
        self.alpha = max(self.alpha, node.value)

        # beta cut-off?
        if self.beta <= self.alpha:
            raise StopIterationAfterNodeTraverse
