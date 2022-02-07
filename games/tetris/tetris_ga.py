# Tetris Genetic algorithms UI
from turtle import bgcolor
from tetris_playable import PlayfieldScreen, config
from tetris_agent import TetrisAgent
from tetris_engine import TetrisEngine
import tkinter as tk
import tkinter.ttk as ttk
import multiprocessing as mp

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI Games - Tetris Genetic algorithms")
        self.geometry("1000x580")
        
        self.playfield_frame = PlayfieldFrame(self, width=200, height=300, bg="pink")
        self.playfield_frame.place(x=10, y=10)

        exit_button = ttk.Button(self, text="Exit", command=exit) # TODO stop everything gracefully
        exit_button.place(x=20, y=540)

        fps = 10 # frames per second i.e. movements in the playfield stored in the queue
        self.speed = int(1000/fps)
        
        weights = {
            "weight_aggregated_height":  5,
            "weight_total_holes":        1.1,
            "weight_bumpiness":          0.8,
            "weight_lines_cleared":    -10
        }
        
        self.queue = mp.Queue() # the queue doesn't need to be top-level like 'run_agent'
        self.p1 = mp.Process(target=run_agent, args=(weights, 100, self.queue))
        self.p1.start()
        # self.p1.join()
        print("joined")

        self.update_playfield_timer = self.after(500, self.update_playfield)

    def exit(self) -> None:
        self.destroy()

    def update_playfield(self) -> None:
        """
        The Tetris Agent is really fast and we won't be able to see in the UI all the movements.
        The easiest way to deal with this is to let the agent run and queue all the data for updating the playfield
        in a queue and with a timer start getting elements until the queue is empty.
        """
        if self.queue.empty():
            print("it is empty")
            self.after_cancel(self.update_playfield_timer)
        else:
            data = self.queue.get()
            self.playfield_frame.update(data)
            self.after(self.speed, self.update_playfield) # Call again the timer

# It has to be top-level or we will get an error when starting the process:
# TypeError: cannot pickle '_tkinter.tkapp' object
def run_agent(weights: dict, max_number_of_movements :int, queue :mp.Queue) -> None:        
    agent = TetrisAgent()
    agent.bind_event(TetrisEngine.Events.ON_PLAYFIELD_UPDATED, lambda data: queue.put(data))
    agent.start_new_game(weights, max_number_of_movements)
    print(f"the queue is {queue.qsize()}")

class PlayfieldFrame(tk.Frame):
    def __init__(self, master, width :int, height :int, **kwargs):
        self.width = width
        self.height = height
        super().__init__(master, width=self.width, height=self.height, **kwargs)

        self.playfield_screen = PlayfieldScreen(self,
            config["playfield"]["columns"],
            config["playfield"]["rows"],
            config["playfield"]["background_color"],
            config["tetrominoes"])
        self.scale_down_playfield_screen(self.playfield_screen)
        self.playfield_screen.place(x=50, y=50)
    
    def scale_down_playfield_screen(self, playfield_screen :PlayfieldScreen) -> None:
        """
        The original playfield is bigger because it is the one used for the playable Tetris
        So instead of copy/paste and make modifications we are using the same class
        but scaling down after every update
        """
        original_width = playfield_screen.width
        original_height = playfield_screen.height
        scale = 0.25 # 1/4 of the size which means that width is half and height is half
        new_width = original_width // 2
        new_height = original_height // 2
        playfield_screen.scale("all", 0, 0, scale*2, scale*2)       # It scales the contents but not the container
        playfield_screen.config(width=new_width, height=new_height) # It scales the container

    def update(self, data :dict) -> None:
        self.playfield_screen.draw(
            data["rows_from_the_bottom_up"],
            data["falling_piece_shape"],
            data["falling_piece_coordinates"],
            data["ghost_dropped_piece_coordinates"])
        self.scale_down_playfield_screen(self.playfield_screen)

if __name__ == "__main__":
    window = Window()
    window.mainloop()