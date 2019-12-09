from collections import deque
import math

masses = [ 142156, 108763, 77236, 78186, 110145, 126414, 115436, 133275,
        132634, 82606, 118669, 90307, 134124, 102597, 128607, 109214, 50160,
        72539, 99033, 145334, 135409, 97525, 109865, 142319, 79027, 96924,
        72530, 85993, 109594, 115991, 107998, 112934, 85198, 112744, 129637,
        95515, 90804, 107052, 89707, 93658, 60115, 118752, 94315, 59645,
        115668, 139320, 70734, 56771, 74741, 69284, 92228, 145376, 103317,
        55143, 58370, 54873, 52424, 95392, 67892, 90858, 74693, 77363, 51496,
        79375, 71206, 103492, 94065, 72084, 144311, 67381, 129958, 86741,
        148906, 123383, 147575, 136327, 118108, 136529, 66356, 70746, 147569,
        107267, 122434, 69688, 122127, 94072, 110203, 50546, 57836, 139334,
        113240, 96729, 68516, 74635, 126951, 138948, 88312, 101477, 129730,
        93816, ]

def day11(masses):
    return sum([math.floor(x / 3.0) - 2 for x in masses])

def day12(masses):
    masses = deque(masses)
    total = 0
    while masses:
        m = masses.popleft()
        f = math.floor(m / 3.) - 2
        if f > 0:
            total += f
            masses.appendleft(f)
    return total

def test():
    assert day11(masses) == 3318632
    assert day12([14]) == 2
    assert day12([1969]) == 966
    assert day12([100756]) == 50346
    assert day12(masses) == 4975084

def main():
    print("day 1/1", day11(masses))
    print("day 1/2", day12(masses))

    test()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    args = parser.parse_args()

    main(**vars(args))
