import itertools

LEN = 6
RANGE = (146810, 612564)

def is_valid(thing, must_have_group_of_two):
    thing = str(thing)
    if len(thing) != LEN:
        # print("length error")
        return False

    it = itertools.groupby(thing)
    for _, group in it:
        l = len(list(group))
        if must_have_group_of_two:
            if l == 2:
                break
        else:
            if l > 1:
                break
    else:
        # print("consecutive characters error")
        return False

    last = int(thing[0])
    for x in thing[1:]:
        x = int(x)
        if x < last:
            # print("order error")
            return False
        last = x

    return True


def count_valid_in_range(start, end, must_have_group_of_two):
    return sum(is_valid(x, must_have_group_of_two) for x in range(start, end))

def test():
    assert is_valid(111111, False)
    assert not is_valid(223450, False)
    assert not is_valid(123789, False)
    assert count_valid_in_range(RANGE[0], RANGE[1] + 1, False) == 1748

    assert is_valid(112233, True)
    assert not is_valid(123444, True)
    assert is_valid(111122, True)
    assert count_valid_in_range(RANGE[0], RANGE[1] + 1, True) == 1180

def main():
    print("day 4/1", count_valid_in_range(RANGE[0], RANGE[1] + 1, False))
    print("day 4/2", count_valid_in_range(RANGE[0], RANGE[1] + 1, True))

    test()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    args = parser.parse_args()

    main(**vars(args))
