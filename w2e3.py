import math, time, random
current_milli_time = lambda: int(round(time.time() * 1000))


class Board:
    EMPTY = '.'
    BLACK = 'x'
    WHITE = 'o'
    SIZE = 8

    def __init__(self, board=None):
        self.option_list = []
        self.value = 0
        if board is not None:
            self.board = board.board.copy()
            self.moves = board.moves
            return
        self.board = []
        self.moves = 0
        for y in range(Board.SIZE):
            for x in range(Board.SIZE):
                self.board.append(Board.EMPTY)

        white = {3 + 3 * Board.SIZE, 4 + 4 * Board.SIZE}
        black = {3 + 4 * Board.SIZE, 4 + 3 * Board.SIZE}

        for w in white:
            self.board[w] = Board.WHITE
        for b in black:
            self.board[b] = Board.BLACK

    def copy(self):
        b = Board(self)
        b.moves = self.moves
        return b

    # def fill_indices(self, indices, fill):
    #     for i in indices:
    #         self.board[i] = fill

    def __repr__(self):
        return "\n" + str(self) + "\n"

    def score(self, colour=None):
        score = {}
        score[Board.BLACK] = 0
        score[Board.WHITE] = 0
        for c in self.board:
            if c == Board.BLACK:
                score[Board.BLACK] += 1
            if c == Board.WHITE:
                score[Board.WHITE] += 1
        if colour is not None:
            return score[colour]
        else:
            return score[self.turn()]

    def finished(self):
        for cell in self.board:
            if cell is Board.EMPTY:
                return False
        return True

    def turn(self):
        return Board.BLACK if self.moves % 2 == 0 else Board.WHITE

    def calculate_moves(self):
        us = Board.BLACK if self.moves % 2 == 0 else Board.WHITE
        them = Board.WHITE if self.moves % 2 == 0 else Board.BLACK
        our_indices = []
        for i in range(0, len(self.board)):
            if self.board[i] == us:
                our_indices.append(i)
        base = Board.SIZE
        adjustments = (-base, -base+1, 1, base+1, base, base-1, -1, -(base+1))  # N NW W SW S SE E NE
        # adjustments = [8]
        possible_moves = []

        for index in our_indices:
            for direction in adjustments:
                index_copy = index
                while 0 <= index_copy + direction < len(self.board):
                    # Check if its a WE movement, if it is, don't switch rows, skip this direction
                    if abs(direction) == 1:
                        if math.floor(index / Board.SIZE) != math.floor((index_copy + direction) / Board.SIZE):
                            break
                    # Check if its a diagonal movement, if it is, don't continue on other side of board
                    if abs(Board.SIZE - abs(direction)) == 1:
                        if abs(((index_copy + direction) % Board.SIZE) - (index_copy % Board.SIZE)) != 1:
                            break
                    if self.board[index_copy + direction] != them:
                        if index_copy != index:
                            index_copy = index_copy + direction
                        break
                    index_copy = index_copy + direction
                if index != index_copy:
                    if self.board[index_copy] == Board.EMPTY:
                        possible_moves.append(index_copy)
        return list(set(possible_moves))

    def options(self, moves=None):
        if len(self.option_list) != 0:
            return self.option_list
        if moves is None:
            moves = self.calculate_moves()
        options = []
        for move in moves:
            options.append(self.move(move))
        self.option_list = options
        return options

    def move(self, index):
        base = Board.SIZE
        us = Board.BLACK if self.moves % 2 == 0 else Board.WHITE
        them = Board.WHITE if self.moves % 2 == 0 else Board.BLACK
        new_board = self.copy()
        adjustments = (-base, -base+1, 1, base+1, base, base-1, -1, -(base+1))  # N NW W SW S SE E NE
        # adjustments = [-1]
        good_directions = []
        for direction in adjustments:
            index_copy = index
            while 0 <= index_copy + direction < len(new_board.board):
                # Check if its a WE movement, if it is, don't switch rows, skip this direction
                if abs(direction) == 1:
                    if math.floor(index / Board.SIZE) != math.floor((index_copy + direction) / Board.SIZE):
                        break
                # Check if its a diagonal movement, if it is, don't continue on other side of board
                if abs(Board.SIZE - abs(direction)) == 1:
                    if abs(((index_copy + direction) % Board.SIZE) - (index_copy % Board.SIZE)) != 1:
                        break
                index_copy = index_copy + direction
                if new_board.board[index_copy] == us:
                    good_directions.append(direction)
                if new_board.board[index_copy] != them:
                    break
        for direction in good_directions:
            index_copy = index + direction
            while new_board.board[index_copy] != us:
                new_board.board[index_copy] = us
                index_copy = index_copy + direction
        new_board.board[index] = us

        new_board.moves = new_board.moves + 1
        return new_board

    def __str__(self):
        string = "  "
        for i in range(1, Board.SIZE + 1):
            fill = '\n' if i % Board.SIZE == 0 and i > 0 else ' '
            string = string + str(i) + fill
        for i in range(1, len(self.board) + 1):
            fill = '\n' if i % Board.SIZE == 0 and i > 0 else ' '
            prefill = '{} '.format(math.ceil(i / Board.SIZE)) if (i - 1) % Board.SIZE == 0 else ''
            string = string + prefill + self.board[i-1] + fill
        return string


def random_adversary(moves):
    return moves[random.randint(0, len(moves)-1)]


def negamax_adversary(board, depth=1, colour=None, a=-999999, b=999999, ab=False):
    if colour is None:
        colour = board.turn()
    enemy = Board.WHITE if colour == Board.BLACK else Board.BLACK
    best_value = -999999
    for option in board.options():
        if depth > 0:
            option_value = -1 * negamax_adversary(option, depth-1, enemy, -b, -a, ab)
        else:
            option_value = option.score(enemy) * -1
        option.value = option_value
        best_value = max(best_value, option_value)
        if ab:
            a = max(a, best_value)
            if a > b: break
    return best_value


def negamax_move(board, depth, ab=False):
    negamax_adversary(board, depth, ab=ab)
    best_opt = False
    for option in board.options():
        if best_opt is False:
            best_opt = option
        if best_opt.value < option.value:
            best_opt = option
    return best_opt


board = Board()

pvp = False
eve = True
alpha_beta = True

begin_time = current_milli_time()
try:
    while not board.finished():

        moves = board.calculate_moves()
        if len(moves) == 0:
            board.moves = board.moves + 1
            continue
        player_turn = board.turn() == Board.BLACK
        if eve:
            board = negamax_move(board, 4, alpha_beta)
            print(board)

            continue

        elif player_turn or pvp:
            # Manual move
            print("Possible moves for {}:".format(board.turn()))
            print(moves)
            choice = input()
            if ' ' in choice:
                choice = choice.split(' ')
                choice = (int(choice[0]) - 1) * Board.SIZE + int(choice[1]) - 1
            choice = int(choice)
            if choice not in moves:
                print("Not valid!")
                continue
            # End manual move
        else:
            board = negamax_move(board, 3, alpha_beta)
            print(board)
            continue
        board = board.move(choice)
        print(board)
    print("Black: {}, White: {}".format(board.score(Board.BLACK), board.score(Board.WHITE)))
    # print(board.calculate_moves())
except KeyboardInterrupt:
    print("\nBye!")

end_time = current_milli_time()
print("We took {} milliseconds to get to this score!".format(end_time - begin_time))