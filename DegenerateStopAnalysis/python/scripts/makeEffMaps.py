#yld = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_SF/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_SF_presel_BinsSummary.pkl"))
#yld = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_LepAll_lep_nopu_SF/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_LepAll_lep_nopu_SF_presel_BinsSummary.pkl"))
yld = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_LepAll_lep_nopu_noisr_SF/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_LepAll_lep_nopu_noisr_SF_presel_BinsSummary.pkl"))
yld = pickle.load(file("/afs/hephy.at/work/n/nrad/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_LepAll_lep_nopu_noisr_BTAG/AdjustedSys/presel/Yields_12864pbm1_ApprovalSys_Mt95_Inccharge_LepAll_lep_nopu_noisr_BTAG_presel_BinsSummary.pkl"))
import Workspace.HEPHYPythonTools.xsecSMS as xsecSMS
stop_xsecs = xsecSMS.stop13TeV_NLONLL



effDicts, yldDicts =  yld.getSignalEffMap( stop_xsecs , 12864.4)






ylds_74x = pickle.load(file("74x_yields.pkl"))


bins = ['SR1a', 'SR1b', 'SR1c', 'SR2']


stop_lsp_bins = [23, 237.5, 812.5, 125, 167.5, 792.5]

bins_to_add = {
                  'SR1a'    : ["SRL1a", "SRV1a", "SRH1a" ]  ,
                  'SR1b'    : ["SRL1b", "SRV1b", "SRH1b" ]  , 
                  'SR1c'    : ["SRL1c", "SRV1c", "SRH1c" ]  ,
                  'SR2'     : ["SRL2" , "SRV2" , "SRH2"  ]  ,
               }




yieldMaps_80x = {}
for s in yld.sigList:
    mstop, mlsp = getMasses(s)
    if not yieldMaps_80x.has_key(mstop):
        yieldMaps_80x[mstop] = {}
    if not yieldMaps_80x[mstop].has_key(mlsp):    
        yieldMaps_80x[mstop][mlsp] = {}
    for b in yldDicts.keys():
        yieldMaps_80x[mstop][mlsp][b] = yldDicts[b][mstop][mlsp]


yieldMaps_74x={}
effMaps_74x = {}
for s in ylds_74x:
    if "FOM" in s: continue
    if not "T2-4bd" in s: continue
    mstop, mlsp = getMasses(s)
    if not mstop in yieldMaps_74x:
        yieldMaps_74x[mstop]={}
    if not mstop in effMaps_74x:
        effMaps_74x[mstop]  = {}
    if not mlsp in effMaps_74x[mstop]:
        effMaps_74x[mstop][mlsp]={}
    yieldMaps_74x[mstop][mlsp]= ylds_74x[s]
    for b, bta in bins_to_add.iteritems():
        yieldMaps_74x[mstop][mlsp][b] = sum([ylds_74x[s][x] for x in bta])
    for b in yieldMaps_74x[mstop][mlsp].keys():
       effMaps_74x[mstop][mlsp][b]  =  yieldMaps_74x[mstop][mlsp][b] / (stop_xsecs[mstop] * 10000 )


effDicts_74x = {}
yldDicts_74x = {}
for b in effDicts.keys():
    effDicts_74x[b] = {}
    yldDicts_74x[b] = {}
    for mstop in effMaps_74x.keys():
        effDicts_74x[b][mstop] = {}
        yldDicts_74x[b][mstop] = {}
        for mlsp in effMaps_74x[mstop].keys():
            effDicts_74x[b][mstop][mlsp] = effMaps_74x[mstop][mlsp][b]
            yldDicts_74x[b][mstop][mlsp] = yieldMaps_74x[mstop][mlsp][b]

yieldMaps_74x_12p9 = {}
for mstop in yieldMaps_74x.keys():
    yieldMaps_74x_12p9[mstop] = {}
    for mlsp in yieldMaps_74x[mstop].keys():
        yieldMaps_74x_12p9[mstop][mlsp] = {}
        for b in yieldMaps_74x[mstop][mlsp].keys():
            yieldMaps_74x_12p9[mstop][mlsp][b] = yieldMaps_74x[mstop][mlsp][b] * 12864.4 / 10000 
            

