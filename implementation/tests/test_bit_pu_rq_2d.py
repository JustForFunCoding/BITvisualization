import unittest

from bit_pu_rq_2d import BitPuRq2d
from support_tests import get_prefix_sums_2d


class Test2dBitPuRq(unittest.TestCase):
    def test_updatep(self):
        """
        2D Point update Range query BIT: Test of updatep method
        """
        bit = BitPuRq2d(5)

        bit.updatep(4, 1, 3)
        self.assertEqual(bit.tree,
                         [
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 0, 3, 0],
                             [0, 0, 0, 0, 0, 0]
                         ])

        bit.updatep(3, 2, -5)
        self.assertEqual(bit.tree,
                         [
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, -5, 0, -5, 0],
                             [0, 3, -2, 0, -2, 0],
                             [0, 0, 0, 0, 0, 0]
                         ])

        bit.updatep(1, 3, 2)
        self.assertEqual(bit.tree,
                         [
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 2, 2, 0],
                             [0, 0, 0, 2, 2, 0],
                             [0, 0, -5, 0, -5, 0],
                             [0, 3, -2, 2, 0, 0],
                             [0, 0, 0, 0, 0, 0]
                         ])

        bit.updatep(2, 1, 4)
        self.assertEqual(bit.tree,
                         [
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 2, 2, 0],
                             [0, 4, 4, 2, 6, 0],
                             [0, 0, -5, 0, -5, 0],
                             [0, 7, 2, 2, 4, 0],
                             [0, 0, 0, 0, 0, 0]
                         ])

        bit.updatep(5, 1, 2)
        self.assertEqual(bit.tree,
                         [
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 2, 2, 0],
                             [0, 4, 4, 2, 6, 0],
                             [0, 0, -5, 0, -5, 0],
                             [0, 7, 2, 2, 4, 0],
                             [0, 2, 2, 0, 2, 0]
                         ])

        ####################
        bit = BitPuRq2d(8)

        bit.updatep(3, 1, 2)
        self.assertEqual(bit.tree,
                         [
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 0, 2, 0, 0, 0, 2],
                             [0, 2, 2, 0, 2, 0, 0, 0, 2],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 0, 2, 0, 0, 0, 2]
                         ])

        bit.updatep(5, 2, -3)
        self.assertEqual(bit.tree,
                         [
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 0, 2, 0, 0, 0, 2],
                             [0, 2, 2, 0, 2, 0, 0, 0, 2],
                             [0, 0, -3, 0, -3, 0, 0, 0, -3],
                             [0, 0, -3, 0, -3, 0, 0, 0, -3],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, -1, 0, -1, 0, 0, 0, -1]
                         ])

        bit.updatep(1, 3, 5)
        self.assertEqual(bit.tree,
                         [
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 5, 5, 0, 0, 0, 5],
                             [0, 0, 0, 5, 5, 0, 0, 0, 5],
                             [0, 2, 2, 0, 2, 0, 0, 0, 2],
                             [0, 2, 2, 5, 7, 0, 0, 0, 7],
                             [0, 0, -3, 0, -3, 0, 0, 0, -3],
                             [0, 0, -3, 0, -3, 0, 0, 0, -3],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, -1, 5, 4, 0, 0, 0, 4]
                         ])

        bit.updatep(7, 1, -3)
        self.assertEqual(bit.tree,
                         [
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 5, 5, 0, 0, 0, 5],
                             [0, 0, 0, 5, 5, 0, 0, 0, 5],
                             [0, 2, 2, 0, 2, 0, 0, 0, 2],
                             [0, 2, 2, 5, 7, 0, 0, 0, 7],
                             [0, 0, -3, 0, -3, 0, 0, 0, -3],
                             [0, 0, -3, 0, -3, 0, 0, 0, -3],
                             [0, -3, -3, 0, -3, 0, 0, 0, -3],
                             [0, -1, -4, 5, 1, 0, 0, 0, 1]
                         ])

    def test_queryr(self):
        """
        2D Point update Range query BIT: Test of queryr method
        """

        arr = [[3, 1, 4, 1, 5],
               [9, 2, 6, 5, 3],
               [5, 8, 9, 7, 9],
               [3, 2, 3, 8, 4],
               [6, 2, 6, 4, 3]]
        n = len(arr)

        bit = BitPuRq2d(n)
        for row in range(n):
            for col in range(n):
                bit.updatep(row + 1, col + 1, arr[row][col])

        # We can also check such a small instance visually by uncommenting the following line:
        # bit.print_true_freqs()
        # But it is generally bad idea, because with larger instances, this is not possible.
        # Hence, we check it with computed prefix sums.

        prefix_sums = get_prefix_sums_2d(arr)
        for row in range(n + 1):
            for col in range(n + 1):
                self.assertEqual(bit.queryr(row, col), prefix_sums[row][col])



if __name__ == "__main__":
    unittest.main()
