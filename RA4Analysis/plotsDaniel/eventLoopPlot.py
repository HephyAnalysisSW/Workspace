import ROOT
import os, sys, copy

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi, getYieldFromChain
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2 import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_softLepton import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.eventShape import * 

binning=[30,0,600]

#prepresel = 'singleLeptonic==1&&'#&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'
#presel = prepresel + 'Jet_pt[1]>80&&nJet30>=2&&nBJetMediumCMVA30==0&&st>=150&&st<=250'#&&htJet30j>500&&htJet30j<750'#&&htJet30j>=500&&st>=200&&deltaPhi_Wl>1&&mt2w>350'

prepresel = 'singleLeptonic==1&&htJet30j>500&&st>250&&nJet30>=4&&nBJetMediumCMVA30==0&&Jet_pt[1]>100&&Jet_pt[2]>60'
presel = prepresel


def getdPhiMetJet(c):
  met = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  JetPt = c.GetLeaf('Jet_pt').GetValue(0)
  JetPhi = c.GetLeaf('Jet_phi').GetValue(0)
  # dPhi = acos((met*JetPt*cos(metPhi-JetPhi))/(met*JetPt))
  dPhi = deltaPhi(metPhi,JetPhi)
  return dPhi

def getFWMT2(c):
  jets = cmgGetJets(c)
  rd = foxWolframMoments(jets)
  return rd['FWMT2']

def getFWMT4(c):
  jets = cmgGetJets(c)
  rd = foxWolframMoments(jets)
  return rd['FWMT4']

def getJetMagnitude(c):
  leadJetPt = c.GetLeaf('Jet_pt').GetValue(0)
  subJetPt = c.GetLeaf('Jet_pt').GetValue(1)
  ht = c.GetLeaf('htJet30j').GetValue()
  nJ = c.GetLeaf('nJet30').GetValue()
  res = (ht)/(nJ)
  return res

def getlinCirc2D(c):
  jets = cmgGetJets(c)
  rd = circularity2D(jets)
  return rd['linC2D']

def getLeadingJet(c):
  Jet0 = c.GetLeaf('Jet_pt').GetValue(0)
  return Jet0

def getNLJet(c):
  Jet1 = c.GetLeaf('Jet_pt').GetValue(1)
  return Jet1

#presel='(abs(genPartAll_pdgId)==11||abs(genPartAll_pdgId)==13)&&(abs(genPartAll_motherId)==24||abs(genPartAll_motherId)==1000024)'
#presel='(abs(genLep_pdgId)==11||abs(genLep_pdgId)==13)&&(abs(genLep_motherId)==24||abs(genLep_motherId)==1000024)'

#presel='abs(genPartAll_pdgId)==1000022&&abs(genPartAll_motherId)==1000024'

#presel='abs(genPartAll_pdgId)==1000024'

signalString='T5qqqqWW_softLep'

varstring="deltaPhi_Wl"
plotDir='/afs/hephy.at/user/d/dspitzbart/www/softLep/'

lepSel='soft'

#BKG Samples
WJETS = getChain(WJetsHTToLNu[lepSel],histname='')
TTJETS = getChain(ttJets[lepSel],histname='')
TTVH = getChain(TTVH[lepSel],histname='')
SINGLETOP = getChain(singleTop[lepSel],histname='')
DY = getChain(DY[lepSel],histname='')
QCD = getChain(QCD[lepSel],histname='')

