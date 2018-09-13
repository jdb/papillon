
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


class Grid:
  pass

class Lexicon:
  pass

# run the unittest with python3 -m unittest boggle.py
import unittest


class TestGrid(unittest.TestCase):
  
  def test_words(self):
    words = Grid('aar', 'tcd', lexicon=Lexicon()).words()
    for word in ['card', 'data', 'act', 'arc', 'cad', 'car', 'cat', 'rat',
                 'rca', 'tad', 'tar', 'ac', 'ad']:
      self.assertIn(word, words)


class TestLexicon(unittest.TestCase):

  def test_lexicon(self):
    lexicon = Lexicon()
    for word in 'car', 'card', 'cart', 'cat':
      lexicon.add(word)
    for word in 'car', 'card', 'cart', 'cat':
      self.assertTrue(lexicon.is_word(word))
      self.assertTrue(lexicon.is_prefix(word))
    for word in 'c', 'ca':
      self.assertFalse(lexicon.is_word(word))
      self.assertTrue(lexicon.is_prefix(word))
    self.assertFalse(lexicon['NoTfOuNd'])



