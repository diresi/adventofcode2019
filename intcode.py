from vmm import VirtualMemory

class Intcode(object):
    ops = {}

    def __init__(self, program, inputs=None, outputs=None):
        self._program = program
        self.mem = VirtualMemory(self._program)
        self.ip = 0
        self.verbose = 0
        self._halt = False
        self.inputs = inputs or []
        self._in_idx = 0
        self.outputs = outputs or []
        self._yield = False
        self._rel= 0

    def reset(self, noun=None, verb=None, inputs=None, outputs=None):
        self.ip = 0
        self._halt = False
        self.mem = VirtualMemory(self._program)
        if noun is not None:
            self.mem[1] = noun
        if verb is not None:
            self.mem[2] = verb
        if inputs is not None:
            self.inputs = inputs
        self._in_idx = 0
        self.outputs = outputs or []
        self._yield = False
        self._rel= 0
        return self

    def add(self, a, b):
        return a + b
    ops[1] = (add, 2, True)

    def mul(self, a, b):
        return a * b
    ops[2] = (mul, 2, True)

    def read_input(self):
        val = self.inputs[self._in_idx]
        self._in_idx += 1
        return val

    def input_(self):
        return self.read_input()
    ops[3] = (input_, 0, True)

    def write_output(self, x):
        self._yield = True
        self.outputs.append(x)

    def output(self, a):
        self.write_output(a)
    ops[4] = (output, 1, False)

    def jump_if_true(self, a, b):
        if a:
            self.ip = b
    ops[5] = (jump_if_true, 2, False)

    def jump_if_false(self, a, b):
        if not a:
            self.ip = b
    ops[6] = (jump_if_false, 2, False)

    def less_than(self, a, b):
        return 1 if a < b else 0
    ops[7] =(less_than, 2, True)

    def equals(self, a, b):
        return 1 if a == b else 0
    ops[8] =(equals, 2, True)

    def set_rel_base(self, a):
        self._rel += a
    ops[9] = (set_rel_base, 1, False)

    def halt(self):
        self._halt = True
    ops[99] = (halt, 0, False)

    def should_compute_next(self):
        if self._halt:
            return False
        return not self._yield

    def is_halted(self):
        return self._halt

    def compute(self):
        while not self.is_halted():
            self.compute_til_yield()
        if self.verbose:
            print(repr(self))
        return self.return_value()

    def compute_til_yield(self):
        self._yield = False
        while self.should_compute_next():
            self.compute_one()

        return self.return_value()

    def compute_one(self):
        if self.verbose:
            print(repr(self))
        instr = self.next_instr()
        if instr is None:
            raise Exception("invalid opcode %s" % self.mem[self.ip:self.ip+10])
        meth, params, addr = instr
        val = meth(self, *params)
        if addr is not None:
            self.mem[addr] = val

    def return_value(self):
        return self.mem[0]

    def load_param_from_ip(self, mode):
        if mode == 1:
            # immediate addressing
            addr = self.ip
        else:
            addr = self.resolve_addr_from_ip(mode)
        return self.mem[addr]

    def resolve_addr_from_ip(self, mode):
        if mode == 0:
            return self.mem[self.ip]
        elif mode == 2:
            return self._rel + self.mem[self.ip]
        else:
            raise Exception("invalid addressing mode: %s" % mode)

    def next_instr(self):
        fop = self.mem[self.ip]
        op = fop % 100
        fop = fop // 100

        self.ip += 1

        instr = self.ops.get(op)
        meth, pcount, has_output = instr
        params = []

        for i in range(pcount):
            mode = fop % 10
            fop = fop // 10

            params.append(self.load_param_from_ip(mode))
            self.ip += 1

        if has_output:
            mode = fop % 10
            fop = fop // 10

            store_addr = self.resolve_addr_from_ip(mode)
            self.ip += 1
        else:
            store_addr = None

        return meth, params, store_addr

    def __repr__(self):
        txt = [repr(self.mem),
               "ip=%s, rel=%s" % (self.ip, self._rel),
               "outputs=%r" % (self.outputs,),
               "inputs=%r" % (self.inputs,),
               "_in_idx=%r" % (self._in_idx,),
              ]
        return "\n".join(txt)

