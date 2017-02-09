# fakeRegions.py
# Definition of regions used in fake rate estimation 
# Mateusz Zarucki 2017

import ROOT
import os, sys
import copy
from pprint import pprint
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.tools.mvaTools import getMVATrees
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters 

def regions(samples, region, lep, WP, cutWeightOptions = cutWeightOptions, oneBin = False, removeTau = True, mva = False):

   # cutWeightOptions format:
   #cutWeightOptions['options']     = ['isr', 'sf']
   #cutWeightOptions['def_weights'] = ['weight', 'pu', 'DataBlind_lumi']
   #cutWeightOptions['settings'] = {
   #         'lepCol': "LepGood",
   #         'lep':    "lep",
   #         'lepTag': "def",
   #         'jetTag': "def",
   #         'btagSF': "SF",
   #         'mvaId':  None,
   #         'bdtcut': None,
   #         'lumis' : lumis,
   #     }

   lepCol = 'LepGood'

   cutWeightOptions['options'] = ['isr']#, 'sf'] NOTE: update
   
   cutWeightOptions['settings']['lepCol'] = lepCol

   if mva:
      cutWeightOptions['settings']['mvaId'] = '30' #MVA Set 
      cutWeightOptions['settings']['bdtcut'] = '0.32' #0.36
   
   cutWeightOptions['settings']['btagSF'] = "SF"
      
   cutWeightOptions['settings']['lep'] = lep 

   # Working points
   map_WP_suff = {'loose':'loose', 'tight':'def'}
 
   cutWeightOptions['settings']['lepTag'] = map_WP_suff[WP] 
  
   #if lep == 'mu':
   #   cutWeightOptions['settings']['lepTag'] = 'lowpt'
   #else:
   #   cutWeightOptions['settings']['lepTag'] = 'def'

   # Triggers
   if "measurement" in region: trigger = triggers['data_jet'] 
   else:                       trigger = triggers['data_met'] 
   
   # Selection dictionary
   selection = {
      'lumis': cutWeightOptions['settings']['lumis'],
      'trigger': trigger, 
      'filters': filters, 
      'kinematic': {}, 
      WP: {}, 
   }
      
   if mva: 
      selection['mvaId'] = cutWeightOptions['settings']['mvaId']
      selection['bdtcut'] = cutWeightOptions['settings']['bdtcut']
   
   cuts_weights = CutsWeights(samples, cutWeightOptions)
   selection[WP]['cuts_weights'] = cuts_weights
   selection[WP]['cuts'] = cuts_weights.cuts

   if "measurement" in region:
      cutDef = region 
      selection[WP][region] = cuts_weights.cuts_weights[cutDef]
      selection['kinematic'][region] = cuts_weights.cuts.cutInsts[cutDef + '_kin']
   elif "application" in region:
      if not mva: suff = '_noPt'
      else:       suff = '' 
      cutDef = region.replace('application_', '') + suff
      selection[WP][region] = cuts_weights.cuts_weights[cutDef]
      selection['kinematic'][region] = cuts_weights.cuts.cutInsts[cutDef.replace('noPt', 'kin')]
   else:   
      print "Region unknown. Exiting."
      sys.exit()
   
   selection['cutDef'] = cutDef

   ## Additonal selection to select one bin   
   #if oneBin:
   #   selection[WP][region] = combineCuts(selection[WP][region], "({lepCol}_pt[{ind}] > 30 && {lepCol}_pt[{ind}] < 50)".format(lepCol = lepCol, ind = index[WP]))

   return selection

def binning(lep, xmax = 200, varBins = False):

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
         bins['pt'] = [0, 5, 12, 20, 30, 50, 100, xmax] #NOTE: Change to 3GeV
         bins['eta'] = [0, 0.9, 1.2, 2.1, etaAcc]
      elif lep == 'el':
         bins['pt'] = [0, 5, 12, 20, 30, 50, 100, xmax]
         bins['eta'] = [0, 0.7, 1.5, etaAcc]
      else:
         bins['eta'] = [0, 0.9, 1.2, 1.5, 2.1, etaAcc]

   return bins
      
#selection['application_sr1'].add(CutClass('x', [['x', 'x']]))
#selection['application_sr1'].remove(['lepPt_lt_30', 'lepEta1p5'])

##Preselection & basic SR cuts
#sr1 = CutClass("SR1", [
#   ["MET","met > 300"],
#   ["HT","ht_basJet_def > 400"],
#   ["ISR100", "nJet_isrHJet_def >= 1"],
#   ["No3rdJet60","nJet_vetoJet_def <= 2"],
#   ["antiQCD","dPhi_j1j2_vetoJet_def < 2.5"],
#   ["BVeto", "nJet_bJet_def < 1"],
#   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
#   ], baseCut = None)
#
#sr1_CT200 = CutClass("SR1_CT200", [
#   ["MET","met > 200"],
#   ["HT","ht_basJet_def > 300"],
#   ["ISR100", "nJet_isrHJet_def >= 1"],
#   ["No3rdJet60","nJet_vetoJet_def <= 2"],
#   ["antiQCD","dPhi_j1j2_vetoJet_def < 2.5"],
#   ["BVeto", "nJet_bJet_def < 1"],
#   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
#   ], baseCut = None)
#
#sr1_invertedAntiQCD = CutClass("SR1_invertedAntiQCD", [
#   ["MET","met > 300"],
#   ["HT","ht_basJet_def > 400"],
#   ["ISR100", "nJet_isrHJet_def >= 1"],
#   ["No3rdJet60", "nJet_vetoJet_def <= 2"],
#   ["invAntiQCD", "(dPhi_j1j2_vetoJet_def > 2.5 || nJet_vetoJet_def <= 1)"], #or required for inclusion of monojet evts
#   ["BVeto", "nJet_bJet_def < 1"],
#   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
#   ], baseCut = None)
#
#sr1_invertedAntiQCD_CT200 = CutClass("SR1_invertedAntiQCD_CT200", [
#   ["MET","met > 200"],
#   ["HT","ht_basJet_def > 300"],
#   ["ISR100", "nJet_isrHJet_def >= 1"],
#   ["No3rdJet60","nJet_vetoJet_def <= 2"],
#   ["invAntiQCD", "(dPhi_j1j2_vetoJet_def > 2.5 || nJet_vetoJet_def <= 1)"], #or required for inclusion of monojet evts
#   ["BVeto", "nJet_bJet_def < 1"],
#   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
#   ], baseCut = None)
#
#sr1_noAntiQCD = CutClass("SR1_noAntiQCD", [
#   ["MET","met > 300"],
#   ["HT","ht_basJet_def > 400"],
#   ["ISR100", "nJet_isrHJet_def >= 1"],
#   ["BVeto", "nJet_bJet_def < 1"],
#   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
#   ], baseCut = None)
#
#sr1_noAntiQCD_CT200 = CutClass("SR1_noAntiQCD_CT200", [
#   ["MET","met > 200"],
#   ["HT","ht_basJet_def > 300"],
#   ["ISR100", "nJet_isrHJet_def >= 1"],
#   ["BVeto", "nJet_bJet_def < 1"],
#   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
#   ], baseCut = None)
