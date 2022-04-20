from typing import List


class BIT2d:
    def __init__(self, size_y: int, size_x: int) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.tree = [[0 for _ in range(size_x)] for _ in range(size_y)]

    def point_update(self, y: int, xx: int, val: int) -> None:
        while y < self.size_y:
            x = xx
            while x < self.size_x:
                self.tree[y][x] += val
                x += LSB(x)
            y += LSB(y)

    def range_query(self, y: int, xx: int) -> int:
        s: int = 0
        while y > 0:
            x = xx
            while x > 0:
                s += self.tree[y][x]
                x -= LSB(x)
            y -= LSB(y)
        return s

    def show_tree(self) -> None:
        for row in self.tree:
            for elem in row:
                print(elem, end='\t')
            print()


def LSB(num: int) -> int:
    return num & (-num)


A = [[0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 3, 1, 3, 2, 0],
     [0, 2, 1, 0, 1, 2, 2, 0],
     [0, 3, 0, 1, 3, 1, 1, 3],
     [0, 2, 1, 8, 1, 3, 2, 5],
     [0, 1, 4, 2, 1, 0, 0, 4],
     [0, 0, 2, 0, 0, 0, 1, 0],
     [0, 0, 0, 1, 3, 1, 0, 2]]


def build_tree(A: List[List[int]]) -> BIT2d:
    ny = len(A)
    nx = len(A[0])
    t: BIT2d = BIT2d(ny, nx)
    for y in range(1, ny):
        for x in range(1, nx):
            t.point_update(y, x, A[y][x])

    return t


def rsum(A: List[List[int]], ny: int, nx: int) -> int:
    s = 0
    for y in range(ny + 1):
        for x in range(nx + 1):
            s += A[y][x]
    return s


def test_query(tree: BIT2d, A: List[List[int]]) -> bool:
    print("** test_query **")
    for y in range(tree.size_y):
        for x in range(tree.size_x):
            got = tree.range_query(y, x)
            expected = rsum(A, y, x)
            if got != expected:
                print("\tnok: y={},x={}, got={}, expected={}"
                      .format(y, x, got, expected))
                return False
    print("\tok")
    return True


if __name__ == '__main__':
    t = build_tree(A)
    t.show_tree()
    # test_query(t, A)
