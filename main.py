import hashlib


#input_file = 'DimityJonesInPuzzleCastle_AnElectronicEscapeNovelInEighty-NineCiphertexts_BETA.txt'
input_file = 'DimityJonesInPuzzleCastle_AnElectronicEscapeNovelInEighty-NineCiphertexts_byO.B.Nakwa_v1.0.txt'
with open(input_file, 'r', encoding='ascii') as f_in:
    text = f_in.read()
    lines = text.splitlines()


def get_checksum(num):
    global lines
    for line in lines:
        if len(line) > 10 and line[0].isdigit() and line[1].isdigit() \
                and int(line[:2]) == num:
            return line[4:]
    return None


def hash_str(s):
    return hashlib.sha256(s.encode('ascii')).digest().hex()


def test_hashing():
    start = text.find('To begin with')
    end = text.find(':', start) + 1
    hash_end = text.find('\n', end)
    s = text[start:end]
    hash_s = text[end:hash_end].strip()
    digest = hash_str(s)
    if digest != hash_s:
        print(f'bad test hash:\n\texpected {hash_s}\n\tactual {digest}')


def get_next_section(s, num):
    needle = f'{num}.#####'
    start = s.find(needle) + len(needle)
    return s[start:]


def check_chapter(num, chapter_text):
    digest = hash_str(chapter_text)
    checksum = get_checksum(num)
    with open(f'chapter{num}.txt', 'w', encoding='ascii') as f1:
        f1.write(chapter_text)
    if digest != checksum:
        print(
            f'bad chapter {num}:\n\texpected {checksum}\n\tactual   {digest}')
        print(chapter_text[:50])
        exit(num)


def interleave_chars(s):
    new_s = ['_'] * len(s)
    i = 0
    j = len(s) - 1
    k = 0
    while i <= j:
        new_s[k] = s[i]
        k += 1
        i += 1
        if j > i:
            new_s[k] = s[j]
            k += 1
            j -= 1
    return ''.join(new_s)


def get_quote(s, index):
    i = -1
    start = 0
    while i < index:
        start = s.find('"""\n', start) + 4
        end = s.find('\n"""', start)
        quote = s[start:end]
        start = end + 4
        i += 1
    return quote


def get_chapter_1(s):
    section = get_next_section(s, 1)
    return interleave_chars(section)


def reverse_sentences(s):
    sentences = s.split('.')
    for i, sentence in enumerate(sentences):
        sentences[i] = ' '.join(reversed(sentence.split(' ')))
    return '.'.join(sentences)


def get_chapter_2(s):
    reverse_check = interleave_chars(get_quote(s, 0))
    reverse_check = reverse_check[:reverse_check.find('. ') + 2] \
        + interleave_chars(reverse_check[reverse_check.find('. ') + 2:])
    disclaimer = reverse_sentences(get_quote(s, 1))
    print(disclaimer)
    section = get_next_section(s, 2)
    return reverse_sentences(section)


def reverse_each_word(s):
    return ' '.join(w[::-1] for w in s.split(' '))


def get_chapter_3(s):
    q = reverse_each_word(get_quote(s, 0))
    print(q)
    section = get_next_section(s, 3)
    return reverse_each_word(section)


def get_chunks(s, chunk_size):
    return (s[i:i+chunk_size] for i in range(0, len(s), chunk_size))


def shuffle_chunks(s, chunk_size, pattern):
    out = ''
    for chunk in get_chunks(s, chunk_size):
        if len(chunk) == chunk_size:
            new_chunk = ''
            for p in pattern:
                new_chunk += chunk[p - 1]
            out += new_chunk
        else:
            out += chunk
    return out


def get_chapter_4(s):
    pattern = [8, 7, 6, 5, 4, 3, 2]
    print(shuffle_chunks(get_quote(s, 2), 8, pattern))
    print(shuffle_chunks(get_quote(s, 4), 8, pattern))
    print(shuffle_chunks(get_quote(s, 5), 8, pattern))
    pattern = [3, 2, 1, 7, 6, 5]
    section = get_next_section(s, 4)
    return shuffle_chunks(section, 8, pattern)


def get_chapter_5(s):
    pattern = [7, 6, 8, 3, 2, 1, 9, 5, 4]
    section = get_next_section(s, 5)
    return shuffle_chunks(section, 9, pattern)


