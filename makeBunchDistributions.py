#!/usr/bin/python

# This script takes the brilcalc output files produced by, for example, processMultiFiles.py (or just a single
# file if you made a single monolithic file) and then makes a file containing the per-fill relative bunch
# distribution. Because pileupCalc.py only speaks run numbers, not fill numbers, we also include a single
# std::map<string, string> to translate run numbers into fill numbers.

import os, sys, csv, argparse, glob, re
import ROOT as r

parser = argparse.ArgumentParser(description="Build a pileup histogram distribution from the given brilcalc output files.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("inputFiles", nargs="*", help="Input brilcalc CSV files", default=["brilcalc_lumi_*.csv"])
parser.add_argument("-o", "--output-file", help="Output file name", default="bunch_distributions.root")
parser.add_argument("--min", dest="minVal", help="Minimum of each distribution histogram", type=float, default=0.2)
parser.add_argument("--max", dest="maxVal", help="Maximum of each distribution histogram", type=float, default=2.2)
parser.add_argument("-n", "--numbins", help="Number of bins in each distribution histogram", type=int, default=100)
args = parser.parse_args()

outfile_name = args.output_file
current_fill = -1

infiles = []
for f in args.inputFiles:
    if f.find("*") >= 0 or f.find("?") or f.find("[") >= 0:
        infiles.extend(glob.glob(f))
    else:
        infiles.append(f)

# the problem of how to sort filenames (probably) with numbers in them is surprisingly tricky!
def sort_function(x):
    l = re.split("(\d+)", x)
    return [int(i) if i.isdigit() else i for i in l]

infiles = sorted(infiles, key=sort_function)

all_histos = []
run_map = r.map('string', 'string')()

for i, infile_name in enumerate(infiles):
    print "Processing file",infile_name
    rows_processed = 0
    with open(infile_name) as infile:
        reader = csv.reader(infile, delimiter=',')
        for row in reader:
            if row[0][0] == '#':
                continue

            (run, fill) = row[0].split(":")
            if fill != current_fill:
                # Note: this logic only works if the fills are contiguous in the input files.  That should
                # certainly be the case unless you're doing something completely crazy. If not, well, you'll
                # get some ROOT warnings and hopefully should be able to figure it out.
                h = r.TH1D("bx_"+fill, "BX distribution for fill "+fill, args.numbins, args.minVal, args.maxVal)
                h.GetXaxis().SetTitle("Relative bunch luminosity")
                h.GetYaxis().SetTitle("Frequency")
                all_histos.append(h)
                print "Beginning fill",fill
                current_fill = fill

            if run_map.count(run) == 0:
                run_map[run] = fill

            # Next, split up the individual BX data. Use the slice
            # to drop the initial and final brackets.
            if len(row) < 9:
                print "Bad row:", row
                sys.exit(1)
            # If there's no data at all, just skip this row.
            if (row[9][0:2] == '[]'):
                continue
            else:
                bx_fields = row[9][1:-1].split(' ')

            # Store the value of each BX as relative to average. This requires two passes.
            tot_lumi = 0
            
            # each triplet is: bx number, inst delivered, inst recorded; for this, we only care about the middle
            for j in range(0, len(bx_fields), 3):
                tot_lumi += float(bx_fields[j+1])
            nbx = len(bx_fields)/3
            avg_lumi = tot_lumi/nbx
            for j in range(0, len(bx_fields), 3):
                rel_lumi = float(bx_fields[j+1])/avg_lumi
                if (rel_lumi < args.minVal or rel_lumi > args.maxVal):
                    print "warning: relative lumi of",rel_lumi,"outside of histogram bounds"
                h.Fill(rel_lumi)

            rows_processed += 1
            if (rows_processed % 1000 == 0):
                print "Processed",rows_processed,"rows"

    # end of lines in file
# end of file loops

f = r.TFile(outfile_name, "RECREATE")
f.WriteObjectAny(run_map, "std::map<std::string,std::string>", "run_map")
for h in all_histos:
    h.Write()
f.Close()
