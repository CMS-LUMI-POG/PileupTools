#!/usr/bin/env python

# This plot script compares the "standard" distribution from pileupCalc to the true bunch-by-bunch
# distribution obtained by using makePileupHisto.py. Note that makePileupHisto.py has the bin centers on whole
# numbers, so you'll need to shift the standard distribution in order to get them to properly match.

import argparse
import ROOT as r

parser = argparse.ArgumentParser(description="Make plots comparing distribution from pileupCalc to true bunch-by-bunch distribution.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("inputFileStandard", help="ROOT file containing histogram from pileupCalc.py")
parser.add_argument("inputFileBunchByBunch", help="ROOT file containing bunch-by-bunch histogram from makePileupHisto.py")
parser.add_argument("-o", "--output-file", help="Output plot file", default="bunch_by_bunch_ratio.png")
parser.add_argument("-y", "--year", help="Year to put on plots", type=int, default=2018)
args = parser.parse_args()

f1 = r.TFile(args.inputFileStandard)
h1 = f1.Get("pileup")
# convert to /pb
h1.Scale(1e-6)

f2 = r.TFile(args.inputFileBunchByBunch)
h2 = f2.Get("pileup")
# as above
h2.Scale(1e-6)

r.gStyle.SetOptStat(0)
c1 = r.TCanvas("c1", "c1", 1000, 500)
c1.Divide(2,1)
c1.cd(1)
h1.SetTitle("Pileup, "+str(args.year)+", golden JSON")
h1.GetXaxis().SetTitle("Pileup")
h1.GetYaxis().SetTitle("Recorded lumi (pb^{-1})")
h1.GetYaxis().SetTitleOffset(1.6)
h1.Draw("hist")
h2.SetLineColor(r.kRed)
h2.Draw("hist same")

label = "%.2f/fb"% (h1.Integral()/1000)
l1 = r.TText(70, 200, label)
l1.Draw()

print "Total lumi in standard histo (1/fb):",h1.Integral()/1000
print "Total lumi in bunch-by-bunch histo (1/fb):",h2.Integral()/1000

l = r.TLegend(0.6, 0.5, 0.9, 0.6)
l.AddEntry(h1, "standard method")
l.AddEntry(h2, "bunch-by-bunch")
l.SetBorderSize(0)
l.Draw()

c1.cd(2)
hdiv = h2.Clone()
hdiv.Divide(h1)
hdiv.SetTitle("Ratio (bbb/standard)")
hdiv.GetXaxis().SetTitle("Pileup")
hdiv.GetYaxis().SetTitle("Ratio")
hdiv.GetYaxis().SetTitleOffset(1.2)
hdiv.Draw()

c1.Print(args.output_file)
print "Press ENTER to exit..."
raw_input()
