# PileupTools

This repository contains tools for doing various pileup studies.

At the moment it contains:

* make2018PileupScenario: a script for making the preliminary 2018
pileup scenario. This takes the 2017 data and "un-levels" it in order
to get an estimation of the 2018 pileup.

* select_low_pileup: this script takes an input JSON, selects only
lumisections with a pileup below a specified threshold (5.0 by
default), and writes out the resulting list of lumisections.

* smearPileupSummer2018: this takes the 2018 pileup scenario using the
extrapolation from the current (as of June 2018) data from Andrea and
applies a smearing to get a final distribution.

Please see the scripts themselves for further documentation.
