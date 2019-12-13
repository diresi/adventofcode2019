import itertools
from intcode import Intcode

PROGRAM = [3,8,1001,8,10,8,105,1,0,0,21,46,55,68,89,110,191,272,353,434,99999,3,9,1002,9,3,9,1001,9,3,9,102,4,9,9,101,4,9,9,1002,9,5,9,4,9,99,3,9,102,3,9,9,4,9,99,3,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,1001,9,5,9,1002,9,2,9,1001,9,5,9,1002,9,3,9,4,9,99,3,9,101,3,9,9,102,3,9,9,101,3,9,9,1002,9,4,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99]


def compute(program, phases, feedback=False):
    vms = []
    inputs = []
    for ph in phases:
        inputs.append(ph)
        vm = Intcode(program, inputs)
        inputs = vm.outputs
        vms.append(vm)

    if feedback:
        vms[0].inputs = vms[-1].outputs

    # input for the first stage
    vms[0].inputs[:] = [phases[0], 0]

    while not vms[-1].is_halted():
        vms = [vm for vm in vms if not vm.is_halted()]
        for vm in vms:
            if vm.verbose:
                print("START VM", vm.inputs)
            vm.compute_til_yield()
            if vm.verbose:
                print("YIELD VM", vm.outputs)
    return vms[-1].outputs[-1]

def max_value(program, phases, feedback=False):
    pairs = ((ph, compute(program, ph, feedback)) for ph in itertools.permutations(phases))
    return max(pairs, key=lambda p: p[1])

def test():
    program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    phases = [4,3,2,1,0]
    assert compute(program, phases) == 43210
    assert max_value(program, [0,1,2,3,4]) == (tuple(phases), 43210)

    program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
            101,5,23,23,1,24,23,23,4,23,99,0,0]
    phases = [0,1,2,3,4]
    assert compute(program, phases) == 54321
    assert max_value(program, [0,1,2,3,4]) == (tuple(phases), 54321)

    program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
            1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    phases = [1,0,4,3,2]
    assert compute(program, phases) == 65210
    assert max_value(program, [0,1,2,3,4]) == (tuple(phases), 65210)

    phases = [3, 2, 4, 0, 1]
    assert compute(PROGRAM, phases) == 440880
    assert max_value(PROGRAM, [0,1,2,3,4]) == (tuple(phases), 440880)

    program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
            27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    phases = [9,8,7,6,5]
    assert compute(program, phases, True) == 139629729
    assert max_value(program, [5,6,7,8,9], True) == (tuple(phases), 139629729)

    program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
            -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
            53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    phases = [9,7,8,5,6]
    assert compute(program, phases, True) == 18216
    assert max_value(program, [5,6,7,8,9], True) == (tuple(phases), 18216)

    phases = [5,7,9,6,8]
    assert compute(PROGRAM, phases, True) == 3745599
    assert max_value(PROGRAM, [5,6,7,8,9], True) == (tuple(phases), 3745599)

def main():
    print("day 7/1", max_value(PROGRAM, [0,1,2,3,4]))
    print("day 7/2", max_value(PROGRAM, [5,6,7,8,9], True))

    test()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    args = parser.parse_args()

    main(**vars(args))
