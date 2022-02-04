from enum import Enum, unique
from math import fabs
import random
from tetris_engine import TetrisEngine, Playfield, TetrominoShape

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
from time import time
from functools import wraps
def timing(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        t_start = time()
        result = f(*args, **kwargs)
        t_end = time()
        print(f'Function {f.__name__} took {t_end-t_start:2.4f} s')
        return result
    return wrap

class TetrisAgent(TetrisEngine):

    @unique
    class GameAction(Enum):
        MOVE_LEFT       = "🡰"
        MOVE_RIGHT      = "🡲"
        ROTATE_LEFT     = "↶"
        ROTATE_RIGHT    = "↷"
        DROP            = "⟱"
        def __str__(self) -> str:
            return self.value

    def __init__(self) -> None:
        random.seed(7) # Important here so we will have always the same first falling piece for our tests. This starts with an L
        # This has to be done before super_init because there we choose already the first piece.
        super().__init__()
        self.bind_event(TetrisEngine.Events.ON_PLAYFIELD_UPDATED, self.update_playfield) # TODO with lambdas kitchen sink
        self.bind_event(TetrisEngine.Events.ON_LINES_CLEARED, self.update_lines_cleared_counter)
        self.bind_event(TetrisEngine.Events.ON_GAME_OVER, self.game_over)

        self.state = {}
        self.is_game_over = False
        self.lines_cleared = 0
        # TODO enable/disable events while calculating posibilities
        # TODO try-out state to avoid some issues

    def get_possible_drop_movements_sequence(self) -> list[list[GameAction]]:
        ga = self.GameAction

        starting_position_sequence = [
            [ ga.DROP ],
            [ ga.ROTATE_LEFT, ga.DROP ],
            [ ga.ROTATE_LEFT, ga.ROTATE_LEFT, ga.DROP ],
            [ ga.ROTATE_LEFT, ga.ROTATE_LEFT, ga.ROTATE_LEFT, ga.DROP ]
        ]

        rotation_sequence = [
            [ ],
            [ ga.ROTATE_LEFT ],
            [ ga.ROTATE_LEFT, ga.ROTATE_LEFT ],
            [ ga.ROTATE_LEFT, ga.ROTATE_LEFT, ga.ROTATE_LEFT ]
        ]
        
        possible_drop_movements_sequence = starting_position_sequence.copy()
        
        moving_left_sequence = []
        moving_right_sequence = []
        movements_each_side = self.playfield.columns // 2
        for _ in range(movements_each_side):
            moving_left_sequence += [ ga.MOVE_LEFT]
            sequences = [ seq + moving_left_sequence + [ ga.DROP ] for seq in rotation_sequence]
            possible_drop_movements_sequence += sequences

            moving_right_sequence += [ ga.MOVE_RIGHT]
            sequences = [ seq + moving_right_sequence + [ ga.DROP ] for seq in rotation_sequence]
            possible_drop_movements_sequence += sequences

        # for seq in possible_drop_movements_sequence:
        #     for mov in seq:
        #         print(str(mov), end=" ")
        #     print("")
        # input("x")

        return possible_drop_movements_sequence

    @timing
    def start_new_game(self) -> None:
        
        self.new_game()        

        possible_sequences = self.get_possible_drop_movements_sequence()
        total_lines_cleared = 0

        total_movements = 0

        while not self.is_game_over:
            self.save_state()
            best_sequence = self.get_best_sequence(possible_sequences)
            self.restore_state() # So we can really play the sequence, not only try-outs
            
            self.is_game_over = False # Important or trying a sequence can cause game over by mistake
            self.lines_cleared = 0
            self.play_sequence(best_sequence) # TODO play but showing in the UI enable update_playfield event
            total_movements += 1
            total_lines_cleared += self.lines_cleared

            #print(self.playfield)
            #print(f'{total_lines_cleared} {self.lines_cleared}')
            #input("Press enter")
        print(f'Game over with {total_lines_cleared} lines cleared and {total_movements} total movements done')

    def get_best_sequence(self, possible_sequences :list[list[GameAction]]) -> list[GameAction]:
        
        results = []
        
        for sequence in possible_sequences:
            self.restore_state() # All the sequences start from the same beginning

            self.try_out_sequence_is_game_over = False
            self.try_out_sequence_lines_cleared = 0
            
            can_play_sequence = self.play_sequence(sequence)            
            
            if can_play_sequence:
                statistics = self.get_playfield_statistics(self.playfield)
                fitting_algorithm = self.calculate_heuristics(statistics, self.try_out_sequence_lines_cleared)
                results.append((sequence, fitting_algorithm))

                sequence_string = ' '.join([str(x) for x in sequence])
                # print(f'Sequence:  {sequence_string}')
                # print(statistics)
                # print(fitting_algorithm)
                # print("")
        
        best_result = min(results, key=lambda item: item[1])
        best_sequence_string = ' '.join([str(x) for x in best_result[0]])
        #print(f"{self.falling_piece} Best sequence: {best_sequence_string}  value: {best_result[1]}")
        return best_result[0] # the sequence

    def play_sequence(self, sequence :list) -> bool:
        """
        Try all the movements in a sequence of movements. If we run all it will return true.

        If we can't reach the end of the sequence it means that the sequence is not valid and it will return false
        """
        ga = self.GameAction
        sequence_length = len(sequence)
        can_move = True
        i = 0
        while i<sequence_length and can_move:

            if sequence[i] == ga.DROP:
                self.drop()
                can_move = True

            elif sequence[i] == ga.MOVE_LEFT:                
                can_move = self.move_left()
                
            elif sequence[i] == ga.MOVE_RIGHT:
                can_move = self.move_right()

            elif sequence[i] == ga.ROTATE_LEFT:
                can_move = self.rotate_left()

            elif sequence[i] == ga.ROTATE_RIGHT:
                can_move = self.rotate_right()

            i += 1

        return can_move
    
    def get_playfield_statistics(self, playfield :Playfield) -> dict:
        """
        Analyses a playfield after a piece has fallen and the lines are cleared
        and returns a list of useful information about the playfield
        """
        statistics = {}
        
        # We start from the top because there could be an empty row in the middle but still pieces "frozen" above
        row_number = playfield.rows
        empty_row = [str(TetrominoShape.NONE)] * playfield.columns
        while self.playfield.get_row(row_number) == empty_row: # Watch out! This comparison works because we are comparing lists of strings
            row_number -= 1
        statistics["highest_non_empty_row"] = row_number

        # how many horizontal "pockets" in populated rows i.e. stretches of empty spaces in a row
        horizontal_pockets = 0
        for row_number in range(1, statistics["highest_non_empty_row"] + 1):
            previous_is_empty_block = False
            row = self.playfield.get_row(row_number)
            for block in row:
                if block == str(TetrominoShape.NONE):
                    if not previous_is_empty_block:
                        horizontal_pockets += 1
                    previous_is_empty_block = True
                else:
                    previous_is_empty_block = False
        statistics["horizontal_pockets"] = horizontal_pockets

        # weighted rows. The more blocks in a lower row the less energy
        # Like potential energy in physics, more energy the higher it gets E = m*g*h
        # In our case the mass is the number of blocks and height is the row number
        # For example this:
        #
        # row 2    L L L • • • • • • •
        # row 1    L • • • • • • • • •
        #
        # E = 1*1 + 3*2 = 1 + 6 = 7
        #
        # However if the base is bigger:
        #
        # row 2    L • • • • • • • • •
        # row 1    L L L • • • • • • •
        #
        # E = 3*1 + 1*2 = 3 + 2 = 5 which is lower energy and therefore preferred
        #
        potential_energy = 0
        g = 0.1 # The reason for this is to not exagerate the potential energy gain from row 1-20
                # without this, the potential energy of a block in row 20 is 20 times that of a block
                # in row 1 but with this it is 20*0.1 = 2 times more only
        for row_number in range(1, statistics["highest_non_empty_row"] + 1):
            row = self.playfield.get_row(row_number)
            occupied_blocks = len(row) - row.count(str(TetrominoShape.NONE))
            potential_energy += occupied_blocks * g * row_number
        statistics["potential_energy"] = potential_energy

        # Blocks that are not supported below by another block get extra weights
        # We work with the columns
        # Example, imagine we have this two rows:
        #
        #  row 2    T T T •
        #  row 1    • T • •
        #
        # rows = [ 
        #   ['T', 'T', 'T', ' '],
        #   [' ', 'T', ' ', ' '] ]
        #
        # reverse_rows = [
        #   [' ', 'T', ' ', ' '],
        #   ['T', 'T', 'T', ' '] ]
        #
        # top_to_bottom_columns = [
        #   [' ', 'T'],
        #   ['T', 'T'],
        #   [' ', 'T'],
        #   [' ', ' '],
        # ] 
        # So it is easy to check from the top which block has no "support" underneath

        unsupported_blocks = 0
        reverse_rows = [self.playfield.get_row(y) for y in range(statistics["highest_non_empty_row"], 0, -1)]
        top_to_bottom_columns = [list(x) for x in zip(*reverse_rows)]
        # We start from the top until row 2 (row 1 is always supported as it is the first one)
        for column in top_to_bottom_columns:
            for index in range(len(column)-1):            
                if column[index] != str(TetrominoShape.NONE) and column[index+1] == str(TetrominoShape.NONE):
                    unsupported_blocks += 1
        statistics["unsuported_blocks"] = unsupported_blocks

        return statistics

    def calculate_heuristics(self, playfield_statistics :dict, lines_cleared :int) -> float:
        # better to put pieces on the sides instead of the middle?
        # hidden empty block that we can lock if we move to the bottom and move left/right, instead of just dropping it?
        # we don't want wells (empty one single line waiting for an I piece)
        # and more (research about it)
        
        #top = playfield_statistics["highest_non_empty_row"] # minimize
        horizontal_pockets = playfield_statistics["horizontal_pockets"] # minimize. Important to move pieces to the sides and avoid wells
        potential_energy = playfield_statistics["potential_energy"] # minimize. To keep things low not growing in rows
        unsupported_blocks = playfield_statistics["unsuported_blocks"] # minimize to avoid empty spaces under blocks

        # our fitting algorithm
        #fitting_algorithm = potential_energy + 2*unsupported_blocks + horizontal_pockets - 100*lines_cleared 165 lines
        fitting_algorithm = potential_energy + 1.9*unsupported_blocks + horizontal_pockets - 100*lines_cleared # 248 lines        

        #print(f'{potential_energy} {unsupported_blocks} {100*lines_cleared}')
        return fitting_algorithm

    def update_playfield(self, data :dict):
        # We only care about this to see what's going on but it won't affect our calculations
        pass

    def update_lines_cleared_counter(self, lines_cleared :int):
        self.try_out_sequence_lines_cleared = lines_cleared
        self.lines_cleared = lines_cleared
        #print("I have lines cleared")

    def game_over(self):
        self.try_out_sequence_is_game_over = True # Only used for the try-out, not the real game
        self.is_game_over = True
        #print("I reached game over") # TODO remove

    def restore_state(self):
        self.playfield._grid = [ row[:] for row in self.state["rows"] ] # TODO something else, shouldn't access internal grid
        self.falling_piece.center_x = self.state["center_x"]
        self.falling_piece.center_y = self.state["center_y"]
        self.falling_piece.set_shape(self.state["shape"])
        self.falling_piece.set_angle(self.state["angle"])

    def save_state(self):
        self.state["rows"] = [ row[:] for row in self.playfield._grid ] # TODO something else, shouldn't access internal grid
        #self.state["grid"] = [self.playfield.get_row(y) for y in range(self.playfield.min_y, self.playfield.rows + 1)]
        self.state["center_x"] = self.falling_piece.center_x
        self.state["center_y"] = self.falling_piece.center_y
        self.state["shape"] = self.falling_piece.shape
        self.state["angle"] = self.falling_piece.angle        

if __name__ == "__main__":
    agent = TetrisAgent()
    agent.start_new_game()