# Union Find (Disjoint Set Union)

## Video Solution

For more details about **Process Restricted Friend Requests**, watch the walkthrough at [resources](https://www.youtube.com/watch?v=EVnIVVF-Jfs).

## Concept

Union Find (also called Disjoint Set Union, DSU) is a data structure that keeps track of a partition of a set into disjoint subsets. It supports two main operations efficiently:

* **Find(x)** – returns the representative (root) of the set containing `x`. With path compression, this runs in nearly‑constant amortized time.
* **Union(x, y)** – merges the sets containing `x` and `y`. Using union by rank/size keeps the tree shallow.

In the *Process Restricted Friend Requests* problem we need to know, for each friend request, whether merging the two people's groups would put any restricted pair into the same group. Union Find lets us maintain the current friendship groups incrementally as we process requests in order.

## When to Use It

Use Union Find when you see:

* Incremental connectivity queries (“are these two nodes connected?”) as edges are added.
* Need to merge sets and answer connectivity repeatedly.
* Problems about friend circles, social networks, number of islands, etc., where relationships are built over time.
* Constraints up to ~10⁵ elements where near‑O(1) per operation is required.

## Template

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0] * n          # or size[] for union by size

    def find(self, x):
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False                 # already in same set
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

## LeetCode Problem Walkthrough

### Problem: 2076. Process Restricted Friend Requests

https://leetcode.com/problems/process-restricted-friend-requests/

### Approach 1: Brute Force (Check connectivity after each tentative union)

**Algorithm**
1. For each request `(u, v)`:
   * Temporarily add the edge `(u, v)` to a copy of the current graph.
   * Run DFS/BFS from every node to label its component.
   * Scan all restrictions; if any restricted pair ends up in the same component, the request fails.
   * If it succeeds, permanently add the edge to the real graph.
2. Return the boolean list of results.

**Implementation**

```python
from collections import deque

class Solution:
    def friendRequests(self, n, restrictions, requests):
        adj = [[] for _ in range(n)]          # current friendship graph
        ans = []

        def bfs(start):
            """Return list of nodes in the component containing start."""
            q = deque([start])
            seen = {start}
            while q:
                cur = q.popleft()
                for nb in adj[cur]:
                    if nb not in seen:
                        seen.add(nb)
                        q.append(nb)
            return list(seen)

        for u, v in requests:
            # try adding edge
            adj[u].append(v)
            adj[v].append(u)

            # compute components
            comp_id = [-1] * n
            comp_cnt = 0
            for i in range(n):
                if comp_id[i] == -1:
                    # label this component
                    nodes = bfs(i)
                    for node in nodes:
                        comp_id[node] = comp_cnt
                    comp_cnt += 1

            # check restrictions
            ok = True
            for a, b in restrictions:
                if comp_id[a] == comp_id[b]:
                    ok = False
                    break

            if ok:
                ans.append(True)          # keep the edge
            else:
                ans.append(False)         # reject, remove the temporary edge
                adj[u].pop()
                adj[v].pop()
        return ans
```

**Complexity Analysis**
* Time: For each request we run BFS from every unvisited node → **O(n + E)** per request, where `E` ≤ requests processed so far. In the worst case `O(requests * (n + requests))`. With `n, requests ≤ 1000` this is ≤ ≈ 2 × 10⁶ operations.
* Space: **O(n + E)** for the adjacency list and auxiliary arrays.

---

### Approach 2: Union Find + Restriction Scan (the submitted solution)

**Intuition**
Instead of rebuilding components from scratch, we maintain them incrementally with a DSU. For a request `(u, v)` we only need to know whether merging the two current components would connect any restricted pair. If we look at each restriction `(x, y)` and check the current roots of `x` and `y`, the request is blocked exactly when one root equals `find(u)` and the other equals `find(v)` (in either order).

**Algorithm**
1. Initialise DSU with `n` singleton sets.
2. For each request `(u, v)`:
   * If `find(u) == find(v)`, they are already friends → request succeeds.
   * Otherwise, iterate through all restrictions:
        * Let `rx = find(x)`, `ry = find(y)`.
        * If `(rx == ru and ry == rv)` or `(rx == rv and ry == ru)`, the union would violate that restriction → block.
   * If no restriction blocks, perform `union(u, v)` and record success.
3. Return the boolean list.

**Implementation**

```python
class Solution:
    def friendRequests(self, n, restrictions, requests):
        parent = list(range(n))
        rank   = [0] * n

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            if rank[px] == rank[py]:
                rank[px] += 1

        ans = []
        for u, v in requests:
            ru, rv = find(u), find(v)
            if ru == rv:
                ans.append(True)
                continue

            blocked = False
            for x, y in restrictions:
                rx, ry = find(x), find(y)
                if (rx == ru and ry == rv) or (rx == rv and ry == ru):
                    blocked = True
                    break

            if not blocked:
                union(ru, rv)
                ans.append(True)
            else:
                ans.append(False)
        return ans
```

**Complexity Analysis**
* Time: Each request scans all restrictions → **O(requests × restrictions × α(n))**. With the given limits (≤ 1000 each) this is about 10⁶ operations.
* Space: **O(n)** for the DSU arrays.

