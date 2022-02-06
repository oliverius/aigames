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
        #self.bind_event(TetrisEngine.Events.ON_PLAYFIELD_UPDATED, self.update_playfield)
        self.bind_event(TetrisEngine.Events.ON_LINES_CLEARED, self.update_lines_cleared_counter)
        self.bind_event(TetrisEngine.Events.ON_GAME_OVER, self.game_over)

        self.state = {}
        self.is_game_over = False
        self.lines_cleared = 0

    def calculate_heuristics(self, playfield_statistics :dict, lines_cleared :int, weights :dict) -> float:       
        fitting_algorithm = (
            weights["weight_aggregated_height"] * playfield_statistics["aggregated_height"] +
            weights["weight_total_holes"]       * playfield_statistics["total_holes"]       +
            weights["weight_bumpiness"]         * playfield_statistics["bumpiness"]         +
            weights["weight_lines_cleared"]     * lines_cleared
        )
        return fitting_algorithm

    def get_best_sequence(self, sequences :list[list[GameAction]], weights :dict) -> list[GameAction]:
        
        results = []
        
        for sequence in sequences:
            self.restore_state() # All the sequences start from the same beginning

            self.try_out_sequence_lines_cleared = 0
            
            can_play_sequence = self.play_sequence(sequence)            
            
            if can_play_sequence:
                statistics = self.get_playfield_statistics(self.playfield)
                fitting_algorithm = self.calculate_heuristics(statistics, self.try_out_sequence_lines_cleared, weights)
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

    def get_playfield_column_statistics(self, column :list[str], first_row :int) -> tuple[int,int]:
        highest_non_empty_row_found = False
        highest_non_empty_row = 0
        holes_count = 0
        for row, value in reversed(list(enumerate(column, start=first_row))):
            if not highest_non_empty_row_found:
                if value != str(TetrominoShape.NONE):
                    highest_non_empty_row_found = True
                    highest_non_empty_row = row
            else:
                if value == str(TetrominoShape.NONE):
                    holes_count += 1
        return (highest_non_empty_row, holes_count)

    def get_playfield_statistics(self, playfield: Playfield) -> dict:
        """
        Analyses a playfield after a piece has fallen and the lines are cleared
        and returns a list of useful information about the playfield
        """
        columns = [list(column) for column in zip(*playfield.get_all_rows())]
        first_row = playfield.min_y
        
        column_statistics = [ self.get_playfield_column_statistics(column, first_row) for column in columns ]
        
        heights, holes = zip(*column_statistics)

        # It is the sum of the absolute difference in height between adjacent columns
        bumpiness = sum([abs(current-next) for current, next in zip(heights, heights[1:])])

        return {
            "aggregated_height": sum(heights),
            "total_holes":       sum(holes),
            "bumpiness":         bumpiness
        }

    def get_possible_drop_movements_sequence(self) -> list[list[GameAction]]: # TODO unit test about this stuff.
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

    @timing
    def start_new_game(self, weights :dict) -> None:
        
        self.new_game()        

        possible_sequences = self.get_possible_drop_movements_sequence()
        total_lines_cleared = 0

        total_movements = 0

        while not self.is_game_over:
            self.save_state()

            self.enable_on_game_over_event = False            
            self.enable_on_playfield_updated_event = False
            
            best_sequence = self.get_best_sequence(possible_sequences, weights)

            self.restore_state() # So we can really play the sequence, not only try-outs
            
            self.is_game_over = False # Important or trying a sequence can cause game over by mistake
            self.lines_cleared = 0

            self.enable_on_game_over_event = True
            self.enable_on_playfield_updated_event = True
            
            self.play_sequence(best_sequence)
            
            total_movements += 1
            total_lines_cleared += self.lines_cleared


        print(f'Game over with {total_lines_cleared} lines cleared and {total_movements} total movements done')

    def game_over(self):
        self.is_game_over = True
        #print("I reached game over") # TODO remove

    def update_lines_cleared_counter(self, lines_cleared :int):
        self.try_out_sequence_lines_cleared = lines_cleared
        self.lines_cleared = lines_cleared
        #print("I have lines cleared")

    def restore_state(self):
        self.playfield.set_all_rows(self.state["rows"])
        self.falling_piece.center_x = self.state["center_x"]
        self.falling_piece.center_y = self.state["center_y"]
        self.falling_piece.set_shape(self.state["shape"])
        self.falling_piece.set_angle(self.state["angle"])

    def save_state(self):       
        self.state["rows"] = self.playfield.get_all_rows()
        self.state["center_x"] = self.falling_piece.center_x
        self.state["center_y"] = self.falling_piece.center_y
        self.state["shape"] = self.falling_piece.shape
        self.state["angle"] = self.falling_piece.angle        

if __name__ == "__main__":
    agent = TetrisAgent()
    weights = {
        "weight_aggregated_height":  5,
        "weight_total_holes":        1.1,
        "weight_bumpiness":          0.8,
        "weight_lines_cleared":    -10
    }
    agent.start_new_game(weights)