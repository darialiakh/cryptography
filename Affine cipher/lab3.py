def calculate_gcd(a, b):
    if b == 0:
        return [a, 1, 0]
    temp = calculate_gcd(b, a % b)
    return [temp[0], temp[2], temp[1] - (a // b) * temp[2]]


# find x for equality ax = b(mod n)
def solve_equality(a, b, n):
    gcd_a_n = calculate_gcd(a, n)
    d = gcd_a_n[0]
    reverse_a = gcd_a_n[1]
    # если нет общих делителей, то решение одно: x = a^-1 * b(mod n)
    if d == 1:
        return [(reverse_a * b) % n]
    else:
        # если a и n не взаимнопростые и b и n - взаимнопростые, решений нет
        if b % d != 0:
            return []
        # иначе сокращаем числа и делаем то же самое
        else:
            a1, b1, n1 = a // d, b // d, n // d
            result = solve_equality(a1, b1, n)
            for i in range(1, d):
                result.append(result[0] + i * n)
            return result


global forbidden_bigrams
forbidden_bigrams = ['уы', 'уь', 'фж', 'фй', 'фх', 'фц', 'фш', 'фщ', 'хы', 'хю', 'цй', 'цф', 'цц', 'цш',
                     'цщ', 'ць', 'цю', 'чж', 'чй', 'чф', 'чц', 'чщ', 'чы', 'чю', 'шг', 'шж', 'шй', 'шх', 'шщ',
                     'шы', 'шэ', 'шю', 'шя', 'щб', 'щв', 'щг', 'щж', 'щз', 'щй', 'щк', 'щл', 'щм', 'що', 'щп',
                     'щф', 'щх', 'щц', 'щч', 'щш', 'щщ', 'щы', 'щю', 'щя', 'ыы', 'ыь', 'ьы', 'ьь', 'эа', 'эе',
                     'эж', 'эи', 'эо', 'эу', 'эч', 'эщ', 'эы', 'эь', 'эю', 'эя', 'юй', 'юы', 'юь', 'яы',
                     'яь', 'аы', 'аь', 'бй', 'бф', 'вй', 'гж', 'гй', 'гц', 'гщ', 'гь', 'дй', 'дщ', 'еы', 'еь',
                     'жй', 'жр', 'жф', 'жц', 'жш', 'жщ', 'жы', 'иы', 'йы', 'йь', 'кы', 'кь', 'мй', 'нй', 'оы',
                     'пж', 'пз', 'пй', 'пм', 'пх', 'пщ']


def is_text_real(text):
    for bigram in forbidden_bigrams:
        if text.__contains__(bigram):
            return bigram
    return 'valid'


global alpha, alpha_len, bi_len
alpha = "абвгдежзийклмнопрстуфхцчшщыьэюя"
alpha_len = len(alpha)
bi_len = alpha_len ** 2

top_ot_bigrams = ['ст', 'но', 'та', 'на', 'ен']
top_o1_bigrams = ['рн', 'ыч', 'нк', 'цз', 'иа']
top_v1_bigrams = ['вэ', 'кь', 'ыу', 'шк', 'ди']

o1_text = open('01.txt', 'r', encoding='utf-8')
o1_text = o1_text.read().replace('\n', '')
v1_text = open('v1', 'r', encoding='utf-8')
v1_text = v1_text.read()

ot = top_ot_bigrams
sht = top_v1_bigrams
sht_text = v1_text


# биграмма в число
def bi_num(bigram): return alpha.index(bigram[0]) * alpha_len + alpha.index(bigram[1])


# число в биграмму
def bi_reverse(num): return alpha[num // alpha_len] + alpha[num % alpha_len]


result = {}
# def search_key(*ot, *sht)
ab = {}
for i1 in range(5):
    for j1 in range(5):
        for i2 in range(5):
            for j2 in range(5):
                if i1 != j1 and i2 != j2:
                    y1, y2 = bi_num(sht[i1]), bi_num(sht[j1])
                    x1, x2 = bi_num(ot[i2]), bi_num(ot[j2])
                    y = y1 - y2
                    x = x1 - x2
                    # print(x, y, bi_len)
                    # reverse_x = calculate_gcd(x, bi_len)[1]
                    a = solve_equality(x, y, bi_len)
                    if len(a) > 0:
                        b = (y1 - a[0] * x1) % bi_len
                        # print(i, j, a, b)
                        ab[a[0]] = b
                        result[a[0]] = [b, sht[i1], sht[j1], ot[i2], ot[j2]]
print(ab)

ot_texts = {a: '' for a in ab.keys()}
print(len(ot_texts))

# def decrypt()
for a, b in ab.items():
    ot_text = ''
    for i in range(1, len(sht_text), 2):
        y = bi_num(sht_text[i - 1] + sht_text[i])
        x = solve_equality(a, y - b, bi_len)
        ot_bigrams = bi_reverse(x[0])
        ot_text += ot_bigrams
    ot_texts[a] = ot_text

file = open('result.txt', 'w')

for a in ot_texts.keys():
    # print(ot_texts[a])
    file.write(ot_texts[a] + '\n')
    file.write(
        'a= ' + str(a) + ' b= ' + str(result[a][0]) + ' y*= ' + result[a][1] + ' y**= ' + result[a][2] + ' x*= '
        + result[a][3] + ' x**= ' + result[a][4] + '\n')
    file.write(is_text_real(ot_texts[a]) +'\n\n\n')

file.close()
