import ROOT

def Draw_CMS_header(lumi_label=36,xPos=0.18,text="Preliminary"):
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextAlign(31)
   tex.SetTextFont(42)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(0.96,0.96,str(lumi_label)+" fb^{-1} (13 TeV)")
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextFont(61)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(xPos,0.96,"CMS")
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextFont(52)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(xPos+0.1,0.96,text)
   return

def Set_axis_pad2(histo):
   histo.GetXaxis().SetLabelFont(42)
   histo.GetXaxis().SetLabelOffset(0.007)
   histo.GetXaxis().SetLabelSize(0.11)
   histo.GetXaxis().SetTitleSize(0.14)
   histo.GetXaxis().SetTitleOffset(0.9)
   histo.GetXaxis().SetTitleFont(42)
   histo.GetYaxis().SetTitle("Data/Pred.")
   histo.GetYaxis().SetDecimals()
   histo.GetYaxis().SetNdivisions(505)
   histo.GetYaxis().SetLabelFont(42)
   histo.GetYaxis().SetLabelOffset(0.007)
   histo.GetYaxis().SetLabelSize(0.11)
   histo.GetYaxis().SetTitleSize(0.14)
   histo.GetYaxis().SetTitleOffset(0.52)
   histo.GetYaxis().SetTitleFont(42)
   histo.GetZaxis().SetLabelFont(42)
   histo.GetZaxis().SetLabelOffset(0.007)
   histo.GetZaxis().SetLabelSize(0.05)
   histo.GetZaxis().SetTitleSize(0.06)
   histo.GetZaxis().SetTitleFont(42)
   return

def Set_axis_pad1(histo):
   histo.GetXaxis().SetLabelFont(42)
   histo.GetXaxis().SetLabelOffset(0.007)
   histo.GetXaxis().SetLabelSize(0.05)
   histo.GetXaxis().SetTitleSize(0.06)
   histo.GetXaxis().SetTitleOffset(0.9)
   histo.GetXaxis().SetTitleFont(42)
   histo.GetYaxis().SetLabelFont(42)
   histo.GetYaxis().SetLabelOffset(0.007)
   histo.GetYaxis().SetLabelSize(0.05)
   histo.GetYaxis().SetTitleSize(0.06)
   histo.GetYaxis().SetTitleOffset(1.35)
   histo.GetYaxis().SetTitleFont(42)
   histo.GetZaxis().SetLabelFont(42)
   histo.GetZaxis().SetLabelOffset(0.007)
   histo.GetZaxis().SetLabelSize(0.05)
   histo.GetZaxis().SetTitleSize(0.06)
   histo.GetZaxis().SetTitleFont(42)
   return

ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)

#input root files
plot = "nBJet"
multib_file_name = "base_plotsCP.root"
cms_header_label = "Preliminary"

signal_suffix = "x10"  #change here if SB
path = "/afs/hephy.at/user/e/easilar/www/Moriond2017/plots_AN_ReminiAOD_ra2bFil/"

multib_file   = ROOT.TFile(multib_file_name) 
hsig1200_mult = multib_file.Get(plot+"_T1tttt_1200_800_norm")
hsig1800_mult = multib_file.Get(plot+"_T1tttt_1800_100_norm")

signals = [\
{"histo":hsig1200_mult ,"name":"s1500_1000","tex":"T1tttt 1.4/1.1 "+signal_suffix,"color":ROOT.TColor.GetColor("#ff00ff")},\
{"histo":hsig1800_mult ,"name":"s1900_100","tex":"T1tttt 1.9/0.1 "+signal_suffix,"color":ROOT.TColor.GetColor("#00ffff")},\
]


