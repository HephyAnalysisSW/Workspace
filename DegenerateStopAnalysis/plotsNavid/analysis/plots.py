import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks

#from Workspace.HEPHYPythonTools.helpers import getChunksFromNFS, getChunksFromDPM, getChunks
#from Workspace.DegenerateStopAnalysis.cmgTuples_v1_Phys14 import *

import os
import math


#from Workspace.RA4Analysis.cmgTuples_v5_Phys14 import ttJets_fromEOS, 

#from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_v6_Phys14V3 import WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600,  WJetsToLNu_HT600toInf, allSignals
from Workspace.DegenerateStopAnalysis.cmgTuples_Phys14_v1 import *
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_v3_Phys14V1 import *
from Workspace.DegenerateStopAnalysis.navidPlotTools import *


targetLumi = 4000. #pb-1
#lumiWeight = xsec[sample['dbsName']]*target_lumi/float(nTotEvents)








tableDir="/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/postProcessed_v4/tables/"
treeName="treeProducerSusySingleLepton"
ROOT.gStyle.SetOptStat ( 000000)


try:
  sampleDict
except NameError:
  TTSample    = getChain(ttJets['none'],histname='') 
  T2DegSample = getChain(T2DegStop_300_270['none'],histname='')
  #WSample     = getChain(WJetsHTToLNu['none'],histname='')
  sampleDict={
            'TTJets':             {'tree':TTSample    , 'color':31          ,'lineColor':1   , 'isSignal':0 , 'isData':0       },
            #'WJets':              {'tree': WSample    , 'color':424         ,'lineColor':1   , 'isSignal':0 , 'isData':0       },
            "T2Deg300_270":       {'tree':T2DegSample , 'color':ROOT.kRed  , 'lineColor':1   , 'isSignal':1 , 'isData':0 },
            #'TTs': {'tree':getChain(ttJets['soft'],histname='') ,               'color':1    , 'isSignal':0 , 'isData':0       },            
         }



###############################################################################
###############################################################################
##########################                      ###############################
########################    Cuts and Variables    #############################
##########################                      ###############################
###############################################################################
###############################################################################





###Cuts and Preselction
muPdg="(abs(LepGood_pdgId)==13)"
muId="(LepGood_mediumMuonId==1)"
muPt5_25="(LepGood_pt > 5 && LepGood_pt < 25)"
muEta="abs(LepGood_eta)<2.4"
muMiniIso="(LepGood_miniRelIso < 0.2 || LepGood_pt < 15)&&(LepGood_miniRelIso < 0.4 || LepGood_pt > 15)"


muonCutList= [

      ["muPdg", muPdg]  ,
      ["muId", muId],
      ["muPt5_25", muPt5_25],
      ["muEta", muEta],
      ["muMiniIso", muMiniIso],

            ]




muSelect= "(%s)"%" && ".join([muPdg,muId,muPt5_25,muEta,muMiniIso]) 

preMET="(met_pt>200)"
preHT="(htJet25 > 300)"
preISR="(Jet_pt[0]>110 && Jet_pt[1]>60)"
preSelection = "("+" && ".join([preMET,preISR  ]) + ")"

preSelection = joinCutStrings([preMET,preISR,preHT])
### Additional Variables:


mt0=80

####
####   Var Templates
####


invMassTemplate =  "sqrt(2*%(TYPE)s_pt*met_pt*(cosh(%(TYPE)s_phi-met_phi)-cos(%(TYPE)s_phi-met_phi)))"
mtTemplate      =  "sqrt(2*%(TYPE)s_pt*met_pt*(1-cos(%(TYPE)s_phi-met_phi)))"
QTemplate       =  "1-%(mt0)s^2/(2*met_pt*%(TYPE)s_pt)"



invMass   = invMassTemplate%{"TYPE":"LepGood"}
mt        = mtTemplate%{"TYPE":"LepGood"}
Q         = QTemplate%{"TYPE":"LepGood","mt0":mt0}
cos       = 'cos(met_phi-LepGood_phi)'
dmt       = Q+":"+cos

mtQline = lambda mt1: "-1*("+str(mt0)+"/"+str(mt1) +')^2*(1 - cos(met_phi-LepGood_phi))+1:cos(met_phi-LepGood_phi)'
#Qcut = lambda mt1: "-1*("+str(mt0)+"/"+str(mt1) +')^2*(cos(met_phi-LepGood_phi)):cos(met_phi-LepGood_phi)'
arbQcut = lambda m,b: ""+str(m)+'*cos(met_phi-LepGood_phi)+'+str(b)
arbQcutline = lambda m,b: arbQcut(m,b)+':cos(met_phi-LepGood_phi)'
arbQcutStr= lambda m, b: '('+Q+')>('+arbQcut(m,b)+')'



binEta=[100,-3,3]
binPT=[100,0,300]
binMT=binPT
binDMT=[40,1.5,-5,40,-1,1]




ht    =             "Sum$(Jet_pt)"
htCut = lambda htv: "(%s>%s)"%(ht,htv)
metCut = lambda met: "(met_pt>%s)"%met

###
###  Signal Regions 
###


SR1="(%s && met_pt>300 && Sum$(nBJetLoose40+nBJetMedium40+nBJetTight40)==0 && LepGood_pdgId==13 && abs(LepGood_eta)<1.5)"%(htCut(300))
SR1a=SR1+"&&(%s<60)"%mt
SR1b=SR1+"&&(%s>60)&&(%s<88)"%(mt,mt)
SR1c=SR1+"&&(%s>88)"%mt



