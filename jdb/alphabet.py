
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