bkg_samples=[
{'sample':"TTV",      'tex':'t#bar{t}V','color':ROOT.kOrange-3},
{"sample":"VV",       "tex":"WW/WZ/ZZ","color":ROOT.kRed+3},
{"sample":"DY",       "tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"SingleT",  "tex":"t/#bar{t}",'color': ROOT.kViolet+5},
{"sample":"QCD",      "tex":"QCD","color":ROOT.kCyan-6},
{"sample":"WJets",    "tex":"W + jets","color":ROOT.kGreen-2},
{"sample":"TTdiLep",  "tex":"t#bar{t} ll + jets",'color':ROOT.kBlue},
{"sample":"TTsemiLep","tex":"t#bar{t} l + jets",'color':ROOT.kBlue-7}
]

for bkg in bkg_samples:
    bkg['histo'] = multib_file.Get(plot+"_"+bkg["sample"])

h_data = multib_file.Get(plot+"_data")

#p = {'ndiv':False,'yaxis':'Events','xaxis':'n_{b-tag}','logy':'True' , 'var':'nBJetMediumCSV30',                   'bin_set':(False,25),          'varname':'nBJetMediumCSV30',      'binlabel':1,  'bin':(10,0,10),       'lowlimit':0,  'limit':10}
##wide bin example
dPhiBins  = array('d', [float(x)/1000. for x in range(0,500,100)+range(500,700,200)+range(700,1000,300)+range(1000,2000,500)+range(2000,3141,1141)+range(3141,4300,1159)])
#lTBins  = array('d', [float(x) for x in range(250,450,100)+range(450,600,150)+range(600,950,350)+range(950,5000,4050)])
#hTBins  = array('d', [float(x) for x in range(500,1250,250)+range(1250,2500,1250)+range(2500,5500,4000)])
p = {'ndiv':False,'yaxis':'< Events / 0.1>','xaxis':'#Delta#Phi(W,l)','logy':'True' , 'var':'deltaPhi_Wl',        'bin_set':(True,0.1),          'varname':'deltaPhi_Wl',       'binlabel':1, 'bin':(len(dPhiBins)-1,dPhiBins)} 
#p = {'ndiv':True,'yaxis':'< Events / 100 GeV >','xaxis':'L_{T} [GeV]','logy':'True' , 'var':  'st',                          'bin_set':(True,100),          'varname':'LT',                  'binlabel':"",  'bin':(len(lTBins)-1,lTBins)} #LT
#p = {'ndiv':True,'yaxis':'< Events / 250 GeV >','xaxis':'H_{T}','logy':'True' , 'var':'htJet30j',                              'bin_set':(True,250),        'varname':'htJet30j',            'binlabel':"",  'bin':(len(hTBins)-1,hTBins)} #HT

cb = ROOT.TCanvas("cb","cb",564,232,600,600)
cb.SetHighLightColor(2)
cb.Range(0,0,1,1)
cb.SetFillColor(0)
cb.SetBorderMode(0)
cb.SetBorderSize(2)
cb.SetTickx(1)
cb.SetTicky(1)
cb.SetLeftMargin(0.18)
cb.SetRightMargin(0.04)
cb.SetTopMargin(0.05)
cb.SetBottomMargin(0.13)
cb.SetFrameFillStyle(0)
cb.SetFrameBorderMode(0)
cb.SetFrameFillStyle(0)
cb.SetFrameBorderMode(0)
cb.cd()

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.05)
latex.SetTextAlign(11)

leg = ROOT.TLegend(0.65,0.5,0.93,0.925)
leg.SetBorderSize(1)
leg_sig = ROOT.TLegend(0.2,0.7,0.6,0.92)
leg_sig.SetBorderSize(1)
leg_sig.SetTextSize(0.04)
Pad1 = ROOT.TPad("Pad1", "Pad1", 0,0.31,1,1)
Pad1.Draw()
Pad1.cd()
#Pad1.Range(-0.7248462,-1.30103,3.302077,3.159352)
Pad1.SetFillColor(0)
Pad1.SetBorderMode(0)
Pad1.SetBorderSize(2)
Pad1.SetLogy()
Pad1.SetTickx(1)
Pad1.SetTicky(1)
Pad1.SetLeftMargin(0.18)
Pad1.SetRightMargin(0.04)
Pad1.SetTopMargin(0.055)
Pad1.SetBottomMargin(0)
Pad1.SetFrameFillStyle(0)
Pad1.SetFrameBorderMode(0)
Pad1.SetFrameFillStyle(0)
Pad1.SetFrameBorderMode(0)
Pad1.SetLogy()
ROOT.gStyle.SetErrorX(.5)
h_Stack = ROOT.THStack('h_Stack','h_Stack')
for bkg in bkg_samples:
  color = bkg['color']
  histo = bkg['histo']
  #histo.Scale(bin[srNJet][stb][htb]['scale_fac'])
  histo.SetFillColor(color)
  histo.SetLineColor(ROOT.kBlack)
  histo.SetLineWidth(1)
  Set_axis_pad1(histo)
  histo.GetYaxis().SetTitle(p['yaxis'])
  h_Stack.Add(histo)

