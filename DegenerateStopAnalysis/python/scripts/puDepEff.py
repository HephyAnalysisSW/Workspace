#yld = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_SF/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_SF_presel_BinsSummary.pkl"))
import pickle
import Workspace.HEPHYPythonTools.xsecSMS as xsecSMS
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import ROOT

ROOT.TH1.SetDefaultSumw2(1)
ROOT.gStyle.SetOptStat(0)

stop_xsecs = xsecSMS.stop13TeV_NLONLL


withPuW = False

if withPuW:
    saveDir = "/afs/hephy.at/user/n/nrad/www/signals/80X/puDep/"
    yldTemp = "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_LepAll_lep_pu{puCut}_SF/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_LepAll_lep_pu{puCut}_SF_presel_BinsSummary.pkl"
    totYldPkl = "puTotYields.pkl"
else:
    saveDir = "/afs/hephy.at/user/n/nrad/www/signals/80X/puDep_noPUW/"
    yldTemp = "/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_LepAll_lep_nopu{puCut}_SF/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_LepAll_lep_nopu{puCut}_SF_presel_BinsSummary.pkl"
    totYldPkl = "puTotYields_noPUW.pkl"

totYld    = pickle.load(file(totYldPkl))


puCuts = [ 15,20,25 ]
#puCuts = [ 20 ]
puOps  = { 'gt':'>=', 'lt':'<' }

tag_legs={
           'gt25' :{'color':   ROOT.kBlue     ,'leg':  "PU >= 25"       , 'style':  1}  , 
           'lt25' :{'color':   ROOT.kBlue     ,'leg':  "PU < 25"        , 'style':  5}  ,
           'gt20' :{'color':   ROOT.kBlue     ,'leg':  "PU >= 20"       , 'style':  1}  , 
           'lt20' :{'color':   ROOT.kBlue     ,'leg':  "PU < 20"        , 'style':  5}  , 
           'gt15' :{'color':   ROOT.kBlue     ,'leg':  "PU >= 15"       , 'style':  1}  , 
           'lt15' :{'color':   ROOT.kBlue     ,'leg':  "PU < 15"        , 'style':  5}  , 
         }

u_float = degTools.u_float
def getBinContentAndError(hist,ib):
    return u_float( hist.GetBinContent(ib), hist.GetBinError(ib) ) 


puYlds = {}
puYldPkls = {}
puYieldDicts = {}
puYieldMaps  = {}
for puCut in puCuts:
    for puOpTag, puOp in puOps.iteritems():
        tag = puOpTag+"%s"%puCut
        puYldPkls[tag] = yldTemp.format(puCut="_"+tag)
        puYlds[tag]     = pickle.load(file(puYldPkls[tag]))
        puYieldDicts[tag] = puYlds[tag].yieldDict
        puYieldMaps[tag]  = puYlds[tag].getSignalYieldMap()


bins = ['SR1a', 'SR1b', 'SR1c', 'SR2']


stop_lsp_bins = [23, 237.5, 812.5, 127, 167.5, 792.5]

bins_to_add = {
                  'SR1a'    : ["SRL1a", "SRV1a", "SRH1a" ]  ,
                  'SR1b'    : ["SRL1b", "SRV1b", "SRH1b" ]  , 
                  'SR1c'    : ["SRL1c", "SRV1c", "SRH1c" ]  ,
                  'SR2'     : ["SRL2" , "SRV2" , "SRH2"  ]  ,
               }

passHists = {}
totHists  = {}
teffHists  = {}
ratios     = {}

mstops = range(250,801,25)
dms    = range(10,81,10)

sigList= puYlds[tag].sigList


def divideEff(e1,e2):
    n = e1.GetTotalHistogram().GetNbinsX()
    a = e1.GetTotalHistogram().GetBinLowEdge(1)
    w = e1.GetTotalHistogram().GetBinWidth(1)
    res = ROOT.TGraphAsymmErrors(n)
    for i in range(n):
        v1 = e1.GetEfficiency(i+1)
        u1 = e1.GetEfficiencyErrorUp(i+1)
        d1 = e1.GetEfficiencyErrorLow(i+1)
        v2 = e2.GetEfficiency(i+1)
        u2 = e2.GetEfficiencyErrorUp(i+1)
        d2 = e2.GetEfficiencyErrorLow(i+1)
        if v1*v2 == 0:
            v = 0.
            u = 0.
            d = 0.
        else:
            v = v1/v2 if v2>0. else 0.
            u = v*sqrt(pow(u1/v1,2)+pow(u2/v2,2))
            d = v*sqrt(pow(d1/v1,2)+pow(d2/v2,2))
        print i,v,u,d
        x = a+(i+0.5)*w
        res.SetPoint(i,x,v)
        res.SetPointError(i,w/2.,w/2.,d,u)
    return res
def divideHist(h1,h2):
    res = h1.Clone()
    res.Divide(h2)
    return res




