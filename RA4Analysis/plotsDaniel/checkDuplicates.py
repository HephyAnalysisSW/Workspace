import ROOT
import os, sys, copy
import pickle, operator
from glob import glob
from Workspace.HEPHYPythonTools.helpers import *


checkChunks = '/data/dspitzbart/cmgTuples/Run2016B-PromptReco-v2/cmgTuples_SingleMuon_Run2016B-PromptReco-v2_heppy/cmgTuples_SingleMuon_Run2016B-PromptReco-v2_heppy_Chunk*'+'/tree.root'
#checkChunks = '/data/easilar/cmgTuples/Run2016B-PromptReco-v2/cmgTuples_SingleElectron_Run2016B-PromptReco-v2_heppy/cmgTuples_SingleElectron_Run2016B-PromptReco-v2_heppy_Chunk*'+'/tree.root'
#checkChunks = '/data/dspitzbart/cmgTuples/RunIISpring16MiniAODv2/cmgTuples_MC25ns_1l_08062016_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1_MC25ns/cmgTuples_MC25ns_1l_08062016_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1_MC25ns_Chunk*'+'/tree.root'

#checkChunks = '/data/dspitzbart/cmgTuples/RunIISpring16MiniAODv2/cmgTuples_MC25ns_1l_08062016_TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1_MC25ns/cmgTuples_MC25ns_1l_08062016_TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1_MC25ns_Chunk*'+'/tree.root'

allChunks = glob(checkChunks)

baselineCut = 'nJet40>7'

evtRunLumiLists = {}

print
print 'Checking Chunks of directory:'
print checkChunks
print
print


for ic,chunk in enumerate(allChunks):
  evtRunLumiLists[ic] = []
  #print
  #print 'Checking Chunk #',ic+1
  c = ROOT.TChain('tree')
  c.Add(chunk)
  c.Draw('>>eList',baselineCut)#insert 'weight*('+
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  if number_events>0:
    print
    print 'Checking Chunk #',ic+1
    print "Looping over " + str(number_events) + " events"
  #Event Loop starts here
  for i in range(number_events):
    if i>0 and (i%10000)==0:
      print "Done with ",i
    c.GetEntry(elist.GetEntry(i))
    evt   = int(getVarValue(c,"evt"))
    run   = int(getVarValue(c,"run"))
    lumi  = int(getVarValue(c,"lumi"))
    a = (evt,run,lumi)
    
    for l in evtRunLumiLists:
      if a in evtRunLumiLists[l]:
        print 'Found duplicate from chunk',l+1, '##################################################'
    print a
    evtRunLumiLists[ic].append(a)
      


  

