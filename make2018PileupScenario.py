#!/usr/bin/python

# This script is used to generate the 2018 pileup scenario. It does so as follows:
# 1) Take all of the fills in Run2017F (selected as a period of stable, high-
# luminosity running that should work as a useful reference period)
# 2) In this time period, LHC was leveling the CMS luminosity at 1.5 x 10^34. So
# we want to "undo" this leveling which we do by finding the peak luminosity
# before the beginning of leveling and performing an exponential interpolation
# to the end of leveling.
# 3) However the luminosity is still expected to be leveled in 2018, just at
# a higher level (expected to be ~2 x 10^34). So if the unleveled luminosity is
# greater than that, cap it at 2 x 10^34 (with some "fuzz" added to account for
# the fact that leveled luminosity isn't perfectly constant).
# 4) Then recalculate the pileup using the new luminosity. The pileup is then
# adjusted to account for the assumption that in 2018 we will have ~the same
# total luminosity but with more bunches, so the pileup will decrease by a
# corresponding factor.
# The script will produce a graph of the resulting pileup along with a dump of
# the array of the contents. It can also produce a graph of the interpolation
# for each fill if requested below, so you can check that the interpolation looks
# reasonable.

# There is usually a crossing angle change when leveling ends, which means
# that the fill spends more time near 1.5 x 10^34 than it would otherwise,
# resulting in a bump in the pileup profile. To fix this, we simply discard
# any lumisections after the end of leveling when the luminosity is higher
# than it was at the end of leveling.

# A few assumptions made and effects neglected:
# - Bunch-to-bunch variation is neglected; we assume all bunches have the same
# luminosity
# - In case the fill is dropped while leveling was still ongoing, the fit from
# the preceding fill is used
# - This doesn't account for the fact that lumi would decay faster if it were
# not leveled
# - There might be some difference in the lumi evolution between BCMS bunches and
# 8b4e bunches which is not accounted for
# - The antileveling (via crossing angle changes) in 2018 may be different than
# in 2017, but we'll just use the 2017 reference

import ROOT as r
import csv
import os
import sys
import math
from array import array

# Data tag to use. NOTE: we can NOT use the standard BRIL normtag because that
# only includes STABLE BEAMS and in order to get the peak lumi before leveling
# we need to look in ADJUST as well. So instead I use the current HFET datatag.
# This might mean that some lumi sections are missing, but as long as they're
# a random sample, that shouldn't cause any major problems.
datatag = "hfet17v8"
# Fill list. All 2017F fills are here.
fillList = [6297, 6298, 6300, 6303, 6304, 6305, 6306, 6307, 6308, 6309, 6311,
            6312, 6313, 6314, 6315, 6317, 6318, 6323, 6324, 6325, 6336, 6337,
            6341, 6343, 6344, 6346, 6347, 6348, 6349, 6351, 6355, 6356, 6358,
            6360, 6362, 6364, 6370, 6371]
# Default number of colliding bunches.
defaultCollidingBunches = 1866
# Fills for which the number of colliding bunches wasn't the default. Note:
# if the number of colliding bunches isn't the default, then the pileup is not
# scaled by the ratio of the number of bunches, since the assumption is that a
# 140b fill will still be 140b in 2018.
otherCollidingBunches = {6336: 140}
# Fills which weren't leveled and so we don't have to do anything.
unleveledFills = [6358]

# cross section and orbit frequency for pileup calculation
xsec = 80000
orbitFreq = 11246

# Factor to scale for 2018 projections. This assumes that we have the same total
# luminosity but spread over more bunches.
pileupScaleFactor = 1866.0/2544.0

# Leveling target for 2018. The "fuzz factor" is the +/- margin around that.
levelTarget = 20000
levelFuzzFactor = 2000

# Leveling target for 2017.
oldLevelTarget = 15000

# Final results histogram
h = r.TH1F("h", "Pileup", 100, 0, 100)

