# 1D
# Point update
# Range query


class BitPuRq:
    """
    Class representing Binary indexed tree for set of operations Point update and Range query.

    Attributes:
        tree:       internal representation of the tree
        size:       size of the tree, which is NOT changed during the existence of the object
    """

    def __init__(self, size: int):
        """
        Constructor initializes tree into array of 0s of the given size + 1.
        Why not only size? Because we have to index from 1, and we want to eliminate
        +- 1 bugs, so we let the array for tree to be [1...size], instead of possible [0...size-1].

        Defined when arguments hold the following conditions:
            0 <= size

        Args:
            size:       given size of the tree
        """
        self.tree = [0] * (size + 1)
        self.size = size

    def updatep(self, idx: int, val: int) -> None:
        """
        Operation of point update as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= idx <= size

        Args:
            idx:    index determining which element should be updated
            val:    value which is added to the given index

        Returns:    nothing is returned, but the tree is changed appropriately
        """
        while idx <= self.size:
            self.tree[idx] += val
            # nakresli update_tree(idx, val)
            idxold=idx
            idx = idx + lsb(idx)
            # nakresli link(idxold, idx)

    def queryr(self, idx: int) -> int:
        """
        Operation of range query as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= idx <= size

        Args:
            idx:    index determining which element should be updated

        Returns:    cumulative frequency at the given index
        """
        cumul_freq = 0
        # skackaj nad idx node value cumul_freq ?
        while idx > 0:
            cumul_freq += self.tree[idx]
            idx = idx - lsb(idx)
        return cumul_freq

    def get_single_freq(self, idx: int) -> int:
        """
        Operation of finding the value of single frequency as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= idx <= size

        Args:
            idx:    index determining which element should be updated

        Returns:    true frequency at the given index
        """
        if idx == 0:
            return self.tree[idx]

        predecessor, parent = idx - 1, idx - lsb(idx)
        res = self.tree[idx]
        while predecessor != parent:
            res -= self.tree[predecessor]
            predecessor -= lsb(predecessor)
        return res

    def print_single_freqs(self) -> None:
        """
        Helper method for user to see the values he/she did so far,
        i.e. virtual representation of the array, which is proper for human.
        For instance, after the following operations:
            bit = BitPuRq(4)
            bit.updatep(2, 1)
            bit.updatep(4, 5),
        bit.print_single_freqs() will print to console: '0 1 0 5'.

        Returns:    nothing is returned, virtual representation is printed to console
        """
        for i in range(1, self.size + 1):
            print(self.get_single_freq(i), end=' ')
        print()


def lsb(num: int) -> int:
    """
    Helper function for counting least significant 1 bit of the given number.

    Args:
        num:    given number

    Returns:    lest significant 1 bit of the given number

    """
    return num & (-num)

# Note: We suppose any argument given into any method / function lsb is the whole number.
# In addition, it also holds the conditions stated in documentation.
