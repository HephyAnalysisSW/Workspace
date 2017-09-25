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

def fakeRegions(samples, region, lep, WP, cutWeightOptions = cutWeightOptions, ptInclusive = True, fakeTauVeto = True, highPtBin = False, mva = False, CT200 = False, invAntiQCD = False, noAntiQCD = False):
   
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
   
   dataSet = None
   if "measurement" in region: # NOTE: only considering data in measurement region for now
      for samp in samples:
         if samples[samp].isData and not "Unblind" in samples[samp].name:
            dataSet = samples[samp].name 
            break
   
   if dataSet: 
      cutWeightOptions['def_weights'].append(dataSet + '_lumi')
      cutWeightOptions['settings']['lumis']['target_lumi'] = cutWeightOptions['settings']['lumis'][dataSet + '_lumi'] #FIXME: Should also have this lumi for MC when splitting into prompt/fake
   else:
      cutWeightOptions['def_weights'].append('DataBlind_lumi')

   cutWeightOptions['settings']['lepCol'] = "LepGood"

   if mva:
      cutWeightOptions['settings']['mvaId'] = '30' #MVA Set 
      cutWeightOptions['settings']['bdtcut'] = '0.33' #0.36
   
   cutWeightOptions['settings']['btagSF'] = "SF"
      
   cutWeightOptions['settings']['lep'] = lep 

   # Working points
   if lep == 'mu':
      map_WP_suff = {'loose':'loose_lowpt', 'tight':'lowpt'}
      cutWeightOptions['settings']['lepTag'] = 'lowpt'
   else:
      map_WP_suff = {'loose':'loose', 'tight':'def'}
      cutWeightOptions['settings']['lepTag'] = 'def'
   
   cutWeightOptions['settings']['lepTag'] = map_WP_suff[WP] 
   cutWeightOptions['settings']['tightWP'] = '_lowpt'

   # Triggers
   if region == "measurement1": 
      trigger = triggers['data_jet'] 
   elif "measurement2" in region: 
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
 
   if "measurement2" in region: 
      alt_vars = {'lepIndex': {'var':'Index{lepCol}_lep{lt}[1]', 'latex':''}} # considering 2nd lepton as main lepton
   else: 
      alt_vars = {}
 
   cuts_weights = CutsWeights(samples, cutWeightOptions, alternative_vars = alt_vars)
   
   selection[WP]['lepIndex'] = cuts_weights.cuts.vars_dict_format['lepIndex']
   
   if "measurement2" in region:
      selection[WP]['tagIndex'] = cuts_weights.cuts.vars_dict_format['tagIndex']
      #cuts_weights.cuts.regions[regDef]['cuts'].append('fakeTauVeto')

   # Region
   regDef = region.replace('application_', '')
   kinDef = regDef.replace('_BVeto', '') + '_kin'
   if 'sr1' in kinDef: kinDef = 'sr1_kin'    
   
   if lep == "mu":
      cuts_weights.cuts.regions[regDef]['cuts'].append('lepPt_gt_3p5')
   
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
      elif regDef in ['sr1a', 'sr1b', 'sr1c', 'sr1ab']: #need to remove cut from baseCut
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
   
      if CT200 and not mva:
         # removing from evt list
         if not 'sr2' in regDef:
            cuts_weights.cuts.regions[kinDef]['cuts'].remove('CT300')
            cuts_weights.cuts.regions[kinDef]['cuts'].append('CT200')
         else:
            cuts_weights.cuts.regions[kinDef]['cuts'].remove('MET300')
            cuts_weights.cuts.regions[kinDef]['cuts'].remove('ISR325')
            cuts_weights.cuts.regions[kinDef]['cuts'].append('CT2_200')

         # removing from region cuts 
         if 'sr1c' in regDef or 'sr1b' in regDef or 'sr1c' in regDef or 'sr1ab' in regDef: # removing cut from baseCut
            baseCut = cuts_weights.cuts.regions[regDef]['baseCut']
            cuts_weights.cuts.regions[baseCut]['cuts'].remove('CT300')
            cuts_weights.cuts.regions[baseCut]['cuts'].append('CT200')
         elif 'sr2' in regDef: # removing cut from cuts
            cuts_weights.cuts.regions[regDef]['cuts'].remove('MET300')
            cuts_weights.cuts.regions[regDef]['cuts'].remove('ISR325')
            cuts_weights.cuts.regions[regDef]['cuts'].append('CT2_200')
         else:
            cuts_weights.cuts.regions[regDef]['cuts'].remove('CT300')
            cuts_weights.cuts.regions[regDef]['cuts'].append('CT200')
      
      if invAntiQCD or noAntiQCD:
         # removing from evt list
         cuts_weights.cuts.regions[kinDef]['cuts'].remove('AntiQCD')
         if invAntiQCD:
            cuts_weights.cuts.regions[kinDef]['cuts'].append('invAntiQCD')

         baseCut = cuts_weights.cuts.regions[regDef]['baseCut']
         # removing from presel 
         if 'sr1c' in regDef or 'sr1b' in regDef or 'sr1c' in regDef or 'sr1ab' in regDef: # removing cut from baseCut
            baseCut2 = cuts_weights.cuts.regions[baseCut]['baseCut']
            cuts_weights.cuts.regions[baseCut2]['cuts'].remove('AntiQCD')
            if invAntiQCD:
               cuts_weights.cuts.regions[baseCut2]['cuts'].append('invAntiQCD')
         else: 
            cuts_weights.cuts.regions[baseCut]['cuts'].remove('AntiQCD')
            if invAntiQCD:
               cuts_weights.cuts.regions[baseCut]['cuts'].append('invAntiQCD')

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
   selection['kinematic'][region] = cuts_weights.cuts.cutInsts[kinDef]
   
   if mva: 
      selection['mvaId'] = cutWeightOptions['settings']['mvaId']
      selection['bdtcut'] = cutWeightOptions['settings']['bdtcut']
      selection['mvaIdIndex'] = cuts_weights.cuts.vars.mvaIdIndex

   return selection
