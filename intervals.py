

def is_overlapping(interval1, interval2):
  """Returns True when the 2 intervals overlap, False otherwise."""
  raise NotImplementedError()


def merge_intervals(interval1, interval2):
  """Returns one interval from 2 intervals."""
  raise NotImplementedError()


def merge_streams(stream1, stream2):
  """Yields intervals from each of the input sorted stream, in order."""
  raise NotImplementedError()


def merge_overlapping_intervals(stream):
  """Yields intervals, merging overlapping intervals from the input stream."""
  raise NotImplementedError()


# Unit tests:
# To run them:
#
# $ cd papillon
# $ python3 -m unittest intervals
#
# To run just the one you are working on:
# $ python3 -m unittest intervals.Test.test_is_overlapping

import unittest

class OverlappingTest(unittest.TestCase):

  def test_is_overlapping(self):
    self.assertEqual()


class MergeIntervalsTest(unittest.TestCase):
  def test_merge_intervals(self):
    self.assertEqual()


class MergeStreamsTest(unittest.TestCase):
  def test_merge_streams(self):
    self.assertEqual()


class MergeOverlappingTest(unittest.TestCase):
  def test_merge_overlapping(self):
    self.assertEqual()
