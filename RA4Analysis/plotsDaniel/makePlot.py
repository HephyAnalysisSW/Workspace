import ROOT
import os, sys, copy

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
from Workspace.RA4Analysis.helpers import *

binning=[30,50,500]

ht = 'htJet40ja>100'#&&htJet40ja<750'
st = '(met_pt+leptonPt)>150'#&&(met_pt+leptonPt)<350'
dPhiCut = 0.
dPhi = 'deltaPhi>'+str(dPhiCut)
cut = 'singleLeptonic==1&&Jet_pt[1]>=80&&nJet30>=6&&nBJetMediumCMVA30==0&&htJet30j>=500&&st>=200&&deltaPhi_Wl>1&&mt2w>0'#&&mt2w>0'#&&nBJetLoose25==0&&nJet>1'

varstring="mt2w"
plotDir='/afs/hephy.at/user/d/dspitzbart/www/'

#BKG Samples
WJETS = getChain(WJetsHTToLNu['hard'],histname='')
TTJETS = getChain(ttJets['hard'],histname='')
TTVH = getChain(TTVH['hard'],histname='')
SINGLETOP = getChain(singleTop['hard'],histname='')
DY = getChain(DY['hard'],histname='')
QCD = getChain(QCD['hard'],histname='')


#SIG Samples
SIG1 = getChain(SMS_T5qqqqWW_Gl1200_Chi1000_LSP800['hard'],histname='')
SIG2 = getChain(SMS_T5qqqqWW_Gl1500_Chi800_LSP100['hard'],histname='')

wjets = {"name":"W + Jets", "chain":WJETS, "weight":"weight", "color":color('wjets'), "histo":ROOT.TH1F("W + Jets", "sqrt(s)", *binning)}
ttjets = {"name":"t#bar{t} + Jets", "chain":TTJETS, "weight":"weight", "color":color('ttjets'), "histo":ROOT.TH1F("tt + Jets", "sqrt(s)", *binning)}
ttvh = {"name":"TTVH", "chain":TTVH, "weight":"weight", "color":color('ttvh'), "histo":ROOT.TH1F("ttvh", "sqrt(s)", *binning)}
singletop = {"name":"single top", "chain":SINGLETOP, "weight":"weight", "color":color('singletop'), "histo":ROOT.TH1F("single top", "sqrt(s)", *binning)}
dy = {"name":"Drell Yan", "chain":DY, "weight":"weight", "color":color('dy'), "histo":ROOT.TH1F("drell yan", "sqrt(s)", *binning)}
qcd = {"name":"QCD", "chain":QCD, "weight":"weight", "color":color('qcd'), "histo":ROOT.TH1F("qcd", "sqrt(s)", *binning)}



signal1 = {'name':'SMS_T5qqqqWW_Gl1200_Chi1000_LSP800', 'chain':SIG1, 'weight':'weight', 'color':ROOT.kBlack, "histo":ROOT.TH1F("Signal 1", "sqrt(s)", *binning)}
signal2 = {'name':'SMS_T5qqqqWW_Gl1500_Chi800_LSP100', 'chain':SIG2, 'weight':'weight', 'color':ROOT.kBlue+2, "histo":ROOT.TH1F("Signal 2", "sqrt(s)", *binning)}

sigSamples=[]
sigSamples.append(signal1)
sigSamples.append(signal2)

bkgSamples=[]
bkgSamples.append(qcd)
bkgSamples.append(ttvh)
bkgSamples.append(dy)
bkgSamples.append(singletop)
bkgSamples.append(wjets)
bkgSamples.append(ttjets)

h_Stack = ROOT.THStack('h_Stack',varstring)
h_Stack_S = ROOT.THStack('h_Stack_S',varstring)

for sample in bkgSamples+sigSamples:
  histo = sample["histo"]
  sample["chain"].Draw('>>eList', cut) #Get the event list 'eList' which has all the events satisfying the cut
#  h_Stack.Add(histo)
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
  for i in range(number_events): #Loop over those events
    if i>0 and (i%10000)==0:
      print "Filled",i
    sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
    if sample["weight"]=="weight":
      thisweight=getVarValue(sample["chain"],"weight")
    else:
      thisweight=sample["weight"]
    varValue = getVarValue(sample["chain"], varstring)   #Get the value of the variable
    #met = sample["chain"].GetLeaf('met_pt').GetValue()
    #leptonPt = sample["chain"].GetLeaf('leptonPt').GetValue()
    #metphi = sample["chain"].GetLeaf('met_phi').GetValue()
    #leptonPhi = sample["chain"].GetLeaf('leptonPhi').GetValue()
    #cdp = cos(leptonPhi-metphi)
    #dPhiValue = acos((leptonPt+met*cdp)/sqrt(leptonPt**2+met**2+2*met*leptonPt*cdp)) 
    #testValue = sample["chain"].GetLeaf('met_phi').GetValue()
    #dPhiValue=stage2DPhi(sample["chain"])
    #print dPhiValue
    #if dPhiValue>dPhiCut:
    sample["histo"].Fill(varValue, thisweight) #Fill the histo
  del elist

