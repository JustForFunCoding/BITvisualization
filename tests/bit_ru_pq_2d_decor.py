# 2D
# Range update
# Point query

from bit_2d_abstract import *
from print_support import *

class BitRuPq2d(Bit2d):
    """
    Class representing 2D Binary indexed tree for set of operations Range update and Point query.

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


    def updater(self, row1: int, col1: int, row2: int, col2: int, val: int,
                text_from_update='', tree_name='bit', spaces_from_update='') -> None:
        """
        Operation of range update as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= row1, col1 <= size
            row1 <= row2 <= size
            col1 <= col2 <= size

        Args:
            row1:               starting row index
            col1:               starting column index
            row2:               ending row index
            col2:               ending column index
            val:                value which is added to every element inside interval given by row and column indices
            text_from_update:   helper text for better visualization

        Returns:    nothing is returned, but the tree is changed appropriately

        """
        updater_info = f'updater({row1},{col1},{row2},{col2},{val})'
        text_from_updater = ' of ' + updater_info + text_from_update
        spaces_from_updater = spaces_from_update + 4 * ' '

        if self.animate:
            self.draw.push_print(f'{spaces_from_update}{tree_name}.{updater_info} starting')
            self.draw.push(self, TreeType.UpdateTree, Bit2d.draw_update_tree, None, None, val,
                           f'{updater_info}{text_from_update} starting')

        if type(row1) is not int or type(row2) is not int or type(col1) is not int \
                or type(col2) is not int or type(val) is not int:
            if self.animate:
                self.draw.push_print(f'{spaces_from_updater}invalid format')
                self.draw.push(self, TreeType.UpdateTree, BitRuPq2d.draw_update_tree, None, None, val,
                               f'{updater_info} got invalid format')
        elif 1 <= row1 <= row2 <= self.size and 1 <= col1 <= col2 <= self.size:
            # valid range checked in updatep
            self.updatep(row1, col1, val, text_from_updater, tree_name, spaces_from_updater)
            self.updatep(row2 + 1, col1, -val, text_from_updater, tree_name, spaces_from_updater)
            self.updatep(row1, col2 + 1, -val, text_from_updater, tree_name, spaces_from_updater)
            self.updatep(row2 + 1, col2 + 1, val, text_from_updater, tree_name, spaces_from_updater)
        elif self.animate:
            self.draw.push_print(f'{spaces_from_updater}invalid interval, updating nothing')
            self.draw.push(self, TreeType.UpdateTree, BitRuPq2d.draw_update_tree, None, None, val,
                           f'{updater_info} got invalid interval')

        if self.animate:
            self.draw.push_print(f'{spaces_from_update}{tree_name}.{updater_info} finished')
            self.draw.push(self, TreeType.UpdateTree, Bit2d.draw_update_tree, None, None, val,
                           f'{updater_info}{text_from_update} finished')

    def queryp(self, row: int, col: int, text_from_query='', result_name='result',
               tree_name='bit', spaces_from_query='') -> int:
        """
        Operation of range query as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= row, col <= size

        Args:
            row:                given row index
            col:                given column index
            text_from_query:    helper text for better visualization
            tree_name:          helper text for better visualization
            spaces_from_query:  for better indentation in console prints

        Returns:    cumulative frequency on position given by row and col indices
        """
        query_info = f'{tree_name}.queryp({row},{col}){text_from_query}'
        spaces = spaces_from_query + 4 * ' '

        if type(row) is not int or type(col) is not int:
            if self.animate:
                self.draw.push_print(f'{query_info} starting')
                self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree,
                               None, None, 0, f'{query_info} starting')
                self.draw.push_print(f'{spaces}invalid format')
                self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree, None, None, 0,
                               f'{query_info} got invalid format')
                self.draw.push_print(f'{query_info} finished')
                self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree,
                               None, None, 0, f'{query_info} finished')
            return 0
        return self.query_virtual(row, col, query_info, result_name, tree_name, spaces_from_query)


# Note: We suppose any argument given into any method / function lsb is the whole number.
# In addition, it also holds the conditions stated in documentation.

if __name__ == '__main__':
    tst = BitRuPq2d(10)
    tst.updater(1,2,3,4,5)
    print(tst.queryp(1,2))
    # tst.print_array()
