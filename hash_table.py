"""
MSCS 532 - Assignment 3
Hash table with separate chaining (Part 2).

By: Alfredo Rosado
Date: 11-02-26

A hash table that resolves collisions by chaining: each slot holds a
chain (a Python list) of (key, value) pairs. Collisions are handled
by the hash function rather than by probing, which is different from
the open-addressing table used in Project 1 (Phase 1), where a miss
walks the probe sequence.

The hash function comes from the universal hash family

    h(x) = ((a * x + b) mod p) mod m

where p is a fixed prime and the coefficients (a, b) are drawn
uniformly at random when the table is created (and again on every
resize). For distinct keys x, y with x - y not a multiple of p,
h(x) = h(y) with probability at most 1/p, which is the
"independently and uniformly distributed" behavior that simple
uniform hashing assumes.

Based on Chapter 11 of Cormen, Leiserson, Rivest & Stein,
"Introduction to Algorithms" (4th ed., 2022).
"""

import random

# A large Mersenne prime, bigger than any key we will hash. Making p
# huge means h(x) = h(y) happens with probability <= 1/p for distinct
# keys, so the family behaves essentially like simple uniform hashing.
_PRIME = 2147483647  # 2^31 - 1


class HashTable:
    """A dictionary-style table with separate chaining.

    Parameter: capacity - initial number of slots (an int >= 1)
    """

    def __init__(self, capacity=16):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._size = 0
        self._chains = [[] for _ in range(capacity)]
        # Pick the hash family once; _rehash picks a fresh one.
        self._rng = random.Random()
        self._a = self._rng.randint(1, _PRIME - 1)
        self._b = self._rng.randint(0, _PRIME - 1)

    # ------------------------------------------------------------------
    # Hash family
    # ------------------------------------------------------------------

    def _hash(self, key):
        """Map a key to a slot using the current family and table size.

        Parameter: key - an integer key
        Return:    a slot index in 0.._capacity - 1
        """
        return ((self._a * key + self._b) % _PRIME) % self._capacity

    def _rehash(self, new_capacity):
        """Rebuild every chain in new_capacity slots with a fresh family.

        The random coefficients are redrawn, so the old layout (and any
        accidental clustering in it) is thrown away.

        Parameter: new_capacity - the number of slots to rehash into
        """
        old_chains = self._chains
        self._capacity = new_capacity
        self._chains = [[] for _ in range(new_capacity)]
        self._a = self._rng.randint(1, _PRIME - 1)
        self._b = self._rng.randint(0, _PRIME - 1)
        for chain in old_chains:
            for key, value in chain:
                self._chains[self._hash(key)].append((key, value))

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def insert(self, key, value):
        """Add (key, value) to the table, or update key's value if it
        is already present.

        Parameter: key   - the key (an integer)
                   value - the value to store
        Return:    None

        Complexity:
            Time - O(1) expected for a search/insert under simple
                   uniform hashing when the load factor stays bounded.
            Space - O(n) for n stored pairs, plus O(m) for the slots.
        """
        self._insert_pair(key, value)

    def search(self, key):
        """Return the value stored under key.

        Parameter: key - the key to look up
        Return:    the value associated with key
        Raises:   KeyError if the key is not in the table

        Complexity: O(1) expected under simple uniform hashing with a
        bounded load factor; the cost is scanning one chain of expected
        length alpha = n/m.
        """
        for k, v in self._chains[self._hash(key)]:
            if k == key:
                return v
        raise KeyError(key)

    def delete(self, key):
        """Remove the pair stored under key.

        Parameter: key - the key to remove
        Return:    None
        Raises:   KeyError if the key is not in the table

        Complexity: O(1) expected, same scan-and-remove as search.
        """
        chain = self._chains[self._hash(key)]
        for i, (k, _) in enumerate(chain):
            if k == key:
                del chain[i]
                self._size -= 1
                return
        raise KeyError(key)

    def __contains__(self, key):
        try:
            self.search(key)
        except KeyError:
            return False
        return True

    # ------------------------------------------------------------------
    # Housekeeping
    # ------------------------------------------------------------------

    def _insert_pair(self, key, value):
        """Insert (key, value), updating an existing key in place.

        Parameter: key   - the key
                   value - the value to store
        """
        chain = self._chains[self._hash(key)]
        for i, (k, _) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)  # update, do not grow the table
                return
        chain.append((key, value))
        self._size += 1
        # Keep the load factor at or below 1: double the table once the
        # chains get long, which halves the expected chain length.
        if self._size >= self._capacity:
            self._rehash(2 * self._capacity)

    def size(self):
        """Number of key-value pairs currently stored."""
        return self._size

    def capacity(self):
        """Number of slots in the table."""
        return self._capacity

    def load_factor(self):
        """alpha = size / capacity; expected chain length is alpha."""
        return self._size / self._capacity
