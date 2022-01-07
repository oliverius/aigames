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
from tkinter import BooleanVar
from typing import Any, List # TODO remove when we are not dealing with terminals and we move to TK
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

class Playfield:

   EMPTY_BLOCK = "🔳"
   FULL_BLOCK = "⬜"
   
   def __init__(self, width: int, height: int) -> None:
       self.width = width
       self.height = height
       self.grid = self.get_initialized_grid()

   def get_block(self, x: int, y: int) -> str:
      return self.grid[self.height - y][x - 1] # Coordinate system with (x,y) = (1,1) as left-bottom corner

   def get_initialized_grid(self) -> List:
      return [[Playfield.EMPTY_BLOCK] * self.width for y in range(self.height)]

   def is_block_available(self, x: int, y: int) -> bool:
      # Order is important. First check for the boundaries and later if it is empty
      # If we do the opposite we may check for a (x,y) that doesn't exist and will error
      return self.is_block_within_boundaries(x, y) and self.is_block_empty(x, y)

   def is_block_empty(self, x: int, y: int) -> bool:
      return self.get_block(x, y) == Playfield.EMPTY_BLOCK

   def is_block_within_boundaries(self, x :int, y: int) -> bool:
      return 1 <= x <= self.width and 1 <= y <= self.height

   def set_block(self, x: int, y: int, value) -> None:
      self.grid[self.height - y][x - 1] = value # Coordinate system with (x,y) = (1,1) as left-bottom corner

   def print_grid(self): # TODO remove this function when we do graphical grid
      printed_grid = ""
      for y in range(self.height):
         for x in range(self.width):
            printed_grid += str(self.grid[y][x]) + " "
         printed_grid += "\n"
      print(printed_grid)

class Tetris:

   FALLING_PIECE_STARTING_X = 5
   FALLING_PIECE_STARTING_Y = 19

   def __init__(self) -> None:
       self.playfield = Playfield(10, 20)
       self.falling_piece = self.get_next_falling_piece()

       x = Tetris.FALLING_PIECE_STARTING_X
       y = Tetris.FALLING_PIECE_STARTING_Y

       self.clear_screen()
       self.put_falling_piece(x, y)
       self.playfield.print_grid()

       key = "X"
       while (key != ""):
         key = input().upper()
         self.clear_screen()
         
         if key == "A":
            self.remove_falling_piece(x, y)
            if self.can_falling_piece_move(x - 1, y):
               x -= 1
            self.put_falling_piece(x, y)

         elif key == "D":
            self.remove_falling_piece(x, y)
            if self.can_falling_piece_move(x + 1, y):
               x += 1
            self.put_falling_piece(x, y)

         elif key == "S":
            self.remove_falling_piece(x, y)
            if self.can_falling_piece_move(x, y - 1):
               y -= 1
            self.put_falling_piece(x, y)

         elif key == "K":
            self.remove_falling_piece(x, y)
            self.falling_piece.rotate_left()
            if not self.can_falling_piece_move(x, y):
               self.falling_piece.rotate_right()
            self.put_falling_piece(x, y)
            
         elif key == "L":
            self.remove_falling_piece(x, y)
            self.falling_piece.rotate_right()
            if not self.can_falling_piece_move(x, y):
               self.falling_piece.rotate_left()
            self.put_falling_piece(x, y)

         self.playfield.print_grid()

   def can_falling_piece_move(self, rotation_center_x :int, rotation_center_y :int) -> bool:
      return all([
         self.playfield.is_block_available(rotation_center_x + relative_x, rotation_center_y + relative_y)
         for relative_x, relative_y in self.falling_piece.current_relative_coordinates])

   def get_next_falling_piece(self) -> Tetromino:      
      return Tetromino(
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
   
   def put_falling_piece(self, rotation_center_x :int, rotation_center_y :int) -> None:
      self.set_falling_piece(rotation_center_x, rotation_center_y, Playfield.FULL_BLOCK)  

   def remove_falling_piece(self, rotation_center_x :int, rotation_center_y :int) -> None:
      self.set_falling_piece(rotation_center_x, rotation_center_y, Playfield.EMPTY_BLOCK)

   def set_falling_piece(self, rotation_center_x :int, rotation_center_y :int, value :str) -> None:
      for relative_x, relative_y in self.falling_piece.current_relative_coordinates:
         self.playfield.set_block(rotation_center_x + relative_x, rotation_center_y + relative_y, value)
   
   def clear_screen(self) -> None:
      os.system('cls' if os.name == 'nt' else 'clear') # TODO remove when we move to TK

# TODO graphics_board (the real game board)
Tetris()