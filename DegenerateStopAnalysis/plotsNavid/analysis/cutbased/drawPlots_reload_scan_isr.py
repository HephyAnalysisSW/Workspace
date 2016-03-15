
import sys,os

#oldargv = sys.argv[ : ]
#sys.argv = [ '-b-' ]
#import ROOT
#ROOT.gROOT.SetBatch(True)
#sys.argv = oldargv

from Workspace.DegenerateStopAnalysis.cuts.cuts import *
from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import *
from Workspace.DegenerateStopAnalysis.navidTools.makeTable import *
from Workspace.DegenerateStopAnalysis.navidTools.limitCalc import  getLimit, plotLimits




from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_mAODv2 import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_mAODv2_7412pass2_scan import getSamples


import plots





mc_path     = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/RunIISpring15DR74_25ns"
signal_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/RunIISpring15DR74_25ns"
data_path   = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/Data_25ns"




print sys.argv
parser = ArgParser()
args=parser.parse(sys.argv)
sampleList= args.sampleList

#cutInstStr = args.cutInst
process = args.process
useHT   = args.useHT

runtag = "isrweight_v1"
doscan = True


scantag = "_Scan" if doscan else ""

print args, sampleList ,  process
htString = "HT" if useHT else "Inc"



saveDir = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/%s/%s'%(runtag,htString)
plotDir = saveDir +"/DataPlots/" 

#sampleList         = [ 's30'   , 's10FS' , 's40FS'  ,'s30FS', 't2tt30FS','wtau','wnotau' , 'qcd'     ,'z'    , 'tt' ,  'w' ,'dblind','d']
sampleList          = [ 's30'   , 's10FS' , 's40FS'  ,'s30FS', 't2tt30FS','qcd'     ,'z'    , 'tt' ,  'w' ,'dblind','d']
try:
    samples
except NameError:
    cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)
    samples = getSamples(wtau=False,sampleList=sampleList,useHT=useHT,skim='presel', scan=doscan, cmgPP=cmgPP, getData=True)


samples.s225_215.color = ROOT.kRed
samples.s225_145.color = ROOT.kBlue



plotList = ["ht","ct"]
plotList = ["met", "mt","ht","ct", "LepPhi", "LepEta", "nJets30", "nJets60", "nBJets", "nSoftBJets", "nHardBJets" ,"LepPt"]
plotListSR = ["LepPtSR","mtSR"] + plotList
plotListCR = plotList


doDataPlots = process
#doDataPlots = False
if doDataPlots:
    yields={}
    tfile = ROOT.TFile("test.root","new")      

    #sampleList         = [  's10FS' , 's30FS' ,'s60FS'   , 'z', 'qcd'      , 'tt' ,  'w' ] 
    #sampleList         = [  's225_215', 's225_145', 'z', 'qcd'      , 'tt' ,  'w' ] 

    sigList     = [ 's225_215', 's225_145' ]
    #sigList     = [ 's10FS' , 's30FS' ,'s60FS'  ] 
    bkgList     = [ 'z', 'qcd'      , 'tt' ,  'w' ]

    sampleList = sigList + bkgList

    print sampleList


    crSampleList       = sampleList + ['dblind']
    srSampleList       = sampleList + ['d']
    fomLimits          = [0,3]

    cutInst = cr1
    sampleList = crSampleList
    setEventListToChains(samples,sampleList, cutInst)
    getPlots(samples, plots.plots , cutInst, sampleList= sampleList, plotList=plotListCR , addOverFlowBin='both',weight="weight"  )
    pl_cr1 = drawPlots(samples,    plots.plots , cutInst, sampleList= sampleList,
                    plotList= plotListCR ,save=plotDir, plotMin=0.01,
                    normalize=False, denoms=["bkg"], noms=["dblind"], fom="RATIO", fomLimits=fomLimits)


    cutInst = cr2
    sampleList = crSampleList
    setEventListToChains(samples,sampleList,cutInst)
    getPlots(samples, plots.plots , cutInst , sampleList= sampleList , plotList=plotListCR , addOverFlowBin='both',weight="weight"  )
    pl_cr2 = drawPlots(samples,    plots.plots , cutInst, sampleList= [ "z","qcd","w","tt"]+sigList+[ "dblind"],
                    plotList= plotListCR ,save=plotDir, plotMin=0.01,
                    normalize=False, denoms=["bkg"], noms=["dblind"], fom="RATIO", fomLimits=fomLimits)



    cutInst = crtt2
    sampleList = crSampleList
    setEventListToChains(samples,sampleList ,cutInst)
    getPlots(samples, plots.plots , cutInst , sampleList= sampleList , plotList=plotListCR , addOverFlowBin='both',weight="weight"  )
    pl_crtt = drawPlots(samples,    plots.plots , cutInst, sampleList= [ "z","qcd","w","tt"]+ sigList + ["dblind"],
                    plotList= plotListCR ,save=plotDir, plotMin=0.01,
                    normalize=False, denoms=["bkg"], noms=["dblind"], fom="RATIO", fomLimits=fomLimits)


    cutInst = presel
    sampleList = srSampleList
    setEventListToChains(samples, sampleList, cutInst)
    getPlots(samples, plots.plots , cutInst  , sampleList= sampleList   , plotList=plotListSR , addOverFlowBin='both',weight="weight"  )
    pl_presel = drawPlots(samples,    plots.plots , cutInst, sampleList= sampleList,
                    plotList= plotListSR ,save=plotDir, plotMin=0.001,
                    normalize=False, denoms=["bkg"], noms=["d"], fom="RATIO", fomLimits=fomLimits)

    cutInst = sr1
    sampleList = srSampleList
    setEventListToChains(samples, sampleList ,cutInst)
    getPlots(samples, plots.plots , cutInst  , sampleList= sampleList    , plotList=plotListSR , addOverFlowBin='both',weight="weight"  )
    pl_sr1 = drawPlots(samples,    plots.plots , cutInst, sampleList= sampleList,
                    plotList= plotListSR ,save=plotDir, plotMin=0.001,
                    normalize=False, denoms=["bkg"], noms=["d"], fom="RATIO", fomLimits=fomLimits)

    cutInst = sr2
    sampleList = srSampleList
    setEventListToChains(samples, sampleList ,cutInst)
    getPlots(samples, plots.plots , cutInst  , sampleList=sampleList      , plotList=plotListSR , addOverFlowBin='both',weight="weight"  )
    setEventListToChains(samples, sampleList ,presel)
    getPlots(samples, plots.plots , cutInst  , sampleList=sampleList     , nMinus1="B" ,plotList=["nBJets","nSoftBJets","nHardBJets"] , addOverFlowBin='both',weight="weight"  )
    pl_sr2 = drawPlots(samples,    plots.plots , cutInst, sampleList= ["z", 'qcd',"w",'tt'] +sigList+["d"],
                    plotList= plotListSR ,save=plotDir, plotMin=0.001,
                    normalize=False, denoms=["bkg"], noms=["d"], fom="RATIO", fomLimits=fomLimits)


    tfile.Write()
    tfile.Close()

