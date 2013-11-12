import ROOT, os, sys
smoother = ROOT.TGraphSmooth("smoother")
doSmooth = True

path = os.path.abspath('../../HEPHYCommonTools/mva')
if not path in sys.path:
    sys.path.insert(1, path)

def delErr(g):
  for i in range(g.GetN()):
    g.GetEX()[i]=0
    g.GetEY()[i]=0
  

from nnAnalysisHelpers import getObjFromFile
foms = [ \
#    {"name":"MLP21","color":ROOT.kBlack,  "fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP21_stop300lsp270FastSim_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},
#    {"name":"MLP22","color":ROOT.kGreen,  "fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP22_stop300lsp270FastSim_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},
#    {"name":"MLP00","color":ROOT.kRed,    "fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP00_stop300lsp270FastSim_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},
#    {"name":"MLP11","color":ROOT.kBlue,   "fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP11_stop300lsp270FastSim_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},
#    {"name":"MLP01","color":ROOT.kMagenta,"fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP01_stop300lsp270FastSim_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},
#    {"name":"MLP10","color":ROOT.kOrange, "fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP10_stop300lsp270FastSim_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},
#    {"name":"MLP32","color":ROOT.kCyan   ,"fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP32_stop300lsp270FastSim_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},

    {"name":"MLP21, 100",   "color":ROOT.kBlack,   "fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP21_stop300lsp270FastSim_refsel_NormDeco_100_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},
    {"name":"MLP21, 1000",  "color":ROOT.kGreen,   "fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP21_stop300lsp270FastSim_refsel_NormDeco_1000_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},
    {"name":"MLP21, 5000",  "color":ROOT.kRed,     "fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP21_stop300lsp270FastSim_refsel_NormDeco_5000_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},
    {"name":"MLP21, 10000", "color":ROOT.kBlue,    "fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP21_stop300lsp270FastSim_refsel_NormDeco_10000_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},
    {"name":"MLP21, 20000", "color":ROOT.kMagenta, "fname":"/afs/hephy.at/user/s/schoefbeck/www/pngMJNN/nnValidation_MonoJet_MLP21_stop300lsp270FastSim_refsel_NormDeco_20000_sigmoid_BP_S03_SE08_softIsolatedMT_type1phiMet_deltaPhi.root"},
]
xRange = [0.10, 1.0]
yRange = [0.1, 0.30]

for f in foms:
  canv = getObjFromFile(f['fname'], "mlpa_canvas")
  pad = canv.GetPrimitive("mlpa_canvas_2")
  l = pad.GetListOfPrimitives().At(1).Clone("l")
  lp = pad.GetListOfPrimitives().At(2).Clone("lp")
  lm = pad.GetListOfPrimitives().At(3).Clone("lm")
  if doSmooth:
    ls = smoother.SmoothLowess(l,"", 0.01, 30, 0).Clone()
    lsp = smoother.SmoothLowess(lp,"", 0.01, 30, 0).Clone()
    lsm = smoother.SmoothLowess(lm,"", 0.01, 3, 0).Clone()
    delErr(ls)
    delErr(lsp)
    delErr(lsm)
  else:
    ls  =  l  
    lsp =  lp
    lsm =  lm

  ls.GetYaxis().SetRangeUser(0, 1)
  ls.GetXaxis().SetRangeUser(0, 1)
  ls.SetLineWidth(2)
  lsp.SetLineWidth(2)
  lsm.SetLineWidth(2)
  ls.SetLineColor(f['color'])
  lsp.SetLineColor(ROOT.kGray)
  lsm.SetLineColor(ROOT.kGray)
  for h in [ls, lsp, lsm]:
    h.SetMarkerColor(h.GetLineColor())
    h.SetMarkerStyle(0)
    h.SetMarkerSize(0)
    h.SetFillColor(h.GetLineColor())

  f['l']  = ls
  f['lp'] = lsp
  f['lm'] = lsm
  

l = ROOT.TLegend(.16, .13, 0.63, 0.35)
l.SetFillColor(ROOT.kWhite)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)

c = ROOT.TCanvas()
drawopt="AL"
for f in foms: 
  f['l'].GetYaxis().SetRangeUser(*xRange)
  f['l'].GetXaxis().SetRangeUser(*yRange)
  f["l"].Draw(drawopt)
  drawopt="L"
  f["l"].GetYaxis().SetTitle("Background rejection")
  f["l"].GetXaxis().SetTitle("Signal efficiency")
#  f["lp"].Draw("L")
#  f["lm"].Draw("L")
  f["l"].Draw("L")

  l.AddEntry(f['l'], f['name'], "LP")

l.Draw()

#subPad.Draw()
#subPad.cd()
#ls_c.GetYaxis().SetRangeUser(0.9965, 1.00)
#ls_c.GetXaxis().SetRangeUser(0.165, 0.205)
#ls_c.GetYaxis().SetTitle()
#ls_c.GetXaxis().SetTitle()
#
#ls_c.GetXaxis().SetTickLength(scale*ls_c.GetXaxis().GetTickLength())
#ls_c.GetYaxis().SetTickLength(scale*ls_c.GetYaxis().GetTickLength())
#ls_c.GetYaxis().SetNdivisions(504)
#ls_c.GetXaxis().SetNdivisions(405)
#ls_c.GetXaxis().SetLabelSize(scale*ls_c.GetXaxis().GetLabelSize()*0.7)
#ls_c.GetYaxis().SetLabelSize(scale*ls_c.GetYaxis().GetLabelSize()*0.7)
#
#l2 = ROOT.TLine(0.18, 0.9965 ,0.18 , 1)
#l2.Draw()
#
#
#ls_c.Draw("AL")
#lp_c.Draw("L")
#lm_c.Draw("L")
#myCut_c.Draw("same")
#
#ar2 = ROOT.TArrow(0.178,1,0.178,0.99915,0.02,"|>")
#ar2.SetLineColor(ROOT.kRed)
#ar2.SetFillColor(ROOT.kRed)
#ar2.Draw()
#
#
#c.RedrawAxis()
#
#
#c.Print("/afs/hephy.at/user/s/schoefbeck/www/pngNN/niceMVAFOMPlot.root")
#c.Print("/afs/hephy.at/user/s/schoefbeck/www/pngNN/niceMVAFOMPlot.png")
#c.Print("/afs/hephy.at/user/s/schoefbeck/www/pngNN/niceMVAFOMPlot.pdf")
#
