"""Merge two sorted list of intervals.

Given 2 sorted lists of non overlapping 2-tuples intervals, 
return one list of non overlapping intervals.
"""

import heapq

def overlapping(first, second):
  "Make sure first[0] < second[0]"
  return first[1] >=  second[0]

def merge_interval(a, b):
  return min(a[0], b[0]), max(a[1], b[1])

def merge(*sequences):
  merged = heapq.merge(*sequences)
  first = next(merged)
  for second in merged:
    if overlapping(first, second):
      first = merge_interval(first, second)
    else:
      yield first
      first = second
  yield first

  
# To run the unit tests:
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


class MergeOverlappingTest(unittest.TestCase):
  def test_merge_overlapping(self):
    merged = list(
        merge(
          [(0, 3), (6, 7)],
          [(1, 2), (3, 4), (5, 6)]))

    self.assertEqual(merged, [(0, 4), (5, 7)])
    self.assertEqual(list(merge([])), [], [])

  def test_overlapping(self):
    for a, b in OVERLAPPING:
      self.assertTrue(overlapping(*sorted([a,b])))
