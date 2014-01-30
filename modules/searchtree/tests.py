import unittest
import nodes


class DepthFirstNodeTests(unittest.TestCase):
    def test_nodes(self):
        test_list = []

        class TestNode(nodes.DepthFirstNode):
            def evaluate(self):
                test_list.append(self.data)
                return self.value

        # http://en.wikipedia.org/wiki/Tree_traversal#Example

        def init(algorithm):
            a = TestNode('a', None, algorithm)
            b = TestNode('b', None, algorithm)
            c = TestNode('c', None, algorithm)
            d = TestNode('d', None, algorithm)
            e = TestNode('e', None, algorithm)
            f = TestNode('f', None, algorithm)
            g = TestNode('g', None, algorithm)
            h = TestNode('h', None, algorithm)
            i = TestNode('i', None, algorithm)

            f.addNode(b).addNode(g)
            b.addNode(a).addNode(d)
            d.addNode(c).addNode(e)
            g.addNode(i)
            i.addNode(h)

            return f

        # preorder
        root = init('preorder')
        root.traverse()

        self.assertListEqual(
            test_list,
            ['f', 'b', 'a', 'd', 'c', 'e', 'g', 'i', 'h']
        )

        # postorder
        test_list = []
        root = init('postodrder')
        root.traverse()

        self.assertListEqual(
            test_list,
            ['a', 'c', 'e', 'd', 'b', 'h', 'i', 'g', 'f']
        )


class MinimaxTests(unittest.TestCase):
    def test_simple(self):
        self.init1(nodes.MinNode, nodes.MaxNode)
        self.root.traverse()
        self.assertEqual(self.root.value, -7)
        self.assertEqual(self.root.data, 'l8')
        self.assertEqual(self.root.evaluations, 22)

        self.init2(nodes.MinNode, nodes.MaxNode)
        self.root.traverse()
        self.assertEqual(self.root.value, 6)
        self.assertEqual(self.root.data, 'l7')
        self.assertEqual(self.root.evaluations, 33)

    def test_ab(self):
        self.init1(nodes.MinABNode, nodes.MaxABNode)
        self.root.traverse()
        self.assertEqual(self.root.value, -7)
        self.assertEqual(self.root.data, 'l8')
        self.assertEqual(self.root.evaluations, 22)

        self.init2(nodes.MinABNode, nodes.MaxABNode)
        self.root.traverse()
        self.assertEqual(self.root.value, 6)
        self.assertEqual(self.root.data, 'l7')
        self.assertEqual(self.root.evaluations, 25)

        self.init3(nodes.MinABNode, nodes.MaxABNode)
        self.root.traverse()
        self.assertEqual(self.root.value, 4)
        self.assertEqual(self.root.data, 'l1')
        self.assertEqual(self.root.evaluations, 11)

    def init1(self, MinNode, MaxNode):
        # http://en.wikipedia.org/wiki/Minimax#Example_2

        # leafs - max nodes- level 4
        l1 = MaxNode('l1', 10)
        l2 = MaxNode('l2', 999999)
        l3 = MaxNode('l3', 5)
        l4 = MaxNode('l4', -10)
        l5 = MaxNode('l5', 7)
        l6 = MaxNode('l6', 5)
        l7 = MaxNode('l7', -999999)
        l8 = MaxNode('l8', -7)
        l9 = MaxNode('l9', -5)

        # level 3 - min nodes
        n31 = MinNode().addNode(l1).addNode(l2)
        n32 = MinNode().addNode(l3)
        n33 = MinNode().addNode(l4)
        n34 = MinNode().addNode(l5).addNode(l6)
        n35 = MinNode().addNode(l7)
        n36 = MinNode().addNode(l8).addNode(l9)

        # level 2 - max nodes
        n21 = MaxNode().addNode(n31).addNode(n32)
        n22 = MaxNode().addNode(n33)
        n23 = MaxNode().addNode(n34).addNode(n35)
        n24 = MaxNode().addNode(n36)

        # level 1 - min nodes
        n11 = MinNode().addNode(n21).addNode(n22)
        n12 = MinNode().addNode(n23).addNode(n24)

        # root - max node
        root = MaxNode().addNode(n11).addNode(n12)

        self.root = root

    def init2(self, MinNode, MaxNode):
        # http://en.wikipedia.org/wiki/File:AB_pruning.svg

        # leafs - max nodes- level 4
        l1 = MaxNode('l1', 5)
        l2 = MaxNode('l2', 6)
        l3 = MaxNode('l3', 7)
        l4 = MaxNode('l4', 4)
        l5 = MaxNode('l5', 5)
        l6 = MaxNode('l6', 3)
        l7 = MaxNode('l7', 6)
        l8 = MaxNode('l8', 6)
        l9 = MaxNode('l9', 9)
        l10 = MaxNode('l10', 7)
        l11 = MaxNode('l11', 5)
        l12 = MaxNode('l12', 9)
        l13 = MaxNode('l13', 8)
        l14 = MaxNode('l14', 6)

        # level 3 - min nodes
        n3_1 = MinNode().addNode(l1).addNode(l2)
        n3_2 = MinNode().addNode(l3).addNode(l4).addNode(l5)
        n3_3 = MinNode().addNode(l6)
        n3_4 = MinNode().addNode(l7)
        n3_5 = MinNode().addNode(l8).addNode(l9)
        n3_6 = MinNode().addNode(l10)
        n3_7 = MinNode().addNode(l11)
        n3_8 = MinNode().addNode(l12).addNode(l13)
        n3_9 = MinNode().addNode(l14)

        # level 2 - max nodes
        n2_1 = MaxNode().addNode(n3_1).addNode(n3_2)
        n2_2 = MaxNode().addNode(n3_3)
        n2_3 = MaxNode().addNode(n3_4).addNode(n3_5)
        n2_4 = MaxNode().addNode(n3_6)
        n2_5 = MaxNode().addNode(n3_7)
        n2_6 = MaxNode().addNode(n3_8).addNode(n3_9)

        # level 1 - min nodes
        n1_1 = MinNode().addNode(n2_1).addNode(n2_2)
        n1_2 = MinNode().addNode(n2_3).addNode(n2_4)
        n1_3 = MinNode().addNode(n2_5).addNode(n2_6)

        # root - max node
        root = MaxNode().addNode(n1_1).addNode(n1_2).addNode(n1_3)

        self.root = root

    def init3(self, MinNode, MaxNode):
        """Best a-b case"""

        # leafs - min nodes- level 3
        l1 = MinNode('l1', 4)
        l2 = MinNode('l2', 1)
        l3 = MinNode('l3', 6)
        l4 = MinNode('l4', 2)
        l5 = MinNode('l5', 3)
        l6 = MinNode('l6', 0)
        l7 = MinNode('l7', 7)
        l8 = MinNode('l8', 8)

        # level 2 - max nodes
        n2_1 = MaxNode().addNode(l1).addNode(l2)
        n2_2 = MaxNode().addNode(l3).addNode(l4)
        n2_3 = MaxNode().addNode(l5).addNode(l6)
        n2_4 = MaxNode().addNode(l7).addNode(l8)

        # level 1 - min nodes
        n1_1 = MinNode().addNode(n2_1).addNode(n2_2)
        n1_2 = MinNode().addNode(n2_3).addNode(n2_4)

        # root - max node
        root = MaxNode().addNode(n1_1).addNode(n1_2)

        self.root = root
