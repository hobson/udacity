# explicit
def quick_sort(arr):
    """
    Explicit version of quicksort.

    Based on rosettacode.org/wiki/Sorting_algorithms/Quicksort#Python

    >>> quick_sort([4, 10, 2, -7, 0, 12, 5, 25, -1 ,-1])
    [-7, -1, -1, 0, 2, 4, 5, 10, 12, 25]
    """
    less = []
    pivots = []
    more = []
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        for i in arr:
            if i < pivot:
                less.append(i)
            elif i > pivot:
                more.append(i)
            else:
                pivots.append(i)
        less = quick_sort(less)
        more = quick_sort(more)
        return less + pivots + more


def qs(L):
    """
    Oneliner of Haskellish python! (list comprehensions, all on one line)

    >>> qs([4, 10, 2, -7, 0, 12, 5, 25, -1 ,-1])
    [-7, -1, -1, 0, 2, 4, 5, 10, 12, 25]
    """
    return (qs([x for x in L[1:] if x < L[0]]) +
            L[:1] +
            qs([x for x in L[1:] if x >= L[0]])) if len(L) > 1 else L


def qsort(L):
    """
    Haskellish, but a bit more explicit

    >>> qsort([4, 10, 2, -7, 0, 12, 5, 25, -1 ,-1])
    [-7, -1, -1, 0, 2, 4, 5, 10, 12, 25]
    """
    if not L:
        return []
    else:
        pivot = L[0]
        less = [x for x in L[1:] if x < pivot]
        more = [x for x in L[1:] if x >= pivot]
        return qsort(less) + [pivot] + qsort(more)
