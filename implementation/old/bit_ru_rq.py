# Range Update - Range Query


from typing import List


class BIT_RU_PQ:
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * size

    def point_update(self, idx: int, val: int) -> None:
        while idx < self.size:
            self.tree[idx] += val
            idx += LSB(idx)

    def range_update(self, x1: int, x2: int, val: int) -> None:
        self.point_update(x1, val)
        if x2 < self.size:
            self.point_update(x2 + 1, -val)

    def point_query(self, idx: int) -> int:
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= LSB(idx)
        return s


class BIT_RU_RQ:
    def __init__(self, size: int) -> None:
        self.size = size
        self.bitc = BIT_RU_PQ(size)
        self.biti = BIT_RU_PQ(size)

    def range_update(self, x1: int, x2: int, c: int) -> None:
        self.bitc.range_update(x1, x2, c)
        self.biti.range_update(x1, x2, -c * (x1 - 1))
        self.biti.range_update(x2 + 1, self.size - 1, c * (x2 - x1 + 1))

    def range_query(self, x: int) -> int:
        a = self.bitc.point_query(x)
        b = self.biti.point_query(x)
        return a * x + b

    def get_all_range_queries(self) -> List[int]:
        res: List[int] = []
        for idx in range(1, self.size):
            res.append(self.range_query(idx))
        return res

    def get_single_freq(self, idx: int) -> int:
        if idx == 0:
            return self.range_query(idx)
        return self.range_query(idx) - self.range_query(idx - 1)

    def get_all_single_freqs(self) -> List[int]:
        res: List[int] = []
        for idx in range(1, self.size):
            res.append(self.get_single_freq(idx))
        return res

    def get_bitc_values(self) -> List[int]:
        return self.bitc.tree

    def get_biti_values(self) -> List[int]:
        return self.biti.tree


def LSB(idx: int) -> int:
    return idx & (-idx)


A = [0, 1, 0, 2, 0, 2, 3, 1]


def build_tree(arr=A) -> BIT_RU_RQ:
    size = len(arr)
    t: BIT_RU_RQ = BIT_RU_RQ(size)

    for i in range(1, size):
        t.range_update(i, i, arr[i])

    return t
