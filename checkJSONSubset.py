#!/usr/bin/env python

# checkJSONSubset.py
# 
# This is a simple script which verifies that the lumisections in a JSON file are a subset of those in another
# JSON file. Specify the smaller file first and the larger file second.

import os, sys, argparse, json

parser = argparse.ArgumentParser()
parser.add_argument("smallerFile", help="First (subset) JSON file")
parser.add_argument("largerFile", help="Second (superset) JSON file")
args = parser.parse_args()

# Read in the second (should be superset) file and convert it to a dictionary of sets.
with open(args.largerFile) as json_input_1:
    parsed_JSON_1 = json.load(json_input_1)
json_ls = {}
for run in parsed_JSON_1:
    json_ls[run] = set()
    for run_range in parsed_JSON_1[run]:
        for ls in range(run_range[0], run_range[1]+1):
            json_ls[run].add(ls)

# Now read in the first file and see if there's anything in it not in the second.
with open(args.smallerFile) as json_input_2:
    parsed_JSON_2 = json.load(json_input_2)
for run in parsed_JSON_2:
    for runRange in parsed_JSON_2[run]:
        for ls in range(runRange[0], runRange[1]+1):
            if run not in json_ls or ls not in json_ls[run]:
                print "run",run,"ls",ls,"not in",args.largerFile
