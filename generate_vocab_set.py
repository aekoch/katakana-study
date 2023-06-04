from __future__ import annotations
from typing import Optional
import os.path
import json
import lxml.etree as etree
from jmdict.models import Entry
from language_utils.language_utils import is_entirely_katakana, katakana_reading

jmdict_file = os.path.abspath(os.path.dirname(__file__)) + '/JMdict_e.xml'

tree = etree.parse(jmdict_file)

gai1_entries = tree.xpath('.//entry[r_ele/re_pri="gai1"]')
gai2_entries = tree.xpath('.//entry[r_ele/re_pri="gai2"]')

short_gai1_entries = [entry for entry in gai1_entries if len(Entry.from_xml(entry).kana_readings[0].kana) < 8]
short_gai2_entries = [entry for entry in gai2_entries if len(Entry.from_xml(entry).kana_readings[0].kana) < 8]


def xml_to_vocab_entry(xml) -> Optional[VocabEntry]:
    entry = Entry.from_xml(xml)
    kana = entry.kana_readings[0].kana
    if not is_entirely_katakana(kana):
        return None
    reading = katakana_reading(kana)
    meaning = "; ".join(entry.senses[0].glosses[:5])
    return VocabEntry(kana, reading, meaning)


class VocabEntry:
    def __init__(self, kana: str, reading: str, meaning: str):
        self.kana = kana
        self.reading = reading
        self.meaning = meaning

    def to_json(self) -> dict:
        return vars(self)

    @classmethod
    def from_json(cls, data: dict) -> VocabEntry:
        return cls(**data)


class VocabSet:
    def __init__(self, entries: list[VocabEntry]):
        self.entries = entries

    def to_json(self) -> list[dict]:
        return [entry.to_json() for entry in self.entries]

    @classmethod
    def from_json(cls, data: list[dict]) -> VocabSet:
        return VocabSet([VocabEntry.from_json(dat) for dat in data])

    def save(self, path: str):
        with open(path, 'w') as f:
            content = json.dumps(self.to_json(), indent=2, ensure_ascii=False)
            f.write(content)
        print(f'Saved vocab set with {len(entries)} entries to {path}')

    @classmethod
    def load(cls, path: str) -> VocabSet:
        with open(path) as f:
            content = f.read()
        data = json.loads(content)
        return cls.from_json(data)


output_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'gai1_short.vocab.json')
with open(output_path, 'w') as file:
    entries = [xml_to_vocab_entry(xml) for xml in short_gai1_entries]
    entries = [entry for entry in entries if entry is not None]
    vocab = VocabSet(entries)
    content = json.dumps(vocab.to_json(), indent=2, ensure_ascii=False)
    file.write(content)

output_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'gai2_short.vocab.json')
with open(output_path, 'w') as file:
    entries = [xml_to_vocab_entry(xml) for xml in short_gai2_entries]
    entries = [entry for entry in entries if entry is not None]
    vocab = VocabSet(entries)
    content = json.dumps(vocab.to_json(), indent=2, ensure_ascii=False)
    file.write(content)
