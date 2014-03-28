import ROOT, pickle
from Workspace.RA4Analysis.simplePlotsCommon import *
ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
#ROOT.gStyle.SetPadRightMargin(0.10);
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()

ROOT.tdrStyle.SetPadRightMargin(0.16)
ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)

#if not globals().has_key("LO_Mu_efficiency"):
#  print "Loading..."
#  globals()["LO_Mu_efficiency"] = pickle.load(open("/data/schoef/efficiencies/msugra/Mu_msugra_LO_efficiency.pkl"))
#  globals()["NLO_Mu_efficiency"] = pickle.load(open("/data/schoef/efficiencies/msugra/Mu_msugra_NLO_efficiency.pkl"))
#  globals()["LO_Ele_efficiency"] = pickle.load(open("/data/schoef/efficiencies/Ele_msugra_LO_efficiency.pkl"))
#  globals()["NLO_Ele_efficiency"] = pickle.load(open("/data/schoef/efficiencies/Ele_msugra_NLO_efficiency.pkl"))
#else:
#  print "Already loaded."

mode = "efficiency"
#mode = "events"
stuff=[]
for sstring in ["Ele_msugra_LO_"+mode, "Ele_msugra_NLO_"+mode, "Mu_msugra_LO_"+mode, "Mu_msugra_NLO_"+mode]:
  if not globals().has_key(sstring):
    filename = "/data/schoef/efficiencies/msugra/"+sstring+".pkl"
    print "Loading", filename
    globals()[sstring] =  pickle.load(open(filename))
    globals()[sstring+"_h"] = ROOT.TH2F(sstring, sstring, 151, 0-10, 3000+10, 51, 0-10, 1000+10)
  for key in eval(sstring)['inc'][750][250].keys():
    m0 = float(key.split("_")[1])
    m12 = float(key.split("_")[2])
    eff = eval(sstring)['inc'][750][250][key]
    if eff>0. and eff < float('inf'):
      eval(sstring+"_h").Fill(m0, m12, eff)
  canv = ROOT.TCanvas()
  canv.SetLogz()
  canv.SetTitle(sstring)
  if mode=="events":
    eval(sstring+"_h").GetZaxis().SetRangeUser(10**(-4), 10**(2))
  if mode=="efficiency":
    eval(sstring+"_h").GetZaxis().SetRangeUser(10**(-4), 10**(-1))
  eval(sstring+"_h").Draw("COLZ")
  stuff.append(canv)

Ele_ratio_c = ROOT.TCanvas()
Ele_ratio_c.SetTitle("ratio "+mode+" NLO/LO Ele")
Ele_ratio = eval("Ele_msugra_NLO_"+mode+"_h").Clone()
Ele_ratio.GetZaxis().SetRangeUser(0,2)
Ele_ratio.Divide(eval("Ele_msugra_LO_"+mode+"_h"))
Ele_ratio.Draw("COLZ")

Mu_ratio_c = ROOT.TCanvas()
Mu_ratio_c.SetTitle("ratio "+mode+" NLO/LO Mu")
Mu_ratio = eval("Mu_msugra_NLO_"+mode+"_h").Clone()
Mu_ratio.GetZaxis().SetRangeUser(0,2)
Mu_ratio.Divide(eval("Mu_msugra_LO_"+mode+"_h"))
Mu_ratio.Draw("COLZ")
