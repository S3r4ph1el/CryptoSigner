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

def gen_keys(bits: int = 64, max_attempts: int = 1000):
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

def str_to_int(message: str, max_bits: int = None) -> int:

    if not isinstance(message, str):
        raise TypeError("message must be a str")
    
    message_bytes = message.encode('utf-8')
    i = int.from_bytes(message_bytes, 'big')

    if max_bits is not None and i.bit_length() >= max_bits:
        raise ValueError("message too large for given modulus/bit-size; split into blocks or use a larger key")
    return i

def int_to_str(i) -> str:

    if isinstance(i, str):
        return i
    
    if not isinstance(i, int):
        raise TypeError("int_to_str expects an int or str")
    
    if i == 0:
        return ""
    
    num_bytes = (i.bit_length() + 7) // 8
    return i.to_bytes(num_bytes, byteorder='big').decode('utf-8', errors='ignore')

def crypt(message, e: int, n: int) -> int:

    # integer path
    if isinstance(message, int):
        if not (0 <= message < n):
            raise ValueError("message must satisfy 0 <= message < n")
        return pow(message, e, n)

    # string path
    if isinstance(message, str):
        message_int = str_to_int(message)
        if not (0 <= message_int < n):
            raise ValueError("message integer must be less than modulus n")
        return pow(message_int, e, n)

    raise TypeError("message must be int or str")

def decrypt(ciphertext: int, d: int, n: int) -> int:

    # integer path
    if not isinstance(ciphertext, int):
        raise TypeError("ciphertext must be an int")
    
    # validate ciphertext range
    if not (0 <= ciphertext < n):
        raise ValueError("ciphertext must satisfy 0 <= ciphertext < n")
    
    plaintext_int = pow(ciphertext, d, n)
    plaintext = int_to_str(plaintext_int)

    return plaintext