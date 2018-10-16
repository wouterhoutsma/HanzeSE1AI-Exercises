import random
import sys
sys.setrecursionlimit(1000)

'''
Script layout;
    Functions
    Variable initialization
    Function calls
'''

# Functions
def roll(state, d):
    '''Apply a die roll d to yield a new state:
    If d == 1, it's a pig-out, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn.
    If d > 1, add d to 'pending' points.
    '''
    if d != 1: return {
        'p': state['p'], 'p1Score': state['p1Score'],
        'p2Score': state['p2Score'], 'pending': state['pending'] + d,
        'bestX': state['bestX']
    }
    # print("Pig-out!")
    if state['p']: return {
        'p': not state['p'], 'p1Score': state['p1Score'],
        'p2Score': state['p2Score'] + 1, 'pending': 0,
        'bestX': state['bestX']
    }
    return {
        'p': not state['p'], 'p1Score': state['p1Score'] + 1,
        'p2Score': state['p2Score'], 'pending': 0,
        'bestX': state['bestX']
    }

def hold(state):
    '''Apply a hold to yield a new state: add the pending points to my total points and
    it becomes the other player's turn.
    '''
    if state['p']: return {
        'p': not state['p'], 'p1Score': state['p1Score'],
        'p2Score': state['p2Score'] + state['pending'], 'pending': 0,
        'bestX': state['bestX']
    }
    return {
        'p': not state['p'], 'p1Score': state['p1Score'] + state['pending'],
        'p2Score': state['p2Score'], 'pending': 0,
        'bestX': state['bestX']
    }

def clueless(state):
    # print("clueless turn", state)
    if random.random() > 0.50: state = roll(state, random.randint(1, 6))
    else: state = hold(state)
    return state

def holdAtX(state):
    # select current players scoreKey in the state dictionary
    # and holdAtX value (if two players use the same strategy with diff values)
    scoreKey = 'p1Score'
    x = HOLD_AT_X
    if state['p']:
        scoreKey = 'p2Score'
        x = HOLD_AT_X2

    # goal will be reached when pending is added
    if (state['pending'] + state[scoreKey]) >= GOAL: state = hold(state)
    # pending reached: hold value of x
    elif state['pending'] >= HOLD_AT_X: state = hold(state)
    # keep rolling until we reach a pending value of x
    else: state = roll(state, random.randint(1, 6))

    return state

def compareHoldAt(x, y, startState, nGames):
    # compare a holdAt value of x versus that of y
    winsX = winsY = 0
    for i in range(nGames):
        endState = holdAtX(startState, x)
        if endState['p1Score'] >= GOAL: winsX = winsX + 1

        endState = holdAtX(startState, y)
        if endState['p1Score'] >= GOAL: winsY = winsY + 1
    return dict(x=x, y=y, winsX=winsX, winsY=winsY, nGames=nGames, startState=startState)

def bestHoldAtXValue(state):
    # select current players scoreKey in the state dictionary
    scoreKey = 'p1Score'
    if state['p']: scoreKey = 'p2Score'

    # goal will be reached when pending is added
    if (state['pending'] + state[scoreKey]) >= GOAL: hold_value = GOAL
    # based on state['pending'], what is the expected holdValue and rollValue
    holdValue = state['pending']
    rollValue = (
        (
            ( (state['pending']*-1) + 1 )
            + (state['pending']+2)
            + (state['pending']+3)
            + (state['pending']+4)
            + (state['pending']+5)
            + (state['pending']+6)
        ) / 6
    )
    # print("values; hold({0}) roll({1})".format(holdValue, rollValue))
    # print(state)

    if holdValue > rollValue:
        if state['bestX'] == 0: state['bestX'] = holdValue
        else: state['bestX'] = (state['bestX'] + holdValue) / 2
        state = hold(state)
    else:
        state = roll(state, random.randint(1, 6))

    return state

def bestAction(state):
    # return the optimal action for a state
    # define key expectedValue for max function
    def expectedValue(action): return evalAction(state, action)
    return max(legalActions(state), key=expectedValue)

