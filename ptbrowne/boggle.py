
# Given a grid of letters and a lexicon, find all the words from
# the lexicon that can be formed in the grid. The rules for forming a
# word:
# - You can start at any position.
# - You can move to one of the 8 adjacent cells (horizontally/vertically/diagonally).
# - You can't visit the same cell twice in the same word.

# The lexicon is a class with these two methods:
# - is_word(string): Returns whether the given string is a valid word.
# - is_prefix(string): Returns whether the given string is a prefix of
#   at least one word in the dictionary.
import json
from collections import defaultdict, OrderedDict
from contextlib import contextmanager

DX = [-1, 0, 1]
DY = [-1, 0, 1]

@contextmanager
def mark_seen(seen, pos, val):
  seen[pos] = val
  yield
  del seen[pos]


def walk(pos, seen, get_neighbors, get_context):
  for neighbor in get_neighbors(pos):
    ctx = get_context(neighbor)
    if ctx['ok']:
      yield ctx['yield']
    if not ctx['stop']:
      seen[pos] = ctx['mark']
      yield from walk(neighbor, seen, get_neighbors, get_context)
      del seen[pos]

class Grid:
  """
  Grid represents a grid of letter. It is possible to get all the words
  from a lexicon that can be formed in a grid.

  It has graph like features to perform lexicon optimized traversals.
  """
  def __init__(self, *lines, **kwargs):
    if not 'lexicon' in kwargs:
      raise ValueError('Must instantiate Grid with a lexicon')
    self.lexicon = kwargs['lexicon']
    self.data = [list(line) for line in lines]
    self.nrows = len(self.data)
    self.ncols = len(self.data[0])

  def neighbors(self, pos):
    """Returns all the valid neighbord of a cell at pos"""
    i, j = pos
    nrows, ncols = self.nrows, self.ncols
    for dx in DX:
      for dy in DY:
        if dx == 0 and dy == 0:
          continue
        ni, nj = (i + dx), (j + dy)
        if ni >= 0 and ni < nrows and nj >= 0 and nj < ncols:
          yield ni, nj

  def value_at(self, pos):
    i, j = pos
    return self.data[i][j]

  def _walk(self, pos, seen=None):
    """Yields all the words that can be formed from a position in the grid"""

    if not seen:
      seen = OrderedDict()

    neighbors = lambda pos: (
      pos for pos in self.neighbors(pos) if not seen.get(pos)
    )
    def get_context(pos):
      letter = self.value_at(pos)
      word = ''.join(seen.values()) + letter
      is_prefix, is_word = self.lexicon.info(word)
      return {
        'ok': is_word,
        'yield': word,
        'stop': not is_prefix,
        'mark': letter
      }
    mark = lambda pos, ctx: mark_seen(seen, pos, ctx['letter'])

    yield from walk(pos, seen, neighbors, get_context)

  def words_iter(self):
    """Yields all the words that can be formed in the grid"""
    starts = [(i, j) for i in range(self.nrows) for j in range(self.ncols)]

    for start in starts:
      yield from self._walk(start)

  def words(self):
    """Returns all the words that can be formed in the grid as a list"""
    return list(self.words_iter())

class TrieNode(object):
  def __init__(self):
    self.is_word = False
    self.trie = defaultdict(lambda: TrieNode())

class Lexicon:
  """
  Lexicon is used for fast checks (O(k)), of whether or not a prefix/word
  is part of a particular dataset (k being the length of the prefix/word).

  Its underlying data structure is a trie. 

  (is_word: False, trie: {
    'c': (is_word: False, trie: {
      'a': (is_word: False, trie: {
        'r': (is_word: True, trie: {})
      })
    })
  })

  Each node of the trie also has the information of whether the current
  path is a word.
  """
  def __init__(self):
    self.root = TrieNode()

  def add(self, word):
    """Add a word to the lexicon trie"""
    _len = len(word)
    trie = self.root.trie
    for i, letter in enumerate(word):
      node = trie[letter]
      is_last_letter = i == _len - 1
      if not node.is_word and is_last_letter:
        node.is_word = True
      trie = node.trie

  def get_node(self, string):
    """
    Returns the trie node of the string (prefix or word).

    Returns None if the string is not in the trie.
    """
    node = self.root
    for letter in string:
      if letter in node.trie:
        node = node.trie[letter]
      else:
        return None
    return node

  def __getitem__(self, word):
    """Cute way to perform is_word"""
    return self.is_word(word)

  def is_prefix(self, prefix):
    """Returns True if prefix prefixes any of the words in the lexicon"""
    leaf = self.get_node(prefix)
    if leaf:
      return True

  def is_word(self, word):
    """Returns True if the word is found in the lexicon"""
    leaf = self.get_node(word)
    return leaf and leaf.is_word

  def info(self, word):
    """is_prefix and is_word in one traversal"""
    leaf = self.get_node(word)
    return bool(leaf), leaf and leaf.is_word

  def __repr__(self):
    return json.dumps(self.root, indent=2)


# run the unittest with python3 -m unittest boggle.py
import unittest

class TestGrid(unittest.TestCase):
  
  def test_words(self):
    lexicon = Lexicon()
    for w in ['card', 'data', 'act', 'arc', 'cad', 'car', 'cat', 'rat',
                 'rca', 'tad', 'tar', 'ac', 'ad']:
      lexicon.add(w)
    words = Grid(
      'aar',
      'tcd',
      lexicon=lexicon
    ).words()
    for word in ['card', 'data', 'act', 'arc', 'cad', 'car', 'cat', 'rat',
                 'rca', 'tad', 'tar', 'ac', 'ad']:
      self.assertIn(word, words)
    for word in ['dra', 'caat', 'acd', 'drac', 'tcd']:
      self.assertNotIn(word, words)

  def test_neighbors(self):
    grid = Grid('aar', 'tcd', lexicon=Lexicon())
    neighbors = list(grid.neighbors((0, 0)))
    for pos in [(1, 0), (0, 1), (1, 1)]:
      self.assertIn(pos, neighbors)
    
    neighbors2 = list(grid.neighbors((1, 1)))
    for pos in [(0, 0), (0, 1), (0, 2), (1, 0)]:
      self.assertIn(pos, neighbors2)
    self.assertNotIn((1, 1), neighbors2)


class TestLexicon(unittest.TestCase):
  def test_lexicon(self):
    lexicon = Lexicon()
    for word in 'car', 'card', 'cart', 'cat':
      lexicon.add(word)

    for word in 'car', 'card', 'cart', 'cat':
      self.assertTrue(lexicon.is_word(word))
      self.assertTrue(lexicon[word])
      self.assertTrue(lexicon.is_prefix(word))
    for word in 'c', 'ca':
      self.assertFalse(lexicon.is_word(word))
      self.assertTrue(lexicon.is_prefix(word))

    self.assertFalse(lexicon['NoTfOuNd'])



