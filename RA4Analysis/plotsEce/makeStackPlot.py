import ROOT
from math import *
parameter = ['Mt','WPT','StLep','njets','met','ht','muCharge']
for p in range(len(parameter)):
  print 'Parameter',parameter[p]
  filename = '/data/easilar/results2014/rootfiles/Signal_Bkg0'+str(parameter[p])+'.root'
  plot1 = 'h_ttJets'
  plot2 = 'h_WJets'
  plot3 = 'h_T51200'
  plot4 = 'h_T51500'
  plot1name = plot1.split('_')[1]
  plot2name = plot2.split('_')[1]
  plot3name = plot3.split('_')[1]
  plot4name = plot4.split('_')[1]

  File = ROOT.TFile(filename)
  histo1 = File.Get(plot1)
  histo2 = File.Get(plot2)
  histo3 = File.Get(plot3)
  histo4 = File.Get(plot4)

  h_Stack = ROOT.THStack('h_Stack',parameter[p])
  histo1.SetFillColor(ROOT.kAzure+10)
  histo2.SetFillColor(ROOT.kAzure+5)
  h_Stack.Add(histo1)
  h_Stack.Add(histo2)

  can = ROOT.TCanvas(parameter[p])
  can.cd()
  h_Stack.Draw()
  histo3.SetLineColor(ROOT.kBlue-3)
  histo3.SetLineWidth(2)
  histo3.Draw('same')
  histo4.SetLineColor(ROOT.kRed+1)
  histo4.SetLineWidth(2)
  histo4.Draw('same')
  leg = ROOT.TLegend(0.8,0.8,1,1)
  leg.AddEntry(histo1, "ttjets","f")
  leg.AddEntry(histo2, "Wjets","f")
  leg.AddEntry(histo3, "1200","f")
  leg.AddEntry(histo4, "1500","f")
  leg.SetFillColor(0)
  leg.Draw()
  can.SetLogy()
  can.Update()
  can.SaveAs("/afs/hephy.at/user/e/easilar/www/21"+parameter[p]+plot1name+plot2name+plot3name+plot4name+"0.png")

  relUncert = 0.2
  Signal_Yield = histo4.Integral()
  Bkg_Yield = histo2.Integral() + histo1.Integral() 
  FOM = Signal_Yield/sqrt((relUncert*Bkg_Yield)**2+Bkg_Yield) 
  print 'Signal:', Signal_Yield
  print 'Bkg:', Bkg_Yield
  print 'FOM:', FOM
