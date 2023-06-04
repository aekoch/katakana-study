import random
import unicodedata
from collections import defaultdict


katakana_long_vowel = 'ー'
katakana_duplicate_consonant = 'ッ'

english_vowels = ['a', 'e', 'i', 'o', 'u']
katakana_base_consonant_order = ['k', 's', 't', 'n', 'h', 'm', 'y', 'r', 'w']
katakana_vowels = {'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o'}

katakana_small_vowels = {'ァ': 'a', 'ィ': 'i', 'ゥ': 'u', 'ェ': 'e', 'ォ': 'o'}
katakana_small_ya_yo_yu = {'ャ': 'ya', 'ュ': 'yu', 'ョ': 'yo'}
katakana_modifiers = ['ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ャ', 'ュ', 'ョ', 'ー', 'ッ']

katakana_to_romaji = {
    'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
    'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
    'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
    'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
    'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
    'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
    'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
    'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
    'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
    'ワ': 'wa', 'ヲ': 'wo',
    'ン': 'n',
}

katakana_dakuten = {
    'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
    'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
    'ダ': 'da', 'ヂ': 'dji', 'ヅ': 'dzu', 'デ': 'de', 'ド': 'do',
    'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
}

katakana_handakuten = {
    'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
}

katakana_all_monograms_set = set(list(katakana_to_romaji.keys()) +
                                 list(katakana_dakuten.keys()) +
                                 list(katakana_handakuten.keys()) +
                                 katakana_modifiers)

katakana_digraph_small_ya_yu_yo = {
    'キャ': 'kya', 'キュ': 'kyu', 'キョ': 'kyo',
    'ギャ': 'gya', 'ギュ': 'gyu', 'ギョ': 'gyo',
    'シャ': 'sha', 'シュ': 'shu', 'ショ': 'sho',
    'ジャ': 'ja', 'ジュ': 'ju', 'ジョ': 'jo',
    'チャ': 'cha', 'チュ': 'chu', 'チョ': 'cho',
    'ニャ': 'nya', 'ニュ': 'nyu', 'ニョ': 'nyo',
    'ヒャ': 'hya', 'ヒュ': 'hyu', 'ヒョ': 'hyo',
    'ビャ': 'bya', 'ビュ': 'byu', 'ビョ': 'byo',
    'ピャ': 'pya', 'ピュ': 'pyu', 'ピョ': 'pyo',
    'ミャ': 'mya', 'ミュ': 'myu', 'ミョ': 'myo',
    'リャ': 'rya', 'リュ': 'ryu', 'リョ': 'ryo',
}

double_consonant_chunks = {
    katakana_duplicate_consonant + kana: reading[0] + reading for kana, reading in dict(
        **katakana_to_romaji, **katakana_dakuten, **katakana_handakuten, **katakana_digraph_small_ya_yu_yo
    ).items() if reading[0] not in english_vowels + ['n']
}

long_vowel_chunks = {
    kana + katakana_long_vowel: reading + reading[-1] for kana, reading in dict(
        **katakana_to_romaji, **katakana_dakuten, **katakana_handakuten, **katakana_digraph_small_ya_yu_yo
    ).items() if reading[-1] in english_vowels
}

long_vowel_and_double_consonant_chunks = {
    kana + katakana_long_vowel: reading + reading[-1] for kana, reading in dict(
        **double_consonant_chunks
    ).items() if reading[-1] in english_vowels
}

all_possible_chunks_with_readings = {
    **katakana_to_romaji, **katakana_dakuten, **katakana_handakuten, **katakana_digraph_small_ya_yu_yo,
    **double_consonant_chunks, **long_vowel_chunks, **long_vowel_and_double_consonant_chunks
}

all_possible_chunks_set = set(list(all_possible_chunks_with_readings.keys()))

chunks_by_size = defaultdict(list)
for chunk in list(all_possible_chunks_with_readings.keys()):
    size = len(chunk)
    chunks_by_size[size].append(chunk)
