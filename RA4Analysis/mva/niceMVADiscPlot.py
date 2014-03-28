import ROOT
smoother = ROOT.TGraphSmooth("smoother")
doSmooth = True

path = os.path.abspath('../../HEPHYPythonTools/mva')
if not path in sys.path:
    sys.path.insert(1, path)


from Workspace.HEPHYPythonTools.nnAnalysisHelpers import getObjFromFile
ifile = "/afs/hephy.at/user/s/schoefbeck/www/pngNN/nnValidation_RA4_test_refWeight1000_T1tttt_4j_bt1_met100_mt2w0_NormDeco_10000_sigmoid_BP_S03_SE08_mgl_1300_mN_850_mT_type1phiMet_mt2w_nbtags_njets_minDeltaPhi_htRatio_deltaPhi.root"

ROOT.TH1F().SetDefaultSumw2()

def delErr(g):
  for i in range(g.GetN()):
    g.GetEX()[i]=0
    g.GetEY()[i]=0
  
canv = getObjFromFile(ifile, "mlpa_canvas")
#myCut = canv.GetPrimitive("mlpa_canvas_1").GetListOfPrimitives().At(2)
pad = canv.GetPrimitive("mlpa_canvas_3")
hbgTest = canv.GetPrimitive("mlpa_canvas_3").GetListOfPrimitives().FindObject("hbgTest")
hsigTest = canv.GetPrimitive("mlpa_canvas_3").GetListOfPrimitives().FindObject("hsigTest")
hbgTrain = canv.GetPrimitive("mlpa_canvas_4").GetListOfPrimitives().FindObject("hbgTrain")
hsigTrain = canv.GetPrimitive("mlpa_canvas_4").GetListOfPrimitives().FindObject("hsigTrain")

hbgTest.SetLineColor(ROOT.kBlue)
hbgTrain.SetLineColor(ROOT.kBlue)
hsigTest.SetLineColor(ROOT.kRed)
hsigTrain.SetLineColor(ROOT.kRed)

for h in [hbgTrain, hsigTest, hsigTrain]:
  h.Scale(hbgTest.Integral() / h.Integral())

for h in [hbgTest, hbgTrain, hsigTest, hsigTrain]:
  s=2
  h.Rebin(s)

hbgTrain.GetYaxis().SetRangeUser(0, 1.3*hbgTrain.GetMaximum())
hbgTrain.GetYaxis().SetTitle("Number of Events")
hbgTrain.GetYaxis().SetTitleOffset(1.4)
hbgTrain.GetXaxis().SetTitle("MLP Discriminator")

hbgTrain.GetXaxis().SetRangeUser(-0.2,1.2)

hbgTest.SetMarkerStyle(21)
hbgTest.SetMarkerSize(.5)
hbgTrain.SetFillStyle(3004)

hsigTest.SetMarkerStyle(21)
hsigTest.SetMarkerSize(.5)
hsigTrain.SetFillStyle(3004)

c = ROOT.TCanvas()
hbgTrain.Draw("")
hbgTest.Draw("e1psame")
hsigTrain.Draw("same")
hsigTest.Draw("e1psame")

l = ROOT.TLegend(.35, .55, 0.95, 0.95)
l.SetFillColor(ROOT.kWhite)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)
l.AddEntry(hbgTrain, "Background training sample", "f")
l.AddEntry(hsigTrain, "Signal training sample", "f")
l.AddEntry(hbgTest, "Background validation sample", "lp")
l.AddEntry(hsigTest, "Signal validation sample", "lp")
l.Draw()

#ar1 = ROOT.TArrow(0.978,2500,0.978,0,0.02,"|>")
#ar1.SetLineColor(ROOT.kRed)
#ar1.SetFillColor(ROOT.kRed)
#ar1.Draw()


c.Print("/afs/hephy.at/user/s/schoefbeck/www/pngNN/niceMVADiscPlot.root")
c.Print("/afs/hephy.at/user/s/schoefbeck/www/pngNN/niceMVADiscPlot.png")
c.Print("/afs/hephy.at/user/s/schoefbeck/www/pngNN/niceMVADiscPlot.pdf")

