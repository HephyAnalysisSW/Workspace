#cutsEle.py
import math
from Workspace.DegenerateStopAnalysis.degTools import CutClass, joinCutStrings, splitCutInPt
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *

removedCut = "sigmaEtaEta"

## --------------------------------------------------------------
##                           Variables
## --------------------------------------------------------------

less = lambda var,val: "(%s < %s)"%(var,val)
more = lambda var,val: "(%s > %s)"%(var,val)
btw = lambda var,minVal,maxVal: "(%s > %s && %s < %s)"%(var, min(minVal,maxVal), var, max(minVal,maxVal))
minAngle = lambda phi1, phi2 : "TMath::Min( (2*pi) - abs({phi1}-{phi2}) , abs({phi1}-{phi2}) )".format(phi1=phi1,phi2=phi2)  

## --------------------------------------------------------------
##                            CUT LISTS
## --------------------------------------------------------------
#Geometric divisions
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
etaAcc = 2.5 #eta acceptance

#Pt division for MVA ID
ptSplit = 10 #we have above and below 10 GeV categories 

#Electron ID Definitions
#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)
WPs = ['None', 'Veto', 'Loose', 'Medium', 'Tight']

#EGamma Standard
standardIDsel = {}
#standardID = {}
for i,iWP in enumerate(WPs):
   standardIDsel[iWP] = "LepGood_SPRING15_25ns_v1 >= " + str(i)
   #standardID[iWP] = CutClass("standardIDsel_" + iWP, [[iWP, standardIDsel[iWP]]],baseCut=None)

#Manual
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
manualIDsels = {iWP:{} for iWP in WPs}

for iWP in WPs:
   for var in variables:
      manualIDsels[iWP][var] = {}

for iWP in WPs:
   for reg in ['EE','EB']:
      manualIDsels[iWP]['sigmaEtaEta'][reg] = "LepGood_sigmaIEtaIEta < " + str(WPcuts[iWP]['sigmaEtaEta'][reg])
      manualIDsels[iWP]['dEta'][reg] = "abs(LepGood_dEtaScTrkIn) < " + str(WPcuts[iWP]['dEta'][reg])
      manualIDsels[iWP]['dPhi'][reg] = "abs(LepGood_dPhiScTrkIn) < " + str(WPcuts[iWP]['dPhi'][reg])
      manualIDsels[iWP]['hOverE'][reg] = "LepGood_hadronicOverEm < " + str(WPcuts[iWP]['hOverE'][reg])
      manualIDsels[iWP]['ooEmooP'][reg] = "abs(LepGood_eInvMinusPInv) < " + str(WPcuts[iWP]['ooEmooP'][reg])
      manualIDsels[iWP]['d0'][reg] = "abs(LepGood_dxy) < " + str(WPcuts[iWP]['d0'][reg])
      manualIDsels[iWP]['dz'][reg] = "abs(LepGood_dz) < " + str(WPcuts[iWP]['dz'][reg])
      manualIDsels[iWP]['MissingHits'][reg] = "LepGood_lostHits <= " + str(WPcuts[iWP]['MissingHits'][reg])
      manualIDsels[iWP]['convVeto'][reg]= "LepGood_convVeto == " + str(WPcuts[iWP]['convVeto'][reg])

geoSel= {'EB':"(abs(LepGood_eta) <= " + str(ebeeSplit) + ")", 'EE':"(abs(LepGood_eta) > " + str(ebeeSplit) + " && abs(LepGood_eta) < " + str(etaAcc) + ")"}


EBsel = {iWP: combineSel(geoSel['EB'], combineSelList([manualIDsels[iWP][var]['EB'] for var in variables])) for iWP in WPs}
EEsel = {iWP: combineSel(geoSel['EE'], combineSelList([manualIDsels[iWP][var]['EE'] for var in variables])) for iWP in WPs}

manualIDsel = {}
manualIDsel = {iWP: "((" + EBsel[iWP] + ") || (" + EEsel[iWP] + "))" for iWP in WPs}

