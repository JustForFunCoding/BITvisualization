from bit_pu_rq_1d_decor import *

"""
Interface of 1D PU RQ BIT:
    - constructor (BitPuRq)
        - takes positive integer
        - returns new instance of 1D PU RQ BIT of the given size
            initialized with 0s
        - for example: bit = BitPuRq(11)
            creates 1D PU RQ BIT of size 11 initialized with 0s
    - syntactic sugar for advanced constructor (init)
        - takes array of integers
        - returns new instance of 1D PU RQ BIT of the size as the given array
            initialized with numbers of array
        - for example: bit = BitPuRq().init([3,1,4])
            creates 1D PU RQ BIT of size 3 initialized with values 3,1,4
    - point update (updatep)
        - takes two numbers: index and value
        - returns nothing, but 1D PU RQ, on which is called updatep
            is modified appropriately
        - for example: bit.updatep(3,7)  
    - range query (queryr)
        - takes one number: index
        - returns the value of rsum(bit[1:index])
        - for example: bit.queryr(5)
"""

bit = BitPuRq(11)
bit.queryr(7)
bit.updatep(5, 3)
bit.queryr(7)
