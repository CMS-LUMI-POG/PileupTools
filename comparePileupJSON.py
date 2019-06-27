#!/usr/bin/env python

import os, argparse, json

# This script compares two pileup JSON files to look for any lumisections present in one and not the other, as
# well as differences between the two within a given (relative) tolerance.

parser = argparse.ArgumentParser(description="Compare two pileup JSON files to look for inconsistencies or missing lumisections.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('file1', help='First file to compare')
parser.add_argument('file2', help='Second file to compare')
parser.add_argument('-t', '--tolerance', default=1e-4, help='Relative tolerance to use in comparing values')
args = parser.parse_args()

def read_pileup_json(file_name):
    formatted_json = {}
    with open(file_name) as json_input:
        parsed_json = json.load(json_input)

    # Reformat this a bit into a dictionary with key of the form run:ls and each entry
    # the three-element array [recorded lumi, RMS bunch lumi, avg bunch lumi]
    # to make it easier to check for missing lumisections
    for r in parsed_json:
        for e in parsed_json[r]:
            formatted_json[r+":"+str(e[0])] = e[1:4]

    return formatted_json

pileup1 = read_pileup_json(args.file1)
pileup2 = read_pileup_json(args.file2)

all_runsls = set(pileup1.keys()) | set(pileup2.keys())

desc = ["recorded lumi", "bunch lumi RMS", "average bunch lumi"]

for r in sorted(all_runsls):
    if r not in pileup1:
        print r,"not found in",args.file1
    elif r not in pileup2:
        print r,"not found in",args.file2
    else:
        # Actually exists in both, now compare them

        for i in range(3):
            if pileup1[r][i] != 0:
                d = (pileup1[r][i] - pileup2[r][i])/pileup1[r][i]
            else:
                d = 0
                if pileup2[r][i] != 0:
                    print "In",r,desc[i],"is 0 in file 1 but",pileup2[r][i],"in file 2"
            if abs(d) > args.tolerance:
                print "Difference found in",r+"!",desc[i],"differs by",d
