import unittest

from bit_pu_rq_1d import BitPuRq
from support_tests import get_prefix_sums


class Test1dBitPuRq(unittest.TestCase):
    def test_updatep(self):
        """
        1D Point update Range query BIT: Test of updatep method
        """
        bit = BitPuRq(8)

        bit.updatep(1, 3)
        self.assertEqual(bit.tree, [0, 3, 3, 0, 3, 0, 0, 0, 3])

        bit.updatep(5, -2)
        self.assertEqual(bit.tree, [0, 3, 3, 0, 3, -2, -2, 0, 1])

        bit.updatep(10, 10)
        self.assertEqual(bit.tree, [0, 3, 3, 0, 3, -2, -2, 0, 1])

        bit.updatep(3, 0)
        self.assertEqual(bit.tree, [0, 3, 3, 0, 3, -2, -2, 0, 1])

        bit.updatep(6, 5)
        self.assertEqual(bit.tree, [0, 3, 3, 0, 3, -2, 3, 0, 6])

        bit.updatep(7, 4)
        self.assertEqual(bit.tree, [0, 3, 3, 0, 3, -2, 3, 4, 10])

        ####################
        bit = BitPuRq(5)

        bit.updatep(1, 2)
        self.assertEqual(bit.tree, [0, 2, 2, 0, 2, 0])

        bit.updatep(2, 3)
        self.assertEqual(bit.tree, [0, 2, 5, 0, 5, 0])

        bit.updatep(5, 1)
        self.assertEqual(bit.tree, [0, 2, 5, 0, 5, 1])

    def test_queryr(self):
        """
        1D Point update Range query BIT: Test of queryr method
        """
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        n = len(arr)
        bit = BitPuRq(11)

        for idx, elem in enumerate(arr):
            bit.updatep(idx + 1, elem)

        prefix_sums = get_prefix_sums(arr)
        # The virtual representation of operations is as in arr
        for idx in range(n + 1):
            self.assertEqual(bit.queryr(idx), prefix_sums[idx])

        ####################
        bit = BitPuRq(5)

        bit.updatep(1, 1)
        bit.updatep(2, -2)
        bit.updatep(3, 5)
        bit.updatep(4, 3)
        bit.updatep(5, -4)

        self.assertEqual(bit.queryr(1), 1)
        self.assertEqual(bit.queryr(2), -1)
        self.assertEqual(bit.queryr(3), 4)
        self.assertEqual(bit.queryr(4), 7)
        self.assertEqual(bit.queryr(5), 3)


if __name__ == "__main__":
    unittest.main()
