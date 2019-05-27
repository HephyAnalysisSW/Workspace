import re
import ROOT

from Workspace.DegenerateStopAnalysis.tools.degTools import getPlotFromChain, getTH2DwithVarBins, uniqueHash, Dict

class Plot(dict):
  def __init__(self, name, var, bins, decor={},cut='',**kwargs):
    super(Plot, self).__init__( name=name, var=var, bins=bins,decor=decor,cut=cut,**kwargs)
    self.__dict__ = self
    #if not all([x in self.__dict__ for x in ['name','tree']]):
    #  assert False,  "Cannot create sample.... Usage:  Sample(name='name', tree=ROOT.TChain, isData=0, isSignal=0, color=ROOT.kBlue)"
    #for attr in defdict:
    #  if attr not in self.__dict__:
    #    self[attr]=defdict[attr]
    if len(self.bins)==3:
      self.is1d = True
    else: self.is1d=  False
    if len(self.bins)==6 and not getattr(self,"binningIsExplicit",False) :
      self.is2d = True
    else: self.is2d = False
    if "hists" not in self.__dict__:
      self.hists=Dict()
  def decorate(hist,decorDict):
    pass

class Plots(dict):
  def __init__(self,  **kwargs):
    plotDict = {}
    for arg in kwargs:
        if not isinstance(arg,Plot):
            #print arg , "Creating Class Plot"
            if not kwargs[arg].has_key('name'): kwargs[arg]['name']=arg
            if not kwargs[arg].has_key('cut'): kwargs[arg]['cut']=''
            plotDict[arg]=Plot(**kwargs[arg])
            #print arg, type(arg)
            #print plotDict
        else:
            #print arg, "already an instance of class Plot"
            plotDict[arg]=kwargs[arg]
    #super(Plots, self).__init__(**kwargs)
    super(Plots, self).__init__(**plotDict)
    self.__dict__=self


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
    tree.SetLineStyle(3)
    bwname = btag_weight.replace(r"%s","")+"_"+unq
    tree.Draw("(0)>>%s%s"%(bwname, str(binning)), btag_weight%"0", "same")
    tree.Draw("(1)>>+%s"%(bwname), btag_weight%"1", "same")
    tree.Draw("(2)>>+%s"%(bwname), btag_weight%"2", "same")
    tree.Draw("(3)>>+%s"%(bwname), btag_weight%"2p" + "-" + btag_weight%"2", "same" )
    h1 = getattr(ROOT,btname)
    h2 = getattr(ROOT,bwname)
    return h1,h2



def getBMultipPlot( tree, btag_weight ="weightBTag%s_SF_def"):
    unq = degTools.uniqueHash()
    bwname = btag_weight.replace(r"%s","")+"_"+unq
    binning = (4,0,4)
    tree.Draw("(0)>>%s%s"%(bwname, str(binning)), btag_weight%"0", "same")
    tree.Draw("(1)>>+%s"%(bwname), btag_weight%"1", "same")
    tree.Draw("(2)>>+%s"%(bwname), btag_weight%"2", "same")
    tree.Draw("(3)>>+%s"%(bwname), btag_weight%"2p" + "-" + btag_weight%"2", "same" )
    h = getattr(ROOT,bwname)
    h.SetLineStyle(3)
    return h

