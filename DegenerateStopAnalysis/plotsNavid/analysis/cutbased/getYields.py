
import sys

#oldargv = sys.argv[ : ]
#sys.argv = [ '-b-' ]
#import ROOT
#ROOT.gROOT.SetBatch(True)
#sys.argv = oldargv

#from Workspace.DegenerateStopAnalysis.cuts import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_mAODv2_7412pass2 import getSamples

from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import *
from Workspace.DegenerateStopAnalysis.navidTools.makeTable import *
from Workspace.DegenerateStopAnalysis.navidTools.limitCalc import  getLimit, plotLimits

from Workspace.DegenerateStopAnalysis.cuts.newSR import *
from Workspace.DegenerateStopAnalysis.cuts.dmt import *
from Workspace.DegenerateStopAnalysis.cuts.tracks import *

print sys.argv
parser = ArgParser()
args=parser.parse(sys.argv)
sampleList= args.sampleList

cutInstStr = args.cutInst
process = args.process
useHT   = args.useHT
print args, sampleList ,  process
htString = "HT" if useHT else "Inc"




saveDir = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/cutbased/%s/Yields/'%htString


try:
    samples
except NameError:
    samples = getSamples(wtau=True,sampleList=sampleList,useHT=useHT,skim='presel')




cutInsts= {
            "presel"    :   {"cut":presel      ,  "opt":"flow"},
            "sr1abc"    :   {"cut":sr1abc      ,  "opt":"list"},
            "sr1"       :   {"cut":sr1      ,  "opt":"flow"},
            "sr1Loose"  :   {"cut":sr1Loose    ,  "opt":"flow"}, 
            "sr1LooseFull"  :   {"cut":sr1Loose  ,  "opt":"fullFlow"},
            "BM1"       :   {"cut":dmt.dmtBM1     ,  "opt":"list"},


            "sr2"       :   {"cut":sr2      ,  "opt":"flow"},

            #"R1"        :   {"cut":dmt.dmtR1   ,  "opt","flow"},
            #"R2"        :   {"cut":dmt.dmtR2   ,  "opt","flow"},
            #"R3"        :   {"cut":dmt.dmtR3   ,  "opt","flow"},
            #"Rej"       :   {"cut":dmt.dmtRej  ,  "opt","flow"},
          }

#cutInst = cutInsts[cutInstStr]

cutInst = cutInsts[cutInstStr]['cut']
cutOpt = cutInsts[cutInstStr]['opt']


if cutInst:
        setEventListToChains(samples,sampleList,cutInst)


tableDir=saveDir+"/Tables/"


if False:
    yields={}
    for cut_name in cutInsts:
        cut = cutInsts[cut_name]
        if cut['cut'].baseCut:
            setEventListToChains(samples,sampleList,cut['cut'].baseCut)
        yields[cut_name]=Yields(samples, sampleList, cut['cut'] , cutOpt= cut['opt'], weight="weight",pklOpt=False,nDigits=2,err=True)
        JinjaTexTable(yields[cut_name],pdfDir=tableDir, caption="" )
        



calcTrkCutLimit = process
if calcTrkCutLimit:
    trkMultipCuts = tracks.makeTrkCuts( tracks.trk, 13 , baseCut=sr1Loose, cutName="nTracks")
    
    limits={}
    yields={}


    trkCuts={}
    for trkCut in trkMultipCuts:
        trkCuts[trkCut]=splitCutInPt(trkMultipCuts[trkCut])

    print sampleList 
    for trkCut in trkCuts:
        
        yields[trkCut]=Yields(samples, sampleList, trkCuts[trkCut], cutOpt= "list2" , weight="weight",pklOpt=True,nDigits=2,err=True)
        limits[trkCut]=getLimit(yields[trkCut])
    pl = plotLimits(limits)
    pl.Draw()

    sr1abcPt = splitCutInPt(sr1abc)

    yields['dmtTrkPt']=Yields(samples, sampleList, dmtTrkPt, cutOpt= "list2" , weight="weight",pklOpt=True,nDigits=2,err=True)
    limits['dmtTrkPt']=getLimit(yields['dmtTrkPt'])
    yields['dmtTrk']=Yields(samples, sampleList, dmtTrk, cutOpt= "list2" , weight="weight",pklOpt=True,nDigits=2,err=True)
    limits['dmtTrk']=getLimit(yields['dmtTrk'])
    yields['sr1abcPt']=Yields(samples, sampleList, sr1abcPt, cutOpt= "list2" , weight="weight",pklOpt=True,nDigits=2,err=True)
    limits['sr1abcPt']=getLimit(yields['sr1abcPt'])
    yields['sr1abc']=Yields(samples, sampleList, sr1abc, cutOpt= "list2" , weight="weight",pklOpt=True,nDigits=2,err=True)
    limits['sr1abc']=getLimit(yields['sr1abc'])

    for cut in ['dmtTrkPt','dmtTrk','sr1abcPt','sr1abc']:
        JinjaTexTable(yields[cut],pdfDir=tableDir, caption="" )

    pl2 = plotLimits(limits)
    pl2.Draw()

    for nTrk in dmtTrkCuts:
        yields[nTrk]=Yields(samples, sampleList, dmtTrkCuts[nTrk], cutOpt= "list2" , weight="weight", pklOpt=True,nDigits=2,err=True)
        limits[nTrk]=getLimit(yields[nTrk])
        JinjaTexTable(yields[nTrk],pdfDir=tableDir)
 
    for nTrk in dmtTrkCutsPt:
        yields[nTrk]=Yields(samples, sampleList, dmtTrkCutsPt[nTrk], cutOpt= "list2" , weight="weight", pklOpt=True,nDigits=2,err=True)
        limits[nTrk]=getLimit(yields[nTrk])
        JinjaTexTable(yields[nTrk],pdfDir=saveDir)

####################### Remove below


  

