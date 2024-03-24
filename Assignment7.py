
import math
import random
import texttable


def print_table(title, headers, data, alignments):
    tt = texttable.Texttable(0)
    tt.set_cols_align(alignments)
    tt.add_rows([headers] + data, True)
    print(title)
    print(tt.draw())
    print()


# [1] (Slides 29-30) Define a function find_postage(amount) that takes an amount of postage and returns
# the breakdown of 4-cent and 5-cent stamps to use. Note: If n ≥ 12, it should always give a solution.
# If n < 12, it should try to solve it for those cases that still work,
# and return "n/a" for those cases that don't work.
def find_postage(amount, stamps):
    if amount == 12:
        stamps[4] += 3
        stamps[5] += 0
    elif amount == 13:
        stamps[4] += 2
        stamps[5] += 1
    elif amount == 14:
        stamps[4] += 1
        stamps[5] += 2
    elif amount == 15:
        stamps[4] += 0
        stamps[5] += 3
    elif amount > 15:
        stamps[4] += 1
        find_postage(amount - 4, stamps)


def q1():
    for amount in range(12, 101):
        stamps = {4: 0, 5: 0}
        find_postage(amount, stamps)
        print("postage for ", amount, " is: ", stamps)


# [2] (Slide 38) Define a function fib_recursive(n) that recursively calculates the n-th Fibonacci number,
# including base cases for n = 0 and n = 1. Then define a second function fib_formula(n) that uses the following
# formula to calculate the n-th Fibonacci number. You will need to import package math to find the square roots (sqrt).
# Finally, make sure to use the int function to convert the floating point number to an integer result.

def fib_recursive(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_formula(n):
    sqrt5 = math.sqrt(5)
    return int(round((1 / sqrt5) * (((1 + sqrt5) / 2) ** n - ((1 - sqrt5) / 2) ** n)))


def fib_loop(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        arr = [0] * (n + 1)
        arr[1] = 1
        for i in range(2, n + 1):
            arr[i] = arr[i - 1] + arr[i - 2]
        return arr[n]


def q2():
    data = []
    for n in range(10):
        data.append([n, fib_recursive(n), fib_formula(n), fib_loop(n), sum_fib(n)])
    headers = ["n", "Fib Recursive", "Fib Formula", "Fib Loop", "Sum Cumulative"]
    title = "Fibonacci Numbers using 3 methods"
    alignments = ["r"] * 5
    print_table(title, headers, data, alignments)


def sum_geometric_formula(n, a, r):
    return n + 1 if r == 1 else a * ((r ** (n + 1) - 1) / (r - 1))


def sum_fib(n):
    sqrt5 = math.sqrt(5)
    a = 1 / sqrt5
    r1 = (1 + sqrt5) / 2
    r2 = (1 - sqrt5) / 2
    return int(round(sum_geometric_formula(n, a, r1) - sum_geometric_formula(n, a, r2)))


# [3] Define a function sum_fib(n) that calculates the sum of Fibonacci numbers f(0)
# thru f(n) using the formula for f(n) of the
# previous question combined with the formula for the geometric series from the previous Assignment.
def q3():
    print("See question number 2")


# [4] (Slide 28) Define a function prime_factorization(n)
# that returns the prime factors of n. If n is prime, the list is just [n].
def q4():
    for i in range(2, 101):
        print("The Prime factorization of ", i, "is: ", prime_factorization(i))


def prime_factorization(n):
    factors = []
    divisor = 2
    while n > 1:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1
    return factors


# [5] Define a function gcd(a, b) that computes the gcd as the product of the common prime factors of a and b.
def q5():
    for i in range(20):
        a = random.randint(1, 101)
        b = random.randint(1, 101)
        print("GCD of ", a, "and", b, "is: ", gcd(a, b))


def gcd(a, b):
    factors_a = prime_factorization(a)
    factors_b = prime_factorization(b)
    factors = []
    g = 1
    for f in factors_a:
        if f in factors_b:
            factors_b.remove(f)
            factors.append(f)
            g += f
    return g


# [6] (Slide 63) Define a function gcd_recursive(a, b) using the reduction
# gcd(a, b) = gcd(b mod a, a) and the condition gcd(0, b) = b when b > 0.
def q6():
    for i in range(20):
        a = random.randint(1, 101)
        b = random.randint(1, 101)
        print("GCD of ", a, "and", b, "is: ", gcd_recursive(a, b))


def gcd_recursive(a, b):
    return a if b == 0 else gcd_recursive(b, a % b)


# [7] Compare the results of questions 5 and 6 with that of built-in function math.gcd(a, b).
# See Task 2 for how to compare two computations for the same input.

def q7():
    for i in range(20):
        a = random.randint(1, 101)
        b = random.randint(1, 101)
        print("Build in math GCD of ", a, "and", b, "is: ", math.gcd(a, b))


# [8] (Slide 44) Define a function all_strings(alphabet, size) that generates all strings
# of length size or smaller using the alphabet that is provided. It should start with the empty string,
# then strings of length 1, etc. Call it for these inputs:

def all_strings(alphabet, size):
    words = [""]
    newList = [""]

    for i in range(size):
        newList = [word + letter for letter in alphabet for word in newList]
        words += newList
    return words


def q8():
    size = 10
    alphabet = ["a"]
    strings = all_strings(alphabet, size)
    print(alphabet, len(alphabet), sum_geometric_formula(size, 1, len(alphabet)), len(strings), strings)
    alphabet2 = ["a", "b", "c"]
    size2 = 3
    strings2 = all_strings(alphabet2, size2)
    print(alphabet2, len(alphabet2), sum_geometric_formula(size2, 1, len(alphabet2)), len(strings2), strings2)
    # the number of strings of length  <= m over an alphabet
    # with n characters is (n^(n+1) - 1) / (n - 1)


def q9():
    data = []
    for i in range(50):
        a = random.randint(1, 101)
        b = random.randint(1, 101)
        data.append([a, b, math.gcd(a, b), gcd(a, b), gcd_recursive(a, b)])
    headers = ["a", "b", "math.gcd", "gcd with PF", "gcd_recursive"]
    title = "Prime Factorization using 3 methods"
    alignments = ["r"] * 5
    print_table(title, headers, data, alignments)


def do_question(q):
    print("question", q.__name__)
    q()
    print()


def main():
    for q in [q1, q2, q3, q4, q5, q6, q7, q8, q9]:
        do_question(q)


if __name__ == "__main__":
    main()
