#!/usr/bin/env python

import csv
import argparse

# Take a csv output file from brilcalc and average the pileup in that file.

# Parse input arguments.
parser = argparse.ArgumentParser()
parser.add_argument('infile', help='Input CSV file to process.')
args = parser.parse_args()

total_weighted_pileup = 0
total_rec = 0

# Parse the brilcalc output.
with open(args.infile) as csv_input:
    reader = csv.reader(csv_input, delimiter=',')

    for row in reader:
        if row[0][0] == '#':
            continue

        lumi_del = float(row[5])
        lumi_rec = float(row[6])
        pileup = float(row[7])

        total_weighted_pileup += pileup*lumi_rec
        total_rec += lumi_rec

# and now the total
print "Luminosity-weighted average pileup in file is %.2f" % (total_weighted_pileup/total_rec)
