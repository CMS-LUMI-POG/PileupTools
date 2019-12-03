#!/usr/bin/env python

# This plot takes the output for the two different 2016 eras and plots the results.

import os
import ROOT as r

# convert to /pb
scale_factor = 1e-6

infile1 = "pileup_2016BF.root"
infile2 = "pileup_2016GH.root"
outfile = "pileup_2016_eras.png"

f1 = r.TFile(infile1)
h1 = f1.Get("pileup")
h1.Scale(scale_factor)

f2 = r.TFile(infile2)
h2 = f2.Get("pileup")
h2.Scale(scale_factor)

r.gStyle.SetOptStat(0)
c1 = r.TCanvas("c1", "c1", 800, 600)
h1.SetLineColor(r.kBlue)
h1.Draw("hist")
h2.SetLineColor(r.kRed)
h2.Draw("hist same")

h1.GetXaxis().SetTitle("Pileup")
h1.GetYaxis().SetTitle("Recorded lumi (pb^{-1})")
h1.GetYaxis().SetTitleOffset(1.4)

l = r.TLegend(0.6, 0.5, 0.9, 0.6)
l.AddEntry(h1, "2016 eras B-F")
l.AddEntry(h2, "2016 eras G-H")
l.SetBorderSize(0)
l.Draw()

c1.Print(outfile)

print "Press ENTER to exit..."
raw_input()
