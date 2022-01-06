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
import random
import os
from tkinter import BooleanVar # TODO remove when we are not dealing with terminals and we move to TK
# from tkinter import *

# screen = Tk()
# screen.title("Example with graphics")
# screen.geometry("500x500")
# welcome_text = Label(screen, text = "my first one")
# welcome_text.pack()
# screen.mainloop()


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
   # Based on https://tetris.fandom.com/wiki/SRS
   tetrominoes = [
      {
         "shape": TetrominoShape.I_SHAPE,
         "color": TetrominoColor.CYAN,
         "orientations": [
            { "angles": [  0, 180 ], "relative_coordinates": [ [0, 0], [-1,  0], [-2,  0], [1,  0] ] },
            { "angles": [ 90, 270 ], "relative_coordinates": [ [0, 0], [ 0,  1], [ 0,  2], [0, -1] ] }
         ]
      }, 
      {
         "shape": TetrominoShape.J_SHAPE,
         "color": TetrominoColor.BLUE,
         "orientations": [
            { "angles": [ 0   ], "relative_coordinates": [ [0, 0], [-1,  0], [-1,  1], [ 1,  0] ] },
            { "angles": [ 90  ], "relative_coordinates": [ [0, 0], [ 0, -1], [ 0,  1], [ 1,  1] ] },
            { "angles": [ 180 ], "relative_coordinates": [ [0, 0], [-1,  0], [ 1,  0], [ 1, -1] ] },
            { "angles": [ 270 ], "relative_coordinates": [ [0, 0], [ 0,  1], [ 0, -1], [-1, -1] ] }
         ]
      },
      {
         "shape": TetrominoShape.L_SHAPE,
         "color": TetrominoColor.ORANGE,
         "orientations": [
            { "angles": [ 0   ], "relative_coordinates": [ [0, 0], [-1,  0], [-1,  1], [ 1,  0] ] },
            { "angles": [ 90  ], "relative_coordinates": [ [0, 0], [ 0, -1], [ 0,  1], [ 1,  1] ] },
            { "angles": [ 180 ], "relative_coordinates": [ [0, 0], [-1,  0], [ 1,  0], [ 1, -1] ] },
            { "angles": [ 270 ], "relative_coordinates": [ [0, 0], [ 0,  1], [ 0, -1], [-1, -1] ] }
         ]
      },
      {
         "shape": TetrominoShape.O_SHAPE,
         "color": TetrominoColor.YELLOW,
         "orientations": [
            { "angles": [ 0, 90, 180, 270 ], "relative_coordinates": [ [0, 0], [0, 1], [1, 0], [1, 1] ] }
         ]
      },
      {
         "shape": TetrominoShape.S_SHAPE,
         "color": TetrominoColor.GREEN,
          "orientations": [
            { "angles": [ 0   ], "relative_coordinates": [ [0, 0], [-1,  0], [ 0,  1], [1,  1] ] },
            { "angles": [ 90  ], "relative_coordinates": [ [0, 0], [ 0,  1], [ 1,  0], [1, -1] ] },
            { "angles": [ 180 ], "relative_coordinates": [ [0, 0], [-1, -1], [ 0, -1], [1,  0] ] },
            { "angles": [ 270 ], "relative_coordinates": [ [0, 0], [-1,  0], [-1,  1], [0, -1] ] }
         ]
      },
      {
         "shape": TetrominoShape.T_SHAPE,
         "color": TetrominoColor.PURPLE,
         "orientations": [
            { "angles": [ 0   ], "relative_coordinates": [ [0, 0], [-1,  0], [1,  0], [0,  1] ] },
            { "angles": [ 90  ], "relative_coordinates": [ [0, 0], [ 0,  1], [0, -1], [1,  0] ] },
            { "angles": [ 180 ], "relative_coordinates": [ [0, 0], [-1,  0], [1,  0], [0, -1] ] },
            { "angles": [ 270 ], "relative_coordinates": [ [0, 0], [-1,  0], [0,  1], [0, -1] ] }
         ]
      },
      {
         "shape": TetrominoShape.Z_SHAPE,
         "color": TetrominoColor.RED,
         "orientations": [
            { "angles": [ 0   ], "relative_coordinates": [ [0, 0], [ 0,  1], [-1,  1], [1,  0] ] },
            { "angles": [ 90  ], "relative_coordinates": [ [0, 0], [ 0, -1], [ 1,  0], [1,  1] ] },
            { "angles": [ 180 ], "relative_coordinates": [ [0, 0], [-1,  0], [ 0, -1], [1, -1] ] },
            { "angles": [ 270 ], "relative_coordinates": [ [0, 0], [-1,  0], [-1, -1], [0,  1] ] }
         ]
      }
   ]
   def __init__(self, shape = TetrominoShape.NONE):
      data = next((tetromino for tetromino in self.tetrominoes if tetromino["shape"] == shape), None)
      self.shape = data["shape"]
      self.color = data["color"]
      self.orientations = data["orientations"]

      self.current_angle = 0
      self.current_relative_coordinates = self.get_relative_coordinates(0)

   def get_relative_coordinates(self, angle = 0):
      data = next((orientation for orientation in self.orientations if angle in orientation["angles"]), None)
      return data["relative_coordinates"]

   def rotate_left(self):
      self.current_angle -= 90
      if self.current_angle == -90 : self.current_angle = 270
      self.current_relative_coordinates = self.get_relative_coordinates(self.current_angle)

   def rotate_right(self):
      self.current_angle += 90
      if self.current_angle == 360 : self.current_angle = 0
      self.current_relative_coordinates = self.get_relative_coordinates(self.current_angle)

