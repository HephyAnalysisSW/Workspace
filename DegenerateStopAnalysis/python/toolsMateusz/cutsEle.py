#cutsEle.py
import math
from Workspace.DegenerateStopAnalysis.toolsMateusz.degTools import CutClass, joinCutStrings, splitCutInPt
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeLine
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *

less = lambda var, val: "(%s < %s)"%(var,val)
more = lambda var, val: "(%s > %s)"%(var,val)
btw = lambda var, minVal, maxVal: "(%s > %s && %s < %s)"%(var, min(minVal, maxVal), var, max(minVal, maxVal))
minAngle = lambda phi1, phi2 : "TMath::Min((2*pi) - abs({phi1}-{phi2}) , abs({phi1}-{phi2}))".format(phi1 = phi1, phi2 = phi2)  

#Geometric divisions
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
etaAcc = 2.5 #eta acceptance

#Pt division for MVA ID
ptSplit = 10 #we have above and below 10 GeV categories 

#Electron ID Definitions
#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)
WPs = ['None', 'Veto', 'Loose', 'Medium', 'Tight']

def electronIDs(ID = "standard", removedCut = "None", iso = False):

   if ID not in ["standard", "MVA", "manual", "nMinus1"]:
      print makeLine() 
      print "Wrong ID input. Choose from: standard, MVA, manual, nMinus1."
      print makeLine() 
      exit()
   
   if iso:
      print makeLine() 
      print "Applying hybrid isolation to electrons"
      print makeLine() 
      hybIso = "((LepGood_pt >= 25 && LepGood_relIso04 < 0.2) || (LepGood_pt < 25 && LepGood_relIso04 < 5))" #(abs(LepGood_pdgId) == 11) && ((LepGood_pt > 5)) && (abs(LepGood_eta) < " + str(etaAcc) + ") && (abs(LepGood_dz) < 0.2) && (abs(LepGood_dxy) < 0.05) && ((LepGood_sip3d < 4))
   
   eleIDsel = {}

   #EGamma Standard
   if ID == "standard":
      
      standardSel = {}
      for i,iWP in enumerate(WPs):
         standardSel[iWP] = "(LepGood_SPRING15_25ns_v1 >= " + str(i) + ")"
         
         if iso: standardSel[iWP] = combineSel(standardSel[iWP], hybIso)
         
      eleIDsel = standardSel
   
   #EGamma MVA
   elif ID == "MVA":
      
      #Pt division for MVA ID
      ptSplit = 10 #we have above and below 10 GeV categories
      
      mvaCuts = {'WP90':\
                {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
                 'WP80':\
                {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311}}

      mvaSel = {}
      
      for iWP in mvaCuts.keys():
         mvaSel[iWP] = "(\
         (LepGood_pt <= " + str(ptSplit) + " && abs(LepGood_eta) < " + str(ebSplit) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB1_lowPt']) + ") || \
         (LepGood_pt <= " + str(ptSplit) + " && abs(LepGood_eta) >= " + str(ebSplit) + " && abs(LepGood_eta) < " + str(ebeeSplit) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB2_lowPt']) + ") || \
         (LepGood_pt <= " + str(ptSplit) + " && abs(LepGood_eta) >= " + str(ebeeSplit) + " && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EE_lowPt']) + ") || \
         (LepGood_pt > " + str(ptSplit) + " && abs(LepGood_eta) < " + str(ebSplit) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB1']) + ") || \
         (LepGood_pt > " + str(ptSplit) + " && abs(LepGood_eta) >= " + str(ebSplit) + " && abs(LepGood_eta) < " + str(ebeeSplit) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB2']) + ") || \
         (LepGood_pt > " + str(ptSplit) + " && abs(LepGood_eta) >= " + str(ebeeSplit) + " && abs(LepGood_eta) < " + str(etaAcc) + " && LepGood_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EE']) + "))"
         
      mvaSel['None'] = "(1)"
         
      if iso: 
         for iWP in mvaSel:
            mvaSel[iWP] = combineSel(mvaSel[iWP], hybIso)
      
      eleIDsel = mvaSel
   
   #Manual/nMinus1
   else:
      WPs.remove('None')
      variables = ['sigmaEtaEta', 'dEta',  'dPhi', 'hOverE', 'ooEmooP', 'd0', 'dz', 'MissingHits', 'convVeto']
      
      WPcuts = {\
      'Veto':{'sigmaEtaEta':{'EB':0.0114, 'EE':0.0352}, 'dEta':{'EB':0.0152, 'EE':0.0113}, 'dPhi':{'EB':0.216, 'EE':0.237}, 'hOverE':{'EB':0.181, 'EE':0.116}, 'ooEmooP':{'EB':0.207, 'EE':0.174},\
      'd0':{'EB':0.0564, 'EE':0.222}, 'dz':{'EB':0.472, 'EE':0.921}, 'MissingHits':{'EB':2, 'EE':3}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.126, 'EE':0.144}},
      
      'Loose':{'sigmaEtaEta':{'EB':0.0103, 'EE':0.0301}, 'dEta':{'EB':0.0105, 'EE':0.00814}, 'dPhi':{'EB':0.115, 'EE':0.182}, 'hOverE':{'EB':0.104, 'EE':0.0897}, 'ooEmooP':{'EB':0.102, 'EE':0.126},\
      'd0':{'EB':0.0261, 'EE':0.118}, 'dz':{'EB':0.41, 'EE':0.822}, 'MissingHits':{'EB':2, 'EE':1}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.0893, 'EE':0.121}},
      
      'Medium':{'sigmaEtaEta':{'EB':0.0101, 'EE':0.0283}, 'dEta':{'EB':0.0103, 'EE':0.00733}, 'dPhi':{'EB':0.0336, 'EE':0.114}, 'hOverE':{'EB':0.0876, 'EE':0.0678}, 'ooEmooP':{'EB':0.0174, 'EE':0.0898},\
      'd0':{'EB':0.0118, 'EE':0.0739}, 'dz':{'EB':0.373, 'EE':0.602}, 'MissingHits':{'EB':2, 'EE':1}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.0766, 'EE':0.0678}},
      
      'Tight':{'sigmaEtaEta':{'EB':0.0101, 'EE':0.0279}, 'dEta':{'EB':0.00926, 'EE':0.00724}, 'dPhi':{'EB':0.0336, 'EE':0.0918}, 'hOverE':{'EB':0.0597, 'EE':0.0615}, 'ooEmooP':{'EB':0.012, 'EE':0.00999},\
      'd0':{'EB':0.0111, 'EE':0.0351}, 'dz':{'EB':0.0466, 'EE':0.417}, 'MissingHits':{'EB':2, 'EE':1}, 'convVeto':{'EB':1, 'EE':1}, 'relIso' : {'EB':0.0354, 'EE':0.0646}}}
      
      #WPcuts['Veto']['sigmaEtaEta']['EB'] = 0.014
      
      #Manual ID selection
      manualSels = {iWP:{} for iWP in WPs}
      
      for iWP in WPs:
         for var in variables:
            manualSels[iWP][var] = {}
      
      for iWP in WPs:
         for reg in ['EE','EB']:
            manualSels[iWP]['sigmaEtaEta'][reg] = "LepGood_sigmaIEtaIEta < " + str(WPcuts[iWP]['sigmaEtaEta'][reg])
            manualSels[iWP]['dEta'][reg] = "abs(LepGood_dEtaScTrkIn) < " + str(WPcuts[iWP]['dEta'][reg])
            manualSels[iWP]['dPhi'][reg] = "abs(LepGood_dPhiScTrkIn) < " + str(WPcuts[iWP]['dPhi'][reg])
            manualSels[iWP]['hOverE'][reg] = "LepGood_hadronicOverEm < " + str(WPcuts[iWP]['hOverE'][reg])
            manualSels[iWP]['ooEmooP'][reg] = "abs(LepGood_eInvMinusPInv) < " + str(WPcuts[iWP]['ooEmooP'][reg])
            manualSels[iWP]['d0'][reg] = "abs(LepGood_dxy) < " + str(WPcuts[iWP]['d0'][reg])
            manualSels[iWP]['dz'][reg] = "abs(LepGood_dz) < " + str(WPcuts[iWP]['dz'][reg])
            manualSels[iWP]['MissingHits'][reg] = "LepGood_lostHits <= " + str(WPcuts[iWP]['MissingHits'][reg])
            manualSels[iWP]['convVeto'][reg]= "LepGood_convVeto == " + str(WPcuts[iWP]['convVeto'][reg])
      
      geoSel= {'EB':"(abs(LepGood_eta) <= " + str(ebeeSplit) + ")", 'EE':"(abs(LepGood_eta) > " + str(ebeeSplit) + " && abs(LepGood_eta) < " + str(etaAcc) + ")"}
      
      EBsel = {iWP: combineSel(geoSel['EB'], combineSelList([manualSels[iWP][var]['EB'] for var in variables])) for iWP in WPs}
      EEsel = {iWP: combineSel(geoSel['EE'], combineSelList([manualSels[iWP][var]['EE'] for var in variables])) for iWP in WPs}
     
      if ID == "manual":
         manualSel = {iWP: "((" + EBsel[iWP] + ") || (" + EEsel[iWP] + "))" for iWP in WPs}
         manualSel['None'] = "(1)"
         
         if iso: 
            for iWP in manualSel:
               manualSel[iWP] = combineSel(manualSel[iWP], hybIso)
      
         eleIDsel = manualSel
       
      elif ID == "nMinus1": 
         if removedCut not in variables:
            print "Wrong variable name for removed cut"
            exit()

         #nMinus1 ID selection
         variables.remove(removedCut)
         EBsel = {iWP: combineSel("abs(LepGood_eta) <= " + str(ebeeSplit), combineSelList([manualSels[iWP][var]['EB'] for var in variables])) for iWP in WPs}
         EEsel = {iWP: combineSel("abs(LepGood_eta) > " + str(ebeeSplit) + " && abs(LepGood_eta) < " + str(etaAcc), combineSelList([manualSels[iWP][var]['EE'] for var in variables])) for iWP in WPs}
         
         nMinus1Sel = {iWP: "((" + EBsel[iWP] + ") || (" + EEsel[iWP] + "))" for iWP in WPs}
         nMinus1Sel['None'] = "(1)"
       
         if iso: 
            for iWP in nMinus1Sel:
               nMinus1Sel[iWP] = combineSel(nMinus1Sel[iWP], hybIso)
         
         eleIDsel = nMinus1Sel
      
   return eleIDsel

