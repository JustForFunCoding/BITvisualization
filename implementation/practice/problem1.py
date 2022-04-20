# Problem statement: https://leetcode.com/problems/range-sum-query-mutable/

# This example shows the usage of 1D BIT Range update Range query


from typing import List


class BIT_RU_PQ:
    def __init__(self, size: int):
        self.tree = [0] * (size + 1)
        self.size = size

    def updatep(self, idx: int, val: int) -> None:
        while idx <= self.size:
            self.tree[idx] += val
            idx += lsb(idx)

    def updater(self, x1: int, x2: int, val: int) -> None:
        self.updatep(x1, val)
        self.updatep(x2 + 1, -val)

    def queryp(self, idx: int) -> int:
        res = 0
        while idx > 0:
            res += self.tree[idx]
            idx -= lsb(idx)
        return res

    def print_tree(self, name: str) -> None:
        print(f'{name}: {self.tree}')


class BIT_RU_RQ:
    def __init__(self, size: int):
        self.bitc = BIT_RU_PQ(size)
        self.biti = BIT_RU_PQ(size)
        self.size = size

    def update(self, x1: int, x2: int, val: int) -> None:
        self.bitc.updater(x1, x2, val)
        self.biti.updater(x1, x2, -val * (x1 - 1))
        self.biti.updater(x2 + 1, self.size, val * (x2 - x1 + 1))

    def query(self, idx: int) -> int:
        a = self.bitc.queryp(idx)
        b = self.biti.queryp(idx)
        return a * idx + b


def lsb(num: int) -> int:
    return num & (-num)


class NumArray:

    def __init__(self, nums: List[int]):
        size = len(nums)
        self.BIT = BIT_RU_RQ(size)
        for idx, num in enumerate(nums):
            idx += 1  # We index from 1.
            self.BIT.update(idx, idx, num)
        self.BIT.bitc.print_tree("bitc")
        self.BIT.biti.print_tree("biti")

    def update(self, index: int, val: int) -> None:
        index += 1
        # At first, we have to find out actual value
        act_val = self.BIT.query(index) - self.BIT.query(index - 1)
        # Now we want to have there value 'val'
        # so we have to count the difference by which we want to update
        diff = val - act_val
        self.BIT.update(index, index, diff)

    def sumRange(self, left: int, right: int) -> int:
        left += 1
        right += 1
        return self.BIT.query(right) - self.BIT.query(left - 1)

# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# obj.update(index,val)
# param_2 = obj.sumRange(left,right)