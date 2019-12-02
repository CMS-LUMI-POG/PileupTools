#!/usr/bin/env python

# This file takes the pileup distribution produced by makePileupHisto.py and then produces the appropriate cfi
# file corresponding to it.

import ROOT as r
import math
import sys

if (len(sys.argv) < 2):
    print "Usage: "+sys.argv[0]+" <input file>"
    sys.exit(1)

infile = sys.argv[1]

f = r.TFile(infile)
h = f.Get("pileup")
h.Scale(1e-6)

final_nums = []
final_weights = []

# Read in the histogram data.
for i in range(1,h.GetXaxis().GetNbins()+1):
    x = h.GetXaxis().GetBinCenter(i)
    if abs(x-int(x)) > 0.000001:
        print "warning: bin center",x,"does not appear to be an integer"
    final_nums.append(int(x))
    final_weights.append(h.GetBinContent(i))

# Shift everything by 1 to account for the fact that pileup is actually the number of EXTRA interactions, not the TOTAL number that we measure.
if final_nums[0] != 0:
    print "warning: expected first bin to be 0"

final_nums.pop(0)
final_weights.pop(0)

# don't forget to subtract 1 from the numbers and renormalize the weights array
total_weight = 0
for i in range(len(final_nums)):
    final_nums[i] -= 1
    total_weight += final_weights[i]

for i in range(len(final_weights)):
    final_weights[i] /= total_weight

if len(final_nums) != len(final_weights):
    print "error: bin center and weight arrays aren't of equal length, wtf?"

# print out the final file.
print "import FWCore.ParameterSet.Config as cms"
print "from SimGeneral.MixingModule.mix_probFunction_25ns_PoissonOOTPU_cfi import *"
print "mix.input.nbPileupEvents.probFunctionVariable = cms.vint32("
lines = []
for i in range(0, len(final_nums), 10):
    lines.append("    "+", ".join(str(x) for x in final_nums[i:i+10]))
print ",\n".join(lines)
print "    )"
print

print "mix.input.nbPileupEvents.probValue = cms.vdouble("
lines = []
for i in range(0, len(final_weights), 5):
    lines.append("    "+", ".join(str(x) for x in final_weights[i:i+5]))
print ",\n".join(lines)
print "    )"
print