---

### Approach 3: Union Find + Restriction Sets per Component (most optimal)

**Intuition**
Scanning every restriction for every request can be wasteful when many requests are processed but only few restrictions matter for a given component. We can store, for each component root, the set of other components it is restricted from (i.e., all nodes that appear in a restriction with any member of the component). When we consider merging two components `A` and `B`, the request is invalid iff `B` appears in `A`’s restriction set **or** `A` appears in `B`’s restriction set. After a successful union we merge the two restriction sets (using small‑to‑large to keep total work near linear).

**Algorithm**
1. DSU as before.
2. `bad[root]` = set of component roots that are forbidden to merge with `root` because of at least one restriction.
   * Initialise by iterating over all restrictions `(x, y)`:
        * `rx = find(x)`, `ry = find(y)`.
        * Add `ry` to `bad[rx]` and `rx` to `bad[ry]`.
3. For each request `(u, v)`:
   * `ru = find(u)`, `rv = find(v)`. If equal → success.
   * If `rv` in `bad[ru]` (or symmetrically `ru` in `bad[rv]`) → block.
   * Otherwise:
        * Union `ru` and `rv` → new root `r`.
        * Merge the restriction sets: attach the smaller set into the larger one (small‑to‑large).
        * For each element `x` in the moved set, also add the new root `r` to `bad[x]` (because now any component restricted to `x` is also restricted to the merged component).
        * Record success.
4. Return results.

**Implementation**

```python
class Solution:
    def friendRequests(self, n, restrictions, requests):
        parent = list(range(n))
        rank   = [0] * n

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            xr, yr = find(x), find(y)
            if xr == yr:
                return xr
            if rank[xr] < rank[yr]:
                xr, yr = yr, xr
            parent[yr] = xr
            if rank[xr] == rank[yr]:
                rank[xr] += 1
            return xr

        # restriction sets per current root
        bad = [set() for _ in range(n)]

        # initialise restrictions using initial singletons
        for a, b in restrictions:
            ra, rb = find(a), find(b)
            bad[ra].add(rb)
            bad[rb].add(ra)

        ans = []
        for u, v in requests:
            ru, rv = find(u), find(v)
            if ru == rv:
                ans.append(True)
                continue

            # check if merging would violate a restriction
            if rv in bad[ru] or ru in bad[rv]:
                ans.append(False)
                continue

            # perform union and merge restriction sets
            new_root = union(ru, rv)

            # small-to-large: ensure bad[new_root] is the larger set
            if len(bad[ru]) < len(bad[rv]):
                ru, rv = rv, ru   # now bad[ru] is larger

            # move all restrictions from rv into ru
            for forbidden in bad[rv]:
                bad[ru].add(forbidden)
                # the forbidden component now also sees the new root as restricted
                bad[forbidden].add(new_root)
            bad[rv].clear()   # optional cleanup

            ans.append(True)
        return ans
```

**Complexity Analysis**
* Time:
  * Building initial `bad` sets: O(restrictions × α(n)).
  * Each request: two `find` calls → O(α(n)).
  * Restriction‑set merge: each restriction entry moves at most O(log n) times because we always merge the smaller set into the larger one (small‑to‑large technique). Hence total work over all requests is O(restrictions × log n).
  * Overall: **O((requests + restrictions) × α(n) + restrictions × log n)**, practically near‑linear.
* Space: **O(n + restrictions)** for DSU plus the restriction sets.

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

We dry‑run the algorithm on Example 1:

* `n = 3`
* `restrictions = [[0,1]]`
* `requests = [[0,2], [2,1]]`

**Initial state**

```
parent = [0,1,2]
rank   = [0,0,0]
bad[0] = {1}
bad[1] = {0}
bad[2] = {}
```

---

#### Request 0: (0, 2)

```
find(0) = 0, find(2) = 2   -> different
Check restrictions:
   bad[0] contains 2? No.
   bad[2] contains 0? No.
=> not blocked
Union(0,2) -> new root 0 (rank[0] becomes 1)
Merge restriction sets:
   bad[2] is empty, nothing to move.
   For each moved element (none) we also add new root to its set.
Result:
parent = [0,1,0]
rank   = [1,0,0]
bad[0] = {1}
bad[1] = {0}
bad[2] = {}   # (unused)
ans = [True]
```

---

#### Request 1: (2, 1)

```
find(2) -> parent[2]=0, parent[0]=0 => 0
find(1) = 1
different roots (0 vs 1)
Check restrictions:
   bad[0] contains 1? Yes -> blocked
=> request fails
ans = [True, False]
```

Final answer `[true, false]` matches the expected output.

---

### Summary

* Start with a brute‑force BFS/DFS approach to grasp the problem.
* Move to a straightforward Union Find that scans all restrictions per request (easy to implement, sufficient for the given limits).
* For larger inputs, optimise by storing per‑component restriction sets and merging them with small‑to‑large, achieving near‑linear time.

Use Union Find whenever you need to maintain dynamic connectivity under incremental edge additions, especially when additional constraints (like forbidden connections) must be checked efficiently.