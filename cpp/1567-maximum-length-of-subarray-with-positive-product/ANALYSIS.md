# Sliding Window

## Video Solution

For more details about **Maximum Length of Subarray With Positive Product**, watch the walkthrough at [https://www.youtube.com/watch?v=isC1Mi4kdIA](https://www.youtube.com/watch?v=isC1Mi4kdIA)

## Concept

We need the longest contiguous segment whose product is **> 0**.  
A product is positive when the segment contains an **even number of negative values** and **no zeros** (zero makes the product zero).  
Thus we can scan the array, treating zeros as natural separators: each zero forces us to start a new window because any subarray crossing it would have product 0.

Within a zero‑free segment we only care about the **parity** (odd/even) of negative numbers.  
If the total count of negatives in the segment is even, the whole segment works.  
If it is odd, we must drop either the prefix up to the first negative **or** the suffix from the last negative to make the remaining part have an even number of negatives. The longer of those two truncations gives the best length for that segment.

## When to Use It

Use a sliding‑window‑style scan when you see:
- Request for longest/shortest **subarray** (contiguous) satisfying a condition that can be updated incrementally.
- The condition depends on a **property that can be tracked with counters** (e.g., number of negatives, sum, parity) and is **broken** by a specific element (here, zero) that forces a reset.
- You can process the array in **O(n)** time with **O(1)** extra space by moving a start pointer only forward.

## Template

```python
def longest_subarray_condition(nums):
    ans = 0
    start = 0                     # left bound of current window
    # any extra state variables go here (e.g., counters, first/last occurrence)
    while start < len(nums):
        # skip elements that break the condition (e.g., zeros)
        if nums[start] == 0:
            start += 1
            continue

        end = start
        # expand end while the condition‑breaking element is not met
        while end < len(nums) and nums[end] != 0:
            # update state with nums[end]
            end += 1

        # now [start, end) is a maximal zero‑free segment
        # evaluate the best sub‑window inside it using the state
        ans = max(ans, best_length_inside_segment(...))

        # move start to the element after the segment (the zero or end of array)
        start = end
    return ans
```

## LeetCode Problem Walkthrough

### Problem: 1567. Maximum Length of Subarray With Positive Product

https://leetcode.com/problems/maximum-length-of-subarray-with-positive-product/

---

### Approach 1: Brute Force

**Algorithm**  
Check every possible subarray, compute its product (or just track sign), and keep the maximum length whose product is positive.  
Because the product can overflow, we only track the sign (negative/positive/zero) while iterating.

**Implementation**

```python
class Solution:
    def getMaxLen(self, nums: List[int]) -> int:
        n = len(nums)
        best = 0
        for i in range(n):
            sign = 1          # 1 = positive, -1 = negative, 0 = zero encountered
            for j in range(i, n):
                if nums[j] == 0:
                    sign = 0
                elif nums[j] < 0:
                    sign *= -1
                # if sign == 0, product is zero → not positive, break early
                if sign == 0:
                    break
                if sign == 1:                 # positive product
                    best = max(best, j - i + 1)
        return best
```

**Complexity Analysis**

- Time complexity: O(n²) — two nested loops over the array.  
- Space complexity: O(1) — only a few integer variables.

---

### Approach 2: Prefix Sign Tracking (Optimized)

**Intuition**  
While scanning a zero‑free segment, the sign of the product of nums[l…r] depends only on the parity of negative numbers seen so far.  
If we store the **first index** where each parity (even/odd) occurs, we can instantly know the longest subarray ending at the current position with an even number of negatives.

**Algorithm**  
- Split the array by zeros.  
- For each segment, maintain a dictionary `first_occurrence` mapping parity (`0` for even negatives seen so far, `1` for odd) to the earliest index where that parity was seen.  
- Initialise parity = 0 (even) before the segment starts, and record `first_occurrence[0] = start‑1` (a virtual index before the segment).  
- As we extend `end`, flip parity when we see a negative.  
- If the current parity has been seen before at index `first_occurrence[parity]`, then the subarray from that index+1 to `end` has an even number of negatives → update answer with its length.  
- If the parity is new, store its first occurrence.

**Implementation**

```python
class Solution:
    def getMaxLen(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        i = 0
        while i < n:
            if nums[i] == 0:
                i += 1
                continue

            # start of a zero‑free segment
            seg_start = i
            # parity 0 = even number of negatives seen, 1 = odd
            first_occurrence = {0: seg_start - 1}   # virtual index before segment
            parity = 0
            while i < n and nums[i] != 0:
                if nums[i] < 0:
                    parity ^= 1                     # flip parity
                if parity in first_occurrence:
                    length = i - first_occurrence[parity]
                    ans = max(ans, length)
                else:
                    first_occurrence[parity] = i
                i += 1
            # i now points at a zero or n; loop continues
        return ans
```

**Complexity Analysis**

- Time complexity: O(n) — each element is processed once.  
- Space complexity: O(1) — the dictionary holds at most two entries (parity 0 and 1).

---

### Approach 3: Single Pass with First/Last Negative (Most Optimal)

**Intuition**  
In a zero‑free segment, if the total number of negatives is even, the whole segment is valid.  
If it is odd, we must exclude either the prefix up to the first negative **or** the suffix after the last negative to make the remaining part have an even count.  
Thus we only need to know:
- the index of the first negative,
- the index of the last negative,
- the total count of negatives.  
No extra storage is required beyond a few variables.

**Algorithm**  
- Iterate through the array, using `start` to mark the beginning of the current zero‑free block.  
- Within the block, maintain `neg_count`, `first_neg`, `last_neg`.  
- When we hit a zero or the array end, evaluate the block:  
  - If `neg_count` is even → whole block length `end - start` is valid.  
  - If odd → best length is max(`end - first_neg - 1`, `last_neg - start`).  
- Reset counters and move `start` to the element after the zero.

**Implementation**

```python
class Solution:
    def getMaxLen(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        start = 0                     # left bound of current zero‑free segment

        while start < n:
            if nums[start] == 0:      # skip zeros
                start += 1
                continue

            end = start
            neg_cnt = 0
            first_neg = -1
            last_neg = -1

            # expand the segment until a zero or end of array
            while end < n and nums[end] != 0:
                if nums[end] < 0:
                    neg_cnt += 1
                    if first_neg == -1:
                        first_neg = end
                    last_neg = end
                end += 1

            # evaluate the segment [start, end)
            if neg_cnt % 2 == 0:               # even negatives → whole segment works
                ans = max(ans, end - start)
            else:                              # odd negatives → drop one side
                # option 1: exclude prefix up to first_neg
                ans = max(ans, end - first_neg - 1)
                # option 2: exclude suffix from last_neg
                ans = max(ans, last_neg - start)

            start = end                         # move to next segment (zero or n)

        return ans
```

**Complexity Analysis**

- Time complexity: O(n) — each index is visited at most twice (once by `start`, once by `end`).  
- Space complexity: O(1) — only a handful of integer variables.

---

### Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

**Dry run** on `nums = [1, -2, -3, 0, 1, -1, -2, -3, 4]`

We'll trace the zero‑free segments and the variables `neg_cnt`, `first_neg`, `last_neg`.

| Step | index | nums[idx] | neg_cnt | first_neg | last_neg | Action / Comment |
|------|-------|-----------|---------|-----------|----------|------------------|
| 1    | 0     | 1         | 0       | -1        | -1       | start=0, segment begins |
| 2    | 1     | -2        | 1       | 1         | 1        | first negative seen |
| 3    | 2     | -3        | 2       | 1         | 2        | second negative → even |
| 4    | 3     | 0         | 2       | 1         | 2        | hit zero → evaluate segment [0,3) |
|      |       |           |         |           |          | `neg_cnt` even → length = 3-0 = 3 → ans=3 |
| 5    | 4     | 1         | 0       | -1        | -1       | new segment start=4 |
| 6    | 5     | -1        | 1       | 5         | 5        |
| 7    | 6     | -2        | 2       | 5         | 6        |
| 8    | 7     | -3        | 3       | 5         | 7        |
| 9    | 8     | 4         | 3       | 5         | 7        |
|10    | 9     | (end)     | 3       | 5         | 7        | reached array end → evaluate segment [4,9) |
|      |       |           |         |           |          | `neg_cnt` odd → |
|      |       |           |         |           |          | option1: end‑first_neg‑1 = 9‑5‑1 = 3 |
|      |       |           |         |           |          | option2: last_neg‑start = 7‑4 = 3 |
|      |       |           |         |           |          | ans stays 3 |

The longest subarray with positive product is length 3 (e.g., `[1,-2,-3]` or `[-1,-2,-3]`).

--- 

**End of Lecture**. Commit this file as `.github/ISSUE_TEMPLATE/lecture-Sliding-Window.md` or directly create a GitHub issue with the above content. Ensure no existing lecture for *Sliding Window* is present in `/lectures/` before creating. If one exists, pick the next uncovered topic from the prescribed rotation list.