#!/usr/bin/env python

import sys
import os
import csv
import json

# This script will select an input JSON file and return the subset of that file for which the pileup is less
# than a specified value. Note that no selection on STABLE BEAMS or anything else is applied, so if you want
# that kind of selection, apply it to the input JSON before feeding it to this script (or just modify the
# brilcalc call below).

# IMPORTANT NOTE: The output will discard any low-pileup periods which are just one LS long, since these are
# assumed to be the bottom of emittance scans rather than any actual useful low-pileup data. If you actually
# want to include these go ahead and change the logic in add_to_list below.

# Specified value of pileup to keep.
pileup_threshold = 5.0

# Input normtag to use. The exact details probably don't matter much as long as it covers the whole input
# period.
normtag_file = "/cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json"

# This stores the run/lumisection numbers to keep. This is stored as a dictionary where the key is the run
# number and the value is the set of lumisections present for that run.
keep_ls = {}

# Get input file name.
if (len(sys.argv) < 2):
    print "Usage: "+sys.argv[0]+" <input file>"
    sys.exit(1)
infile = sys.argv[1]

# Execute brilcalc using the input JSON file.
brilcalc_output="temp_brilcalc.csv"
print "Getting data from brilcalc, please wait a moment..."
os.system('brilcalc lumi -i '+infile+' --normtag '+normtag_file+' --byls -o '+brilcalc_output)

# Parse the brilcalc output.
with open(brilcalc_output) as csv_input:
    reader = csv.reader(csv_input, delimiter=',')

    for row in reader:
        if row[0][0] == '#':
            continue

        runfill = row[0].split(":")
        lsls = row[1].split(":")
        run = int(runfill[0])
        ls = int(lsls[0])
        pileup = float(row[7])

        # If we want to keep it, store it in the dictionary. Storing it as a set also protects us against the
        # LSes in the output being out of order (which they may be in some cases).
        if (pileup < pileup_threshold):
            if not run in keep_ls:
                keep_ls[run] = set([ls])
            else:
                keep_ls[run].add(ls)

# We're done, so write out the output! First, convert the list of kept lumisections into ranges of beginning
# and ending lumisections. This code is mostly borrowed from doFillValidation.py since I know it works (but
# simplified somewhat since we don't have to deal with multiple luminometers).

lastRun = -1
startLS = -1
lastLS = -1
output_json = {}

def add_to_list(run, startLS, lastLS):
    # Low-pileup periods that are only one LS long are probably just the bottoms of emittance scans, which are
    # not actually really useful for low-pileup studies. So if there's just one LS in the period, go ahead and
    # throw it out.
    if (startLS != lastLS):
        if not str(lastRun) in output_json:
            output_json[str(lastRun)] = [[startLS, lastLS]]
        else:
            output_json[str(lastRun)].append([startLS, lastLS])
    
for r in sorted(keep_ls.keys()):
    for ls in sorted(keep_ls[r]):
        # If new run, or discontinuous LS range, save the previous range and move on
        if ((r != lastRun and lastRun != -1) or
            (ls != lastLS + 1 and lastLS != -1)):
            add_to_list(str(lastRun), startLS, lastLS)
            startLS = ls
        lastRun = r
        lastLS = ls
        if startLS == -1:
            startLS = ls
# Don't forget the end! However if we got nothing at all, then do forget the end.
if (lastRun != -1):
    add_to_list(str(lastRun), startLS, lastLS)

# Create output file name by adding _lowPU to the end of the part before the dot.
file_fields = os.path.basename(infile).split(".")
if (len(file_fields) >= 2):
    file_fields[-2] += "_lowPU"
else:
    file_fields[0] += "_lowPU"
outfile_name = ".".join(file_fields)

# Unfortunately json.dump only has two kinds of formatting: either everything on one line,
# or else every single list element on its own line, both of which are rather difficult to
# read. So instead iterate over the dictionary ourselves and use json.dumps to format each
# element. Not the most elegant solution in the world, but it works.
with open(outfile_name, "w") as outfile:
    output_lines = []
    for r in sorted(output_json.keys()):
        output_lines.append("\""+r+"\": "+json.dumps(output_json[r]))
    outfile.write("{\n")
    outfile.write(",\n".join(output_lines))
    outfile.write("\n}\n")

# Don't forget to clean up!
os.unlink(brilcalc_output)
outfile.close()

print "Output JSON written to "+outfile_name+"."
