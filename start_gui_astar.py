import tkinter as tk
from tkinter import ttk
from w1e4 import Node
from queue import PriorityQueue

import random

#assuming a resulution of 1920 x 1080 = 16 : 9

# global color scheme
bgc = '#FDF6E3'
gridc = '#542437'
blockc = 'red'
pathc = 'blue'
startc = '#C7F464'
goalc = 'yellow'

# global vars
PAUSE_STATUS = False
PROB = 0.2 # probability blocking node
SIZE  = 25 # the nr of nodes=grid crossings in a row (or column)

# global var: pixel sizes
CELL  = 35 # size of cell/square in pixels
W  = (SIZE-1) * CELL # width of grid in pixels
H  = W # height of grid
TR = 10 # translate/move the grid, upper left is 10,10

grid  = [[0 for x in range(SIZE)] for y in range(SIZE)]
start = (0, 0)
goal  = (SIZE-1, SIZE-1)

# class PriorityQueue:
#     # to be use in the A* algorithm
#     # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
#     # in a min-heap, the keys of parent nodes are less than or equal to those
#     # of the children and the lowest key is in the root node
#     def __init__(self):
#         # create a min heap (as a list)
#         self.elements = []
#
#     def empty(self):
#         return len(self.elements) == 0
#
#     # heap elements are tuples (priority, item)
#     def put(self, item, priority):
#         heapq.heappush(self.elements, (priority, item))
#
#     # pop returns the smallest item from the heap
#     # i.e. the root element = element (priority, item) with highest priority
#     def get(self):
#         return heapq.heappop(self.elements)[1]

def bernoulli_trial():
    return 1 if random.random() < PROB else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value

def make_grid(c):
    # vertical lines
    for i in range(0, W+1, CELL):
        c.create_line(i+TR, 0+TR, i+TR, H+TR, fill = gridc)

    # horizontal lines
    for i in range(0, H+1, CELL):
        c.create_line(0+TR, i+TR, W+TR, i+TR, fill = gridc)

def init_grid(c):
    for x in range(SIZE):
        for y in range(SIZE):
            node = (x, y)
            # start and goal cannot be bloking nodes
            if bernoulli_trial() and node != start and node != goal:
                set_grid_value(node, 'b') # blocked
                plot_node(c, node, color=blockc)
            else:
                set_grid_value(node, -1)  # init costs, -1 means infinite

def plot_line_segment(c, x0, y0, x1, y1):
    c.create_line(x0*CELL+TR, y0*CELL+TR, x1*CELL+TR, y1*CELL+TR, fill = pathc, width = 2)

def plot_node(c, node, color):
    # size of (red) rectangle is 8 by 8
    x0 = node[0] * CELL - 4
    y0 = node[1] * CELL - 4
    x1 = x0 + 8 + 1
    y1 = y0 + 8 + 1
    c.create_rectangle(x0+TR, y0+TR, x1+TR, y1+TR, fill = color)

def control_panel():
    mf = ttk.LabelFrame(right_frame)
    mf.grid(column=0, row=0, padx=8, pady=4)
    mf.grid_rowconfigure(2, minsize=10)

    def start():
        # With help of Nicholas W. Swift
        # used info from: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
        start = (0, 0)
        end = (24, 24)
        if bt_alg.get() == "A*": path = aStar(grid, start, end)
        else: path = UCS(grid, start, end)
        print("path is {}".format(path))
        print("total path length is: {}".format(len(path)))
        # plot a sample path for demonstration
        for i in range(len(path)-1):
            # def plot_line_segment(c, x0, y0, x1, y1):
            plot_line_segment(canvas, path[i][0], path[i][1], path[i+1][0], path[i+1][1])

    def pause():
        global PAUSE_STATUS
        if PAUSE_STATUS:
            pause_button.configure(background='SystemButtonFace')
            PAUSE_STATUS = False
        else:
            pause_button.configure(background='red')
            PAUSE_STATUS = True

    start_button = tk.Button(mf, text="Start", command=start, width=10)
    start_button.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    pause_button = tk.Button(mf, text="Pause", command=pause, width=10)
    pause_button.grid(row=2, column=1, sticky='w', padx=5, pady=5)

    def sel():
        print('algorithm =', bt_alg.get())

    r1_button = tk.Radiobutton(mf, text='UCS', value='UCS', variable=bt_alg, command=sel)
    r2_button = tk.Radiobutton(mf, text='A*', value='A*', variable=bt_alg, command=sel)
    bt_alg.set('UCS')

    r1_button.grid(row=3, column=1, columnspan=2, sticky='w')
    r2_button.grid(row=4, column=1, columnspan=2, sticky='w')

    def box_update1(event):
        print('speed is set to:', box1.get())

    def box_update2(event):
        print('prob. blocking is set to:', box2.get())

    lf = ttk.LabelFrame(right_frame, relief="sunken")
    lf.grid(column=0, row=1, padx=5, pady=5)

    ttk.Label(lf, text="Speed ").grid(row=1, column=1, sticky='w')
    box1 = ttk.Combobox(lf, textvariable=speed, state='readonly', width=6)
    box1.grid(row=2, column=1, sticky='w')
    box1['values'] = tuple(str(i) for i in range(10))
    box1.current(5)
    box1.bind("<<ComboboxSelected>>", box_update1)

    ttk.Label(lf, text="Prob. blocking").grid(row=3, column=1, sticky='w')
    box2 = ttk.Combobox(lf, textvariable=prob, state='readonly', width=6)
    box2.grid(row=4, column=1, sticky='ew')
    box2['values'] = tuple(str(i) for i in range(10))
    box2.current(3)
    box2.bind("<<ComboboxSelected>>", box_update2)

