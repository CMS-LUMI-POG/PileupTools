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
c1 = r.TCanvas("c1", "c1", 1200, 600)
c1.Divide(2,1)
c1.cd(1)

hs = h1.Clone("sum")
hs.Add(h2)
hs.SetLineColor(r.kBlack)
hs.Draw("hist")

h1.SetLineColor(r.kBlue)
h1.Draw("hist same")
h2.SetLineColor(r.kRed)
h2.Draw("hist same")

hs.GetXaxis().SetTitle("Pileup")
hs.GetYaxis().SetTitle("Recorded lumi (pb^{-1})")
hs.GetYaxis().SetTitleOffset(1.5)

l = r.TLegend(0.6, 0.5, 0.9, 0.6)
l.AddEntry(hs, "all 2016")
l.AddEntry(h1, "2016 eras B-F")
l.AddEntry(h2, "2016 eras G-H")
l.SetBorderSize(0)
l.Draw()

hsn = hs.Clone()
h1n = h1.Clone()
h2n = h2.Clone()
h1n.Scale(1.0/h1n.Integral())
hsn.Scale(1.0/hsn.Integral())
h2n.Scale(1.0/h2n.Integral())
c1.cd(2)
hsn.Draw("hist")
h1n.Draw("hist same")
h2n.Draw("hist same")
hsn.SetTitle("Pileup, normalized to 1")
hsn.GetYaxis().SetTitle("Event fraction")
hsn.SetMaximum(h1n.GetMaximum()*1.1)
l2 = l.Clone()
l2.Draw()

c1.Print(outfile)

c2 = r.TCanvas("c2", "c2", 1200, 600)
c2.Divide(2,1)
c2.cd(1)
hs1r = h1n.Clone()
hs1r.Divide(hsn)
hs1r.Draw()
hs1r.SetTitle("Reweighting overall #rightarrow B-F")
hs1r.GetXaxis().SetTitle("Pileup")
hs1r.GetYaxis().SetTitle("Weight factor")

c2.cd(2)
hs2r = h2n.Clone()
hs2r.Divide(hsn)
hs2r.Draw()
hs2r.SetTitle("Reweighting overall #rightarrow G-H")
hs2r.GetXaxis().SetTitle("Pileup")
hs2r.GetYaxis().SetTitle("Weight factor")

c2.Print("ratios_2016.png")

print "Press ENTER to exit..."
raw_input()
