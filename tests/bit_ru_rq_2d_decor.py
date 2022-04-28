# 2D
# Range update
# Range query


from print_support import *
from bit_ru_pq_2d_decor import *


class BitRuRq2d(BitRuPq2d):
    """
    Class representing 2D Binary indexed tree for set of operations Range update and Range query.

    Attributes:
        bitxy:      tree for counting xy term
        bitx:       tree for counting x term
        bity:       tree for counting y term
        biti:       tree for independent term (inherited)
        size:       size of the trees, which is NOT changed during the existence of the object
    """
    def __init__(self, size: int = 0, do_animate = True):
        """
        Constructor initializes all trees into the given size.

        Args:
            size:   size of the trees
        """
        self.bitx = BitRuPq2d(size, do_animate, "2", "bitx")
        self.bity = BitRuPq2d(size, do_animate, "3", "bity")
        self.biti = BitRuPq2d(size, do_animate, "4", "biti")
        super().__init__(size, do_animate, "1", "bitxy")
        self.bitxy = self

    def update(self, x1: int, y1: int, x2: int, y2: int, c: int) -> None:
        """
        Operation of update as described in the thesis.
        We use also the same notation as in the thesis.

        Defined when arguments hold the following conditions:
            1 <= x1, y1 <= size
            x1 <= y2 <= size
            y1 <= y2 <= size

        Args:
            x1:     starting row index
            y1:     starting column index
            y2:     ending row index
            y2:     ending column index
            c:      value which is added to every element inside interval given by row and column indices

        Returns:    nothing is returned, but the tree is changed appropriately
        """
        update_info = f'update({x1},{y1},{x2},{y2},{c})'
        text_from_update = f' of {update_info}'
        spaces = 4 * ' '

        if self.animate:
            self.draw.push_print(f'{update_info} starting')
            self.draw.push(self, TreeType.UpdateTree, Bit2d.draw_update_tree, None, None, c,
                           f'{update_info} starting')

        if type(x1) is not int or type(x2) is not int or type(y1) is not int or type(y2) is not int or type(c) is not int:
            if self.animate:
                self.bitxy.draw.push_print(f'{spaces}invalid format')
                self.bitxy.draw.push(self.bitxy, TreeType.UpdateTree, Bit2d.draw_update_tree, None, None, c,
                                     f'{update_info} got invalid format')
        elif 1 <= x1 <= x2 <= self.size and 1 <= y1 <= y2 <= self.size:
            spaces = 4 * ' '
            self.bitxy.updater(x1, y1, x2, y2, c, text_from_update, 'bitxy', spaces)
            self.bitx.updater(x1, y1, x2, y2, -c * (y1 - 1), text_from_update, 'bitx', spaces)
            self.bitx.updater(x1, y2 + 1, x2, self.size, c * (y2 - y1 + 1), text_from_update, 'bitx', spaces)
            self.bity.updater(x1, y1, x2, y2, -c * (x1 - 1), text_from_update, 'bity', spaces)
            self.bity.updater(x2 + 1, y1, self.size, y2, c * (x2 - x1 + 1), text_from_update, 'bity', spaces)
            self.biti.updater(x1, y1, x2, y2, c * (x1 * y1 - x1 - y1 + 1), text_from_update, 'biti', spaces)
            self.biti.updater(x2 + 1, y1, self.size, y2,
                              -c * (y1 - 1) * (x2 - x1 + 1), text_from_update, 'biti', spaces)
            self.biti.updater(x1, y2 + 1, x2, self.size,
                              -c * (x1 - 1) * (y2 - y1 + 1), text_from_update, 'biti', spaces)
            self.biti.updater(x2 + 1, y2 + 1, self.size, self.size,
                              c * (x2 - x1 + 1) * (y2 - y1 + 1), text_from_update, 'biti', spaces)
        elif self.animate:
            self.bitxy.draw.push_print(f'{spaces}invalid interval, updating nothing')
            self.bitxy.draw.push(self.bitxy, TreeType.UpdateTree, Bit2d.draw_update_tree, None, None, c,
                                 f'{update_info} got invalid interval')

        if self.animate:
            self.draw.push_print(f'{update_info} finished')
            self.draw.push(self, TreeType.UpdateTree, Bit2d.draw_update_tree, None, None, c,
                           f'{update_info} finished')

    def query(self, x: int, y: int) -> int:
        """
        Operation of range query as described in the thesis.

        Defined when argument hold the following conditions:
            1 <= x, y <= size

        Args:
            x:      ending row index
            y:      ending column index

        Returns:    cumulative frequency in the 2d subarray [1,1 : x,y]
        """
        query_info = f'query({x},{y})'
        text_from_query = f' of {query_info}'
        spaces_from_query = 4 * ' '

        if self.animate:
            self.draw.push_print(f'{query_info} starting')
            self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree, None, None, 0,
                           f'{query_info} starting')

        if type(x) is not int or type(y) is not int:
            if self.animate:
                self.bitxy.draw.push_print(f'{spaces_from_query}invalid format')
                self.bitxy.draw.push(self.bitxy, TreeType.QueryTree, Bit2d.draw_query_tree, None, None, 0,
                                     f'{query_info} got invalid format')
                self.bitxy.draw.push_print(f'{spaces_from_query}{query_info} = 0')
                self.bitxy.draw.push_print(f'{query_info} finished')
                self.bitxy.draw.push(self.bitxy, TreeType.QueryTree, Bit2d.draw_query_tree, None, None, 0,
                                     f'{query_info} finished, result = 0')
        elif 1 <= x <= self.size and 1 <= y <= self.size:
            a = self.bitxy.queryp(x, y, text_from_query, 'a', 'bitxy', spaces_from_query)
            b = self.bitx.queryp(x, y, text_from_query, 'b', 'bitx', spaces_from_query)
            c = self.bity.queryp(x, y, text_from_query, 'c', 'bity', spaces_from_query)
            d = self.biti.queryp(x, y, text_from_query, 'd', 'biti', spaces_from_query)
            res = a * x * y + b * x + c * y + d
        elif self.animate:
            self.bitxy.draw.push_print(f'{spaces_from_query}out of range, querying nothing')
            self.bitxy.draw.push_print(f'{spaces_from_query}{query_info} = 0')
            self.bitxy.draw.push(self.bitxy, TreeType.QueryTree, Bit2d.draw_query_tree, None, None, 0,
                                 f'{query_info} out of range')
            self.bitxy.draw.push_print(f'{query_info} finished')
            self.bitxy.draw.push(self.bitxy, TreeType.QueryTree, Bit2d.draw_query_tree, None, None, 0,
                                 f'{query_info} finished, result = 0')
            return 0

        if self.animate:
            # if self.animate and not (1 <= x <= self.size and 1 <= y <= self.size), we are returning 0, so we never get here
            self.draw.push_print(f'    {query_info} = a*{x}*{y} + b*{x} + c*{y} + d = {a}*{x}*{y} + {b}*{x} + {c}*{y} + {d} = {res}')
            self.draw.push_print(f'{query_info} finished')
            if d >= 0:
                self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree, None, None, 0,
                               f'{query_info} finished, result = ({a}*{x}*{y}) + ({b}*{x}) + ({c}*{y}) + {d} = {res}')
            else:
                self.draw.push(self, TreeType.QueryTree, Bit2d.draw_query_tree, None, None, 0,
                               f'{query_info} finished, result = ({a}*{x}*{y}) + ({b}*{x}) + ({c}*{y}) - {-d} = {res}')
        return res


if __name__ == '__main__':
    tst = BitRuRq2d(10)
    tst.update(1,2,3,4,5)
    print(tst.query(1,2))
    