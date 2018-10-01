"""Count the number of islands on a 2D grid.

You are given a 2-dimensional map of tiles where each tile is either land or
water. You have to write a function that counts the number of islands. Two tiles
belong to the same island if they are both land and are adjacent horizontally
orvertically, but not diagonally. The input to your function is a tuple of
strings 2-dimensional array of booleans, where the character '0' means water and
the character '1' means land. The function should simply return the number of
islands.

Pseudo-code of this solution:
- make a set of all *land* position,
- sets the number of island to zero
- while the set is non-empty:
  - pick a random position from the set
  - visit the position:
    - remove the position from the set
    - for each unvisited neighbors: visit the neighbor as the new position
  - now, the whole island got visited, increment the number of island by one.
- return the number of island
"""

import unittest


Position = Tuple[int, int]


def island_count(*grid: str) -> int:
  """Returns the number of islands on the grid."""
  unvisited = {(x, y)
               for (y, row) in enumerate(grid)
               for (x, char) in enumerate(row)
               if bool(int(char))}

  number_of_islands = 0
  while unvisited:
    explore_island(next(iter(unvisited)), unvisited)
    number_of_islands += 1
  return number_of_islands


def neighbors(position: Position) -> Iterator[Position]:
  """Yields the neighbors of position."""
  for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
    yield position[0] + dx, position[1] + dy


def explore_island(position: Position, unvisited: set[Position]):
  """Removes positions from unvisited on the same island of 'position'."""
  unvisited.remove(position)
  for neighbor in neighbors(position):
    if neighbor in unvisited:
      explore_island(neighbor, unvisited)


class IslandCountTestCase(unittest.TestCase):

  def test_count1(self):
    self.assertEqual(island_count('0'), 0)

  def test_count2(self):
    self.assertEqual(island_count('1'), 1)

  def test_count3(self):
    self.assertEqual(island_count('010',
                                  '000',
                                  '010'), 2)

  def test_count4(self):
    self.assertEqual(island_count('011',
                                  '000',
                                  '010'), 2)

  def test_count5(self):
    self.assertEqual(island_count('011',
                                  '010',
                                  '010'), 1)

  def test_count6(self):
    self.assertEqual(island_count('0101',
                                  '1100',
                                  '0010',
                                  '0010'), 3)

