# 2D
# Point update
# Range query

from print_support import *
import copy

def draw_array(obj, method_name, row = None, col = None, frq_val = 0, clear = False, method_info = ''):
    """
    Draw values in  2d array

    Returns:    nothing is returned, 2d array is drawn to canvas
    """
    #print('DA:',obj, method_name, row, col, frq_val, clear)
    # bind the method used to get the proper value from obj tree
    to_call = getattr(obj, method_name)
    size = obj.size
    drw = obj.draw
    if clear:
        drw.cls()
    old_animate = obj.animate
    obj.animate = False
    drw.text_left(30, 20, obj.name)
    drw.text_left(100, 20, 'Val:'+str(frq_val))
    # in case we also want some submethod info
    # if row is not None and col is not None:
    #     drw.text_left(160, 20, submethod)
    drw.text_big(160, 20, method_info)
    for r in range(0, size):
        for c in range(0, size):
            val = to_call(r+1, c+1)
            drw.cell_2d(obj.startx + c * obj.box_size, obj.starty + r * obj.box_size, obj.box_size, str(val))
    if row is not None and col is not None:
        val = to_call(row, col)
        drw.cell_2d_hi(obj.startx + (col - 1) * obj.box_size, obj.starty + (row - 1) * obj.box_size, obj.box_size, str(val), True)
    obj.animate = old_animate

def lsb(num: int) -> int:
    """
    Helper function for counting least significant 1 bit of the given number.

    Args:
        num:    given number

    Returns:    lest significant 1 bit of the given number
    """
    return num & (-num)


