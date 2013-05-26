'''
States are represented as a tuple of (p, me, you, pending) where
p:       an int, 0 or 1, indicating which player's turn it is.
me:      an int, the player-to-move's current score
you:     an int, the other player's current score.
pending: an int, the number of points accumulated on current turn, not yet scored
'
'''

import random
from functools import update_wrapper
import itertools
import collections
import fractions

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(*args)
    _f.cache = cache
    return _f

################################################################################
## This defines the game of PIG -- the "what"

def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    (p, me, you, pending) = state
    if d == 1:
        return (other[p], you, me+1, 0) # pig out; other player's turn
    else:
        return (p, me, you, pending+d)  # accumulate die roll in pending

def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    (p, me, you, pending) = state
    return (other[p], you, me+pending, 0)

def dierolls():
    "Generate die rolls."
    while True:
        yield random.randint(1, 6)

other = {1:0, 0:1}    # mapping from player to other player
goal  = 40

def play_pig(A, B, dierolls = dierolls()):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    strategies = [A, B]
    state = (0, 0, 0, 0)
    while True:
        (p, me, you, pending) = state
        if me >= goal:
            return strategies[p]
        elif you >= goal:
            return strategies[other[p]]
        else:
            action = strategies[p](state)
            if action == 'hold':
                state = hold(state)
            elif action == 'roll':
                state = roll(state, next(dierolls))
            else: # Illegal action?  You lose!
                return strategies[other[p]]

################################################################################
## This defines strategies for playing Pig -- the "how"

def bad_strategy(state):
    "A strategy that could never win, unless a player makes an illegal move"
    return 'hold'

def illegal_strategy(state):
    return 'I want to win pig please.'

def Q_pig(state, action, Pwin):
    "The expected value of choosing action in state."
    if action == 'hold':
        return 1 - Pwin(hold(state))
    if action == 'roll':
        return (1 - Pwin(roll(state, 1))
                + sum(Pwin(roll(state, d)) for d in (2, 3, 4, 5, 6))) / 6.
    raise ValueError

def best_action(state, actions, Q, U):
    "Return the optimal action for a state, given U."
    def EU(action): return Q(state, action, U)
    return max(actions(state), key = EU)

def pig_actions(state):
    "The legal actions from a state."
    _, _, _, pending = state
    return ['roll', 'hold'] if pending else ['roll']

@memo
def Pwin(state):
    """The utility of a state; here just the probability that an optimal player
    whose turn it is to move can win from the current state."""
    # Assumes opponent also plays with optimal strategy.
    (p, me, you, pending) = state
    if me + pending >= goal:
        return 1
    elif you >= goal:
        return 0
    else:
        return max(Q_pig(state, action, Pwin)
                   for action in pig_actions(state))

@memo
def win_diff(state):
    "The utility of a state: here the winning differential (pos or neg)."
    (p, me, you, pending) = state
    if me + pending >= goal or you >= goal:
        return (me + pending - you)
    else:
        return max(Q_pig(state, action, win_diff)
                   for action in pig_actions(state))

def max_diffs(state):
    """A strategy that maximizes the expected difference between my final score
    and my opponent's."""
    return best_action(state, pig_actions, Q_pig, win_diff)

def max_wins(state):
    "The optimal pig strategy chooses an action with the highest win probability."
    return best_action(state, pig_actions, Q_pig, Pwin)

possible_moves = ['roll', 'hold']

def clueless(state):
    "A strategy that ignores the state and chooses at random from possible moves."
    return random.choice(possible_moves)

def always_roll(state):
    return 'roll'

def always_hold(state):
    return 'hold'

def hold_at(x):
    """Return a strategy that holds if and only if
    pending >= x or player reaches goal."""
    def strategy(state):
        (p, me, you, pending) = state
        return 'hold' if (pending >= x or me + pending >= goal) else 'roll'
    strategy.__name__ = 'hold_at(%d)' % x
    return strategy

