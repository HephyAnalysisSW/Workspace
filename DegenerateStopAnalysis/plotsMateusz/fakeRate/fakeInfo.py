# fakeInfo.py
# Common arguments, samples, savedirs for fake rate estimation scripts
# Mateusz Zarucki 2017

import ROOT
import os, sys
import argparse
import pickle
import copy
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeDir
from Workspace.DegenerateStopAnalysis.tools.colors import colors
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.tools.mvaTools import getMVATrees
from Workspace.HEPHYPythonTools.helpers import getYieldFromChain
from Workspace.HEPHYPythonTools import u_float
from pprint import pprint
from array import array
from math import pi, sqrt
from fakeCuts import fakeCuts

def fakeParser(script):
   parser = argparse.ArgumentParser(description="Input options")
   parser.add_argument("--lep",         help = "Lepton", type = str, default = "el")
   parser.add_argument("--region",      help = "Measurement or application region", dest = "region", type = str, default = "application_sr1")
   parser.add_argument("--mva",         help = "MVA", action = "store_true")
   parser.add_argument("--getData",     help = "Get data", action = "store_true")
   parser.add_argument("--considerFakeTaus", help = "Veto fakes from taus", dest = "considerFakeTaus", type = int, default = 1)
   parser.add_argument("--doPlots",     help = "Plot", dest = "doPlots", type = int, default = 1)
   parser.add_argument("--doYields",    help = "Calculate yields", action = "store_true")
   parser.add_argument("--varBins",     help = "Variable bin size", type = int, default = 1)
   parser.add_argument("--logy",        help = "Toggle logy", dest = "logy", action = "store_true")
   parser.add_argument("--save",        help="Toggle save", dest="save", type=int, default=1)
   parser.add_argument("--verbose",     help="Verbosity switch", action = "store_true")
   parser.add_argument("--VR",      help = "Validation region", type = str, default = None, choices = ["CT200", "EVR1", "EVR2"])
   parser.add_argument("--fakeRateMeasurement", dest = "fakeRateMeasurement", help = "Source of fake rate measurement (data-EWK or MC)", type = str, default = "")

   if script in ["plotFakeRegions.py", "fakesEstimation.py", "fakesUncertainties.py", "scanFakeRegions.py"]:
      parser.add_argument("--looseNotTight", help = "Loose-not-tight CR", action = "store_true")
      parser.add_argument("--ptBin", help = "(lowBin,highBin)", dest = "ptBin",  type = str, nargs = "+", default = None)
      parser.add_argument("--invAntiQCD", help = "Invert anti-QCD cut",  action = "store_true")
      parser.add_argument("--noAntiQCD",  help = "Remove anti-QCD cut",  action = "store_true")
      
      if script == "plotFakeRegions.py" or script == "scanFakeRegions.py":
         parser.add_argument("--WP", dest = "WP", help = "Loose or Tight WP", type = str, default = "loose")
      
   if script == "fakeRate.py" or script == "scanFakeRegions.py":
      parser.add_argument("--sample", dest = "sample", help = "Sample", type = str, default = "w")
      if script == "fakeRate.py": 
         parser.add_argument("--noWeights", help = "Sample", action = "store_true")
         parser.add_argument("--do2D", dest = "do2D", help = "2D fake rate", action = "store_true")
      elif script == "scanFakeRegions.py":
         parser.add_argument("--category", dest = "category", help = "Total/Prompt/Fake", type = str, default = "total")
   
   if script in ["plotFakeRegions.py", "fakesEstimation.py", "fakesUncertainties.py", "simulFakesUnc.py"]:
      parser.add_argument("--doControlPlots", help = "Additional plots of regions", action = "store_true")
      if script in ["fakesEstimation.py", "fakesUncertainties.py", "simulFakesUnc.py"]:
         parser.add_argument("--measurementRegion", dest = "measurementRegion", help = "Measurement region", type = str, default = "measurement1")
         parser.add_argument("--closureDef", dest = "closureDef", help = "Definition of closure (standard vs ratio)", type = str, default = "standard")
      
   
   if "simulFakeRate" in script:
      parser.add_argument("--variable", dest = "variable", help = "Plotting variable", type = str, default = "pt")
  
   args = parser.parse_args()
   
   if not len(sys.argv) > 1:
      print makeLine()
      print "No arguments given. Using default settings."
      print makeLine()
   
   if args.verbose:
      print makeLine() 
      print "Returning arguments for script:", script
      print makeLine() 
 
   return args

