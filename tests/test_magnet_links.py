# -*- coding: utf-8 -*-

import unittest

from mitorrent import mitorrent


class TestBTIH(unittest.TestCase):

    def test_bittorrent_info_hash_from_dict(self):
        test = mitorrent.bittorrent_info_hash(b'd3:key5:valuee')
        self.assertEqual(test, 'ccbb2fe3e9d73c084bd141dcfdb644b888321d67')


class TestMagnetLinks(unittest.TestCase):

    def test_magnet_link(self):
        test = mitorrent.magnet_uri('hash', 123, 'name.ext')
        self.assertEqual(test, 'magnet:?xt=urn:btih:hash&xl=123&dn=name.ext')

    def test_magnet_link_urlencode_name(self):
        # name = string space string space en-dash space string
        test = mitorrent.magnet_uri('h1s2', 123, 'My Name – Test')
        self.assertEqual(
            test,
            'magnet:?xt=urn:btih:h1s2&xl=123&dn=My%20Name%20%E2%80%93%20Test')

if __name__ == '__main__':
    unittest.main()