chunks_by_size = {k: d for k, d in chunks_by_size.items()}


for kana, reading in double_consonant_chunks.items():
    print(f'{kana: <8}, {reading: <8}')
for kana, reading in long_vowel_chunks.items():
    print(f'{kana: <8}, {reading: <8}')
for kana, reading in long_vowel_and_double_consonant_chunks.items():
    print(f'{kana: <8}, {reading: <8}')

AnyString = str

Japanese = str
English = str

Kanji = str
KanjiChar = str

Hiragana = str
HiraganaChar = str

Katakana = str
KatakanaChar = str


def is_katakana_char(char: str) -> bool:
    if len(char) < 1:
        return False
    if len(char) > 1:
        print(f'Warning: Misuse of `is_katakana_char({char})`, input is length {len(char)}')
        return False
    return char in katakana_all_monograms_set


def is_entirely_katakana(string: str) -> bool:
    return set(string).issubset(katakana_all_monograms_set)


def contains_katakana(string: str):
    for char in string:
        if char in katakana_all_monograms_set:
            return True
    return False


def contains_small_vowel(kana: str) -> bool:
    return len(set(kana).intersection(set(katakana_small_vowels.keys()))) != 0


def contains_small_ya_yu_yo(kana: str) -> bool:
    return len(set(kana).intersection(set(katakana_small_ya_yo_yu.keys()))) != 0


def contains_dakuten(kana: str) -> bool:
    return len(set(kana).intersection(set(katakana_dakuten.keys()))) != 0


def contains_handakuten(kana: str) -> bool:
    return len(set(kana).intersection(set(katakana_handakuten.keys()))) != 0


def strip_modifiers(kana: str) -> str:
    result = kana
    for modifier in katakana_modifiers:
        result = result.replace(modifier, '')
    return result


def strip_dakuten(kana: str) -> str:
    result = ''
    for char in kana:
        decomp = unicodedata.decomposition(char)
        if not decomp:
            result += char
            continue
        decomp = decomp.split(' ')
        if '3099' in decomp or '309A' in decomp:
            result += chr(int(decomp[0], 16))
        else:
            result += char
    return result


def katakana_table_row(kana: str) -> str:
    base_kana = strip_modifiers(strip_dakuten(kana))
    reading = katakana_to_romaji[base_kana]
    result = ''
    if reading in english_vowels:
        result = 'vowel'
    elif reading.startswith('c'):
        result = 't'
    elif reading.startswith('f'):
        result = 'h'
    elif reading == 'n':
        result = 'w'
    else:
        result = reading[0]
    if contains_dakuten(kana):
        result += '1'
    elif contains_handakuten(kana):
        result += '2'
    return result


def katakana_table_col(kana: str) -> str:
    base_kana = strip_modifiers(strip_dakuten(kana))
    reading = katakana_to_romaji[base_kana]
    if reading == 'n':
        return 'o'
    if reading == 'wo':
        return 'u'
    if contains_small_ya_yu_yo(kana):
        return 'ya' if 'ャ' in kana else 'yu' if 'ュ' in kana else 'yo'
    return reading[-1]


def chunk_modifiers(kana: str) -> list[str]:
    if not kana:
        return []
    suffix_modifiers = set(katakana_modifiers)
    suffix_modifiers.remove(katakana_duplicate_consonant)

    non_modifier_indexes = [i for i, char in enumerate(kana) if char in set(list(katakana_to_romaji.keys()) + list(katakana_dakuten.keys()) + list(katakana_handakuten.keys()))]
    possible_chunks = []
    for index in non_modifier_indexes:
        l, h = index, index + 1
        if kana[max(0, index-1)] == katakana_duplicate_consonant:
            l -= 1
        if kana[min(len(kana)-1, index+1)] in suffix_modifiers:
            h += 1
            if kana[min(len(kana)-1, index+2)] in suffix_modifiers:
                h += 1
        possible_chunks.append(kana[l:h])
    return possible_chunks


