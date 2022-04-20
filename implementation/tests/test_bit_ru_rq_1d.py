import unittest

from bit_ru_rq_1d import BitRuRq
from support_tests import get_prefix_sums


class Test1dBitRuRq(unittest.TestCase):
    def test_update(self):
        """
        1D Range update Range query BIT: Test of update method
        """

        bit = BitRuRq(5)

        bit.update(1, 3, 2)
        # updater(bitc, 1, 3, 2)
        #   bitc: [0, 2, 2, 0, 0, 0]
        # updater(biti, 1, 3, -2 * (1 - 1) = 0)
        #   biti: [0, 0, 0, 0, 0, 0]
        # updater(biti, 4, 5, 2 * (3 - 1 + 1) = 6)
        #   biti: [0, 0, 0, 0, 6, 0]
        self.assertEqual(bit.bitc.tree, [0, 2, 2, 0, 0, 0])
        self.assertEqual(bit.biti.tree, [0, 0, 0, 0, 6, 0])

        bit.update(2, 2, -3)
        # updater(bitc, 2, 2, -3)
        #   bitc: [0, 2, -1, 3, 0, 0]
        # updater(biti, 2, 2, -(-3) * (2 - 1) = 3)
        #   biti: [0, 0, 3, -3, 6, 0]
        # updater(biti, 3, 5, -3 * (2 - 2 + 1) = -3)
        #   biti: [0, 0, 3, -6, 3, 0]
        self.assertEqual(bit.bitc.tree, [0, 2, -1, 3, 0, 0])
        self.assertEqual(bit.biti.tree, [0, 0, 3, -6, 3, 0])

        bit.update(1, 4, 5)
        # updater(bitc, 1, 3, 5)
        #   bitc: [0, 7, 4, 3, 5, -5]
        # updater(biti, 1, 3, -5 * (1 - 1) = 0)
        #   biti: [0, 0, 3, -6, 3, 0]
        # updater(biti, 5, 5, 5 * (4 - 1 + 1) = 20)
        #   biti: [0, 0, 3, -6, 3, 20]
        self.assertEqual(bit.bitc.tree, [0, 7, 4, 3, 5, -5])
        self.assertEqual(bit.biti.tree, [0, 0, 3, -6, 3, 20])

        ####################
        bit = BitRuRq(11)

        bit.update(6, 8, 3)
        # updater(bitc, 6, 8, 3)
        #   bitc: [0, 0, 0, 0, 0, 0, 3, 0, 3, -3, -3, 0]
        # updater(biti, 6, 8, -3 * (6 - 1) = -15)
        #   biti: [0, 0, 0, 0, 0, 0, -15, 0, -15, 15, 15, 0]
        # updater(biti, 9, 11, 3 * (8 - 6 + 1) = 9)
        #   biti: [0, 0, 0, 0, 0, 0, -15, 0, -15, 24, 24, 0]
        self.assertEqual(bit.bitc.tree, [0, 0, 0, 0, 0, 0, 3, 0, 3, -3, -3, 0])
        self.assertEqual(bit.biti.tree, [0, 0, 0, 0, 0, 0, -15, 0, -15, 24, 24, 0])

        bit.update(1, 5, 2)
        # updater(bitc, 1, 5, 2)
        #   bitc: [0, 2, 2, 0, 2, 0, 1, 0, 3, -3, -3, 0]
        # updater(biti, 1, 5, -2 * (1 - 1) = 0)
        #   biti: [0, 0, 0, 0, 0, 0, -15, 0, -15, 24, 24, 0]
        # updater(biti, 6, 11, 2 * (5 - 1 + 1) = 10)
        #   biti: [0, 0, 0, 0, 0, 0, -5, 0, -5, 24, 24, 0]
        self.assertEqual(bit.bitc.tree, [0, 2, 2, 0, 2, 0, 1, 0, 3, -3, -3, 0])
        self.assertEqual(bit.biti.tree, [0, 0, 0, 0, 0, 0, -5, 0, -5, 24, 24, 0])

        bit.update(3, 9, 2)
        # updater(bitc, 3, 9, 2)
        #   bitc: [0, 2, 2, 2, 4, 0, 1, 0, 5, -3, -5, 0]
        # udpater(biti, 3, 9, -2 * (3 - 1) = -4)
        #   biti: [0, 0, 0, -4, -4, 0, -5, 0, -9, 24, 28, 0]
        # updater(biti, 10, 11, 2 * (9 - 3 + 1) = 14)
        #   biti: [0, 0, 0, -4, -4, 0, -5, 0, -9, 24, 42, 0]
        self.assertEqual(bit.bitc.tree, [0, 2, 2, 2, 4, 0, 1, 0, 5, -3, -5, 0])
        self.assertEqual(bit.biti.tree, [0, 0, 0, -4, -4, 0, -5, 0, -9, 24, 42, 0])

    def test_query(self):
        """
        1D Range update Range query BIT: Test of query method
        """
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        n = len(arr)
        bit = BitRuRq(n)

        for idx, elem in enumerate(arr):
            bit.update(idx + 1, idx + 1, elem)

        prefix_sums = get_prefix_sums(arr)
        for idx in range(1, n + 1):
            self.assertEqual(bit.query(idx), prefix_sums[idx])

        ####################
        bit = BitRuRq(5)

        bit.update(1, 1, 1)
        bit.update(2, 2, -2)
        bit.update(3, 3, 5)
        bit.update(4, 4, 3)
        bit.update(5, 5, -4)

        self.assertEqual(bit.query(1), 1)
        self.assertEqual(bit.query(2), -1)
        self.assertEqual(bit.query(3), 4)
        self.assertEqual(bit.query(4), 7)
        self.assertEqual(bit.query(5), 3)



if __name__ == "__main__":
    unittest.main()
