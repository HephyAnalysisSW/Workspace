import ROOT
from array import array
from math import *
import os, copy, sys
from simpleStatTools import niceNum
from Workspace.RA4Analysis.simplePlotsCommon import *
from processStatistics import productionCode
import xsec, pickle

small = True
maxEvents = -1
if small:
  maxEvents = 1000
mode = "Mu"
#mode = "Ele"
if len(sys.argv)>1:
  mode = sys.argv[1]

if mode == "Mu":
  from defaultMuSamples import *

if mode == "Ele":
  from defaultEleSamples import *
targetLumi=4700.

presel = "pf-3j40"
scanpath = "/data/schoef/pat_120121/"
chainstring = "empty"
commoncf = "(0)"
prefix = mode 

binningHT =  [750, 1000]
binningMET = [250, 350, 450, 550]


bjetbins = {"inc":"(1)", \
            "b0":"(!(btag0>1.74))",
            "b1":"(btag0>1.74&&(!(btag1>1.74)))",
            "b2":"(btag1>1.74)"
            }

bjetbinsPy = {}
for bj in bjetbins.keys():
  bjetbinsPy[bj] = bjetbins[bj].replace("&&"," and ").replace("!", " not ")

samples = {"mc":mc, \
           "data":data}

allSamples = samples.values() 

additionalCut = ""

if mode == "Mu":
  if presel == "pf-3j40":
    chainstring = "Events"
    commoncf = "jet2pt>40&&leptonPt>20&&singleMuonic&&nvetoElectrons==0&&nvetoMuons==1"

if mode == "Ele":
  if presel == "pf-3j40":
    chainstring = "Events"
    commoncf = "jet2pt>40&&leptonPt>20&&singleElectronic&&nvetoElectrons==1&&nvetoMuons==0"

if additionalCut != "":
  commoncf = commoncf + "&&" +  additionalCut

#Calculating msugra efficiencies
xsecNLODict = pickle.load(file('/data/schoef/efficiencies/msugra/tanb10.msugra_xsecs.pc'))
def xsecNLO(m0, m12, pcode):
  if (xsecNLODict.has_key(int(m12))) and not pcode == "--":
    if (xsecNLODict[int(m12)].has_key(int(m0))):
      return xsecNLODict[int(m12)][int(m0)][pcode]

  return float('nan')

xsecLODict =  pickle.load(file('/data/schoef/efficiencies/msugra/goodModelNames_10_0_1.pkl'))
def xsecLO(m0, m12):
  if xsecLODict.has_key((m0, m12, 10,0,1)):
    return xsecLODict[(m0, m12, 10, 0, 1)]
  else:
    return float('nan')

countsPP   =  pickle.load(file('/data/schoef/efficiencies/msugra/msugra_countsPP.pkl'))
countsTotal=  pickle.load(file('/data/schoef/efficiencies/msugra/msugra_counts.pkl'))

LO_efficiency = {}
efficiencyPP = {}
LO_events = {}
LO_eventsPP = {}
LO_countsPP = {}
NLO_efficiency = {}
NLO_events = {}
NLO_eventsPP = {}
NLO_countsPP = {}

c = ROOT.TChain("Events")
files = "*.root"
if small:
  files = "histo_1_*.root"
if mode == "Mu":
  c.Add(scanpath+"/Mu/msugra/"+files)
if mode == "Ele":
  c.Add(scanpath+"/EG/msugra/"+files)
for bj in bjetbins.keys():
  LO_efficiency[bj]={}
  efficiencyPP[bj]={}
  LO_events[bj]={}
  LO_eventsPP[bj]={}
  LO_countsPP[bj]={}
  NLO_efficiency[bj]={}
  NLO_events[bj]={}
  NLO_eventsPP[bj]={}
  NLO_countsPP[bj]={}
  for lhbin in binningHT:
    LO_efficiency[bj][lhbin]={}
    efficiencyPP[bj][lhbin]={}
    LO_events[bj][lhbin]={}
    LO_eventsPP[bj][lhbin]={}
    LO_countsPP[bj][lhbin]={}
    NLO_efficiency[bj][lhbin]={}
    NLO_events[bj][lhbin]={}
    NLO_eventsPP[bj][lhbin]={}
    NLO_countsPP[bj][lhbin]={}
    for lmbin in binningMET:
      LO_efficiency[bj][lhbin][lmbin]={}
      efficiencyPP[bj][lhbin][lmbin]={}
      LO_events[bj][lhbin][lmbin]={}
      LO_eventsPP[bj][lhbin][lmbin]={}
      LO_countsPP[bj][lhbin][lmbin]={}
      NLO_efficiency[bj][lhbin][lmbin]={}
      NLO_events[bj][lhbin][lmbin]={}
      NLO_eventsPP[bj][lhbin][lmbin]={}
      NLO_countsPP[bj][lhbin][lmbin]={}

