'''
* Concept Inventory
** board         2D array
** letters       str
** words         str
** hand          str
** legal play    fn(pos, dir, word)
** score         fn
** letters       {'Z':10}
** play          fn
** bonus         pos --> DW (double word), TL (triple letter) 
** dictionary    set(words)
** blank         str ' ', '_'
'''

import time
import doctest

NOPLAY = None

POINTS = dict(A = 1, B = 3, C = 3, D = 2, E = 1, F = 4, G = 2, H = 4, I = 1,
              J = 8, K = 5, L = 1, M = 3, N = 1, O = 1, P = 3, Q = 10, R = 1,
              S = 1, T = 1, U = 1, V = 4, W = 4, X = 8, Y = 4, Z = 10, _ = 0)

ACROSS, DOWN = (1, 0), (0, 1) # Directions that words can go

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

class anchor(set):
    "An anchor is where a new word can be placed; has a set of allowable letters."

ANY = anchor(LETTERS) # The anchor that can be any letter

################################################################################
## Utilities

def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

def is_letter(sq):
    return isinstance(sq, str) and sq in LETTERS

def is_empty(sq):
    "Is this an empty square (no letters, but a valid position on board)."
    return sq  == '.' or sq == '*' or isinstance(sq, anchor) 

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]
            
def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    wordset = set(file(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

def transpose(matrix):
    "Transpose e.g. [[1,2,3], [4,5,6]] to [[1, 4], [2, 5], [3, 6]]"
    # or [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
    return map(list, zip(*matrix))

def neighbors(board, i, j):
    """Return a list of the contents of the four neighboring squares,
    in the order N,S,E,W."""
    return [board[j-1][i], board[j+1][i],
            board[j][i+1], board[j][i-1]]

# On Unix use time.time, on Windows use time.clock
def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.time()
    result = fn(*args)
    t1 = time.time()
    return t1-t0, result

################################################################################
## Plays

def row_plays(hand, row):
    "Return a set of legal plays in row.  A row play is an (start, 'WORD') pair."
    results = set()
    ## To each allowable prefix, add all suffixes, keeping words
    for (i, sq) in enumerate(row[1:-1], 1):
        if isinstance(sq, anchor):
            pre, maxsize = legal_prefix(i, row)
            if pre: ## Add to the letters already on the board
                start = i - len(pre)
                add_suffixes(hand, pre, start, row, results, anchored = False)
            else: ## Empty to left: go through the set of all possible prefixes
                for pre in find_prefixes(hand):
                    if len(pre) <= maxsize:
                        start = i - len(pre)
                        add_suffixes(removed(hand, pre), pre, start, row, results,
                                     anchored = False)
    return results

def add_suffixes(hand, pre, start, row, results, anchored = True):
    "Add all possible suffixes, and accumulate (start, word) pairs in results."
    i = start + len(pre)
    if pre in WORDS and anchored and not is_letter(row[i]):
        results.add((start, pre))
    if pre in PREFIXES:       
        sq = row[i]
        if is_letter(sq):
            add_suffixes(hand, pre+sq, start, row, results)        
        elif is_empty(sq):        
            possibilities = sq if isinstance(sq, anchor) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes(hand.replace(L, '', 1), pre+L, start, row, results)
    return results

def legal_prefix(i, row):
    """A legal prefix of an anchor at row[i] is either a string of letters
    already on the board, or new letters that fit into an empty space.
    Return the tuple (prefix_on_board, maxsize) to indicate this.
    E.g. legal_prefix(9, a_row) == ('BE', 2) and for 6, ('', 2)."""
    s = i
    while is_letter(row[s-1]): s -= 1
    if s < i: ## There is a prefix
        return ''.join(row[s:i]), i-s
    while is_empty(row[s-1]) and not isinstance(row[s-1], anchor): s -= 1
    return ('', i-s)

prev_hand, prev_results = '', set() # cache for find_prefixes

def find_prefixes(hand, pre = '', results = None):
    """Find all prefixes (of words) that can be made from letters in hand."""
    ## Cache the most recent full hand (don't cache intermediate results)
    global prev_hand, prev_results
    if hand == prev_hand: return prev_results
    if results is None: results = set()
    if pre == '': prev_hand, prev_results = hand, results
    # Now do the computation
    if pre in WORDS or pre in PREFIXES: results.add(pre)
    if pre in PREFIXES:
        for L in hand:
            find_prefixes(hand.replace(L, '', 1), pre+L, results)
    return results

def horizontal_plays(hand, board):
    "Find all horizontal plays -- ((i, j), word) pairs -- across all rows."
    results = set()
    for (j, row) in enumerate(board[1:-1], 1):
        set_anchors(row, j, board)
        for (i, word) in row_plays(hand, row):
            score = calculate_score(board, (i, j), ACROSS, hand, word)
            results.add( (score, (i, j), word) )
    return results

def set_anchors(row, j, board):
    """Anchors are empty squares with a neighboring letter. Some are restricted
    by cross-words to be only a subset of letters."""
    for (i, sq) in enumerate(row[1:-1], 1):
        neighborlist = (N, S, E, W) = neighbors(board, i, j)
        # Anchors are squares adjacent to a letter.  Plus the '*' square.
        if sq == '*' or (is_empty(sq) and any(map(is_letter, neighborlist))):    
            if is_letter(N) or is_letter(S):   
                # Find letters that fit with the cross (vertical) word
                (j2, w) = find_cross_word(board, i, j)
                row[i] = anchor(L for L in LETTERS if w.replace('.', L) in WORDS)
            else: # Unrestricted empty square -- any letter will fit.
                row[i] = ANY

def find_cross_word(board, i, j):
    """Find the vertical word that crosses board[j][i]. Return (j2, w),
    where j2 is the starting row, and w is the word"""
    sq = board[j][i]
    w = sq if is_letter(sq) else '.'
    for j2 in range(j, 0, -1):
        sq2 = board[j2-1][i]
        if is_letter(sq2): w = sq2 + w
        else: break
    for j3 in range(j+1, len(board)):
        sq3 = board[j3][i]
        if is_letter(sq3): w = w + sq3
        else: break
    return (j2, w)

def all_plays(hand, board):
    """All plays in both directions. A play is a (pos, dir, word) tuple,
    where pos is an (i, j) pair, and dir is ACROSS or DOWN."""
    hplays = horizontal_plays(hand, board)            # set of ((i, j), word)
    vplays = horizontal_plays(hand, transpose(board)) # set of ((j, i), word)
    return (set((score, (i, j), ACROSS, word) for (score, (i, j), word) in hplays)
            | set((score, (i, j), DOWN, word) for (score, (j, i), word) in vplays))

def make_play(play, board):
    "Put the word down on the board."
    (score, (i, j), (di, dj), word) = play
    for (n, L) in enumerate(word):
        board[j+ n*dj][i + n*di] = L
    return board

def best_play(hand, board):
    "Return the highest-scoring play.  Or None."
    plays = all_plays(hand, board)
    return sorted(plays)[-1] if plays else NOPLAY

################################################################################
## Scoring

# hand is an argument but it is never used!
def calculate_score(board, pos, direction, hand, word):
    "Return the total score for this play."
    total, crosstotal, word_mult = 0, 0, 1
    starti, startj = pos
    di, dj = direction
    other_direction = DOWN if direction == ACROSS else ACROSS
    for (n, L) in enumerate(word):
        i, j = starti + n*di, startj + n*dj
        sq = board[j][i]
        b = BONUS[j][i]
        word_mult *= (1 if is_letter(sq) else
                      3 if b == TW else
                      2 if b in (DW, '*') else
                      1)
        letter_mult = (1 if is_letter(sq) else
                       3 if b == TL else
                       2 if b == DL else 1)
        total += POINTS[L] * letter_mult
        if isinstance(sq, anchor) and sq is not ANY and direction is not DOWN:
            crosstotal += cross_word_score(board, L, (i, j), other_direction)
    return crosstotal + word_mult * total

def cross_word_score(board, L, pos, direction):
    "Return the score of a word made in the other direction from the main word."
    i, j = pos
    (j2, word) = find_cross_word(board, i, j)
    return calculate_score(board, (i, j2), DOWN, L, word.replace('.', L))

################################################################################
## BONUS

def bonus_template(quadrant):
    "Make a board from the upper-left quadrant."
    return mirror(map(mirror, quadrant.split()))

def mirror(sequence): return sequence + sequence[-2::-1]

SCRABBLE = bonus_template("""
|||||||||
|3..:...3
|.2...;..
|..2...:.
|:..2...:
|....2...
|.;...;..
|..:...:.
|3..:...*
""")

WWF = bonus_template("""
|||||||||
|...3..;.
|..:..2..
|.:..:...
|3..;...2
|..:...:.
|.2...3..
|;...:...
|...:...*
""")

BONUS = WWF

DW, TW, DL, TL = '23:;'   

################################################################################
## Display routines

def show(board):
    """Print the board, and the BONUS[j][i] entries where appropriate.
    >>> show(a_board())
    | | | | | | | | | | | | | | | | |
    | J . . 3 . . ; . ; . . 3 . I . |
    | A . : . . 2 B E . C . . : D . |
    | G U Y . : . . F . H : . . L . |
    | | | | | | | | | | | | | | | | |
    """
    print('\n'.join(
        ' '.join(
            [letter if (is_letter(letter) or letter == '|') else BONUS[j][i]
             for i, letter in enumerate(row)])
        for j, row in enumerate(board)))

def show_best(hand, board):
    '''
    >>> show_best(a_hand, a_board())    
    Current board:
    | | | | | | | | | | | | | | | | |
    | J . . 3 . . ; . ; . . 3 . I . |
    | A . : . . 2 B E . C . . : D . |
    | G U Y . : . . F . H : . . L . |
    | | | | | | | | | | | | | | | | |
    <BLANKLINE>
    New word: 'BACKBENCH' scores 64
    | | | | | | | | | | | | | | | | |
    | J . . 3 . . ; . ; . . 3 . I . |
    | A . B A C K B E N C H . : D . |
    | G U Y . : . . F . H : . . L . |
    | | | | | | | | | | | | | | | | |
    '''
    print('Current board:')
    show(board)
    play = best_play(hand, board)
    if play:
        print('\nNew word: %r scores %d' % (play[-1], play[0]))
        show(make_play(play, board))
    else:
        print('Sorry, no legal plays')

################################################################################
## Tests

def a_board():
    return map(list, ['|||||||||||||||||',
                      '|J............I.|',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])

# >>> a_board()
# [['|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|'], 
#  ['|', 'J', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'I', '.', '|'],
#  ['|', 'A', '.', '.', '.', '.', '.', 'B', 'E', '.', 'C', '.', '.', '.', 'D', '.', '|'],
#  ['|', 'G', 'U', 'Y', '.', '.', '.', '.', 'F', '.', 'H', '.', '.', '.', 'L', '.', '|'], 
#  ['|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|']]

mnx = anchor(list('MNX'))
moab = anchor(list('MOAB'))

a_row = ['|', 'A', mnx, moab, '.', '.', ANY, 'B', 'E', ANY, 'C', ANY, '.', ANY,
         'D', ANY, '|']
a_hand = 'ABCEHKN'

hands = {  ## Regression test
    'ABECEDR': set(['BE', 'CARE', 'BAR', 'BA', 'ACE', 'READ', 'CAR', 'DE', 'BED', 'BEE',
         'ERE', 'BAD', 'ERA', 'REC', 'DEAR', 'CAB', 'DEB', 'DEE', 'RED', 'CAD',
         'CEE', 'DAB', 'REE', 'RE', 'RACE', 'EAR', 'AB', 'AE', 'AD', 'ED', 'RAD',
         'BEAR', 'AR', 'REB', 'ER', 'ARB', 'ARC', 'ARE', 'BRA']),
    'AEINRST': set(['SIR', 'NAE', 'TIS', 'TIN', 'ANTSIER', 'TIE', 'SIN', 'TAR', 'TAS',
         'RAN', 'SIT', 'SAE', 'RIN', 'TAE', 'RAT', 'RAS', 'TAN', 'RIA', 'RISE',
         'ANESTRI', 'RATINES', 'NEAR', 'REI', 'NIT', 'NASTIER', 'SEAT', 'RATE',
         'RETAINS', 'STAINER', 'TRAIN', 'STIR', 'EN', 'STAIR', 'ENS', 'RAIN', 'ET',
         'STAIN', 'ES', 'ER', 'ANE', 'ANI', 'INS', 'ANT', 'SENT', 'TEA', 'ATE',
         'RAISE', 'RES', 'RET', 'ETA', 'NET', 'ARTS', 'SET', 'SER', 'TEN', 'RE',
         'NA', 'NE', 'SEA', 'SEN', 'EAST', 'SEI', 'SRI', 'RETSINA', 'EARN', 'SI',
         'SAT', 'ITS', 'ERS', 'AIT', 'AIS', 'AIR', 'AIN', 'ERA', 'ERN', 'STEARIN',
         'TEAR', 'RETINAS', 'TI', 'EAR', 'EAT', 'TA', 'AE', 'AI', 'IS', 'IT',
         'REST', 'AN', 'AS', 'AR', 'AT', 'IN', 'IRE', 'ARS', 'ART', 'ARE']),
    'DRAMITC': set(['DIM', 'AIT', 'MID', 'AIR', 'AIM', 'CAM', 'ACT', 'DIT', 'AID', 'MIR',
         'TIC', 'AMI', 'RAD', 'TAR', 'DAM', 'RAM', 'TAD', 'RAT', 'RIM', 'TI',
         'TAM', 'RID', 'CAD', 'RIA', 'AD', 'AI', 'AM', 'IT', 'AR', 'AT', 'ART',
         'CAT', 'ID', 'MAR', 'MA', 'MAT', 'MI', 'CAR', 'MAC', 'ARC', 'MAD', 'TA',
         'ARM']),
    'ADEINRST': set(['SIR', 'NAE', 'TIS', 'TIN', 'ANTSIER', 'DEAR', 'TIE', 'SIN', 'RAD', 
         'TAR', 'TAS', 'RAN', 'SIT', 'SAE', 'SAD', 'TAD', 'RE', 'RAT', 'RAS', 'RID',
         'RIA', 'ENDS', 'RISE', 'IDEA', 'ANESTRI', 'IRE', 'RATINES', 'SEND',
         'NEAR', 'REI', 'DETRAIN', 'DINE', 'ASIDE', 'SEAT', 'RATE', 'STAND',
         'DEN', 'TRIED', 'RETAINS', 'RIDE', 'STAINER', 'TRAIN', 'STIR', 'EN',
         'END', 'STAIR', 'ED', 'ENS', 'RAIN', 'ET', 'STAIN', 'ES', 'ER', 'AND',
         'ANE', 'SAID', 'ANI', 'INS', 'ANT', 'IDEAS', 'NIT', 'TEA', 'ATE', 'RAISE',
         'READ', 'RES', 'IDS', 'RET', 'ETA', 'INSTEAD', 'NET', 'RED', 'RIN',
         'ARTS', 'SET', 'SER', 'TEN', 'TAE', 'NA', 'TED', 'NE', 'TRADE', 'SEA',
         'AIT', 'SEN', 'EAST', 'SEI', 'RAISED', 'SENT', 'ADS', 'SRI', 'NASTIER',
         'RETSINA', 'TAN', 'EARN', 'SI', 'SAT', 'ITS', 'DIN', 'ERS', 'DIE', 'DE',
         'AIS', 'AIR', 'DATE', 'AIN', 'ERA', 'SIDE', 'DIT', 'AID', 'ERN',
         'STEARIN', 'DIS', 'TEAR', 'RETINAS', 'TI', 'EAR', 'EAT', 'TA', 'AE',
         'AD', 'AI', 'IS', 'IT', 'REST', 'AN', 'AS', 'AR', 'AT', 'IN', 'ID', 'ARS',
         'ART', 'ANTIRED', 'ARE', 'TRAINED', 'RANDIEST', 'STRAINED', 'DETRAINS']),
    'ETAOIN': set(['ATE', 'NAE', 'AIT', 'EON', 'TIN', 'OAT', 'TON', 'TIE', 'NET', 'TOE',
         'ANT', 'TEN', 'TAE', 'TEA', 'AIN', 'NE', 'ONE', 'TO', 'TI', 'TAN',
         'TAO', 'EAT', 'TA', 'EN', 'AE', 'ANE', 'AI', 'INTO', 'IT', 'AN', 'AT',
         'IN', 'ET', 'ON', 'OE', 'NO', 'ANI', 'NOTE', 'ETA', 'ION', 'NA', 'NOT',
         'NIT']),
    'SHRDLU': set(['URD', 'SH', 'UH', 'US']),
    'SHROUDT': set(['DO', 'SHORT', 'TOR', 'HO', 'DOR', 'DOS', 'SOUTH', 'HOURS', 'SOD',
         'HOUR', 'SORT', 'ODS', 'ROD', 'OUD', 'HUT', 'TO', 'SOU', 'SOT', 'OUR',
         'ROT', 'OHS', 'URD', 'HOD', 'SHOT', 'DUO', 'THUS', 'THO', 'UTS', 'HOT',
         'TOD', 'DUST', 'DOT', 'OH', 'UT', 'ORT', 'OD', 'ORS', 'US', 'OR',
         'SHOUT', 'SH', 'SO', 'UH', 'RHO', 'OUT', 'OS', 'UDO', 'RUT']),
    'TOXENSI': set(['TO', 'STONE', 'ONES', 'SIT', 'SIX', 'EON', 'TIS', 'TIN', 'XI', 'TON',
         'ONE', 'TIE', 'NET', 'NEXT', 'SIN', 'TOE', 'SOX', 'SET', 'TEN', 'NO',
         'NE', 'SEX', 'ION', 'NOSE', 'TI', 'ONS', 'OSE', 'INTO', 'SEI', 'SOT',
         'EN', 'NIT', 'NIX', 'IS', 'IT', 'ENS', 'EX', 'IN', 'ET', 'ES', 'ON',
         'OES', 'OS', 'OE', 'INS', 'NOTE', 'EXIST', 'SI', 'XIS', 'SO', 'SON',
         'OX', 'NOT', 'SEN', 'ITS', 'SENT', 'NOS'])}

def test():
    assert len(WORDS)    == 3892
    assert len(PREFIXES) == 6475
    assert 'UMIAQS' in WORDS
    assert 'MOVING' in WORDS
    assert 'UNDERSTANDIN' in PREFIXES
    assert 'ZOMB' in PREFIXES
    assert (word_plays('ADEQUAT', set('IRE')) ==
            set(['DIE', 'ATE', 'READ', 'AIT', 'DE', 'IDEA', 'RET', 'QUID',
                 'DATE', 'RATE', 'ETA', 'QUIET', 'ERA', 'TIE', 'DEAR', 'AID',
                 'TRADE', 'TRUE', 'DEE', 'RED', 'RAD', 'TAR', 'TAE', 'TEAR',
                 'TEA', 'TED', 'TEE', 'QUITE', 'RE', 'RAT', 'QUADRATE', 'EAR',
                 'EAU', 'EAT', 'QAID', 'URD', 'DUI', 'DIT', 'AE', 'AI', 'ED',
                 'TI', 'IT', 'DUE', 'AQUAE', 'AR', 'ET', 'ID', 'ER', 'QUIT',
                 'ART', 'AREA', 'EQUID', 'RUE', 'TUI', 'ARE', 'QI', 'ADEQUATE',
                 'RUT']))
    assert (longest_words('ADEQUAT', set('IRE')) == ['QUADRATE', 'ADEQUATE',
        'QUIET', 'TRADE', 'QUITE', 'AQUAE', 'EQUID', 'READ', 'IDEA', 'QUID', 'DATE',
        'RATE', 'DEAR', 'TRUE', 'TEAR', 'QAID', 'QUIT', 'AREA', 'DIE', 'ATE', 'AIT',
        'RET', 'ETA', 'ERA', 'TIE', 'AID', 'DEE', 'RED', 'RAD', 'TAR', 'TAE', 'TEA',
        'TED', 'TEE', 'RAT', 'EAR', 'EAU', 'EAT', 'URD', 'DUI', 'DIT', 'DUE', 'ART',
        'RUE', 'TUI', 'ARE', 'RUT', 'DE', 'RE', 'AE', 'AI', 'ED', 'TI', 'IT', 'AR',
        'ET', 'ID', 'ER', 'QI'])
    assert prefixes('hello') == ['', 'h', 'he', 'hel', 'hell']
    assert is_letter('A')
    assert not is_letter('|')
    assert is_empty('.')
    assert is_empty('*')
    assert is_empty(anchor(['A']))        
    assert not is_empty('A')

    # a_row : | A * * _ _ * B E * C * _ * D |
    # The prefix starting at 9 is 'BE' and max length is 2
    assert legal_prefix(9, a_row) == ('BE', 2)
    # The prefix starting at 6 is '' but could be as long as 2
    assert legal_prefix(6, a_row) == ('', 2)    
    assert ([legal_prefix(i, a_row) for i in range(len(a_row))] == [
        ('', 0), ('', 0), ('A', 1), ('', 0), ('', 0), ('', 1), ('', 2), ('', 0),
        ('B', 1), ('BE', 2), ('', 0), ('C', 1), ('', 0), ('', 1), ('', 0),
        ('D', 1), ('', 0)])

    assert find_words('BEEN') == set(['BE', 'BEE', 'BEEN', 'BEN', 'EN', 'NE',
        'NEB', 'NEE'])
    assert find_words('EEN', pre = 'B') == set(['BE', 'BEE', 'BEEN', 'BEN'])

    # your hand is 'BEEEZUS', the board has a 'J',
    # word_plays('BEEEZUS', 'J') is the set of all possible words formed from
    # hand and board letters.
    assert word_plays('BEEEZUS', 'J') == set(['BEJEEZUS', 'JEE', 'JEEZ', 'JEU', 'JUS'])

    # find words or prefixes that start with 'Z' and use letters from hand 'JEBW'
    assert find_prefixes('JEBW', 'Z') == set(['Z', 'ZE', 'ZEB', 'ZW'])
    assert all(
        (p in WORDS or p in PREFIXES) for p in find_prefixes(a_hand, ''.join(LETTERS)))

    assert (anchor(L for L in LETTERS if '.U'.replace('.', L) in WORDS)
            == anchor(['X', 'M', 'N']))

    assert find_cross_word(a_board(), 2, 2) == (2, '.U')   
    assert find_cross_word(a_board(), 1, 2) == (1, 'JAG')
    assert find_cross_word(a_board(), 3, 2) == (2, '.Y')
    assert find_cross_word(a_board(), 5, 2) == (2, '.')
    assert find_cross_word(a_board(), 8, 1) == (1, '.EF')
    assert find_cross_word(a_board(), 8, 2) == (2, 'EF')
    assert find_cross_word(a_board(), 7, 3) == (2, 'B.')

    assert neighbors(a_board(), 2, 2) == ['.', 'U', '.', 'A']

    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose(transpose(a_board())) == a_board()

    b = a_board()
    set_anchors(b[2], 2, b)
    assert b[2] == a_row

    # regression test
    assert (sorted(horizontal_plays(a_hand, a_board()))
            == [(2, (13, 1), 'AI'),
                (2, (13, 3), 'AL'),
                (2, (13, 3), 'EL'),
                (2, (14, 1), 'IN'),
                (2, (14, 3), 'LA'),
                (3, (13, 1), 'AIN'),
                (3, (13, 3), 'ALE'),
                (3, (14, 2), 'DE'),
                (4, (1, 2), 'AN'),
                (4, (13, 1), 'BI'),
                (4, (13, 2), 'AD'),
                (4, (13, 2), 'ED'),
                (5, (10, 2), 'CAN'),
                (5, (12, 2), 'AND'),
                (5, (12, 2), 'END'),
                (5, (12, 3), 'BAL'),
                (5, (12, 3), 'BEL'),
                (5, (12, 3), 'CEL'),
                (5, (13, 1), 'BIN'),
                (5, (13, 1), 'HI'),
                (5, (13, 1), 'NIB'),
                (5, (13, 3), 'ALB'),
                (6, (10, 3), 'HA'),
                (6, (10, 3), 'HE'),
                (6, (12, 3), 'ABLE'),
                (6, (13, 1), 'HIE'),
                (6, (13, 1), 'HIN'),
                (7, (10, 2), 'CAB'),
                (7, (10, 3), 'HAE'),
                (7, (10, 3), 'HEN'),
                (7, (12, 2), 'BAD'),
                (7, (12, 2), 'BED'),
                (7, (12, 2), 'CAD'),
                (7, (13, 1), 'KIN'),
                (7, (13, 3), 'ELK'),
                (8, (12, 2), 'HAD'),
                (8, (13, 1), 'HIC'),
                (8, (13, 2), 'EDH'),
                (9, (3, 2), 'AE'),
                (9, (3, 2), 'AN'),
                (9, (7, 3), 'EF'),
                (9, (8, 3), 'FEH'),
                (9, (12, 1), 'ANI'),
                (10, (3, 2), 'ANE'),
                (10, (6, 1), 'NA'),
                (10, (10, 3), 'HAH'),
                (10, (10, 3), 'HEH'),
                (11, (3, 2), 'AB'),
                (12, (1, 1), 'JAB'),
                (12, (1, 2), 'ANA'),
                (12, (3, 2), 'ACE'),
                (12, (3, 2), 'AH'),
                (12, (6, 1), 'BA'),
                (12, (7, 2), 'BENCH'),
                (13, (6, 1), 'HA'),
                (14, (6, 1), 'KA'),
                (14, (6, 3), 'KAF'),
                (14, (6, 3), 'KEF'),
                (15, (5, 1), 'KEA'),
                (17, (3, 2), 'BA'),
                (17, (3, 2), 'BE'),
                (18, (3, 2), 'BAN'),
                (18, (3, 2), 'BEN'),
                (18, (8, 1), 'KA'),
                (21, (3, 2), 'BAH'),
                (24, (12, 1), 'CHI'),
                (30, (12, 1), 'KHI'),
                (51, (1, 1), 'JACK'),
                (64, (3, 2), 'BACKBENCH')])
    return 'tests pass'

def test_row_plays():
    # Should be ~ 0.001
    assert timedcall(row_plays, a_hand, a_row)[0] < 0.01
    return 'test_row_plays passes'

def test_words():
    assert removed('LETTERS', 'L') == 'ETTERS'
    assert removed('LETTERS', 'T') == 'LETERS'
    assert removed('LETTERS', 'SET') == 'LTER'
    assert removed('LETTERS', 'SETTER') == 'L'
    t, results = timedcall(map, find_words, hands)
    for ((hand, expected), got) in zip(hands.items(), results):
        assert got == expected, "For %r: got %s, expected %s (diff %s)" % (
            hand, got, expected, expected ^ got)
    print(t)
    return 'test_words passes'

def test_score():
    assert mirror('|.....*') == '|.....*.....|'
    assert mirror("^._") == "^._.^"
    assert bonus_template("""
        ||||
        |3.3
        |.:.
        |3.*
        """) == [
        '|||||||',
        '|3.3.3|',
        '|.:.:.|',
        '|3.*.3|',
        '|.:.:.|',
        '|3.3.3|',
        '|||||||']
    assert sorted(all_plays(a_hand, a_board()), reverse = True)
    return 'test_score passes'

def test_play():
    assert best_play(a_hand, a_board()) == (64, (3, 2), (1, 0), 'BACKBENCH')
    return 'test_play passes'

################################################################################
## Scaffolding (developmental code not used in the final product)

def find_words(letters, pre = '', results = None):
    """Find all words that can be made from the letters in hand.
    All words start with pre. results, if given, is expected to be a set.
    """
    if results is None: results = set()
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            find_words(letters.replace(L, '', 1), pre+L, results)
    return results

def add_suffixes_old(hand, pre, results):
    """Return the set of words that can be formed by extending pre with letters
    in hand."""
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in hand:
            add_suffixes_old(hand.replace(L, '', 1), pre+L, results)
    return results

def word_plays(hand, board_letters):
    "Find all word plays from hand that can be made to abut with a letter on board."
    # Find prefix + L + suffix; L from board_letters, rest from hand
    results = set()
    for pre in find_prefixes(hand):
        for L in board_letters:
            add_suffixes_old(removed(hand, pre), pre+L, results)
    return results

def longest_words(hand, board_letters):
    "Return all word plays, longest first."
    words = word_plays(hand, board_letters)
    return sorted(words, reverse = True, key = len)

def word_score(word):
    "The sum of the individual letter point scores for this word."
    return sum(POINTS[L] for L in word)

def topn(hand, board_letters, n = 10):
    "Return a list of the top n words that hand can play, sorted by word score."
    words = word_plays(hand, board_letters)    
    return sorted(words, key = word_score, reverse = True)[:n]

def test_add_suffixes_old():
    # add_suffixes_old returns words starting with the prefix 'BE', using the hand
    # to create suffixes
    assert add_suffixes_old(a_hand, 'BE', set()) == set(['BE', 'BEE', 'BEEN',
        'BEN', 'BENCH'])
    assert (add_suffixes_old(a_hand, '', set()) == set(['NAB', 'BE', 'BEN', 'BA',
        'ACE', 'NAE', 'NAH', 'NEB', 'BACK', 'BENCH', 'EN', 'CAN', 'BAN', 'CAB',
        'HA', 'BAH', 'HE', 'NA', 'NE', 'AB', 'AE', 'EH', 'KAB', 'AH', 'HAE', 'AN',
        'HEN', 'BANK', 'ANE', 'KA', 'NECK', 'KAE', 'KEA', 'EACH', 'KEN']))

    
################################################################################

if __name__ == '__main__':
    print test()
    print test_row_plays()
    print test_words()
    print test_score()
    print test_play()    
    show(a_board())
    show_best(a_hand, a_board())    
    print(doctest.testmod())
 
