from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import Plots
#import Workspace.DegenerateStopAnalysis.navidTools.tracks as tracks


class LepPlots():
    def __init__( self,  lepCollection="LepGood" , lep="mu"):

        self.collection = lepCollection
        self.lep = lep
        lepIndex = "Index{lepCol}_{Lep}".format(lepCol=lepCollection, Lep=lep)


        fargs = {
                   "lepCol"  : lepCollection,
                   "lep"     : lep,
                   "lepIndex": lepIndex,
                }

        print fargs


        #   ## dPhiJetMets: 
        #   dPhiJetMet = "Min$(acos(cos(met_phi- (Jet_phi*(Jet_pt>60) + (  met_phi + 3.14)*(Jet_pt<60)))))"
        #   dPhiJetXMet = lambda x : "Min$(acos(cos(met_phi- (Jet_phi*(Jet_pt>{x}) + (  met_phi + 3.14)*(Jet_pt<{x})))))".format(x=x)
        #   
        #   l=["Alt$(acos(cos(met_phi-(Jet_phi[{x}]*(Jet_pt[{x}]>{{jpt}})+(met_phi+3.14)*(Jet_pt[{x}]<{{jpt}}) ))), 999 )".format(x=x) for x in range(4)]
        #   mins = ["min(%s,%s)"%( l[ i ],l[ i+1 ]) for i in range(0,len(l)-1,2)]
        #   dPhiJets60_1to4Met_var = ("min(%s,%s)"%tuple(mins)).format(jpt=60)
        #   dPhi4JetsXMet = lambda x:  ("min(%s,%s)"%tuple(mins)).format(jpt=x)
        #   
        #   l=["Alt$(acos(cos(met_phi-(Jet_phi[{x}]*(Jet_pt[{x}]>{{jpt}})+(met_phi+3.14)*(Jet_pt[{x}]<{{jpt}}) ))), 999 )".format(x=x) for x in range(2)]
        #   dPhi2JetsXMet = lambda x:  ("min(%s,%s)"%tuple(l)).format(jpt=x)
        
        
        
        plotDict =\
              {
                "{lep}mt".format(**fargs):           {'var':"{lepCol}_mt[{lepIndex}[0]]".format(**fargs)      ,"bins":[60,0,200]          ,"nMinus1":None         ,"decor":{"title":"{lep}MT".format(**fargs)    ,"x":"{lep} M_{{T}}".format(**fargs)      ,"y":"Events / 15 GeV "  ,'log':[0,1,0] }},
                "{lep}mtSR".format(**fargs):         {'var':"{lepCol}_mt[{lepIndex}[0]]".format(**fargs)       ,"bins":[20,0,200]          ,"nMinus1":None         ,"decor":{"title":"{lep}MT".format(**fargs)    ,"x":"{lep} M_{{T}}".format(**fargs)      ,"y":"Events / 15 GeV "  ,'log':[0,1,0] }},
                #"mtSR":        {'var':"mt"                           ,"bins":[30,0,150]          ,"nMinus1":None         ,"decor":{"title":"MT"    ,"x":"M_{T}"      ,"y":"Events / 5 GeV "  ,'log':[0,1,0] }},
                "{lep}Pt".format(**fargs) :        {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)       ,"bins":[40,0,200]          ,"nMinus1":""      ,"decor":{"title":"{lep}Pt".format(**fargs)     ,"x":"{lep} P_{{T}}".format(**fargs)       ,"y":"Events / 5 GeV "  ,'log':[0,1,0] }},
                "{lep}PtSR".format(**fargs) :      {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)        ,"bins":[35,0,35]           ,"nMinus1":""           ,"decor":{"title":"{lep}Pt".format(**fargs)     ,"x":"{lep} P_{{T}}".format(**fargs)       ,"y":"Events / 1 GeV "  ,'log':[0,1,0] }},
                "{lep}Eta".format(**fargs) :       {'var':"{lepCol}_eta[{lepIndex}[0]]".format(**fargs)                         ,"bins":[20,-3,3]           ,"nMinus1":""         ,"decor":{"title":"{lep}Eta".format(**fargs)     ,"x":"{lep} Eta".format(**fargs)       ,"y":"Events  "  ,'log':[0,1,0] }},
                "{lep}Phi".format(**fargs) :      {'var':"{lepCol}_phi[{lepIndex}[0]]".format(**fargs)                         ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"{lep}Phi".format(**fargs)     ,"x":"{lep} Phi".format(**fargs)       ,"y":"Events  "  ,'log':[0,1,0] }},
                "met":          {'var':"met"                            ,"bins":[20,200,900]        ,"nMinus1":"met"        ,"decor":{"title":"MET"    ,"x":"E^{miss}_{T}"      ,"y":"Events / 35 GeV "  ,'log':[0,1,0] }},
                "ht":           {'var':"ht_basJet"                     ,"bins":[20,200,900]        ,"nMinus1":""           ,"decor":{"title":"HT"    ,"x":"H_{T}"      ,"y":"Events / 35 GeV "  ,'log':[0,1,0] }},
                "ct":           {'var':"min(met_pt,ht_basJet)"                ,"bins":[20,200,900]        ,"nMinus1":""           ,"decor":{"title":"CT"    ,"x":"C_{T}"      ,"y":"Events / 35 GeV "  ,'log':[0,1,0] }},
                "MetPhi":      {'var':"met_phi"                        ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"MetPhi"    ,"x":"Met Phi"      ,"y":"Events  "  ,'log':[0,1,0] }},
                #"dPhiJet12":   {'var':"deltaPhi_j12"                  ,"bins":[20,0,3.2]          ,"nMinus1":None         ,"decor":{"title":"dPhi_J12"    ,"x":"dPhi_J12"      ,"y":"Events "  ,'log':[0,1,0] }},
                #"dPhiJetMet":  {'var':dPhiJetMet                      ,"bins":[20,0,3.2]          ,"nMinus1":None         ,"decor":{"title":"dPhi_JetMet"    ,"x":"dPhi_JetMet"      ,"y":"Events "  ,'log':[0,1,0], 'fom_reverse':True }},
                #"MetOverHT":   {'var':"met_pt/htJet30j"               ,"bins":[20,0,4]            ,"nMinus1":None         ,"decor":{"title":"MetOverHT"    ,"x":"Met/HT"      ,"y":"Events "  ,'log':[0,1,0], 'fom_reverse':False }},
                "isrPt":       {'var':"Jet_pt[IndexJet_basJet[0]]"     ,"bins":[60,100,500]          ,"nMinus1":None         ,"decor":{"title":"PT of Leading Jet"    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets30":      {'var':"nBasJet"                        ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"N(Jet_{Pt>30})"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets60":      {'var':"nVetoJet"                        ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 60GeV"    ,"x":"N(Jet_{Pt>60})"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nSoftBJets":   {'var':"(nBSoftJet)"                ,"bins":[6,0,6]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets"    ,"x":"N(BSoftJets)"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nHardBJets":   {'var':"(nBHardJet)"                ,"bins":[6,0,6]            ,"nMinus1":None         ,"decor":{"title":"Number of Hard B-Tagged Jets"    ,"x":"N(BHardJets)"      ,"y":"Events  "  ,'log':[0,1,0] }},
        
              }
        
        
        
        
        
        
        
        self.plots = Plots(**plotDict)
        self.plots = Plots(**plotDict)
        
        
        
        
        self.nminus1s=   {
                            "met":          ["met","CT"]   , 
                            "mt":           ["mt"]   , 
                            "ht":           ["ht","CT"]   , 
                            "ct":           ["CT"]   , 
                            "{lep}Phi".format(**fargs) :       [""]   , 
                            "{lep}Eta".format(**fargs) :       ["lepEta".format(**fargs) ]   , 
                            "nJets30":      ["",]   , 
                            "nJets60":      ["Jet60"]   , 
                            #"nBJets":       ["BVeto"]   , 
                            "nBJets":       ["CRTT2", ""]   , 
                            "nSoftBJets":   ["Soft"]   , 
                            "nHardBJets" :  ["Hard"]   , 
                            #"{lep}Pt":        ["lepPt","MuPt"]
                            #"{lep}Pt":        [""],
                    }




if __name__ == "__main__":
    lepPlots = LepPlots("LepGood","lep")
    muPlots  = LepPlots("LepGood","mu")
    elPlots  = LepPlots("LepGood","el")