print "Mode",mode,"...Chaining...msugraScan", commoncf
c.Draw(">>eList", commoncf)
eList = ROOT.gROOT.Get("eList")
print "Total # of Events in Scan:",eList.GetN()

nev = eList.GetN()
if maxEvents>0:
  nev = min(maxEvents, eList.GetN())
for nEvent in range(0, nev):
  if (nEvent%10000 == 0) and i>0 :
    print nEvent

  c.GetEntry(eList.GetEntry(nEvent))
  m0      =      getValue( c, "msugraM0")
  m12     =      getValue( c, "msugraM12")
#    tanb    =      getValue( c, "msugraTanbeta")
#    A0      =      getValue( c, "msugraA0")
#    signMu  =      getValue( c, "msugraSignMu")
  btag0   =      getValue( c, "btag0")
  btag1   =      getValue( c, "btag1")
  ht =           getValue( c, "ht")
  barepfMet =    getValue( c, "barepfmet")
  ileaf = c.GetLeaf("ints_pfRA4Tupelizer_sparticles_PAT.obj")
  pcode = productionCode([int(ileaf.GetValue(0)), int(ileaf.GetValue(1))])
#    sstring = getMSUGRAShortString(m0, m12, tanb, A0, signMu)
  sstring = getMSUGRAShortString(m0, m12, 10, 0, 1)
  for bj in bjetbins.keys():
    for lhbin in binningHT:
      for lmbin in binningMET:
        if not LO_efficiency[bj][lhbin][lmbin].has_key(sstring):
          LO_efficiency[bj][lhbin][lmbin][sstring] = 0
          LO_events[bj][lhbin][lmbin][sstring] = 0
          NLO_efficiency[bj][lhbin][lmbin][sstring] = 0
          NLO_events[bj][lhbin][lmbin][sstring] = 0

        if not efficiencyPP[bj][lhbin][lmbin].has_key(sstring):
          efficiencyPP[bj][lhbin][lmbin][sstring] = {}
          LO_eventsPP[bj][lhbin][lmbin][sstring] = {}
          NLO_eventsPP[bj][lhbin][lmbin][sstring] = {}
          LO_countsPP[bj][lhbin][lmbin][sstring] = {}
          NLO_countsPP[bj][lhbin][lmbin][sstring] = {}
        if not efficiencyPP[bj][lhbin][lmbin][sstring].has_key(pcode):
          efficiencyPP[bj][lhbin][lmbin][sstring][pcode] = 0
          LO_eventsPP[bj][lhbin][lmbin][sstring][pcode] = 0
          NLO_eventsPP[bj][lhbin][lmbin][sstring][pcode] = 0
          LO_countsPP[bj][lhbin][lmbin][sstring][pcode] = 0
          NLO_countsPP[bj][lhbin][lmbin][sstring][pcode] = 0

        if eval(bjetbinsPy[bj]) and ht>lhbin and barepfMet>lmbin:
          efficiencyPP[bj][lhbin][lmbin][sstring][pcode]+=1
          LO_weight = targetLumi*xsecLO(m0, m12)/10000.
          LO_events[bj][lhbin][lmbin][sstring]+=LO_weight
          LO_eventsPP[bj][lhbin][lmbin][sstring][pcode]+=LO_weight
          LO_countsPP[bj][lhbin][lmbin][sstring][pcode]+=1
          if countsTotal.has_key(sstring):
            if countsTotal[sstring]>9900:
              counts_in_process= -1
              if countsPP.has_key(sstring):
                if countsPP[sstring].has_key(pcode):
                  counts_in_process= countsPP[sstring][pcode]
  #              print "Hello",counts_in_process
              if counts_in_process>0:
                NLO_weight = targetLumi*xsecNLO(m0, m12, pcode)/counts_in_process
                if NLO_weight>0 and NLO_weight<float('inf'):
                  NLO_events[bj][lhbin][lmbin][sstring]+=NLO_weight
                  NLO_eventsPP[bj][lhbin][lmbin][sstring][pcode]+=NLO_weight
                  NLO_countsPP[bj][lhbin][lmbin][sstring][pcode]+=1
#                print LO_weight, NLO_weight, NLO_weight/LO_weight

