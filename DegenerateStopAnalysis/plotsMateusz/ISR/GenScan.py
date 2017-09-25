# GenScan.py
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
import copy
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeSimpleLatexTable, makeDir, makeLegend
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters, lumis
#from Workspace.DegenerateStopAnalysis.tools.colors import colors
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
#from Workspace.DegenerateStopAnalysis.tools.mvaTools import getMVATrees
from Workspace.HEPHYPythonTools import u_float
from pprint import pprint
from array import array
from math import pi, sqrt

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--sample", dest = "sample", help = "Sample", type = str, default = "tt_1l")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 0)
parser.add_argument("--getSignal", dest = "getSignal",  help = "Get signal samples", type = int, default = 0)
parser.add_argument("--genISR", dest = "genISR",  help = "Generated ISR", type = str, default = "")
parser.add_argument("--doControlPlots", dest = "doControlPlots",  help = "Do control plots", type = int, default = 1)
parser.add_argument("--region", dest = "region",  help = "Region", type = str, default = "none")
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("--verbose", dest = "verbose",  help = "Verbosity switch", type = int, default = 0)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
sample =         args.sample
getData =        args.getData
getSignal =      args.getSignal
genISR =         args.genISR
doControlPlots = args.doControlPlots
region =         args.region
logy =           args.logy
save =           args.save
verbose =        args.verbose

if verbose:
   print makeDoubleLine()
   print "Running ISR script"
   print makeDoubleLine()

#Samples
cmgPP = cmgTuplesPostProcessed()

samplesList = [sample]
#samplesList = ["s30_FullSim", "s20_FullSim", "s50_FullSim"]
#samplesList = ["st", "vv", "qcd", "dy5to50", "dy", "z", "tt_2l", "tt_1l", "w"]

if getData:
   data = "dblind"
   samplesList.append(data)

samples = getSamples(cmgPP = cmgPP, skim = 'met200', sampleList = samplesList, scan = getSignal, useHT = True, getData = getData, def_weights = [])
#samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = getSignal, useHT = True, getData = getData, def_weights = [])


if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else:
         print "!!! Sample " + sample + " unavailable."
         sys.exit()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/ISR/GenScans"%tag

   suff = "_" + sample

   if genISR:
      suff += "_GenJets"
      #savedir += "/GenJets"
   else:
      suff += "_RecoJets"
      #savedir += "/RecoJets"

   suff += "_" + region

   #savedir += "/" + region

   makeDir(savedir)

if 'all' in sample:

   from Workspace.DegenerateStopAnalysis.tools.Sample import Sample, Samples

   sampleDict = {}

   allSignal = ROOT.TChain("Events", "Events")
   for s in samples.sigList():
      if 't2tt' in s and not 't2ttold' in s:
         allSignal.Add(samples[s].tree)

   sampleDict.update({
      'allSignal':{'name':'allSignal', 'sample':{'dir':samples[samples.keys()[0]].dir}, 'tree':allSignal, 'color':ROOT.kRed, 'isSignal':3 , 'isData':0, 'lumi':lumis["MC_lumi"]},
   })

   sampleDict2 = {}
   sampleDict2['allSignal'] = Sample(**sampleDict['allSignal'])
   samples = Samples(**sampleDict2)

cuts_weights = CutsWeights(samples, cutWeightOptions)

# N-1 
reg = cuts_weights.cuts.removeCut(region, 'ISR100')
if reg != region: isrPtInc = '_no_ISR100'
else: isrPtInc = ''

var = {}

if genISR:
   trueISR = 'trueGenISR'
   var['pt'] = 'GenIsrPt'
   if doControlPlots:
      var['recoil'] = 'GenISR_Recoil'
      var['dRmin'] =  'GenISR_dRmin'
      var['pdgId'] =  'GenISR_pdgId'
