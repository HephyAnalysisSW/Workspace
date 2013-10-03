import ROOT
from array import array
from simplePlotsCommon import *
ROOT.setTDRStyle()

filename = "/afs/hephy.at/user/s/schoefbeck/www/pngFake2012/525_5fb_typeIpfMET_templates.root"
rf = ROOT.TFile(filename)

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

mode = "EleMu"
bjetbins = {"inc":"(1)", \
            "b0":"(!(btag0>0.679))",
            "b1":"(btag0>0.679&&(!(btag1>0.679)))",
            "b1p":"(btag0>0.679)",
            "b2":"(btag1>0.679)"
            }

htbins = [h[0] for h in htvals] + [htvals[-1][1]]

template={}
template_j={}
for bmode in bjetbins.keys():
  template[bmode]={}
  template_j[bmode]={}
  for htval in htvals:
    rf.cd()
    hname = "met_shape_"+mode+"_"+bmode+"_ht_"+str(htval[0])+"_"+str(htval[1])
    hname_j = "met_shape_"+bmode+"_ht_"+str(htval[0])+"_"+str(htval[1])+"_njet_4"
    htmp = rf.Get(hname)
    htmp_j = rf.Get(hname_j)
    ROOT.gDirectory.cd("PyROOT:/")
    template[bmode][htval[0]] = htmp.Clone(hname+"_clone")
    template[bmode][htval[0]].SetName(hname)
    template_j[bmode][htval[0]] = htmp_j.Clone(hname_j+"_clone")
    template_j[bmode][htval[0]].SetName(hname_j)
    print "Read",template[bmode][htval[0]], template_j[bmode][htval[0]], "from",filename

rf.Close()

niceName = {"b0":"==0 btags", "b1":"==1 btags", "b1p":">=1 btags", "b2":">=2 btags"}
mean = {}
mean_j = {}
for bmode in bjetbins.keys():
  mean[bmode] = ROOT.TH1F("mean_"+bmode, "mean_"+bmode, len(htbins) - 1, array('d',htbins))
  mean_j[bmode] = ROOT.TH1F("mean_"+bmode, "mean_"+bmode, len(htbins) - 1, array('d',htbins))
  for htval in htvals:
    b = mean[bmode].FindBin(htval[0])
    mean[bmode].SetBinContent(b, template[bmode][htval[0]].GetMean())
    mean[bmode].SetBinError  (b, template[bmode][htval[0]].GetMeanError())
    mean_j[bmode].SetBinContent(b, template_j[bmode][htval[0]].GetMean())
    mean_j[bmode].SetBinError  (b, template_j[bmode][htval[0]].GetMeanError())

#l = ROOT.TLegend(0.7,0.2,1,0.6)
#l.SetFillColor(0)
#l.SetShadowColor(ROOT.kWhite)
#l.SetBorderSize(1)
#colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen]

#for i, b in enumerate(reversed(["b0", "b1", "b1p", "b2"])):
#  mean[b].SetLineColor(colors[i])
#  mean[b].SetLineStyle(0)
#  mean[b].SetLineWidth(0)
#  mean[b].SetMarkerColor(colors[i])
#  mean[b].SetMarkerStyle(0);
#  mean[b].GetXaxis().SetTitle("H_{T} (GeV)")
#  mean[b].GetYaxis().SetTitle("Mean of fake MET template")
#
#  if i==0:
#    mean[b].Draw("h")
#  else:
#    mean[b].Draw("hsame")
#
#  l.AddEntry(mean[b], niceName[b])
#
#l.Draw()

l = ROOT.TLegend(0.7,0.2,1,0.6)
l.SetFillColor(0)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)
colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen]
for i, b in enumerate(reversed(["b0", "b1", "b1p", "b2"])):
  mean_j[b].SetLineColor(colors[i])
  mean_j[b].SetLineStyle(0)
  mean_j[b].SetLineWidth(0)
  mean_j[b].SetMarkerColor(colors[i])
  mean_j[b].SetMarkerStyle(0);
  mean_j[b].GetXaxis().SetTitle("H_{T} (GeV)")
  mean_j[b].GetYaxis().SetTitle("mean_j of fake MET template")

  if i==0:
    mean_j[b].Draw("h")
  else:
    mean_j[b].Draw("hsame")

  l.AddEntry(mean_j[b], niceName[b])

l.Draw()