tableDir=saveDir+"/Tables/"
if not os.path.isdir(tableDir):
    os.mkdir(tableDir)


cutInsts= {
            "runI"      :   {"cut":runI      ,  "opt":"list"},
          }
cutInstStr="runI"
cutInst = cutInsts[cutInstStr]['cut']
cutOpt = cutInsts[cutInstStr]['opt']

#calcTrkCutLimit = False
calcTrkCutLimit = process
if calcTrkCutLimit:

    limits={}
    yields={}

    bkgListForTable = [  'qcd' ,'z'   ,    'tt',  'w' ] 
    sigListForTable = [  's30'   , 's30FS' , 's10FS' , 's60FS'   , 't2tt30FS' ] 
    scanListForTable = [s for s in samples if samples[s].isSignal and s not in sigListForTable]
    scanListForTable = [s for s in samples if samples[s].isSignal and not any(x in s for x in ["s350_290","s325_275","s375_315","s350_270"]) and s not in sigListForTable]
    #sampleList = scanListForTable  + sigListForTable + bkgListForTable
    sampleList = scanListForTable  + bkgListForTable
    print sampleList
    

    setEventListToChains(samples,sampleList,presel)

    print "Getting Yields"
    cutName = "runI_%s"%htString
    runI.name = runI.name + "_" + htString
    yields[cutName]=Yields(samples, sampleList, runI, cutOpt= "list2" , weight="weight",pklOpt=True , tableName = "{cut}_%s%s"%(runtag,scantag),nDigits=2,err=True, verbose=True)
    #limits[cutName]=getLimit(yields[cutName])
    JinjaTexTable(yields[cutName],pdfDir=tableDir, caption="" )
    #getLimit(yields[cutName], cardBaseName = "" )
    #pl2 = plotLimits(limits)
    #pl2.Draw()


    #signalList = [s for s in sampleList if samples[s].isSignal ]
    if doscan:
        signalList=  scanListForTable

        limits = {}
        for sig in signalList:
            #limits[sig] = getLimit(yields[cutName], sig=sig , cardBaseName = "mass_scan_isr/isrrw")
            limits[sig] = getLimit(yields[cutName], sig=sig , outDir="./cards/13TeV/HT/IsrWeight_10000pbm1" , postix= htString +"_" + runtag + scantag)

####    #################a Remove below


        limit_vals={}
        for k in limits:
            mstop, mlsp = [int(x) for x in k[1:].rsplit("_")]
            if not limit_vals.has_key(mstop):
                limit_vals[mstop]={}
            if len(limits[k][1])>2:
                limit_vals[mstop][mlsp]=limits[k][1]['0.500']
            else: 
                limit_vals[mstop][mlsp]=999

        pl = makeStopLSPPlot(runtag, limit_vals, title="Exp. Limit", key=None)
        pl.Draw("COLZ TEXT")
        plot = pl
        plot.SetContour(2 )
        plot.SetContourLevel(0,0 )
        plot.SetContourLevel(1,1 )
        plot.SetContourLevel(2,10 )
        ROOT.gStyle.SetPaintTextFormat("0.02f")
        canv = ROOT.TCanvas("excpl","excpl",1920,1080)
        pl.Draw("COLZ TEXT")
        canv.SaveAs(saveDir+"/ExclPlot_%s_%s%s.png"%(htString, runtag,scantag))
