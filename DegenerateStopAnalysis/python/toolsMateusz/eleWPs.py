#eleWPs.py
import math
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, splitCutInPt
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

#def electronIDsIndex(ID = "standard", removedCut = "None", iso = "", collection = "LepGood"):
# 
#   #if index == "leadingEle":
#   ind = "Index" + collection + "_el[0]"
#
#   print makeLine()
#   print "Applying electron ID to leading electron."
#   print makeLine()
#
#   #elif index == "leadingLep":
#   #   ind = "0"
#
#   #   print makeLine()
#   #   print "Applying electron ID to leading lepton."
#   #   print makeLine()
# 
#   WPs = ['None', 'Veto', 'Loose', 'Medium', 'Tight']
#
#   if ID not in ["standard", "MVA", "manual", "nMinus1"]:
#      print makeLine() 
#      print "Wrong ID input. Choose from: standard, MVA, manual, nMinus1."
#      print makeLine() 
#      exit()
#   else:
#      print makeLine()
#      print "Using " + ID + " electron ID from " + collection + " collection."
#      if ID == "nMinus1": print "with " + removedCut + " cut removed."
#      print makeLine()
#   
#   if iso:
#      print makeLine() 
#      print "Applying " + iso + " to electrons"
#      print makeLine() 
#      # absIso, absIso03, relIso03, relIso04, miniRelIso
#      if iso == "hybIso03": hybIso = "(" + collection + "_pt[" + ind + "] < 25 && " + collection + "_absIso03[" + ind + "] < 5) || ((" + collection + "_pt[" + ind + "] >= 25 && " + collection + "_relIso03[" + ind + "] < 0.2))" 
#      elif iso == "hybIso04": hybIso = "(" + collection + "_pt[" + ind + "] < 25 && " + collection + "_absIso[" + ind + "] < 5) || ((" + collection + "_pt[" + ind + "] >= 25 && " + collection + "_relIso04[" + ind + "] < 0.2))" 
#      else:
#         print makeLine() 
#         print "Wrong iso input. Choose from: hybIso03, hybIso04. Using no isolation."
#         print makeLine()
#         hybIso == "1"
#
#   eleIDselIndex = {}
#
#   #EGamma Standard
#   if ID == "standard":
#      
#      standardSel = {}
#      for i,iWP in enumerate(WPs):
#         standardSel[iWP] = "(" + collection + "_SPRING15_25ns_v1[" + ind + "] >= " + str(i) + ")"
#         
#      eleIDselIndex = standardSel
#   
#   #EGamma MVA
#   elif ID == "MVA":
#      
#      #Pt division for MVA ID
#      ptSplit = 10 #we have above and below 10 GeV categories
#      
#      mvaCuts = {'WP90':\
#                {'EB1_lowPt':-0.083313, 'EB2_lowPt':-0.235222, 'EE_lowPt':-0.67099, 'EB1':0.913286, 'EB2':0.805013, 'EE':0.358969},\
#                 'WP80':\
#                {'EB1_lowPt':0.287435, 'EB2_lowPt':0.221846, 'EE_lowPt':-0.303263, 'EB1':0.967083, 'EB2':0.929117, 'EE':0.726311}}
#
#      mvaSel = {}
#      
#      for iWP in mvaCuts.keys():
#         mvaSel[iWP] = "(\
#         (" + collection + "_pt[" + ind + "] <= " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(ebSplit) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EB1_lowPt']) + ") || \
#         (" + collection + "_pt[" + ind + "] <= " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) >= " + str(ebSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(ebeeSplit) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EB2_lowPt']) + ") || \
#         (" + collection + "_pt[" + ind + "] <= " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) >= " + str(ebeeSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(etaAcc) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EE_lowPt']) + ") || \
#         (" + collection + "_pt[" + ind + "] > " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(ebSplit) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EB1']) + ") || \
#         (" + collection + "_pt[" + ind + "] > " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) >= " + str(ebSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(ebeeSplit) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EB2']) + ") || \
#         (" + collection + "_pt[" + ind + "] > " + str(ptSplit) + " && abs(" + collection + "_eta[" + ind + "]) >= " + str(ebeeSplit) + " && abs(" + collection + "_eta[" + ind + "]) < " + str(etaAcc) + " && " + collection + "_mvaIdSpring15[" + ind + "] >= " + str(mvaCuts[iWP]['EE']) + "))"
#         
#      mvaSel['None'] = "(1)"
#         
#      eleIDselIndex = mvaSel
#   
#   #Manual/nMinus1
#   else:
#      WPs = ['Veto', 'Loose', 'Medium', 'Tight']
# 
#      variables = ['sigmaEtaEta', 'dEta',  'dPhi', 'hOverE', 'ooEmooP', 'd0', 'dz', 'MissingHits', 'convVeto']
#      
#      WPcuts = {\
#      'Veto':{
#         'sigmaEtaEta':{'EB':0.0114, 'EE':0.0352}, 
#         'dEta':{       'EB':0.0152, 'EE':0.0113}, 
#         'dPhi':{       'EB':0.216,  'EE':0.237}, 
#         'hOverE':{     'EB':0.181,  'EE':0.116}, 
#         'ooEmooP':{    'EB':0.207,  'EE':0.174},
#         'd0':{         'EB':0.0564, 'EE':0.222}, 
#         'dz':{         'EB':0.472,  'EE':0.921}, 
#         'MissingHits':{'EB':2,      'EE':3}, 
#         'convVeto':{   'EB':1,      'EE':1}, 
#         #'relIso' : {   'EB':0.126, 'EE':0.144}},
#      },
#      'Loose':{
#         'sigmaEtaEta':{'EB':0.0103, 'EE':0.0301},
#         'dEta':{       'EB':0.0105, 'EE':0.00814}, 
#         'dPhi':{       'EB':0.115,  'EE':0.182}, 
#         'hOverE':{     'EB':0.104,  'EE':0.0897},
#         'ooEmooP':{    'EB':0.102,  'EE':0.126},
#         'd0':{         'EB':0.0261, 'EE':0.118},
#         'dz':{         'EB':0.41,   'EE':0.822},
#         'MissingHits':{'EB':2, 'EE':1},
#         'convVeto':{   'EB':1, 'EE':1},
#         #'relIso' : {   'EB':0.0893, 'EE':0.121}},
#      },
#      'Medium':{
#         'sigmaEtaEta':{'EB':0.0101, 'EE':0.0283}, 
#         'dEta':{       'EB':0.0103, 'EE':0.00733},
#         'dPhi':{       'EB':0.0336, 'EE':0.114},
#         'hOverE':{     'EB':0.0876, 'EE':0.0678},
#         'ooEmooP':{    'EB':0.0174, 'EE':0.0898},
#         'd0':{         'EB':0.0118, 'EE':0.0739},
#         'dz':{         'EB':0.373,  'EE':0.602},
#         'MissingHits':{'EB':2, 'EE':1},
#         'convVeto':{   'EB':1, 'EE':1},
#         #'relIso' : {   'EB':0.0766, 'EE':0.0678}},
#      },
#      'Tight':{
#         'sigmaEtaEta':{'EB':0.0101, 'EE':0.0279},
#         'dEta':{       'EB':0.00926,'EE':0.00724},
#         'dPhi':{       'EB':0.0336, 'EE':0.0918},
#         'hOverE':{     'EB':0.0597, 'EE':0.0615},
#         'ooEmooP':{    'EB':0.012,  'EE':0.00999},
#         'd0':{         'EB':0.0111, 'EE':0.0351},
#         'dz':{         'EB':0.0466, 'EE':0.417},
#         'MissingHits':{'EB':2, 'EE':1},
#         'convVeto':{   'EB':1, 'EE':1}, 
#         #'relIso' : {'EB':0.0354, 'EE':0.0646}}}
#      }} 
#      
#      #Modifying cut values 
#      #WPcuts['Veto']['sigmaEtaEta']['EB'] = 0.014
#      
#      #Manual ID selection
#      manualSels = {iWP:{} for iWP in WPs}
#      
#      for iWP in WPs:
#         for var in variables:
#            manualSels[iWP][var] = {}
#      
#      for iWP in WPs:
#         for reg in ['EE','EB']:
#            manualSels[iWP]['sigmaEtaEta'][reg] =  collection + "_sigmaIEtaIEta[" + ind + "] < " + str(WPcuts[iWP]['sigmaEtaEta'][reg])
#            manualSels[iWP]['dEta'][reg] = "abs(" + collection + "_dEtaScTrkIn[" + ind + "]) < " + str(WPcuts[iWP]['dEta'][reg])
#            manualSels[iWP]['dPhi'][reg] = "abs(" + collection + "_dPhiScTrkIn[" + ind + "]) < " + str(WPcuts[iWP]['dPhi'][reg])
#            manualSels[iWP]['hOverE'][reg] = collection + "_hadronicOverEm[" + ind + "] < " + str(WPcuts[iWP]['hOverE'][reg])
#            manualSels[iWP]['ooEmooP'][reg] = "abs(" + collection + "_eInvMinusPInv[" + ind + "]) < " + str(WPcuts[iWP]['ooEmooP'][reg])
#            manualSels[iWP]['d0'][reg] = "abs(" + collection + "_dxy[" + ind + "]) < " + str(WPcuts[iWP]['d0'][reg])
#            manualSels[iWP]['dz'][reg] = "abs(" + collection + "_dz[" + ind + "]) < " + str(WPcuts[iWP]['dz'][reg])
#            manualSels[iWP]['MissingHits'][reg] = collection + "_lostHits[" + ind + "] <= " + str(WPcuts[iWP]['MissingHits'][reg])
#            manualSels[iWP]['convVeto'][reg]= collection + "_convVeto[" + ind + "] == " + str(WPcuts[iWP]['convVeto'][reg])
#      
#      geoSel= {'EB':"(abs(" + collection + "_etaSc[" + ind + "]) <= " + str(ebeeSplit) + ")", 'EE':"(abs(" + collection + "_etaSc[" + ind + "]) > " + str(ebeeSplit) + " && abs(" + collection + "_etaSc[" + ind + "]) < " + str(etaAcc) + ")"}
#      
#      EBsel = {iWP: combineCuts(geoSel['EB'], combineCutsList([manualSels[iWP][var]['EB'] for var in variables])) for iWP in WPs}
#      EEsel = {iWP: combineCuts(geoSel['EE'], combineCutsList([manualSels[iWP][var]['EE'] for var in variables])) for iWP in WPs}
#     
#      if ID == "manual":
#         manualSel = {iWP: "((" + EBsel[iWP] + ") || (" + EEsel[iWP] + "))" for iWP in WPs}
#         manualSel['None'] = "(1)"
#         
#         eleIDselIndex = manualSel
#       
#      elif ID == "nMinus1": 
#         if removedCut not in variables:
#            print "Wrong variable name for removed cut"
#            exit()
#
#         #nMinus1 ID selection
#         variables.remove(removedCut)
#         EBsel = {iWP: combineCuts("abs(" + collection + "_etaSc[" + ind + "]) <= " + str(ebeeSplit), combineCutsList([manualSels[iWP][var]['EB'] for var in variables])) for iWP in WPs}
#         EEsel = {iWP: combineCuts("abs(" + collection + "_etaSc[" + ind + "]) > " + str(ebeeSplit) + " && abs(" + collection + "_etaSc[" + ind + "]) < " + str(etaAcc), combineCutsList([manualSels[iWP][var]['EE'] for var in variables])) for iWP in WPs}
#         
#         nMinus1Sel = {iWP: "((" + EBsel[iWP] + ") || (" + EEsel[iWP] + "))" for iWP in WPs}
#         nMinus1Sel['None'] = "(1)"
#         
#         eleIDselIndex = nMinus1Sel
#  
#   #adding pt cut   
#   for iWP in eleIDselIndex:
#      eleIDselIndex[iWP] = combineCuts(eleIDselIndex[iWP], collection + "_pt[" + ind + "] > 5")
#         
#      if iso: eleIDselIndex[iWP] = combineCuts(eleIDselIndex[iWP], hybIso)
#    
#   return eleIDselIndex
