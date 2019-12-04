def format_edges(line):
    edge_strs = line.split(",")
    return [(edge[0], int(edge[1:])) for edge in edge_strs]


# returns a dictionary of (x, y) -> d
# where d is the minimum length of wire
# to reach coordinate x, y
def coord_dists(edges):
    x, y = 0, 0
    dist = 0
    dists = {}
    for (d, length) in edges:
        dx, dy = {
            'U': (0, 1),
            'D': (0, -1),
            'R': (1, 0),
            'L': (-1, 0)
        }[d]
        for _ in range(length):
            x += dx
            y += dy
            dist += 1
            if (x, y) not in dists:
                dists[(x, y)] = dist
    return dists


with open("input.txt") as f:
    edges1 = format_edges(f.readline())
    edges2 = format_edges(f.readline())

    dists1 = coord_dists(edges1)
    dists2 = coord_dists(edges2)

    intersections = dists1.keys() & dists2.keys()

    manhattan_dists = [abs(x) + abs(y) for x, y in intersections]
    part_1 = min(manhattan_dists)
    print(part_1)

    total_dists = [dists1[coord] + dists2[coord] for coord in intersections]
    part_2 = min(total_dists)
    print(part_2)
