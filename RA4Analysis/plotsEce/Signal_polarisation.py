import ROOT
import pickle
from array import array
import operator
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.cmgObjectSelection import *
from Workspace.RA4Analysis.signalRegions import *
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.general_config import *
#from math import sqrt, pi
from math import *
ROOT.TH1F().SetDefaultSumw2()

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/WPolarizationVariation.C+")

hWlep =  ROOT.TH1D("hWlep","hWlep", 20,-1,1)
hchiW = ROOT.TH1D("hchiW","hchiW", 20,-1,1)

signal = SMS_T5qqqqVV_TuneCUETP8M1
s_chain = getChain(signal[1900][100],histname='')
#s_chain = getChain(signal[1300][1000],histname='')

for i in range(s_chain.GetEntries()):
  s_chain.GetEntry(i)
  c= s_chain
  weight = c.GetLeaf('weight').GetValue()
  genPartAll = [getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], j) for j in range(int(c.GetLeaf('nGenPart').GetValue()))]
  lepton = filter(lambda l:abs(l['pdgId']) in [11,13,15], genPartAll)
  lFromW = filter(lambda w:abs(w['motherId'])==24, lepton)
  wboson = filter(lambda w:abs(w['pdgId'])==24, genPartAll)
  wFromChi = filter(lambda chi:abs(chi['motherId'])==1000024, wboson)
  #print "n W = n w from chi :" , len(wboson) , len(wFromChi) 
  if not len(lFromW)==1: continue
  #print 10*"*"
  #print "number of lepton from W :" , len (lFromW)
  i = 0 
  genW = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], int(lFromW[i]['motherIndex']))
  W = ROOT.TLorentzVector()
  W.SetPtEtaPhiM(genW['pt'],genW['eta'],genW['phi'],genW['mass'])
  lep = ROOT.TLorentzVector()
  lep.SetPtEtaPhiM(lFromW[i]['pt'],lFromW[i]['eta'],lFromW[i]['phi'],lFromW[i]['mass'])
  p4lepton = ROOT.LorentzVector(lep.Px(),lep.Py(),lep.Pz(),lep.E())
  p4w = ROOT.LorentzVector(W.Px(),W.Py(),W.Pz(),W.E())
  #print "W : " , W.Px(),W.Py(),W.Pz(),W.E()    
  #print "lep : " , lep.Px(),lep.Py(),lep.Pz(),lep.E()

  cosTheta_Wlep = ROOT.WjetPolarizationAngle(p4w, p4lepton )
  #print cosTheta_Wlep

  hWlep.Fill(cosTheta_Wlep,weight*(36.5/3))

  chi = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], int(genW['motherIndex']))
  vchi = ROOT.TLorentzVector()
  vchi.SetPtEtaPhiM(chi['pt'],chi['eta'],chi['phi'],chi['mass'])
  p4chi = ROOT.LorentzVector(vchi.Px(),vchi.Py(),vchi.Pz(),vchi.E())
  

  cosTheta_ChiW = ROOT.WjetPolarizationAngle(p4chi, p4w )
  #print cosTheta_ChiW

  hchiW.Fill(cosTheta_ChiW,weight*(36.5/3))

histos = [hchiW , hWlep]  

cb = ROOT.TCanvas("cb","cb",800,800)
cb.cd()
cb.SetRightMargin(3)
tex = ROOT.TLatex()
leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
leg.SetBorderSize(1)
hchiW.SetLineColor(ROOT.kBlue)
hWlep.SetLineColor(ROOT.kRed)
hchiW.SetMarkerColor(ROOT.kBlue)
hWlep.SetMarkerColor(ROOT.kRed)
for histo in histos:
  histo.GetXaxis().SetTitle("cos #theta")
  histo.GetYaxis().SetTitle("Events")
  histo.SetMinimum(0)
  #histo.SetMaximum(100)
  histo.SetMaximum(5)
  leg.AddEntry(histo,histo.GetName(),"F")
  histo.Draw("Histosame")
  histo.Draw("E1Psame")

leg.Draw()
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.SetTextAlign(11)
latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Simulation}")
latex.DrawLatex(0.6,0.958,"#bf{L=36 fb^{-1} (13 TeV)}")
latex.DrawLatex(0.55,0.6,"T5qqqqWW 1.9/0.1")
path = "/afs/hephy.at/user/e/easilar/www/Moriond2017/signal_Polarisation/"
if not os.path.exists(path):
  os.makedirs(path)

cb.SaveAs(path+'_costheta_1900_100_.png')
cb.SaveAs(path+'_costheta_1900_100_.pdf')
cb.SaveAs(path+'_costheta_1900_100_.root')


