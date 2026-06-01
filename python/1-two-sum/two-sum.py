class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        seen = {}

        for i, v in enumerate(nums):
            need = target - v

            if need in seen:
                return [seen[need], i]

            seen[v] = i