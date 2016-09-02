import ROOT
import os, sys, copy
import pickle, operator

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *

TTJets_DiLep = {\
"name" : "TTJets_DiLep",
"chunkString":"TTJets_DiLepton",
"skimAnalyzerDir":'',
"rootFileLocation":'METtree.root',
'dir' : "/afs/hephy.at/work/d/dspitzbart/MET/CMSSW_8_0_11/src/CMGTools/ObjectStudies/cfg/TT_Dilep/",
'isData':False
}

DYJets_M50 = {\
"name" : "DYJets_M50",
"chunkString":"DYJetsToLL_M50",
"skimAnalyzerDir":'',
"rootFileLocation":'METtree.root',
'dir' : "/afs/hephy.at/work/d/dspitzbart/MET/CMSSW_8_0_11/src/CMGTools/ObjectStudies/cfg/DYJetsToLL_M50/",
'isData':False
}

DoubleMuon_Run2016B = {\
"name": "DoubleMuon_Run2016B",
"chunkString":"DoubleMuon_Run2016B_PromptReco_v2",
"skimAnalyzerDir":'',
"rootFileLocation":'METtree.root',
'dir' : "/afs/hephy.at/work/d/dspitzbart/MET/CMSSW_8_0_11/src/CMGTools/ObjectStudies/cfg/DoubleMuon_v2/",
'isData':True
}

DoubleMuon_Run2016C = {\
"name": "DoubleMuon_Run2016C",
"chunkString":"DoubleMuon_Run2016C_PromptReco_v2",
"skimAnalyzerDir":'',
"rootFileLocation":'METtree.root',
'dir' : "/afs/hephy.at/work/d/dspitzbart/MET/CMSSW_8_0_11/src/CMGTools/ObjectStudies/cfg/DoubleMuon_v2/",
'isData':True
}

DoubleMuon_Run2016D = {\
"name": "DoubleMuon_Run2016D",
"chunkString":"DoubleMuon_Run2016D_PromptReco_v2",
"skimAnalyzerDir":'',
"rootFileLocation":'METtree.root',
'dir' : "/afs/hephy.at/work/d/dspitzbart/MET/CMSSW_8_0_11/src/CMGTools/ObjectStudies/cfg/DoubleMuon_v2/",
'isData':True
}

data = [DoubleMuon_Run2016B, DoubleMuon_Run2016C, DoubleMuon_Run2016D]
for d in data:
  d['chunks'], d['nEvents'] = getChunks(d)

Data = {}
Data['chain'] = getChain(DoubleMuon_Run2016B['chunks']+DoubleMuon_Run2016C['chunks']+DoubleMuon_Run2016D['chunks'], histname='', treeName='METtree')
Data['hist'] = ROOT.TH1F('Data','',50,0,100)
Data['chain'].Draw('met_sig>>Data','(1)','goff')

TTJets_DiLep['chunks'], TTJets_DiLep['nEvents'] = getChunks(TTJets_DiLep)
TTJets_DiLep['chain'] = getChain(TTJets_DiLep['chunks'], histname='', treeName='METtree')
TTJets_DiLep['color'] = ROOT.kRed-6

DYJets_M50['chunks'], DYJets_M50['nEvents'] = getChunks(DYJets_M50)
DYJets_M50['chain'] = getChain(DYJets_M50['chunks'], histname='', treeName='METtree')
DYJets_M50['color'] = ROOT.kYellow

bkgSamples = [TTJets_DiLep,DYJets_M50]

data_int = Data['hist'].Integral()

targetLumi = 1.

totalH = ROOT.TH1F('totalH','',50,0,100)

bins = 50
maxSig = 100

for s in bkgSamples:
  s['hist'] = ROOT.TH1F(s['name'],'',bins,0,maxSig)
  s['chain'].Draw('met_sig>>'+s['name'],str(targetLumi)+'*genWeight*xsec/'+str(s['nEvents']),'goff')
  s['hist'].SetFillColor(s['color'])
  s['hist'].SetLineWidth(2)
  #stack.Add(s['hist'])
  totalH.Add(s['hist'])

total_int = totalH.Integral()

totalH.Scale(data_int/total_int)
const = totalH.GetBinContent(1)

stack = ROOT.THStack()
for s in bkgSamples:
  s['hist'].Scale(data_int/total_int)
  stack.Add(s['hist'])

const = const/ROOT.TMath.Exp(-(float(maxSig)/bins)/4.)
chi2_2 = ROOT.TF1("chi22","TMath::Exp(-x/2)*"+str(const),0,100)

can = ROOT.TCanvas('can','can',700,700)

pad1=ROOT.TPad("pad1","MyTitle",0.,0.3,1.,1.)
pad1.SetLeftMargin(0.15)
pad1.SetBottomMargin(0.02)
pad1.Draw()
pad1.cd()

pad1.SetLogy()

stack.Draw('hist')
stack.SetMinimum(0.1)
stack.SetMaximum(10000)
stack.GetXaxis().SetLabelSize(0)
stack.GetYaxis().SetTitle('Events')

Data['hist'].Draw('e0p same')

chi2_2.SetLineColor(ROOT.kBlack)
chi2_2.SetLineWidth(2)
chi2_2.Draw('same')

leg = ROOT.TLegend(0.75,0.65,0.95,0.92)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(0)
leg.SetTextSize(0.045)

leg.AddEntry(chi2_2,'#chi^{2} d.o.f 2','l')
leg.AddEntry(Data['hist'],'Data')
leg.AddEntry(TTJets_DiLep['hist'],'Top','f')
leg.AddEntry(DYJets_M50['hist'],'Drell Yan','f')

leg.Draw()

can.cd()

pad2=ROOT.TPad("pad2","datavsMC",0.,0.,1.,.3)
pad2.SetLeftMargin(0.15)
pad2.SetBottomMargin(0.3)
pad2.SetTopMargin(0.04)
#pad2.SetGrid()
pad2.Draw()
pad2.cd()

ratio = ROOT.TH1F('ratio','',bins,0,maxSig)
ratio.Sumw2()
ratio = Data['hist'].Clone()
ratio.Divide(totalH)
ratio.SetLineColor(ROOT.kBlack)
ratio.SetMarkerStyle(8)
ratio.SetMarkerSize(1)
ratio.SetLineWidth(0)
ratio.GetXaxis().SetTitle('')

ratio.SetMaximum(2.0)
ratio.SetMinimum(0.)

ratio.GetXaxis().SetTitle('E_{T}^{miss} Significance')
ratio.GetXaxis().SetTitleSize(0.12)
ratio.GetXaxis().SetLabelSize(0.12)

ratio.GetYaxis().SetLabelSize(0.12)
ratio.GetYaxis().SetNdivisions(108)

ratio.Draw('e0p')

one = ROOT.TF1("one","1",0,100)
one.SetLineColor(ROOT.kRed+1)
one.SetLineWidth(2)
one.Draw('same')

ratio.Draw('e0p same')
