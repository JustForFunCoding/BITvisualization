# 1D
# Point Update - Range Query


from typing import Optional, List


class BIT:
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * size

    def point_update(self, idx: int, val: int) -> None:
        # updates self.tree[idx] += val
        # and every other index needed
        while idx < self.size:
            self.tree[idx] += val
            idx += LSB(idx)

    def range_query(self, idx: int) -> int:
        # returns value of A[1..idx]
        s = 0
        while idx >= 0:
            s += self.tree[idx]
            idx -= LSB(idx)
        return s

    def get_all_range_queries(self, start: int, end: int) -> List[int]:
        res: List[int] = []
        for i in range(start, end + 1):
            res.append(self.range_query(i))
        return res

    def get_single_freq(self, idx: int) -> int:
        # returns exact value of A[idx], not cumulative, not tree
        if idx == 0:
            return self.tree[0]

        alpha, beta, gamma = idx, idx - 1, idx - LSB(idx)
        s = self.tree[alpha]  # tree[alpha], not cumul_freq[alpha]
        while beta > gamma:
            s -= self.tree[beta]
            beta -= LSB(beta)
        return s

    def get_all_single_freqs(self, start: int, end: int) -> List[int]:
        res: List[int] = []
        for i in range(start, end + 1):
            res.append(self.get_single_freq(i))
        return res

    def get_index(self, cumul_freq: int) -> Optional[int]:
        # given cumulative frequency, functions returns index
        # s.t. cumsum(A[index]) == cumul_freq
        if cumul_freq < self.tree[0]:
            return None

        idx, mask = 0, self.size // 2
        while mask > 0:
            test_idx = idx + mask
            if cumul_freq >= self.tree[test_idx]:
                cumul_freq -= self.tree[test_idx]
                mask = test_idx
            mask //= 2
        return None if self.tree[idx] != 0 else idx

    def show_tree(self):
        print(self.tree)


def LSB(num: int) -> int:
    return num & (-num)


def rsum(arr: List[int], j: int) -> int:
    s = 0
    for i in range(j + 1):
        s += arr[i]
    return s


def range_query_test(t: BIT, arr: List[int]) -> bool:
    print("\t** range query test **")

    for i in range(t.size):
        got = t.range_query(i)
        expected = rsum(arr, i)
        if got != expected:
            print("\t\tnok: i={}, got={}, expcted={}"
                  .format(i, got, expected))
            return False

    print("\t\tok")
    return True


def get_single_freq_test(t: BIT, arr: List[int]) -> bool:
    print("\t** single freq test **")

    for i in range(t.size):
        got = t.get_single_freq(i)
        expected = arr[i]
        if got != expected:
            print("\t\tnok: i={}, got={}, expected={}"
                  .format(i, got, expected))
            return False
    print("\t\tok")
    return True


def get_index_test(t: BIT, arr: List[int]) -> bool:
    print("\t** get index test **")

    max_cum_freq = sum(arr)
    for cumul_freq in range(max_cum_freq + 5):
        got = t.get_index(cumul_freq)
        if got != cumul_freq:
            print("\t\tnok: cum_freq={}, got={}"
                  .format(cumul_freq, got))
            return False
    print("\t\tok")
    return True


def tests(t: BIT, arr: List[int]) -> None:
    print("** tests **")
    ok = True

    # we want to run other test even tho in case preceding tests
    # have failed
    ok = range_query_test(t, arr) and \
        get_single_freq_test(t, arr) and \
        get_index_test(t, arr)

    string = "\t* ok *" if ok else "\t* nok *"
    print(string)


def build_tree(arr: List[int]) -> BIT:
    n = len(arr)
    t = BIT(n)

    for i in range(1, n):
        t.point_update(i, arr[i])

    return t


def __main__():
    arr = [0, 1, 0, 2, 0, 2, 3, 1]
    t = build_tree(arr)

    print("arr:", arr)
    print("tree values: ", end='')
    t.show_tree()
    print("cumulative frequencies: ", t.get_all_range_queries(0, 7))
    print("single frequencies: ", t.get_all_single_freqs(0, 7))

    print("===")
    print("point_update(2, 5)")
    t.point_update(2, 5)
    print("===")

    print("tree values: ", end='')
    t.show_tree()
    print("cumulative frequencies: ", t.get_all_range_queries(0, 7))
    print("single frequencies: ", t.get_all_single_freqs(0, 7))

    # tests(t, arr)


if __name__ == '__main__':
    __main__()
