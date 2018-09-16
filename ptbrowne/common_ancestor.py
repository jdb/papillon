"""
1. Given a node in the binary tree returns the list of ancestor nodes, including
itself. Lowest first.
2. Given two binary tree nodes, returns the lowest common ancestor.
"""

import unittest


def ancestors(tree, node):
  """Returns ancestors of a node in a binary tree. Includes itself."""
  if tree == node:
    return [node]
  else:
    for leaf in [tree.left, tree.right]:
      if leaf:
        ancestors_leaf = ancestors(leaf, node)
        if ancestors_leaf is not None:
          ancestors_leaf.append(tree)
          return ancestors_leaf


def common_ancestor(tree, node_a, node_b):
  """Returns common ancestor of two binary trees"""
  return next(
      reversed([
          ancestor_a
          for (ancestor_a, ancestor_b) in zip(
              reversed(list(ancestors(tree, node_a))),
              reversed(list(ancestors(tree, node_b)))
          ) if ancestor_a == ancestor_b
      ]),
      None
  )


class BinaryTree:
  def __init__(self, value, left=None, right=None):
    self.left = left
    self.right = right
    self.value = value

  def __repr__(self):
    return "BinaryTree<value={value}>".format(value=self.value)


class TestBinaryTree(unittest.TestCase):
  def test_ancestors(self):
    node = BinaryTree(10, None, None)
    tree = BinaryTree(
        1,
        BinaryTree(
            3,
            BinaryTree(4, None, None),
            BinaryTree(5, node, None)
        ),
        BinaryTree(6, None, None)
    )
    self.assertEqual(
        [x.value for x in ancestors(tree, node)],
        [10, 5, 3, 1]
    )


  def test_common_ancestors(self):
    node = BinaryTree(10)
    node_4 = BinaryTree(4)
    node_15 = BinaryTree(15)
    node_16 = BinaryTree(16)
    tree = BinaryTree(
        1,
        BinaryTree(
            3,
            node_4,
            BinaryTree(5, node)
        ),
        BinaryTree(
            6,
            node_15,
            BinaryTree(
                7,
                node_16
            )
        )
    )
    self.assertEqual(common_ancestor(tree, node_15, node_16).value, 6)
    self.assertEqual(common_ancestor(tree, node_4, node_16).value, 1)
