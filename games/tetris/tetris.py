"""
TETRIS

https://en.wikipedia.org/wiki/Tetromino
https://tetris.fandom.com/wiki/SRS
https://tetris.fandom.com/wiki/Tetris_Guideline

"""

from enum import Enum, unique
import random
from typing import Any, List # TODO remove when we are not dealing with terminals and we move to TK
import tkinter as tk

@unique
class TetrominoColor(Enum):
   NONE = "#E8E8E8"
   BLUE = "blue"
   CYAN = "cyan"
   PURPLE = "purple"
   RED = "red"
   ORANGE = "orange"
   GREEN = "green"
   YELLOW = "yellow"
   def __str__(self) -> str:
      return self.value

@unique
class TetrominoShape(Enum):
   NONE = " "
   I_SHAPE = "I"
   J_SHAPE = "J"
   L_SHAPE = "L"
   O_SHAPE = "O"
   S_SHAPE = "S"
   T_SHAPE = "T"
   Z_SHAPE = "Z"
   def __str__(self) -> str:
       return self.value

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
      "background_color": "grey",
      "falling_piece": {
         "starting_x": 5,
         "starting_y": 19
      }
   }
}

class Playfield:
   
   def __init__(self, width: int, height: int) -> None:
       self.width = width
       self.height = height
       self.grid = [[str(TetrominoShape.NONE)] * self.width for y in range(self.height)]

   def clear_full_lines(self) -> None:
      """
      It is difficult to remove elements (full lines) from a grid.
      It is safer to create a new grid without those full lines
      and later add empty lines at the top to replace the full lines removed
      """
      new_grid = [ self.grid[y].copy() for y in range(self.height) if str(TetrominoShape.NONE) in self.grid[y] ]
      
      lines_cleared = self.height - len(new_grid)
      for _ in range(lines_cleared):
         new_grid.insert(0, [str(TetrominoShape.NONE)] * self.width)

      self.grid = new_grid

   def get_block(self, x: int, y: int) -> str:
      return self.grid[self.height - y][x - 1] # Coordinate system with (x,y) = (1,1) as left-bottom corner

   def is_block_available(self, x: int, y: int) -> bool:
      """
      Order is important. First check for the boundaries and later if it is empty.
      If we do the opposite we may check for a (x,y) that doesn't exist and will error
      """
      return self.is_block_within_boundaries(x, y) and self.is_block_empty(x, y)

   def is_block_empty(self, x: int, y: int) -> bool:
      return self.get_block(x, y) == str(TetrominoShape.NONE)

   def is_block_within_boundaries(self, x :int, y: int) -> bool:
      return 1 <= x <= self.width and 1 <= y <= self.height

   def set_block(self, x: int, y: int, shape: TetrominoShape) -> None:
      self.grid[self.height - y][x - 1] = str(shape) # Coordinate system with (x,y) = (1,1) as left-bottom corner

class Falling_Piece:

   def __init__(self, shape :TetrominoShape, tetrominoes_data :list) -> None:
      self.tetrominoes_data = tetrominoes_data
      self.set_shape(shape)
      self.set_starting_position()

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

   def set_starting_position(self) -> None:
      self.center_x = config["playfield"]["falling_piece"]["starting_x"]
      self.center_y = config["playfield"]["falling_piece"]["starting_y"]

class TetrisEngine:

   def __init__(self, cfg: object) -> None:
      self.playfield = Playfield(cfg["playfield"]["width"], cfg["playfield"]["height"])
      
      next_shape = self.get_next_shape()
      self.falling_piece = Falling_Piece(next_shape, cfg["tetrominoes"])

      self.events = {
         "keyboard_event": object # TODO one before clear lines and one after
      }

   def can_falling_piece_move(self, center_x :int, center_y :int) -> bool:
      return all([
         self.playfield.is_block_available(x, y)
         for x, y in self.falling_piece.get_absolute_coordinates(center_x, center_y)
      ]) 

   def drop(self) -> None:
      self.remove_falling_piece()
      
      while self.can_falling_piece_move(self.falling_piece.center_x, self.falling_piece.center_y - 1):
         self.falling_piece.center_y -= 1
      self.put_falling_piece()
      next_shape = self.get_next_shape()
      self.falling_piece.set_shape(next_shape)
      self.falling_piece.set_starting_position()
      self.playfield.clear_full_lines()
      
      self.put_falling_piece()
      self.raise_keyboard_event()

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
   
   def move_down(self) -> None:
      self.remove_falling_piece()
      
      if self.can_falling_piece_move(self.falling_piece.center_x, self.falling_piece.center_y - 1):
         self.falling_piece.center_y -= 1
      else:
         self.put_falling_piece()
         next_shape = self.get_next_shape()
         self.falling_piece.set_shape(next_shape)
         self.falling_piece.set_starting_position()
         self.playfield.clear_full_lines()
      
      self.put_falling_piece()
      self.raise_keyboard_event()

   def move_left(self) -> None:
      self.remove_falling_piece()

      if self.can_falling_piece_move(self.falling_piece.center_x - 1, self.falling_piece.center_y):
         self.falling_piece.center_x -= 1 
      
      self.put_falling_piece()
      self.raise_keyboard_event()

   def move_right(self) -> None:
      self.remove_falling_piece()
      
      if self.can_falling_piece_move(self.falling_piece.center_x + 1, self.falling_piece.center_y):
         self.falling_piece.center_x += 1 
      
      self.put_falling_piece()
      self.raise_keyboard_event()

   def rotate_left(self) -> None:
      self.remove_falling_piece() # remove_falling_piece inside "can_falling_Piece_move"
      
      self.falling_piece.rotate_left()
      if not self.can_falling_piece_move(self.falling_piece.center_x, self.falling_piece.center_y):
         self.falling_piece.rotate_right()
      
      self.put_falling_piece()
      self.raise_keyboard_event()

   def rotate_right(self) -> None:
      self.remove_falling_piece() # remove_falling_piece inside "can_falling_Piece_move"
      
      self.falling_piece.rotate_right()
      if not self.can_falling_piece_move(self.falling_piece.center_x, self.falling_piece.center_y):
         self.falling_piece.rotate_left()
      
      self.put_falling_piece()
      self.raise_keyboard_event()

   def put_falling_piece(self) -> None:
      self.set_falling_piece(self.falling_piece.shape)  

   def remove_falling_piece(self) -> None:
      self.set_falling_piece(TetrominoShape.NONE)

   def raise_keyboard_event(self) -> None:
      self.events["keyboard_event"](self.playfield.grid)

   def run(self):      

      self.put_falling_piece()
      self.raise_keyboard_event()

   def set_event_handler(self, event_name :str, function :object) -> None:
      self.events[event_name] = function

   def set_falling_piece(self, shape :TetrominoShape) -> None:
      for x, y in self.falling_piece.get_absolute_coordinates(self.falling_piece.center_x, self.falling_piece.center_y):
         self.playfield.set_block(x, y, shape)

