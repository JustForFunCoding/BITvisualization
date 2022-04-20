# 1D
# Range update
# Point query


class BitRuPq:
    """
    Class representing Binary indexed tree for set of operations Range update and Point query.

    Attributes:
        tree:       internal representation of the tree
        size:       size of the tree, which is NOT changed during the existence of the object
    """
    def __init__(self, size: int):
        """
        Constructor initializes tree into array of 0s of the given size + 1.
        The reason why it's size + 1 see in bit_pu_rq_1d.py.

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
            idx += lsb(idx)

    def updater(self, left: int, right: int, val: int) -> None:
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
        self.updatep(left, val)
        self.updatep(right + 1, -val)

    def queryp(self, idx: int) -> int:
        """
        Operation of range query as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= idx <= size

        Args:
            idx:    index determining which element should be updated

        Returns:    cumulative frequency at the given index
        """
        cumul_freq = 0
        while idx > 0:
            cumul_freq += self.tree[idx]
            idx -= lsb(idx)
        return cumul_freq

    def print_tree(self, tree_name: str) -> None:
        """
        Helper method for user to see the content of the current tree values.

        Args:
            tree_name:  name of the tree

        Returns:        nothing is returned, but the tree name with its content is printed into console
        """
        print(tree_name + ": " + str(self.tree[1:]))


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