SR1cutList=[
      ["noCut","(1)"],
      ["LepGood","LepGood_pt"],
      ["met300", metCut(300) ],
      ["ht300",htCut(300)],
      ["bVeto","Sum$(nBJetLoose40+nBJetMedium40+nBJetTight40)==0",],
      ["eta1.5","abs(LepGood_eta)<1.5"] ,
      ["ht+met", joinCutStrings([metCut(300),htCut(300) ])],
      ["ht+met+bVeto",joinCutStrings([ "Sum$(nBJetLoose40+nBJetMedium40+nBJetTight40)==0",metCut(300),htCut(300) ])],
      ["ht+met+bVeto+eta",joinCutStrings([ "Sum$(nBJetLoose40+nBJetMedium40+nBJetTight40)==0",metCut(300),htCut(300), "abs(LepGood_eta)<1.5"  ])],
      ["all",SR1],
      ]





syncCutList=[
      #["stCut"," (nLepGood[0]+met_pt > 200)"],
      ["noCut","(1)"],
      ["nMuon==1","(nLepGood==1)&&(abs(LepGood_pdgId[0])==13)"],
      ["dxy0.02 dz0.5","(abs(LepGood_dxy[0])<0.02)&&(abs(LepGood_dz[0])<0.5)"],
      ["pt30 eta2.1","(LepGood_pt[0]<30.)&&(abs(LepGood_eta[0]<2.1))"],
      ["charge","LepGood_charge[0]<0."],
      ["relIso","LepGood_relIso03[0]<0.2"],
      ["met>200","met_pt>200"],
      ["nJet25==2","nJet25==2"],
      ["nBJetLoose25>0","nBJetLoose25>0"],
      ["jetPt>110","Jet_pt[0]>110."],
      #["isrJet","isrJet_pt[0]>300."],
	]

syncCutFlow= makeCutFlowList(syncCutList)


cutDict = [
      {"noCut": "(1)" } ,
      {"preSel": preSelection} ,
      {"muIndex": muSelect} ,
      {"preSel_muIndex": muSelect} ,
      {"SR1": SR1 } ,
      {"presel_SR1": "(%s&&%s)"%(preSelection,SR1) } ,
      {"presel_SR1a": "(%s&&%s)"%(preSelection,SR1a) } ,
      {"presel_SR1b": "(%s&&%s)"%(preSelection,SR1b) } ,
      {"presel_SR1c": "(%s&&%s)"%(preSelection,SR1c) } ,
           ]



cutList = [
      ["noCut", "(1)" ] ,
      ["preSel", preSelection] ,
      ["muIndex", muSelect] ,
      #["preSel_muIndex", "(%s&&%s)"%(muSelect, preSelection)] ,
      ["SR1", SR1 ] ,
      ["presel_SR1", "(%s&&%s)"%(preSelection,SR1) ] ,
      ["presel_SR1a", "(%s&&%s)"%(preSelection,SR1a) ] ,
      ["presel_SR1b", "(%s&&%s)"%(preSelection,SR1b) ] ,
      ["presel_SR1c", "(%s&&%s)"%(preSelection,SR1c) ] ,
           ]








plotDict = {


      #'lep_pt':  {'var':"LepGood_pt",    "presel":preSelection,              "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binPT,  "title":""    ,"xLabel":"lep_pt",    "yLabel":"",     "xLog":0, "yLog":1                  },
      #'lep_MT':     {'var':mt,           "presel":preSelection,              "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binMT,  "title":""    ,"xLabel":"lep_MT",    "yLabel":"",     "xLog":0, "yLog":1                  },
      #'lep_dmt':    {'var':dmt,          "presel":preSelection,              "cut":"(1)", "fillColor":"" ,"color":""     ,"lineWidth":1 , "bin":binDMT, "title":""    ,"xLabel":"cos(\phi)", "yLabel":"Q",    "xLog":0, "yLog":0    ,"zLog":1     },

      'mu_pt':  {'var':"LepGood_pt",    "presel":"(%s&&%s)"%( "(%s)"%" && ".join([muId,muEta,muMiniIso]) ,preSelection), "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binPT,  "title":"Muon P_{T}"    ,"xLabel":"mu_pt",     "yLabel":"",     "xLog":0, "yLog":1                  },
      'mu_MT':     {'var':mt,           "presel":"(%s&&%s)"%( "(%s)"%" && ".join([muId,muEta,muMiniIso]) ,preSelection), "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binMT,  "title":"MT"    ,"xLabel":"MT",        "yLabel":"",     "xLog":0, "yLog":1                  },
      #'mu_MT_presel':     {'var':mt,           "presel":"(%s)"%(preSelection), "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binMT,  "title":"MT"    ,"xLabel":"MT",        "yLabel":"",     "xLog":0, "yLog":1                  },
      'mu_dmt':    {'var':dmt,          "presel":joinCutStrings([preSelection]), "cut":"(1)", "fillColor":"" ,"color":""     ,"lineWidth":1 , "bin":binDMT, "title":"Deconstructed_MT"    ,"xLabel":"cos(\phi)", "yLabel":"Q",    "xLog":0, "yLog":0 ,"zLog":1        },
      'mu_eta':  {'var':"LepGood_eta",    "presel":preSelection, "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binEta,  "title":"Muon Eta"    ,"xLabel":"mu_eta",     "yLabel":"",     "xLog":0, "yLog":1                  },

      }














###############################################################################
###############################################################################
##########################                    #################################
##########################      YIELDS        #################################
##########################                    #################################
###############################################################################
###############################################################################





  
  



#
#
#
#
#
#
#
#




#### WJET DMT

#h2=ROOT.TH2F("h2","h2",*binDMT)
#for w in ["W4", "W2", "W3", "W1"]:
#  sampleWDict[w]['tree'].Draw( plotDict['mu_dmt']['var'] + ">>+h2", "(" + str( sampleWDict[w]['weight'] ) +")*" +plotDict['mu_dmt']['presel'] , "COLZ")














#
