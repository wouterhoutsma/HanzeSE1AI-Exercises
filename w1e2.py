import random

n = 16
loop_nodes = True


class Node:
    def __init__(self, x, y, character):
        self.x = x
        self.y = y
        self.char = character
        self.neighbours = []
        self.part_of_n_words = 0

    def add_neighbour(self, node):
        self.neighbours.append(node)

    def inc_parts_n(self):
        self.part_of_n_words = self.part_of_n_words + 1

    def __str__(self):
        colours = [
            '\033[0m',
            '\033[92m',  # OKGREEN
            '\033[93m',  # Warning
            '\033[94m',  # OKBLUE
        ]
        colour = colours[3] if self.part_of_n_words >= 3 else colours[self.part_of_n_words]
        return colour + self.char + '\033[0m'


def dfs(word, node, path=[]):
    global loop_nodes
    if not loop_nodes:
        if node in path:
            return False
    path.append(node)
    # Check if path + this node == word.
    comparison = ''
    for element in path:
        comparison = comparison + element.char
    if comparison == word:
        return path
    # Check if this node is correct for the word.
    if word[len(path) - 1: len(path)] == node.char:
        for child in node.neighbours:
            new_path = dfs(word, child, path)
            if new_path is not False:
                return new_path
    return False

words = []
with open('words.txt', 'r') as myfile:
    for line in myfile:
        words.append(line)
words = set(words)

# Generate graph
characters = 'abcdefghijklmnopqrstuvwxyz'  # missing characters, can't have all words
nodes = {}
for x in range(0, n):
    nodes[x] = {}
    for y in range(0, n):
        nodes[x][y] = Node(x, y, characters[random.randint(0, len(characters)-1)])

# We now have a 2 dimensional list of Nodes. Now we have to find the neighbours for each node.
for x in range(0, n):
    for y in range(0, n):
        node = nodes[x][y]
        if x > 0:
            node.add_neighbour(nodes[x-1][y])
        if x < n - 1:
            node.add_neighbour(nodes[x+1][y])
        if y > 0:
            node.add_neighbour(nodes[x][y-1])
        if y < n - 1:
            node.add_neighbour(nodes[x][y+1])

for word in words:
    word = word.strip()
    for x in nodes:
        for y in nodes[x]:
            path = dfs(word, nodes[x][y], [])
            if path:
                print(str(path[0].y + 1) + "," + str(path[0].x + 1) + ": " + word)
                for node in path:
                    node.inc_parts_n()

# Print board
print('  ', end='')
for y in nodes[0]:
    print('___', end=' ')
print()
for x in nodes:
    print(' | ', end='')
    for y in nodes[x]:
        print(nodes[x][y], end=' | ')
    print('')
    print('  ', end='')
    for y in nodes[x]:
        print('___', end=' ')
    print('')