rand = r.TRandom3(71556)

# Function for smearing
gf = r.TF1("g", "gaus", -10, 10)
gf.SetParameter(0,1/math.sqrt(2*math.pi))
gf.SetParameter(1,0)
gf.SetParameter(2,2)

for fill in fillList:
    lumiFileName = "lumi_%d.csv" % (fill)
    if not os.path.exists(lumiFileName):
        # Invoke brilcalc to get the lumi for this fill if we don't have it already.
        print "One second, getting lumi for fill "+str(fill)
        os.system('brilcalc lumi -f '+str(fill)+' --normtag '+datatag+' -u hz/ub --byls -o '+lumiFileName)

    # Get the number of colliding bunches.
    if fill in otherCollidingBunches:
        nCollidingBunches = otherCollidingBunches[fill]
    else:
        nCollidingBunches = defaultCollidingBunches
    print "Fill "+str(fill)+" has "+str(nCollidingBunches)+" bunches"

    # Get and parse the lumi data.
    rowNumber = 0
    fillData = []
    with open(lumiFileName) as csv_input:
        reader = csv.reader(csv_input, delimiter=',')
        for row in reader:
            if row[0][0] == '#':
                continue
            runfill=row[0].split(':')
            run=int(runfill[0])
            fill=int(runfill[1])
            lsnums=row[1].split(':')
            ls=int(lsnums[0])
            thisdet=row[8]
            data = {"run": int(runfill[0]), "fill": int(runfill[1]), "ls": int(lsnums[0]),
                    "time": row[2], "status": row[3], "lumi": float(row[5]), "det": row[8]}
            fillData.append(data)

    # OK now do the actual analysis. Step 1: find the maximum lumi (probably occurs during ADJUST).
    # Also find the lumi section where Stable Beams starts.
    maxLumi = -1
    maxLumiLS = -1 # counting LSes from the beginning of the fill, not actually a "real" LS number
    stableBeamsLS = -1
    for i in range(len(fillData)):
        if (stableBeamsLS == -1 and fillData[i]["status"] == "STABLE BEAMS"):
            stableBeamsLS = i
        if fillData[i]["lumi"] > maxLumi:
            maxLumi = fillData[i]["lumi"]
            maxLumiLS = i
    
    print "Max lumi is %f in LS %d; stable beams starts at %d" % (maxLumi, maxLumiLS, stableBeamsLS)

    # Maybe this fill wasn't leveled at all. In that case, our job is easy!
    if maxLumi < oldLevelTarget or fill in unleveledFills:
        print "Looks like this fill wasn't leveled."
        thisFillLeveled = False
    else:
        thisFillLeveled = True

        # That was easy. Now for the harder part -- finding the end of leveling.
        # The end of leveling is usually followed by an emittance scan, so let's look for that. This
        # requires a few steps. First we look for the beginning of the emittance scan, defined as the first
        # part where the lumi goes below 1.2e33 (start a little after stable beams in case there's some
        # instability at the start):
        beginEmitScanLS = -1
        for i in range(stableBeamsLS+5, len(fillData)):
            if fillData[i]["lumi"] < 12000 and fillData[i]["lumi"] > 1000:
                beginEmitScanLS = i
                break

        if (beginEmitScanLS == -1):
            print "Uh-oh, didn't find end of leveling in this fill!"
            print "I will proceed assuming that we dropped the fill during leveling."
            # In this case: use the same peak value
            # but use the lifetime from the last fill
            # so we just don't change expoMultiplier
            expoConstant = maxLumi
        else:
            endLevelingLS = -1
            curLumi = fillData[beginEmitScanLS]["lumi"]
            # Next work backwards to the peak luminosity.
            for i in range(beginEmitScanLS-1, 1, -1):
                if fillData[i]["lumi"] > curLumi:
                    curLumi = fillData[i]["lumi"]
                    endLevelingLS = i
                else:
                    break

            if (endLevelingLS == -1):
                print "Leveling end finder failed!"
                sys.exit(1)

            # OK, let's hope that worked.
            print "Found end of leveling at LS %d (run %d LS %d)" % (endLevelingLS, fillData[endLevelingLS]["run"], fillData[endLevelingLS]["ls"])

            # Now we're making progress! Let's go ahead and do the fit. Since we're just doing two points we can do it ourselves, even.
            expoConstant = maxLumi
            expoMultiplier = -math.log(maxLumi/curLumi)/(endLevelingLS-maxLumiLS)

    # Make some plots. This is kinda slow so once you have them you should disable
    # this section.
    if False:
        # OK. Now regardless of whether we're leveled or not, draw the graph.
        c1 = r.TCanvas("c1", "c1", 800, 600)
        x = array('d')
        y = array('d')
        for i in range(len(fillData)):
            x.append(float(i))
            y.append(float(fillData[i]["lumi"]))
        g = r.TGraph(len(fillData), x, y)
        g.Draw("ALP")
        g.GetXaxis().SetTitle("LS since start of fill")
        g.GetYaxis().SetTitle("Instantaneous lumi (Hz/ub)")
        g.GetYaxis().SetTitleOffset(1.5)
        g.SetTitle("Fill "+str(fill))

        # And draw the fit if we are leveled.
        if thisFillLeveled:
            f = r.TF1("f", "[0]*exp((x-[1])*[2])", maxLumiLS, endLevelingLS)
            f.SetParameter(0, expoConstant)
            f.SetParameter(1, maxLumiLS)
            f.SetParameter(2, expoMultiplier)
            f.SetLineColor(r.kRed)
            f.Draw("same")

        c1.Print(str(fill)+".png")

    # Calculate the "corrected" luminosity and pileup, and then
    # put it in the histogram.
    for i in range(len(fillData)):
        # Skip things that aren't STABLE BEAMS, or things with very low lumi
        # (since those are probably times when the fill was dumped and we didn't
        # notice until later)
        if fillData[i]["status"] != "STABLE BEAMS" or fillData[i]["lumi"] < 100:
            continue
        if thisFillLeveled and (i < endLevelingLS):
            l = expoConstant*math.exp((i-maxLumiLS)*expoMultiplier)
        else:
            l = fillData[i]["lumi"]

        # Check to see if this is a LS after the end of leveling but with lumi
        # higher than the end of leveling, in which case skip it.
        if thisFillLeveled and (i > endLevelingLS) and (l > curLumi):
            continue

        # If the unleveled lumi is too big, relevel it. Add some fuzz to it too.
        if l > levelTarget:
            l = levelTarget
            l += rand.Rndm()*2*levelFuzzFactor - levelFuzzFactor

        # Calculate pileup. Assume constant lumi across bunches
        avgLumi = l/nCollidingBunches
        pileup = avgLumi*xsec/orbitFreq

        # Scale by scale factor (if this fill has the default number of bunches)
        if (nCollidingBunches == defaultCollidingBunches):
            pileup *= pileupScaleFactor
        
        #print "run %d ls %d corr lumi %.2f pileup %.2f" % (fillData[i]["run"], fillData[i]["ls"], l, pileup)
        # Apply smearing
        # h.Fill(pileup)
        for x in range(-10, 11):
            h.Fill(pileup+x, gf.Eval(x))

    # Done with this fill

c1 = r.TCanvas("c1", "c1", 800, 600)
h.Scale(1.0/h.Integral())
h.Draw()
h.SetTitle("Projected 2018 luminosity profile")
h.GetXaxis().SetTitle("Pileup")
h.GetYaxis().SetTitle("Event fraction")
h.GetYaxis().SetTitleOffset(1.4)
c1.Print("pileup2018smeared.png")

binContents=[]
for i in range(1,101):
    binContents.append(h.GetBinContent(i))
print binContents

while(1):
    pass
