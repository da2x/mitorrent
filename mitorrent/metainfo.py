# -*- coding: utf-8 -*-

import os
import sys

from mitorrent import bencode as bencoder
from mitorrent import files
from mitorrent import pieces

bencode = bencoder.bencode


class MetaDictionary():

    def __init__(self):
        self.announces = []
        self.comment = None
        self.created_by = None
        self.creation_date = None
        self.info = None
        self.nodes = []
        self.website = None

    def add_node(self, input):
        host, colon, port = input.partition(':')
        self.nodes.append([str(host), int(port)])

    def add_announce(self, address):
        self.announces.append(str(address))

    def get_bencoded(self):
        meta_dictionary = {
            'comment': self.comment,
            'created by': self.created_by,
            'creation date': self.creation_date,
            'website': self.website
        }
        if not self.info:
            return False
        meta_dictionary.update({
            'info': self.info.get()
        })
        if len(self.announces) == 1:
            meta_dictionary.update({
                'announce': self.announces[0]
            })
        elif len(self.announces) > 1:
            meta_dictionary.update({
                'announce': self.announces[0],
                'announce-list': self.announces
            })
        if self.nodes:
            meta_dictionary['nodes'] = self.nodes
        return bencode(meta_dictionary)


class InfoDictionary():

    def __init__(self, path, max_piece_length=None, include_dotfiles=False):
        self.path = path
        self.files = []
        # self.length should always hold total length even for multifile
        self.length = None
        self.name = None
        self.piece_length = None
        self.pieces = None
        self.private = None
        self.scan_payload(path,
                          max_piece_length=max_piece_length,
                          include_dotfiles=include_dotfiles)

    def scan_payload(self,
                     path,
                     max_piece_length=None,
                     include_dotfiles=False):
        path = files.check_basename_path(path)
        if path:
            if os.path.isfile(path):
                file_list = [path]
                self.length = files.file_length(path)
            elif os.path.isdir(path):
                dir_contents = files.DirectoryScanner(
                    path,
                    include_dotfiles=include_dotfiles)
                file_list, files_dict_list, length = dir_contents.get_files()
                self.files = files_dict_list
                self.length = length
            else:
                raise IOError

            if self.length < 1:
                print('Transfer payload consists entirely of empty files or \
                      nothing. Pointless to continue.',
                      file=sys.stderr)
                sys.exit(1)
            piece_length = pieces.find_piece_size(
                self.length,
                max_piece_length=max_piece_length)
            self.piece_length = piece_length
            pieces_hash = b''
            binary_pieces = pieces.Pieces(
                file_list,
                piece_length=piece_length)
            for piece in binary_pieces:
                pieces_hash += pieces.hash_binary_piece(piece)
            self.pieces = pieces_hash

    def get_bencoded(self):
        return bencode(self.get())

    def get(self):
        # multifile does not set length but does set files
        info_dict = {
            'name': self.name,
            'piece length': self.piece_length,
            'pieces': self.pieces,
            'private': self.private
        }
        if os.path.isdir(self.path) and len(self.files) > 0:
            info_dict['files'] = self.files
        elif os.path.isfile(self.path) and self.length:
            info_dict['length'] = self.length
        else:
            print('Invalid torrent: Either a direcory with one or more files\
                   or a single file must be set.',
                  file=sys.stderr)
            sys.exit(1)
        return info_dict
