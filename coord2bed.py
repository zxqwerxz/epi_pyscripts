#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert a list of coordinates into a BED file or coordaintes.

This module takes a tab-delimited file of Ensembl-style coordinates and
converts it into a BED file format.

Example:
    python coord2bed.py [infile] > [out.bed]

Expected infile format (tab-delimited file):
    Column A: Ensembl-style coordinate
        chr20:34,141,593-34,141,709
        chr20:34,150,777-34,150,924
        chr20:34,150,777-34,150,924
    Column B (optional): Name
        EPD001C
        EPD001D
        EPD002C
"""

import argparse

__author__ = 'Jeffrey Zhou'
__copyright__ = 'Copyright (C) 2017, EpigenDx Inc.'
__credits__ = ['Jeffrey Zhou']
__version__ = '0.0.1'
__status__ = 'Prototype'


def print_amplicon(amplicon):
    """Print a given amplicon into tsv format.

    Args:
        amplicon (dict of str): Dictionary representing an amplicon

    Returns:
        None

    """
    print '\t'.join([
        amplicon['chr'],
        str(amplicon['start']),
        str(amplicon['end']),
        amplicon['name'],
    ])


def main(infile, expand_list, merge):
    """Run main method.

    Args:
        infile (str): The filename of the amplicon coordinate list.

    Returns:
        None

    """
    # Read csv file
    coord_list = []
    with open(infile, 'r') as f:
        for line in f:
            row = line.strip().split('\t')
            coordinate = row[0].strip().replace(',', '')
            coord_list.append({
                'name': row[1],
                'chr': coordinate.split(":")[0],
                'start': int(coordinate.split(":")[1].split("-")[0]),
                'end': int(coordinate.split(":")[1].split("-")[1]),
            })

    if expand_list:
        for cor in coord_list:
            cor['start'] = cor['start'] - expand_list[0]
            cor['end'] = cor['end'] + expand_list[1]

    if merge:
        sorted_list = sorted(coord_list, key=lambda k: (k['chr'], k['start']))
        merged_list = []
        last = None
        for cor in sorted_list:
            if last:
                if (cor['chr'] == last['chr'] and cor['start'] < last['end']):
                    # These amplicons are overlapping
                    last['name'] = last['name'] + "_" + cor['name']
                    last['end'] = cor['end']
                else:
                    merged_list.append(last)
                    last = cor
            else:
                last = cor
        merged_list.append(last)
        coord_list = merged_list

    # Print the coordinate list
    for cor in coord_list:
        print '\t'.join([
            cor['chr'],
            str(cor['start']),
            str(cor['end']),
            cor['name'],
        ])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        metavar="coordinate_list",
                        help="line-delimited file of coordinates")
    parser.add_argument('-e', '--expand',
                        nargs=2,
                        type=int,
                        help="Expand flanking sequence by n bp")
    parser.add_argument('--merge',
                        action="store_true",
                        help="Set flag to merge overlapping coordinates")
    args = parser.parse_args()
    main(args.infile, args.expand, args.merge)
