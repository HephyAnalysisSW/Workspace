import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
from Workspace.DegenerateStopAnalysis.tools.degTools import Plots
#import Workspace.DegenerateStopAnalysis.tools.tracks as tracks
from Workspace.DegenerateStopAnalysis.tools.degTools import getPlotFromChain
import ROOT



def compareBJets( tree, btag_var="nJet_bJet_def", btag_weight = "weightBTag%s_MC_def"):
    unq = degTools.uniqueHash()
    def_col = tree.GetLineColor()
    tree.SetLineWidth(2)
    tree.SetLineColor(ROOT.kBlue)
    binning = (4,0,4)
    btname = btag_var + "_"+unq
    tree.Draw(btag_var+">>%s%s"%(btname, str(binning)))
    tree.SetLineColor(def_col)
    tree.SetLineWidth(1)
    bwname = btag_weight.replace(r"%s","")+"_"+unq
    tree.Draw("(0)>>%s%s"%(bwname, str(binning)), btag_weight%"0", "same")
    tree.Draw("(1)>>+%s"%(bwname), btag_weight%"1", "same")
    tree.Draw("(2)>>+%s"%(bwname), btag_weight%"2", "same")
    tree.Draw("(3)>>+%s"%(bwname), btag_weight%"2p" + "-" + btag_weight%"2", "same" )
    h1 = getattr(ROOT,btname)
    h2 = getattr(ROOT,bwname)
    return h1,h2




