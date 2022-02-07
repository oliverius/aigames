# Tetris Genetic algorithms UI
from turtle import bgcolor
from numpy import place
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
        self.geometry("1000x600")
        
        self.setup_playfield_frames()

        exit_button = ttk.Button(self, text="Exit", command=exit) # TODO stop everything gracefully
        exit_button.place(x=900, y=550)

        weights = {
            "weight_aggregated_height":  5,
            "weight_total_holes":        1.1,
            "weight_bumpiness":          0.8,
            "weight_lines_cleared":    -10
        }
        self.set_weight_labels(1, weights)

        fps = 10 # frames per second i.e. movements in the playfield stored in the queue
        self.speed = int(1000/fps)
        
        self.queue = mp.Queue() # the queue doesn't need to be top-level like 'run_agent'
        self.processes :list[mp.Process] = []
        self.event = mp.Event()
        p = mp.Process(target=run_agent, args=(weights, 100, self.queue), kwargs={'event': self.event})
        self.processes.append((p, self.event))
        for p, _ in self.processes:
            p.start()

        print("joined")

        self.update_playfield_timer = self.after(500, self.update_playfield)

    def exit(self) -> None:
        while not self.queue.empty():
            self.queue.get()
        for _, event in self.processes:
            event.set()
        for p, _ in self.processes:
            p.terminate()
            p.join()

        self.destroy()

    def set_weight_labels(self, agent_number :int, weights :dict) -> None:
        index = agent_number - 1
        self.playfield_frames[index].set_weight_labels(weights)

    def setup_playfield_frames(self) -> None:
        agent_number = 1
        self.playfield_frames :list[PlayfieldFrame] = []
        for y in range(2):
            for x in range(3):
                playfield_frame = PlayfieldFrame(self, width=310, height=250, bg="lightslategrey")

                x0 = 10 + (playfield_frame.width  + 20) * x
                y0 = 10 + (playfield_frame.height + 20) * y
                
                playfield_frame.set_agent_number_label(agent_number)
                #playfield_frame.set_weight_labels(weights)
                playfield_frame.place(x=x0, y=y0)
                
                self.playfield_frames.append(playfield_frame)
                agent_number += 1

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
            self.playfield_frames[0].update(data)
            self.after(self.speed, self.update_playfield) # Call again the timer

# It has to be top-level or we will get an error when starting the process:
# TypeError: cannot pickle '_tkinter.tkapp' object
def run_agent(weights: dict, max_number_of_movements :int, queue :mp.Queue, event=None) -> None:
    agent = TetrisAgent()
    agent.bind_event(TetrisEngine.Events.ON_PLAYFIELD_UPDATED, lambda data: queue.put(data))
    agent.start_new_game(weights, max_number_of_movements)
    print(f"the queue is {queue.qsize()}")

class PlayfieldFrame(tk.Frame):
    def __init__(self, master, width :int, height :int, **kwargs):
        self.width = width
        self.height = height
        super().__init__(master, width=self.width, height=self.height, borderwidth=2, relief="groove", **kwargs)

        x = 10
        y = 10

        self.playfield_screen = PlayfieldScreen(self,
            config["playfield"]["columns"],
            config["playfield"]["rows"],
            config["playfield"]["background_color"],
            config["tetrominoes"])
        self.scale_down_playfield_screen(self.playfield_screen)
        self.playfield_screen.place(x=x, y=y)

        x = 140

        self.agent_number_text = tk.StringVar()
        ttk.Label(self, textvariable=self.agent_number_text).place(x=x, y=y)

        self.weight_aggregated_height_text = tk.StringVar()
        ttk.Label(self, textvariable=self.weight_aggregated_height_text).place(x=x, y=y+20)

        self.weight_total_holes_text = tk.StringVar()
        ttk.Label(self, textvariable=self.weight_total_holes_text).place(x=x, y=y+40)

        self.weight_bumpiness_text = tk.StringVar()
        ttk.Label(self, textvariable=self.weight_bumpiness_text).place(x=x, y=y+60)

        self.weight_lines_cleared_text = tk.StringVar()
        ttk.Label(self, textvariable=self.weight_lines_cleared_text).place(x=x, y=y+80)

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

    def set_agent_number_label(self, agent_number: int) -> None:
        self.agent_number_text.set(f"Agent #{agent_number}")
    
    def set_weight_labels(self, weights :dict) -> None:
        self.weight_aggregated_height_text.set(f'Weight aggregated height: {weights["weight_aggregated_height"]}')
        self.weight_total_holes_text.set(f'Weight total holes: {weights["weight_total_holes"]}')
        self.weight_bumpiness_text.set(f'Weight bumpiness: {weights["weight_bumpiness"]}')
        self.weight_lines_cleared_text.set(f'Weight lines cleared: {weights["weight_lines_cleared"]}')

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