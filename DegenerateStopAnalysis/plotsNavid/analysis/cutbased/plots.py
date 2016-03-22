from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import Plots

nTrk= 'Sum$((abs(Tracks_dz)<0.1 && abs(Tracks_dxy)<0.1 && Tracks_pt>2.5 && abs( Tracks_eta) <2.5 && Tracks_CosPhiJet12 < 0.707 && (Tracks_matchedJetDr > 0.4 || Jet_pt[Tracks_matchedJetIndex] < 60 )))'

nGenTrk = 'Sum$(( GenTracks_pt>2.5 && abs( GenTracks_eta) <2.5 && GenTracks_CosPhiJet12 < 0.707 && (GenTracks_matchedJetDr > 0.4 || Jet_pt[GenTracks_matchedJetIndex] < 60 )))'

plotDict =\
      {
        "mt":          {'var':"mt"                             ,"bins":[20,0,300]          ,"nMinus1":None         ,"decor":{"title":"MT"    ,"x":"M_{T}"      ,"y":"Events / 15 GeV "  ,'log':[0,1,0] }},
        "mtSR":          {'var':"mt"                           ,"bins":[20,0,200]          ,"nMinus1":None         ,"decor":{"title":"MT"    ,"x":"M_{T}"      ,"y":"Events / 10 GeV "  ,'log':[0,1,0] }},
        "LepPt":       {'var':"lepPt"                          ,"bins":[40,0,200]          ,"nMinus1":"lepPt"      ,"decor":{"title":"LepPt"    ,"x":"Lepton P_{T}"      ,"y":"Events / 5 GeV "  ,'log':[0,1,0] }},
        "LepPtSR":     {'var':"lepPt"                          ,"bins":[35,0,35]           ,"nMinus1":""           ,"decor":{"title":"LepPt"    ,"x":"Lepton P_{T}"      ,"y":"Events / 1 GeV "  ,'log':[0,1,0] }},
        "met":         {'var':"met"                            ,"bins":[20,200,900]        ,"nMinus1":"met"        ,"decor":{"title":"MET"    ,"x":"E^{miss}_{T}"      ,"y":"Events / 35 GeV "  ,'log':[0,1,0] }},
        "ht":         {'var':"htJet30j"                        ,"bins":[20,200,900]        ,"nMinus1":""           ,"decor":{"title":"HT"    ,"x":"H_{T}"      ,"y":"Events / 35 GeV "  ,'log':[0,1,0] }},
        "ct":         {'var':"min(met,htJet30j-100)"           ,"bins":[20,200,900]        ,"nMinus1":""           ,"decor":{"title":"CT"    ,"x":"C_{T}"      ,"y":"Events / 35 GeV "  ,'log':[0,1,0] }},
        "LepEta":       {'var':"lepEta"                        ,"bins":[20,-3,3]           ,"nMinus1":"lepEta"         ,"decor":{"title":"LepEta"    ,"x":"Lepton Eta"      ,"y":"Events  "  ,'log':[0,1,0] }},
        "LepPhi":       {'var':"lepPhi"                        ,"bins":[20,-5,5]           ,"nMinus1":None         ,"decor":{"title":"LepPhi"    ,"x":"Lepton Phi"      ,"y":"Events  "  ,'log':[0,1,0] }},

        #"JetPt":        {'var':"Jet_pt"                        ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"N(Jets Pt>30)"      ,"y":"Events  "  ,'log':[0,1,0] }},
        "nJets30":      {'var':"nJet30"                        ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"N(Jets Pt>30)"      ,"y":"Events  "  ,'log':[0,1,0] }},
        "nJets60":      {'var':"nJet60"                        ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 60GeV"    ,"x":"N(Jets Pt>60)"      ,"y":"Events  "  ,'log':[0,1,0] }},
        "nBJets":       {'var':"(nSoftBJetsCSV +nHardBJetsCSV)" ,"bins":[6,0,6]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets"    ,"x":"N(BJets)"      ,"y":"Events  "  ,'log':[0,1,0] }},
        "nSoftBJets":   {'var':"(nSoftBJetsCSV)"                ,"bins":[6,0,6]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets"    ,"x":"N(BSoftJets)"      ,"y":"Events  "  ,'log':[0,1,0] }},
        "nHardBJets":   {'var':"(nHardBJetsCSV)"                ,"bins":[6,0,6]            ,"nMinus1":None         ,"decor":{"title":"Number of Hard B-Tagged Jets"    ,"x":"N(BHardJets)"      ,"y":"Events  "  ,'log':[0,1,0] }},

      }


newVars = \
    {
        "Q80":         {'var':"Q80"                            ,"bins":[20,-2,1]           ,"nMinus1":None          ,"decor":{"title":"Q80"           ,"x":"Q80"          ,"y":"Events"    ,'log':[0,1,0] }},
        "CosLMet":     {'var':"CosLMet"                        ,"bins":[20,-1,1]           ,"nMinus1":None          ,"decor":{"title":"CosLMet"       ,"x":"CosLMet"      ,"y":"Events"    ,'log':[0,1,0] }},
        "DMT":         {'var':"Q80:CosLMet"                    ,"bins":[20,-1,1,20,-2,1]   ,"nMinus1":None         ,"decor":{"title":"{SAMP} Decons. MT"    ,"x":"CosLMet"      ,"y":" Q80 "  ,'log':[0,0,1] }},

        "QnTrk":         {'var':"Q80:%s"%nTrk                  ,"bins":[30,0,30,20,-2,1]   ,"nMinus1":None         ,"decor":{"title":"Q vs NTrk"    ,"x":"nTrk"      ,"y":"Q80"  ,'log':[0,0,1] }},
        "cosNTrk":       {'var':"CosLMet:%s"%nTrk              ,"bins":[30,0,30,20,-2,1]   ,"nMinus1":None         ,"decor":{"title":"Q vs NTrk"    ,"x":"nTrk"      ,"y":"Q80"  ,'log':[0,0,1] }},
        "QnGenTrk":         {'var':"Q80:%s"%nGenTrk                  ,"bins":[30,0,30,20,-2,1]   ,"nMinus1":None         ,"decor":{"title":"Q vs NGenTrk"    ,"x":"nGenTrk"      ,"y":"Q80"  ,'log':[0,0,1] }},
        "cosNGenTrk":       {'var':"CosLMet:%s"%nGenTrk              ,"bins":[30,0,30,20,-2,1]   ,"nMinus1":None         ,"decor":{"title":"Q vs NGenTrk"    ,"x":"nGenTrk"      ,"y":"Q80"  ,'log':[0,0,1] }},
    }


trackQualityPlots = {

        "CosPhiJet":         {'var':"Track_CosPhiJet12"                  ,"bins":[30,0,30,20,-2,1]   ,"nMinus1":None         ,"decor":{"title":"Q vs NTrk"    ,"x":"nTrk"      ,"y":"Q80"  ,'log':[0,0,1] }},
        "QnTrk":         {'var':"Q80:%s"%nTrk                  ,"bins":[30,0,30,20,-2,1]   ,"nMinus1":None         ,"decor":{"title":"Q vs NTrk"    ,"x":"nTrk"      ,"y":"Q80"  ,'log':[0,0,1] }},

        }

plotDict.update(trackQualityPlots)
plotDict.update(newVars)




plots = Plots(**plotDict)
