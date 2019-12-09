from day2 import Intcode as _Intcode

PROGRAM = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,65,73,225,1101,37,7,225,1101,42,58,225,1102,62,44,224,101,-2728,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1,69,126,224,101,-92,224,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1102,41,84,225,1001,22,92,224,101,-150,224,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1101,80,65,225,1101,32,13,224,101,-45,224,224,4,224,102,8,223,223,101,1,224,224,1,224,223,223,1101,21,18,225,1102,5,51,225,2,17,14,224,1001,224,-2701,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,101,68,95,224,101,-148,224,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1102,12,22,225,102,58,173,224,1001,224,-696,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1002,121,62,224,1001,224,-1302,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,226,677,224,102,2,223,223,1005,224,329,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,344,1001,223,1,223,1007,226,677,224,1002,223,2,223,1006,224,359,1001,223,1,223,1007,677,677,224,102,2,223,223,1005,224,374,1001,223,1,223,108,677,677,224,102,2,223,223,1006,224,389,101,1,223,223,8,226,677,224,102,2,223,223,1005,224,404,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,419,101,1,223,223,8,677,226,224,1002,223,2,223,1005,224,434,101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,449,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,464,101,1,223,223,1107,226,226,224,102,2,223,223,1006,224,479,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,108,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,524,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,539,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,554,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,569,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,584,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,599,1001,223,1,223,1008,677,677,224,1002,223,2,223,1005,224,614,101,1,223,223,1107,226,677,224,102,2,223,223,1005,224,629,101,1,223,223,1108,677,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1107,677,226,224,1002,223,2,223,1006,224,659,1001,223,1,223,108,226,226,224,102,2,223,223,1006,224,674,101,1,223,223,4,223,99,226]

class Intcode(_Intcode):
    ops = dict(_Intcode.ops)

    def __init__(self, program, inputs = None, outputs=None):
        super(Intcode, self).__init__(program)
        self._inputs = inputs or []
        self.inputs = iter(self._inputs)
        self.outputs = outputs or []

    def restore(self, *a, **kw):
        super(Intcode, self).restore(*a, **kw)
        self.inputs = iter(self._inputs)

    def read_input(self):
        return next(self.inputs)

    def write_output(self, x):
        self.outputs.append(x)

    def input_(self):
        return self.read_input()
    ops[3] = (input_, 0, True)

    def output(self, a):
        self.write_output(a)
    ops[4] = (output, 1, False)

class IntcodeWithAddressing(Intcode):
    def next_instr(self):
        ip = self.ip
        program = self.program
        # print("P", program[ip:])

        fop = program[ip]
        op = fop % 100
        fop = fop // 100
        ip += 1

        instr = self.ops.get(op)
        if self.is_sentinel(instr):
            return instr

        meth, pcount, has_output = instr
        params = []

        for i in range(pcount):
            # print("fop=%s" % fop)
            mode = fop % 10
            fop = fop // 10
            addr = program[ip]

            # print("mode=%s addr=%s" % (mode, addr))

            if mode == 0:
                # direct addressing
                params.append(program[addr])
            elif mode == 1:
                # immediate addressing
                params.append(addr)
            else:
                raise Exception("invalid addressing mode: %s" % mode)
            ip += 1

        if has_output:
            # append last parameter as address (i.e. immediate value)
            store_addr = program[ip]
            ip += 1
        else:
            store_addr = None

        self.ip = ip
        # print("next_instr", meth, params)
        return meth, params, store_addr

def test():
    program = [3,0,4,0,99]

    vm = Intcode(program, [123])
    vm.compute()
    assert vm.outputs == [123]

    vm = Intcode(program, ["test"])
    vm.compute()
    assert vm.outputs == ["test"]

    vm = IntcodeWithAddressing([1002,4,3,0,99])
    assert vm.compute() == 99 * 3

    vm = IntcodeWithAddressing(PROGRAM, [1])
    vm.compute()
    assert all(x == 0 for x in vm.outputs[:-1])
    assert vm.outputs[-1] == 14522484

def main():
    vm = IntcodeWithAddressing(PROGRAM, [1])
    # vm.verbose = True

    # oops, res is ignored. the diagnostic code is the last output :)
    # res = vm.compute()
    vm.compute()
    print("day 5/1", vm.outputs[:-1], vm.outputs[-1])

    print("day 5/2", )

    test()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    args = parser.parse_args()

    main(**vars(args))
