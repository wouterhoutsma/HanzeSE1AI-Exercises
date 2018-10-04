import time

def Break():
    pass

# helper function
def cross(A, B):
    # cross product of chars in string A and chars in string B
    return [a+b for a in A for b in B]

#   1 2 3 4 .. 9
# A
# B
# C
# D
# ..
# I


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
cells = cross(rows, cols) # for 3x3 81 cells A1..9, B1..9, C1..9, ...

# unit = a row, a column, a box; list of all units
unit_list = ([cross(r, cols) for r in rows] +                             # 9 rows
             [cross(rows, c) for c in cols] +                             # 9 cols
             [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]) # 9 units
# peers is a dict {cell : list of peers}
# every cell c has 20 peers p (i.e. cells that share a row, col, box)
# units['A1'] is a list of lists, and sum(units['A1'],[]) flattens this list
units = dict((s, [u for u in unit_list if s in u]) for s in cells)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in cells)


def test():
    # a set of tests that must pass
    assert len(cells) == 81
    assert len(unit_list) == 27
    assert all(len(units[s]) == 3 for s in cells)
    assert all(len(peers[s]) == 20 for s in cells)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == {['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                            'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                            'A1', 'A3', 'B1', 'B3']}
    print('All tests pass.')


def display(grid, original=None):
    # grid is a dict of {cell: string}, e.g. grid['A1'] = '1234'
    print()
    for r in rows:
        for c in cols:
            v = grid[r+c]
            # avoid the '123456789'
            if len(v) > 1:
                v = '.'
            if original is not None:
                if len(original[r+c]) == 1:
                    v = '\033[1m\033[32m{}\033[0m'.format(v)
            elif v != '.':
                v = '\033[1m\033[32m{}\033[0m'.format(v)
            print (''.join(v), end=' ')
            if c == '3' or c == '6': print('|', end='')
        print()
        if r == 'C' or r == 'F':
            print('-------------------')
    print()


def parse_string_to_dict(grid_string):
    # grid_string is a string like '4.....8.5.3..........7......2.....6....   '
    # convert grid_string into a dict of {cell: chars}
    char_list1 = [c for c in grid_string if c in digits or c == '.']
    # char_list1 = ['8', '5', '.', '.', '.', '2', '4', ...  ]

    assert len(char_list1) == 81

    # replace '.' with '1234567'
    char_list2 = [s.replace('.', '123456789') for s in char_list1]

    # grid {'A1': '8', 'A2': '5', 'A3': '123456789',  }
    grid = dict(zip(cells, char_list2))

    # select all cells c with number of values == 1
    # singles = [c for c in cells if len(grid[c]) == 1]
    # for c in singles:
    #     if not(assign(grid, c, grid[c])):
    #         return False
    return grid

def remove_multiple_options(grid):
    options = '123456789'
    for value in grid.values():
        options = options.replace(value, '')
    if len(options) > 1:
        for key, value in grid.items():
            if len(value) != len(options):
                continue
            value_copy = value
            for c in options:
                value_copy = value_copy.replace(c, '')
            if len(value_copy) == 0:
                grid[key] = options[0]
                truncate_options(grid)
                return


def remove_hidden_singles(grid):

    for key in grid.keys():
        row = key[0]
        column = key[1]
        possible_values = grid[key]
        if len(possible_values) == 1:
            continue
        # Rows, horizontal
        unique_horizontal = possible_values
        for c_column in range(1, len(digits) + 1):
            if c_column == column:
                continue
            c_key = str(row) + str(c_column)
            for c in grid[c_key]:
                unique_horizontal = unique_horizontal.replace(c, '')
        if len(unique_horizontal) == 1:
            grid[key] = unique_horizontal
            continue
        # Columns, vertical
        unique_vertical = possible_values
        c_rows = rows.replace(row, '')
        for c_row in range(0, len(c_rows)):
            c_row = c_rows[c_row]
            if c_row == row:
                continue
            c_key = str(c_row) + str(column)
            for c in grid[c_key]:
                unique_vertical = unique_vertical.replace(c, '')
        if len(unique_vertical) == 1:
            grid[key] = unique_vertical
            continue
    return grid


