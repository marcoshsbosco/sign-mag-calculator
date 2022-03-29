def read_input():
    a = int(input("Supply first operand: "))
    op = input("Supply operator (+, -, *, /): ")
    b = int(input("Supply second operand: "))

    print("")

    return a, b, op


def is_zero(a, b):
    return True if a == 0 or b == 0 else False


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
    res = ""
    carry = 0

    if a[0] == b[0]:  # if same sign
        for i in range(len(a) - 1, 0, -1):  # loop bits from right to left except sign bit
            tmp = int(a[i]) + int(b[i]) + carry

            if tmp > 1:
                res += "0" if tmp == 2 else "1"
                carry = 1
            else:
                res += str(tmp)
                carry = 0

        res += a[0]  # repeat sign bit
        res = res[::-1]
    else:  # if one number negative and other positive
        # checks for larger magnitude number
        for i in range(1, len(a)):
            if a[i] != b[i]:
                # create absolute copies of a and b to pass to subtract function
                a_abs = "0" + a[1:]
                b_abs = "0" + b[1:]

                if a[i] == "1":  # a is larger
                    res = subtract(a_abs, b_abs)
                    res = a[0] + res[1:]  # repeat sign bit from a
                else:
                    res = subtract(b_abs, a_abs)
                    res = b[0] + res[1:]

                break
        else:  # both numbers have the same magnitude
            res = 0


    return res


def subtract(a, b):
    res = ""
    carry = 0

    # magnitude check
    for i in range(1, len(a)):
        if a[i] != b[i]:
            if a[i] == "1":
                largest = "a"
            else:
                largest = "b"

            break
    else:
        largest = "a"

    if a[0] == b[0]:
        # if b > a, then subtract a from b and make result negative
        if largest == "b":
            tmp = a
            a = b
            b = tmp
            sign = "1"
        else:
            sign = "0"

        # if both operands are negative, invert result's sign
        if a[0] == "1":
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
        a_abs = a
        b_abs = b
        a_abs = "0" + a[1:]
        b_abs = "0" + b[1:]

        res = add(a_abs, b_abs)

    return res


a, b, op = read_input()

a = to_binary(a, bits=16)
b = to_binary(b, bits=16)
print(f"a: {a}")
print(f"b: {b}")

if op == "+":
    res = add(a, b)
if op == "-":
    res = subtract(a, b)

print(f"Result: {res}")
