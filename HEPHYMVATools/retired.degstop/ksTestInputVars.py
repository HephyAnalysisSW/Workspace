import ROOT, os, sys
from Workspace.HEPHYPythonTools.nnAnalysisHelpers import getObjFromFile
from array import array
#ifile = "/data/schoef/MonoJetNNAnalysis/MVA_Analyzer/MonoJet_BDTvsMLP_RudiTest_stop300lsp270FastSim_sigScale100_softIsolatedMT_type1phiMet_deltaPhi.root"
for nj in range(1,5):
  ifile = "/data/schoef/MonoJetNNAnalysis/MVA_Analyzer/MonoJet_BDTvsMLP_reducedSigStat_stop300lsp270FastSim_convTest20_convImprove1e-7_W"+str(nj)+"JetsToLNu_softIsolatedMT_type1phiMet_deltaPhi.root"
  testTree = getObjFromFile(ifile, "TestTree")
  trainTree = getObjFromFile(ifile, "TrainTree")

  for v, binning in [ ("deltaPhi", (15,0,3.1415)), ('softIsolatedMT', (20,0,200)), ('type1phiMet', (20, 0, 1000))]:
    trainSigVals = [] 
    trainBkgVals = [] 
    for i in range(trainTree.GetEntries()):
      trainTree.GetEntry(i)
      type = trainTree.GetLeaf("classID").GetValue() 
      if type:
        trainSigVals.append(trainTree.GetLeaf(v).GetValue())
      else:
        trainBkgVals.append(trainTree.GetLeaf(v).GetValue())
    testSigVals = [] 
    testBkgVals = [] 
    for i in range(testTree.GetEntries()):
      testTree.GetEntry(i)
      type = testTree.GetLeaf("classID").GetValue() 
      if type:
        testSigVals.append(testTree.GetLeaf(v).GetValue())
      else:
        testBkgVals.append(testTree.GetLeaf(v).GetValue())

    resSig = ROOT.TMath.KolmogorovTest(len(testSigVals), array('d', testSigVals), len(trainSigVals), array('d', trainSigVals), "M")
    resBkg = ROOT.TMath.KolmogorovTest(len(testBkgVals), array('d', testBkgVals), len(trainBkgVals), array('d', trainBkgVals), "M")
    print "var:",v,"bkg",resBkg,"sig",resSig
    for classID in [0,1]:
      cut = "classID=="+str(classID)
      c1 = ROOT.TCanvas()
      trainTree.Draw(v+">>htrain("+",".join([str(x) for x in binning])+")", cut)
      htrain = ROOT.gDirectory.Get("htrain")
      testTree.Draw(v+">>htest("+",".join([str(x) for x in binning])+")", cut)
      htest = ROOT.gDirectory.Get("htest")
      htrain.Draw()
      c1.SetLogy()
      htest.SetLineColor(ROOT.kRed)
      htest.Draw("same")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngMJ/"+v+"_classID"+str(classID)+"W"+str(nj)+".png")
      del htest
      del htrain
