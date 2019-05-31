This contains some of the results for the generation of the 2018 ultra-legacy pileup scenario. The process is basically the same as for the 2017 UL generation:

* Start with the golden certification JSON, `Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt`.

* Use `splitJSON.py` to split into smaller pieces for processing.

* Use `processMultiFiles.py` to actually run brilcalc on each of the individual pieces, using the physics JSON file `/cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json`.

* Use `makePileupHisto.py` to actually extract the pileup histogram from the brilcalc results.

The ROOT file `pileup_fixed_shifts.root` contains this final pileup histogram, as well as alternate versions with systematic shifts (pileup0...5 corresponds to -3...+3 sigma). The final plots are also included.
