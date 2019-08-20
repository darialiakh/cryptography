import random


def calculate_gcd(a, b):
    if b == 0:
        return [a, 1, 0]
    temp = calculate_gcd(b, a % b)
    return [temp[0], temp[2], temp[1] - (a // b) * temp[2]]


def prime_test(p):
    first_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for x in first_prime:
        if p % x == 0:
            return False
    # тест Міллера-Рабіна
    print(p)
    counter = 0
    n = p - 1
    s = 0
    while n % 2 == 0:
        n = n // 2
        s += 1
    d = int(n)
    k = 20
    for i in range(k):
        x = random.randint(2, p-1)
        gcd_x_p = calculate_gcd(x, p)[0]
        if gcd_x_p > 1:
            return False
        else:
            pseudo_simple = False
            pow_x_d = pow(x, d, p)
            if pow_x_d == 1 or pow_x_d == p-1:
                pseudo_simple = True
            else:
                for r in range(1, s):
                    x_r = pow(x, d*(2**r), p)
                    if x_r == p-1:
                        pseudo_simple = True
                        break
                    elif x_r == 1:
                        pseudo_simple = False
                        break
                    else:
                        continue
            if pseudo_simple:
                counter += 1
            else:
                return False
    if counter < k:
        return False
    else:
        print('prime')
        return True


def generate_number(bit_len):
    number = random.getrandbits(bit_len - 1)
    number += 2 ** (bit_len - 1)
    return number


def generate_key_pair(p, q):
    n = p * q
    phi = (p - 1)*(q - 1)
    print('phi = ', phi)
    while True:
        e = random.randint(2, phi)
        if calculate_gcd(e, phi)[0] == 1:
            break
    d = calculate_gcd(e, phi)[1] % phi
    return [e, n, d]


def encrypt(message, open_keys):
    e, n = open_keys[0], open_keys[1]
    encrypt_message = pow(message, e, n)
    return encrypt_message


def decrypt(encrypt_message, secret_keys):
    n, d = secret_keys[0], secret_keys[1]
    message = pow(encrypt_message, d, n)
    return message


def sign(message, secret_keys):
    n, d = secret_keys[0], secret_keys[1]
    s = pow(message, d, n)
    return s


def verify(message, s, open_keys):
    e, n = open_keys[0], open_keys[1]
    if message == pow(s, e, n):
        return True
    else:
        return False


def send_key(secret_keys_a, open_keys_b):
    n = secret_keys_a[0]
    n1 = open_keys_b[1]
    if n1 >= n:
        k = random.randint(1, n)
        # k = random.getrandbits(6*8)*256 + 23
        print('k = ', k)
        s = sign(k, secret_keys_a)
        print('s = ', s)
        s1 = encrypt(s, open_keys_b)
        k1 = encrypt(k, open_keys_b)
        return [k1, s1]
    else: return 0


def receive_key(ks, secret_keys_b, open_keys_a):
    k1, s1 = ks[0], ks[1]
    k = decrypt(k1, secret_keys_b)
    print('decrypt k = ', k)
    s = decrypt(s1, secret_keys_b)
    print('decrypt s =  ', s)
    result = verify(k, s, open_keys_a)
    return result


prime_numbers = []
counter = 0
bit_len = 256
while True:
    number = generate_number(bit_len)
    if prime_test(number):
        prime_numbers.append(number)
        counter += 1
    if counter == 4:
        break
prime_numbers = sorted(prime_numbers)
p, q = prime_numbers[0], prime_numbers[1]
p1, q1 = prime_numbers[2], prime_numbers[3]
print('prime numbers:', p, q, p1, q1, sep='\n')
keys = generate_key_pair(p, q)
keys1 = generate_key_pair(p1, q1)
open_keys, secret_key = [keys[0], keys[1]], [keys[1], keys[2]]
open_keys1, secret_key1 = [keys1[0], keys1[1]], [keys1[1], keys1[2]]
print('open and secret keys:')
print('e = ', open_keys[0])
print('n = ', open_keys[1])
print('d = ', secret_key[1])
print('e1 = ', open_keys1[0])
print('n1 = ', open_keys1[1])
print('d1 = ', secret_key1[1])
# e n d    e n public   n d secret
message = random.randint(0, open_keys[1])
print('Message:', message)
cryptogram_a = encrypt(message, open_keys)
cryptogram_b = encrypt(message, open_keys1)
print('Cryptogram_a:', cryptogram_a)
print('Cryptogram_b:', cryptogram_b)
decrypt_message_a = decrypt(cryptogram_a, secret_key)
decrypt_message_b = decrypt(cryptogram_b, secret_key1)
print('Decrypt_a:', decrypt_message_a)
print('Decrypt_b:', decrypt_message_b)
if message == decrypt_message_a:
    print('right decrypt a')
else:
    print('wrong')
if message == decrypt_message_b:
    print('right decrypt b')
else:
    print('wrong')

sp_a = sign(message, secret_key)
sp_b = sign(message, secret_key1)
print('sign_a:', sp_a)
print('sign_b:', sp_b)
if verify(message, sp_a, open_keys):
    print('verify a')
else:
    print('wrong')
if verify(message, sp_b, open_keys1):
    print('verify b')
else:
    print('wrong')
snd_key = send_key(secret_key, open_keys1)
print('k1: ', snd_key[0])
print('s1: ', snd_key[1])
if receive_key(snd_key, secret_key1, open_keys):
    print('verify a')
else:
    print('wrong')

