# scanFakeRegions.py
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
import copy
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.HEPHYPythonTools.helpers import getYieldFromChain
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeDir
from Workspace.DegenerateStopAnalysis.tools.mvaTools import getMVATrees
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from pprint import pprint
from array import array
from math import pi, sqrt #cos, sin, sinh, log
from fakeRegions import fakeRegions, fakeBinning

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--sample", dest = "sample",  help = "Sample", type = str, default = "qcd")
parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "el")
parser.add_argument("--region", dest = "region",  help = "Measurement or application region", type = str, default = "application_sr1")
parser.add_argument("--WP", dest = "WP",  help = "Loose or tight WP", type = str, default = "tight")
parser.add_argument("--category", dest = "category",  help = "Total/Prompt/Fake", type = str, default = "total")
parser.add_argument("--ptBin", dest = "ptBin",  help = "(lowBin,highBin)", type = str, nargs = "+", default = None)
parser.add_argument("--mva", help = "MVA", action = "store_true")
parser.add_argument("--looseNotTight", help = "Loose-not-tight CR", action = "store_true")
parser.add_argument("--doYields", help = "Calculate yields", action = "store_true")
parser.add_argument("--getData", dest = "getData",  help = "Get data", type = int, default = 0)
parser.add_argument("--varBins", help = "Variable bin size", action = "store_true")
parser.add_argument("--save", dest="save",  help="Toggle save", action="store_true", default=False)
parser.add_argument("--verbose", dest="verbose",  help="Verbosity switch", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch mode", action="store_true", default=False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
sample = args.sample
lep = args.lep
region = args.region
WP = args.WP
category = args.category
ptBin = args.ptBin
mva = args.mva
looseNotTight = args.looseNotTight
doYields = args.doYields
getData = args.getData
varBins = args.varBins
save = args.save
verbose = args.verbose

#Samples
cmgPP = cmgTuplesPostProcessed()

samplesList = [sample]
#samplesList = ["w", "tt_1l", "tt_2l", "qcd", "st", "vv", "z", "dy"]

if "measurement" in region:
   skim = "oneLepGood"
   fom = "RATIO"
   mva = False
   if region == "measurement2":
      fakeTauVeto = False

   if getData:
      if region == "measurement1":
         dataSample = 'djetBlind'

      elif region == "measurement2":
         samplesList.reverse()
         if lep == "el":
            dataSample = 'd1elBlind'
         elif lep == "mu":
            dataSample = 'd1muBlind'
         else:
            print "Wrong lepton input for measurement region 2. Exiting."
            sys.exit()

      samplesList.append(dataSample)

elif "application" in region:
   skim = "preIncLep"
   samplesList.reverse()
   getData = False #NOTE: For now, do not plot data near SR
   fom = False

if region == "measurement2":
   samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = False, def_weights = [])
   if getData: samples.update(getSamples(cmgPP = cmgPP, skim = 'lt120', sampleList = [dataSample], scan = False, useHT = True, getData = True, def_weights = []))
else:
   samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = False, useHT = True, getData = getData, def_weights = [])

# Gets MVA friend trees
if mva:
   getMVATrees(samples, mvaIdIndex = 'Sum$((mva_methodId=={mvaId}) * Iteration$)'.format(mvaId = '30'))

if verbose:
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

selection = fakeRegions(samples, region, lep, WP, highPtBin = False, mva = mva)
setEventListToChains(samples, samplesList, selection['kinematic'][region])

if verbose:
   print makeLine()
   print "Using the following selection: \n",
   pprint(selection)
   print "\n",
   print makeLine()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation"%tag

   if mva: savedir += "/%s_id%s_bdt%s"%(region, selection['mvaId'], selection['bdtcut'])
   else:   savedir += "/%s"%region
 
   savedir += "/scanFakeRegions"
 
   if ptBin: savedir += "/ptBin_%s_%s"%(ptBin[0], ptBin[1])
   else:     savedir += "/allBins"

   savedir += "/%s/%s"%(lepton, category)

   if looseNotTight: savedir += "/L!T"
   else: savedir += "/Loose"
   
   suffix = "_%s_%s_%s"%(region, lep, WP)
   suffix2 = "%s_%s"%(suffix, sample)
  
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

## Signal region
#region = {'SR':{}, 'looseCR':{}}
#
#region['SR']['total'] =  [selection['tight']['cuts'], selection['regDef']] 
#region['SR']['prompt'] = [selection['tight']['cuts'], selection['regDef'] + '_prompt'] 
#region['SR']['fake'] =   [selection['tight']['cuts'], selection['regDef'] + '_fake'] 
#
## Loose (not-Tight) CR
#if looseNotTight:
#   notTight = "_notTight"
#else:
#   notTight = ""
#
#region['looseCR']['total'] =  [selection['loose']['cuts'], selection['regDef'] + notTight] 
#region['looseCR']['prompt'] = [selection['loose']['cuts'], selection['regDef'] + notTight + '_prompt'] 
#region['looseCR']['fake'] =   [selection['loose']['cuts'], selection['regDef'] + notTight + '_fake' ] 

