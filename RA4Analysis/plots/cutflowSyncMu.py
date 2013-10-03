import ROOT
import os, copy

from simplePlotsCommon import *
#execfile("simplePlotsCommon.py")
import xsec
small = False

from simpleStatTools import niceNum
from defaultMuSamples import *
#data={}
#data["name"]     = "Data";
#data["dirname"] = "/data/schoef/pat_120918/mc8TeV/"
#data["bins"]    = [ '8TeV-TTJets']
data={}
data["name"]     = "Data";
data["dirname"] = "/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_5_3_3_patch2/src/Workspace/RA4Analysis/crab/"
data["bins"]    = [ 'pickEvents']
sample = data
#sample = qcd 
#targetLumi = 35.76
res = {}
#ttbar["dirname"] = "/scratch/schoef/pat_110120/Mu-PU/"

table = [\
  [("1"), "Filters"],
  ["jet0pt>=40", ">=1 Jets"],
  ["jet1pt>=40", ">=2 Jets"],
  ["jet2pt>=40", ">=3 Jets"],
  ["jet3pt>=40", ">=4 Jets"],
  ["jet3pt>=40&&ngoodMuons==1", ">=4 Jets ==1 Mu"],
  ["jet3pt>=40&&ngoodMuons==1&&ngoodElectrons==0", ">= 4 Jets ==1 Mu && ==0 Ele"],
  ["jet3pt>=40&&ngoodMuons==1&&ngoodElectrons==0&&nvetoMuons==1", ">= 4 Jets ==1 Mu && ==0 Ele && ==1 vMuons"],
  ["jet3pt>=40&&ngoodMuons==1&&ngoodElectrons==0&&nvetoMuons==1&&nvetoElectrons==0", ">= 4 Jets ==1 Mu && ==0 Ele && ==1 vMuons && ==0 vEle"],
  ["jet3pt>=40&&ngoodMuons==1&&ngoodElectrons==0&&nvetoMuons==1&&nvetoElectrons==0&&ht>300", ">= 4 Jets ==1 Mu && ==0 Ele && ==1 vMuons && ==0 vEle && ht>300"],
  ["jet3pt>=40&&ngoodMuons==1&&ngoodElectrons==0&&nvetoMuons==1&&nvetoElectrons==0&&ht>300&&type1phiMet>100", ">= 4 Jets ==1 Mu && ==0 Ele && ==1 vMuons && ==0 vEle && ht>300 && type-I-phi met>100"],
  ["jet3pt>=40&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1&&ht>300&&type1phiMet>100", ">= 4 Jets ==0 Mu && ==1 Ele && ==0 vMuons && ==1 vEle && ht>300 && type-I-phi met>100"],
  ["(ngoodMuons==1&&ngoodElectrons==0)||(ngoodMuons==0&&ngoodElectrons==1)", "1 tight Mu or Ele (exclusive)"],
  ["(ngoodMuons==1&&ngoodElectrons==0)", "1 tight Mu 0 tight Ele"],
  ["(ngoodMuons==1&&ngoodElectrons==0&&nvetoMuons==1&&nvetoElectrons==0)", "1 tight Mu 0 tight Ele + lepton veto"],
  ["(ngoodMuons==0&&ngoodElectrons==1)", "1 tight Ele 0 tight Mu"],
  ["(ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1)", "1 tight Ele 0 tight Mu + lepton veto"],
  ["((ngoodMuons==1&&ngoodElectrons==0)||(ngoodMuons==0&&ngoodElectrons==1))&&jet2pt>=40", "1 tight Mu or Ele (exclusive) + >=3 jets >40 GeV"],
  ["((ngoodMuons==1&&ngoodElectrons==0)||(ngoodMuons==0&&ngoodElectrons==1))&&jet2pt>=40&&nbtags>0", "1 tight Mu or Ele (exclusive) + >=3 jets >40 GeV + >=1 btags (among all jets > 40 GeV)"],
  ["((ngoodMuons==1&&ngoodElectrons==0)||(ngoodMuons==0&&ngoodElectrons==1))&&jet3pt>=40", "1 tight Mu or Ele (exclusive) + >=4 jets >40 GeV"],
  ["((ngoodMuons==1&&ngoodElectrons==0)||(ngoodMuons==0&&ngoodElectrons==1))&&jet3pt>=40&&nbtags>0", "1 tight Mu or Ele (exclusive) + >=4 jets >40 GeV + >=1 btags (among all jets > 40 GeV)"],
  ["((ngoodMuons==1&&ngoodElectrons==0)||(ngoodMuons==0&&ngoodElectrons==1))&&jet2pt>=40&&met>50", "1 tight Mu or Ele (exclusive) + >= 3 jets + typeI-MET > 50 GeV"],
  ["((ngoodMuons==1&&ngoodElectrons==0)||(ngoodMuons==0&&ngoodElectrons==1))&&jet2pt>=40&&type1phiMet>50", "1 tight Mu or Ele (exclusive) + >= 3 jets + typeI-phi-MET > 50 GeV"],
  ]

