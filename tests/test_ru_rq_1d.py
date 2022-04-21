from bit_ru_rq_1d_decor import *

"""
Interface of 1D RU RQ BIT:
    - constructor (BitRuRq)
        - takes positive integer: size
        - returns new instance of 1D RU RQ BIT, which is able to solve range update and range query
            operations, whose range is inside interval [1,size]
        - for example: bit = BitRuRq(11)
    - range update (update)
        - takes three integers: left, right, val
        - returns nothing, but 1D RU RQ BIT, on which is operation called is updated appropriately
        - for example: bit.update(3, 7, 4)
    - range query (query)
        - takes one integer: idx
        - returns value of cumulative sum of interval [1,idx]
        - for example: bit.query(8)
"""

bit = BitRuRq(11)
bit.update(3, 7, 4)
bit.query(8)
