package main

import (
    "bufio"
    "os"
    "fmt"
    "strconv"
    "strings"
)

func compute(codes []int, noun int, verb int) int {
    codes[1] = noun
    codes[2] = verb
    ip := 0
    for codes[ip] != 99 {
        op := codes[ip]
        mem1 := codes[ip + 1]
        mem2 := codes[ip + 2]
        dest := codes[ip + 3]
        val1 := codes[mem1]
        val2 := codes[mem2]
        if op == 1 {
            codes[dest] = val1 + val2
        }
        if op == 2 {
            codes[dest] = val1 * val2
        }   
        ip += 4
    }
    return codes[0]
}

func main() {
    file, err := os.Open("input.txt")
    if err != nil {
        fmt.Println(err)
    }
    scanner := bufio.NewScanner(file)
    scanner.Scan()
    csv := scanner.Text()
    strs := strings.Split(csv, ",")
    codes := make([]int, len(strs))
    for i, str := range strs {
        codes[i], err = strconv.Atoi(str)
        if err != nil {
            fmt.Println(err)
        }
    }
    for n := 0; n < 100; n++ {
        for v := 0; v < 100; v++ {
            cpy := make([]int, len(codes))
            copy(cpy, codes)
            res := compute(cpy, n, v)
            if res == 19690720 {
                fmt.Println(100 * n + v)
            }
        }
    }        
}
    
