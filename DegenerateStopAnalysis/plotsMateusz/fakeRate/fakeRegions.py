# fakeRegions.py
# Definition of regions used in fake rate estimation 
# Mateusz Zarucki 2017

import ROOT
import os, sys
from pprint import pprint
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass

def regions(region, lep, METcut = "40", MTcut = "30"):

   #filters
   filters = "Flag_Filters"
   if "measurement" in region: trigger = "HLT_PFHT800"
   else: trigger = "1"
      
   #index
   index = {'loose':"IndexLepGood_%s_loose[0]"%lep, 'tight':"IndexLepGood_%s_def[0]"%lep}
   
   pt = "LepGood_pt[%s]"%index['loose']
   eta = "abs(LepGood_eta[%s])"%index['loose']
   mt = "LepGood_mt[%s]"%index['loose']
    
   #Preselection & basic SR cuts
   measurement = CutClass("measurement", [
      ["HT","ht_basJet_def > 900"],
      ["MET","met < " + METcut],
      ["MT", mt + " < " + MTcut],
      ], baseCut = None)
   
   #Preselection & basic SR cuts
   sr1 = CutClass("SR1", [
      ["MET","met > 300"],
      ["HT","ht_basJet_def > 400"],
      ["ISR100", "nJet_isrHJet_def >= 1"],
      ["No3rdJet60","nJet_vetoJet_def <= 2"],
      ["antiQCD","dPhi_j1j2_vetoJet_def < 2.5"],
      ["BVeto", "nJet_bJet_def < 1"],
      ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
      #["MuVeto","(nLepGood_mu == 0 || (nLepGood_mu == 1 && LepGood_pt[IndexLepGood_mu[0]] < 20))"],
      ], baseCut = None)
   
   #setEventListToChains(samples, samplesList, baseline)
   
   selection = {
      'trigger': trigger, 
      'filters': filters, 
      'index': index,
      'looseFake': "(LepGood_mcMatchId[{ind}] == 0)".format(ind = index['loose']),
      'tightFake': "(LepGood_mcMatchId[{ind}] == 0)".format(ind = index['tight']),
      'match': "(%s == %s)"%(index['loose'], index['tight']),
   }

   if "measurement" in region: selection['measurement'] = measurement.combined
   elif "sr1" in region:       selection['application_sr1'] = sr1.combined
   else:
      print "Region unknown. Exiting."
      sys.exit()
   
   if "measurement" in region:
      selection['loose'] = "(nLepGood_{lep}_loose > 0)".format(lep = lep) 
      selection['tight'] = "(nLepGood_{lep}_def > 0)".format(lep = lep)
   elif "sr1" in region: 
      selection['loose'] = "((nLepGood_{lep}_loose == 1 && abs(LepGood_eta[{ind}]) < 1.5) || (nLepGood_{lep}_loose == 2 && LepGood_pt[IndexLepGood_{lep}_loose[1]] < 20))".format(lep = lep, ind = index['loose'])
      selection['tight'] = "((nLepGood_{lep}_def == 1 && abs(LepGood_eta[{ind}]) < 1.5) || (nLepGood_{lep}_def == 2 && LepGood_pt[IndexLepGood_{lep}_def[1]] < 20))".format(lep = lep, ind = index['tight'])

   return selection

##Yields
#if doYields:
#   selList['loose'] = [filters, selection[region], selection['loose']] 
#   selList['tight'] = selList['loose'][:]
#   selList['tight'].extend([selection['tight'], selection['match']]) 
#   
#   selClass = {}
#   selClass['loose'] = CutClass("loose", [["loose", combineCutsList(selList['loose'])]], baseCut = None)
#   selClass['tight'] = CutClass("tight", [["tight", combineCutsList(selList['tight'])]], baseCut = None)
#   
#   yields = {}
#   
#   yields['loose'] = Yields(samples, samplesList, selClass['loose'], cutOpt = "combinedList", pklOpt = False, tableName = "loose", nDigits = 2, err = True, verbose = True, nSpaces = 1)
#   yields['tight'] = Yields(samples, samplesList, selClass['tight'], cutOpt = "combinedList", pklOpt = False, tableName = "tight", nDigits = 2, err = True, verbose = True, nSpaces = 1)

#   #nBin['cmg'][bin] = getYieldFromChain(t1, skimString, "1")
#   
#   for samp in samplesList:
#      print "***"
#      print "Sample: ", samp
#      print "Using Yields class:"
#      print "L Entries (Yields):"
#      pprint(yields['loose'].yieldDictFull[samp])
#      print "From Histogram::"
#      print "L Entries (Hist): ", hists['loose']['pt'][samp].Integral(0, 100000)
#      print "T Entries (Hist): ", hists['tight']['pt'][samp].Integral(0, 100000)

#if doYields: 
#   print "Sample: data-EWK"
#   print "L Entries (Hist)", hists['loose']['pt']['data-EWK'].Integral(0, 1000)
#   print "T Entries (Hist)", hists['tight']['pt']['data-EWK'].Integral(0, 1000)
#   print "***"

