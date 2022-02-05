import unittest

# mainly tests to make sure that the playfield statistics algorithm is correct
# and to avoid having a big comment explaining how we calculate the statistics
# when we can comment about them here

min_y = 1
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

    #return [item for row in rows for item in row.translate( {ord(' '):None, ord('•'):' '} ) ]

def get_highest_non_empty_row(rows :list[list[str]]) -> int:
    get_row = lambda y: rows[y-min_y] # y-min_y because indeces start in 0

    y = len(rows)
    num_columns = len(rows[0])
    empty_row = [empty_block] * num_columns
    while y >= min_y and get_row(y) == empty_row:
        y -= 1

    return y

def get_non_empty_rows(rows :list[list[str]]) -> list[list[str]]:
    get_row = lambda y: rows[y-min_y] # y-min_y because indeces start in 0
    max_row = get_highest_non_empty_row(rows)
    return [ get_row(y) for y in range(min_y, max_row + 1) ]

def get_max_height_each_column(rows :list[list[str]]):
    get_row = lambda y: rows[y-min_y] # y-min_y because indeces start in 0

    # get only the populated rows, not all
    max_row = get_highest_non_empty_row(rows)
    
    non_empty_rows = [get_row(y) for y in range(min_y, max_row+1)]

    return 0

class TestTetris(unittest.TestCase):

    def test_01_transform_debug_rows_to_playfield_working_as_intended(self):
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

    def test_02_playfield_statistics_highest_non_empty_row(self):
        
        # arrange
        rows = transform_debug_rows_to_playfield(playfield_test)        
        
        # act
        y = get_highest_non_empty_row(rows)
        
        #assert
        self.assertEqual(22, len(rows))
        self.assertEqual(7, y)

    # def test_03_playfield_statistics_all_non_empty_rows(self):
        
    #     # arrange
    #     rows = transform_debug_rows_to_playfield(playfield_test)

    #     # act
    #     non_empty_rows = get_non_empty_rows(rows)
    
    #     # assert
    #     expected = [
    #         ['S', 'S', ' ', 'O', 'O', 'S', 'S', 'T', 'T', 'T'],     # row  1
    #         [' ', 'S', 'S', 'O', 'O', ' ', 'S', 'S', 'T', 'S'],     # row  2
    #         ['O', 'O', 'I', 'I', 'I', 'I', ' ', ' ', 'S', 'S'],     # row  3
    #         ['O', 'O', 'O', 'O', 'I', 'I', 'I', 'I', 'S', ' '],     # row  4
    #         [' ', ' ', 'O', 'O', ' ', ' ', ' ', 'S', ' ', ' '],     # row  5
    #         [' ', ' ', ' ', ' ', ' ', ' ', 'S', 'S', ' ', ' '],     # row  6
    #         [' ', ' ', ' ', ' ', ' ', ' ', 'S', ' ', ' ', ' '],     # row  7
    #     print(non_empty_rows)


if __name__ == "__main__":
    unittest.main()