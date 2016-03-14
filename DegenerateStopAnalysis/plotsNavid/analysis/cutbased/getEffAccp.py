
from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import makeStopLSPPlot, getTH2FbinContent
from Workspace.HEPHYPythonTools.xsecSMS import stop13TeV_NLONLL , stop8TeV_NLONLL 
import ROOT
import pickle

lumi_8tev = 19700  ##pb-1


yield_opts = {
              #'isr': { 'pkl':"./pkl/YieldInstance_Reload_Inc.pkl" , 'saveDir':"/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload_scan_isrweight/effmap/" ,'lumi':10000},
              'isr': { 'pkl':"./pkl/YieldInstance_Reload_Inc.pkl" , 'saveDir':"/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload_scan_isrweight/effmap/" , 'lumi':10000},
              'isr23fbm1': { 'pkl':"./pkl/YieldInstance_Reload_HT_isrweight_v1_Scan.pkl" , 'saveDir':"/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload_scan_isrweight/HT/effmap/" , 'lumi':10000},
              'v0':  { 'pkl':"./pkl/Scan_v0/RunII_Reload_Scan_Yields.pkl" , 'saveDir':"/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload_scan/effmap/" , 'lumi':10000},
             }

yieldopt=yield_opts['isr23fbm1']

yield_pickle =   yieldopt['pkl'] 
saveDir      =   yieldopt['saveDir']

lumi = yieldopt['lumi'] * 23000/10000.

yld = pickle.load(open(yield_pickle,"r"))
ROOT.gStyle.SetPaintTextFormat("0.2f")


cutLegend = yld.cutLegend[0][1:]
cutDict   = {i:c for i,c in enumerate(cutLegend)}


sigList = [x for x in yld.sigList if x not in  ['s30',  's30FS',  's10FS',  's60FS',  't2tt30FS'] ] 


ae = {}

icut = 0
cut = cutDict[icut]

ae={}
ylds={}

#canv = ROOT.TCanvas("canv","canv",1916,1026)
canv = ROOT.TCanvas("canv","canv",1500,1026)
canv.SetTopMargin(0.1)
canv.SetRightMargin(0.1)
canv.SetLeftMargin(0.12)
#bins = [22,100,650, 65,0,650 ]
bins = [13,87.5,412.5, 75, 17.5, 392.5 ]


ltitle = ROOT.TLatex()
ltitle.SetNDC()
ltitle.SetTextAlign(12)
lside = ROOT.TLatex()
lside.SetNDC()
lside.SetTextAlign(10)
lside.SetTextAngle(90)


tf = ROOT.TFile("8TeVMaterials/efficienciesSRSL.root")
eff8tev = tf.effSRSL1a
eff8tevDict = getTH2FbinContent(eff8tev)

pl8tev = makeStopLSPPlot("eff8tev", eff8tevDict, bins=bins)
#pl8tev = 
#assert False

title_13tev = "CMS Simulation #sqrt{s}=13 TeV"
title_8tev  = "CMS Simulation #sqrt{s}=8 TeV"
ytop = 1.05- canv.GetTopMargin()
ltitle_info = [0.1, ytop]
lside_info = [0.95,0.11]

for icut, cut in enumerate(cutLegend):
    ae[cut]={}
    ylds[cut]={}
    pl_ae={}
    pl_yl={}
    for sig in sigList:
        mstop , mlsp = [int(x) for x in sig[1:].rsplit("_")]
        yld_val = yld.yieldDictRaw[sig][icut].val
        if not ae[cut].has_key(mstop):
            ylds[cut][mstop] = {}
            ae[cut][mstop] = {}
        ylds[cut][mstop][mlsp]=yld_val
        ae[cut][mstop][mlsp]=yld_val/ ( stop13TeV_NLONLL[mstop] * lumi)
        #print mstop, mlsp , yld_val,stop13TeV_NLONLL[mstop],ae[cut][mstop][mlsp]
    pl_ae[cut] = makeStopLSPPlot("ae_%s"%cut, ae[cut], bins=bins )
    pl_yl[cut] = makeStopLSPPlot("yl_%s"%cut, ylds[cut], bins=bins )


    ROOT.gStyle.SetPaintTextFormat("0.1e")
    pl_ae[cut].Draw("COL TEXT")
    pl_ae[cut].GetYaxis().SetTitleOffset(0.9)

    ltitle.DrawLatex(ltitle_info[0], ltitle_info[1] ,title_13tev )
    lside.DrawLatex(lside_info[0], lside_info[1] , "Acceptance x Efficiency For %s"%cut)
    
    canv.Update()
    canv.SaveAs(saveDir+"AccptxEff_%s.png"%cut)
    ROOT.gStyle.SetPaintTextFormat("0.2f")
    pl_yl[cut].Draw("COL TEXT")
    pl_yl[cut].GetYaxis().SetTitleOffset(0.9)
    ltitle.DrawLatex(ltitle_info[0], ltitle_info[1] ,title_13tev )
    lside.DrawLatex(lside_info[0], lside_info[1], "Yields For %s"%cut)
    #ltitle.DrawLatex(0.5,ytop, "       Yields For %s (13TeV)"%cut )
    canv.SaveAs(saveDir+"Yields_%s.png"%cut)