c = ROOT.TChain("Events")
for thisbin in sample["bins"]:
  d = ROOT.TChain("Runs")
#  for thisbin in sample["bins"]:
  print "Adding thisbin",thisbin
  subdirname = sample["dirname"]+thisbin
  filelist=os.listdir(sample["dirname"]+thisbin)
  for thisfile in filelist:
    if os.path.isfile(subdirname+"/"+thisfile) and thisfile[-5:]==".root" and thisfile.count("histo")==1:
      c.Add(subdirname+"/"+thisfile)
      d.Add(subdirname+"/"+thisfile)
  nevents = 0
  nruns = d.GetEntries()
  for i in range(0, nruns):
    d.GetEntry(i)
#    print "Counts = ",getValue(d,"uint_EventCounter_runCounts_PAT.obj")
    nevents += getValue(d,"uint_EventCounter_runCounts_PAT.obj")

  n = nevents 
  print "Sample Name", sample["name"], sample["dirname"],"bin", thisbin, "nevents", nevents
  weight = 1
#  if xsec.xsec.has_key(thisbin):
#    weight = targetLumi*xsec.xsec[thisbin]/float(countHLTFilter)
  for f in ["uint_EventCounterAfterHLT_runCounts_PAT.obj", "uint_EventCounterAfterScraping_runCounts_PAT.obj", "uint_EventCounterAfterPV_runCounts_PAT.obj", "uint_EventCounterAfterHBHE_runCounts_PAT.obj", "uint_EventCounterAfterTrackingFailure_runCounts_PAT.obj", "uint_EventCounterAfterLaser_runCounts_PAT.obj", "uint_EventCounterAfterCSC_runCounts_PAT.obj", "uint_EventCounterAfterEEBadSC_runCounts_PAT.obj", "uint_EventCounterAfterECALTP_runCounts_PAT.obj"]:
    thisres = 0
    for i in range(0, nruns):
      d.GetEntry(i)
  #    print "Counts = ",getValue(d,"uint_EventCounter_runCounts_PAT.obj")
      thisres += getValue(d, f)
    print f, thisres

  for t in table:
    n = c.GetEntries(t[0])
    basis = weight*n
    res[t[1]] = weight*n 
    print t[0], n, "(",weight*n,")"

for t in table:
  print t[1], res[t[1]]

