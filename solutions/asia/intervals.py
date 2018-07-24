def order(interval1, interval2):
    """Returns True when intervals are in a good order"""
    return interval1[0] < interval2[0]


def is_overlapping(interval1, interval2):
    """Returns True when the 2 intervals overlap, False otherwise."""

    if order(interval2, interval1):
        interval1, interval2 = interval2, interval1
    return interval1[1] >= interval2[0]

    # return not (interval1[1] < interval2[0] or interval2[1] < interval1[0])


def merge_intervals(interval1, interval2):
    """Returns one interval from 2 intervals."""
    if is_overlapping(interval1, interval2):
        return min(interval1[0], interval2[0]), max(interval1[1], interval2[1])


def merge_streams(stream1, stream2):
    """Yields intervals from each of the input sorted stream, in order."""

    a, b = 0, 0

    # for i in range(0, (len(stream1)+len(stream2))):
    while True:
        if len(stream1) == 0:
            c = 2
            break
        if len(stream2) == 0:
            c = 1
            break

        if order(stream1[a], stream2[b]):
            yield stream1[a]
            a += 1
            if a == len(stream1):
                c = 2
                break
        else:
            yield stream2[b]
            b += 1
            if b == len(stream2):
                c = 1
                break

    if c == 1:
        for i in range(a, len(stream1)):
            yield stream1[i]

    if c == 2:
        for i in range(b, len(stream2)):
            yield stream2[i]


def merge_overlapping_intervals(stream):
    """Yields intervals, merging overlapping intervals from the input stream (already sorted)."""

    s = stream[0]

    for a in range(1, len(stream)):
        if is_overlapping(s, stream[a]):
            s = merge_intervals(s, stream[a])
        else:
            yield s
            s = stream[a]

    yield s


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
        self.assertFalse(is_overlapping((1, 2), (3, 4)))


# class MergeIntervalsTest(unittest.TestCase):
#  def test_merge_intervals(self):
#    for i1, i2 in OVERLAPPING:
#      self.assertEqual(i)

class MergeIntervalsTest(unittest.TestCase):
    def test_merge_intervals(self):
        for i1, i2 in OVERLAPPING:
            self.assertEqual(merge_intervals(i1, i2), (1, 4))


SORTED_STREAMS_EXPECTED = ()


class MergeStreamsTest(unittest.TestCase):
    def test_merge_streams1(self):
        self.assertEqual(list(merge_streams([(1, 2)], [(3, 4), (5, 8)])),
                         [(1, 2), (3, 4), (5, 8)])

    def test_merge_streams2(self):
        self.assertEqual(list(merge_streams([(1, 4)], [(2, 3), (5, 7)])),
                         [(1, 4), (2, 3), (5, 7)])

    def test_merge_streams3(self):
        self.assertEqual(list(merge_streams([(2, 3)], [(1, 4), (5, 7)])),
                         [(1, 4), (2, 3), (5, 7)])

    def test_merge_streams4(self):
        self.assertEqual(
            list(merge_streams([], [(1, 4), (5, 6)])),
            [(1, 4), (5, 6)])

    def test_merge_streams5(self):
        self.assertEqual(list(
            merge_streams([(1, 4), (5, 6)], [(2, 3)])),
            [(1, 4), (2, 3), (5, 6)])


class MergeOverlappingTest(unittest.TestCase):
    def test_merge_overlapping(self):
        merged = list(
            merge_overlapping_intervals(list(
                merge_streams([(0, 3), (6, 7)], [(1, 2), (3, 4), (5, 6)]))))

        self.assertEqual(merged, [(0, 4), (5, 7)])
