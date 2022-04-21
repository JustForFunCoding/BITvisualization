from bit_pu_rq_2d_decor import *

"""
Interface of 2D PU RQ BIT:
    - constructor (BitPuRq2d)
        - takes one integer: size
        - creates new instance of 2D PU RQ BIT of the given size, which is able to solve
            operations point update and range query
        - for example: bit2d = BitPuRq2d(8)
    - point update (updatep)
        - takes three integers: row, col and val
        - returns nothing, but 2D PU RQ BIT, on which is updatep called is modified appropriately
        - for example: bit2d.updatep(3, 7, 12)
    - range query (queryr)
        - takes two integers: row and col
        - returns rsum(bit2d[1,1 : row,col])
        - for example: bit2d.queryr(7, 4)
"""

bit2d = BitPuRq2d(10)
bit2d.updatep(3, 4, 5)
bit2d.queryr(5, 7)
