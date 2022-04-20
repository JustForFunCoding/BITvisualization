# 2D
# Range update
# Range query


from bit_ru_pq_2d import BitRuPq2d


class BitRuRq2d:
    """
    Class representing 2D Binary indexed tree for set of operations Range update and Range query.

    Attributes:
        bitxy:      tree for counting xy term
        bitx:       tree for counting x term
        bity:       tree for counting y term
        biti:       tree for independent term
        size:       size of the trees, which is NOT changed during the existence of the object
    """
    def __init__(self, size: int):
        """
        Constructor initializes all trees into the given size.

        Args:
            size:   size of the trees
        """
        self.bitxy = BitRuPq2d(size)
        self.bitx = BitRuPq2d(size)
        self.bity = BitRuPq2d(size)
        self.biti = BitRuPq2d(size)
        self.size = size

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
        self.bitxy.updater(x1, y1, x2, y2, c)
        self.bitx.updater(x1, y1, x2, y2, -c * (y1 - 1))
        self.bitx.updater(x1, y2 + 1, x2, self.size, c * (y2 - y1 + 1))
        self.bity.updater(x1, y1, x2, y2, -c * (x1 - 1))
        self.bity.updater(x2 + 1, y1, self.size, y2, c * (x2 - x1 + 1))
        self.biti.updater(x1, y1, x2, y2, c * (x1 * y1 - x1 - y1 + 1))
        self.biti.updater(x2 + 1, y1, self.size, y2,
                          -c * (y1 - 1) * (x2 - x1 + 1))
        self.biti.updater(x1, y2 + 1, x2, self.size,
                          -c * (x1 - 1) * (y2 - y1 + 1))
        self.biti.updater(x2 + 1, y2 + 1, self.size, self.size,
                          c * (x2 - x1 + 1) * (y2 - y1 + 1))

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
        a = self.bitxy.queryp(x, y)
        b = self.bitx.queryp(x, y)
        c = self.bity.queryp(x, y)
        d = self.biti.queryp(x, y)
        return a * x * y + b * x + c * y + d


def lsb(num: int) -> int:
    """
    Helper function for counting least significant 1 bit of the given number.

    Args:
        num:    given number

    Returns:    lest significant 1 bit of the given number
    """
    return num & (-num)
