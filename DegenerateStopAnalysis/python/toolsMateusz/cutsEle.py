#cutsEle.py
import math
from Workspace.DegenerateStopAnalysis.toolsMateusz.degTools import CutClass, combineCuts, splitCutInPt
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
#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tig (~70% eff)

def electronIDs(ID = "standard", removedCut = "None", iso = "", collection = "LepGood"):
  
   WPs = ['None', 'Veto', 'Loose', 'Medium', 'Tight']

   if ID not in ["standard", "MVA", "manual", "nMinus1"]:
      print makeLine() 
      print "Wrong ID input. Choose from: standard, MVA, manual, nMinus1."
      print makeLine() 
      exit()
   else:
      print makeLine()
      print "Using " + ID + " electron ID from " + collection + " collection."
      if ID == "nMinus1": print "with " + removedCut + " cut removed."
      print makeLine()
   
   if iso:
      print makeLine() 
      print "Applying " + iso + " to electrons"
      print makeLine() 
      # absIso, absIso03, relIso03, relIso04, miniRelIso
      if iso == "hybIso03": hybIso = "(" + collection + "_pt < 25 && " + collection + "_absIso03 < 5) || ((" + collection + "_pt >= 25 && " + collection + "_relIso03 < 0.2))" 
      elif iso == "hybIso04": hybIso = "(" + collection + "_pt < 25 && " + collection + "_absIso < 5) || ((" + collection + "_pt >= 25 && " + collection + "_relIso04 < 0.2))" 
      else:
         print makeLine() 
         print "Wrong iso input. Choose from: hybIso03, hybIso04. Using no isolation."
         print makeLine()
         hybIso = "1"

   eleIDsel = {}

   #EGamma Standard
   if ID == "standard":
      
      standardSel = {}
      for i,iWP in enumerate(WPs):
         standardSel[iWP] = "(" + collection + "_SPRING15_25ns_v1 >= " + str(i) + ")"
         
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
         (" + collection + "_pt <= " + str(ptSplit) + " && abs(" + collection + "_eta) < " + str(ebSplit) + " && " + collection + "_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB1_lowPt']) + ") || \
         (" + collection + "_pt <= " + str(ptSplit) + " && abs(" + collection + "_eta) >= " + str(ebSplit) + " && abs(" + collection + "_eta) < " + str(ebeeSplit) + " && " + collection + "_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB2_lowPt']) + ") || \
         (" + collection + "_pt <= " + str(ptSplit) + " && abs(" + collection + "_eta) >= " + str(ebeeSplit) + " && abs(" + collection + "_eta) < " + str(etaAcc) + " && " + collection + "_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EE_lowPt']) + ") || \
         (" + collection + "_pt > " + str(ptSplit) + " && abs(" + collection + "_eta) < " + str(ebSplit) + " && " + collection + "_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB1']) + ") || \
         (" + collection + "_pt > " + str(ptSplit) + " && abs(" + collection + "_eta) >= " + str(ebSplit) + " && abs(" + collection + "_eta) < " + str(ebeeSplit) + " && " + collection + "_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EB2']) + ") || \
         (" + collection + "_pt > " + str(ptSplit) + " && abs(" + collection + "_eta) >= " + str(ebeeSplit) + " && abs(" + collection + "_eta) < " + str(etaAcc) + " && " + collection + "_mvaIdSpring15 >= " + str(mvaCuts[iWP]['EE']) + "))"
         
      mvaSel['None'] = "(1)"
         
      eleIDsel = mvaSel
   
   #Manual/nMinus1
   else:
      WPs = ['Veto', 'Loose', 'Medium', 'Tight']
 
      variables = ['sigmaEtaEta', 'dEta',  'dPhi', 'hOverE', 'ooEmooP', 'd0', 'dz', 'MissingHits', 'convVeto']
      
      WPcuts = {\
      'Veto':{
         'sigmaEtaEta':{'EB':0.0114, 'EE':0.0352}, 
         'dEta':{       'EB':0.0152, 'EE':0.0113}, 
         'dPhi':{       'EB':0.216,  'EE':0.237}, 
         'hOverE':{     'EB':0.181,  'EE':0.116}, 
         'ooEmooP':{    'EB':0.207,  'EE':0.174},
         'd0':{         'EB':0.0564, 'EE':0.222}, 
         'dz':{         'EB':0.472,  'EE':0.921}, 
         'MissingHits':{'EB':2,      'EE':3}, 
         'convVeto':{   'EB':1,      'EE':1}, 
         #'relIso' : {   'EB':0.126, 'EE':0.144}},
      },
      'Loose':{
         'sigmaEtaEta':{'EB':0.0103, 'EE':0.0301},
         'dEta':{       'EB':0.0105, 'EE':0.00814}, 
         'dPhi':{       'EB':0.115,  'EE':0.182}, 
         'hOverE':{     'EB':0.104,  'EE':0.0897},
         'ooEmooP':{    'EB':0.102,  'EE':0.126},
         'd0':{         'EB':0.0261, 'EE':0.118},
         'dz':{         'EB':0.41,   'EE':0.822},
         'MissingHits':{'EB':2, 'EE':1},
         'convVeto':{   'EB':1, 'EE':1},
         #'relIso' : {   'EB':0.0893, 'EE':0.121}},
      },
      'Medium':{
         'sigmaEtaEta':{'EB':0.0101, 'EE':0.0283}, 
         'dEta':{       'EB':0.0103, 'EE':0.00733},
         'dPhi':{       'EB':0.0336, 'EE':0.114},
         'hOverE':{     'EB':0.0876, 'EE':0.0678},
         'ooEmooP':{    'EB':0.0174, 'EE':0.0898},
         'd0':{         'EB':0.0118, 'EE':0.0739},
         'dz':{         'EB':0.373,  'EE':0.602},
         'MissingHits':{'EB':2, 'EE':1},
         'convVeto':{   'EB':1, 'EE':1},
         #'relIso' : {   'EB':0.0766, 'EE':0.0678}},
      },
      'Tight':{
         'sigmaEtaEta':{'EB':0.0101, 'EE':0.0279},
         'dEta':{       'EB':0.00926,'EE':0.00724},
         'dPhi':{       'EB':0.0336, 'EE':0.0918},
         'hOverE':{     'EB':0.0597, 'EE':0.0615},
         'ooEmooP':{    'EB':0.012,  'EE':0.00999},
         'd0':{         'EB':0.0111, 'EE':0.0351},
         'dz':{         'EB':0.0466, 'EE':0.417},
         'MissingHits':{'EB':2, 'EE':1},
         'convVeto':{   'EB':1, 'EE':1}, 
         #'relIso' : {'EB':0.0354, 'EE':0.0646}}}
      }} 
      
      #Modifying cut values 
      #WPcuts['Veto']['sigmaEtaEta']['EB'] = 0.014
      
      #Manual ID selection
      manualSels = {iWP:{} for iWP in WPs}
      
      for iWP in WPs:
         for var in variables:
            manualSels[iWP][var] = {}
      
      for iWP in WPs:
         for reg in ['EE','EB']:
            manualSels[iWP]['sigmaEtaEta'][reg] =  collection + "_sigmaIEtaIEta < " + str(WPcuts[iWP]['sigmaEtaEta'][reg])
            manualSels[iWP]['dEta'][reg] = "abs(" + collection + "_dEtaScTrkIn) < " + str(WPcuts[iWP]['dEta'][reg])
            manualSels[iWP]['dPhi'][reg] = "abs(" + collection + "_dPhiScTrkIn) < " + str(WPcuts[iWP]['dPhi'][reg])
            manualSels[iWP]['hOverE'][reg] = collection + "_hadronicOverEm < " + str(WPcuts[iWP]['hOverE'][reg])
            manualSels[iWP]['ooEmooP'][reg] = "abs(" + collection + "_eInvMinusPInv) < " + str(WPcuts[iWP]['ooEmooP'][reg])
            manualSels[iWP]['d0'][reg] = "abs(" + collection + "_dxy) < " + str(WPcuts[iWP]['d0'][reg])
            manualSels[iWP]['dz'][reg] = "abs(" + collection + "_dz) < " + str(WPcuts[iWP]['dz'][reg])
            manualSels[iWP]['MissingHits'][reg] = collection + "_lostHits <= " + str(WPcuts[iWP]['MissingHits'][reg])
            manualSels[iWP]['convVeto'][reg]= collection + "_convVeto == " + str(WPcuts[iWP]['convVeto'][reg])
      
      geoSel= {'EB':"(abs(" + collection + "_etaSc) <= " + str(ebeeSplit) + ")", 'EE':"(abs(" + collection + "_etaSc) > " + str(ebeeSplit) + " && abs(" + collection + "_etaSc) < " + str(etaAcc) + ")"}
      
      EBsel = {iWP: combineCuts(geoSel['EB'], combineCutsList([manualSels[iWP][var]['EB'] for var in variables])) for iWP in WPs}
      EEsel = {iWP: combineCuts(geoSel['EE'], combineCutsList([manualSels[iWP][var]['EE'] for var in variables])) for iWP in WPs}
     
      if ID == "manual" or (ID == "nMinus1" and removedCut == "None"):
         manualSel = {iWP: "((" + EBsel[iWP] + ") || (" + EEsel[iWP] + "))" for iWP in WPs}
         manualSel['None'] = "(1)"
         
         eleIDsel = manualSel
       
      elif ID == "nMinus1" and not removedCut == "None": 
         if removedCut not in variables:
            print "Wrong variable name for removed cut"
            exit()

         #nMinus1 ID selection
         variables.remove(removedCut)
         EBsel = {iWP: combineCuts("abs(" + collection + "_etaSc) <= " + str(ebeeSplit), combineCutsList([manualSels[iWP][var]['EB'] for var in variables])) for iWP in WPs}
         EEsel = {iWP: combineCuts("abs(" + collection + "_etaSc) > " + str(ebeeSplit) + " && abs(" + collection + "_etaSc) < " + str(etaAcc), combineCutsList([manualSels[iWP][var]['EE'] for var in variables])) for iWP in WPs}
         
         nMinus1Sel = {iWP: "((" + EBsel[iWP] + ") || (" + EEsel[iWP] + "))" for iWP in WPs}
         nMinus1Sel['None'] = "(1)"
         
         eleIDsel = nMinus1Sel
  
   #adding pt cut   
   for iWP in eleIDsel:
      eleIDsel[iWP] = combineCuts(eleIDsel[iWP], collection + "_pt > 5")
         
      if iso: eleIDsel[iWP] = combineCuts(eleIDsel[iWP], hybIso)
    
   return eleIDsel

