"""Binary trees.

A binary tree is a class which has an attribute named right, and an attribute
named left. Each right and left attribute is either empty or points to another
binary tree node. This is a recursive data structure.

To make it useful in practice, there is at least one more attribute, named for
example 'value' that stores a user value.

Note: this is not about a binary search tree, just a binary tree.

Please make 2 functions:

1. given a node in the binary tree returns the list of ancestor nodes, including
itself. Lowest first.

2. given two binary tree nodes, returns the lowest common ancestor.
"""

"""
1. Given a node in the binary tree returns the list of ancestor nodes, including
itself. Lowest first.
2. Given two binary tree nodes, returns the lowest common ancestor.
"""

import unittest


class TestBinaryTree(unittest.TestCase):

  def test_ancestors(self):

    tree = BinaryTree(
        (1,
         (3,
          (4,),
          (5,
           None,
           (10,))),
         (6,)))
    node = tree.left.right.right # 10
    self.assertEqual(
        [x.value for x in tree.ancestors(node)],
        [10, 5, 3, 1])


  def test_common_ancestors(self):
    tree = tree_from_tuples(
        (1,
         (3,
          (4,),
          (5,)
         ),
         (6,
          (15,),
          (7,
           None,
           (16, )))))
    node_15 = tree.right.left
    node_16 = tree.right.right.right
    node_4 = tree.left.left
    self.assertEqual(common_ancestor(node_15, node_16).value, 6)
    self.assertEqual(common_ancestor(node_4, node_16).value, 1)
