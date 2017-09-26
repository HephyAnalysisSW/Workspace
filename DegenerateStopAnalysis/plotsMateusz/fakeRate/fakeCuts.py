# fakeCuts.py
# Definition of regions used in fake rate estimation 
# Mateusz Zarucki 2017

import sys
import copy
from Workspace.DegenerateStopAnalysis.tools.degCuts2 import Cuts, CutsWeights
from Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo import cutWeightOptions, triggers, filters 

def fakeCuts(samples, region, lep, WP, cutWeightOptions = cutWeightOptions, ptInclusive = True, eta1p5 = None, considerFakeTaus = 1, mva = False, VR = None, invAntiQCD = False, noAntiQCD = False, ptBin = None, noWttWeights = False, highWeightVeto = True):
   
   if not ("application" in region or "measurement" in region):   
      print "Region unknown. Exiting."
      sys.exit()

   #  cutWeightOptions format:
   #  cutWeightOptions['def_weights'] = ['weight', 'DataBlind_lumi']
   #  cutWeightOptions['options']     = ['isr', 'sf', 'pu', 'isr_tt', 'wpt', 'trig_eff']
   #  cutWeightOptions['settings'] = {
   #         'lepCol': "LepGood",
   #         'lep':    "lep",
   #         'lepTag': "def",
   #         'jetTag': "def",
   #         'btagSF': "SF",
   #         'mvaId':  None,
   #         'bdtcut_sr': None,
   #         'bdtcut_cr': None,
   #         'lumis' : lumis,
   #     }
   
   # Data
   dataset = None

   if 'dblind' in samples.keys():
      dataset = samples['dblind'].name
   else:
      for samp in samples:
         if (samples[samp].isData and not "Unblind" in samples[samp].name):
            dataset = samples[samp].name 
            break
  
   ### Options ###
   
   cutWeightOptions['def_weights'] = ['weight']

   if not (dataset and 'application' in region) and 'trig_eff' in cutWeightOptions['options']: cutWeightOptions['options'].remove('trig_eff') # NOTE: MET trigger efficiency not applicable for the measurement regions
 
   if noWttWeights:
      if 'wpt'    in cutWeightOptions['options']: cutWeightOptions['options'].remove('wpt')
      if 'isr_tt' in cutWeightOptions['options']: cutWeightOptions['options'].remove('isr_tt')
 
   # Default: 
   #cutWeightOptions['settings']['lepCol'] = "LepGood"
   #cutWeightOptions['settings']['btagSF'] = "SF"
   
   if dataset: 
      cutWeightOptions['def_weights'].append(dataset + '_lumi')
      cutWeightOptions['settings']['lumis']['target_lumi'] = cutWeightOptions['settings']['lumis'][dataset + '_lumi']
   else:
      cutWeightOptions['def_weights'].append('DataBlind_lumi')

   if mva:
      cutWeightOptions['settings']['mvaId'] = '30' #MVA Set 
      cutWeightOptions['settings']['bdtcut_sr'] = '0.4' #33' #0.36
      cutWeightOptions['settings']['bdtcut_cr'] = '0.2' #33' #0.36
   
   cutWeightOptions['settings']['lep'] = lep 

   if "measurement1" in region:
      cutWeightOptions['options'].append('trig_mc_jet')
   elif "measurement2" in region or "measurement3" in region:
      cutWeightOptions['options'].append('trig_mc_lep')
   elif "measurement4" in region:
      cutWeightOptions['options'].append('trig_mc_%s'%lep)

   # Working points
   #if lep == 'mu':
   map_WP_suff = {'loose':'loose_lowpt', 'tight':'lowpt'} #NOTE: using lowpt tag for both muons and electrons
   cutWeightOptions['settings']['lepTag'] = map_WP_suff[WP]
   cutWeightOptions['settings']['tightWP'] = '_lowpt'

   #else: 
   #   map_WP_suff = {'loose':'loose', 'tight':'def'}
   #   cutWeightOptions['settings']['lepTag'] = map_WP_suff[WP]
   
   if "measurement2" in region:
      alt_vars = {'lepIndex1':   {'var':'Index{lepCol}_lep_%s[1]'%map_WP_suff[WP],   'latex':''}} # considering 2nd lepton as main lepton
   elif "measurement3" in region: 
      alt_vars = {'lepIndex1':   {'var':'Index{lepCol}_lep_%s[2]'%map_WP_suff[WP],   'latex':''}} # considering 3rd lepton as main lepton
   elif not "measurement" in region: # application region 
      alt_vars = {'lepIndex_veto':{'var':'Index{lepCol}_lep_%s'%map_WP_suff['tight'], 'latex':''}} # for correct lepton veto 
   else:
      alt_vars = {}

   #alt_vars.update({'tagIndex1':{'var':'Index{lepCol}_%s_%s'%(lep, map_WP_suff['tight']), 'latex':''}})
   #alt_vars = {'lepIndex1':   {'var':'Index{lepCol}_lep_%s[1]'%map_WP_suff[WP],   'latex':''}} # considering 2nd lepton as main lepton

   # NOTE: Implemented with the loose lepTag 
   #alt_vars = {'lepIndex1':     {'var':'Index{lepCol}_{lep}_%s[0]'%map_WP_suff[WP], 'latex':''},
   #            'lepIndex1_lep': {'var':'Index{lepCol}_lep_%s[0]'%map_WP_suff[WP],   'latex':''},
   #            'nLep':         {'var': 'n{lepCol}_{lep}_%s'%map_WP_suff[WP],       'latex':''}}

   ### Cuts and Weights ###
         
   cuts_weights = CutsWeights(samples, cutWeightOptions, alternative_vars = alt_vars)
   
   # Region
   regDefs = {}

   regDefs['base'] = region.replace('application_', '').replace('_bVeto', '').replace('_bTag', '') # region definition with all cuts
   regDefs['kinDef'] = regDefs['base'].replace('_bVeto', '').replace('_bTag', '') + '_kin'         # region definition only with kinematic cuts (for evt lists)

   if   'sr1' in regDefs['kinDef']: regDefs['kinDef'] = 'sr1_kin'    
   elif 'sr2' in regDefs['kinDef']: regDefs['kinDef'] = 'sr2_kin'    
   
   regDefs['regDef'] = regDefs['base'] 
  
   if lep == "mu":
      cuts_weights.cuts.regions[regDefs['regDef']]['cuts'].append('lepPt_gt_3p5')
  
   if mva: ptInclusive = False # NOTE: focus on pT < 30 GeV only
 
   # pT inclusive application region 
   if "application" in region and ptInclusive:
  
      regDefs['regDef'] = cuts_weights.cuts.removeCut(regDefs['regDef'], 'lepPt_lt_30')

      if VR and not mva:
         for d in regDefs.keys(): 
            regDefs[d] = cuts_weights.cuts.removeCut(regDefs[d], 'CT300')
            regDefs[d] = cuts_weights.cuts.removeCut(regDefs[d], 'MET300')
            regDefs[d] = cuts_weights.cuts.removeCut(regDefs[d], 'ISR325')
            
            if 'sr2' in regDefs[d] and VR == "CT200": 
               regDefs[d] = cuts_weights.cuts.addCut(regDefs[d], 'CT2_200')
            else:
               regDefs[d] = cuts_weights.cuts.addCut(regDefs[d], VR)

      if invAntiQCD or noAntiQCD:
         for d in regDefs.keys(): 
            regDefs[d] = cuts_weights.cuts.removeCut(regDefs[d], 'AntiQCD')
         if invAntiQCD:
            regDefs[d] = cuts_weights.cuts.addCut(regDefs[d], 'invAntiQCD')
   
   elif "measurement" in region:
      if 'bTag' in region: 
         regDefs['regDef'] = cuts_weights.cuts.addCut(regDefs['regDef'], 'B1p')
      elif 'bVeto' in region:
         regDefs['regDef'] = cuts_weights.cuts.addCut(regDefs['regDef'], 'B0')

   # common MR + AR modifications
   if eta1p5 == "lt":
      regDefs['regDef'] = cuts_weights.cuts.addCut(regDefs['regDef'], 'lepEta_lt_1p5')
   elif eta1p5 == "gt":
      regDefs['regDef'] = cuts_weights.cuts.addCut(regDefs['regDef'], 'lepEta_gt_1p5')

   if considerFakeTaus:
      cuts_weights.cuts.cuts_dict_orig['prompt']['cut'] = "(%s) || (%s == 1)"%(cuts_weights.cuts.cuts_dict_orig['prompt']['cut'], cuts_weights.cuts.vars.isFakeFromTau1)
      cuts_weights.cuts.cuts_dict_orig['fake']['cut'] =   "(%s) && (%s == 0)"%(cuts_weights.cuts.cuts_dict_orig['fake']['cut'], cuts_weights.cuts.vars.isFakeFromTau1)

   if ptBin:
      if type(ptBin) != type([]):
         print "Wrong input for ptBin. Requires tuple. Exiting"
         sys.exit()
      cuts_weights.cuts.cuts_dict_orig['ptBin']['cut'] = "({lepPt} > {low}) && ({lepPt} < {high})".format(lepPt = cuts_weights.cuts.vars.lepPt, low = ptBin[0], high = ptBin[1]) 
      regDefs['regDef'] = cuts_weights.cuts.addCut(regDefs['regDef'], 'ptBin')

   if highWeightVeto: 
      regDefs['regDef'] = cuts_weights.cuts.addCut(regDefs['regDef'], 'highWeightVeto')

   # L!T
   if "application" in region and WP == "loose":  
      regDefs['regDef_notTight'] = cuts_weights.cuts.addCut(regDefs['regDef'], 'notTight')

   # Splitting into prompt and fakes
   for x in ['prompt', 'fake']: 
      cuts_weights.cuts.addCut(regDefs['regDef'], x)
      
      # L!T
      if "application" in region and WP == "loose": 
         cuts_weights.cuts.addCut(regDefs['regDef_notTight'], x)
   
   # Updating all cuts classes
   cuts_weights.cuts._update(reset = False)
   cuts_weights._update()
   
   # Triggers
   if "measurement1" in region: 
      trigger = triggers['data_jet'] 
   elif "measurement2" in region or "measurement3" in region: 
      trigger = triggers['data_lep']
   elif "measurement4" in region:
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
   
   selection[WP]['lepIndex1'] = cuts_weights.cuts.vars_dict_format['lepIndex1']
   
   if "measurement2" in region or "measurement3" in region:
      selection[WP]['tagIndex1'] = cuts_weights.cuts.vars_dict_format['tagIndex1']
      if "measurement3" in region:
         selection[WP]['tagIndex2'] = cuts_weights.cuts.vars_dict_format['tagIndex2']
 
   selection['regDefs'] = regDefs
   selection[WP]['cuts_weights'] = cuts_weights
   selection[WP]['cuts'] = cuts_weights.cuts
   selection[WP][region] = cuts_weights.cuts_weights[regDefs['regDef']]
   selection['kinematic'][region] = cuts_weights.cuts.cutInsts[regDefs['kinDef']]
   
   if mva: 
      selection['mvaId'] = cutWeightOptions['settings']['mvaId']
      selection['bdtcut_sr'] = cutWeightOptions['settings']['bdtcut_sr']
      selection['bdtcut_cr'] = cutWeightOptions['settings']['bdtcut_cr']
      selection['mvaIdIndex'] = cuts_weights.cuts.vars.mvaIdIndex

   return selection