root = tk.Tk()
root.title('A* demo')

speed = tk.StringVar()
prob = tk.StringVar()
bt_alg = tk.StringVar()
left_frame = ttk.Frame(root, padding="3 3 12 12")
left_frame.grid(column=0, row=0)

right_frame = ttk.Frame(root, padding="3 3 12 12")
right_frame.grid(column=1, row=0)

canvas = tk.Canvas(left_frame, height=H+4*TR, width=W+4*TR, borderwidth=-TR, bg = bgc)
canvas.pack(fill=tk.BOTH, expand=True)

make_grid(canvas)
init_grid(canvas)

# show start and goal nodes
plot_node(canvas, start, color=startc)
plot_node(canvas, goal, color=goalc)

# plot a path found by a*
# gridGraph = Graph()
# gridGraph.populate(grid, gridGraph.rootNode)

def pythagoreanDistanceEstimate(child, endNode):
    return (
        (child.position[0] - endNode.position[0]) ** 2
    ) + (
        (child.position[1] - endNode.position[1]) ** 2
    )

def aStar(grid, start, end):
    startNode = Node(None, start)
    startNode.g = startNode.h = startNode.f = 0
    endNode = Node(None, end)
    endNode.g = endNode.h = endNode.f = 0

    openList = PriorityQueue()
    closedList = []

    openList.put((startNode.g, startNode))
    while not openList.empty():
        pos, currentNode = openList.get()

        closedList.append(currentNode)

        # Found the goal, endNode (backtracking and forming the final path)
        if currentNode == endNode:
            print("found goal node at {}".format(currentNode.position))
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return in reverse order

        # Generate children
        children = []
        adjustments = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for newPosition in adjustments:
            # childPosition is the (oldPositionX + adjustmentX, oldPositionY + adjustmentY)
            childPosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])
            if childPosition[0] > len(grid)-1 or childPosition[1] > len(grid)-1: continue
            if childPosition[0] < 0 or childPosition[1] < 0: continue
            if grid[childPosition[0]][childPosition[1]] == 'b': continue
            newChildNode = Node(currentNode, childPosition)
            children.append(newChildNode)

        # Loop through the generated children
        for child in children:
            if child in closedList: continue
            # Set the f, g and h values
            child.g = currentNode.g + 1
            child.h = pythagoreanDistanceEstimate(child, endNode)
            child.f = child.g + child.h

            # Child is already in the openList
            match = False
            for openNode in openList.queue:
                if child == openNode[1]: match = True
                if match and child.g > openNode[1].g: break # worse path
                if match and child.g < openNode[1].g: # better path
                    openNode[1].parent = currentNode
                    openNode[1].g = currentNode.g + 1
                    openNode[1].f = child.g + child.h
            # if the child is found on the openList, with a better path: continue
            if match: continue
            openList.put((child.g, child))

def UCS(grid, start, end):
    startNode = Node(None, start)
    endNode = Node(None, end)
    startNode.f = endNode.f = 0

    openList = []
    closedList = []

    openList.append(startNode)
    while len(openList) > 0:
        currentNode = openList[0]
        currentIndex = 0
        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                currentIndex = index

        openList.pop(currentIndex)
        closedList.append(currentNode)

        # Found the goal, endNode (backtracking and forming the final path)
        if currentNode == endNode:
            print("found goal node at {}".format(currentNode.position))
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return in reverse order

        # Generate children
        children = []
        adjustments = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for newPosition in adjustments:
            # childPosition is the (oldPositionX + adjustmentX, oldPositionY + adjustmentY)
            childPosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])
            if childPosition[0] > len(grid)-1 or childPosition[1] > len(grid)-1: continue
            if childPosition[0] < 0 or childPosition[1] < 0: continue
            if grid[childPosition[0]][childPosition[1]] == 'b': continue
            newChildNode = Node(currentNode, childPosition)
            children.append(newChildNode)

        # Loop through the generated children
        for child in children:
            if child in closedList: continue
            # Set the f value
            child.f = currentNode.f + 1

            # Child is already in the openList
            match = False
            for openNode in openList:
                if child == openNode: match = True
                if match and child.f > openNode.f: break # worse path
                if match and child.f < openNode.f: # better path
                    openNode.parent = currentNode
                    openNode.f = currentNode.f + 1
            # if the child is found on the openList, with a better path: continue
            if match: continue
            openList.append(child)





control_panel()

root.mainloop()