else:
   trueISR = 'trueISR'
   var['pt'] = 'isrPt'
   if doControlPlots:
      var['recoil'] =         'ISR_recoil'
      var['dRmin'] =          'ISR_dRmin'
      var['pdgId'] =          'ISR_pdgId'
      var['mcFlavour'] =      'ISR_mcFlavour'
      var['partonFlavour'] =  'ISR_partonFlavour'
      var['mcMatchFlav'] =    'ISR_mcMatchFlav'
      var['partonId'] =       'ISR_partonId'
      var['partonMotherId'] = 'ISR_partonMotherId'
      var['qgl'] =            'ISR_qgl'

cuts_weights.cuts.addCut(region + isrPtInc, "ISRinEvt")
isrInEvt = "_plus_ISRinEvt"

# True ISR
cuts_weights.cuts.addCut(region + isrPtInc + isrInEvt, trueISR)
trueISRcutName = '_plus_' + trueISR

if not genISR:
   cuts_weights.cuts.addCut(region + isrPtInc + isrInEvt, "ISRfromGluon")

cuts_weights.cuts._update(reset = False)
cuts_weights._update()

cutString = cuts_weights.cuts_weights[region + isrPtInc + isrInEvt][sample][0]

# Scan
varGeneral = ["evt", "nGenPart"]
varGenPart = ["motherId", "motherIndex", "pdgId", "pt", "eta", "phi", "sourceId", "grandmotherId", "status", "isPromptHard"]
varJet =    ["pt","eta","phi"]

if not genISR:
   varJet.extend(['mcFlavour', 'partonFlavour', 'partonId', 'partonMotherId', 'hadronFlavour', 'mcMatchId', 'mcMatchFlav']) # 'nLeptons'

varGenPart = ["GenPart_"+x for x in varGenPart]
varJet =  [genISR+"Jet_"+x for x in varJet]

varExtra = [cutString]
#varExtra = ["met_pt", "met_phi", "met_genPt", "met_genPhi"]# "nJet_basJet_def"]
#varGenPart.insert(0, 'nGenPart')

variables = ":".join(varGeneral+varGenPart+varJet+varExtra)

if verbose:
   print makeLine()
   print "Cut: ", cutString
   print makeLine()
   print "Variables: ", variables
   print makeLine()

t = samples[sample].tree

if save:
   t.SetScanField(0)
   t.GetPlayer().SetScanRedirect(True)
   t.GetPlayer().SetScanFileName(savedir + "/GenScan%s.txt"%suff)

t.Scan(variables, "1")

# GenPart variables
# nGenPart nGenPart/I : 0 at: 0x4fbf7b0
# GenPart_motherId  pdgId of the mother of the particle for Hard scattering particles, with ancestry and links : 0 at: 0x4fc3dd0
# GenPart_grandmotherId   pdgId of the grandmother of the particle for Hard scattering particles, with ancestry and links : 0 at: 0x4fc4450
# GenPart_sourceId  origin of the particle (heaviest ancestor): 6=t, 25=h, 23/24=W/Z for Hard scattering particles, with ancestry and links : 0 at: 0x4facaa0
# GenPart_charge charge for Hard scattering particles, with ancestry and links : 0 at: 0x4fad1a0
# GenPart_status status for Hard scattering particles, with ancestry and links : 0 at: 0x4fc1d00
# GenPart_isPromptHard isPromptHard for Hard scattering particles, with ancestry and links : 0 at: 0x4fc2330
# GenPart_pdgId  pdgId for Hard scattering particles, with ancestry and links : 0 at: 0x4faad20
# GenPart_pt  pt for Hard scattering particles, with ancestry and links : 0 at: 0x4fab380
# GenPart_eta eta for Hard scattering particles, with ancestry and links : 0 at: 0x4ce9c50
# GenPart_phi phi for Hard scattering particles, with ancestry and links : 0 at: 0x4cea2b0
# GenPart_mass   mass for Hard scattering particles, with ancestry and links : 0 at: 0x4fbe200
# GenPart_motherIndex  index of the mother in the generatorSummary for Hard scattering particles, with ancestry and links : 0 at: 0x4fbe860
