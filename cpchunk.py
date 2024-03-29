#!/usr/bin/env python
# cpchunk: copy chunks of files
#
# Copyright 2014 Kef Schecter
# This program is under the MIT license.
# See COPYING.txt for license terms.
#
# Written for Python 3.4
import argparse
import sys


# NB: also update setup.py when changing
__version__ = '1.0.0.4'


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = get_args(argv)

    src = args.src
    dest = args.dest
    src_offset = int(args.src_offset, 0)
    dest_offset = args.dest_offset
    append_mode = args.append
    length = int(args.len, 0)

    if append_mode:
        out_mode = 'ab'
    elif dest_offset is None:
        dest_offset = 0
        out_mode = 'wb'                     # truncate output
    else:
        dest_offset = int(dest_offset, 0)
        out_mode = 'r+b'                    # do not truncate output

    try:
        with open(src, 'rb') as infile:
            infile.seek(src_offset)
            data = infile.read(length)
    except OSError as e:
        print("Error reading {0}: {1}".format(src, e), file=sys.stderr)
        return 1

    try:
        with open(dest, out_mode) as outfile:
            if not append_mode:
                outfile.seek(dest_offset)
            outfile.write(data)
    except OSError as e:
        print("Error writing {0}: {1}".format(dest, e), file=sys.stderr)
        return 1


def get_args(argv):
    parser = argparse.ArgumentParser(
        prog="cpchunk",
        description="Copy part or all of a file and insert it into "
                    "another file.",
        epilog="All numbers are in decimal unless prefixed with 0x (hex), 0b "
               "(binary), or 0o (octal). Unless using one of these prefixes, "
               "a nonzero number may not start with the digit 0."
    )
    parser.add_argument('src')
    parser.add_argument('dest')
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument(
        '-s', '--src-offset',
        default='0',
        help="offset in source file to copy from. Default 0")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-d', '--dest-offset',
        help="offset in destination file to copy to. "
             "Data at this offset will be overwritten. "
             "If not specified, the output file will be truncated"
    )
    group.add_argument(
        '-a', '--append',
        action='store_true',
        help="append to end of destination file. "
             "Mutually exclusive with -d"
    )

    parser.add_argument(
        '-l', '--len', '--size',
        default='-1',
        help="number of bytes to copy. "
             "If not specified, copy whole file")

    return parser.parse_args(argv)


if __name__ == '__main__':
    sys.exit(main())
