t = ROOT.TChain("Events")
t.Add("T2DegStop_300_270_0.root")

t.Draw("LepGood_pt","","")
