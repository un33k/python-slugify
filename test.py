# -*- coding: utf-8 -*-

import unittest
from slugify import slugify

class TestSequenceFunctions(unittest.TestCase):

    def test_space_dash(self):
        txt = "This is a test ---"
        r = slugify(txt)
        self.assertEquals(r, "this-is-a-test")

    def test_special_chars(self):
        txt = 'C\'est déjà l\'été.'
        r = slugify(txt)
        self.assertEquals(r, "cest-deja-lete")

        txt = 'Nín hǎo. Wǒ shì zhōng guó rén'
        r = slugify(txt)
        self.assertEquals(r, "nin-hao-wo-shi-zhong-guo-ren")

        txt = '影師嗎'
        r = slugify(txt)
        self.assertEquals(r, "ying-shi-ma")

if __name__ == '__main__':
    unittest.main()


