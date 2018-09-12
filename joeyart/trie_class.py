"""Let's refactor this code to make it into a class so the unit test pass."""

from typing import List


def is_prefix(trie, string: str) -> bool:
    """Returns True if the string is a prefix for one or more words."""
    return any(w.startswith(string) for w in trie)


def is_word(trie, string: str) -> bool:
    """Returns True if the string is a full correct word."""
    return any(w == string for w in trie)


# To run all the tests:
# $ python3 -m unittest trie

# To run one specific test:
# $ python3 -m unittest trie_class.TrieTest.test_is_prefix
# $ python3 -m unittest trie_class.TrieTest.test_is_word


import unittest


class TrieTest(unittest.TestCase):

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
