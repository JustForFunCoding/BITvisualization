# 1D
# Range update
# Point query

from print_support import *
from typing import Tuple
from copy import copy
from bit_ru_pq_1d_decor import BitRuPq
#from pdb import set_trace

class BitRuRq:
    """
    Class representing 1D Binary indexed tree for set of operations Range update and Range query.

    Attributes:
        bitc:           tree for counting of linear term
        biti:           tree for counting of independent term
        size:           size of the trees
    """
        
    def __init__(self, size: int = 0, do_animate = True):
        """
        Constructor creates 2 BITs for Range update Point query operations.

        Defined when arguments hold the following conditions:
            0 <= size

        Args:
            size:       given size of the tree
        """
        self.bitc = BitRuPq(size, do_animate, 1, "bitc:")
        self.biti = BitRuPq(size, do_animate, 2, "biti:")
        self.size = size
        self.animate = do_animate

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
        #####
        update_info = f'update({left},{right},{val})'
        text_from_update = f' of {update_info}'
        if self.animate:
            self.bitc.draw.push_print(f'{update_info} starting')
            self.bitc.draw.push(self.bitc, TreeType.UpdateTree, BitRuPq.draw_update_tree, f'{update_info} starting')
            self.biti.draw.push(self.biti, TreeType.UpdateTree, BitRuPq.draw_update_tree, f'{update_info} starting')

        if 1 <= left <= right <= self.size:
            spaces = 4 * ' '
            self.bitc.updater(left, right, val, text_from_update, 'bitc', spaces)
            self.biti.updater(left, right, -val * (left - 1), text_from_update, 'biti', spaces)
            self.biti.updater(right + 1, self.size, val * (right - left + 1), text_from_update, 'biti', spaces)
        elif self.animate:
            self.bitc.draw.push_print(f'    invalid interval, updating nothing')
            self.bitc.draw.push(self.bitc, TreeType.UpdateTree, BitRuPq.draw_update_tree, f'{update_info} got invalid interval')

        if self.animate:
            self.bitc.draw.push_print(f'{update_info} finished')
            self.bitc.draw.push(self.bitc, TreeType.UpdateTree, BitRuPq.draw_update_tree, f'{update_info} finished')
            self.biti.draw.push(self.biti, TreeType.UpdateTree, BitRuPq.draw_update_tree, f'{update_info} finished')

    def init(self, values: list, animate = True):
        """
        Initialize whole BIT with array of integers

        Returns:    initialized BitRuRq instance
        """
        self = BitRuRq(len(values), animate)
        if self.animate:
            self.bitc.draw.push_print("init({})".format(values))
        for idx, elem in enumerate(values):
            self.update(idx + 1, idx + 1, elem)
        return self

    def clone(self):
        """
        Copy a separate instance of itself, to keep the object state except for canvas

        Returns:    copy of self
        """
        duplicate = copy(self)
        duplicate.bitc = self.bitc.clone()
        duplicate.biti = self.biti.clone()
        return duplicate

    def query(self, idx: int) -> int:
        """
        Operation of range query as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= idx <= size

        Args:
            idx:    index determining which element should be updated

        Returns:    cumulative frequency at the given index
        """

        # a, b are not very descriptive names, however we use the same notation
        # as is used in the thesis
        query_info = f'query({idx})'
        text_from_query = f' of {query_info}'

        if self.animate:
            self.bitc.draw.push_print(f'{query_info} starting')
            self.bitc.draw.push(self.bitc, TreeType.QueryTree, BitRuPq.draw_query_tree,
                                f'{query_info} starting')

        if 1 <= idx <= self.size:
            a = self.bitc.queryp(idx, text_from_query, 'a', 'bitc')
            b = self.biti.queryp(idx, text_from_query, 'b', 'biti')
            cumul_freq = a * idx + b
        elif self.animate:
            self.bitc.draw.push_print(f'    out of range, querying nothing')
            self.bitc.draw.push_print(f'    {query_info} = 0')
            self.bitc.draw.push_print(f'{query_info} finished')
            self.bitc.draw.push(self.bitc, TreeType.QueryTree, BitRuPq.draw_query_tree,
                                f'{query_info} out of range')
            self.bitc.draw.push(self.bitc, TreeType.QueryTree, BitRuPq.draw_query_tree,
                                f'{query_info} finished, result = 0')
            return 0

        if self.animate:
            # if self.animate and not 1 <= idx <= self.size, we are returning 0, so we never get here
            self.bitc.draw.push_print(f'    {query_info} = a * {idx} + b = {a} * {idx} + {b} = {cumul_freq}')
            self.bitc.draw.push_print(f'{query_info} finished')
            self.bitc.draw.push(self.bitc, TreeType.QueryTree, BitRuPq.draw_query_tree,
                                f'{query_info} finished, result = {a}*{idx} + {b} = {cumul_freq}')
        return cumul_freq


    def print_structure(self):
        """
        Helper method for user to see the content of two internal trees: bitc and biti.

        Returns:    nothing is returned, mentioned tree content with corresponding names is printed into console
        """
        self.bitc.print_tree()
        self.biti.print_tree()


    def get_single_freq(self, idx: int) -> Tuple[int,int]:
        """
        Operation of finding the values of single frequencies from subordinate BITs.

        Defined when arguments hold the following conditions:
            1 <= idx <= size

        Args:
            idx:    index determining which element should be returned

        Returns:    true frequencies from subordinated BITs at the given index, bitc first, biti second
        """
        return self.bitc.get_single_freq(idx),self.biti.get_single_freq(idx)

    def get_single_freqs(self) -> list:
        """
        Helper method for user to see the values he/she did so far,
        i.e. virtual representation of the array, which is proper for human.

        Returns:    list of virtual frequencies tuples, also printed to console
        """
        item_freqs = [self.get_single_freq(i) for i in range(1, self.size + 1)]
        if self.animate:
            self.bitc.draw.push_print("Item frequencies: {}".format(item_freqs))
        return item_freqs

    def draw_tree(self, a_tree_type: TreeType) -> None:
        if a_tree_type is TreeType.QueryTree:
            self.bitc.draw_query_tree()
            self.biti.draw_query_tree()
        else:
            self.bitc.draw_update_tree()
            self.biti.draw_update_tree()

# Note: We suppose any argument given into any method / function lsb is the whole number.
# In addition, it also holds the conditions stated in documentation.


def demo():
    print("Queuing demo")  

    t = BitRuRq().init([1,2,3,2,3])
    t.update(1, 3, 2)
    t.update(2, 2, -3)
    t.get_single_freqs()
    t.query(1)
    t.query(2)
    t.query(5)
    t.print_structure()
    t.draw_tree(TreeType.QueryTree)
    t.draw_tree(TreeType.QueryTree)
    print("Demo queued")  

if __name__ == '__main__':
    demo()
