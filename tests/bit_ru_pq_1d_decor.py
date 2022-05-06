# 1D
# Range update
# Point query

from print_support import *
from typing import Tuple
from copy import copy
#from pdb import set_trace

class BitRuPq:
    """
    Class representing Binary indexed tree for set of operations Range update and Point query.

    Attributes:
        tree:       internal representation of the tree
        size:       size of the tree, which is NOT changed during the existence of the object
    """
        
    def __init__(self, size: int = 0, do_animate = True, canvas = "1", name = ""):
        """
        Constructor initializes tree into array of 0s of the given size + 1.
        The reason why it's size + 1 see in bit_pu_rq_1d.py.

        Defined when arguments hold the following conditions:
            0 <= size

        Args:
            size:       given size of the tree
        """
        self.draw = CanvasDraw("canvas"+str(canvas))
        if type(size) is not int:
            self.draw.push_print(f'size has to be int')
            raise ValueError("Size has to be of type int")
        self.tree = [0] * (size + 1)
        self.size = size
        self.animate = do_animate
        self.startx = draw_settings["start_x"]
        self.starty = draw_settings["start_y"]
        self.circle_diameter = draw_settings["circle_diameter"]
        self.name = name
        if self.animate and size > 0:
            tree_name = name[:-1] if len(name) > 1 else 'bit'  # this is because RuRq gives us "bitc:"
            self.draw.push_print("{}: {}".format(tree_name, self.tree[1:]))  # we don't want to show 0th index
            self.draw.push(self, TreeType.UpdateTree, BitRuPq.draw_update_tree)
            
        if ('__BRYTHON__' in globals()):
            from browser import timer
            af = timer.request_animation_frame(animate)

    def updatep(self, idx: int, val: int, text_from_updater='', tree_name='bit', spaces_from_updater='') -> None:
        """
        Operation of point update as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= idx <= size

        Args:
            idx:                    index determining which element should be updated
            val:                    value which is added to the given index
            text_from_updater:      helper text for better visualization
            tree_name:              name of the tree printed into console
            spaces_from_updater:    helper indentation for nicer print in console

        Returns:    nothing is returned, but the tree is changed appropriately
        """
        updatep_info = f'updatep({idx},{val})'
        text_from_updatep = updatep_info + text_from_updater
        spaces = spaces_from_updater + 4 * ' '

        if self.animate:
            self.draw.push_print(f'{spaces_from_updater}{tree_name}.{updatep_info} starting')
            self.draw.push(self, TreeType.UpdateTree, BitRuPq.draw_update_tree,
                           f'{text_from_updatep} starting')

        if type(idx) is not int or type(val) is not int:
            if self.animate:
                self.draw.push_print(f'{spaces}invalid format')
                self.draw.push(self, TreeType.UpdateTree, BitRuPq.draw_update_tree,
                               f'{text_from_updatep} got invalid format')
        elif 1 <= idx <= self.size:
            while idx <= self.size:
                # draw update_tree(idx, val)
                if self.animate:
                    self.draw.push_print(f'{spaces}{tree_name}[{idx}] += {val}')
                    self.draw.push(self, TreeType.UpdateTree, BitRuPq.draw_update_tree, text_from_updatep, idx)
                # do the update
                self.tree[idx] += val
                # probably not needed
                #if self.animate:
                #    self.draw.push(self, BitRuPq.draw_update_tree, idx)
                idxold = idx
                idx = idx + lsb(idx)
                # draw link(idxold, idx)
                if self.animate:
                    self.draw.push(self, TreeType.UpdateTree, BitRuPq.draw_update_tree, text_from_updatep, idxold, idxold)
        elif self.animate:
            self.draw.push_print(f'{spaces}out of range, updating nothing')
            self.draw.push(self, TreeType.UpdateTree, BitRuPq.draw_update_tree,
                           f'{text_from_updatep} out of range', idx, idx)

        if self.animate:
            self.draw.push_print(f'{spaces_from_updater}{tree_name}.{updatep_info} finished')
            self.draw.push_print(f'{spaces_from_updater}{tree_name} after {updatep_info}: {self.tree[1:]}')
            # if we knew that this is followed by other calls to updatep we can skip this push
            self.draw.push(self, TreeType.UpdateTree, BitRuPq.draw_update_tree, f'{text_from_updatep} finished')

    def init(self, values: list, animate = True):
        """
        Initialize whole BIT with array of integers

        Returns:    initialized BitRuPq instance
        """
        self = BitRuPq(len(values), animate)
        if self.animate:
            self.draw.push_print("{}init({})".format(self.name, values))
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
        
    def updater(self, left: int, right: int, val: int, text_from_update='',
                tree_name='bit', spaces_from_udpate='') -> None:
        """
        Operation of range update as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= left <= size
            left <= right <= size

        Args:
            left:               index representing left boundary of the interval to be updated
            right:              index representing right boundary of the interval to be updated
            val:                value which is added to every element in the given interval
            text_from_update:   helper text for better visualization
            tree_name:          name of the tree printed into console
            spaces_from_udpate: helper indentation for print in console

        Returns:    nothing is returned, but the tree is changed appropriately
        """
        updater_info = f'updater({left},{right},{val})'
        text_from_updater = ' of ' + updater_info + text_from_update
        spaces = spaces_from_udpate + 4 * ' '

        if self.animate:
            self.draw.push_print(f'{spaces_from_udpate}{tree_name}.{updater_info} starting')
            self.draw.push(self, TreeType.UpdateTree, BitRuPq.draw_update_tree, f'{updater_info}{text_from_update} starting')

        if type(left) is not int or type(right) is not int or type(val) is not int:
            if self.animate:
                self.draw.push_print(f'{spaces}invalid format')
                self.draw.push(self, TreeType.UpdateTree, BitRuPq.draw_update_tree,
                               f'{updater_info}{text_from_update} got invalid format')
        elif 1 <= left <= right <= self.size:
            spaces_from_updater = spaces_from_udpate + 4 * ' '
            self.updatep(left, val, text_from_updater, tree_name, spaces_from_updater)
            self.updatep(right + 1, -val, text_from_updater, tree_name, spaces_from_updater)
        elif animate:
            self.draw.push_print(f'{spaces}invalid interval, updating nothing')
            self.draw.push(self, TreeType.UpdateTree, BitRuPq.draw_update_tree, f'{updater_info}{text_from_update} got invalid interval')

        if self.animate:
            self.draw.push_print(f'{spaces_from_udpate}{tree_name}.{updater_info} finished')
            self.draw.push(self, TreeType.UpdateTree, BitRuPq.draw_update_tree, f'{updater_info}{text_from_update} finished')

    def queryp(self, idx: int, text_from_query='', result_name='result', tree_name='bit') -> int:
        """
        Operation of range query as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= idx <= size

        Args:
            idx:                index determining which element should be updated
            text_from_query:    helper text for better visualization
            result_name:        helper text for better visualization
            tree_name:          helper text for better console print

        Returns:    cumulative frequency at the given index
        """
        cumul_freq = 0
        idx0 = idx
        queryp_info = f'queryp({idx})'
        queryp_whole_info = queryp_info + text_from_query
        spaces_from_query = 4 * ' ' if text_from_query != '' else ''
        spaces = spaces_from_query + 4 * ' '

        if self.animate:
            self.draw.push_print(f'{spaces_from_query}{tree_name}.{queryp_info} starting')
            self.draw.push_print(f'{spaces}{result_name} = 0')
            self.draw.push(self, TreeType.QueryTree, BitRuPq.draw_query_tree, f'{queryp_whole_info} starting, {result_name} := 0')

        if type(idx) is not int:
            if self.animate:
                self.draw.push_print(f'{spaces}invalid format')
                self.draw.push(self, TreeType.QueryTree, BitRuPq.draw_query_tree,
                               f'{queryp_whole_info} got invalid format')
        elif 1 <= idx <= self.size:
            while idx > 0:
                if self.animate:
                    self.draw.push_print(f'{spaces}{result_name} += {tree_name}[{idx}] (={self.tree[idx]})')
                    if self.tree[idx] >= 0:
                        self.draw.push(self, TreeType.QueryTree, BitRuPq.draw_query_tree,
                                       f'{result_name} := {result_name} + {self.tree[idx]} in {queryp_whole_info}', False, cumul_freq, idx)
                    else:
                        self.draw.push(self, TreeType.QueryTree, BitRuPq.draw_query_tree,
                                       f'{result_name} := {result_name} - {-self.tree[idx]} in {queryp_whole_info}', False, cumul_freq, idx)
                cumul_freq += self.tree[idx]
                # update cumul_freq
                idxold = idx
                # link(idxold, idx)
                idx = idx - lsb(idx)
                if self.animate:
                    if self.tree[idxold] >= 0:
                        self.draw.push(self, TreeType.QueryTree, BitRuPq.draw_query_tree,
                                       f'{result_name} := {result_name} + {self.tree[idxold]} in {queryp_whole_info}',
                                       False, cumul_freq, idxold, idx)
                    else:
                        self.draw.push(self, TreeType.QueryTree, BitRuPq.draw_query_tree,
                                       f'{result_name} := {result_name} - {-self.tree[idxold]} in {queryp_whole_info}',
                                       False, cumul_freq, idxold, idx)
        elif self.animate:
            self.draw.push_print(f'{spaces}out of range, querying nothing')
            self.draw.push(self, TreeType.QueryTree, BitRuPq.draw_query_tree,
                           f'{queryp_whole_info} out of range')

        if self.animate:
            self.draw.push_print(f'{spaces}{tree_name}.{queryp_info} = {result_name} = {cumul_freq}')
            self.draw.push_print(f'{spaces_from_query}{tree_name}.{queryp_info} finished')
            self.draw.push(self, TreeType.QueryTree, BitRuPq.draw_query_tree,
                           f'{queryp_whole_info} finished, {result_name} = {cumul_freq}', True, cumul_freq)
        return cumul_freq


    def print_tree(self) -> None:
        """
        Helper method for user to see the content of the current tree values.

        Returns:        nothing is returned, but the tree name with its content is printed into console
        """
        self.draw.push_print(self.name + " " + str(self.tree[1:]))


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
            self.draw.push(self, TreeType.QueryTree, BitRuPq.draw_query_tree, 0)
        if idx == 0:
            # always 0
            return 0

        res = self.queryp(idx)
        if self.animate:
            self.draw.push_print('{}get_single_freq({})={}'.format(self.name, idx,res))
            self.draw.push(self, TreeType.QueryTree, BitRuPq.draw_query_tree, res)
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
        item_freqs = [self.queryp(i) for i in range(1, self.size + 1)]
        if self.animate:
            self.draw.push_print("{}Item frequencies: {}".format(self.name, item_freqs))
        return item_freqs

    def draw_tree(self, a_tree_type: TreeType) -> None:
        if a_tree_type is TreeType.QueryTree:
            self.draw_query_tree()
        else:
            self.draw_update_tree()


    def draw_query_tree(self, method_info = '', last_draw = False, cumul_freq = 0, idx = None, highidx = None) -> None:
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
        self.draw.text_left(self.startx, max_y_1+3*self.circle_diameter, self.name+"RU PQ tree")
        self.draw.text_big(self.startx + 150, self.starty, method_info)
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

    def draw_update_tree(self, method_info = '', highlight = 0, highidx = None) -> None:
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
        # clear the canvas
        self.draw.cls()
        self.draw.text_left(self.startx, self.starty+3*self.circle_diameter, 'P:')
        self.draw.text_left(self.startx, max_y+3*self.circle_diameter, 'V:')
        self.draw.text_left(self.startx, max_y_1+3*self.circle_diameter, self.name+"RU PQ tree")
        self.draw.text_big(self.startx, 20, method_info)
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
            self.starty + self.get_vertex_height(idx, tree_type) * self.circle_diameter * 3 + 40  # some space so 3x


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

    t = BitRuPq().init([1,2,3])
    t.updater(2,2,3)
    t.queryp(3)
    t.get_single_freqs()
    print("Demo finished")  

if __name__ == '__main__':
    demo()
