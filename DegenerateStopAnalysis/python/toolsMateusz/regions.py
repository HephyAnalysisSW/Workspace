#regions.py
import math
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, splitCutInPt
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeLine
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *

less = lambda var, val: "(%s < %s)"%(var,val)
more = lambda var, val: "(%s > %s)"%(var,val)
btw = lambda var, minVal, maxVal: "(%s > %s && %s < %s)"%(var, min(minVal, maxVal), var, max(minVal, maxVal))
minAngle = lambda phi1, phi2 : "TMath::Min((2*pi) - abs({phi1}-{phi2}) , abs({phi1}-{phi2}))".format(phi1 = phi1, phi2 = phi2)  

#Signal regions
def signalRegions(lepton, index = ""):
   if lepton == "electron":
      pdgId = "11"
      if index == "2": ind = "IndexLepAll_el2[0]"
      else: ind = "IndexLepAll_el[0]"
   elif lepton == "muon":
      pdgId = "13"
      if index == "2": ind = "IndexLepAll_mu2[0]"
      else: ind = "IndexLepAll_mu[0]"
   else:
      assert False

   SRs = {\
      #'SR1':["SR1","LepAll_pt[" + ind + "] < 30"],
      'SR1a':["SR1a",   combineCuts("LepAll_pdgId[" + ind + "] == " + pdgId, "LepAll_mt[" + ind + "] < 60", "LepAll_pt[" + ind + "] < 30")],
      'SR1b':["SR1b",   combineCuts("LepAll_pdgId[" + ind + "] == " + pdgId, btw("LepAll_mt[" + ind + "]", 60, 95), "LepAll_pt[" + ind + "] < 30")],
      'SR1c':["SR1c",   combineCuts("LepAll_mt[" + ind + "] > 95", "LepAll_pt[" + ind + "] < 30")],

      'SRL1':["SRL1", btw("LepAll_pt[" + ind + "]", 5, 12)],
      'SRH1':["SRH1", btw("LepAll_pt[" + ind + "]", 12, 20)],
      'SRV1':["SRV1", btw("LepAll_pt[" + ind + "]", 20, 30)],

      'SRL1a':["SRL1a", combineCuts("LepAll_pdgId[" + ind + "] == " + pdgId, "LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 5, 12))],
      'SRH1a':["SRH1a", combineCuts("LepAll_pdgId[" + ind + "] == " + pdgId, "LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 12, 20))],
      'SRV1a':["SRV1a", combineCuts("LepAll_pdgId[" + ind + "] == " + pdgId, "LepAll_mt[" + ind + "] < 60", btw("LepAll_pt[" + ind + "]", 20, 30))],

      'SRL1b':["SRL1b", combineCuts("LepAll_pdgId[" + ind + "] == " + pdgId, btw("LepAll_mt[" + ind + "]", 60, 95), btw("LepAll_pt[" + ind + "]", 5, 12))],
      'SRH1b':["SRH1b", combineCuts("LepAll_pdgId[" + ind + "] == " + pdgId, btw("LepAll_mt[" + ind + "]", 60, 95), btw("LepAll_pt[" + ind + "]", 12, 20))],
      'SRV1b':["SRV1b", combineCuts("LepAll_pdgId[" + ind + "] == " + pdgId, btw("LepAll_mt[" + ind + "]", 60, 95), btw("LepAll_pt[" + ind + "]", 20, 30))],

      'SRL1c':["SRL1c", combineCuts("LepAll_mt[" + ind + "] > 95", btw("LepAll_pt[" + ind + "]", 5, 12))],
      'SRH1c':["SRH1c", combineCuts("LepAll_mt[" + ind + "] > 95", btw("LepAll_pt[" + ind + "]", 12, 20))],
      'SRV1c':["SRV1c", combineCuts("LepAll_mt[" + ind + "] > 95", btw("LepAll_pt[" + ind + "]", 20, 30))]}

   SRs['SR1'] = ["SR1", "(" + SRs['SR1a'][1] + ") || (" + SRs['SR1b'][1] + ") || (" + SRs['SR1c'][1] + ")"]

   return SRs

def cutClasses(eleIDsel, ID = "standard"):
   if not eleIDsel: 
      print makeLine() 
      print "No electron selection. Exiting."
      print makeLine() 
      exit()
      
   if ID == "MVA": WPs = ['None', 'WP80', 'WP90']
   else: WPs = ['None', 'Veto', 'Loose', 'Medium', 'Tight']
   
   allCuts = {iWP:{} for iWP in WPs}

   ###############No selection################
   nosel = CutClass("nosel", [["true", "1"]], baseCut=None)
   
   ###############Preselection################
   
   #Common preselection between electrons and muons
   presel = CutClass("presel", [
                               ["MET200","met > 200"],
                               ["HT300","ht_basJet > 300"],
                               ["ISR110","nIsrJet >= 1"],
                               ["No3rdJet60","nVetoJet <= 2"],
                               ["AntiQCD", "vetoJet_dPhi_j1j2 < 2.5"], # monojet
                               ["1El-2ndEl20Veto", "(nLepGood_el == 1 || (nLepGood_el == 2 && LepGood_pt[IndexLepGood_el[1]] < 20))"],
                               ["MuVeto","(nLepGood_mu ==0 || (nLepGood_mu==1 && LepGood_pt[IndexLepGood_mu[0]] < 20))"],
                               ["TauVeto","(Sum$(TauGood_idMVANewDM && TauGood_pt > 20 ) == 0)"],
                               ], baseCut=None)
   
   #SR1
   sr1 = {}
   mtabc = {}
   mtabc_ptbin = {}
   sr1Loose = {}
   sr1abc = {}
   sr1abc_ptbin = {}
   #SR2
   sr2 = {}
   sr2_ptbin = {}
   #CR1
   cr1 = {}
   cr1Loose = {}
   cr1abc = {}
   crtt2 = {}
   #CR2
   cr2 = {}
   cr2_ = {}
   
   #RunI 
   runI = {}
   runIflow = {}

   #Combined 
   regions_sr1 = {}
   regions_sr2 = {}
   regions_cr1 = {}
   regions_cr2 = {}
      
   allCuts['None']['nosel'] = nosel
   allCuts['None']['presel'] = presel
   
   #Dictionaries for different WPs 
   preselEle = {}
   electronSel = {}  
   elePt = {}
   absEleEta = {} 
   eleMt = {} 
   
   for iWP in WPs:
      electronSel[iWP] = "(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && (" + eleIDsel[iWP] + "))"
      elePt[iWP] = "Max$(LepGood_pt*(" + electronSel[iWP] + "))"
      absEleEta[iWP] = "Max$(abs(LepGood_eta*(" + electronSel[iWP] + ")))" #absolute value
      eleMt[iWP] = "Max$(LepGood_mt*(" + electronSel[iWP] + "))"
      #elePhi[iWP] = "Max$(LepGood_phi*(" + electronSel[iWP] + "))"
      #eleMt[iWP] = "Max$(sqrt(2*met*{pt}*(1 - cos(met_phi - LepGood_phi)))*(LepGood_pt == {pt}))".format(pt=elePt[iWP]) #%(elePt[iWP], elePhi[iWP], elePt[iWP])
      #eleMt[iWP] = "Max$(sqrt(2*met*%s*(1 - cos(met_phi - %s)))*(LepGood_pt == %s))"%(elePt[iWP], elePhi[iWP], elePt[iWP])
 
      ##################Electron Preselection###########
      
      preselEle[iWP] = CutClass("preselEle_" + iWP, [
                              ["oneEle", "Sum$(" + electronSel[iWP] + ") == 1"], # single electron
                              #["pt>7", "Sum$(" + elePt[iWP] + " > 7) == 1"], # pt > 7
                              ], baseCut=presel)
   
      ##################Signal Regions##################
   
      #SR1
      sr1[iWP] = CutClass("SR1_" + iWP, [
                              ["CT300","min(met, ht_basJet - 100) > 300"],
                              ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
                              #["negEle", "Max$(LepGood_pdgId*(" + electronSel[iWP] + ")) == 11"],
                              ["absEleEta1.5", absEleEta[iWP] + " < 1.5"],
                              ["elePt<30", elePt[iWP] + " < 30"],
                              ], baseCut = preselEle[iWP])
                              #["400","ht_basJet>400"],
                              #["met300","met>300"],
   
      #sr1abc[iWP] = CutClass("SR1abc_" + iWP,[
      #                        ["SR1a", eleMt[iWP] + " < 60"],
      #                        ["SR1b", btw(eleMt[iWP], 60, 88)],
      #                        ["SR1c", eleMt[iWP] + " > 88"]
      #                        ], baseCut = sr1[iWP])
   
      sr1abc_ptbin[iWP] = CutClass("SR1abc_ptbin_" + iWP, [
                              #["SR1a", eleMt[iWP] + " < 60"],
                              ["SRL1a", combineCuts(eleMt[iWP] + " < 60", btw(elePt[iWP], 5, 12), "Max$(LepGood_pdgId*(" + electronSel[iWP] + ")) == 11")],
                              ["SRH1a", combineCuts(eleMt[iWP] + " < 60", btw(elePt[iWP], 12, 20), "Max$(LepGood_pdgId*(" + electronSel[iWP] + ")) == 11")],
                              ["SRV1a", combineCuts(eleMt[iWP] + " < 60", btw(elePt[iWP], 20, 30), "Max$(LepGood_pdgId*(" + electronSel[iWP] + ")) == 11")],
                              #["SR1b",btw(eleMt[iWP], 60, 88)],
                              ["SRL1b", combineCuts(btw(eleMt[iWP], 60, 95), btw(elePt[iWP], 5, 12), "Max$(LepGood_pdgId*(" + electronSel[iWP] + ")) == 11")],
                              ["SRH1b", combineCuts(btw(eleMt[iWP], 60, 95), btw(elePt[iWP], 12, 20), "Max$(LepGood_pdgId*(" + electronSel[iWP] + ")) == 11")],
                              ["SRV1b", combineCuts(btw(eleMt[iWP], 60, 95), btw(elePt[iWP], 20, 30), "Max$(LepGood_pdgId*(" + electronSel[iWP] + ")) == 11")],
                              #["SR1c",eleMt[iWP] + " > 88"],
                              ["SRL1c", combineCuts(eleMt[iWP] + " > 95", btw(elePt[iWP], 5, 12))],
                              ["SRH1c", combineCuts(eleMt[iWP] + " > 95", btw(elePt[iWP], 12, 20))],
                              ["SRV1c", combineCuts(eleMt[iWP] + " > 95", btw(elePt[iWP], 20, 30))]
                              ], baseCut = sr1[iWP])
      
      #mtabc[iWP] = CutClass ("MTabc_" + iWP, [
      #                        ["MTa", eleMt[iWP] + " < 60"],
      #                        ["MTb", btw(eleMt[iWP], 60, 88)],
      #                        ["MTc", eleMt[iWP] + " > 88"]
      #                        ], baseCut = sr1[iWP])
      # 
      #mtabc_ptbin[iWP] = splitCutInPt(mtabc[iWP])
   
      #SR2
      sr2[iWP] = CutClass("SR2_" + iWP, [
                              ["ISR325", "nIsrHJet > 0"],
                              ["MET300", "met > 300"],
                              ["SoftBJet", "nBSoftJet >= 1"],# && nBHardJet == 0"],
                              ["elePt<30", elePt[iWP] + " < 30"]
                              ], baseCut = preselEle[iWP])
      
      sr2_ptbin[iWP] = CutClass("SR2_PtBinned_" + iWP, [
                              ["SRL2", btw(elePt[iWP], 5, 12)],
                              ["SRH2", btw(elePt[iWP], 12, 20)],
                              ["SRV2", btw(elePt[iWP], 20, 30)]
                              ], baseCut = sr2[iWP])
   
      ##################Control Regions##################
   
      #CR1
      cr1[iWP] = CutClass("CR1_" + iWP, [
                              ["CT300","min(met, ht_basJet - 100) > 300"],
                              ["BVeto","nBSoftJet == 0 && nBHardJet == 0"],
                              ["negEle", "Max$(LepGood_pdgId*(" + electronSel[iWP] + ")) == 11"],
                              ["absEleEta1.5", absEleEta[iWP] + " < 1.5"],
                              ["elePt>30", elePt[iWP] + " > 30"], #greater than
                              ], baseCut = preselEle[iWP])
                              #["BVeto_Medium25","nBJetMedium25==0"],
                              #["400 ","ht_basJet>400"],
                              #["met300","met>300"],
     
      #cr1Loose[iWP] = CutClass("CR1Loose_" + iWP, [ # no CT cut
      #                        ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
      #                        ["negEle", "LepGood_pdgId == 11"],
      #                        ["absEleEta1.5", absEleEta[iWP] + " < 1.5"],
      #                        ["elePt>30", elePt[iWP] + " > 30"], #greater than
      #                        ], baseCut= preselEle[iWP])
      
      cr1abc[iWP] = CutClass("CR1abc_" + iWP, [
                              ["CR1a", eleMt[iWP] + " < 60"],
                              ["CR1b", btw(eleMt[iWP], 60, 88)],
                              ["CR1c", eleMt[iWP] + " > 88"]
                              ], baseCut = cr1[iWP])
      
      #CR2 
      cr2[iWP] = CutClass("CR2_" + iWP, [
                              ["OneOrMoreSoftB","nBSoftJet >= 1"],
                              ["noHardB", "nBHardJet == 0"],
                              ["Jet325", "nIsrHJet > 0"],
                              ["elePt>30", elePt[iWP] + " > 30"], #greater than
                              ], baseCut = preselEle[iWP])
                              #["met300","met>300"],
      
      cr2_[iWP] = CutClass("CR2_" + iWP, [
                              ["CR2", "(1)"]
                              ], baseCut = cr2[iWP])
      
      #CRTT2
      crtt2[iWP] = CutClass("CRTT2_" + iWP, [
                              ["CRTT2","((nBSoftJet + nBHardJet) > 1) && nBHardJet > 0"]
                              ], baseCut= preselEle[iWP])
      

      regions_sr1[iWP] = {'sr1': sr1[iWP], 'sr1abc_ptbin': sr1abc_ptbin[iWP], } #'sr1Loose': sr1Loose[iWP], 'sr1abc': sr1abc[iWP], 'mtabc': mtabc[iWP], 'mtabc_ptbin': mtabc_ptbin[iWP]
      regions_sr2[iWP] = {'sr2': sr2[iWP], 'sr2_ptbin': sr2_ptbin[iWP]}
      regions_cr1[iWP] = {'cr1': cr1[iWP], 'cr1abc': cr1abc[iWP]} #'cr1Loose': cr1Loose[iWP],
      regions_cr2[iWP] = {'cr2': cr2[iWP], 'crtt2': crtt2[iWP]}

      runI[iWP] = CutClass("RunI_Ele_" + iWP, [] , baseCut = preselEle[iWP])
      runI[iWP].add(sr1abc_ptbin[iWP], baseCutString = sr1[iWP].inclCombined)
      runI[iWP].add(sr2_ptbin[iWP], baseCutString = sr2[iWP].inclCombined)
      runI[iWP].add(cr1abc[iWP], baseCutString = cr1[iWP].inclCombined)
      runI[iWP].add(cr2_[iWP], baseCutString = cr2[iWP].inclCombined)
      runI[iWP].add(crtt2[iWP])
   
      runIflow[iWP] = CutClass("RunI_Ele_Flow_" + iWP, [], baseCut = None)
      runIflow[iWP].add(preselEle[iWP], 'flow', baseCutString = None)
      runIflow[iWP].add(sr1[iWP], 'inclFlow', baseCutString = preselEle[iWP].combined)
      runIflow[iWP].add(sr2[iWP], 'inclFlow', baseCutString = preselEle[iWP].combined)
      
      allCuts[iWP]['eleID_' + iWP] = eleIDsel[iWP]
      allCuts[iWP]['eleSel'] = electronSel[iWP] 
      allCuts[iWP]['preselEle'] = preselEle[iWP]  
      allCuts[iWP]['runI'] = runI[iWP]  
      allCuts[iWP]['runIflow'] = runIflow[iWP]  
      allCuts[iWP].update(regions_sr1[iWP])
      allCuts[iWP].update(regions_sr2[iWP])
      allCuts[iWP].update(regions_cr1[iWP])
      allCuts[iWP].update(regions_cr2[iWP])
  
   return allCuts

def cutClassesIndex(eleIDselIndex, ID = "standard"):
   if not eleIDselIndex: 
      print makeLine() 
      print "No electron selection. Exiting."
      print makeLine() 
      exit()
      
   if ID == "MVA": WPs = ['None', 'WP80', 'WP90']
   else: WPs = ['None', 'Veto', 'Loose', 'Medium', 'Tight']
   
   allCuts = {iWP:{} for iWP in WPs}

   ###############No selection################
   nosel = CutClass("nosel", [["true", "1"]], baseCut=None)
   
   ###############Preselection################
   
   #Common preselection between electrons and muons
   presel = CutClass("presel", [
                               ["MET200","met > 200"],
                               ["HT300","ht_basJet > 300"],
                               ["ISR110","nIsrJet >= 1"],
                               ["AntiQCD", "vetoJet_dPhi_j1j2 < 2.5"], # monojet
                               ["No3rdJet60","nVetoJet <= 2"],
                               #["TauElVeto","(Sum$(TauGood_idMVA) == 0) && (Sum$(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + "&& LepGood_SPRING15_25ns_v1 == 1) == 0)"],
                               #["1Mu-2ndMu20Veto", "(nlep==1 || (nlep ==2 && LepGood_pt[looseMuonIndex2] < 20) )"],
                               ], baseCut=None)
   
   presel_loose = CutClass("presel_loose", [
                               ["MET200","met > 200"],
                               ["HT200","ht_basJet > 200"],
                               ["ISR110","nIsrJet >= 1"],
                               ["AntiQCD", "vetoJet_dPhi_j1j2 < 2.5"], # monojet
                               ["No3rdJet60","nVetoJet <= 2"],
                               #["TauElVeto","(Sum$(TauGood_idMVA) == 0) && (Sum$(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + "&& LepGood_SPRING15_25ns_v1 == 1) == 0)"],
                               #["1Mu-2ndMu20Veto", "(nlep==1 || (nlep ==2 && LepGood_pt[looseMuonIndex2] < 20) )"],
                               ], baseCut=None)
   
   allCuts['None']['nosel'] = nosel
   allCuts['None']['presel'] = presel
   allCuts['None']['presel_loose'] = presel_loose
   
   #SR1
   sr1 = {}
   mtabc = {}
   mtabc_ptbin = {}
   sr1Loose = {}
   sr1abc = {}
   sr1abc_ptbin = {}
   #SR2
   sr2 = {}
   sr2_ptbin = {}
   #CR1
   cr1 = {}
   cr1Loose = {}
   cr1abc = {}
   crtt2 = {}
   #CR2
   cr2 = {}
   cr2_ = {}
   
   #RunI 
   runI = {}
   runIflow = {}

   #Combined 
   regions_sr1 = {}
   regions_sr2 = {}
   regions_cr1 = {}
   regions_cr2 = {}
      
   #Dictionaries for different WPs 
   preselEle = {}
   electronSel = {}  
   elePt = {}
   absEleEta = {} 
   eleMt = {} 
   
   for iWP in WPs:
      electronSel[iWP] = "(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && (" + eleIDselIndex[iWP] + "))"
      elePt[iWP] = "Max$(LepGood_pt*(" + electronSel[iWP] + "))"
      absEleEta[iWP] = "Max$(abs(LepGood_eta*(" + electronSel[iWP] + ")))" #absolute value
      eleMt[iWP] = "Max$(LepGood_mt*(" + electronSel[iWP] + "))"
      #elePhi[iWP] = "Max$(LepGood_phi*(" + electronSel[iWP] + "))"
      #eleMt[iWP] = "Max$(sqrt(2*met*{pt}*(1 - cos(met_phi - LepGood_phi)))*(LepGood_pt == {pt}))".format(pt=elePt[iWP]) #%(elePt[iWP], elePhi[iWP], elePt[iWP])
      #eleMt[iWP] = "Max$(sqrt(2*met*%s*(1 - cos(met_phi - %s)))*(LepGood_pt == %s))"%(elePt[iWP], elePhi[iWP], elePt[iWP])
 
      ##################Electron Preselection###########
      
      preselEle[iWP] = CutClass("preselEle_" + iWP, [
                              ["oneEle", "Sum$(" + electronSel[iWP] + ") == 1"], # single electron
                              #["pt>7", "Sum$(" + elePt[iWP] + " > 7) == 1"], # pt > 7
                              ], baseCut=presel)
   
      ##################Signal Regions##################
   
      #SR1
      sr1[iWP] = CutClass("SR1_" + iWP, [
                              ["CT300","min(met, ht_basJet - 100) > 300"],
                              ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
                              ["negEle", "Max$(LepGood_pdgId*(" + electronSel[iWP] + ")) == 11"],
                              ["absEleEta1.5", absEleEta[iWP] + " < 1.5"],
                              ["elePt<30", elePt[iWP] + " < 30"],
                              ], baseCut = preselEle[iWP])
                              #["400","ht_basJet>400"],
                              #["met300","met>300"],
   
      #sr1abc[iWP] = CutClass("SR1abc_" + iWP,[
      #                        ["SR1a", eleMt[iWP] + " < 60"],
      #                        ["SR1b", btw(eleMt[iWP], 60, 88)],
      #                        ["SR1c", eleMt[iWP] + " > 88"]
      #                        ], baseCut = sr1[iWP])
   
      sr1abc_ptbin[iWP] = CutClass("SR1abc_ptbin_" + iWP, [
                              #["SR1a", eleMt[iWP] + " < 60"],
                              ["SRL1a", combineCuts(eleMt[iWP] + " < 60", btw(elePt[iWP], 5, 12))],
                              ["SRH1a", combineCuts(eleMt[iWP] + " < 60", btw(elePt[iWP], 12, 20))],
                              ["SRV1a", combineCuts(eleMt[iWP] + " < 60", btw(elePt[iWP], 20, 30))],
                              #["SR1b",btw(eleMt[iWP], 60, 88)],
                              ["SRL1b", combineCuts(btw(eleMt[iWP], 60, 88), btw(elePt[iWP], 5, 12))],
                              ["SRH1b", combineCuts(btw(eleMt[iWP], 60, 88), btw(elePt[iWP], 12, 20))],
                              ["SRV1b", combineCuts(btw(eleMt[iWP], 60, 88), btw(elePt[iWP], 20, 30))],
                              #["SR1c",eleMt[iWP] + " > 88"],
                              ["SRL1c", combineCuts(eleMt[iWP] + " > 88", btw(elePt[iWP], 5, 12))],
                              ["SRH1c", combineCuts(eleMt[iWP] + " > 88", btw(elePt[iWP], 12, 20))],
                              ["SRV1c", combineCuts(eleMt[iWP] + " > 88", btw(elePt[iWP], 20, 30))]
                              ], baseCut = sr1[iWP])
      
      #mtabc[iWP] = CutClass ("MTabc_" + iWP, [
      #                        ["MTa", eleMt[iWP] + " < 60"],
      #                        ["MTb", btw(eleMt[iWP], 60, 88)],
      #                        ["MTc", eleMt[iWP] + " > 88"]
      #                        ], baseCut = sr1[iWP])
      # 
      #mtabc_ptbin[iWP] = splitCutInPt(mtabc[iWP])
   
      #SR2
      sr2[iWP] = CutClass("SR2_" + iWP, [
                              ["ISR325", "nIsrHJet > 0"],
                              ["MET300", "met > 300"],
                              ["SoftBJet", "nBSoftJet >= 1 && nBHardJet == 0"],
                              ["elePt<30", elePt[iWP] + " < 30"]
                              ], baseCut = preselEle[iWP])
      
      sr2_ptbin[iWP] = CutClass("SR2_PtBinned_" + iWP, [
                              ["SRL2", btw(elePt[iWP], 5, 12)],
                              ["SRH2", btw(elePt[iWP], 12, 20)],
                              ["SRV2", btw(elePt[iWP], 20, 30)]
                              ], baseCut = sr2[iWP])
   
      ##################Control Regions##################
   
      #CR1
      cr1[iWP] = CutClass("CR1_" + iWP, [
                              ["CT300","min(met, ht_basJet - 100) > 300"],
                              ["BVeto","nBSoftJet == 0 && nBHardJet == 0"],
                              ["negEle", "Max$(LepGood_pdgId*(" + electronSel[iWP] + ")) == 11"],
                              ["absEleEta1.5", absEleEta[iWP] + " < 1.5"],
                              ["elePt>30", elePt[iWP] + " > 30"], #greater than
                              ], baseCut = preselEle[iWP])
                              #["BVeto_Medium25","nBJetMedium25==0"],
                              #["400 ","ht_basJet>400"],
                              #["met300","met>300"],
     
      #cr1Loose[iWP] = CutClass("CR1Loose_" + iWP, [ # no CT cut
      #                        ["BVeto","(nBSoftJet == 0 && nBHardJet == 0)"],
      #                        ["negEle", "LepGood_pdgId == 11"],
      #                        ["absEleEta1.5", absEleEta[iWP] + " < 1.5"],
      #                        ["elePt>30", elePt[iWP] + " > 30"], #greater than
      #                        ], baseCut= preselEle[iWP])
      
      cr1abc[iWP] = CutClass("CR1abc_" + iWP, [
                              ["CR1a", eleMt[iWP] + " < 60"],
                              ["CR1b", btw(eleMt[iWP], 60, 88)],
                              ["CR1c", eleMt[iWP] + " > 88"]
                              ], baseCut = cr1[iWP])
      
      #CR2 
      cr2[iWP] = CutClass("CR2_" + iWP, [
                              ["OneOrMoreSoftB","nBSoftJet >= 1"],
                              ["noHardB", "nBHardJet == 0"],
                              ["Jet325", "nIsrHJet > 0"],
                              ["elePt>30", elePt[iWP] + " > 30"], #greater than
                              ], baseCut = preselEle[iWP])
                              #["met300","met>300"],
      
      cr2_[iWP] = CutClass("CR2_" + iWP, [
                              ["CR2", "(1)"]
                              ], baseCut = cr2[iWP])
      
      #CRTT2
      crtt2[iWP] = CutClass("CRTT2_" + iWP, [
                              ["CRTT2","((nBSoftJet + nBHardJet) > 1) && nBHardJet > 0"]
                              ], baseCut= preselEle[iWP])
      

      regions_sr1[iWP] = {'sr1': sr1[iWP], 'sr1abc_ptbin': sr1abc_ptbin[iWP], } #'sr1Loose': sr1Loose[iWP], 'sr1abc': sr1abc[iWP], 'mtabc': mtabc[iWP], 'mtabc_ptbin': mtabc_ptbin[iWP]
      regions_sr2[iWP] = {'sr2': sr2[iWP], 'sr2_ptbin': sr2_ptbin[iWP]}
      regions_cr1[iWP] = {'cr1': cr1[iWP], 'cr1abc': cr1abc[iWP]} #'cr1Loose': cr1Loose[iWP],
      regions_cr2[iWP] = {'cr2': cr2[iWP], 'crtt2': crtt2[iWP]}

      runI[iWP] = CutClass("RunI_Ele_" + iWP, [] , baseCut = preselEle[iWP])
      runI[iWP].add(sr1abc_ptbin[iWP], baseCutString = sr1[iWP].inclCombined)
      runI[iWP].add(sr2_ptbin[iWP], baseCutString = sr2[iWP].inclCombined)
      runI[iWP].add(cr1abc[iWP], baseCutString = cr1[iWP].inclCombined)
      runI[iWP].add(cr2_[iWP], baseCutString = cr2[iWP].inclCombined)
      runI[iWP].add(crtt2[iWP])
   
      runIflow[iWP] = CutClass("RunI_Ele_Flow_" + iWP, [], baseCut = None)
      runIflow[iWP].add(preselEle[iWP], 'flow', baseCutString = None)
      runIflow[iWP].add(sr1[iWP], 'inclFlow', baseCutString = preselEle[iWP].combined)
      runIflow[iWP].add(sr2[iWP], 'inclFlow', baseCutString = preselEle[iWP].combined)
      
      allCuts[iWP]['eleID_' + iWP] = eleIDselIndex[iWP]
      allCuts[iWP]['eleSel'] = electronSel[iWP] 
      allCuts[iWP]['preselEle'] = preselEle[iWP]  
      allCuts[iWP]['runI'] = runI[iWP]  
      allCuts[iWP]['runIflow'] = runIflow[iWP]  
      allCuts[iWP].update(regions_sr1[iWP])
      allCuts[iWP].update(regions_sr2[iWP])
      allCuts[iWP].update(regions_cr1[iWP])
      allCuts[iWP].update(regions_cr2[iWP])
  
   return allCuts
