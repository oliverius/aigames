"""
TETRIS
                 *
   *   *         *
** *   *  ** **  *  ***
** ** ** **   ** *   *

O  L  J  S   Z   I   T

https://en.wikipedia.org/wiki/Tetromino

tetrominoes, name and shape (maybe colour as well)

"""

from enum import Enum, unique



tetrominoes = [




]

 # only possibles values is 0 (none) or one of the colours for the tetrominos
# in the wikipedia the colours are blue, cyan, purple, red, orange, green and yellow
# first test is to show the pieces on the screen and rotate them in the board.

@unique
class TetrominoColor(Enum):
   NONE = 0
   BLUE = 1
   CYAN = 2
   PURPLE = 3
   RED = 4
   ORANGE = 5
   GREEN = 6
   YELLOW = 7

@unique
class TetrominoShape(Enum):
   NONE = 0
   I_SHAPE = 1
   J_SHAPE = 2
   L_SHAPE = 3
   O_SHAPE = 4
   S_SHAPE = 5
   T_SHAPE = 6
   Z_SHAPE = 7



class Tetromino:
   def __init__(self):
      self.shape = TetrominoShape.NONE
      self.orientation = 0
      self.color = TetrominoColor.NONE

   def rotate_left():
      pass

   def rotate_right():
      pass

class Board:
   def __init__(self, width, height):
      self.width = width
      self.height = height
      self.grid = []
      self.initialize_grid()
      
   def initialize_grid(self):
      self.grid = [[0] * self.width for i in range(self.height)]

   def print_grid(self):
      printed_grid = ""
      for y in range(self.height):
         for x in range(self.width):
            printed_grid += str(self.grid[y][x]) + " "
         printed_grid += "\n"
      print(printed_grid)

class TetrisGame:
   def __init__(self) -> None:
      self.board = Board(10, 20)
      self.board.print_grid()

   def can_falling_piece_move_left():
      pass

   def can_falling_piece_move_right():
      pass

   def can_falling_piece_move_down():
      pass

   def can_falling_piece_rotate_left():
      pass

   def can_falling_piece_rotate_right():
      pass


game = TetrisGame()