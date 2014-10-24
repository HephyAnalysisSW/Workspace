import ROOT

filename = 'Mt03.root'
plot1 = 'h_DeltaPhi' 
plot2 = 'h_GenDeltaPhi'
plot1name = plot1.split('_')[1]
plot2name = plot2.split('_')[1]


File = ROOT.TFile(filename)
histo1 = File.Get(plot1)
histo2 = File.Get(plot2)

can = ROOT.TCanvas("Comparison of "+plot1name+"and"+plot2name)
can.cd()
Pad1 = ROOT.TPad("Pad1", "Pad1", 0, 0.1, 1, 1.0)
Pad1.Draw()
Pad1.cd()
histo1.SetTitle("Delta Phi Closure test")
histo1.SetLineColor(ROOT.kBlue-3)
histo1.SetLineWidth(2)
histo1.Draw()
histo2.SetLineColor(ROOT.kRed+1)
histo2.SetLineWidth(2)
histo2.Draw('same')
leg = ROOT.TLegend(0.8,0.65,0.9,0.75)
leg.AddEntry(histo1, "Predicted","l")
leg.AddEntry(histo2, "Truth","l")
leg.SetFillColor(0)
leg.Draw()
Pad1.SetLogy()
Pad2 = ROOT.TPad("Pad2", "Pad2", 0, 0, 1, 0.1)
Pad2.Draw()
Pad2.cd()
h_ratio = histo1.Clone("h_ratio")
h_ratio.SetMinimum(0.0)
h_ratio.SetMaximum(2.0)
h_ratio.Sumw2()
h_ratio.SetStats(0)
h_ratio.Divide(histo2)
h_ratio.SetLineColor(ROOT.kBlack)
h_ratio.SetLineWidth(2)
h_ratio.SetMarkerStyle(21)
h_ratio.GetYaxis().SetNdivisions(505)
h_ratio.GetYaxis().SetTitle("ratio")
h_ratio.SetMarkerSize(0.5)
h_ratio.Draw("ep")
h_ratio.SetTitle("")
can.SetGridx()
can.Update()
can.SaveAs("/afs/hephy.at/user/e/easilar/www/comp"+plot1name+plot2name+".png")
