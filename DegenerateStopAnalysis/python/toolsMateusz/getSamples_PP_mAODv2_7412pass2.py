#getSamples_PP_mAODv2_7412pass2.py
import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_mAODv2_7412pass2 import *
from Workspace.DegenerateStopAnalysis.tools.Sample import Sample, Samples

skim='presel'

mc_lumi   = 10000
data_lumi_unblinded = 135.21
data_lumi_blinded = 1547.74

#METDataOct05 = getChain(MET_Run2015D_05Oct2015_v1[skim],histname='')
#METDataBlind       = getChain(MET_Run2015D_PromptReco_v4[skim],histname='')
#METDataBlind.Add(METDataOct05)
#METDataUnblind = METDataBlind.CopyTree("run<=257599")

def getSamples(wtau=False, useHT=False, getData=False):
   S300_270 = getChain(T2DegStop_300_270[skim],histname='')
   S300_240FS = getChain(T2DegStop_300_240_FastSim[skim],histname='')
   S300_270FS = getChain(T2DegStop_300_270_FastSim[skim],histname='')
   S300_290FS = getChain(T2DegStop_300_290_FastSim[skim],histname='')
   T2tt300_270FS = getChain(T2tt_300_270_FastSim[skim],histname='')
   WJetsIncSample = getChain(WJetsInc[skim],histname='')
   WJetsHTSample = getChain(WJetsHT[skim],histname='')
   ZJetsHTSample = getChain(ZJetsHT[skim],histname='')
   WSample = WJetsHTSample if useHT else WJetsIncSample
   TTJetsIncSample = getChain(TTJetsInc[skim],histname='')
   QCDSample = getChain(QCD[skim],histname='')
   
   sampleDict = {
   'qcd':        {'tree':QCDSample,         'name':'QCD',             'color':ROOT.kViolet-5,    'isSignal':0,   'isData':0,   "lumi":mc_lumi},
   'z':          {'tree':ZJetsHTSample,     'name':'ZJets',           'color':ROOT.kSpring+10,   'isSignal':0,   'isData':0,   "lumi":mc_lumi},# ,'sumWeights':WJets[1] ,'xsec':20508.9*3},
   'tt':         {'tree':TTJetsIncSample,   'name':'TTJets',          'color':ROOT.kAzure-5,     'isSignal':0,   'isData':0,   "lumi":mc_lumi},
   'w':          {'tree':WJetsHTSample,     'name':'WJets',           'color':ROOT.kSpring-5,    'isSignal':0,   'isData':0,   "lumi":mc_lumi},# ,'sumWeights':WJets[1] ,'xsec':20508.9*3},
   "s30":        {'tree':S300_270,          'name':'S300_270',        'color':ROOT.kRed+1,       'isSignal':1,   'isData':0,   "lumi":mc_lumi},# ,'sumWeights':T2Deg[1] ,'xsec':8.51615},
   "s30FS":      {'tree':S300_270FS,        'name':'S300_270FS',      'color':ROOT.kOrange+8,    'isSignal':1,   'isData':0,   "lumi":mc_lumi,   "weight":"(weight*0.2647)"},# ,'sumWeights':T2Deg[1] ,'xsec':8.51615},
   "s10FS":      {'tree':S300_290FS,        'name':'S300_290FS',      'color':ROOT.kAzure+7,     'isSignal':1,   'isData':0,   "lumi":mc_lumi,   "weight":"(weight*0.2546)"},# ,'sumWeights':T2Deg[1] ,'xsec':8.51615},
   "s60FS":      {'tree':S300_240FS,        'name':'S300_240FS',      'color':ROOT.kMagenta-2,   'isSignal':1,   'isData':0,   "lumi":mc_lumi,   "weight":"(weight*0.3520)"},# ,'sumWeights':T2Deg[1] ,'xsec':8.51615},
   "t2tt30FS":   {'tree':T2tt300_270FS,     'name':'T2tt300_270FS',   'color':ROOT.kOrange-1,    'isSignal':1,   'isData':0,   "lumi":mc_lumi,   "weight":"(weight*0.2783)"} # ,'sumWeights':T2Deg[1] ,'xsec':8.51615},
   #"d":          {'tree':METDataUnblind     'name':"data",            'color':ROOT.kBlack,       'isSignal':0,   'isData':1,   'lumi': data_lumi_unblinded,   "weight":"(1)"},
   #"dblind":     {'tree':METDataBlind       'name':"dblind",          'color':ROOT.kBlack,       'isSignal':0,   'isData':1,   'lumi': data_lumi_blinded,     "weight":"(1)"}
   }
   
   if wtau:
       print "Creating a sample for the Tau and NonTau Components of WJets ... this might take some time"
       WTau=WSample.CopyTree("Sum$(abs(GenPart_pdgId)==15)>=1")
       WNoTau=WSample.CopyTree("Sum$(abs(GenPart_pdgId)==15)==0")
       sampleDict.update({
           'wtau':     {'tree':WTau,     'name':'WTau',     'color':ROOT.kSpring-2,   'isSignal':0,   'isData':0,   "lumi":mc_lumi},
           'wnotau':   {'tree':WNoTau,   'name':'WNoTau',   'color':ROOT.kSpring+2,   'isSignal':0,   'isData':0,   "lumi":mc_lumi} 
           })
   
   sampleDict2 = {}
   for samp in sampleDict:
     sampleDict2[samp]=Sample(**sampleDict[samp])
   samples = Samples(**sampleDict2)

   return samples
