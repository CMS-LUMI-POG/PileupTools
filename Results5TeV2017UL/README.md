This contains the instructions and some of the results for the generation of the 5TeV 2017 ultra-legacy pileup scenario. The steps to derive the pileup profile are as follows:

* Initialize brilcalc (see [https://twiki.cern.ch/twiki/bin/view/CMS/BrilcalcQuickStart](BrilcalcQuickStart)):<br>
  `export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH`<br>
  `pip install --user --upgrade brilws`

* Use `splitJSON.py` to split the Golden JSON into smaller pieces for processing:<br>
  `./splitJSON.py /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/5TeV/ReReco/Cert_306546-306826_5TeV_EOY2017ReReco_Collisions17_JSON.txt`

* Use `processMultiFiles.py` to run brilcalc on each of the individual pieces, using the physics JSON file:<br>
  `./processMultiFiles.py`

* Use `makePileupHisto.py` to extract the pileup histogram from the brilcalc results:<br>
  `./makePileupHisto.py -x 65000 -n 30 brilcalc_lumi_*.csv -s -o pileup_2017_5tev.root`

* To plot the comparison between the scenarios with systematically shifted cross sections:<br>
  `./plotShifts.py pileup_2017_5tev.root`

For the comparison with the result obtained with `pileupCalc.py`, run the following steps:

* Run `pileupCalc.py` using the centrally provided files (this needs CMSSW):<br>
  `pileupCalc.py -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/5TeV/ReReco/Cert_306546-306826_5TeV_EOY2017ReReco_Collisions17_JSON.txt --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/5TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 65000 --maxPileupBin 30 --numPileupBins 30 pileup_2017_5tev_from_pileupCalc.root`

* Create a shifted version of the histogram:<br>
  `./Results5TeV2017UL/convert.py`

* Create the comparison plots:<br>
  `./plotStandardDifference.py pileup_2017_5tev_from_pileupCalc.root pileup_2017_5tev.root -y 2017`

