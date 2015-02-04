import ROOT
cMC = ROOT.TChain("Events")
cMC.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/TTJets-PowHeg/*.root")
cData = ROOT.TChain("Events")
cData.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/data/*.root")
cData.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/data/*.root")

c1 = ROOT.TCanvas()
c1.SetLogy()
commoncf = "met>150&&ht>1000&&jet3pt>40&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)"
commoncf = "met>150&&ht>1000&&jet3pt>40&&(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)"
cMC.Draw("met>>hMC(101,0,1010)",commoncf) 
cData.Draw("met>>hData(101,0,1010)",commoncf,"same") 
hMC = ROOT.gDirectory.Get("hMC")
hData = ROOT.gDirectory.Get("hData")

hMC.Scale(hData.Integral(20,-1)/hMC.Integral(20,-1))
hMC.SetLineColor(ROOT.kRed)
hData.Draw()
hMC.Draw("same")

c.Draw("sqrt( (metpx+leptonPt*cos(leptonPhi))**2 + (metpy+leptonPt*sin(leptonPhi))**2):mT", "njets>=4&&(singleMuonic||singleElectronic)", "COLZ")
