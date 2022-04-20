from bit_ru_rq_2d_decor import *

"""
Interface of 2D RU RQ BIT:
    - constructor (BitRuRq2d)
        - takes one integer: size of the 2D RU RQ BIT
        - creates new instance of 2D RU RQ BIT of the given size,
            which is able to solve operations range update and range query
        - for example: bit2d = BitRuRq2d(10)
    - range update (update)
        - takes five integers:
            - row1 - starting row index
            - col1 - starting column index
            - row2 - ending row index
            - col2 - ending column index
            - val  - given constant
        - returns nothing, but 2D RU RQ BIT, on which is update called
            is modified appropriately
        - for example: bit2d.update(3, 4, 7, 5, 21)
    - range query (query)
        - takes two integers:
            - row - ending row index
            - col - ending column index
        - returns cumulative sum of [1,1 : row,col]
        - for example: bit2d.query(5, 6)
"""

bit2d = BitRuRq2d(10)
bit2d.update(3, 2, 7, 10, 5)
bit2d.query(8, 5)
