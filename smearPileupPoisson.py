#!/usr/bin/env python

# This is a simple script which shows what the "observed" distribution
# looks like by taking the "true" distribution and applying Poisson
# smearing to it.

import ROOT as r
import math

f = r.TFile("pileup_official.root")
h1 = f.Get("pileup")
h1.Scale(1e-6)

h2 = r.TH1F("h2", "Smeared pileup", 100, -0.5, 99.5)

rand = r.TRandom3(71556)

# Function for smearing
p = r.TF1("p", "TMath::Poisson(x,[0])", 0, 100)
p.SetParameter(0,1)

for i in range(1,101):
    n = h1.GetBinContent(i)

    for j in range(0, 100):
        w = n*r.TMath.Poisson(j, h1.GetXaxis().GetBinCenter(i))
        h2.Fill(j, w)


# r.gStyle.SetOptStat(0)
c1 = r.TCanvas("c1", "c1", 1000, 500)
c1.Divide(2,1)
c1.cd(1)
h1.SetTitle("\"True\" pileup distribution, 2017")
h1.GetXaxis().SetTitle("Pileup")
h1.GetYaxis().SetTitle("Recorded lumi (pb^{-1})")
h1.GetYaxis().SetTitleOffset(1.6)
h1.Draw("hist")
c1.cd(2)
h2.SetTitle("\"Observed\" pileup distribution, 2017")
h2.GetXaxis().SetTitle("Pileup")
h2.GetYaxis().SetTitle("Recorded lumi (pb^{-1})")
h2.GetYaxis().SetTitleOffset(1.6)
h2.Draw("hist")
c1.Print("pileup_smearing.png")

print "Press ENTER to finish..."
raw_input()
