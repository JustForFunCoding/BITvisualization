# 1D
# Range update
# Range query


from bit_ru_pq_1d import BitRuPq


class BitRuRq:
    """
    Class representing 1D Binary indexed tree for set of operations Range update and Range query.

    Attributes:
        bitc:           tree for counting of linear term
        biti:           tree for counting of independent term
        size:           size of the trees
    """
    def __init__(self, size: int):
        """
        Constructor creates 2 BITs for Range update Point query operations.

        Defined when arguments hold the following conditions:
            0 <= size

        Args:
            size:       given size of the tree
        """
        self.bitc = BitRuPq(size)
        self.biti = BitRuPq(size)
        self.size = size

    def update(self, left: int, right: int, val: int) -> None:
        """
        Operation of range update as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= left <= size
            left <= right <= size

        Args:
            left:   index representing left boundary of the interval to be updated
            right:  index representing right boundary of the interval to be updated
            val:    value which is added to every element in the given interval

        Returns:    nothing is returned, but the tree is changed appropriately
        """
        self.bitc.updater(left, right, val)
        self.biti.updater(left, right, -val * (left - 1))
        self.biti.updater(right + 1, self.size, val * (right - left + 1))

    def query(self, idx: int) -> int:
        """
        Operation of range query as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= idx <= size

        Args:
            idx:    index determining which element should be returned

        Returns:    cumulative frequency at the given index
        """

        # a, b are not very descriptive names, however we use the same notation
        # as is used in the thesis

        a = self.bitc.queryp(idx)
        b = self.biti.queryp(idx)
        return a * idx + b

    def print_structure(self):
        """
        Helper method for user to see the content of two internal trees: bitc and biti.

        Returns:    nothing is returned, mentioned tree content with corresponding names is printed into console
        """
        self.bitc.print_tree("bitc")
        self.biti.print_tree("biti")


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
