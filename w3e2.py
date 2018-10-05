from itertools import permutations

class Node():
    def __init__(self, parent, options, board, children=[]):
        self.board = board
        self.parent = parent
        self.children = children
        self.options = options

    def __eq__(self, other):
        if type(other) is not Node: return False
        return self.board == other.board

    def __str__(self):
        return str(self.moves)

def ContinueException(arg):
    pass

def ace(neighbors, l):
    king = False
    for neighbor in neighbors:
        if l[neighbor] == 'q': return False
        if l[neighbor] == 'a': return False
        if l[neighbor] == 'k': king = True
    return king

def king(neighbors, l):
    queen = False
    for neighbor in neighbors:
        if l[neighbor] == 'k': return False
        if l[neighbor] == 'q': queen = True
    return queen

def queen(neighbors, l):
    jack = False
    for neighbor in neighbors:
        if l[neighbor] == 'q': return False
        if l[neighbor] == 'j': jack = True
    return jack

def jack(neighbors, l):
    for neighbor in neighbors:
        if l[neighbor] == 'j': return False
    return True

def boardIsValid(board):
    for i in range(len(board)):
        if board[i] == 'a' and not ace(neighbors[i], board): return False
        if board[i] == 'k' and not king(neighbors[i], board): return False
        if board[i] == 'q' and not queen(neighbors[i], board): return False
        if board[i] == 'j' and not jack(neighbors[i], board): return False
    return True

def dfs(cards, board=[0,0,0,0,0,0,0,0]):
    if not boardIsValid(board):
        return False
    if len(cards) == 0:
        if boardIsValid(board):
            return board
        return False

    for i in range(len(board)):
        if board[i] != 0: continue
        for card in cards:
            t_board = board.copy()
            t_board[i] = card
            t_cards = cards.copy()
            t_cards.remove(card)
            result = dfs(t_cards, t_board)
            if result == False: continue
            else: return result
    return False

# Week 3, Opgave 2
board = [ 0, 1, 2, 3, 4, 5, 6, 7 ]
neighbors = [ [3], [2], [1,3,4], [0,2,5], [2,5], [3,4,6,7], [5], [5] ]
cards = ['a', 'a', 'k', 'k', 'q', 'q', 'j', 'j']

result = None
# for l in list(permutations(cards)):
#     try:
#         for i in range(len(l)):
#             if l[i] == 'a' and not ace(neighbors[i], l): raise ValueError()
#             if l[i] == 'k' and not king(neighbors[i], l): raise ValueError()
#             if l[i] == 'q' and not queen(neighbors[i], l): raise ValueError()
#             if l[i] == 'j' and not jack(neighbors[i], l): raise ValueError()
#             result = l
#     except:
#         continue
#     break

result = dfs(cards)
# print(result)
print('. . {} .'.format(result[0]))
print('{} {} {} .'.format(result[1], result[2], result[3]))
print('. {} {} {}'.format(result[4], result[5], result[6]))
print('. . {} .'.format(result[7]))
