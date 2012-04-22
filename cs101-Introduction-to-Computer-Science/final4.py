# the collatz conjecture is that this always terminates?

def collatz_steps(n):
    # n = any positive integer
    n=abs(int(n))
    i=0
    while n != 1:
        i += 1
        if n % 2 == 0: # the % means remainder, so this tests if n is even
            n = n / 2
        else:
            n = 3 * n  +  1
    return i
