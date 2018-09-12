import unittest
import operator
from itertools import product, chain

def flatmap(iterable, fn):
  return chain.from_iterable(map(fn, iterable))

def dfs(node, neighbors, already, depth = 0):
  if node not in already:
    already.add(node)
    yield (node, depth)
    for neighbor in set(neighbors(node)) - already:
      yield from dfs(neighbor, neighbors, already, depth + 1)

def count_islands(grid):
  rows = len(grid)
  cols = len(grid[0])

  def inside_boundary(pos):
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols

  def is_earth(pos):
    x, y = pos
    return grid[x][y] == '1'

  def neighbors(pos):
    deltas = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    neighbors = map(lambda delta: tuple(map(operator.add, pos, delta)), deltas)
    return filter(lambda pos: inside_boundary(pos) and is_earth(pos), neighbors)

  starts = filter(is_earth, product(range(rows), range(cols)))
  already = set()
  dfs_ = lambda start: dfs(start, neighbors, already)
  depths = flatmap(starts, dfs_)
  return sum(map(lambda _: 1, filter(lambda celldepth: celldepth[1] == 0, depths)))


class TestIslands(unittest.TestCase):
  def test_islands(self):
    tests = [
      ("""
        0101000
        1101100
        1111001
        0000010
      """, 3),

      ("""
        0101000
        1101100
        1101000
      """, 2),

      ("""
        0101000
        1101100
        1101000
        1101001
      """, 3),

      ("""
        0101000
        1101100
        1111001
        0000011
      """, 2),

      ("""
        0111000
        0101100
        1101001
        0000011
      """, 2),

      ("""
        0111011
        0001110
        1101001
        0000011
      """, 3),

      ("""
        0101011
        0001110
        1101001
        0000011
      """, 4),

      ("""
        0101011
        0001010
        1101001
        0000011
      """, 5),

      ("""
        1111111
        1000001
        1000001
        1111111
      """, 1),

      ("""
        1110110
        0100101
        1100110
        0000000
      """, 3),

      ("""
        1100011
        0111010
        0001110
        0000100
      """, 1),

      ("""
        1110110001001110111010111010101010111
        0100101011101010101000101011101110101
        0100101001001110110010111010101010111
        1100110000001010101010101010101010101
      """, 13)
    ]

    for grid_str, expected in tests:
      grid = [line.strip() for line in grid_str.split('\n') if line.strip()]
      self.assertEqual(expected, count_islands(grid))


if __name__ == '__main__':
  unittest.main()
