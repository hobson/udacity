def print_multiplication_table(N):
    """
    Example:
    >>> print_multiplication_table(2)
    1*1=1
    1*2=2
    2*1=2
    2*2=4
    >>> print_multiplication_table(3)
    1*1=1
    1*2=2
    1*3=3
    2*1=2
    2*2=4
    2*3=6
    3*1=3
    3*2=6
    3*3=9
    """
    for i in range(1,N+1):
        for j in range(1,N+1):
            print '{0}*{1}={2}'.format(i,j,i*j)

def _test():
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    _test()
