
# number of unique baseball cards you want to collect
N_unique = 3
target = set(range(N_unique))
# number of attempts each trial took to get a collection
results = []
# you don't currently have any cards in your collection
state = set()

# number of times you want to run the "monte carlo" experiment
N_trials = 3

import random

#for N_unique in range(2, 5):
for i_trial in range(N_trials):
    state = set()
    attempts = 0
    while state != target:
        print state, target
        state = state.union(set([random.randint(0,N_unique-1)]))
        attempts += 1
    results += [attempts]

import plotutil
