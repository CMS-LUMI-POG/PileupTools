#!/usr/bin/python

# This script makes some plots illustrating the difference between the "standard" approximation that
# pileupCalc uses of estimating the per-bunch distribution as a Gaussian and the actual per-bunch
# distribution. To use it, first create a brilcalc output file using something like this:
# brilcalc lumi -u hz/ub --byls --xing -i "{300777:[[40,64]]}" --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -o sample.csv
# and then run providing that file as the input.
#
# Arguments for this script:
# input file -- output file from brilcalc as above
# -n NUM -- use only the first NUM lumi sections from the input file (instead of all)
# -o NAME -- use NAME as the name of the output file (default is bxlumi_FILL.png)

import sys, csv, math, argparse
import ROOT as r

parser = argparse.ArgumentParser(description="Plot the distribution of BX lumi given a brilcalc output file.")
parser.add_argument("inputFile", help="Input file from brilcalc")
parser.add_argument("-n", "--num-ls", help="Number of lumi sections to use from file (default: all)", type=int)
parser.add_argument("-o", "--output-file", help="Output file name (default: bxlumi_FILL.png")
args = parser.parse_args()

tot_ls = 0
tot_lum_bx = [0] * 3565   # this goes 1...3564 so we need 3565 elements

with open(args.inputFile) as csv_input:
    reader = csv.reader(csv_input, delimiter=',')

    for row in reader:
        if row[0][0] == '#':
            continue

        if tot_ls == 0:
            fill = (row[0].split(":"))[1]
        else:
            this_fill = (row[0].split(":"))[1]
            if fill != this_fill:
                print "Error: fill number changed from "+fill+" to "+this_fill+", aborting!"
                print "Suggest using -n to limit the number of lumi sections used."
                sys.exit(1)

        lsdata = row[9]
        lsdata = lsdata[1:-1]  # strip starting and ending brackets
        lsfields = lsdata.split(" ")

        for i in range(0, len(lsfields), 3):
            bx = int(lsfields[i])
            lum_deliv = float(lsfields[i+1])

            tot_lum_bx[bx] += lum_deliv

        tot_ls += 1
        if (args.num_ls and tot_ls >= args.num_ls):
            break

print "Read",tot_ls,"lumisections"

r.gStyle.SetOptStat(0)
h1 = r.TH1F("h1", "h1", 70, 3, 10)
h1.GetXaxis().SetTitle("Instantaneous luminosity (Hz/#mub)")
h1.GetYaxis().SetTitle("Number of bunches")
h1.GetYaxis().SetTitleOffset(1.5)
h1.SetTitle("Luminosity per bunch, fill "+fill)

for i in range(0, 3565):
    avg_lum = tot_lum_bx[i]/tot_ls
    if avg_lum > 0.1:
        h1.Fill(avg_lum)

f1 = r.TF1("f1", "gaus", 0, 10)
f1.SetParameters(h1.Integral("width")/(h1.GetStdDev()*math.sqrt(2*math.pi)), h1.GetMean(), h1.GetStdDev())

c1 = r.TCanvas("c1", "c1", 1000, 500)
c1.Divide(2,1)
c1.cd(1)
h1.Draw()
f1.Draw("same")

l = r.TLegend(0.45, 0.75, 0.88, 0.88)
l.AddEntry(h1, "actual bunches")
l.AddEntry(f1, "Gaussian approximation")
l.SetBorderSize(0)
l.Draw()

c1.cd(2)
hc = h1.Clone()
hc.Draw()
f1.Draw("same")
r.gPad.SetLogy()
hc.GetYaxis().SetRangeUser(1e-4,500)
if args.output_file:
    c1.Print(args.output_file)
else:
    c1.Print("bxlumi_"+fill+".png")

raw_input("Press ENTER to exit...")
