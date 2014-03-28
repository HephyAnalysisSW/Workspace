import ROOT
#c = ROOT.TChain("MonteCarlo")
#c.Add("/data/schoef/MonoJetNNAnalysis/datasets/MonoJet_BDTvsMLP_stop300lsp270FastSim_refsel_None_softIsolatedMT_type1phiMet_deltaPhi_isrJetPt_htRatio.root")
#c.SetScanField(10**7)
#
#c.Scan("type:weight:weightForMVA:type1phiMet:softIsolatedMuPt:isrJetPt:softIsolatedMT:deltaPhi:htRatio:softIsolatedMuCharge", "","@colsize=20")

import ROOT, os, sys
path = os.path.abspath('../../HEPHYCommonTools/mva')
if not path in sys.path:
    sys.path.insert(1, path)
from Workspace.HEPHYCommonTools.nnAnalysisHelpers import getObjFromFile
from array import array

if len(sys.argv)>2:
  ifile = sys.argv[2] 

if len(sys.argv)>1:
  if sys.argv[1].lower()=="test":
    tree = getObjFromFile(ifile, "TestTree")
  if sys.argv[1].lower()=="train":
    tree = getObjFromFile(ifile, "TrainTree")

  tree.SetScanField(10**7)
  tree.Scan("classID:weight:type1phiMet:softIsolatedMT:deltaPhi:MLP33_nCyc500", "","@colsize=20")