################################################################################
## Simulation

strategies = [clueless, hold_at(goal/4), hold_at(1+goal/3), hold_at(goal/2),
              hold_at(goal), max_wins]

def play_tournament(strategies, series_length = 50):
    result = collections.defaultdict(int)
    for A, B in itertools.combinations(strategies, 2):
        for _ in range(series_length):
            if play_pig(A, B) == A:
                result[A, B] += 1
            else:
                result[B, A] += 1
            if play_pig(B, A) == A:
                result[A, B] += 1
            else:
                result[B, A] += 1
    result = dict(result)
    print(report_tournament(strategies, result))

def report_tournament(strategies, result):
    N = len(strategies)
    table = []
    for s in strategies:
        items = [result.get((s, t), 0) for t in strategies]
        items = ['{0:<15}'.format(s.__name__)]+map('{0:>5}'.format, items + [sum(items)])
        print(' '.join(items))


################################################################################
## Exploratory data analysis

states = [(0, me, you, pending)
          for me in range(goal+1)
          for you in range(goal+1)
          for pending in range(goal+1)
          if me + pending <= goal]

def compare_strategies(A, B):
    print(len(states))
    r = collections.defaultdict(int)
    for s in states:
        r[A(s), B(s)] += 1
    r = dict(r)
    print(r)

def story():
    r = collections.defaultdict(lambda: [0, 0])
    for s in states:
        w, d = max_wins(s), max_diffs(s)
        if w != d:
            _, _, _, pending = s
            i = 0 if (w == 'roll') else 1
            r[pending][i] += 1
    for (delta, (wrolls, drolls)) in sorted(r.items()):
        print('%4d: %3d %3d'%(delta, wrolls, drolls))

################################################################################
## Tests

def test():
    winner = play_pig(bad_strategy, illegal_strategy)
    assert winner.__name__ == 'bad_strategy'

    # The first three test cases are examples where max_wins and
    # max_diffs return the same action.
    assert max_diffs((1, 26, 21, 15)) == "hold"
    assert max_diffs((1, 23, 36, 7))  == "roll"
    assert max_diffs((0, 29, 4, 3))   == "roll"
    # The remaining test cases are examples where max_wins and
    # max_diffs return different actions.
    assert max_diffs((0, 36, 32, 5))  == "roll"
    assert max_diffs((1, 37, 16, 3))  == "roll"
    assert max_diffs((1, 33, 39, 7))  == "roll"
    assert max_diffs((0, 7, 9, 18))   == "hold"
    assert max_diffs((1, 0, 35, 35))  == "hold"
    assert max_diffs((0, 36, 7, 4))   == "roll"
    assert max_diffs((1, 5, 12, 21))  == "hold"
    assert max_diffs((0, 3, 13, 27))  == "hold"
    assert max_diffs((0, 0, 39, 37))  == "hold"

    assert max_wins((1, 5, 34, 4))   == "roll"
    assert max_wins((1, 18, 27, 8))  == "roll"
    assert max_wins((0, 23, 8, 8))   == "roll"
    assert max_wins((0, 31, 22, 9))  == "hold"
    assert max_wins((1, 11, 13, 21)) == "roll"
    assert max_wins((1, 33, 16, 6))  == "roll"
    assert max_wins((1, 12, 17, 27)) == "roll"
    assert max_wins((1, 9, 32, 5))   == "roll"
    assert max_wins((0, 28, 27, 5))  == "roll"
    assert max_wins((1, 7, 26, 34))  == "hold"
    assert max_wins((1, 20, 29, 17)) == "roll"
    assert max_wins((0, 34, 23, 7))  == "hold"
    assert max_wins((0, 30, 23, 11)) == "hold"
    assert max_wins((0, 22, 36, 6))  == "roll"
    assert max_wins((0, 21, 38, 12)) == "roll"
    assert max_wins((0, 1, 13, 21))  == "roll"
    assert max_wins((0, 11, 25, 14)) == "roll"
    assert max_wins((0, 22, 4, 7))   == "roll"
    assert max_wins((1, 28, 3, 2))   == "roll"
    assert max_wins((0, 11, 0, 24))  == "roll"

    A, B = hold_at(50), clueless
    rolls = iter([6]*9)
    assert play_pig(A, B, rolls) == A

    for _ in range(10):
        winner = play_pig(always_hold, always_roll)
        assert winner.__name__ == 'always_roll'

    global goal
    goal = 50
    assert hold_at(30)((1, 29, 15, 20)) == 'roll'
    assert hold_at(30)((1, 29, 15, 21)) == 'hold'
    assert hold_at(15)((0, 2, 30, 10))  == 'roll'
    assert hold_at(15)((0, 2, 30, 15))  == 'hold'

    assert hold((1, 10, 20, 7))    == (0, 20, 17, 0)
    assert hold((0, 5, 15, 10))    == (1, 15, 15, 0)
    assert roll((1, 10, 20, 7), 1) == (0, 20, 11, 0)
    assert roll((0, 5, 15, 10), 5) == (0, 5, 15, 15)
    goal = 40
    return 'tests pass'

