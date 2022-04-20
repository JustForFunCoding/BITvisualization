"""
Helper module for testing of query operations.

Let's imagine the following situation:
We have got some array and created from this array BIT.
Now we want to find out whether this tree correctly responds to queries.

Let's say our array is: [3, 1, 4, 1, 5].
Correct BIT should respond correctly, e.g. for range query of index 3, it should return 8, since 8 = 3 + 1 + 4.

In order to test whether BIT responded correctly, we have to check it,
e.g. range query of index 3 == sum of subarray from ending at index 3, which would cost O(n).

However, if we would want to check query for every index this way, we spend n * O(n) = O(n^2) time,
which is clearly suboptimal.

That's when prefix sums comes in.
We create prefix sum for index (k+1) from knowledge of prefix sum for index k:
prefix_sum[k+1] = prefix_sum[k] + <value of (k+1)th element in the array>
By this manner, we compute prefix sums for all indices in O(n), instead of O(n^2) !!
So it's enough to just compute all prefix sums and then use this information.
"""
from typing import List


def get_prefix_sums(arr: List[int]) -> List[int]:
    """
    Function computes prefix sums for the given array.

    Args:
        arr:    given array

    Returns:    array of prefix sums
                prefix_sums[idx] = rsum(arr[0 : idx-1])
    """
    prefix_sums = [0]
    for elem in arr:
        prefix_sums.append(prefix_sums[-1] + elem)
    return prefix_sums


def get_prefix_sums_2d(arr: List[List[int]]) -> List[List[int]]:
    """
    Function computes prefix sums for the given 2d array.

    Args:
        arr:    given 2d array

    Returns:    2d array of prefix sums
                prefix_sums[row][col] = rsum(arr[0, 0 : row-1, col-1])
    """
    n = len(arr)
    prefix_sums = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    for row in range(1, n + 1):
        for col in range(1, n + 1):
            # To compute new cell, we'll use inclusion - exclusion principle
            prefix_sums[row][col] = arr[row - 1][col - 1] +\
                                    prefix_sums[row - 1][col] +\
                                    prefix_sums[row][col - 1] -\
                                    prefix_sums[row - 1][col - 1]
    return prefix_sums
