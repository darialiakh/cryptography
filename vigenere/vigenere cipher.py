import re


def encrypt(keylen, key, opentext):
    shtext = ''
    for i in range(len(opentext)):
        k = key[i % keylen]
        shtext += alpha[(alpha.index(opentext[i]) + alpha.index(k)) % 32]
    return shtext


def calculate_compliance_index(textlen, text):
    index = 0
    for a in alpha:
        i = 0  # n[a]
        for letter in text:
            if letter == a:
                i += 1
        index += i * (i - 1)
    index *= 1 / (textlen * (textlen - 1))
    return index


global alpha
alpha = [chr(i) for i in range(1072, 1104)]
global alpha_len
alpha_len = len(alpha)


# форматирование ОТ
ot = open("text.txt", "r")
ot = ot.read().lower().replace('ё', 'е')
ot = re.sub(r'[^а-я]', '', ot)
textlen = len(ot)


keys = {
    2: 'да', 3: 'нет', 4: 'стоп', 5: 'огонь', 10: 'горитогонь',
    11: 'температура', 12: 'разнообразие',
    13: 'благодарность', 14: 'дождьпрольется',
    15: 'бомбардировщики', 16: 'смотретьнасолнце',
    17: 'дальшеонишлимолча', 18: 'высокаятемпература',
    19: 'вкомнатебылохолодно', 20: 'окнабылияркоосвещены',
}

sht = {}
compliance_index = {}
compliance_index[0] = calculate_compliance_index(textlen, ot)
for r, key in keys.items():
    sht[r] = encrypt(r, key, ot)
    compliance_index[r] = calculate_compliance_index(textlen, sht[r])

for r, index in compliance_index.items():
    print(r, ': ', '%.4f' % index)

# ----------------------------------
# discrypt
cipher = open('cipher.txt', 'r')
cipher = cipher.read().replace('\n', '')

index_cipher = calculate_compliance_index(len(cipher), cipher)
print('Cipher: ', index_cipher)

# разбить на блоки
y = {}
for r in range(2, 33):
    y[r] = ['' for i in range(r)]
    for i in range(len(cipher)):
        y[r][i % r] += cipher[i]

# посчитать ИС каждого блока
indexes2 = {}
for r in range(2, 33):
    indexes2[r] = [0 for i in range(r)]
    bl_index = []
    for i in range(r):
        bl_index += [calculate_compliance_index(len(y[r][i]), y[r][i])]
    indexes2[r] = sum(bl_index) / r

# вывод индексов совпадений
for r, index in indexes2.items():
    print(r, ': ', '%.4f' % index)

# длинна ключа
r_key = max(indexes2, key=indexes2.get)

# поиск самой часто встречающейся буквы
frequency_let = {}
for i in range(len(y[r_key])):
    frequency = {}
    for a in alpha:
        frequency[a] = 0
        for letter in y[r_key][i]:
            if letter == a:
                frequency[a] += 1
    frequency_let[i] = max(frequency, key=frequency.get)

# нахождение ключа
k = ''
for i in range(r_key):
    if i == 3:
        k += alpha[(alpha.index(frequency_let[i]) - alpha.index('е')) % alpha_len]
    else:
        k += alpha[(alpha.index(frequency_let[i]) - alpha.index('о')) % alpha_len]
print(k)

# расшифровка текста
open_text = ''
for i in range(len(cipher)):
    open_text += alpha[(alpha.index(cipher[i]) - alpha.index(k[i % len(k)])) % alpha_len]

print(open_text)

file = open('result.txt', 'w')
file.write(open_text)
