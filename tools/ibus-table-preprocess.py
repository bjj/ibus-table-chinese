#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim:et sts=4 sw=4
#
# ibus-table-preprocess - Apply transformations to ibus-table txt files to trim non-
#                         displayable characters and/or transfer character frequency data
#
# Copyright (c) 2022 Valve Corporation
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Trim ibus-table to available glyphs in given font and transfer frequency data')
    parser.add_argument(
        '--debug',
        action='store_true', dest='debug',
        help='Debugging on')
    parser.add_argument(
        '-s', '--source',
        required=True,
        action='store', dest='source',
        help='Specifies the file containing the table source .txt')
    parser.add_argument(
        '-o', '--output',
        required=True,
        action='store', dest='output',
        help='Specifies output file location for modified .txt')
    parser.add_argument(
        '-f', '--font',
        required=False,
        action='store', dest='font',
        help='Font path, e.g. "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc" from noto-fonts-cjk. All table entries using characters that can\'t be displayed in the given font will be commented out.')
    parser.add_argument(
        '-q', '--freq',
        required=False,
        action='store', dest='freq',
        help='Second source table .txt which will be used to update frequency data.')
    parser.add_argument(
        '--low-priority-char-threshold',
        action='store', type=int, dest='low_priority_char_threshold',
        default=1000,
        help='Cutoff for transferring priority (below, retain existing priority)')
    args = parser.parse_args()
    return args

def read_font_charset(font):
    """Extract the charset (the map of characters present in the font) to a dictionary."""
    charset = {}
    if not font:
        return charset

    import subprocess
    proc = subprocess.Popen(['fc-query', '--index=0', '--format=%{charset}', font], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        for rnge in line.decode('utf-8').split():
            startend = rnge.split('-')
            if len(startend) == 2:
                start, end = startend
            else:
                start = startend[0]
                end = startend[0]
            start, end = int(start, 16), int(end, 16)
            for i in range(start, end + 1):  # end is inclusive
                charset[i] = True
    return charset

def read_alternate_freq(source):
    """Read the frequency data from a table."""
    other_freq = {}
    if not source:
        return other_freq

    in_table = False
    with open(source) as source:
        line = source.readline()
        while line:
            if line.startswith('END_TABLE'):
                in_table = False

            if line.startswith('###'):
                pass
            elif in_table:
                try:
                    key, char, freq = line.split("\t")
                    other_freq[char] = int(freq)
                except ValueError: # some files have errors
                    pass
            if line.startswith('BEGIN_TABLE'):
                in_table = True
            line = source.readline()
    return other_freq

if __name__ == "__main__":
    args = parse_args();
    charset = read_font_charset(args.font)
    other_freq = read_alternate_freq(args.freq)

    with open(args.source) as source, open(args.output, 'w') as output:
        if args.font:
            output.write("### Filtered to characters present in %s\n" % args.font)
        if args.freq:
            output.write("### Frequency data transferred from %s\n" % args.freq)

        in_table = False
        line = source.readline()
        while line:
            if line.startswith('END_TABLE'):
                in_table = False

            if line.startswith('###'):
                pass
            elif in_table:
                okay = True
                try:
                    key, char, freq = line.split("\t")
                    freq = int(freq)
                    if args.font:
                        for c in char:
                            if ord(c) not in charset:
                                okay = False
                    if args.freq:
                        if freq >= args.low_priority_char_threshold:
                            freq = other_freq.get(char, 0) + args.low_priority_char_threshold
                            line = "%s\t%s\t%d\n" % (key, char, freq)
                except ValueError: # some files have errors
                    okay = False
                if not okay:
                    output.write("### ")

            output.write(line)

            if line.startswith('BEGIN_TABLE'):
                in_table = True
            line = source.readline()
