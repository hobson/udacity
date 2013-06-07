#probutil.py

# stdlib
import math
import bisect
import math
import random
import sys

# AIMA
from graphutil import UndirectedGraph, Graph, Node, RandomGraph

# map route planning problem from Udacity class
romania = UndirectedGraph(Dict(
    A=Dict(Z=75, S=140, T=118),
    B=Dict(U=85, P=101, G=90, F=211),
    C=Dict(D=120, R=146, P=138),
    D=Dict(M=75),
    E=Dict(H=86),
    F=Dict(S=99),
    H=Dict(U=98),
    I=Dict(V=92, N=87),
    L=Dict(T=111, M=70),
    O=Dict(Z=71, S=151),
    P=Dict(R=97),
    R=Dict(S=80),
    U=Dict(V=142)))
romania.locations = Dict(
    A=( 91, 492),    B=(400, 327),    C=(253, 288),   D=(165, 299),
    E=(562, 293),    F=(305, 449),    G=(375, 270),   H=(534, 350),
    I=(473, 506),    L=(165, 379),    M=(168, 339),   N=(406, 537),
    O=(131, 571),    P=(320, 368),    R=(233, 410),   S=(207, 457),
    T=( 94, 410),    U=(456, 350),    V=(509, 444),   Z=(108, 531))

australia = UndirectedGraph(Dict(
    T=Dict(),
    SA=Dict(WA=1, NT=1, Q=1, NSW=1, V=1),
    NT=Dict(WA=1, Q=1),
    NSW=Dict(Q=1, V=1)))
australia.locations = Dict(WA=(120, 24), NT=(135, 20), SA=(135, 30),
                           Q=(145, 20), NSW=(145, 32), T=(145, 42), V=(145, 37))


