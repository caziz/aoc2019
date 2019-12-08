def op_1(ip, codes, vals, regs):
    codes[regs[2]] = vals[0] + vals[1]
    return ip


def op_2(ip, codes, vals, regs):
    codes[regs[2]] = vals[0] * vals[1]
    return ip


def op_3(ip, codes, vals, regs):
    codes[regs[0]] = int(input(">>> "))
    return ip


def op_4(ip, codes, vals, regs):
    print(vals[0])
    return ip


def op_5(ip, codes, vals, regs):
    if vals[0] != 0:
        ip = vals[1]
    return ip


def op_6(ip, codes, vals, regs):
    if vals[0] == 0:
        ip = vals[1]
    return ip


def op_7(ip, codes, vals, regs):
    if vals[0] < vals[1]:
        codes[regs[2]] = 1
    else:
        codes[regs[2]] = 0
    return ip


def op_8(ip, codes, vals, regs):
    if vals[0] == vals[1]:
        codes[regs[2]] = 1
    else:
        codes[regs[2]] = 0
    return ip


def op_99(ip, codes, vals, regs):
    return -1


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


def op_arity(op):
    return operations[op][0]


def op_func(op):
    return operations[op][1]


def parse_modes(raw_modes, arity):
    return [raw_modes // (10 ** i) % 10 for i in range(0, arity)]


def val(param, mode, codes):
    return param if mode == 1 else codes[param]


def compute(codes):
    ip = 0
    while ip != -1:
        op = codes[ip] % 100
        raw_modes = codes[ip] // 100
        ip += 1
        arity = op_arity(op)
        modes = parse_modes(raw_modes, arity)
        params = codes[ip:ip+arity]
        ip += arity
        vals = [val(param, mode, codes) for param, mode in zip(params, modes)]
        func = op_func(op)
        ip = func(ip, codes, vals, params)


with open("input.txt") as f:
    code_strs = f.readline().split(",")
    codes = [int(code) for code in code_strs]
    compute(codes)
