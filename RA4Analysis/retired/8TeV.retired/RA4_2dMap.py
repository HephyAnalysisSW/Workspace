import ROOT
from array import array
from math import *
import os, copy

from Workspace.RA4Analysis.simplePlotsCommon import *
from funcs import *

import xsec
small = False

from defaultMuSamples import *
targetLumi = 1000
ttbar["name"] = "TTbar"
wjets["name"] = "WJets"
stop["name"]  = "singleTop"
qcd["name"]   = "QCD"
dy["name"]    = "DYJets"

allSamples = [ttbar,wjets]

#signalNumbers = [1,8]
additionalCut = ""
presel = "pf-3j40"
subdir = "/pngMC/"
metvar = "genmet"
preprefix="2Dmap_TT+W_"+metvar


if presel == "4j30":
  chainstring = "RA4Analyzer/Events"
  commoncf = "jet1pt>30&&jet3pt>30&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
if presel == "pf-4j30":                                                                         
  chainstring = "pfRA4Analyzer/Events"                                                          
  commoncf = "jet1pt>30&&jet3pt>30&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
if presel == "pf-ex3j30":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>30&&jet2pt>30&&(!(jet3pt>30))&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
if presel == "pf-3j40":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>40&&jet2pt>40&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
if presel == "pf-4j40":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>40&&jet3pt>40&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"
if presel == "pf-2j40":
  chainstring = "pfRA4Analyzer/Events"
  commoncf = "jet1pt>40&&lepton_pt>20&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= presel+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"

for sample in allSamples:
  sample["Chain"] = chainstring

for var in allVars:
  var.logy=True
for sample in allSamples:
  sample["filenames"]={}
  sample["weight"]={}
  if not sample.has_key("bins"):
    sample["bins"]=[""]
  for bin in sample["bins"]:
    subdirname = sample["dirname"]+"/"+bin+"/"
    if sample["bins"]==[""]:
      subdirname = sample["dirname"]+"/"
    c = ROOT.TChain("countingHLTFilter/CountTree")
    sample["filenames"][bin]=[]
    if small:
      filelist=os.listdir(subdirname)
      counter = 1   #Joining n files
      for thisfile in filelist:
        if os.path.isfile(subdirname+thisfile) and thisfile[-5:]==".root" and thisfile.count("histo")==1:
          sample["filenames"][bin].append(subdirname+thisfile)
#          c.Add(sample["dirname"]+file)
          if counter==0:
            break
          counter=counter-1
    else:
      sample["filenames"][bin] = [subdirname+"/h*.root"]
    for thisfile in sample["filenames"][bin]:
      c.Add(thisfile)
    lookupCHF = True
    if sample.has_key("hasCountingHLTFilter"):
      if sample["hasCountingHLTFilter"]==False:
        lookupCHF = False
    nevents = -1.
    if lookupCHF:
      nevents = c.GetEntries()
    weight = 1.
    lumi = 1.
    normToLumi = False
    if globals().has_key("targetLumi"):
      lumi = targetLumi
    if xsec.xsec.has_key(bin):
      normToLumi = True
      if nevents>0:
        weight = xsec.xsec[bin]*lumi/float(nevents)
      else:
        weight = 0.
    if normToLumi:
      print "Normalizing to lumi", lumi, sample["dirname"] , sample["name"], bin, nevents,"weight",weight
    else:
      print "Do NOT normalize to lumi;", sample["dirname"] , sample["name"], bin, nevents,"weight",weight
    sample["weight"][bin]=weight
    del c


stuff=[]
def drawBox(htval, metval):
  lines = [ \
   ROOT.TLine(metval[0],htval[0],metval[0],htval[1]),
   ROOT.TLine(metval[0],htval[1],metval[1],htval[1]),
   ROOT.TLine(metval[1],htval[1],metval[1],htval[0]),
   ROOT.TLine(metval[1],htval[0],metval[0],htval[0])]
  for l in lines:
    l.Draw()
    stuff.append(l)
canv = ROOT.TCanvas() 
hist = ROOT.TH2F("met_VS_ht","met_VS_ht;"+metvar+";H_{T}", 100,0,1000,100,0,1400)
hist.Draw()
hist.GetYaxis().SetLabelSize(0.03)
hist.GetXaxis().SetLabelSize(0.03)
htvals = [[300,400],[400,500],[500,600],[600,700],[700,800],[800,900],[900,1000],[1000,1200],[1200,1400]]
metvals = [[100,300],[300,500],[500,1000]]
results={}
for htval in htvals:
  results[str(htval[0])]={}
  for metval in metvals:
    resstring=""
    drawBox(htval, metval)
    results[str(htval[0])][str(metval[0])]={}
    htcut = "ht>"+str(htval[0])+"&&ht<"+str(htval[1])
    metcut = metvar+">"+str(metval[0])+"&&"+metvar+"<"+str(metval[1])
    cutstring = addCutString(commoncf, addCutString(htcut, metcut))
    print cutstring
    for sample in allSamples:
      results[str(htval[0])][str(metval[0])][sample["name"]] = 0.
      for bin in sample["bins"]:
        chainstring = "recoJetAnalyzer/Events"
        if sample.has_key("Chain"):
          chainstring = sample["Chain"]
        c = ROOT.TChain(chainstring)
        for thisfile in sample["filenames"][bin]:
          c.Add(thisfile)
        entries = c.GetEntries(cutstring)
        events = sample["weight"][bin]*entries
        print "At ht ",htval,metvar,metval,sample["name"],"adding",sample["weight"][bin],"*",entries,"=",events
        results[str(htval[0])][str(metval[0])][sample["name"]] += events
      resstring +=" #splitline{"+sample["name"]+"}{"+str(round(results[str(htval[0])][str(metval[0])][sample["name"]],2))+"}"
    restext = ROOT.TLatex(sum(metval)/2., sum(htval)/2., resstring)
    restext.SetTextAlign(22)
    restext.SetTextSize(0.02)
    restext.Draw()
    stuff.append(restext)
canv.Print(defaultWWWPath+subdir+prefix+"2DMap.png")
