import ROOT
import os, copy

from Workspace.RA4Analysis.simplePlotsCommon import *
#execfile("simplePlotsCommon.py")
import xsec
small = False

from simpleStatTools import niceNum

from defaultEleSamples import *

data={}
data["name"]     = "Data";
data["dirname"] = "/data/schoef/pat_111201/EG/"
#data["bins"]    = [ 'Run2011A-May10ReReco', 'Run2011A-PromptReco-v4']
data["bins"]    = ['Run2011A-May10ReReco']
sample = data
#sample = ttbar
#sample = qcd 
#targetLumi = 35.76
res = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#ttbar["dirname"] = "/scratch/schoef/pat_110120/Mu-PU/"

niceName={}
commoncf = "(1)"
#commoncf = "run==173660"
commoncf = "electronTriggerUnprescaled"

for thisbin in sample["bins"]:
  c = ROOT.TChain("Events")
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
  if xsec.xsec.has_key(thisbin):
    weight = targetLumi*xsec.xsec[thisbin]/float(countHLTFilter)
  for f in ["uint_EventCounterAfterHLT_runCounts_PAT.obj", "uint_EventCounterAfterScraping_runCounts_PAT.obj", "uint_EventCounterAfterPV_runCounts_PAT.obj", "uint_EventCounterAfterHBHE_runCounts_PAT.obj", "uint_EventCounterAfterCSC_runCounts_PAT.obj", "uint_EventCounterAfterTrackingFailure_runCounts_PAT.obj", "uint_EventCounterAfterECALTP_runCounts_PAT.obj", "uint_EventCounterAfterECALBE_runCounts_PAT.obj"]:
    thisres = 0
    for i in range(0, nruns):
      d.GetEntry(i)
  #    print "Counts = ",getValue(d,"uint_EventCounter_runCounts_PAT.obj")
      thisres += getValue(d, f)
    print f, thisres
  n = c.GetEntries(commoncf)
  basis = weight*n
  res[0]+=weight*n
  niceName["0"] = "HBHE + pV + scr.-V + Trig.                                                 "
  print niceName["0"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

  n = c.GetEntries(commoncf)
  basis = weight*n
  res[0]+=weight*n 
  niceName["0"] = "HBHE + pV + scr.-V + Trig." 
  print niceName["0"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

  n = c.GetEntries(commoncf+"&&"+"jet0pt>40")
  res[1]+=weight*n 
  niceName["1"] = ">=1 Jets"  
  print niceName["1"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

  n = c.GetEntries(commoncf+"&&"+"jet1pt>40")
  res[2]+=weight*n 
  niceName["2"] = ">=2 Jets"  
  print niceName["2"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

  n = c.GetEntries(commoncf+"&&"+"jet2pt>40")
  res[3]+=weight*n 
  niceName["3"] = ">=3 Jets"  
  print niceName["3"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

  n = c.GetEntries(commoncf+"&&"+"jet3pt>40")
  res[4]+=weight*n 
  niceName["4"] = ">=4 Jets"  
  print niceName["4"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

  n = c.GetEntries(commoncf+"&&"+"jet3pt>40&&ngoodElectrons==1")
  res[5]+=weight*n 
  niceName["5"] = ">=4 Jets ==1 Ele" 
  print niceName["5"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

  n = c.GetEntries(commoncf+"&&"+"jet3pt>40&&ngoodElectrons==1&&ngoodMuons==0")
  res[6]+=weight*n 
  niceName["6"] = ">= 4 Jets ==1 Ele && ==0 Mu" 
  print niceName["6"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

  n = c.GetEntries(commoncf+"&&"+"jet3pt>40&&ngoodElectrons==1&&ngoodMuons==0&&nvetoElectrons==1")
  res[7]+=weight*n 
  niceName["7"] = ">= 4 Jets ==1 Ele && ==0 Mu && ==1 vElectrons"  
  print niceName["7"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

  n = c.GetEntries(commoncf+"&&"+"jet3pt>40&&ngoodElectrons==1&&ngoodMuons==0&&nvetoElectrons==1&&nvetoMuons==0")
  res[8]+=weight*n 
  niceName["8"] = ">= 4 Jets ==1 Ele && ==0 Mu && ==1 vElectrons && ==0 vMuon"   
  print niceName["8"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

  n = c.GetEntries(commoncf+"&&"+"jet3pt>40&&ngoodElectrons==1&&ngoodMuons==0&&nvetoElectrons==1&&nvetoMuons==0&&ht>300")
  res[9]+=weight*n 
  niceName["9"] = ">= 4 Jets ==1 Ele && ==0 Mu && ==1 vElectrons && ==0 vMuon && ht>300" 
  print niceName["9"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

  n = c.GetEntries(commoncf+"&&"+"jet3pt>40&&ngoodElectrons==1&&ngoodMuons==0&&nvetoElectrons==1&&nvetoMuons==0&&ht>300&&barepfmet>100")
  niceName["10"] = ">= 4 Jets ==1 Ele && ==0 Mu && ==1 vElectrons && ==0 vMuon && ht>300 && barepfmet>100 " 
  print niceName["10"], n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
  res[10]+=weight*n 

#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons>0")
#  print ">0  Mu", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[1]+=weight*n 
#  niceName["1"] = ">0  Mu" 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1")
#  print "==1 Mu", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[2]+=weight*n 
#  niceName["2"] = "==1 Mu" 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0")
#  print "==1 Mu && ==0 Ele", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[3]+=weight*n 
#  niceName["3"] = "==1 Mu && ==0 Ele" 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet0pt>=30.")
#  print "==1 Mu && ==0 Ele && >=1jets", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[4]+=weight*n 
#  niceName["4"] = "==1 Mu && ==0 Ele && >=1jets" 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet1pt>=30.")
#  print "==1 Mu && ==0 Ele && >=2jets", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[5]+=weight*n 
#  niceName["5"] = "==1 Mu && ==0 Ele && >=2jets" 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet2pt>=30.")
#  print "==1 Mu && ==0 Ele && >=3jets", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[6]+=weight*n 
#  niceName["6"] = "==1 Mu && ==0 Ele && >=3jets" 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet3pt>=30.")
#  print "==1 Mu && ==0 Ele && >=4jets", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[7]+=weight*n 
#  niceName["7"] = "==1 Mu && ==0 Ele && >=4jets" 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet3pt>30.&& 300<ht&&ht<350 && 2.5<kinMetSig&&kinMetSig<4.5")
#  print "...&&300<HT<350 && 2.5<METsig<4.5", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  niceName["8"] = "...&&300<HT<350 && 2.5<METsig<4.5 " 
#  res[8]+=weight*n 
#
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet3pt>30.&& 400<ht&& 2.5<kinMetSig&&kinMetSig<4.5")
#  print "...&&400<HT && 2.5<METsig <4.5", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[9]+=weight*n 
#  niceName["9"] = "...&&400<HT && 2.5<METsig <4.5" 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet3pt>30.&& 300<ht&&ht<350 && 4.5<kinMetSig")
#  print "...&&300<HT<350 && 4.5<METsig", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[10]+=weight*n 
#  niceName["10"] ="...&&300<HT<350 && 4.5<METsig" 
#
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet3pt>30.&& 400<ht          && 4.5<kinMetSig")
#  print "...&&400<HT && 4.5<METsig ", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[11]+=weight*n 
#  niceName["11"] ="...&&400<HT && 2.5<METsig <4.5" 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet3pt>30.&& 300<ht&&ht<650 && 2.5<kinMetSig&&kinMetSig<5.5")
#  print "...&&300<HT<650 && 2.5<METsig<5.5", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  niceName["12"] ="...&&300<HT<650 && 2.5<METsig<5.5 " 
#  res[12]+=weight*n 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet3pt>30.&& 650<ht&& 2.5<kinMetSig&&kinMetSig<5.5")
#  print "...&&650<HT && 2.5<METsig <5.5", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[13]+=weight*n 
#  niceName["13"] ="...&&650<HT && 2.5<METsig <5.5" 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet3pt>30.&& 300<ht&&ht<650 && 5.5<kinMetSig")
#  print "...&&300<HT<650 && 5.5<METsig", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[14]+=weight*n 
#  niceName["14"] ="...&&300<HT<650 && 5.5<METsig" 
#
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==1&&ngoodElectrons==0&&jet3pt>30.&& 650<ht          && 5.5<kinMetSig")
#  print "...&&650<HT && 5.5<METsig ", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[15]+=weight*n 
#  niceName["15"] ="...&&650<HT && 5.5<METsig" 
basis = res[0]
print 
for nr in range(len(res)):
  sstring = ""
  if niceName.has_key(str(nr)):
    sstring += niceName[str(nr)]
    print sstring+"  "+niceNum(res[nr])+" "+niceNum(100*res[nr]/basis)+"%"

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
