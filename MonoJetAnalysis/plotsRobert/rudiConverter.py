import ROOT

c = ROOT.TChain("MonteCarlo")
c.Add("/data/schoef/MonoJetNNAnalysis/datasets/MonoJet_BDTvsMLP_stop300lsp270FastSim_refsel_None_softIsolatedMT_type1phiMet_deltaPhi_isrJetPt_htRatio.root")
c.SetScanField(10**7)

c.Scan("type:weight:weightForMVA:type1phiMet:softIsolatedMuPt:isrJetPt:softIsolatedMT:deltaPhi:htRatio:softIsolatedMuCharge", "","@colsize=20")
