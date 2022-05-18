import math
import time

from Crypto.Random import random, get_random_bytes
from Crypto.Util.number import getPrime, isPrime


def jacobi_symbol(a, n):
    """

    :param a: nr intreg
    :param n: nr intreg
    :return: simbolul Jacobi (a/n)
    """
    result = 1
    if a == 0 or a == 1:
        return a
    while a:
        # regula de reducere
        if a > n:
            a = a % n
        # regula de multiplicitate (daca a este par)
        while a % 2 == 0:
            a = a // 2
            if n % 8 == 3 or n % 8 == 5:
                result = -result
        # legea reciprocitatii
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        n = n % a
        if a == 1:
            return result
        else:
            a, n = n, a


def ss_testing(n, t):
    """
    Test probabilistic ce determina daca un numar este compus sau prim
    :param n: numar intreg
    :param t: parametru de securitate
    :return: este n numar prim/compus?
    """
    if n < 3 and t < 1:
        raise ValueError("n < 3 or t < 1")
    for i in range(t):
        a = random.randrange(2, n - 1)
        # if math.gcd(a, n) != 1:
        #     print("{:d}: composite".format(n))
        #     return
        r = pow(a, (n - 1) // 2, n)
        if r != 1 and r != n - 1:
            print("{:d}: composite".format(n))
            return
        s = jacobi_symbol(a, n)
        if r != s % n:
            print("{:d}: composite".format(n))
            return
    print("{:d}: prime".format(n))
    return


def mersenne_reduction(s):
    """
    Test ce determina daca un numar Mersenne este prim/compus (reducere modulara)
    :param s:
    :return:

    asemanator cu functia de mai jos, numai ca pt (u^2 - 2) % n actualizam
    prin a aduna impartirea lui u la 2^n cu restul acestei impartiri (si trecem
    apoi la modulo 2^(n-1))
    """
    n = (2 ** s) - 1
    u = 4
    for k in range(s - 2):
        u = (u ** 2 - 2) % n
        u = (u % (2 ** n) + u // (2 ** n)) % (2 ** n - 1)
    print("{:d}: prime".format(n)) if u == 0 else print("{:d}: composite".format(n))


def ll_testing(s):
    """
    Test ce determina daca un numar Mersenne este prim/compus
    :param s: nr intreg folosit pentru a crea numarul Mersenne
    :return: este n numar prim/compus?
    """
    n = (2 ** s) - 1
    u = 4
    for k in range(s - 2):
        u = (u ** 2 - 2) % n
    print("{:d}: prime".format(n)) if u == 0 else print("{:d}: composite".format(n))


print("---Solovay-Strassen primality test---")
for i in range(4, 50):
    ss_testing(i, 99)

print("\n---Lucas-Lehmer primality test---")
start = time.time()
for i in range(4, 25):
    ll_testing(i)
end = time.time()
print("Normal modular reduction time:", end - start)

print('\n---Lucas-Lehmer primality test using modular reduction---')
start = time.time()
for i in range(4, 25):
    mersenne_reduction(i)
end = time.time()
print("Dedicated modular reduction time:", end - start)
