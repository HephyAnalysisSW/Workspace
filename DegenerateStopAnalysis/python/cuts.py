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
                baseCut="(1)",
                ) 


preselection = presel.combined



sr1   = CutClass ("sr1",    [
                              ["negMuon","lepPdg==13"],
                              ["MuEta1.5","abs(lepEta)<1.5"],
                              ["BVeto_Medium25","nBJetMedium25==0"],
                              ["MuPt30","lepPt<30"],
                           ] , 
                  baseCut = presel.combined,
                  )






  








