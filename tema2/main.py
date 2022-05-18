import math
import time

from Crypto.Random import get_random_bytes
from Crypto.Util.number import getPrime

p = getPrime(512, randfunc=get_random_bytes)
q = getPrime(512, randfunc=get_random_bytes)
r = getPrime(512, randfunc=get_random_bytes)


# p, q, r = 3, 5, 7


def multiprime_rsa(p, q, r):
    n = p * q * r
    phi = (p - 1) * (q - 1) * (r - 1)

    # cheia publica
    e = getPrime(16, randfunc=get_random_bytes)
    # e = 11
    while math.gcd(e, phi) != 1:
        e = getPrime(16, randfunc=get_random_bytes)

    # cheia privata
    d = pow(e, -1, phi)

    y = getPrime(512, randfunc=get_random_bytes)
    # y = 17

    print("n:", n)
    print("phi:", phi)
    print("e:", e)
    print("d:", d)
    print("y:", y)

    # regular modular exponential algorithm
    start = time.time()
    plaintext = pow(y, d, n)
    end = time.time()
    print("Regular modular exp. algorithm:", plaintext)
    print("Time: %s" % (end - start))

    # modular exponential algorithm using CRT-Garner
    start = time.time()
    x_p = pow(y % p, d % (p - 1), p)
    x_q = pow(y % q, d % (q - 1), q)
    x_r = pow(y % r, d % (r - 1), r)

    x1 = x_p
    # x2 = x1 + p * alfa = x_q mod q
    alfa = (x_q - x1) * pow(p, -1, q) % q
    x2 = x1 + alfa * p
    # x3 = x2 + p * q * beta = x_r mod r
    beta = (x_r - x2) * pow(p * q, -1, r) % r
    x3 = x2 + beta * p * q
    end = time.time()
    print("Modular exp. algorithm using CRT-Garner:", x3)
    print("Time: %s" % (end - start))


def multipower_rsa(p, q):
    n = p * p * q
    phi = p * (p - 1) * (q - 1)

    # cheia publica
    e = getPrime(16, randfunc=get_random_bytes)
    # e = 11
    while math.gcd(e, phi) != 1:
        e = getPrime(16, randfunc=get_random_bytes)

    # cheia privata
    d = pow(e, -1, phi)

    y = getPrime(512, randfunc=get_random_bytes)
    # y = 22

    print("n:", n)
    print("phi:", phi)
    print("e:", e)
    print("d:", d)
    print("y:", y)

    # regular modular exponential algorithm
    start = time.time()
    plaintext = pow(y, d, n)
    end = time.time()
    print("Regular modular exp. algorithm:", plaintext)
    print("Time: %s" % (end - start))

    # modular exponential algorithm using CRT + Hensel
    start = time.time()
    x_q = pow(y % q, d % (q - 1), q)

    # x_p2 = x0 + p * x1
    x0 = pow(y % p, d % (p - 1), p)
    alpha = (y - pow(x0, e, p ** 2)) // p
    x1 = alpha * pow(e * pow(x0, e - 1, p ** 2), -1, p) % p
    x_p = x0 + p * x1

    xi = x_p % (p ** 2)
    alfa = (x_q - xi) * pow(p ** 2, -1, q) % q
    xii = xi + alfa * (p ** 2)

    end = time.time()
    print("Modular exp. algorithm using Hensel and CRT:", xii)
    print("Time: %s" % (end - start))


print("p:", p)
print("q:", q)
print("r:", r)

print("\n---Multiprime RSA---")
multiprime_rsa(p, q, r)
print("\n---Multipower RSA---")
multipower_rsa(p, q)

e = getPrime(16, randfunc=get_random_bytes)
while math.gcd(e, (p - 1) * (q - 1) * (r - 1)) != 1:
    e = getPrime(16, randfunc=get_random_bytes)
d_mpr = pow(e, -1, (p - 1) * (q - 1) * (r - 1))


def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(n % b)
        n = n // b
    return digits[::-1]


def binary_chains(x, m, n):
    start = time.time()
    n_digits = int(bin(n)[2:])
    n_digits = [int(a) for a in str(n_digits)]
    y = 1
    for i in range(len(n_digits) - 1, -1, -1):
        y = pow(y, 2, m)
        if n_digits[i] == 1:
            y = (y * x) % m
    end = time.time()
    print("\nMetoda binara:", end - start)
    return y


def beta_chains(x, m, n):
    start = time.time()
    xi = [0 for i in range(8)]
    xi[0] = 1
    for i in range(1, 8):
        xi[i] = (xi[i - 1] * x) % m
    n_digits = numberToBase(n, 8)
    y = 1
    for i in range(len(n_digits)):
        y = pow(y, 8, m)
        y = (y * xi[n_digits[i]]) % m
    end = time.time()
    print("\nMetoda ferestrei fixe(?):", end - start)
    return y


bc = binary_chains(d_mpr % (p-1), d_mpr % (q-1), d_mpr % (r-1))
ff = beta_chains(d_mpr % (p-1), d_mpr % (q-1), d_mpr % (r-1))
