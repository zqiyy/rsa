# RSA Encryption — Implementasi From Scratch (Python)

Implementasi algoritma RSA (Rivest, Shamir, and Adleman) murni dari awal tanpa menggunakan library enkripsi seperti `rsa`, `cryptography`, atau sejenisnya. Seluruh logika matematis dibangun manual.

---

## Deskripsi

Program ini mendemonstrasikan tiga tahap utama algoritma RSA secara step-by-step:

**1. Key Generation**

Pembangkitan kunci publik `(e, n)` dan kunci privat `(d, n)` dengan langkah-langkah: pertama, pilih dua bilangan prima besar `p` dan `q` yang berbeda. Kemudian hitung modulus `n = p × q` dan nilai Euler totient `φ(n) = (p-1)(q-1)`. Selanjutnya pilih `e` (biasanya 65537) yang coprime dengan `φ(n)`, dan terakhir hitung `d` sebagai invers modular dari `e` mod `φ(n)` menggunakan Extended Euclidean Algorithm.

**2. Enkripsi**

Mengubah plaintext → ciphertext dengan rumus `C = M^e mod n` di mana `M` adalah representasi ASCII dari karakter.

**3. Dekripsi**

Mengembalikan ciphertext → plaintext dengan rumus `M = C^d mod n` dan konversi kembali ke karakter.

---

## Cara Menjalankan

### Prasyarat
- Python 3.10 atau lebih baru
- Tidak perlu instalasi library tambahan (hanya `math` dan `random` dari standard library)

### Langkah

```bash
# 1. Clone repository
git clone https://github.com/zqiyy/rsa.git
cd rsa

# 2. Jalankan program
python3 RSA.py
```

---

##  Struktur File

```
rsa/
├── RSA.py  
└── README.md    
```

---

## Penjelasan Fungsi Utama

### `is_prime(n)` — Uji Primalitas (Miller-Rabin)
Mengecek apakah bilangan `n` adalah prima menggunakan algoritma Miller-Rabin dengan witness deterministik. Akurat untuk semua bilangan di bawah 3,3 × 10²⁴.

### `generate_prime(bits)` — Pembangkitan Bilangan Prima
Menghasilkan bilangan prima acak sepanjang `bits` bit dengan cara:
1. Buat bilangan acak ganjil
2. Uji keprimaan
3. Ulangi hingga prima ditemukan

### `extended_gcd(a, b)` — Extended Euclidean Algorithm
Menghitung GCD dan koefisien Bezier `(x, y)` sehingga `a*x + b*y = gcd(a,b)`.

### `mod_inverse(e, phi)` — Invers Modular
Menghitung `d` sehingga `(e * d) % phi == 1`, digunakan untuk membuat kunci privat.

### `generate_keys(bits)` — Pembangkitan Kunci RSA
```
p, q  →  prima acak
n     = p × q
φ(n)  = (p-1)(q-1)
e     = 65537  (public exponent)
d     = e⁻¹ mod φ(n)
```
Output: `public_key = (e, n)`, `private_key = (d, n)`

### `encrypt(plaintext, public_key)` — Enkripsi
Setiap karakter dikonversi ke ASCII lalu:
```
C = M^e mod n
```

### `decrypt(ciphertext, private_key)` — Dekripsi
```
M = C^d mod n  →  chr(M)
```

---

## Contoh Output

```
╔═════════════════════╗
║   RSA ENCRYPTION  ║
╚═════════════════════╝

================================================
  TAHAP 1: KEY GENERATION
================================================
    p = 44017
    q = 59399
    n = 2614565783
    φ(n) = 2614462368
    e = 65537  →  gcd(e, φ(n)) = 1
    d = 1837148801

 Public  Key : (e=65537, n=…2614565783)
 Private Key : (d=…1837148801, n=…2614565783)

================================================
  TAHAP 2: ENKRIPSI
================================================

Plaintext  : "Coba RSA"
Public Key : e = 65537, n = …2614565783

Char   ASCII (M)    Ciphertext (C = M^e mod n)
-----------------------------------------------
  'C'  67           281666941
  'o'  111          1659340989
  'b'  98           632304578
  'a'  97           1122415886
  ' '  32           1424027213
  'R'  82           928948034
  'S'  83           1807420362
  'A'  65           1407151335

 Ciphertext : [281666941, 1659340989, 632304578, 1122415886, 1424027213, 928948034, 1807420362, 1407151335]

================================================
  TAHAP 3: DEKRIPSI
================================================

Private Key : d = …1837148801, n = …2614565783

Ciphertext (C)       ASCII (M = C^d mod n)  Char
------------------------------------------------
  281666941          67                     'C'
  1659340989         111                    'o'
  632304578          98                     'b'
  1122415886         97                     'a'
  1424027213         32                     ' '
  928948034          82                     'R'
  1807420362         83                     'S'
  1407151335         65                     'A'

 Decrypted Text : "Coba RSA"

================================================
 VERIFIKASI HASIL
================================================

  Plaintext  asli    : "Coba RSA"
  Hasil dekripsi      : "Coba RSA"
```

---

## Referensi

- Rivest, R., Shamir, A., & Adleman, L. (1978). *A Method for Obtaining Digital Signatures and Public-Key Cryptosystems*. Communications of the ACM.
- NIST FIPS 186-4 — Digital Signature Standard
- Menezes, A. et al. *Handbook of Applied Cryptography* (Chapter 8)

---

## Author

Nama        : Zakia Minhatul Maula 

NIM         : 24051204141 

Mata Kuliah : Keamanan Data & Informasi 



