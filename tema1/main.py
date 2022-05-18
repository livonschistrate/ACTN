import copy
import itertools, numpy
import random
import time

from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.number import getPrime, inverse


def polynom(m, x, k):
    sum = 0
    for c in (range(k - 1)):
        sum += m[c] * (x ** (c + 1))
    return sum


def polynom_decode(z, subset):
    sum = 0
    coef = []
    for i in subset:
        prod = 1
        for j in subset:
            if i != j:
                prod *= inverse(i - j, p)
        sum += z[i - 1] * prod
    sum %= p
    return sum


p = getPrime(161, randfunc=get_random_bytes)
p = 11

with open("input.txt") as fd:
    input_char = fd.read()

s = 1
k = len(input_char) + 1
n = k + 2 * s

# Initial, avem input_char = (a_0, ..., a_k-2) si o transformam in (a_k-2, ..., a_0)
r_input_char = input_char[::-1]

print("Avem textul (m):", input_char)
print("s = %2d" % s)
print("k = %2d" % k)
print("n = %2d" % n)

# Codificare

input_over_zp = []
input_number = 0
for i in input_char:
    if '0' <= i <= '9':
        input_number = input_number * 10 + int(i)
        input_over_zp.append(input_number % p)

print("\nReprezentand vectorul peste Z_p, obtinem:")
print(input_over_zp)

y = []
r_zp = input_over_zp[::-1]
for i in range(n):
    polynom_result = polynom(r_zp, i + 1, k)
    y.append(polynom_result % p)

print("\nCodificand efectiv vectorul, vom avea (y):")
print(y)

# Decodificare

z = [9, 2, 6, 5, 8]
# z = copy.deepcopy(y)
#
# position = random.randrange(len(z))
# new_value = random.randrange(p)
# while new_value == z[position]:
#     new_value = random.randrange(0, 9)
#
# z[position] = new_value
print("\nModificand vectorul obtinut a.i. sa aiba o eroare, vom avea:", z)

z_wo_errors = []
arg_wo_errors = []
for i in range(len(z)):
    if z[i] == y[i]:
        z_wo_errors.append(z[i])
        arg_wo_errors.append(i + 1)

print("Acel vector, fara erori, va fi:", z_wo_errors)

print("Vom crea o submultime de la:", arg_wo_errors)


def kk_inversions(subsets, z):
    start = time.time()
    selected_subset = 0
    fc_list = []
    fc = 0

    while selected_subset < len(subsets):
        for i in (subsets[selected_subset]):
            prod = 1
            for j in (subsets[selected_subset]):
                if i != j:
                    prod *= (j * inverse(j - i, p))
                    # prod *= j/(i-j) # versiunea din fisa, cu ea obtin coeficienti liberi nenuli
            fc += z[i - 1] * prod
        fc %= p
        fc_list.append(fc)
        selected_subset += 1

    end = time.time()
    rtime = end - start
    print("\nk*(k-1): Avem coeficientii liberi:")
    print(fc_list)
    print("Timp: ", rtime)


def k_inversions(subsets, z):
    start = time.time()
    selected_subset = 0
    fc_list = []
    fc = 0

    while selected_subset < len(subsets):
        for i in (subsets[selected_subset]):
            prod = 1
            nom = 1
            for j in (subsets[selected_subset]):
                if i != j:
                    prod *= j
                    nom = inverse(j - i, p)
            prod = prod * nom
            fc += z[i - 1] * prod
        fc %= p
        fc_list.append(fc)
        selected_subset += 1

    end = time.time()
    rtime = end - start
    print("\nk: Avem coeficientii liberi:")
    print(fc_list)
    print("Timp: ", rtime)


def one_inversion(subsets, z):
    start = time.time()
    selected_subset = 0
    fc_list = []
    fc = 0

    numer, denom = [], []

    while selected_subset < len(subsets):
        for i in (subsets[selected_subset]):
            num = z[i - 1]
            den = 1
            for j in (subsets[selected_subset]):
                if i != j:
                    num *= j
                    den *= (j - i)
            numer.append(num)
            denom.append(den)

        sum, div = 0, 1
        for i in range(len(numer)):
            add = numer[i]
            for j in range(len(numer)):
                add *= denom[j]
            sum += add
            div *= denom[i]
        fc = sum * inverse(div, p)
        fc %= p
        fc_list.append(fc)
        selected_subset += 1

    end = time.time()
    rtime = end - start
    print("\n1: Avem coeficientii liberi:")
    print(fc_list)
    print("Timp: ", rtime)


subsets = list(itertools.combinations(arg_wo_errors, k))

kk_inversions(subsets, z)
k_inversions(subsets, z)
one_inversion(subsets, z)

# selected_subset = 0
#
# fc_list = []
# fc = 0
#
# while selected_subset < len(subsets):
#     for i in (subsets[selected_subset]):
#         prod = 1
#         for j in (subsets[selected_subset]):
#             if i != j:
#                 prod *= (j * inverse(j-i, p))
#                 # prod *= j/(i-j) # versiunea din fisa, cu ea obtin coeficienti liberi nenuli
#         fc += z[i-1] * prod
#     fc %= p
#     fc_list.append(fc)
#     selected_subset += 1
#
# print("\nAvem coeficientii liberi:")
# print(fc_list)

decode_result = []
for selected_subset in range(len(subsets)):
    decode_result.append(polynom_decode(z, subsets[selected_subset]))

print("\nRezultatul decodificarii: ", decode_result)
