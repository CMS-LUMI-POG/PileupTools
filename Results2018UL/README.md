This contains some of the results for the generation of the 2018 ultra-legacy pileup scenario. The process is basically the same as for the 2017 UL generation:

* Start with the golden certification JSON, `Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt`.

* Use `splitJSON.py` to split into smaller pieces for processing.

* Use `processMultiFiles.py` to actually run brilcalc on each of the individual pieces, using the physics JSON file `/cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json`.

* Use `makePileupHisto.py` to actually extract the pileup histogram from the brilcalc results.

The ROOT file `pileup_2018_shifts.root` contains this final pileup histogram, as well as alternate versions with systematic shifts (pileup0...5 corresponds to -3...+3 sigma).

The final plots are also included, consisting of `bunch_by_bunch_ratio_2018.png` (produced by `plotStandardDifference.py`), `shifts_2018_{1,2}.png` (produced by `plotShifts.py`), and `bxlumi_{6719,7117}.png` (produced by `makeBXPlot.py` using a couple of the brilcalc output files). See the talk [here](https://indico.cern.ch/event/826107/contributions/3465964/attachments/1861686/3059846/PileupPPD20190613.pdf) for more details on these plots.

Finally, the ROOT file `bunch_distributions_2018.root` contains the relative bunch-by-bunch luminosities on a fill-by-fill basis, as produced by `makeBunchDistributions.py` (which you can consult for futher documentation). See the main README for more information on how to use this file.