for puCut in puCuts:
    for puOpTag, puOp in puOps.iteritems():
        tag = puOpTag+"%s"%puCut

        passHists[tag]={}
        totHists[tag]={}
        teffHists[tag]={}
        for sig in sigList:
            mstop, mlsp = degTools.getMasses(sig)
            passHists[tag][sig] = ROOT.TH1D( "pass_%s_%s"%(sig,tag), "pass_%s_%s"%(sig,tag), len(bins), 0,4) 
            totHists[tag][sig]  = ROOT.TH1D( "tot_%s_%s"% (sig,tag),  "tot_%s_%s"%(sig,tag), len(bins), 0,4)       
            for ib, b in enumerate(bins):
                passHists[tag][sig].SetBinContent(ib+1, puYieldDicts[tag][sig][b].val ) 
                passHists[tag][sig].SetBinError(ib+1, puYieldDicts[tag][sig][b].sigma ) 
                passHists[tag][sig].GetXaxis().SetBinLabel(ib+1,b)
                passHists[tag][sig].SetNdivisions(504,'x')
                totHists[tag][sig].SetBinContent(ib+1, totYld[mstop][mlsp][tag].val ) 
                totHists[tag][sig].SetBinError(ib+1, totYld[mstop][mlsp][tag].sigma ) 
                totHists[tag][sig].GetXaxis().SetBinLabel(ib+1,b)

                totHists[tag][sig].SetLineColor(tag_legs[tag]['color'])
                totHists[tag][sig].SetLineStyle(tag_legs[tag]['style'])
                passHists[tag][sig].SetLineColor(tag_legs[tag]['color'])
                passHists[tag][sig].SetLineStyle(tag_legs[tag]['style'])
            #assert False
            passHists[tag][sig].Sumw2()
            totHists[tag][sig].Sumw2()

                    
            #teffHists[tag][sig]=ROOT.TEfficiency( passHists[tag][sig],totHists[tag][sig] )
            teffHists[tag][sig] = passHists[tag][sig].Clone()
            teffHists[tag][sig].Divide( totHists[tag][sig] )
            teffHists[tag][sig].SetLineStyle(tag_legs[tag]['style'])

for puCut in puCuts:
    ratios[puCut]={}
    for sig in sigList:
        gtTag = 'gt%s'%puCut
        ltTag = 'lt%s'%puCut
        #ratios[puCut][sig]=divideEff( teffHists[gtTag][sig] , teffHists[ltTag][sig] )
        ratios[puCut][sig]=divideHist( teffHists[gtTag][sig] , teffHists[ltTag][sig] )



canvs = {}
legs = {}

puCut = puCuts[0]
unity = passHists[tag][sig].Clone("unity")
unity.Divide(passHists[tag][sig])
unity.Sumw2(0)
unity.SetLineColor(ROOT.kBlack)


for sig in ['s300_270', 's300_290', 's300_220']:
    canvs[sig]=degTools.makeCanvasMultiPads(sig,pads=[], padRatios=[2,1])
    canvs[sig][1].cd()
    canvs[sig][1].SetRightMargin(0.05)
    canvs[sig][2].SetRightMargin(0.05)
    canvs[sig][1].SetLeftMargin(0.15)
    canvs[sig][2].SetLeftMargin(0.15)
    legs[sig] = ROOT.TLegend(0.6,0.6,0.95,0.9,"%s"%sig)

    gtTag = 'gt%s'%puCut
    ltTag = 'lt%s'%puCut

    teffHists[gtTag][sig].Draw()
    teffHists[ltTag][sig].Draw('same')

    legs[sig].AddEntry( teffHists[gtTag][sig], tag_legs[gtTag]['leg'],"l" )
    legs[sig].AddEntry( teffHists[ltTag][sig], tag_legs[ltTag]['leg'],"l" )

    legs[sig].Draw()
    canvs[sig][2].cd()
    passHists[tag][sig].Draw("AXIS")
    passHists[tag][sig].SetStats(0)
    passHists[tag][sig].SetYTitle("#frac{Accp*Eff  %s}{Accp*Eff  %s}   "%(tag_legs[gtTag]['leg'],tag_legs[ltTag]['leg']))
    passHists[tag][sig].GetYaxis().SetTitleSize(0.07)
    passHists[tag][sig].GetYaxis().SetTitleOffset(0.55)
    #passHists[tag][sig].
    #passHists[tag][sig].
    passHists[tag][sig].GetYaxis().SetLabelSize(0.06)
    #passHists[tag][sig].GetYaxis().SetLabel('asdfa')
    passHists[tag][sig].SetNdivisions(504,"y")
    passHists[tag][sig].SetMinimum(0)
    passHists[tag][sig].SetMaximum(2)
    passHists[tag][sig].SetLabelSize(0.18)
    ratios[puCut][sig].Draw("same")
    ratios[puCut][sig].Draw("E0same")
    unity.Draw("same")
    canvs[sig][0].Update()

    saveDir_ = saveDir +"/" + 'pu%s'%puCut+"/"
    degTools.makeDir(saveDir_)
    canvs[sig][0].SaveAs(saveDir_+"/%s.png"%sig)

            #for ib, b in enumerate(bins):
            #    effHists[tag][sig].GetXaxis().SetBinLabel(ib+1,b)
            #    effHists[tag][sig].SetNdivisions(504,'x')


def getPUDep(sig,puCut,ib):
    ltp = getBinContentAndError( passHists['lt%s'%puCut][sig],ib)
    ltt = getBinContentAndError( totHists['lt%s'%puCut][sig],ib)
    ltp / ltt
    gtt = getBinContentAndError( totHists['gt%s'%puCut][sig],ib)
    gtp = getBinContentAndError( passHists['gt%s'%puCut][sig],ib)
    gtp / gtt
    lteff = ltp / ltt
    gteff = gtp / gtt
    return gteff/lteff






