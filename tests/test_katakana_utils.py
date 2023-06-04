import unittest
from language_utils.language_utils import is_entirely_katakana
from language_utils.language_utils import contains_small_vowel
from language_utils.language_utils import contains_small_ya_yu_yo
from language_utils.language_utils import contains_dakuten
from language_utils.language_utils import contains_handakuten
from language_utils.language_utils import strip_modifiers
from language_utils.language_utils import strip_dakuten
from language_utils.language_utils import chunk_modifiers
from language_utils.language_utils import generate_option


class TestKatakana(unittest.TestCase):
    def test_contains_small_vowel(self):
        self.assertTrue(contains_small_vowel('ファ'))
        self.assertFalse(contains_small_vowel('フ'))

    def test_contains_small_ya_yu_yo(self):
        self.assertTrue(contains_small_ya_yu_yo('キャ'))
        self.assertFalse(contains_small_ya_yu_yo('キ'))

    def test_contains_dakuten(self):
        self.assertTrue(contains_dakuten('ギ'))
        self.assertFalse(contains_dakuten('キ'))
        self.assertFalse(contains_dakuten('ピ'))

    def test_contains_handakuten(self):
        self.assertTrue(contains_handakuten('ピ'))
        self.assertFalse(contains_handakuten('ギ'))
        self.assertFalse(contains_handakuten('キ'))

    def test_strip_modifiers(self):
        self.assertEqual(strip_modifiers('カッギャー'), 'カギ')

    def test_strip_dakuten(self):
        self.assertEqual(strip_dakuten('ギピ'), 'キヒ')
        self.assertEqual(strip_dakuten('カッギャー'), 'カッキャー')

    def test_chunk_by_modifier(self):
        self.assertEqual(chunk_modifiers(''), [])
        self.assertEqual(chunk_modifiers('カカ'), ['カ', 'カ'])
        self.assertEqual(chunk_modifiers('カーギャ'), ['カー', 'ギャ'])
        self.assertEqual(chunk_modifiers('カギー'), ['カ', 'ギー'])
        self.assertEqual(chunk_modifiers('カギャー'), ['カ', 'ギャー'])
        self.assertEqual(chunk_modifiers('カッギャー'), ['カ', 'ッギャー'])

    def test_generate_choices(self):
        original = 'カッギャーカカ'
        for _ in range(10):
            option = generate_option(original)
            self.assertNotEqual(original, option, f'{option} should not equal {original}')
            self.assertEqual(len(chunk_modifiers(original)), len(chunk_modifiers(option)), f'{option} has a different number of chunks than {original}')
            self.assertTrue(is_entirely_katakana(option), f'{option} is not entirely katakana')


if __name__ == '__main__':
    unittest.main()
