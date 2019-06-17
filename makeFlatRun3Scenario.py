#!/usr/bin/env python

# The same as make_cfi_file.py but makes a flat distribution from 55 to 75 (used for the initial Run 3 pileup
# scenario).

import ROOT as r
import math
import sys

final_nums = []
final_weights = []

for i in range(0,76):
    final_nums.append(i)
    if i < 55:
        final_weights.append(0)
    else:
        final_weights.append(1.0/21)

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