#t5qqqq1400_315_300 = ROOT.TChain('tree')
#t5qqqq1400_315_300.Add('/data/dspitzbart/Phys14_V3/T5qqqqWWDeg_mGo1400_mCh315_mChi300/treeProducerSusySingleLepton/tree.root')
#
#t5qqqq1000_315_300 = ROOT.TChain('tree')
#t5qqqq1000_315_300.Add('/data/dspitzbart/Phys14_V3/T5qqqqWWDeg_mGo1000_mCh315_mChi300/treeProducerSusySingleLepton/tree.root')
#
#t5qqqq1000_325_300 = ROOT.TChain('tree')
#t5qqqq1000_325_300.Add('/data/dspitzbart/Phys14_V3/T5qqqqWWDeg_mGo1000_mCh325_mChi300/treeProducerSusySingleLepton/tree.root')
#
#t5qqqq1000_310_300 = ROOT.TChain('tree')
#t5qqqq1000_310_300.Add('/data/dspitzbart/Phys14_V3/T5qqqqWWDeg_mGo1000_mCh310_mChi300/treeProducerSusySingleLepton/tree.root')
#
#t5qqqq800_305_300 = ROOT.TChain('tree')
#t5qqqq800_305_300.Add('/data/dspitzbart/Phys14_V3/T5qqqqWWDeg_mGo800_mCh305_mChi300/treeProducerSusySingleLepton/tree.root')
#
#t5qqqq1000_800_700 = ROOT.TChain('tree')
#t5qqqq1000_800_700.Add('/data/easilar/Phys14_V3/T5qqqqWW_mGo1000_mCh800_mChi700/treeProducerSusySingleLepton/tree.root')
#
#t5qqqq1500_800_100 = ROOT.TChain('tree')
#t5qqqq1500_800_100.Add('/data/dspitzbart/Phys14_V3/T5qqqqWW_mGo1500_mCh800_mChi100/treeProducerSusySingleLepton/tree.root')
#
#t5qqqq1200_1000_800 = ROOT.TChain('tree')
#t5qqqq1200_1000_800.Add('/data/easilar/Phys14_V3/T5qqqqWW_mGo1200_mCh1000_mChi800/treeProducerSusySingleLepton/tree.root')


#SIG Samples
SIG1 = getChain(T5qqqqWWDeg_mGo1000_mCh325_mChi300[lepSel],histname='')
SIG2 = getChain(T5qqqqWWDeg_mGo1000_mCh310_mChi300[lepSel],histname='')
SIG3 = getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname='')
SIG4 = getChain(T5qqqqWWDeg_mGo800_mCh305_mChi300[lepSel],histname='')


wjets = {
  "name":"W + Jets", "chain":WJETS, "weight":"weight", "color":color('wjets')}
ttjets = {
  "name":"t#bar{t} + Jets", "chain":TTJETS, "weight":"weight", "color":color('ttjets')}
ttvh = {
  "name":"TTVH", "chain":TTVH, "weight":"weight", "color":color('ttvh')}
singletop = {
  "name":"single top", "chain":SINGLETOP, "weight":"weight", "color":color('singletop')}
dy = {
  "name":"Drell Yan", "chain":DY, "weight":"weight", "color":color('dy')}
qcd = {
  "name":"QCD", "chain":QCD, "weight":"weight", "color":color('qcd')}



signal1 = {'name':'T5qqqqWWDeg_mGo1000_mCh325_mChi300', 'chain':SIG1, 'weight':'weight', 'color':ROOT.kBlack, "histo":ROOT.TH1F("Signal 1", "sqrt(s)", *binning)}
signal2 = {'name':'T5qqqqWWDeg_mGo1000_mCh310_mChi300', 'chain':SIG2, 'weight':'weight', 'color':ROOT.kRed+1, "histo":ROOT.TH1F("Signal 2", "sqrt(s)", *binning)}
signal3 = {'name':'T5qqqqWW_mGo1000_mCh800_mChi700', 'chain':SIG3, 'weight':'weight', 'color':ROOT.kMagenta+1, "histo":ROOT.TH1F("Signal 3", "sqrt(s)", *binning)}
signal4 = {'name':'T5qqqqWWDeg_mGo800_mCh305_mChi300', 'chain':SIG4, 'weight':'weight', 'color':ROOT.kCyan+3, "histo":ROOT.TH1F("Signal 4", "sqrt(s)", *binning)}