def cutClasses(ID, eleIDsel):
   if not eleIDsel: 
      print makeLine() 
      print "No electron selection. Exiting."
      print makeLine() 
      exit()
  
   if ID == "MVA": WPs = ['None', 'WP80', 'WP90']
   else: WPs = ['None', 'Veto', 'Loose', 'Medium', 'Tight']
   
   allCuts = {iWP:{} for iWP in WPs}
 
   for iWP in WPs:   
      allCuts[iWP]['eleID_' + iWP] = eleIDsel[iWP]
      allCuts[iWP]['eleSel'] = "Sum$(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && (" + eleIDsel[iWP] + "))"

   ###############No selection################
   nosel = CutClass("nosel", [["true", "1"]], baseCut=None)
   
   ###############Preselection################
   
   #Common preselection between electrons and muons
   presel = CutClass("presel", [
                               ["MET200","met > 200"],
                               ["HT300","htJet30j > 300"],
                               ["ISR110","nJet110 >= 1" ],
                               ["AntiQCD", " (deltaPhi_j12 < 2.5)"], # monojet
                               #["TauElVeto","(Sum$(TauGood_idMVA) == 0) && (Sum$(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + "&& LepGood_SPRING15_25ns_v1 == 1) == 0)"],
                               #["1Mu-2ndMu20Veto", "(nlep==1 || (nlep ==2 && LepGood_pt[looseMuonIndex2] < 20) )"],
                               ["No3rdJet60","nJet60 <= 2"],
                               ], baseCut=None)
   
   #Dictionaries for different WPs 
   preselEle = {}
   
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
   
   electronSel = {}  
   elePt = {}
   eleEta = {} 
   eleMt = {} 
   
   for iWP in WPs:
      electronSel[iWP] = "(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && " + eleIDsel[iWP] + ")"
      elePt[iWP] = "Max$(LepGood_pt*(" + electronSel[iWP] + "))"
      eleEta[iWP] = "Max$(abs(LepGood_eta*(" + electronSel[iWP] + ")))" #absolute value
      eleMt[iWP] = "Max$(LepGood_mt*(" + electronSel[iWP] + "))"
      #elePhi[iWP] = "Max$(LepGood_phi*(" + electronSel[iWP] + "))"
      #eleMt[iWP] = "Max$(sqrt(2*met*{pt}*(1 - cos(met_phi - LepGood_phi)))*(LepGood_pt == {pt}))".format(pt=elePt[iWP]) #%(elePt[iWP], elePhi[iWP], elePt[iWP])
      #eleMt[iWP] = "Max$(sqrt(2*met*%s*(1 - cos(met_phi - %s)))*(LepGood_pt == %s))"%(elePt[iWP], elePhi[iWP], elePt[iWP])
 
      ##################Electron Preselection###########
      
      preselEle[iWP] = CutClass("preselEle_" + iWP, [
                              ["nEle=1", "Sum$(" + electronSel[iWP] + ") == 1"], # single electron
                              #["pt>7", "Sum$(" + elePt[iWP] + " > 7) == 1"], # pt > 7
                              ], baseCut=presel)
   
      ##################Signal Regions##################
   
      #SR1
      sr1[iWP] = CutClass("SR1_" + iWP, [
                              ["CT300","min(met, htJet30j - 100) > 300"],
                              ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV == 0)"],
                              ["negEle", "Sum$(LepGood_pdgId*(" + electronSel[iWP] + ") == 11)"],
                              ["eleEta1.5", eleEta[iWP] + " < 1.5"],
                              ["elePt<30", elePt[iWP] + " < 30"],
                              ], baseCut = preselEle[iWP])
                              #["HT400","htJet30j>400"],
                              #["met300","met>300"],
   
      sr1Loose[iWP] = CutClass("SR1Loose_" + iWP, [
                              ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV == 0)"],
                              ["negEle","LepGood_pdgId == 11"],
                              ["eleEta2.4", eleEta[iWP] + " < 2.4"], #looser eta cut than sr1
                              ["elePt<30", elePt[iWP] + " < 30"],
                              ], baseCut = preselEle[iWP])
                              #["HT400","htJet30j>400"],
                              #["met300","met>300"],
      
      sr1abc[iWP] = CutClass("SR1abc_" + iWP,[
                              ["SR1a", eleMt[iWP] + " < 60"],
                              ["SR1b", btw(eleMt[iWP], 60, 88)],
                              ["SR1c", eleMt[iWP] + " > 88"]
                              ], baseCut = sr1[iWP])
   
      sr1abc_ptbin[iWP] = CutClass("SR1abc_ptbin_" + iWP, [
                              #["SR1a", eleMt[iWP] + " < 60"],
                              ["SRL1a", joinCutStrings([eleMt[iWP] + " < 60", btw(elePt[iWP], 5, 12)])],
                              ["SRH1a", joinCutStrings([eleMt[iWP] + " < 60", btw(elePt[iWP], 12, 20)])],
                              ["SRV1a", joinCutStrings([eleMt[iWP] + " < 60", btw(elePt[iWP], 20, 30)])],
                              #["SR1b",btw(eleMt[iWP], 60, 88)],
                              ["SRL1b", joinCutStrings([btw(eleMt[iWP], 60, 88), btw(elePt[iWP], 5, 12)])],
                              ["SRH1b", joinCutStrings([btw(eleMt[iWP], 60, 88), btw(elePt[iWP], 12, 20)])],
                              ["SRV1b", joinCutStrings([btw(eleMt[iWP], 60, 88), btw(elePt[iWP], 20, 30)])],
                              #["SR1c",eleMt[iWP] + " > 88"],
                              ["SRL1c", joinCutStrings([eleMt[iWP] + " > 88", btw(elePt[iWP], 5, 12)])],
                              ["SRH1c", joinCutStrings([eleMt[iWP] + " > 88", btw(elePt[iWP], 12, 20)])],
                              ["SRV1c", joinCutStrings([eleMt[iWP] + " > 88", btw(elePt[iWP], 20, 30)])]
                              ], baseCut = sr1[iWP])
      
      mtabc[iWP] = CutClass ("MTabc_" + iWP, [
                              ["MTa", eleMt[iWP] + " < 60"],
                              ["MTb", btw(eleMt[iWP], 60, 88)],
                              ["MTc", eleMt[iWP] + " > 88"]
                              ], baseCut = sr1[iWP])
       
      mtabc_ptbin[iWP] = splitCutInPt(mtabc[iWP])
   
      #SR2
      sr2[iWP] = CutClass("SR2_" + iWP, [
                              ["ISR325+MET300", "nJet325 > 0 && met > 300"],
                              ["SoftBJet", "(nSoftBJetsCSV >= 1) && (nHardBJetsCSV == 0)"],
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
                              ["CT300","min(met,htJet30j-100) > 300"],
                              ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV == 0)"],
                              ["negEle", "LepGood_pdgId == 11"],
                              ["eleEta1.5", eleEta[iWP] + " < 1.5"],
                              ["elePt>30", elePt[iWP] + " > 30"], #greater than
                              ], baseCut = preselEle[iWP])
                              #["BVeto_Medium25","nBJetMedium25==0"],
                              #["HT400 ","htJet30j>400"],
                              #["met300","met>300"],
     
      cr1Loose[iWP] = CutClass("CR1Loose_" + iWP, [ # no CT cut
                              ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV == 0)"],
                              ["negEle", "LepGood_pdgId == 11"],
                              ["eleEta1.5", eleEta[iWP] + " < 1.5"],
                              ["elePt>30", elePt[iWP] + " > 30"], #greater than
                              ], baseCut= preselEle[iWP])
      
      cr1abc[iWP] = CutClass("CR1abc_" + iWP, [
                              ["CR1a", eleMt[iWP] + " < 60"],
                              ["CR1b", btw(eleMt[iWP], 60, 88)],
                              ["CR1c", eleMt[iWP] + " > 88"]
                              ], baseCut = cr1[iWP])
      
      crtt2[iWP] = CutClass("CRTT2_" + iWP, [
                              ["CRTT2","((nSoftBJetsCSV + nHardBJetsCSV) > 1) && (nHardBJetsCSV > 0)"]
                              ], baseCut= preselEle[iWP])
      
      #CR2 
      cr2[iWP] = CutClass("CR2_" + iWP, [
                              ["OneOrMoreSoftB","nSoftBJetsCSV >= 1"],
                              ["noHardB", "nHardBJetsCSV == 0"],
                              ["Jet325", "nJet325 > 0"],
                              ["elePt>30", elePt[iWP] + " > 30"], #greater than
                              ], baseCut = preselEle[iWP])
                              #["met300","met>300"],
      
      cr2_[iWP] = CutClass("CR2_" + iWP, [
                              ["CR2", "(1)"]
                              ], baseCut = cr2[iWP])

      regions_sr1[iWP] = {'sr1': sr1[iWP], 'sr1Loose': sr1Loose[iWP], 'sr1abc': sr1abc[iWP], 'sr1abc_ptbin': sr1abc_ptbin[iWP], 'mtabc': mtabc[iWP], 'mtabc_ptbin': mtabc_ptbin[iWP]}
      regions_sr2[iWP] = {'sr2': sr2[iWP], 'sr2_ptbin': sr2_ptbin[iWP]}
      regions_cr1[iWP] = {'cr1': cr1[iWP], 'cr1Loose': cr1Loose[iWP], 'cr1abc': cr1abc[iWP], 'crtt2': crtt2[iWP]}
      regions_cr2[iWP] = {'cr2': cr2[iWP]}

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
   
      allCuts[iWP]['preselEle'] = preselEle[iWP]  
      allCuts[iWP]['runI'] = runI[iWP]  
      allCuts[iWP]['runIflow'] = runI[iWP]  
      allCuts[iWP].update(regions_sr1[iWP])
      allCuts[iWP].update(regions_sr2[iWP])
      allCuts[iWP].update(regions_cr1[iWP])
      allCuts[iWP].update(regions_cr2[iWP])
  
   return allCuts
