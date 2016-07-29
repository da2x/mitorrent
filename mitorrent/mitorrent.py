# -*- coding: utf-8 -*-

import argparse
import hashlib
import os
import sys
import urllib.parse

from mitorrent import files
from mitorrent import metainfo

__cmdname__ = 'mitorrent'
__version__ = '0.9.6'


def bittorrent_info_hash(info_dict):
    piece_hash = hashlib.sha1()
    piece_hash.update(info_dict)
    return piece_hash.hexdigest()


def magnet_uri(btih, length, name):
    magnet_template = 'magnet:?xt=urn:btih:{0}&xl={1}&dn={2}'
    return magnet_template.format(btih, length, urllib.parse.quote(name))


def parse_user_arguments():
    user_arguments = argparse.ArgumentParser(
        description='None of these arguments are need for most uses. The \
            default is a small torrent file for use with the decentralized \
            DHT network with good compatibility. Just supply the name of a \
            file or folder and a ready to use torrent will pop out on the \
            other end.',
        epilog='The torrent file will be created in the current working \
            directory named PATH.torrent. The output can be redirected to \
            another file when processing a single file or directory: \
            {0} > myfile.torrent'.format(sys.argv[0]))
    user_arguments.add_argument('-i', '--include-dotfiles',
                                action='store_true',
                                dest='include_dotfiles',
                                help='Include hidden files and folders \
                                    (.hidden dotfiles). These are not \
                                    included by default.')
    user_arguments.add_argument('-v', '--version',
                                action='version',
                                version='{0} {1}'.format(__cmdname__,
                                                         __version__))
    network_args = user_arguments.add_argument_group(
        title='optional peer-discovery arguments',
        description='Include methods for discovering peers. All \
            arguments default to unset.')
    network_args.add_argument('-n', '--node',
                              action='append',
                              dest='nodes',
                              metavar='HOST:PORT',
                              type=test_node,
                              help='Include a UDP nodes on the DHT network \
                                  for bootstrapping fast transfers. \
                                  Argument can be used multiple times to \
                                  include more nodes.')
    network_args.add_argument('-a', '--announce',
                              action='append',
                              dest='announces',
                              metavar='URL',
                              type=str,
                              help='Include the announce URL for a tracker. \
                                  Not needed for decentralized (DHT) \
                                  torrents. Argument can used multiple times \
                                  to include more trackers.')
    private_arg = network_args.add_mutually_exclusive_group(required=False)
    private_arg.add_argument('-p', '--private',
                             action='store_true',
                             dest='private',
                             help='Mark torrent as private to disable \
                                 non-announcer peer-discovery methods. For use\
                                 on private trackers.')
    private_arg.add_argument('--no-private',
                             action='store_false',
                             dest='private',
                             help='Explicitly mark torrent as public (equivalent \
                                 to unset which is the default).')
    private_arg.set_defaults(private=None)
    nitpick_args = user_arguments.add_argument_group(
        title='optional nitpick arguments',
        description='Fine-tuning of non-essential arguments.')
    nitpick_args.add_argument('-c', '--comment',
                              type=str,
                              help='Include a comment describing the torrent \
                                  or the weather.')
    nitpick_args.add_argument('--creator',
                              metavar='NAME',
                              type=str,
                              help='Name of the software that produced the \
                                  torrent file.')
    nitpick_args.add_argument('-d', '--date',
                              type=int,
                              help='UNIX timestamp of torrent file creation.')
    nitpick_args.add_argument('-l', '--max-piece-length',
                              metavar='INT',
                              type=test_max_piece_length,
                              help='Set a ceiling on the maximum piece length.\
                                  Value must be 32kiB or larger and a power of\
                                  two. Piece length is adjusted automatically \
                                  based on the file size up to this limit. \
                                  Only change if you have very specific \
                                  requirements. Default is 16 MiB.')
    nitpick_args.add_argument('-w', '--website',
                              metavar='URL',
                              type=str,
                              help='Include a URL to a web page relevant to \
                                  the files or the torrent.')
    extra_output = user_arguments.add_argument_group(
        title='optional output arguments',
        description='Print some extra information to stdout after creating the\
            torrent. (Sent to stderr if output is redirected.)')
    extra_output.add_argument('-m', '--magnet',
                              action='store_true',
                              help='Magnet URI for the torrent')
    extra_output.add_argument('-b', '--btih',
                              action='store_true',
                              help='BitTorrent Info Hash (BTIH)')
    user_arguments.add_argument('paths',
                                nargs='+',
                                type=str,
                                help='Paths to the files or directories to be \
                                    distributed.')
    user_arguments = user_arguments.parse_args()
    return user_arguments


