from Workspace.DegenerateStopAnalysis.navidPlotTools import *

import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks

#from Workspace.HEPHYPythonTools.helpers import getChunksFromNFS, getChunksFromDPM, getChunks
#from Workspace.DegenerateStopAnalysis.cmgTuples_v1_Phys14 import *

import os
import math
tableDir="/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/postProcessed_v4/tables/"

t = ROOT.TChain("tree")
#t.Add("/afs/cern.ch/user/n/nrad/CMSSW/CMSSW_7_2_3/src/CMGTools/TTHAnalysis/cfg/sync/T2DegStop_300_270/treeProducerSusySingleLepton/tree.root")
t.Add("/afs/cern.ch/work/n/nrad/delme/CMSSW_7_2_3/src/CMGTools/TTHAnalysis/cfg/sync/T2DegStop_300_270/treeProducerSusySingleLepton/tree.root")
weight= 4000*8.5161504/t.GetEntries()

sampleDict= {
          'T2Deg': {'tree':t    , "weight":"(1)", 'color':31          ,'lineColor':1   , 'isSignal':1 , 'isData':0       }
            }



syncCutList=[
      #["stCut"," (nLepGood[0]+met_pt > 200)"],
      ["noCut","(1)"],
      ["nMuon==1","(nLepGood==1)&&(abs(LepGood_pdgId[0])==13)"],
      #["dxy0.02 dz0.5","(abs(LepGood_dxy[0])<0.02)&&(abs(LepGood_dz[0])<0.5)"],
      ["pt30 eta2.1","(LepGood_pt[0]<30.)&&(abs(LepGood_eta[0]<2.1))"],
      ["charge","LepGood_charge[0]<0."],
      ["relIso","LepGood_relIso03[0]<0.2"],
      ["met>200","met_pt>200"],
      ["nJet25==2","nJet25==2"],
      ["nBJetLoose25>0","nBJetLoose25>0"],
      ["jetPt>110","Jet_pt[0]>110."],
      #["isrJet","isrJet_pt[0]>300."],
	]

syncCutFlow=makeCutFlowList(syncCutList)

if 0:
  makeTableFromYieldDict(sampleDict,syncCutList,output="sync",saveDir=tableDir)
