import math
from queue import PriorityQueue
ucs = False


class Board:
    def __init__(self, n, previous=None):
        self.board = {}
        self.n = n
        self.previous = previous if previous is not None else []
        self.score = False
        for i in range(n):
            self.board[i] = {}
            for j in range(n):
                self.board[i][j] = None

    def set_number(self, x, y, number):
        self.board[y][x] = int(number)

    def digit_offset(self, digit, x, y):
        pref_y = math.floor((digit - 1) / self.n)
        pref_x = digit - pref_y * self.n - 1
        return abs(pref_x - x) + abs(pref_y - y)

    def calc_score(self):
        if not self.score:
            global ucs
            if ucs:
                return len(self.previous) + 1
            score = len(self.previous)
            for y in self.board:
                for x in self.board[y]:
                    number = self.board[y][x]
                    if number != 0:
                        offset = self.digit_offset(number, x, y)
                        score += offset**2  # sq(Offset) <= minimal distance to target
            self.score = score
        return int(self.score)

    def is_goal(self):
        score = self.calc_score() - len(self.previous)
        if score > 0:
            return False
        return True

    def __lt__(self, other):
        return self.calc_score() < other.calc_score()

    # needed for not in / in list comparison
    def __eq__(self, other):
        return self.board == other.board

    def options(self):
        # Find zero
        options = []
        zero_coords = (0, 0)
        for y in self.board:
            for x in self.board:
                if self.board[y][x] == 0:
                    zero_coords = (x, y)

        if zero_coords[0] > 0:
            # Swap left
            board = self.copy()
            board.previous.append(self)
            board.swap(zero_coords[0], zero_coords[1], zero_coords[0] - 1, zero_coords[1])
            if board not in self.previous:
                options.append(board)
        if zero_coords[0] < self.n - 1:
            # Swap right
            board = self.copy()
            board.previous.append(self)
            board.swap(zero_coords[0], zero_coords[1], zero_coords[0] + 1, zero_coords[1])
            if board not in self.previous:
                options.append(board)
        if zero_coords[1] > 0:
            # Swap above
            board = self.copy()
            board.previous.append(self)
            board.swap(zero_coords[0], zero_coords[1], zero_coords[0], zero_coords[1] - 1)
            if board not in self.previous:
                options.append(board)
        if zero_coords[1] < self.n - 1:
            # Swap below
            board = self.copy()
            board.previous.append(self)
            board.swap(zero_coords[0], zero_coords[1], zero_coords[0], zero_coords[1] + 1)
            if board not in self.previous:
                options.append(board)
        return options

    def swap(self, x1, y1, x2, y2):
        temp = self.board[y1][x1]
        self.board[y1][x1] = self.board[y2][x2]
        self.board[y2][x2] = temp

    def copy(self):
        board = Board(self.n, self.previous.copy())
        for y in self.board:
            for x in self.board[y]:
                board.set_number(x, y, self.board[y][x])
        return board

    def __str__(self):
        string = "______\n"
        for y in self.board:
            for x in self.board[y]:
                string = string + str(self.board[y][x]) + " "
            string = string + "\n"
        return string + "______"


def astar(queue):
    goal = None
    count = 0
    done = []
    while not queue.empty():
        p, board = queue.get()
        done.append(board)
        if board.is_goal():
            goal = board
            break
        for option in board.options():
            if option not in done:
                queue.put((option.calc_score(), option))
        count += 1
    print("Found {} in {} iterations, path is {} steps".format("nothing" if goal is None else "goal", count, len(goal.previous)-1))
    return goal
#
# start = """0 1 3
# 5 2 6
# 4 7 8"""

start = """8 6 7
2 5 4
3 0 1"""

temp_board = start.split('\n')
size = len(temp_board)
board = Board(size)
for i in range(len(temp_board)):
    y = temp_board[i].split(' ')
    for j in range(len(y)):
        board.set_number(j, i, y[j])

queue = PriorityQueue()
queue.put((board.calc_score(), board))
board = astar(queue)

print("__________________")
for boards in board.previous:
    print(boards)
print(board)

