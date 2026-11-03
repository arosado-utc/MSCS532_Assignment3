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

TODO: implement both quick sort variants.
"""


def deterministic_quick_sort(arr):
    """Sort a list of comparable elements IN PLACE in increasing order.

    TODO: implement the deterministic quick sort (always pick the FIRST
    element of the subarray as the pivot, partition with the Lomuto
    scheme, then recursively sort the two parts).
    """
    # Placeholder - the algorithm is not implemented yet.
    return arr


def randomized_quick_sort(arr):
    """Sort a list of comparable elements IN PLACE in increasing order.

    TODO: implement the randomized quick sort (pick a pivot uniformly at
    random from the current subarray, partition with the Lomuto scheme,
    then recursively sort the two parts).
    """
    # Placeholder - the algorithm is not implemented yet.
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
