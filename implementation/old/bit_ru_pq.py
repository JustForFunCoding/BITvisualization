# 1D
# Range update - Point Query


from typing import List


class BIT:
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * size

    def point_update(self, idx: int, val: int) -> None:
        # updates frequency at index «idx» by «val»
        # and updates all other tree values that need to be updated
        while idx < self.size:
            self.tree[idx] += val
            idx += LSB(idx)

    def range_update(self, x1: int, x2: int, val: int) -> None:
        # updates all frequencies x s.t. x₁ ≤ x ≤ x₂ by val
        # uses inclusion-exclusion principle
        self.point_update(x1, val)
        if x2 < self.size - 1:
            self.point_update(x2 + 1, -val)

    def point_query(self, idx: int) -> int:
        # point query is exactly the same as range query
        # in Point Update Range Query model
        # but be aware of this important property:
        #   in PU-RQ this computed value A[1..idx] (also now?)
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= LSB(idx)
        return s

    def get_all_cumul_freqs(self) -> List[int]:
        res: List[int] = []
        for i in range(1, self.size):
            res.append(self.point_query(i))
        return res

    def get_single_freq(self, idx: int) -> int:
        if idx == 0:
            return self.tree[idx]

        alpha, beta, gamma = idx, idx - 1, idx - LSB(idx)
        s = self.tree[alpha]
        while beta > gamma:
            s -= self.tree[beta]
            beta -= LSB(beta)
        return s

    def get_all_single_freqs(self) -> List[int]:
        res: List[int] = []
        for i in range(1, self.size):
            res.append(self.get_single_freq(i))
        return res

    def show_tree_values(self) -> None:
        print(self.tree)


def LSB(idx: int) -> int:
    return idx & (-idx)


def build_tree(arr: List[int]) -> BIT:
    size = len(arr)
    t = BIT(size)

    for i in range(1, size):
        t.point_update(i, arr[i])
        # t.range_update(i, i, arr[i])

    return t


if __name__ == '__main__':
    arr = [0, 1, 0, 2, 0, 2, 3, 1]
    print("arr:", arr)
    t = build_tree(arr)

    print("tree values: ", end='')
    t.show_tree_values()
    # print("cumulative frequencies: ", t.get_all_cumul_freqs())
    print("point queries: ", t.get_all_cumul_freqs())
    print("single frequencies: ", t.get_all_single_freqs())

    print("===")
    print("doing range_update(2, 5, 7)")
    t.range_update(2, 5, 7)
    print("===")

    print("tree values: ", end='')
    t.show_tree_values()
    # print("cumulative frequencies: ", t.get_all_cumul_freqs())
    print("point queries: ", t.get_all_cumul_freqs())
    print("single frequencies: ", t.get_all_single_freqs())
