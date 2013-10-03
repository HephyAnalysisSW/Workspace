import ROOT
from simplePlotsCommon import *

small = False

c = ROOT.TChain("Events")
if small:
  c.Add("/data/mhickel/pat_121211/8TeV-TTJets-powheg-v1+2/histo_10_*.root")
  c.Add("/data/mhickel/pat_121211/8TeV-TTJets-powheg-v1+2/histo_20_*.root")
  c.Add("/data/mhickel/pat_121211/8TeV-TTJets-powheg-v1+2/histo_30_*.root")
else:
  c.Add("/data/mhickel/pat_121211/8TeV-TTJets-powheg-v1+2/histo_*.root")

prefix = "met-150"

htcVals = [500, 750, 1000]
hISR = {}
hNJets = {}
hNbtags = {}
for htc in htcVals:
  print "At", htc
  c.Draw("sqrt((top0Px + top1Px) **2 + (top0Py + top1Py) **2)>>hISR"+str(htc)+"(15, 0, 1500)", "ht>"+str(htc)+"&&type1phiMet>50&&type1phiMet>150&&leptonPt>30&&(singleMuonic||singleElectronic)", "goff")
  c.Draw("njets>>hnjets"+str(htc)+"(15, 0, 15)", "ht>"+str(htc)+"&&type1phiMet>100&&type1phiMet>150&&leptonPt>30&&(singleMuonic||singleElectronic)", "goff")
  c.Draw("nbtags>>hnbtags"+str(htc)+"(7, 0, 7)", "ht>"+str(htc)+"&&type1phiMet>100&&type1phiMet>150&&leptonPt>30&&(singleMuonic||singleElectronic)", "goff")
  hISR[htc] = ROOT.gDirectory.Get("hISR"+str(htc)).Clone()
  hISR[htc].GetXaxis().SetTitle("p_{T} of ttbar system")
  hISR[htc].GetYaxis().SetTitle("Number of Events / 100 GeV")
  hNJets[htc] = ROOT.gDirectory.Get("hnjets"+str(htc)).Clone()
  hNJets[htc].GetXaxis().SetTitle("jet multiplicity")
  hNJets[htc].GetYaxis().SetTitle("Number of Events")
  hNbtags[htc] = ROOT.gDirectory.Get("hnbtags"+str(htc)).Clone()
  hNbtags[htc].GetXaxis().SetTitle("b-jet multiplicity")
  hNbtags[htc].GetYaxis().SetTitle("Number of Events")

colors = {500:ROOT.kBlue, 750:ROOT.kRed, 1000:ROOT.kGreen}

for name, plot in [["njets", hNJets], ["isr", hISR], ["btags", hNbtags]]:
  l = ROOT.TLegend(0.61,0.95 - 0.08*5,.95,.95)
  l.SetFillColor(0)
  l.SetShadowColor(ROOT.kWhite)
  l.SetBorderSize(1)
  c1 = ROOT.TCanvas()
  c1.SetLogy()
  for htc in htcVals:
    plot[htc].SetLineColor(colors[htc])
    plot[htc].SetMarkerColor(colors[htc])
    plot[htc].SetMarkerSize(0)
    if htc == htcVals[0]:
      plot[htc].SetTitle("")
      plot[htc].Draw()
    else:
      plot[htc].Draw("same")
    l.AddEntry(plot[htc], "H_{T} #geq "+str(htc))
  l.Draw()
  if not small:
    c1.Print("/afs/hephy.at/user/s/schoefbeck/www/etc/"+prefix+"_"+name+".png")
  del c1
  del l

for plot in [hNJets[htc] for htc in [500, 750, 1000]]:
  p = plot.Clone()
  p.SetBinContent(1, 0)
  p.SetBinContent(2, 0)
  p.SetBinContent(3, 0)
  p.SetBinContent(4, 0)
  p.SetBinContent(5, 0)
  print p.GetMean()
