# Union Find (Disjoint Set Union)

## Video Solution

For more details about **Largest Component Size by Common Factor**, watch the walkthrough at [https://www.youtube.com/watch?v=DNfNZwilaC4](https://www.youtube.com/watch?v=DNfNZwilaC4).

## Concept

Union Find (also called Disjoint Set Union, DSU) is a data structure that keeps track of a partition of a set into disjoint subsets. It supports two near‑constant‑time operations:

* **find(x)** – returns the representative (root) of the set containing `x`, with path compression.
* **union(x, y)** – merges the sets containing `x` and `y`, using union by rank/size to keep the tree shallow.

The classic use case is to dynamically maintain connectivity information as edges are added to an undirected graph. When two vertices share an edge we `union` them; later we can query whether two vertices are in the same connected component by checking if `find(u) == find(v)`.

In the “Largest Component Size by Common Factor” problem we cannot afford to check every pair of numbers (O(n²)). Instead we notice that an edge exists iff the two numbers share a prime factor > 1. By union‑ing each number with **all of its prime factors**, numbers that share a factor end up in the same set implicitly. After processing all numbers, the size of the largest set equals the answer.

## When to Use It

Use Union Find when you see:

* A problem that asks for the size/number of connected components in an implicit graph.
* Edges are defined by a property that can be decomposed into per‑node attributes (e.g., sharing a prime factor, having the same remainder modulo k, belonging to the same interval).
* You need to incrementally add edges and query component sizes.
* Constraints are large enough that O(n²) pairwise checks are infeasible, but each node can be processed via a small set of “keys” (factors, bits, etc.).

Typical clues: “common factor”, “gcd > 1”, “same remainder”, “overlapping intervals”, “friends of friends”.

## Template

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0] * n          # or size = [1] * n for union by size

    def find(self, x):
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return
        # Union by rank (attach shallower tree under deeper one)
        if self.rank[xr] < self.rank[yr]:
            xr, yr = yr, xr
        self.parent[yr] = xr
        if self.rank[xr] == self.rank[yr]:
            self.rank[xr] += 1
```

## LeetCode Problem Walkthrough

### Problem: 952. Largest Component Size by Common Factor

https://leetcode.com/problems/largest-component-size-by-common-factor/

---

### Approach 1: Brute Force – Pairwise GCD

**Algorithm**
1. Initialise a DSU for `n = len(nums)`.
2. For every pair `(i, j)` with `i < j`:
   * Compute `g = gcd(nums[i], nums[j])`.
   * If `g > 1`, union the indices `i` and `j`.
3. After all unions, count how many indices belong to each root.
4. Return the maximum count.

**Intuition**  
The definition of an edge is exactly “share a common factor > 1”. The most direct way is to test every pair.

**Implementation**

```python
from math import gcd
from collections import defaultdict

class Solution:
    def largestComponentSize(self, nums):
        n = len(nums)
        dsu = DSU(n)

        for i in range(n):
            for j in range(i + 1, n):
                if gcd(nums[i], nums[j]) > 1:
                    dsu.union(i, j)

        comp_size = defaultdict(int)
        for i in range(n):
            root = dsu.find(i)
            comp_size[root] += 1

        return max(comp_size.values())
```

**Complexity Analysis**
- Time complexity: O(n² · log M) – `gcd` is O(log M) where M = max(nums). The double loop dominates.
- Space complexity: O(n) – DSU arrays + hashmap for component sizes.

---

### Approach 2: Union Each Number with Its Prime Factors

**Algorithm**
1. Let `max_val = max(nums)`. Initialise a DSU that can hold elements `0 … max_val`.  
   We'll treat each integer itself and each possible prime factor as a node.
2. For each number `x` in `nums`:
   * Factorise `x` into its distinct prime factors `p₁, p₂, …`.
   * For each prime factor `p`, union the node representing `x` with the node representing `p`.
3. After processing all numbers, count how many original numbers map to each root (ignore pure factor nodes).
4. Return the largest count.

**Intuition**  
If two numbers share a prime factor `p`, they will both be unioned with the node `p`. Transitivity of union‑find then puts them in the same set. Thus we avoid checking every pair; we only need to union each number with its (few) prime factors.

**Implementation**

```python
class Solution:
    def largestComponentSize(self, nums):
        max_val = max(nums)
        dsu = DSU(max_val + 1)          # extra slot for 0‑based indexing

        def prime_factors(x):
            factors = set()
            d = 2
            while d * d <= x:
                if x % d == 0:
                    factors.add(d)
                    while x % d == 0:
                        x //= d
                d += 1 if d == 2 else 2   # after 2, test only odd numbers
            if x > 1:
                factors.add(x)
            return factors

        for num in nums:
            for p in prime_factors(num):
                dsu.union(num, p)

        # count how many input numbers belong to each component
        from collections import Counter
        root_count = Counter()
        for num in nums:
            root_count[dsu.find(num)] += 1

        return max(root_count.values())
