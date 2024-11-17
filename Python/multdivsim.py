#!/usr/bin/python3

## Compute signed integer multiplication and division via multiple algorithms,
## printing colorized progress along the way.
## By Tyler Bletsch for Duke ECE 350.
## 
## History:
##   2023-09-30  Intial public release
##

from reg import Reg # custom library to simulate n-bit registers
import argparse

def bitsplit(r,bits):
    assert False
    hi = r[bits:]
    lo = r[0:bits]
    return hi,lo
    
def bitmerge(hi,lo):
    assert False
    return hi.resize(hi.width+lo.width)<<lo.width | lo

COLOR_R = "\033[31;91m"
COLOR_G = "\033[32;92m"
COLOR_SEL = "\033[43;48;5;226m"
COLOR_RESET = "\033[m"

def colorize(s,color,first,last):
    p_first = len(s)-first
    p_last = len(s)-last
    return s[0:p_first] + color + s[p_first:p_last] + COLOR_RESET

def naive_mult(m,r,bits=4):
    m_orig = m
    r_orig = r
    m = Reg(bits,m)
    r = Reg(bits,r)
    r_neg = r[-1]

    print(f"  {m} = {m_orig}")
    print(f"x {r} = {r_orig}")
    print("")
    if r_neg:
        r = -r
        print(f"* Negating the multiplier to {r}")
        print("")
    out = r.resize(2*bits)
    b = bits
    out_fmt = colorize(out.bin(),COLOR_R,b,0)
    print(f"{'Init':14s} {out_fmt}")
    lefthole = 0
    while b>0:
        step = ""
        if out&1:
            step = "Add? yes"
            hi,lo = out.split(bits)

            hi = hi.resize(bits+1)
            hi = (hi + m)
            lefthole = hi[-1] # catch the "extra" bit on the left side for later shifting
            hi = hi.resize(bits)
            
            out = hi.concatenate(lo)
        else:
            step = "Add? no"
            lefthole=0
        out_fmt = colorize(out.bin(),COLOR_R,b,0)
        print(f"{step:14s} {out_fmt}")
        if m_orig>0:
            step = "Log Shift"
            out = out>>1
        else:
            step = "Arith Shift"
            out = out.asr(1)
        
        # okay, so in naive multiplication, there's a little issue where we lose the sign bit sometimes and need to patch it back in
        # in an actual implementation, you'd probably have an extra bit in the product register
        # i'm manually patching it up since i discovered this organically
        # i could fix a more elegant solution, but nobody's implementing naive algo, so I'm not
        if lefthole:
            if not out[-1]:
                print("NEEDED to patch left hole")
            out |= lefthole<<(2*bits-1)
        b -= 1
        out_fmt = colorize(out.bin(),COLOR_R,b,0)
        print(f"{step:14s} {out_fmt}")
    if r_neg:
        out = -out
        print(f"{'Negate':14s} {out.bin()}")
    print(f"{'':14s} = {out.int_signed()}")
    return out.int_signed()
    
def booth_mult(m,r,bits=4):
    m_orig = m
    r_orig = r
    m = Reg(bits,m)
    r = Reg(bits,r)

    print(f"  {m} = {m_orig}")
    print(f"x {r} = {r_orig}")
    print("")
    
    out = r.resize(2*bits)
    hole = 0 # the extra bit to the right, starts at 0
    b = bits
    out_fmt = colorize(out.bin(),COLOR_R,b,0)
    print(f"{'Init':14s} {out_fmt} {hole}")
    while b>0:
        step = ""
        picker = (out&1)<<1  |  hole
        if picker==0b00 or picker==0b11:
            step = "Add/sub? no"
        elif picker==0b10:
            step = "Add/sub? sub"
            hi,lo = out.split(bits)
            hi = (hi - m)
            out = hi.concatenate(lo)
        elif picker==0b01:
            step = "Add/sub? add"
            hi,lo = out.split(bits)
            hi = (hi + m)
            out = hi.concatenate(lo)
        else:
            raise Exception("impossible")
        out_fmt = colorize(out.bin(),COLOR_R,b,0)
        print(f"{step:14s} {out_fmt} {hole}")
        step = "Shift"
        hole = int(out&1)
        out = out.asr(1)
        b -= 1
        out_fmt = colorize(out.bin(),COLOR_R,b,0)
        print(f"{step:14s} {out_fmt} {hole}")
    print(f"{'':14s} = {out.int_signed()}")
    return out.int_signed()

