#!/usr/bin/env python

import ROOT

# shift 'pileupCalc' histogram by 0.5 to properly match 'makePileupHisto' histogram

inputname = 'pileup_2017_5tev_from_pileupCalc.root'
outputname = 'pileup_2017_5tev_from_pileupCalc_shifted.root'

inputfile = ROOT.TFile.Open(inputname)
oldhist = inputfile.Get('pileup')
nbins = oldhist.GetNbinsX()
xmin = oldhist.GetBinLowEdge(1)
xmax = oldhist.GetBinLowEdge(nbins+1)
newhist = ROOT.TH1D('pileup_shifted', oldhist.GetTitle(), nbins, xmin-0.5, xmax-0.5)
for i in range(nbins+2):
    newhist.SetBinContent(i, oldhist.GetBinContent(i))
outputfile = ROOT.TFile.Open(outputname, 'RECREATE')
newhist.Write('pileup')
outputfile.Close()
inputfile.Close()
