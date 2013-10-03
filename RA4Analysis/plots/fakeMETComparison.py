import ROOT
from simplePlotsCommon import *

htvals = [\
    [350,400,   "HLTHT300"],
    [400,450,   "HLTHT300"],
    [450,500,   "HLTHT350"],
    [500,550,   "HLTHT400"],
    [550,600,   "HLTHT450"],
    [600,650,   "HLTHT500"],
    [650,700,   "HLTHT550"],
    [700,750,   "HLTHT550"],
    [750,800,   "HLTHT650"],
    [800,1000,  "HLTHT650"],
    [1000,1200, "HLTHT750"],
    [1200,1500, "HLTHT750"],
    [1500,2500, "HLTHT750"]
  ]

if not globals().has_key("loadedNCP"):
  ROOT.gROOT.ProcessLine(".L ../../Scripts/aclic/useNiceColorPalette.C")
  ROOT.useNiceColorPalette(255)
  globals()["loadedNCP"] = True


htbins = [x[0] for x in htvals]+[htvals[-1][1]]
cut = "njets>=4&&((singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)||(singleElectronic&&nvetoMuons==0&&nvetoElectrons==1))"
prefix = "nj4"
shiftPar = {}

for sample in ["TTJets-PowHeg", "WJetsHT250"]:
  shiftPar[sample] = {}

  c = ROOT.TChain("Events")
  c.Add("/data/schoef/convertedTuples_v16/copyMET/Mu/"+sample+"/h*.root")
  c.Add("/data/schoef/convertedTuples_v16/copyMET/Ele/"+sample+"/h*.root")


  for metVar in ["rawMet", "met", "type1phiMet"]:
    c.Draw("acos( ( ("+metVar+"px-genmetpx)*genmetpx+("+metVar+"py-genmetpy)*genmetpy ) / ( sqrt(("+metVar+"px-genmetpx)**2+("+metVar+"py-genmetpy)**2)*genmet) ):genmet>>hTMP(33,150,975,20,0,3.14)", cut+"&&type1phiMet>150&ht>400", "COLZ")
    hTmp = ROOT.gDirectory.Get("hTMP")
    hTmp.GetYaxis().SetTitle("#Delta#phi(fake - #slash{E}_{T}, #slash{E}_{T})")
    hTmp.GetXaxis().SetTitle("gen. #slash{E}_{T}")
    c1 = ROOT.TCanvas()
    c1.SetLogz()
    hTmp.Draw("COLZ")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/fakeMetStudy/"+sample+"_"+metVar+".png")
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/fakeMetStudy/"+sample+"_"+metVar+".pdf")
    del c1
    del hTmp
    shiftPar[sample][metVar] = ROOT.TH1F('g', 'g', len(htbins)-1, array('d', htbins))
    for htval in htvals:
      c.Draw("( ("+metVar+"px-genmetpx)*genmetpx+("+metVar+"py-genmetpy)*genmetpy ) / genmet >> hgenMetProj(20,-120,120)",  cut+"&&type1phiMet>150&ht>"+str(htval[0])+"&&ht<"+str(htval[1]), "goff")
      hgenMetProj = ROOT.gDirectory.Get("hgenMetProj")
      hgenMetProj.GetXaxis().SetTitle("fake - #slash{E}_{par.}")
      c1 = ROOT.TCanvas()
      c1.SetLogz()
      ROOT.gStyle.SetOptStat()
      hgenMetProj.Draw()
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/fakeMetStudy/"+prefix+"_"+metVar+"_genMetProj_"+sample+"ht_"+str(htval[0])+"_"+str(htval[1])+".png")
      c1.Print("/afs/hephy.at/user/s/schoefbeck/www/fakeMetStudy/"+prefix+"_"+metVar+"_genMetProj_"+sample+"ht_"+str(htval[0])+"_"+str(htval[1])+".pdf")
      shiftPar[sample][metVar].SetBinContent(shiftPar[sample][metVar].FindBin(.5*(htval[0]+htval[1])), hgenMetProj.GetMean())
      shiftPar[sample][metVar].SetBinError(shiftPar[sample][metVar].FindBin(.5*(htval[0]+htval[1])),   hgenMetProj.GetMeanError())
      del c1
      del hgenMetProj

for sample in ["TTJets-PowHeg", "WJetsHT250"]:
  c1 = ROOT.TCanvas()
  ROOT.gStyle.SetOptStat(0)
  shiftPar[sample]["met"].GetYaxis().SetRangeUser(-10,28)
  shiftPar[sample]["met"].GetYaxis().SetTitle("mean of par. fake-#slash{E}_{T}")
  shiftPar[sample]["met"].GetXaxis().SetTitle("H_{T} (GeV)")
  shiftPar[sample]["met"].Draw()
  shiftPar[sample]["met"].Fit("pol1")
  shiftPar[sample]["type1phiMet"].GetYaxis().SetRangeUser(-10,28)
  shiftPar[sample]["type1phiMet"].GetYaxis().SetTitle("mean of par. fake-#slash{E}_{T}")
  shiftPar[sample]["type1phiMet"].GetXaxis().SetTitle("H_{T} (GeV)")
  shiftPar[sample]["type1phiMet"].SetLineColor(ROOT.kRed)
  shiftPar[sample]["type1phiMet"].SetMarkerColor(ROOT.kRed)
  shiftPar[sample]["type1phiMet"].Draw("same")
  shiftPar[sample]["type1phiMet"].Fit("pol1")
  shiftPar[sample]["rawMet"].SetLineColor(ROOT.kBlue)
  shiftPar[sample]["rawMet"].SetMarkerColor(ROOT.kBlue)
  shiftPar[sample]["rawMet"].Draw("same")
  l = ROOT.TLegend(0.2, 0.8, 0.6, 1.0)
  l.SetFillColor(0)
  l.SetShadowColor(ROOT.kWhite)
  l.SetBorderSize(1)
  l.AddEntry(shiftPar[sample]["met"], "type-I pf-MET")
  l.AddEntry(shiftPar[sample]["type1phiMet"], "type-I #phi pf-MET")
  l.AddEntry(shiftPar[sample]["rawMet"], "raw pf-MET")
  l.Draw()
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/fakeMetStudy/"+prefix+"_genMetProj_"+sample+"_shiftParams.png")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/fakeMetStudy/"+prefix+"_genMetProj_"+sample+"_shiftParams.pdf")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/fakeMetStudy/"+prefix+"_genMetProj_"+sample+"_shiftParams.root")
  del c1
