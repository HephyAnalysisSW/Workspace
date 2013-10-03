import ROOT

#d = ROOT.TChain("Events")
#c = ROOT.TChain("Events")
#d.Add("/data/mhickel/pat_121211/8TeV-TTJets-powheg-v1+2/h*.root")
#c.Add("/data/mhickel/pat_121211/8TeV-WJets-HT400/histo_*.root")

#hOrth  =  "abs(jet0pt*(- sin(jet0phi)*genmetpx + cos(jet0phi)*genmetpy)/genmet)"
#hOrth += "+abs(jet1pt*(- sin(jet1phi)*genmetpx + cos(jet1phi)*genmetpy)/genmet)"
#hOrth += "+abs(jet2pt*(- sin(jet2phi)*genmetpx + cos(jet2phi)*genmetpy)/genmet)"
#hOrth += "+abs(jet3pt*(- sin(jet3phi)*genmetpx + cos(jet3phi)*genmetpy)/genmet)"
#
#hPar  =  "abs(jet0pt*(cos(jet0phi)*genmetpx + sin(jet0phi)*genmetpy)/genmet)"
#hPar += "+abs(jet1pt*(cos(jet1phi)*genmetpx + sin(jet1phi)*genmetpy)/genmet)"
#hPar += "+abs(jet2pt*(cos(jet2phi)*genmetpx + sin(jet2phi)*genmetpy)/genmet)"
#hPar += "+abs(jet3pt*(cos(jet3phi)*genmetpx + sin(jet3phi)*genmetpy)/genmet)"
#
#
#c.Draw(hOrth+">>histOrthW(50,0,1000)", "genmet>150&&(ht>450&&ht<500&&njets==4&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))")
#d.Draw(hOrth+">>histOrthT(50,0,1000)", "genmet>150&&(ht>450&&ht<500&&njets==4&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))")
#c.Draw(hPar+" >>histParW(50,0,1000)",  "genmet>150&&(ht>450&&ht<500&&njets==4&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))")
#d.Draw(hPar+" >>histParT(50,0,1000)",  "genmet>150&&(ht>450&&ht<500&&njets==4&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))")
#histOrthW = ROOT.gDirectory.Get("histOrthW")
#histOrthT = ROOT.gDirectory.Get("histOrthT")
#histParW = ROOT.gDirectory.Get("histParW")
#histParT = ROOT.gDirectory.Get("histParT")
#
#histOrthW.Scale(ROOT.histOrthT.Integral()/ROOT.histOrthW.Integral())
#histOrthW.SetLineColor(ROOT.kRed)
#c1 = ROOT.TCanvas()
#c1.SetLogy()
#histOrthW.Draw()
#histOrthT.Draw("same")
#c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/hOrth.png")
#del c1
#
#histParW.Scale(ROOT.histParT.Integral()/ROOT.histParW.Integral())
#histParW.SetLineColor(ROOT.kRed)
#c1 = ROOT.TCanvas()
#c1.SetLogy()
#histParW.Draw()
#histParT.Draw("same")
#c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/hPar.png")
#del c1
##del histOrthW, histOrthT, histParW, histParT

#c.Draw("(cos(jet0phi)*genmetpx + sin(jet0phi)*genmetpy)/genmet>>h_DP3_W(20,-1,1)", "leptonEta<1.0&&(ht>450&&njets==4&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))")
#d.Draw("(cos(jet0phi)*genmetpx + sin(jet0phi)*genmetpy)/genmet>>h_DP3_T(20,-1,1)", "leptonEta<1.0&&(ht>450&&njets==4&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))")

c = ROOT.TChain("Events")
c.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/WJetsHT250/h*.root")
c.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/WJetsHT250/h*.root")
d = ROOT.TChain("Events")
d.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/TTJets-PowHeg/h*.root")
d.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/TTJets-PowHeg/h*.root")

w = {}
t = {}
c1 = ROOT.TCanvas()
for i in range(4):
  w[i] = {}
  t[i] = {}
  for j in range(i):
    var = "jet"+str(i)+"pt/jet"+str(j)+"pt"
    cut = "weight*(njets>=4&&genmet>150&& (singleMuonic&&nvetoMuons==1&&nvetoElectrons==0||singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))&&0<"+var
    print i,j, var, cut
    hname = "hn_"+str(i)+"_over_"+str(j)
    w[i][j] = ROOT.TProfile("WJetsHT250_"+hname, "WJetsHT250_"+hname, 14, 300, 1000) 
    w[i][j].GetYaxis().SetRangeUser(0,1)
    w[i][j].SetLineColor(ROOT.kRed)
    t[i][j] = ROOT.TProfile("TTJetsPowHeg_"+hname, "TTJetsPowHeg_"+hname, 14, 300, 1000) 
    t[i][j].GetYaxis().SetRangeUser(0,1)
    c.Draw(var+":ht>>WJetsHT250_"+hname, cut)
    d.Draw(var+":ht>>TTJetsPowHeg_"+hname, cut)
    hw = ROOT.gDirectory.Get("WJetsHT250_"+hname).Clone()
    ht = ROOT.gDirectory.Get("TTJetsPowHeg_"+hname).Clone()
    hw.Draw()
    ht.Draw("same")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/erf/"+hname+".png")
    del hw, ht 
