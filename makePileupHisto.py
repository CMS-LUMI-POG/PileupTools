#!/usr/bin/python

# This script takes the brilcalc output files produced by, for example, processMultiFiles.py and then extracts
# the bunch-by-bunch pileup from it in order to fill a histogram. By default (see below), it can also produce
# histograms in which the inelastic cross section has been systematically shifted (warning: this is much
# slower).

import os, sys, csv, argparse, glob, re
import ROOT as r

parser = argparse.ArgumentParser(description="Build a pileup histogram distribution from the given brilcalc output files.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("inputFiles", nargs="*", help="Input brilcalc CSV files", default=["brilcalc_lumi_*.csv"])
parser.add_argument("-o", "--output-file", help="Output file name", default="pileup.root")
parser.add_argument("-x", "--cross-section", help="Inelastic pileup cross section in ub", type=int, default=69200)
parser.add_argument("-s", "--systematic-shifts", help="Calculate histograms for systematically shifted cross sections in addition to nominal", action="store_true")
parser.add_argument("-u", "--systematic-uncertainty", help="Relative systematic uncertainty in inelastic pileup cross section", type=float, default=0.046)
parser.add_argument("-n", "--numbins", help="Number of bins in final histogram", type=int, default=100)
parser.add_argument("-v", "--verbose", help="Write out histograms for each individual file", action="store_true")
args = parser.parse_args()

outfile_name = args.output_file
outfile_name_parts = os.path.splitext(outfile_name)
do_syst = args.systematic_shifts
write_part_files = args.verbose
ls_length = 24.95e-9*3564*2**18

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

h = r.TH1D("pileup", "Pileup", args.numbins, -0.5, args.numbins-0.5)

# inelastic cross section (in ub) divided by revolution frequency (in Hz)
calibration_factor = args.cross_section/11245.8
if do_syst:
    syst_percentage = args.systematic_uncertainty
    syst_factor = [1-3*syst_percentage, 1-2*syst_percentage,
                   1-syst_percentage, 1+syst_percentage,
                   1+2*syst_percentage, 1+3*syst_percentage]
    n_syst = len(syst_factor)
    hshift = []
    for i in range(n_syst):
        hshift.append(r.TH1D("pileup"+str(i), "Pileup", args.numbins, -0.5, args.numbins-0.5))

for i, infile_name in enumerate(infiles):
    print "Processing file",infile_name
    rows_processed = 0
    tot_recorded = 0

    # Accumulate the results for each file separately to minimize issues with floating-point precision. Note:
    # this actually seems to be redundant now that we've switched to using TH1D for the main histogram, but
    # I'll keep this in just in case (we don't bother with this for the smeared histograms though).
    h1 = r.TH1D("h1", "accumulator", args.numbins, -0.5, args.numbins-0.5)

    with open(infile_name) as infile:
        reader = csv.reader(infile, delimiter=',')
        for row in reader:
            if row[0][0] == '#':
                continue

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

            # Find the filled BXes and the luminosity in them.
            for j in range(0, len(bx_fields), 3):
                this_pileup = float(bx_fields[j+1])*calibration_factor
                this_recorded = float(bx_fields[j+2])
                tot_recorded += this_recorded
                # fill using recorded lumi as weight. note: this is lacking the factor of the LS length
                # but it's faster to apply that at the end.
                if (this_pileup>args.numbins):
                    print "warning, pileup is outside of range, losing lumi"
                h1.Fill(this_pileup, this_recorded)
                if do_syst:
                    for j in range(n_syst):
                        hshift[j].Fill(this_pileup*syst_factor[j], this_recorded)

            rows_processed += 1
            if (rows_processed % 1000 == 0):
                print "Processed",rows_processed,"rows"

    # Scale by lumi section length to get recorded luminosity.
    h1.Scale(ls_length)
    h.Add(h1)

    if write_part_files:
        f1 = r.TFile(outfile_name_parts[0]+"_part"+str(i+1)+outfile_name_parts[1], "RECREATE")
        h1.Write()
        f1.Close()
    del h1

    print "Found %.3f /fb recorded lumi (integral is %.3f /fb)" % (tot_recorded*ls_length/1e9, h.Integral()/1e9)
    i += 1

f = r.TFile(outfile_name, "RECREATE")
h.Write()
if do_syst:
    for i in range(n_syst):
        hshift[i].Scale(ls_length)
        hshift[i].Write()
f.Close()
