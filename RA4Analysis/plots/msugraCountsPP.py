import ROOT
from array import array
from math import *
import os, copy, sys
from simpleStatTools import niceNum
from Workspace.RA4Analysis.simplePlotsCommon import *
from processStatistics import productionCode
import xsec, pickle

small = False
maxEvents = -1
if small:
  maxEvents = 1000
targetLumi=4700.

scanpath = "/data/schoef/pat_120121/"
chainstring = "Events"

counts = {}
countsPP = {}

c = ROOT.TChain("msugraCounter/Events")
files = "*.root"
if small:
  files = "histo_10*.root"
c.Add(scanpath+"/count-msugra/"+files)

c.Draw(">>eList", "(1)")
eList = ROOT.gROOT.Get("eList")
print "Total # of Events in Count-Scan:",eList.GetN()

nev = eList.GetN()
if maxEvents>0:
  nev = min(maxEvents, eList.GetN())
for nEvent in range(0, nev):
  if (nEvent%10000 == 0):
    print nEvent

  c.GetEntry(eList.GetEntry(nEvent))
  m0      =      getValue( c, "msugraM0")
  m12     =      getValue( c, "msugraM12")
  pcode = productionCode([getValue( c, "sparticle0"), getValue( c, "sparticle1") ])
  sstring = getMSUGRAShortString(m0, m12, 10, 0, 1)
  if not counts.has_key(sstring):
    counts[sstring] = 0
    countsPP[sstring] = {}

  if not countsPP[sstring].has_key(pcode):
    countsPP[sstring][pcode] = 0
  counts[sstring]+=1
  countsPP[sstring][pcode]+=1
if not small:
  pickle.dump(counts,     open("/data/schoef/efficiencies/msugra_counts.pkl", 'wb'))
  print "Written", "/data/schoef/efficiencies/msugra_counts.pkl"
  pickle.dump(countsPP,   open("/data/schoef/efficiencies/msugra_countsPP.pkl", 'wb'))
  print "Written", "/data/schoef/efficiencies/msugra_countsPP.pkl"

#  else:
#    print "No writing when small"
