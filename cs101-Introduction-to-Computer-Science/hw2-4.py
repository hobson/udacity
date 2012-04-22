def countdown(N):
    """
    Examples:
    >>> countdown(3)
    3
    2
    1
    Blastoff!
    """
    for i in range(N,0,-1):
        print i
    print 'Blastoff!'

def _test():
	import doctest
	doctest.testmod(verbose=True)

if __name__ == "__main__":
	_test()