```

**Complexity Analysis**
- Time complexity: O(N · √M log M) in the worst case (factorising each number by trial division).  
  Each `union`/`find` is practically O(α(N+M)) ≈ O(1).  
  With `M ≤ 10⁵`, √M ≈ 316, easily fast enough for N = 2·10⁴.
- Space complexity: O(M) for the DSU arrays (≈ 10⁵) + O(N) for the counter.

---

### Approach 3: Pre‑compute Smallest Prime Factor (SPF) Sieve – Fastest Factorisation

**Algorithm**
1. Build an array `spf[i]` = smallest prime factor of `i` for every `i ≤ max_val` using a linear sieve (O(max_val)).
2. Initialise DSU for `0 … max_val`.
3. For each number `x` in `nums`:
   * Repeatedly extract its prime factors using `spf`: while `x > 1`:  
        `p = spf[x]`; union the original number with `p`; divide `x` by `p` until not divisible.
   * This yields distinct prime factors without duplicate work.
4. Count component sizes as before and return the maximum.

**Intuition**  
Factoring each number by trial division can be slow if many numbers are large. Pre‑computing the smallest prime factor for every integer up to `max_val` lets us factor any number in O(number of prime factors) time, which is optimal.

**Implementation**

```python
class Solution:
    def largestComponentSize(self, nums):
        max_val = max(nums)
        # ---------- SPF sieve ----------
        spf = list(range(max_val + 1))
        for i in range(2, int(max_val**0.5) + 1):
            if spf[i] == i:                     # i is prime
                for j in range(i * i, max_val + 1, i):
                    if spf[j] == j:
                        spf[j] = i
        # --------------------------------

        dsu = DSU(max_val + 1)

        def union_with_factors(x):
            original = x
            while x > 1:
                p = spf[x]
                dsu.union(original, p)
                while x % p == 0:
                    x //= p

        for num in nums:
            union_with_factors(num)

        from collections import Counter
        cnt = Counter()
        for num in nums:
            cnt[dsu.find(num)] += 1
        return max(cnt.values())
```

**Complexity Analysis**
- Time complexity: O(max_val log log max_val + N · log max_val)  
  * Sieve: O(max_val log log max_val) (practically linear).  
  * Factoring each number: O(number of prime factors) ≤ O(log max_val).  
  With `max_val = 10⁵` this is well under a millisecond.
- Space complexity: O(max_val) for `spf` + DSU arrays ≈ 2·10⁵ integers.

---

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

We trace **Approach 2** on the sample `nums = [4, 6, 15, 35]`.

`max_val = 35`, DSU holds nodes `0…35`.

| Step | num | prime factors | Union operations performed | DSU parent snapshot (representative) |
|------|-----|---------------|----------------------------|--------------------------------------|
| 1    | 4   | {2}           | union(4,2)                 | 4‑2 share root 2                     |
| 2    | 6   | {2,3}         | union(6,2) → 6 joins {4,2}<br>union(6,3) → 3 joins same set | {2,4,6,3} all connected |
| 3    | 15  | {3,5}         | union(15,3) → 15 joins big set<br>union(15,5) → 5 joins big set | {2,4,6,3,15,5} |
| 4    | 35  | {5,7}         | union(35,5) → 35 joins big set<br>union(35,7) → 7 joins big set | All numbers {2,3,4,5,6,7,15,35,4,6,15,35} in one set |

After processing, each original number's root is the same, so component size = 4.

```
Input: nums = [4,6,15,35]

Number → factors → unions
4  → {2}          → 4‑2
6  → {2,3}        → 6‑2 (now 4‑2‑6), 6‑3 (adds 3)
15 → {3,5}        → 15‑3 (connects to big set), 15‑5 (adds 5)
35 → {5,7}        → 35‑5 (connects), 35‑7 (adds 7)

All four input nodes share the same root → answer = 4.
```

This dry‑run shows how union‑ing via prime factors merges everything into a single component, giving the correct output.

--- 

**End of lecture**. Save this as `lectures/2025-09-26-union-find.md` (or the appropriate date if today differs). Ensure no other files are modified.