"""
TETRIS

https://en.wikipedia.org/wiki/Tetromino
https://tetris.fandom.com/wiki/SRS
https://tetris.fandom.com/wiki/Tetris_Guideline

Playfield   : just a grid with all the tetrominoes, each cell has one letter value
FallingPiece: information about the piece about to fall
TetrisEngine: all the Tetris logic

"""

from enum import Enum, IntEnum, unique
import random

@unique
class TetrominoColor(Enum):
    NONE = "#F4F0EC"     # Isabelline
    BLUE = "#325BBA"     # Dark cornflower blue
    CYAN = "#188BC2"     # Cyan cornflower blue
    PURPLE = "#915C83"   # Antique fuchsia
    RED = "#CC0002"      # Boston University Red
    ORANGE = "#F28500"   # Tangerine
    GREEN = "#289D8C"    # Deep aquamarine
    YELLOW = "#DEB887"   # Burlywood
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
            { "angles": [ 0   ], "relative_coordinates": [ [0, 0], [-1,  0], [1,  0], [ 1,  1] ] },
            { "angles": [ 90  ], "relative_coordinates": [ [0, 0], [ 0,  1], [0, -1], [ 1, -1] ] },
            { "angles": [ 180 ], "relative_coordinates": [ [0, 0], [-1,  0], [1,  0], [-1, -1] ] },
            { "angles": [ 270 ], "relative_coordinates": [ [0, 0], [ 0,  1], [0, -1], [-1,  1] ] }
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
        "height": 22,
        "hidden_top_rows": 2,
        "background_color": "grey",
        "falling_piece": {
            "starting_x": 5,
            "starting_y": 20,
            "gravity_speed": 2000 # ms
        }
    }
}

class Playfield:
   
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.clear()

    def get_grid_coordinates(self, x :int, y :int) -> list:
        """
        Playfield coordinates to internal grid coordinates
        Playfield (x,y) = (1,1) is the left bottom corner
        """
        return [x - 1, self.height - y]

    def clear(self) -> None:
        self.grid = [[str(TetrominoShape.NONE)] * self.width for y in range(self.height)]

    def clear_full_lines(self) -> int:
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

        return lines_cleared

    def get_block(self, x :int, y :int) -> str:
        [grid_x, grid_y] = self.get_grid_coordinates(x, y)
        return self.grid[grid_y][grid_x]

    def get_row(self, y :int) -> list:
        """ Bottom row is row y=1 """
        [_, grid_y] = self.get_grid_coordinates(1, y)
        return self.grid[grid_y]

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
        [grid_x, grid_y] = self.get_grid_coordinates(x, y)
        self.grid[grid_y][grid_x] = str(shape)

    def __str__(self) -> str:
        """ Useful for debugging to dump to the command line the grid values """
        grid = ""
        for row in self.grid:
            line = ""
            for block in row:
                line = line + " " + (block if block != str(TetrominoShape.NONE) else "•")
            grid = grid + line + '\n'
        return grid
class FallingPiece:

    def __init__(self, shape :TetrominoShape) -> None:
        self.tetrominoes = config["tetrominoes"]
        self.set_new_falling_piece(shape)

    def __str__(self) -> str:
        return f'{self.shape} - {self.angle}°'

    def get_absolute_coordinates(self, center_x :int, center_y :int):
        return [ [center_x + relative_x, center_y + relative_y] for relative_x, relative_y in self.relative_coordinates]

    def get_current_absolute_coordinates(self):
        return self.get_absolute_coordinates(self.center_x, self.center_y)

    def get_relative_coordinates(self, angle :int) -> any:
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

    def set_angle(self, angle :int) -> None:
        self.angle = angle
        self.relative_coordinates = self.get_relative_coordinates(self.angle)

    def set_new_falling_piece(self, shape: TetrominoShape) -> None:
        self.set_shape(shape)
        self.set_angle(0)
        self.set_starting_position()

    def set_shape(self, shape: TetrominoShape) -> None:
        self.shape = shape

        data = next((tetromino for tetromino in self.tetrominoes if tetromino["shape"] == self.shape), None)
        self.orientations = data["orientations"]

    def set_starting_position(self) -> None:
        self.center_x = config["playfield"]["falling_piece"]["starting_x"]
        self.center_y = config["playfield"]["falling_piece"]["starting_y"]

