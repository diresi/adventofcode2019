import itertools
from day5 import IntcodeWithAddressing

PROGRAM = [3,8,1001,8,10,8,105,1,0,0,21,46,55,68,89,110,191,272,353,434,99999,3,9,1002,9,3,9,1001,9,3,9,102,4,9,9,101,4,9,9,1002,9,5,9,4,9,99,3,9,102,3,9,9,4,9,99,3,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,1001,9,5,9,1002,9,2,9,1001,9,5,9,1002,9,3,9,4,9,99,3,9,101,3,9,9,102,3,9,9,101,3,9,9,1002,9,4,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99]

def compute(program, phases):
    vms = []
    inputs = []
    for ph in phases:
        inputs.append(ph)
        vm = IntcodeWithAddressing(program, inputs)
        inputs = vm.outputs
        vms.append(vm)

    # input for the first stage
    vms[0].inputs.append(0)

    for vm in vms:
        vm.compute()
    return vms[-1].outputs[0]

def max_value(program):
    phases = [0, 1, 2, 3, 4]
    pairs = ((ph, compute(program, ph)) for ph in itertools.permutations(phases))
    return max(pairs, key=lambda p: p[1])

def test():
    program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    phases = [4,3,2,1,0]
    assert compute(program, phases) == 43210
    assert max_value(program) == (tuple(phases), 43210)

    program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
            101,5,23,23,1,24,23,23,4,23,99,0,0]
    phases = [0,1,2,3,4]
    assert compute(program, phases) == 54321
    assert max_value(program) == (tuple(phases), 54321)

    program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
            1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    phases = [1,0,4,3,2]
    assert compute(program, phases) == 65210
    assert max_value(program) == (tuple(phases), 65210)

    phases = [3, 2, 4, 0, 1]
    assert compute(PROGRAM, phases) == 440880
    assert max_value(PROGRAM) == (tuple(phases), 440880)

def main():
    print("day 7/1", max_value(PROGRAM))

    test()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    args = parser.parse_args()

    main(**vars(args))
