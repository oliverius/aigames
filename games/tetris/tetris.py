"""
TETRIS
                 *
   *   *         *
** *   *  ** **  *  ***
** ** ** **   ** *   *

O  L  J  S   Z   I   T

https://en.wikipedia.org/wiki/Tetromino
https://tetris.fandom.com/wiki/SRS
https://tetris.fandom.com/wiki/Tetris_Guideline

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
   tetrominoes = [
      {
         "shape": TetrominoShape.I_SHAPE,             #
         "color": TetrominoColor.CYAN,                #
         "orientation": 0,                            #
         "coordinates": [[0,0], [0,1], [0,2], [0,3]]  #  O O O O
      },
      {
         "shape": TetrominoShape.J_SHAPE,             #
         "color": TetrominoColor.BLUE,                #
         "orientation": 0,                            #  O
         "coordinates": [[0,0], [0,1], [0,2], [0,3]]  #  O O O O
      },
      {
         "shape": TetrominoShape.L_SHAPE,             #
         "color": TetrominoColor.ORANGE,              #
         "orientation": 0,                            #        O
         "coordinates": [[0,0], [1,0], [0,1], [0,2]]  #  O O O O
      },
      {
         "shape": TetrominoShape.O_SHAPE,             #
         "color": TetrominoColor.YELLOW,              #
         "orientation": 0,                            #  O O
         "coordinates": [[0,0], [0,1], [0,2], [0,3]]  #  O O
      },
      {
         "shape": TetrominoShape.S_SHAPE,             #
         "color": TetrominoColor.GREEN,               #
         "orientation": 0,                            #    O O
         "coordinates": [[0,0], [0,1], [0,2], [0,3]]  #  O O
      },
      {
         "shape": TetrominoShape.T_SHAPE,             #
         "color": TetrominoColor.PURPLE,              #
         "orientation": 0,                            #    O
         "coordinates": [[0,0], [0,1], [0,2], [0,3]]  #  O O O
      },
      {
         "shape": TetrominoShape.Z_SHAPE,             #
         "color": TetrominoColor.RED,                 #
         "orientation": 0,                            #  O O
         "coordinates": [[0,0], [0,1], [0,2], [0,3]]  #    O O
      }
   ]
   def __init__(self, shape = TetrominoShape.NONE):
      data = next((tetromino for tetromino in self.tetrominoes if tetromino["shape"] == shape), None)
      self.shape = data["shape"]
      self.orientation = data["orientation"]
      self.color = data["color"]
      self.coordinates = data["coordinates"]

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
      self.grid = [["◻"] * self.width for i in range(self.height)]





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
      piece = self.get_next_falling_piece()


      self.board.print_grid()

   def can_falling_piece_move_left(self):
      pass

   def can_falling_piece_move_right(self):
      pass

   def can_falling_piece_move_down(self):
      pass

   def can_falling_piece_rotate_left(self):
      pass

   def can_falling_piece_rotate_right(self):
      pass

   def get_next_falling_piece(self) -> Tetromino:
      falling_piece = Tetromino(TetrominoShape.L_SHAPE)
      return falling_piece



game = TetrisGame()