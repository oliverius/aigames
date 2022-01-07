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

config = {
   # Based on https://tetris.fandom.com/wiki/SRS
   "tetrominoes": [
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
   ],
   "playfield": {
      "width": 10,
      "height": 20,
      "falling_piece": {
         "starting_x": 5,
         "starting_y": 19
      },
      "blocks": {
          "empty_block": "🔳",
          "full_block" : "⬜"
      }
   }
}

class Playfield:
   
   def __init__(self, width: int, height: int, empty_block :str, full_block :str) -> None:
       self.width = width
       self.height = height
       self.empty_block = empty_block
       self.full_block = full_block
       self.grid = self.get_initialized_grid()

   def get_block(self, x: int, y: int) -> str:
      return self.grid[self.height - y][x - 1] # Coordinate system with (x,y) = (1,1) as left-bottom corner

   def get_initialized_grid(self) -> List:
      return [[self.empty_block] * self.width for y in range(self.height)]

   def is_block_available(self, x: int, y: int) -> bool:
      # Order is important. First check for the boundaries and later if it is empty
      # If we do the opposite we may check for a (x,y) that doesn't exist and will error
      return self.is_block_within_boundaries(x, y) and self.is_block_empty(x, y)

   def is_block_empty(self, x: int, y: int) -> bool:
      return self.get_block(x, y) == self.empty_block

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

class Falling_Piece:

   def __init__(self, shape :TetrominoShape, tetrominoes_data :list) -> None:
      self.center_x = 0
      self.center_y = 0
      
      self.tetrominoes_data = tetrominoes_data

      self.set_shape(shape)

   def get_absolute_coordinates(self, center_x :int, center_y :int):
      return [ [center_x + relative_x, center_y + relative_y] for relative_x, relative_y in self.relative_coordinates]

   def get_relative_coordinates(self, angle :int) -> Any:
      data = next((orientation for orientation in self.orientations if angle in orientation["angles"]), None)
      return data["relative_coordinates"]

   def rotate_left(self):
      self.angle -= 90
      if self.angle == -90 : self.angle = 270
      self.relative_coordinates = self.get_relative_coordinates(self.angle)

   def rotate_right(self):
      self.angle += 90
      if self.angle == 360 : self.angle = 0
      self.relative_coordinates = self.get_relative_coordinates(self.angle)

   def set_shape(self, shape: TetrominoShape) -> None:
      self.shape = shape

      data = next((tetromino for tetromino in self.tetrominoes_data if tetromino["shape"] == self.shape), None)
      self.orientations = data["orientations"]
      
      self.angle = 0
      self.relative_coordinates = self.get_relative_coordinates(self.angle)

class Tetris:

   def __init__(self, cfg: object) -> None:
      self.playfield = Playfield(
         cfg["playfield"]["width"],
         cfg["playfield"]["height"],
         cfg["playfield"]["blocks"]["empty_block"],
         cfg["playfield"]["blocks"]["full_block"])

      next_shape = self.get_next_shape()
      self.falling_piece = Falling_Piece(next_shape, cfg["tetrominoes"])
      
      self.falling_piece_starting_x = cfg["playfield"]["falling_piece"]["starting_x"]
      self.falling_piece_starting_y = cfg["playfield"]["falling_piece"]["starting_y"]

      x = self.falling_piece_starting_x
      y = self.falling_piece_starting_y

      self.clear_screen()
      self.put_falling_piece(x, y)
      self.playfield.print_grid()

      key = "X"
      while (key != ""):
         key = input().upper()
         
         self.clear_screen()
         self.remove_falling_piece(x, y)

         if key == "A":
            if self.can_falling_piece_move(x - 1, y):
               x -= 1            

         elif key == "D":
            if self.can_falling_piece_move(x + 1, y):
               x += 1

         elif key == "S":
            if self.can_falling_piece_move(x, y - 1):
               y -= 1

         elif key == "K":
            self.falling_piece.rotate_left()
            if not self.can_falling_piece_move(x, y):
               self.falling_piece.rotate_right()

         elif key == "L":
            self.falling_piece.rotate_right()
            if not self.can_falling_piece_move(x, y):
               self.falling_piece.rotate_left()

         elif key == " ":
            [x, y] = self.drop_falling_piece(x, y)
            self.put_falling_piece(x, y)

            x = self.falling_piece_starting_x
            y = self.falling_piece_starting_y
            next_shape = self.get_next_shape()
            self.falling_piece.set_shape(next_shape)

         self.put_falling_piece(x, y)
         self.playfield.print_grid()

   def can_falling_piece_move(self, center_x :int, center_y :int) -> bool:
      return all([
         self.playfield.is_block_available(x, y)
         for x, y in self.falling_piece.get_absolute_coordinates(center_x, center_y)])

   def drop_falling_piece(self, center_x :int, center_y :int) -> List:
      while self.can_falling_piece_move(center_x, center_y - 1):
         center_y -= 1
      return [center_x, center_y]

   def get_next_shape(self) -> TetrominoShape:
      return random.choice([
         TetrominoShape.I_SHAPE,
         TetrominoShape.J_SHAPE,
         TetrominoShape.L_SHAPE,
         TetrominoShape.O_SHAPE,
         TetrominoShape.S_SHAPE,
         TetrominoShape.T_SHAPE,
         TetrominoShape.Z_SHAPE
      ])
   
   def put_falling_piece(self, center_x :int, center_y :int) -> None:
      self.set_falling_piece(center_x, center_y, self.playfield.full_block)  

   def remove_falling_piece(self, center_x :int, center_y :int) -> None:
      self.set_falling_piece(center_x, center_y, self.playfield.empty_block)

   def set_falling_piece(self, center_x :int, center_y :int, value :str) -> None:
      for x, y in self.falling_piece.get_absolute_coordinates(center_x, center_y):
         self.playfield.set_block(x, y, value)
   
   def clear_screen(self) -> None:
      os.system('cls' if os.name == 'nt' else 'clear') # TODO remove when we move to TK

# TODO graphics_board (the real game board)
# TODO clear lines in playfield
# TODO get absolute coordinates in Falling_Piece and modify methods that have relative coordinates
Tetris(config)