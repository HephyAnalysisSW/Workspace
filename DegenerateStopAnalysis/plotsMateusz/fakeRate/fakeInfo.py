# fakeInfo.py
# Common arguments, samples, savedirs for fake rate estimation scripts
# Mateusz Zarucki 2017

import ROOT
import os, sys
import collections 
import argparse
import pickle
import copy
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, setup_style, makeSimpleLatexTable, makeDir, makeLegend
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
   parser.add_argument("--eta1p5",      help = "Eta 1p5 cut", type = str, default = None, choices = ["lt", "gt"])
   parser.add_argument("--doPlots",     help = "Plot", dest = "doPlots", type = int, default = 1)
   parser.add_argument("--doYields",    help = "Calculate yields", action = "store_true")
   parser.add_argument("--varBins",     help = "Variable bin size", type = int, default = 1)
   parser.add_argument("--logy",        help = "Toggle logy", dest = "logy", action = "store_true")
   parser.add_argument("--save",        help="Toggle save", dest="save", type=int, default=1)
   parser.add_argument("--verbose",     help="Verbosity switch", action = "store_true")
   parser.add_argument("--VR",          help = "Validation region", type = str, default = None, choices = ["CT200", "EVR1", "EVR2"])
   parser.add_argument("--considerFakeTaus", help = "Veto fakes from taus", dest = "considerFakeTaus", type = int, default = 1)
   parser.add_argument("--measurementType", help = "Source of fake rate measurement (data-EWK or MC)", dest = "measurementType", type = str, default = "")
   parser.add_argument("--noWttWeights",    help="No Wpt and tt reweighting", action = "store_true")
   parser.add_argument("--highWeightVeto",  help="Veto events with high weight", dest="highWeightVeto", type=int, default=1)

   if script in ["plotFakeRegions.py", "fakesClosure.py", "fakesEstimationFinal.py", "fakesUncertainties.py", "scanFakeRegions.py"]:
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
   
   if script in ["plotFakeRegions.py", "fakesClosure.py", "fakesEstimationFinal.py", "fakesUncertainties.py", "simulFakesUnc.py"]:
      parser.add_argument("--doControlPlots", help = "Additional plots of regions", action = "store_true")
      if script in ["fakesClosure.py", "fakesEstimationFinal.py", "fakesUncertainties.py", "simulFakesUnc.py"]:
         parser.add_argument("--doClosure",  dest = "doClosure",  help = "Do closure", type = int, default = 1)
         parser.add_argument("--mergeHighPtBins",  dest = "mergeHighPtBins",  help = "Merge high pt bins into one CR bin", action = "store_true")
         parser.add_argument("--addMRsys",  help = "Add TL non-univ. systematics to closure",  action = "store_true")
         if script != "fakesEstimationFinal.py":
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
   eta1p5 =              args['eta1p5'] if              'eta1p5'              in args.keys() else None
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
   measurementType =     args['measurementType'] if     'measurementType'     in args.keys() else None
   measurementRegion =   args['measurementRegion'] if   'measurementRegion'   in args.keys() else None
   
   noWttWeights =        args['noWttWeights'] if        'noWttWeights'        in args.keys() else None
   highWeightVeto =      args['highWeightVeto'] if      'highWeightVeto'      in args.keys() else None
   doClosure =           args['doClosure'] if           'doClosure'           in args.keys() else None
  
   if script == "fakesEstimationFinal.py": looseNotTight = True
   
   if "measurement" in region: highWeightVeto = 0
 
   if verbose:
      print makeLine() 
      print "Getting samples, cut-strings and save directories for:", script
      print "Arguments:", args
      print makeLine() 

   if script == "fakeRate.py" and measurementType and not "measurement" in region:
      print "Fake rate measurement only in measurement region. Exiting."
      sys.exit()

   # Sets TDR style
   if script in ["fakesClosure.py", "fakesEstimationFinal.py"] and not "application" in region:
      print "Region for estimation should be an application region. Exiting."
      sys.exit()

   # Samples
   if "measurement2" in region or "measurement3" in region:
      ppDir = '/afs/hephy.at/data/mzarucki01/cmgTuples/postProcessed_mAODv2/8025_mAODv2_v7/80X_postProcessing_v0/analysisHephy_13TeV_2016_v2_4/step1'
      mc_path     = ppDir + "/RunIISummer16MiniAODv2_v7"
      data_path   = ppDir + "/Data2016_v7"

      cmgPP = cmgTuplesPostProcessed(mc_path = mc_path, signal_path = mc_path, data_path = data_path)
   else:
      cmgPP = cmgTuplesPostProcessed()
   
   if script == "fakeRate.py" and not measurementType:
      samplesList = []
   elif script == "scanFakeRegions.py":
      samplesList = [sample]
   elif "simul" in script:
      samplesList = ["st"]
   else:
      samplesList = ["st", "qcd", "dy5to50", "dy", "z", "tt_2l", "tt_1l", "w"]
      #samplesList = ["st", "vv", "qcd", "dy5to50", "dy", "z", "tt_2l", "tt_1l", "w"]

   dataset = None

   if "measurement" in region:
      mva = False
      if "measurement1" in region:
         skim = 'oneLepGood_HT800'
         if len(samplesList) == 9: samplesList.append(samplesList.pop(2)) # moves qcd to end of list 
      elif "measurement2" in region or "measurement3" in region:
         skim = 'oneLepGood20' #'lt120'
      elif "measurement4" in region:
         if lep == "mu":
            skim = 'oneLepGood_HT100_MET40_MT30'
         elif lep == "el":
            skim = 'oneElGood50_ISR100_MET40_MT30'
      else:
         print "Incorrect input for measurement region. Exiting."
         sys.exit()
   
      if script == "fakeRate.py":
         if measurementType:
            if measurementType == "data-EWK":
               getData = True
            elif measurementType == "MC" or measurementType == "MC-EWK":
               getData = False
            else:
               print "Incorrect input for fake rate measurement. Exiting."
               sys.exit()
         elif sample: samplesList.append(sample)

      if script == "plotFakeRegions.py": getData = True
         
      if "measurement2" in region or "measurement3" in region:
         getData = False # FIXME: until samples are ready

      if getData:
         if "measurement1" in region:
            dataset = 'djetBlind'
   
         elif "measurement2" in region or "measurement3" in region:
            dataset = 'd1lepBlind'

         elif "measurement4" in region:
            if   lep == "el":  dataset = 'd1elBlind' 
            elif lep == "mu":  dataset = 'd1muBlind' 
            elif lep == "lep": dataset = 'd1lepBlind' 
 
   elif "application" in region:
      skim = "preIncLep"
      if script == "fakesEstimationFinal.py" and measurementType == "data-EWK":
         getData = True # NOTE: careful with data around SR
         dataset = 'dblind'
      else:
         getData = False
      if script == "fakeRate.py":
         if sample: samplesList.append(sample)
      if 'sr1' in region and "simul" not in script:
         eta1p5 = 'lt'
   else:
      print "Region unknown. Exiting."
      sys.exit()
         
   if dataset: samplesList.append(dataset)
   if skim == 'lt120' or skim == 'oneLepGood_HT100_MET40_MT30' or skim == "preIncLep": samplesList.append('ttx') #or skim == 'oneElGood50_ISR100_MET40_MT30'

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

   if lep == "el":    lepton = "Electron"
   elif lep == "mu":  lepton = "Muon"
   elif lep == "lep": lepton = "Lepton"

   # Only veto fakes from taus if no data plotted 
   if script == "plotFakeRegions.py" and getData: considerFakeTaus = 0
   
   selection = {}
   WPs = ['tight', 'loose']
   for iWP in WPs:
      selection.update(fakeCuts(samples, region, lep, iWP, mva = mva, considerFakeTaus = considerFakeTaus, eta1p5 = eta1p5, VR = VR, invAntiQCD = invAntiQCD, noAntiQCD = noAntiQCD, ptBin = ptBin, noWttWeights = noWttWeights, highWeightVeto = highWeightVeto))
 
   if mva:
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
     
      if eta1p5: etaBin = "eta_%s_1p5"%eta1p5
      else:      etaBin = "etaIncl"
     
      savedir = baseDir

      if script == "simulFakeRateMeasurement.py":  
         savedir += "/measurementRegions/simulFakeRateMeasurement" 
      else:
         if "application" in region:
            savedir += "/applicationRegions"
         elif "measurement" in region:
            savedir += "/measurementRegions"

         if mva: savedir += "/%s_id%s_bdt%s_%s"%(region, selection['mvaId'], selection['bdtcut_sr'], selection['bdtcut_cr'])
         else:   savedir += "/%s"%region
      
         if script == "fakeRate.py" or script == "simulFakeRatePlots.py": 
            savedir += "/tightToLooseRatio"
         elif script == "plotFakeRegions.py":
            savedir += "/distributions"
         elif script in ["fakesClosure.py", "fakesEstimationFinal.py"] or script == "fakesUncertainties.py":
            savedir += "/estimation"
            if script == "fakesClosure.py":
               savedir += "/closure"
            elif script == "fakesEstimationFinal.py":
               savedir += "/finalEstimate"
         elif script == "scanFakeRegions.py":
            savedir += "/scanRegions"
         
         if "application" in region: 
            if   VR and invAntiQCD: VRdir = "%s_invAntiQCD"%VR
            elif VR and noAntiQCD:  VRdir = "%s_noAntiQCD"%VR
            elif VR:                VRdir = "%s"%VR
            elif invAntiQCD:        VRdir = "invAntiQCD"
            elif noAntiQCD:         VRdir = "noAntiQCD"
            else:                   VRdir = "SR"
            savedir += "/" + VRdir
      
      if measurementRegion: savedir += "/" + measurementRegion
         
      if ptBin: savedir += "/ptBin_%s_%s"%(ptBin[0], ptBin[1])
      else:     savedir += "/allBins"
         
      if considerFakeTaus: savedir += "/fakeTausConsidered"
      else:                savedir += "/fakeTausNotConsidered"

      savedir += "/" + lepton

      if script not in ["fakeRate.py", "simulFakeRatePlots.py", "simulFakeRateMeasurement.py"]: 
         if looseNotTight: 
            savedir += "/LnotT"
         else: 
            savedir += "/Loose"

      if measurementType and script in ["fakesClosure.py", "fakesUncertainties.py", "fakesEstimationFinal.py", "fakesEstimationFinal_sr2.py"]:
         binDir = "/TL_" + measurementType
         savedir += binDir
      else:
         binDir = None

      if not varBins: savedir += "/fixedBins"
      else:           savedir += "/varBins"
     
      if (script == "fakeRate.py" and measurementType) or script == "promptContamination.py":
         savedir += "/" + measurementType
         
      savedir += "/" + etaBin
      
      if noWttWeights: savedir += "/noWttWeights"
      
      if doYields and script not in ["simulFakeRatePlots.py", "fakesUncertainties.py", "simulFakesUnc.py", "fakesClosure.py", "fakesEstimationFinal.py"]: 
         yieldDir = "%s/yields"%savedir
         makeDir(yieldDir+'/composition')

      if logy: savedir += "/log"
     
      if script not in ["simulFakeRatePlots.py", "fakesUncertainties.py", "simulFakesUnc.py"]: 
         makeDir(savedir + "/root")
         makeDir(savedir + "/pdf")
      
      # Suffix
      suffix = "_%s"%lep

      if script != "simulFakeRateMeasurement.py":
         suffix += "_%s"%region

      if measurementType:
         suffix += "_%s"%measurementType
      elif sample: 
         suffix += "_%s"%sample
      
      if WP: 
         suffix += "_%s"%WP
      
      if VR: 
         suffix += "_%s"%VR

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
      ret['etaBin'] =      etaBin 
      ret['suffix'] =      suffix
      if doYields and script not in ["simulFakeRatePlots.py", "fakesUncertainties.py", "simulFakesUnc.py", "fakesClosure.py", "fakesEstimationFinal.py"]: 
         ret['yieldDir'] = yieldDir
      if binDir:
         ret['binDir'] = binDir

   return ret