def evalAction(state, action):
    '''The expected value of an action in this state.
    pWin is the utility function, i.e. the probability of winning: 1 point for winning and 0 points for loosing
    We will look into the possible future, consider all legal actions, until the goal is reached
    '''
    # if we hold, our opponent will move, our probability of winning is 1 - pWin(opponent)
    if action == 'hold':
        if (state['pending'] + state['p1Score']) >= GOAL: return 1
        return 1 - pWin(hold(state), 0)
    # if d==1: it's a pig-out, our opponent will move, our probability of winning is 1 - pWin(opponent)
    # if d >1: get pWin for each value of d and calculate average
    if action == 'roll':
        return (1 - pWin(roll(state, 1), 0) + sum(pWin(roll(state, d), 1) for d in (2,3,4,5,6))) / 6.0
    raise ValueError

def legalActions(state):
    # The legal actions from a state. If pending == 0 then we must roll
    if state['pending'] == 0: return ['roll']
    return ['roll', 'hold']

def pWin(state, player):
    # The value of a state: the probability that an optimal player whose turn it is
    # can win from the current state. Returns a value between 0.00 and 1.00
    if isGameover(state): return 1 if state['p'] else 0
    if not state['p'] and (state['pending'] + state['p1Score']) >= GOAL:
        return 1
    if state['p'] and (state['pending'] + state['p2Score']) >= GOAL:
        return 0

    nextStates = []
    if 'hold' in legalActions(state): nextStates.append(hold(state))
    for i in range(2, 7):
        nextStates.append(roll(state, i))

    results = []
    for nextState in nextStates:
        results.append(pWin(nextState, player))

    return results.count(player) / len(results)

def playOptimal(state):
    # print("playOptimal turn", state)
    action = bestAction(state)
    if action == 'hold': state = hold(state)
    else: state = roll(state, random.randint(1, 6))
    return state

def isGameover(state):
    return state['p1Score'] >= GOAL or state['p2Score'] >= GOAL

def playPig(p1Strat, p2Strat, state):
    if isGameover(state): return state
    if state['p'] == False: state = p1Strat(state)
    elif state['p'] == True: state = p2Strat(state)
    # print("turn state is", state)
    return playPig(p1Strat, p2Strat, state)

# Variable initialization
GOAL = 10
HOLD_AT_X = 20      # P1
HOLD_AT_X2 = 10     # P2
# p1 == False, p2 == True
startState = {'p': False, 'p1Score': 0, 'p2Score': 0, 'pending': 0, 'bestX': 0}

# Function calls

# endState = playPig(holdAtX, holdAtX, startState)
# playerWon = '1' if endState['p'] else '2'
# strategy = "holdAtX({})".format(HOLD_AT_X) if endState['p'] else "holdAtX({})".format(HOLD_AT_X2)
# print("endState:", endState)
# print("player {0} wins with the {1} strategy".format(playerWon, strategy))
# C
# games = []
# p1 = 0
# p2 = 0
# while len(games) < 100:
#     endState = playPig(holdAtX, holdAtX, startState)
#     p1 = (p1 + 1) if endState['p'] else p1
#     p2 = (p2 + 1) if not endState['p'] else p2
#     games.append(endState)
# print("holdAtX(20) won {0} of a 100 games".format(p1))
# print("holdAtX(10) won {0} of a 100 games".format(p2))

# D
# endState = bestHoldAtXValue(startState)
# print("game has ended with the following endState:", endState)
#
# E
# foundAction = bestAction(startState)
# print("The best action to start for p1 is", foundAction)
# endState = playOptimal(startState)
# print("Optimal game results: ", endState)
#
# F
endState = playPig(playOptimal, clueless, startState)
print("final state after playing with a goal of {0}".format(GOAL), endState)

# print("startState: ", startState)
# print("the best action for a goal of 6 is: ", bestAction(startState))
# nextState = playOptimal(startState) # player 1, turn 1 (uses bestAction)
# i = 1
# print("turn {0}:".format(i), nextState)
# while nextState['p1Score'] <= GOAL and nextState['p2Score'] <= GOAL:
#     i = i + 1
#     nextState = playOptimal(nextState)
#     print("turn {0}:".format(i), nextState)

# Wat is de beste keuze bij aan het begin bij goal = 6, dus wat is dan best_action(('me', 0, 0, 0)))?
# print("best action for 6 is", bestAction(startState))
# Wat is mijn kans op winnen als ik begin bij een goal = 6, m.a.w. wat is de waarde van p_win(('me', 0, 0, 0))?
# print("pWin(startState) with a goal of 6, is", pWin(startState))
# Wat is mijn kans op winnen als ik begin bij een goal = 40?
# GOAL = 40
# print("pWin(startState) with a goal of 40 is", pWin(startState))