class Bit2d(object):
    """
    Class representing 2D Binary indexed abstract tree.

    Attributes:
        tree:       internal representation of the tree
        size:       size of the tree, which is NOT changed during the existence of the object
    """
    def __init__(self, size: int = 0, do_animate = True, canvas = "1", name = ""):
        """
        Constructor initializes tree into 2d array of 0s of size (size + 1) * (size + 1).
        The reason is the same as was with 1d BITs.

        Defined when arguments hold the following conditions:
            0 <= size < 20 (for reasonable screen width)

        Args:
            size:   given size of the tree
        """
        self.tree = [[0 for _ in range(size+1)] for _ in range(size+1)]
        self.size = size
        self.draw = CanvasDraw("canvas"+str(canvas))
        self.canvas_name = canvas
        self.name = name
        self.animate = do_animate
        self.startx = draw_settings["start_x"]
        self.starty = draw_settings["start_y"]
        self.box_size = draw_settings['box_size']
        if self.animate and size > 0:
            self.draw.push_print(f'{name}:')
            self.show_table(4 * ' ')
            self.draw.push(self, TreeType.UpdateTree, Bit2d.draw_update_tree)
            
        if ('__BRYTHON__' in globals()):
            from browser import timer
            af = timer.request_animation_frame(animate)

    def clone(self):
        """
        Copy a separate instance of itself, to keep the object state except for canvas

        Returns:    copy of self
        """
        duplicate = copy.copy(self)
        duplicate.tree = copy.deepcopy(self.tree)
        return duplicate
        
    """ get tree physical array element 2d """
    def get(self, row: int, col: int):
        #print("get:",row,col)
        if row < 1 or col < 1 or row > self.size or col > self.size:
            return 0
        val = self.tree[row][col]
        # careful this should not be enabled in callbacks fetched from queue
        if self.animate:
            print("get:",row,col)
            self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree, row, col, val)
        return val
        
    def updatep(self, row: int, col: int, val: int, text_from_updater='',
                tree_name='bit', spaces_from_updater='') -> None:
        """
        Operation of point update as described in the thesis.

        Defined when arguments hold the following conditions:
            1 <= row, col <= size

        Args:
            row:                    given row index
            col:                    given column index
            val:                    value which is added to the element given by row and col indices
            text_from_updater:      helper text for better visualization
            tree_name:              helper text for better visualization
            spaces_from_updater:    for better indentation in console prints

        Returns:    nothing is returned, but the tree is changed appropriately
        """
        updatep_info = f'updatep({row},{col},{val})'
        text_from_updatep = updatep_info + text_from_updater
        spaces_from_updatep = spaces_from_updater + 4 * ' '

        if self.animate:
            self.draw.push_print(f'{spaces_from_updater}{tree_name}.{updatep_info} starting')
            self.draw.push(self, TreeType.UpdateTree, Bit2d.draw_update_tree, None, None, val,
                           f'{text_from_updatep} starting')

        if 1 <= row <= self.size and 1 <= col <= self.size:
            r = row
            while r <= self.size:
                c = col
                while c <= self.size:
                    if self.animate:
                        self.draw.push_print(f'{spaces_from_updatep}{tree_name}[{r}][{c}] += {val}')
                        self.draw.push(self, TreeType.UpdateTree, Bit2d.draw_update_tree, r, c, val,
                                       f'{text_from_updatep}')
                    self.tree[r][c] += val
                    c += lsb(c)
                r += lsb(r)
        elif self.animate:
            self.draw.push_print(f'{spaces_from_updatep} out of range, updating nothing')
            self.draw.push(self, TreeType.UpdateTree, Bit2d.draw_update_tree, None, None, val,
                           f'{text_from_updatep} out of range')

        if self.animate and self.size > 0:
            self.draw.push_print(f'{spaces_from_updater}{tree_name}.{updatep_info} finished')
            self.draw.push_print(f'{spaces_from_updater}{tree_name} after {tree_name}.{updatep_info}:')
            self.show_table(spaces_from_updater + 4 * ' ')
            # shows last updated cell, plus removes highlight
            self.draw.push(self, TreeType.UpdateTree, Bit2d.draw_update_tree, None, None, val,
                           f'{text_from_updatep} finished')

    def query_virtual(self, row: int, col: int, query_info='', result_name='result',
                      tree_name='bit', spaces='') -> int:
        """
        Operation of range/point query as described in the thesis, depends on caller.

        Defined when arguments hold the following conditions:
            1 <= row, col <= size

        Args:
            row:    given row index
            col:    given column index
            result_name:    name of the result for better visualization
            tree_name:      name of the tree for better visualization
            spaces:         indentation for nicer console prints

        Returns:    cumulative frequency on position given by row and col indices
        """
        cumul_freq = 0
        actual_info = query_info.split()[0]
        if self.animate:
            self.draw.push_print(f'{spaces}{tree_name}.{actual_info} starting')
            self.draw.push_print(f'    {spaces}{result_name} = 0')
            rowarg = row if 1 <= row <= self.size else None
            colarg = col if 1 <= col <= self.size else None
            self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree, rowarg, colarg, cumul_freq, f'{query_info} starting, {result_name} := 0')

        if 1 <= row <= self.size and 1 <= col <= self.size:
            r = row
            while r > 0:
                c = col
                while c > 0:
                    # careful this should not be enabled in callbacks fetched from queue
                    if self.animate:
                        self.draw.push_print(f'    {spaces}{result_name} += {tree_name}[{r}][{c}] (={self.tree[r][c]})')
                        self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree, r, c, cumul_freq,
                                       f'{result_name} := {result_name} + {self.tree[r][c]} in {query_info}')
                    cumul_freq += self.tree[r][c]
                    c -= lsb(c)
                r -= lsb(r)
        elif self.animate:
            self.draw.push_print(f'    {spaces}out of range, querying nothing')
            self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree, None, None, cumul_freq,
                           f'{query_info} out of range')

        if self.animate:
            self.draw.push_print(f'    {spaces}{tree_name}.{actual_info} = {result_name} = {cumul_freq}')
            self.draw.push_print(f'{spaces}{tree_name}.{actual_info} finished')
            self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree, None, None, cumul_freq,
                           f'{query_info} finished, {result_name} = {cumul_freq}')
        return cumul_freq

    def show_table(self, spaces='    '):
        "Helper method for printing into console"
        for row in self.tree[1:]:
            self.draw.push_print(f'{spaces}{row[1:]}')

    def draw_query_tree(self, row = None, col = None, cumul_freq = 0, method_info = "") -> None:
        if not self.animate:
            return
        #print('DQT',cumul_freq, row, col)
        draw_array(self, "get", row, col, cumul_freq, True, method_info)
        return
        # TODO how shall we animate query

    def draw_update_tree(self, row = None, col = None, val = 0, method_info = "") -> None:
        if not self.animate:
            return
        draw_array(self, "get", row, col, val, True, method_info)
        #print('DUT', row, col, val)
        return
        # TODO how shall we animate update

# Note: We suppose any argument given into any method / function lsb is the whole number.
# In addition, it also holds the conditions stated in documentation.
