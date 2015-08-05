import ROOT
from getSamples import *
from cutLists import *
from Workspace.DegenerateStopAnalysis.navidPlotTools import getPlots, getYieldTable, drawPlots,cutClass, makeTableFromYieldDict

saveDir = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/"
tableDir=saveDir+"/table"


lumiConvertFactor = 20000./3000.
for sample in sampleDict:
  if sampleDict[sample].has_key("weight"):
    sampleDict[sample]["weight"] = str(sampleDict[sample]["weight"])+"*%s"%lumiConvertFactor
  else:
    sampleDict[sample]["weight"] = "weight*%s"%lumiConvertFactor




#minAng = lambda x: minAngleString("Jet_phi[0]","Jet_phi[%s]"%x)
#sampleDict['T2Deg300_270']['tree'].Scan("Jet_phi:%s:%s"%(minAng("1"),minAng("")), "(Sum$(Jet_pt>=60) >=1 ) && (TMath::Min( (2*pi) - abs(Jet_phi[0]-Jet_phi[]) , abs(Jet_phi[0]-Jet_phi[]) )<2.5)" )

#lumiConvertFactor = 20000./4000
#for sample in sampleDict:
#  if sampleDict[sample].has_key("weight"):
#    sampleDict[sample]["weight"] = str(sampleDict[sample]["weight"])+"*%s"%lumiConvertFactor
#  else:
#    sampleDict[sample]["weight"] = "weight*%s"%lumiConvertFactor

#c=sampleDict['T2Deg300_270']['tree']
#sampleDict['T2Deg300_270_RunII']['tree'].Scan("nJet:abs(Jet_phi[0]-Jet_phi[1])","nJet==1 || (nJet==2 )","COLZ")
#sampleDict['T2Deg300_270_RunII']['tree'].Scan("nJet:abs(Jet_phi[0]-Jet_phi[1])","nJet==1 || (nJet==2 && (nJet==2 && abs(Jet_phi[1]-Jet_phi[0])) )","COLZ")
#
#sampleDict['T4Deg300_270_RunII']['tree'].Draw("nJet:abs(Jet_phi[0]-Jet_phi[1])>>(8,0,2*pi,5,0,5)","nJet==1 || (nJet==2)","COLZ") 
def getSyncTable(cutList = sr1sync.list,output= "sr1sync" ):
  syncYields=getYieldTable(sampleDict,  cutList , treeList="", orderedKeys=["TTJets", "WJets", "bkg", "T2Deg300_270","T2Deg300_270_RunII", "T2Deg350_330",  "fom_T2Deg300_270_RunII"  ], output=output ,saveDir=tableDir)
  #getYieldTable(sampleDict,  sr1sync.list , treeList="", bkgs=["TTJets", "WJets"],sigs=["T2Deg350_330","T2Deg300_270", "T2Deg300_270_RunII"], output= "sync_antiQCDfix" ,saveDir=tableDir) 
  return syncYields



