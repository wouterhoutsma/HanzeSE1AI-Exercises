import math
ucs = False


class Board:
    def __init__(self, n, previous=None):
        self.board = {}
        self.n = n
        self.previous = previous if previous is not None else []
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

    def score(self):
        global ucs
        if ucs:
            return len(self.previous) + 1
        score = len(self.previous)
        for y in self.board:
            for x in self.board[y]:
                number = self.board[y][x]
                if number != 0:
                    score += self.digit_offset(number, x, y)
        return int(score)

    def is_goal(self):
        for y in self.board:
            for x in self.board[y]:
                number = self.board[y][x]
                if number != 0:
                    if self.digit_offset(number, x, y) > 0:
                        return False
        return True

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
        string = "\n______\n"
        for y in self.board:
            for x in self.board[y]:
                string = string + str(self.board[y][x]) + " "
            string = string + "\n"
        return string + "______\n"


class PriorityQueue:
    def __init__(self):
        self.queue = {}
        self.visited = []

    def add(self, board, priority):
        if board in self.visited:
            return
        priority = int(priority)
        if priority not in self.queue:
            self.queue[priority] = []
        self.queue[priority].append(board)

    def next(self):
        lowest = None
        for key in self.queue.keys():
            if lowest is None or lowest > key:
                lowest = key
        return_value = self.queue[lowest].pop()
        if len(self.queue[lowest]) == 0:
            self.queue.pop(lowest)
        self.visited.append(return_value)
        return return_value

    def __str__(self):
        string = ""
        for key in self.queue.keys():
            string = string + str(key) + ', '
        return string[0:-2]


# def astar(queue):
#     board = queue.next()
#     if board.is_goal():
#         return board
#     for option in board.options():
#         queue.add(option, option.score())
#
#     return astar(queue)

def astar(queue):
    goal = None
    i = 0
    while goal is None:
        i += 1
        if i % 1000 == 0:
            print(i)
        board = queue.next()
        if board.is_goal():
            goal = board
        for option in board.options():
            queue.add(option, option.score())
    print(i)
    return goal

start = """2 5 8
0 6 3
1 4 7"""

# start = """0 1 3
# 5 2 6
# 4 7 8"""

temp_board = start.split('\n')
size = len(temp_board)
board = Board(size)
for i in range(len(temp_board)):
    y = temp_board[i].split(' ')
    for j in range(len(y)):
        board.set_number(j, i, y[j])

queue = PriorityQueue()
queue.add(board, board.score())
board = astar(queue)

print("__________________")
for boards in board.previous:
    print(boards)
print(board)

