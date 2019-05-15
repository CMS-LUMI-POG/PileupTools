#!/usr/bin/env python

# A very simple script to divide an input file into individual pieces so you can run brilcalc over each piece
# in parallel rather than having one huge job.

import sys, json

if (len(sys.argv) < 2):
    print "Usage: "+sys.argv[0]+" <input file>"
    sys.exit(1)

infile = sys.argv[1]
runs_per_file = 10
output_template = "split_file_%d_test.json"

# First, read in the input JSON file.
with open(infile) as json_input:
    parsedJSON = json.load(json_input)

# Now segment it.
input_runs = sorted(parsedJSON.keys())
counter = 1
for i in range(0, len(input_runs), runs_per_file):
    these_runs = input_runs[i:i+runs_per_file]
    outfile_name = output_template % (counter)
    outfile = open(outfile_name, "w")
    outfile.write("{"+",\n".join("\""+x+"\": "+json.dumps(parsedJSON[x]) for x in these_runs)+"}\n")
    outfile.close()
    counter += 1

print len(input_runs),"runs processed"
