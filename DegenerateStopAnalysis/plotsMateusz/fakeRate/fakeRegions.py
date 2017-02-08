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

   cutWeightOptions['options'] = ['isr'] #TODO: add 'sf' 
   
   cutWeightOptions['settings']['lepCol'] = lepCol

   if mva:
      cutWeightOptions['settings']['mvaId'] = '30' 
      cutWeightOptions['settings']['bdtcut'] = '0.10'
   
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
   
   # Indicies
   index = {}
   index[WP] =     "Index{lepCol}_{lep}_{suff}[0]".format(lepCol = lepCol, lep = lep, suff = map_WP_suff[WP])
   index[WP+'2'] = "Alt$(Index{lepCol}_{lep}_{suff}[1], -999)".format(lepCol = lepCol, lep = lep, suff = map_WP_suff[WP])

   selection[WP]['index'] = index[WP]
   
   selection[WP]['fake'] =   "({lepCol}_mcMatchId[{ind}] == 0 || {lepCol}_mcMatchId[{ind}] == 99 || {lepCol}_mcMatchId[{ind}] == 100)".format(lepCol = lepCol, ind = index[WP])
   selection[WP]['prompt'] = "({lepCol}_mcMatchId[{ind}] != 0 && {lepCol}_mcMatchId[{ind}] != 99 && {lepCol}_mcMatchId[{ind}] != 100)".format(lepCol = lepCol, ind = index[WP])
   
   # Measurement Region Cuts
   if "measurement" in region:
   
      mt = "{lepCol}_mt[{ind}]".format(lepCol = lepCol, ind = index[WP])
  
      measurement = {}
 
      measurement['kinematic'] = CutClass("measurement_kinematic", [
         ["HT","ht_basJet_def > 900"],
         ["MET","met < 40"],
         ], baseCut = None)
         
      selection['kinematic'][region] = measurement['kinematic'] 
      
      measurement['total'] = CutClass("measurement", [
         ["MT", mt + " < 30"],
         ], baseCut = measurement['kinematic'])

      selection[WP][region] = combineCuts(measurement['total'].combined, "(n{lepCol}_{lep}_{suff} > 0)".format(lepCol = lepCol, lep = lep, suff = map_WP_suff[WP]))

   # Application Region Cuts
   elif "application" in region: 
      # Getting all cuts and weights
      cuts_weights = CutsWeights(samples, cutWeightOptions)
      cuts = cuts_weights.cuts 
      cuts_weights._update(samples, cuts, nMinus1 = ['{lepCol}_pt'.format(lepCol = lepCol)]) #NOTE: removes lepton pT cuts (NOTE:including veto!) 
      selection[WP]['cuts_weights'] = cuts_weights
      
      selection[WP][region] = cuts_weights.cuts_weights[region.replace('application_', '')]
      
      # Kinematic cuts only (for event lists) 
      cuts_weights_kinematic = CutsWeights(samples, cutWeightOptions)
      cuts_weights_kinematic._update(samples, cuts, nMinus1 = [lepCol]) #NOTE: removes all leptonic cuts 
      cuts_weights_kinematic_dict = cuts_weights_kinematic.cuts_weights[region.replace('application_', '')]
      selection['kinematic'][region] = CutClass(region + "_kinematic", [[region + "_kinematic", cuts_weights_kinematic_dict[cuts_weights_kinematic_dict.keys()[0]][0]]], baseCut = None) # converts into CutClass

      #Allowing for extra soft lepton
      extraSoftLep = {}
      extraSoftLep[WP] =  "(n{lepCol}_{lep}_{suff} == 1 || (n{lepCol}_{lep}_{suff} == 2 && {lepCol}_pt[{ind2}] < 20))".format(lepCol = lepCol, lep = lep, suff = map_WP_suff[WP], ind2 = index[WP+'2'])
         
      selection[WP]['extraSoftLep'] = extraSoftLep[WP]
      for samp in selection[WP][region]:
         selection[WP][region][samp] = list(selection[WP][region][samp]) 
         selection[WP][region][samp][0] = combineCuts(selection[WP][region][samp][0], extraSoftLep[WP])
         selection[WP][region][samp] = tuple(selection[WP][region][samp]) 

      #Veto on other leptons
      otherLepVeto = {}
      otherLepVeto[WP] = "(n{lepCol}_{otherLep}_{suff} == 0 || (n{lepCol}_{otherLep}_{suff} == 1 && {lepCol}_pt[Alt$(Index{lepCol}_{otherLep}_{suff}[0],-999)] < 20))"
      #otherLepVeto['loose'] = "(nLepGood_{otherLep}_loose == 0)"
      #otherLepVeto['tight'] = "(nLepGood_{otherLep}_def == 0)"

      if lep == 'mu':
         otherLepVeto[WP] = otherLepVeto[WP].format(lepCol = lepCol, otherLep = 'el', suff = map_WP_suff[WP])
      elif lep == 'el':
         otherLepVeto[WP] = otherLepVeto[WP].format(lepCol = lepCol, otherLep = 'mu', suff = map_WP_suff[WP])
      elif lep == 'lep':
         otherLepVeto[WP] = None

      if otherLepVeto[WP]:
         selection[WP]['otherLepVeto'] = otherLepVeto[WP]
         for samp in selection[WP][region]:
            selection[WP][region][samp] = list(selection[WP][region][samp]) 
            selection[WP][region][samp][0] = combineCuts(selection[WP][region][samp][0], otherLepVeto[WP])
            selection[WP][region][samp] = tuple(selection[WP][region][samp]) 

   else:
      print "Region unknown. Exiting."
      sys.exit()

   if WP == "loose": 
      selection[WP]['notTight'] =  "(n{lepCol}_{lep}_{suff1} != n{lepCol}_{lep}_{suff2})".format(lepCol = lepCol, lep = lep, suff1 = map_WP_suff['loose'], suff2 = map_WP_suff['tight']) #(%s != %s)"%(index['loose'], index['tight']) #NOTE: when index array empty, evaluates incorrectly as zero

   # Additonal selection to select one bin   
   if oneBin:
      selection[WP][region] = combineCuts(selection[WP][region], "({lepCol}_pt[{ind}] > 30 && {lepCol}_pt[{ind}] < 50)".format(lepCol = lepCol, ind = index[WP]))

   #remove Tau
   if removeTau:
      genCond = "(abs(GenPart_pdgId) == 15 && (abs(GenPart_motherId) == 24 || abs(GenPart_motherId) == 23 || (GenPart_motherId == -9999 && Iteration$ < 3)))"
      genCondFalse = "(Sum$(%s) == 0)"%genCond

      deltaR = "(deltaR(GenPart_eta, {lepCol}_eta[{ind}], GenPart_phi, {lepCol}_phi[{ind}]))".format(lepCol = lepCol, ind = index[WP])
      dRmin = "MinIf$(%s,%s)"%(deltaR, genCond)
      selection[WP]['noTau'] = combineCuts("(n{lepCol}_{lep}_{suff} > 0)".format(lepCol = lepCol, lep = lep, suff = map_WP_suff[WP]), "(({condFalse}) || (({dR}) > 0.15))".format(dR = dRmin, condFalse = genCondFalse))

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
