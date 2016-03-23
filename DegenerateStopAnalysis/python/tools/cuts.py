import math
from Workspace.DegenerateStopAnalysis.navidTools.CutTools import *


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



presel = CutClass ("presel", [
                              ["MET200","met>200"],
                              ["ISR110","nJet110>=1" ],
                              ["HT300","htJet30j>300"],
                              ["2ndJetPt60","nJet60<=2 "],
                              ["AntiQCD", "deltaPhi_j12 < 2.5" ],
                              ["singleLep",    "nlep==1"  ],
                            ] ,
                baseCut=None,
                ) 
preselection = presel.combined



sr1   = CutClass ("sr1",    [
                              ["negMuon","lepPdgId==13"],
                              ["MuEta1.5","abs(lepEta)<1.5"],
                              ["BVeto_Medium25","nBJetMedium25==0"],
                              ["MuPt30","lepPt<30"],
                              ["met300","met>300"],
                              ["HT400","htJet30j>400"],
                           ] , 
                  baseCut = presel,
                  )


sr1Loose   = CutClass ("sr1_loose",    [
                              ["negMuon","lepPdgId==13"],
                              ["MuEta1.5","abs(lepEta)<1.5"],
                              ["BVeto_Medium25","nBJetMedium25==0"],
                              ["MuPt30","lepPt<30"],
                              #["met300","met>300"],
                              #["HT400","htJet30j>400"],
                           ] , 
                  baseCut = presel,
                  )


sr1abc   = CutClass ("sr1abc",    [
                               ["SR1a","mt<60"],
                                  ["SR1a_1",joinCutStrings(   ["mt<60",         btw("lepPt",5,12)]  )],
                                  ["SR1a_2",joinCutStrings(   ["mt<60",         btw("lepPt",12,20)] )],
                                  ["SR1a_3",joinCutStrings(   ["mt<60",         btw("lepPt",20,30)] )],
                               ["SR1b",btw("mt",60,88)],
                                  ["SR1b_1",joinCutStrings(   [btw("mt",60,88), btw("lepPt",5,12)]  )],
                                  ["SR1b_2",joinCutStrings(   [btw("mt",60,88), btw("lepPt",12,20)] )],
                                  ["SR1b_3",joinCutStrings(   [btw("mt",60,88), btw("lepPt",20,30)] )],
                               ["SR1c","mt>88"],
                                  ["SR1c_1",joinCutStrings(   ["mt>88",         btw("lepPt",5,12)]  )],
                                  ["SR1c_2",joinCutStrings(   ["mt>88",         btw("lepPt",12,20)] )],
                                  ["SR1c_3",joinCutStrings(   ["mt>88",         btw("lepPt",20,30)] )],
                           ] , 
                  baseCut = sr1,
                  )


  








