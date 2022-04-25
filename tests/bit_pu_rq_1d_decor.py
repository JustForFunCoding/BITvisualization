# 1D    
# Point update
# Range query

from print_support import *
from typing import Tuple
from copy import copy

class BitPuRq(object):
    """
    Class for animated Binary Indexed Tree for set of operations Point update and Range query.

    Attributes:
        tree:       internal representation of the tree
        size:       size of the tree, which is NOT changed during the existence of the object
    """

    def __init__(self, size: int = 0, do_animate = True, canvas = "1", name = "bit"):
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
        self.animate = do_animate
        self.startx = draw_settings["start_x"]
        self.starty = draw_settings["start_y"]
        self.circle_diameter = draw_settings["circle_diameter"]
        self.name = name
        self.draw = CanvasDraw("canvas"+str(canvas))
        if self.animate and size > 0:
            self.draw.push_print("{}: {}".format(self.name, self.tree[1:]))  # we don't want to show 0th index
            self.draw.push(self, TreeType.UpdateTree, BitPuRq.draw_update_tree)
            
        if ('__BRYTHON__' in globals()):
            from browser import timer
            af = timer.request_animation_frame(animate)
        
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
        updatep_info = f'updatep({idx},{val})'
        tree_name = "bit"
        spaces = 4 * ' '

        if self.animate:
            self.draw.push_print(f'{tree_name}.{updatep_info} starting')
            self.draw.push(self, TreeType.UpdateTree, BitPuRq.draw_update_tree, idx, idx, f'{updatep_info} starting')

        if type(idx) is not int or type(val) is not int:
            if self.animate:
                self.draw.push_print(f'{spaces}invalid format')
                self.draw.push(self, TreeType.UpdateTree, BitPuRq.draw_update_tree, idx, idx,
                               f'{updatep_info} got invalid format')
        elif 1 <= idx <= self.size:
            while idx <= self.size:
                if self.animate:
                    self.draw.push_print(f'{spaces}{tree_name}[{idx}] += {val}')
                    self.draw.push(self, TreeType.UpdateTree, BitPuRq.draw_update_tree, idx, idx, updatep_info)
                # do the update
                self.tree[idx] += val
                # probably not needed
                #if self.animate:
                #    self.draw.push(self, BitPuRq.draw_update_tree, idx, False)
                idxold = idx
                idx = idx + lsb(idx)
                # draw link(idxold, idx)
                if self.animate:
                    self.draw.push(self, TreeType.UpdateTree, BitPuRq.draw_update_tree, idxold, idxold, updatep_info)
        elif self.animate:
            self.draw.push_print(f'{spaces}out of range, updating nothing')
            self.draw.push(self, TreeType.UpdateTree, BitPuRq.draw_update_tree, idx, idx, f'{updatep_info} out of range')

        if self.animate:
            self.draw.push_print(f'{tree_name}.{updatep_info} finished')
            self.draw.push_print(f'{tree_name} after {tree_name}.{updatep_info}: {self.tree[1:]}')
            # if we knew that this is followed by other calls to updatep we can skip this push
            self.draw.push(self, TreeType.UpdateTree, BitPuRq.draw_update_tree, idx, idx, f'{updatep_info} finished')

    def init(self, values: list, animate = True):
        """
        Initialize whole BIT with array of integers

        Returns:    nothing is returned, but the tree is changed appropriately
        """
        self = BitPuRq(len(values), animate)
        if self.animate:
            self.draw.push_print("init({})".format(values))
        for i in range(1,len(values)+1):
            self.updatep(i, values[i-1])
        return self
        
    def clone(self):
        """
        Copy a separate instance of itself, to keep the object state except for canvas

        Returns:    copy of self
        """
        duplicate = copy(self)
        duplicate.tree = self.tree[:]
        return duplicate
        
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
        idx0 = idx
        queryr_info = f'queryr({idx})'
        tree_name = "bit"
        spaces = 4 * ' '

        if self.animate:
            self.draw.push_print(f'{tree_name}.{queryr_info} starting')
            self.draw.push_print(f'{spaces}result = 0')
            self.draw.push(self, TreeType.QueryTree, BitPuRq.draw_query_tree, f'{queryr_info} starting, result := 0', 0)

        if type(idx) is not int:
            if self.animate:
                self.draw.push_print(f'{spaces}invalid format')
                self.draw.push(self, TreeType.QueryTree, BitPuRq.draw_query_tree,
                               f'{queryr_info} got invalid format')
        elif 1 <= idx <= self.size:
            while idx > 0:
                if self.animate:
                    self.draw.push_print(f'{spaces}result += {tree_name}[{idx}] (={self.tree[idx]})')
                    self.draw.push(self, TreeType.QueryTree, BitPuRq.draw_query_tree,
                                   f'result := result + {self.tree[idx]} in {queryr_info}', False, cumul_freq, idx)
                cumul_freq += self.tree[idx]
                # update cumul_freq
                idxold = idx
                # link(idxold, idx)
                idx = idx - lsb(idx)
                if self.animate:
                    self.draw.push(self, TreeType.QueryTree, BitPuRq.draw_query_tree,
                                   f'result := result + {self.tree[idx]} in {queryr_info}', False, cumul_freq, idxold, idx)
        elif self.animate:
            self.draw.push_print(f'{spaces}out of range, querying nothing')
            self.draw.push(self, TreeType.QueryTree, BitPuRq.draw_query_tree, f'{queryr_info} out of range')

        if self.animate:
            self.draw.push_print('{}{}.queryr({}) = result = {}'.format(spaces, tree_name, idx0, cumul_freq))
            self.draw.push_print(f'{tree_name}.{queryr_info} finished')
            self.draw.push(self, TreeType.QueryTree, BitPuRq.draw_query_tree,
                           f'{queryr_info} finished, result = {cumul_freq}', True, cumul_freq)
        return cumul_freq

    def get_single_freq(self, idx: int) -> int:
        """
        Operation of finding the value of single frequency as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= idx <= size

        Args:
            idx:    index determining which element should be returned

        Returns:    true frequency at the given index
        """
        if self.animate:
            self.draw.push(self, TreeType.QueryTree, BitPuRq.draw_query_tree, 0)
        if idx == 0:
            # always 0
            return 0

        predecessor, parent = idx - 1, idx - lsb(idx)
        res = self.tree[idx]
        if self.animate:
            self.draw.push(self, TreeType.QueryTree, BitPuRq.draw_query_tree, res, idx)
        while predecessor != parent:
            res -= self.tree[predecessor]
            if self.animate:
                self.draw.push(self, TreeType.QueryTree, BitPuRq.draw_query_tree, res, predecessor)
            predecessor -= lsb(predecessor)
            if self.animate:
                self.draw.push(self, TreeType.QueryTree, BitPuRq.draw_query_tree, res, predecessor)
        if self.animate:
            self.draw.push_print('get_single_freq({})={}'.format(idx,res))
            self.draw.push(self, TreeType.QueryTree, BitPuRq.draw_query_tree, res)
        return res

    def get_single_freqs(self) -> list:
        """
        Helper method for user to see the values he/she did so far,
        i.e. virtual representation of the array, which is proper for human.
        For instance, after the following operations:
            bit = BitPuRq(4)
            bit.updatep(2, 1)
            bit.updatep(4, 5),
        bit.print_single_freqs() will print to console: '0 1 0 5'.

        Returns:    list of virtual frequencies, also printed to console
        """
        item_freqs = [self.get_single_freq(i) for i in range(1, self.size + 1)]
        if self.animate:
            self.draw.push_print("Item frequencies: {}".format(item_freqs))
        return item_freqs

    def draw_tree(self, a_tree_type: TreeType) -> None:
        if a_tree_type is TreeType.QueryTree:
            self.draw_query_tree()
        else:
            self.draw_update_tree()


    def draw_query_tree(self, queryr_info = '', last_draw = False, cumul_freq = 0, idx = None, highidx = None) -> None:
        if not self.animate:
            return
        #print('DQT')
        min_x, max_y = self.get_circle_center_pos(1, TreeType.UpdateTree)
        max_y = max_y + self.circle_diameter * 3
        max_y_1 = max_y + self.circle_diameter * 3
        self.animate = False
        freqs = [0] + self.get_single_freqs()
        self.animate = True
        change = 0.7071067811865476 * self.circle_diameter # math.cos(math.pi / 4) * change
        # clear the canvas
        self.draw.cls()
        self.draw.text_left(self.startx, self.starty, 'C:')
        h_width = draw_settings['highlight_line_width']
        h_color = draw_settings['highlight_color']
        self.draw.text_left(self.startx, self.starty+3*self.circle_diameter, 'P:')
        self.draw.text_left(self.startx, max_y_1, 'V:')
        self.draw.text_big(self.startx + 150, self.starty, queryr_info)

        for i in range(self.size + 1):
            act_x, act_y = self.get_circle_center_pos(i, TreeType.QueryTree)
            if i == 0:
                self.draw.text_in_circle_h(act_x, act_y, self.circle_diameter, cumul_freq, last_draw)
            else:
                self.draw.text_in_circle_h(act_x, act_y, self.circle_diameter, self.tree[i], idx != None and i == idx)
            self.draw.text_in_circle_h(act_x, max_y_1, self.circle_diameter, freqs[i], idx != None and i == idx)
            self.draw.text_center(act_x, max_y, i)
            if i > 0:
                parent_idx = i - lsb(i)
                parent_x, parent_y = self.get_circle_center_pos(parent_idx, TreeType.QueryTree)
                if highidx != None and parent_idx == highidx and i == idx:
                    self.draw.vector_hi(parent_x + change, parent_y + change, act_x - change, act_y - change)
                else:
                    self.draw.vector(parent_x + change, parent_y + change, act_x - change, act_y - change)

    def draw_update_tree(self, highlight = 0, highidx = None, updatep_info = '') -> None:
        if not self.animate:
            return
        #print('DUT',highlight, highidx)
        end_index = self.size + 1
        min_x, max_y = self.get_circle_center_pos(1, TreeType.UpdateTree)
        max_y = max_y + self.circle_diameter * 3
        max_y_1 = max_y + self.circle_diameter * 3
        self.animate = False
        freqs = [0] + self.get_single_freqs()
        self.animate = True
        change = 0.7071067811865476 * self.circle_diameter # math.cos(math.pi / 4) * diam
        self.draw.text_big(self.startx, 20, updatep_info)
        # clear the canvas
        self.draw.cls()
        self.draw.text_left(self.startx, self.starty+3*self.circle_diameter, 'P:')
        self.draw.text_left(self.startx, max_y+3*self.circle_diameter, 'V:')
        self.draw.text_big(self.startx, 20, updatep_info)

        
        for i in range(1, self.size + 2):
            act_x, act_y = self.get_circle_center_pos(i, TreeType.UpdateTree)
            #print("D:", act_x, act_y, circle_diameter, self.bit.tree[i-1])
            if i < end_index:
                if highlight != 0 and highlight == i:
                    width = draw_settings['highlight_line_width']
                    color = draw_settings['highlight_color']
                else:
                    width = draw_settings['default_line_width'] 
                    color = draw_settings['default_color'] 
                self.draw.text_in_circle(act_x, act_y, self.circle_diameter, self.tree[i], width, color)
                self.draw.text_in_circle(act_x, max_y_1, self.circle_diameter, freqs[i], width, color)
                self.draw.text_center(act_x, max_y, i)
                # This prevents us from bad parent indices.
                # For instance, if we would have tree of size 11, then element at index 8
                # would have parent at index 16, but it's not possible because of the tree size.
                # That's why we have to pick minimum.
                parent_idx = min(i + lsb(i), end_index)
                parent_x, parent_y = self.get_circle_center_pos(parent_idx, TreeType.UpdateTree)
                if highidx != None and i == highidx:
                    self.draw.vector_hi(act_x + change, act_y - change,
                            parent_x + - change, parent_y + change)
                else:
                    self.draw.vector(act_x + change, act_y - change,
                            parent_x + - change, parent_y + change)
            else:
                self.draw.text_in_circle(act_x, act_y, self.circle_diameter, "END")
                self.draw.text_center(act_x, max_y, "END")

    def get_vertex_height(self, idx: int, tree_type: TreeType) -> int:
        if tree_type is TreeType.QueryTree:
            return bin(idx).count('1')

        # In case of update tree we have to traverse the path to END node.
        height = 0
        while idx <= self.size:
            idx += lsb(idx)
            height += 1
        return height

    def get_circle_center_pos(self, idx: int, tree_type: TreeType) -> Tuple[float, float]:
        return self.startx + (idx + 1 if tree_type is TreeType.QueryTree else idx) * self.circle_diameter * 3, \
            self.starty + self.get_vertex_height(idx, tree_type) * self.circle_diameter * 3  # some space so 3x


def parent_index(idx: int) -> int:
    if idx == 0:
        raise IndexError
    return idx - lsb(idx)


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



def demo():
    print("Starting demo")  

    t = BitPuRq().init([1,2,3])
    t.updatep(2,2)
    t.queryr(3)
    t.get_single_freqs()
    print("Demo finished")  

if __name__ == '__main__':
    demo()