#for thisbin in sample["bins"]: 
#  c = ROOT.TChain("pfRA4Analyzer/Events") 
##  for thisbin in sample["bins"]: 
#  print "Adding thisbin",thisbin 
#  c.Add(sample["dirname"]+thisbin+"/*.root") 
#  c.Draw(">>eList",commoncf+"&&"+"jet3pt>40&&ngoodMuons==1&&ngoodElectrons==0&&nvetoMuons==1&&nvetoElectrons==0&&ht>300&&met>150") 
#  elist = ROOT.gDirectory.Get("eList") 
#  number_events = elist.GetN() 
#  for i in range(0, number_events): 
#    c.GetEntry(elist.GetEntry(i)) 
#    print "event, run, lumiblock: ", int(c.GetLeaf("event").GetValue()), int(c.GetLeaf("run").GetValue()), int(c.GetLeaf("lumiblock").GetValue()) 
#    print "met, lepton-pt, ht            :", niceNum(c.GetLeaf("met").GetValue()   ) , niceNum(c.GetLeaf("lepton_pt").GetValue()) , niceNum(c.GetLeaf("ht").GetValue()    ) 
#    print "jet0pt, jet1pt, jet2pt, jet3pt:", niceNum(c.GetLeaf("jet0pt").GetValue()) , niceNum(c.GetLeaf("jet1pt").GetValue()   ) , niceNum(c.GetLeaf("jet2pt").GetValue()), niceNum( c.GetLeaf("jet3pt").GetValue()) 
#    print  

  

#for ana in ["pfRA4Analyzer_cleanPatJetsAK5PF", "pfRA4Analyzer_patJets", "pfRA4Analyzer_patJetsAK5PF", "pfRA4Analyzer_patJetsPF", "pfRA4Analyzer_selectedPatJetsPF"]:
#  for thisbin in sample["bins"]:
#    print "ana:", ana, "##############################"
#    c = ROOT.TChain(ana+"/Events")
#    c.Add("../crab/SDmu/histo.root")
#    c.Draw(">>eList","ngoodMuons==1&&ngoodElectrons==0&&nvetoMuons==1&&nvetoElectrons==0")
#    elist = ROOT.gDirectory.Get("eList")
#    number_events = elist.GetN()
#    for i in range(0, number_events):
#      c.GetEntry(elist.GetEntry(i))
#      print "event, run, lumiblock: ", int(c.GetLeaf("event").GetValue()), int(c.GetLeaf("run").GetValue()), int(c.GetLeaf("lumiblock").GetValue())
#      print "met, lepton-pt, ht            :", niceNum(c.GetLeaf("met").GetValue()   ) , niceNum(c.GetLeaf("lepton_pt").GetValue()) , niceNum(c.GetLeaf("ht").GetValue()    )
#      print "jet0pt, jet1pt, jet2pt, jet3pt:", niceNum(c.GetLeaf("jet0pt").GetValue()) , niceNum(c.GetLeaf("jet1pt").GetValue()   ) , niceNum(c.GetLeaf("jet2pt").GetValue()), niceNum( c.GetLeaf("jet3pt").GetValue())
#      print

c.SetScanField(10000000)
#c.Scan("event:leptonPdg:met:ht:njets:nvetoMuons:nvetoElectrons", "(ngoodMuons==1&&ngoodElectrons==0)||(ngoodMuons==0&&ngoodElectrons==1)", "@colsize=6") 
for i in [2]:
  t = table[i] 
  print "\n\n",t[1],"\n"
  c.Scan("event:lumi:leptonPdg:met:type1phiMet:ht:njets:nvetoMuons:nvetoElectrons", t[0], "@colsize=12") 


#mode = "Ele"
#fileIN = open("chris"+mode+".txt", "r")
#line = fileIN.readline()
#oldevent = -1
#n=0
#while line:
#  ls=line.replace(" ","").split("*")
#  event = ls[3]
#  if oldevent==event:
#    line = fileIN.readline()
#    continue
#  print "\n\n"
#  print line
#  if mode=="Ele":
#    c.Scan("event:leptonPt:leptonEta:leptonPhi:leptonPF03PhotonIso:leptonPF03NeutralHadronIso:eleRho:leptonPF03ChargedHadronIso","event=="+str(event),"@colsize=10")
#  if mode=="Mu":
#    c.Scan("event:leptonPt:leptonEta:leptonPhi:leptonPF04PhotonIso:leptonPF04NeutralHadronIso:eleRho:leptonPF04ChargedHadronIso","event=="+str(event),"@colsize=10")
#  line = fileIN.readline()
#  oldevent = event
##  if n>10:
##    break
#  n+=1
