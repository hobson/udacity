def find_last(t,s):
    """
    Example:
    >>> find_last('aaaa','a')
    3
    >>> find_last('hello world','war')
    -1
    """
    return t.rfind(s)

def _test():
	import doctest
	doctest.testmod(verbose=True)

if __name__ == "__main__":
	_test()
