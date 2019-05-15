#!/usr/bin/python

# This script takes the brilcalc output files produced by, for example, processMultiFiles.py and then extracts
# the bunch-by-bunch pileup from it in order to fill a histogram. By default (see below), it can also produce
# histograms in which the inelastic cross section has been systematically shifted (warning: this is much
# slower).

# Note: you have to scale this histogram by the length of a lumisection (23.31) in order to get the recorded
# luminosity.

import os, sys, csv
import ROOT as r

infile_template = "brilcalc_lumi_%d.csv"
outfile_name = "pileup_fixed_shifts.root"
# If True, this will also make histograms for systematic shifts to the inelastic cross section. Much slower!
do_syst = True
# If True, this will also write an output histogram for each input file separately, for debugging.
write_part_files = False

h = r.TH1D("pileup", "Pileup", 100, -0.5, 99.5)

# inelastic cross section (in ub) divided by revolution frequency (in Hz)
calibration_factor = 69200.0/11245.8
if do_syst:
    syst_percentage = 0.046
    syst_factor = [1-3*syst_percentage, 1-2*syst_percentage,
                   1-syst_percentage, 1+syst_percentage,
                   1+2*syst_percentage, 1+3*syst_percentage]
    n_syst = len(syst_factor)
    hshift = []
    for i in range(n_syst):
        hshift.append(r.TH1D("pileup"+str(i), "Pileup", 100, -0.5, 99.5))

i = 1
while (1):
    infile_name = infile_template % (i)
    if not os.path.exists(infile_name):
        break

    print "Processing file",infile_name
    rows_processed = 0
    tot_recorded = 0

    # Accumulate the results for each file separately to minimize issues with floating-point precision. Note:
    # this actually seems to be redundant now that we've switched to using TH1D for the main histogram, but
    # I'll keep this in just in case (we don't bother with this for the smeared histograms though).
    h1 = r.TH1D("h1", "accumulator", 100, -0.5, 99.5)

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
                if (this_pileup>100):
                    print "warning, pileup is outside of range, losing lumi"
                h1.Fill(this_pileup, this_recorded)
                if do_syst:
                    for j in range(n_syst):
                        hshift[j].Fill(this_pileup*syst_factor[j], this_recorded)

            rows_processed += 1
            if (rows_processed % 1000 == 0):
                print "Processed",rows_processed,"rows"

    h.Add(h1)

    if write_part_files:
        f1 = r.TFile("pileup_part"+str(i)+".root", "RECREATE")
        h1.Write()
        f1.Close()
    del h1

    print "Found %.3f recorded lumi (integral is %.3f)" % (tot_recorded*23.31/1e9, h.Integral()*23.31/1e9)
    i += 1

f = r.TFile(outfile_name, "RECREATE")
h.Write()
if do_syst:
    for i in range(n_syst):
        hshift[i].Write()
f.Close()
