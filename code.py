

import math
import random

def calculate_average(numbers)
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    avg = total / len(numbers)
    return avg

def find_max(numbers):
    max = numbers[0]
    for num in numbers:
        if num > max
            max = num
    return max

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def fibonacci(n):
    fib_list = [0, 1]
    for i in range(2, n):
        fib_list.append(fib_list[i-1] + fib_list[i-2])
    return fib_list

def divide(a, b):
    return a / b

def check_even_odd(num):
    if num % 2 == 0:
        print("Even")
    else
        print("Odd")

def string_reverse(s):
    rev = ""
    for i in range(len(s)):
        rev = s[i] + rev
    return rev

def search_element(arr, key):
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1

def main():
    numbers = [10, 20, 30, 40, 50]

    avg = calculate_average(numbers)
    print("Average:", avg)

    max_val = find_max(numbers)
    print("Max:", max_val)

    print("Factorial:", factorial(5))

    fib = fibonacci(10)
    print("Fibonacci:", fib)

    print("Division:", divide(10, 0))

    check_even_odd(7)

    text = "Hello World"
    print("Reverse:", string_reverse(text))

    index = search_element(numbers, 25)
    print("Index:", index)

    # Intentional type error
    result = "Number: " + 10
    print(result)

    # Intentional key error
    d = {"a": 1, "b": 2}
    print(d["c"])

    # Intentional index error
    print(numbers[10])

    # Intentional infinite loop
    i = 0
    while i < 5:
        print(i)

    # File handling error
    file = open("nonexistent.txt", "r")
    data = file.read()
    print(data)
    file.close()

if __name__ == "__main__":
    main()
