import ROOT

filename1 = '/data/easilar/results2014/rootfiles/PhiSil.root'
#filename1 = '/data/easilar/results2014/rootfiles/DiLepEffht500met250njet3.root'
#filename2 = '/data/easilar/results2014/rootfiles/DiLepEff110ht500met250njet3.root'
#filename3 = '/data/easilar/results2014/rootfiles/DiLepEff09ht500met250njet3.root'
#plot1 = 'h_GenDeltaPhi' 
#plot2 = 'h_DeltaPhi'
#plot3 = 'h_DeltaPhi'
#plot4 = 'h_DeltaPhi'
plot1 = 'hDeltaPhi' 
plot2 = 'hDeltaPhiPred'
plot3 = 'hDeltaPhiPred110'
plot4 = 'hDeltaPhiPred09'
plot1name = plot1.split('h')[1]
plot2name = plot2.split('h')[1]

File1 = ROOT.TFile(filename1)
#File2 = ROOT.TFile(filename2)
#File3 = ROOT.TFile(filename3)
histo1 = File1.Get(plot1)
histo2 = File1.Get(plot2)
histo3 = File1.Get(plot3)
histo4 = File1.Get(plot4)

can = ROOT.TCanvas("c","Comparison of "+plot1name+"and"+plot2name,800,800)
Pad1 = ROOT.TPad("Pad1", "Pad1", 0, 0.3, 1, 1.0)
Pad1.SetLogy()
Pad1.SetBottomMargin(0)
Pad1.SetGridx()
Pad1.Draw()
Pad1.cd()
histo1.SetTitle("DeltaPhi Eff Unceartinity Had Tau")
histo1.SetStats(0)
histo1.SetLineColor(ROOT.kBlack)
histo1.SetLineWidth(2)
histo1.SetAxisRange(0.1, 5*(histo1.GetMaximum()),"Y")
histo1.Draw()
histo2.SetStats(0)
histo2.SetLineColor(ROOT.kRed+1)
histo2.SetLineWidth(2)
histo2.Draw('same')
histo3.SetStats(0)
histo3.SetLineColor(ROOT.kAzure+10)
histo3.SetLineStyle(2)
histo3.Draw('same')
histo4.SetStats(0)
histo4.SetLineColor(ROOT.kAzure)
histo4.SetLineStyle(2)
histo4.Draw('same')
histo4.GetYaxis().SetLabelSize(0.)
histo1.GetYaxis().SetTitle("# of Events")
histo1.GetYaxis().SetTitleSize(20)
histo1.GetYaxis().SetTitleFont(43)
histo1.GetYaxis().SetTitleOffset(1.55)
histo1.GetYaxis().SetLabelFont(43)
histo1.GetYaxis().SetLabelSize(15)
#axis = ROOT.TGaxis( -5, 20, -5, 220, 20,220,510,"")
#axis.SetLabelFont(43)
#axis.SetLabelSize(15)
#axis.Draw()
leg = ROOT.TLegend(0.7,0.6,0.9,0.77)
leg.AddEntry(histo2, "Predicted","l")
leg.AddEntry(histo1, "Truth","l")
leg.AddEntry(histo3, "1.1*Eff Pred","l")
leg.AddEntry(histo4, "0.9*Eff Pred","l")
leg.SetFillColor(0)
leg.Draw()
can.cd()
Pad2 = ROOT.TPad("Pad2", "Pad2",  0, 0.05, 1, 0.3)
Pad2.SetTopMargin(0)
Pad2.SetBottomMargin(0.2)
Pad2.SetGridx()
Pad2.Draw()
Pad2.cd()
h_ratio = histo1.Clone("h_ratio")
h_ratio.SetLineColor(ROOT.kBlack)
h_ratio.SetLineWidth(2)
h_ratio.SetMinimum(0.0)
h_ratio.SetMaximum(2.0)
h_ratio.Sumw2()
h_ratio.SetStats(0)
h_ratio.Divide(histo2)
h_ratio.SetMarkerStyle(21)
#h_ratio.SetMarkerSize(0.5)
h_ratio.Draw("ep")
h_ratio.SetTitle("")
h_ratio.GetYaxis().SetTitle("ratio Truth/Pred ")
h_ratio.GetYaxis().SetNdivisions(505)
h_ratio.GetYaxis().SetTitleSize(20)
h_ratio.GetYaxis().SetTitleFont(43)
h_ratio.GetYaxis().SetTitleOffset(1.55)
h_ratio.GetYaxis().SetLabelFont(43)
h_ratio.GetYaxis().SetLabelSize(15)
h_ratio.GetXaxis().SetTitleSize(20)
h_ratio.GetXaxis().SetTitleFont(43)
h_ratio.GetXaxis().SetTitleOffset(4.)
h_ratio.GetXaxis().SetLabelFont(43)
h_ratio.GetXaxis().SetLabelSize(15)
#can.SetGridx()
#can.Update()
#can.SaveAs("/afs/hephy.at/user/e/easilar/www/27Oct/HadTau_HT750_met250_njets_3_NoBtagCut"+plot1name+".png")
                                              
ePred = ROOT.Double()
eTruth = ROOT.Double()
ePred110 = ROOT.Double()
Pred = histo2.IntegralAndError(0,histo2.GetNbinsX(),ePred)
Truth = histo1.IntegralAndError(0,histo1.GetNbinsX(),eTruth)
Pred110 = histo3.IntegralAndError(0,histo3.GetNbinsX(),eTruth)
print 'Prediction yield:', Pred
print 'Truth yield:', Truth
print 'ePred :', ePred
print 'eTruth:', eTruth                  
print 'Pred:' , Pred, '+-',ePred,'(stat)+-', Pred110-Pred,'Leff' 
print 'Truth:' , Truth, '+-',eTruth,'(stat)+-'
                           
