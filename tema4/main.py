import math
import random
from sympy import legendre_symbol
from sympy.ntheory.modular import crt as sycrt

from Crypto.Util.number import getPrime
from Crypto.Random import get_random_bytes

# shanks algorithm

print("---Shanks algorithm---")

p = getPrime(8, randfunc=get_random_bytes)
# p = 13
beta = random.randint(1, p - 1)
# beta = 11
alfa = random.randint(2, p - 2)
# alfa = 2
# pow(alfa, (p - 1) // 2, p)
while legendre_symbol(alfa, p) != -1:
    alfa = random.randint(2, p - 2)

m = math.ceil(math.sqrt(p - 1))

print("p:", p)
print("beta:", beta)
print("alfa:", alfa)
print("m:", m)

# baby steps
L = []
for j in range(m):
    L.append((len(L), pow(alfa, j, p)))

print("L:", L)
found = False

# giant steps
for i in range(100):
    gst = (beta * pow(alfa, -m * i, p)) % p
    for j in range(m):
        if L[j][1] == gst:
            print("Rezultat:", i * m + j)
            found = True
            break
    if found:
        break


# epsilon = (math.log(beta, alfa)) % p
# i = epsilon // m
# j = epsilon % m

def primeFactorList(n):
    f = []

    for i in range(2, n + 1):
        if n % i == 0:
            f.append([i, 0])
        while n % i == 0:
            f[len(f) - 1][1] += 1
            n /= i

    return f


# silver-pohlig-hellman algorithm
print("\n---Silver-Pohlig-Hellman algorithm---")

# p = 41
print("p:", p)

f = primeFactorList(p - 1)
print("Factorii primi a lui", p - 1, ":", f)

beta = random.randint(1, p - 1)
# beta = 5
alfa = random.randint(2, p - 2)
# alfa = 6
# pow(alfa, (p - 1) // 2, p)
while legendre_symbol(alfa, p) != -1:
    alfa = random.randint(2, p - 2)

print("beta:", beta)
print("alfa:", alfa)

alfa_i = []
co = []
for i in range(len(f)):
    alfa_i.append([pow(alfa, (p - 1) // f[i][0], p), f[i][0]])
    # co.append(math.log(pow(beta, (p-1) // alfa_i[i][1], p), alfa_i[i][0]))

print("alfas:", alfa_i)


def bin_to_dec(num, b):
    pw, r = 1, 0
    while num != 0:
        r += num % 10 * pw
        pw *= b
        num = num // 10
    return r


crt = []
for i in range(len(f)):
    j = 1
    pw = 10
    d_list = []
    s = math.ceil(math.log(pow(beta, (p - 1) // f[i][0], p), alfa_i[i][0]))
    d_list.append(s)
    for j in range(1, f[i][1]):
        sb = int(bin_to_dec(s, f[i][0]))
        bb = pow(beta, (p - 1) // pow(alfa_i[i][1], (j + 1)), p)
        aa = pow(alfa, (p - 1) * (-sb) // pow(alfa_i[i][1], (j + 1)), p)
        s += pw * math.log(pow(bb * aa, 1, p), alfa_i[i][0])
        pw *= 10
        d_list.append(math.ceil(s))
    if f[i][1] == 1:
        crt.append([int(bin_to_dec(s, f[i][0])), pow(alfa_i[i][1], 1)])
    else:
        crt.append([int(bin_to_dec(s, f[i][0])), pow(alfa_i[i][1], (j + 1))])
    co.append(d_list)

print("crt:", crt)

m, v = [], []
for i in crt:
    v.append(i[0])
    m.append(i[1])

# m = [3, 5, 7]
# v = [2, 3, 2]
crt_mv = sycrt(m, v)
print("Solutia SPH folosind CRT din sympy", crt_mv)

pmod = 1
for i in m:
    pmod *= i

x = 0
for i in range(len(m)):
    c = pmod // m[i]
    px = 1
    while True:
        psol = (c * px - v[i]) % m[i]
        if psol == 0:
            x += c * px
            break
        px += 1

print("CRT solution:", x % pmod)
