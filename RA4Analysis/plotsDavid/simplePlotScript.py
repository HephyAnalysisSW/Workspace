import ROOT
ROOT.gROOT.ProcessLine('.L /afs/hephy.at/scratch/d/dhandl/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
import os, copy, sys

from Workspace.HEPHYPythonTools.helpers import getChain
from Workspace.RA4Analysis.cmgTuplesPostProcessed import *
c = getChain(ttJetsCSA1450ns)

cut = "singleMuonic&&nBJetLoose25==0&&nJet>=6"
prefix = 'singleMuonic_nBJetLoose_0_nJet>5'

allVariables = []

met = {'name':'mymet', 'varString':"met_pt", 'legendName':'#slash{E}_{T}', 'binning':[60,0,1500]}

allVariables.append(met)

def getVarValue(c, var, n=0):         #A general method to get the value of a variable from a chain after chain.GetEntry(i) has been called
  varNameHisto = var
  leaf = var
  #leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  else:
    return float('nan')

#Create Chain with Data
#data = ROOT.TChain("Events")
#data.Add("/data/schoef/convertedTuples_v21/copyMET/Mu/data/histo_data.root")
#data.Add("/data/schoef/convertedTuples_v21/copyMET/Ele/data/histo_data.root")

#Create Chain with MC
#QCD_MC = ROOT.TChain("Events")
#QCD_MC.Add("/data/schoef/convertedTuples_v21/copyMET/Mu/QCD/histo_QCD.root")
#QCD_MC.Add("/data/schoef/convertedTuples_v21/copyMET/Ele/QCD/histo_QCD.root")

#SINGLETOP_MC = ROOT.TChain("Events")
#SINGLETOP_MC.Add("/data/schoef/convertedTuples_v21/copyMET/Mu/singleTop/histo_singleTop.root")
#SINGLETOP_MC.Add("/data/schoef/convertedTuples_v21/copyMET/Ele/singleTop/histo_singleTop.root")

WJETS_MC = ROOT.TChain("Events")
WJETS_MC.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/WJetsToLNu_HT100to200/WJetsToLNu_HT100to200_0.root")
WJETS_MC.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/WJetsToLNu_HT200to400/WJetsToLNu_HT200to400_0.root")
WJETS_MC.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/WJetsToLNu_HT400to600/WJetsToLNu_HT400to600_0.root")
WJETS_MC.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/WJetsToLNu_HT600toInf/WJetsToLNu_HT600toInf_0.root")

TTJETSCSA14_MC = ROOT.TChain("Events")
TTJETSCSA14_MC.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_0.root")
TTJETSCSA14_MC.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_1.root")
TTJETSCSA14_MC.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_2.root")
TTJETSCSA14_MC.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_3.root")
TTJETSCSA14_MC.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_4.root")
TTJETSCSA14_MC.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_5.root")
TTJETSCSA14_MC.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_6.root")

#Create Chain with Signal
SIGNAL1200_1000 = ROOT.TChain("Events")
SIGNAL1200_1000.Add("/data/schoef/cmgTuples/postProcessed_v0/singleLepton/T5Full_1200_1000_800/T5Full_1200_1000_800_0.root")

SIGNAL1500_800 = ROOT.TChain("Events")
SIGNAL1500_800.Add('/data/schoef/cmgTuples/postProcessed_v0/singleLepton/T5Full_1500_800_100/T5Full_1500_800_100_0.root')

#Define two samples; I used dicts. Adapt as you need.
#data        = {"name":"Data",          "chain":data,                    "weight":1,        "color":ROOT.kBlack}
#qcd_mc      = {"name":"QCD",           "chain":QCD_MC,                  "weight":"weight", "color":ROOT.kBlue - 4}
#singletop_mc     = {"name":"singleTop",     "chain":SINGLETOP_MC,            "weight":"weight", "color":ROOT.kOrange + 4}
wjets_mc = {"name":"WJets", "chain":WJETS_MC,        "weight":"weight", "color":ROOT.kYellow}
ttjets_mc  = {"name":"TTJets", "chain":TTJETSCSA14_MC,         "weight":"weight", "color":ROOT.kRed + 1}
signal1200 = {'name':'T5Full_1200_1000', 'chain':SIGNAL1200_1000, 'weight':'weight', 'color':ROOT.kBlack}
signal1500 = {'name':'T5Full_1500_800', 'chain':SIGNAL1500_800, 'weight':'weight', 'color':ROOT.kBlue+2}

allMCSamples = [wjets_mc, ttjets_mc]
#extraSamples = [data]
signals = [signal1200, signal1500]

histos = {}

for sample in allMCSamples + signals: #Loop over samples
  histos[sample['name']] = {}

  for var in allVariables:
    histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], *var['binning'])

  sample["chain"].Draw(">>eList",cut) #Get the event list 'eList' which has all the events satisfying the cut
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut

  for i in range(number_events): #Loop over those events
    sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
    for var in allVariables: 
      varValue = getVarValue(sample["chain"], var['varString'])   #Get the value of the variable
      weight = 1
      if sample.has_key('weight'):
        if type(sample['weight'])==type(''):
          weight = getVarValue(sample['chain'], sample['weight'])
        else:
          weight = sample['weight']
      histos[sample['name']][var['name']].Fill(varValue, weight)
  del elist

for sample in signals:
  for var in allVariables:
    if histos[sample['name']][var['name']].Integral()>0:
      histos[sample['name']][var['name']].Scale(histos['TTJets'][var['name']].Integral()/histos[sample['name']][var['name']].Integral())

#Define and stack the histograms...
for var in allVariables:
  canvas = ROOT.TCanvas(var['name']+' Window',var['name']+' Window')
  canvas.SetLogy()
  l = ROOT.TLegend(0.6,0.7,0.95,0.95)
  l.SetFillColor(0)
  l.SetBorderSize(1)
  l.SetShadowColor(ROOT.kWhite)
  stack = ROOT.THStack('stack','Stacked Histograms')
  #stack.SetMaximum(4*10**4)

  #text = ROOT.TLatex()
  #text.SetTextAlign(12)
  #text.SetTextSizePixels(15)
  #text.SetTextFont(22)
  #text.SetNDC()

  for sample in allMCSamples:
    histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
    histos[sample['name']][var['name']].SetFillColor(sample['color'])
    histos[sample['name']][var['name']].SetMarkerStyle(0)
    histos[sample['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
    histos[sample['name']][var['name']].GetYaxis().SetTitle('Number of Events /'+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
    histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.04)
    histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
    stack.Add(histos[sample['name']][var['name']])
    l.AddEntry(histos[sample['name']][var['name']], sample['name'],'f')

  stack.Draw()
  stack.GetXaxis().SetTitle(var['legendName'])
  stack.GetYaxis().SetTitle('Number of Events /'+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')

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
  #text.DrawLatex(0.2,.9,"CMS Collaboration")
  #text.DrawLatex(0.2,0.85,"19.7 fb^{-1}, #sqrt{s}=8 TeV")

  #canvas.Print('/afs/hephy.at/user/d/dhandl/www/png/simplemetPlot/'+prefix+'_'+var['name']+'.png')
  #canvas.Print('/afs/hephy.at/user/d/dhandl/www/png/simplemetPlot/'+prefix+'_'+var['name']+'.root')
  #canvas.Print('/afs/hephy.at/user/d/dhandl/www/png/simplemetPlot/'+prefix+'_'+var['name']+'.pdf')

