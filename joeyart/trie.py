"""Let's build a 'Trie' datastructure.

When you know a list of words, there are two frequent questions:
- is this arbitratry string a prefix of a known word?
- is this arbitrary string a full known word?

When you have a Trie datastructure, you can use 2 functions or methods:
- is_prefix(string) -> a boolean
- is_word(string) -> a boolean.
"""

from typing import List
import math

class Trie:

    def __init__(self, words: List[str]=None):
        """Returns a Trie datastructure. """


    def is_prefix(self, string: str) -> bool:
        """ Returns True if the string is a prefix for one or more words."""
 
    def is_word(self, string: str) -> bool:
        """Returns True if the string is a full correct word."""


# To run all the tests:
# $ python3 -m unittest trie

# To run one specific test:
# $ python3 -m unittest trie.TrieTest
# $ python3 -m unittest trie.TrieTest.test_init
# $ python3 -m unittest trie.TrieTest.test_is_prefix
# $ python3 -m unittest trie.TrieTest.test_is_word

# Please send a PR when you have a test passing :)
# Then, later, we can work on different ways to have a Trie:
# 1. with Python classes
# 2. efficient implementations of is_prefix(), is_word().
# Good luck !!


import unittest


class TrieTest(unittest.TestCase):

    def test_init(self):
        self.assertIsNotNone(Trie(['car', 'cat', 'python']))

    def test_is_prefix(self):
        trie = Trie(['car', 'cat', 'python'])

        self.assertTrue(trie.is_prefix('ca'))
        self.assertTrue(trie.is_prefix('car'))
        self.assertTrue(trie.is_prefix('cat'))

        self.assertFalse(trie.is_prefix('zebr'))

    def test_is_word(self):
        trie = Trie(['car', 'cat', 'python'])
        self.assertTrue(trie.is_word('car'))
        self.assertTrue(trie.is_word('cat'))
        self.assertTrue(trie.is_word('python'))

        self.assertFalse(trie.is_word('zebra'))
