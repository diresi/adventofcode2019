PROGRAM = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,9,23,1,23,9,27,1,10,27,31,1,13,31,35,1,35,10,39,2,39,9,43,1,43,13,47,1,5,47,51,1,6,51,55,1,13,55,59,1,59,6,63,1,63,10,67,2,67,6,71,1,71,5,75,2,75,10,79,1,79,6,83,1,83,5,87,1,87,6,91,1,91,13,95,1,95,6,99,2,99,10,103,1,103,6,107,2,6,107,111,1,13,111,115,2,115,10,119,1,119,5,123,2,10,123,127,2,127,9,131,1,5,131,135,2,10,135,139,2,139,9,143,1,143,2,147,1,5,147,0,99,2,0,14,0]

OP_ADD = 1
OP_MUL = 2
OP_HLT = 99

def compute_one(op, a, b):
    if op == OP_ADD:
        return a + b
    if op == OP_MUL:
        return a * b
    raise Exception("invalid opcode %s" % op)

def compute(program):
    ip = 0
    while True:
        op, i1, i2, i3 = program[ip:ip+4]
        ip += 4
        if op == OP_HLT:
            break
        a = program[i1]
        b = program[i2]
        program[i3] = compute_one(op, a, b)

    return program[0]

def restore(program, noun, verb):
    program = list(program)
    program[1] = noun
    program[2] = verb
    return program

def provide_number(lb=0, ub=99):
    used = set()
    n = random.randint(lb, ub)
    yield n
    while True:
        used.add(n)
        gg

def search(program, answer):
    for noun in range(100):
        for verb in range(100):
            if compute(restore(program, noun, verb)) == answer:
                return noun, verb
    raise Exception("brute force failed")

def test():
    assert compute(restore(PROGRAM, 12, 2)) == 5534943
    assert search(PROGRAM, 19690720) == (76, 3)

def main():
    res = compute(restore(PROGRAM, 12, 2))
    print("day 2/1", res)

    noun, verb = search(PROGRAM, 19690720)
    print("day 2/2, noun=%s, verb=%s, answer=%s" % (noun, verb, 100 * noun + verb))

    test()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    args = parser.parse_args()

    main(**vars(args))
