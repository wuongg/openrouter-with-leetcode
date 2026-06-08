# Stack

## Video Solution

For more details about **Decode String**, watch the walkthrough at [resources](https://www.youtube.com/watch?v=qB0zZpBJlh8).

## Concept

The **stack** technique lets us handle nested structures by processing the innermost pieces first and then bubbling the results outward.  
Think of a set of Russian nesting dolls: you cannot see the outer doll’s final form until you open each inner doll, resolve what’s inside, and then reassemble. In the *decode string* problem, each `k[ ... ]` block is a doll, and the stack stores the state (the repeat count and the string built so far) each time we enter a new level of nesting.

## When to Use It

Use a stack when you see:
- Nested patterns indicated by matching brackets/parentheses (`[]`, `{}`, `()`).
- A need to pause processing of an outer construct while you resolve an inner one.
- Problems that ask you to decode, evaluate, or build strings based on repetition counts inside brackets (e.g., `k[encoded_string]`).
- Situations where the input guarantees well‑formed nesting (no mismatched brackets).

## Template

```python
# Generic stack‑based pattern for nested repetition
def decode_pattern(s: str) -> str:
    count_stack = []   # stores repeat counts
    result_stack = []  # stores the string built before the current '['
    cur_num = 0
    cur_str = []

    for ch in s:
        if ch.isdigit():
            # build multi‑digit numbers
            cur_num = cur_num * 10 + int(ch)
        elif ch == '[':
            # push current context and start a fresh one
            count_stack.append(cur_num)
            result_stack.append(''.join(cur_str))
            cur_num = 0
            cur_str = []
        elif ch == ']':
            # finish current block: repeat it and attach to previous context
            repeat = count_stack.pop()
            prev = result_stack.pop()
            cur_str = [prev + ''.join(cur_str) * repeat]
        else:
            # regular character
            cur_str.append(ch)

    return ''.join(cur_str)
```

## LeetCode Problem Walkthrough

### Problem: 394. Decode String
https://leetcode.com/problems/decode-string/

---

### Approach 1: Brute Force – Recursive Expansion

**Algorithm**
1. Scan the string left‑to‑right.
2. When a digit is found, read the full integer `k`.
3. Locate the matching closing bracket for the current `[` using a counter.
4. Recursively decode the substring inside the brackets.
5. Repeat the decoded substring `k` times and concatenate with the part before the bracket.
6. Continue scanning after the closing bracket.

**Implementation**
```python
class Solution:
    def decodeString(self, s: str) -> str:
        def helper(i: int) -> tuple[str, int]:
            """Returns (decoded_substring, next_index_after_processed_part)"""
            res = []
            n = len(s)
            while i < n and s[i] != ']':
                if s[i].isdigit():
                    # read full number
                    k = 0
                    while i < n and s[i].isdigit():
                        k = k * 10 + int(s[i])
                        i += 1
                    # skip '['
                    i += 1  # now at start of encoded part
                    decoded, i = helper(i)   # decode inside brackets
                    res.append(decoded * k)
                else:
                    res.append(s[i])
                    i += 1
            # i points to ']' or end
            return ''.join(res), i + 1   # skip ']'

        decoded, _ = helper(0)
        return decoded
```

**Complexity Analysis**
- Time complexity: O(n * output_length) – each level may repeat work when constructing the final string; in the worst case (deep nesting) we copy strings many times.
- Space complexity: O(output_length + recursion_depth) – the call stack plus the result.

---

### Approach 2: Two‑Stack Iterative (Optimal)

**Intuition**
Instead of recomputing substrings repeatedly, we keep track of two independent pieces of information:
1. How many times the upcoming block should be repeated (`count_stack`).
2. The string that has been built *before* the current block (`result_stack`).  
When we encounter a `[`, we push the current context and start fresh. When we hit a `]`, we pop the repeat count and the previous string, expand the current block, and attach it to the previous context. This avoids repeated string copying and processes each character exactly once.

**Algorithm**
- Iterate over each character.
- On a digit, accumulate the full repeat count.
- On `[`, push the accumulated count and the current built string onto their respective stacks, then reset them.
- On `]`, pop the repeat count and previous string, repeat the current built string that many times, and prepend the previous string.
- On a letter, append it to the current built string.

**Implementation**
```python
class Solution:
    def decodeString(self, s: str) -> str:
        count_stack = []   # stores repeat counts
        result_stack = []  # stores strings built before each '['
        cur_num = 0
        cur_str = []       # use list for efficient appends

        for ch in s:
            if ch.isdigit():
                cur_num = cur_num * 10 + int(ch)
            elif ch == '[':
                count_stack.append(cur_num)
                result_stack.append(''.join(cur_str))
                cur_num = 0
                cur_str = []
            elif ch == ']':
                repeat = count_stack.pop()
                prev = result_stack.pop()
                cur_str = [prev + ''.join(cur_str) * repeat]
            else:  # regular letter
                cur_str.append(ch)

        return ''.join(cur_str)
```

**Complexity Analysis**
- Time complexity: O(n + output_length) – each character is processed once; building the final string takes time proportional to its size.
- Space complexity: O(n) – the two stacks together store at most O(n) integers/strings (depth of nesting), plus the output.

---

### Approach 3: Single Stack of Tuples (Alternative Optimal)

**Intuition**
We can combine the two stacks into a single stack where each element is a tuple `(prev_string, repeat_count)`. This halves the number of stack operations and makes the intent clearer: each stack frame remembers what we had before entering a bracket and how many times to repeat the forthcoming block.

**Algorithm**
- Push a base frame `("", 1)` to simplify edge cases.
- While scanning:
  - Digits → build the current repeat count.
  - `[` → push `(current_string, current_count)` and reset both.
  - `]` → pop `(prev_string, repeat)`; set `current_string = prev_string + current_string * repeat`.
  - Letter → append to `current_string`.
- At the end, `current_string` holds the answer.

**Implementation**
```python
class Solution:
    def decodeString(self, s: str) -> str:
        stack = [("", 1)]          # (accumulated_string, repeat_count_for_next_block)
        cur_num = 0
        cur_str = []

        for ch in s:
            if ch.isdigit():
                cur_num = cur_num * 10 + int(ch)
            elif ch == '[':
                stack.append((''.join(cur_str), cur_num))
                cur_str = []
                cur_num = 0
            elif ch == ']':
                prev_str, repeat = stack.pop()
                cur_str = [prev_str + ''.join(cur_str) * repeat]
            else:
                cur_str.append(ch)

        return ''.join(cur_str)
```

**Complexity Analysis**
- Time complexity: O(n + output_length) – identical to the two‑stack version.
- Space complexity: O(n) – one stack of at most depth‑of‑nesting elements.

---

## Provide a Visual Demonstration

**Impact: HIGH** | **Category: explanation** | **Tags:** dry-run, trace, example

### Dry Run

We trace the two‑stack algorithm on the input `s = "3[a2[c]]"`.

| Step | ch | cur_num | cur_str (as string) | count_stack          | result_stack          | Action                                            |
|------|----|---------|----------------------|----------------------|-----------------------|---------------------------------------------------|
| 0    | –  | 0       | ""                   | []                   | []                    | start                                             |
| 1    | '3'| 3       | ""                   | []                   | []                    | digit → accumulate                               |
| 2    | '['| 0       | ""                   | [3]                  | [""]                  | push count & string, reset                       |
| 3    | 'a'| 0       | "a"                  | [3]                  | [""]                  | regular char                                     |
| 4    | '2'| 2       | "a"                  | [3]                  | [""]                  | digit → accumulate                               |
| 5    | '['| 0       | "a"                  | [3, 2]               | ["", "a"]             | push count & string, reset                       |
| 6    | 'c'| 0       | "c"                  | [3, 2]               | ["", "a"]             | regular char                                     |
| 7    | ']'| 0       | "acc"                | [3]                  | [""]                  | pop repeat=2, prev="a" → "a" + "c"*2 = "acc"    |
| 8    | ']'| 0       | "accaccacc"          | []                   | []                    | pop repeat=3, prev="" → "" + "acc"*3 = "accaccacc"|
| End  | –  | 0       | "accaccacc"          | []                   | []                    | return result                                    |

The final decoded string matches the expected output `"accaccacc"`.

--- 

*End of lecture.*