#Draw the histograms ...
c=ROOT.TCanvas('c1','',1200,1000)

pad1=ROOT.TPad("pad1","MyTitle",0,0.3,1,1.0)
pad1.SetBottomMargin(0)
pad1.SetLeftMargin(0.1)
pad1.SetGrid()
pad1.SetLogy()
pad1.Draw()
pad1.cd()

h1=ROOT.TH1F("MCDataCombined","MCDataCombined", *binning)
h3=ROOT.TH1F("MCDataCombined","MCDataCombined", *binning)

l = ROOT.TLegend(0.65,0.65,0.9,0.9)
l.SetFillColor(0)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)



for sample in bkgSamples:
  #sample["histo"].Add(h1)
  h1.Add(sample["histo"])
  sample["histo"]=h1.Clone()
  sample["histo"].SetLineColor(ROOT.kBlack)#sample["color"])
  sample["histo"].SetLineWidth(1)
  sample["histo"].SetMarkerSize(0)
  sample["histo"].SetMarkerStyle(0)
  sample["histo"].SetTitleSize(20)
  sample["histo"].GetXaxis().SetTitle(varstring)
  sample["histo"].GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
  sample["histo"].GetXaxis().SetLabelSize(0.04)
  sample["histo"].GetYaxis().SetLabelSize(0.04)
  sample["histo"].GetYaxis().SetTitleOffset(0.8)
  sample["histo"].GetYaxis().SetTitleSize(0.05)
  sample["histo"].SetFillColor(sample["color"])
  sample["histo"].SetFillStyle(1001)
  l.AddEntry(sample["histo"], sample["name"])

for sample in sigSamples:
  sample["histo"].SetLineColor(ROOT.kBlack)#sample["color"])
  sample["histo"].SetLineWidth(1)
  sample["histo"].SetMarkerSize(0)
  sample["histo"].SetMarkerStyle(0)
  sample["histo"].SetTitleSize(20)
  sample["histo"].GetXaxis().SetTitle(varstring)
  sample["histo"].GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
  sample["histo"].GetXaxis().SetLabelSize(0.04)
  sample["histo"].GetYaxis().SetLabelSize(0.04)
  sample["histo"].GetYaxis().SetTitleOffset(0.8)
  sample["histo"].GetYaxis().SetTitleSize(0.05)
  sample["histo"].SetLineColor(sample["color"])
  sample["histo"].SetLineWidth(2)
  sample["histo"].SetFillColor(0)
  sample["histo"].SetMarkerStyle(0)
  
  l.AddEntry(sample["histo"], sample["name"])

i=max=len(bkgSamples)-1
while i>=0:
  bkgSamples[i]["histo"].SetMaximum(1000)
  bkgSamples[i]["histo"].SetMinimum(0.003)
  bkgSamples[i]["histo"].Draw("same")
  i-=1

for sample in sigSamples:
  sample["histo"].SetMaximum(1000)
  sample["histo"].SetMinimum(0.003)
  sample["histo"].Draw("same")


l.Draw()

#Draw ratio MC/Data
c.cd()
pad2=ROOT.TPad("pad2","pad2",0,0.05,1.,0.3)
pad2.SetGrid()
pad2.Draw()
pad2.cd()
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.3)
pad2.SetLeftMargin(0.1)

for sample in sigSamples:
  h3.Add(sample["histo"])
h3.Divide(h1)
h3.SetMaximum(1.5)
h3.SetMinimum(0.)
h3.GetXaxis().SetLabelSize(0.10)
h3.GetXaxis().SetTitle(varstring)
h3.GetXaxis().SetTitleSize(0.15)

h3.GetYaxis().SetLabelSize(0.10)
h3.GetYaxis().SetTitle("Signal / BG")
h3.GetYaxis().SetNdivisions(505)
h3.GetYaxis().SetTitleSize(0.15)
h3.GetYaxis().SetTitleOffset(0.3)
h3.SetLineColor(ROOT.kBlack)
h3.Draw("E1P")

#Draw Title
c.cd()
pad1.cd()
t1=ROOT.TLatex()
t1.SetTextFont(22)
t1.DrawLatex(150,600,"CMS preliminary")
t1.DrawLatex(150,300,"L=19.4 fb^{-1}, #sqrt{s}=8TeV")

c.Print(plotDir+varstring+'_5.png')
c.Print(plotDir+varstring+'_5.pdf')
c.Print(plotDir+varstring+'_5.root')

