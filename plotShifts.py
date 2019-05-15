#!/usr/bin/python

# This plot script takes the output from makePileupHisto.py and compares the distribution with the nominal
# cross section to those where it has been systematically shifted.

import ROOT as r

scale_factor = 23.31*1e-6

f = r.TFile("pileup_fixed_shifts.root")
h0 = f.Get("pileup")
h0.Scale(scale_factor)

labels = ["-3 #sigma", "-2 #sigma", "-1 #sigma", "+1 #sigma", "+2 #sigma", "+3 #sigma"]
all_h = []
all_l = []

r.gStyle.SetOptStat(0)
c1 = r.TCanvas("c1", "c1", 1200, 600)
c1.Divide(3,2)
c2 = r.TCanvas("c2", "c2", 1200, 600)
c2.Divide(3,2)

for i in range(6):
    if (i<3):
        c1.cd(i+1)
    else:
        c2.cd(i-2)

    h = f.Get("pileup"+str(i))
    h.Scale(scale_factor)
    
    h.SetTitle(labels[i])
    h.GetXaxis().SetTitle("Pileup")
    h.GetYaxis().SetTitle("Recorded lumi (pb^{-1})")
    h.GetYaxis().SetTitleOffset(1.6)
    h.SetLineColor(r.kRed)
    h.Draw("hist")
    h0.Draw("hist same")
    if i >= 3:
        h.SetMaximum(h0.GetMaximum()*1.1)

    l = r.TLegend(0.6, 0.5, 0.9, 0.6)
    l.AddEntry(h0, "no shift")
    l.AddEntry(h, "shifted by "+labels[i])
    l.SetBorderSize(0)
    l.Draw()

    if (i<3):
        c1.cd(i+4)
    else:
        c2.cd(i+1)

    hdiv = h.Clone()
    hdiv.Divide(h0)
    hdiv.SetTitle("Ratio (shifted/unshifted)")
    hdiv.GetXaxis().SetTitle("Pileup")
    hdiv.GetYaxis().SetTitle("Ratio")
    hdiv.GetYaxis().SetTitleOffset(1.2)
    if i >= 3:
        hdiv.SetMaximum(10)
    hdiv.Draw()

    all_h.append(hdiv)
    all_l.append(l)

c1.Print("shifts1.png")
c2.Print("shifts2.png")

print "Press ENTER to exit..."
raw_input()