for bj in bjetbins.keys():
  for lhbin in binningHT:
    for lmbin in binningMET:
      for sstring in  LO_efficiency[bj][lhbin][lmbin].keys():
        m0 = int(sstring.split("_")[1])
        m12 = int(sstring.split("_")[2])
        LO_efficiency[bj][lhbin][lmbin][sstring] = LO_events[bj][lhbin][lmbin][sstring] / (targetLumi*xsecLO(m0, m12))
        for pcode in efficiencyPP[bj][lhbin][lmbin][sstring].keys():
          if countsTotal.has_key(sstring):
            if countsTotal[sstring]>9900:
              counts_in_process = -1
              if countsPP.has_key(sstring):
                if countsPP[sstring].has_key(pcode):
                  counts_in_process = countsPP[sstring][pcode]
              if counts_in_process>0:
                efficiencyPP[bj][lhbin][lmbin][sstring][pcode] = efficiencyPP[bj][lhbin][lmbin][sstring][pcode]/float(counts_in_process)
              else:
                efficiencyPP[bj][lhbin][lmbin][sstring][pcode] = -1.
            else:
              efficiencyPP[bj][lhbin][lmbin][sstring][pcode] = -1.
        if xsecNLO(m0, m12, 'total')>0 and xsecNLO(m0, m12, 'total')<float('inf'):
          NLO_efficiency[bj][lhbin][lmbin][sstring] = NLO_events[bj][lhbin][lmbin][sstring] / (targetLumi*xsecNLO(m0, m12, 'total') )
        else:
          NLO_efficiency[bj][lhbin][lmbin][sstring] = 0. 

del eList
del c

if not small:
#  filename  = "/data/schoef/efficiencies/" + mode +"_LO_msugraEfficiencies.py"
#  ofile = open(filename, "w")
#  ofile.write("commoncf = "+repr(commoncf)+"\n")
#  ofile.write("LO_efficiency = "   +repr(LO_efficiency)+"\n")
#  ofile.write("LO_efficiencyPP = " +repr(LO_efficiencyPP)+"\n")
#  ofile.write("LO_events = "       +repr(LO_events)+"\n")
#  ofile.write("LO_eventsPP = "     +repr(LO_eventsPP)+"\n")
#  ofile.close()
#  print "Written",filename
  pickle.dump(efficiencyPP,      open("/data/schoef/efficiencies/msugra/"+prefix+'_msugra_efficiencyPP.pkl', 'wb'))
  print "/data/schoef/efficiencies/msugra/"+prefix+'_msugra_efficiencyPP.pkl'
  pickle.dump(LO_events,         open("/data/schoef/efficiencies/msugra/"+prefix+'_msugra_LO_events.pkl', 'wb'))
  print "/data/schoef/efficiencies/msugra/"+prefix+'_msugra_LO_events.pkl'
  pickle.dump(LO_eventsPP,       open("/data/schoef/efficiencies/msugra/"+prefix+'_msugra_LO_eventsPP.pkl', 'wb'))
  print "/data/schoef/efficiencies/msugra/"+prefix+'_msugra_LO_eventsPP.pkl'
  pickle.dump(LO_countsPP,       open("/data/schoef/efficiencies/msugra/"+prefix+'_msugra_LO_countsPP.pkl', 'wb'))
  print "/data/schoef/efficiencies/msugra/"+prefix+'_msugra_LO_countsPP.pkl'
  pickle.dump(LO_efficiency,     open("/data/schoef/efficiencies/msugra/"+prefix+'_msugra_LO_efficiency.pkl', 'wb'))
  print "/data/schoef/efficiencies/msugra/"+prefix+'_msugra_LO_efficiency.pkl'
  pickle.dump(NLO_events,         open("/data/schoef/efficiencies/msugra/"+prefix+'_msugra_NLO_events.pkl', 'wb'))
  print "/data/schoef/efficiencies/msugra/"+prefix+'_msugra_NLO_events.pkl'
  pickle.dump(NLO_eventsPP,       open("/data/schoef/efficiencies/msugra/"+prefix+'_msugra_NLO_eventsPP.pkl', 'wb'))
  print "/data/schoef/efficiencies/msugra/"+prefix+'_msugra_NLO_eventsPP.pkl'
  pickle.dump(NLO_countsPP,       open("/data/schoef/efficiencies/msugra/"+prefix+'_msugra_NLO_countsPP.pkl', 'wb'))
  print "/data/schoef/efficiencies/msugra/"+prefix+'_msugra_NLO_countsPP.pkl'
  pickle.dump(NLO_efficiency,     open("/data/schoef/efficiencies/msugra/"+prefix+'_msugra_NLO_efficiency.pkl', 'wb'))
  print "/data/schoef/efficiencies/msugra/"+prefix+'_msugra_NLO_efficiency.pkl'

#  else:
#    print "No writing when small"
