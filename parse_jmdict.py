from __future__ import annotations
import os.path
import xml.etree.ElementTree as ET
import lxml.etree as etree
from dataclasses import dataclass
from io import StringIO
import random
from jmdict.models import KanaReading, KanjiReading, Sense, Entry
import pykakasi
from language_utils.language_utils import contains_small_vowel, contains_small_ya_yu_yo, contains_dakuten, contains_handakuten, katakana_long_vowel, katakana_duplicate_consonant, chunk_modifiers, generate_option, generate_options, katakana_reading

kks = pykakasi.kakasi()


def get_gai1_entries(path):
    # Parse the XML file.
    tree = ET.parse(path)
    root = tree.getroot()

    # Define the XML namespace.
    ns = {'jmdict': 'http://www.edrdg.org/jmdict'}

    # Find all entries.
    entries = root.findall('JMdict:entry')

    # Filter for entries tagged with 'gai1'.
    gai1_entries = []
    for entry in entries:
        senses = entry.findall('jmdict:sense')
        for sense in senses:
            miscs = sense.findall('jmdict:misc')
            for misc in miscs:
                if misc.text == 'gai1':
                    gai1_entries.append(entry)

    return gai1_entries


def print_xml(xml):
    etree.tostring(xml, pretty_print=True, encoding='unicode')

# Use the function.
jmdict_file = os.path.abspath(os.path.dirname(__file__)) + '/JMdict_e.xml'


tree = etree.parse(jmdict_file)
# Get the root element of the tree
root = tree.getroot()
etree.indent(tree, space='  ')
print(root.tag)

# entries = tree.xpath('.//entry[r_ele/re_pri="gai1"]')
# # entries = tree.xpath('.//entry')
# for entry_xml in random.sample(entries, 5):
#     # print(etree.tostring(entry_xml, encoding='unicode', pretty_print=True))
#
#     entry = Entry.from_xml(entry_xml)
#     print(entry.kana_readings[0].kana)

# # Find the first <entry> element in the root element
# # entry = tree.find('.//entry')
# # entry = tree.xpath('//entry')[500]
entry = tree.xpath('.//entry[r_ele/re_pri="gai1"]')[30]
# # entry = tree.xpath('.//entry[r_ele/re_pri="ichi1"]')[30]
#
# print(etree.tostring(entry, encoding='unicode', pretty_print=True))
#
# # This will print the first <entry> element in the JMdict file
# # print(ET.tostring(entry, encoding='unicode'))
# etree.tostring(entry, pretty_print=True)


gai1_entries = tree.xpath('.//entry[r_ele/re_pri="gai1"]')
# print(len(gai1_entries))
# for entry_xml in random.sample(gai1_entries, 100):
#     entry = Entry.from_xml(entry_xml)
#     try:
#         print(f'{entry.kana_readings[0].kana} - {kks.convert(entry.kana_readings[0].kana)[0]["hepburn"]} - {"; ".join(entry.senses[0].glosses)}')
#     except IndexError as e:
#         print(e)
#         print(entry)
#         print_xml(entry_xml)
#         break

csv_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'output', 'csv')
all_csv_path = os.path.join(csv_dir, 'all-katakana.csv')
short_csv_path = os.path.join(csv_dir, 'short-katakana.csv')

short_entries = [entry for entry in gai1_entries if len(Entry.from_xml(entry).kana_readings[0].kana) < 8]
print(len(short_entries))
for entry_xml in random.sample(short_entries, 100):
    entry = Entry.from_xml(entry_xml)
    try:
        print(f'{entry.kana_readings[0].kana} - {kks.convert(entry.kana_readings[0].kana)[0]["hepburn"]} - {"; ".join(entry.senses[0].glosses)}')
    except IndexError as e:
        print(e)
        print(entry)
        print_xml(entry_xml)
        break

total = len(short_entries)
short_entries = [Entry.from_xml(xml) for xml in short_entries]

print('-' * 80)
has_long_vowel = [entry for entry in short_entries if katakana_long_vowel in entry.kana_readings[0].kana]
print(f'{len(has_long_vowel)}/{total} has a long vowel marker')
for entry in random.sample(has_long_vowel, 5):
    print(f'{entry.kana_readings[0].kana} - {kks.convert(entry.kana_readings[0].kana)[0]["hepburn"]} - {"; ".join(entry.senses[0].glosses)}')

print('-' * 80)
has_small_ya_yu_yo = [entry for entry in short_entries if contains_small_ya_yu_yo(entry.kana_readings[0].kana)]
print(f'{len(has_small_ya_yu_yo)}/{total} has a small ya, yu, or yo')
for entry in random.sample(has_small_ya_yu_yo, 5):
    print(f'{entry.kana_readings[0].kana} - {kks.convert(entry.kana_readings[0].kana)[0]["hepburn"]} - {"; ".join(entry.senses[0].glosses)}')

print('-' * 80)
has_small_vowel = [entry for entry in short_entries if contains_small_vowel(entry.kana_readings[0].kana)]
print(f'{len(has_small_vowel)}/{total} has a small vowel')
for entry in random.sample(has_small_vowel, 5):
    print(f'{entry.kana_readings[0].kana} - {kks.convert(entry.kana_readings[0].kana)[0]["hepburn"]} - {"; ".join(entry.senses[0].glosses)}')

print('-' * 80)
usages = {}
for entry in has_small_vowel:
    chunks = chunk_modifiers(entry.kana_readings[0].kana)
    chunks = [chunk for chunk in chunks if contains_small_vowel(chunk)]
    chunks = [chunk.replace(katakana_long_vowel, '').replace(katakana_duplicate_consonant, '') for chunk in chunks]
    for chunk in chunks:
        usages[chunk] = usages.get(chunk, []) + [entry.kana_readings[0].kana]

for kana, words in sorted(usages.items(), key=lambda x: -len(x[1])):
    print(kana, len(words))
    print(words)
    print('-' * 80)


for entry in random.sample(short_entries, 5):
    original_kana = entry.kana_readings[0].kana
    print(f'{original_kana}')
    for i, option in enumerate(generate_options(original_kana)):
        print(f'    {i+1}. {katakana_reading(option)}')
    print('-' * 80)

# entries = tree.findall('JMdict:entry')

# gai1_entries = get_gai1_entries(jmdict_file)
#
# # Print the first 10 gai1 entries, for example.
# for entry in gai1_entries[:10]:
#     print(ET.tostring(entry, encoding='unicode'))