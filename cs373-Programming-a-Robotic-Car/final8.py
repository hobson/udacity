from aima.games import *

class Final8(Game):
    """The game represented in the AI-Class Final Exam, Problem 8.
    
    The Exam Problem 8 is identical in structure to AIMA textbook Figure 5.2.
    >>> g = Final8()
    >>> minimax_decision('A', g)
    'a1'
    >>> alphabeta_full_search('A', g)
    'a1'
    >>> alphabeta_search('A', g)
    'a1'
    """
    
    # funny ordering to ensure that order of search is left to right as required by the exam
    succs = dict(A0=dict(a1='A1', a2='A2', a3='A3'),
                 A1=dict(b1='B1', b2='B2', b3='B3'),
                 A2=dict(c1='C1', c2='C2', c3='C3'),
                 A3=dict(d1='D1', d2='D2', d3='D3'))
    utils = dict(B1=4, B2=8, B3=7, C1=5, C2=2, C3=1, D1=1, D2=6, D3=0)
    initial = 'A0'

    def actions(self, state):
        sorted_actions = sorted(self.succs.get(state, {}).keys()) 
        print 'the available moves for state {0} are {1}'.format(str(state),str(sorted_actions))
        return sorted_actions

    def result(self, state, move):
        print 'Getting destination from {0} with action {1}'.format(str(state),str(move))
        return self.succs[state][move]

    def utility(self, state, player):
        print '{0} requesting utility at {1}'.format(str(player),str(state))
        if player == 'MAX':
            return self.utils[state]
        else:
            return -self.utils[state]

    def terminal_test(self, state):
        return state not in ('A0', 'A1', 'A2', 'A3')

    def to_move(self, state):
        return if_(state in 'BCD', 'MIN', 'MAX')
        
#g1 = Final8()
#print '--------------- minimax_decision("A", g1)'
#result_minimax = minimax_decision('A', g1)
#print result_minimax
g2 = Final8()
print '--------------- alphabeta_full_search("A0", g2)'
result_alphabeta_full = alphabeta_full_search('A0', g2)
print result_alphabeta_full
#g3 = Final8()
#print '--------------- alphabeta_search("A0", g3)'
#result_alphabeta = alphabeta_search('A0', g3)
#print result_alphabeta
#g4 = Final8()
#print '--------------- minimax_decision("B", g4)'
#result_minimax = minimax_decision('B', g4)
#print result_minimax
#g5 = Final8()
#print '--------------- alphabeta_full_search("B", g5)'
#result_alphabeta_full = alphabeta_full_search('B', g5)
#print result_alphabeta_full
#g6 = Final8()
#print '--------------- alphabeta_search("B", g6)'
#result_alphabeta = alphabeta_search('B', g6)
#print result_alphabeta

