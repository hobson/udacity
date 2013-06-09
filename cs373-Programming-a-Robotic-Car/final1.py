
# Problem #1

import hannoi
import aima.search


#sr = aima.search.breadth_first_tree_search(prob)
# can't use an InstrumentedProblem for a depth_first_graph_search because of recursive call to InstrumentedProblem.goal_tests or test_goal()
# the missing 2 states are 0001 0002, so making these a goal to get solution
initial_state = [0,0,0,0]
goal_state    = [2,2,2,2]

print 'depth first graph search without heuristic'
prob_depth = hannoi.HanoiTowerGraphProblem(initial_state,goal_state)
depth_results = aima.search.depth_first_graph_search(prob_depth)
print 'unique states: ',len(prob_depth.unique_states)
print 'solution depth: ',depth_results.depth
print 'solution path: ',str(list(depth_results.path()))

print 'best first graph search with depth heuristic (breadth search)'
prob_breadth = hannoi.HanoiTowerGraphProblem(initial_state,goal_state)
breadth_results = aima.search.best_first_graph_search(prob_breadth, hannoi.f_depth)
print 'unique states: ',len(prob_breadth.unique_states)
print 'solution depth: ',breadth_results.depth
print 'solution path: ',str(list(breadth_results.path()))

print 'best first graph search with rings on first peg heuristic (best search)'
prob_heuristic = hannoi.HanoiTowerGraphProblem(initial_state,goal_state)
heuristic_results = aima.search.best_first_graph_search(prob_heuristic, hannoi.f_heuristic)
print 'unique states: ',len(prob_heuristic.unique_states)
print 'solution depth: ',heuristic_results.depth
print 'solution path: ',str(list(heuristic_results.path()))

print 'A* graph search with admissible heuristic'
prob_astar = hannoi.HanoiTowerGraphProblem(initial_state,goal_state)
astar_results = aima.search.astar_search(prob_astar, hannoi.f_heuristic)
print 'unique states: ',len(prob_astar.unique_states)
print 'solution depth: ',astar_results.depth
print 'solution path: ',str(list(astar_results.path()))

print 'best first graph search with spanning heuristic (find all states search)'
prob_span = hannoi.HanoiTowerGraphProblem(initial_state,goal_state)
span_results = aima.search.best_first_graph_search(prob_span, hannoi.f_span)
print 'unique states: ',len(prob_span.unique_states)
print 'solution depth: ',span_results.depth
print 'solution path: ',str(list(span_results.path()))

all_states = prob_breadth.unique_states | prob_span.unique_states | prob_breadth.unique_states | prob_heuristic.unique_states

state_list = list(all_states)
state_list.sort()
print 'Do you see any missing that are reachable from the existing states to get the 81? 3x3x3x3?'
print state_list
state_nums = [int(x) for x in state_list]

## 25 states with little ring on 1st peg
# 7 states with 00, the missing 2 states are 0001 0002, so making these a goal to get solution
#    0000
#    0010
#    0011
#    0012
#    0020
#    0021
#    0022
# 9 states with 01
#    0100
#    0101
#    0102
#    0110
#    0111
#    0112
#    0120
#    0121
#    0122
# 9 states with 02
#    0200
#    0201
#    0202
#    0210
#    0211
#    0212
#    0220
#    0221
#    0222
## 27 states with little ring on 2nd peg
#    1000
#    1001
#    1002
#    1010
#    1011
#    1012
#    1020
#    1021
#    1022
#    1100
#    1101
#    1102
#    1110
#    1111
#    1112
#    1120
#    1121
#    1122
#    1200
#    1201
#    1202
#    1210
#    1211
#    1212
#    1220
#    1221
#    1222
## 27 states with little ring on 3rd peg (including goal)
#    2000
#    2001
#    2002
#    2010
#    2011
#    2012
#    2020
#    2021
#    2022
#    2100
#    2101
#    2102
#    2110
#    2111
#    2112
#    2120
#    2121
#    2122
#    2200
#    2201
#    2202
#    2210
#    2211
#    2212
#    2220
#    2221
#    2222

## 24 states with big ring on middle peg
#1000
#1002
#1010
#1011
#1012
#1020
#1021
#1022
#1100
#1101
#1102
#1110
#1112
#1120
#1121
#1200
#1201
#1202
#1210
#1211
#1212
#1220
#1221
#1222

## 25 states with big ring on last peg (didn't count goal state)
#2000
#2001
#2002
#2010
#2011
#2012
#2020
#2021
#2022
#2100
#2101
#2102
#2110
#2111
#2112
#2120
#2121
#2122
#2200
#2201
#2202
#2210
#2212
#2220
#2221

# so symmetry says we may have 3 more states or perhaps 1+2+3 states = 6 missing
# so maximum guess from this ennumeration is 72+6 = 78, 81 still seems plausible
