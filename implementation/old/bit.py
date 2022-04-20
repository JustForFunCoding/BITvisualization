from math import inf


class BIT:
    def __init__(self, size=16):
        self.size = size
        # Variable freqs is just as a helping array.
        # Not present in actual implementation.
        self.freqs = [0 for _ in range(self.size)]
        self.cumul_freqs = [0 for _ in range(self.size)]
        self.tree = [0 for _ in range(self.size)]

    def init_freqs(self, freqs):
        # If one doesn't want to have 0 initialized frequencies.

        # Every of them has to be nonnegative
        # It's because of counting cumulative frequencies
        # But 0th freq has to be 0, see book about BITs
        if freqs[0] != 0:
            print("Error: 0th frequency has to be zero.")
            return

        self.freqs = freqs
        self.compute_cumul_freqs()
        self.compute_tree()

    def compute_cumul_freqs(self):
        # We can use get_cumul_freq function, but it would be slower.
        s = 0
        for idx in range(self.size):
            s += self.freqs[idx]
            self.cumul_freqs[idx] = s

    def compute_tree(self):
        for idx, freq in enumerate(self.freqs[1:]):
            self.update_freq(idx+1, freq)

    def update_freq(self, idx, c):
        # Adds to the element at index «idx» constant «c».
        while idx < self.size:
            self.tree[idx] += c
            idx += LSB(idx)

    def get_cumul_freq(self, idx):
        res_cumul_sum = self.tree[0]
        while idx > 0:
            res_cumul_sum += self.tree[idx]
            idx = self.parent_index(idx)
        return res_cumul_sum

    def get_single_freq(self, idx):
        if idx < 0:
            print("Error: idx has to be non-negative")

        res_freq = self.tree[idx]
        pred, parent = idx-1, self.parent_index(idx)
        while pred != parent:
            res_freq -= self.tree[pred]
            pred = self.parent_index(pred)
        return res_freq

    def get_cumul_freq_index(self, freq_to_find):
        idx, mask = 0, self.size // 2

        while mask > 0:
            test_idx = idx + mask
            if freq_to_find >= self.tree[test_idx]:
                idx = test_idx
                freq_to_find -= self.tree[test_idx]
            mask //= 2

        return idx if freq_to_find == 0 else -1

    def parent_index(self, idx):
        if idx == 0:
            return -1
        return idx - LSB(idx)

    def show_interrogation_tree(self):
        print("** Interrogation tree **")
        for idx in range(self.size):
            while idx >= 0:
                print("{} -> ".format(idx), end='')
                idx = self.parent_index(idx)
            print("\\")
        print()

    def show_update_tree(self):
        print("** Update tree **")
        for idx in range(1, self.size+1):
            while idx <= self.size:
                print("{} -> ".format(idx), end='')
                idx = idx + (idx & (-idx))
            print("\\")
        print()

    def show_BIT(self):
        print("indices, freqs, cumul_freqs, tree:")
        print_array([idx for idx in range(self.size)])
        print_array(self.freqs)
        print_array(self.cumul_freqs)
        print_array(self.tree)


def print_array(arr, sep='\t'):
    print(sep.join(map(str, arr)))


def LSB(idx):
    return idx & (-idx)


def minmax(arr):
    m, M = inf, -inf
    for elem in arr:
        m = min(m, elem)
        M = max(M, elem)
    return m, M


def tests(bin_idx_tree):
    if not test_cumul_freq(bin_idx_tree):
        return
    if not test_get_single_freq(bin_idx_tree):
        return
    if not test_cumul_freq_index(bin_idx_tree):
        return


def test_cumul_freq(bin_idx_tree):
    print("** test_cumul_freq **")
    for idx in range(bin_idx_tree.size):
        got, expected = bin_idx_tree.get_cumul_freq(idx), \
            sum(bin_idx_tree.freqs[:idx+1])
        if got != expected:
            print("\tnok: bad result on idx={}: got {}, expected {}"
                  .format(idx, got, expected))
            return False
    print("\tok")
    return True


def test_get_single_freq(bin_idx_tree):
    print("** test_get_single_freq **")
    for idx in range(bin_idx_tree.size):
        got, expected = bin_idx_tree.get_single_freq(idx), \
            bin_idx_tree.freqs[idx]
        if got != expected:
            print("\tnok: bad result on idx={}: got {}, expected {}"
                  .format(idx, got, expected))
            return False
    print("\tok")
    return True


def test_cumul_freq_index(bin_idx_tree):
    print("** test_cumul_freq_index **")
    m, M = minmax(bin_idx_tree.cumul_freqs)
    for cumul_freq in range(m, M+1):
        got = bin_idx_tree.get_cumul_freq_index(cumul_freq)
        if got != -1 and bin_idx_tree.cumul_freqs[got] != cumul_freq:
            print("\tnok: bad result on cumul_freq={}, got: {}"
                  .format(cumul_freq, got))
            return False
    print("\tok")
    return True


def main():
    t = BIT()

    t.init_freqs([0, 1, 0, 2, 0, 2, 3, 1, 2, 3, 0, 1, 2, 0, 3, 1])
    return t


"""
    t.init_freqs([0, 2, 1, 1, 3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8])
    t.show_BIT()
    tests(t)
"""


"""
    # t.show_interrogation_tree()
    # t.show_update_tree()
    # t.show_BIT()
    t.init_freqs([0, 2, 0, 1, 1, 1, 0, 4, 4, 0, 1, 0, 1, 2, 3, 0])
    t.show_BIT()
    tests(t)
"""


main()