def electronIDsIndex(ID = "standard", removedCut = "None", iso = "", collection = "LepGood"):
 
   #if index == "leadingEle":
   ind = "Index" + collection + "_el[0]"

   print makeLine()
   print "Applying electron ID to leading electron."
   print makeLine()

   #elif index == "leadingLep":
   #   ind = "0"

   #   print makeLine()
   #   print "Applying electron ID to leading lepton."
   #   print makeLine()
 
   WPs = ['None', 'Veto', 'Loose', 'Medium', 'Tight']

   if ID not in ["standard", "MVA", "manual", "nMinus1"]:
      print makeLine() 
      print "Wrong ID input. Choose from: standard, MVA, manual, nMinus1."
      print makeLine() 
      exit()
   else:
      print makeLine()
      print "Using " + ID + " electron ID from " + collection + " collection."
      if ID == "nMinus1": print "with " + removedCut + " cut removed."
      print makeLine()
   
   if iso:
      print makeLine() 
      print "Applying " + iso + " to electrons"
      print makeLine() 
      # absIso, absIso03, relIso03, relIso04, miniRelIso
      if iso == "hybIso03": hybIso = "(" + collection + "_pt[" + ind + "] < 25 && " + collection + "_absIso03[" + ind + "] < 5) || ((" + collection + "_pt[" + ind + "] >= 25 && " + collection + "_relIso03[" + ind + "] < 0.2))" 
      elif iso == "hybIso04": hybIso = "(" + collection + "_pt[" + ind + "] < 25 && " + collection + "_absIso[" + ind + "] < 5) || ((" + collection + "_pt[" + ind + "] >= 25 && " + collection + "_relIso04[" + ind + "] < 0.2))" 
      else:
         print makeLine() 
         print "Wrong iso input. Choose from: hybIso03, hybIso04. Using no isolation."
         print makeLine()
         hybIso == "1"

   eleIDselIndex = {}

   #EGamma Standard
   if ID == "standard":
      
      standardSel = {}
      for i,iWP in enumerate(WPs):
         standardSel[iWP] = "(" + collection + "_SPRING15_25ns_v1[" + ind + "] >= " + str(i) + ")"
         
      eleIDselIndex = standardSel
   
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
         (" + collection + "_pt[" + ind + "] <= " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(ebSplit) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EB1_lowPt']) + ") || \
         (" + collection + "_pt[" + ind + "] <= " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) >= " + str(ebSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(ebeeSplit) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EB2_lowPt']) + ") || \
         (" + collection + "_pt[" + ind + "] <= " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) >= " + str(ebeeSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(etaAcc) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EE_lowPt']) + ") || \
         (" + collection + "_pt[" + ind + "] > " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(ebSplit) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EB1']) + ") || \
         (" + collection + "_pt[" + ind + "] > " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) >= " + str(ebSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(ebeeSplit) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EB2']) + ") || \
         (" + collection + "_pt[" + ind + "] > " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) >= " + str(ebeeSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(etaAcc) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EE']) + "))"
         
      mvaSel['None'] = "(1)"
         
      eleIDselIndex = mvaSel
   
   #Manual/nMinus1
   else:
      WPs = ['Veto', 'Loose', 'Medium', 'Tight']
 
      variables = ['sigmaEtaEta', 'dEta',  'dPhi', 'hOverE', 'ooEmooP', 'd0', 'dz', 'MissingHits', 'convVeto']
      
      WPcuts = {\
      'Veto':{
         'sigmaEtaEta':{'EB':0.0114, 'EE':0.0352}, 
         'dEta':{       'EB':0.0152, 'EE':0.0113}, 
         'dPhi':{       'EB':0.216,  'EE':0.237}, 
         'hOverE':{     'EB':0.181,  'EE':0.116}, 
         'ooEmooP':{    'EB':0.207,  'EE':0.174},
         'd0':{         'EB':0.0564, 'EE':0.222}, 
         'dz':{         'EB':0.472,  'EE':0.921}, 
         'MissingHits':{'EB':2,      'EE':3}, 
         'convVeto':{   'EB':1,      'EE':1}, 
         #'relIso' : {   'EB':0.126, 'EE':0.144}},
      },
      'Loose':{
         'sigmaEtaEta':{'EB':0.0103, 'EE':0.0301},
         'dEta':{       'EB':0.0105, 'EE':0.00814}, 
         'dPhi':{       'EB':0.115,  'EE':0.182}, 
         'hOverE':{     'EB':0.104,  'EE':0.0897},
         'ooEmooP':{    'EB':0.102,  'EE':0.126},
         'd0':{         'EB':0.0261, 'EE':0.118},
         'dz':{         'EB':0.41,   'EE':0.822},
         'MissingHits':{'EB':2, 'EE':1},
         'convVeto':{   'EB':1, 'EE':1},
         #'relIso' : {   'EB':0.0893, 'EE':0.121}},
      },
      'Medium':{
         'sigmaEtaEta':{'EB':0.0101, 'EE':0.0283}, 
         'dEta':{       'EB':0.0103, 'EE':0.00733},
         'dPhi':{       'EB':0.0336, 'EE':0.114},
         'hOverE':{     'EB':0.0876, 'EE':0.0678},
         'ooEmooP':{    'EB':0.0174, 'EE':0.0898},
         'd0':{         'EB':0.0118, 'EE':0.0739},
         'dz':{         'EB':0.373,  'EE':0.602},
         'MissingHits':{'EB':2, 'EE':1},
         'convVeto':{   'EB':1, 'EE':1},
         #'relIso' : {   'EB':0.0766, 'EE':0.0678}},
      },
      'Tight':{
         'sigmaEtaEta':{'EB':0.0101, 'EE':0.0279},
         'dEta':{       'EB':0.00926,'EE':0.00724},
         'dPhi':{       'EB':0.0336, 'EE':0.0918},
         'hOverE':{     'EB':0.0597, 'EE':0.0615},
         'ooEmooP':{    'EB':0.012,  'EE':0.00999},
         'd0':{         'EB':0.0111, 'EE':0.0351},
         'dz':{         'EB':0.0466, 'EE':0.417},
         'MissingHits':{'EB':2, 'EE':1},
         'convVeto':{   'EB':1, 'EE':1}, 
         #'relIso' : {'EB':0.0354, 'EE':0.0646}}}
      }} 
      
      #Modifying cut values 
      #WPcuts['Veto']['sigmaEtaEta']['EB'] = 0.014
      
      #Manual ID selection
      manualSels = {iWP:{} for iWP in WPs}
      
      for iWP in WPs:
         for var in variables:
            manualSels[iWP][var] = {}
      
      for iWP in WPs:
         for reg in ['EE','EB']:
            manualSels[iWP]['sigmaEtaEta'][reg] =  collection + "_sigmaIEtaIEta[" + ind + "] < " + str(WPcuts[iWP]['sigmaEtaEta'][reg])
            manualSels[iWP]['dEta'][reg] = "abs(" + collection + "_dEtaScTrkIn[" + ind + "]) < " + str(WPcuts[iWP]['dEta'][reg])
            manualSels[iWP]['dPhi'][reg] = "abs(" + collection + "_dPhiScTrkIn[" + ind + "]) < " + str(WPcuts[iWP]['dPhi'][reg])
            manualSels[iWP]['hOverE'][reg] = collection + "_hadronicOverEm[" + ind + "] < " + str(WPcuts[iWP]['hOverE'][reg])
            manualSels[iWP]['ooEmooP'][reg] = "abs(" + collection + "_eInvMinusPInv[" + ind + "]) < " + str(WPcuts[iWP]['ooEmooP'][reg])
            manualSels[iWP]['d0'][reg] = "abs(" + collection + "_dxy[" + ind + "]) < " + str(WPcuts[iWP]['d0'][reg])
            manualSels[iWP]['dz'][reg] = "abs(" + collection + "_dz[" + ind + "]) < " + str(WPcuts[iWP]['dz'][reg])
            manualSels[iWP]['MissingHits'][reg] = collection + "_lostHits[" + ind + "] <= " + str(WPcuts[iWP]['MissingHits'][reg])
            manualSels[iWP]['convVeto'][reg]= collection + "_convVeto[" + ind + "] == " + str(WPcuts[iWP]['convVeto'][reg])
      
      geoSel= {'EB':"(abs(" + collection + "_etaSc[" + ind + "]) <= " + str(ebeeSplit) + ")", 'EE':"(abs(" + collection + "_etaSc[" + ind + "]) > " + str(ebeeSplit) + " && abs(" + collection + "_etaSc[" + ind + "]) < " + str(etaAcc) + ")"}
      
      EBsel = {iWP: combineCuts(geoSel['EB'], combineCutsList([manualSels[iWP][var]['EB'] for var in variables])) for iWP in WPs}
      EEsel = {iWP: combineCuts(geoSel['EE'], combineCutsList([manualSels[iWP][var]['EE'] for var in variables])) for iWP in WPs}
     
      if ID == "manual":
         manualSel = {iWP: "((" + EBsel[iWP] + ") || (" + EEsel[iWP] + "))" for iWP in WPs}
         manualSel['None'] = "(1)"
         
         eleIDselIndex = manualSel
       
      elif ID == "nMinus1": 
         if removedCut not in variables:
            print "Wrong variable name for removed cut"
            exit()

         #nMinus1 ID selection
         variables.remove(removedCut)
         EBsel = {iWP: combineCuts("abs(" + collection + "_etaSc[" + ind + "]) <= " + str(ebeeSplit), combineCutsList([manualSels[iWP][var]['EB'] for var in variables])) for iWP in WPs}
         EEsel = {iWP: combineCuts("abs(" + collection + "_etaSc[" + ind + "]) > " + str(ebeeSplit) + " && abs(" + collection + "_etaSc[" + ind + "]) < " + str(etaAcc), combineCutsList([manualSels[iWP][var]['EE'] for var in variables])) for iWP in WPs}
         
         nMinus1Sel = {iWP: "((" + EBsel[iWP] + ") || (" + EEsel[iWP] + "))" for iWP in WPs}
         nMinus1Sel['None'] = "(1)"
         
         eleIDselIndex = nMinus1Sel
  
   #adding pt cut   
   for iWP in eleIDselIndex:
      eleIDselIndex[iWP] = combineCuts(eleIDselIndex[iWP], collection + "_pt[" + ind + "] > 5")
         
      if iso: eleIDselIndex[iWP] = combineCuts(eleIDselIndex[iWP], hybIso)
    
   return eleIDselIndex

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
