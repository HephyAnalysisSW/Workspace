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
from Workspace.DegenerateStopAnalysis.tools.mvaTools import getMVATrees
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from Workspace.HEPHYPythonTools.helpers import getYieldFromChain
from Workspace.HEPHYPythonTools import u_float
from pprint import pprint
from array import array
from math import pi, sqrt
from fakeRegions import fakeRegions

def fakeParser(script):
   parser = argparse.ArgumentParser(description="Input options")
   parser.add_argument("--lep",         help = "Lepton", type = str, default = "el")
   parser.add_argument("--region",      help = "Measurement or application region", dest = "region", type = str, default = "application_sr1")
   parser.add_argument("--mva",         help = "MVA", action = "store_true")
   parser.add_argument("--getData",     help = "Get data", action = "store_true")
   parser.add_argument("--fakeTauVeto", help = "Veto fakes from taus", dest = "fakeTauVeto", type = bool, default = True)
   parser.add_argument("--doPlots",     help = "Plot", dest = "doPlots", type = int, default = 1)
   parser.add_argument("--doYields",    help = "Calculate yields", action = "store_true")
   parser.add_argument("--varBins",     help = "Variable bin size", type = int, default = 1)
   parser.add_argument("--logy",        help = "Toggle logy", dest = "logy", action = "store_true")
   parser.add_argument("--save",        help="Toggle save", dest="save", type=int, default=1)
   parser.add_argument("--verbose",     help="Verbosity switch", action = "store_true")

   if script == "plotFakeRegions.py" or script == "fakesEstimation.py" or script == "scanFakeRegions.py":
      parser.add_argument("--looseNotTight", help = "Loose-not-tight CR", action = "store_true")
      parser.add_argument("--ptBin", help = "(lowBin,highBin)", dest = "ptBin",  type = str, nargs = "+", default = None)
      parser.add_argument("--CT200",      help = "Loosen CT cut to 200", action = "store_true")
      parser.add_argument("--invAntiQCD", help = "Invert anti-QCD cut",  action = "store_true")
      parser.add_argument("--noAntiQCD",  help = "Remove anti-QCD cut",  action = "store_true")
      
      if script == "plotFakeRegions.py" or script == "scanFakeRegions.py":
         parser.add_argument("--WP", dest = "WP", help = "Loose or Tight WP", type = str, default = "loose")
      
   if script == "fakeRate.py" or script == "scanFakeRegions.py":
      parser.add_argument("--sample", dest = "sample", help = "Sample", type = str, default = "qcd")
      if script == "fakeRate.py": 
         parser.add_argument("--noWeights", help = "Sample", action = "store_true")
         parser.add_argument("--do2D", dest = "do2D", help = "2D fake rate", action = "store_true")
      elif script == "scanFakeRegions.py":
         parser.add_argument("--category", dest = "category", help = "Total/Prompt/Fake", type = str, default = "total")
   
   if script == "plotFakeRegions.py" or script == "fakesEstimation.py":
      parser.add_argument("--doControlPlots", help = "Additional plots of regions", action = "store_true")
      if script == "fakesEstimation.py":
         parser.add_argument("--measurementRegion", dest = "measurementRegion", help = "Measurement region", type = str, default = "measurement1")
         parser.add_argument("--closureDef", dest = "closureDef", help = "Definition of closure (standard vs ratio)", type = str, default = "standard")
      
   if script == "fakeRate.py" or script == "fakesEstimation.py":
      parser.add_argument("--fakeRateMeasurement", dest = "fakeRateMeasurement", help = "Source of fake rate measurement (data-EWK or MC)", type = str, default = "")
  
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
   fakeTauVeto =         args['fakeTauVeto'] if         'fakeTauVeto'         in args.keys() else None
   doPlots =             args['doPlots'] if             'doPlots'             in args.keys() else None
   doYields =            args['doYields'] if            'doYields'            in args.keys() else None
   varBins =             args['varBins'] if             'varBins'             in args.keys() else None
   logy =                args['logy'] if                'logy'                in args.keys() else None
   save =                args['save'] if                'save'                in args.keys() else None
   verbose =             args['verbose'] if             'verbose'             in args.keys() else None
   
   looseNotTight =       args['looseNotTight'] if       'looseNotTight'       in args.keys() else None
   ptBin =               args['ptBin'] if               'ptBin'               in args.keys() else None
   CT200 =               args['CT200'] if               'CT200'               in args.keys() else None
   invAntiQCD =          args['invAntiQCD'] if          'invAntiQCD'          in args.keys() else None
   noAntiQCD =           args['noAntiQCD'] if           'noAntiQCD'           in args.keys() else None
   
   WP =                  args['WP'] if                  'WP'                  in args.keys() else None
   sample =              args['sample'] if              'sample'              in args.keys() else None
   noWeights =           args['noWeights'] if           'noWeights'           in args.keys() else None
   fakeRateMeasurement = args['fakeRateMeasurement'] if 'fakeRateMeasurement' in args.keys() else None
   measurementRegion =   args['measurementRegion'] if   'measurementRegion'   in args.keys() else None
   do2D =                args['do2D'] if                'do2D'                in args.keys() else None
   category =            args['category'] if            'category'            in args.keys() else None
   doControlPlots =      args['doControlPlots'] if      'doControlPlots'      in args.keys() else None
   
   if verbose:
      print makeLine() 
      print "Getting samples, cut-strings and save directories for:", script
      print "Arguments:", args
      print makeLine() 

   if script == "fakeRate.py" and fakeRateMeasurement and not "measurement" in region:
      print "Fake rate measurement only in measurement region. Exiting."
      sys.exit()

   if script != "fakeRate.py":
      #Sets TDR style
      setup_style()

   if script == "fakesEstimation.py" and not "application" in region:
      print "Region for estimation should be an application region."
      sys.exit()

   # Samples
   cmgPP = cmgTuplesPostProcessed()
   
   if script == "fakeRate.py" and not fakeRateMeasurement:
      samplesList = []
   elif script == "scanFakeRegions.py":
      samplesList = [sample]
   else:
      samplesList = ["st", "vv", "qcd", "z", "dy", "w", "tt"]
   
   if script == "plotFakeRegions.py":
      splitTT = True
   else:
      splitTT = False

   if splitTT:
      samplesList.remove("tt")
      samplesList.extend(["tt_1l", "tt_2l"])

   dataSample = ''

   if "measurement" in region:
      skim = "oneLepGood"
      mva = False
      if "measurement2" in region:
         fakeTauVeto = False
   
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
            dataSample = 'djetBlind'
   
         elif "measurement2" in region:
            samplesList.reverse()
            dataSample = 'd1lepBlind'
      
         if dataSample: samplesList.append(dataSample)
   
   elif "application" in region:
      skim = "preIncLep"
      samplesList.reverse()
      getData = False #NOTE: For now, do not plot data near SR
      if script == "fakeRate.py":
         if sample: samplesList.append(sample)
   else:
      print "Region unknown. Exiting."
      sys.exit()

   if "measurement2" in region:
      samples =                  getSamples(cmgPP = cmgPP, skim = skim,    sampleList = samplesList,  scan = False, useHT = True, getData = False, def_weights = [])
      if getData: samples.update(getSamples(cmgPP = cmgPP, skim = 'lt120', sampleList = [dataSample], scan = False, useHT = True, getData = True,  def_weights = []))
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

   # Only veto fakes from taus if no data plotted 
   if getData: fakeTauVeto = False
   
   selection = {'MC':{}, 'data':{}}
   WPs = ['loose', 'tight']
   for iWP in WPs:
      selection['MC'].update(  fakeRegions(samples, region, lep, iWP, mva = mva, fakeTauVeto = fakeTauVeto, CT200 = CT200, invAntiQCD = invAntiQCD, noAntiQCD = noAntiQCD))
      selection['data'].update(fakeRegions(samples, region, lep, iWP, mva = mva, fakeTauVeto = False, invAntiQCD = invAntiQCD, noAntiQCD = noAntiQCD))
   
   setEventListToChains(samples, samplesList, selection['MC']['kinematic'][region])
   
   if verbose:
      print makeLine()
      print "Using the following selection: \n",
      pprint(selection)
      print "\n",
      print makeLine()
    
   # Save (http://www.hephy.at/user/mzarucki/plots)
   if save: 
      tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
      baseDir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/fakesEstimation"%tag

      savedir = baseDir
 
      if "application" in region:
         savedir += "/applicationRegions"
      elif "measurement" in region:
         savedir += "/measurementRegions"
 
      if mva: savedir += "/%s_id%s_bdt%s"%(region, selection['MC']['mvaId'], selection['MC']['bdtcut'])
      else:   savedir += "/%s"%region
      
      if doYields:
         yieldDir = "%s/yields"%savedir
         makeDir(yieldDir)

      if script == "fakeRate.py": 
         savedir += "/tightToLooseRatio"
      elif script == "plotFakeRegions.py":
         savedir += "/distributions"
      elif script == "fakesEstimation.py":
         savedir += "/estimation"
      elif script == "scanFakeRegions.py":
         savedir += "/scanRegions"
      
      if CT200 and invAntiQCD:  savedir += "/CT200_invAntiQCD"
      elif CT200 and noAntiQCD: savedir += "/CT200_noAntiQCD"
      elif CT200:               savedir += "/CT200"
      elif invAntiQCD:          savedir += "/invAntiQCD"
      elif noAntiQCD:           savedir += "/noAntiQCD"

      if measurementRegion: savedir += "/" + measurementRegion

      if ptBin: savedir += "/ptBin_%s_%s"%(ptBin[0], ptBin[1])
      else:     savedir += "/allBins"

      savedir += "/" + lepton

      if script != "fakeRate.py": 
         if looseNotTight: 
            savedir += "/L!T"
            if doYields: yieldDir += "/L!T"
         else: 
            savedir += "/Loose"
            if doYields: yieldDir += "/Loose"

      if not (script == "fakesEstimation.py" and fakeRateMeasurement):
         if not varBins: savedir += "/fixedBins"
         else:           savedir += "/varBins"
     
         if logy: savedir += "/log"
     
      if script != "fakesEstimation.py": 
         makeDir(savedir + "/root")
         makeDir(savedir + "/pdf")
         if doYields: makeDir(yieldDir)
  
      # Suffix 
      suffix = "_%s_%s"%(region, lep)
      
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
   ret['dataSample'] =  dataSample
   ret['selection'] =   selection
   ret['bins'] =        bins
   
   if save:
      ret['savedir'] =     savedir
      ret['suffix'] =      suffix
      if doYields:
         ret['yieldDir'] = yieldDir

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
      bins['mt'] = [0, 30, 60, 95, 120, xmax]

      if lep == 'mu':
         bins['pt'] = [0, 3.5, 5, 12, 20, 30, 50, 100, xmax]
         bins['eta'] = [0, 0.9, 1.2, 2.1, etaAcc]
      elif lep == 'el':
         bins['pt'] = [0, 5, 12, 20, 30, 50, 100, xmax]
         bins['eta'] = [0, 0.7, 1.5, etaAcc]
      else:
         bins['pt'] = [0, 5, 12, 20, 30, 50, 100, xmax]
         bins['eta'] = [0, 0.9, 1.2, 1.5, 2.1, etaAcc]

   return bins
