import ROOT
ROOT.gROOT.ProcessLine('.L /afs/hephy.at/scratch/d/dhandl/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
import os, copy, sys

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi
from Workspace.RA4Analysis.cmgTuplesPostProcessed import *

#Create Chain with MC
WJETS_MC = getChain(WJetsHTToLNu)
TTJETSCSA14_MC = getChain(ttJetsCSA1450ns)

#Create Chain with Signal
SIGNAL1200_1000 = getChain(T5Full_1200_1000_800)
SIGNAL1500_800 = getChain(T5Full_1500_800_100)

#defining the cut
cut = "htJet40ja>400&&nBJetLoose25==0&&nJet>=6"

prefix = 'ht>400_nBJetLoose_0_nJet>5'
isoTrackPrefix = 'isoTrpt<15_isoTrpdg_211_isoTrdz<005'
wwwDir = 'testpng/'

allVariables = []

#met = {'name':'mymet', 'varString':"met_pt", 'legendName':'#slash{E}_{T}', 'binning':[30,0,1500]}
#isoTrack = {'name':'myisoTrack', 'legendName':'isoTrack', 'binning':[10,0,10]}
relIso = {'name':'myrelIso', 'legendName':'relIso', 'binning':[50,0,0.5]}

#allVariables.append(met)
#allVariables.append(isoTrack)
allVariables.append(relIso)

#def getVarValue(c, var, n=0):         #A general method to get the value of a variable from a chain after chain.GetEntry(i) has been called
#  varNameHisto = var
#  leaf = var
  #leaf = c.GetAlias(varNameHisto)
#  if leaf!='':
#    return c.GetLeaf(leaf).GetValue(n)
#  else:
#    return float('nan')

#Define two samples; I used dicts. Adapt as you need.
#data        = {"name":"Data",          "chain":data,                    "weight":1,        "color":ROOT.kBlack}
#qcd_mc      = {"name":"QCD",           "chain":QCD_MC,                  "weight":"weight", "color":ROOT.kBlue - 4}
#singletop_mc     = {"name":"singleTop",     "chain":SINGLETOP_MC,            "weight":"weight", "color":ROOT.kOrange + 4}
wjets_mc = {"name":"WJets", "chain":WJETS_MC,        "weight":"weight", "color":ROOT.kYellow}
ttjets_mc  = {"name":"TTJets", "chain":TTJETSCSA14_MC,         "weight":"weight", "color":ROOT.kRed - 3}
signal1200 = {'name':'T5Full_1200_1000_800', 'chain':SIGNAL1200_1000, 'weight':'weight', 'color':ROOT.kBlack}
signal1500 = {'name':'T5Full_1500_800_100', 'chain':SIGNAL1500_800, 'weight':'weight', 'color':ROOT.kBlue+2}

bkgSamples = [wjets_mc, ttjets_mc]
#extraSamples = [data]
signals = [signal1200, signal1500]

histos = {}

for sample in bkgSamples + signals: #Loop over samples
  histos[sample['name']] = {}

  for var in allVariables:
		histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], *var['binning'])
		histos[sample['name']][var['name']].Reset()
		#sample['chain'].Draw("Sum$(isoTrack_pt<15&&abs(isoTrack_pdgId)==211&&abs(isoTrack_dz)<0.05)"+">>"+sample["name"]+"_"+var["name"])#weight missing!
		#sample['chain'].Draw(var['varString']+">>"+sample['name']+'_'+var['name'], sample["weight"]+"*("+cut+")")
  	
  sample["chain"].Draw(">>eList",cut) #Get the event list 'eList' which has all the events satisfying the cut
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut

#Event loop
  for i in range(number_events): #Loop over those events
    sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
    number_isoTracks = getVarValue(sample['chain'],'nisoTrack')
#Track loop
#    if int(number_isoTracks)>1:
#      pt = sample['chain'].GetLeaf('isoTrack_pt').GetValue(1)
#      print 'Event number',i,' : ',int(number_isoTracks),' : ',pt

    for n in range(int(number_isoTracks)):
    #calculate relIso
      absIso = sample['chain'].GetLeaf('isoTrack_absIso').GetValue(n)
      trackpt = sample['chain'].GetLeaf('isoTrack_pt').GetValue(n)
      if absIso!=0 and trackpt!=0:
        relIsoVar = absIso/trackpt       
#      for var in allVariables: 
#      varValue = getVarValue(sample["chain"], var['varString'])   #Get the value of the variable
      weight = 1
      if sample.has_key('weight'):
        if type(sample['weight'])==type(''):
          weight = getVarValue(sample['chain'], sample['weight'])
        else:
          weight = sample['weight']
      histos[sample['name']][var['name']].Fill(relIsoVar, weight)
  del elist

#for sample in signals:
#  for var in allVariables:
#    if histos[sample['name']][var['name']].Integral()>0:
#      histos[sample['name']][var['name']].Scale(histos['TTJets'][var['name']].Integral()/histos[sample['name']][var['name']].Integral())

