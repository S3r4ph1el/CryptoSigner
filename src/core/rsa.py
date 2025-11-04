from random import Random

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def gen_prime(bits: int = 32):
    rnd = Random()
    if bits < 2:
        raise ValueError("bits must be >= 2")
    while True:
        a = rnd.getrandbits(bits)
        a |= (1 << (bits - 1)) | 1
        if is_prime(a):
            return a

def mdc(a, b):
    while b:
        a, b = b, a % b
    return a

def modinv(a, m):
    if m <= 0:
        raise ValueError("m must be > 0")
    a %= m

    try:
        return pow(a, -1, m)
    except TypeError:
        pass
    except ValueError:
        return None
    
    if mdc(a, m) != 1:
        return None

    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0

    aa, mm = a, m
    while aa > 1:
        q = aa // mm
        aa, mm = aa % mm, aa
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def gen_keys(bits: int = 48, max_attempts: int = 1000):
    e = 65537
    attempts = 0
    while attempts < max_attempts:
        p = gen_prime(bits)
        q = gen_prime(bits)
        if p == q:
            attempts += 1
            continue

        n = p * q
        phi = (p - 1) * (q - 1)

        # ensure e is coprime with phi
        if mdc(e, phi) != 1:
            attempts += 1
            continue

        d = modinv(e, phi)
        if d is None:
            attempts += 1
            continue

        return (n, e, d)

    raise RuntimeError(f"failed to generate keys after {max_attempts} attempts")

def sign(hash_bytes: bytes, d: int, n: int) -> int:

    if not isinstance(hash_bytes, (bytes, bytearray)):
        raise TypeError("sign expects hash_bytes as bytes")
    
    hash_int = int.from_bytes(hash_bytes, byteorder='big', signed=False)
    return pow(hash_int, d, n)

def verify(signature: int, hash_bytes: bytes, e: int, n: int) -> bool:

    if not isinstance(hash_bytes, (bytes, bytearray)):
        raise TypeError("verify expects hash_bytes as bytes")
    recovered = pow(signature, e, n)

    hash_int = int.from_bytes(hash_bytes, byteorder='big', signed=False)
    return recovered == (hash_int % n)