if __name__ == '__main__':
    print test()

    # play_tournament(strategies)
    '''
    |               |  0 |  1 |  2 |  3 |  4 |  5 | total |
    |---------------+----+----+----+----+----+----+-------|
    | clueless 0    |  0 |  2 |  2 |  4 |  6 |  9 |    23 |
    | hold_at(10) 1 | 98 |  0 | 44 | 27 | 43 | 27 |   239 |
    | hold_at(14) 2 | 98 | 56 |  0 | 55 | 43 | 36 |   288 |
    | hold_at(20) 3 | 96 | 73 | 45 |  0 | 50 | 50 |   314 |
    | hold_at(40) 4 | 94 | 57 | 57 | 50 |  0 | 53 |   311 |
    | max_wins 5    | 91 | 73 | 64 | 50 | 47 |  0 |   325 |
    '''

    # play_tournament(strategies, 2000)
    '''
    |               |    0 |    1 |    2 |     3 |    4 |    5 | total |
    |---------------+------+------+------+-------+------+------+-------|
    | clueless 0    |    0 |  120 |  115 |   123 |  231 |  178 |   767 |
    | hold_at(10) 1 | 3880 |    0 | 1559 |  1230 | 1467 | 1333 |  9469 |
    | hold_at(14) 2 | 3885 | 2441 |    0 | 01605 | 1705 | 1549 | 11185 |
    | hold_at(20) 3 | 3877 | 2770 | 2395 |     0 | 2004 | 1860 | 12906 |
    | hold_at(40) 4 | 3769 | 2533 | 2295 |  1996 |    0 | 1974 | 12567 |
    | max_wins 5    | 3822 | 2667 | 2451 |  2140 | 2026 |    0 | 13106 |

    '''

    # compare_strategies(max_wins, max_diffs)
    '''
    {('hold', 'hold'): 1204,  ('hold', 'roll'): 381,
     ('roll', 'roll'): 29741, ('roll', 'hold'): 3975}
    '''

    # story()
    '''
       2:   0  40
       3:   0  40
       4:   0  40
       5:   0  40
       6:   0  40
       7:   0  40
       8:   0  40
       9:   0  40
      10:   0  28
      11:   0  19
      12:   0  12
      13:   0   2
      16:  11   0
      17:  68   0
      18: 128   0
      19: 201   0
      20: 287   0
      21: 327   0
      22: 334   0
      23: 322   0
      24: 307   0
      25: 290   0
      26: 281   0
      27: 253   0
      28: 243   0
      29: 213   0
      30: 187   0
      31: 149   0
      32: 125   0
      33:  95   0
      34:  66   0
      35:  31   0
      36:  22   0
      37:  16   0
      38:  11   0
      39:   7   0
      40:   1   0
    '''
