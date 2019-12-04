package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Edge struct {
	dir  byte
	dist int
}

type Coord struct {
	x, y int
}

func FormatEdges(line string) []Edge {
	edge_strs := strings.Split(line, ",")
	edges := make([]Edge, len(edge_strs))
	for i, edge_str := range edge_strs {
		dist, _ := strconv.Atoi(edge_str[1:])
		edges[i] = Edge{edge_str[0], dist}
	}
	return edges
}

func CoordDistances(edges []Edge) map[Coord]int {
	x, y := 0, 0
	dist := 0
	dists := make(map[Coord]int)
	for _, edge := range edges {
		for i := 0; i < edge.dist; i++ {
			switch edge.dir {
			case 'U':
				y += 1
			case 'D':
				y -= 1
			case 'R':
				x += 1
			case 'L':
				x -= 1
			}
			dist += 1
			c := Coord{x, y}
			_, ok := dists[c]
			if !ok {
				dists[c] = dist
			}
		}
	}
	return dists
}

func MapIntersection(coords1, coords2 map[Coord]int) []Coord {
	coords := make([]Coord, 0, len(coords1))
	for coord := range coords1 {
		_, ok := coords2[coord]
		if ok {
			coords = append(coords, coord)
		}
	}
	return coords
}

func Min(x, y int) int {
	if x < y {
		return x
	}
	return y
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	file, _ := os.Open("input.txt")
	scanner := bufio.NewScanner(file)

	scanner.Scan()
	line1 := scanner.Text()
	edges1 := FormatEdges(line1)
	dists1 := CoordDistances(edges1)

	scanner.Scan()
	line2 := scanner.Text()
	edges2 := FormatEdges(line2)
	dists2 := CoordDistances(edges2)

	intersections := MapIntersection(dists1, dists2)

	manDist := func(coord Coord) int {
		return Abs(coord.x) + Abs(coord.y)
	}
	wireDist := func(coord Coord) int {
		return dists1[coord] + dists2[coord]
	}
	minManDist := manDist(intersections[0])
	minWireDist := wireDist(intersections[0])
	for _, coord := range intersections {
		minManDist = Min(minManDist, manDist(coord))
		minWireDist = Min(minWireDist, wireDist(coord))
	}
	fmt.Println(minManDist)
	fmt.Println(minWireDist)
}
