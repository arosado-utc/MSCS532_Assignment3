"""
MSCS 532 - Assignment 3
Understanding Algorithm Efficiency and Scalability

By: Alfredo Rosado
Date: 11-02-26

Two quick sort variants for Part 1:

  1. Deterministic Quick Sort - always picks the first element of the
     subarray as the pivot.
  2. Randomized Quick Sort - picks the pivot uniformly at random from
     the subarray, so performance no longer depends on input order.

Based on Chapter 8 of Cormen, Leiserson, Rivest & Stein,
"Introduction to Algorithms" (4th ed., 2022).
"""

import random


def deterministic_quick_sort(arr):
    """Sort a list of comparable elements IN PLACE in increasing order.

    Always picks the FIRST element of the current subarray as the pivot.
    Because the pivot choice depends on the input order, sorted and
    reverse-sorted inputs drive the O(n^2) worst case: every partition
    peels off exactly one element.

    Parameter: arr - list of comparable elements
    Return:    the same list object, sorted in increasing order

    Complexity:
        Time   - O(n log n) on average; O(n^2) in the worst case
                  (sorted or reverse-sorted input).
        Space  - O(log n) call stack on average, O(n) in the worst
                  case (the recursion is that deep on sorted input).
        Stable - no, because the partition swaps elements freely.
    """
    if not arr:
        return arr
    _quicksort(arr, 0, len(arr) - 1, randomized=False)
    return arr


def partition(arr, low, high, pivot_index):
    """Lomuto partition: rearrange arr[low..high] around the pivot.

    The pivot is the element at pivot_index; it is first swapped to
    position high. After the call, arr[p] holds the pivot, every
    element left of p is <= pivot, and every element right of p is >
    pivot.

    Parameter: arr         - the list
               low         - left bound of the subarray (inclusive)
               high        - right bound of the subarray (inclusive)
               pivot_index - index of the element to use as the pivot
    Return:    p, the final index of the pivot
    """
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    pivot = arr[high]
    i = low - 1  # index of the last element known to be <= pivot
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    # Put the pivot between the two regions.
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def _quicksort(arr, low, high, randomized):
    """Recursive driver for the quick sorts; bounds are inclusive.

    Parameter: arr        - the list
               low        - left bound of the subarray (inclusive)
               high       - right bound of the subarray (inclusive)
               randomized - True picks a random pivot, False picks the
                            first element
    """
    if low >= high:
        return
    if randomized:
        pivot_index = random.randint(low, high)
    else:
        pivot_index = low
    p = partition(arr, low, high, pivot_index)
    _quicksort(arr, low, p - 1, randomized)
    _quicksort(arr, p + 1, high, randomized)


def randomized_quick_sort(arr):
    """Sort a list of comparable elements IN PLACE in increasing order.

    Picks the pivot uniformly at random from the current subarray, so no
    particular input order is guaranteed to be the worst case. The
    expected number of comparisons on ANY input of n distinct keys is
    about (2 ln n) n, giving O(n log n) expected time.

    Parameter: arr - list of comparable elements
    Return:    the same list object, sorted in increasing order

    Complexity:
        Time   - O(n log n) expected on every input; O(n^2) is still
                  possible for any fixed input, but it requires n
                  unlucky pivot choices in a row (probability 1/n!).
        Space  - O(log n) call stack on average, O(n) in the worst case.
        Stable - no, because the partition swaps elements freely.
    """
    if not arr:
        return arr
    _quicksort(arr, 0, len(arr) - 1, randomized=True)
    return arr


def main():
    # A few sample lists to demonstrate the sorts
    sample_arrays = [
        [12, 11, 13, 5, 6],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [4, 4, 2, 4, 1],
        [-3, 0, -7, 4, -1],
    ]

    for sample in sample_arrays:
        original = list(sample)
        det = deterministic_quick_sort(sample[:])
        rand = randomized_quick_sort(sample[:])
        print(f"Before:        {original}")
        print(f"deterministic: {det}")
        print(f"randomized:    {rand}")
        print()


if __name__ == "__main__":
    main()