baseCutString = selection[WP][region][sample][0] 

weight = selection[WP][region][sample][1] 

if category == "total":
   cutString = baseCutString
elif category in ["prompt", "fake"]:
   cutString = combineCuts(baseCutString, selection[WP]['cuts'].cuts_dict[category]['cut'])

# Loose (not-Tight) CR
if WP == "loose" and looseNotTight:
   cutString = combineCuts(cutString, selection[WP]['cuts'].cuts_dict['notTight']['cut'])

if ptBin:
   lepPt = selection[WP]['cuts'].vars_dict_format['lepPt']
   cutString = combineCuts(cutString, "({lepPt} > {low}) && ({lepPt} < {high})".format(lepPt = lepPt, low = ptBin[0], high = ptBin[1]))

lepInd = selection[WP]['lepIndex']

# Scan
varGeneral = ["evt", weight, "nGenPart"]
varGenPart = ["pdgId", "pt", "eta", "phi", "motherId"]#, "motherIndex", "sourceId", "grandmotherId", "status", "isPromptHard"]
#varGenJet = ["pt","eta","phi"]
varLepGood = ["pdgId", "pt", "eta", "phi", "mt", "mcMatchId", "mcMatchAny", "mcMatchTau"] #"dxy", "dz", 
#varTauGood = ["pt", "eta"]

varGenPart = ["GenPart_"+x for x in varGenPart]
#varGenJet =  ["GenJet_"+x for x in varGenJet]
varLepGood = ["LepGood_%s[%s]"%(x,lepInd) for x in varLepGood]
#varTauGood = ["TauGood_"+x for x in varTauGood] #NOTE: adding these variables limits output of the TTree:Scan()

varExtra = ["met_pt", "met_phi", "met_genPt", "met_genPhi"]# "nJet_basJet_def"]
#varGenPart.insert(0, 'nGenPart')
#varLepGood.insert(0, 'nLepGood_{}_{}'.format(lep, WP).replace('tight', 'def'))

variables = ":".join(varGeneral+varGenPart+varLepGood+varExtra) #varGenJet+varTauGood

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
   t.GetPlayer().SetScanFileName(savedir + "/scan%s.txt"%suffix2)

t.Scan(variables, cutString)

if doYields:

   yld, err =  getYieldFromChain(samples[sample].tree, cutString, weight = weight, returnError = True)
   
   if verbose:
      print makeLine() 
      print "Sample: ", sample
      print "Yield: ", yld, "+-", err
      print makeLine() 
  
   if save:
      yieldFile = "%s/fakeYields%s.txt"%(savedir, suffix) 
      if not os.path.isfile(yieldFile):
         outfile = open(yieldFile, "w")
         outfile.write("Fake Estimation Yields in %s\n"%region.title())
         outfile.write("Sample             Yield\n")

      with open(yieldFile, "a") as outfile:
         outfile.write(sample.ljust(10) + "%.2f+-%.2f\n"%(yld,err))
 
## Yields 
#if doYields:
#   yields = {'SR':{}, 'looseCR':{}}
#
#   for x in yields: 
#      yields[x]['total'] =  Yields(samples, samplesList, cutInst = None, cuts = region[x]['total'],  cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
#      yields[x]['prompt'] = Yields(samples, samplesList, cutInst = None, cuts = region[x]['prompt'], cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
#      yields[x]['fake'] =   Yields(samples, samplesList, cutInst = None, cuts = region[x]['fake'],   cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
#
#   if save:
#      if not os.path.isfile("%s/fakeYields_%s.txt"%(savedir, suffix)):
#         outfile = open("%s/fakeYields_%s.txt"%(savedir, suffix), "w")
#         outfile.write("Fake Estimation Yields in %s\n"%region.title())
#         outfile.write("Sample      Loose CR: Total         Loose CR: Prompt          Loose CR: Fakes          SR: Total              SR: Prompt               SR: Fakes\n") 
#
#      yieldsList = samplesList[:]
#      yieldsList.append('Total')
#
#      with open("%s/fakeYields_%s.txt"%(savedir, suffix), "a") as outfile:
#        for samp in yieldsList:
#            outfile.write(samp.ljust(10) +\
#            str(yields['looseCR']['total'].yieldDictFull[samp][selection['regDef'] + notTight].round(2)).ljust(25) +\
#            str(yields['looseCR']['prompt'].yieldDictFull[samp][selection['regDef'] + notTight + '_prompt'].round(2)).ljust(25) +\
#            str(yields['looseCR']['fake'].yieldDictFull[samp][selection['regDef'] + notTight + '_fake'].round(2)).ljust(25) +\
#            str(yields['SR']['total'].yieldDictFull[samp][selection['regDef']].round(2)).ljust(25) +\
#            str(yields['SR']['prompt'].yieldDictFull[samp][selection['regDef'] + '_prompt'].round(2)).ljust(25) +\
#            str(yields['SR']['fake'].yieldDictFull[samp][selection['regDef'] + '_fake'].round(2)) + "\n")# .ljust(18) +\

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

