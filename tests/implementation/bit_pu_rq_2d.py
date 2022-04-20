# 2D
# Point update
# Range query


class BitPuRq2d:
    """
    Class representing 2D Binary indexed tree for set of operations Point update and Range query.

    Attributes:
        tree:       internal representation of the tree
        size:       size of the tree, which is NOT changed during the existence of the object
    """
    def __init__(self, size: int):
        """
        Constructor initializes tree into 2d array of 0s of size (size + 1) * (size + 1).
        The reason is the same as was with 1d BITs.

        Defined when arguments hold the following conditions:
            0 <= size

        Args:
            size:   given size of the tree
        """
        self.tree = [[0 for _ in range(size+1)] for _ in range(size+1)]
        self.size = size

    def updatep(self, row: int, col: int, val: int) -> None:
        """
        Operation of point update as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= row, col <= size

        Args:
            row:    given row index
            col:    given column index
            val:    value which is added to the element given by row and col indices

        Returns:    nothing is returned, but the tree is changed appropriately
        """
        r = row
        while r <= self.size:
            c = col
            while c <= self.size:
                self.tree[r][c] += val
                c += lsb(c)
            r += lsb(r)

    def queryr(self, row: int, col: int) -> int:
        """
        Operation of range query as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= row, col <= size

        Args:
            row:    given row index
            col:    given column index

        Returns:    cumulative frequency on position given by row and col indices
        """
        cumul_freq = 0
        r = row
        while r > 0:
            c = col
            while c > 0:
                cumul_freq += self.tree[r][c]
                c -= lsb(c)
            r -= lsb(r)
        return cumul_freq

    def queryp(self, row: int, col: int) -> int:
        """
        Helper method to count true frequency (a.k.a. actual frequency).

        Args:
            row:    given row index
            col:    given column index

        Returns:    true frequency on position given by row and col indices
        """
        return self.queryr(row, col) -\
            self.queryr(row - 1, col) -\
            self.queryr(row, col - 1) +\
            self.queryr(row - 1, col - 1)

    def print_true_freqs(self) -> None:
        """
        Helper method for user to see the values he/she did so far,
        i.e. virtual representation of the 2d array, which is proper for human.

        Returns:    nothing is returned, virtual representation of 2d array is printed to console
        """
        print("True frequencies")
        for r in range(1, self.size + 1):
            for c in range(1, self.size + 1):
                row_print = ""
                if c > 1:
                    row_print += "\t"
                row_print += str(self.queryp(r, c))
                print(row_print, end='')
            print()
        print("==========")


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