class Window(tk.Tk):
   def __init__(self):
      super().__init__()
      self.title("AI Games - Tetris")
      self.geometry("800x600")

      exit_button = tk.Button(self, text="Exit", command=self.exit)
      exit_button.pack(side=tk.BOTTOM, padx=(20,0), pady=(0,20))

      print_button = tk.Button(self, text="Print grid", command=self.print_grid)
      print_button.pack(side=tk.BOTTOM, padx=(20,0), pady=(0,20))

      self.playfield_screen = Playfield_Screen(self)
      self.playfield_screen.pack(side=tk.TOP, anchor=tk.N)

      self.tetris_engine = TetrisEngine(config)
      self.tetris_engine.set_event_handler("keyboard_event", self.test_event) # rename it as bind, as in Tkinter
      
      self.bind('<KeyPress>', self.on_key_down)

      self.tetris_engine.run()

   def print_grid(self):
      printed_grid = ""
      for y in range(self.tetris_engine.playfield.height):
         for x in range(self.tetris_engine.playfield.width):
            printed_grid = printed_grid + self.tetris_engine.playfield.grid[y][x] + " "
         printed_grid += "\n"
      print(printed_grid)

   def exit(self):
      self.destroy()

   def test_event(self, tetris_engine_playfield_grid :list):
      self.playfield_screen.draw(tetris_engine_playfield_grid)

   def on_key_down(self, event=None):
      key = event.keysym
      if key == "Left":
         self.tetris_engine.move_left()
      elif key == "Right":
         self.tetris_engine.move_right()
      elif key == "Down":
         self.tetris_engine.move_down()
      elif key == "space":
         self.tetris_engine.drop()
      elif key == "z":
         self.tetris_engine.rotate_left()
      elif key == "x":
         self.tetris_engine.rotate_right()

class Playfield_Screen(tk.Canvas):
   def __init__(self, master, **kwargs):
      self.width = 224
      self.height = 444
      self.background = config["playfield"]["background_color"]
      super().__init__(master, width=self.width, height=self.height, bg=self.background, **kwargs)

      self.grid_width = 10
      self.grid_height = 20

      self.grid_x0 = 4
      self.grid_y0 = 4
      self.well_border_width = 2
      self.block_length = 20
      self.block_length_gap = 2
      
      self.build_color_dictionary()
      self.draw_blank_grid()

   def build_color_dictionary(self) -> None:
      self.colors_by_shape = {}
      self.colors_by_shape[" "] = str(TetrominoColor.NONE)
      for tetromino in config["tetrominoes"]:
         self.colors_by_shape[str(tetromino["shape"])] = str(tetromino["color"])

   def draw(self, grid :list) -> None:
      # TODO erase all before every frame. Read this https://stackoverflow.com/a/15840231
      # Probably better just changing color of blocks if they are different from before?
      # Need to have a copy of previous playfield, or just check colors of what we have in the current grid internally?
      # For now I will erase all
      self.delete("all")
      self.draw_well()
      self.draw_grid(grid)

   def draw_blank_grid(self) -> None:
      self.draw([[str(TetrominoShape.NONE)] * self.grid_width for y in range(self.grid_height)])

   def draw_block(self, grid_x :int, grid_y :int, shape :TetrominoShape) -> None:
      x = self.grid_x0 + grid_x * (self.block_length + self.block_length_gap)
      y = self.grid_x0 + grid_y * (self.block_length + self.block_length_gap)
      color = self.colors_by_shape[shape]
      self.create_rectangle( (x, y, x + self.block_length, y + self.block_length), outline="black", fill=color)

   def draw_grid(self, grid :list) -> None:
      for y in range(self.grid_height):
         for x in range(self.grid_width):
            shape = grid[y][x]
            self.draw_block(x, y, shape)

   def draw_well(self):
      self.create_line(3, 0, 3, self.height, width=self.well_border_width, fill="black") # TODO why not 0 instead of 3 pixels to the right?
      self.create_line(0, self.height, self.width, self.height, width=self.well_border_width, fill="black")
      self.create_line(self.width, self.height, self.width, 0, width=self.well_border_width, fill="black")

if __name__ == "__main__":
   window = Window()
   window.mainloop()
