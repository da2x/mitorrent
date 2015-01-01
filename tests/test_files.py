# -*- coding: utf-8 -*-

from shutil import rmtree
import os
import sys
import tempfile
import unittest

from mitorrent import files


class TestCheckBasenamePath(unittest.TestCase):

    def test_check_basename_path_dir(self):
        temp_dir = tempfile.mkdtemp()
        test = files.check_basename_path(temp_dir)
        rmtree(temp_dir)
        self.assertEqual(test, temp_dir)

    def test_check_basename_path_dir_dot_is_current(self):
        test = files.check_basename_path('.')
        self.assertEqual(test, os.getcwd())

    def test_check_basename_path_dir_removes_trailing_ossep(self):
        temp_dir = tempfile.mkdtemp()
        test = files.check_basename_path(temp_dir + os.sep)
        rmtree(temp_dir)
        self.assertEqual(test, temp_dir)

    def test_check_basename_path_file(self):
        fh, temp_file = tempfile.mkstemp()
        os.close(fh)
        test = files.check_basename_path(temp_file)
        os.remove(temp_file)
        self.assertEqual(test, temp_file)

    def test_check_basename_path_file_nonexistance(self):
        fh, temp_file = tempfile.mkstemp()
        os.close(fh)
        test = files.check_basename_path(temp_file + 'nosuchfile')
        os.remove(temp_file)
        self.assertFalse(test)


