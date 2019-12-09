def render(column):
    val = [pixel for pixel in column if pixel != 2][0]
    return [' ', 'X'][val]


with open("input.txt") as f:
    nums = [int(num) for num in f.readline()]
    width = 25
    height = 6
    size = width * height
    layers = [nums[i:i+size] for i in range(0, len(nums), size)]
    fewest_0 = min(layers, key=lambda layer: layer.count(0))
    part_1 = fewest_0.count(1) * fewest_0.count(2)
    print(part_1)

    raw_image = [render(column) for column in zip(*layers)]
    image = ["".join(raw_image[i:i+width])
             for i in range(0, len(raw_image), width)]
    print("\n".join(image))
