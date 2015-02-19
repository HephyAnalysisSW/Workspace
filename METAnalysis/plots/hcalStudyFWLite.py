import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy, random, subprocess, datetime
import pickle

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()


ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")

ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
#ROOT.gStyle.SetPadRightMargin(0.10);
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()

ROOT.tdrStyle.SetPadRightMargin(0.18)
ROOT.useNiceColorPalette(255)


maxEvts=-1

#53X PromptReco JetHT RECO 203835
#files = [
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/2418E19C-7E0B-E211-BA6E-0019B9F70468.root',
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/32130242-8C0B-E211-A5E8-003048D2C0F2.root',
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/34151EB5-800B-E211-82F8-001D09F29524.root',
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/404A4DE0-760B-E211-831F-003048D2C020.root',
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/9E999D7B-880B-E211-9F7F-001D09F2A49C.root',
#  'root://eoscms.cern.ch//eos/cms/store/data/Run2012D/JetHT/RECO/PromptReco-v1/000/203/835/C2405F36-8C0B-E211-AEC5-003048D2BD66.root'
#]
#73X RECO of JetHT_RECO_GR_R_73_V0_HcalExtValid_RelVal_jet2012D_v2
#from files import JetHT_RECO_GR_R_73_V0_HcalExtValid_RelVal_jet2012D_v2
#files = JetHT_RECO_GR_R_73_V0_HcalExtValid_RelVal_jet2012D_v2

#53X Jan22 rereco JetHT AOD of run 208352
files_53X=[
'root://eoscms.cern.ch//eos/cms/store/cmst3/group/susy/schoef/Run2012D_JetHT_AOD_22Jan2013-v1_10001_CE3F0E9D-E496-E211-AF4F-001EC9D7F1F3.root',
'root://eoscms.cern.ch//eos/cms/store/cmst3/group/susy/schoef/Run2012D_JetHT_AOD_22Jan2013-v1_10001_E44B778C-2897-E211-8D62-00259073E482.root',
'root://eoscms.cern.ch//eos/cms/store/cmst3/group/susy/schoef/Run2012D_JetHT_AOD_22Jan2013-v1_10001_F241442B-1D97-E211-ABC8-00259073E446.root',
'root://eoscms.cern.ch//eos/cms/store/cmst3/group/susy/schoef/Run2012D_JetHT_AOD_22Jan2013-v1_10002_ECCBD06E-4B97-E211-A0FB-0025907277BE.root',
]
##73X JetHT_RECO_GR_R_73_V0_HcalExtValid_RelVal_jet2012D_v2 RECO run 208352
files_73X=['root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/0C38D6DD-2FB5-E411-9EE7-0025905964CC.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/28287B06-29B5-E411-9D08-0025905A612A.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/3813BA50-31B5-E411-8FED-003048FFD71E.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/40E2486B-1AB5-E411-89D8-0025905A608C.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/64DFB678-28B5-E411-AF21-0025905A60EE.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/A2FEE11F-30B5-E411-8515-0025905A612A.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/C6F1138A-31B5-E411-99DA-0025905A48FC.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/CE5D6E95-25B5-E411-96C5-0025905A608C.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/FA472010-33B5-E411-B8E3-0025905A610C.root',
 'root://eoscms.cern.ch//store/relval/CMSSW_7_3_2_patch1/JetHT/RECO/GR_R_73_V0_HcalExtValid_RelVal_jet2012D-v2/00000/FC998BD1-34B5-E411-AD7B-0025905938A8.root']

from vetoed import vetoed as vetoedEvents

edmCollections = [ \
  ("vector<reco::PFMET>", "pfMet", "")#, "RECO")
] 

handles={v[1]:Handle(v[0]) for v in edmCollections}

res={}
for files, ver in [[files_53X, "53X"],[files_73X,"73X"]]:
  print "Reading",ver,"files",files
  res[ver]={}
  events = Events(files)
  events.toBegin()
  fileNames=events._filenames
  usedFiles=[]
  runs=[]
  products={}
  size=events.size()
  for nev in range(size):
    if nev%10000==0:print nev,'/',size
    events.to(nev)
    eaux=events.eventAuxiliary()
    run=eaux.run()            
    if run==208352:
      event=eaux.event()
      lumi=eaux.luminosityBlock()
      for v in edmCollections:
        events.getByLabel(v[1:],handles[v[1]])
        products[v[1]] =handles[v[1]].product()
      res[ver][":".join(str(x) for x in [run,lumi,event])] = {'met':products["pfMet"][0].pt(),  'sumEt':products["pfMet"][0].sumEt(), 'metPhi':products["pfMet"][0].phi()}

commonKeys =  [val for val in res['53X'].keys() if val in res['73X'].keys()]
print "Have",len(commonKeys),"events in common"

import ROOT
sumEt = ROOT.TH2F('sumEt','sumEt',100,0,5000,100,0,5000)
met = ROOT.TH2F('met','met',100,0,500,100,0,500)
metPhi = ROOT.TH2F('met','met',100,-pi,pi,100,-pi,pi)
for k in commonKeys:
  if k in vetoedEvents:
    print "Vetoed",k
  else:
    met.Fill(res['53X'][k]['met'], res['73X'][k]['met'])
    sumEt.Fill(res['53X'][k]['sumEt'], res['73X'][k]['sumEt'])
    metPhi.Fill(res['53X'][k]['metPhi'], res['73X'][k]['metPhi'])

metPhi.GetXaxis().SetTitle("53X #phi(MET)")
metPhi.GetXaxis().SetLabelSize(0.04)
metPhi.GetYaxis().SetLabelSize(0.04)
metPhi.GetYaxis().SetTitle("73X #phi(MET)")

met.GetXaxis().SetTitle("53X MET")
met.GetXaxis().SetLabelSize(0.04)
met.GetYaxis().SetLabelSize(0.04)
met.GetYaxis().SetTitle("73X MET")
sumEt.GetXaxis().SetTitle("53X sumEt")
sumEt.GetYaxis().SetTitle("73X sumEt")
sumEt.GetYaxis().SetLabelSize(0.04)
sumEt.GetXaxis().SetLabelSize(0.04)
sumEt.GetXaxis().SetRangeUser(0,3000)
sumEt.GetYaxis().SetRangeUser(0,3000)

c1 = ROOT.TCanvas()
met.Draw('colz')
c1.Print('met.png')
c1.Print('met.pdf')
metPhi.Draw('colz')
c1.Print('metPhi.png')
c1.Print('metPhi.pdf')
sumEt.Draw('colz')
c1.Print('sumEt.png')
c1.Print('sumEt.pdf')


#  if run not in runs:
#    runs.append(run)
#    print "Added run",run
#  if run==208352:
#    nf = fileNames[events.fileIndex()]
#    if nf not in usedFiles:
#      print "Found file",run,nf
#      usedFiles.append(nf)

#  print ":".join([str(x) for x in [event, run, lumi]] ),products['pfMet'][0].pt(),  products['pfMet'][0].sumEt()
