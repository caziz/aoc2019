package main

import (
	"bufio"
	"fmt"
	"strconv"
	"os"
)

func fuelRequired(mass int) int {
	fuel := (mass / 3) - 2
	if fuel < 0 {
		return 0
	}
	return fuel + fuelRequired(fuel)
}

func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		fmt.Println(err)
	}
	sum := 0
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		mass, err := strconv.Atoi(scanner.Text())
		if err != nil {
			fmt.Println(err)
		}
		sum += fuelRequired(mass)
	}
	fmt.Println(sum)
}