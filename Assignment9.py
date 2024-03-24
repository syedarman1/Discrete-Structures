
import inspect
import pandas as pd
from itertools import product
import numpy as np
from math import log, sqrt
import random
import texttable
import Assignment8 as as8

dict_funcs = {}


def func_name(func):
    return func.__name__ + " " + as8.func_body(func)


def compute_values(funcs, inputs):
    dict_f = {}
    for func in funcs:
        funcName = func_name(func)
        dict_f[funcName] = {}
        for n in inputs:
            val = func(func, n)
            log_val = 0 if val <= 0 else log(val, 10)
            dict_f[funcName][n] = log_val
    return dict_f


# evaluate recursive function
def ff(f, n):
    n = int(n)
    func_name = f.__name__
    if func_name not in dict_funcs:
        dict_funcs[func_name] = {}
    dict_func = dict_funcs[func_name]
    if n not in dict_func:
        dict_func[n] = f(f, n)
    return dict_func[n]


# [1] Define a function to parse a linear homogeneous recurrence and extract both its initial conditions and
# coefficients
def get_sides(eqn):
    parts = eqn.split("=")
    return parts[0].strip(), parts[1].strip()


def get_rhs(eqn):
    return get_sides(eqn)[1]  # 1 gets the rhs


def parse_recurrence(recurrence):
    var = recurrence.strip()[0]
    parts = recurrence.split(",")
    f_0 = float(get_rhs(parts[0]))
    f_1 = float(get_rhs(parts[1]))
    f_n = get_rhs(parts[2])
    idx1 = f_n.find(var)
    temp1 = f_n[:idx1].strip()
    c1 = 1 if temp1 == "" else float(temp1)
    idx2 = f_n.find(")")
    idx3 = f_n.find(var, idx2 + 1)
    temp2 = f_n[idx2 + 1:idx3].replace(" ", "").strip()
    c2 = 1 if temp2 == "+" or temp2 == "-" else float(temp2)
    return var, f_0, f_1, c1, c2


# [2] Define a function to reconstruct the recurrence from the parameters and print the recurrence in standard form.
def reconstruct_recurrence(var, a0, a1, c1, c2):
    recurrence = f"{var}(0) = {a0}, {var}(1) = {a1}, {var}(n) = {c1} {var}(n-1) + {c2} {var}(n-2)"
    return recurrence


# [3] Define a function to determine and print the characteristic equation for the recurrence
# [4] Define a function to find the root(s) of the characteristic equation
def solve_characteristic_equation(c1, c0):
    characteristic_equation = "r^2 - " + ("" if c1 == 1 else str(c1)) + "r - " + str(c0)
    a = 1
    b = -1 * c1
    c = -1 * c0
    temp = sqrt(b ** 2 - 4 * a * c)
    r1 = ((-1 * b) + temp) / (2 * a)
    r2 = ((-1 * b) - temp) / (2 * a)
    return characteristic_equation, r1, r2


# [5] Define a function to determine the coefficients of those roots in the solution. Make sure to handle both the case
# of distinct and duplicate roots.
def coefficients_of_roots(r1, r2, a0, a1):
    distinct = r1 != r2
    A = np.array([[r1 ** 0, (0 if not distinct else 1) * r2 ** 0], [r1 ** 1, (1 if not distinct else 1) * r2 ** 1]])
    B = np.array([a0, a1])
    X = np.linalg.solve(A, B)
    return X[0], X[1]


# [6] Define a function to display the closed-form formula using the results of the previous tasks
def closed_form_formula(r1, r2, t1, t2, distinct):
    return f"a(n) = {t1} * {r1} ^n + {t2} * {'n*' if not distinct else ''} {r2} ^n"


def evaluate_a2(c1, c2, a1, a0, t1, t2, r1, r2, distinct):
    a2_recurrence = c1 * a1 + c2 * a0
    a2_formula = t1 * r1 ** 2 + t2 * (2 if not distinct else 1) * r2 ** 2
    return a2_recurrence, a2_formula


# [7] For several different linear homogeneous recurrences,
# print the recurrence
# print the context in which it arises (e.g. slide or website)
# solve the recurrence
# evaluate the recurrence (use code from previous assignment and compare  with closed form)
# plot the value


# [8] Collect the output for all the functions and present it in a table,
# Use this code as a starting point for some of the tasks above.
def solve_recurrence(desc, c1, c0, a0, a1):
    print(desc)
    recurrence = "a(n) = " + str(c1) + "*a(n-1) + " + str(c0) + "*a(n-2)"
    print("The recurrence is", recurrence)
    characteristic_equation = "r^2 - " + ("" if c1 == 1 else str(c1)) + "r - " + str(c0)
    print("characteristic equation is", characteristic_equation)
    a = 1
    b = -1 * c1
    c = -1 * c0
    temp = sqrt(b ** 2 - 4 * a * c)
    r1 = ((-1 * b) + temp) / (2 * a)
    r2 = ((-1 * b) - temp) / (2 * a)
    print("The roots are ", r1, r2)
    distinct = r1 != r2
    A = np.array([[r1 ** 0, (0 if not distinct else 1) * r2 ** 0], [r1 ** 1, (1 if not distinct else 1) * r2 ** 1]])
    B = np.array([a0, a1])
    X = np.linalg.solve(A, B)
    print("The coefficients are", X[0], X[1])
    formula = ("a(n) = " + str(X[0]) + "*" + str(r1) + "^n" + " + " + str(X[1]) + "*" + (
        "n*" if not distinct else "") + str(r2) + "^n")
    print("The closed-form formulas is", formula)
    a2_recurrence = c1 * a1 + c0 * a0
    a2_formula = X[0] * r1 ** 2 + X[1] * (2 if not distinct else 1) * r2 ** 2
    print("a2_recurrence", a2_recurrence)
    print("a2_formula", a2_formula)
    print()


