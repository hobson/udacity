

def quicksort_unlimitedram(unsorted_array):
    """Return a sorted array of the elements in `unsorted_array`, without RAM restrictions"""
    if len(unsorted_array) < 2:
        return unsorted_array
    if len(unsorted_array) == 2:
        if unsorted_array[0] <= unsorted_array[1]:
            return unsorted_array
        return [unsorted_array[1], unsorted_array[0]]
    pivot = unsorted-array[len(unsorted_array) / 2]  # floors the index
    lrm = ([], [], [])
    for i in range(len(unsorted_array))
        # are if statements any slower than arithmatic (indexing)
        # always 2 comparisons (equivalent to boolean if?) and 2 array appends and 5 array indexes and 1 subraction for ever iteration
        # if would have 1-3 comparisons, and similarly variable array appends/indexes and no arithmatic
        # this approach might help scale down the worst case performance of quicksort
        lrm[unsorted_array[i] < pivot] += [unsorted_array[i]]
        lrm[2 - unsorted_array[i] == pivot] += [lrm[1][-1]]
    return quicksort_unlimitedram(lrm[0] + lrm[2] + lrm[1])
