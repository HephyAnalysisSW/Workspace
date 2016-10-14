"""
run after running something like:

ipython -i   degStop.py -- --cfg=ApprovalSys --task=bkg_est  --lepCol=LepGood --lep=lep --cutInst bins_sum   --weight=nopu_noisr --btag=btag --ppSet=74x

with desired lepCol and lep opts
"""

import pickle
import Workspace.HEPHYPythonTools.xsecSMS as xsecSMS
stop_xsecs = xsecSMS.stop13TeV_NLONLL

ROOT.gStyle.SetPaintTextFormat("0.2f")


saveDirBase = "/afs/hephy.at/user/n/nrad/www/signals/80X/"

lepCol="LepGood"
lep="mu"

lepCol = args.lepCol
lep    = args.lep

saveDir = saveDirBase + "/%s_%s/"%(lepCol,lep)

yldpkls = {}
yldpkls['74x']="/afs/hephy.at/work/n/nrad/results/cards_and_limits/7412pass2_mAODv2_v6/74X_postProcessing_v4/13TeV/HT/ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG_presel_BinsSummary.pkl".format(lepCol=lepCol,lep=lep)
yldpkls['80x']="/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_{lepCol}_{lep}_nopu_noisr_BTAG_presel_BinsSummary.pkl".format(lepCol=lepCol,lep=lep)


yldInsts = {}
yldDicts = {}
yldMaps  = {}
effMaps  = {}

yldPlots = {}
effPlots = {}
ratio80x74xPlots = {}
ratio13TeVvs8TeVPlots = {}



## 8TeV
tf = ROOT.TFile("efficienciesSRSL.root")


combined_bins = {
                    "SRSL1a": "SR1a"  ,
                    "SRSL1b": "SR1b"  ,
                    "SRSL1c": "SR1c"  ,
                    "SRSL2" : "SR2"   , 
                }

eff8tev = {}
effPlts8tev = {}
for ob,nb in combined_bins.iteritems():
    effPlts8tev[nb] = getattr(tf,"eff"+ob)
    eff8tev[nb]     = getTH2FbinContent( effPlts8tev[nb] ) 


def getVal(uf):
    if hasattr(uf,"val"):
        return uf.val
    else:
        return uf

doStuff = False
if doStuff:
    for era in yldpkls.keys():
        yldInsts[era] = pickle.load(file(yldpkls[era]))
        yldDicts[era] = yldInsts[era].getNiceYieldDict()
        #yldMaps[era]  = yldInsts[era].getSignalYieldMap()
        effMaps[era] , yldMaps[era] = yldInsts[era].getSignalEffMap(stop_xsecs, lumi = 12864.4)
    
        bins = yldInsts[era].cutNames
        for b in bins:
            yldPlots[era] = makeStopLSPPlot("Yields_"+b+"_"+era, yldMaps[era][b], "Yields_"+b +"_"+era, key = lambda x: x.val)
            effPlots[era] = makeStopLSPPlot("AccEff_"+b+"_"+era, effMaps[era][b], "AccEff_"+b +"_"+era, key = lambda x: x.val) 
    
    
        
    c1 = ROOT.TCanvas("Ratios","Ratios", 1400,950)
    makeDir(saveDir+"/vs74x/")
    makeDir(saveDir+"/vs8TeV/")
    
    for b in bins:
        ratio80x74xPlots[b]      = makeStopLSPRatioPlot("Ratio80xVs74x%s"%b   , effMaps['80x'][b], effMaps['74x'][b], bins= [23, 237.5, 812.5, 127, 167.5, 792.5] , key =  lambda x: x.val )
        ratio80x74xPlots[b][0].Draw("COLZ TEXT")
        c1.SaveAs(saveDir+"/vs74x/%s.png"%b)
    
        if b in combined_bins.values():
            ratio13TeVvs8TeVPlots[b] = makeStopLSPRatioPlot("Ratio13TeVvs8TeV%s"%b, effMaps['80x'][b], eff8tev[b], bins= [23, 237.5, 812.5, 127, 167.5, 792.5] , key =  lambda x: getVal(x) )
            ratio13TeVvs8TeVPlots[b][0].Draw("COLZ TEXT")
            c1.SaveAs(saveDir+"/vs8TeV/%s.png"%b)
    
    
    
    