def truncate_options(grid):
    for key in grid.keys():
        row = key[0]
        column = key[1]
        possible_values = grid[key]
        if len(possible_values) == 1:
            continue
        # Horizontal
        for c_column in range(1, len(digits) + 1):
            if c_column == column:
                continue
            c_key = str(row) + str(c_column)
            if len(grid[c_key]) == 1:
                possible_values = possible_values.replace(grid[c_key], '')
        # Vertical
        c_rows = rows.replace(row, '')
        for c_row in range(0, len(c_rows)):
            c_row = c_rows[c_row]
            if c_row == row:
                continue
            c_key = str(c_row) + str(column)
            if len(grid[c_key]) == 1:
                possible_values = possible_values.replace(grid[c_key], '')
        # Blocks
        row_blocks = (('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'H', 'I'))
        column_blocks = (('1', '2', '3'), ('4', '5', '6'), ('7', '8', '9'))
        try:

            for row_block in row_blocks:
                if row not in row_block:
                    continue
                for column_block in column_blocks:

                    if column not in column_block:
                        continue
                    # Here, we have the right column block and row block
                    for c_row in row_block:
                        for c_col in column_block:
                            if c_col == column and c_row == row:
                                continue
                            c_key = str(c_row) + str(c_col)
                            if len(grid[c_key]) == 1:
                                possible_values = possible_values.replace(grid[c_key], '')
                    raise Break()
        except:
            pass

        grid[key] = possible_values
    remove_multiple_options(grid)


def solve(grid):
    # Remove options that can't be made
    truncate_options(grid)

    # Check for a hidden single in block
    row_blocks = (('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'H', 'I'))
    column_blocks = (('1', '2', '3'), ('4', '5', '6'), ('7', '8', '9'))
    for row_block in row_blocks:
        for column_block in column_blocks:
            for row in row_block:
                for column in column_block:
                    current_key = row + column
                    sure_options = grid[current_key]
                    for c_row in row_block:
                        for c_column in column_block:
                            c_key = c_row + c_column
                            if c_key == current_key:
                                continue
                            for c in grid[c_key]:
                                sure_options = sure_options.replace(c, '')
                    if len(sure_options) != 0 and len(grid[current_key]) > 1:
                        grid[current_key] = sure_options

    # Check for a hidden single in row and column
    remove_hidden_singles(grid)
    # Given new decisions made, truncate options that don't make sense
    truncate_options(grid)
    # Check if the board has options
    for value in grid.values():
        if len(value) == 0:
            return False

    smallest_cell = False
    for key, value in grid.items():
        if len(value) > 1:
            if smallest_cell is False or len(grid[smallest_cell]) > len(value):
                smallest_cell = key
    if smallest_cell is False:
        return grid

    for option_index in range(0, len(grid[smallest_cell])):
        grid_copy = grid.copy()
        grid_copy[smallest_cell] = grid[smallest_cell][option_index]
        grid_copy = solve(grid_copy)
        if grid_copy is not False:
            break
    return grid_copy


s1 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
s2 = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
s3 = '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
s4 = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
s5 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
s6 = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
s7 = '6..3.2....5.....1..........7.26............543.........8.15........4.2........7..'
s8 = '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
s9 = '..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..'
s10 = '3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....'
s11 = '1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......'
s12 = '6..3.2....4.....1..........7.26............543.........8.15........4.2........7..'
s13 = '....3..9....2....1.5.9..............1.2.8.4.6.8.5...2..75......4.1..6..3.....4.6.'
s14 = '45.....3....8.1....9...........5..9.2..7.....8.........1..4..........7.2...6..8..'

slist = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14]

# puzzle1  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
# puzzle2  = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
# puzzle3  = '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
# puzzle4  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
# puzzle5  = '.....5.8....6.1.43..........1.5........1.6...3.......553.....61........4.........'
#
# slist = [puzzle1, puzzle2, puzzle3, puzzle4, puzzle5]
i = 1
for s in slist:
    print('__________')
    print('{}\n________'.format(i))
    i = i + 1
    d = parse_string_to_dict(s)
    values = '123456789'
    for c in d.values():
        if len(c) == 1:
            values = values.replace(c, '')
    if len(values) > 1:
        print('This puzzle has more than one answer.')
        continue

    start_time = time.time()
    grid = solve(d.copy())
    display(d)
    display(grid, d)
    print(time.time()-start_time)