##
##  Combine PtBins 
##

combined_bins = {
                    "SRSL1a": ['SRL1a', 'SRH1a', 'SRV1a'] ,
                    "SRSL1b": ['SRL1b', 'SRH1b', 'SRV1b'] ,
                    "SRSL1c": [ 'SRL1c', 'SRH1c', 'SRV1c'],
                    "SRSL2" : ['SRL2', 'SRH2', 'SRV2'],
                }

for cut in combined_bins:

    tocombine = combined_bins[cut]

    ae[cut]={}
    ylds[cut]={}
    for sig in sigList:
        mstop , mlsp = [int(x) for x in sig[1:].rsplit("_")]
    
    
        if not ae[cut].has_key(mstop):
            ylds[cut][mstop] = {}
            ae[cut][mstop] = {}
        yld_val = sum([ylds[ic][mstop][mlsp] for ic in tocombine])
        ylds[cut][mstop][mlsp] = yld_val 
        ae[cut][mstop][mlsp]=yld_val/ ( stop13TeV_NLONLL[mstop] * lumi)

    
    pl_ae[cut] = makeStopLSPPlot("ae_%s"%cut, ae[cut], bins=bins )
    pl_yl[cut] = makeStopLSPPlot("yl_%s"%cut, ylds[cut], bins=bins )
    
    
    
    ROOT.gStyle.SetPaintTextFormat("0.1e")
    pl_ae[cut].Draw("COL TEXT")
    pl_ae[cut].GetYaxis().SetTitleOffset(0.9)
    
    ltitle.DrawLatex(ltitle_info[0], ltitle_info[1] ,title_13tev )
    lside.DrawLatex(lside_info[0], lside_info[1], "Acceptance x Efficiency For %s"%cut)

    
    canv.Update()
    canv.SaveAs(saveDir+"AccptxEff_%s.png"%cut)
    ROOT.gStyle.SetPaintTextFormat("0.2f")
    pl_yl[cut].Draw("COL TEXT")
    pl_yl[cut].GetYaxis().SetTitleOffset(0.9)

    ltitle.DrawLatex(ltitle_info[0], ltitle_info[1] ,title_13tev )
    lside.DrawLatex(lside_info[0], lside_info[1], "Yields For %s"%cut)


    #ltitle.DrawLatex(0.5,ytop, "       Yields For %s (13TeV)"%cut )
    canv.SaveAs(saveDir+"Yields_%s.png"%cut)




    

##
##  Take Ratio of 13TeV and 8TeV
##    



ratio={}
pl_ratio = {}
pl_8tev={}
pl_yl8tev={}
eff8tevdicts = {}
yld_ratio = {} 
yldpl_ratio = {}
yld8tevDict = {}

ltitle2 = ROOT.TLatex()
ltitle2.SetNDC()


