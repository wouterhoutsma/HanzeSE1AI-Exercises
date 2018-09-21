class Path:
    def __init__(self, nodelist):
        self.nodes = nodelist
        self.base = nodelist[0].get_num()
        self.end = nodelist[-1].get_num()
        self.valid = len(nodelist) == self.end - self.base + 1

    def fill_zeroes(self):
        inc = 0
        for node in self.nodes:
            node.add_num(self.base + inc)
            inc = inc + 1

    def cancel(self):
        for node in self.nodes:
            node.pop()

    def __str__(self):
        string = ""
        for node in self.nodes:
            string = string + str(node) + ', '
        return string[0:-2] + '\n'


class Node:
    def __init__(self, number):
        self.numbers = [number]
        self.neighbours = []

    def add_neighbour(self, node):
        self.neighbours.append(node)

    def get_num(self):
        return self.numbers[-1]

    def add_num(self, number):
        self.numbers.append(number)

    def pop(self):
        self.numbers.pop()

    def __str__(self):
        return str(self.get_num())


def generate_paths(node, nodelist=None):
    paths = []
    if nodelist is None:
        nodelist = []
    nodelist.append(node)
    for neighbour in node.neighbours:
        # is a link in path, not a goal
        if neighbour in nodelist:
            continue
        if neighbour.get_num() == 0:
            # generate paths
            new_paths = generate_paths(neighbour, nodelist.copy())
            for path in new_paths:
                paths.append(path)
        else:
            end_list = nodelist.copy()
            end_list.append(neighbour)
            path = Path(end_list)
            if path.valid:
                paths.append(path)
    return paths


def dfs(node):
    global goal
    paths = generate_paths(node)
    lowest = goal
    good_paths = []
    for path in paths:
        if path.end < lowest:
            lowest = path.end
            good_paths = []
        if path.end == lowest:
            good_paths.append(path)
    paths = good_paths
    for path in paths:
        path.fill_zeroes()
        if path.end == goal:
            return True
        if dfs(path.nodes[-1]):
            return True

        path.cancel()
    return False
s = """
0  0  0  0  0  0  0  0 81
0  0 46 45  0 55 74  0  0
0 38  0  0 43  0  0 78  0
0 35  0  0  0  0  0 71  0
0  0 33  0  0  0 59  0  0
0 17  0  0  0  0  0 67  0
0 18  0  0 11  0  0 64  0
0  0 24 21  0  1  2  0  0
0  0  0  0  0  0  0  0  0 """
s = s.replace('  ', ' ')
board = s.strip().split('\n')
goal = 0
for i in range(len(board)):
    board[i] = board[i].split(' ')
    goal = goal + 1 * len(board)

new_board = {}
for x in range(len(board)):
    new_board[x] = {}
    for y in range(len(board[x])):
        node = Node(int(board[x][y]))
        new_board[x][y] = node
        if x > 0:
            cnode = new_board[x-1][y]
            cnode.add_neighbour(node)
            node.add_neighbour(cnode)
        if y > 0:
            cnode = new_board[x][y-1]
            cnode.add_neighbour(node)
            node.add_neighbour(cnode)

first = new_board[7][5]
dfs(first)

for y in new_board.keys():
    for x in new_board[y].keys():
        print(new_board[y][x], end='\t')
    print('')