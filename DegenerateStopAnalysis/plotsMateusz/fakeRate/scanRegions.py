# scanRegions.py 
# Scans events in regions 
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeDir
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeLine, newLine
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from pprint import pprint
from array import array
from math import pi, sqrt #cos, sin, sinh, log
from fakeRegions import regions, binning

parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "el")
parser.add_argument("--WP", dest = "WP",  help = "Working point", type = str, default = "loose")
parser.add_argument("--sample", dest = "sample",  help = "Sample", type = str, default = "w")
parser.add_argument("--region", dest = "reg",  help = "Measurement or application region", type = str, default = "application_sr1")
parser.add_argument("--category", dest = "category",  help = "Total/Prompt/Fake", type = str, default = "fakes")
parser.add_argument("--oneBin", help = "One bin", action = "store_true")
parser.add_argument("--save", help="Toggle save", action="store_true")
parser.add_argument("--verbose", dest="verbose",  help="Verbosity switch", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
lep = args.lep
WP = args.WP
sample = args.sample
reg = args.reg
category = args.category
oneBin = args.oneBin
save = args.save
verbose = args.verbose

#Samples
cmgPP = cmgTuplesPostProcessed()

if "measurement" in reg:
   skim = "oneLepGood"
   #samplesList = ["w", "tt", "qcd"]
elif "application" in reg:
   skim = "preIncLep"
   #samplesList = ["st", "vv", "qcd", "z", "dy", "tt", "w"]
   getData = False #NOTE: For now, do not plot data near SR
else:
   print "Region unknown. Exiting."
   sys.exit()

samplesList = [sample]

if getData and "measurement" in reg:
   samplesList.append("djetBlind")

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = getData)

print makeLine()
print "Using samples:"
newLine()
for s in samplesList:
   if s: print samples[s].name,":",s
   else:
      print "!!! Sample " + sample + " unavailable."
      sys.exit()

if lep == "el":    lepton = "Electron" #pdgId = "11"
elif lep == "mu":  lepton = "Muon" #pdgId = "13"
elif lep == "lep": lepton = "Lepton"
      
#Save
if save:
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation"%tag
  
   if oneBin: savedir += "/oneBin"

   savedir += "/%s/scanRegions/%s"%(reg, lepton)
 
   makeDir(savedir)
   
   suffix = "_%s_%s_%s"%(sample, WP, category)
   
selection = regions(reg, lep, oneBin = oneBin)
setEventListToChains(samples, samplesList, selection[reg])

print makeLine()
print "Using the following selection: \n",
pprint(selection)
print "\n",
print reg, "= \n",
pprint(selection[reg].fullList)
print makeLine()

index = selection['index']

region = {}

if reg:
   region['total'] = CutClass(reg, [
      ["WP", selection[WP]],
      #["noTau", selection['noTauLoose']],
      ], baseCut = selection[reg])
  
   region['prompt'] = CutClass(reg + "_prompt", [
      ["WP", selection[WP]],
      ["prompt", selection['promptLoose']],
      #["noTau", selection['noTauLoose']],
      ], baseCut = selection[reg])
   
   region['fakes'] = CutClass(reg + "_fakes", [
      ["WP", selection[WP]],
      ["fake", selection['fakeLoose']],
      #["noTau", selection['noTauLoose']],
      ], baseCut = selection[reg])

   cutString = region[category].combined

   #cutString += "&& abs(GenPart_pdgId) == 15"

else:
   cutString = ""

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

genCond = "(abs(GenPart_pdgId) == 15 && (abs(GenPart_motherId) == 24 || abs(GenPart_motherId) == 23 || (GenPart_motherId == -9999 && Iteration$ < 3)))"
dR = "(sqrt((GenPart_eta - LepGood_eta[{ind}])^2 + (GenPart_phi - LepGood_phi[{ind}])^2))".format(ind = index[WP])
#dR = "(deltaR(GenPart_eta, LepGood_eta[{ind}], GenPart_phi, LepGood_phi[{ind}]))".format(ind = index[WP])

dRmin = "MinIf$(%s,%s)"%(dR, genCond)

varExtra = [genCond, genCond2, dR, dRmin]
   
varGeneral = ["evt"]#, "weight", "puReweight", "nTauGood"]
varGenPart = ["pdgId", "pt", "eta", "phi", "motherId"]#, "motherIndex", "sourceId", "grandmotherId", "status", "isPromptHard"]
#varGenJet = ["pt","eta","phi"]
varLepGood = ["pdgId", "pt", "eta", "phi", "mcMatchId", "mcMatchAny", "mcMatchTau"] #"dxy", "dz", 
#varTauGood = ["pt", "eta"]

varGenPart = ["GenPart_"+x for x in varGenPart]
#varGenJet =  ["GenJet_"+x for x in varGenJet]
varLepGood = ["LepGood_"+x+"[%s]"%index[WP] for x in varLepGood]
#varTauGood = ["TauGood_"+x for x in varTauGood] #NOTE: adding these variables limits output of the TTree:Scan()

varGenPart.insert(0, 'nGenPart')
varLepGood.insert(0, 'nLepGood_{}_{}'.format(lep, WP).replace('tight', 'def'))

variables = ":".join(varGeneral+varGenPart+varLepGood+varExtra) #varGenJet+varTauGood

if verbose:
   print "Cut: ", cutString
   print "Variables: ", variables

t = samples[sample].tree

if save:
   t.SetScanField(0)
   t.GetPlayer().SetScanRedirect(True)
   t.GetPlayer().SetScanFileName(savedir + "/scan%s.txt"%suffix)

t.Scan(variables, cutString)
