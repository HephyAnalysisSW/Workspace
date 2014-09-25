import ROOT
import os, copy

from Workspace.RA4Analysis.simplePlotsCommon import *
#execfile("simplePlotsCommon.py")
import xsec
small = False

from simpleStatTools import niceNum

from defaultEleSamples import *
allSamples = [ttbar, wjets, qcd, stop, dy, data]
ttbar["name"] = "TT + Jets"
wjets["name"] = "W + Jets"
wjets["bins"] = ["WJetsToLNu"]
stop["name"] = "single $t$"
qcd["name"] = "QCD"
dy["name"] = "DY + Jets"
data["name"] = "Data"

res = {}
niceName={}
#commoncf = "muonTriggerUnprescaled" 
commoncf = "(1)" 
basis = {}
for sample in allSamples:
  res[sample["name"]] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  for thisbin in sample["bins"]:
    c = ROOT.TChain("Events")
    d = ROOT.TChain("Runs")
  #  for thisbin in sample["bins"]:
    print "Adding ",thisbin
    subdirname = sample["dirname"]+thisbin
    filelist=os.listdir(sample["dirname"]+thisbin)
    if small:
      filelist = filelist[:5]
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
    weight = 1
    if xsec.xsec.has_key(thisbin):
      weight = 4700*xsec.xsec[thisbin] / nevents
    print "added ",nevents ,"events"
    n = c.GetEntries(commoncf)
    if n==0:
      n=1
    basis[sample["name"]] = weight*n
    res[sample["name"]][0]+=weight*n 
    niceName["0"] = "cleaning + HLT" 
    print niceName["0"], n, "(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"

    n = c.GetEntries(commoncf+"&&ngoodElectrons==1")
    res[sample["name"]][1]+=weight*n 
    niceName["1"] ="$==1$ e" 
    print niceName["1"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"

    n = c.GetEntries(commoncf+"&&ngoodMuons==0&&ngoodElectrons==1")
    res[sample["name"]][2]+=weight*n 
    niceName["2"] ="$==0$ $\mu$" 
    print niceName["2"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"

    n = c.GetEntries(commoncf+"&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1")
    res[sample["name"]][3]+=weight*n 
    niceName["3"] ="$==0$ veto e" 
    print niceName["3"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"

    n = c.GetEntries(commoncf+"&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0")
    res[sample["name"]][4]+=weight*n 
    niceName["4"] ="$==0$ veto $\mu$"  
    print niceName["4"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"


    n = c.GetEntries(commoncf+"&&"+"jet0pt>40&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1")
    res[sample["name"]][5]+=weight*n 
    niceName["5"] ="$>=1$ Jets"  
    print niceName["5"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"

    n = c.GetEntries(commoncf+"&&"+"jet1pt>40&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1")
    res[sample["name"]][6]+=weight*n 
    niceName["6"] ="$>=2$ Jets"  
    print niceName["6"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"

    n = c.GetEntries(commoncf+"&&"+"jet2pt>40&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1")
    res[sample["name"]][7]+=weight*n 
    niceName["7"] ="$>=3$ Jets"  
    print niceName["7"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"

    n = c.GetEntries(commoncf+"&&"+"ht>300&&jet2pt>40&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1")
    res[sample["name"]][8]+=weight*n 
    niceName["8"] ="$\HT$>=300 \GeV"  
    print niceName["8"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"

    n = c.GetEntries(commoncf+"&&"+"barepfmet>100&&ht>300&&jet2pt>40&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1")
    res[sample["name"]][9]+=weight*n 
    niceName["9"] ="$\ETmiss$>=100 \GeV"  
    print niceName["9"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"

  #  n = c.GetEntries(commoncf+"&&"+"jet3pt>40")
  #  res[sample["name"]][4]+=weight*n 
  #  niceName["4"] =">=4 Jets"  
  #  print niceName["4"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"


    n = c.GetEntries(commoncf+"&&"+"jet2pt>40&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1&&(!(btag0>=1.74))")
    res[sample["name"]][10]+=weight*n 
    niceName["10"] ="$==0$ bjets" 
    print niceName["10"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"

    n = c.GetEntries(commoncf+"&&"+"jet2pt>40&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1&&((btag0>=1.74)&&(!(btag1>=1.74)))")
    res[sample["name"]][11]+=weight*n 
    niceName["11"] ="$==1$ bjets" 
    print niceName["11"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"

    n = c.GetEntries(commoncf+"&&"+"jet2pt>40&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1&&(btag1>=1.74)")
    res[sample["name"]][12]+=weight*n 
    niceName["12"] ="$>=2$ bjets" 
    print niceName["12"], n,"(",weight*n,")",round(100*weight*n/(basis[sample["name"]]),2),"%"
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons>0")
#  res[1]+=weight*n 
#  niceName["1"] = ">0  Mu                                                                   " 
#  print niceName["1"].rstrip(), n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0")
#  res[2]+=weight*n 
#  niceName["2"] = "==1 Mu                                                                   " 
#  print niceName["2"].rstrip(), n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&nvetoMuons==0")
#  res[3]+=weight*n 
#  niceName["3"] = "==1 Mu && ==0 vMu                                                        " 
#  print niceName["3"].rstrip(), n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&nvetoMuons==0&&ngoodElectrons==1")
#  res[4]+=weight*n 
#  niceName["4"] = "==1 Mu && ==0 vMu && ==0 Ele                                             " 
#  print niceName["4"].rstrip(), n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&nvetoMuons==0&&ngoodElectrons==1&&nvetoElectrons==1")
#  res[5]+=weight*n 
#  niceName["5"] = "==1 Mu && ==0 vMu && ==0 Ele && ==0 vEle                                 " 
#  print niceName["5"].rstrip(), n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&nvetoMuons==0&&ngoodElectrons==1&&nvetoElectrons==1&&jet0pt>=40.")
#  res[6]+=weight*n 
#  niceName["6"] = "==1 Mu && ==0 vMu && ==0 Ele && ==0 vEle && >=1jets                      " 
#  print niceName["6"].rstrip(), n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&nvetoMuons==0&&ngoodElectrons==1&&nvetoElectrons==1&&jet1pt>=40.")
#  res[7]+=weight*n 
#  niceName["7"] = "==1 Mu && ==0 vMu && ==0 Ele && ==0 vEle && >=2jets                      " 
#  print niceName["7"].rstrip(), n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&nvetoMuons==0&&ngoodElectrons==1&&nvetoElectrons==1&&jet2pt>=40.")
#  res[8]+=weight*n 
#  niceName["8"] = "==1 Mu && ==0 vMu && ==0 Ele && ==0 vEle && >=3jets                      " 
#  print niceName["8"].rstrip(), n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&nvetoMuons==0&&ngoodElectrons==1&&nvetoElectrons==1&&jet3pt>=40.")
#  res[9]+=weight*n 
#  niceName["9"] = "==1 Mu && ==0 vMu && ==0 Ele && ==0 vEle && >=4jets                      " 
#  print niceName["9"].rstrip(), n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&nvetoMuons==0&&ngoodElectrons==1&&nvetoElectrons==1&&jet2pt>=40.&&met>60")
#  res[10]+=weight*n 
#  niceName["10"]= "==1 Mu && ==0 vMu && ==0 Ele && ==0 vEle && >=3jets && met>60            " 
#  print niceName["10"].rstrip(), n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&nvetoMuons==0&&ngoodElectrons==1&&nvetoElectrons==1&&jet2pt>=40.&&met>60&&ht>300")
#  res[11]+=weight*n 
#  niceName["11"]= "==1 Mu && ==0 vMu && ==0 Ele && && ==0 vEle >=3jets && met>60 && ht>300  " 
#  print niceName["11"].rstrip(), n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"

#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&ngoodElectrons==1&&jet3pt>30.&& 300<ht&&ht<350 && 2.5<kinMetSig&&kinMetSig<4.5")
#  print "...&&300<HT<350 && 2.5<METsig<4.5", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  niceName["8"] = "...&&300<HT<350 && 2.5<METsig<4.5 " 
#  res[8]+=weight*n 
#
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&ngoodElectrons==1&&jet3pt>30.&& 400<ht&& 2.5<kinMetSig&&kinMetSig<4.5")
#  print "...&&400<HT && 2.5<METsig <4.5", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[9]+=weight*n 
#  niceName["9"] = "...&&400<HT && 2.5<METsig <4.5    " 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&ngoodElectrons==1&&jet3pt>30.&& 300<ht&&ht<350 && 4.5<kinMetSig")
#  print "...&&300<HT<350 && 4.5<METsig", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[10]+=weight*n 
#  niceName["10"] ="...&&300<HT<350 && 4.5<METsig     " 
#
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&ngoodElectrons==1&&jet3pt>30.&& 400<ht          && 4.5<kinMetSig")
#  print "...&&400<HT && 4.5<METsig ", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[11]+=weight*n 
#  niceName["11"] ="...&&400<HT && 2.5<METsig <4.5    " 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&ngoodElectrons==1&&jet3pt>30.&& 300<ht&&ht<650 && 2.5<kinMetSig&&kinMetSig<5.5")
#  print "...&&300<HT<650 && 2.5<METsig<5.5", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  niceName["12"] ="...&&300<HT<650 && 2.5<METsig<5.5 " 
#  res[12]+=weight*n 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&ngoodElectrons==1&&jet3pt>30.&& 650<ht&& 2.5<kinMetSig&&kinMetSig<5.5")
#  print "...&&650<HT && 2.5<METsig <5.5", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[13]+=weight*n 
#  niceName["13"] ="...&&650<HT && 2.5<METsig <5.5    " 
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&ngoodElectrons==1&&jet3pt>30.&& 300<ht&&ht<650 && 5.5<kinMetSig")
#  print "...&&300<HT<650 && 5.5<METsig", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[14]+=weight*n 
#  niceName["14"] ="...&&300<HT<650 && 5.5<METsig     " 
#
#
#  n = c.GetEntries(commoncf+"&&"+"ngoodMuons==0&&ngoodElectrons==1&&jet3pt>30.&& 650<ht          && 5.5<kinMetSig")
#  print "...&&650<HT && 5.5<METsig ", n, "(",weight*n,")",round(100*weight*n/(basis),2),"%"
#  res[15]+=weight*n 
#  niceName["15"] ="...&&650<HT && 5.5<METsig         " 
print 
nstring = " & "
for sample in allSamples:
  nstring+=" \multicolumn{2}{c}{"+sample["name"]+"} &"

nstring = nstring[:-1]+"\\hline\\\\"
print nstring

for nr in range(0,100):
  sstring = ""
  if niceName.has_key(str(nr)):
    sstring += niceName[str(nr)]+" & "
    for sample in allSamples:
      sstring+=niceNum(res[sample["name"]][nr])+"&"+niceNum(100*res[sample["name"]][nr]/res[sample["name"]][0])+"\\% &"
    sstring = sstring[:-1]+"\\\\"
    print sstring

#for thisbin in sample["bins"]: 
#  c = ROOT.TChain("pfRA4Analyzer/Events") 
##  for thisbin in sample["bins"]: 
#  print "Adding thisbin",thisbin 
#  c.Add(sample["dirname"]+thisbin+"/*.root") 
#  c.Draw(">>eList",commoncf+"&&"+"jet3pt>40&&ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1&&ht>300&&met>150") 
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
#    c.Draw(">>eList","ngoodMuons==0&&ngoodElectrons==1&&nvetoMuons==0&&nvetoElectrons==1")
#    elist = ROOT.gDirectory.Get("eList")
#    number_events = elist.GetN()
#    for i in range(0, number_events):
#      c.GetEntry(elist.GetEntry(i))
#      print "event, run, lumiblock: ", int(c.GetLeaf("event").GetValue()), int(c.GetLeaf("run").GetValue()), int(c.GetLeaf("lumiblock").GetValue())
#      print "met, lepton-pt, ht            :", niceNum(c.GetLeaf("met").GetValue()   ) , niceNum(c.GetLeaf("lepton_pt").GetValue()) , niceNum(c.GetLeaf("ht").GetValue()    )
#      print "jet0pt, jet1pt, jet2pt, jet3pt:", niceNum(c.GetLeaf("jet0pt").GetValue()) , niceNum(c.GetLeaf("jet1pt").GetValue()   ) , niceNum(c.GetLeaf("jet2pt").GetValue()), niceNum( c.GetLeaf("jet3pt").GetValue())
#      print 
