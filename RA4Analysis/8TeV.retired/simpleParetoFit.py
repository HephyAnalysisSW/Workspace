import ROOT
c = ROOT.TChain("Events")
mode = "EleMu"
c.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/TTJets-PowHeg/histo_TTJets-PowHeg.root")
c.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/TTJets-PowHeg/histo_TTJets-PowHeg.root")
#c.Add("/data/schoef/convertedTuples_v16/copyMET/"+mode+"/single"+mode+"Data/histo_single"+mode+"Data.root")
#c.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/singleMuData/histo_singleMuData.root")
#c.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/singleEleData/histo_singleEleData.root")
#c.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/TTJets-PowHeg/histo_TTJets-PowHeg.root")

metvar = "met"

ROOT.TH1F().SetDefaultSumw2()
ROOT.gStyle.SetOptFit(1)

for lowR in [150,175,200]:
  for njcut, name in  [ \
      ["njets>=4", "nj-gr-4"],
      ["njets>=3", "nj-gr-3"],
      ["njets>=6", "nj-gr-6"],
      ["njets==3", "nj3"],
      ["njets==4", "nj4"],
      ["njets==5", "nj5"]]:
      
#    c.Draw(metvar+">>hnj(60,0,1500)", "weight*("+njcut+"&&leptonPt>30&&nbtags>=2&&"+metvar+">150&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoElectrons==1&&nvetoMuons==0))")
    c.Draw(metvar+">>hnj(30,0,1500)", "weight*("+njcut+"&&nbtags>=2&&"+metvar+">150&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoElectrons==1&&nvetoMuons==0))")
    hnj = ROOT.gDirectory.Get("hnj")

    fitRange = [lowR, 1500]
    func = ROOT.TF1("pareto", "[0]*TMath::Power( 1.+[2]*(x-150.)/[1], -1.-1./[2])/[1]", *fitRange)
    func.SetParameter(0, 1000000)
    func.SetParameter(1, 25) 
    func.SetParameter(2, 0.1)
    func.SetParLimits(2, 0.002, 0.9)
    c1 = ROOT.TCanvas()
    c1.SetLogy()
    hnj.GetYaxis().SetRangeUser(10**(-3.5), 3*hnj.GetMaximum())
    hnj.Draw("e")
    hnj.Fit(func, "s","s", *fitRange)
    func.Draw("sames")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/TTJets_"+mode+"_bt2_"+njcut+"_fr_"+str(fitRange[0])+"_"+str(fitRange[1])+".png")
