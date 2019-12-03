This contains the results for the generation of the 2016 ultra-legacy pileup scenario. The process is similar to the 2017 and 2018 UL generation, but with a few changes.

The most important change necessary is that the current `normtag_PHYSICS.json` uses DT as the primary backup luminometer to PCC. However, DT does not have bunch-by-bunch information, so we have to use a different luminometer. I made a copy of `normtag_PHYSICS.json` as `normtag_PHYSICS_noDT.json` and made the following changes:
* For nearly all runs, replaced `dt16v1pre6` with `hfoc16v4pre1` (the HFOC version in the normtag).
* For a few runs, `hfoc16v4pre1` was not available either, so in this case I used the PLT version in `normtag_BRIL.json` which was `pltzero16v3`. This normtag is quite old but it's only for a few lumisections so shouldn't have a major effect on the result.
* The runs affected were the six runs 275757, 58, 59, 61, 67, and 72, as well as part of 276587 (specifically lumisections 442-451).

I've included the modified normtag here for reference. When the paper version of the normtag comes out, it shouldn't have DT any more so we won't have to worry about this.

Next, the procedure goes similarly to how it was for 2017-18:

* Start with the golden certification JSON, `Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt`.

Because we have been requested to make scenarios separately for eras B-F and G-H, split this file into two pieces (era F ends at 278808, and era G begins at 278820) and follow the next steps separately for each part.

* Use `splitJSON.py` to split the JSON file into smaller pieces for processing.

* Use `processMultiFiles.py` to actually run brilcalc on each of the individual pieces. Use the `-n` flag to specify the modified normtag file you created above.

* Use `makePileupHisto.py` to actually extract the pileup histogram from the brilcalc results. (Make sure to use the `-s` flag to include the systematic shifts.)

The ROOT files `pileup_2016BF.root` and `pileup_2016GH.root` contain the final pileup histogram for each period, as well as alternate versions with systematic shifts (pileup0...5 corresponds to -3...+3 sigma).

For this year I didn't make the comparison plots, since it didn't seem that we needed them, but you can produce them as usual using `plotStandardDifference.py` for the comparison with the regular pileupCalc output, `plotShifts.py` to plot the systematic shifts, and `makeBXPlot.py` to make the sample BX disribution.

There is a simple script `plotEras.py` which plots both eras on the same plot for comparison. `pileup_2016_eras.png` is the result.

Finally, the ROOT file `bunch_distributions_2016.root` contains the relative bunch-by-bunch luminosities on a fill-by-fill basis, as produced by `makeBunchDistributions.py` (which you can consult for futher documentation). See the main README for more information on how to use this file.
