package main

import (
	"fmt"
	"strconv"
)

func main() {
	part1 := 0
	part2 := 0
	for i := 240298; i <= 784956; i++ {
		str := strconv.Itoa(i)
		decreasing := false
		double := false
		double_alone := false
		for i, _ := range str {
			if i == 0 {
				continue
			}
			c0 := str[i-1]
			c1 := str[i]
			if c0 > c1 {
				decreasing = true
				break
			}
			if c0 == c1 {
				double = true
				front := i == 1 || str[i-2] != c1
				back := i == len(str)-1 || str[i+1] != c1
				if front && back {
					double_alone = true
				}
			}
		}
		if !decreasing && double {
			part1++
			if double_alone {
				part2++
			}
		}
	}
	fmt.Println(part1)
	fmt.Println(part2)
}
