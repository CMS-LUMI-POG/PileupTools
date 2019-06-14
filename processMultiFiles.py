#!/usr/bin/env python

# This script takes the split JSON files produced by divideJSON.py and runs brilcalc over them. As currently
# written it does things one by one but it could also be parallelized if necessary.

import os
json_template = "split_file_%d.json"
outfile_template = "brilcalc_lumi_%d.csv"

i = 1
while (1):
    json_name = json_template % (i)
    if not os.path.exists(json_name):
        break

    print "Processing json file",i,"please wait..."
    outfile_name = outfile_template % (i)
    if not os.path.exists(outfile_name):
        os.system('brilcalc lumi --xing -b "STABLE BEAMS" -u hz/ub -i '+json_name+' --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json --xingTr 0.1 -o '+outfile_name)
    i += 1
