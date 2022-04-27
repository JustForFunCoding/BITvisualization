# 2D
# Point update
# Range query

from bit_2d_abstract import *
from print_support import *


class BitPuRq2d(Bit2d):
    """
    Class representing 2D Binary indexed tree for set of operations Point update and Range query.

    Attributes:
        tree:       internal representation of the tree
        size:       size of the tree, which is NOT changed during the existence of the object
    """
    def __init__(self, size: int = 0, do_animate = True, canvas = "1", name = "bit"):
        """
        Constructor initializes tree into 2d array of 0s of size (size + 1) * (size + 1).
        The reason is the same as was with 1d BITs.

        Defined when arguments hold the following conditions:
            0 <= size

        Args:
            size:   given size of the tree
        """
        super().__init__(size, do_animate, canvas, name)

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
        tree_name = "bit"
        query_info = f'queryr({row},{col})'
        spaces = 4 * ' '

        if type(row) is not int or type(col) is not int:
            if self.animate:
                self.draw.push_print(f'{tree_name}.{query_info} starting')
                self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree,
                               None, None, 0, f'{query_info} starting')
                self.draw.push_print(f'{spaces}invalid format')
                self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree, None, None, 0,
                               f'{query_info} got invalid format')
                self.draw.push_print(f'{tree_name}.{query_info} finished')
                self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree,
                               None, None, 0, f'{query_info} finished')
            return 0
        return self.query_virtual(row, col, query_info, tree_name)

    def queryp(self, row: int, col: int) -> int:
        """
        Helper method to count true frequency (a.k.a. actual frequency).

        Args:
            row:    given row index
            col:    given column index

        Returns:    true frequency on position given by row and col indices
        """
        if self.animate:
            self.draw.push_print("{}queryp({},{})=?".format(self.name, row, col))
        true_freq=self.queryr(row, col) -\
            self.queryr(row - 1, col) -\
            self.queryr(row, col - 1) +\
            self.queryr(row - 1, col - 1)
        if self.animate:
            self.draw.push_print("{}queryp({},{})={}".format(self.name, row, col, true_freq))
        return true_freq

# Note: We suppose any argument given into any method / function lsb is the whole number.
# In addition, it also holds the conditions stated in documentation.

if __name__ == '__main__':
    tst = BitPuRq2d(10)
    tst.updatep(1,2,5)
    tst.queryr(1,2)
    tst.queryp(1,2)
