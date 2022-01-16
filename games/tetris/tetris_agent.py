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
        super().__init__()
        super().bind_event(TetrisEngine.Events.ON_PLAYFIELD_UPDATED, self.update_playfield)
        super().bind_event(TetrisEngine.Events.ON_LINES_CLEARED, self.update_lines_cleared_counter)
        super().bind_event(TetrisEngine.Events.ON_GAME_OVER, self.game_over)

    def new_game(self) -> None:
        # we try every possible combination for the current piece from the top

        # algorithm
        # where we put the piece, drop the piece
        # get information about how many lines we would clear doing this and the statistics
        # rotate the piece if possible, repeat the same information
        # move to the left as much as we can and do the same
        # move back to where we started and do the same procedure to the right
        # gather all the fitting algorithms and see which one is better. That would be the correct move
        pass
    
    def get_playfield_statistics(self):
        # TODO how tall the blocks reach in a current playfield -> minimize
        # how many lines I do -> maximize
        # better to put pieces on the sides instead of the middle?
        # hidden empty block that we can lock if we move to the bottom and move left/right, instead of just dropping it?
        # we don't want wells (empty one single line waiting for an I piece)
        # and more (research about it)
        pass

    def calculate_heuristics(self):
        # our fitting algorithm
        pass

    def update_playfield(self, ghost_dropped_piece_coordinates :list):
        # We only care about this to see what's going on but it won't affect our calculations
        pass

    def update_lines_cleared_counter(self):
        pass

    def game_over(self):
        pass

