from Workspace.DegenerateStopAnalysis.tools.degTools import Plots
#import Workspace.DegenerateStopAnalysis.tools.tracks as tracks
from Workspace.DegenerateStopAnalysis.tools.degTools import getPlotFromChain
import ROOT

class DegPlots():

    #( sample , bins = plot.bins, cutString=cut_str, weight=weight_str, addOverFlowBin=addOverFlowBin, binningIsExplicit=binningIsExplicit)

    @staticmethod
    def makeNBJetPlotFunc(bjet_var):
        def nBJetPlot( sample, bins, cutString, weight, addOverFlowBin = '', binningIsExplicit = False, bjet_var="nBJet"):
            from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import btag_to_weight_vars, weight_to_btag_vars
            nBs = min(bins[-1], 2)
            hists = []
            if sample.isData:
                histo = getPlotFromChain( sample.tree, bjet_var,  bins, cutString, weight, addOverFlowBin=addOverFlowBin, binningIsExplicit=binningIsExplicit, uniqueName = True)
            else:
                hist_lists = ROOT.TList()
                for nB in range(nBs+1):
                    bTagWeight = btag_to_weight_vars[bjet_var]%nB 
                    print bTagWeight
                    hist_ = getPlotFromChain( sample.tree,  "%s"%nB ,  bins , cutString , weight +"* %s"%bTagWeight ,  addOverFlowBin= addOverFlowBin, binningIsExplicit= binningIsExplicit, uniqueName = True)
                    hist_lists.Add(hist_)
                bTagWeight = "( %s - %s )"%( btag_to_weight_vars[bjet_var]%(str(nBs)+"p") ,  btag_to_weight_vars[bjet_var]%(nBs) )
                print "%s"%(nB+1) ,   bTagWeight
                hist_ = getPlotFromChain( sample.tree,  "%s"%(nB+1) ,  bins , cutString , weight +"* %s"%bTagWeight ,  addOverFlowBin= addOverFlowBin, binningIsExplicit= binningIsExplicit, uniqueName = True)
                hist_lists.Add(hist_)
                histo = hist_.Clone()
                histo.Reset()
                histo.Merge(hist_lists)
            return histo
        return nBJetPlot

    

    #def nBJetPlot( sample, bins, cutString, weight, addOverFlowBin = '', binningIsExplicit = False, bjet_var="nBJet"):
    #    from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import btag_to_weight_vars, weight_to_btag_vars
    #    nBs = min(bins[-1], 2)
    #    hists = []
    #    if sample.isData:
    #        histo = getPlotFromChain( sample.tree, bjet_var,  bins, cutString, weight, addOverFlowBin=addOverFlowBin, binningIsExplicit=binningIsExplicit, uniqueName = True)
    #    else:
    #        hist_lists = ROOT.TList()
    #        for nB in range(nBs+1):
    #            bTagWeight = btag_to_weight_vars[bjet_var]%nB 
    #            print bTagWeight
    #            hist_ = getPlotFromChain( sample.tree,  "%s"%nB ,  bins , cutString , weight +"* %s"%bTagWeight ,  addOverFlowBin= addOverFlowBin, binningIsExplicit= binningIsExplicit, uniqueName = True)
    #            hist_lists.Add(hist_)
    #        bTagWeight = "(1-%s)%"%btag_to_weight_vars[bjet_var]%(nBs) 
    #        print "%s"%(nB+1) ,   bTagWeight
    #        hist_ = getPlotFromChain( sample.tree,  "%s"%(nB+1) ,  bins , cutString , weight +"* %s"%bTagWeight ,  addOverFlowBin= addOverFlowBin, binningIsExplicit= binningIsExplicit, uniqueName = True)
    #        hist_lists.Add(hist_)
    #        histo = hist_.Clone()
    #        histo.Reset()
    #        histo.Merge(hist_lists)
    #    return histo



    def __init__( self,  lepCollection="LepGood" , lep="mu"):

        self.collection = lepCollection
        self.lep = lep
        lepIndex = "Index{lepCol}_{Lep}".format(lepCol=lepCollection, Lep=lep)


        fargs = {
                   "lepCol"  : lepCollection,
                   "lep"     : lep,
                   "lepIndex": lepIndex,
                    "lepLatex": { "mu":"mu", "el":"e","lep":"l" }[lep],
                    "lepTitle": { "mu":"Mu", "el":"El","lep":"Lep" }[lep],
        
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
                "{lepTitle}mt".format(**fargs):           {'var':"{lepCol}_mt[{lepIndex}[0]]".format(**fargs)       ,"bins":[40,0,200]          ,"nMinus1":None         ,"decor":{"title":"{lep}MT".format(**fargs)    ,"x":"M_{{T}}({lepLatex}) ".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
                "{lepTitle}mtSR".format(**fargs):         {'var':"{lepCol}_mt[{lepIndex}[0]]".format(**fargs)       ,"bins":[20,0,200]          ,"nMinus1":None         ,"decor":{"title":"{lep}MT".format(**fargs)    ,"x":"M_{{T}}({lepLatex}) ".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
                #"mtSR":        {'var':"mt"                           ,"bins":[30,0,150]          ,"nMinus1":None         ,"decor":{"title":"MT"    ,"x":"M_{T}"      ,"y":"Events / 5 GeV "  ,'log':[0,1,0] }},
                "{lepTitle}Pt".format(**fargs) :        {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)       ,"bins":[40,0,200]          ,"nMinus1":""      ,"decor":{"title":"{lep}Pt".format(**fargs)           ,"x":"P_{{T}}({lepLatex})".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "{lepTitle}PtSR".format(**fargs) :      {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)        ,"bins":[35,0,35]           ,"nMinus1":""           ,"decor":{"title":"{lep}Pt".format(**fargs)     ,"x":"P_{{T}}({lepLatex})".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "{lepTitle}Eta".format(**fargs) :       {'var':"{lepCol}_eta[{lepIndex}[0]]".format(**fargs)                         ,"bins":[20,-3,3]           ,"nMinus1":""         ,"decor":{"title":"{lep}Eta".format(**fargs)     ,"x":"#eta({lepLatex})".format(**fargs)       ,"y":"Events  "  ,'log':[0,1,0] }},
                "{lepTitle}Phi".format(**fargs) :      {'var':"{lepCol}_phi[{lepIndex}[0]]".format(**fargs)                         ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"{lep}Phi".format(**fargs)     ,"x":"{lep} Phi".format(**fargs)       ,"y":"Events  "  ,'log':[0,1,0] }},
                "met":          {'var':"met"                            ,"bins":[40,200,1000]        ,"nMinus1":"met"        ,"decor":{"title":"MET"    ,"x":"E^{miss}_{T}"      ,"y":"Events"  ,'log':[0,1,0] }},
                "ht":           {'var':"ht_basJet"                     ,"bins":[40,200,1000]        ,"nMinus1":""           ,"decor":{"title":"HT"    ,"x":"H_{T}"      ,"y":"Events"  ,'log':[0,1,0] }},
                "ct":           {'var':"min(met_pt,ht_basJet)"         ,"bins":[40,100,1000]        ,"nMinus1":""           ,"decor":{"title":"CT"    ,"x":"C_{T}"      ,"y":"Events"  ,'log':[0,1,0] }},
                "MetPhi":      {'var':"met_phi"                        ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"MetPhi"    ,"x":"Met Phi"      ,"y":"Events"  ,'log':[0,1,0] }},
                #"dPhiJet12":   {'var':"deltaPhi_j12"                  ,"bins":[20,0,3.2]          ,"nMinus1":None         ,"decor":{"title":"dPhi_J12"    ,"x":"dPhi_J12"      ,"y":"Events "  ,'log':[0,1,0] }},
                #"dPhiJetMet":  {'var':dPhiJetMet                      ,"bins":[20,0,3.2]          ,"nMinus1":None         ,"decor":{"title":"dPhi_JetMet"    ,"x":"dPhi_JetMet"      ,"y":"Events "  ,'log':[0,1,0], 'fom_reverse':True }},
                #"MetOverHT":   {'var':"met_pt/htJet30j"               ,"bins":[20,0,4]            ,"nMinus1":None         ,"decor":{"title":"MetOverHT"    ,"x":"Met/HT"      ,"y":"Events "  ,'log':[0,1,0], 'fom_reverse':False }},
                "isrPt":       {'var':"Jet_pt[IndexJet_basJet[0]]"     ,"bins":[45,100,1000]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}}"    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrPt2":       {'var':"Jet_pt[IndexJet_basJet[0]]"     ,"bins":[20,100,900]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}}"    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrPt_fine":   {'var':"Jet_pt[IndexJet_basJet[0]]"    ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}} "    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets30":      {'var':"nBasJet"                       ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"Number of Jets with P_{T} > 30GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets60":      {'var':"nVetoJet"                      ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 60GeV"    ,"x":"Number of Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nSoftBJets":   {'var':"(nBSoftJet)"                   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets with P_{{T}} < 60GeV"    ,"x":"Number of Soft B-Tagged Jets with P_{T} < 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nHardBJets":   {'var':"(nBHardJet)"                   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets with P_{{T}} > 60GeV"    ,"x":"Number of Hard B-Tagged Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nBJets":       {'var':"(nBHardJet + nBSoftJet)"       ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets"                         ,"x":"Number of B-Tagged Jets"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nBJetsWeight": {'var':self.makeNBJetPlotFunc("nBJet")       ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets"                         ,"x":"Number of B-Tagged Jets"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nSoftBJetsWeight":   {'var':self.makeNBJetPlotFunc("nBSoftJet")   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets with P_{{T}} < 60GeV"    ,"x":"Number of Soft B-Tagged Jets with P_{T} < 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nHardBJetsWeight":   {'var':self.makeNBJetPlotFunc("nBHardJet")   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets with P_{{T}} > 60GeV"    ,"x":"Number of Hard B-Tagged Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "bJetPt":       {'var':"Jet_pt[ max(IndexJet_bJet[0],0)] *(nBJet>0)"      ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"bJet P_{{T}} "    ,"x":"P_{T}(BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "bSoftJetPt":       {'var':"Jet_pt[ max(IndexJet_bSoftJet[0],0)] *(nBSoftJet>0)"      ,"bins":[10,20,70]          ,"nMinus1":None         ,"decor":{"title":"bSoftJet P_{{T}} "    ,"x":"P_{T}(Soft BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "bHardJetPt":       {'var':"Jet_pt[ max(IndexJet_bHardJet[0],0)] *(nBHardJet>0)"      ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"bHardJet P_{{T}} "    ,"x":"P_{T}(Hard BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
              }
        
        
        
        
        
        
        
        self.plots = Plots(**plotDict)
        
        
        
        
        self.nminus1s=   {
                            "met":          ["",""]   , 
                            "mt":           ["mt"]   , 
                            "ht":           ["ht","CT"]   , 
                            "ct":           ["CT"]   , 
                            "{lep}Phi".format(**fargs) :       [""]   , 
                            "{lep}Eta".format(**fargs) :       ["lepEta".format(**fargs) ]   , 
                            "nJets30":      ["",]   , 
                            "nJets60":      ["Jet60"]   , 
                            #"nBJets":       ["BVeto"]   , 
                            "nBJets":       ["BJet"]   , 
                            "nSoftBJets":   ["Soft"]   , 
                            "nHardBJets" :  ["Hard"]   , 
                            "bSoftJetPt" :  ["Soft"]   , 
                            "bHardJetPt" :  ["Hard", "Soft"]   , 
                            "bJetPt" :      ["Hard","Soft"]   , 
                            #"isrPt" :       ["ISR", "HT", "MET", "CT"]   , 
                            "isrPt_fine" :       ["ISR", "HT", "MET", "CT", "Jet60"]   , 
                            #"nHardBJets" :  ["Hard"]   , 
                            #"{lep}Pt":        ["lepPt","MuPt"]
                            #"{lep}Pt":        [""],
                    }




if __name__ == "__main__":
    lepPlots = degPlots("LepGood","lep")
    muPlots  = degPlots("LepGood","mu")
    elPlots  = degPlots("LepGood","el")