def get_chapter_6(s):
    bricks = ["DED", "RE NOT NEE", "AYS W",
              "HERE YOU", " HAV", "MEMBER AL",
              "W", "RE", "THESE A", "E BEEN"]
    pattern = [8, 6, 7, 3, 4, 5, 10]
    print(''.join((bricks[p - 1] for p in pattern)))
    pattern = [len(bricks[p - 1]) for p in pattern]
    section = get_next_section(s, 6)
    return shuffle_chunks(section, 9, pattern)


def get_chapter_7(s):
    section = get_next_section(s, 7)
    blocks = [(b[1:b.find('"', 1)],
               int(b[b.find('(') + 1:b.find(')')])) for b in get_quote(
        s, 0).replace('\n\n', '\n').split('\n')]
    pattern = [4, 2, 14, 5, 1]
    quote = ''.join((blocks[p - 1][0] for p in pattern))
    print(quote)
    pattern = [blocks[p - 1][1] for p in pattern]
    return shuffle_chunks(section, max(pattern), pattern)


def get_chapter_8(s):
    nums = [int(i) for i in s[s.find('{')+1:s.find('}')].split(', ')]
    sets = [[]]
    for n in nums:
        sets += [s+[n] for s in sets]
    pattern = []
    for sx in sets:
        if sum(sx) == 29290:
            print(sx)
            for n in sorted(sx):
                for i, m in enumerate(nums):
                    if n == m:
                        pattern += [i + 1]
    print(pattern)
    section = get_next_section(s, 8)
    return shuffle_chunks(section, max(pattern), pattern)


def get_alphabet_order(s):
    words = [w.lower() for w in s.split(' ')]
    sorted_words = {}
    i = 0
    for i, w in enumerate(sorted(words)):
        if w not in sorted_words:
            sorted_words[w] = [i + 1]
        else:
            sorted_words[w].append(i + 1)
    # sorted_words = {w: i + 1 for i, w in enumerate(sorted(words))}
    pattern = []
    for w in words:
        pattern.append(sorted_words[w][0])
        sorted_words[w].remove(sorted_words[w][0])
    print(s, pattern)
    return pattern


def get_chapter_9(s):
    q = get_quote(s, 0).split('\n')[3].split('.')[0]
    pattern = get_alphabet_order(q)
    q = get_quote(s, 0).split('\n')[5]
    pattern.extend(get_alphabet_order(q)[1:6])
    section = get_next_section(s, 9)
    return shuffle_chunks(section, max(pattern), pattern)


def get_alpha_pattern(s):
    return get_alphabet_order(' '.join(c for c in s))


def get_chapter_10(s):
    q = get_quote(s, 0).split('\n')[0].replace(' ', '').replace('.', '')
    # q2 = get_quote(s, 0).split('\n')[1].replace(', ', '')
    print(q)
    # print(q2, len(q2))
    pattern = get_alpha_pattern(q)
    print(pattern, len(pattern))
    section = get_next_section(s, 10)
    return shuffle_chunks(section, max(pattern), pattern)


def get_chapter_11(s):
    section = get_next_section(s, 11)
    q = get_quote(s, 0)
    print(q)
    pattern = get_alpha_pattern("the puzzle castle is a book that you at least once must read")
    return shuffle_chunks(section, max(pattern), pattern)


if __name__ == "__main__":
    test_hashing()
    ch1 = get_chapter_1(text)
    check_chapter(1, ch1)
    ch2 = get_chapter_2(ch1)
    check_chapter(2, ch2)
    ch3 = get_chapter_3(ch2)
    check_chapter(3, ch3)
    ch4 = get_chapter_4(ch3)
    check_chapter(4, ch4)
    ch5 = get_chapter_5(ch4)
    check_chapter(5, ch5)
    ch6 = get_chapter_6(ch5)
    check_chapter(6, ch6)
    ch7 = get_chapter_7(ch6)
    check_chapter(7, ch7)
    ch8 = get_chapter_8(ch7)
    check_chapter(8, ch8)
    ch9 = get_chapter_9(ch8)
    check_chapter(9, ch9)
    ch10 = get_chapter_10(ch9)
    check_chapter(10, ch10)
    ch11 = get_chapter_11(ch10)
    check_chapter(11, ch11)
