from tetris_agent import TetrisAgent, TetrominoShape
import unittest

# mainly tests to make sure that the playfield statistics algorithm is correct
# and to avoid having a big comment explaining how we calculate the statistics
# when we can comment about them here

empty_block = ' '

playfield_test = [
    [ '• • • • • • • • • •' ], # row 22
    [ '• • • • • • • • • •' ], # row 21
    [ '• • • • • • • • • •' ], # row 20
    [ '• • • • • • • • • •' ], # row 19
    [ '• • • • • • • • • •' ], # row 18
    [ '• • • • • • • • • •' ], # row 17
    [ '• • • • • • • • • •' ], # row 16
    [ '• • • • • • • • • •' ], # row 15
    [ '• • • • • • • • • •' ], # row 14
    [ '• • • • • • • • • •' ], # row 13
    [ '• • • • • • • • • •' ], # row 12
    [ '• • • • • • • • • •' ], # row 11
    [ '• • • • • • • • • •' ], # row 10
    [ '• • • • • • • • • •' ], # row  9
    [ '• • • • • • • • • •' ], # row  8
    [ '• • • • • • S • • •' ], # row  7
    [ '• • • • • • S S • •' ], # row  6
    [ '• • O O • • • S • •' ], # row  5
    [ 'O O O O I I I I S •' ], # row  4
    [ 'O O I I I I • • S S' ], # row  3
    [ '• S S O O • S S T S' ], # row  2
    [ 'S S • O O S S T T T' ]  # row  1
]

def transform_debug_rows_to_playfield(rows):
    # Convert to correct shapes (instead of '•' we have ' ')
    return list(reversed([list(value.translate( {ord(' '):None, ord('•'):empty_block} )) for row in rows for value in row ]))

class TestTetris(unittest.TestCase):

    def test_01_transform_debug_rows_to_playfield_working_as_intended(self):
        
        # arrange
        expected = [
            ['S', 'S', ' ', 'O', 'O', 'S', 'S', 'T', 'T', 'T'],     # row  1
            [' ', 'S', 'S', 'O', 'O', ' ', 'S', 'S', 'T', 'S'],     # row  2
            ['O', 'O', 'I', 'I', 'I', 'I', ' ', ' ', 'S', 'S'],     # row  3
            ['O', 'O', 'O', 'O', 'I', 'I', 'I', 'I', 'S', ' '],     # row  4
            [' ', ' ', 'O', 'O', ' ', ' ', ' ', 'S', ' ', ' '],     # row  5
            [' ', ' ', ' ', ' ', ' ', ' ', 'S', 'S', ' ', ' '],     # row  6
            [' ', ' ', ' ', ' ', ' ', ' ', 'S', ' ', ' ', ' '],     # row  7
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row  8
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row  9
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 10
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 11
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 12
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 13
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 14
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 15
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 16
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 17
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 18
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 19
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 20
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],     # row 21
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']      # row 22
        ]

        # assert
        self.assertEqual(expected, transform_debug_rows_to_playfield(playfield_test))

    def test_02_playfield_columns_highest_row_and_number_of_holes(self):

        # arrange
        agent = TetrisAgent()
        first_row = agent.playfield.min_y
        # values are from row 1 to row 22
        column_no_holes =    ['S', 'S', 'O', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        column_one_hole =    ['S', ' ', 'O', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        column_two_holes =   ['S', 'S', ' ', 'I', ' ', 'S', 'S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        column_double_hole = ['S', 'S', ' ', ' ', 'I', 'S', 'S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        column_no_values =   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

        # act
        result_no_holes =    agent.get_playfield_column_statistics(column_no_holes,    first_row)
        result_one_hole =    agent.get_playfield_column_statistics(column_one_hole,    first_row)
        result_two_holes =   agent.get_playfield_column_statistics(column_two_holes,   first_row)
        result_double_hole = agent.get_playfield_column_statistics(column_double_hole, first_row)
        result_no_values =   agent.get_playfield_column_statistics(column_no_values,   first_row)

        # assert
        self.assertEqual( (4,    0), result_no_holes)
        self.assertEqual( (4,    1), result_one_hole)
        self.assertEqual( (7,    2), result_two_holes)
        self.assertEqual( (7,    2), result_double_hole)
        self.assertEqual( (None, 0), result_no_values)

    def test_03_playfield_statistics(self):
        
        # arrange
        rows = transform_debug_rows_to_playfield(playfield_test)
        agent = TetrisAgent()
        agent.playfield.set_all_rows(rows)

        # act
        statistics = agent.get_playfield_statistics2(agent.playfield)       

        # assert
        self.assertEqual(46, statistics["aggregated_height"])
        self.assertEqual( 6, statistics["total_holes"])
        self.assertEqual( 9, statistics["bumpiness"])

if __name__ == "__main__":
    unittest.main()