def getWeightsEtaPt( tree, var = "Jet_eta:Jet_pt" , cutString = "(1)", btag_weight ="weightBTag%s_SF_def"):
    xbins    = [10,20,30,50,70,100,140,200,300,600,800]
    ybins    = [-2.6,-2.4,0,2.4,2.6 ]
    with_wgt = degTools.getTH2DwithVarBins( tree, var, cutString=cutString, weight = btag_weight , xbins=xbins , ybins=ybins )
    no_wgt   = degTools.getTH2DwithVarBins( tree, var, cutString=cutString, weight = "(1)"       , xbins=xbins , ybins=ybins )
    ratio    = with_wgt.Clone()
    ratio.Divide(no_wgt)
    return ratio, with_wgt, no_wgt


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
        def nBJetPlot( sample, bins, cutString, weight, addOverFlowBin = '', binningIsExplicit = False, bjet_var=bjet_var, variableBinning = False, uniqueName = False):
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


    @staticmethod
    def makeNBJetPlotFunc3(bjet_var, cuts ):
        def nBJetPlot( sample, bins, cutString, weight, addOverFlowBin = '', binningIsExplicit = False, bjet_var=bjet_var, variableBinning = False, uniqueName = False):
            #from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import BTagSFMap
            #btag_sf_map = BTagSFMap('sf')
            jet_thresh   = 'def'
            bjet_var_map = {
                            variables.nBJetSoft.string : [ getattr( weights , "BSoft%s"%x ).string for x in [0,1,2,"2p"]  ] ,  
                            variables.nBJetHard.string : [ getattr( weights , "BHard%s"%x ).string for x in [0,1,2,"2p"]  ] ,
                            variables.nBJet.string     : [ getattr( weights , "B%s"%x ).string     for x in [0,1,2,"2p"]  ] , 
                           }

             
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
    
    def deltaRFunc(self, sample, bins, cutString, weight, addOverFlowBin = '', binningIsExplicit = False , variableBinning = False, uniqueName = False):

        import Workspace.DegenerateStopAnalysis.cmgPostProcessing.cmgObjectSelection as cmgObjectSelection
        from Workspace.DegenerateStopAnalysis.cmgPostProcessing.cmgObjectSelection import cmgObject
        import operator
        from Workspace.HEPHYPythonTools.helpers import deltaR
        import time

        tree = sample.tree

        weights = [w for w in re.split('\(|\)| |\*|', weight) if w]
        weight_branches = [ x for x in weights if x.isalpha() ]
        numerical_weights_ = [x for x in weights if not x in weight_branches ] 
        numerical_weights = [ eval(x) for x in numerical_weights_]

        maxDr = 2
        histo = ROOT.TH1F(sample.name, sample.name, 50,0,maxDr)
        #histo = ROOT.TH1F(sample.name, sample.name, 40,0,100)
        
        #nEventsTotal = sample.tree.GetEntries()
        lgCol = "LepGood"
        loCol = "LepOther"

        tree.Draw(">>eList",cutString)
        eList = ROOT.eList
        nEvents = eList.GetN()
        lep_vars = ['pt', 'pdgId', 'phi','eta']
        
        perc_mark = 0
        start_time = time.time()
        for elEvt in xrange(nEvents):
            ievt = eList.GetEntry(elEvt)
            tree.GetEntry(ievt)
            lgObj = cmgObject( sample.tree, sample.tree, lgCol, lep_vars )
            if not lgObj.nObj:
                continue
            loObj = cmgObject( sample.tree, sample.tree, loCol, lep_vars )


            mus = []
            lepObjs = [lgObj, loObj]
            for lepObj in lepObjs:
                mu_idx = lepObj.getSelectionIndexList(tree, lambda x, lObj, i: abs(lObj.pdgId[i])==13 )
                mus.extend( lepObj.getObjDictList(lep_vars, mu_idx ))

            sorted_mus = sorted(  mus, key = lambda x: x['pt'], reverse = True)
            if len( sorted_mus ) < 2:
                continue

            minDr = 999
            for imu, mu1 in enumerate(mus):
                for jmu, mu2 in enumerate(mus[imu+1:]):
                    dR = deltaR(mu1, mu2) 
                    if dR < minDr:
                        minDr = dR
            if minDr > maxDr :
                continue
            

            
            #fill = sorted_mus[0]['pt']
            fill = minDr 

            weight_values = []
            for wb in weight_branches:
                weight_values.append( tree.GetLeaf(wb).GetValue(0))
            total_weight = reduce( operator.mul, weight_values + numerical_weights )
            histo.Fill(fill,total_weight)

            perc= (elEvt/float(nEvents)*100)
            if perc > perc_mark:
                print "%s%%"%int(perc)
                perc_mark += 10

        end_time = time.time()
        total_time = end_time - start_time
        print "Took %0.2f seconds"%total_time
        return histo


    #def makeDeltaRFunc(self, minMuPt,maxMuPt , selectGoodMu= True, allMuons=False, selectIsolatedMuon=False ):
    def makeDeltaRFunc(self, minMuPt, maxMuPt , option="selectGoodMuon" ):
        def deltaRFunc(sample, bins, cutString, weight, addOverFlowBin = '', binningIsExplicit = False , variableBinning = False, uniqueName = False):
            import  Workspace.DegenerateStopAnalysis.cmgPostProcessing.cmgObjectSelection as cmgObjectSelection
            from    Workspace.DegenerateStopAnalysis.cmgPostProcessing.cmgObjectSelection import cmgObject
            import  operator
            from    Workspace.HEPHYPythonTools.helpers import deltaR
            import  time


            options_list =  ["selectGoodMuon", "allMuons", "selectIsolatedMuon" ]
            if option not in options_list:
                raise Exception("Option (%s) not recognized as one of %s"%(option, options_list))
            

            options = { opt: opt.lower() == option.lower() for opt in options_list } 


            tree            = sample.tree
            weights         = [w for w in re.split('\(|\)| |\*|', weight) if w]
            weight_branches = [ x for x in weights if x.isalpha() ]
            numerical_weights_ = [x for x in weights if not x in weight_branches ] 
            numerical_weights  = [ eval(x) for x in numerical_weights_]
            maxDr = 2
            histo = ROOT.TH1F(sample.name, sample.name, 50,0,maxDr)
            #histo = ROOT.TH1F(sample.name, sample.name, 40,0,100)
            #nEventsTotal = sample.tree.GetEntries()
            lgCol = "LepGood"
            loCol = "LepOther"
            tree.Draw(">>eList",cutString)
            eList = ROOT.eList
            nEvents = eList.GetN()
            lep_vars = ['pt', 'pdgId', 'phi','eta']
            perc_mark  = 0
            start_time = time.time()
            for elEvt in xrange(nEvents):
                ievt = eList.GetEntry(elEvt)
                tree.GetEntry(ievt)
                lgObj = cmgObject( sample.tree, sample.tree, lgCol, lep_vars )
                if not lgObj.nObj:
                    continue
                loObj   = cmgObject( sample.tree, sample.tree, loCol, lep_vars )
                mus     = []
                lepObjs = [lgObj, loObj]

                lepObj = lgObj 
                mu_idx = lepObj.getSelectionIndexList(tree, lambda x, lObj, i: abs(lObj.pdgId[i])==13 )
                good_mus  = lepObj.getObjDictList(lep_vars, mu_idx )
                tight_mus_idx =  [ tree.IndexLepGood_mu_def[x] for x in range(tree.nLepGood_mu_def)  ] 
                tight_mus  = lepObj.getObjDictList(lep_vars, tight_mus_idx )
                mus.extend(good_mus)

                lepObj = loObj 
                mu_idx = lepObj.getSelectionIndexList(tree, lambda x, lObj, i: abs(lObj.pdgId[i])==13 )
                other_mus = lepObj.getObjDictList(lep_vars, mu_idx )
                mus.extend( other_mus ) 

                if not good_mus:
                    continue
                good_mu_pt    = good_mus[0]['pt']
                if good_mu_pt > maxMuPt:
                    continue
                if good_mu_pt < minMuPt:
                    continue 

                sorted_mus = sorted(  mus, key = lambda x: x['pt'], reverse = True)
                if len( sorted_mus ) < 2:
                    continue
                minDr = 999

                if options.get("selectGoodMuon"):
                    mu_good = good_mus[0]
                    other_mus = good_mus[1:] + other_mus 
                    for jmu, mu2 in enumerate(other_mus):
                        dR = deltaR(mu_good, mu2)
                        if dR < minDr:
                            minDr = dR
                    if minDr > maxDr:
                        continue    
                elif options.get("selectIsolatedMuon"):
                    mu_good   = tight_mus[0]
                    if not mu_good in good_mus:
                        assert False
                    other_mus = [mu for mu in good_mus + other_mus if not mu == mu_good]
                    assert len(other_mus) == len(mus)+1 , (other_mus, mus, good_mus)
                    for jmu, mu2 in enumerate(other_mus):
                        dR = deltaR(mu_good, mu2)
                        if dR < minDr:
                            minDr = dR
                    if minDr > maxDr:
                        continue    
                elif options.get("allMuons"): ## get min deltaR between all muons
                    for imu, mu1 in enumerate(mus):
                        for jmu, mu2 in enumerate(mus[imu+1:]):
                            dR = deltaR(mu1, mu2) 
                            if dR < minDr:
                                minDr = dR
                    if minDr > maxDr :
                        continue
                fill = minDr 
                weight_values = []
                for wb in weight_branches:
                    weight_values.append( tree.GetLeaf(wb).GetValue(0))
                total_weight = reduce( operator.mul, weight_values + numerical_weights )
                histo.Fill(fill,total_weight)
                perc= (elEvt/float(nEvents)*100)
                if perc > perc_mark:
                    print "%s%%"%int(perc)
                    perc_mark += 10
            end_time = time.time()
            total_time = end_time - start_time
            print "Took %0.2f seconds"%total_time
            return histo

        return deltaRFunc

    def __init__(self, lepCollection = "LepGood", lep = "lep", lepThresh = "", jetThresh = "", variables = None):
        """
        TODO:  Variables input should eventually replace the other arguments, right now only used for nbjet multip plots

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

        plotDict =\
              {
                "Lepmt":           {'var':"{lepCol}_mt[{lepIndex}[0]]".format(**fargs)       ,"bins":[40,0,200]          ,"nMinus1":None         ,"decor":{"title":"{lep}MT".format(**fargs)    ,"x":"M_{{T}}({lepLatex}, E^{{miss}}_{{T}}) [GeV] ".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
                "LepQ80":          {'var':"{lepCol}_Q80[{lepIndex}[0]]".format(**fargs)       ,"bins":[40,-2.5,1.5]          ,"nMinus1":None         ,"decor":{"title":"{lep}Q80".format(**fargs)    ,"x":"Q80({lepLatex}, E^{{miss}}_{{T}}) [GeV] ".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
                "Lepmt_2":         {'var':"{lepCol}_mt[{lepIndex}[0]]".format(**fargs)       ,"bins":[20,0,200]          ,"nMinus1":None         ,"decor":{"title":"{lep}MT".format(**fargs)    ,"x":"M_{{T}}({lepLatex}, E^{{miss}}_{{T}}) [GeV]".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
                "LepmtSR1s":       {'var':"{lepCol}_mt[{lepIndex}[0]]".format(**fargs)       ,"bins":[0,60,95,200]     ,"binningIsExplicit":True    ,"nMinus1":None         ,"decor":{"title":"{lep}MT".format(**fargs)    ,"x":"M_{{T}}({lepLatex}, E^{{miss}}_{{T}}) [GeV]".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
                "LepmtSR1s_2":       {'var':"{lepCol}_mt[{lepIndex}[0]]".format(**fargs)       ,"bins":[0,60,95,200,1000]     ,"binningIsExplicit":True    ,"nMinus1":None         ,"decor":{"title":"{lep}MT".format(**fargs)    ,"x":"M_{{T}}({lepLatex}, E^{{miss}}_{{T}}) [GeV]".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
                "LepmtBins":       {'var':"{lepCol}_mt[{lepIndex}[0]]".format(**fargs)       ,"bins":[0,60,95,200,210]     ,"binningIsExplicit":True    ,"nMinus1":None         ,"decor":{"title":"{lep}MT".format(**fargs)    ,"x":"M_{{T}}({lepLatex}, E^{{miss}}_{{T}}) [GeV]".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
                #"mtSR":        {'var':"mt"                           ,"bins":[30,0,150]          ,"nMinus1":None         ,"decor":{"title":"MT"    ,"x":"M_{T}"      ,"y":"Events / 5 GeV "  ,'log':[0,1,0] }},
                "LepPt3" :        {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)      ,"bins":[30,0,200]          ,"nMinus1":""      ,"decor":{"title":"{lep}Pt".format(**fargs)           ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "LepPt2" :        {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)      ,"bins":[40,3.5,200]          ,"nMinus1":""      ,"decor":{"title":"{lep}Pt".format(**fargs)           ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "LepPtSR" :      {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)       ,"bins":[20,3.5,50]          ,"nMinus1":""      ,"decor":{"title":"{lep}Pt".format(**fargs)           ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "LepPt" :        {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)       ,"bins":[20,0,200]          ,"nMinus1":""      ,"decor":{"title":"{lep}Pt".format(**fargs)           ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "LepPtNMinus1" : {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)       ,"bins":[40,0,500]          ,"nMinus1":"LepPt"      ,"decor":{"title":"{lep}Pt".format(**fargs)           ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                #"LepPtSR" :      {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)       ,"bins":[35,0,35]           ,"nMinus1":""           ,"decor":{"title":"{lep}Pt".format(**fargs)     ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] , 'fom_reverse':False } },
                "LepPtSR_2" :    {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)      ,"bins":[53,3.5,30]           ,"nMinus1":""           ,"decor":{"title":"{lep}Pt".format(**fargs)     ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "LepPtSR_3" :    {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)      ,"bins":[54,3.0,30]           ,"nMinus1":""           ,"decor":{"title":"{lep}Pt".format(**fargs)     ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                #"LepPtSRBins" :      {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)   ,"bins":[0,3.5,5, 12, 20, 30,100,400]     ,'binningIsExplicit':True       ,"nMinus1":""           ,"decor":{"title":"{lep}Pt".format(**fargs)     ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "LepPtShape" :   {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)   ,"bins":[0,3.5, 5, 12, 20, 30, 50, 80, 200]     ,'binningIsExplicit':True       ,"nMinus1":""           ,"decor":{"title":"{lep}Pt".format(**fargs)     ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "LepPtShape2" :   {'var':"{lepCol}_pt[{lepIndex}[0]]".format(**fargs)   ,"bins":[0,3.5, 5, 12, 20, 30, 50, 80, 200, 210]     ,'binningIsExplicit':True       ,"nMinus1":""           ,"decor":{"title":"{lep}Pt".format(**fargs)     ,"x":"P_{{T}}({lepLatex}) [GeV]".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "LepEta" :       {'var':"{lepCol}_eta[{lepIndex}[0]]".format(**fargs)                         ,"bins":[20,-3,3]           ,"nMinus1":""         ,"decor":{"title":"{lep}Eta".format(**fargs)     ,"x":"#eta({lepLatex})".format(**fargs)       ,"y":"Events  "  ,'log':[0,1,0] }},
                "LepPhi" :      {'var':"{lepCol}_phi[{lepIndex}[0]]".format(**fargs)                         ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"{lep}Phi".format(**fargs)     ,"x":"{lep} Phi".format(**fargs)       ,"y":"Events  "  ,'log':[0,1,0] }},
                "met":          {'var':"met"                            ,"bins":[40,200,1000]        ,"nMinus1":"met"        ,"decor":{"title":"MET"    ,"x":"E^{miss}_{T} [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "ht":           {'var':"ht_{jet}".format(**fargs)       ,"bins":[40,200,1000]        ,"nMinus1":""           ,"decor":{"title":"HT"    ,"x":"H_{T} [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "ht2":           {'var':"ht_{jet}".format(**fargs)  ,"bins":[50,300,2000]        ,"nMinus1":""           ,"decor":{"title":"HT"    ,"x":"H_{T} [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "ct1":           {'var':"min(met_pt,ht_{jet}-100)".format(**fargs)         ,"bins":[40,200,1000]        ,"nMinus1":""           ,"decor":{"title":"CT1"    ,"x":"C_{T1} [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "ct2":           {'var':"min(met_pt, Jet_pt[{jetIndex}[0]] - 25)".format(**fargs)         ,"bins":[40,200,1000]        ,"nMinus1":""           ,"decor":{"title":"CT2"    ,"x":"C_{T2} [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "MetPhi":      {'var':"met_phi"                        ,"bins":[20,-3.15,3.15]           ,"nMinus1":None         ,"decor":{"title":"MetPhi"    ,"x":"Met Phi"      ,"y":"Events"  ,'log':[0,1,0] }},
                #"dPhiJet12":   {'var':"deltaPhi_j12"                  ,"bins":[20,0,3.2]          ,"nMinus1":None         ,"decor":{"title":"dPhi_J12"    ,"x":"dPhi_J12"      ,"y":"Events "  ,'log':[0,1,0] }},
                #"dPhiJetMet":  {'var':dPhiJetMet                      ,"bins":[20,0,3.2]          ,"nMinus1":None         ,"decor":{"title":"dPhi_JetMet"    ,"x":"dPhi_JetMet"      ,"y":"Events "  ,'log':[0,1,0], 'fom_reverse':True }},
                #"MetOverHT":   {'var':"met_pt/htJet30j"               ,"bins":[20,0,4]            ,"nMinus1":None         ,"decor":{"title":"MetOverHT"    ,"x":"Met/HT"      ,"y":"Events "  ,'log':[0,1,0], 'fom_reverse':False }},

                "jetCSV":      {'var':"Jet_btagCSV".format(**fargs)     ,"bins":[45,0,1.1]          ,"nMinus1":None         ,"decor":{"title":"btag CSVs"    ,"x":"btag CSV"      ,"y":"Events  "  ,'log':[0,1,0] }},

                "isrPt" :      {'var':"Jet_pt[{jetIndex}[0]]".format(**fargs)     ,"bins":[45,100,1000]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}} [GeV]"    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},

                "wpt":          {'var':"{lepCol}_Wpt[{lepIndex}[0]]".format(**fargs)                        ,"bins":[40,200,1000]        ,"nMinus1":""        ,"decor":{"title":"WPT"    ,"x":"P_{T}(W) [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "wpt2":         {'var':"{lepCol}_Wpt[{lepIndex}[0]]".format(**fargs)                        ,"bins":[20,0,1000]        ,"nMinus1":""        ,"decor":{"title":"WPT"    ,"x":"P_{T}(W) [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "wpt3":         {'var':"{lepCol}_Wpt[{lepIndex}[0]]".format(**fargs)                        ,"bins":[0,200,250,350,450,650,800,1400]   , 'binningIsExplicit':True    ,"nMinus1":""        ,"decor":{"title":"WPT"    ,"x":"P_{T}(W) [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},
                "wpt4":         {'var':"{lepCol}_Wpt[{lepIndex}[0]]".format(**fargs)                        ,"bins":[0,50,100,150,200,300,400,600,800,1000]   , 'binningIsExplicit':True    ,"nMinus1":""        ,"decor":{"title":"WPT"    ,"x":"P_{T}(W) [GeV]"      ,"y":"Events"  ,'log':[0,1,0] }},

                "isrPt2":       {'var':"Jet_pt[{jetIndex}[0]]".format(**fargs)     ,"bins":[20,100,900]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}} [GeV]"    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "isrEta":       {'var':"Jet_eta[{jetIndex}[0]]".format(**fargs)   ,"bins":[20,-3,3]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet Eta "    ,"x":"#eta(LeadingJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},


                "dR2LepISR" :        {'var':"deltaR( LepGood_eta[{lepIndex}[0]] , Jet_eta[{jetIndex}[0]],  LepGood_phi[{lepIndex}[0]] , Jet_phi[{jetIndex}[0]] )".format(**fargs)       ,"bins":[50,0,20]          ,"nMinus1":""      ,"decor":{"title":"dR2LepISR".format(**fargs)           ,"x":"dR2(Lep, ISR)".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "dR2Leps" :          {'var':"deltaR( LepGood_eta[{lepIndex}[0]] , LepGood_eta[{lepIndex}[1]],  LepGood_phi[{lepIndex}[0]] , LepGood_phi[{lepIndex}[1]] )".format(**fargs)       ,"bins":[50,0,20]          ,"nMinus1":""      ,"decor":{"title":"dR2Leps".format(**fargs)           ,"x":"dR2(Lep 1, Lep 2)".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "dPhiLepISR" :      {'var':"acos(cos(  LepGood_phi[{lepIndex}[0]] - Jet_phi[{jetIndex}[0]] ))".format(**fargs)       ,"bins":[50,0,3.5]          ,"nMinus1":""      ,"decor":{"title":"dPhiLepISR".format(**fargs)           ,"x":"dPhi(Lep, ISR)".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
                "dPhiLepMET" :      {'var':"acos(cos(  LepGood_phi[{lepIndex}[0]] - met_phi  ))".format(**fargs)       ,"bins":[50,0,3.5]          ,"nMinus1":""      ,"decor":{"title":"dPhiLepMET".format(**fargs)           ,"x":"dPhi(Lep, MET)".format(**fargs)       ,"y":"Events"  ,'log':[0,1,0] }},
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
                "nLep":            {'var':"n{lepCol}_{lep}".format(**fargs)       ,"bins":[4,0,4]               ,"nMinus1":None         ,"decor":{"title":"n{lepCol}_{lep}".format(**fargs)    ,"x":"n{lepCol}_{lep}".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
                "LepLooseMuonId":  {'var':"{lepCol}_looseMuonId[{lepIndex}[0]]".format(**fargs)         ,"bins":[3,0,3]          ,"nMinus1":None                ,"decor":{"title":"{lep}_LooseMuonId".format(**fargs)   ,"x": "{lep}_LooseMuonId".format(**fargs)     ,"y":"Events"  ,'log':[0,1,0] }},


                "LepDxy":          {'var':"{lepCol}_dxy[{lepIndex}[0]]".format(**fargs)                 ,"bins":[40,-0.05,0.05]          ,"nMinus1":None          ,"decor":{"title":"{lep}_dxy".format(**fargs)           ,"x": "{lep}_dxy".format(**fargs)             ,"y":"Events"  ,'log':[0,1,0] }},
                "LepDz":           {'var':"{lepCol}_dz[{lepIndex}[0]]".format(**fargs)                  ,"bins":[40,-0.1,0.1]          ,"nMinus1":None          ,"decor":{"title":"{lep}_dz".format(**fargs)            ,"x": "{lep}_dz".format(**fargs)              ,"y":"Events"  ,'log':[0,1,0] }},
                "LeplooseMuonId":  {'var':"{lepCol}_looseMuonId[{lepIndex}[0]]".format(**fargs)         ,"bins":[3,0,3]          ,"nMinus1":None                ,"decor":{"title":"{lep}_LooseMuonId".format(**fargs)   ,"x": "{lep}_LooseMuonId".format(**fargs)     ,"y":"Events"  ,'log':[0,1,0] }},
                "LepsoftMuonId":  {'var':"{lepCol}_softMuonId[{lepIndex}[0]]".format(**fargs)         ,"bins":[3,0,3]          ,"nMinus1":None                ,"decor":{"title":"{lep}_softMuonId".format(**fargs)   ,"x": "{lep}_softMuonId".format(**fargs)     ,"y":"Events"  ,'log':[0,1,0] }},
                "LepmediumMuonId":  {'var':"{lepCol}_mediumMuonId[{lepIndex}[0]]".format(**fargs)         ,"bins":[3,0,3]          ,"nMinus1":None                ,"decor":{"title":"{lep}_mediumMuonId".format(**fargs)   ,"x": "{lep}_mediumMuonId".format(**fargs)     ,"y":"Events"  ,'log':[0,1,0] }},
                "LepSpring15":     {'var':"{lepCol}_SPRING15_25ns_v1[{lepIndex}[0]]".format(**fargs)    ,"bins":[7,0,7]          ,"nMinus1":None                ,"decor":{"title":"{lep}_Spring15".format(**fargs)      ,"x": "{lep}_Spring15".format(**fargs)        ,"y":"Events"  ,'log':[0,1,0] }},
                "LepPdgId":        {'var':"{lepCol}_pdgId[{lepIndex}[0]]".format(**fargs)               ,"bins":[40,-20,20]          ,"nMinus1":None            ,"decor":{"title":"{lep}_pdgId".format(**fargs)         ,"x": "{lep}_pdgId".format(**fargs)           ,"y":"Events"  ,'log':[0,1,0] }},
                "LepRelIso":       {'var':"{lepCol}_relIso03[{lepIndex}[0]]".format(**fargs)            ,"bins":[40,0,1]          ,"nMinus1":None               ,"decor":{"title":"{lep}_relIso".format(**fargs)        ,"x": "{lep}_relIso".format(**fargs)          ,"y":"Events"  ,'log':[0,1,0] }},
                "LepabsIso":       {'var':"{lepCol}_absIso03[{lepIndex}[0]]".format(**fargs)            ,"bins":[40,0,10]          ,"nMinus1":None           ,"decor":{"title":"{lep}_absIso".format(**fargs)        ,"x": "{lep}_absIso".format(**fargs)          ,"y":"Events"  ,'log':[0,1,0] }},



                "nVert":       {'var':"nVert"       ,"bins":[60,0,60]            ,"nMinus1":None         ,"decor":{"title":"nVert"                         ,"x":"nVert"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nTrueInt":    {'var':"nTrueInt"    ,"bins":[50,0,50]            ,"nMinus1":None         ,"decor":{"title":"nTrueInt"                         ,"x":"nTrueInt"      ,"y":"Events  "  ,'log':[0,1,0] }},



                "isrPt_fine":         {'var':"Jet_pt[{jetIndex}[0]]".format(**fargs)    ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"Leading Jet P_{{T}} "    ,"x":"isrJetPt"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets30":            {'var':"nJet_basJet_{jetThresh}".format(**fargs)                      ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"Number of Jets with P_{T} > 30GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets20":            {'var':"nJet_basJet_lowpt".format(**fargs)                      ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"Number of Jets with P_{T} > 20GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets60":            {'var':"nJet_vetoJet_{jetThresh}".format(**fargs)                      ,"bins":[10,0,10]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 60GeV"    ,"x":"Number of Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets60_2":            {'var':"nJet_vetoJet_{jetThresh}".format(**fargs)                    ,"bins":[4,1,5]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 60GeV"    ,"x":"Number of Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJets30_2":            {'var':"nJet_basJet_{jetThresh}".format(**fargs)                      ,"bins":[4,1,5]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"Number of Jets with P_{T} > 30GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                #"nJets30_2":          {'var':"nJet_".format(**fargs)                     ,"bins":[4,0,4]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 30GeV"    ,"x":"Number of Jets with P_{T} > 30GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                #"nJets60_2":          {'var':"nJet_vetoJet_{jetThresh}".format(**fargs)                    ,"bins":[4,0,4]          ,"nMinus1":None         ,"decor":{"title":"Number of Jets with P_{{T}} > 60GeV"    ,"x":"Number of Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},



                "nJet_bJetSoft":           {'var':"nJet_bJetSoft_{jetThresh}".format(**fargs)                   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets with P_{{T}} < 60GeV"    ,"x":"Number of Soft B-Tagged Jets with P_{T} < 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJet_bJetSoft_20":        {'var':"nJet_bJetSoft_lowpt".format(**fargs)                   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets with P_{{T}} < 60GeV"    ,"x":"Number of Soft B-Tagged Jets with 20GeV < P_{T} < 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJet_bJetSoft_30":        {'var':"nJet_bJetSoft_def".format(**fargs)                   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets with P_{{T}} < 60GeV"    ,"x":"Number of Soft B-Tagged Jets with 30GeV < P_{T} < 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJet_bJetHard":           {'var':"nJet_bJetHard_{jetThresh}".format(**fargs)                   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets with P_{{T}} > 60GeV"    ,"x":"Number of Hard B-Tagged Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJet_bJetTot":           {'var':"nJet_bJetHard_{jetThresh} + nJet_bJetSoft_{jetThresh}".format(**fargs)       ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets"                         ,"x":"Number of B-Tagged Jets"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJet_bJet":               {'var':"nJet_bJet_{jetThresh}".format(**fargs)       ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets"                         ,"x":"Number of B-Tagged Jets"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJet_bJet_weights":       {'var':self.makeNBJetPlotFunc2("nBJet")       ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets"                         ,"x":"Number of B-Tagged Jets"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJet_bJetSoft_weights":   {'var':self.makeNBJetPlotFunc2("nBSoftJet")   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of Soft B-Tagged Jets with P_{{T}} < 60GeV"    ,"x":"Number of Soft B-Tagged Jets with P_{T} < 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "nJet_bJetHard_weights":   {'var':self.makeNBJetPlotFunc2("nBHardJet")   ,"bins":[4,0,4]            ,"nMinus1":None         ,"decor":{"title":"Number of B-Tagged Jets with P_{{T}} > 60GeV"    ,"x":"Number of Hard B-Tagged Jets with P_{T} > 60GeV"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "bJetPt":                  {'var':"Jet_pt[ max(IndexJet_bJet_{jetThresh}[0],0)] *(nJet_bJet_{jetThresh}>0)"      ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"bJet P_{{T}} "    ,"x":"P_{T}(BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "bJetSoftPt":              {'var':"Jet_pt[ max(IndexJet_bJetSoft_{jetThresh}[0] ,0)] *(nJet_bJetSoft_{jetThresh}>0)".format(**fargs)      ,"bins":[10,20,70]          ,"nMinus1":None         ,"decor":{"title":"bSoftJet P_{{T}} "    ,"x":"P_{T}(Soft BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
                "bJetHardPt":              {'var':"Jet_pt[ max(IndexJet_bJetHard_{jetThresh}[0] ,0)] *(nJet_bJetHard_{jetThresh}>0)".format(**fargs)      ,"bins":[100,0,1000]          ,"nMinus1":None         ,"decor":{"title":"bHardJet P_{{T}} "    ,"x":"P_{T}(Hard BJet)"      ,"y":"Events  "  ,'log':[0,1,0] }},
              }


        options_list =  ["selectGoodMuon", "allMuons", "selectIsolatedMuon" ]
        option_tags = {
                        'selectGoodMuon'        : { 'title': 'Min dR of loose iso muon and all muons' },
                        'allMuons'              : { 'title': 'Min dR of all muons' },
                        'selectIsolatedMuon': { 'title': 'Min dR of tight muon and all muons' },
                       }
        for option in ["selectGoodMuon", "allMuons", "selectIsolatedMuon" ]:
            option_title = option_tags[option]['title'] 
            if option == "allMuons":
                ptmin , ptmax = ( 0 , 2000000   )
                plot_name = option +"_"+ 'drMuPairPt'
                plot_title= option_title + "%s < muPt <%s"%(ptmin, ptmax)
                plotDict[plot_name] = {'var':self.makeDeltaRFunc(ptmin, ptmax )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":plot_title   ,"x":plot_title    ,"y":"Events"  ,'log':[0,1,0] }}
            else:
                for ptmax in range(10,200,10):
                    ptmin = ptmax - 10
                    plot_name = option +"_"+ 'drMuPairPt_%sTo%s'%(ptmin,ptmax)
                    plot_title= option_title + "%s < muPt <%s"%(ptmin, ptmax)
                    plotDict[plot_name] = {'var':self.makeDeltaRFunc(ptmin, ptmax )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":plot_title   ,"x":plot_title    ,"y":"Events"  ,'log':[0,1,0] }}

                ptmin ,ptmax = (200,2000000)
                plot_name = option +"_"+ 'drMuPairPt_%sp'%ptmin
                plot_title= option_title + "%s < muPt"%(ptmin)
                plotDict[plot_name] = {'var':self.makeDeltaRFunc(ptmin, ptmax )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":plot_title   ,"x":plot_title    ,"y":"Events"  ,'log':[0,1,0] }}

                ptmin ,ptmax = (0,40)
                plot_name = option +"_"+ 'drMuPairPt_%sTo%s'%(ptmin, ptmax)
                plot_title= option_title + "%s < muPt < %s"%(ptmin, ptmax)
                plotDict[plot_name] = {'var':self.makeDeltaRFunc(ptmin, ptmax )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":plot_title   ,"x":plot_title    ,"y":"Events"  ,'log':[0,1,0] }}


        #plotDict.update({
        #        "dRMuPair3":          {'var':self.deltaRFunc      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPair":           {'var':"deltaR( LepGood_eta[0] , LepGood_eta[1] , LepGood_phi[0] , LepGood_phi[1] )"      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPair2":          {'var':"deltaR( LepGood_eta[0] , LepOther_eta[0], LepGood_phi[0] , LepOther_phi[0] )"       ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},


        #        "dRMuPairPt":            {'var':self.makeDeltaRFunc(0,100000 )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt10":          {'var':self.makeDeltaRFunc(0,10 )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt20":          {'var':self.makeDeltaRFunc(10 ,20 )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt30":          {'var':self.makeDeltaRFunc(20 ,30 )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt40":          {'var':self.makeDeltaRFunc(30 ,40 )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt50":          {'var':self.makeDeltaRFunc(40 ,50 )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt60":          {'var':self.makeDeltaRFunc(50 ,60 )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt70":          {'var':self.makeDeltaRFunc(60 ,70 )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt80":          {'var':self.makeDeltaRFunc(70 ,80 )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt90":          {'var':self.makeDeltaRFunc(80 ,90 )      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt100":          {'var':self.makeDeltaRFunc(90 ,100)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt110":          {'var':self.makeDeltaRFunc(100,110)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt120":          {'var':self.makeDeltaRFunc(110,120)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt130":          {'var':self.makeDeltaRFunc(120,130)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt140":          {'var':self.makeDeltaRFunc(130,140)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt150":          {'var':self.makeDeltaRFunc(140,150)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt160":          {'var':self.makeDeltaRFunc(150,160)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt170":          {'var':self.makeDeltaRFunc(160,170)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt180":          {'var':self.makeDeltaRFunc(170,180)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt190":          {'var':self.makeDeltaRFunc(180,190)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt200":          {'var':self.makeDeltaRFunc(190,200)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},
        #        "dRMuPairPt200p":         {'var':self.makeDeltaRFunc(200,10000000)      ,"bins":[40,0,2]          ,"nMinus1":None         ,"decor":{"title":"dR lead-sublead Mu".format(**fargs)    ,"x":"dR lead-sublead Mu".format(**fargs)      ,"y":"Events"  ,'log':[0,1,0] }},

        #        })

        
        mva_vars = {
        "mva_methodId"       :{'bins':[25,-0.5,0.5] , 'decor':{} },      
        "mva_response"       :{'bins':[25,-0.5,0.5] , 'decor':{} },       
        "mva_signalTag"      :{'bins':[25,-0.5,0.5] , 'decor':{} },       
        "mva_backgroundTag"  :{'bins':[25,-0.5,0.5] , 'decor':{} },           
        "mva_trainingEvent"  :{'bins':[25,-0.5,0.5] , 'decor':{} },           
        "mva_testEvent"      :{'bins':[25,-0.5,0.5] , 'decor':{} },           
        "mva_preselectedEvent"      :{'bins':[25,-0.5,0.5] , 'decor':{} },           
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
                            "mva_response_0":          ["mva_response"]   , 
                          #  "met":          ["met",""]   , 
                          #  "Lepmt":           ["mt"]   , 
                          #  "LepmtSR":           ["SR1c"]   , 
                          #  "ht":           ["ht","CT"]   , 
                          #  "ct":           ["CT"]   , 
                          #  "{lep}Phi".format(**fargs) :       [""]   , 
                          #  "LepEta".format(**fargs) :       ["lepEta" ]   , 
                          #  "nJets30":      ["",]   , 
                          #  "nJets60":      ["Jet60"]   , 
                          #  "nJets30":      ["",]   , 
                          #  "nJets60_2":      ["Jet60"]   , 
                          #  #"nBJets":       ["BVeto"]   , 
                          #  "nBJets":       ["BJet"]   , 
                          #  "nSoftBJets":   ["Soft"]   , 
                          #  "nHardBJets" :  ["Hard"]   , 
                          #  "bSoftJetPt" :  ["Soft"]   , 
                          #  "bHardJetPt" :  ["Hard", "Soft"]   , 
                          #  "bJetPt" :      ["Hard","Soft"]   , 
                          #  #"isrPt" :       ["ISR", "HT", "MET", "CT"]   , 
                          #  "isrPt_fine" :       ["ISR", "HT", "MET", "CT", "Jet60"]   , 
                          #  #"nHardBJets" :  ["Hard"]   , 
                          #  #"{lep}Pt":        ["lepPt","MuPt"]
                          #  #"{lep}Pt":        [""],
                    }




if __name__ == "__main__":
    lepPlots = DegPlots("LepGood","lep")
    muPlots  = DegPlots("LepGood","mu")
    elPlots  = DegPlots("LepGood","el")
