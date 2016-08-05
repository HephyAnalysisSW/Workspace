import ROOT
import glob
import argparse
import sys
from Workspace.HEPHYPythonTools.helpers import getYieldFromChain # getChain, getPlotFromChain, getChunks
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeLine, makeDoubleLine
#from Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISpring16MiniAODv2_v1 import * #including sample_path and allComponents TODO: automatically get dir from here 
#from Workspace.DegenerateStopAnalysis.samples.cmgTuples.Data2016_v1_1 import *  #including sample_path [and sample_path_8012 for Run2016D] and allComponents TODO: automatically get dir from here
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.tools.getSamples_8011 import getSamples

#cmgDir = '/data/nrad/cmgTuples/8011_mAODv2_v1/RunIISpring16MiniAODv2'
#cmgDataDir = '/data/nrad/cmgTuples/8011_mAODv2_v1/RunIISpring16MiniAODv2'
#/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1
#/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1_Chunk_*/tree.root

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 1)
parser.add_argument("--skim", dest = "skim",  help = "Skim", type = str, default = "preIncLep")
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()

#Arguments
getData = args.getData
skim = args.skim

ppsDir = '/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8011_mAODv2_v1/80X_postProcessing_v6/analysisHephy_13TeV_2016_v0/step1' 

mc_path     = ppsDir + "/RunIISpring16MiniAODv2_v1"
signal_path = ppsDir + "/RunIISpring16MiniAODv2_v1"
data_path   = ppsDir + "/Data2016_v1_1"

cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)

samplesList = ["dy"]#, "vv", "st", "z", "dy", "w"] #"tt" is more complicated with lheHT skims 

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = getData)

if skim == "preIncLep": 
    # branches for preselection (scalars or vectors) must be included in readVar or readVectors
    metCut = "(met_pt>200)"
    leadingJet_pt = "((Max$(Jet_pt*(abs(Jet_eta)<2.4 && Jet_id) ) > 90 ) >=1)"
    HTCut = "(Sum$(Jet_pt*(Jet_pt>30 && abs(Jet_eta)<2.4 && (Jet_id)) ) >200)"

    skimString = "(%s)" % '&&'.join([metCut, leadingJet_pt, HTCut])

# lepton skimming
if skim == 'oneLep':
    skimString = " ((nLepGood >=1 && LepGood_pt[0] > 20) || (nLepOther >=1 && LepOther_pt[0] > 20))"

for samp in samplesList:
   nCMG = 0
   for bin in samples[samp].sample['bins']:
      if samples[samp].isData: 
         if "Run2016D" in bin:
            cmgPath = data_sample_path_8012 + "/" + bin + "/" + bin + "_Chunk*/tree.root"
         else:
            cmgPath = data_sample_path + "/" + bin + "/" + bin + "_Chunk*/tree.root"
      else:
         cmgPath = mc_sample_path + "/" + bin + "/" + bin + "_Chunk*/tree.root"

      files = glob.glob(cmgPath)
      
      t = ROOT.TChain("tree")
      
      for f in files:
         t.Add(f)

      nBin = getYieldFromChain(t, skimString, "1")

      print makeLine()
      print "# Events in bin ", bin, ": ", nBin 
      print makeLine()
      nCMG += nBin 
   
   nPPS = getYieldFromChain(samples[samp].tree, "1", "1")
  
   print makeDoubleLine() 
   print "Skim: ", skim
   print "Number of Events @ CMG: ", nCMG
   print "Number of Events @ PPS: ", nPPS 
   print makeDoubleLine() 