for cut in combined_bins:
    tocombine = combined_bins[cut]
    ratio[cut]={}
    eff8tev = getattr(tf, "eff%s"%cut ) 
    eff8tevDict = getTH2FbinContent(eff8tev)
    eff8tevdicts[cut]=eff8tevDict

    for sig in sigList:
        mstop , mlsp = [int(x) for x in sig[1:].rsplit("_")]    
        if mstop > 425: continue
        if not ratio[cut].has_key(mstop):
            ratio[cut][mstop]={}
        ratio[cut][mstop][mlsp] = ae[cut][mstop][mlsp]/eff8tevDict[mstop][mlsp]         

    pl_ratio[cut] = makeStopLSPPlot("ratio_%s"%cut, ratio[cut], bins=bins )
    pl_ratio[cut].SetContour(4 ) 
    pl_ratio[cut].SetContourLevel(0,0 )
    pl_ratio[cut].SetContourLevel(1,1 )
    pl_ratio[cut].SetContourLevel(2,2 )
    pl_ratio[cut].SetContourLevel(3,10 )
    pl_ratio[cut].SetContourLevel(4,100 )
    ROOT.gStyle.SetPaintTextFormat("0.1e")
    pl_ratio[cut].Draw("COL TEXT")
    pl_ratio[cut].GetYaxis().SetTitleOffset(0.9)
    ltitle.DrawLatex(0.2, 0.8, "#frac{A.#varepsilon(13TeV)}{A.#varepsilon(8TeV)}       %s"%cut  )
    #lside.DrawLatex(0.98,0.15, "#frac{A.#varepsilon(13TeV)}{A.#varepsilon(8TeV)} For %s"%cut)
    #lside.DrawLatex(0.98,0.15, "#frac{A.#varepsilon(13TeV)}{A.#varepsilon(8TeV)} For %s"%cut)


    

    canv.SaveAs(saveDir+"RatioEffMap_%s.png"%cut)
    #canv.SaveAs(saveDiAcceptance x Efficiency For a
    pl_8tev[cut] = makeStopLSPPlot("effMap_8TeV_%s"%cut, eff8tevDict , bins=bins )
    pl_8tev[cut].Draw("COL TEXT")
    pl_8tev[cut].GetYaxis().SetTitleOffset(0.9)
    ltitle.DrawLatex(ltitle_info[0], ltitle_info[1] ,title_8tev )
    lside.DrawLatex(lside_info[0], lside_info[1], "Acceptance x Efficiency For %s"%cut)
    canv.SaveAs(saveDir+"AcceptxEff_8TeV_%s.png"%cut)



    yld8tevDict[cut] = {}
    
    for mstop in eff8tevDict:
        if not yld8tevDict[cut].has_key(mstop): yld8tevDict[cut][mstop]={}
        for mlsp in eff8tevDict[mstop]:
            yld8tevDict[cut][mstop][mlsp]= eff8tevDict[mstop][mlsp] * stop8TeV_NLONLL[mstop] * lumi_8tev 
    pl_yl8tev[cut] = makeStopLSPPlot("Yields_8TeV_%s"%cut, yld8tevDict[cut] , bins=bins ) 
    ROOT.gStyle.SetPaintTextFormat("0.2f")
    pl_yl8tev[cut].Draw("COL TEXT")
    pl_yl8tev[cut].GetYaxis().SetTitleOffset(0.9)
    ltitle.DrawLatex(ltitle_info[0], ltitle_info[1] ,title_8tev )
    lside.DrawLatex(lside_info[0], lside_info[1], "Acceptance x Efficiency For %s"%cut)
    canv.SaveAs(saveDir+"Yields_8TeV_%s.png"%cut)




    yldpl_ratio[cut] = {}
    yld_ratio[cut] = {}
    for sig in sigList:
        mstop , mlsp = [int(x) for x in sig[1:].rsplit("_")]    
        if mstop > 425: continue
        if not yld_ratio[cut].has_key(mstop):
            yld_ratio[cut][mstop]={}
        #yld_ratio[cut][mstop][mlsp] = ae[cut][mstop][mlsp]/eff8tevDict[mstop][mlsp]         
        yld_ratio[cut][mstop][mlsp] = ylds[cut][mstop][mlsp]/yld8tevDict[cut][mstop][mlsp]

    yldpl_ratio[cut] = makeStopLSPPlot("Ratio_Yield_%s"%cut, ratio[cut], bins=bins )
    yldpl_ratio[cut].SetContour(4 ) 
    yldpl_ratio[cut].SetContourLevel(0,0 )
    yldpl_ratio[cut].SetContourLevel(1,1 )
    yldpl_ratio[cut].SetContourLevel(2,2 )
    yldpl_ratio[cut].SetContourLevel(3,10 )
    yldpl_ratio[cut].SetContourLevel(4,100 )
    ROOT.gStyle.SetPaintTextFormat("0.1e")
    yldpl_ratio[cut].Draw("COL TEXT")
    yldpl_ratio[cut].GetYaxis().SetTitleOffset(0.9)
    ltitle.DrawLatex(0.2, 0.8, "#frac{ Y_{13TeV} }{ Y_{8TeV} }        %s"%cut  )
    canv.SaveAs(saveDir+"RatioYields_%s.png"%cut)
    #lside.DrawLatex(0.98,0.15, "#frac{A.#varepsilon(13TeV)}{A.#varepsilon(8TeV)} For %s"%cut)
    #lside.DrawLatex(0.98,0.15, "#frac{A.#varepsilon(13TeV)}{A.#varepsilon(8TeV)} For %s"%cut)