def test_max_piece_length(value):
    value = int(value)
    if value < (32 * 1024) or not bin(value).count('1') == 1:
        raise argparse.ArgumentTypeError(
            '{0} is not 32kiB or larger and a power of two'.format(value))
    return value


def test_node(value):
    value = str(value)
    # TODO: IPv6?
    host, colon, port = value.partition(':')
    if not colon or not port.isdigit():
        raise argparse.ArgumentTypeError(
            '{0} does not match <host:port>'.format(value))
    return value


def main():
    user_arguments = parse_user_arguments()
    if user_arguments and user_arguments.paths:
        for in_path in user_arguments.paths:
            in_path = files.check_basename_path(in_path)
            if in_path:
                in_path = files.check_basename_path(in_path)
                basename = files.file_name_from_path(in_path)
                meta_dict = metainfo.MetaDictionary()
                if user_arguments.announces:
                    for announce in user_arguments.announces:
                        meta_dict.add_announce(str(announce))
                if user_arguments.comment:
                    meta_dict.comment = str(user_arguments.comment)
                if user_arguments.creator:
                    meta_dict.created_by = str(user_arguments.creator)
                if user_arguments.date:
                    meta_dict.creation_date = int(user_arguments.date)
                if user_arguments.nodes:
                    for node in user_arguments.nodes:
                        meta_dict.add_node(str(node))
                if user_arguments.website:
                    meta_dict.website = str(user_arguments.website)
                meta_dict.info = metainfo.InfoDictionary(
                    in_path,
                    max_piece_length=user_arguments.max_piece_length,
                    include_dotfiles=user_arguments.include_dotfiles)
                meta_dict.info.name = basename
                meta_dict.info.private = user_arguments.private
                if sys.stdout.isatty():
                    extra_print_destination = sys.stdout
                else:
                    extra_print_destination = sys.stderr
                if user_arguments.btih:
                    magnet_btih = bittorrent_info_hash(
                        meta_dict.info.get_bencoded())
                    print(magnet_btih, file=extra_print_destination)
                if user_arguments.magnet:
                    magnet_btih = bittorrent_info_hash(
                        meta_dict.info.get_bencoded())
                    magnet_size = int(meta_dict.info.length)
                    magnet_name = basename
                    print(magnet_uri(
                        magnet_btih,
                        magnet_size,
                        magnet_name),
                        file=extra_print_destination)
                meta_file = meta_dict.get_bencoded()
                torrent_name = basename + '.torrent'
                if meta_file:
                    # Save to file or stdout if redirected and single
                    if not sys.stdout.isatty():
                        if len(user_arguments.paths) == 1:
                            sys.stdout.buffer.write(meta_file)
                            sys.exit(0)
                    torrent_path = os.getcwd() + os.sep + torrent_name
                    open(torrent_path, 'wb').write(meta_file)
                    print(
                        'Wrote torrent file "{0}" ({1} torrent file for \
                         {2} files).'.format(
                            torrent_name,
                            files.file_length_hfmt(len(meta_file)),
                            files.file_length_hfmt(meta_dict.info.length)),
                        file=sys.stderr)
                else:
                    print(
                        'Torrent file "{0}" could not be bencoded because \
                        reasons. Ouch.'.format(torrent_name),
                        file=sys.stderr)
            else:
                print(
                    'There was a problem accessing the file path: {0}'.format(
                        in_path),
                    file=sys.stderr)
    else:
        user_arguments.print_usage()
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
