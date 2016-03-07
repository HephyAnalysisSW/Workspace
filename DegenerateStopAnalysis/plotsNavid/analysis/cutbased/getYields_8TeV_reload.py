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






saveDir = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload/%s/'%htString
tableDir=saveDir+"/Tables/"


try:
    samples
except NameError:
    samples = getSamples(wtau=True,sampleList=sampleList,useHT=useHT,skim='presel')




cutInsts= {
            "runI"      :   {"cut":runI      ,  "opt":"list"},
          }


cutInst = cutInsts[cutInstStr]['cut']
cutOpt = cutInsts[cutInstStr]['opt']




if cutInst:
        setEventListToChains(samples,sampleList,presel)




calcTrkCutLimit = process
if calcTrkCutLimit:



    limits={}
    yields={}

    print sampleList 



    cutName = "runI_%s"%htString
    runI.name = runI.name + "_" + htString
    yields[cutName]=Yields(samples, sampleList, runI, cutOpt= "list2" , weight="weight",pklOpt=True,nDigits=2,err=True)
    limits[cutName]=getLimit(yields[cutName])
    JinjaTexTable(yields[cutName],pdfDir=tableDir, caption="" )

    pl2 = plotLimits(limits)
    pl2.Draw()




####################### Remove below


  

