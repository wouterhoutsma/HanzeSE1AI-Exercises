class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

























# # eerst maken we een graph met de startNode (start punt 0,0)
# class Graph:
#     def populate(self, grid, node):
#         # starts at 0,0 continues to 24,0 (x first)
#         for y in range(len(grid)):
#             for x in range(1, len(grid)):
#                 newNode = Node(x, y, grid[x][y] == "b")
#                 self.listOfNodes.append(newNode)
#         self.fixNeighbors(grid)
#
#     def fixNeighbors(self, grid):
#         # Notice order is important (-1, 0 is the left neighbour). Uses tuples
#         neighborsX = -1, 0, 1, 0
#         neighborsY = 0, -1, 0, 1
#         for node in self.listOfNodes:
#             for i in range(len(neighborsX)):
#                 x = node.x + neighborsX[i]
#                 y = node.y + neighborsX[i]
#                 if x < 0 or y < 0 or x > len(grid)-1 or y > len(grid)-1: continue;
#                 node.addNeighbor(self.getNodeFromList(x, y))
#
#     def getNodeFromList(self, x, y):
#         for node in self.listOfNodes:
#             if node.x == x and node.y == y: return node;
#
#     def __str__(self):
#         result = ""
#         for node in self.listOfNodes:
#             result = result + "\n" + str(node)
#         return result
#
#     def __init__(self):
#         self.startNode = Node(0, 0)
#         self.endNode = Node(24, 24)
#         self.startNode.g = self.startNode.h = self.startNode.f = 0
#         self.endNode.g = self.endNode.h = self.endNode.f = 0
#         self.listOfNodes = [self.startNode];
#
# class Node:
#     def __init__(self, x, y, blocked = False):
#         self.neighbors = []
#         self.x = x
#         self.y = y
#         self.parent = None
#         self.blocked = blocked
#         self.populated = False
#         self.fValue = None
#         self.gValue = None
#         self.hValue = None
#
#     def setPopulated(self): self.populated = True
#
#     def __str__(self):
#         return "| {0},{1} = blocked({2}) | neighbors: {3}".format(
#             self.x, self.y, self.blocked, len(self.neighbors)
#         )
#
#     def addNeighbor(self, node): self.neighbors.append(node)
