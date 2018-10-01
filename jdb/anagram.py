from collections import Counter
import re


def _normalize(s, case_sensitive=True):
  if not case_sensitive:
    s = s.lower()
  return [Counter(word) for word in sorted(re.split('\W+', s))]


def is_anagram(a, b, case_sensitive=True):
  if len(a) != len(b):
    return False
  return _normalize(a, case_sensitive) == _normalize(b, case_sensitive)


# run the unittest with python -m unittest q1_1_anagram.py
# tests in the same file for convenience, as long as implementation is short.
import unittest

class TestAnagrams(unittest.TestCase):
  """Tests shamelessly stolen from Laida (thank you!)."""

  def test_word(self):
    self.assertTrue(is_anagram("banana", "nanaba", False))
    self.assertTrue(is_anagram("BaNana", "NaBana", True))
    self.assertFalse(is_anagram("apple", "elapa", False))
    self.assertFalse(is_anagram("oRaNge", "oarNge", True))

  def test_sentence(self):
    self.assertTrue(is_anagram("hello world", "rowld lehlo", False))
    self.assertTrue(is_anagram("Google CodeU", "gooGle UedoC", True))
    self.assertFalse(is_anagram("python test", "thypo sett", False))
    self.assertFalse(is_anagram("UnIt TeSt", "uNiT seTT", True))


class Node:
  def __init__(self, value=None):
    self.value, self.next = value, None

# This implementation uses the iterator a lot, it is not better in
# terms of complexity:
# pros: shorter methods, more consistent with other Python containers list, dicts...
# cons: confusing to the reader unfamiliar with iterators
#
# resource on Python's iterators:
# https://www.programiz.com/python-programming/iterator
# http://www.diveintopython3.net/iterators.html

class LinkedList:
  def __init__(self, original_list):
    # __init__ loops over the input list: O(n)

    if not original_list:
      self.head = None
      return

    current = self.head = Node(original_list[0])
    for value in original_list[1:]:
      current.next = Node(value)
      current = current.next

  def __iter__(self):
    # - iter returns a interator object in constant time.
    # - then the caller of the iterator can call 'next()'
    #   and next will returns each Node, and once exhausted
    #   the iterator will raise a StopIteration exception.
    #
    # When using the for loop over an iterable, __iter__
    # then __next__ are called automatically (these steps
    # are called the iterator protocol).
    current = self.head
    while current:
      yield current
      current = current.next

  def __len__(self):
    # enumerate returns an iterator immediately, and the for
    # loop will call next() on the the enumerate iterator until
    # exhausted. You can call next on an enumerate iterator as
    # many times as there are elements in the iterator provided
    # to enumerate. __iter__ will yields the n elements, so enumerate
    # will also return n elements. __len__ is in O(n).
    if not self.head:
      return 0
    for index, _ in enumerate(self): pass
    return index + 1

  def __getitem__(self, k):
    if k < 0:
      return self[len(self) + k]  # O(n) due to len()
    else:
      for index, node in enumerate(self):  # O(n) due to __iter__
        if index == k:
          return node
      else:
        raise IndexError('LinkedList only has %s elements, no %sth element'
                         % (index + 1, k))


# run the unittest with python -m unittest ex1-1-linkedlistD
# tests in the same file for convenience, as long as implementation is short.
import unittest

class TestLinkedList(unittest.TestCase):

  def test_construct_iter(self):
    list_ = [1, 2, 3, 4, 5, 6, 6]
    self.assertEqual([n.value for n in LinkedList(list_)], list_)

  def test_len(self):
    """len() of a LinkedList must be equal to the len of the input list."""
    # for 2 sample lists, I test that the len of the list is the len
    # of the LinkedList that is constructed with the list.
    l1 = [1]
    self.assertEqual(len(LinkedList(l1)), len(l1))
    l2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    self.assertEqual(len(LinkedList(l2)), len(l2))
    l3 = []
    self.assertEqual(len(LinkedList(l3)), len(l3))


  def test_forward(self):
    ll = LinkedList(range(10))
    for index_value in range(10):
      self.assertEqual(ll[index_value].value, index_value)

  def test_get_negative_k(self):
    ll = LinkedList(range(-10, 0))
    for v in range(-10, 0):
      self.assertEqual(ll[v].value, v)

  def test_None_is_an_acceptable_value(self):
    self.assertEqual(LinkedList([1, None, 2])[1].value, None)


"""A solution for the CodeU Emea assignment #2: binary trees."""

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



from collections import OrderedDict
from itertools import product

