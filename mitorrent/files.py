# -*- coding: utf-8 -*-

import os
import sys


def check_basename_path(in_path):
    # in particular, this expands current dir when given as a dot
    in_path = os.path.abspath(in_path)
    if os.access(in_path, os.F_OK | os.R_OK):
        if os.path.isdir(in_path) and in_path.endswith(os.sep):
            # Strip path separator for folders
            # Behavior used in os.path.basename() and the output name
            return in_path[:-1]
        return in_path
    return False


def file_length(path):
    try:
        return os.path.getsize(path)
    except FileNotFoundError:
        return 0


def file_length_hfmt(byte_length):
    for human_terms in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']:
        if float(byte_length) < float(1024):
            return '{0:.2f} {1}'.format(byte_length, human_terms)
        byte_length = byte_length / float(1024)
    return '{0:.2f} YiB'.format(byte_length)


def file_name_from_path(path):
    name = os.path.basename(path)
    if name and name != '':
        return name
    return False


class DirectoryScanner:

    def __init__(self, directory, include_dotfiles=False):
        self._dir = directory
        self._include_dotfiles = include_dotfiles

    def get_files(self):
        base_dir = self._dir
        infodir = []
        allfiles = []
        total_length = 0
        infodir_dict = dict()

        for subdir, subdirlist, pathlist in os.walk(base_dir,
                                                    followlinks=True):
            if not self._include_dotfiles:
                dotdirs = [
                    subdir for subdir in subdirlist if subdir.startswith('.')]
                for dotdir in dotdirs:
                    print('Skipping: {0} (hidden/dotfile)'.format(
                        os.path.relpath(os.path.join(subdir, dotdir),
                                        base_dir) + os.sep),
                          file=sys.stderr)
                    subdirlist.remove(dotdir)
            for path in pathlist:
                fullpath = os.path.join(subdir, path)
                relpath = os.path.relpath(fullpath, base_dir)
                path_components = self.path2list(
                    os.path.relpath(fullpath, base_dir))
                if not self._include_dotfiles:
                    if path.startswith('.'):
                        print('Skipping: {0} (hidden/dotfile)'.format(relpath),
                              file=sys.stderr)
                        continue
                try:
                    open(fullpath, 'rb').close()
                except:
                    print(
                        'Skipping: {0} (unreadable)'.format(
                            relpath),
                        file=sys.stderr)
                    continue
                #infodir.append(self.file2infodict(fullpath, path_components))
                infodir_dict[fullpath] = self.file2infodict(fullpath, path_components)
                allfiles.append(fullpath)
                total_length += file_length(fullpath)
        allfiles = sorted(allfiles, key=str.lower)
        infodir = [infodir_dict[af] for af in allfiles]
        return (allfiles, infodir, total_length)

    def file2infodict(self, fullpath, path_components):
        return {
            'length': file_length(fullpath),
            'path': path_components,
        }

    def path2list(self, path):
        res = []
        head, tail = os.path.split(path)
        res.append(tail)
        while not head == '':
            head, tail = os.path.split(head)
            res.append(tail)
        res.reverse()
        return res
