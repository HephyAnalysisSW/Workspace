import ROOT
from array import array
from math import *
import os, copy
from simpleStatTools import niceNum
from Workspace.RA4Analysis.simplePlotsCommon import *
import xsec, pickle

from msugraCount import msugraCount
from msugraxsec import msugraxsec

ROOT.gROOT.SetBatch(1)
ROOT.gSystem.Load('../../../StatisticalTools/RooStatsRoutines/root/roostats_cl95_C.so')

#This file stores the results for the backup method (2D reweighting) for the muon case ("prediction", "predictionError", "data")
res_file = "/afs/hephy.at/user/s/schoefbeck/www//pngBM//Mu_pf-3j40_res.py"
execfile(res_file)

print "Used in ",res_file
print "targetLumi",targetLumi,"commoncf",commoncf

# This will give you the dicts "efficiency" and "efficiencykinMetSig" which hold all the msugra efficiencies:
eff_file = "/afs/hephy.at/user/s/schoefbeck/www//pngBM/Mu_pf-3j40_msugraEfficiencies.py" 
execfile(eff_file)
print "Used in ",eff_file
print "targetLumi",targetLumi,"commoncf",commoncf

#find optimal HT/kMs cuts by simple measure: Total number of msugra points with s/sqrt(b)>threshold 
bjetbin = "binc"
hbins = prediction[bjetbin].keys()
mbins = prediction[bjetbin][hbins[0]].keys()
hbins.sort()
mbins.sort()
threshold = 1
cutResults=[]
#for hbin in hbins[1:-1]:  #Loop over cut pairs
#  for mbin in mbins[1:-1]:
for hbin in [1000]:
  for mbin in [9]:
    msugra_points = efficiencykinMetSig[bjetbin][hbin][mbin].keys()
    count = 0 
    bg = prediction[bjetbin][hbin][mbin]
    bgerr = predictionError[bjetbin][hbin][mbin]
    for ms_point in msugra_points:
      if int(ms_point.split("_")[1])>300 or int(ms_point.split("_")[2])>300:  #consider msugra points with m0>300 or m12>300 only
        sig = efficiencykinMetSig[bjetbin][hbin][mbin][ms_point]*msugraxsec[ms_point]*targetLumi
#        if sig/bgerr>count:
        if sig/ROOT.sqrt(bg)>count:
          count+=1
          print "Counting",ms_point,"for cuts: ht>",hbin,"and mbin>",mbin,"sig",sig,"bg",bg
    cutResults.append([count,hbin,mbin,bg,bgerr])
#    print "Counts",count, "for cuts: ht>",hbin,"and mbin>",mbin
cutResults.sort()
cutResults.reverse()
print "Best cut results:"
for thisresult in cutResults:
  print "s/sigma-b >",threshold,"for",thisresult[0],"MSUGRA points for ht >",thisresult[1],"and kMs >",thisresult[2], "with bkg =",thisresult[3],"(bkg-err =",thisresult[4],")"

     
##pick scenario: lower HT cut 800, lower kMs cut 11 (note to self:there's an implicit UPPER cut at 1500 and 25 as long as I don't take the overflowbins!)
#hlbin = 800 #HT lower cut; possible values: Have a look by prediction["binc"].keys()  after the execfile(infile) statement
#mlbin = 11 #kinMetSig lower cut; possible values: prediction["binc"][800].keys()
#bj = "binc" #b-tag bin possible values: "binc", "b0" (==0), "b1" (==1), "b2" (>=2)
#
##msugra point
#m0     =   800
#m12    =   140
#tanb   =    10
#A0     =     0
#signMu =     1
#
#
##Let's get some numbers
#pred = prediction[bj][hlbin][mlbin]     
#predErr = predictionError[bj][hlbin][mlbin]
#obs = data[bj][hlbin][mlbin]
#print "Lower Cuts: HT:",hlbin,"kinMetSig:",mlbin,"Predicted background:",niceNum(pred),"+/-",niceNum(predErr),"(stat.) Observed in Data: ",obs
#
##read msugra efficiency from file (should be there Friday morning with reasonable numbers;-) 
#
#sigEff = efficiencykinMetSig[bj][hlbin][mlbin][getMSUGRAShortString(m0,m12,tanb,A0,signMu)]      #This is how to access msugra signal efficiency!
#print "Using msugra signal efficiency", sigEff, "for",getMSUGRAShortString(m0,m12,tanb,A0,signMu)

#sigEffErr = 0.01 #A guess.

##calculate limit
#limit = ROOT.roostats_limit(targetLumi, 0.045*targetLumi, sigEff, sigEffErr, pred, predErr, int(obs), False, 0, 'cls', 'stat.png', 0)
#print "obs. limit", limit.GetObservedLimit(), "exp. limit", limit.GetExpectedLimit(), "+1sig.",limit.GetOneSigmaHighRange(), "-1sig.",limit.GetOneSigmaLowRange(), "+2sig.",limit.GetTwoSigmaHighRange(), "-2sig.",limit.GetTwoSigmaLowRange() 
