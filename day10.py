import math
from intcode import Intcode

VERBOSE = False

THE_BITMAP = """
.###..#......###..#...#
#.#..#.##..###..#...#.#
#.#.#.##.#..##.#.###.##
.#..#...####.#.##..##..
#.###.#.####.##.#######
..#######..##..##.#.###
.##.#...##.##.####..###
....####.####.#########
#.########.#...##.####.
.#.#..#.#.#.#.##.###.##
#..#.#..##...#..#.####.
.###.#.#...###....###..
###..#.###..###.#.###.#
...###.##.#.##.#...#..#
#......#.#.##..#...#.#.
###.##.#..##...#..#.#.#
###..###..##.##..##.###
###.###.####....######.
.###.#####.#.#.#.#####.
##.#.###.###.##.##..##.
##.#..#..#..#.####.#.#.
.#.#.#.##.##########..#
#####.##......#.#.####.
"""

def load(txt):
    lines = []
    for line in txt.splitlines():
        line = line.strip()
        if not line:
            continue
        lines.append(list(None if x == "." else x for x in line))
    return lines

def count_chars(lines, what="#"):
    if not lines:
        return 0
    if isinstance(lines, str):
        return lines.count(what)
    return sum(line.count(what) for line in lines)

def iter_chars(lines, what="#"):
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == what:
                yield (x, y)

def add(v1, v2):
    return tuple(a+b for a, b in zip(v1, v2))

def smul(v, f):
    return tuple(x*f for x in v)

def iter_in_circles():
    dist = 1

    while True:
        pt = (dist, 0)
        while pt[0] > 0:
            yield dist, pt
            pt = add(pt, (-1, 1))

        while pt[1] > 0:
            yield dist, pt
            pt = add(pt, (-1, -1))

        while pt[0] < 0:
            yield dist, pt
            pt = add(pt, (1, -1))

        while pt[1] < 0:
            yield dist, pt
            pt = add(pt, (1, 1))

        dist += 1


def iter_in_circles_on_map(lines, start):
    last_dist = 1
    one_on_map = False
    for dist, d in iter_in_circles():
        if dist != last_dist:
            if not one_on_map:
                break
            one_on_map = False
            last_dist = dist
        pt = add(d, start)
        onm = False
        if pt[0] < 0:
            continue
        if pt[1] < 0:
            continue
        if pt[1] >= len(lines):
            continue
        if pt[0] >= len(lines[pt[1]]):
            continue
        one_on_map = True
        yield d, pt

def c_at(lines, pt):
    return lines[pt[1]][pt[0]]