def fakeInfo(script, args):
   
   # Arguments
   lep =                 args['lep'] if                 'lep'                 in args.keys() else None
   region =              args['region'] if              'region'              in args.keys() else None
   mva =                 args['mva'] if                 'mva'                 in args.keys() else None
   getData =             args['getData'] if             'getData'             in args.keys() else None
   considerFakeTaus =    args['considerFakeTaus'] if    'considerFakeTaus'    in args.keys() else None
   doYields =            args['doYields'] if            'doYields'            in args.keys() else None
   varBins =             args['varBins'] if             'varBins'             in args.keys() else None
   logy =                args['logy'] if                'logy'                in args.keys() else None
   save =                args['save'] if                'save'                in args.keys() else None
   verbose =             args['verbose'] if             'verbose'             in args.keys() else None
   
   looseNotTight =       args['looseNotTight'] if       'looseNotTight'       in args.keys() else None
   ptBin =               args['ptBin'] if               'ptBin'               in args.keys() else None
   VR =                  args['VR'] if                  'VR'                  in args.keys() else None
   invAntiQCD =          args['invAntiQCD'] if          'invAntiQCD'          in args.keys() else None
   noAntiQCD =           args['noAntiQCD'] if           'noAntiQCD'           in args.keys() else None
   
   WP =                  args['WP'] if                  'WP'                  in args.keys() else None
   sample =              args['sample'] if              'sample'              in args.keys() else None
   fakeRateMeasurement = args['fakeRateMeasurement'] if 'fakeRateMeasurement' in args.keys() else None
   measurementRegion =   args['measurementRegion'] if   'measurementRegion'   in args.keys() else None
   
   if verbose:
      print makeLine() 
      print "Getting samples, cut-strings and save directories for:", script
      print "Arguments:", args
      print makeLine() 

   if script == "fakeRate.py" and fakeRateMeasurement and not "measurement" in region:
      print "Fake rate measurement only in measurement region. Exiting."
      sys.exit()

   # Sets TDR style
   if script == "fakesEstimation.py" and not "application" in region:
      print "Region for estimation should be an application region. Exiting."
      sys.exit()

   # Samples
   cmgPP = cmgTuplesPostProcessed()
   
   if script == "fakeRate.py" and not fakeRateMeasurement:
      samplesList = []
   elif script == "scanFakeRegions.py":
      samplesList = [sample]
   elif "simul" in script:
      samplesList = ["st"]
   else:
      samplesList = ["st", "vv", "qcd", "dy", "z", "tt_2l", "tt_1l", "w"]
 
   dataset = None

   if "measurement" in region:
      mva = False
      if "measurement1" in region:
         skim = 'oneLepGood_HT800'
         if len(samplesList) > 2: samplesList.append(samplesList.pop(2)) # moves qcd to end of list 
      elif "measurement2" in region:
         skim = 'lt120'
      else:
         print "Incorrect input for measurement region. Exiting."
         sys.exit()
   
      if script == "fakeRate.py" and fakeRateMeasurement:
         if fakeRateMeasurement == "data-EWK":
            getData = True
         elif fakeRateMeasurement == "MC" or fakeRateMeasurement == "MC-EWK":
            getData = False
         else:
            print "Incorrect input for fake rate measurement. Exiting."
            sys.exit()
      elif sample: samplesList.append(sample)

      if script == "plotFakeRegions.py": getData = True

      if getData:
         if region == "measurement1":
            dataset = 'djetBlind'
   
         elif "measurement2" in region:
            dataset = 'd1lepBlind'
      
         if dataset: samplesList.append(dataset)
   
   elif "application" in region:
      skim = "preIncLep"
      getData = False #NOTE: For now, do not plot data near SR
      if script == "fakeRate.py":
         if sample: samplesList.append(sample)
   else:
      print "Region unknown. Exiting."
      sys.exit()

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

   # Only veto fakes from taus if no data plotted 
   if script == "plotFakeRegions.py" and getData: considerFakeTaus = 0
   
   selection = {}
   WPs = ['loose', 'tight']
   for iWP in WPs:
      selection.update(fakeCuts(samples, region, lep, iWP, mva = mva, considerFakeTaus = considerFakeTaus, VR = VR, invAntiQCD = invAntiQCD, noAntiQCD = noAntiQCD))
   
   setEventListToChains(samples, samplesList, selection['kinematic'][region])
   
   if verbose:
      print makeLine()
      print "Using the following selection: \n",
      pprint(selection)
      print "\n",
      print makeLine()
      
   # Save (http://www.hephy.at/user/mzarucki/plots)
   if save: 
      saveTag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
      baseDir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation"%saveTag

      savedir = baseDir

      if script == "simulFakeRateMeasurement.py":  
         savedir += "/measurementRegions/simulFakeRateMeasurement" 
      else:
         if "application" in region:
            savedir += "/applicationRegions"
         elif "measurement" in region:
            savedir += "/measurementRegions"

         if mva: savedir += "/%s_id%s_bdt%s"%(region, selection['mvaId'], selection['bdtcut'])
         else:   savedir += "/%s"%region
      
         if script == "fakeRate.py" or script == "simulFakeRatePlots.py": 
            savedir += "/tightToLooseRatio"
         elif script == "plotFakeRegions.py":
            savedir += "/distributions"
         elif script == "fakesEstimation.py" or script == "fakesUncertainties.py":
            savedir += "/estimation"
         elif script == "scanFakeRegions.py":
            savedir += "/scanRegions"
         
         if "application" in region: 
            if   VR and invAntiQCD: savedir += "/%s_invAntiQCD"%VR
            elif VR and noAntiQCD:  savedir += "/%s_noAntiQCD"%VR
            elif VR:                savedir += "/%s"%VR
            elif invAntiQCD:        savedir += "/invAntiQCD"
            elif noAntiQCD:         savedir += "/noAntiQCD"
            else:                   savedir += "/SR"
      
      if measurementRegion: savedir += "/" + measurementRegion
         
      if ptBin: savedir += "/ptBin_%s_%s"%(ptBin[0], ptBin[1])
      else:     savedir += "/allBins"
         
      if considerFakeTaus: savedir += "/fakeTausConsidered"
      else:                savedir += "/fakeTausNotConsidered"

      savedir += "/" + lepton

      if script not in ["fakeRate.py", "simulFakeRatePlots.py", "simulFakeRateMeasurement.py"]: 
         if looseNotTight: 
            savedir += "/L!T"
            if doYields: yieldDir += "/L!T"
         else: 
            savedir += "/Loose"
            if doYields: yieldDir += "/Loose"

      if script in ["fakesEstimation.py", "fakesUncertainties.py"]:
         binDir = "/TL_" + fakeRateMeasurement
         savedir += binDir
      else:
         binDir = None

      if not varBins: savedir += "/fixedBins"
      else:           savedir += "/varBins"
     
      if script == "fakeRate.py" and fakeRateMeasurement:
         savedir += "/" + fakeRateMeasurement
         
      if doYields and script in ['fakeRate.py', 'plotFakeRegions.py']:
         yieldDir = "%s/yields"%savedir
         makeDir(yieldDir)

      if logy: savedir += "/log"
     
      if script not in ["simulFakeRatePlots.py", "fakesUncertainties.py", "simulFakesUnc.py"]: 
         makeDir(savedir + "/root")
         makeDir(savedir + "/pdf")
         if doYields: makeDir(yieldDir)
  
      # Suffix
      suffix = "_%s"%lep

      if script != "simulFakeRateMeasurement.py":
         suffix += "_%s"%region

      if fakeRateMeasurement:
         suffix += "_%s"%fakeRateMeasurement
      elif sample: 
         suffix += "_%s"%sample
      
      if WP: 
         suffix += "_%s"%WP

      if verbose:
         print makeLine()
         print "baseDir:",   baseDir 
         print "Saving to:", savedir 
         print makeLine()

   bins = fakeBinning(lep, varBins = varBins)

   ret = {}
   ret['lepton'] =      lepton
   ret['samplesList'] = samplesList
   ret['samples'] =     samples
   ret['dataset'] =     dataset
   ret['selection'] =   selection
   ret['bins'] =        bins
   
   if save:
      ret['baseDir'] =     baseDir 
      ret['saveTag'] =     saveTag 
      ret['savedir'] =     savedir
      ret['suffix'] =      suffix
      if doYields:
         ret['yieldDir'] = yieldDir
      if binDir:
         ret['binDir'] =   binDir

   return ret

