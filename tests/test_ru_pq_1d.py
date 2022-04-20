from bit_ru_pq_1d_decor import *

"""
Interface of 1D RU PQ BIT:
    - constructor (BitRuPq)
        - takes positive integer
        - returns new instance of 1D RU PQ BIT of the given size
            initialized with 0s
        - for example: bit = BitRuPq(10)
            creates 1D RU PQ BIT of size initialized with 0s
    - range update (updater)
        - takes three integers: left, right, val
        - returns nothing, but 1D RU PQ BIT, on which is called updater
            is modified appropriately
        - for example: bit.updater(4,7,3)
    - point query (queryp)
        - takes one positive integer: idx
        - returns the value of point query at index idx
        - for example: bit.queryp(3)
"""

bit = BitRuPq(11)
bit.updater(3, 8, 5)
bit.queryp(7)
bit.queryp(10)
