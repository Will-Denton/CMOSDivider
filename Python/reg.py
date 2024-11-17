def ones(n):
    return (1<<n)-1

# this class simulates an n-bit register
# most operators are supported, and you can mix plain integers and Regs and it will do something reasonable
class Reg:
    def __init__(self, width, n=0):
        self.width = width
        self.value = n & ones(width)

    def __int__(self):
        return self.value # gives the int as unsigned (since no zero extension)

    def __str__(self):
        return f"Reg{self.width}({self.bin()})"
        
    def int_signed(self):
        if self.value >= (1 << (self.width - 1)):
            # If the value is negative or zero, use two's complement representation
            return self.value - (1 << self.width)
        else:
            return self.value        

    def promote(self, other):
        if isinstance(other, int):
            return Reg(max(self.width, other.bit_length()), other)
        elif isinstance(other, Reg):
            return Reg(max(self.width, other.width), other.value)
        else:
            raise ValueError("Invalid operand")

    def resize(self, new_width):
        if isinstance(new_width, int):
            return Reg(new_width, self.value)
        else:
            raise ValueError("Invalid operand")

    def resize_signed(self, new_width):
        if isinstance(new_width, int):
            return Reg(new_width, self.int_signed())
        else:
            raise ValueError("Invalid operand")

    def __add__(self, other):
        other = self.promote(other)
        result = self.value + other.value
        return Reg(max(self.width, other.width), result)

    def __sub__(self, other):
        other = self.promote(other)
        result = self.value - other.value
        return Reg(max(self.width, other.width), result)

    def __mul__(self, other):
        other = self.promote(other)
        result = self.value * other.value
        return Reg(max(self.width, other.width), result)

    def __floordiv__(self, other):
        other = self.promote(other)
        if other.value == 0:
            raise ZeroDivisionError("Division by zero")
        result = self.value // other.value
        return Reg(max(self.width, other.width), result)

    def __mod__(self, other):
        other = self.promote(other)
        if other.value == 0:
            raise ZeroDivisionError("Modulo by zero")
        result = self.value % other.value
        return Reg(max(self.width, other.width), result)

    def __eq__(self, other):
        other = self.promote(other)
        return self.value == other.value

    def __ne__(self, other):
        other = self.promote(other)
        return self.value != other.value

    def __lt__(self, other):
        other = self.promote(other)
        return self.value < other.value

    def __le__(self, other):
        other = self.promote(other)
        return self.value <= other.value

    def __gt__(self, other):
        other = self.promote(other)
        return self.value > other.value

    def __ge__(self, other):
        other = self.promote(other)
        return self.value >= other.value

    def __and__(self, other):
        other = self.promote(other)
        result = self.value & other.value
        return Reg(max(self.width, other.width), result)

    def __or__(self, other):
        other = self.promote(other)
        result = self.value | other.value
        return Reg(max(self.width, other.width), result)

    def __xor__(self, other):
        other = self.promote(other)
        result = self.value ^ other.value
        return Reg(max(self.width, other.width), result)

    def __lshift__(self, other):
        other = self.promote(other)
        result = self.value << other.value
        return Reg(max(self.width, other.width), result)

    def __rshift__(self, other):
        other = self.promote(other)
        result = self.value >> other.value
        return Reg(max(self.width, other.width), result)

    def __neg__(self):
        return Reg(self.width, -self.value)

    def __invert__(self):
        return Reg(self.width, ~self.value)
        
    # return individual bits or ranges of bits using subscript:
    #   r[0] is LSB of r as an int
    #   r[1:3] is bits 3 down to 1 of r as a Reg
    # read-only, setting not supported
    def __getitem__(self, index):
        if isinstance(index, int):
            if 0 <= index < self.width:
                mask = 1 << index
                return (self.value & mask) >> index
            elif -self.width <= index < 0:
                return self[self.width+index] # reverse lookup support
            else:
                raise IndexError("Bit index out of range")
        elif isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step
            if start is None:
                start = 0
            if stop is None:
                stop = self.width
            if step is None:
                step = 1

            if 0 <= start < self.width and 0 <= stop <= self.width:
                result = 0
                for i in range(start, stop, step):
                    mask = 1 << i
                    result |= (self.value & mask) >> i << (i - start)
                return Reg(stop - start, result)
            else:
                raise IndexError("Bit slice index out of range")
        else:
            raise TypeError("Invalid index type")        
            
    # arithmetic shift right
    # native shifts << and >> are also supported, but are logical shifts
    def asr(self, n):
        if n < 0:
            raise ValueError("Shift amount must be non-negative")

        result = self.value >> n
        sign_extension_mask = ((1 << n) - 1) << (self.width - n)

        if self.value & (1 << (self.width - 1)):
            # If the sign bit is set, extend with 1s
            result |= sign_extension_mask
        else:
            # If the sign bit is not set, extend with 0s
            result &= ~sign_extension_mask

        return Reg(self.width, result)
        
    # separate this Reg into two smaller ones, with lo getting bits many bits, and hi getting the rest
    # returns a tuple of hi,lo
    def split(self,bits):
        hi = self[bits:]
        lo = self[0:bits]
        return hi,lo
        
    # takes the given Reg lo and concatenates its bits to self, making a new Reg of width equal to the sum of self and lo
    def concatenate(self,lo):
        return self.resize(self.width+lo.width)<<lo.width | lo

        
    def copy(self):
        return Reg(self.width, self.value)
        
    # generate binary string representation
    def bin(self):
        return format(self.value, f'0{self.width}b')
        
    def __bool__(self):
        return self.value != 0        
        
# Example usage:
if __name__ == "__main__":
    reg1 = Reg(8, 5)
    reg2 = Reg(16, 3)

    # Using built-in operators
    result1 = reg1 + reg2
    print(result1)  # Output: Reg(16, 8)

    # Bitwise operations
    result3 = reg1 & reg2
    print(result3)  # Output: Reg(16, 1)

    # Shift operations
    result4 = reg1 << 2
    print(result4)  # Output: Reg(16, 20)

    print("--")
    r = Reg(4,5)
    print(r,r.int_signed(),r.bin())
    r = -r
    print(r,r.int_signed(),r.bin())
    r = r.asr(1)
    print(r,r.int_signed(),r.bin())
    r <<= 1
    print(r,r.int_signed(),r.bin())
    print(r[0], r[1], r[-1], r[0:2])
    if r==0b1010:
        print(f"{r} yah")
