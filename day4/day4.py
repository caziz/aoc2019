part_1 = 0
part_2 = 0
for num in range(240298, 784956):
    num_str = str(num)
    decreasing = False
    double = False
    double_alone = False
    for i, c1 in enumerate(num_str):
        if i == 0:
            continue
        c0 = num_str[i - 1]
        if c0 > c1:
            decreasing = True
            break
        if c0 == c1:
            double = True
            front = i == 1 or num_str[i - 2] != c1
            back = i == len(num_str) - 1 or num_str[i + 1] != c1
            if front and back:
                double_alone = True
    if not decreasing and double:
        part_1 += 1
        if double_alone:
            part_2 += 1
print(part_1)
print(part_2)
