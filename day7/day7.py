from itertools import permutations
from threading import Thread
from queue import Queue


class Program:
    def __init__(self, mem):
        self.mem = mem
        self.ip = 0
        self.halt = False
        self.sentinel = object()
        self.stdin = Queue()
        self.stdout = Queue()

    def op_1(self, vals, params):
        self.mem[params[2]] = vals[0] + vals[1]

    def op_2(self, vals, params):
        self.mem[params[2]] = vals[0] * vals[1]

    def op_3(self, vals, params):
        val = self.stdin.get()
        self.mem[params[0]] = val

    def op_4(self, vals, params):
        self.stdout.put(vals[0])

    def op_5(self, vals, params):
        if vals[0] != 0:
            self.ip = vals[1]

    def op_6(self, vals, params):
        if vals[0] == 0:
            self.ip = vals[1]

    def op_7(self, vals, params):
        if vals[0] < vals[1]:
            self.mem[params[2]] = 1
        else:
            self.mem[params[2]] = 0

    def op_8(self, vals, params):
        if vals[0] == vals[1]:
            self.mem[params[2]] = 1
        else:
            self.mem[params[2]] = 0

    def op_99(self, vals, params):
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
        99: [0, op_99]
    }

    def op_arity(self, op):
        return self.operations[op][0]

    def op_func(self, op):
        return self.operations[op][1]

    def parse_modes(self, raw_modes, arity):
        return [raw_modes // (10 ** i) % 10 for i in range(0, arity)]

    def val(self, param, mode):
        return param if mode == 1 else self.mem[param]

    def run(self):
        while not self.halt:
            op = self.mem[self.ip] % 100
            raw_modes = self.mem[self.ip] // 100
            arity = self.op_arity(op)
            modes = self.parse_modes(raw_modes, arity)
            params = self.mem[self.ip+1: self.ip+arity+1]
            vals = list(map(self.val, params, modes))
            func = self.op_func(op)
            self.ip += arity + 1
            func(self, vals, params)
        # inform consumer that stdout is closed
        self.stdout.put(self.sentinel)


def run_io(mem):
    p = Program(mem)
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


def run_part2(mem):
    high_score = 0
    for permutation in permutations(range(5, 10)):
        processes = []
        threads = []
        for phase in permutation:
            p = Program(mem.copy())
            if not processes:
                p.stdin.put(phase)
                p.stdin.put(0)
            else:
                prev = processes[-1]
                p.stdin = prev.stdout
                p.stdin.put(phase)
            processes.append(p)
            t = Thread(target=p.run)
            threads.append(t)

        score = [0]

        def run_tpipe():
            while True:
                val = processes[-1].stdout.get()
                if val is processes[-1].sentinel:
                    break
                score[0] = val
                processes[0].stdin.put(val)
        tpipe = Thread(target=run_tpipe)
        tpipe.start()
        for thread in threads:
            thread.start()
        tpipe.join()
        high_score = max(high_score, score[0])
    return high_score


def run_part1(mem):
    high_score = 0
    for permutation in permutations(range(5)):
        processes = []
        threads = []
        score = 0
        for phase in permutation:
            p = Program(mem.copy())
            if not processes:
                p.stdin.put(phase)
                p.stdin.put(0)
            else:
                p.stdin = processes[-1].stdout
                p.stdin.put(phase)
            processes.append(p)
            t = Thread(target=p.run)
            threads.append(t)
        for thread in threads:
            thread.start()
        score = processes[-1].stdout.get()
        high_score = max(high_score, score)
    return high_score


with open("input.txt") as f:
    code_strs = f.readline().split(",")
    mem = [int(code) for code in code_strs]
    print(run_part1(mem.copy()))
    print(run_part2(mem.copy()))
