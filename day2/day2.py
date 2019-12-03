def compute(codes, noun, verb):
    codes[1] = noun
    codes[2] = verb
    ip = 0
    while codes[ip] != 99:
        instr = codes[ip:ip+4:]
        op, mem1, mem2, dest = instr
        val1 = codes[mem1]
        val2 = codes[mem2]
        if op == 1:
            codes[dest] = val1 + val2
        if op == 2:
            codes[dest] = val1 * val2
        ip += 4
    return codes[0]


with open("input.txt") as f:
    code_strs = f.readline().split(",")
    codes = [int(code) for code in code_strs]
    for n in range(100):
        for v in range(100):
            res = compute(codes.copy(), n, v)
            if res == 19690720:
                print(100 * n + v)