# this one has signed inaccuracy when 2*m overflows
def modbooth_mult(m,r,bits=4):
    if bits%2 != 0:
         raise ValueError(f"Modified booth requires bit-width to be a multiple of 2. Width {bits} was provided.")
    
    m_orig = m
    r_orig = r
    m = Reg(bits,m)
    r = Reg(bits,r)

    print(f"  {m} = {m_orig}")
    print(f"x {r} = {r_orig}")
    print("")
    
    out = r.resize(2*bits)
    hole = 0 # the extra bit to the right, starts at 0
    b = bits
    out_fmt = colorize(out.bin(),COLOR_R,b,0)
    print(f"{'Init':14s} {out_fmt} {hole}")
    while b>0:
        step = ""
        picker = (out&0b11)<<1  |  hole
        if picker==0b000 or picker==0b111:
            step = "Add/sub? no"
        elif picker==0b100:
            step = "Add/sub? -2m"
            hi,lo = out.split(bits)
            hi = (hi - (m<<1))
            out = hi.concatenate(lo)
        elif picker==0b010:
            step = "Add/sub? +m"
            hi,lo = out.split(bits)
            hi = (hi + m)
            out = hi.concatenate(lo)
        elif picker==0b110:
            step = "Add/sub? -m"
            hi,lo = out.split(bits)
            hi = (hi - m)
            out = hi.concatenate(lo)
        elif picker==0b001:
            step = "Add/sub? +m"
            hi,lo = out.split(bits)
            hi = (hi + m)
            out = hi.concatenate(lo)
        elif picker==0b101:
            step = "Add/sub? -m"
            hi,lo = out.split(bits)
            hi = (hi - m)
            out = hi.concatenate(lo)
        elif picker==0b011:
            step = "Add/sub? +2m"
            hi,lo = out.split(bits)
            hi = (hi + (m<<1))
            out = hi.concatenate(lo)
        else:
            raise Exception("impossible")
        out_fmt = colorize(out.bin(),COLOR_R,b,0)
        print(f"{step:14s} {out_fmt} {hole}")
        step = "Shift"
        out = out.asr(1)
        b -= 1
        hole = out[0]
        out = out.asr(1)
        b -= 1
        out_fmt = colorize(out.bin(),COLOR_R,b,0)
        print(f"{step:14s} {out_fmt} {hole}")
    print(f"{'':14s} = {out.int_signed()}")
    return out.int_signed()

# this one uses a "bonus bit" so that 2*m can never overflow
def modbooth_mult2(m,r,bits=4):
    if bits%2 != 0:
         raise ValueError(f"Modified booth requires bit-width to be a multiple of 2. Width {bits} was provided.")
    
    m_orig = m
    r_orig = r
    m = Reg(bits,m)
    r = Reg(bits,r)
    dm = m.resize_signed(bits+1)

    print(f"  {m} = {m_orig}")
    print(f"x {r} = {r_orig}")
    print("")
    
    out = r.resize(2*bits+1)
    hole = 0 # the extra bit to the right, starts at 0
    b = bits
    out_fmt = colorize(out.bin(),COLOR_R,b,0)
    print(f"{'Init':14s} {out_fmt} {hole}")
    while b>0:
        step = ""
        picker = (out&0b11)<<1  |  hole
        if picker==0b000 or picker==0b111:
            step = "Add/sub? no"
        elif picker==0b100:
            step = "Add/sub? -2m"
            hi,lo = out.split(bits)
            hi = (hi - (dm<<1))
            out = hi.concatenate(lo)
        elif picker==0b010:
            step = "Add/sub? +m"
            hi,lo = out.split(bits)
            hi = (hi + dm)
            out = hi.concatenate(lo)
        elif picker==0b110:
            step = "Add/sub? -m"
            hi,lo = out.split(bits)
            hi = (hi - dm)
            out = hi.concatenate(lo)
        elif picker==0b001:
            step = "Add/sub? +m"
            hi,lo = out.split(bits)
            hi = (hi + dm)
            out = hi.concatenate(lo)
        elif picker==0b101:
            step = "Add/sub? -m"
            hi,lo = out.split(bits)
            hi = (hi - dm)
            out = hi.concatenate(lo)
        elif picker==0b011:
            step = "Add/sub? +2m"
            hi,lo = out.split(bits)
            hi = (hi + (dm<<1))
            out = hi.concatenate(lo)
        else:
            raise Exception("impossible")
        out_fmt = colorize(out.bin(),COLOR_R,b,0)
        print(f"{step:14s} {out_fmt} {hole}")
        step = "Shift"
        out = out.asr(1)
        b -= 1
        hole = out[0]
        out = out.asr(1)
        b -= 1
        out_fmt = colorize(out.bin(),COLOR_R,b,0)
        print(f"{step:14s} {out_fmt} {hole}")
    out = out.resize(2*bits)
    print(f"{'Truncate':14s}  {out.bin()}")
    print(f"{'':14s} = {out.int_signed()}")
    return out.int_signed()

