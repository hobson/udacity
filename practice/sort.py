
from decorators import debug_report


def qs(unsorted_array):
    """Return a sorted array of the elements in `unsorted_array`, without RAM restrictions"""
    if len(unsorted_array) < 2:
        return unsorted_array
    if len(unsorted_array) == 2:
        if unsorted_array[0] <= unsorted_array[1]:
            return unsorted_array
        return [unsorted_array[1], unsorted_array[0]]
    pivot = unsorted_array[len(unsorted_array) / 2]  # floors the index
    left, middle, right
    lmr = ([], [], [])
    for i, val in enumerate(unsorted_array):
        # are if statements any slower than arithmatic (indexing)?
        # always 2 comparisons (equivalent to boolean if?) and 2 array appends and 5 array indexes and 1 subraction for ever iteration
        # if would have 1-3 comparisons, and similarly variable array appends/indexes and no arithmatic
        # this approach might help scale down the worst case performance of quicksort
        lmr[0] += [val]
        lmr[2 * (val >= pivot)] += [lmr[0].pop()]
        lmr[2 - int(val == pivot)] += [lmr[2][-1]]
    return qs(lmr[0]) + lmr[1] + qs(lmr[2])


def quicksort(x):
    N = len(x)
    if len(x) <= 1:
        return x
    pivot = x[len(x)/2]
    first = 0
    last = N - 1
    while first < last:
        while x[first] < pivot:
            first += 1
        while x[last] > pivot:
            last -= 1
        if x[first] <= x[last]:
            x[first], x[last] = x[last], x[first]
            first += 1
            last -= 1
    return quicksort(x[first:]) + quicksort(x[:last+1])


@debug_report
def ms(x):
    x = list(x)
    print 'ms ' + repr(x)
    if len(x) <= 1:
        return list(x)
    return merge(ms(x[:len(x)/2]), ms(x[len(x)/2:]))


@debug_report
def merge(l, r):
    print 'merge ' + repr(l) + ',' + repr(r)
    ret = []
    j0 = 0
    for i, lval in enumerate(l):
        for j, rval in enumerate(r[j0:]):
            if lval <= rval:
                ret += [lval]
                break
            ret += [rval]
            # could delete the record in r, but that would require a lot of memeory shifting
            j0 += 1
    if l:
        ret += l[i:]
    if r:
        ret += r[j0:]
    return ret