def find_visible(lines, start, what="#"):
    visible = set()
    visible_d = set()

    def norm_d(d):
        gcd = math.gcd(*d)
        d = tuple(x//gcd for x in d)
        return d

    def add_meteor_at_dist(d):
        visible_d.add(norm_d(d))

    def is_hidden(d):
        # it's implicitly granted that |d| >= |dd| since iter_in_circles()
        # produces monotonically increasing distances
        # also, we'll never see d = (0, 0)
        return norm_d(d) in visible_d

    for d, pt in iter_in_circles_on_map(lines, start):
        if c_at(lines, pt) == what:
            if is_hidden(d):
                continue
            visible.add(pt)

            # find normed distance vector
            add_meteor_at_dist(d)

    if VERBOSE:
        img = []
        for y in range(len(lines)):
            line = []
            for x in range(len(lines[y])):
                pt = (x, y)
                if pt == start:
                    line.append("+")
                elif pt in visible:
                    line.append("#")
                else:
                    line.append(".")
            img.append("".join(line))

        oimg = []
        for y, line in enumerate(lines):
            line = [("+" if (x,y) == start else (c or ".")) for x, c in enumerate(line)]
            oimg.append("".join(line))

        dimg = []
        for l0, l1 in zip(oimg, img):
            line = []
            for c0, c1 in zip(l0, l1):
                if c0 != c1:
                    line.append("+")
                else:
                    line.append(".")
            dimg.append("".join(line))

        cimg = []
        for l0, l1, l2  in zip(oimg, img, dimg):
            line = l0 + "  " + l1 + "  " + l2
            cimg.append(line)
        print("-" * len(lines[0]))
        print("count=%s at pos=%s" % (len(visible), start))
        print("\n".join(cimg))
        print("-" * len(lines[0]))

    return len(visible)

def find_best_pos(txt, meteorite="#"):
    bm = load(txt)
    max_n = 0
    pos = None
    n = find_visible(bm, (5,8), meteorite)
    for p in iter_chars(bm, meteorite):
        n = find_visible(bm, p, meteorite)
        if n > max_n:
            max_n = n
            pos = p
    return (max_n, pos)

def test():
    it = iter_in_circles()
    # d = 1
    assert next(it) == (1, (1, 0))
    assert next(it) == (1, (0, 1))
    assert next(it) == (1, (-1, 0))
    assert next(it) == (1, (0, -1))
    # d = 2
    assert next(it) == (2, (2, 0))
    assert next(it) == (2, (1, 1))
    assert next(it) == (2, (0, 2))
    assert next(it) == (2, (-1, 1))
    assert next(it) == (2, (-2, 0))
    assert next(it) == (2, (-1, -1))
    assert next(it) == (2, (0, -2))
    assert next(it) == (2, (1, -1))
    # d = 3
    assert next(it) == (3, (3, 0))
    assert next(it) == (3, (2, 1))
    assert next(it) == (3, (1, 2))
    assert next(it) == (3, (0, 3))
    assert next(it) == (3, (-1, 2))
    assert next(it) == (3, (-2, 1))
    assert next(it) == (3, (-3, 0))
    assert next(it) == (3, (-2, -1))

    txt = """
.....
.....
.....
.....
.....
"""
    bm = load(txt)
    it = iter_in_circles_on_map(bm, (2,2))
    seen = set([(2,2)])
    def addsecond(x):
        seen.add(x[1])
        return x
    # d = 1
    assert next(it) == addsecond(((1, 0), (3, 2)))
    assert next(it) == addsecond(((0, 1), (2, 3)))
    assert next(it) == addsecond(((-1, 0), (1, 2)))
    assert next(it) == addsecond(((0, -1), (2, 1)))
    # d = 2
    assert next(it) == addsecond(((2, 0), (4, 2)))
    assert next(it) == addsecond(((1, 1), (3, 3)))
    assert next(it) == addsecond(((0, 2), (2, 4)))
    assert next(it) == addsecond(((-1, 1), (1, 3)))
    assert next(it) == addsecond(((-2, 0), (0, 2)))
    assert next(it) == addsecond(((-1, -1), (1, 1)))
    assert next(it) == addsecond(((0, -2), (2, 0)))
    assert next(it) == addsecond(((1, -1), (3, 1)))
    # d = 3
    assert next(it) == addsecond(((2, 1), (4, 3)))
    assert next(it) == addsecond(((1, 2), (3, 4)))
    assert next(it) == addsecond(((-1, 2), (1, 4)))
    assert next(it) == addsecond(((-2, 1), (0, 3)))
    assert next(it) == addsecond(((-2, -1), (0, 1)))
    assert next(it) == addsecond(((-1, -2), (1, 0)))
    assert next(it) == addsecond(((1, -2), (3, 0)))
    assert next(it) == addsecond(((2, -1), (4, 1)))
    # d = 4
    assert next(it) == addsecond(((2, 2), (4, 4)))
    assert next(it) == addsecond(((-2, 2), (0, 4)))
    assert next(it) == addsecond(((-2, -2), (0, 0)))
    assert next(it) == addsecond(((2, -2), (4, 0)))

    for y in range(len(bm)):
        for x in range(len(bm[0])):
            assert (x, y) in seen

    txt = """
.#..#
.....
#####
....#
...##
"""
    assert find_best_pos(txt) == (8, (3, 4))

    txt = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""
    assert find_best_pos(txt) == (33, (5,8))

    txt = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""
    assert find_best_pos(txt) == (35, (1,2))

    txt = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""
    assert find_best_pos(txt) == (41, (6,3))

    txt = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
    assert find_best_pos(txt) == (210, (11,13))

    assert find_best_pos(THE_BITMAP) == (230, (19,11))


def main():
    print("day 10/1", find_best_pos(THE_BITMAP))

    print("day 10/2")

    test()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    args = parser.parse_args()

    main(**vars(args))