#t5qqqq1 = {'name':'T5qqqqWW_Gl1400_Chi315_LSP300', 'chain':t5qqqq1400_315_300, 'weight':'(1)', 'color':ROOT.kBlue, "histo":ROOT.TH1F("Signal 1", "sqrt(s)", *binning)}
#t5qqqq2 = {'name':'T5qqqqWW_Gl1000_Chi315_LSP300', 'chain':t5qqqq1000_315_300, 'weight':'(1)', 'color':ROOT.kBlack, "histo":ROOT.TH1F("Signal 2", "sqrt(s)", *binning)}
#t5qqqq3 = {'name':'T5qqqqWW_Gl1000_Chi325_LSP300', 'chain':t5qqqq1000_325_300, 'weight':'(1)', 'color':ROOT.kMagenta, "histo":ROOT.TH1F("Signal 3", "sqrt(s)", *binning)}
#t5qqqq4 = {'name':'T5qqqqWW_Gl1000_Chi310_LSP300', 'chain':t5qqqq1000_310_300, 'weight':'(1)', 'color':ROOT.kGreen+2, "histo":ROOT.TH1F("Signal 4", "sqrt(s)", *binning)}
#t5qqqq5 = {'name':'T5qqqqWW_Gl800_Chi305_LSP300', 'chain':t5qqqq800_305_300, 'weight':'(1)', 'color':ROOT.kOrange, "histo":ROOT.TH1F("Signal 5", "sqrt(s)", *binning)}
#t5qqqq6 = {'name':'T5qqqqWW_Gl1000_Chi800_LSP700', 'chain':t5qqqq1000_800_700, 'weight':'(1)', 'color':ROOT.kRed+1, "histo":ROOT.TH1F("Signal 6", "sqrt(s)", *binning)}
#t5qqqq7 = {'name':'T5qqqqWW_Gl1500_Chi800_LSP100', 'chain':t5qqqq1500_800_100, 'weight':'(1)', 'color':ROOT.kRed-1, "histo":ROOT.TH1F("Signal 7", "sqrt(s)", *binning)}
#t5qqqq8 = {'name':'T5qqqqWW_Gl1200_Chi1000_LSP800', 'chain':t5qqqq1200_1000_800, 'weight':'(1)', 'color':ROOT.kCyan+1, "histo":ROOT.TH1F("Signal 8", "sqrt(s)", *binning)}


sigSamples=[]
sigSamples.append(signal1)
sigSamples.append(signal2)
sigSamples.append(signal3)
sigSamples.append(signal4)


#sigSamples.append(t5qqqq6)
#sigSamples.append(t5qqqq7)
#sigSamples.append(t5qqqq8)
#sigSamples.append(t5qqqq1)
#sigSamples.append(t5qqqq3)
#sigSamples.append(t5qqqq2)
#sigSamples.append(t5qqqq4)
#sigSamples.append(t5qqqq5)


bkgSamples=[]
bkgSamples.append(qcd)
bkgSamples.append(ttvh)
bkgSamples.append(dy)
bkgSamples.append(singletop)
bkgSamples.append(wjets)
bkgSamples.append(ttjets)

