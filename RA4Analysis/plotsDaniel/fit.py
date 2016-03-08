import ROOT


#def fline(x, p):
#  if x[0] > 2.5 and x[0]<3.5:
#    ROOT.TF1.RejectPoint()
#    return 100
#  return p[0] + p[1]*x[0]


#def exclude():
f1 = ROOT.TF1("f1", "[0] + [1]*x + gaus(2)", 0, 5)
f1.SetParameters(6,1,5,3,0.2)
h = ROOT.TH1F("h", "background + signal", 100, 0, 5)
h.FillRandom("f1", 10000)
#f1 = ROOT.TF1("f1", fline, 0, 5, 2)
#f1 = ROOT.TF1("f1", "[0]+[1]*x", 0, 5)
#f1.SetParameters(2,-1)

f2 = ROOT.TF1("f2", "[0]*exp(-([1]+x)**2)", 0, 5)

#fgaus = ROOT.TF1("fgaus", "[0]+[1]*exp(-(x+[3])**2) + [4]*x", -5, 5)

#fline.SetParameters(2, -1)
#res = h.Fit("f1", "S") #used "l" before
res2 = h.Fit("f2", "S")
#h.Fit("fgaus")

res.Print("V")

h.Draw("hist")

#f1.Draw('same')
f2.Draw('same')
#fgaus.Draw('same')

hint1 = ROOT.TH1F("hint1", "1 sigma", 100, 0, 5)
hint2 = ROOT.TH1F("hint2", "2 sigma", 100, 0, 5)
hint1.SetMarkerSize(0)
hint2.SetMarkerSize(0)
ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint1, 0.68)
ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint2, 0.95)

#hint.SetStats(False)
hint1.SetFillColorAlpha(ROOT.kGreen, 0.45)
hint2.SetFillColorAlpha(ROOT.kYellow, 0.45)
#f2.Draw('same')

#h.SetFillColorAlpha(ROOT.kBlue, 0.35)
#h.Draw("hist same")

#hint.SetLineWidth(1)
hint2.Draw("e3 same")
hint1.Draw("e3 same")
f2.Draw('same')
h.Draw("hist same")


#h.SetFillColorAlpha(ROOT.kBlue, 0.35)
#h.Draw("hist same")

#ngr = 100
#gr = ROOT.TGraph(ngr)
#gr.SetName("GraphNoError")
#
#for i in range(ngr):
#   x = ROOT.gRandom.Uniform(-1, 1)
#   y = -1 + 2*x + ROOT.gRandom.Gaus(0, 1)
#   gr.SetPoint(i, x, y)
#
#
##Create the fitting function
#fpol = ROOT.TF1("fpol", "pol1", -1, 1)
#fpol.SetLineWidth(2)
#gr.Fit(fpol, "Q")
#
##Create a TGraphErrors to hold the confidence intervals
#grint = ROOT.TGraphErrors(ngr)
#grint.SetTitle("Fitted line with .95 conf. band")
#for i in range(ngr):
#   grint.SetPoint(i, gr.GetX()[i], 0)
#
##Compute the confidence intervals at the x points of the created graph
#ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(grint)
##Now the "grint" graph contains function values as its y-coordinates
##and confidence intervals as the errors on these coordinates
##Draw the graph, the function and the confidence intervals
#
##myc->cd(1);
#grint.SetLineColor(ROOT.kRed)
#grint.Draw("ap")
#gr.SetMarkerStyle(5)
#gr.SetMarkerSize(0.7)
#gr.Draw("psame")


