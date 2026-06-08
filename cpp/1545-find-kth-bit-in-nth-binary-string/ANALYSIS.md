# Divide and Conquer

## Video Solution

For more details about **Find Kth Bit in Nth Binary String**, watch the walkthrough at [resources](https://www.youtube.com/watch?v=h9DOEqeb_ZA).

## Concept

The string `Sₙ` is defined recursively:

- `S₁ = "0"`
- For `i > 1`: `Sᵢ = Sᵢ₋₁ + "1" + reverse(invert(Sᵢ₋₁))`

The length of `Sₙ` is `2ⁿ − 1`. The middle character (position `2ⁿ⁻¹`) is always `'1'`.  
The left half is exactly `Sₙ₋₁`. The right half is the mirror of the left half with every bit flipped.

Because of this symmetry we can locate the `k`‑th bit without constructing the whole string:

1. If `k` is the middle → answer is `'1'`.
2. If `k` lies in the left half → recurse on `Sₙ₋₁` with the same `k`.
3. If `k` lies in the right half → map it to the corresponding position in the left half, recurse, then flip the result.

This is a classic divide‑and‑conquer on a recursively defined sequence.

## When to Use It

Use this pattern when you see:

- A string (or sequence) built recursively with a clear middle/pivot.
- Length grows exponentially (e.g., `2ⁿ − 1`) making explicit construction infeasible.
- The problem asks for a single character/value at position `k` rather than the whole structure.
- The definition involves `reverse` and `invert` (or similar mirror‑and‑flip) operations.

## Template

```python
def kth_bit_recursive(n: int, k: int) -> str:
    """
    Return the k-th bit (1-indexed) in S_n.
    """
    if n == 1:                     # base case
        return '0'
    mid = 1 << (n - 1)             # 2^(n-1)
    if k == mid:                   # middle character is always '1'
        return '1'
    if k < mid:                    # left half -> same as S_{n-1}
        return kth_bit_recursive(n - 1, k)
    # right half -> map to left half and flip
    mirror = mid - (k - mid)       # position in S_{n-1}
    bit = kth_bit_recursive(n - 1, mirror)
    return '1' if bit == '0' else '0'
```

## LeetCode Problem Walkthrough

### Problem: 1545. Find Kth Bit in Nth Binary String

https://leetcode.com/problems/find-kth-bit-in-nth-binary-string/

### Approach 1: Brute Force (Construct the String)

**Algorithm**
- Build `Sᵢ` iteratively from `i = 1` up to `n` using the definition.
- After building `Sₙ`, return the character at index `k‑1`.

**Implementation**

```python
def findKthBit_brute(n: int, k: int) -> str:
    s = "0"
    for _ in range(2, n + 1):
        inverted = ''.join('1' if ch == '0' else '0' for ch in s)
        s = s + "1" + inverted[::-1]
    return s[k - 1]
```

**Complexity Analysis**
- Time complexity: O(2ⁿ) — each step doubles the length of the string.
- Space complexity: O(2ⁿ) — we store the full string `Sₙ`.

---

### Approach 2: Recursive Divide & Conquer (Optimal)

**Intuition**
The middle character is always `'1'` and the two halves are mirror images with a bit‑flip. By checking whether `k` falls in the left half, middle, or right half we can reduce the problem size by one level without ever building the string.

**Algorithm**
- Base case: `n == 1 → return '0'`.
- Compute `mid = 2ⁿ⁻¹`.
- If `k == mid` → return `'1'`.
- If `k < mid` → recurse on `(n‑1, k)`.
- If `k > mid` → map `k` to its mirror in the left half: `mirror = mid - (k - mid)`, recurse, then flip the bit.

**Implementation**

```python
def findKthBit_recursive(n: int, k: int) -> str:
    if n == 1:
        return '0'
    mid = 1 << (n - 1)          # 2^(n-1)
    if k == mid:
        return '1'
    if k < mid:
        return findKthBit_recursive(n - 1, k)
    mirror = mid - (k - mid)    # position in S_{n-1}
    bit = findKthBit_recursive(n - 1, mirror)
    return '1' if bit == '0' else '0'
```

**Complexity Analysis**
- Time complexity: O(n) — we descend at most `n` levels.
- Space complexity: O(n) — recursion stack depth.

---

### Approach 3: Iterative with Flip Flag

**Intuition**
Instead of recursion we can walk down the levels, keeping a boolean `flip` that tells us whether the current segment has been inverted an odd number of times. When we go to the right half we toggle `flip` because that half is inverted relative to the left.

**Algorithm**
- Initialize `flip = False`.
- While `n > 1`:
  - `mid = 2ⁿ⁻¹`.
  - If `k == mid`: answer is `'1'` flipped by `flip`; break.
  - If `k > mid`: set `k = mid - (k - mid)` (mirror to left) and toggle `flip`.
  - Decrement `n`.
- If we exit the loop (`n == 1`), the base bit is `'0'`; return it flipped by `flip`.

**Implementation**

```python
def findKthBit_iterative(n: int, k: int) -> str:
    flip = False
    while n > 1:
        mid = 1 << (n - 1)
        if k == mid:
            return '1' if not flip else '0'
        if k > mid:
            k = mid - (k - mid)   # mirror to left half
            flip = not flip
        n -= 1
    # n == 1 -> base string "0"
    return '0' if not flip else '1'
```

**Complexity Analysis**
- Time complexity: O(n) — one iteration per level.
- Space complexity: O(1) — only a few variables.

---

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

We trace the recursive solution on the example `n = 4, k = 11` (expected output `'1'`).

```
n=4, k=11
mid = 2^(4-1) = 8
k > mid → right half
mirror = 8 - (11-8) = 5          # map to position 5 in S3
flip needed later

n=3, k=5
mid = 2^(3-1) = 4
k > mid → right half
mirror = 4 - (5-4) = 3           # map to position 3 in S2
flip toggled (will flip twice total)

n=2, k=3
mid = 2^(2-1) = 2
k > mid → right half
mirror = 2 - (3-2) = 1           # map to position 1 in S1
flip toggled again (total flips = 2 → even)

n=1, k=1 → base case returns '0'
Apply flips: even number → unchanged → '0'
But recall each right‑half step also inverts the bit.
We performed two inversions → net effect: '0' → '1' → '0' → '1'? 
Let's accumulate: 
- Start base '0'.
- First inversion (n=2 step): '0' → '1'.
- Second inversion (n=3 step): '1' → '0'.
- Third inversion (n=4 step): '0' → '1'.
Thus final answer = '1'.
```

The table below captures each level:

| Level (n) | k before | mid | k > mid? | new k (mirror) | flip toggled? |
|-----------|----------|-----|----------|----------------|---------------|
| 4         | 11       | 8   | Yes      | 5              | Yes           |
| 3         | 5        | 4   | Yes      | 3              | Yes           |
| 2         | 3        | 2   | Yes      | 1              | Yes           |
| 1         | 1        | –   | –        | –              | –             |

Base bit = `'0'`; three flips → `'1'`.

This matches the expected output.