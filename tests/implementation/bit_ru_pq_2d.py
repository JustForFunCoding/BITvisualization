# 2D
# Range update
# Point query


class BitRuPq2d:
    """
    Class representing 2D Binary indexed tree for set of operations Range update and Point query.

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

    def queryp(self, row: int, col: int) -> int:
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

    def updater(self, row1: int, col1: int, row2: int, col2: int, val: int) -> None:
        """
        Operation of range update as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= row1, col1 <= size
            row1 <= row2 <= size
            col1 <= col2 <= size

        Args:
            row1:   starting row index
            col1:   starting column index
            row2:   ending row index
            col2:   ending column index
            val:    value which is added to every element inside interval given by row and column indices

        Returns:    nothing is returned, but the tree is changed appropriately

        """
        self.updatep(row1, col1, val)
        self.updatep(row2 + 1, col1, -val)
        self.updatep(row1, col2 + 1, -val)
        self.updatep(row2 + 1, col2 + 1, val)

    def print_tree(self, tree_name: str) -> None:
        """
        Helper method for user to see the content of the current tree values.

        Args:
            tree_name:  name of the tree

        Returns:        nothing is returned, but the tree name with its content is printed into console
        """
        print(tree_name)
        for row in self.tree:
            print("\t".join(map(str, row)))
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
