"""
1. Given a node in the binary tree returns the list of ancestor nodes, including
itself. Lowest first.
2. Given two binary tree nodes, returns the lowest common ancestor.
"""

import unittest


def ancestors(node):
  """Returns ancestors of a node in a binary tree. Includes itself."""
  while node:
    yield node
    node = node.parent


def common_ancestor(node_a, node_b):
  """Returns common ancestor of two binary trees.

  O(1) memory. O(nb_ancestors) CPU"""
  ancestors_a = ancestors(node_a)
  ancestors_b = ancestors(node_b)
  lowest_ancestors = ancestors_a if node_a.level > node_b.level else ancestors_b
  for _ in range(abs(node_a.level - node_b.level)):
    next(lowest_ancestors)
  same = (pa for pa, pb in zip(ancestors_a, ancestors_b) if pa == pb)
  return next(same)


class BinaryTree:
  """Binary tree, each node knows its parent and level"""
  def __init__(self, value, left=None, right=None, parent=None):
    self.left = left
    self.right = right
    self.value = value
    self.set_parent(parent)

  def set_parent(self, parent):
    """Sets the parent and updates the level"""
    self.parent = parent
    self.level = parent.level + 1 if parent else 0

  def __repr__(self):
    return "BinaryTree<value={value}>".format(value=self.value)


def tree_from_tuples(tuple_tree, parent=None):
  """Returns a tree from a tuple representation"""
  node = BinaryTree(tuple_tree[0], None, None, parent)
  left = tree_from_tuples(tuple_tree[1], node) if tuple_tree[1] else None
  right = tree_from_tuples(tuple_tree[2], node) if tuple_tree[2] else None
  node.left = left
  node.right = right
  return node


class TestBinaryTree(unittest.TestCase):
  """Test for binary tree"""
  def test_ancestors(self):
    """Test the ancestors methods"""
    tree = tree_from_tuples(
        (1,
         (3,
          (4, None, None),
          (5,
           None,
           (10, None, None)
          )
         ),
         (6, None, None)
        )
    )
    node = tree.left.right.right # 10
    self.assertEqual(
        [x.value for x in ancestors(node)],
        [10, 5, 3, 1]
    )


  def test_common_ancestors(self):
    """Test the common ancestors"""
    tree = tree_from_tuples(
        (1,
         (3,
          (4, None, None),
          (5, None, None)
         ),
         (6,
          (15, None, None),
          (7,
           None,
           (16, None, None)
          )
         )
        )
    )
    node_15 = tree.right.left
    node_16 = tree.right.right.right
    node_4 = tree.left.left
    assert node_15
    assert node_16
    assert node_4
    self.assertEqual(common_ancestor(node_15, node_16).value, 6)
    self.assertEqual(common_ancestor(node_4, node_16).value, 1)
