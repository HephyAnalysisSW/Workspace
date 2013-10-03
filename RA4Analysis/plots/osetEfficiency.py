import ROOT
from array import array
from math import *
import os, copy, sys
from simpleStatTools import niceNum
from simplePlotsCommon import *
import xsec

small = False
maxEvents = -1
if small:
  maxEvents = 1000
mode = "Ele"
mode = "Mu"
if len(sys.argv)>1:
  mode = sys.argv[1]

if mode == "Mu":
  from defaultMuSamples import *
if mode == "Ele":
  from defaultEleSamples import *
#model = "T3wb"
#model = "T1tttt"
model = "T2ttww"
if len(sys.argv)>2:
  model = sys.argv[2]
eventsPerPoint = {"T3w":50000, "T1tttt":50000, "T2tt":50000, "T3wb":10000, "T2ttww":50000}

print "Model:",model, "mode:",mode
twoStep = False
if model =="T2tt" or model == "T1tttt" or model == "T2ttww":
  twoStep = True

presel = "pf-3j40"
subdir = "/pngBM/"
scanpath = "/data/schoef/pat_111201/"
if model == "T2ttww":
  scanpath = "/data/schoef/pat_120213/"
chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

binningHT =  [750, 1000]
binningMET = [250, 350, 450, 550 ]

bjetbins = {"inc":"(1)", \
            "b0":"(!(btag0>1.74))",
            "b1":"(btag0>1.74&&(!(btag1>1.74)))",
            "b2":"(btag1>1.74)",
            "b3":"(btag2>1.74)"
            }

bjetbinsPy = {}
for bj in bjetbins.keys():
  bjetbinsPy[bj] = bjetbins[bj].replace("&&"," and ").replace("!", " not ")

samples = {"mc":mc, \
           "data":data}
allSamples = samples.values() 

additionalCut = ""
preprefix = mode

if mode == "Mu":
  if presel == "pf-3j40":
    chainstring = "Events"
    commoncf = "jet1pt>40&&jet2pt>40&&leptonPt>20&&singleMuonic&&nvetoElectrons==0&&nvetoMuons==1"
if mode == "Ele":
  if presel == "pf-3j40":
    chainstring = "Events"
    commoncf = "jet1pt>40&&jet2pt>40&&leptonPt>20&&singleElectronic&&nvetoElectrons==1&&nvetoMuons==0"

if additionalCut != "":
  commoncf = commoncf + "&&" +  additionalCut

prefix = preprefix


#Calculating SMS efficiencies
#filename = "/afs/hephy.at/user/s/schoefbeck/www/"+subdir+"/"+prefix+"_"+model+"_Efficiencies.py"
filename = "/data/schoef/efficiencies/"+prefix+"_"+model+"_Efficiencies.py"
efficiency = {}
if True or not os.path.exists(filename):
  c = ROOT.TChain("Events")
  files = "*.root"
  if small:
    files = "histo_1*.root"
  if mode == "Mu":
    c.Add(scanpath+"/Mu/"+model+"/"+files)
  if mode == "Ele":
    c.Add(scanpath+"/EG/"+model+"/"+files)
#  cutstring = commoncf+"&&"+bjetbins[bj]+"&&"+addCutString("ht>"+str(lhbin),"kinMetSig>"+str(lmbin))
  for bj in bjetbins.keys():
    efficiency[bj]={}
    for lhbin in binningHT:
      efficiency[bj][lhbin]={}
      for lmbin in binningMET:
        efficiency[bj][lhbin][lmbin]={}
  print "Mode",mode,"...Chaining...",model,"scan", commoncf
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
    mgl     =      getValue( c, "osetMgl")
    mn      =      getValue( c, "osetMN")
    mc      =      getValue( c, "osetMC")
    case = (mn-mc)/(mn-mgl)
    if twoStep:
      case = "def"
      mc = -1
    btag0   =      getValue( c, "btag0")
    btag1   =      getValue( c, "btag1")
    btag2   =      getValue( c, "btag2")
    ht =           getValue( c, "ht")
    barepfMet =    getValue( c, "barepfmet")
#    print ht, barepfMet, btag0, btag1
    sstring = getOSTShortString(model, mgl, mn, mc)
#    print sstring, mgl, mn, mc
    for bj in bjetbins.keys():
      for lhbin in binningHT:
        for lmbin in binningMET:
          if not efficiency[bj][lhbin][lmbin].has_key(case):
            efficiency[bj][lhbin][lmbin][case] = {}
          if not efficiency[bj][lhbin][lmbin][case].has_key(sstring):
            efficiency[bj][lhbin][lmbin][case][sstring] = 0
          if eval(bjetbinsPy[bj]) and ht>lhbin and barepfMet>lmbin:
            efficiency[bj][lhbin][lmbin][case][sstring]+=1

  for bj in bjetbins.keys():
    for lhbin in binningHT:
      for lmbin in binningMET:
        for ckey in  efficiency[bj][lhbin][lmbin].keys():
          for skey in  efficiency[bj][lhbin][lmbin][ckey].keys():
            efficiency[bj][lhbin][lmbin][ckey][skey] = efficiency[bj][lhbin][lmbin][ckey][skey]/float(eventsPerPoint[model])
  del eList
  del c
  if not small:
    ofile = open(filename, "w")
    ofile.write("commoncf = "+repr(commoncf)+"\n")
    ofile.write("efficiency = "+repr(efficiency)+"\n")
    ofile.close()
    print "Written",filename
else:
  execfile(filename)
  print "Loaded",filename
