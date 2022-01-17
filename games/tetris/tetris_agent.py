import random
from tetris_engine import TetrisEngine

"""
TODO if we record how the agent performs we can use emojis

🡲 Wide-Headed Rightwards Medium Barb Arrow
🡰 Wide-Headed Leftwards Medium Barb Arrow
🡳 Wide-Headed Downwards Medium Barb Arrow
↶ anticlockwise top semicircle arrow symbol
↷     clockwise top semicircle arrow symbol
⟱ downwards quadruple arrow
☰ Trigram for heaven

So for example if we record:
L🡰🡰↶⟱2☰
It means that we had an L-shape tetromino, we moved it twice to the left, rotate 90deg counterclockwise,
drop it and we made 2 lines

"""

class TetrisAgent(TetrisEngine):
    def __init__(self) -> None:
        random.seed(7) # Important here so we will have always the same first falling piece for our tests. This starts with an L
        # This has to be done before super_init because there we choose already the first piece.
        super().__init__()
        self.bind_event(TetrisEngine.Events.ON_PLAYFIELD_UPDATED, self.update_playfield) # TODO with lambdas kitchen sink
        self.bind_event(TetrisEngine.Events.ON_LINES_CLEARED, self.update_lines_cleared_counter)
        self.bind_event(TetrisEngine.Events.ON_GAME_OVER, self.game_over)

        self.state = {}

    def start_new_game(self) -> None:
        # we try every possible combination for the current piece from the top
        self.new_game()
        

        fp = self.falling_piece
        starting_x = self.falling_piece.center_x
        starting_y = self.falling_piece.center_y
        print(fp.shape)

        # Starting point
        self.save_state()
        self.falling_piece.set_starting_position()
        while self.can_move_falling_piece(self.falling_piece.center_x, self.falling_piece.center_y - 1):
            self.move_falling_piece(self.falling_piece.center_x, self.falling_piece.center_y - 1)
        self.set_falling_piece(self.playfield)
        lines_cleared = self.playfield.clear_full_lines()
        self.calculate_heuristics(lines_cleared, self.playfield.grid)
        self.restore_state()

        # From center, move left as much as we can
        x = starting_x
        y = starting_y
        while self.can_move_falling_piece(x-1, y):
            x -= 1
            print("hello")

        # From center, move right as much as we can
        x = starting_x
        y = starting_y
        while self.can_move_falling_piece(x+1, y):
            x += 1
            print("goodbye")


        # algorithm
        # where we put the piece, drop the piece
        # get information about how many lines we would clear doing this and the statistics
        # rotate the piece if possible, repeat the same information
        # move to the left as much as we can and do the same
        # move back to where we started and do the same procedure to the right
        # gather all the fitting algorithms and see which one is better. That would be the correct move
        pass
    
    def get_final_grid(self, falling_piece_center_x :int, falling_piece_center_y :int, starting_grid :list) -> list:
        pass

    def get_playfield_statistics(self):
        # TODO how tall the blocks reach in a current playfield -> minimize
        # how many lines I do -> maximize
        # better to put pieces on the sides instead of the middle?
        # hidden empty block that we can lock if we move to the bottom and move left/right, instead of just dropping it?
        # we don't want wells (empty one single line waiting for an I piece)
        # and more (research about it)
        pass

    def calculate_heuristics(self, lines_cleared :int, grid :list):
        # our fitting algorithm
        pass

    def update_playfield(self):
        # We only care about this to see what's going on but it won't affect our calculations
        pass

    def update_lines_cleared_counter(self):
        pass

    def game_over(self):
        pass

    def restore_state(self):
        self.playfield.grid = self.state["grid"]
        self.falling_piece.center_x = self.state["center_x"]
        self.falling_piece.center_y = self.state["center_y"]
        self.falling_piece.set_shape(self.state["shape"])
        self.falling_piece.set_angle(self.state["angle"])

    def save_state(self):
        self.state["grid"] = self.playfield.grid
        self.state["center_x"] = self.falling_piece.center_x
        self.state["center_y"] = self.falling_piece.center_y
        self.state["shape"] = self.falling_piece.shape
        self.state["angle"] = self.falling_piece.angle        

if __name__ == "__main__":
    agent = TetrisAgent()
    agent.start_new_game()