class DegPlots():

    #( sample , bins = plot.bins, cutString=cut_str, weight=weight_str, addOverFlowBin=addOverFlowBin, binningIsExplicit=binningIsExplicit)

    @staticmethod
    def makeNBJetPlotFunc(bjet_var):
        def nBJetPlot( sample, bins, cutString, weight, addOverFlowBin = '', binningIsExplicit = False, bjet_var=bjet_var):
            #from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import btag_to_weight_vars, weight_to_btag_vars, sf_to_btag , btag_to_sf
            from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import BTagSFMap
            btag_sf_map = BTagSFMap('sf')

            
            btag_to_weight_vars    =  btag_sf_map.btag_to_weight_vars     
            weight_to_btag_vars    =  btag_sf_map.weight_to_btag_vars         
            sf_to_btag             =  btag_sf_map.sf_to_btag              
            btag_to_sf             =  btag_sf_map.btag_to_sf              

            nBs = min(bins[-1], 2)
            hists = []

            if sample.isData:
                cutString_ = cutString
                #cutString_ = cutString_.replace("((nBHardJet + nBSoftJet)== 0 )","((nBHardJet)== 0 )")
                #cutString_ = cutString_.replace("((nBHardJet + nBSoftJet)== 0 )","(1)")
                histo = getPlotFromChain( sample.tree, bjet_var,  bins, cutString_, weight, addOverFlowBin=addOverFlowBin, binningIsExplicit=binningIsExplicit, uniqueName = True)
            else:
                hist_lists = ROOT.TList()
                for nB in range(nBs+1):
                    bTagWeight = btag_to_weight_vars[bjet_var]%nB 
                    #print btag_to_weight_vars
                    print bjet_var + "  >>>  " + bTagWeight
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

    @staticmethod
    def makeNBJetPlotFunc2(bjet_var):
        def nBJetPlot( sample, bins, cutString, weight, addOverFlowBin = '', binningIsExplicit = False, bjet_var=bjet_var):
            #from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import btag_to_weight_vars, weight_to_btag_vars, sf_to_btag , btag_to_sf
            from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import BTagSFMap
            btag_sf_map = BTagSFMap('sf')

            
            btag_to_weight_vars    =  btag_sf_map.btag_to_weight_vars     
            weight_to_btag_vars    =  btag_sf_map.weight_to_btag_vars         
            sf_to_btag             =  btag_sf_map.sf_to_btag              
            btag_to_sf             =  btag_sf_map.btag_to_sf              

            nBs = min(bins[-1], 2)
            hists = []

            if sample.isData:
                cutString_ = cutString[:]
                sample.tree.SetEventList(0)
                if bjet_var == "nBSoftJet":
                    pass
                elif bjet_var == "nBHardJet":
                    pass
                #cutString_ = cutString_.replace("((nBHardJet + nBSoftJet)== 0 )","((nBHardJet)== 0 )")
                #cutString_ = cutString_.replace("((nBHardJet + nBSoftJet)== 0 )","(1)")
                cutString_ = cutString_.replace("(nBSoftJet>=1) && (nBHardJet==0)","(nBHardJet==0)")
                histo = getPlotFromChain( sample.tree, bjet_var,  bins, cutString_, weight, addOverFlowBin=addOverFlowBin, binningIsExplicit=binningIsExplicit, uniqueName = True)
            else:
                hist_lists = ROOT.TList()
                for nB in range(nBs+1):
                    #bVeto = "weightHBTag0_SF"
                    bVeto = "(1)"
                    bTagWeight = "(%s)*(%s)"%((btag_to_weight_vars[bjet_var]%nB), bVeto)
                    #print btag_to_weight_vars
                    print bjet_var + "  >>>  " + bTagWeight
                    weightStr = weight +"* %s"%bTagWeight
                    weightStr_ = weightStr.replace("(weightSBTag1p_SF * weightHBTag0_SF)","(1)")
                    #print "Cut: %s"%cutString
                    print "Weight: %s"%weightStr_
                    hist_ = getPlotFromChain( sample.tree,  "%s"%nB ,  bins , cutString , weightStr_,  addOverFlowBin= addOverFlowBin, binningIsExplicit= binningIsExplicit, uniqueName = True)
                    hist_lists.Add(hist_)
                bTagWeight = "( %s - %s )*(%s)"%( btag_to_weight_vars[bjet_var]%(str(nBs)+"p") ,  btag_to_weight_vars[bjet_var]%(nBs) , bVeto)
                print "%s"%(nB+1) ,   bTagWeight
                weightStr = weight +"* %s"%bTagWeight 
                #print "Cut: %s"%cutString
                print "Weight: %s"%weightStr_
                weightStr_ = weightStr.replace("(weightSBTag1p_SF * weightHBTag0_SF)","(1)")
                hist_ = getPlotFromChain( sample.tree,  "%s"%(nB+1) ,  bins , cutString , weightStr_ ,  addOverFlowBin= addOverFlowBin, binningIsExplicit= binningIsExplicit, uniqueName = True)
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



    def __init__( self,  lepCollection="LepGood" , lep="mu", lepThresh="", jetThresh="", variables=None):
        """
        

        """

        self.collection = lepCollection
        self.lep = lep if not lepThresh else lep+"_"+lepThresh
        lepIndex = "Index{lepCol}_{Lep}".format(lepCol=lepCollection, Lep=self.lep)
        basJet   = "basJet"
        jetCol   = "Jet"
        jet      = basJet if not jetThresh else basJet + "_" + jetThresh

        fargs = {
                   "lepCol"  : lepCollection,
                   "lep"     : lep if not lepThresh else lep+"_"+lepThresh,
                   "lepIndex": lepIndex,
                   "lepLatex": { "mu":"mu", "el":"e","lep":"l"    }[lep],
                   "lepTitle": { "mu":"Mu", "el":"El","lep":"Lep" }[lep],
                   "jet"     : jet, 
                   "jetCol"  : jetCol,
                   "jetIndex": "Index%s_%s"%(jetCol,jet),
                   "jetThresh": jetThresh,
                   "jetTitle": "",
                }



        wpt = "(sqrt(({lepCol}_pt[max(0,{lepIndex}[0])]*cos({lepCol}_phi[max(0,{lepIndex}[0])]) + met_pt*cos(met_phi) ) **2 + ( {lepCol}_pt[max(0,{lepIndex}[0])]*sin({lepCol}_phi[max(0,{lepIndex}[0])])+met_pt*sin(met_phi) )^2 ))".format(lepCol = lepCollection , lepIndex = lepIndex, Lep=lep)


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
                "Lepmt":           {'var':"{lepCol}_mt[{lepIndex}[0]]".format(**fargs)       ,"bins":[40,0,200]          ,"nMinus1":None         ,"decor":{"title":"{lep}MT".format(**fargs)    ,"x":"M_{{T}}({lepLatex}, E^{{miss}}_{{T}}) [GeV] ".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
                "LepmtSR":         {'var':"{lepCol}_mt[{lepIndex}[0]]".format(**fargs)       ,"bins":[20,0,200]          ,"nMinus1":None         ,"decor":{"title":"{lep}MT".format(**fargs)    ,"x":"M_{{T}}({lepLatex}, E^{{miss}}_{{T}}) [GeV]".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
                #"mtSR":        {'var':"mt"                           ,"bins":[30,0,150]          ,"nMinus1":None         ,"decor":{"title":"MT"    ,"x":"M_{T}"      ,"y":"Events / 5 GeV "  ,'log':[0,1,0] }},
                "LepPt" :        {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)       ,"bins":[40,0,200]          ,"nMinus1":""      ,"decor":{"title":"{lep}Pt".format(**fargs)           ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "LepPtNMinus1" : {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)       ,"bins":[40,0,500]          ,"nMinus1":"LepPt"      ,"decor":{"title":"{lep}Pt".format(**fargs)           ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "LepPtSR" :      {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)        ,"bins":[35,0,35]           ,"nMinus1":""           ,"decor":{"title":"{lep}Pt".format(**fargs)     ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "LepEta" :       {'var':"{lepCol}_eta[{lepIndex}[0]]".format(**fargs)                         ,"bins":[20,-3,3]           ,"nMinus1":""         ,"decor":{"title":"{lep}Eta".format(**fargs)     ,"x":"#eta({lepLatex})".format(**fargs)       ,"y":"Events  "  ,'log':[0,1,0] }},
                "LepPhi" :      {'var':"{lepCol}_phi[{lepIndex}[0]]".format(**fargs)                         ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"{lep}Phi".format(**fargs)     ,"x":"{lep} Phi".format(**fargs)       ,"y":"Events  "  ,'log':[0,1,0] }},
                "met":          {'var':"met"                            ,"bins":[40,200,1000]        ,"nMinus1":"met"        ,"decor":{"title":"MET"    ,"x":"E^{miss}_{T} [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "ht":           {'var':"ht_{jet}".format(**fargs)       ,"bins":[40,200,1000]        ,"nMinus1":""           ,"decor":{"title":"HT"    ,"x":"H_{T} [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "ht2":           {'var':"ht_{jet}".format(**fargs)  ,"bins":[100,200,2000]        ,"nMinus1":""           ,"decor":{"title":"HT"    ,"x":"H_{T} [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "ct":           {'var':"min(met_pt,ht_{jet})".format(**fargs)         ,"bins":[40,100,1000]        ,"nMinus1":""           ,"decor":{"title":"CT"    ,"x":"C_{T} [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "MetPhi":      {'var':"met_phi"                        ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"MetPhi"    ,"x":"Met Phi"      ,"y":"Events"  ,'log':[0,1,0] }},
                #"dPhiJet12":   {'var':"deltaPhi_j12"                  ,"bins":[20,0,3.2]          ,"nMinus1":None         ,"decor":{"title":"dPhi_J12"    ,"x":"dPhi_J12"      ,"y":"Events "  ,'log':[0,1,0] }},
                #"dPhiJetMet":  {'var':dPhiJetMet                      ,"bins":[20,0,3.2]          ,"nMinus1":None         ,"decor":{"title":"dPhi_JetMet"    ,"x":"dPhi_JetMet"      ,"y":"Events "  ,'log':[0,1,0], 'fom_reverse':True }},
                #"MetOverHT":   {'var':"met_pt/htJet30j"               ,"bins":[20,0,4]            ,"nMinus1":None         ,"decor":{"title":"MetOverHT"    ,"x":"Met/HT"      ,"y":"Events "  ,'log':[0,1,0], 'fom_reverse':False }},
                "isrPt":       {'var':"Jet_pt[{jetIndex}[0]]".format(**fargs)     ,"bins":[45,100,1000]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}} [GeV]"    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},


                "wpt":          {'var':wpt                            ,"bins":[40,200,1000]        ,"nMinus1":""        ,"decor":{"title":"WPT"    ,"x":"P_{T}(W) [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},

                "isrPt2":       {'var':"Jet_pt[{jetIndex}[0]]".format(**fargs)     ,"bins":[20,100,900]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}} [GeV]"    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrEta":       {'var':"Jet_eta[{jetIndex}[0]]".format(**fargs)   ,"bins":[20,-3,3]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet Eta "    ,"x":"#eta(LeadingJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},


                #
                #   ISR Quality Plots
                #
                "isrcharge":     {'var':"Jet_charge[{jetIndex}[0]]".format(**fargs)     ,"bins":[20,-2,2]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet Charge"                           ,"x": "Leading Jet Charge"                            ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrchHEF":      {'var':"Jet_chHEF[{jetIndex}[0]]".format(**fargs)      ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Leading Jet Charge Hadron Fraction"           ,"x": "Leading Jet Charge Hadron Fraction"            ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrneHEF":      {'var':"Jet_neHEF[{jetIndex}[0]]".format(**fargs)      ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Leading Jet Neutral Hadron Energy Fraction"   ,"x": "Leading Jet Neutral Hadron Energy Fraction"    ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrphEF":       {'var':"Jet_phEF[{jetIndex}[0]]".format(**fargs)       ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Leading Jet Photon Energy Fraction"           ,"x": "Leading Jet Photon Energy Fraction"            ,"y":"Events  "  ,'log':[0,1,0] }},
                "isreEF":        {'var':"Jet_eEF[{jetIndex}[0]]".format(**fargs)        ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Leading Jet Electorn Energy Fraction"         ,"x": "Leading Jet Electorn Energy Fraction"          ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrmuEF":       {'var':"Jet_muEF[{jetIndex}[0]]".format(**fargs)       ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Leading Jet Muon Energy Fraction"             ,"x": "Leading Jet Muon Energy Fraction"              ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrHFHEF":      {'var':"Jet_HFHEF[{jetIndex}[0]]".format(**fargs)      ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Leading Jet HF Hadron Energy Fraction"        ,"x": "Leading Jet HF Hadron Energy Fraction"         ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrHFEMEF":     {'var':"Jet_HFEMEF[{jetIndex}[0]]".format(**fargs)     ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Leading Jet HF EM Energy Fraction"            ,"x": "Leading Jet HF EM Energy Fraction"             ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrchHMult":    {'var':"Jet_chHMult[{jetIndex}[0]]".format(**fargs)    ,"bins":[40,0,40]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet Charge Hadron Multip"             ,"x": "Leading Jet Charge Hadron Multip"              ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrneHMult":    {'var':"Jet_neHMult[{jetIndex}[0]]".format(**fargs)    ,"bins":[40,0,40]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet Neutral Hadron Multip"            ,"x": "Leading Jet Neutral Hadron Multip"             ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrphMult":     {'var':"Jet_phMult[{jetIndex}[0]]".format(**fargs)     ,"bins":[40,0,40]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet Photon Multip"                    ,"x": "Leading Jet Photon Multip"                     ,"y":"Events  "  ,'log':[0,1,0] }},
                "isreMult":      {'var':"Jet_eMult[{jetIndex}[0]]".format(**fargs)      ,"bins":[6,0,6]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet Electron Multip"                  ,"x": "Leading Jet Electron Multip"                   ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrmuMult":     {'var':"Jet_muMult[{jetIndex}[0]]".format(**fargs)     ,"bins":[6,0,6]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet Electron Multip"                  ,"x": "Leading Jet Electron Multip"                   ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrHFHMult":    {'var':"Jet_HFHMult[{jetIndex}[0]]".format(**fargs)    ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet HF Hadron Multip"                 ,"x": "Leading Jet HF Hadron Multip"                  ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrHFEMMult":   {'var':"Jet_HFEMMult[{jetIndex}[0]]".format(**fargs)   ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet HF EM Multip"                     ,"x": "Leading Jet HF EM Multip"                      ,"y":"Events  "  ,'log':[0,1,0] }},



                



                #
                # Jet Quality Plots
                #


                #"jetcharge":     {'var':"Jet_charge[]"     ,"bins":[20,-2,2]          ,"nMinus1":None         ,"decor":{"title":"Jet Charge"                           ,"x": "Jet Charge"                            ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetchHEF":      {'var':"Jet_chHEF[]"      ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Jet Charge Hadron Fraction"           ,"x": "Jet Charge Hadron Fraction"            ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetneHEF":      {'var':"Jet_neHEF[]"      ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Jet Neutral Hadron Energy Fraction"   ,"x": "Jet Neutral Hadron Energy Fraction"    ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetphEF":       {'var':"Jet_phEF[]"       ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Jet Photon Energy Fraction"           ,"x": "Jet Photon Energy Fraction"            ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jeteEF":        {'var':"Jet_eEF[]"        ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Jet Electorn Energy Fraction"         ,"x": "Jet Electorn Energy Fraction"          ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetmuEF":       {'var':"Jet_muEF[]"       ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Jet Muon Energy Fraction"             ,"x": "Jet Muon Energy Fraction"              ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetHFHEF":      {'var':"Jet_HFHEF[]"      ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Jet HF Hadron Energy Fraction"        ,"x": "Jet HF Hadron Energy Fraction"         ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetHFEMEF":     {'var':"Jet_HFEMEF[]"     ,"bins":[50,0,1]          ,"nMinus1":None          ,"decor":{"title":"Jet HF EM Energy Fraction"            ,"x": "Jet HF EM Energy Fraction"             ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetchHMult":    {'var':"Jet_chHMult[]"    ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Jet Charge Hadron Multip"             ,"x": "Jet Charge Hadron Multip"              ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetneHMult":    {'var':"Jet_neHMult[]"    ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Jet Neutral Hadron Multip"            ,"x": "Jet Neutral Hadron Multip"             ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetphMult":     {'var':"Jet_phMult[]"     ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Jet Photon Multip"                    ,"x": "Jet Photon Multip"                     ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jeteMult":      {'var':"Jet_eMult[]"      ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Jet Electron Multip"                  ,"x": "Jet Electron Multip"                   ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetmuMult":     {'var':"Jet_muMult[]"     ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Jet Electron Multip"                  ,"x": "Jet Electron Multip"                   ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetHFHMult":    {'var':"Jet_HFHMult[]"    ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Jet HF Hadron Multip"                 ,"x": "Jet HF Hadron Multip"                  ,"y":"Events  "  ,'log':[0,1,0] }},
                #"jetHFEMMult":   {'var':"Jet_HFEMMult[]"   ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Jet HF EM Multip"                     ,"x": "Jet HF EM Multip"                      ,"y":"Events  "  ,'log':[0,1,0] }},


                #
                #   Lepton Quality Plots
                #

                "LepDxy":          {'var':"{lepCol}_dxy[{lepIndex}[0]]".format(**fargs)                 ,"bins":[40,-0.05,0.05]          ,"nMinus1":None          ,"decor":{"title":"{lep}_dxy".format(**fargs)           ,"x": "{lep}_dxy".format(**fargs)             ,"y":"Events"  ,'log':[0,1,0] }},
                "LepDz":           {'var':"{lepCol}_dz[{lepIndex}[0]]".format(**fargs)                  ,"bins":[40,-0.1,0.1]          ,"nMinus1":None          ,"decor":{"title":"{lep}_dz".format(**fargs)            ,"x": "{lep}_dz".format(**fargs)              ,"y":"Events"  ,'log':[0,1,0] }},
                "LepLooseMuonId":  {'var':"{lepCol}_looseMuonId[{lepIndex}[0]]".format(**fargs)         ,"bins":[3,0,3]          ,"nMinus1":None                ,"decor":{"title":"{lep}_LooseMuonId".format(**fargs)   ,"x": "{lep}_LooseMuonId".format(**fargs)     ,"y":"Events"  ,'log':[0,1,0] }},
                "LepSpring15":     {'var':"{lepCol}_SPRING15_25ns_v1[{lepIndex}[0]]".format(**fargs)    ,"bins":[7,0,7]          ,"nMinus1":None                ,"decor":{"title":"{lep}_Spring15".format(**fargs)      ,"x": "{lep}_Spring15".format(**fargs)        ,"y":"Events"  ,'log':[0,1,0] }},
                "LepPdgId":        {'var':"{lepCol}_pdgId[{lepIndex}[0]]".format(**fargs)               ,"bins":[40,-20,20]          ,"nMinus1":None            ,"decor":{"title":"{lep}_pdgId".format(**fargs)         ,"x": "{lep}_pdgId".format(**fargs)           ,"y":"Events"  ,'log':[0,1,0] }},
                "LepRelIso":       {'var':"{lepCol}_relIso03[{lepIndex}[0]]".format(**fargs)            ,"bins":[40,0,1]          ,"nMinus1":None               ,"decor":{"title":"{lep}_relIso".format(**fargs)        ,"x": "{lep}_relIso".format(**fargs)          ,"y":"Events"  ,'log':[0,1,0] }},
                "LepabsIso":          {'var':"{lepCol}_absIso03[{lepIndex}[0]]".format(**fargs)            ,"bins":[40,0,10]          ,"nMinus1":None           ,"decor":{"title":"{lep}_absIso".format(**fargs)        ,"x": "{lep}_absIso".format(**fargs)          ,"y":"Events"  ,'log':[0,1,0] }},



                "nVert":       {'var':"nVert"       ,"bins":[60,0,60]            ,"nMinus1":None         ,"decor":{"title":"nVert"                         ,"x":"nVert"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nTrueInt":    {'var':"nTrueInt"    ,"bins":[50,0,50]            ,"nMinus1":None         ,"decor":{"title":"nTrueInt"                         ,"x":"nTrueInt"      ,"y":"Events  "  ,'log':[0,1,0] }},



                "isrPt_fine":   {'var':"Jet_pt[{jetIndex}[0]]".format(**fargs)    ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}} "    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets30":      {'var':"n{jet}".format(**fargs)                      ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"Number of Jets with P_{T} > 30GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets60":      {'var':"nJet_vetoJet_{jetThresh}".format(**fargs)                      ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 60GeV"    ,"x":"Number of Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets30_2":    {'var':"n{jet}".format(**fargs)                     ,"bins":[4,0,4]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"Number of Jets with P_{T} > 30GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets60_2":    {'var':"nJet_vetoJet_{jetThresh}".format(**fargs)                    ,"bins":[4,0,4]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 60GeV"    ,"x":"Number of Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nSoftBJets":   {'var':"(nJet_bJetSoft_{jetThresh})".format(**fargs)                   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets with P_{{T}} < 60GeV"    ,"x":"Number of Soft B-Tagged Jets with P_{T} < 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nHardBJets":   {'var':"(nJet_bJetHard_{jetThresh})".format(**fargs)                   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets with P_{{T}} > 60GeV"    ,"x":"Number of Hard B-Tagged Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nBJets":       {'var':"(nJet_bJetHard_{jetThresh} + nJet_bJetSoft_{jetThresh})".format(**fargs)       ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets"                         ,"x":"Number of B-Tagged Jets"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nBJets2":      {'var':"(nJet_bJet_{jetThresh})".format(**fargs)       ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets"                         ,"x":"Number of B-Tagged Jets"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nBJetsWeight": {'var':self.makeNBJetPlotFunc2("nBJet")       ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets"                         ,"x":"Number of B-Tagged Jets"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nSoftBJetsWeight":   {'var':self.makeNBJetPlotFunc2("nBSoftJet")   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets with P_{{T}} < 60GeV"    ,"x":"Number of Soft B-Tagged Jets with P_{T} < 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nHardBJetsWeight":   {'var':self.makeNBJetPlotFunc2("nBHardJet")   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets with P_{{T}} > 60GeV"    ,"x":"Number of Hard B-Tagged Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "bJetPt":       {'var':"Jet_pt[ max(IndexJet_bJet[0],0)] *(nBJet>0)"      ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"bJet P_{{T}} "    ,"x":"P_{T}(BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "bSoftJetPt":       {'var':"Jet_pt[ max(IndexJet_bSoftJet_{jetThresh}[0] ,0)] *(nJet_bJetSoft_{jetThresh}>0)".format(**fargs)      ,"bins":[10,20,70]          ,"nMinus1":None         ,"decor":{"title":"bSoftJet P_{{T}} "    ,"x":"P_{T}(Soft BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "bHardJetPt":       {'var':"Jet_pt[ max(IndexJet_bHardJet_{jetThresh}[0] ,0)] *(nJet_bJetHard_{jetThresh}>0)".format(**fargs)      ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"bHardJet P_{{T}} "    ,"x":"P_{T}(Hard BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
              }
        
        mva_vars = {
        "mva_methodId"       :{'bins':[20,-0.8,0.8] , 'decor':{} },      
        "mva_response"       :{'bins':[20,-0.8,0.8] , 'decor':{} },       
        "mva_signalTag"      :{'bins':[20,-0.8,0.8] , 'decor':{} },       
        "mva_backgroundTag"  :{'bins':[20,-0.8,0.8] , 'decor':{} },           
        "mva_trainingEvent"  :{'bins':[20,-0.8,0.8] , 'decor':{} },           
        "mva_testEvent"      :{'bins':[20,-0.8,0.8] , 'decor':{} },           
        }
        nMVAMethods = 10
        for mva_var, var_dict in mva_vars.items():
            for imethod in range(nMVAMethods):
                varname = "%s_%s"%(mva_var , imethod) 
                decor = var_dict['decor']
                decor = {'title':varname, 'x':varname, 'y': 'nEvents', 'log':[0,1,0]}
                plotDict[varname]={
                                    'var':"%s[%s]"%(mva_var, imethod),      'bins':var_dict['bins']  , 'decor':decor,

                                    }
        
        
        self.plots = Plots(**plotDict)
        
        
        
        
        self.nminus1s=   {
                            "met":          ["",""]   , 
                            "Lepmt":           ["mt"]   , 
                            "LepmtSR":           ["SR1c"]   , 
                            "ht":           ["ht","CT"]   , 
                            "ct":           ["CT"]   , 
                            "{lep}Phi".format(**fargs) :       [""]   , 
                            "LepEta".format(**fargs) :       ["lepEta" ]   , 
                            "nJets30":      ["",]   , 
                            "nJets60":      ["Jet60"]   , 
                            "nJets30":      ["",]   , 
                            "nJets60_2":      ["Jet60"]   , 
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

