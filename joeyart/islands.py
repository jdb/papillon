"""Let's count the number of islands on a 2D grid.

You are given a 2-dimensional map of tiles where each tile is either land or
water. You have to write a function that counts the number of islands. Two tiles
belong to the same island if they are both land and are adjacent horizontally
orvertically, but not diagonally. The input to your function is a tuple of
strings 2-dimensional array of booleans, where the character '0' means water and
the character '1' means land. The function should simply return the number of
islands.

"""

def count_islands(rows):
  raise NotImplementedError()


import unittest
class TestIslands(unittest.TestCase):
  def test_islands(self):
    tests = [
      (('0101000',
        '1101100',
        '1111001',
        '0000010'), 3),
      
      (('0101000',
        '1101100',
        '1101000'), 2),
      
      (('0101000',
        '1101100',
        '1101000',
        '1101001'), 3),
      
      (('0101000',
        '1101100',
        '1111001',
        '0000011'), 2),
      
      (('0111000',
        '0101100',
        '1101001',
        '0000011'), 2),
      
      (('0111011',
        '0001110',
        '1101001',
        '0000011'), 3),
      
      (('0101011',
        '0001110',
        '1101001',
        '0000011'), 4),
      
      (('0101011',
        '0001010',
        '1101001',
        '0000011'), 5),
      
      (('1111111',
        '1000001',
        '1000001',
        '1111111'), 1),
      
      (('1110110',
        '0100101',
        '1100110',
        '0000000'), 3),
      
      (('1100011',
        '0111010',
        '0001110',
        '0000100'), 1)]
    
    for grid, expected_count in tests:
      self.assertEqual(count_islands(grid), expected_count)

if __name__ == '__main__':
  unittest.main()