def fakeBinning(lep, xmax = 200, varBins = False):

   if lep == "el":    etaAcc = 2.5
   elif lep == "mu":  etaAcc = 2.4
   elif lep == "lep": etaAcc = 2.5
   else:
      print "Lepton input not recongised. Choose from: el, mu, lep. Exiting."
      sys.exit()

   if not varBins:
      bins = {'pt':[int(xmax/10), 0, xmax], 'eta':[int(etaAcc*10), 0, etaAcc], 'mt':[int(xmax/10), 0, xmax]}
   else: # variable bin size
      bins = {}
      bins['mt'] = [0, 30, 60, 95, 120, 200]
      bins['eta'] = [0, 1.5, etaAcc]

      if lep == 'mu':
         bins['pt'] = [0, 3.5, 5, 12, 20, 30, 80, xmax, xmax+5]
         #bins['eta'] = [0, 0.9, 1.2, 2.1, etaAcc]
      elif lep == 'el':
         bins['pt'] = [0, 5, 12, 20, 30, 80, xmax, xmax+5]
         #bins['eta'] = [0, 0.7, 1.5, etaAcc]
      else:
         bins['pt'] = [0, 3.5, 5, 12, 20, 30, 80, xmax, xmax+5]
         #bins['eta'] = [0, 0.9, 1.2, 1.5, 2.1, etaAcc]

   return bins
