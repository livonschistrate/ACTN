HW2:

1. Implement multi-prime RSA decryption (i.e., computing y^d mod n, for n = pqr, where p, q, and r are distinct 512-bit primes) using the Chinese remainder theorem algorithm discussed in class. Perform time comparisons between this modular exponentiation algorithm and the regular modular exponentiation algorithm (the one that is implemented in your large integers library)

2. Implement multi-power RSA decryption (i.e., computing y^d mod n, for n = (p^2)q, where p and q are distinct 512-bit primes) using the Chinese remainder theorem algorithm and Hensel’s lifting lemma discussed in class. Perform time comparisons between this modular exponentiation algorithm and the regular modular exponentiation algorithm (the one that is implemented in your large integers library)

3. Combine (1) with constructing short addition chains for the elements d mod (p-1), d mod (q-1), d mod (r-1).