import ROOT
smoother = ROOT.TGraphSmooth("smoother")
doSmooth = True

path = os.path.abspath('../../HEPHYCommonTools/mva')
if not path in sys.path:
    sys.path.insert(1, path)

from nnAnalysisHelpers import getObjFromFile
#ifile = "/afs/hephy.at/user/s/schoefbeck/www/pngNN/nnValidation_RA4_test_T1tttt-madgraph_4j_met100_mt2w200_NormDeco_10000_sigmoid_BP_S03_SE08_mD_600_800_mN_500_600_mT_type1phiMet_mt2w_nbtags_njets_minDeltaPhi_htRatio_deltaPhi.root"
#ifile = "/afs/hephy.at/user/s/schoefbeck/www/pngNN/nnValidation_RA4_4j_met100_mt2w200_NormDeco_5000_sigmoid_mD_200_400_mN_500_600_mT_type1phiMet_mt2w_nbtags_njets_minDeltaPhi_htRatio_deltaPhi.root"
#ifile = "/afs/hephy.at/user/s/schoefbeck/www/pngNN/nnValidation_RA4_test_refWeight200_T1tttt-madgraph_4j_met100_mt2w200_NormDeco_10000_sigmoid_BP_S03_SE08_mgl_1400_mN_800_mT_type1phiMet_mt2w_nbtags_njets_minDeltaPhi_htRatio_deltaPhi.root"
#ifile ="/afs/hephy.at/user/s/schoefbeck/www/pngNN/nnValidation_RA4_test_refWeight200_T1tttt_4j_met100_mt2w200_NormDeco_10000_sigmoid_BP_S03_SE08_mgl_1200_mN_750_mT_type1phiMet_mt2w_nbtags_njets_minDeltaPhi_htRatio_deltaPhi.root"
ifile = "/afs/hephy.at/user/s/schoefbeck/www/pngNN/nnValidation_RA4_test_refWeight1000_T1tttt_4j_bt1_met100_mt2w0_NormDeco_10000_sigmoid_BP_S03_SE08_mgl_1300_mN_850_mT_type1phiMet_mt2w_nbtags_njets_minDeltaPhi_htRatio_deltaPhi.root"

def delErr(g):
  for i in range(g.GetN()):
    g.GetEX()[i]=0
    g.GetEY()[i]=0
  
canv = getObjFromFile(ifile, "mlpa_canvas")
myCut = canv.GetPrimitive("mlpa_canvas_1").GetListOfPrimitives().At(2)
pad = canv.GetPrimitive("mlpa_canvas_2")
l = pad.GetListOfPrimitives().At(1).Clone("l")
lp = pad.GetListOfPrimitives().At(2).Clone("lp")
lm = pad.GetListOfPrimitives().At(3).Clone("lm")
#lmT = pad.GetListOfPrimitives().At(5).Clone("lmT")
#lmet = pad.GetListOfPrimitives().At(8).Clone("lmet")

c = ROOT.TCanvas()

#res = smoother.Approx(l, "constant" )
if doSmooth:
  ls = smoother.SmoothLowess(l,"", 0.01, 30, 0).Clone()
  lsp = smoother.SmoothLowess(lp,"", 0.01, 30, 0).Clone()
  lsm = smoother.SmoothLowess(lm,"", 0.01, 3, 0).Clone()
#  lsmT = smoother.SmoothLowess(lmT,"", 0.03, 3, 0).Clone()
#  lsmet = smoother.SmoothLowess(lmet,"", 0.01, 15, 0).Clone()
  delErr(ls)
  delErr(lsp)
  delErr(lsm)
#  delErr(lsmT)
#  delErr(lsmet)
else:
  ls =   l  
  lsp =  lp
  lsm =  lm
#  lsmT =  lmT 
#  lsmet = lmet

ls.GetYaxis().SetRangeUser(0, 1)
ls.GetXaxis().SetRangeUser(0, 1)
ls.SetLineWidth(2)
lsp.SetLineWidth(2)
lsm.SetLineWidth(2)
ls.SetLineColor(ROOT.kBlue)
lsp.SetLineColor(ROOT.kGray)
lsm.SetLineColor(ROOT.kGray)
#lsmT.SetLineColor(ROOT.kGreen)
#lsmT.SetLineWidth(2)
#lsmet.SetLineColor(ROOT.kMagenta)
#lsmet.SetLineWidth(2)

