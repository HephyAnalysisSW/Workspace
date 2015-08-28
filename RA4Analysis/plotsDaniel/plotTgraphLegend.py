import ROOT
import os, sys, copy
import pickle

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

path = '/afs/hephy.at/user/d/dspitzbart/www/Spring15/'
#t = ROOT.TFile(path+'WjetScatterTotalGenLT/scatter_st350-450_ht750-1000_njetEq5_nbtagEq0.root')
t = ROOT.TFile(path+'WjetScatterEnhancedStatHighDPhi/scatter_st350-450_ht750-1000_njetEq5_nbtagEq0.root')
#t = ROOT.TFile(path+'WjetScatterEnhancedStatHighDPhi/scatter_st250-350_ht1000_njetEq3_nbtagEq0.root')

c = t.Get('c1')
c.Draw()

dot = []

colors = [ROOT.kBlue+2, ROOT.kBlue-4, ROOT.kBlue-7, ROOT.kBlue-9, ROOT.kCyan-9, ROOT.kCyan-6, ROOT.kCyan-2,ROOT.kGreen+3,ROOT.kGreen-2,ROOT.kGreen-6,ROOT.kGreen-7, ROOT.kOrange-4, ROOT.kOrange+1, ROOT.kOrange+8, ROOT.kRed, ROOT.kRed+1]
#colors2 = [colors[5], colors[13], colors[8], colors[1]]
strings = ["#geq 450", "[350,450)", "[250,350)", "[0, 250)"]



tex =  ROOT.TLatex()
tex.SetNDC()
tex.SetTextSize(0.04)
tex.SetTextAlign(11)

#tex.DrawLatex(0.71,0.85,"L_{T}^{true} [GeV]")
tex.DrawLatex(0.6,0.87,"#Delta#Phi(W,l) > 1.")

for t in range(16):
  dot.append(ROOT.TGraph())
  #dot[-1].SetPoint(0,450,550-40*t)
  dot[-1].SetPoint(0,518,550-31.5*t)
  #dot[-1].SetPoint(0,435,458-26.3*t)
  dot[-1].SetMarkerStyle(20)
  dot[-1].SetMarkerSize(2.5)#3
  dot[-1].SetMarkerColor(colors[t])
  dot[-1].Draw('p same')
  #tex.DrawLatex(0.75,0.8-0.049*t,strings[t])
  tex.DrawLatex(0.83,0.8-0.039*t,'['+str(t*0.2)+', '+str((t+1)*0.2)+')')
  
  


