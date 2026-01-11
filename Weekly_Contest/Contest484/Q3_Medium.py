"""
Docstring for Untitled-1

You are given an array words of n strings. Each string has length m and contains only lowercase English letters.

Two strings s and t are similar if we can apply the following operation any number of times (possibly zero times) so that s and t become equal.

Choose either s or t.
Replace every letter in the chosen string with the next letter in the alphabet cyclically. The next letter after 'z' is 'a'.
Count the number of pairs of indices (i, j) such that:

i < j
words[i] and words[j] are similar.
Return an integer denoting the number of such pairs.

 

Example 1:

Input: words = ["fusion","layout"]

Output: 1

Explanation:

words[0] = "fusion" and words[1] = "layout" are similar because we can apply the operation to "fusion" 6 times. The string "fusion" changes as follows.

"fusion"
"gvtjpo"
"hwukqp"
"ixvlrq"
"jywmsr"
"kzxnts"
"layout"
Example 2:

Input: words = ["ab","aa","za","aa"]

Output: 2

Explanation:

words[0] = "ab" and words[2] = "za" are similar. words[1] = "aa" and words[3] = "aa" are similar.

 

Constraints:

1 <= n == words.length <= 105
1 <= m == words[i].length <= 105
1 <= n * m <= 105
words[i] consists only of lowercase English letters.

Note: Please do not copy the description during the contest to maintain the integrity of your submissions.

"""

# Coding Section

from typing import List
from collections import defaultdict

class Solution:
    def countPairs(self, words: List[str]) -> int:   
        
        """
        Count the number of similar string pairs in a list of words.

        Intuition:
        Two strings are similar if one can be shifted cyclically to match the other.
        This is equivalent to checking if all characters in the string have the same
        relative differences modulo 26.

        Approach:
        - Convert each word into a "pattern" representing the difference of each character
          from the first character modulo 26.
        - Use a dictionary to count how many times each pattern occurs.
        - For each pattern that occurs k times, there are k * (k - 1) / 2 similar pairs.

        Complexity:
        - Time: O(N * M), where N is the number of words and M is the length of each word,
          to compute patterns for all words.
        - Space: O(N * M) in the worst case for storing patterns in the dictionary.

        Returns:
            int: Total number of similar word pairs.
        """
             
        pattern_count = defaultdict(int)
        res = 0

        for word in words:
            # compute pattern: difference from first char
            pattern = tuple((ord(c) - ord(word[0])) % 26 for c in word)
            pattern_count[pattern] += 1

        # count pairs
        for count in pattern_count.values():
            if count >= 2:
                res += count * (count - 1) // 2

        return res