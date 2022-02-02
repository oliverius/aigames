from tetris_engine import TetrisEngine, TetrominoColor, TetrominoShape
from tetris_engine import config
import tkinter as tk
import tkinter.ttk as ttk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI Games - Tetris")
        self.geometry("264x580")

        self.lines_cleared_text = tk.StringVar()
        self.reset_lines_cleared_counter()
        lines_cleared_label = ttk.Label(self, textvariable=self.lines_cleared_text)
        lines_cleared_label.place(x=20, y=480)

        self.game_over_text = tk.StringVar()
        self.game_over_text.set("")
        game_over_label = ttk.Label(self, textvariable=self.game_over_text)
        game_over_label.place(x=170, y=480)

        self.show_ghost_dropped_piece_checkbutton_value = tk.IntVar(value=1)
        show_ghost_dropped_piece_checkbutton = ttk.Checkbutton(self,
            text="Show ghost dropped piece",
            variable=self.show_ghost_dropped_piece_checkbutton_value,
            command=self.show_ghost)
        show_ghost_dropped_piece_checkbutton.place(x=20, y=500)

        exit_button = ttk.Button(self, text="Exit", command=self.exit)
        exit_button.place(x=20, y=540)

        new_game_button = ttk.Button(self, text="New game", command=self.new_game)
        new_game_button.place(x=170, y=540)

        self.bind('<KeyPress>', self.on_key_down)

        self.tetris_engine = TetrisEngine()
        self.tetris_engine.bind_event(TetrisEngine.Events.ON_PLAYFIELD_UPDATED, self.update_playfield)
        self.tetris_engine.bind_event(TetrisEngine.Events.ON_LINES_CLEARED, self.update_lines_cleared_counter)
        self.tetris_engine.bind_event(TetrisEngine.Events.ON_GAME_OVER, self.game_over)

        self.playfield_screen = PlayfieldScreen(self,
            config["playfield"]["columns"],
            config["playfield"]["rows"],
            config["playfield"]["background_color"],
            config["tetrominoes"])
        self.playfield_screen.place(x=20, y=20)

        self.gravity_speed = config["playfield"]["falling_piece"]["gravity_speed"]
        self.gravity_timer = None # It has to be define outside new_game or it will mess up after_cancel
                                # since the value will be None
        self.new_game()

    def exit(self) -> None:
        self.destroy()

    def execute_gravity(self) -> None:
        if self.is_game_over:
            self.stop_timer()
            return
        self.tetris_engine.move_down()
        self.gravity_timer = self.after(self.gravity_speed, self.execute_gravity)

    def game_over(self) -> None:
        self.is_game_over = True
        self.game_over_text.set("Game over")
   
    def new_game(self) -> None:
        self.is_game_over = False # Needed because we always had one more call to execute_gravity, starting the timer again
        
        self.stop_timer()
        self.reset_lines_cleared_counter()
        self.game_over_text.set("")
        self.focus_set() # This is important to avoid the button "new game" on focus when we press space bar while playing

        self.tetris_engine.new_game()
        
        self.execute_gravity()

    def on_key_down(self, event=None):
        if self.is_game_over:
            return
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

    def reset_lines_cleared_counter(self) -> None:
        self.total_lines_cleared = 0
        self.update_lines_cleared_counter(0)

    def show_ghost(self) -> None:
        self.focus_set()
        if self.show_ghost_dropped_piece_checkbutton_value.get() == 0:
            self.update_playfield()
            # It doesn't wait for next update to the playfield (after the timer)
            # to show the ghost piece or not, this feels more responsive

    def stop_timer(self) -> None:
        if self.gravity_timer:
            self.after_cancel(self.gravity_timer)

    def update_lines_cleared_counter(self, lines_cleared :int):
        self.total_lines_cleared += lines_cleared
        self.lines_cleared_text.set(f"Lines cleared: {self.total_lines_cleared}")

    def update_playfield(self, data :dict):        
        if self.show_ghost_dropped_piece_checkbutton_value.get() == 1:
            self.playfield_screen.draw(
                data["rows_from_the_bottom_up"],
                data["falling_piece_coordinates"],
                data["ghost_dropped_piece_coordinates"])
        else:
            self.playfield_screen.draw(
                data["rows_from_the_bottom_up"],
                data["falling_piece_coordinates"],
                [])