#Define and stack the histograms...
for var in allVariables:
  canvas = ROOT.TCanvas(var['name']+' Window',var['name']+' Window')
  pad1 = ROOT.TPad(var['name']+' Pad',var['name']+' Pad',0.,0.3,1.,1.)
  pad1.SetBottomMargin(0)
  pad1.SetLogy()
  pad1.Draw()
  pad1.cd()
  l = ROOT.TLegend(0.6,0.7,0.95,0.95)
  l.SetFillColor(0)
  l.SetBorderSize(1)
  l.SetShadowColor(ROOT.kWhite)
  stack = ROOT.THStack('stack','Stacked Histograms')
  #stack.SetMaximum(4*10**4)

  #text = ROOT.TLatex()
  #text.SetTextAlign(12)
	#text.SetNDC()
  #text.SetTextSizePixels(15) 

  for sample in bkgSamples:
    histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
    histos[sample['name']][var['name']].SetFillColor(sample['color'])
    histos[sample['name']][var['name']].SetMarkerStyle(0)
    histos[sample['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
    histos[sample['name']][var['name']].GetYaxis().SetTitle('Events')# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
    histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.04)
    histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
    stack.Add(histos[sample['name']][var['name']])
    l.AddEntry(histos[sample['name']][var['name']], sample['name'],'f')

  stack.Draw()
  stack.GetXaxis().SetTitle(var['legendName'])
  stack.GetYaxis().SetTitle('Events')# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')

  #for extra in extraSamples:
  #  histos[extra['name']][var['name']].SetMarkerStyle(21)
  #  histos[extra['name']][var['name']].Draw('same E')
  #  l.AddEntry(histos[extra['name']][var['name']],extra['name'])

  for sig in signals:
    histos[sig['name']][var['name']].SetLineColor(sig['color'])
    histos[sig['name']][var['name']].SetLineWidth(2)
    histos[sig['name']][var['name']].SetFillColor(0)
    histos[sig['name']][var['name']].SetMarkerStyle(0)
    histos[sig['name']][var['name']].Draw('same')
    l.AddEntry(histos[sig['name']][var['name']], sig['name'])

  l.Draw()
  #text.DrawLatex(0.2,.9,"CMS Simulation")
  #text.DrawLatex(0.88,0.9,"L=2 fb^{-1} (13 TeV)")

  canvas.cd()
  pad2 = ROOT.TPad(var['name']+" Ratio",var['name']+" Ratio",0.,0.,1.,0.3)
  pad2.SetTopMargin(0)
  pad2.SetBottomMargin(0.3)
  pad2.Draw()
  pad2.cd()
  histo_merge = ROOT.TH1F(var['name']+" Ratio",var['name']+" Ratio",*var['binning'])
  histo_merge.Merge(stack.GetHists())
  h_ratio = histos['T5Full_1200_1000_800'][var['name']].Clone('h_ratio')
  h_ratio.SetLineColor(signal1200['color'])
  h_ratio.SetLineWidth(2)
  h_ratio.Sumw2()
  h_ratio.SetStats(0)
  h_ratio.Divide(histo_merge)
  h_ratio.SetMarkerStyle(21)
  h_ratio.Draw("ep")
  h_ratio.GetXaxis().SetTitle(var['legendName'])
  h_ratio.GetYaxis().SetTitle("Signal/MC")
  h_ratio.GetYaxis().SetNdivisions(505)
  h_ratio.GetYaxis().SetTitleSize(23)
  h_ratio.GetYaxis().SetTitleFont(43)
  h_ratio.GetYaxis().SetTitleOffset(1.8)
  h_ratio.GetYaxis().SetLabelFont(43)
  h_ratio.GetYaxis().SetLabelSize(20)
  h_ratio.GetYaxis().SetLabelOffset(0.015)
  h_ratio.GetXaxis().SetTitleSize(23)
  h_ratio.GetXaxis().SetTitleFont(43)
  h_ratio.GetXaxis().SetTitleOffset(3.4)
  h_ratio.GetXaxis().SetLabelFont(43)
  h_ratio.GetXaxis().SetLabelSize(20)
  h_ratio.GetXaxis().SetLabelOffset(0.04)

#  h_ratio2 = ROOT.TH1F(var['name']+" Ratio",var['name']+" Ratio",*var['binning'])
#  h_ratio2.Merge(stack.GetHists())
  h_ratio2 = histos['T5Full_1500_800_100'][var['name']].Clone('h_ratio2')
  h_ratio2.SetLineColor(signal1500['color'])
  h_ratio2.SetLineWidth(2)
  h_ratio2.Sumw2()
  h_ratio2.SetStats(0)
  h_ratio2.Divide(histo_merge)
  h_ratio2.SetMarkerStyle(21)
  h_ratio2.SetMarkerColor(ROOT.kBlue+2)
  h_ratio2.Draw("same")

  canvas.cd()
  canvas.Print('/afs/hephy.at/user/d/dhandl/www/'+wwwDir+prefix+'_'+var['name']+'.png')
  canvas.Print('/afs/hephy.at/user/d/dhandl/www/'+wwwDir+prefix+'_'+var['name']+'.root')
  canvas.Print('/afs/hephy.at/user/d/dhandl/www/'+wwwDir+prefix+'_'+var['name']+'.pdf')