class Grid:

  def __init__(self, *grid, lexicon=None):
    self.grid, self.lexicon = grid, lexicon if lexicon else load_lexicon()
    self.x_max, self.y_max = len(grid[0]), len(grid)

  def __getitem__(self, position):
    """Returns the letter found at 'position'."""
    return self.grid[position[1]][position[0]]

  def words(self):
    """Returns words found on the grid."""
    words = set()
    for slot in product(range(self.x_max), range(self.y_max)):
      self._check_prefixes(slot, words)
    # the returned words are reverse-sorted by word length.
    return sorted(words, key=len, reverse=True)

  def _check_prefixes(self, slot, words):
    traversal = self._traverse(slot)
    backtrack_request = None
    while True:
      try:
        path = traversal.send(backtrack_request)
      except StopIteration:
        return words

      prefix = ''.join(self[s] for s in path)
      if not self.lexicon.is_prefix(prefix):
        backtrack_request = True
      else:
        backtrack_request = False
        if self.lexicon.is_word(prefix):
          words.add(prefix)


  def _traverse(self, slot, path=None):
    """Traverses the paths starting from 'position'."""
    if path is None:
      path = OrderedDict()

    path[slot] = True

    backtrack_request = yield path
    if not backtrack_request:
      for slot in self._children(path, *slot):
        yield from self._traverse(slot, path)

    path.popitem()

  def _children(self, visited, x, y):
    """Generate the unvisited neighbors of 'position'."""
    for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
        xn, yn = x + dx, y + dy
        if (0 <= xn < self.x_max and 0 <= yn < self.y_max and
            (xn, yn) not in visited):
          yield xn, yn


def load_lexicon():
  trie = Trie()
  # On linux, install the file below with:
  # $ sudo apt-get install wamerican
  with open('/usr/share/dict/american-english') as f:
    for word in [w.strip().lower() for w in f
                 if not w.strip().endswith("'s") and len(w.strip())>1]:
      trie.add(word)
  return trie


class Trie:

  def __init__(self):
    self.children = {}
    self.full_word = False

  def add(self, letters):
    first, *rest = letters
    if first not in self.children:
      self.children[first] = Trie()
    if rest:
      self.children[first].add(rest)
    else:
      self.children[first].full_word = True

  def __getitem__(self, letters):
    first, *rest = letters
    if first not in self.children:
      return False
    return self.children[first][rest] if rest else self.children[first]

  def is_word(self, letters):
    trie = self[letters]
    return trie.full_word if trie else False

  def is_prefix(self, letters):
    return bool(self[letters])


# run the unittest with python -m unittest wordsearch.py
import unittest

class TestTrie(unittest.TestCase):

  def test_trie(self):
    trie = Trie()
    for word in 'car', 'card', 'cart', 'cat':
      trie.add(word)
    for word in 'car', 'card', 'cart', 'cat':
      self.assertTrue(trie.is_word(word))
      self.assertTrue(trie.is_prefix(word))
    for word in 'c', 'ca':
      self.assertFalse(trie.is_word(word))
      self.assertTrue(trie.is_prefix(word))
    self.assertFalse(trie['NoTfOuNd'])


class TestBuggles(unittest.TestCase):

  def test_children(self):
    neighbors = list(Grid('abc', 'def', 'ghi', lexicon=True)
                     ._children(set(), 1, 0))
    self.assertIn((1, 1), neighbors)
    self.assertIn((0, 0), neighbors)
    self.assertNotIn((1, 2), neighbors)
    self.assertNotIn((1, -1), neighbors)

  def test_getitem(self):
    grid = Grid('abc', 'def', 'ghi', lexicon=True)
    for letter, position in zip('abcdefghi',
                                ((x, y) for y in range(3) for x in range(3))):
      self.assertEqual(grid[position], letter)

  def test_words(self):
    lexicon = Trie()
    word_list = ['card', 'data', 'act', 'arc', 'cad', 'car', 'cat', 'rat',
                 'rca', 'tad', 'tar', 'ac', 'ad']
    for word in word_list:
      lexicon.add(word)

    words = Grid('aar', 'tcd', lexicon=lexicon).words()
    for word in word_list:
      self.assertIn(word, words)


"""Count islands.

Pseudo-code:
- make a set of all *land* position,
- sets the number of island to zero
- while the set is non-empty:
  - pick a random position from the set
  - visit the position:
    - remove the position from the set
    - for each unvisited neighbors: visit the neighbor as the new position
  - now, the whole island got visited, increment the number of island by one.
- return the number of island
"""

import unittest


def island_count(*grid):
  """Returns the number of islands on the grid."""
  unvisited = {(x, y)
               for (y, row) in enumerate(grid)
               for (x, char) in enumerate(row)
               if bool(int(char))}

  number_of_islands = 0
  while unvisited:
    visit_dfs(next(iter(unvisited)), unvisited)
    number_of_islands += 1
  return number_of_islands


def neighbors(position):
  """Yields the neighbors of position."""
  for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
    yield position[0] + dx, position[1] + dy


def visit_dfs(position, unvisited):
  """Returns when all positions on the same island are visited."""
  unvisited.remove(position)
  for neighbor in neighbors(position):
    if neighbor in unvisited:
      visit_dfs(neighbor, unvisited)


