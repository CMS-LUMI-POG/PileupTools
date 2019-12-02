#!/usr/bin/env python

# This script takes the split JSON files produced by divideJSON.py and runs brilcalc over them. As currently
# written it does things one by one but it could also be parallelized if necessary.

import sys, os, argparse
default_json_template = "split_file_%d.json"
default_outfile_template = "brilcalc_lumi_%d.csv"
default_normtag = "/cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json"

parser = argparse.ArgumentParser(description="Invoke brilcalc on a series of input JSON files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--input-file-template", help="Input JSON file name template", default=default_json_template)
parser.add_argument("-o", "--output-file-template", help="Output file name template", default=default_outfile_template)
parser.add_argument("-n", "--normtag", help="Normtag file to use", default=default_normtag)
args = parser.parse_args()

json_template = args.input_file_template
outfile_template = args.output_file_template
normtag = args.normtag

if json_template.find("%d") < 0:
    print "Error: input file name template should include %d (example: "+default_json_template+")"
    sys.exit(1)

if outfile_template.find("%d") < 0:
    print "Error: output file name template should include %d (example: "+default_outfile_template+")"
    sys.exit(1)

i = 1
while (1):
    json_name = json_template % (i)
    if not os.path.exists(json_name):
        break

    print "Processing json file",i,"please wait..."
    outfile_name = outfile_template % (i)
    if not os.path.exists(outfile_name):
        os.system('brilcalc lumi --xing -b "STABLE BEAMS" -u hz/ub -i '+json_name+' --normtag '+normtag+' --xingTr 0.1 -o '+outfile_name)
    i += 1
