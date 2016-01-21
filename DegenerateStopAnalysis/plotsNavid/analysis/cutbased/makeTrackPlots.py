from Workspace.DegenerateStopAnalysis.cuts import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_mAODv2_7412pass2 import getSamples
from makeTable import *
from limitCalc import *

from Tracks import *



from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import *






import dmt
import tracks


saveDir = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/newSignals/WTauNoTau_v4/'
#sampleList=['s10FS', 's30', 's30FS', 's60FS', 't2tt30FS', 'z', 'tt', 'wtau', 'wnotau']
sampleList=['s10FS', 's30', 's30FS', 's60FS', 't2tt30FS', 'z', 'tt', 'w']
sampleList=['s10FS' , 's30' , 'z' , 'w']
plotList=[]

try:
    samples
except NameError:
    samples = getSamples(wtau=False,useHT=False)

if not samples.s30.tree.GetEventList():
    pass
    #setEventListToChains(samples,sampleList,sr1Loose)



gen2p5vetoOpp12 = [  x for x in  tracks.multipPlots.keys() if \
                                ("vetoJet" in x or "onlyJet"  in x) 
                            and "ElVeto" not in x and "LepVeto" not in x
                            and "Pt2p5" in x  
                            and "Jet12" in x 
                            #and ( "Jet30Trk" in x or "Jet60Trk" in x)  
                            #and ( "Opp90" in x or "Opp270" in x)
                            and ( "Jet60Trk"  in x  or "Jet30Trk" in x )  
                            and ( "Opp270" in x or "Opp90" in x)
                  ]


trkq        = [  x for x in  tracks.quantPlots.keys() if \
                                ("vetoJet" in x or "onlyJet"  in x)
                            and "ElVeto" not in x and "LepVeto" not in x
                            and "Pt2p5" in x 
                            and "Jet12" in x 
                            #and ( "Jet30Trk" in x or "Jet60Trk" in x)  
                            #and ( "Opp90" in x or "Opp270" in x)
                            and ( "Jet60Trk" in x  )
                            and ( "Opp270" in x )
                            and  "pt_" in x
                  ]



ntrkPlotList = tracks.multipPlots.keys()
ntrkPlotList = gen2p5vetoOpp12

ntrkPlotList = [ x for x in ntrkPlotList if "nTracks" in x]

print ntrkPlotList


dmtBMs= [ dmt.dmtBM1R1, dmt.dmtBM1R2 , dmt.dmtBM1R3   ]
getDMTRegions=False
if getDMTRegions:
    cutInst = sr1Loose
    setEventListToChains(samples,sampleList,cutInst)
    print "--"*30
    print cutInst.name
    print "--"*30
    #getPlots(samples, dmt.plots , cutInst, sampleList = sampleList , plotList= ['DMT'] )
    #draw2DPlots(samples, dmt.plots , cutInst , sampleList = sampleList, plotList=['DMT'], save=saveDir , leg=False)
    getPlots(samples, tracks.multipPlots , cutInst, sampleList = sampleList, plotList=ntrkPlotList, addOverFlowBin='upper' )
    drawPlots(samples,  tracks.multipPlots , cutInst, sampleList = sampleList, plotList=ntrkPlotList , save=saveDir, min=0.1)


dOpt="samelp"
iColor=1
rocs={}

first=True
for p in ntrkPlotList:
    sHist = samples.s30.cuts.sr1Loose[p]
    bHist = samples.w.cuts.sr1Loose[p]
    if first:
        eff=get2DEffFOM(sHist,bHist,10,10,fom="AMSSYS")
        eff.Draw("COLZ")
    roc = getROC(sHist,bHist,fom="AMSSYS" )
    roc['roc'].SetName(p)
    roc['roc'].SetLineColor(iColor)
    roc['roc'].Draw(dOpt)
    rocs[p]=roc
    iColor+=1
    dOpt = "lpsame"     


if False:
    foms={}
    canvs={}
    fomTestDir='/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/fomTestDir/'
    for fom in fomFuncs: 
        foms[fom]=get2DEffFOM(sHist, bHist, nBinsX=20, nBinsY=20, bkgRej=True, fom=fom)
        canvs[fom]=ROOT.TCanvas(fom,fom)
        foms[fom].Draw("COLZTEXT")
        canvs[fom].SaveAs(fomTestDir+"/%s.png"%fom)