effPlots = {}
yldPlots = {}
effPlots_74x = {}
yldPlots_74x = {}
c1 = ROOT.TCanvas("c1","c1", 1600, 1000 )
for b in bins:
    effPlots[b]  = makeStopLSPPlot(     "EffMap_%s"%b    , effDicts[b]       , title= "effMap_%s"%b,    bins = stop_lsp_bins , key = lambda x: x.val, func=None, setbin=False, massFunc=None)
    yldPlots[b]  = makeStopLSPPlot(     "YldMap_%s"%b    , yldDicts[b]     , title= "YldMap_%s"%b,    bins = stop_lsp_bins , key = lambda x: x.val, func=None, setbin=False, massFunc=None)
    effPlots_74x[b] = makeStopLSPPlot(  "EffMap74X_%s"%b , effDicts_74x[b]   , title= "effMap74X_%s"%b, bins = stop_lsp_bins , key = lambda x: x.val, func=None, setbin=False, massFunc=None)
    yldPlots_74x[b] = makeStopLSPPlot(  "YldMap74X_%s"%b , yldDicts_74x[b]   , title= "YldMap74X_%s"%b, bins = stop_lsp_bins , key = lambda x: x.val, func=None, setbin=False, massFunc=None)
    if False:
        effPlots[b].Draw("COLZ TEXT")
    effPlots[b].SetMarkerSize(0.7)
    yldPlots[b].SetMarkerSize(0.7)
    effPlots_74x[b].SetMarkerSize(0.7)
    yldPlots_74x[b].SetMarkerSize(0.7)




effRatio80Xvs74x = {}
yldRatio80Xvs74x = {}
for b in bins:
    effRatio80Xvs74x[b] = effPlots[b].Clone("EffAccpRatio80Xvs74x_%s"%s)
    effRatio80Xvs74x[b].Divide( effPlots_74x[b] )
    yldRatio80Xvs74x[b] = yldPlots[b].Clone("YieldRatio80Xvs74x_%s"%s)
    yldRatio80Xvs74x[b].Divide( yldPlots_74x[b] )
    yldRatio80Xvs74x[b].Scale(10000./12864.4)

doDraw = True

saveDir = "/afs/hephy.at/user/n/nrad/www/signals/80X/EffMaps/vs74x/"
ROOT.gStyle.SetPaintTextFormat("0.2f")

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.05)






bins_to_add_2 = {
                   "CR1" : ["CR1a","CR1b","CR1c"],
                   "CR"  : ["CR1a","CR1b","CR1c", "CR2"],
                   "SR1" : [ "SRL1a", "SRH1a", "SRV1a" ,  "SRL1b", "SRH1b", "SRV1b",   "SRL1c", "SRH1c", "SRV1c"],
                   "SR"  : [ "SRL1a", "SRH1a", "SRV1a" ,  "SRL1b", "SRH1b", "SRV1b",   "SRL1c", "SRH1c", "SRV1c" , "SRL2","SRH2","SRV2"],
                   "CRSR": ["SRL1a", "SRH1a", "SRV1a" ,  "SRL1b", "SRH1b", "SRV1b",   "SRL1c", "SRH1c", "SRV1c" , "SRL2","SRH2","SRV2", "CR1a","CR1b","CR1c", "CR2"],
                }


for bt,bta in bins_to_add_2.iteritems():
    effRatio80Xvs74x[bt] , d = makeStopLSPRatioPlot("test", yieldMaps_80x, yieldMaps_74x_12p9 ,bins=stop_lsp_bins, key = lambda a: ( sum([a[b] for b in bta]) ).val )    




if doDraw:
    for b in effRatio80Xvs74x.keys():
        effRatio80Xvs74x[b].Draw("COLZ TEXT")
        latex.DrawLatex(0.2,0.7, "#frac{Acc.*eff(80X)}{Acc.*eff(74X)}  %s"%b)
        c1.SaveAs(saveDir + "/effRatio80Xvs74x_%s.png"%b)


