"""Merge two sorted list of intervals.

Given 2 sorted lists of non overlapping 2-tuples intervals, 
return one list of non overlapping intervals.
"""



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
        merge_intervals(
          [(0, 3), (6, 7)],
          [(1, 2), (3, 4), (5, 6)]))

    self.assertEqual(merged, [(0, 4), (5, 7)])
