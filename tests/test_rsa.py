from src.core import rsa

def test_modinv():
    res1 = rsa.modinv(3, 11)
    res2 = rsa.modinv(6, 12)
    print("modinv(3, 11) ->", res1)
    print("modinv(6, 12) ->", res2)
    assert res1 == 4
    assert res2 is None


def test_gen_prime_and_is_prime():
    p = rsa.gen_prime(48)
    print("generated prime p ->", p)
    print("p.bit_length() ->", p.bit_length())
    assert rsa.is_prime(p)
    assert p.bit_length() == 48


def test_rsa_encrypt_decrypt():
    n, e, d = rsa.gen_keys(bits=48, max_attempts=200)
    m = "Example mess"
    print("n ->", n)
    print("e ->", e)
    print("d ->", d)
    print("message m ->", m)
    m_int = rsa.str_to_int(m)
    print("message as int ->", m_int)
    assert m_int < n, "message integer must be less than modulus n"
    assert 0 <= m_int < n
    c = rsa.crypt(m_int, e, n)
    print("ciphertext c ->", c)
    
    decrypted = rsa.decrypt(c, d, n)
    print("decrypted ->", decrypted)
    assert decrypted == m_int or rsa.int_to_str(decrypted) == m, "decrypted message does not match original"

if __name__ == "__main__":
    test_modinv()
    test_gen_prime_and_is_prime()
    test_rsa_encrypt_decrypt()
    print("All tests passed.")