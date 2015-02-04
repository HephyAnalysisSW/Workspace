import ROOT

if not globals().has_key("loadedNCP"):
  ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")
  ROOT.useNiceColorPalette(255)
  globals()["loadedNCP"] = True



cMC = ROOT.TChain("Events")
cMC.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/TTJets-PowHeg/*.root")
cMC.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/WJetsHT250/*.root")
cMC.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/TTJets-PowHeg/*.root")
cMC.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/WJetsHT250/*.root")

cSig = ROOT.TChain("Events")
cSig.Add("/data/adamwo/convertedTuples_v15/copyMET/Mu/T1tttt_1000_100/h*.root")
cSig.Add("/data/adamwo/convertedTuples_v15/copyMET/Ele/T1tttt_1000_100/h*.root")


commoncf = "(met>200&&ht>400&&njets>=6&&((singleElectronic&&nvetoMuons==0&&nvetoElectrons==1)||(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)))"


c1 = ROOT.TCanvas()
ROOT.gStyle.SetOptStat(0)
for prefix, cut in [["met200-ht400-njets6", commoncf ]]:
  c1.SetLogz()
  c1.SetLogx(0)
  c1.SetLogy(0)
  
  varString = "sqrt( (metpx+leptonPt*cos(leptonPhi))**2 + (metpy+leptonPt*sin(leptonPhi))**2):mT"
  cMC.Draw(varString+">>hMC(30,0,900,30,0,900)", "weight*("+cut+")", "COLZ")
  hMC = ROOT.gDirectory.Get("hMC")
  hMC.GetZaxis().SetRangeUser(0.07, 10**3)
  hMC.GetXaxis().SetTitle("m_{T} (GeV)")
  hMC.GetYaxis().SetTitle("p_{T,W} (GeV)")
  hMC.SetTitle("")
  hMC.Draw("COLZ")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/MT/"+prefix+"_Bkg_ptW_vs_MT.png")   
  del hMC

  cSig.Draw(varString+">>hSig(30,0,900,30,0,1000)", "weight*("+cut+")", "COLZ")
  hSig = ROOT.gDirectory.Get("hSig")
  hSig.GetZaxis().SetRangeUser(0.07, 10**3)
  hSig.GetXaxis().SetTitle("m_{T} (GeV)")
  hSig.GetYaxis().SetTitle("p_{T,W} (GeV)")
  hSig.SetTitle("")
  hSig.Draw("COLZ")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/MT/"+prefix+"_Sig_ptW_vs_MT.png")   
  del hSig

  varString = "ht:mT"
  cMC.Draw(varString+">>hMC(30,0,900,30,0,1800)", "weight*("+cut+")", "COLZ")
  hMC = ROOT.gDirectory.Get("hMC")
  hMC.GetZaxis().SetRangeUser(0.07, 10**3)
  hMC.GetXaxis().SetTitle("m_{T} (GeV)")
  hMC.GetYaxis().SetTitle("H_{T} (GeV)")
  hMC.SetTitle("")
  hMC.Draw("COLZ")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/MT/"+prefix+"_Bkg_HT_vs_MT.png")   
  del hMC

  cSig.Draw(varString+">>hSig(30,0,900,30,0,1800)", "weight*("+cut+")", "COLZ")
  hSig = ROOT.gDirectory.Get("hSig")
  hSig.GetZaxis().SetRangeUser(0.07, 10**3)
  hSig.GetXaxis().SetTitle("m_{T} (GeV)")
  hSig.GetYaxis().SetTitle("H_{T} (GeV)")
  hSig.SetTitle("")
  hSig.Draw("COLZ")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/MT/"+prefix+"_Sig_HT_vs_MT.png")   
  del hSig

  for var, varname, binning in [["sqrt( (metpx+leptonPt*cos(leptonPhi))**2 + (metpy+leptonPt*sin(leptonPhi))**2)", "ptW", [30,0,900]],\
                             ["njets", "njets", [10,4,14]], ["ht", "ht", [30,0,1800]], ["met", "met", [30,0,900]], ["mT", "mT",  [30,0,900]] ]:

    cMC.Draw(var+">>hMC("+str(binning[0])+","+str(binning[1])+","+str(binning[2])+")", "weight*("+cut+")")
    hMC = ROOT.gDirectory.Get("hMC")
    cSig.Draw(var+">>hSig("+str(binning[0])+","+str(binning[1])+","+str(binning[2])+")", "weight*("+cut+")")
    hSig = ROOT.gDirectory.Get("hSig")
    hSig.SetLineColor(ROOT.kRed)
    c1.SetLogx(0)
    c1.SetLogy()
    hMC.Draw()
    hMC.GetXaxis().SetTitle(varname)
    hMC.GetYaxis().SetRangeUser(0.7, 3*max(hMC.GetMaximum(), hSig.GetMaximum()))
    hSig.Draw("same")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/MT/"+prefix+"_"+varname+".png")
    del hMC
    del hSig
  
#cSig.Draw(varString+">>hSig", commoncf, "COLZ")
#hSig = ROOT.gDirectory.Get("hSig")
#
#hMC.Draw("same")
#
#

