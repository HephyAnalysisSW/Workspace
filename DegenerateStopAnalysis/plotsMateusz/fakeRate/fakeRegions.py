# fakeRegions.py
# Definition of regions used in fake rate estimation 
# Mateusz Zarucki 2017

import ROOT
import os, sys
from pprint import pprint
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass

def regions(region, lep, METcut = "40", MTcut = "30", lowPt = False, oneBin = False, removeTau = True, mtReg = None):

   #if lowPt:
   #   lowPtString = "_lowpt"
   #else:
   #   lowPtString = ""

   #filters
   filters = "Flag_Filters"
   if "measurement" in region: trigger = "(HLT_PFHT800 || HLT_PFJet450 || HLT_AK8PFJet450)"
   else: trigger = "1"
      
   #index
   index = {
      'loose':      "IndexLepGood_%s_loose[0]"%lep,
      'loose2':"Alt$(IndexLepGood_%s_loose[1],-999)"%lep,
      'tight':      "IndexLepGood_%s_def[0]"%lep,
      'tight2':"Alt$(IndexLepGood_%s_def[1],-999)"%lep,
   } 

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
      ], baseCut = None)
   
   sr1_CT200 = CutClass("SR1_CT200", [
      ["MET","met > 200"],
      ["HT","ht_basJet_def > 300"],
      ["ISR100", "nJet_isrHJet_def >= 1"],
      ["No3rdJet60","nJet_vetoJet_def <= 2"],
      ["antiQCD","dPhi_j1j2_vetoJet_def < 2.5"],
      ["BVeto", "nJet_bJet_def < 1"],
      ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
      ], baseCut = None)
   
   sr1_invertedAntiQCD = CutClass("SR1_invertedAntiQCD", [
      ["MET","met > 300"],
      ["HT","ht_basJet_def > 400"],
      ["ISR100", "nJet_isrHJet_def >= 1"],
      ["No3rdJet60", "nJet_vetoJet_def <= 2"],
      ["invAntiQCD", "(dPhi_j1j2_vetoJet_def > 2.5 || nJet_vetoJet_def <= 1)"], #or required for inclusion of monojet evts
      ["BVeto", "nJet_bJet_def < 1"],
      ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
      ], baseCut = None)
   
   sr1_invertedAntiQCD_CT200 = CutClass("SR1_invertedAntiQCD_CT200", [
      ["MET","met > 200"],
      ["HT","ht_basJet_def > 300"],
      ["ISR100", "nJet_isrHJet_def >= 1"],
      ["No3rdJet60","nJet_vetoJet_def <= 2"],
      ["invAntiQCD", "(dPhi_j1j2_vetoJet_def > 2.5 || nJet_vetoJet_def <= 1)"], #or required for inclusion of monojet evts
      ["BVeto", "nJet_bJet_def < 1"],
      ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
      ], baseCut = None)
   
   sr1_noAntiQCD = CutClass("SR1_noAntiQCD", [
      ["MET","met > 300"],
      ["HT","ht_basJet_def > 400"],
      ["ISR100", "nJet_isrHJet_def >= 1"],
      ["BVeto", "nJet_bJet_def < 1"],
      ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
      ], baseCut = None)
   
   sr1_noAntiQCD_CT200 = CutClass("SR1_noAntiQCD_CT200", [
      ["MET","met > 200"],
      ["HT","ht_basJet_def > 300"],
      ["ISR100", "nJet_isrHJet_def >= 1"],
      ["BVeto", "nJet_bJet_def < 1"],
      ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
      ], baseCut = None)
   
   selection = {
      'trigger': trigger, 
      'filters': filters, 
      'index': index,
      'fakeLoose':   "(LepGood_mcMatchId[{ind}] == 0 || LepGood_mcMatchId[{ind}] == 99 || LepGood_mcMatchId[{ind}] == 100)".format(ind = index['loose']),
      'fakeTight':   "(LepGood_mcMatchId[{ind}] == 0 || LepGood_mcMatchId[{ind}] == 99 || LepGood_mcMatchId[{ind}] == 100)".format(ind = index['tight']),
      'promptLoose': "(LepGood_mcMatchId[{ind}] != 0 && LepGood_mcMatchId[{ind}] != 99 && LepGood_mcMatchId[{ind}] != 100)".format(ind = index['loose']), 
      'promptTight': "(LepGood_mcMatchId[{ind}] != 0 && LepGood_mcMatchId[{ind}] != 99 && LepGood_mcMatchId[{ind}] != 100)".format(ind = index['tight']),
      'match': "(%s == %s)"%(index['loose'], index['tight']),
   }
    
   if "measurement" in region: selection['measurement'] = measurement
   elif "sr1" in region:       
      selection['application_sr1'] = selection['application_sr1a'] = selection['application_sr1b'] = selection['application_sr1c'] = sr1
      selection['application_sr1_CT200'] = sr1_CT200
      selection['application_sr1_noAntiQCD'] = sr1_noAntiQCD
      selection['application_sr1_noAntiQCD_CT200'] = sr1_noAntiQCD_CT200
      selection['application_sr1_invertedAntiQCD'] = sr1_invertedAntiQCD
      selection['application_sr1_invertedAntiQCD_CT200'] = sr1_invertedAntiQCD_CT200
   else:
      print "Region unknown. Exiting."
      sys.exit()
   
   if "measurement" in region:
      selection['loose'] = "(nLepGood_{lep}_loose > 0)".format(lep = lep) 
      selection['tight'] = "(nLepGood_{lep}_def > 0)".format(lep = lep)
   elif "sr1" in region: 
      #selection['loose'] =    "((nLepGood_{lep}_loose == 1 || (nLepGood_{lep}_loose == 2 && LepGood_pt[{ind2}] < 20)) && abs(LepGood_eta[{ind}]) < 1.5)".format(lep = lep, ind = index['loose'], ind2 = index['loose2']) #LepGood_pt[{ind}] < 30  
      #selection['tight'] =    "((nLepGood_{lep}_def == 1   || (nLepGood_{lep}_def == 2 &&   LepGood_pt[{ind2}] < 20)) && abs(LepGood_eta[{ind}]) < 1.5)".format(lep = lep, ind = index['tight'], ind2 = index['tight2']) #LepGood_pt[{ind}] < 30  
      selection['loose'] =    "(nLepGood_{lep}_loose == 1 && abs(LepGood_eta[{ind}]) < 1.5)".format(lep = lep, ind = index['loose'])
      selection['tight'] =    "(nLepGood_{lep}_def == 1   && abs(LepGood_eta[{ind}]) < 1.5)".format(lep = lep, ind = index['tight'])
      selection['notTight'] =  "(nLepGood_{lep}_loose != nLepGood_{lep}_def)".format(lep = lep) #(%s != %s)"%(index['loose'], index['tight']) #NOTE: when index array empty, evaluates incorrectly as zero

      #Veto on other leptons
      otherLepVeto = {}
      #otherLepVeto['loose'] = "(nLepGood_{otherLep}_loose == 0 || (nLepGood_{otherLep}_loose == 1 && LepGood_pt[Alt$(IndexLepGood_{otherLep}_loose[0],-999)] < 20))"
      #otherLepVeto['tight'] = "(nLepGood_{otherLep}_def == 0   || (nLepGood_{otherLep}_def == 1   && LepGood_pt[Alt$(IndexLepGood_{otherLep}_def[0],-999)] < 20))"
      otherLepVeto['loose'] = "(nLepGood_{otherLep}_loose == 0)"
      otherLepVeto['tight'] = "(nLepGood_{otherLep}_def == 0)"

      for x in ['loose', 'tight']:
         if lep == 'mu':
            otherLepVeto[x] = otherLepVeto[x].format(otherLep = 'el') 
         elif lep == 'el':
            otherLepVeto[x] = otherLepVeto[x].format(otherLep = 'mu') 
         elif lep == 'lep':
            otherLepVeto[x] = None
         
         if otherLepVeto[x]:
            selection[x] = combineCuts(selection[x], otherLepVeto[x])

      
      mtRegions = ['sr1a', 'sr1b', 'sr1c'] 
     
      mtRegion = [x for x in mtRegions if x in region]

      if len(mtRegion): 
         for x in ['loose', 'tight']:
            mtCuts = {
               'sr1a':"(LepGood_mt[{ind}] < 60 && (LepGood_pdgId[{ind}] == abs(LepGood_pdgId[{ind}])))".format(lep = lep, ind = index[x]), # or pdgId > 0
               'sr1b':"((LepGood_mt[{ind}] > 60) && (LepGood_mt[{ind}] < 95) && (LepGood_pdgId[{ind}] == abs(LepGood_pdgId[{ind}])))".format(lep = lep, ind = index[x]), # or pdgId > 0
               'sr1c':"(LepGood_mt[{ind}] > 95)".format(lep = lep, ind = index[x]),
             }
         
            selection[x] = combineCuts(selection[x], mtCuts[mtRegion[0]])

      print selection

   # Additonal selection to select one bin   
   if oneBin:
      for x in ['loose', 'tight']:
         selection[x] = combineCuts(selection[x], "(LepGood_pt[{ind}] > 30 && LepGood_pt[{ind}] < 50)".format(ind = index[x]))

   #remove Tau
   if removeTau:
      genCond = "(abs(GenPart_pdgId) == 15 && (abs(GenPart_motherId) == 24 || abs(GenPart_motherId) == 23 || (GenPart_motherId == -9999 && Iteration$ < 3)))"
      #genCond = "(abs(GenPart_pdgId) == 15 && (abs(GenPart_motherId) == 24 || abs(GenPart_motherId) == 23))"
      genCondFalse = "(Sum$(%s) == 0)"%genCond

      for x in ['loose', 'tight']:
         deltaR = "(sqrt((GenPart_eta - LepGood_eta[{ind}])^2 + (GenPart_phi - LepGood_phi[{ind}])^2))".format(ind = index[x])
         #deltaR = "(deltaR(GenPart_eta, LepGood_eta[{ind}], GenPart_phi, LepGood_phi[{ind}]))".format(ind = index[x])
         dRmin = "MinIf$(%s,%s)"%(deltaR, genCond)
         selection['noTau'+x.title()] = combineCuts("(nLepGood_{lep}_{x} > 0)".format(lep = lep, x = x).replace('tight', 'def'), "(({condFalse}) || (({dR}) > 0.15))".format(dR = dRmin, condFalse = genCondFalse))

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
      bins['pt'] = [0, 5, 12, 20, 30, 50, 100, xmax]
      bins['mt'] = [0, 30, 60, 95, 120, xmax]

      if lep == 'mu':
         bins['eta'] = [0, 0.9, 1.2, 2.1, etaAcc]
      elif lep == 'el':
         bins['eta'] = [0, 0.7, 1.5, etaAcc]
      else:
         bins['eta'] = [0, 0.9, 1.2, 1.5, 2.1, etaAcc]

   return bins