def get_reading(chunk: str) -> str:
    return all_possible_chunks_with_readings.get(chunk, '?')


def katakana_reading(kana: str) -> str:
    if not is_entirely_katakana(kana):
        raise ValueError(f'Input is not entirely katakana: {kana}')
    result = ''
    for chunk in chunk_modifiers(kana):
        result += get_reading(chunk)
    return result


def generate_option(katakana_word: str) -> str:
    chunks = chunk_modifiers(katakana_word)
    number_of_chunks_to_modify = random.randint(1, len(chunks))
    indexes_of_chunks_to_modify = random.sample(list(range(len(chunks))), number_of_chunks_to_modify)
    for index in indexes_of_chunks_to_modify:
        original_chunk = chunks[index]
        allowed_chunks = list(chunks_by_size[len(original_chunk)])
        allowed_chunks.remove(original_chunk)
        chunks[index] = random.choice(allowed_chunks)
    return ''.join(chunks)


def generate_options(katakana_word: str, count: int = 4) -> list[str]:
    wrong_options = [generate_option(katakana_word) for _ in range(count-1)]
    options = [katakana_word] + wrong_options
    random.shuffle(options)
    return options


class KatakanaWord:
    def __init__(self, kana: str):
        self.kana = kana
        self.validate(kana)

    @staticmethod
    def validate(kana: str):
        if len(kana) == 0:
            return  # The empty word is valid, useful for testing
        if kana[0] in katakana_modifiers:
            raise ValueError(f'The first letter of a word cannot be a modifier: {kana[0]}')
        if not is_entirely_katakana(kana):
            raise ValueError(f'Not entirely katakana: {kana}')


katakana_with_long_vowel = {
    kana + katakana_long_vowel: roma + roma[-1]
    for kana, roma in katakana_to_romaji.items()
    if roma[-1] in english_vowels
}
katakana_with_consonant_duplication = {
    katakana_duplicate_consonant + kana: roma[0] + roma
    for kana, roma in katakana_to_romaji.items()
    if roma[0] not in english_vowels + ['n']
}



if __name__ == '__main__':
    base_katakana_table = {k:v for k, v in katakana_to_romaji.items()}
    base_katakana_table.update(katakana_dakuten)
    base_katakana_table.update(katakana_handakuten)
    base_katakana_table.update(katakana_digraph_small_ya_yu_yo)

    katakana_table_by_row_col = {
        (katakana_table_row(kana), katakana_table_col(kana)): (kana, reading) for kana, reading in base_katakana_table.items()
    }

    row_order_dakuten_integrated = ['vowel', 'k', 'k1', 's', 's1', 't', 't1', 'n', 'h', 'h1', 'h2', 'm', 'y', 'r', 'w']
    row_order_dakuten_seperate = ['vowel', 'k', 's', 't', 'n', 'h',  'm', 'y', 'r', 'w', 'k1', 's1', 't1', 'h1', 'h2']
    for row in row_order_dakuten_seperate:
        for col in ['a', 'i', 'u', 'e', 'o', 'ya', 'yu', 'yo']:
            kana, reading = katakana_table_by_row_col.get((row, col), ('', ''))
            if kana:
                print(f'| {kana: ^7} - {reading: ^7} ', end='')
            else:
                print('|' + ' ' * 20, end='')
        print('|', end='')
        for col in ['ya', 'yu', 'yo']:
            pass
        print('\n', end='')

# for k, v in katakana_to_romaji.items():
#     print(k, v)
#
# print('-' * 80)
# for k, v in katakana_with_long_vowel.items():
#     print(k, v)
#
# print('-' * 80)
# for k, v in katakana_with_consonant_duplication.items():
#     print(k, v)

# print(strip_dakuten('プギ'))
#
# print(unicodedata.normalize('NFC', 'プ'))
# print(unicodedata.decomposition('プ'))
# print(unicodedata.decomposition('ギ'))
# print('\u30D5', '\u309A')
# print(u'プ'.encode('utf-16'))
# print(u'フ'.encode('utf-16'))




