import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
import os
#c = ROOT.TChain("Events")
#AOD
keys = ["1:191256:19125577","1:253183:25318208","1:223695:22369500","1:372766:37276556","1:69715:6971460","1:291179:29117871","1:306556:30655508","1:359169:35916875","1:362516:36251565","1:85315:8531490","1:272127:27212661","1:149868:14986728","1:414754:41475340","1:328925:32892452","1:396431:39643053","1:541791:54179016","1:391174:39117318","1:19812:1981158","1:475204:47520390","1:428663:42866215","1:444126:44412507","1:492068:49206794","1:526193:52619285","1:226200:22619951","1:510695:51069421"]

cEOS = ROOT.TChain('tree')
cEOS.Add('root://eoscms.cern.ch//eos/cms/store/cmst3/group/susy/Phys14_V1/WJetsToLNu_HT100to200/treeProducerSusySingleLepton/tree.root')
#cEOS.Scan('run:lumi:evt:met_pt:met_genPt',"met_pt>500")

resCMGOld={}
for k in keys:
  run, lumi, event=k.split(":")
  cut = "run=="+run+"&&lumi=="+lumi+"&&evt=="+event
  cEOS.Draw(">>eL",cut)
  eL=ROOT.gDirectory.Get("eL")
  if eL.GetN()==1:
    cEOS.GetEntry(eL.GetEntry(0))
    resCMGOld[k]={'met':cEOS.GetLeaf('met_pt').GetValue(),'genMet':cEOS.GetLeaf('met_genPt').GetValue()}
    print "Found ",k, resCMGOld[k]
  else:
    print "Warning, not found:", k
  del eL

cNew = ROOT.TChain('tree')
cNew.Add('')
resCMGNew={}
for k in keys:
  run, lumi, event=k.split(":")
  cut = "run=="+run+"&&lumi=="+lumi+"&&evt=="+event
  cNew.Draw(">>eL",cut)
  eL=ROOT.gDirectory.Get("eL")
  if eL.GetN()==1:
    cNew.GetEntry(eL.GetEntry(0))
    resCMGNew[k]={'met':cNew.GetLeaf('met_pt').GetValue(),'genMet':cNew.GetLeaf('met_genPt').GetValue()}
    print "Found ",k, resCMGNew[k]
  else:
    print "Warning, not found:", k
  del eL

dirAOD = '../../HEPHYPythonTools/crab/pickEvents/crab_0_150122_110626/res/'
files=os.listdir(dirAOD)
events = Events([dirAOD+'/'+f for f in files if f[-5:]==".root"])
events.toBegin()
pfMetLabel = ("pfMet")
pfMetHandle = Handle("vector<reco::PFMET>")
pfChMetLabel = ("pfChMet")
pfChMetHandle = Handle("vector<reco::PFMET>")
pfMetEILabel = ("pfMetEI")
pfMetEIHandle = Handle("vector<reco::PFMET>")
genMetLabel = ("genMetTrue")
genMetHandle = Handle("vector<reco::GenMET>")
resAOD={}
for i in range(events.size()):
  events.to(i)
  events.getByLabel(pfMetLabel,pfMetHandle)
  pfMet =pfMetHandle.product()
  events.getByLabel(pfChMetLabel,pfChMetHandle)
  pfChMet =pfChMetHandle.product()
  events.getByLabel(pfMetEILabel,pfMetEIHandle)
  pfMetEI =pfMetEIHandle.product()
  events.getByLabel(genMetLabel,genMetHandle)
  genMet =genMetHandle.product()
  key=":".join([str(x) for x in [events._event.event().id().run(), events._event.event().id().luminosityBlock(), events._event.event().id().event()]])
  resAOD[key] = {'genMet':genMet[0].pt(), 'pfMet': pfMet[0].pt()}
#  print i, 'genMet', genMet[0].pt(),'pfMet', pfMet[0].pt(),'pfChMet', pfChMet[0].pt(), 'pfMetEI',pfMetEI[0].pt()

dirMINIAOD = '../../HEPHYPythonTools/crab/pickEvents//crab_0_150122_110053/res/'
files=os.listdir(dirMINIAOD)
events = Events([dirMINIAOD+'/'+f for f in files if f[-5:]==".root"])
events.toBegin()
slimmedMETsLabel = ("slimmedMETs")
slimmedMETsHandle = Handle("vector<pat::MET>")
resMINIAOD={}
for i in range(events.size()):
  events.to(i)
  events.getByLabel(slimmedMETsLabel,slimmedMETsHandle)
  slimmedMETs =slimmedMETsHandle.product()
  key=":".join([str(x) for x in [events._event.event().id().run(), events._event.event().id().luminosityBlock(), events._event.event().id().event()]])
  resMINIAOD[key] = {'type1PfMet':slimmedMETs[0].pt(), 'genMet':slimmedMETs[0].genMET().pt()}
#  print i, 'genMet', genMet[0].pt(),'pfMet', pfMet[0].pt(),'pfChMet', pfChMet[0].pt(), 'pfMetEI',pfMetEI[0].pt()

for k in keys:
  l=[ k, 'genMet AOD', str(round(resAOD[k]['genMet'],2)), "pfMet AOD",str(round(resAOD[k]['pfMet'],2))]
  if resMINIAOD.has_key(k):l+=["t1 pfMet MAOD", str(round(resMINIAOD[k]['type1PfMet'],2))] #, "(genMet MAOD",resMINIAOD[k]['genMet']],")"
  if resCMGOld.has_key(k):l+=["CMG met_pt", str(round(resCMGOld[k]['met'],2))] 
  if resCMGNew.has_key(k):l+=["CMG met_pt", str(round(resCMGNew[k]['met'],2))] 
  print " ".join(l)
