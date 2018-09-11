"""Let's build a 'Trie' datastructure.

When you know a list of words, there are two frequent questions: 
- is this arbitratry string a prefix of a known word?
- is this arbitrary string a full known word?

When you have a Trie datastructure, you can use 2 functions or methods:
- is_prefix(string) -> a boolean
- is_word(string) -> a boolean.
"""

from typing import List

def init_trie(words: List[str]):
    """Returns a Trie datastructure."""
    raise NotImplementedError()


def is_prefix(trie, string: str) -> bool:
    """Returns True if the string is a prefix for one or more words."""
    raise NotImplementedError()


def is_word(trie, string: str) -> bool:
    """Returns True if the string is a full correct word."""
    raise NotImplementedError()


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
        self.assertIsNotNone(init_trie(['car', 'cat', 'python']))

    def test_is_prefix(self):
        trie = init_trie(['car', 'cat', 'python'])
        
        self.assertTrue(is_prefix(trie, 'ca'))
        self.assertTrue(is_prefix(trie, 'car'))
        self.assertTrue(is_prefix(trie, 'cat'))

        self.assertFalse(is_prefix(trie, 'zebr'))

    def test_is_word(self):
        trie = init_trie(['car', 'cat', 'python'])
        self.assertTrue(is_word(trie, 'car'))
        self.assertTrue(is_word(trie, 'cat'))
        self.assertTrue(is_word(trie, 'python'))

        self.assertFalse(is_word(trie, 'zebra'))
