"""Binary trees.

A binary tree is an object which has an attribute named right, and an attribute
named left. Each right and left attribute is either empty or points to another
binary tree node. This is a recursive data structure.

Note: this is not about a binary search tree, just a binary tree.

To make it useful in practice, there is at least one more attribute, named for
example 'value' that stores a user value. More attributes can be present,
depending on the problem to solve.

Please make 2 functions:
1. given a node in the binary tree returns the list of ancestor nodes, including 
   itself. Lowest first.
2. given two binary tree nodes, returns the lowest common ancestor.

"""

import unittest
from typing import Iterator, Tuple, TypeVar

# To run the mypy static type checker (http://mypy-lang.org/):
# $ mypy tree.py
T = TypeVar('T')  # the generic type of values held in each node.

class Node:
  """This class and the 2 public methods is the solution."""
  def __init__(self, value : T,
               left: Tuple = None, right: Tuple = None, parent: 'Node' =None):
    self.value, self.parent = value, parent
    self.left = Node(*left, parent=self) if left else None
    self.right = Node(*right, parent=self) if right else None

  def _ancestors(self) -> Iterator['Node']:
    """Yields the current node, then the ancestor nodes up to the root.
    The first element is the node itself (the node is an ancestor of itself)."""
    yield self
    if self.parent:
      yield from self.parent._ancestors()

  def print_ancestors(self):
    print(' '.join(str(i) for i in self._ancestors()))

  def lowest_common_ancestor(self, node1: 'Node', node2: 'Node') -> 'Node':
    """Returns the node that is the lowest common ancestor of node1, node2."""
    depth1 = sum(1 for _ in node1._ancestors())
    depth2 = sum(1 for _ in node2._ancestors())

    deeper, shallower  = (node2, node1) if depth2 > depth1 else (node1, node2)
    for _ in range(abs(depth2 - depth1)):
      deeper = deeper.parent

    # ancestors() and zip() return generators, and generators behaves lazily. So
    # ancestors() will not reach to the root, saving work, unless required: each
    # generator will be pulled just enough times to find the common ancestor.
    for a1, a2 in zip(deeper._ancestors(), shallower._ancestors()):
      if a1 == a2:
        return a1
    raise ValueError('The two nodes have no common ancestor, '
                     'Did you check the graph is actually connected?')

  ### Unit tests helpers. Not required for the solution
  def __iter__(self):
    yield self
    for subtree in self.left, self.right:
      if subtree:
        yield from subtree

  def search(self, value: T):
    for node in self:
      if node.value == value:
        return node
    raise KeyError("Value '%s' not found in the tree." % value)


class NodeTest(unittest.TestCase):
  """To run the unittest:
  $ python3 -m unittest tree
  """

  def setUp(self):
    self.input = (
        6, # value
        (3, # left subtree...
         (1,
          (2,)),
         (4,
          (5,))),
        (8,  # right subtree...
         (7,),
         (9,
          (0,))))
    self.tree = Node(*self.input)

  def test_init(self):
    self.assertEqual(self.tree.value, 6)
    self.assertEqual(self.tree.left.value, 3)
    self.assertEqual(self.tree.right.value, 8)

  def test_search(self):
    self.assertEqual(self.tree.search(1).parent, self.tree.search(3))
    self.assertEqual(self.tree.search(0).parent.parent, self.tree.search(8))
    with self.assertRaises(KeyError):
      self.tree.search(9999)

  def test_ancestors(self):
    self.assertEqual([node.value for node in self.tree.search(0)._ancestors()],
                     [0, 9, 8, 6])

  def test_lowest_common_common(self):
    self.assertEqual(
        self.tree.lowest_common_ancestor(self.tree.search(0),
                                         self.tree.search(3)).value,
        6,'Two nodes must have a common root')

    self.assertEqual(
        self.tree.lowest_common_ancestor(self.tree.search(0),
                                         self.tree.search(6)).value,
        6, 'The direct ancestor of another node is the lca.')

    self.assertEqual(
        self.tree.lowest_common_ancestor(self.tree.search(7),
                                         self.tree.search(0)).value,
        8, 'The common ancestor of two nodes is not the root')

    self.assertEqual(
        self.tree.lowest_common_ancestor(self.tree.search(4),
                                         self.tree.search(4)).value,
        4, 'The common ancestor of the exact same node is the node.')

    with self.assertRaises(ValueError,
                           msg='Disconnected trees raise a ValueError'):
      self.tree.lowest_common_ancestor(self.tree.search(0), Node(999))

  def test_loop(self):

    def check_loops(value: T,
                    left: tuple = None,
                    right: tuple = None,
                    seen: set =None):
      """Helper function handy to validate a Node input against loop."""
      if seen is None:
        seen = set()
      for subtree in left, right:
        if not subtree:
          continue
        if id(subtree) in seen:
          raise ValueError('Loop detected, the input is not a real tree.')
        else:
          seen.add(id(subtree))
        check_loops(*subtree, seen=seen)

    looping_graph = [2, [1, ], [3, ]]

    # Note that this is a contrived unit test that only works because the type
    # checks are optional: the construction of a looping graph is only possible
    # because the Python list is used here, and the Python list is mutable.
    # one can only append to the list because the list is mutable.  Should the
    # type annotations of the Node constructor be respected, only Python tuples
    # would be used. Because Python tuples are immutable, and it is impossible
    # to construct an input looping graph in the first place, out of tuples
    # only.

    # tree's right node is appended tree itself on the left: not a tree anymore
    looping_graph[2].append(looping_graph)

    with self.assertRaises(ValueError, msg='Looping graphs are detected.'):
      check_loops(*looping_graph)

