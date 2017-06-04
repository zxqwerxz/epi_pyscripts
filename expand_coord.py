#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Expand the coordinate range of amplicons by n bp without overlapping.

This module takes a comma-delimited file of PCR amplicons and their genomic
coordinates and expands the coordinate range by a given number of base pairs.
If any amplicons overlap after coordinate expansion, they will be merged.

Example:
    python expand_coord.py infile.csv 100 100 > outfile.csv

Expected infile format (comma-delimited file):
    Column A: Amplicon name
    Column B: Chromosome name
    Column C: Start position
    COlumn D: End position
"""


def print_amplicon(amplicon):
    """Print a given amplicon into csv format.

    Args:
        amplicon (dict of str): Dictionary representing an amplicon

    Returns:
        None

    """
    print ','.join([
        amplicon['amplicon'],
        amplicon['chr'],
        str(amplicon['start']),
        str(amplicon['end'])
    ])


def main(infile, upstream, downstream):
    """Expand a csv file of amplicons by a given number of bases.

    Args:
        infile (str): The csv file containing the list of amplicons
        upstream (int): Number of bases to expand upstream of start.
        downstream (int): Number of bases to expand downstream of end.

    Returns:
        None

    """
    # Read csv file
    amplicon_list = []
    with open(infile, 'r') as f:
        for line in f:
            row = line.strip().split(',')
            amplicon_list.append({
                'amplicon': row[0],
                'chr': row[1],
                'start': int(row[2]),
                'end': int(row[3]),
            })

    # Sort csv file
    sorted_list = sorted(amplicon_list, key=lambda k: (k['chr'], k['start']))

    # Iterate through sorted list and expand the coordinates
    for amplicon in sorted_list:
        amplicon['start'] = amplicon['start'] - upstream
        amplicon['end'] = amplicon['end'] + downstream

    # Iterate one more time to merge overlapping amplicons
    last = None
    for amp in sorted_list:
        if last:
            if (amp['chr'] == last['chr'] and amp['start'] < last['end']):
                # These amplicons are overlapping
                last['amplicon'] = last['amplicon'] + "_" + amp['amplicon']
                last['end'] = amp['end']
            else:
                print_amplicon(last)
                last = amp
        else:
            last = amp
    print_amplicon(last)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        metavar="amplicon_list",
                        help="csv file of amplicon coordinates")
    parser.add_argument('upstream',
                        metavar="bp_upstream",
                        help="number of bases upstream of start",
                        type=int)
    parser.add_argument('downstream',
                        metavar="bp_downstream",
                        help="number of bases downstream of end",
                        type=int)
    args = parser.parse_args()
    main(args.infile, args.upstream, args.downstream)