def process_recurrence(data, desc, recurrence, n, func, verbose=False):
    var, a0, a1, c1, c2 = parse_recurrence(recurrence)
    new_recurrence = reconstruct_recurrence(var, a0, a1, c1, c2)
    characteristic_equation, r1, r2 = solve_characteristic_equation(c1, c2)
    t1, t2 = coefficients_of_roots(r1, r2, a0, a1)
    distinct = r1 != r2
    formula = closed_form_formula(r1, r2, t1, t2, distinct)
    a2_recurrence, a2_formula = evaluate_a2(c1, c2, a1, a0, t1, t2, r1, r2, distinct)
    a_n = ff(func, n)
    log_val = 0 if a_n <= 0 else log(a_n, 10)
    if verbose:
        print()
        print("Description", desc)
        print("Old recurrence", recurrence)
        print("New recurrence", new_recurrence)
        print("The characteristic equation is", characteristic_equation)
        print("The roots are", r1, r2)
        print("The coefficients are", t1, t2)
        print("The closed  formula is", formula)
        print("a(2) using recurrence is", a2_recurrence)
        print("a(2) using formula is", a2_formula)
        print("a(n) computed recursively is", a_n)
        print()
    name = func.__name__
    syntax = as8.func_body(func)
    data.append([name, desc, recurrence, new_recurrence, syntax, characteristic_equation, formula, a_n, log_val])


def process_recurrences(recurrences, n, verbose=False):
    data = []
    for r in recurrences:
        desc, recurrence, func = r
        process_recurrence(data, desc, recurrence, n, func, verbose)
    return data


def prepare_output(data, n, ranked=False):
    print()
    if ranked:
        data = sorted(data, key=lambda l: l[-1])
    title = f"Linear Homogenous Recurrences for n={n}"
    heads = ["Name", "Description", "Recurrence", "New Recurrence", "Function Syntax", "Characteristic Equation",
             "Formula", "Value", "Log Value"]
    align = ["l", "l", "l", "l", "l", "l", "l", "r", "r"]
    as8.print_table(title, heads, data, align)


# fibonacci
def f1(f, n):
    return 0 if n == 0 else (1 if n == 1 else ff(f1, n - 1) + ff(f1, n - 2))


def f2(f, n):
    return 2 if n == 0 else (7 if n == 1 else ff(f2, n - 1) + 2 * ff(f2, n - 2))


def f3(f, n):
    return 1 if n == 0 else (6 if n == 1 else 6 * ff(f3, n - 1) - 9 * ff(f3, n - 2))


def f4(f, n):
    return 2 if n == 0 else (3 if n == 1 else 4 * ff(f4, n - 1) - 6 * ff(f4, n - 2))


def f5(f, n):
    return 1 if n == 0 else (2 if n == 1 else 12 * ff(f5, n - 1) - 27 * ff(f5, n - 2))


def f6(f, n):
    return 6 if n == 0 else (7 if n == 1 else 9 * ff(f6, n - 1) - 8 * ff(f6, n - 2))


def f7(f, n):
    return 3 if n == 0 else (4 if n == 1 else 2 * ff(f7, n - 1) + 3 * ff(f7, n - 2))



def main():
    n = 2
    recurrences = [
        ("fibonacci", "f(0) = 0, f(1) = 1, f(n) = f(n-1)+f(n-2)", f1),
        ("Ch8, slide 22", "f(0) = 2, f(1) = 7, f(n) = f(n-1)+2f(n-2)", f2),
        ("Ch8, slide 26", "f(0) = 1, f(1) = 6, f(n) = 6f(n-1)-9f(n-2)", f3),
        ("Rec Doc, Ex9", "f(0) = 2, f(1) = 3, f(n) = 5f(n-1)-6f(n-2)", f4),
        ("Rec Doc, Ex", "f(0) = 1, f(1) = 2, f(n) = 12f(n-1)-27f(n-2)", f5),
        ("Summer 2023 Exam", "f(0) = 6, f(1) = 7, f(n) = 9f(n-1)-8f(n-2)", f6),
        ("Custom Recurrence", "f(0) = 3, f(1) = 4, f(n) = 2f(n-1)+3f(n-2)", f7)

    ]
    data = process_recurrences(recurrences, n, True)
    prepare_output(data, n)
    inputs = [i for i in range(n + 1)]
    funcs = [recurrence[2] for recurrence in recurrences]
    dict_funcs2 = as8.compute_values(funcs, inputs)
    as8.plot_values("Assignment9.png", dict_funcs2, inputs, funcs)


if __name__ == '__main__':
    main()