class Problem(object):
    """The abstract class for a formal problem.  You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        abstract

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        abstract

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        abstract


class GraphProblem(Problem):
    "The problem of searching a graph from one node to another."
    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph

    def actions(self, A):
        "The actions at a graph node are just its neighbors."
        return self.graph.get(A).keys()

    def result(self, state, action):
        "The result of going to a neighbor is just that neighbor."
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A,B) or infinity)

    def h(self, node):
        "h function is straight-line distance from a node's state to goal."
        locs = getattr(self.graph, 'locations', None)
        if locs:
            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return infinity


class NQueensProblem(Problem):
    """The problem of placing N queens on an NxN board with none attacking
    each other.  A state is represented as an N-element array, where
    a value of r in the c-th entry means there is a queen at column c,
    row r, and a value of None means that the c-th column has not been
    filled in yet.  We fill in columns left to right.
    >>> depth_first_tree_search(NQueensProblem(8))
    <Node [7, 3, 0, 2, 5, 1, 6, 4]>
    """
    def __init__(self, N):
        self.N = N
        self.initial = [None] * N

    def actions(self, state):
        "In the leftmost empty column, try all non-conflicting rows."
        if state[-1] is not None:
            return [] # All columns filled; no successors
        else:
            col = state.index(None)
            return [row for row in range(self.N)
                    if not self.conflicted(state, row, col)]

    def result(self, state, row):
        "Place the next queen at the given row."
        col = state.index(None)
        new = state[:]
        new[col] = row
        return new

    def conflicted(self, state, row, col):
        "Would placing a queen at (row, col) conflict with anything?"
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        "Would putting two queens in (row1, col1) and (row2, col2) conflict?"
        return (row1 == row2 ## same row
                or col1 == col2 ## same column
                or row1-col1 == row2-col2  ## same \ diagonal
                or row1+col1 == row2+col2) ## same / diagonal

    def goal_test(self, state):
        "Check if all columns filled, no conflicts."
        if state[-1] is None:
            return False
        return not any(self.conflicted(state, state[col], col)
                       for col in range(len(state)))

# Inverse Boggle: Search for a high-scoring Boggle board. A good domain for
# iterative-repair and related search techniques, as suggested by Justin Boyan.

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

cubes16 = ['FORIXB', 'MOQABJ', 'GURILW', 'SETUPL',
           'CMPDAE', 'ACITAO', 'SLCRAE', 'ROMASH',
           'NODESW', 'HEFIYE', 'ONUDTK', 'TEVIGN',
           'ANEDVZ', 'PINESH', 'ABILYT', 'GKYLEU']

def random_boggle(n=4):
    """Return a random Boggle board of size n x n.
    We represent a board as a linear list of letters."""
    cubes = [cubes16[i % 16] for i in range(n*n)]
    random.shuffle(cubes)
    return map(random.choice, cubes)

# The best 5x5 board found by Boyan, with our word list this board scores
# 2274 words, for a score of 9837

boyan_best = list('RSTCSDEIAEGNLRPEATESMSSID')

def print_boggle(board):
    "Print the board in a 2-d array."
    n2 = len(board); n = exact_sqrt(n2)
    for i in range(n2):
        if i % n == 0 and i > 0: print
        if board[i] == 'Q': print 'Qu',
        else: print str(board[i]) + ' ',
    print

def boggle_neighbors(n2, cache={}):
    """Return a list of lists, where the i-th element is the list of indexes
    for the neighbors of square i."""
    if cache.get(n2):
        return cache.get(n2)
    n = exact_sqrt(n2)
    neighbors = [None] * n2
    for i in range(n2):
        neighbors[i] = []
        on_top = i < n
        on_bottom = i >= n2 - n
        on_left = i % n == 0
        on_right = (i+1) % n == 0
        if not on_top:
            neighbors[i].append(i - n)
            if not on_left:  neighbors[i].append(i - n - 1)
            if not on_right: neighbors[i].append(i - n + 1)
        if not on_bottom:
            neighbors[i].append(i + n)
            if not on_left:  neighbors[i].append(i + n - 1)
            if not on_right: neighbors[i].append(i + n + 1)
        if not on_left: neighbors[i].append(i - 1)
        if not on_right: neighbors[i].append(i + 1)
    cache[n2] = neighbors
    return neighbors

def exact_sqrt(n2):
    "If n2 is a perfect square, return its square root, else raise error."
    n = int(math.sqrt(n2))
    assert n * n == n2
    return n

#_____________________________________________________________________________

class Wordlist:
    """This class holds a list of words. You can use (word in wordlist)
    to check if a word is in the list, or wordlist.lookup(prefix)
    to see if prefix starts any of the words in the list."""
    def __init__(self, filename, min_len=3):
        lines = open(filename).read().upper().split()
        self.words = [word for word in lines if len(word) >= min_len]
        self.words.sort()
        self.bounds = {}
        for c in ALPHABET:
            c2 = chr(ord(c) + 1)
            self.bounds[c] = (bisect.bisect(self.words, c),
                              bisect.bisect(self.words, c2))

    def lookup(self, prefix, lo=0, hi=None):
        """See if prefix is in dictionary, as a full word or as a prefix.
        Return two values: the first is the lowest i such that
        words[i].startswith(prefix), or is None; the second is
        True iff prefix itself is in the Wordlist."""
        words = self.words
        if hi is None: hi = len(words)
        i = bisect.bisect_left(words, prefix, lo, hi)
        if i < len(words) and words[i].startswith(prefix):
            return i, (words[i] == prefix)
        else:
            return None, False

    def __contains__(self, word):
        return self.lookup(word)[1]

    def __len__(self):
        return len(self.words)

#_____________________________________________________________________________

class BoggleFinder:
    """A class that allows you to find all the words in a Boggle board. """

    wordlist = None ## A class variable, holding a wordlist

    def __init__(self, board=None):
        if BoggleFinder.wordlist is None:
            BoggleFinder.wordlist = Wordlist("../data/EN-text/wordlist")
        self.found = {}
        if board:
            self.set_board(board)

    def set_board(self, board=None):
        "Set the board, and find all the words in it."
        if board is None:
            board = random_boggle()
        self.board = board
        self.neighbors = boggle_neighbors(len(board))
        self.found = {}
        for i in range(len(board)):
            lo, hi = self.wordlist.bounds[board[i]]
            self.find(lo, hi, i, [], '')
        return self

    def find(self, lo, hi, i, visited, prefix):
        """Looking in square i, find the words that continue the prefix,
        considering the entries in self.wordlist.words[lo:hi], and not
        revisiting the squares in visited."""
        if i in visited:
            return
        wordpos, is_word = self.wordlist.lookup(prefix, lo, hi)
        if wordpos is not None:
            if is_word:
                self.found[prefix] = True
            visited.append(i)
            c = self.board[i]
            if c == 'Q': c = 'QU'
            prefix += c
            for j in self.neighbors[i]:
                self.find(wordpos, hi, j, visited, prefix)
            visited.pop()

    def words(self):
        "The words found."
        return self.found.keys()

    scores = [0, 0, 0, 0, 1, 2, 3, 5] + [11] * 100

    def score(self):
        "The total score for the words found, according to the rules."
        return sum([self.scores[len(w)] for w in self.words()])

    def __len__(self):
        "The number of words found."
        return len(self.found)

#_____________________________________________________________________________

def boggle_hill_climbing(board=None, ntimes=100, verbose=True):
    """Solve inverse Boggle by hill-climbing: find a high-scoring board by
    starting with a random one and changing it."""
    finder = BoggleFinder()
    if board is None:
        board = random_boggle()
    best = len(finder.set_board(board))
    for _ in range(ntimes):
        i, oldc = mutate_boggle(board)
        new = len(finder.set_board(board))
        if new > best:
            best = new
            if verbose: print best, _, board
        else:
            board[i] = oldc ## Change back
    if verbose:
        print_boggle(board)
    return board, best

def mutate_boggle(board):
    i = random.randrange(len(board))
    oldc = board[i]
    board[i] = random.choice(random.choice(cubes16)) ##random.choice(boyan_best)
    return i, oldc

#______________________________________________________________________________

# Code to compare searchers on various problems.

class InstrumentedProblem(Problem):
    """Delegates to a problem, and keeps statistics."""

    def __init__(self, problem):
        self.problem = problem
        self.succs = self.goal_tests = self.states = 0
        self.found = None

    def actions(self, state):
        self.succs += 1
        return self.problem.actions(state)

    def result(self, state, action):
        self.states += 1
        return self.problem.result(state, action)

    def goal_test(self, state):
        self.goal_tests += 1
        result = self.problem.goal_test(state)
        if result:
            self.found = state
        return result

    def path_cost(self, c, state1, action, state2):
        return self.problem.path_cost(c, state1, action, state2)

    def value(self, state):
        return self.problem.value(state)

    def __getattr__(self, attr):
        return getattr(self.problem, attr)

    def __repr__(self):
        return '<%4d/%4d/%4d/%s>' % (self.succs, self.goal_tests,
                                     self.states, str(self.found)[:4])

def compare_searchers(problems, header,
                      searchers=[breadth_first_tree_search,
                                 breadth_first_search, depth_first_graph_search,
                                 iterative_deepening_search,
                                 depth_limited_search,
                                 recursive_best_first_search]):
    def do(searcher, problem):
        p = InstrumentedProblem(problem)
        searcher(p)
        return p
    table = [[name(s)] + [do(s, p) for p in problems] for s in searchers]
    print_table(table, header)

def compare_graph_searchers():
    """Prints a table of results like this:
