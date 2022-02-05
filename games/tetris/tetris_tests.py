from tetris_agent import TetrisAgent, TetrominoShape
import unittest

# mainly tests to make sure that the playfield statistics algorithm is correct
# and to avoid having a big comment explaining how we calculate the statistics
# when we can comment about them here

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

class TestTetris(unittest.TestCase):

    def get_playfield_statistics_from_debug_rows(self, debug_rows :list[list[str]]) -> dict:
        rows = self.transform_debug_rows_to_playfield_rows(debug_rows)
        agent = TetrisAgent()
        agent.playfield.set_all_rows(rows)
        return agent.get_playfield_statistics(agent.playfield)

    def transform_debug_rows_to_playfield_rows(self, rows :list[list[str]]) -> list[list[str]]:
        # In our examples we need to have 22 rows, so if 'rows' is less we pad at the end with empty rows
        empty_block = str(TetrominoShape.NONE)
        empty_row_debug = ['• • • • • • • • • •']
        rows = (22 - len(rows)) * [empty_row_debug] + rows

        # Convert to correct shapes (instead of '•' we have ' ')
        return list(reversed([list(value.translate( {ord(' '):None, ord('•'):empty_block} )) for row in rows for value in row ]))

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
        self.assertEqual(expected, self.transform_debug_rows_to_playfield_rows(playfield_test))

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
        self.assertEqual( (4, 0), result_no_holes)
        self.assertEqual( (4, 1), result_one_hole)
        self.assertEqual( (7, 2), result_two_holes)
        self.assertEqual( (7, 2), result_double_hole)
        self.assertEqual( (0, 0), result_no_values)

    def test_03_playfield_statistics(self):
        
        # arrange
        rows = self.transform_debug_rows_to_playfield_rows(playfield_test)
        agent = TetrisAgent()
        agent.playfield.set_all_rows(rows)

        # act
        statistics = agent.get_playfield_statistics(agent.playfield)       

        # assert
        self.assertEqual(46, statistics["aggregated_height"])
        self.assertEqual( 6, statistics["total_holes"])
        self.assertEqual( 9, statistics["bumpiness"])

    def test_04_playfield_scenario_drop_s_piece(self):
        """
        We want to prove that when dropping an S shape (for example) we get a better fitting algorithm
        when that piece is put covering an empty hole than when it is not.
        """

        # arrange
        scenario_1 = [
            ['• • • • • S S • • I'],
            ['• • • Z S S • • • I']
        ]
        scenario_2 = [
            ['• • S S • • • • • I'],
            ['• S S Z • • • • • I']
        ]
        scenario_3 = [
            ['• • • S • • • • • I'],
            ['• • • S S • • • • I'],
            ['• • • Z S • • • • I']
        ]

        # act
        playfield_statistics_scenario_1 = self.get_playfield_statistics_from_debug_rows(scenario_1)
        playfield_statistics_scenario_2 = self.get_playfield_statistics_from_debug_rows(scenario_2)
        playfield_statistics_scenario_3 = self.get_playfield_statistics_from_debug_rows(scenario_3)

        self.assertDictEqual({'aggregated_height': 8, 'total_holes': 1, 'bumpiness': 6}, playfield_statistics_scenario_1)
        self.assertDictEqual({'aggregated_height': 7, 'total_holes': 0, 'bumpiness': 6}, playfield_statistics_scenario_2)
        self.assertDictEqual({'aggregated_height': 8, 'total_holes': 0, 'bumpiness': 9}, playfield_statistics_scenario_3)

if __name__ == "__main__":
    unittest.main()