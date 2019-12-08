from collections import defaultdict


def check_sum(body, count, sats):
    children_counts = [check_sum(sat, count + 1, sats)
                       for sat in sats[body]]
    return count + sum(children_counts)


def find_path(centers, body):
    path = []
    while body in centers:
        body = centers[body]
        path.append(body)
    path.reverse()
    return path


with open("input.txt") as f:
    sats = defaultdict(set)
    centers = {}
    raw_edges = [line.rstrip('\n').split(")") for line in f]
    for body, sat in raw_edges:
        sats[body].add(sat)
        centers[sat] = body
    count = check_sum("COM", 0, sats)
    you_path = find_path(centers, "YOU")
    san_path = find_path(centers, "SAN")
    common_path = [x for x, y in zip(you_path, san_path) if x == y]
    dist = len(san_path) + len(you_path) - 2 * len(common_path)

    print(count)
    print(dist)
