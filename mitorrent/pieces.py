# -*- coding: utf-8 -*-

from math import ceil, log
from multiprocessing import Array, Pipe, Process, freeze_support
import ctypes
import hashlib

from mitorrent import files


def hash_binary_piece(piece):
    piece_hash = hashlib.sha1()
    piece_hash.update(piece)
    return piece_hash.digest()


def round_up_2(value):
    return 2**ceil(log(value, 2))


def find_piece_size(byte_size, max_piece_length=None):
    if byte_size <= 0:
        return 0
    elif byte_size <= 64 * 1024:
        return max(16 * 1024, round_up_2(byte_size))
    elif byte_size < 64 * 1024 * 2200:
        return 64 * 1024
    else:
        if (max_piece_length and
                max_piece_length == round_up_2(float(max_piece_length))):
            maxsize = max_piece_length
        else:
            maxsize = 16 * 1024 * 1024
        autosize = round_up_2(byte_size / 2200)
        return min(maxsize, autosize)


def PieceReaderWorkerProcess(files_list, piece_length, arrays, pipe):
    reader = PiecesReader(files_list, piece_length)
    chunk = None
    bytes_read = 0
    try:
        chunk = reader.__next__()
        bytes_read = len(chunk)
        arrays[0].value = bytes(chunk)
    except:
        pipe.send(None)
    ready_array = 0
    while True:
        pipe.recv()
        pipe.send((ready_array, bytes_read))
        next_array = (ready_array + 1) % 2
        try:
            chunk = reader.__next__()
            bytes_read = len(chunk)
            arrays[next_array].value = bytes(chunk)
            ready_array = next_array
        except StopIteration:
            break

    pipe.send((None, None))


class Pieces:
    def __init__(self, files_list, piece_length):
        self.mypipe, self.subpipe = Pipe()
        self.arrays = (
            Array(ctypes.c_char, piece_length, lock=False),
            Array(ctypes.c_char, piece_length, lock=False))
        self.subproc = Process(
            target=PieceReaderWorkerProcess,
            args=(files_list,
                  piece_length,
                  self.arrays,
                  self.subpipe))
        self.subproc.start()

    def __iter__(self):
        return self

    def __next__(self):
        self.mypipe.send(True)
        array, bytes_read = self.mypipe.recv()
        if array is None:
            raise StopIteration
        res = self.arrays[array].raw[:bytes_read]
        return res


class PiecesReader:
    def __init__(self, files_list, piece_length):
        # empty files do not contribute pieces
        if len(files_list) < 1:
            return None
        self.files_list = [
            (fname, files.file_length(fname)) for fname in files_list]
        self.files_list = [
            (fname, size) for fname, size in self.files_list if size > 0]

        self.piece_length = piece_length
        self.pos = 0
        self.filenum = 0
        self.current = open(self.files_list[0][0], 'rb')
        self.total = sum([file[1] for file in self.files_list])

    def __iter__(self):
        return self

    def __next__(self):
        # check if we can actually get a full chunk
        piece_length = self.piece_length
        if (self.total - self.pos < piece_length):
            piece_length = self.total - self.pos
        if piece_length == 0:
            raise StopIteration

        remainder = piece_length
        res = bytearray()
        while (remainder > 0):
            filesize = self.files_list[self.filenum][1]
            file_remaining = filesize - self.current.tell()
            if file_remaining == 0:
                self.filenum = self.filenum + 1
                self.current.close()
                if self.filenum == len(self.files_list):
                    break
                self.current = open(self.files_list[self.filenum][0], 'rb')
            data = self.current.read(remainder)
            res.extend(data)
            remainder = remainder - len(data)
            self.pos = self.pos + len(data)
        return res

if __name__ == '__main__':
    freeze_support()
