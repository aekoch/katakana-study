from __future__ import annotations
import os.path
import xml.etree.ElementTree as ET
import lxml.etree as etree
from dataclasses import dataclass
from io import StringIO
import random


@dataclass
class KanaReading:
    """wraps a <r_ele> tag"""
    kana: str  # <reb> tag - the kana reading
    priority_tags: list[str]  # <re_pri> tag - optional - potentially multiple - examples: gai1, ichi2, news1

    @classmethod
    def from_xml(cls, xml) -> KanaReading:
        kana = xml.find('reb').text
        priority_tags = [pri.text for pri in xml.findall('re_pri')]
        return KanaReading(kana=kana, priority_tags=priority_tags)


@dataclass
class KanjiReading:
    """wraps a <k_ele> tag"""
    kanji: str  # <keb> tag - the kanji
    priority_tags: list[str]  # <re_pri> tags - optional - potentially multiple - examples: gai1, ichi2, news1

    @classmethod
    def from_xml(cls, xml) -> KanjiReading:
        kanji = xml.find('keb').text
        priority_tags = [pri.text for pri in xml.findall('ke_pri')]
        return KanjiReading(kanji, priority_tags)


@dataclass
class Sense:
    """wraps a <sense> tag"""
    pos: str  # <pos> tag - part of speach - may also contain other data like (common) or (temporal)
    glosses: list[str]  # <gloss> tags - at least one required - potentially multiple - This represents one distinct meaning
    # TODO: Handle <xref> tags
    # TODO: Handle <misc> tags
    # TODO: Handle <s_inf> tags

    @property
    def jisho_style_text(self) -> str:
        return f'({self.pos}) {"; ".join(self.glosses)}'

    @classmethod
    def from_xml(cls, xml) -> Sense:
        pos = xml.find('pos').text
        glosses = [gloss.text for gloss in xml.findall('gloss')]
        return Sense(pos, glosses)


@dataclass
class Entry:
    id: int
    kana_readings: list[KanaReading]
    kanji_readings: list[KanjiReading]
    senses: list[Sense]

    @classmethod
    def from_xml(cls, xml) -> Entry:
        _id = int(xml.find('ent_seq').text)
        kana_readings = [KanaReading.from_xml(e) for e in xml.findall('r_ele')]
        kanji_readings = []  # [KanaReading.from_xml(e) for e in xml.findall('reb')]
        senses = [Sense.from_xml(e) for e in xml.findall('sense')]
        return Entry(_id, kana_readings, kanji_readings, senses)