>>> compare_graph_searchers()
Searcher                      Romania(A, B)        Romania(O, N)         Australia          
breadth_first_tree_search     <  21/  22/  59/B>   <1158/1159/3288/N>    <   7/   8/  22/WA>
breadth_first_search          <   7/  11/  18/B>   <  19/  20/  45/N>    <   2/   6/   8/WA>
depth_first_graph_search      <   8/   9/  20/B>   <  16/  17/  38/N>    <   4/   5/  11/WA>
iterative_deepening_search    <  11/  33/  31/B>   < 656/1815/1812/N>    <   3/  11/  11/WA>
depth_limited_search          <  54/  65/ 185/B>   < 387/1012/1125/N>    <  50/  54/ 200/WA>
recursive_best_first_search   <   5/   6/  15/B>   <5887/5888/16532/N>   <  11/  12/  43/WA>"""
    compare_searchers(problems=[GraphProblem('A', 'B', romania),
                                GraphProblem('O', 'N', romania),
                                GraphProblem('Q', 'WA', australia)],
            header=['Searcher', 'Romania(A, B)', 'Romania(O, N)', 'Australia'])


__doc__ += """
>>> ab = GraphProblem('A', 'B', romania)
>>> breadth_first_tree_search(ab).solution()
['S', 'F', 'B']
>>> breadth_first_search(ab).solution()
['S', 'F', 'B']
>>> uniform_cost_search(ab).solution()
['S', 'R', 'P', 'B']
>>> depth_first_graph_search(ab).solution()
['T', 'L', 'M', 'D', 'C', 'P', 'B']
>>> iterative_deepening_search(ab).solution()
['S', 'F', 'B']
>>> len(depth_limited_search(ab).solution())
50
>>> astar_search(ab).solution()
['S', 'R', 'P', 'B']
>>> recursive_best_first_search(ab).solution()
['S', 'R', 'P', 'B']