if p["bin_set"][0]: stack_hist=ROOT.TH1F("stack_hist","stack_hist", p['bin'][0],p['bin'][1])
else: stack_hist=ROOT.TH1F("stack_hist","stack_hist",p['bin'][0],p['bin'][1],p['bin'][2])
stack_hist.Merge(h_Stack.GetHists())
max_bin = stack_hist.GetMaximum()*10000
h_Stack.SetMaximum(max_bin)
h_Stack.SetMinimum(0.00001)
#h_Stack.SetMinimum(0.11)

color = ROOT.kBlack
h_data.SetMarkerStyle(20)
h_data.SetMarkerSize(1.1)
h_data.SetLineColor(color)
h_data.GetXaxis().SetTitle(p['xaxis'])
h_data.SetTitle("")
Set_axis_pad1(h_data)
h_data.Draw("E1")
h_data.SetMaximum(max_bin)
h_data.SetMinimum(0.11)
h_Stack.Draw("HistoSame")
for sig in signals:
  h_sig = sig["histo"]
  h_sig.SetLineColor(sig["color"])
  h_sig.SetLineWidth(3)
  h_sig.SetTitle("")
  h_sig.Draw("HistoSame")
  leg_sig.AddEntry(h_sig, sig['tex'],"l")
  del h_sig
h_data.Draw("E1 Same")
if p['ndiv']:
  h_data.GetXaxis().SetNdivisions(505)
  h_data.GetYaxis().SetTitle(p['yaxis'])
if not p['ndiv']:
  h_data.GetYaxis().SetTitle(p['yaxis'])
leg.AddEntry(h_data, "Data","PL")
for bkg in reversed(bkg_samples):
  color = bkg['color']
  histo = bkg['histo']
  histo.SetFillColor(color)
  histo.SetLineColor(ROOT.kBlack)
  histo.SetLineWidth(1)
  leg.AddEntry(histo, bkg['tex'],"f")

leg.SetFillColor(0)
leg.SetLineColor(0)
leg.Draw()
leg_sig.SetFillColor(0)
leg_sig.SetLineColor(0)
leg_sig.Draw()
Draw_CMS_header(text=cms_header_label)
Pad1.RedrawAxis()
cb.cd()
Pad2 = ROOT.TPad("Pad2", "Pad2",  0, 0, 1, 0.31)
Pad2.Draw()
Pad2.cd()
Pad2.SetFillColor(0)
Pad2.SetFillStyle(4000)
Pad2.SetBorderMode(0)
Pad2.SetBorderSize(2)
Pad2.SetTickx(1)
Pad2.SetTicky(1)
Pad2.SetLeftMargin(0.18)
Pad2.SetRightMargin(0.04)
Pad2.SetTopMargin(0)
Pad2.SetBottomMargin(0.3)
Pad2.SetFrameFillStyle(0)
Pad2.SetFrameBorderMode(0)
Pad2.SetFrameFillStyle(0)
Pad2.SetFrameBorderMode(0)
if p["bin_set"][0] : Func = ROOT.TF1('Func',"[0]",p['bin'][1][0],p['bin'][1][-1])
else: Func = ROOT.TF1('Func',"[0]",p['bin'][1],p['bin'][2])
Func.SetParameter(0,1)
Func.SetLineColor(58)
Func.SetLineWidth(2)
h_ratio = h_data.Clone('h_ratio')
h_ratio.Sumw2()
h_ratio.SetStats(0)
h_ratio.Divide(stack_hist)
rmax = 2
for b in xrange(1,h_ratio.GetNbinsX()+1):
  if h_ratio.GetBinContent(b) == 0: continue
  rmax = max([ rmax, h_ratio.GetBinContent(b) + 2*h_ratio.GetBinError(b) ])
print rmax
h_ratio.SetMinimum(0.01)
h_ratio.SetMaximum(min(rmax,1.9))
h_ratio.SetMarkerStyle(20)
h_ratio.SetMarkerSize(1.1)
h_ratio.SetMarkerColor(ROOT.kBlack)
h_ratio.SetTitle("")
Set_axis_pad2(h_ratio)
h_ratio.GetYaxis().SetTitle("Data/Pred. ")
h_ratio.GetXaxis().SetTitle(p['xaxis'])
h_ratio.GetYaxis().SetNdivisions(505)
h_ratio.Draw("E1")
Func.Draw("same")
h_ratio.Draw("E1 Same")
cb.Draw()
cb.SaveAs(path+plot+'.png')
cb.SaveAs(path+plot+'.pdf')
cb.SaveAs(path+plot+'.root')
