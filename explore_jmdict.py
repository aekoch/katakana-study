from __future__ import annotations
import os.path
import lxml.etree as etree
from dataclasses import dataclass
from io import StringIO
import random
from collections import defaultdict
from itertools import chain


jmdict_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'JMdict_e.xml')
tree = etree.parse(jmdict_file)


def get_tag_counts(xml) -> dict[str, int]:
    counts = defaultdict(int)
    for child in xml:
        counts[child.tag] += 1
    return dict(counts)

def merge_tag_counts_to_tag_ranges(tag_count_dicts: list[dict[str, int]]) -> dict[str, tuple[int, int]]:
    all_keys = set().union(*(d.keys() for d in tag_count_dicts))
    required_keys = all_keys.intersection(*(d.keys() for d in tag_count_dicts))
    optional_keys = all_keys.difference(required_keys)
    result = {key: (0, 0) for key in all_keys}
    for key in all_keys:
        for tag_count_dict in tag_count_dicts:
            result[key][1] = max(result[key][1], tag_count_dict.get(key, 0))



print(get_tag_counts(tree.getroot()))
