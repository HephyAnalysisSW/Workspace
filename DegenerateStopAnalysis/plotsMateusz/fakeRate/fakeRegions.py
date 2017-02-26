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

def fakeRegions(samples, region, lep, WP, cutWeightOptions = cutWeightOptions, ptInclusive = True, fakeTauVeto = True, highPtBin = False, mva = False):
   
   if not ("application" in region or "measurement" in region):   
      print "Region unknown. Exiting."
      sys.exit()

   #  cutWeightOptions format:
   #  cutWeightOptions['options']     = ['isr', 'sf']
   #  cutWeightOptions['def_weights'] = ['weight', 'pu', 'DataBlind_lumi']
   #  cutWeightOptions['settings'] = {
   #         'lepCol': "LepGood",
   #         'lep':    "lep",
   #         'lepTag': "def",
   #         'jetTag': "def",
   #         'btagSF': "SF",
   #         'mvaId':  None,
   #         'bdtcut': None,
   #         'lumis' : lumis,
   #     }
   
   cutWeightOptions['def_weights'] = ['weight', 'pu']
   if 'djet' in samples.keys() or "measurement1" in region:
      cutWeightOptions['def_weights'].append('JetHTDataBlind_lumi')
   else:
      cutWeightOptions['def_weights'].append('DataBlind_lumi')

   cutWeightOptions['settings']['lepCol'] = "LepGood"

   if mva:
      cutWeightOptions['settings']['mvaId'] = '30' #MVA Set 
      cutWeightOptions['settings']['bdtcut'] = '0.33' #0.36
   
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
   if region == "measurement1": 
      trigger = triggers['data_jet'] 
   elif region == "measurement2": 
      trigger = triggers['data_%s'%lep]
   else:
      trigger = triggers['data_met'] 
   
   # Selection dictionary
   selection = {
      'lumis': cutWeightOptions['settings']['lumis'],
      'trigger': trigger, 
      'filters': filters, 
      'kinematic': {}, 
      WP: {}, 
   }
  
   if region == "measurement2": 
      alt_vars = {'lepIndex': {'var':'Index{lepCol}_{lep}{lt}[1]', 'latex':''}} # considering 2nd lepton
   else:
      alt_vars = {}
 
   cuts_weights = CutsWeights(samples, cutWeightOptions, alternative_vars = alt_vars)
   selection[WP]['index'] = cuts_weights.cuts.vars_dict_format['lepIndex']

   # Region
   regDef = region.replace('application_', '')
  
   # pT inclusive application region 
   if "application" in region and ptInclusive:
      regDef2 = regDef + '_incPt'
      if mva: #need to remove cut from baseCut
         baseCut = cuts_weights.cuts.regions[regDef]['baseCut']
         baseCut2 = baseCut + '_incPt'
         cuts_weights.cuts.regions[baseCut2] = copy.deepcopy(cuts_weights.cuts.regions[baseCut])
         cuts_weights.cuts.regions[baseCut2]['cuts'].remove('lepPt_lt_30')
         cuts_weights.cuts.regions[regDef2] = copy.deepcopy(cuts_weights.cuts.regions[regDef])
         cuts_weights.cuts.regions[regDef2]['baseCut'] = baseCut2
      elif 'sr1c' in region: #need to remove cut from baseCut
         baseCut = cuts_weights.cuts.regions[regDef]['baseCut']
         baseCut2 = baseCut + '_incPt'
         cuts_weights.cuts.regions[baseCut2] = copy.deepcopy(cuts_weights.cuts.regions[baseCut])
         cuts_weights.cuts.regions[baseCut2]['cuts'].remove('lepPt_lt_30')
         cuts_weights.cuts.regions[regDef2] = copy.deepcopy(cuts_weights.cuts.regions[regDef])
         cuts_weights.cuts.regions[regDef2]['baseCut'] = baseCut2
      else:
         cuts_weights.cuts.regions[regDef2] = copy.deepcopy(cuts_weights.cuts.regions[regDef])
         cuts_weights.cuts.regions[regDef2]['cuts'].remove('lepPt_lt_30')   
      regDef = regDef2
    
   if fakeTauVeto: cuts_weights.cuts.regions[regDef]['cuts'].append('fakeTauVeto')
   if highPtBin:   cuts_weights.cuts.regions[regDef]['cuts'].append('lepPt_100_200')

   # L!T
   if "application" in region and WP == "loose":  
      cuts_weights.cuts.regions['%s_notTight'%regDef] = copy.deepcopy(cuts_weights.cuts.regions[regDef])
      cuts_weights.cuts.regions['%s_notTight'%regDef]['cuts'].append('notTight')

   # Splitting into prompt and fakes
   for x in ['prompt', 'fake']: 
      cuts_weights.cuts.regions['%s_%s'%(regDef, x)] = copy.deepcopy(cuts_weights.cuts.regions[regDef])
      cuts_weights.cuts.regions['%s_%s'%(regDef, x)]['cuts'].append(x)
      
      # L!T
      if "application" in region and WP == "loose": 
         cuts_weights.cuts.regions['%s_notTight_%s'%(regDef, x)] = copy.deepcopy(cuts_weights.cuts.regions['%s_notTight'%regDef])
         cuts_weights.cuts.regions['%s_notTight_%s'%(regDef, x)]['cuts'].append(x)

   # Updating all cuts classes
   cuts_weights.cuts._update(reset = False)
   cuts_weights._update()
 
   selection['regDef'] = regDef
   selection[WP]['cuts_weights'] = cuts_weights
   selection[WP]['cuts'] = cuts_weights.cuts
   selection[WP][region] = cuts_weights.cuts_weights[regDef]
   selection['kinematic'][region] = cuts_weights.cuts.cutInsts[regDef.replace('_incPt', '') + '_kin']
   
   if mva: 
      selection['mvaId'] = cutWeightOptions['settings']['mvaId']
      selection['bdtcut'] = cutWeightOptions['settings']['bdtcut']
      selection['mvaIdIndex'] = cuts_weights.cuts.vars.mvaIdIndex

   return selection

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
         bins['pt'] = [0, 5, 12, 20, 30, 50, 100, xmax]
         bins['eta'] = [0, 0.9, 1.2, 2.1, etaAcc]
      elif lep == 'el':
         bins['pt'] = [0, 5, 12, 20, 30, 50, 100, xmax]
         bins['eta'] = [0, 0.7, 1.5, etaAcc]
      else:
         bins['eta'] = [0, 0.9, 1.2, 1.5, 2.1, etaAcc]

   return bins
      
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
