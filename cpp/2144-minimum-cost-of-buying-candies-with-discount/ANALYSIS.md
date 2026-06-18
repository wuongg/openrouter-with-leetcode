# Greedy

## Video Solution

For more details about **Minimum Cost of Buying Candies With Discount**, watch the walkthrough at [resources](https://www.youtube.com/watch?v=0J5WA8qx3vU).

## Concept

When you can get a free candy for every two you buy, the free candy must be **no more expensive** than the cheaper of the two you paid for.  
To minimise the total amount you spend, you want the *most expensive* candies to be the ones you actually pay for, and the *cheapest* possible candies to be the free ones.  

A greedy way to achieve this is:

1. Sort the candy prices in **descending** order.  
2. Walk through the sorted list, paying for the first two candies and skipping (getting for free) the third candy.  
3. Repeat until the list is exhausted.

Because the list is sorted from high to low, the two candies you pay for in each group are the two most expensive remaining candies, and the skipped candy is the cheapest among the three—exactly what the discount rule allows.

## When to Use It

Use this greedy / sorting pattern when you see:

- A problem that gives a discount or reward based on buying a fixed number of items.  
- The goal is to **minimise cost** or **maximise benefit** by choosing which items to pay for.  
- The free/discounted item must be **no more expensive** than a certain threshold (often the minimum of the paid items).  
- Sorting the values and then processing them in groups yields an optimal solution.

## Template

```python
def greedy_group_process(arr, group_size, pay_count):
    """
    Generic template: sort descending, then for each group of size `group_size`
    pay for the first `pay_count` items and skip the rest.
    """
    arr.sort(reverse=True)
    total = 0
    for i, val in enumerate(arr):
        # i % group_size < pay_count  → we pay for this item
        if i % group_size < pay_count:
            total += val
    return total
```

For this problem `group_size = 3` and `pay_count = 2`.

## LeetCode Problem Walkthrough

### Problem: 2144. Minimum Cost of Buying Candies With Discount

https://leetcode.com/problems/minimum-cost-of-buying-candies-with-discount/

### Approach 1: Brute Force (try all purchase orders)

**Algorithm**  
The brute force way would be to consider every possible ordering in which you could buy the candies, apply the discount rule greedily for that order, and keep the minimum total cost.  
With *n* candies there are *n!* possible orderings – infeasible for n up to 100.

**Implementation**  
*(Only shown for completeness; not used in practice.)*

```python
from itertools import permutations

class SolutionBrute:
    def minimumCost(self, cost):
        n = len(cost)
        best = float('inf')
        for perm in permutations(cost):
            total = 0
            i = 0
            while i < n:
                # pay for up to two candies
                total += perm[i]          # first paid
                i += 1
                if i < n:
                    total += perm[i]      # second paid (if exists)
                    i += 1
                # skip one free candy if any remain
                if i < n:
                    i += 1                # free candy
            best = min(best, total)
        return best
```

**Complexity Analysis**

- Time complexity: O(n! × n) — we generate all permutations and scan each.
- Space complexity: O(n) — for the current permutation.

This approach is far too slow; we need a smarter method.

### Approach 2: Sorting + Greedy (optimal)

**Intuition**  
If we always pay for the two most expensive remaining candies, we can safely take the cheapest remaining candy as the free one (because it will never exceed the minimum of the two we just paid for). Sorting the prices descending lets us pick those groups in a single linear pass.

**Algorithm**  

1. Sort `cost` in descending order.  
2. Initialise `total = 0`.  
3. Iterate over the sorted list with index `i`.  
   - If `i % 3` is `0` or `1` (i.e., we are looking at the first or second element of a group of three), add `cost[i]` to `total`.  
   - If `i % 3` is `2`, skip the candy (it is free).  
4. Return `total`.

**Implementation**

```python
class Solution:
    def minimumCost(self, cost):
        """
        :type cost: List[int]
        :rtype: int
        """
        cost.sort(reverse=True)          # step 1: most expensive first
        total = 0
        for i, price in enumerate(cost):
            # pay for indices 0,1 of each block of 3; skip index 2
            if i % 3 != 2:               # 0 -> pay, 1 -> pay, 2 -> free
                total += price
        return total
```

**Complexity Analysis**

- Time complexity: O(n log n) — dominated by the sort.  
- Space complexity: O(1) — sort is in‑place, only a few extra variables.

### Approach 3: Max‑Heap (equivalent to sorting)

**Intuition**  
Instead of sorting up front, we can repeatedly extract the two most expensive candies using a max‑heap, add their prices to the answer, and discard the next most expensive candy (the free one). This yields the same result as the sorting approach but works incrementally.

**Algorithm**  

1. Push all candy prices into a max‑heap.  
2. While the heap is not empty:  
   - Pop the largest → add to total (first paid).  
   - If heap not empty, pop the next largest → add to total (second paid).  
   - If heap not empty, pop one more → discard (free candy).  
3. Return the accumulated total.

**Implementation**

```python
import heapq

class SolutionHeap:
    def minimumCost(self, cost):
        # Python's heapq is a min‑heap → store negatives to simulate max‑heap
        max_heap = [-c for c in cost]
        heapq.heapify(max_heap)

        total = 0
        while max_heap:
            # first paid candy
            total += -heapq.heappop(max_heap)
            # second paid candy (if any)
            if max_heap:
                total += -heapq.heappop(max_heap)
            # free candy (if any) – just discard
            if max_heap:
                heapq.heappop(max_heap)
        return total
```

**Complexity Analysis**

- Time complexity: O(n log n) — each heap pop/push is O(log n) and we perform O(n) of them.  
- Space complexity: O(n) — the heap stores all candy prices.

Both the sorting and heap solutions are optimal; the sorting version is slightly more concise and has lower constant factors.

---

**Key takeaway:**  
When a discount lets you get a free item whose price is bounded by the cheaper of two purchased items, **always pay for the most expensive items first** and take the cheapest possible items for free. Sorting descending (or using a max‑heap) and processing in groups of three yields the minimum total cost.