#nMinus1 ID selection
variables.remove(removedCut)
EBsel = {iWP: combineSel("abs(LepGood_eta) <= " + str(ebeeSplit), combineSelList([manualIDsels[iWP][var]['EB'] for var in variables])) for iWP in WPs}
EEsel = {iWP: combineSel("abs(LepGood_eta) > " + str(ebeeSplit) + " && abs(LepGood_eta) < " + str(etaAcc), combineSelList([manualIDsels[iWP][var]['EE'] for var in variables])) for iWP in WPs}

nMinus1IDsel = {iWP: "((" + EBsel[iWP] + ") || (" + EEsel[iWP] + "))" for iWP in WPs}

#preSel1 = "(met_pt > 200)" #MET
#preSel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
#preSel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR
#
#nSel = ["(nLepGood == 0)", "(nLepGood == 1)", "(nLepGood == 2)"]
#acceptance = "(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + ")"

#manualID = {}
#nMinus1ID = {}
#
#for iWP in WPs:
#   manualID[iWP] = CutClass("manualIDsel_" + iWP, [[iWP, manualIDsel[iWP]]],baseCut=None)
#   nMinus1ID[iWP] = CutClass("nMinus1sel_" + iWP, [[iWP, nMinus1IDsel[iWP]]],baseCut=None)