class TetrisEngine:

    @unique
    class Events(IntEnum):
        ON_PLAYFIELD_UPDATED = 1,
        ON_LINES_CLEARED     = 2,
        ON_GAME_OVER         = 3

    def __init__(self) -> None:
        self.playfield = Playfield(config["playfield"]["width"], config["playfield"]["height"])
        self.playfield_with_falling_piece = Playfield(config["playfield"]["width"], config["playfield"]["height"])
        self.ghost_dropped_piece_coordinates = []

        next_shape = self.get_next_shape()
        self.falling_piece = FallingPiece(next_shape)

        self.event_bindings = {}
        self.enable_on_playfield_updated_event = True
        self.enable_on_lines_cleared_event = True
        self.enable_on_game_over_event = True

    def bind_event(self, event_name :Events, func:object) -> None:
        self.event_bindings[event_name] = func

    # todo can_have_new_piece(self)

    def can_move_falling_piece(self, new_center_x :int, new_center_y :int) -> bool:
        return all([
            self.playfield.is_block_available(x, y)
            for x, y in self.falling_piece.get_absolute_coordinates(new_center_x, new_center_y)
        ])

    def drop(self) -> None:
        while self.can_move_falling_piece(self.falling_piece.center_x, self.falling_piece.center_y - 1):
            self.move_falling_piece(self.falling_piece.center_x, self.falling_piece.center_y - 1)
        self.lock_falling_piece()
        self.raise_on_playfield_updated_event()

    def get_next_piece_or_game_over(self) -> None:
        self.get_next_piece()

        if self.can_move_falling_piece(self.falling_piece.center_x, self.falling_piece.center_y):
            self.raise_on_playfield_updated_event()
        else:            
            self.raise_on_game_over_event()

    def get_next_piece(self) -> None:
        next_shape = self.get_next_shape()
        self.falling_piece.set_new_falling_piece(next_shape)

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

    def lock_falling_piece(self) -> None:
        self.set_falling_piece(self.playfield)

        lines_cleared = self.playfield.clear_full_lines()
        if lines_cleared > 0:
            self.raise_on_lines_cleared_event(lines_cleared)
        
        self.get_next_piece_or_game_over()

    def move_down(self) -> None:
        """ It moves the falling piece down if it can (it returns true) otherwise it returns false """
        if self.can_move_falling_piece(self.falling_piece.center_x, self.falling_piece.center_y - 1):
            self.move_falling_piece(self.falling_piece.center_x, self.falling_piece.center_y - 1)
        else:
            self.lock_falling_piece()
        self.raise_on_playfield_updated_event()

    def move_falling_piece(self, new_center_x :int, new_center_y :int) -> None:
        self.falling_piece.center_x = new_center_x
        self.falling_piece.center_y = new_center_y

    def move_left(self) -> bool:
        """ It moves the falling piece to the left if it can (it returns true) otherwise it returns false """
        if self.can_move_falling_piece(self.falling_piece.center_x - 1, self.falling_piece.center_y):
            self.move_falling_piece(self.falling_piece.center_x - 1, self.falling_piece.center_y)
            self.raise_on_playfield_updated_event()
            return True
        else:
            return False

    def move_right(self) -> bool:
        """ It moves the falling piece to the right if it can (it returns true) otherwise it returns false """
        if self.can_move_falling_piece(self.falling_piece.center_x + 1, self.falling_piece.center_y):
            self.move_falling_piece(self.falling_piece.center_x + 1, self.falling_piece.center_y)
            self.raise_on_playfield_updated_event()
            return True
        else:
            return False

    def rotate_left(self) -> bool:
        """ It rotates the falling piece to the left if it can (it returns true) otherwise it returns false """
        self.falling_piece.rotate_left()
        if not self.can_move_falling_piece(self.falling_piece.center_x, self.falling_piece.center_y):
            self.falling_piece.rotate_right()
            return False
        else:
            self.raise_on_playfield_updated_event()
            return True

    def rotate_right(self) -> bool:
        """ It rotates the falling piece to the right if it can (it returns true) otherwise it returns false """
        self.falling_piece.rotate_right()
        if not self.can_move_falling_piece(self.falling_piece.center_x, self.falling_piece.center_y):
            self.falling_piece.rotate_left()
            return False
        else:
            self.raise_on_playfield_updated_event()
            return True

    def raise_on_game_over_event(self) -> None:
        if self.enable_on_game_over_event:
            self.event_bindings[TetrisEngine.Events.ON_GAME_OVER]()

    def raise_on_lines_cleared_event(self, lines :int) -> None:
        if self.enable_on_lines_cleared_event:
            self.event_bindings[TetrisEngine.Events.ON_LINES_CLEARED](lines)

    def raise_on_playfield_updated_event(self) -> None:
        if not self.enable_on_playfield_updated_event:
            return
            
        # print(str(self.playfield)) # for debugging
        # merge together the playfield with the falling piece into a playfield we can send to the UI
        self.playfield_with_falling_piece.grid = [row[:] for row in self.playfield.grid]
        self.set_falling_piece(self.playfield_with_falling_piece)
        self.ghost_dropped_piece_coordinates = [
            self.playfield.get_grid_coordinates(x,y) for x, y in self.get_ghost_dropped_piece_coordinates()]

        self.event_bindings[TetrisEngine.Events.ON_PLAYFIELD_UPDATED]()

    def get_ghost_dropped_piece_coordinates(self) -> list:
        center_x = self.falling_piece.center_x
        center_y = self.falling_piece.center_y
        while self.can_move_falling_piece(center_x, center_y - 1):
            center_y -= 1
        return self.falling_piece.get_absolute_coordinates(center_x, center_y)

    def new_game(self) -> None:
        self.playfield.clear()
        self.falling_piece.set_starting_position()
        self.raise_on_playfield_updated_event()

    def set_falling_piece(self, playfield :Playfield) -> None:
        for x, y in self.falling_piece.get_current_absolute_coordinates():
            playfield.set_block(x, y, self.falling_piece.shape)