for h in [ls, lsp, lsm]:
  h.SetMarkerColor(h.GetLineColor())
  h.SetMarkerStyle(0)
  h.SetMarkerSize(0)
  h.SetFillColor(h.GetLineColor())

#res.SetLineColor(ROOT.kRed)
ls.Draw("AL")
ls.GetYaxis().SetTitle("Background rejection")
ls.GetXaxis().SetTitle("Signal efficiency")
lsp.Draw("L")
lsm.Draw("L")
ls.Draw("L")

#lsmT.Draw("L")
#lsmet.Draw("L")
myCut_c=myCut.Clone()
s=4
myCut.Rebin(s)
myCut.Scale(1./float(s))
myCut.Smooth(5)
myCut.Draw("same")
myCut.SetLineColor(ROOT.kBlack)

ar1 = ROOT.TArrow(0.178,0.9,0.178,0.99915,0.02,"|>")
ar1.SetLineColor(ROOT.kRed)
ar1.SetFillColor(ROOT.kRed)
ar1.Draw()

c.RedrawAxis()

l = ROOT.TLegend(.16, .13, 0.63, 0.35)
l.SetFillColor(ROOT.kWhite)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)
l.AddEntry(ls, "MLP strategy", "LP")
#l.AddEntry(lsp, "MLP #pm 1#sigma", "LP")
#l.AddEntry(lmet, "only #slash{E}_{T} cut", "LP")
#l.AddEntry(lmT, "only m_{T} cut", "LP")
l.AddEntry(myCut, "cut-based strategy")
l.Draw()
line1 = ROOT.TLine()
line1.SetLineColor(lsp.GetLineColor())
line1.DrawLineNDC(0.177,0.305,0.258,0.305)
line1.DrawLineNDC(0.177,0.285,0.258,0.285)

ls_c=ls.Clone()
lp_c=lp.Clone()
lm_c=lm.Clone()
lp_c.SetLineColor(ROOT.kGray)
lm_c.SetLineColor(ROOT.kGray)
lp_c.SetLineWidth(2)
lm_c.SetLineWidth(2)

posX = 0.2
posY = 0.4
width = 0.45
subPad = ROOT.TPad("sub","sub", posX, posY, posX+width, posY+width)
subPad.SetLeftMargin(0.18)
scale = 1/width

myCut_c.Smooth(5)
myCut_c.SetLineColor(myCut.GetLineColor())


subPad.Draw()
subPad.cd()
ls_c.GetYaxis().SetRangeUser(0.9965, 1.00)
ls_c.GetXaxis().SetRangeUser(0.165, 0.205)
ls_c.GetYaxis().SetTitle()
ls_c.GetXaxis().SetTitle()

ls_c.GetXaxis().SetTickLength(scale*ls_c.GetXaxis().GetTickLength())
ls_c.GetYaxis().SetTickLength(scale*ls_c.GetYaxis().GetTickLength())
ls_c.GetYaxis().SetNdivisions(504)
ls_c.GetXaxis().SetNdivisions(405)
ls_c.GetXaxis().SetLabelSize(scale*ls_c.GetXaxis().GetLabelSize()*0.7)
ls_c.GetYaxis().SetLabelSize(scale*ls_c.GetYaxis().GetLabelSize()*0.7)

l2 = ROOT.TLine(0.18, 0.9965 ,0.18 , 1)
l2.Draw()


ls_c.Draw("AL")
lp_c.Draw("L")
lm_c.Draw("L")
myCut_c.Draw("same")

ar2 = ROOT.TArrow(0.178,1,0.178,0.99915,0.02,"|>")
ar2.SetLineColor(ROOT.kRed)
ar2.SetFillColor(ROOT.kRed)
ar2.Draw()


c.RedrawAxis()


c.Print("/afs/hephy.at/user/s/schoefbeck/www/pngNN/niceMVAFOMPlot.root")
c.Print("/afs/hephy.at/user/s/schoefbeck/www/pngNN/niceMVAFOMPlot.png")
c.Print("/afs/hephy.at/user/s/schoefbeck/www/pngNN/niceMVAFOMPlot.pdf")

