from bit_ru_pq_2d_decor import *

"""
Interface of 2D PU RQ BIT:
    - constructor (BitRuPq2d)
        - takes one integer: size
        - creates new instance of 2D RU PQ BIT of the given size, which is able to solve
            operations range update and point query
        - for example: bit2d = BitRuPq2d(12)
    - range update (updater)
        - takes three integers: row1, col1, row2, col2 and val
        - returns nothing, but 2D PU RQ BIT, on which is updater called is modified appropriately
        - for example: bit2d.updater(1, 2, 5, 3, 42)
    - range query (queryp)
        - takes two integers: row and col
        - returns value of point query at position given by row index row and column index col
        - for example: bit2d.queryp(8, 9)
"""

bit2d = BitRuPq2d(11)
bit2d.updater(3, 4, 5, 7, 12)
bit2d.queryp(8, 11)
