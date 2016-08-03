import ROOT
import glob

from Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISpring16MiniAODv2_v1 import * 
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import * #cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.tools.getSamples_8011 import getSamples

#cmgDir = '/data/nrad/cmgTuples/8011_mAODv2_v1/RunIISpring16MiniAODv2'
#cmgDataDir = '/data/nrad/cmgTuples/8011_mAODv2_v1/RunIISpring16MiniAODv2'
#/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1
#/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1_Chunk_*/tree.root

ppsDir = '/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8011_mAODv2_v1/80X_postProcessing_v4/analysisHephy_13TeV_2016_v0/step1/' 

## most recent paths, can be replaced when initializing the cmgTuplesPostProcessed class
mc_path     = ppsDir + "/RunIISpring16MiniAODv2_v1"
signal_path = ppsDir + "/RunIISpring16MiniAODv2_v1"
data_path   = ppsDir + "/Data2016_v1_1"

getData = True

cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)

samplesList = ["qcd", "vv", "st", "z", "dy", "tt", "w"]

samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = getData)

if skimPreselect: 
    # branches for preselection (scalars or vectors) must be included in readVar or readVectors
    metCut = "(met_pt>200)"
    leadingJet_pt = "((Max$(Jet_pt*(abs(Jet_eta)<2.4 && Jet_id) ) > 90 ) >=1)"
    HTCut = "(Sum$(Jet_pt*(Jet_pt>30 && abs(Jet_eta)<2.4 && (Jet_id)) ) >200)"

    skimPreselectCondition = "(%s)" % '&&'.join([metCut, leadingJet_pt, HTCut])

# lepton skimming
if skimLepton == 'incLep':
    skimLeptonCondition = ''
elif skimLepton == 'oneLep':
    skimLeptonCondition = " ((nLepGood >=1 && LepGood_pt[0] > 20) || (nLepOther >=1 && LepOther_pt[0] > 20))"
