"""
MSCS 532 - Assignment 3
Test suite for the quick sort and hash table implementations.

Run with:  python3 tests.py

Covers correctness against Python's built-in sorted(), the in-place
contract of both quick sorts, the quadratic worst case on ordered
input, and the hash table's insert/search/delete behavior including
key updates, resizes, and missing-key errors.
"""

import random
import sys

from main import deterministic_quick_sort, randomized_quick_sort
from hash_table import HashTable


def test_deterministic_quick_sort_matches_builtin():
    """Deterministic quick sort must agree with sorted() on random data."""
    rng = random.Random(7)
    for n in (0, 1, 2, 5, 50, 500):
        data = [rng.randint(-1000, 1000) for _ in range(n)]
        deterministic_quick_sort(data)
        assert data == sorted(data), f"n={n}"


def test_deterministic_quick_sort_is_in_place():
    """deterministic_quick_sort must sort the SAME list and return it."""
    data = [5, 3, 8, 1]
    result = deterministic_quick_sort(data)
    assert result is data, "must sort in place"
    assert data == [1, 3, 5, 8]


def test_deterministic_quick_sort_worst_case_sorted():
    """Already-sorted input hits the O(n^2) worst case with the
    first-element pivot; it must still produce the right answer."""
    sys.setrecursionlimit(100_000)
    data = list(range(4096))
    deterministic_quick_sort(data)
    assert data == list(range(4096))


def test_deterministic_quick_sort_worst_case_reverse_sorted():
    """Reverse-sorted input is the other degenerate case."""
    sys.setrecursionlimit(100_000)
    data = list(range(4096, 0, -1))
    deterministic_quick_sort(data)
    assert data == list(range(1, 4097))


def test_randomized_quick_sort_matches_builtin():
    """Randomized quick sort must agree with sorted() on random data.
    Several trials, since the pivot choices differ from run to run."""
    rng = random.Random(99)
    for trial in range(20):
        n = rng.choice((0, 1, 2, 5, 50, 500, 5000))
        data = [rng.randint(-1000, 1000) for _ in range(n)]
        randomized_quick_sort(data)
        assert data == sorted(data), f"trial={trial} n={n}"


def test_randomized_quick_sort_on_sorted_input():
    """Sorted input used to be the killer case for a fixed pivot;
    randomization must still sort it correctly."""
    sys.setrecursionlimit(100_000)
    data = list(range(4096))
    randomized_quick_sort(data)
    assert data == list(range(4096))


def test_quick_sorts_duplicates():
    """Many equal elements must not break the partition."""
    data = [3, 3, 3, 1, 3, 2, 3, 3]
    deterministic_quick_sort(data[:])
    randomized_quick_sort(data)
    assert data == [1, 2, 3, 3, 3, 3, 3, 3]


def test_both_sorts_agree():
    """On the same random data the two algorithms must produce the
    same sorted result."""
    rng = random.Random(1234)
    data = [rng.randint(-500, 500) for _ in range(300)]
    a = data[:]
    b = data[:]
    deterministic_quick_sort(a)
    randomized_quick_sort(b)
    assert a == b


def test_hash_table_insert_search():
    """Inserted pairs must be found, with their values intact."""
    table = HashTable()
    for k in range(50):
        table.insert(k, k * 3)
    for k in range(50):
        assert table.search(k) == k * 3
        assert k in table


def test_hash_table_update_existing_key():
    """Inserting a key that is already present must update the value
    without growing the table."""
    table = HashTable()
    table.insert(7, "old")
    size = table.size()
    table.insert(7, "new")
    assert table.search(7) == "new"
    assert table.size() == size


def test_hash_table_delete():
    """Deleted keys must be gone, and the rest untouched."""
    table = HashTable()
    for k in range(40):
        table.insert(k, k)
    table.delete(13)
    assert 13 not in table
    assert table.size() == 39
    for k in range(40):
        if k == 13:
            continue
        assert table.search(k) == k


def test_hash_table_missing_key_errors():
    """search and delete must raise KeyError for absent keys."""
    table = HashTable()
    table.insert(1, "one")
    for absent in (0, 2, -5):
        try:
            table.search(absent)
            raise AssertionError(f"search({absent}) should have raised")
        except KeyError:
            pass
        try:
            table.delete(absent)
            raise AssertionError(f"delete({absent}) should have raised")
        except KeyError:
            pass


def test_hash_table_resize_keeps_everything():
    """Inserting far more keys than the initial capacity forces
    several doublings; nothing may be lost along the way."""
    table = HashTable(capacity=8)
    for k in range(1000):
        table.insert(k, k * 10)
    assert table.size() == 1000
    assert table.load_factor() <= 1.0
    for k in range(1000):
        assert table.search(k) == k * 10


def test_hash_table_random_mix_against_dict():
    """A random mix of insert/search/delete must track a dict exactly."""
    rng = random.Random(2026)
    table = HashTable()
    reference = {}
    for step in range(20000):
        key = rng.randint(-5000, 5000)
        value = rng.randint(0, 10 ** 6)
        op = rng.random()
        if op < 0.5:
            table.insert(key, value)
            reference[key] = value
        elif op < 0.8:
            try:
                got = table.search(key)
            except KeyError:
                assert key not in reference, f"step {step}: spurious miss"
            else:
                assert got == reference[key], f"step {step}: wrong value"
        else:
            try:
                table.delete(key)
            except KeyError:
                assert key not in reference, f"step {step}: delete of missing"
            else:
                assert key in reference, f"step {step}: deleted but reference has it"
                del reference[key]
    assert table.size() == len(reference)


def test_hash_table_negative_and_large_keys():
    """The universal family must handle negative and huge keys."""
    table = HashTable()
    table.insert(-123456, "neg")
    table.insert(2 ** 60, "big")
    assert table.search(-123456) == "neg"
    assert table.search(2 ** 60) == "big"


def main():
    tests = [
        test_deterministic_quick_sort_matches_builtin,
        test_deterministic_quick_sort_is_in_place,
        test_deterministic_quick_sort_worst_case_sorted,
        test_deterministic_quick_sort_worst_case_reverse_sorted,
        test_randomized_quick_sort_matches_builtin,
        test_randomized_quick_sort_on_sorted_input,
        test_quick_sorts_duplicates,
        test_both_sorts_agree,
        test_hash_table_insert_search,
        test_hash_table_update_existing_key,
        test_hash_table_delete,
        test_hash_table_missing_key_errors,
        test_hash_table_resize_keeps_everything,
        test_hash_table_random_mix_against_dict,
        test_hash_table_negative_and_large_keys,
    ]

    failed = 0
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL: {test.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"ERROR: {test.__name__}: {type(e).__name__}: {e}")

    print()
    if failed:
        print(f"{failed} of {len(tests)} test(s) FAILED.")
        raise SystemExit(1)
    print(f"All {len(tests)} tests passed.")


if __name__ == "__main__":
    main()
