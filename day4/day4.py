part_1 = 0
part_2 = 0
for n in range(240298, 784956):
    increasing = False
    nums = []
    counts = []
    while n != 0:
        d = n % 10
        n //= 10
        if nums and d > nums[-1]:
            increasing = True
            break
        if nums and d == nums[-1]:
            counts[-1] += 1
        else:
            nums.append(d)
            counts.append(1)
    if not increasing and len(counts) != 6:
        part_1 += 1
        if 2 in counts:
            part_2 += 1
print(part_1)
print(part_2)