noAdCut = {'name':'noAddCut', 'varString':'mt2w', 'legendName':'#Delta#Phi(#slash{E}_{T},J_{1})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
dphimetjet = {'name':'mydPhimetjet', 'varFunc':getdPhiMetJet, 'legendName':'#Delta#Phi(#slash{E}_{T},J_{1})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
minDPhiMetJetthree = {'name':'myminDPhiMetJet123', 'varFunc':cmgMinDPhiJet, 'legendName':'min #Delta#Phi(#slash{E}_{T},J_{1,2,3})', 'Ytitle':'# of Events', 'binning':[20,0,pi]}#, 'binningIsExplicit':True}
fwmt2 = {'name':'myfwmt2', 'varFunc':getFWMT2, 'legendName':'FWMT2', 'Ytitle':'# of Events ', 'binning':[20,0,1]}
fwmt4 = {'name':'myfwmt4', 'varFunc':getFWMT4, 'legendName':'FWMT4', 'Ytitle':'# of Events ', 'binning':[20,0,1]}
MT2W = {'name':'mymt2w', 'varString':'mt2w', 'legendName':'M^{W}_{T2}', 'Ytitle':'# of Events / 10GeV', 'binning':[45,0,450]}
jetMag = {'name':'myjetmag', 'varFunc':getJetMagnitude, 'legendName':'#frac{H_{T}}{nJets}', 'Ytitle':'# of Events', 'binning':[35,0,350]}
lincirc = {'name':'mylincirc', 'varFunc':getlinCirc2D, 'legendName':'lin. Circularity', 'Ytitle':'# of Events ', 'binning':[20,0,1]}

met = {'name':'mymet', 'varString':"met_pt", 'legendName':'#slash{E}_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
ht = {'name':'myht', 'varString':"htJet30j", 'legendName':'H_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
St = {'name':'myst', 'varString':"st", 'legendName':'S_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
nJets = {'name':'mynJets', 'varString':'nJet30', 'legendName':'Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
Jet_pt_1 = {'name':'myJetPt1', 'varFunc':getLeadingJet, 'legendName': 'leading Jet p_{T}', 'Ytitle':'# of Events', 'binning':[20,0,1000]}
Jet_pt_2 = {'name':'myJetPt2', 'varFunc':getNLJet, 'legendName': 'next-to-leading Jet p_{T}', 'Ytitle':'# of Events', 'binning':[20,0,1000]}
deltaPhi = {'name':'mydeltaPhi', 'varString':'deltaPhi_Wl', 'legendName':'#Delta #Phi', 'Ytitle':'# of Events', 'binning':[16,0,3.2]}

allVariables = []
#jets = cmgGetJets(c)

#allVariables.append(dphimetjet)
allVariables.append(minDPhiMetJetthree)

cutVar = noAdCut
adCut = 0.
varNew = MT2W

h_Stack = ROOT.THStack('h_Stack',varstring)
h_Stack_S = ROOT.THStack('h_Stack_S',varstring)

can1 = ROOT.TCanvas(varstring,varstring,800,600)

h1=ROOT.TH1F("MCDataCombined","MCDataCombined", *binning)
h3=ROOT.TH1F("MCDataCombined","MCDataCombined", *binning)

l = ROOT.TLegend(0.7,0.75,1.,1.)
l.SetFillColor(0)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)

for sample in bkgSamples:
  chain = sample["chain"]
  print chain
  histo = 'h_'+sample["name"]
  histoname = histo
  print histoname
  histo = ROOT.TH1F(str(histo) ,str(histo),*binning)
  print histo
  color = sample["color"]
  print color
  
  chain.Draw('>>eList',presel)#insert 'weight*('+
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "Looping over " + str(number_events) + " events"
  #Event Loop starts here
  first = True
  for i in range(number_events):
    if i>0 and (i%10000)==0:
      print "Filled ",i
    sample['chain'].GetEntry(elist.GetEntry(i))
    if sample["weight"]=="weight":
      thisweight=getVarValue(sample["chain"],"weight")
    else:
      thisweight=sample["weight"]
    if first:
      print 'Weight: ',thisweight
      first = False
    #varvalue = getVarValue(sample['chain'],varstring)
    varvalue = getVarValue(sample["chain"], varNew['varString']) if varNew.has_key('varString') else varNew['varFunc'](sample["chain"])
    #varvalue = varNew['varFunc'](sample['chain'])
    adValueToCut = getVarValue(sample["chain"], cutVar['varString']) if cutVar.has_key('varString') else cutVar['varFunc'](sample["chain"])
    if adValueToCut > adCut:
      histo.Fill(varvalue,thisweight)

  histo.SetLineColor(ROOT.kBlack)
  histo.SetLineWidth(1)
  histo.SetMarkerSize(0)
  histo.SetMarkerStyle(0)
  histo.SetTitleSize(20)
  histo.GetXaxis().SetTitle(varNew['legendName'])
  histo.GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
  histo.GetXaxis().SetLabelSize(0.04)
  histo.GetYaxis().SetLabelSize(0.04)
  histo.GetYaxis().SetTitleOffset(0.8)
  histo.GetYaxis().SetTitleSize(0.05)
  histo.SetFillColor(sample["color"])
  histo.SetFillStyle(1001)
  histo.SetMinimum(.8)
  h_Stack.Add(histo)
  h1.Add(histo)
  l.AddEntry(histo, sample["name"])

for sample in sigSamples:
  chain = sample["chain"]
  print chain
  histo = 'h_'+sample["name"]
  histoname = histo
  print histoname
  histo = ROOT.TH1F(str(histo) ,str(histo),*binning)
  print histo
  color = sample["color"]
  print color

  chain.Draw('>>eList',presel)#insert 'weight*('+
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "Looping over " + str(number_events) + " events"
  #Event Loop starts here
  first = True
  for i in range(number_events):
    if i>0 and (i%1000)==0:
      print "Filled ",i
    sample['chain'].GetEntry(elist.GetEntry(i))
    if sample["weight"]=="weight":
      thisweight=getVarValue(sample["chain"],"weight")
    else:
      thisweight=sample["weight"]
    if first:
      print 'Weight: ',thisweight
      first = False
    #varvalue = getVarValue(sample['chain'],varstring)
    varvalue = getVarValue(sample["chain"], varNew['varString']) if varNew.has_key('varString') else varNew['varFunc'](sample["chain"])
    #varvalue = varNew['varFunc'](sample['chain'])
    adValueToCut = getVarValue(sample["chain"], cutVar['varString']) if cutVar.has_key('varString') else cutVar['varFunc'](sample["chain"])
    if adValueToCut > adCut:
      histo.Fill(varvalue,thisweight)
  histo.SetLineColor(color)
  histo.SetLineWidth(2)
  histo.SetMarkerSize(0)
  histo.SetMarkerStyle(0)
  histo.SetTitleSize(20)
  histo.GetXaxis().SetTitle(varNew['legendName'])
  histo.GetXaxis().SetLabelSize(0.04)
  histo.GetXaxis().SetTitleOffset(0.3)
  histo.GetXaxis().SetTitleSize(0.06)
  histo.GetYaxis().SetTitle("Events")
  histo.GetYaxis().SetLabelSize(0.04)
  histo.GetYaxis().SetTitleOffset(0.3)
  histo.GetYaxis().SetTitleSize(0.06)
  histo.SetFillColor(0)
  histo.SetMinimum(.8)
  h_Stack_S.Add(histo)
  h3.Add(histo)
  l.AddEntry(histo, sample["name"])
  #signalString+=sample["name"]

#pad1=ROOT.TPad("pad1","MyTitle",0,0.3,1,1.0)
#pad1.SetBottomMargin(0)
#pad1.SetLeftMargin(0.1)
#pad1.SetGrid()
#pad1.SetLogy()
#pad1.Draw()
#pad1.cd()

#when not using pads
can1.SetGrid()
can1.SetLogy()

histo.GetXaxis().SetTitle(varNew['legendName'])
histo.GetXaxis().SetLabelSize(0.04)
histo.GetXaxis().SetTitleOffset(0.3)
histo.GetXaxis().SetTitleSize(0.15)

histo.GetYaxis().SetTitle("Events")
histo.GetYaxis().SetLabelSize(0.04)
histo.GetYaxis().SetTitleOffset(0.3)
histo.GetYaxis().SetTitleSize(0.15)



h_Stack.Draw()
h_Stack.SetMinimum(0.8)
h_Stack_S.Draw('noStacksame')
#h_Stack_S.Draw('noStack')
h_Stack.GetYaxis().SetTitle("Events") #add _S if no bkg
h_Stack.GetYaxis().SetLabelSize(0.04)
h_Stack.GetYaxis().SetTitleOffset(1.1)
h_Stack.GetYaxis().SetTitleSize(0.04)
h_Stack.GetXaxis().SetTitle(varNew['legendName'])
h_Stack.GetXaxis().SetLabelSize(0.04)
h_Stack.GetXaxis().SetTitleOffset(1.3)
h_Stack.GetXaxis().SetTitleSize(0.04)
#h_Stack_S.Draw('noStack')
l.Draw()

##Draw ratio MC/Data
#can1.cd()
#pad2=ROOT.TPad("pad2","pad2",0,0.05,1.,0.3)
#pad2.SetGrid()
#pad2.Draw()
#pad2.cd()
#pad2.SetTopMargin(0)
#pad2.SetBottomMargin(0.3)
#pad2.SetLeftMargin(0.1)
#
#h3.Divide(h1)
#h3.SetMaximum(1.35)
#h3.SetMinimum(0.)
#h3.GetXaxis().SetLabelSize(0.10)
#h3.GetXaxis().SetTitle(varstring)
#h3.GetXaxis().SetTitleSize(0.15)
#
#h3.GetYaxis().SetLabelSize(0.10)
#h3.GetYaxis().SetTitle("Signal / BG")
#h3.GetYaxis().SetNdivisions(505)
#h3.GetYaxis().SetTitleSize(0.15)
#h3.GetYaxis().SetTitleOffset(0.3)
#h3.SetLineColor(ROOT.kBlack)
#h3.Draw("E1P")

#Draw Title
#can1.cd()
#pad1.cd()
#t1=ROOT.TLatex()
#t1.SetTextFont(22)
#t1.DrawLatex(150,600,"CMS preliminary")
#t1.DrawLatex(150,300,"L=19.4 fb^{-1}, #sqrt{s}=8TeV")

can1.Print(plotDir+varNew['name']+'_'+cutVar['name']+'_'+presel+signalString+'.png')
can1.Print(plotDir+varNew['name']+'_'+cutVar['name']+'_'+presel+signalString+'.pdf')
can1.Print(plotDir+varNew['name']+'_'+cutVar['name']+'_'+presel+signalString+'.root')



#can1.SetLogy()

