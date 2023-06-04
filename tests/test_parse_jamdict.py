from __future__ import annotations
import lxml.etree as etree
import unittest
from jmdict.models import KanaReading, KanjiReading, Sense, Entry


class JMDictElementParseTests(unittest.TestCase):
    def test_parse_kana_reading(self):
        xml_text = '''
        <r_ele>
            <reb>おにいさん</reb>
            <re_pri>ichi1</re_pri>
        </r_ele>
        '''
        expected = KanaReading(kana='おにいさん', priority_tags=['ichi1'])
        actual = KanaReading.from_xml(etree.fromstring(xml_text))
        self.assertEqual(expected, actual)

    def test_parse_kanji_reading(self):
        xml_text = '''
        <k_ele>
            <keb>兄</keb>
            <ke_pri>news1</ke_pri>
            <ke_pri>ichi1</ke_pri>
        </k_ele>
        '''
        expected = KanjiReading(kanji='兄', priority_tags=['news1', 'ichi1'])
        actual = KanjiReading.from_xml(etree.fromstring(xml_text))
        self.assertEqual(expected, actual)

    def test_parse_sense(self):
        xml_text = '''
        <!ENTITY n "noun (common) (futsuumeishi)">
        <sense>
            <pos>&n;</pos>
            <gloss>elder brother</gloss>
            <gloss>big brother</gloss>
        </sense>
        '''
        expected = Sense(pos='&n;', glosses=['elder brother', 'big brother'])
        actual = Sense.from_xml(etree.fromstring(xml_text))
        self.assertEqual(expected, actual)

    def test_parse_entry(self):
        xml_text = '''
        <!ENTITY n "noun (common) (futsuumeishi)">
        <entry>
            <ent_seq>123456</ent_seq>
            <r_ele>
                <reb>おにいさん</reb>
                <re_pri>ichi1</re_pri>
            </r_ele>
            <k_ele>
                <keb>兄</keb>
                <ke_pri>news1</ke_pri>
                <ke_pri>ichi1</ke_pri>
            </k_ele>
            <sense>
                <pos>&n;</pos>
                <gloss>elder brother</gloss>
            </sense>
        </entry>
        '''
        expected = Entry(
            id=123456,
            kana_readings=[KanaReading(kana='おにいさん', priority_tags=['ichi1'])],
            kanji_readings=[KanjiReading(kanji='兄', priority_tags=['news1', 'ichi1'])],
            senses=[Sense(pos='&n;', glosses=['elder brother'])]
        )
        actual = Entry.from_xml(etree.fromstring(xml_text))
        self.assertEqual(expected, actual)


unittest.main()

