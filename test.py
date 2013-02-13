# -*- coding: utf-8 -*-

import unittest
from slugify import slugify

class TestSequenceFunctions(unittest.TestCase):

    def test_manager(self):
        
        txt = "This is a test ---"
        r = slugify(txt)
        self.assertEquals(r, "this-is-a-test")
        
        txt = "This -- is a ## test ---"
        r = slugify(txt)
        self.assertEquals(r, "this-is-a-test")
        
        txt = 'C\'est déjà l\'été.'
        r = slugify(txt)
        self.assertEquals(r, "cest-deja-lete")

        txt = 'Nín hǎo. Wǒ shì zhōng guó rén'
        r = slugify(txt)
        self.assertEquals(r, "nin-hao-wo-shi-zhong-guo-ren")

        txt = 'Компьютер'
        r = slugify(txt)
        self.assertEquals(r, "kompiuter")

        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt)
        self.assertEquals(r, "jaja-lol-mememeoo-a")

        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=9)
        self.assertEquals(r, "jaja-lol")

        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=15)
        self.assertEquals(r, "jaja-lol-mememe")

        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=50)
        self.assertEquals(r, "jaja-lol-mememeoo-a")

        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=15, word_boundary=True)
        self.assertEquals(r, "jaja-lol-a")

        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=19, word_boundary=True)
        self.assertEquals(r, "jaja-lol-mememeoo")

        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=20, word_boundary=True)
        self.assertEquals(r, "jaja-lol-mememeoo-a")

if __name__ == '__main__':
    unittest.main()


