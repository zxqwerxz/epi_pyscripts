#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fetch genomic sequence for a list of genome coordinates from ENSEMBL.

This module takes a comma-delimited file of genomic coordinates and ouputs a
single FASTA file containing the genomic sequences. This is done by leveraging
the ENSEMBL REST API.

Example:
    python fetch_seq.py infile.csv human > outfile.fasta

Expected infile format (comma-delimited file):
    Column A: Desired FASTA entry name (e.g. ADS2830)
    Column B: Chromosome name (e.g. X)
    Column C: Start position (e.g. 431000)
    Column D: End position (e.g. 432000)
    Column E: Strand (Optional: default to +) (e.g. -)

Valid species options can be found in the ensembl website. Either the official
alias (e.g. mouse, rat, human) or the scientific name (e.g. homo_sapiens) can
be used.

Note that coordinates automatically assume the most recent ensembl assembly for
a given species.

TODO:
* Providing strand information in the infile is completely untested.
* Error handling if queried sequence does not exist.

"""

import argparse
import json
import requests
import sys

__author__ = 'Jeffrey Zhou'
__copyright__ = 'Copyright (C) 2017, EpigenDx Inc.'
__credits__ = ['Jeffrey Zhou']
__version__ = '0.0.1'
__status__ = 'Prototype'

api = 'http://rest.ensembl.org/sequence/region/'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}


def print_seq(seq):
    """Print a genomic sequence at 70 characters per line for FASTA format.

    Args:
        seq (str): The DNA sequence to print.

    Returns:
        None

    """
    count = 0
    buf = ''
    for c in seq:
        if count < 70:
            buf = buf + c
            count = count + 1
        else:
            print buf
            count = 0
            buf = ''
    if len(buf) > 0:
        print buf


def main(infile, species):
    """Fetch genomic sequences for given coordinate and produce FASTA file.

    Args:
        infile (str): The csv file containing the list of coordinates.
        species (str): The name of the species the coordinates apply to.

    Returns:
        None

    """
    # Read csv file
    coord_list = []
    metadata = []
    with open(infile, 'r') as f:
        for line in f:
            row = line.strip().split(',')
            query = row[1] + ':' + row[2] + '..' + row[3]
            try:
                if row[4] == '+':
                    query = query + ':1'
                elif row[4] == '-':
                    query = query + ':-1'
            except IndexError:
                pass
            coord_list.append(query)
            metadata.append({
                'name': row[0],
                'chr': row[1],
                'start': row[2],
                'end': row[3],
            })

    # Send query to ensembl REST API
    payload = {'regions': coord_list}
    r = requests.post(api + species, headers=headers, data=json.dumps(payload))
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    response = r.json()

    # Match response to original fasta names
    for entry in response:
        data = str(entry['id']).split(':')[-4:]
        c = data[0]
        s = data[1]
        e = data[2]
        found = False
        for meta in metadata:
            if c == meta['chr'] and s == meta['start'] and e == meta['end']:
                found = True
                print '>' + meta['name']
                print_seq(str(entry['seq']))
        if not found:
            raise Exception("Unable to match sequence to original query.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                        metavar="coordinate_list",
                        help="csv file of genomic coordinatess")
    parser.add_argument('species',
                        help="species name (ensembl)")
    args = parser.parse_args()
    main(args.infile, args.species)
