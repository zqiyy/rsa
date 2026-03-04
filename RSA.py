import random
import math


# ─────────────────────────────────────────────────────────────────────────────
# 1. FUNGSI BANTU MATEMATIS
# ─────────────────────────────────────────────────────────────────────────────

def is_prime(n: int) -> bool:
    """Cek apakah bilangan n adalah bilangan prima (Miller-Rabin sederhana)."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)         
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int = 512) -> int:
    """Generate bilangan prima acak dengan panjang `bits` bit."""
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1))  
        candidate |= 1                
        if is_prime(candidate):
            return candidate


def extended_gcd(a: int, b: int):
    """
    Extended Euclidean Algorithm.
    Mengembalikan (gcd, x, y) sehingga a*x + b*y = gcd(a, b).
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(e: int, phi: int) -> int:
    """
    Hitung invers modular dari e terhadap phi menggunakan Extended Euclidean.
    Mengembalikan d sehingga (e * d) % phi == 1.
    """
    gcd, x, _ = extended_gcd(e % phi, phi)
    if gcd != 1:
        raise ValueError("Invers modular tidak ada (e dan phi tidak koprima).")
    return x % phi


# ─────────────────────────────────────────────────────────────────────────────
# 2. KEY GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def generate_keys(bits: int = 512):
    """
    Pembangkitan Kunci RSA.

    Langkah:
      1. Pilih dua bilangan prima p dan q
      2. Hitung n = p * q
      3. Hitung φ(n) = (p-1)(q-1)
      4. Pilih e: 1 < e < φ(n), gcd(e, φ(n)) = 1
      5. Hitung d = e^(-1) mod φ(n)

    Returns:
      public_key  : (e, n)
      private_key : (d, n)
    """
    print("\n" + "="*48)
    print("  TAHAP 1: KEY GENERATION")
    print("="*48)

    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:                         
        q = generate_prime(bits)
    print(f"    p = {p}")
    print(f"    q = {q}")

    n = p * q
    print(f"    n = {n}")

    phi = (p - 1) * (q - 1)
    print(f"    φ(n) = {phi}")

    e = 65537                              
    if math.gcd(e, phi) != 1:
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2
    print(f"    e = {e}  →  gcd(e, φ(n)) = {math.gcd(e, phi)}")

    d = mod_inverse(e, phi)
    print(f"    d = {d}")

    print(f"\n Public  Key : (e={e}, n=…{str(n)[-10:]})")
    print(f" Private Key : (d=…{str(d)[-10:]}, n=…{str(n)[-10:]})")

    return (e, n), (d, n)


# ─────────────────────────────────────────────────────────────────────────────
# 3. ENKRIPSI
# ─────────────────────────────────────────────────────────────────────────────

def encrypt(plaintext: str, public_key: tuple) -> list[int]:
    """
    Enkripsi plaintext menggunakan public key (e, n).

    Setiap karakter dikonversi ke nilai ASCII, lalu:
        C = M^e mod n
    """
    e, n = public_key

    print("\n" + "="*48)
    print("  TAHAP 2: ENKRIPSI")
    print("="*48)
    print(f"\nPlaintext  : \"{plaintext}\"")
    print(f"Public Key : e = {e}, n = …{str(n)[-10:]}\n")

    ciphertext = []
    print(f"{'Char':<6} {'ASCII (M)':<12} {'Ciphertext (C = M^e mod n)'}")
    print("-" * 47)

    for char in plaintext:
        m = ord(char)                      
        c = pow(m, e, n)                   
        ciphertext.append(c)
        print(f"  {char!r:<4} {m:<12} {c}")

    print(f"\n Ciphertext : {ciphertext}")
    return ciphertext


# ─────────────────────────────────────────────────────────────────────────────
# 4. DEKRIPSI
# ─────────────────────────────────────────────────────────────────────────────

def decrypt(ciphertext: list[int], private_key: tuple) -> str:
    """
    Dekripsi ciphertext menggunakan private key (d, n).

        M = C^d mod n
    """
    d, n = private_key

    print("\n" + "="*48)
    print("  TAHAP 3: DEKRIPSI")
    print("="*48)
    print(f"\nPrivate Key : d = …{str(d)[-10:]}, n = …{str(n)[-10:]}\n")

    decrypted_chars = []
    print(f"{'Ciphertext (C)':<20} {'ASCII (M = C^d mod n)':<22} {'Char'}")
    print("-" * 48)

    for c in ciphertext:
        m = pow(c, d, n)                   
        char = chr(m)
        decrypted_chars.append(char)
        print(f"  {c:<18} {m:<22} {char!r}")

    result = "".join(decrypted_chars)
    print(f"\n Decrypted Text : \"{result}\"")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# 5. DEMO UTAMA
# ─────────────────────────────────────────────────────────────────────────────

def demo():
    print("\n" + "╔" + "═"*21 + "╗")
    print("║   RSA ENCRYPTION  ║")
    print("╚" + "═"*21 + "╝")

    
    DEMO_BITS = 16         

    # 1. Generate Keys
    public_key, private_key = generate_keys(bits=DEMO_BITS)

    # 2. Teks yang akan dienkripsi
    plaintext = "Coba RSA"

    # 3. Enkripsi
    ciphertext = encrypt(plaintext, public_key)

    # 4. Dekripsi
    decrypted = decrypt(ciphertext, private_key)

    # 5. Verifikasi hasil
    print("\n" + "="*48)
    print(" VERIFIKASI HASIL")
    print("="*48)
    print(f"\n  Plaintext  asli    : \"{plaintext}\"")
    print(f"  Hasil dekripsi      : \"{decrypted}\"")


if __name__ == "__main__":
    demo()