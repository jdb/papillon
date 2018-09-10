import unittest


def dfs(node, neighbors, already, depth = 0):
  if node not in already:
    already.add(node)
    yield (node, depth)
    for neighbor in set(neighbors(node)) - already:
      yield from dfs(neighbor, neighbors, already, depth + 1)


def count_islands(grid):
  already = set()
  rows = len(grid)
  cols = len(grid[0])

  def neighbors(pos):
    for dx, dy in [
      (0, -1), (0, 1), (-1, 0), (1, 0)
    ]:
      nx, ny = pos[0] + dx, pos[1] + dy
      if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
        yield nx, ny

  starts = list(
    (i, j)
    for i in range(len(grid))
    for j in range(len(grid[0]))
    if grid[i][j] == '1'
  )
  already = set()
  cell_depths = list((cell, depth) for start in starts for cell, depth in dfs(start, neighbors, already))
  return sum(1 for cell, depth in cell_depths if depth == 0)


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