def restore_div(d,v,bits=4):
    d_neg = d<0
    if d_neg: d = -d
    
    v_neg = v<0
    if v_neg: v = -v
    
    d_orig = d
    v_orig = v
    
    d = Reg(bits,d)
    v = Reg(bits,v)
    rq = d.resize(2*bits) # hi=r=0000, lo=q=dividend
    
    if d_neg or v_neg:
        print("Negatives detected: taking absolute value, will patch signs afterward.")
        print("")

    print(f"  {d} = {d_orig}")
    print(f"/ {v} = {v_orig}")
    print("")

    n = bits
    rq_fmt = colorize(rq.bin(),COLOR_G,bits-n,0)
    print(f"{'Init':16s} {rq_fmt}")
    while n>0:
        print(f"n={n}")
        step = "LShift RQ"
        rq <<= 1
        rq_fmt = colorize(rq.bin(),COLOR_G,bits-n,0)
        print(f"{step:16s} {rq_fmt}")
        
        step = "R -= V"
        r,q = rq.split(bits)
        r_classic = r.copy()
        r -= v
        rq = r.concatenate(q)
        rq_fmt = colorize(rq.bin(),COLOR_G,bits-n,0)
        print(f"{step:16s} {rq_fmt}")
        
        msb_r = r[-1]
        if msb_r==0: #0
            step = "Q[0]=1"
            q |= 1 # q[0]=1
        else: #1
            step = "Q[0]=0, restore"
            q &= ~1 # q[0]=0
            r = r_classic
        rq = r.concatenate(q)
        rq_fmt = colorize(rq.bin(),COLOR_G,bits-n+1,0)
        print(f"{step:16s} {rq_fmt}")
        #print("")
        
        n -= 1

    r,q = rq.split(bits)
    if d_neg or v_neg:
        r_neg = d_neg
        q_neg = d_neg ^ v_neg
        
        if r_neg:
            r = -r
        if q_neg:
            q = -q
        step = "Patch signs"
        rq = r.concatenate(q)
        print(f"{step:16s} {rq.bin()}")
        qv = q.int_signed()
        rv = r.int_signed()
    else:
        qv = int(q)
        rv = int(r)
    
    print(f"{'':16s} = {qv} R {rv}")
    return qv,rv
    
def nonrestore_div(d,v,bits=4):
    d_neg = d<0
    if d_neg: d = -d
    
    v_neg = v<0
    if v_neg: v = -v
    
    d_orig = d
    v_orig = v
    d = Reg(bits,d)
    v = Reg(bits,v)
    rq = d.resize(2*bits) # hi=r=0000, lo=q=dividend

    if d_neg or v_neg:
        print("Negatives detected: taking absolute value, will patch signs afterward.")
        print("")
        
    print(f"  {d} = {d_orig}")
    print(f"/ {v} = {v_orig}")
    print("")

    n = bits
    rq_fmt = colorize(rq.bin(),COLOR_G,bits-n,0)
    print(f"{'Init':16s} {rq_fmt}")
    while n>0:
        print(f"n={n}")
        msb_r = rq[-1]
        step = "LShift RQ"
        rq <<= 1
        rq_fmt = colorize(rq.bin(),COLOR_G,bits-n,0)
        print(f"{step:16s} {rq_fmt}")
        
        r,q = rq.split(bits)
        if msb_r==0: #0
            step = "R -= V"
            r -= v
        else: #1
            step = "R += V"
            r += v
        rq = r.concatenate(q)
        
        rq_fmt = colorize(rq.bin(),COLOR_G,bits-n,0)
        print(f"{step:16s} {rq_fmt}")
        
        msb_r = rq[-1]
        if msb_r==0: #0
            step = "Q[0]=1"
            rq |= 1 # q[0]=1
        else: #1
            step = "Q[0]=0"
            rq &= ~1 # q[0]=0
        
        rq_fmt = colorize(rq.bin(),COLOR_G,bits-n+1,0)
        print(f"{step:16s} {rq_fmt}")

        n -= 1

    msb_r = rq[-1]
    r,q = rq.split(bits)
    if msb_r==1:
        step = "R += V (final)"
        r += v
    rq = r.concatenate(q)
    rq_fmt = colorize(rq.bin(),COLOR_G,bits,0)
    print(f"{step:16s} {rq_fmt}")
    
    if d_neg or v_neg:
        r_neg = d_neg
        q_neg = d_neg ^ v_neg
        
        if r_neg:
            r = -r
        if q_neg:
            q = -q
        step = "Patch signs"
        rq = r.concatenate(q)
        print(f"{step:16s} {rq.bin()}")
        qv = q.int_signed()
        rv = r.int_signed()
    else:
        qv = int(q)
        rv = int(r)
    print(f"{'':16s} = {qv} R {rv}")
    return qv,rv
    
