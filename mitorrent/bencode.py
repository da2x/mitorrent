# -*- coding: utf-8 -*-


def bencode(item):
    return methods[type(item)](item)


def bencode_bytes(bytes):
    data = str(len(bytes)).encode('UTF-8') + b':' + bytes
    return data


def bencode_dict(dictionary):
    data = bytearray()
    for key in sorted(dictionary.keys()):
        value = dictionary[key]
        if value is None:
            continue
        data.extend(bencode(key))
        data.extend(bencode(dictionary[key]))
    data = b'd' + data + b'e'
    return data


def bencode_int(integer):
    data = b'i' + str(int(integer)).encode('UTF-8') + b'e'
    return data


def bencode_list(list):
    data = bytearray()
    for item in list:
        data.extend(bencode(item))
    data = b'l' + data + b'e'
    return data


def bencode_str(string):
    string = str(string).encode('UTF-8')
    data = str(len(string)).encode('UTF-8') + b':' + string
    return data


def __bencode_bool(boolean):
    return bencode_int(int(boolean))


methods = {
    bool: __bencode_bool,
    bytes: bencode_bytes,
    bytearray: bencode_bytes,
    dict: bencode_dict,
    int: bencode_int,
    list: bencode_list,
    tuple: bencode_list,
    str: bencode_str
}
