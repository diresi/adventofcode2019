PROGRAM = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,9,23,1,23,9,27,1,10,27,31,1,13,31,35,1,35,10,39,2,39,9,43,1,43,13,47,1,5,47,51,1,6,51,55,1,13,55,59,1,59,6,63,1,63,10,67,2,67,6,71,1,71,5,75,2,75,10,79,1,79,6,83,1,83,5,87,1,87,6,91,1,91,13,95,1,95,6,99,2,99,10,103,1,103,6,107,2,6,107,111,1,13,111,115,2,115,10,119,1,119,5,123,2,10,123,127,2,127,9,131,1,5,131,135,2,10,135,139,2,139,9,143,1,143,2,147,1,5,147,0,99,2,0,14,0]

class Intcode(object):
    ops = {}

    def __init__(self, program):
        self._program = program
        self.program = list(self._program)
        self.ip = 0
        self.verbose = 0
        self._halt = False

    def add(self, a, b):
        return a + b
    ops[1] = (add, 2, True)

    def mul(self, a, b):
        return a * b
    ops[2] = (mul, 2, True)

    def halt(self):
        self._halt = True
    ops[99] = (halt, 0, False)

    def should_compute_next(self):
        return not self._halt

    def next_instr(self):
        ip = self.ip
        program = self.program

        op = program[ip]

        instr = self.ops.get(op)

        meth, pcount, has_output = instr
        # resolve direct addresses
        addrs = program[ip+1:ip+1+pcount]
        params = [program[addr] for addr in addrs]

        ip += 1 + pcount

        if has_output:
            store_addr = program[ip]
            ip += 1
        else:
            store_addr = None

        self.ip = ip
        return meth, params, store_addr

    def compute(self):
        while self.should_compute_next():
            instr = self.next_instr()
            if instr is None:
                raise Exception("invalid opcode %s" % self.program[self.ip:self.ip+10])
            meth, params, addr = instr
            val = meth(self, *params)
            if self.verbose:
                print("INSTR", meth, params, addr, val)
            if addr is not None:
                self.program[addr] = val

        return self.return_value()

    def return_value(self):
        return self.program[0]

    def reset(self, noun=None, verb=None):
        self.ip = 0
        self._halt = False
        self.program = list(self._program)
        if noun is not None:
            self.program[1] = noun
        if verb is not None:
            self.program[2] = verb
        return self

def search(program, answer):
    vm = Intcode(program)
    for noun in range(100):
        for verb in range(100):
            if vm.reset(noun, verb).compute() == answer:
                return noun, verb
    raise Exception("brute force failed")

def test():
    assert Intcode(PROGRAM).reset(12, 2).compute() == 5534943
    assert search(PROGRAM, 19690720) == (76, 3)

def main():
    res = Intcode(PROGRAM).reset(12, 2).compute()
    print("day 2/1", res)

    noun, verb = search(PROGRAM, 19690720)
    print("day 2/2, noun=%s, verb=%s, answer=%s" % (noun, verb, 100 * noun + verb))

    test()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    args = parser.parse_args()

    main(**vars(args))
