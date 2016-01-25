from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import Plots
from Workspace.DegenerateStopAnalysis.cuts import *
import ROOT
import math



plots =Plots(**
      {
        "Q80":         {'var':"Q80"                            ,"bins":[20,-2,1]           ,"nMinus1":None          ,"decor":{"title":"Q80"           ,"x":"Q80"          ,"y":"nEvents"    ,'log':[0,1,0] }},
        "CosLMet":     {'var':"CosLMet"                        ,"bins":[20,-1,1]           ,"nMinus1":None          ,"decor":{"title":"CosLMet"       ,"x":"CosLMet"      ,"y":"nEvents"    ,'log':[0,1,0] }},
        "DMT":         {'var':"Q80:CosLMet"                    ,"bins":[20,-1,1,20,-2,1]   ,"nMinus1":None         ,"decor":{"title":"{SAMP} Decons. MT"    ,"x":"CosLMet"      ,"y":"Q80"  ,'log':[0,0,1] }},
        "mt":          {'var':"mt"                             ,"bins":[20,0,300]          ,"nMinus1":None         ,"decor":{"title":"MT"    ,"x":"M_{T}"      ,"y":"nEvents"  ,'log':[0,1,0] }},
        "LepPt":       {'var':"lepPt"                          ,"bins":[20,0,300]          ,"nMinus1":"lepPt"         ,"decor":{"title":"LepPt"    ,"x":"Lepton P_{T}"      ,"y":"nEvents"  ,'log':[0,1,0] }},
        "met":         {'var':"met"                            ,"bins":[20,150,800]          ,"nMinus1":"met"         ,"decor":{"title":"MET"    ,"x":"MET"      ,"y":"nEvents"  ,'log':[0,1,0] }},
        "LepEta":       {'var':"lepEta"                        ,"bins":[20,-3,3]           ,"nMinus1":"lepEta"         ,"decor":{"title":"LepEta"    ,"x":"Lepton Eta"      ,"y":"nEvents"  ,'log':[0,0,0] }},
        "LepPhi":       {'var':"lepPhi"                        ,"bins":[20,-5,5]           ,"nMinus1":None         ,"decor":{"title":"LepPhi"    ,"x":"Lepton Phi"      ,"y":"nEvents"  ,'log':[0,0,0] }},

      }
        )
