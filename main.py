import jamdict
from jamdict import Jamdict

jam = Jamdict()

# jam.jmnedict.search()

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
    'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
    'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
    'ダ': 'da', 'ヂ': 'dji', 'ヅ': 'dzu', 'デ': 'de', 'ド': 'do',
    'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
    'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
}
romaji_to_katakana = {roma: kana for kana, roma in katakana_to_romaji.items()}


def lookup_words(kana: str, length: int, limit: int = None) -> list[jamdict.util.JMDEntry]:
    result = []
    query_prototype = '?' * length
    for i in range(length):
        query = query_prototype[:i] + kana + query_prototype[i+1:]
        print(f'Searching for query: {query}')
        response = jam.lookup(query)
        print(f'Got {len(response.entries)}')
        for entry in response.entries:
            result.append(entry)
            if len(result) >= limit:
                break

    return result


result = jam.lookup('%ふ?')
for entry in result.entries:
    print(entry.text(no_id=True))
    # print(entry)
    print(entry.senses)
    print('-' * 80)


# for entry in lookup_words('ミ', length=4, limit=10):
#     print(entry)