>>> board = list('SARTELNID')
>>> print_boggle(board)
S  A  R 
T  E  L 
N  I  D 
>>> f = BoggleFinder(board)
>>> len(f)
206
"""

__doc__ += random_tests("""
>>> ' '.join(f.words())
'LID LARES DEAL LIE DIETS LIN LINT TIL TIN RATED ERAS LATEN DEAR TIE LINE INTER STEAL LATED LAST TAR SAL DITES RALES SAE RETS TAE RAT RAS SAT IDLE TILDES LEAST IDEAS LITE SATED TINED LEST LIT RASE RENTS TINEA EDIT EDITS NITES ALES LATE LETS RELIT TINES LEI LAT ELINT LATI SENT TARED DINE STAR SEAR NEST LITAS TIED SEAT SERAL RATE DINT DEL DEN SEAL TIER TIES NET SALINE DILATE EAST TIDES LINTER NEAR LITS ELINTS DENI RASED SERA TILE NEAT DERAT IDLEST NIDE LIEN STARED LIER LIES SETA NITS TINE DITAS ALINE SATIN TAS ASTER LEAS TSAR LAR NITE RALE LAS REAL NITER ATE RES RATEL IDEA RET IDEAL REI RATS STALE DENT RED IDES ALIEN SET TEL SER TEN TEA TED SALE TALE STILE ARES SEA TILDE SEN SEL ALINES SEI LASE DINES ILEA LINES ELD TIDE RENT DIEL STELA TAEL STALED EARL LEA TILES TILER LED ETA TALI ALE LASED TELA LET IDLER REIN ALIT ITS NIDES DIN DIE DENTS STIED LINER LASTED RATINE ERA IDLES DIT RENTAL DINER SENTI TINEAL DEIL TEAR LITER LINTS TEAL DIES EAR EAT ARLES SATE STARE DITS DELI DENTAL REST DITE DENTIL DINTS DITA DIET LENT NETS NIL NIT SETAL LATS TARE ARE SATI'

>>> boggle_hill_climbing(list('ABCDEFGHI'), verbose=False)
(['E', 'P', 'R', 'D', 'O', 'A', 'G', 'S', 'T'], 123)
""")