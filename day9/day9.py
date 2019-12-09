from itertools import permutations
from threading import Thread
from queue import Queue


class Process:
    def __init__(self, mem):
        self.mem = Memory(mem)
        self.ip = 0
        self.rb = 0
        self.halt = False
        self.sentinel = object()
        self.stdin = Queue()
        self.stdout = Queue()

    def op_1(self, rargs, wargs):
        self.mem[wargs[2]] = rargs[0] + rargs[1]

    def op_2(self, rargs, wargs):
        self.mem[wargs[2]] = rargs[0] * rargs[1]

    def op_3(self, rargs, wargs):
        val = self.stdin.get()
        self.mem[wargs[0]] = val

    def op_4(self, rargs, wargs):
        self.stdout.put(rargs[0])

    def op_5(self, rargs, wargs):
        if rargs[0] != 0:
            self.ip = rargs[1]

    def op_6(self, rargs, wargs):
        if rargs[0] == 0:
            self.ip = rargs[1]

    def op_7(self, rargs, wargs):
        if rargs[0] < rargs[1]:
            self.mem[wargs[2]] = 1
        else:
            self.mem[wargs[2]] = 0

    def op_8(self, rargs, wargs):
        if rargs[0] == rargs[1]:
            self.mem[wargs[2]] = 1
        else:
            self.mem[wargs[2]] = 0

    def op_9(self, rargs, wargs):
        self.rb += rargs[0]

    def op_99(self, rargs, wargs):
        self.halt = True

    operations = {
        1: [3, op_1],
        2: [3, op_2],
        3: [1, op_3],
        4: [1, op_4],
        5: [2, op_5],
        6: [2, op_6],
        7: [3, op_7],
        8: [3, op_8],
        9: [1, op_9],
        99: [0, op_99]
    }

    def op_arity(self, op):
        return self.operations[op][0]

    def op_func(self, op):
        return self.operations[op][1]

    def parse_modes(self, raw_modes, arity):
        return [raw_modes // (10 ** i) % 10 for i in range(arity)]

    def read_arg(self, arg, mode):
        return {
            0: self.mem[arg],
            1: arg,
            2: self.mem[arg + self.rb]
        }[mode]

    def write_arg(self, arg, mode):
        return {
            0: arg,
            1: None,
            2: arg + self.rb
        }[mode]

    def run(self):
        while not self.halt:
            op = self.mem[self.ip] % 100
            raw_modes = self.mem[self.ip] // 100
            arity = self.op_arity(op)
            modes = self.parse_modes(raw_modes, arity)
            args = self.mem[self.ip+1: self.ip+arity+1]
            wargs = list(map(self.write_arg, args, modes))
            rargs = list(map(self.read_arg, args, modes))
            func = self.op_func(op)
            self.ip += arity + 1
            func(self, rargs, wargs)
        # inform consumer that stdout is closed
        self.stdout.put(self.sentinel)


class Memory(list):
    default_val = 0

    def extend_memory(self, index):
        self.extend([self.default_val] * (2 * index - len(self)))

    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend_memory(index)
        list.__setitem__(self, index, value)

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.stop >= len(self):
                self.extend_memory(key.stop)
        elif key >= len(self):
            self.extend_memory(key)
        return list.__getitem__(self, key)


def run_io(mem):
    p = Process(mem)
    Thread(target=p.run).start()

    def process_out():
        while True:
            val = p.stdout.get()
            if val is p.sentinel:
                break
            print(val)
    Thread(target=process_out).start()

    def process_in():
        while True:
            val = int(input())
            p.stdin.put(val)
    Thread(target=process_in, daemon=True).start()


with open("input.txt") as f:
    code_strs = f.readline().split(",")
    mem = [int(code) for code in code_strs]
    run_io(mem)
