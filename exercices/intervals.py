


def is_overlapping(interval1, interval2):
  """Returns True when the 2 intervals overlap, False otherwise."""
  raise NotImplementedError()


def merge_intervals(interval1, interval2):
  """Returns one interval from 2 intervals."""
  raise NotImplementedError()


def merge_overlapping_intervals(stream):
  """Yields intervals, merging overlapping intervals from the input stream.

  Hint: you'll likely want to use heapq.merge to create an iterator
  from 2 sorted streams.

  """
  raise NotImplementedError()


# Unit tests:
# To run them:
#
# $ cd papillon
# $ python3 -m unittest intervals
#
# To run just the one you are working on:
# $ python3 -m unittest intervals.OverlappingTest.test_is_overlapping

import unittest


# Examples of two overlapping intervals
OVERLAPPING = (((1, 3), (2, 4)),
               ((1, 4), (2, 3)),
               ((2, 4), (1, 3)),
               ((2, 3), (1, 4)),
               ((1, 2), (2, 4)),
               ((1, 4), (3, 4)))


class OverlappingTest(unittest.TestCase):

  def test_is_overlapping(self):
     for i1, i2 in OVERLAPPING:
       self.assertTrue(is_overlapping(i1, i2))

  def test_is_not_overlapping(self):
    self.assertFalse(is_overlapping((1, 2), (3, 4) ))


class MergeIntervalsTest(unittest.TestCase):
  def test_merge_intervals(self):
    for i1, i2 in OVERLAPPING:
      self.assertEqual()
      

class MergeOverlappingTest(unittest.TestCase):
  def test_merge_overlapping(self):

    merged = list(
        merge_overlapping_intervals(
            merge_2list([(0, 3), (6, 7)],
                        [(1, 2), (3, 4), (5, 6)])))

    self.assertEqual(merged, [(0, 4), (5, 7)])
