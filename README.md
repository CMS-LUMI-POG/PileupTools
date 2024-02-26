# PileupTools

This repository contains tools for doing various pileup studies. In general the individual scripts should have some documentation built in so you can run with the `-h` flag to see the expected arguments, options, etc.; there should also be comments at the top of the script which describe it. See also the TWiki pages <https://twiki.cern.ch/twiki/bin/view/CMS/PileupScenariosRun2> for more details on the individual pileup scenarios available and <https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJSONFileforData> for information on using `pileupCalc`.

At the moment it contains:

### Tools for 2017-18 UL scenarios

* `splitJSON.py`: Takes a certification JSON and divides it into smaller chunks, so they can be run in parallel.

* `processMultiFiles.py`: Takes the scripts produced by `splitJSON.py` and invokes brilcalc to produce the per-bunch luminosity for each. NOTE: This uses a default bunch threshold of 0.1 (i.e., any bunches with a luminosity less than 0.1 of the maximum individual bunch luminosity will be discarded), which may need to be changed for unusual running conditions.

* `makePileupHisto.py`: Takes the brilcalc output files produced by `processMultiFiles.py` and generates the final histogram containing the bunch-by-bunch pileup distribution.

* `makeBXPlot.py`: A script to illustrate the difference between the true bunch-by-bunch distribution of luminosity and the Gaussian approximation used in `pileupCalc.py`.

* `plotStandardDifference.py`: Plots the difference between the pileup scenario generated by `makePileupHisto.py`, using the true bunch-by-bunch distribution, with the pileup distribution generated by `pileupCalc.py`.

* `plotShifts.py`: Plots the difference between the pileup scenario generated with the nominal inelastic cross section with the systematically shifted scenarios.

* `makeBunchDistributions.py`: This script takes the brilcalc output files and generates a set of histograms, one for each fill, with the relative bunch-by-bunch distributions for each fill. See below for more details.

The directories `Results2017UL/` and `Results2018UL/` contain the results for the generation of the 2017 and 2018 UL scenarios and some more specific documentation on the details of the process.

### Tools for other pileup scenarios

* `makeFlatRun3Scenario.py`: This makes the initial Run 3 scenario using a flat distribution of pileup from 55 to 75.

* `smearPileupSummer2018.py`: This script was used for making the mid-2018 pileup scenario. It works by using the extrapolation from the data through June 2018 from Andrea and applying a smearing to get a final distribution. The resulting plot is `PileupSummer2018.png`.

* `make2018PileupScenario.py`: This script was used for making the preliminary 2018 pileup scenario. This takes the 2017 data and "un-levels" it in order to get an estimation of the 2018 pileup. The resulting plots are found in `pileup2018.png` (raw), `pileup2018cleaned.png` (removing the spike caused by leveling), `pileup2018smeared.png` (includes smearing of the resulting pileup), and `pileupFill6358.png` (same procedure but using the data only from fill 6358). The fits to "un-level" individual fills are stored in the `LevelingFits2017/` directory.

### Other tools

* `averagePileup.py`: A very simple script that will take a CSV output file from brilcalc and compute the luminosity-weighted average pileup in that file.

* `checkJSONSubset.py`: A script which will verify that a given JSON is a subset of another. Used to check for inconsistencies between the DCSOnly JSON and the golden JSON files (which should be, but are not always, a strict subset of the DCSOnly file).

* `comparePileupJSON.py`: A script to look for discrepancies between two pileup JSON files within a given tolerance.

* `make_cfi_file.py`: Takes a histogram of the pileup distribution, as produced by `makePileupHisto.py` or `pileupCalc.py`, and generates the corresponding cfi file that can be used in CMSSW for MC generation.

* `select_low_pileup.py`: This script takes an input JSON, selects only lumisections with a pileup below a specified threshold (5.0 by default), and writes out the resulting list of lumisections.

* `smearPileupPoisson.py`: This script shows the difference between the "true" and "observed" pileup distributions by applying a Poisson smearing to the former. The resulting plot is shown in `pileup_smearing.png`.

### Relative bunch distributions

The relative bunch distribution files in `Results2017UL` and `Results2018UL` are intended for use in the new version of pileupCalc currently being developed. These files contains one histogram per fill, named `bx_FILL`, where `FILL` is the fill number, and a `std::map<std::string, std::string>`, `run_map`, for translating run numbers (as present in the pileup JSON file) to fill numbers. In pyROOT, it can be used simply as follows:

```python
>>> f = r.TFile("bunch_distributions_2018.root")
>>> run_map = f.Get("run_map")
>>> run_map["322068"]
'7117'
```
