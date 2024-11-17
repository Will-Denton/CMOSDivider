def divide(A, B):
    """
    Args: 
        A: binary float
        B: binary float
        Both are represented as 1 sign bit, 5 exponent bits, and 6 mantissa bits

    Returns:
        A / B
    
    """
    EXPONENT_OFFSET = 2**4 - 1
    
    sign_A = sign(A)
    sign_B = sign(B)

    sign_result = sign_A ^ sign_B

    exponent_A = exponent(A)
    exponent_B = exponent(B)
    exponent_result_intermediate = exponent_A - exponent_B + EXPONENT_OFFSET

    # mantissa really needs a leading 1
    mantissa_A = mantissa(A)
    mantissa_B = mantissa(B)
    mantissa_A |= 0b1000000
    mantissa_B |= 0b1000000
    mantissa_result_intermediate = int((mantissa_A / mantissa_B) * 2**6)

    print(f"mantissa_A: {mantissa_A}")
    print(f"mantissa_B: {mantissa_B}")
    print(f"mantisa_result_intermediate: {mantissa_result_intermediate}\n")
    print("exponent_result_intermediate: ", exponent_result_intermediate)

    # get MSB
    if not ((mantissa_result_intermediate >> 6) & 0b1):
        mantissa_result_intermediate <<= 1
        exponent_result_intermediate -= 1

    print(f"sign_result: {bin(sign_result)}")
    print(f"exponent_result_intermediate: {bin(exponent_result_intermediate)}")
    print(f"mantissa_result_intermediate: {bin(mantissa_result_intermediate)}\n")

    return (sign_result << 11) | (exponent_result_intermediate << 6) | (mantissa_result_intermediate & 0b111111)

def print_binary(num):
    """
    Args:
        num: binary float
    """
    EXPONENT_OFFSET = 2**4 - 1

    si = sign(num)
    expo = exponent(num)
    mant = mantissa(num)

    if si == 1:
        print("-", end="")
    
    real_exponent = (expo - EXPONENT_OFFSET)
    real_decimal = 1 + (mant / 2**6)
    real_num = real_decimal * 2**real_exponent
    print(f"{real_num:.3f}")

def sign(num):
    """
    Args:
        num: binary float
    Returns:
        sign bit of num
    """
    return num >> 11

def exponent(num):
    """
    Args:
        num: binary float
    Returns:
        exponent of num
    """
    return (num >> 6) & 0b11111

def mantissa(num):
    """
    Args:
        num: binary float
    Returns:
        mantissa of num
    """
    return num & 0b111111


if __name__ == "__main__":
    A = 0b110001111000 #0 10001 111000
    B = 0b010001100000 #1 10001 100000

    # print("{:01b}".format(sign(A)), end=" ")
    # print("{:05b}".format(exponent(A)), end=" ")
    # print("{:06b}".format(mantissa(A)))

    print_binary(A)
    print_binary(B)

    S = divide(A, B)
    print_binary(S)
    print(bin(S))