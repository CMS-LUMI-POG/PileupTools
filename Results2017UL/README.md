This contains some of the results for the generation of the 2017 ultra-legacy pileup scenario. The process is as follows:

* Start with the golden certification JSON, `Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt`.

* Use `splitJSON.py` to split into smaller pieces for processing.

* Use `processMultiFiles.py` to actually run brilcalc on each of the individual pieces, using the physics JSON file `/cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json`.

* Use `makePileupHisto.py` to actually extract the pileup histogram from the brilcalc results.

The ROOT file `pileup_fixed_shifts.root` contains this final pileup histogram, as well as alternate versions with systematic shifts (pileup0...5 corresponds to -3...+3 sigma). The final plots are also included; for more details, have a look at the talks [here](https://indico.cern.ch/event/815042/contributions/3406023/attachments/1834447/3004998/PileupPPD20190425.pdf) and [here](https://indico.cern.ch/event/815042/contributions/3406023/attachments/1834447/3008406/PileupFollowup.pdf).

WARNING: When I first ran this I was using a TH1F as the histogram type and this caused problems due to floating-point precision issues when running over the whole dataset (frustratingly difficult to track down, since everything worked fine when you run on only one pieces -- it's only when you accumulate several tens of millions of events that the errors accumulate enough to be significant). Switching to a TH1D seemed to eliminate the problem, but I'm writing this down here just in case it potentially causes issues again in the future.