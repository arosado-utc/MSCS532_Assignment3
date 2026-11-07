# Assignment 3: Understanding Algorithm Efficiency and Scalability

For this assignment I implemented two quick sort variants — a
deterministic one that always takes the first element as the pivot, and
a randomized one that picks the pivot uniformly at random — and
benchmarked them against each other on random, sorted, reverse-sorted,
and repeated inputs. For Part 2 I implemented a hash table with
separate chaining on top of a universal hash family and analyzed the
expected cost of search, insert, and delete under simple uniform
hashing.

Reference: Cormen, Leiserson, Rivest & Stein, *Introduction to
Algorithms* (4th ed., 2022), Chapters 8 and 11.

## How to run

Python 3.8 or higher. matplotlib is only needed to regenerate the
plots.

```bash
python3 main.py        # demo of both sorts
python3 tests.py       # test suite (15 tests)
python3 benchmark.py   # reruns the benchmark, rewrites results/ and plots/
```

## Files

| File           | Description                                                    |
| -------------- | -------------------------------------------------------------- |
| `main.py`      | The two quick sort variants + a small demo                     |
| `hash_table.py`| Hash table with chaining and a universal hash family           |
| `benchmark.py` | Benchmark harness (wall time + peak memory, CSV + log-log plots) |
| `tests.py`     | Test suite covering both parts                                 |
| `results/`     | `benchmark_results.csv` — the measured data                    |
| `plots/`       | Log-log comparison plots generated from the CSV                |

## Part 1: Randomized Quicksort

### Implementation

Both variants sort in place with the Lomuto partition scheme (the same
scheme I used in Assignment 2). The only difference between them is
the pivot choice: `deterministic_quick_sort` always takes the first
element of the current subarray, while `randomized_quick_sort` picks a
pivot uniformly at random from the subarray.