class Board:
   EMPTY_SYMBOL = "🔳"


   def __init__(self, width, height):
      self.width = width
      self.height = height
      self.internal_board = []
      self.initialize_internal_board() # todo board is really 22 height but the upper 2 lines are invisible and that's where we drop the pieces
      self.falling_piece = {}
      self.falling_piece_x = 0
      self_falling_piece_y = 0
      
   def initialize_internal_board(self) -> None:
      self.internal_board = [[Board.EMPTY_SYMBOL] * self.width for y in range(self.height)]

      # coordinate system where bottom-left corner is (1,1)
      self.internal_board_x = lambda x: x - 1
      self.internal_board_y = lambda y: self.height - y

   def can_falling_piece_move(self, offset_x, offset_y) -> BooleanVar:
      can_move = True
      for coords in self.falling_piece.current_relative_coordinates:
         pass

      return can_move

   def can_falling_piece_move_down(self):
      pass

   def can_falling_piece_move_left(self):
      
      pass

   def can_falling_piece_move_right(self):
      pass

   def can_falling_piece_rotate_left(self):
      pass

   def can_falling_piece_rotate_right(self):
      pass   

   def draw_piece(self, piece, x = 0, y = 0, symbol = EMPTY_SYMBOL) -> None:
      for coords in piece.current_relative_coordinates:
         relative_x = coords[0]
         relative_y = coords[1]
         self.set_internal_board_symbol(x + relative_x, y + relative_y, symbol)

   def draw_falling_piece(self, falling_piece, x = 0, y = 0) -> None:
      self.draw_piece(falling_piece, x, y, "⬜")

   def erase_falling_piece(self, falling_piece, x = 0, y = 0) -> None:
      self.draw_piece(falling_piece, x, y, Board.EMPTY_SYMBOL)

   def get_internal_board_symbol(self, x: int, y: int) -> str:
      return self.internal_board[self.internal_board_y(y)][self.internal_board_x(x)]

   def print_grid(self):
      printed_grid = ""
      for y in range(self.height):
         for x in range(self.width):
            printed_grid += str(self.internal_board[y][x]) + " "
         printed_grid += "\n"
      print(printed_grid)

   def set_internal_board_symbol(self, x: int, y: int, symbol: str) -> None:
      self.internal_board[self.internal_board_y(y)][self.internal_board_x(x)] = symbol
class TetrisGame:

   FALLING_PIECE_STARTING_X = 5
   FALLING_PIECE_STARTING_Y = 18

   def __init__(self) -> None:
      self.board = Board(10, 20)
      falling_piece = self.get_next_falling_piece()

      self.clear_screen()
      self.board.print_grid()
      key = " "
      starting_x = 5
      starting_y = 6   
      while (key != ""):
         offset_x = 0
         offset_y = 0
         key = input()
         key = key.upper()
         self.clear_screen()
         self.board.erase_falling_piece(falling_piece, starting_x, starting_y)
         
         if key == "A":   offset_x = -1
         elif key == "D": offset_x = 1
         elif key == "S": offset_y = -1
         elif key == "K": falling_piece.rotate_left()
         elif key == "L": falling_piece.rotate_right()

         starting_x = starting_x + offset_x
         starting_y = starting_y + offset_y       
         self.board.draw_falling_piece(falling_piece, starting_x, starting_y)
         self.board.print_grid()

   def clear_screen(self) -> None:
     os.system('cls' if os.name == 'nt' else 'clear') # TODO remove when we move to TK

   def get_next_falling_piece(self) -> Tetromino:
      #falling_piece = Tetromino(TetrominoShape.L_SHAPE) # TODO random shapes
      falling_piece = Tetromino(
         random.choice([
            TetrominoShape.I_SHAPE,
            TetrominoShape.J_SHAPE,
            TetrominoShape.L_SHAPE,
            TetrominoShape.O_SHAPE,
            TetrominoShape.S_SHAPE,
            TetrominoShape.T_SHAPE,
            TetrominoShape.Z_SHAPE
         ])
      )
      return falling_piece

TetrisGame()
# TODO graphics_board (the real game board)