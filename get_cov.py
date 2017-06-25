#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Get coverage on every position on a list of bam files.

This module takes a list of bam files and print the coverage for each position
and sample.

Example:
    python get_cov.py [ infile1 infile2 ... infileN ] > [out.csv]

Outfile column structure
    Column A: Sample Name
    Column B: Chromosome/sequence name
    Column C: position
    Column D: Coverage
    Column E: Number of A's
    Column F: Number of C's
    Column G: Number of G's
    Column H: Number of T's
    Column I: Number of deletions
"""

import argparse
import pysam

__author__ = 'Jeffrey Zhou'
__copyright__ = 'Copyright (C) 2017, EpigenDx Inc.'
__credits__ = ['Jeffrey Zhou']
__version__ = '0.0.1'
__status__ = 'Prototype'


def main(bam_list):
    """Execute main method.

    Args:
        bam_list (list of str): List of filenames of bam files

    Returns:
        None

    """
    for bam in bam_list:
        filename = bam.split('.')[-2]
        samfile = pysam.AlignmentFile(bam, 'rb')
        for c in samfile.pileup():
            base = [0, 0, 0, 0, 0]
            for r in c.pileups:
                if not r.is_del and not r.is_refskip:
                    seq = r.alignment.query_sequence[r.query_position]
                    if seq == 'A':
                        base[0] = base[0] + 1
                    elif seq == 'C':
                        base[1] = base[1] + 1
                    elif seq == 'G':
                        base[2] = base[2] + 1
                    elif seq == 'T':
                        base[3] = base[3] + 1
                if r.is_del:
                    base[4] = base[4] + 1
            record = [
                filename,
                c.reference_name,
                str(c.pos),
                str(c.n),
                str(base[0]),
                str(base[1]),
                str(base[2]),
                str(base[3]),
                str(base[4])
            ]
            print "\t".join(record)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infiles',
                        metavar='bamfiles',
                        nargs='+',
                        help='List of bam files')
    args = parser.parse_args()
    main(args.infiles)
