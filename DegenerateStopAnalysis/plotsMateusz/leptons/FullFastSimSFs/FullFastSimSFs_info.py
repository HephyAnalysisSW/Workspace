# FullFastSimSFs_info.py
# Mateusz Zarucki 2016

import ROOT
import os, sys
import copy
import math
import argparse
import pickle
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, makeSimpleLatexTable, makeDir, setup_style
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.tools.Sample import Sample
from Workspace.DegenerateStopAnalysis.cmgPostProcessing import cmgObjectSelection
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters
from Workspace.HEPHYPythonTools import u_float
from array import array
from math import pi, sqrt #cos, sin, sinh, log

ROOT.gStyle.SetOptStat(0) #1111 adds histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

#Input options
def getParser(script):
   parser = argparse.ArgumentParser(description="Input options")
   parser.add_argument("--lep", dest = "lep", help = "Lepton", type = str, default = "mu")
   parser.add_argument("--sample", dest = "sample", help = "Sample", type = str, default = "allFullSim")
   parser.add_argument("--standardBins", dest = "standardBins",  help = "Standard binning", type = int, default = 0)
   parser.add_argument("--varBins", dest = "varBins",  help = "Variable bin size", type = int, default = 0)
   parser.add_argument("--applyWeights", dest = "applyWeights",  help = "Apply weights", type = int, default = 0)
   parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
   parser.add_argument("--save", dest = "save",  help = "Toggle save", type=int, default = 1)
   parser.add_argument("--verbose", dest="verbose", help="Verbosity switch", type=int, default = 1)

   if 'factorised' in script:
      parser.add_argument("--base",     dest = "base",  help = "Base cut", type = str, default = "ID")
      parser.add_argument("--variable", dest = "variable",  help = "Variable", type = str, default = "HI+IP")

   args = parser.parse_args()

   if not len(sys.argv) > 1:
      print makeLine()
      print "No arguments given. Using default settings."
      print makeLine()

   #if args.verbose:
   #   print makeLine()
   #   print "Returning arguments for script:", script
   #   print makeLine()

   return args

def getInfo(script, args):

   scriptTag = script.replace('FullFastSimSFs_', '').replace('.py','')

   # Arguments
   lep =                 args['lep'] if                 'lep'                 in args.keys() else None
   sample =              args['sample'] if              'sample'              in args.keys() else None
   variable =            args['variable'] if            'variable'            in args.keys() else None
   base =                args['base'] if                'base'                in args.keys() else None
   varBins =             args['varBins'] if             'varBins'             in args.keys() else None
   standardBins =        args['standardBins'] if        'standardBins'        in args.keys() else None
   logy =                args['logy'] if                'logy'                in args.keys() else None
   save =                args['save'] if                'save'                in args.keys() else None
   verbose =             args['verbose'] if             'verbose'             in args.keys() else None

   if lep == "el":
      lepton = "Electron"
      pdgId = "11"
   elif lep == "mu":
      pdgId = "13"
      lepton = "Muon"
   
   #Samples
   cmgPP = cmgTuplesPostProcessed()
   
   #samplesList = ["s30_FullSim", "s20_FullSim", "s50_FullSim"]
   samplesList = [sample]

   samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = True, useHT = True, getData = 0, def_weights = [])
   
   if 'all' in sample: 
      allFastSim = ROOT.TChain("Events", "Events")
      for s in samples.sigList():
         if 't2tt' in s and not 't2ttold' in s:
            if 'global' in scriptTag and s not in ['t2tt275_205', 't2tt350_330', 't2tt400_350']: continue
            allFastSim.Add(samples[s].tree)
   
   #samples['allFastSim'] = samples[samples.sigList()[0]].copy()
   #samples['allFastSim']['tree'] = allFastSim 
   #samples['allFastSim']['name'] = "allFastSim" 
   #samples['allFastSim']['bins'] = []
   #samples['allFastSim'] = Sample(samples['allFastSim'])
 
   #Save
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      saveTag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
      baseDir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/FullFastSimSFs"%saveTag
     
      savedir = baseDir
      savedir += "/" + sample
      savedir += "/" + scriptTag
      
      suffix = "_" + lep
      
      if base and variable:
         savedir += "/%s_base/%s"%(base, variable)
         suffix  += "_" + variable
      
      if standardBins: savedir += "/standardBins"
      else:            savedir += "/myBins"
      
      if varBins: savedir += "/varBins"
      else:       savedir += "/fixedBins"
    
      makeDir(savedir + "/root")
      makeDir(savedir + "/pdf")

   bins = getBinning(lep, varBins = varBins, standardBins = standardBins)

   # gen filter efficiencies
   genFilterEffs = {'FullSim_275_205':0.37852336637702982, 'FullSim_350_330':0.42898240336017424, 'FullSim_400_350':0.46153974794637842}
   genFilterEffs['allFullSim'] = (0.37852336637702982+0.42898240336017424+0.46153974794637842)/3

   ret = {}
   ret['lepton'] =  lepton
   ret['samples'] = samples
   ret['bins'] =    bins
   ret['genFilterEffs'] = genFilterEffs
   if 'all' in sample: 
      ret['allFastSim'] = allFastSim

   if save:
      ret['baseDir'] = baseDir
      ret['saveTag'] = saveTag
      ret['savedir'] = savedir
      ret['suffix'] =  suffix

   return ret

# Binning
def getBinning(lep, varBins = False, standardBins = False, xmax = 200):
   if lep == 'el':   etaAcc = 2.5 #eta acceptance
   elif lep == 'mu': etaAcc = 2.4

   bins = {}
   if not varBins:
      if standardBins:
         bins = {'pt':[20, 0, xmax], 'eta':[int(etaAcc*10), 0, etaAcc]}
      else: 
         bins = {'pt':[int(xmax/10), 0, xmax], 'eta':[int(etaAcc*10), 0, etaAcc], 'mt':[int(xmax/10), 0, xmax]}
   else: # variable bin size
      if standardBins:
         bins = {'pt': range(0,50,10) + range(50,200+150,150)}
      else: 
         bins['pt'] = [0, 3.5, 5, 12, 20, 30, xmax+5]
   
      if lep == 'mu':
         bins['eta'] = [0, 0.9, 1.2, 2.1, 2.4]
      elif lep == 'el':
         bins['eta'] = [0, 1.4442, 1.556, 2.5]
      else:
         bins['eta'] = [0, 1.5, etaAcc]
   
   return bins
