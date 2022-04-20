import unittest

from bit_ru_pq_1d import BitRuPq


class Test1dBitRuPq(unittest.TestCase):
    def test_updatep(self):
        """
        1D Range update Point query BIT: Test of updatep method
        """

        bit = BitRuPq(4)

        bit.updatep(1, 4)
        self.assertEqual(bit.tree, [0, 4, 4, 0, 4])

        bit.updatep(3, 2)
        self.assertEqual(bit.tree, [0, 4, 4, 2, 6])

        bit.updatep(4, -2)
        self.assertEqual(bit.tree, [0, 4, 4, 2, 4])

        # Method is undefined here, but in this undefined scenario it has no impact.
        bit.updatep(100, 10)
        self.assertEqual(bit.tree, [0, 4, 4, 2, 4])

        bit.updatep(2, -3)
        self.assertEqual(bit.tree, [0, 4, 1, 2, 1])

        ####################

        bit = BitRuPq(12)

        bit.updatep(3, 2)
        self.assertEqual(bit.tree, [0, 0, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0])

        bit.updatep(5, -3)
        self.assertEqual(bit.tree, [0, 0, 0, 2, 2, -3, -3, 0, -1, 0, 0, 0, 0])

        bit.updatep(9, 4)
        self.assertEqual(bit.tree, [0, 0, 0, 2, 2, -3, -3, 0, -1, 4, 4, 0, 4])

        bit.updatep(6, 3)
        self.assertEqual(bit.tree, [0, 0, 0, 2, 2, -3, 0, 0, 2, 4, 4, 0, 4])

        bit.updatep(7, 5)
        self.assertEqual(bit.tree, [0, 0, 0, 2, 2, -3, 0, 5, 7, 4, 4, 0, 4])

        bit.updatep(11, 3)
        self.assertEqual(bit.tree, [0, 0, 0, 2, 2, -3, 0, 5, 7, 4, 4, 3, 7])

    def test_updater(self):
        """
        1D Range update Point query BIT: Test of updater method
        """
        bit = BitRuPq(5)

        bit.updater(2, 3, 2)
        self.assertEqual(bit.tree, [0, 0, 2, 0, 0, 0])

        bit.updater(3, 5, -3)
        self.assertEqual(bit.tree, [0, 0, 2, -3, -3, 0])

        bit.updater(3, 4, 1)
        self.assertEqual(bit.tree, [0, 0, 2, -2, -2, -1])

        bit.updater(1, 1, 3)
        self.assertEqual(bit.tree, [0, 3, 2, -2, -2, -1])

        ####################

        bit = BitRuPq(8)

        bit.updater(1, 4, 3)
        self.assertEqual(bit.tree, [0, 3, 3, 0, 3, -3, -3, 0, 0])

        bit.updater(3, 6, -2)
        self.assertEqual(bit.tree, [0, 3, 3, -2, 1, -3, -3, 2, 0])

        bit.updater(2, 5, 1)
        self.assertEqual(bit.tree, [0, 3, 4, -2, 2, -3, -4, 2, 0])

        bit.updater(5, 8, 3)
        self.assertEqual(bit.tree, [0, 3, 4, -2, 2, 0, -1, 2, 3])

    def test_queryr(self):
        """
        1D Range update Point query BIT: Test of queryr method
        """
        bit = BitRuPq(12)

        arr = [2, 7, 1, 8, 2, 8, 1, 8, 2, 8, 4, 5]
        for idx, elem in enumerate(arr):
            bit.updater(idx + 1, idx + 1, elem)

        for idx in range(len(arr)):
            self.assertEqual(bit.queryp(idx + 1), arr[idx])


if __name__ == "__main__":
    unittest.main()
