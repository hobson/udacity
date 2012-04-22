#!/usr/bin/python2.6

def split_string(source,splitlist):
    """
    Examples:
    >>> print split_string("This is a test-of the,string separation-code!", " ,!-")
    ['This', 'is', 'a', 'test', 'of', 'the', 'string', 'separation', 'code']
    >>> print split_string("After  the flood   ...  all the colors came out.", " .")
    ['After', 'the', 'flood', 'all', 'the', 'colors', 'came', 'out']
    """
    # like nltk.tokenize()
    result =[]
    i0=0
    nonsep=False
    for i,c in enumerate(source):
        if c in splitlist:
            if i>i0 and nonsep:
                result.append(source[i0:i])
            i0=i+1
            nonsep = False
        else:
            nonsep = True
    return result

def test():
	import doctest
	doctest.testmod(verbose=True)

if __name__ == "__main__":
	test()