algos = {
    'mult-naive': {'func': naive_mult, 'desc': "Naive signed multiplication"},
    'mult-booth': {'func': booth_mult, 'desc': "Classic Booth's signed multiplication"},
    'mult-mbooth': {'func': modbooth_mult, 'desc': "Modified Booth's signed multiplication (no 'bonus bit', has edge case errors, e.g. 6x6 4-bit)"},
    'mult-mbooth-bb': {'func': modbooth_mult2, 'desc': "Modified Booth's signed multiplication with a 'bonus bit'"},
    'div-restore': {'func': restore_div, 'desc': "Restore-method signed division"},
    'div-nonrestore': {'func': nonrestore_div, 'desc': "Non-restore-method signed division"}
}
    
    
class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass
# Create an ArgumentParser object
parser = argparse.ArgumentParser(
    description="Compute signed integer multiplication and division via multiple algorithms, printing colorized progress along the way. By Tyler Bletsch for Duke ECE 350.",
    formatter_class=CustomFormatter,
    epilog="Supported algorithms for -a:\n" + "\n".join(f"  {k:15s}: {algos[k]['desc']}" for k in algos.keys())
)

# Add the command-line arguments
parser.add_argument("-b", metavar="BITS", type=int, help="An integer value for BITS, defaults to 'just big enough'")
parser.add_argument("-a", required=True, choices=algos.keys(), help="Choose the operation and algorithm to do")
parser.add_argument("v1", type=int, help="First operand (multiplicand/dividend)")
parser.add_argument("v2", type=int, help="Second operand (multiplier/divisor)")

# Parse the command-line arguments
args = parser.parse_args()

# Access the parsed values
algo_str = args.a
algo_func = algos[algo_str]['func']
v1 = args.v1
v2 = args.v2
bits = args.b
if not bits:
    bits = max(v1.bit_length()+1, v2.bit_length()+1)

# Now you can use the values in your program
print("BITS:", bits)
print("Algorithm:", algo_str)
print("Operand 1:", v1)
print("Operand 2:", v2)
print("")

algo_func(v1,v2,bits)

#naive_mult(-1,1,4)
#booth_mult(-5,7,4)
#modbooth_mult(5,-6,4)
#modbooth_mult2(5,-6,4)

#restore_div(7,3,4)
#nonrestore_div(7,3,4)

# mult test sweeps, disabled by default
if 0:
    for d in range(0,15+1):
        for v in range(1,7+1):
            q=d//v
            r=d%v
            q1,r1 = restore_div(d,v,4)
            if (q != q1 or r != r1): print(f"RESTORE FAIL: {d}/{v}={q}r{r} but I got {q1}r{r1}")
            q2,r2 = nonrestore_div(d,v,4)
            if (q != q2 or r != r2): print(f"NONRESTORE FAIL: {d}/{v}={q}r{r} but I got {q2}r{r2}")

# div test sweeps, disabled by default
if 0:
    for m in range(-7,7+1):
        for r in range(-7,7+1):
            p = m*r
            p1 = naive_mult(m,r,4)
            if (p != p1): print(f"NAIVE FAIL: {m}*{r}={p} but I got {p1}")
            p2 = booth_mult(m,r,4)
            if (p != p2): print(f"BOOTH FAIL: {m}*{r}={p} but I got {p2}")
            p3 = modbooth_mult2(m,r,4)
            if (p != p3): print(f"MODBOOTH FAIL: {m}*{r}={p} but I got {p3}")
            print("RESULTS",p,p1,p2,p3)
