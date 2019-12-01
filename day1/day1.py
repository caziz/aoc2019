def fuel_required(mass):
    fuel = (mass // 3) - 2
    return 0 if fuel < 0 else fuel + fuel_required(fuel)


with open("input.txt") as f:
    masses = [int(line) for line in f]
    fuels = [fuel_required(mass) for mass in masses]
    total_fuel = sum(fuels)
    print(total_fuel)