class IslandCountTestCase(unittest.TestCase):

  def test_count1(self):
    self.assertEqual(island_count('0'), 0)

  def test_count2(self):
    self.assertEqual(island_count('1'), 1)

  def test_count3(self):
    self.assertEqual(island_count('010',
                                  '000',
                                  '010'), 2)

  def test_count4(self):
    self.assertEqual(island_count('011',
                                  '000',
                                  '010'), 2)

  def test_count5(self):
    self.assertEqual(island_count('011',
                                  '010',
                                  '010'), 1)

  def test_count6(self):
    self.assertEqual(island_count('0101',
                                  '1100',
                                  '0010',
                                  '0010'), 3)


import copy
from collections import defaultdict, OrderedDict
from itertools import zip_longest, islice


def words(only_ascii=False):
  "Yields words from /usr/share/dict/american-english."
  with open('/usr/share/dict/american-english') as f:
    for w in f:
      if "'" not in w and (not only_ascii or '\\' not in ascii(w)):
        yield w.strip()


def ordered_pairs(words):
  "Yields 2-tuples of ordered letters."
  before = next(words)
  for after in words:
    for b, a in zip_longest(before, after, fillvalue='-'):
      if b == a:
        yield '-', a
      else:
        yield b, a
        break
    before = after


def make_graph(pairs):
  "Returns a graph as 2 dicts: parent to children and child to parents."
  children, parents = defaultdict(set), defaultdict(set)
  for before, after in pairs:
    if before in children and after in children[before]:
      raise ValueError('Loop detected: %s, %s' % (before, after))
    children[after].add(before)
    parents[before].add(after)
  return parents, children


def topsort(parents, children):
  "Returns a list of letters, in order. O(n)."
  path = OrderedDict()

  def dfs(before):
    for after in parents[before] - set(path):
      dfs(after)
    path[before] = True

  for letter in set(parents).difference(children):
    dfs(letter)

  return reversed(path.keys())


def topsort_all(parents, children, path=None, free_letters=None):
  "Yields all list of letters, in all possible orders. O(n!)."

  # Different approach:
  #
  # 1. The algorithm keeps track an ordered list of letters, it is named "path".
  # 2. The algorithm keeps track of a set of current "free letters". A "free
  # letter" is a letter without no ordering constraint anymore. Given the
  # current previous letters, the free letter can be located anywhere later in
  # the alphabet.
  #
  # Algorithm:
  #
  # - if no more roots and no more free letter:
  #    yield the current alphabet alphabet and backtrack
  # - for each root or current "free letter" of the graph:
  #   - copy the graph
  #   - remove the root from the copy and add the "free" letters to a set.
  #   - append the root to the alphabet
  #   - recurse the algorithm the copy of the graph
  #   - pop the root from the alphabet
  #
  # In the worst case, the graph is {a: {b, c, d, e,  ... x, y, z}}
  # There are n! permutations of an array of n elements
  # And there are as many alphabets as there are permutations of {b, c ... , z}

  if path == None:
    path, free_letters = [], set()

  roots = set(parents).difference(children)  # O(n) already

  if not roots and not free_letters:  # 0/3: stop condition.
    yield path

  else:
    for letter in sorted(roots.union(free_letters)):

      # 1/3: this stack of the recursion does not mutate the input.
      nparents = copy.deepcopy(parents)
      nchildren = copy.deepcopy(children)
      nfree_letters = set(free_letters)

      # 2/3: shrink the graph by removing the letter, before recursing
      if letter in roots:
        removed = nparents.pop(letter)
        for child in removed:
          nchildren[child].remove(letter)
          if not nchildren[child]:
            del nchildren[child]
            if child not in nparents:
              nfree_letters.add(child)

      else:  # if letter not in roots, then it must be in nfree_letters
        nfree_letters.remove(letter)

      # 3/3. recursing: running the same logic on a smaller graph
      path.append(letter)
      yield from topsort_all(nparents, nchildren, path, nfree_letters)
      path.pop()


def alphabet(ascii=False):
    return topsort(*make_graph(ordered_pairs(words(ascii))))


def all_alphabet(ascii=False):
    return topsort_all(*make_graph(ordered_pairs(words(ascii))))


import unittest


class TestAlphabet(unittest.TestCase):

    def testordered_pairs(self):
      for before, after in ordered_pairs(words(), ):
        self.assertLess(before, after)

    def test_one_alphabet(self):
        letters = alphabet()
        before = next(letters)
        for after in letters:
            try:
                bytes(after, 'ascii')
            except UnicodeEncodeError:
                continue
            self.assertLess(before, after)
            before = after

    def test_all_alphabet(self):
        self.assertEqual(sum(1 for _ in islice(all_alphabet(), 1000)), 1000)
