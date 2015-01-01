# -*- coding: utf-8 -*-

from multiprocessing import freeze_support
from shutil import rmtree
import os
import tempfile
import unittest

from mitorrent import metainfo


class TestMetaDictionary(unittest.TestCase):

    def test_meta_dictionary_empty_bencode(self):
        test = metainfo.MetaDictionary().get_bencoded()
        self.assertFalse(test)


class TestMetaDictionaryAddAnnounces(unittest.TestCase):

    def test_meta_dictionary_add_announce(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        meta_dict = metainfo.MetaDictionary()
        meta_dict.info = metainfo.InfoDictionary(temp_dir)
        meta_dict.add_announce('example.com:6881')
        test = meta_dict.get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd8:announce16:example.com:68814:infod5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x13ee')  # noqa

    def test_meta_dictionary_add_announces(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        meta_dict = metainfo.MetaDictionary()
        meta_dict.info = metainfo.InfoDictionary(temp_dir)
        meta_dict.add_announce('example.com:6881')
        meta_dict.add_announce('203.0.113.29:8618')
        meta_dict.add_announce('203.0.113.79:5432')
        test = meta_dict.get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd8:announce16:example.com:688113:announce-listl16:example.com:688117:203.0.113.29:861817:203.0.113.79:5432e4:infod5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x13ee')  # noqa


class TestMetaDictionaryAddNodes(unittest.TestCase):

    def test_meta_dictionary_add_node(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        meta_dict = metainfo.MetaDictionary()
        meta_dict.info = metainfo.InfoDictionary(temp_dir)
        meta_dict.add_node('example.com:6881')
        test = meta_dict.get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd4:infod5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x13e5:nodesll11:example.comi6881eeee')  # noqa

    def test_meta_dictionary_add_nodes(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        meta_dict = metainfo.MetaDictionary()
        meta_dict.info = metainfo.InfoDictionary(temp_dir)
        meta_dict.add_node('example.com:6881')
        meta_dict.add_node('203.0.113.29:8618')
        test = meta_dict.get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd4:infod5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x13e5:nodesll11:example.comi6881eel12:203.0.113.29i8618eeee')  # noqa


class TestMetaDictionaryExtraMetadata(unittest.TestCase):

    def test_meta_dictionary_comment(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        meta_dict = metainfo.MetaDictionary()
        meta_dict.info = metainfo.InfoDictionary(temp_dir)
        meta_dict.comment = 'Such a good test comment!'
        test = meta_dict.get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd7:comment25:Such a good test comment!4:infod5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x13ee')  # noqa

    def test_meta_dictionary_created_by(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        meta_dict = metainfo.MetaDictionary()
        meta_dict.info = metainfo.InfoDictionary(temp_dir)
        meta_dict.created_by = 'Test God/2.4'
        test = meta_dict.get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd10:created by12:Test God/2.44:infod5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x13ee')  # noqa

    def test_meta_dictionary_creation(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        meta_dict = metainfo.MetaDictionary()
        meta_dict.info = metainfo.InfoDictionary(temp_dir)
        meta_dict.creation_date = 12345678
        test = meta_dict.get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd13:creation datei12345678e4:infod5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x13ee')  # noqa

    def test_meta_dictionary_website(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        meta_dict = metainfo.MetaDictionary()
        meta_dict.info = metainfo.InfoDictionary(temp_dir)
        meta_dict.website = 'http://example.com/'
        test = meta_dict.get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd4:infod5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x13e7:website19:http://example.com/e')  # noqa


class TestInfoDictionaryPayloads(unittest.TestCase):

    def test_info_dictionary_empty_payload(self):
        temp_dir = tempfile.mkdtemp()
        empty_test_file = open(temp_dir + os.sep + 'file', 'w')
        empty_test_file.write('')
        empty_test_file.close()
        with self.assertRaises(SystemExit):
            metainfo.InfoDictionary(temp_dir)
        rmtree(temp_dir)

    def test_info_dictionary_single_file_payload(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        test = metainfo.InfoDictionary(temp_dir).get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x13e')  # noqa

    def test_info_dictionary_exclude_dotfile(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        test_dotfile = open(temp_dir + os.sep + '.file', 'w')
        test_dotfile.write('Hidden')
        test_dotfile.close()
        test = metainfo.InfoDictionary(temp_dir,
                                       include_dotfiles=False).get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x13e')  # noqa

    def test_info_dictionary_include_dotfile(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        test_dotfile = open(temp_dir + os.sep + '.file', 'w')
        test_dotfile.write('Hidden')
        test_dotfile.close()
        test = metainfo.InfoDictionary(temp_dir,
                                       include_dotfiles=True).get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd5:filesld6:lengthi6e4:pathl5:.fileeed6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\x05\x136\xb2_\x98\xd9\xd3T\x97\x1a\xd3\x1ea\xdd{\x1dS!0e')  # noqa

    def test_info_dictionary_empty_payload_dir(self):
        temp_dir = tempfile.mkdtemp()
        empty_test_file = open(temp_dir + os.sep + 'file', 'w')
        empty_test_file.write('')
        empty_test_file.close()
        with self.assertRaises(SystemExit):
            metainfo.InfoDictionary(empty_test_file.name)
        rmtree(temp_dir)

    def test_info_dictionary_simple_payload_dir(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        test = metainfo.InfoDictionary(temp_dir).get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x13e')  # noqa


class TestInfoDictionaryPrivate(unittest.TestCase):

    def test_info_dictionary_private_false(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        info_dict = metainfo.InfoDictionary(temp_dir)
        info_dict.private = False
        test = info_dict.get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x137:privatei0ee')  # noqa

    def test_info_dictionary_private_true(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        info_dict = metainfo.InfoDictionary(temp_dir)
        info_dict.private = True
        test = info_dict.get_bencoded()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            b'd5:filesld6:lengthi13e4:pathl4:fileeee12:piece lengthi16384e6:pieces20:\xc5\x1e-\x8c\xd4\xb3\xabz\xbf\xaaA_\xad=O6\x94}\xdc\x137:privatei1ee')  # noqa

if __name__ == '__main__':
    freeze_support()
    unittest.main()