getChains = True
if getChains:
    mc_path_80x =   "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8012_mAODv2_v3/80X_postProcessing_v10/analysisHephy_13TeV_2016_v0/step1/RunIISpring16MiniAODv2_v3/"
    sig_path_80x =   "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8012_mAODv2_v3_1/80X_postProcessing_v10_1/analysisHephy_13TeV_2016_v0/step1/RunIISpring16MiniAODv2_v3/"
    data_path_80x =   "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8012_mAODv2_v3/80X_postProcessing_v10/analysisHephy_13TeV_2016_v0/step1/Data2016_v3/"





    from Workspace.DegenerateStopAnalysis.tools.getSamples_8011 import getSamples , weights
    from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
    cmgPP     = cmgTuplesPostProcessed( mc_path_80x, sig_path_80x, data_path_80x)
    sample_info  = {
                     "sampleList"   :    ['tt', 'w','qcd','z','s300_270','s300_290','s300_220']          ,
                     "wtau"         :    False          ,
                     "useHT"        :    True          ,
                     "skim"         :    'preIncLep'       ,
                     "scan"         :    True           ,
                     "getData"      :    False          ,
                     "weights"      :    cfg.weight        ,
                     "def_weights"      :    cfg.def_weights        ,
                       }
    samples80x   =   getSamples(   cmgPP = cmgPP, **sample_info   )
    samples74x   =   samples

    #assert "74" in samples74x.s300_290.tree.GetCurrentFile().GetName()




getGenWMass = True
if getGenWMass:



    #ptString = lambda x: "Max$( GenPart_pt*(abs(GenPart_pdgId)==%s) )"%x
    ptString = lambda x: "Max$( GenPart_pt*((GenPart_pdgId)==%s) )"%x


    #phiString = lambda x: "Max$( GenPart_phi*(abs(GenPart_pdgId)==%s) )"%x
    #etaString = lambda x: "Max$( GenPart_eta*(abs(GenPart_pdgId)==%s) )"%x


    lepIndex = "Max$(IndexGen_lep)"
    nuIndex  = "Max$(IndexGen_lep)+1"



    isPdg    = lambda pdg : "(GenPart_pt==%s)"%ptString(pdg)

    phiString = lambda pdg : "Sum$(GenPart_phi * %s)"%isPdg(pdg)
    etaString = lambda pdg : "Sum$(GenPart_eta * %s)"%isPdg(pdg)

    #muPt = ptString(13)
    #nuPt = ptString(-14)
    #muEta= etaString(13)
    #nuEta= etaString(-14)
    #muPhi= phiString(13)
    #nuPhi= phiString(-14)


    muPt     = "(GenPart_pt[%s] )" %lepIndex
    muPhi    = "(GenPart_phi[%s])"%lepIndex
    muEta    = "(GenPart_eta[%s])"%lepIndex

    nuPt     = "GenPart_pt[%s]" %nuIndex
    nuPhi    = "GenPart_phi[%s]"%nuIndex
    nuEta    = "GenPart_eta[%s]"%nuIndex


    isMu     = "(GenPart_pt==%s)"%muPt
    isNu     = "(GenPart_pt==%s)"%nuPt

    invMassString = lambda pt1, eta1, phi1 , pt2, eta2, phi2 : "sqrt( 2*{pt1}*{pt2}*(cosh({eta1}-{eta2}) - cos({phi1} - {phi2}) ))".format(
                                                                            pt1=pt1, eta1=eta1, phi1=phi1, pt2=pt2, eta2=eta2, phi2=phi2)
    mtString = lambda pt1, phi1 , pt2, phi2 : "sqrt( 2*{pt1}*{pt2}*(1 - cos({phi1} - {phi2}) ))".format(
                                                                            pt1=pt1,  phi1=phi1, pt2=pt2,  phi2=phi2)
   
    genWMass = invMassString( muPt , muEta, muPhi, nuPt, nuEta, nuPhi ) 
    genWmt   = mtString(muPt, muPhi,  nuPt, nuPhi)
    
    'sqrt( 2*Max$( GenPart_pt*(abs(GenPart_pdgId)==13) )*Max$( GenPart_pt*(abs(GenPart_pdgId)==14) )*(1 - cos(Sum$(GenPart_phi * (GenPart_pt==Max$( GenPart_pt*(abs(GenPart_pdgId)==14) ))) - Sum$(GenPart_phi * (GenPart_pt==Max$( GenPart_pt*(abs(GenPart_pdgId)==14) )))) ))' 