```python
def partition(arr, low, high, pivot_index):
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

After `partition`, `arr[p]` holds the pivot, everything left of `p` is
`<= pivot`, and everything right of `p` is `> pivot`; the two sides
are then sorted recursively. I tested both on empty and single-element
lists, duplicates, and already-sorted input (see `tests.py`) — none of
these need special cases, because a partition that produces an empty
side simply stops the recursion there.

### Why the average case is O(n log n)

The standard indicator-variable argument is the cleanest way to see
why the average case does not depend on the input order. Let `X_ij` be
the indicator that keys `a_i` and `a_j` are compared directly during
the run. Two keys are compared if and only if one of them is chosen as
the pivot before any key between them is; the first pivot chosen from
the range `a_i..a_j` is equally likely to be any of its `j - i + 1`
elements, so

    E[X_ij] = Pr[a_i or a_j is compared] = 2 / (j - i + 1).

The total number of comparisons is `X = sum_ij X_ij`, so by linearity
of expectation

    E[X] = sum_{i<j} 2/(j-i+1)
         = sum_{d=1}^{n-1} 2(n-d)/(d+1)
         <= 2n * sum_{d=1}^{n-1} 1/d
         = 2n * H_{n-1}  ~  2n ln n.

That gives O(n log n) expected comparisons on **every** input of n
distinct keys — it is the pivot choices, not the input order, that make
the argument work.

The same result follows from the recurrence side: the pivot position
is uniform, so with `T(n)` the expected running time,

    E[T(n)] = n - 1 + (1/n) * sum_{j=1}^{n} (T(j-1) + T(n-j)),

and substituting the guess `T(n) <= c n log n` satisfies it (the summed
term averages to about n log n, leaving the n - 1 partition cost). I
included both views because the indicator version makes the
input-order independence explicit, while the recurrence is the one
you would actually use to bound running time.

For the deterministic variant, averaged over uniformly random input
orders the first element is just as good a pivot as a random pick (the
first value of a random permutation is a random key), so its average
case is the same O(n log n). The difference is the worst case: on
sorted or reverse-sorted input the first element is always the minimum
or maximum, every partition peels off exactly one element, and
`T(n) = T(n-1) + Theta(n)` gives Theta(n^2). Randomization removes the
dependence on input order entirely.

### What the benchmark shows

I ran both sorts on four input types — random, sorted, reverse-sorted,
and repeated (values drawn from the range 0–100 so most elements
collide) — across several sizes. Measured wall times (ms), averaged
over 3 runs (1 run at the largest sizes); the full data is in
`results/benchmark_results.csv`:

| Dataset        | n     | deterministic | randomized |
| -------------- | ----- | ------------: | ---------: |
| random         | 1,024 |           0.40 |       0.49 |
| random         | 2,048 |           1.05 |       1.24 |
| random         | 4,096 |           2.49 |       2.99 |
| random         | 8,192 |           5.79 |       6.32 |
| random         | 16,384|          12.12 |      13.26 |
| random         | 32,768|          26.25 |      28.73 |
| sorted         | 1,024 |           4.25 |       0.44 |
| sorted         | 2,048 |        1,465.02 |       1.09 |
| sorted         | 4,096 |      20,258.57 |       2.71 |
| reverse_sorted | 1,024 |           8.40 |       0.43 |
| reverse_sorted | 2,048 |        2,276.71 |       1.16 |
| reverse_sorted | 4,096 |      34,934.67 |       2.60 |
| repeated       | 1,024 |           0.45 |       0.60 |
| repeated       | 2,048 |           1.48 |       2.06 |
| repeated       | 4,096 |          13.72 |      31.88 |

**Random data.** Both variants grow roughly 2.1–2.6x per doubling —
the n log n signature (the theoretical doubling ratio is
2(1 + 1/log2 n), about 2.1–2.2) — and randomized stays within 10–20%
of deterministic. That matches the analysis: on a random input the
first element is already a random key, so the two pivot rules are
statistically the same.

**Sorted and reverse-sorted data.** Deterministic quick sort blows up:
1,465 ms at n = 2,048 and 20.3 s at n = 4,096, while randomized stays
on the n log n curve (2.7 ms at 4,096 — about 1/7,500th of the
deterministic time). That is exactly the worst case the analysis
predicts: one element peeled off per partition.

One discrepancy worth flagging: the deterministic growth ratio between
n = 1,024 and n = 2,048 (about 345x) is steeper than the 4x per
doubling that Theta(n^2) implies. The cause is measurement overhead,
not the algorithm: the quadratic runs recurse n levels deep, so the
live object graph (the whole call stack) is large, and the
instrumentation (`tracemalloc`) plus garbage collection cost grows
with it. A clean run without any measurement code gives 4.3 / 22.7 /
95.3 ms for n = 1,024 / 2,048 / 4,096 — a clean ~4x per doubling, the
Theta(n^2) signature.

**Repeated elements.** Both variants are slower than on random data
(clean runs: ~2.9x per doubling instead of ~2.2–2.3x), and at
n = 4,096 randomized was actually the slower of the two (31.9 vs
13.7 ms). The two-way Lomuto partition is the culprit: inside a run of
equal values every partition peels off a single element, adding extra
quadratic work that the average-case analysis does not count, because
the indicator argument above assumes distinct keys. This is the
discrepancy between theory and practice that the assignment asks
about: the theory's assumptions matter, and the standard fix is a
three-way (Dijkstra) partition that groups equal values together.

### Complexity summary

- **Deterministic:** O(n log n) average, Theta(n^2) worst case
  (ordered input with the first-element pivot), O(log n) stack space
  on average and O(n) in the worst case, not stable.
- **Randomized:** O(n log n) expected time on every input (a quadratic
  run still exists but needs n unlucky pivots in a row), O(log n)
  expected stack space, not stable.

## Part 2: Hashing with Chaining

### What I implemented

The table uses separate chaining: each slot holds a chain of
`(key, value)` pairs in a Python list. Chaining was a natural contrast
to the open-addressing table from Project 1 (Phase 1): with chaining,
insert and delete do not depend on where existing entries cluster, and
deletion needs no tombstones because removing a pair from its chain is
all that is required.

For the hash function I used the universal family
`h(x) = ((a*x + b) mod p) mod m` with `p = 2^31 - 1`, drawing the
coefficients `(a, b)` uniformly at random when the table is created.
For distinct keys whose difference is not a multiple of p,
`Pr[h(x) = h(y)] <= 1/p`, so for the key sizes here the family
behaves like simple uniform hashing. A fresh `(a, b)` is drawn on
every resize, which discards any accidental bad layout.

The operations:

- `insert(key, value)` — scans the chain and, if the key is already
  present, replaces the value in place, so updating does not grow the
  table
- `search(key)` — walks the chain for the key (raises `KeyError` if
  missing)
- `delete(key)` — removes the pair from its chain

When the load factor reaches 1 the table doubles and every pair is
rehashed into the new slots. `tests.py` checks all of this, including
a random mix of 20,000 insert/search/delete operations verified
against a plain dict as a reference.

### Expected cost under simple uniform hashing

Let `n` be the number of stored pairs, `m` the number of slots, and
`alpha = n/m` the load factor. Under simple uniform hashing each pair
lands in each slot with probability 1/m, so a chain has expected
length `alpha`:

- **Unsuccessful search:** 1 + alpha — one step to reach the bucket,
  then a full scan of the expected chain length
- **Successful search:** 1 + (1/2)(1 + alpha) — the wanted key sits,
  on average, halfway down its chain
- **Insert:** 1 + alpha — scan the chain (to detect an existing key),
  then append
- **Delete:** 1 + alpha — scan the chain, then remove the pair

Every operation is O(1) in expectation as long as `alpha` stays
bounded.

### Keeping the load factor down

The expected chain length is exactly `alpha`, so every operation runs
in Theta(1 + alpha): keep `alpha` bounded and the table is constant
time; let `alpha` grow and every operation degrades linearly in
`alpha`. My strategy is to double the table the moment `alpha = 1`. A
resize costs Theta(n), but it happens infrequently enough that the
amortized cost of an insert is still O(1), and doubling guarantees the
load factor never exceeds 1, i.e. the expected chain length stays at
most 1. There are two complementary ways to keep collisions low: the
universal hash family (random coefficients per table, redrawn on
resize) prevents inputs from forcing a bad distribution, and resizing
keeps the expected chain length bounded. (Shrinking the table again
when `alpha` falls below about 1/4 is another common trick to save
memory; I did not implement it because the payoff is small for this
use case.)

## Benchmark notes

- Random data runs from 1,024 to 32,768 elements. The sorted,
  reverse-sorted, and repeated datasets stop at 4,096: the quadratic
  worst case makes each doubling cost 4x more, and in pure Python
  4,096 is already a long run, so three doublings are enough to show
  the trend.
- Time is wall time around the sort call, averaged over the runs;
  memory is the peak of Python allocations tracked by `tracemalloc`.
  Both sorts are in place, so peak memory is near zero on random
  data; the small growth on ordered data (0.17 MB at 4,096) is the
  deep recursion stack.
- The recursion limit is raised to 100,000 because deterministic quick
  sort on ordered input recurses n levels deep.

## References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022).
  *Introduction to Algorithms* (4th ed.). MIT Press.
