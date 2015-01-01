# -*- coding: utf-8 -*-

from unittest import TestCase

from mitorrent import bencode


class TestBencoder(TestCase):

    def test_bencode_bytes(self):
        test = bencode.bencode_bytes(bytearray.fromhex('f09f92a9'))
        self.assertEqual(test, '4:💩'.encode('UTF-8'))  # Pile of Poo

    def test_bencode_bool_False(self):
        test = bencode.bencode(False)
        self.assertEqual(test, 'i0e'.encode('UTF-8'))

    def test_bencode_bool_true(self):
        test = bencode.bencode(True)
        self.assertEqual(test, 'i1e'.encode('UTF-8'))

    def test_bencode_dict(self):
        test = bencode.bencode_dict({'key': 'value'})
        self.assertEqual(test, str('d3:key5:valuee').encode('UTF-8'))

    def test_bencode_int(self):
        test = bencode.bencode_int(int(12345))
        self.assertEqual(test, str('i12345e').encode('UTF-8'))

    def test_bencode_int_neg(self):
        test = bencode.bencode_int(int(-1))
        self.assertEqual(test, str('i-1e').encode('UTF-8'))

    def test_bencode_int_neg_zero(self):
        test = bencode.bencode_int(int(-0))
        self.assertEqual(test, str('i0e').encode('UTF-8'))

    def test_bencode_int_zero(self):
        test = bencode.bencode_int(int(0))
        self.assertEqual(test, str('i0e').encode('UTF-8'))

    def test_bencode_list(self):
        test = bencode.bencode_list([12, 'three', 45])
        self.assertEqual(test, str('li12e5:threei45ee').encode('UTF-8'))

    def test_bencode_none(self):
        self.assertRaises(KeyError, bencode.bencode, None)

    def test_bencode_str(self):
        test = bencode.bencode_str(str('Hello World'))
        self.assertEqual(test, str('11:Hello World').encode('UTF-8'))

    def test_bencode_str_unicode(self):
        test = bencode.bencode_str(str('Blåbærsyltetøy'))
        self.assertEqual(test, str('17:Blåbærsyltetøy').encode('UTF-8'))

    def test_bencode(self):
        test = bencode.bencode({'key': 'value',
                                'more': {1: [2, 3]},
                                'less': bytearray.fromhex('f09f92a9')})
        self.assertEqual(
            test,
            str('d3:key5:value4:less4:💩4:moredi1eli2ei3eeee').encode('UTF-8'))
