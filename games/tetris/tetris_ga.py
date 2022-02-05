# Tetris Genetic algorithms UI
from tetris_standalone_game import PlayfieldScreen, config
from tetris_agent import TetrisAgent
import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI Games - Tetris Genetic algorithms")
        self.geometry("1000x580")

        self.playfield_screen_1 = self.get_playfield(20, 20)
        self.playfield_screen_2 = self.get_playfield(200, 20)

        agent = TetrisAgent()
        weights = {
            "weight_aggregated_height":   5,
            "weight_total_holes":         1.1,
            "weight_bumpiness":           0.8,
            "weight_lines_cleared":    -10
        }
        #agent.start_new_game(weights)

    def get_playfield(self, x :int, y :int) -> PlayfieldScreen:
        playfield_screen = PlayfieldScreen(self,
            config["playfield"]["columns"],
            config["playfield"]["rows"],
            config["playfield"]["background_color"],
            config["tetrominoes"])
        original_width = playfield_screen.width
        original_height = playfield_screen.height
        scale = 0.25 # 1/4 of the size which means that width is half and height is half
        new_width = original_width // 2
        new_height = original_height // 2
        playfield_screen.scale("all", 0, 0, scale*2, scale*2)       # It scales the contents but not the container
        playfield_screen.config(width=new_width, height=new_height) # It scales the container
        
        playfield_screen.place(x=x, y=y)

        return playfield_screen

if __name__ == "__main__":
    window = Window()
    window.mainloop()