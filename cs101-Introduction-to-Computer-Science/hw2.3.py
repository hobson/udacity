def median(a,b,c):
    """
    Examples:
    >>> median(1,2,3)
    2
    >>> median(9,3,6)
    6
    >>> median(7,8,7)
    7
    """
    if a<=b<=c or c<=b<=a:
        return b
    elif a<=c<=b or b<=c<=a:
        return c
    else:
        return a

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()
