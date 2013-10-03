import ROOT
from simplePlotsCommon import *

c = ROOT.TChain("Events")
c.Add("/data/schoef/convertedTuples_v12/copyMET/Mu/data/histo_data.root")
c.Add("/data/schoef/convertedTuples_v12/copyMET/Ele/data/histo_data.root")
d = ROOT.TChain("Events")
d.Add("/data/schoef/convertedTuples_v13/copyMET/Mu/data/histo_data.root")
d.Add("/data/schoef/convertedTuples_v13/copyMET/Ele/data/histo_data.root")

var = "met"
c.Draw(var+">>hOld(100,0,2000)", "(singleMuonic||singleElectronic)&&run<203002")
d.Draw(var+">>hNew(100,0,2000)", "(singleMuonic||singleElectronic)&&run<203002")
#var = "njets"
#c.Draw("njets>>hOld(30,0,30)", "ht>400&&met>150&&(singleMuonic||singleElectronic)&&run<203002")
#d.Draw("njets>>hNew(30,0,30)", "ht>400&&met>150&&(singleMuonic||singleElectronic)&&run<203002")

hOld = ROOT.gDirectory.Get("hOld")
hNew = ROOT.gDirectory.Get("hNew")

hOld.SetLineColor(ROOT.kBlue)
hOld.SetMarkerStyle(0)
hNew.SetMarkerStyle(0)

c1 = ROOT.TCanvas()
c1.SetLogy()
l = ROOT.TLegend(0.6,0.7,1.0,1.0)
l.AddEntry(hOld, "Oct. recipe")
l.AddEntry(hNew, "Dec. recipe")
hOld.GetYaxis().SetRangeUser(0.1, 10**0.7*hOld.GetMaximum())
hOld.Draw()
hNew.Draw("same")
l.Draw()
c1.Print("/afs/hephy.at/user/s/schoefbeck/www/noiseStudy/"+var+".png")
