def read_input():
    a = int(input("Supply first operand: "))
    op = input("Supply operator (+, -, *, /): ")
    b = int(input("Supply second operand: "))

    print("")

    return a, b, op


def to_binary(n, bits):
    negative = True if n < 0 else False
    binary = ""

    n = abs(n)

    while n > 0:
        b = n % 2
        n = n // 2

        binary += str(b)

    binary += "0" * (bits - 1 - len(binary))  # zero pad until 15 bits

    binary += "1" if negative else "0"

    binary = binary[::-1]  # reverse string

    return binary


def add(a, b):
    print("Executing addition...")

    res = ""
    carry = 0

    if a[0] == b[0]:  # if same sign
        print("Operands of same sign - trivial addition")

        for i in range(len(a) - 1, 0, -1):  # loop bits from right to left except sign bit
            tmp = int(a[i]) + int(b[i]) + carry

            if tmp > 1:
                res += "0" if tmp == 2 else "1"  # tmp is either 2 or 3 (10 or 11), so store 2nd bit
                carry = 1
            else:
                res += str(tmp)
                carry = 0

        res += a[0]  # repeat sign bit
        res = res[::-1]
    else:  # if one number negative and other positive
        print("Operands of opposite signs")

        # checks for larger magnitude number
        for i in range(1, len(a)):
            if a[i] != b[i]:
                # create absolute copies of a and b to pass to subtract function
                a_abs = "0" + a[1:]
                b_abs = "0" + b[1:]

                if a[i] == "1":  # a is larger
                    print("a is of largest magnitude - subtract b from a (absolute values) and repeat sign bit from a")

                    res = subtract(a_abs, b_abs)
                    res = a[0] + res[1:]  # repeat sign bit from a
                else:
                    print("b is of largest magnitude - subtract a from b (absolute values, b is passed as a and vice-versa) and repeat sign bit from b")

                    res = subtract(b_abs, a_abs)
                    res = b[0] + res[1:]

                break
        else:  # both numbers have the same magnitude
            print("Operands of same magnitude, result is zero (trivial)")
            res = 0


    return res


def subtract(a, b):
    print("Executing subtraction...")

    res = ""
    carry = 0

    # magnitude check
    for i in range(1, len(a)):
        if a[i] != b[i]:
            if a[i] == "1":
                largest = "a"
            else:
                largest = "b"

            print(f"{largest} is of largest magnitude")

            break
    else:
        largest = "a"

        print("Operands of same magnitude - treating a as largest anyway")

    if a[0] == b[0]:
        print("Operands of same sign")

        # if b > a, then subtract a from b and make result negative
        if largest == "b":
            print("subtracting a from b and making result negative")

            tmp = a
            a = b
            b = tmp
            sign = "1"
        else:
            print("subtracting b from a and making result positive")

            sign = "0"

        # if both operands are negative, invert result's sign
        if a[0] == "1":
            print("Both operands are negative - inverting result's sign")

            sign = "1" if sign == "0" else "0"

        for i in range(len(a) - 1, 0, -1):
            tmp = int(a[i]) - int(b[i]) - carry  # carry in

            if tmp < 0:
                tmp += 2  # carry out
                carry = 1  # carry in for next bit
            else:
                carry = 0

            res += str(tmp)

        res += sign
        res = res[::-1]
    else:
        print("Operands of opposite signs - adding a and b (absolute values) and repeating sign bit from a")

        a_abs = a
        b_abs = b
        a_abs = "0" + a[1:]
        b_abs = "0" + b[1:]

        res = add(a_abs, b_abs)
        res = a[0] + res[1:]

    return res


def multiply(q, m):
    print("Executing multiplication...")

    # check if q or m is zero
    if q == "0" * 16 or m == "0" * 16 or q == "1" + "0" * 15 or m == "1" + "0" * 15:
        print("At least one operand is zero, result is zero (trivial)")

        return "0" * 16

    if q[0] == m[0]:
        print("Operands of same sign, result will be positive")
        res_sign = "0"
    else:
        print("Operands of opposite signs, result will be negative")
        res_sign = "1"

    # ignore sign bits
    q = q[1:]
    m = m[1:]

    c = "0"
    a = "0" * 15
    print("\n---Initial values---")
    print(f"c: {c}")
    print(f"a: {a}")
    print(f"q: {q}")
    print(f"m: {m}")

    for i in range(len(q), 0, -1):  # loops q from right to left
        print(f"\n---Cycle {len(q) + 1 - i}---")

        if q[len(q) - 1] == "1":  # least significant bit in q (q0)
            # c,a = a + m
            print("(q0 = 1)\nc,a receiving a + m")
            r = add("0" + a, "0" + m)
            c = r[0]
            a = r[1:]

            print(f"c: {c}")
            print(f"a: {a}\n")
        else:
            print("(q0 = 0)")

        # right shift c,a,q
        print("Right-shifting c,a,q")
        q = a[len(a) - 1] + q[:-1]
        a = c + a[:-1]
        c = "0"

        print(f"c: {c}")
        print(f"a: {a}")
        print(f"q: {q}")
        print(f"m: {m}")

    res = res_sign + a + q

    return res


def divide(d, v):
    print("Executing division...")

    # check if v is zero
    if v == "0" * 16 or v == "1" + "0" * 15:
        if d == "0" * 16 or d == "1" + "0" * 15:
            print("d and v are zero, result is indeterminate (trivial)")

            return "Indeterminate"
        else:
            print("v is zero, can't divide")

            return "Undefined"

    if d[0] == v[0]:
        print("Operands of same sign, result will be positive")
        res_sign = "0"
    else:
        print("Operands of opposite signs, result will be negative")
        res_sign = "1"

    print(f"Remainder will have the same sign as d ({d[0]})")
    rem_sign = d[0]

    # ignore sign bits
    d = d[1:]
    v = v[1:]

    # magnitude check
    for i in range(1, len(d)):
        if d[i] != v[i]:
            if d[i] == "1":
                largest = "d"
            else:
                largest = "v"

            break
    else:
        largest = "d"

    q = "0" * len(d)

    # division
    while largest == "d":
        print("\nd is not less than v")

        d = subtract(d, v)
        q = add(q, "0" * (len(d) - 1) + "1")  # increment

        # magnitude check
        for i in range(1, len(d)):
            if d[i] != v[i]:
                if d[i] == "1":
                    largest = "d"
                else:
                    largest = "v"

                break
        else:
            largest = "d"

    print("\nd is less than v")
    print(f"Remainder: {rem_sign + d}")

    return res_sign + q


a, b, op = read_input()

a = to_binary(a, bits=16)
b = to_binary(b, bits=16)
print(f"a: {a}")
print(f"b: {b}")
print("")

if op == "+":
    res = add(a, b)
if op == "-":
    res = subtract(a, b)
if op == "*":
    res = multiply(a, b)
if op == "/":
    res = divide(a, b)

print(f"\nResult: {res}")
