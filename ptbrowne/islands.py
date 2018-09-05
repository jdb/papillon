#-*- coding: utf-8 -*-

class Grid:
  def __init__(self, grid_str):
    self.grid = [
      [int(x) for x in line.strip()]
      for line in grid_str.split('\n') if line.strip()
    ]
    self.nrows = len(self.grid)
    self.ncols = len(self.grid[0])

  def count_islands(self):
    """
    Returns the number of islands in the grid.

    Dynamic programming is used here, in one pass we go through 
    the grid and iterate over a triplet of cells (top, left, cur)
    to count the islands.

    O(n) to count the islands.
    """
    count = 0
    grid = self.grid

    earth = (
      (i, j) for i in range(self.nrows) for j in range(self.ncols)
      if self.grid[i][j]
    )
    neighbors = ((
      (i - 1, j), (i, j - 1), (i, j)
    ) for (i, j) in earth)

    islands = dict()
    island_id = 0
    for top, left, cur in neighbors:
      top_island, left_island = islands.get(top), islands.get(left)
      if not left_island and not top_island:
        # new island
        count += 1 
        island_id += 1
        islands[cur] = island_id # maybe we can use count here ?
      elif not (left_island and top_island):
        # merge with current island
        islands[cur] = left_island or top_island
      else:
        islands[cur] = top_island
        # join two islands
        if left_island != top_island:
          count -= 1
          islands[left] = top_island
    return count

  def __repr__(self):
    return '\n'.join(
      ''.join('█' if cell == 1 else ' ' for cell in row)
      for row in self.grid
    )

def test(grid_str, expected_count, verbose=False):
  grid = Grid(grid_str)
  count = grid.count_islands()
  ok = expected_count == count
  print('expected {}, got {} {}'.format(expected_count, count, '✅' if ok else '❌'))
  print(grid)


if __name__ == '__main__':
  test("""
    0101000
    1101100
    1111001
    0000010
  """, 3)

  test("""
    0101000
    1101100
    1101000
  """, 2)

  test("""
    0101000
    1101100
    1101000
    1101001
  """, 3)

  test("""
    0101000
    1101100
    1111001
    0000011
  """, 2)

  test("""
    0111000
    0101100
    1101001
    0000011
  """, 2)

  test("""
    0111011
    0001110
    1101001
    0000011
  """, 3)

  test("""
    0101011
    0001110
    1101001
    0000011
  """, 4)

  test("""
    0101011
    0001010
    1101001
    0000011
  """, 5)


  test("""
    1111111
    1000001
    1000001
    1111111
  """, 1)

  test("""
    1110110
    0100101
    1100110
    0000000
  """, 3)

  test("""
    1100011
    0111010
    0001110
    0000100
  """, 1)
