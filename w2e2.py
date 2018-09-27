from collections import namedtuple
import random

GOAL = 6

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
    if state['p1Score'] >= GOAL or state['p2Score'] >= GOAL: return state
    randomFloat = random.random()
    if randomFloat > 0.50: state = roll(state, random.randint(1, 6))
    else: state = hold(state)
    return clueless(state)

def holdAtX(state, x):
    # goal reached
    if state['p1Score'] >= GOAL or state['p2Score'] >= GOAL: return state

    # select current players scoreKey in the state dictionary
    scoreKey = 'p1Score'
    if state['p']: scoreKey = 'p2Score'

    # goal will be reached when pending is added
    if (state['pending'] + state[scoreKey]) >= GOAL: state = hold(state)
    # pending reached: hold value of x
    elif state['pending'] >= x: state = hold(state)
    # keep rolling until we reach a pending value of x
    else: state = roll(state, random.randint(1, 6))

    # next turn
    return holdAtX(state, x)

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
    # goal reached
    if state['p1Score'] >= GOAL or state['p2Score'] >= GOAL: return state

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
    print("values; hold({0}) roll({1})".format(holdValue, rollValue))
    print(state)

    if holdValue > rollValue:
        if state['bestX'] == 0: state['bestX'] = holdValue
        else: state['bestX'] = (state['bestX'] + holdValue) / 2
        state = hold(state)
    else:
        state = roll(state, random.randint(1, 6))

    return bestHoldAtXValue(state)

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
        return 1 - pWin(hold(state))
    # if d==1: it's a pig-out, our opponent will move, our probability of winning is 1 - pWin(opponent)
    # if d >1: get pWin for each value of d and calculate average
    if action == 'roll':
        return (1 - pWin(roll(state, 1)) + sum(pWin(roll(state, d)) for d in (2,3,4,5,6))) / 6.0
    raise ValueError

def legalActions(state):
    # The legal actions from a state. If pending == 0 then we must roll
    if state['pending'] == 0: return ['roll']
    return ['roll', 'hold']

def pWin(state):
    # The value of a state: the probability that an optimal player whose turn it is
    # can win from the current state.
    currPlayer = 'p1Score'
    otherPlayer = 'p2Score'
    if state['p']:
        currPlayer = 'p2Score'
        otherPlayer = 'p1Score'

    actions = ['roll', 'hold']
    while True:
        if state[currPlayer] >= GOAL: return 1
        if state[otherPlayer] >= GOAL: return 0
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
        if holdValue > rollValue: state = hold(state)
        else: state = roll(state, random.randint(1, 6))

def playOptimal(state):
    action = None
    while state['p1Score'] < GOAL and state['p2Score'] < GOAL:
        action = bestAction(state)
        # call function, by referencing its name as a string
        if action == 'hold': state = hold(state)
        else: state = roll(state, random.randint(1, 6))
    return state

GOAL = 40
# p1 == False, p2 == True
startState = {'p': False, 'p1Score': 0, 'p2Score': 0, 'pending': 0, 'bestX': 0}
# A
# endState = clueless(startState)
# print("game has ended with the following endState:", endState)
#
# B
# endState = holdAtX(startState, 20)
# print("game has ended with the following endState:", endState)
#
# C
# results = compareHoldAt(10, 20, startState, 100)
# print("results are: ", results)
# print("A value of 10 had {0} first player wins over {1} games".format(results['winsX'], results['nGames']))
# print("A value of 20 had {0} first player wins over {1} games".format(results['winsY'], results['nGames']))
#
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
GOAL = 6
endState = playOptimal(startState)
print("final state after playing with a goal of 6", endState)

# Wat is de beste keuze bij aan het begin bij goal = 6, dus wat is dan best_action(('me', 0, 0, 0)))?
print("best action for 6 is", bestAction(startState))
# Wat is mijn kans op winnen als ik begin bij een goal = 6, m.a.w. wat is de waarde van p_win(('me', 0, 0, 0))?
print("pWin(startState) with a goal of 6, is", pWin(startState))
# Wat is mijn kans op winnen als ik begin bij een goal = 40?
GOAL = 40
print("pWin(startState) with a goal of 40 is", pWin(startState))