class PlayfieldScreen(tk.Canvas):
    def __init__(self, master, columns: int, rows: int, background_color :str, tetrominoes: any, **kwargs):
        self.width = 224
        self.height = 444
        self.background = background_color
        super().__init__(master, width=self.width, height=self.height, bg=self.background, **kwargs)

        self.columns = columns
        self.rows = rows

        # coordinates in pixels of (1,1)
        self.x1 = 4
        self.y1 = 400

        self.well_border_width = 2
        self.block_length = 20
        self.block_length_gap = 2
        
        self.build_color_dictionary(tetrominoes)
        self.clear()

    def build_color_dictionary(self, tetrominoes :any) -> None:
        self.colors_by_shape = {}
        self.colors_by_shape[str(TetrominoShape.NONE)] = str(TetrominoColor.NONE)
        for tetromino in tetrominoes:
            self.colors_by_shape[str(tetromino["shape"])] = str(tetromino["color"])

    def draw(self,
        rows_from_the_bottom_up :list[list[str]],
        falling_piece_coordinates :list[list] = [],
        ghost_dropped_piece_coordinates :list[list] = []) -> None:
        # The right thing to do is to tag each block and redraw only the ones that are different
        # i.e. different color. See this answer from comments: https://stackoverflow.com/a/15840231
        # But due to the simplicity of our grid and since I can't see any slowdown due to this,
        # we will delete all the graphics and redraw them in each frame
        self.delete("all")
        self.draw_well()
        self.draw_rows(rows_from_the_bottom_up)
        self.draw_falling_piece(falling_piece_coordinates)
        self.draw_ghost_dropped_piece(ghost_dropped_piece_coordinates)

    def clear(self) -> None:
        self.draw([[str(TetrominoShape.NONE)] * self.columns for y in range(self.rows)])

    def draw_block2(self, grid_x :int, grid_y :int, shape :TetrominoShape) -> None:
        x = self.x1 + grid_x * (self.block_length + self.block_length_gap)
        y = self.x1 + grid_y * (self.block_length + self.block_length_gap)
        color = self.colors_by_shape[shape]
        self.create_rectangle( (x, y, x + self.block_length, y + self.block_length), outline="black", fill=color)

    def draw_block(self, playfield_x :int, playfield_y :int, shape :str) -> None:
        x = self.x1 + (playfield_x - 1) * (self.block_length + self.block_length_gap)
        y = self.y1 - (playfield_y - 1) * (self.block_length + self.block_length_gap)
        color = self.colors_by_shape[shape]
        self.create_rectangle( (x, y, x + self.block_length, y + self.block_length), outline="black", fill=color)

    def draw_falling_piece(self, coordinates: list[list]) -> None:
        if not coordinates:
            return
        for x, y in coordinates:
            self.draw_block(x, y, str(TetrominoShape.I_SHAPE)) # TODO pass the shape in the dictionary

    def draw_ghost_dropped_piece(self, coordinates :list) -> None:
        if not coordinates:
            return
        # inset_px = 2
        # for grid_x, grid_y in ghost_dropped_piece_coordinates:
        #     visible_grid_y = grid_y - self.hidden_top_rows
        #     x = self.grid_x0 + grid_x * (self.block_length + self.block_length_gap)
        #     y = self.grid_x0 + visible_grid_y * (self.block_length + self.block_length_gap)
        #     color = "black"
        #     self.create_rectangle(
        #         (x + inset_px, y + inset_px, x + self.block_length - inset_px, y + self.block_length - inset_px),
        #         outline=color, fill="#D0D0D0")

    def draw_rows(self, rows: list[list[str]]) -> None:
        for y, row in enumerate(rows, start=1):
            for x, value in enumerate(row, start=1):
                self.draw_block(x, y, value)

    def draw_well(self):
        self.create_line(3, 0, 3, self.height, width=self.well_border_width, fill="black") # TODO why not 0 instead of 3 pixels to the right?
        self.create_line(0, self.height, self.width, self.height, width=self.well_border_width, fill="black")
        self.create_line(self.width, self.height, self.width, 0, width=self.well_border_width, fill="black")

if __name__ == "__main__":
    window = Window()
    window.mainloop()