class TestFileLengthHFMT(unittest.TestCase):

    def test_file_length_hfmt_bytes(self):
        test = files.file_length_hfmt(102)
        self.assertEqual(test, '102.00 B')

    def test_file_length_hfmt_kib(self):
        test = files.file_length_hfmt(1024)
        self.assertEqual(test, '1.00 KiB')

    def test_file_length_hfmt_mib(self):
        test = files.file_length_hfmt(1024 * 1024)
        self.assertEqual(test, '1.00 MiB')

    def test_file_length_hfmt_gib(self):
        test = files.file_length_hfmt(1024 * 1024 * 1024)
        self.assertEqual(test, '1.00 GiB')

    def test_file_length_hfmt_tib(self):
        test = files.file_length_hfmt(1024 * 1024 * 1024 * 1024)
        self.assertEqual(test, '1.00 TiB')

    def test_file_length_hfmt_pib(self):
        test = files.file_length_hfmt(1024 * 1024 * 1024 * 1024 * 1024)
        self.assertEqual(test, '1.00 PiB')

    def test_file_length_hfmt_eib(self):
        test = files.file_length_hfmt(1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        self.assertEqual(test, '1.00 EiB')

    def test_file_length_hfmt_zib(self):
        test = files.file_length_hfmt(1024 * 1024 * 1024 * 1024 *
                                      1024 * 1024 * 1024)
        self.assertEqual(test, '1.00 ZiB')

    def test_file_length_hfmt_yib(self):
        test = files.file_length_hfmt(1024 * 1024 * 1024 * 1024 * 1024 *
                                      1024 * 1024 * 1024)
        self.assertEqual(test, '1.00 YiB')

    def test_file_length_hfmt_xxx(self):
        test = files.file_length_hfmt(1024 * 1024 * 1024 * 1024 * 1024 *
                                      1024 * 1024 * 1024 * 1024 * 10.24)
        self.assertEqual(test, '10485.76 YiB')


class TestFileNameFromPath(unittest.TestCase):

    def test_file_name_from_path_directory(self):
        test = files.file_name_from_path('/home/user')
        self.assertEqual(test, 'user')

    def test_file_name_from_path_directory_trailing_slash(self):
        test = files.file_name_from_path('/home/user/')
        self.assertFalse(test)

    def test_file_name_from_path_empty(self):
        test = files.file_name_from_path('')
        self.assertFalse(test)

    def test_file_name_from_path_file(self):
        test = files.file_name_from_path('/home/user/text.txt')
        self.assertEqual(test, 'text.txt')

    def test_file_name_from_path_file_space(self):
        test = files.file_name_from_path('/home/user/File Name.txt')
        self.assertEqual(test, 'File Name.txt')

    def test_file_name_from_path_file_unicode(self):
        test = files.file_name_from_path('/home/user/Test — Path')
        self.assertEqual(test, 'Test — Path')

    def test_file_name_from_path_root(self):
        test = files.file_name_from_path('/')
        self.assertFalse(test)


class TestDirectoryScanner(unittest.TestCase):

    def test_directory_empty_payload(self):
        temp_dir = tempfile.mkdtemp()
        empty_test_file = open(temp_dir + os.sep + 'file', 'w')
        empty_test_file.write('')
        empty_test_file.close()
        test = files.DirectoryScanner(temp_dir).get_files()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            ([temp_dir + os.sep + 'file'],
             [{'length': 0, 'path': ['file']}],
             0))

    def test_directory_exclude_dotfile(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        test_dotfile = open(temp_dir + os.sep + '.hide', 'w')
        test_dotfile.write('Hidden')
        test_dotfile.close()
        test = files.DirectoryScanner(temp_dir,
                                      include_dotfiles=False).get_files()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            ([temp_dir + os.sep + 'file'],
             [{'length': 13, 'path': ['file']}], 13))

    def test_directory_include_dotfile(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        test_dotfile = open(temp_dir + os.sep + '.hide', 'w')
        test_dotfile.write('Hidden')
        test_dotfile.close()
        test = files.DirectoryScanner(temp_dir,
                                      include_dotfiles=True).get_files()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            ([temp_dir + os.sep + '.hide',
              temp_dir + os.sep + 'file'],
             [{'length': 6, 'path': ['.hide']},
              {'length': 13, 'path': ['file']}],
             19))

    def test_directory_exclude_dotdirectory(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        os.mkdir(temp_dir + os.sep + '.hide')
        test_file2 = open(temp_dir + os.sep + '.hide' + os.sep + 'file', 'w')
        test_file2.write('Hidden')
        test_file2.close()
        test = files.DirectoryScanner(temp_dir,
                                      include_dotfiles=False).get_files()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            ([temp_dir + os.sep + 'file'],
             [{'length': 13, 'path': ['file']}], 13))

    def test_directory_include_dotdirectory(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        os.mkdir(temp_dir + os.sep + '.hide')
        test_file2 = open(temp_dir + os.sep + '.hide' + os.sep + 'hide', 'w')
        test_file2.write('Hidden')
        test_file2.close()
        test = files.DirectoryScanner(temp_dir,
                                      include_dotfiles=True).get_files()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            ([temp_dir + os.sep + '.hide' + os.sep + 'hide',
              temp_dir + os.sep + 'file'],
             [{'path': ['.hide', 'hide'], 'length': 6},
              {'path': ['file'], 'length': 13}],
             19))

    @unittest.skipIf(sys.platform.startswith('win'),
                     'Feature not supported by Windows')
    def test_directory_exclude_unreadable(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        test_file2 = open(temp_dir + os.sep + 'unreadable', 'w')
        test_file2.write('Hidden')
        test_file2.close()
        os.chmod(temp_dir + os.sep + 'unreadable', 200)
        test = files.DirectoryScanner(temp_dir).get_files()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            ([temp_dir + os.sep + 'file'],
             [{'length': 13, 'path': ['file']}], 13))

    @unittest.skipIf(sys.platform.startswith('win'),
                     'Feature not supported by Windows')
    def test_directory_hardlink(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        os.link(temp_dir + os.sep + 'file', temp_dir + os.sep + 'file2')
        test = files.DirectoryScanner(temp_dir).get_files()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            ([temp_dir + os.sep + 'file',
             temp_dir + os.sep + 'file2'],
             [{'length': 13, 'path': ['file']},
              {'length': 13, 'path': ['file2']}],
             26))

    @unittest.skipIf(sys.platform.startswith('win'),
                     'Feature not supported by Windows')
    def test_directory_symlink(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        os.symlink(temp_dir + os.sep + 'file', temp_dir + os.sep + 'file2')
        test = files.DirectoryScanner(temp_dir).get_files()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            ([temp_dir + os.sep + 'file',
             temp_dir + os.sep + 'file2'],
             [{'length': 13, 'path': ['file']},
              {'length': 13, 'path': ['file2']}],
             26))

    @unittest.skipIf(sys.platform.startswith('win'),
                     'Feature not supported by Windows')
    def test_directory_broken_symlink(self):
        temp_dir = tempfile.mkdtemp()
        test_file = open(temp_dir + os.sep + 'file', 'w')
        test_file.write('Hello Testers')
        test_file.close()
        os.symlink(temp_dir + os.sep + 'broken-link',
                   temp_dir + os.sep + 'file2')
        test = files.DirectoryScanner(temp_dir).get_files()
        rmtree(temp_dir)
        self.assertEqual(
            test,
            ([temp_dir + os.sep + 'file'],
             [{'length': 13, 'path': ['file']}],
             13))

if __name__ == '__main__':
    unittest.main()