def cutClasses_eleID(ID = "standard"):
   eleIDsel = {}
   WPs = ['Veto', 'Loose', 'Medium', 'Tight']
   if ID == "standard": WPs.append('None')
  
   for iWP in WPs:   
      if ID == "standard": eleIDsel[iWP] = standardIDsel[iWP]
      elif ID == "manual": eleIDsel[iWP] = manualIDsel[iWP]
      elif ID == "nMinus1": eleIDsel[iWP] = nMinus1IDsel[iWP]
      else: 
         print "Wrong electron ID definition (standard, manual, nMinus1). Exiting."
         exit()

   ###############No selection################
   nosel = CutClass("nosel", [["true", "1"]], baseCut=None)
   
   ###############Preselection################
   
   #Common preselection between electrons and muons
   presel = CutClass("presel", [\
                                 ["MET200","met>200"],\
                                 ["ISR110","nJet110>=1" ],\
                                 ["HT300","htJet30j>300"],\
                                 ["AntiQCD", " (deltaPhi_j12 < 2.5)" ]], # monojet
                   baseCut=None)
   
   #Dictionaries for different WPs 
   preselEle_eleID = {}
   
   #SR1
   sr1_eleID = {}
   mtabc_eleID = {}
   mtabc_ptbin_eleID = {}
   sr1Loose_eleID = {}
   sr1abc_eleID = {}
   sr1abc_ptbin_eleID = {}
   #SR2
   sr2_eleID = {}
   sr2_ptbin_eleID = {}
   #CR1
   cr1_eleID = {}
   cr1Loose_eleID = {}
   cr1abc_eleID = {}
   crtt2_eleID = {}
   #CR2
   cr2_eleID = {}
  
   #Combined 
   regions_eleID_sr1 = {}
   regions_eleID_sr2 = {}
   regions_eleID_cr1 = {}
   regions_eleID_cr2 = {}
   
   allRegions_eleID = {iWP:{} for iWP in WPs}
      
   allRegions_eleID['None']['NoSel'] = nosel
   allRegions_eleID['None']['Presel'] = presel
   
   electronSel = {}  
   elePt = {}
   eleEta = {} 
   eleMt = {} 
   
   for iWP in WPs:
      electronSel[iWP] = "(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < " + str(etaAcc) + " && " + eleIDsel[iWP] + ")"
      elePt[iWP] = "Max$(LepGood_pt*(" + electronSel[iWP] + "))"
      eleEta[iWP] = "Max$(abs(LepGood_eta*(" + electronSel[iWP] + ")))" #absolute value
      eleMt[iWP] = "(sqrt(2*met*%s*(1 - cos(met_phi - LepGood_phi)))*(LepGood_pt==%s))"%(elePt[iWP], elePt[iWP])#.format(pt=elePt[iWP])
 
      ##################Electron Preselection###########
      
      preselEle_eleID[iWP] = CutClass("preselEle_eleID_" + iWP, [\
                              ["nEle>=1", "nLepGood >= 1 && Sum$(" + electronSel[iWP] + ") == 1"], #at least one electron
                              ["No3rdJet60","nJet60<=2"]],\
                               baseCut=presel)
   
      ##################Signal Regions##################
   
      #SR1
      sr1_eleID[iWP] = CutClass("SR1_eleID_" + iWP, [\
                      ["negEle","LepGood_pdgId == 11"],\
                      ["elePt<30", elePt[iWP] + " < 30"],\
                      ["eleEta1.5", eleEta[iWP] + " < 1.5"],\
                      ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV == 0)"],\
                      ["CT300","min(met, htJet30j - 100) > 300"]],\
                      baseCut = preselEle_eleID[iWP])
   
      sr1Loose_eleID[iWP] = CutClass("sr1Loose_eleID_" + iWP, [\
                                    ["negEle","LepGood_pdgId == 11"],\
                                    ["elePt<30", elePt[iWP] + " < 30"],\
                                    ["eleEta2.4", eleEta[iWP] + " < 2.4"], #looser eta cut than sr1
                                    ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV == 0)"],\
                                    #["met300","met>300"],
                                    #["HT400","htJet30j>400"],
                                    ],
                        baseCut = preselEle_eleID[iWP])
      
      sr1abc_eleID[iWP] = CutClass("sr1abc_eleID_" + iWP,[\
                                     ["SR1a", eleMt[iWP] + " < 60"],\
                                     ["SR1b", btw(eleMt[iWP], 60, 88)],\
                                     ["SR1c", eleMt[iWP] + " > 88"]],\
                           baseCut = sr1_eleID[iWP])
   
      sr1abc_ptbin_eleID[iWP] = CutClass ("SR1abc_PtBinned_eleID_" + iWP, [\
                                     #["SR1a", eleMt[iWP] + " < 60"],
                                        ["SRL1a", joinCutStrings([eleMt[iWP] + " < 60", btw(elePt[iWP], 5, 12)])],\
                                        ["SRH1a", joinCutStrings([eleMt[iWP] + " < 60", btw(elePt[iWP], 12, 20)])],\
                                        ["SRV1a", joinCutStrings([eleMt[iWP] + " < 60", btw(elePt[iWP], 20, 30)])],\
                                     #["SR1b",btw(eleMt[iWP], 60, 88)],
                                        ["SRL1b", joinCutStrings([btw(eleMt[iWP], 60, 88), btw(elePt[iWP], 5, 12)])],\
                                        ["SRH1b", joinCutStrings([btw(eleMt[iWP], 60, 88), btw(elePt[iWP], 12, 20)])],\
                                        ["SRV1b", joinCutStrings([btw(eleMt[iWP], 60, 88), btw(elePt[iWP], 20, 30)])],\
                                     #["SR1c",eleMt[iWP] + " > 88"],
                                        ["SRL1c", joinCutStrings([eleMt[iWP] + " > 88", btw(elePt[iWP], 5, 12)])],\
                                        ["SRH1c", joinCutStrings([eleMt[iWP] + " > 88", btw(elePt[iWP], 12, 20)])],\
                                        ["SRV1c", joinCutStrings([eleMt[iWP] + " > 88", btw(elePt[iWP], 20, 30)])]],\
                                     baseCut = sr1_eleID[iWP])
      
      mtabc_eleID[iWP] = CutClass ("MTabc_eleID_" + iWP, [\
                      ["MTa", eleMt[iWP] + " < 60"],
                      ["MTb", btw(eleMt[iWP], 60, 88)],
                      ["MTc", eleMt[iWP] + " > 88"]],\
                      baseCut = sr1_eleID[iWP])
       
      mtabc_ptbin_eleID[iWP] = splitCutInPt(mtabc_eleID[iWP])
   
      #SR2
      sr2_eleID[iWP] = CutClass ("SR2_eleID_" + iWP, [\
                             ["ISR325", "nJet325 > 0"],\
                             ["OneOrMoreSoftB", "nSoftBJetsCSV >= 1"],\
                             ["noHardB", "nHardBJetsCSV == 0"],\
                             ["elePt<30", elePt[iWP] + " < 30"]],\
                             baseCut = preselEle_eleID[iWP])
      
      sr2_ptbin_eleID[iWP] = CutClass ("SR2_PtBinned_eleID_" + iWP, [\
                                        ["SRL2", btw(elePt[iWP], 5, 12)],\
                                        ["SRH2", btw(elePt[iWP], 12, 20)],\
                                        ["SRV2", btw(elePt[iWP], 20, 30)]],\
                           baseCut = sr2_eleID[iWP])
   
      ##################Control Regions##################
   
      #CR1
      cr1_eleID[iWP] = CutClass ("CR1_eleID_" + iWP, [\
                                    ["negEle", "LepGood_pdgId == 11"],\
                                    ["elePt>30", elePt[iWP] + " > 30"], #greater than
                                    ["eleEta1.5", eleEta[iWP] + " < 1.5"],\
                                    ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV == 0)"],\
                                    ["CT300","min(met,htJet30j-100) > 300"],\
                                    #["BVeto_Medium25","nBJetMedium25==0"],
                                    #["HT400 ","htJet30j>400"],
                                    #["met300","met>300"],
                                    ],
                        baseCut = preselEle_eleID[iWP])
     
      cr1Loose_eleID[iWP] = CutClass("cr1Loose_eleID_" + iWP, [\
                                ["negEle", "LepGood_pdgId == 11"],
                                ["elePt>30", elePt[iWP] + " > 30"], #greater than
                                ["eleEta1.5", eleEta[iWP] + " < 1.5"],\
                                ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV == 0)"]],
                          baseCut= preselEle_eleID[iWP])
      
      cr1abc_eleID[iWP] = CutClass ("CR1abc_eleID_" + iWP, [\
                                     ["CR1a", eleMt[iWP] + " < 60"],
                                     ["CR1b", btw(eleMt[iWP], 60, 88)],
                                     ["CR1c", eleMt[iWP] + " > 88"]],
                        baseCut = cr1_eleID[iWP])
      
      crtt2_eleID[iWP] = CutClass("CRTT2_eleID_" + iWP, [\
                            ["CRTT2","((nSoftBJetsCSV + nHardBJetsCSV) > 1) && (nHardBJetsCSV > 0)"]],\
                          baseCut= preselEle_eleID[iWP])
      
      #CR2 
      cr2_eleID[iWP] = CutClass ("CR2_eleID_" + iWP, [\
                              ["Jet325", "nJet325 > 0"],
                              ["OneOrMoreSoftB","nSoftBJetsCSV >= 1"],
                              ["noHardB", "nHardBJetsCSV == 0"],
                              ["elePt>30", elePt[iWP] + " > 30"], #greater than
                              #["met300","met>300"],
                              ],
                        baseCut = preselEle_eleID[iWP])
      
      regions_eleID_sr1[iWP] = {'sr1': sr1_eleID[iWP], 'sr1Loose': sr1Loose_eleID[iWP], 'sr1abc': sr1abc_eleID[iWP], 'sr1abc_ptbin': sr1abc_ptbin_eleID[iWP], 'mtabc': mtabc_eleID[iWP]} #, , 'mtabc_ptbin': mtabc_ptbin_eleID[iWP],
      regions_eleID_sr2[iWP] = {'sr2': sr2_eleID[iWP], 'sr2_ptbin': sr2_ptbin_eleID[iWP]}
      regions_eleID_cr1[iWP] = {'cr1': cr1_eleID[iWP], 'cr1Loose': cr1Loose_eleID[iWP], 'cr1abc': cr1abc_eleID[iWP], 'crtt2': crtt2_eleID[iWP]}
      regions_eleID_cr2[iWP] = {'cr2': cr2_eleID[iWP]}

      allRegions_eleID[iWP]['preselEle'] = preselEle_eleID[iWP]  
      allRegions_eleID[iWP].update(regions_eleID_sr1[iWP])
      allRegions_eleID[iWP].update(regions_eleID_sr2[iWP])
      allRegions_eleID[iWP].update(regions_eleID_cr1[iWP])
      allRegions_eleID[iWP].update(regions_eleID_cr2[iWP])
  
   return allRegions_eleID 
 
   #Following commented out as 'None' electron ID is an option
   
   #preselEle = CutClass("preselEle", [
   #                                  ["nEle>=1", "nLepGood >= 1 && (Sum$(abs(LepGood_pdgId) == 11 && abs(LepGood_eta) < 2.5) == 1)"],\
   #                                  ["No3rdJet60","nJet60<=2"]],\
   #                                  #["2ndMu20Veto", "(nlep==1 || nlep ==2 && LepGood_pt[looseMuonIndex2] < 20)"],
   #                baseCut=presel)
   #
   #["2ndMu20Veto", "(nlep==1 || nlep ==2 && LepGood_pt[looseMuonIndex2] < 20)"],
   #
   #preselection = preselEle.combined
   #   
   #2ndMuVeto = "nlep==1 ||" + 'Sum$(  \
   #                    (abs(LepGood_pdgId)==13) && ((LepGood_pt > 5)) && (LepGood_pt < 30) && (abs(LepGood_eta)<2.4) && \
   #                    (abs(LepGood_dz)<0.2) && (abs(LepGood_dxy)<0.05) && ((LepGood_sip3d < 4)) && (((LepGood_pt >= 25) \
   #                 && (LepGood_relIso04 < 0.2) ) || ( (LepGood_pt < 25) && (( LepGood_pt*LepGood_relIso04 ) < 5))) && (LepGood_mediumMuonId==1))==1'
   #
   #  
   #sr1 = CutClass("SR1", [
   #               ["elePt30","LepGood_pt < 30"],
   #               ["negEle","LepGood_pdgId == 11"],
   #               ["eleEta1.5","abs(LepGood_eta) < 1.5"],
   #               ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV ==0)"],
   #               ["CT300","min(met,htJet30j-100) > 300"]],
   #               #["HT400","htJet30j>400"],
   #               #["met300","met>300"],
   #               baseCut = preselEle)
   #
   #mtabc = CutClass ("MTabc", [\
   #                  ["MTa","mt<60"],
   #                  ["MTb",btw("mt",60,88)],
   #                  ["MTc","mt>88"]],\
   #                  baseCut = sr1)
   #
   #mtabc_pt = splitCutInPt(mtabc)
   #
   #sr1Loose = CutClass ("sr1Loose", [
   #                              ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV ==0)"],\
   #                              ["elePt30","LepGood_pt < 30"],\
   #                              ["negEle","LepGood_pdgId == 11"],\
   #                              ["eleEta2.4","abs(LepGood_eta) < 2.4"]],
   #                              #["met300","met>300"],
   #                              #["HT400","htJet30j>400"],
   #                  baseCut = preselEle)
   #
   #sr1abc_ptbin   = CutClass ("SR1abc_PtBinned", [\
   #                               #["SR1a","mt<60"],
   #                                  ["SRL1a",joinCutStrings(   ["mt<60",         btw("lepPt",5,12)] )],\
   #                                  ["SRH1a",joinCutStrings(   ["mt<60",         btw("lepPt",12,20)])],\
   #                                  ["SRV1a",joinCutStrings(   ["mt<60",         btw("lepPt",20,30)])],\
   #                               #["SR1b",btw("mt",60,88)],
   #                                  ["SRL1b",joinCutStrings(   [btw("mt",60,88), btw("lepPt",5,12)] )],\
   #                                  ["SRH1b",joinCutStrings(   [btw("mt",60,88), btw("lepPt",12,20)])],\
   #                                  ["SRV1b",joinCutStrings(   [btw("mt",60,88), btw("lepPt",20,30)])],\
   #                               #["SR1c","mt>88"],
   #                                  ["SRL1c",joinCutStrings(   ["mt>88",         btw("lepPt",5,12)] )],\
   #                                  ["SRH1c",joinCutStrings(   ["mt>88",         btw("lepPt",12,20)])],\
   #                                  ["SRV1c",joinCutStrings(   ["mt>88",         btw("lepPt",20,30)])]],\
   #                               baseCut = sr1)
   #
   #sr1abc   = CutClass ("sr1abc",[\
   #                               ["SR1a","mt<60"],\
   #                               ["SR1b",btw("mt",60,88)]\
   #                               ["SR1c","mt>88"]],\
   #                     baseCut = sr1)
   #
   #sr2 = CutClass ("SR2", [\
   #                       ["ISR325","nJet325>0"],\
   #                       ["OneOrMoreSoftB","nSoftBJetsCSV>=1"],\
   #                       ["noHardB","nHardBJetsCSV==0"],\
   #                       ["elePt<30","LepGood_pt < 30"]],\
   #                     baseCut = preselEle)
   #
   #sr2_ptbin = CutClass ("SR2_PtBinned", [\
   #                                  ["SRL2", btw("lepPt",5,12) ],\
   #                                  ["SRH2", btw("lepPt",12,20)],\
   #                                  ["SRV2", btw("lepPt",20,30)]],\
   #                     baseCut = sr2)
   #  
   #
   ##################Control Regions##################
   #
   #
   #cr1Loose    = CutClass ( "cr1Loose", [
   #                          ["MuPt30","lepPt>30"],
   #                          ["negMuon","lepPdgId==13"],
   #                          ["MuEta1.5","abs(lepEta)<1.5"],
   #                          ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV ==0)"],
   #                    ],
   #                    baseCut= preselEle,
   #                )
   #
   #
   #crtt2    = CutClass ( "CRTT2", [
   #                      ["CRTT2","( (nSoftBJetsCSV + nHardBJetsCSV) > 1 ) && ( nHardBJetsCSV > 0  )"],
   #                             ],
   #                    baseCut= preselEle ,
   #                )
   #
   #cr1   = CutClass ("CR1",    [
   #                              ["MuPt_gt_30","lepPt>30"],
   #                              ["negMuon","lepPdgId==13"],
   #                              ["MuEta1.5","abs(lepEta)<1.5"],
   #                              ["BVeto","(nSoftBJetsCSV == 0 && nHardBJetsCSV ==0)"],
   #                              #["BVeto_Medium25","nBJetMedium25==0"],
   #                              ["CT300","min(met,htJet30j-100) > 300 "],
   #                              #["HT400 ","htJet30j>400"],
   #                              #["met300","met>300"],
   #                           ] , 
   #                  baseCut = preselEle,
   #                  )
   #
   #
   #cr1abc   = CutClass ("CR1abc",    [
   #                               ["CR1a", "mt<60"],
   #                               ["CR1b", btw("mt",60,88)],
   #                               ["CR1c", "mt>88"],
   #                           ] , 
   #                  baseCut = cr1,
   #                  )
   #
   #
   #
   #cr2      = CutClass ("CR2",   [
   #                                ["Jet325","nJet325>0"],
   #                                #["met300","met>300"],
   #                                ["OneOrMoreSoftB","nSoftBJetsCSV>=1"],
   #                                ["noHardB","nHardBJetsCSV==0"],
   #                                ["MuPt_gt_30","lepPt>30"],
   #                              ],
   #                  baseCut = preselEle,
   #                  )
   #cr2_      = CutClass( "CR2", [ ["CR2", "(1)"] ],
   #                    baseCut = cr2
   #                    ) 
   #
   #
   #
   #runI        =   CutClass( "Reload" , [] , baseCut = preselEle )
   #runI.add(   sr1abc_ptbin    , baseCutString = sr1.inclCombined )
   #runI.add(   sr2_ptbin       , baseCutString = sr2.inclCombined ) 
   #runI.add(   cr1abc          , baseCutString = cr1.inclCombined )
   #runI.add(   cr2_             , baseCutString = cr2.inclCombined ) 
   #runI.add(   crtt2        ) 
   #
   #
   #
   #
   #runIflow   =    CutClass( "RunIFlow", [], baseCut = None)
   #runIflow.add( preselEle, 'flow', baseCutString = None)
   #runIflow.add( sr1, 'inclFlow', baseCutString = preselEle.combined)
   #runIflow.add( sr2, 'inclFlow', baseCutString = preselEle.combined)
