import ROOT
import pickle
from localConfig import afsUser, nfsUser, localPlotDir
from array import array
import os, sys

for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/mva', 'HEPHYCommonTools/cardFileWriter/', '../../HEPHYCommonTools/python', '../python', '../../HEPHYCommonTools/cardFileWriter']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from nnAnalysisHelpers import getEList, constructDataset, getYield, fillNNHisto, getObjFromFile, getVarValList, getPlot
from xsec import xsec
from xsecSMS import gluino8TeV_NLONLL, gluino14TeV_NLO
import copy, sys
from monoJetFuncs import softIsolatedMT
from cardFileWriter import cardFileWriter
from helpers import KolmogorovProbability, KolmogorovDistance
#RA4

#prefix =  /data/schoef/MonoJetNNAnalysis/MVA_Analyzer/MonoJet_stop300lsp270FastSim_BkgMix_0_nTrees400_nCuts_-1_maxDepthComparison_softIsolatedMT_type1phiMet_deltaPhi.root 

ksProbSigMine = ROOT.TH1F('ksProbSigTestMine', 'ksProbSigTest', 100, 0, 1)
ksProbBkgMine = ROOT.TH1F('ksProbBkgTestMine', 'ksProbBkgTest', 100, 0, 1)
ksProbSigTH1  = ROOT.TH1F('ksProbSigTestTH1', 'ksProbSigTest',  100, 0, 1)
ksProbBkgTH1  = ROOT.TH1F('ksProbBkgTestTH1', 'ksProbBkgTest',  100, 0, 1)
ksProbSigTH1X = ROOT.TH1F('ksProbSigTestTH1X', 'ksProbSigTest', 100, 0, 1)
ksProbBkgTH1X = ROOT.TH1F('ksProbBkgTestTH1X', 'ksProbBkgTest', 100, 0, 1)

for i in range(1):
#  prefix =  "MonoJet_stop300lsp270FastSim_BkgMix_"+str(i)+"_nTrees400_nCuts_-1_maxDepthComparison_softIsolatedMT_type1phiMet_deltaPhi"
#  prefix =  "MonoJet_stop300lsp270FastSim_BkgMix_"+str(i)+"_nTrees400_nCuts_-1_maxDepthComparison_softIsolatedMT_type1phiMet"
  prefix =  "MonoJet_stopDeltaM30FastSim_BkgMix_"+str(i)+"_nTrees400_nCuts_-1_maxDepthComparison_softIsolatedMT_type1phiMet"

  setup=pickle.load(file('/data/'+nfsUser+'/MonoJetNNAnalysis/MVA_Analyzer/'+prefix+'.pkl'))

  reader = ROOT.TMVA.Reader()  
  for var in setup['mvaInputVars']:
    var_i  = array('f',[0])
  #  vars[var] = var_i
    reader.AddVariable(var,var_i)

  allMethods = {}
  for m in setup['methodConfigs']:
    if m['type']!=ROOT.TMVA.Types.kCuts: 
      allMethods[m['name']] = {'reader':reader.BookMVA(m['name'],setup['weightDir']+'/TMVAClassification_'+m['name']+'.weights.xml'), 'config':m}
    else:
      allMethods[m['name']] = {'reader':reader.BookMVA(m['name'],setup['weightDir']+'/TMVAClassification_'+m['name']+'.weights.xml'), 'config':m}
  for mD in [1,2,3,4,10]:
    trainTree = getObjFromFile(setup['TMVAOutputFile'], 'TrainTree')
    varListBkgTrain = getVarValList(trainTree, 'BDT_maxDepth'+str(mD), "classID==0")
    varListSigTrain = getVarValList(trainTree, 'BDT_maxDepth'+str(mD), "classID==1")

    testTree = getObjFromFile(setup['TMVAOutputFile'], 'TestTree')
    varListBkgTest = getVarValList(testTree, 'BDT_maxDepth'+str(mD), "classID==0")
    varListSigTest = getVarValList(testTree, 'BDT_maxDepth'+str(mD), "classID==1")


    #Binned version
    plotBkgTest = getPlot(testTree,"classID==0", 'BDT_maxDepth'+str(mD))
    plotSigTest = getPlot(testTree,"classID==1", 'BDT_maxDepth'+str(mD))
    plotBkgTrain = getPlot(trainTree,"classID==0", 'BDT_maxDepth'+str(mD))
    plotSigTrain = getPlot(trainTree,"classID==1", 'BDT_maxDepth'+str(mD))
    print "maxDepth",mD,"test/train",len(varListBkgTest),len(varListBkgTrain),"unbinned, Bkg", KolmogorovProbability(varListBkgTrain, varListBkgTest), 'binned', plotBkgTest.KolmogorovTest(plotBkgTrain),"X", plotBkgTest.KolmogorovTest(plotBkgTrain, "X") 
    print "maxDepth",mD,"test/train",len(varListSigTest),len(varListSigTrain),"unbinned, Sig", KolmogorovProbability(varListSigTrain, varListSigTest), 'binned', plotSigTest.KolmogorovTest(plotSigTrain),"X", plotSigTest.KolmogorovTest(plotSigTrain, "X")
    if mD==1:
      ksProbBkgMine.Fill( KolmogorovProbability(varListBkgTrain, varListBkgTest) )
      ksProbSigMine.Fill( KolmogorovProbability(varListSigTrain, varListSigTest) )
      ksProbBkgTH1 .Fill(plotBkgTest.KolmogorovTest(plotBkgTrain)) 
      ksProbSigTH1 .Fill(plotSigTest.KolmogorovTest(plotSigTrain))
      ksProbBkgTH1X.Fill(plotBkgTest.KolmogorovTest(plotBkgTrain, "X"))
      ksProbSigTH1X.Fill(plotSigTest.KolmogorovTest(plotSigTrain, "X"))

c1=ROOT.TCanvas()
ksProbSigMine.SetLineColor(ROOT.kRed)
ksProbBkgMine.Draw()
ksProbSigMine.Draw("same")
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMJ/KSTest_maxDepthComparison_mD1_Mine.png')
ksProbSigTH1.SetLineColor(ROOT.kRed)
ksProbBkgTH1.Draw()
ksProbSigTH1.Draw("same")
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMJ/KSTest_maxDepthComparison_mD1_TH1.png')
ksProbSigTH1X.SetLineColor(ROOT.kRed)
ksProbBkgTH1X.Draw()
ksProbSigTH1X.Draw("same")
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMJ/KSTest_maxDepthComparison_mD1_TH1X.png')