def fakeBinning(lep, xmax = 200, varBins = False, mergeHighPtBins = False):

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
         
      if mergeHighPtBins:
         bins['pt'] = [0, 3.5, 5, 12, 20, 30, xmax+5]
      else:
         bins['pt'] = [0, 3.5, 5, 12, 20, 30, 50, 80, xmax, xmax+5]

      #if lep == 'mu':
      #   if mergeHighPtBins:
      #      bins['pt'] = [0, 3.5, 5, 12, 20, 30, xmax+5]
      #   else:
      #      bins['pt'] = [0, 3.5, 5, 12, 20, 30, 50, 80, xmax, xmax+5]
      #   #bins['eta'] = [0, 0.9, 1.2, 2.1, etaAcc]
      #elif lep == 'el':
      #   if mergeHighPtBins:
      #      bins['pt'] = [0, 5, 12, 20, 30, xmax+5]
      #   else:
      #      bins['pt'] = [0, 5, 12, 20, 30, 50, 80, xmax, xmax+5]
      #   #bins['eta'] = [0, 0.7, 1.5, etaAcc]
      #else:
      #   if mergeHighPtBins:
      #      bins['pt'] = [0, 3.5, 5, 12, 20, 30, xmax+5]
      #   else:
      #      bins['pt'] = [0, 3.5, 5, 12, 20, 30, 50, 80, xmax, xmax+5]
      #   #bins['eta'] = [0, 0.9, 1.2, 1.5, 2.1, etaAcc]

   return bins

binMaps = {}
binMaps_ = {}
invBinMaps = {}
invBinMaps_ = {}

binMaps_['el'] = [('1', '0_3p5'), ('2','ptVL'), ('3','ptL'), ('4','ptM'), ('5','ptH'), ('6','30-50'), ('7','50-80'), ('8','80-200'), ('9','>200')]
binMaps_['mu'] = [('1', '0_3p5'), ('2','ptVL'), ('3','ptL'), ('4','ptM'), ('5','ptH'), ('6','30-50'), ('7','50-80'), ('8','80-200'), ('9','>200')]
#binMaps_['el'] = [('1', '0_5'),                 ('2','ptL'), ('3','ptM'), ('4','ptH'), ('5','30-50'), ('6','50-80'), ('7','80-200'), ('8','>200')]

for lep in binMaps_:
   invBinMaps_[lep] = [x[::-1] for x in binMaps_[lep]]

binMaps['el'] =    collections.OrderedDict(binMaps_['el'])
binMaps['mu'] =    collections.OrderedDict(binMaps_['mu'])
invBinMaps['el'] = collections.OrderedDict(invBinMaps_['el'])
invBinMaps['mu'] = collections.OrderedDict(invBinMaps_['mu'])
