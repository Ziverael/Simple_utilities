#!/usr/bin/env python

import sys
import math
"""
Module include few functions which deals with finding Pythagorean triples with condition a + b + c = value.
Each of these functions get value which is unsigned  integer and return tuple (found, a, b, c, op).

found - if exists triple that fulfil given condition
a, b, c - values of the triple; if triple doesn' t exists they are equal -1
op - operations number

For that problem assume that every operation is +, -, *, /, condition check
Absolute value of a complex number is counted as 4 operations,
"""

def brute(value):
    """
    Brute force finding of triples. Generate all combinations of (a,b,c) where each is from range [1,value).
    Then check condition if it is a Pythagorean triple and if a + b + c = value.
    """

    try:
        value = int(value)
        if value < 1:
            raise ValueError("Value must be positive")
    except:
        raise TypeError

    op = 0
    for a in range(1, value):
        for b in range(1, value):
            for c in range(1, value):
                op += 9
                if a * a + b * b == c * c and a + b + c == value:
                    return (True, a, b, c, op)
    return(False, -1, -1, -1, op)

def brute_vol2(value):
    """
    Brute force finding of triples. Generate all combinations of (a,b,c) where each is from range [1,value // 2).
    Then check condition if it is a Pythagorean triple and if a + b + c = value.
    """

    try:
        value = int(value)
        if value < 1:
            raise ValueError("Value must be positive")
    except:
        raise TypeError
    
    op = 0
    for a in range(1, value // 2):
        for b in range(1, value // 2):
            for c in range(1, value // 2):
                op += 9
                if a * a + b * b == c * c and a + b + c == value:
                    return (True, a, b, c, op)
    return(False, -1, -1, -1, op)


def one_factor_elimination(value):
    """
    Generate (b,c) where each is from range [1, value // 2). a is calculated from expression a + b + c = value.
    Finally check if is (a, b, c) a Pythagorean triple.
    """
    
    try:
        value = int(value)
        if value < 1:
            raise ValueError("Value must be positive")
    except:
        raise TypeError
    
    op = 0
    for b in range(1, value // 2 ):
        for c in range(b + 1, value // 2 + 1):
            #print(b ,c)
            #if b == 4 and c == 5:
            #    print(math.sqrt((c - b) * (c + b)))
            op += 10
            if value == b + c + math.sqrt((c - b) * (c + b)):
                a = value - b - c
                return (True, a, b, c, op)
    return(False, -1, -1, -1, op)

def pythagorean_from_imagine(value):
    """
    Generate Pythagorean triples such that (a, b, c) = (Re(x), Im(x), abs(x)), while x = a + b * j
    and check if condition a + b + c = value is fulfiled.
    """
    
    try:
        value = int(value)
        if value < 1:
            raise ValueError("Value must be positive")
    except:
        raise TypeError
    
    op = 0
    for a in range(1, value // 2):
        for b in range(a, value // 2 +1):
            if a == b:
                op += 1
                continue
            op += 12
            compl = a + b*1j
            
            c = abs(compl)

            if a + b + c == value:
                return (True, a, b, int(c), op)
    return(False, -1, -1, -1, op)

def euclid_formula(value):
    """
    Generate pythagorean triples from such that (a, b, c) = (2 * m * n * k, k * (m * m - n * n), k * (m * m + n * n))
    and check if a + b + c = value.
    """
    
    try:
        value = int(value)
        if value < 1:
            raise ValueError("Value must be positive")
    except:
        raise TypeError
    
    op = 3

    m, n ,k= 2, 1, 1
    while 2 * m * (n + m) <= value:
        buff = 2 * m * (n + m)
        while buff * k < value:
            k += 1
            op += 3

        if buff * k == value:
            op += 1
            return (True, 2 * m * n * k, k * (m * m - n * n), k * (m * m + n * n), op)
        k = 1
        m += 1
        op += 9
        if m > value /(2 * (n + m)):
            n += 1
            m = n + 1
            op += 4
    return (False, -1, -1, -1, op)


def test(n, print_only_tris = False):
    """
    Test module functions on values from range [1,n], where n >= 1.

    ARGS
    ----
    n - [int] number of tries
    print_only_tris - [bool] print only Pythagorean Triples
    """
    for i in range(1, n + 1):
        buffer = brute(i)
        if print_only_tris:
            if not buffer[0]:
                continue
        print("a + b + c = {}".format(i))
        print(buffer)
        print(brute_vol2(i))
        print(pythagorean_from_imagine(i))
        print(euclid_formula(i))
        print(one_factor_elimination(i))

def main(args):
    if len(args) == 1:
        test(200)
    if len(args) in (2, 3):
        try:
            n = int(args[1])
            if n <= 0:
                raise ValueError("Test number must be positive value")
        except:
            raise TypeError("Expected integer")
        if len(args) == 3:
            try:
                boolean = bool(args[2])
            except:
                raise TypeError("Expected boolean")
            test(n, boolean)
        else:
            test(n)



if __name__ == "__main__":
    main(sys.argv)

