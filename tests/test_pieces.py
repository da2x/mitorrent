# -*- coding: utf-8 -*-

import unittest

from mitorrent import pieces


class TestPiecesHashing(unittest.TestCase):

    def test_hash_binary_piece(self):
        test = pieces.hash_binary_piece(b'Hello World')
        self.assertEqual(
            test,
            b'\nMU\xa8\xd7x\xe5\x02/\xabp\x19w\xc5\xd8@\xbb\xc4\x86\xd0')


class TestRoundUpTwo(unittest.TestCase):

    def test_round_up_2_neative(self):
        self.assertRaises(ValueError, pieces.round_up_2, -10)

    def test_round_up_2_zero(self):
        self.assertRaises(ValueError, pieces.round_up_2, 0)

    def test_round_up_2_three(self):
        test = pieces.round_up_2(3)
        self.assertEqual(test, 4)

    def test_round_up_2_normal(self):
        test = pieces.round_up_2(1024)
        self.assertEqual(test, 1024)

    def test_round_up_2_large(self):
        test = pieces.round_up_2(1536)
        self.assertEqual(test, 2048)


class TestFindPieceSize(unittest.TestCase):

    def test_find_piece_size_negative(self):
        test = pieces.find_piece_size(-1024)
        self.assertEqual(test, 0)

    def test_find_piece_size_one(self):
        test = pieces.find_piece_size(1)
        self.assertEqual(test, 16384)

    def test_find_piece_size_zero(self):
        test = pieces.find_piece_size(0)
        self.assertEqual(test, 0)

    def test_find_piece_size_14KiB(self):
        test = pieces.find_piece_size(144179199)
        self.assertEqual(test, 65536)

    def test_find_piece_size_30MiB(self):
        test = pieces.find_piece_size(30410000)
        self.assertEqual(test, 65536)

    def test_find_piece_size_760MiB(self):
        test = pieces.find_piece_size(796900000)
        self.assertEqual(test, 524288)

    def test_find_piece_size_1_5GiB(self):
        test = pieces.find_piece_size(1610000000)
        self.assertEqual(test, 1048576)

    def test_find_piece_size_1_5GiB_500MiB_max_length(self):
        test = pieces.find_piece_size(1610000000,
                                      max_piece_length=536870912)
        self.assertEqual(test, 1048576)

    def test_find_piece_size_105TiB_256MiB_max_length(self):
        test = pieces.find_piece_size(115400000000000,
                                      max_piece_length=268435456)
        self.assertEqual(test, 268435456)

    def test_find_piece_size_105TiB_invalid_max_length(self):
        test = pieces.find_piece_size(115400000000000,
                                      max_piece_length=425769801)
        self.assertEqual(test, 16777216)

    def test_find_piece_size_189YiB(self):
        test = pieces.find_piece_size(228500000000000000000000000)
        self.assertEqual(test, 16777216)

    def test_find_piece_size_189YiB_1024MiB_max_length(self):
        test = pieces.find_piece_size(228500000000000000000000000,
                                      max_piece_length=1073741824)
        self.assertEqual(test, 1073741824)

if __name__ == '__main__':
    unittest.main()
