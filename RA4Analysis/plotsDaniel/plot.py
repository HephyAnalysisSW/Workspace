import ROOT
import os, sys, copy
import pickle, operator

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_postProcessed import *



lepSel = 'hard'
##50ns samples
#WJETS = {'name':'WJets', 'chain':getChain(WJetsToLNu_50ns,histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets'}
#TTJETS = {'name':'TTJets', 'chain':getChain(TTJets_50ns,histname=''), 'color':color('TTJets'),'weight':'weight', 'niceName':'t#bar{t} Jets'}
#DY = {'name':'DY', 'chain':getChain(DY_50ns,histname=''), 'color':color('DY'),'weight':'weight', 'niceName':'Drell Yan'}
#singleTop = {'name':'singleTop', 'chain':getChain(singleTop_50ns,histname=''), 'color':color('singleTop'),'weight':'weight', 'niceName':'single Top'}
#QCD = {'name':'QCD', 'chain':getChain(QCDMu_50ns,histname=''), 'color':color('QCD'),'weight':'weight', 'niceName':'QCD'}
#samples = [WJETS, TTJETS, DY, singleTop, QCD]

#25ns samples
WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu_25ns,histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets'}
TTJETS = {'name':'TTJets', 'chain':getChain(TTJets_25ns,histname=''), 'color':color('TTJets'),'weight':'weight', 'niceName':'t#bar{t} Jets'}
DY = {'name':'DY', 'chain':getChain(DY_25ns,histname=''), 'color':color('DY'),'weight':'weight', 'niceName':'Drell Yan'}
singleTop = {'name':'singleTop', 'chain':getChain(singleTop_25ns,histname=''), 'color':color('singleTop'),'weight':'weight', 'niceName':'single Top'}
QCD = {'name':'QCD', 'chain':getChain(QCDMu_25ns,histname=''), 'color':color('QCD'),'weight':'weight', 'niceName':'QCD'}
samples = [WJETS, TTJETS, singleTop, DY, QCD]

# older samples
#WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu[lepSel],histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets'}
#TTJETS = {'name':'TTJets', 'chain':getChain(ttJets[lepSel],histname=''), 'color':color('TTJets'),'weight':'weight', 'niceName':'t#bar{t} Jets'}
#DY = {}
#QCD = {}
#samples = [WJETS, TTJETS]#, DY, QCD]

#PHYS14 signals:
T5qqqqWW_mGo1000_mCh800_mChi700 = {'name':'T5qqqqWW_mGo1000_mCh800_mChi700', 'chain':getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname=''), 'color':ROOT.kOrange+1,'weight':'weight', 'niceName':'T5q^{4} 1.0/0.8/0.7'}
T5qqqqWW_mGo1200_mCh1000_mChi800 = {'name':'T5qqqqWW_mGo1200_mCh1000_mChi800', 'chain':getChain(T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel],histname=''), 'color':ROOT.kRed+1,'weight':'weight', 'niceName':'T5q^{4} 1.2/1.0/0.8'}
T5qqqqWW_mGo1500_mCh800_mChi100 = {'name':'T5qqqqWW_mGo1500_mCh800_mChi100', 'chain':getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname=''), 'color':ROOT.kYellow+1,'weight':'weight', 'niceName':'T5q^{4} 1.5/0.8/0.1'}

signals = [T5qqqqWW_mGo1000_mCh800_mChi700,T5qqqqWW_mGo1200_mCh1000_mChi800,T5qqqqWW_mGo1500_mCh800_mChi100]

dPhiJet1Met = {'name':'acos(cos(Jet_phi[0]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{1},#slash{E}_{T})', 'titleY':'Events'}
dPhiJet2Met = {'name':'acos(cos(Jet_phi[1]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{2},#slash{E}_{T})', 'titleY':'Events'}
dPhiJet3Met = {'name':'acos(cos(Jet_phi[2]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{3},#slash{E}_{T})', 'titleY':'Events'}
dPhiJet4Met = {'name':'acos(cos(Jet_phi[3]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{4},#slash{E}_{T})', 'titleY':'Events'}

dPhiJet1GenMet = {'name':'acos(cos(Jet_phi[0]-met_genPhi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{1},#slash{E}_{T}^{gen})', 'titleY':'Events'}
dPhiJet2GenMet = {'name':'acos(cos(Jet_phi[1]-met_genPhi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{2},#slash{E}_{T}^{gen})', 'titleY':'Events'}
dPhiJet3GenMet = {'name':'acos(cos(Jet_phi[2]-met_genPhi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{3},#slash{E}_{T}^{gen})', 'titleY':'Events'}


st = {'name':'st', 'binning':[37,250,2100], 'titleX':'L_{T} [GeV]', 'titleY':'Events'}
ht = {'name':'htJet30j', 'binning':[52,500,3100], 'titleX':'H_{T} [GeV]', 'titleY':'Events'}
njet = {'name':'nJet30', 'binning':[15,0,15], 'titleX':'n_{jets}', 'titleY':'Events'}
deltaPhi = {'name':'deltaPhi_Wl', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(W,l)', 'titleY':'Events'}
leptonPt = {'name':'leptonPt', 'binning':[40,0,1000], 'titleX':'p_{T} [GeV]', 'titleY':'Events'}
leadingJetPt = {'name':'Jet_pt[0]', 'binning':[40,0,2000], 'titleX':'p_{T} (leading jet) [GeV]', 'titleY':'Events'}


variables = [st]

presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500&&nBJetMediumCSV30==0"
newpresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500&&nBJetMediumCSV30==0"

newPreselCut = {'name':'presel','string':newpresel,'niceName':'Preselection'}
newPreselCutSingleMuAN = {'name':'presel','string':newpresel+'&&singleMuonic&&nJet30>3','niceName':'Preselection'}
newPreselCutSingleEleAN = {'name':'presel','string':newpresel+'&&singleElectronic&&nJet30>3','niceName':'Preselection'}

Flag_EcalDeadCellTriggerPrimitiveFilter = {'name':'ecalFilterCut','string':newpresel+'&&Flag_EcalDeadCellTriggerPrimitiveFilter','niceName':'EcalDeadCellFilter'}
Flag_HBHENoiseFilter  = {'name':'ecalFilterCut','string':newpresel+'&&Flag_HBHENoiseFilter','niceName':'HBHENoiseFilter'}
Flag_CSCTightHaloFilter = {'name':'ecalFilterCut','string':newpresel+'&&Flag_CSCTightHaloFilter','niceName':'CSCTightHaloFilter'}
Flag_goodVertices = {'name':'ecalFilterCut','string':newpresel+'&&Flag_goodVertices','niceName':'goodVertices'}
Flag_eeBadScFilter = {'name':'ecalFilterCut','string':newpresel+'&&Flag_eeBadScFilter','niceName':'eeBadScFilter'}
allFiltersNoEcal = {'name':'ecalFilterCut','string':newpresel+'&&Flag_eeBadScFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter','niceName':'All but EcalDeadCell filter'}
allFilters = {'name':'ecalFilterCut','string':newpresel+'&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_eeBadScFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter','niceName':'All filters'}

filterCutList = [Flag_EcalDeadCellTriggerPrimitiveFilter,Flag_HBHENoiseFilter,Flag_CSCTightHaloFilter,Flag_goodVertices,Flag_eeBadScFilter,allFiltersNoEcal,allFilters]

fakeMet = "sqrt((met_pt*cos(met_phi)-met_genPt*cos(met_genPhi))**2+(met_pt*sin(met_phi)-met_genPt*sin(met_genPhi))**2)"
fakeMetSelection = '('+fakeMet+'>50||'+fakeMet+'>met_genPt)'
antiFakeMetSelection = '('+fakeMet+'<50&&'+fakeMet+'<met_genPt)'

AFMCut = {'name':'AFMCut','string':newpresel+"&&acos(cos(Jet_phi[0]-met_phi))>0.45&&acos(cos(Jet_phi[1]-met_phi))>0.45", 'niceName':'E_{T}^{miss} veto'}


name, cut = nameAndCut((250,350),(1000,-1),(5,5),btb=(0,0),presel=presel)
cut1 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [1000,-1)'}
name, cut = nameAndCut((350,450),(750,1000),(5,5),btb=(0,0),presel=presel)
cut2 = {'name':name,'string':cut,'niceName':'L_{T} [350,450), H_{T} [750,1000)'}
name, cut = nameAndCut((450,-1),(750,1000),(5,5),btb=(0,0),presel=presel)
cut3 = {'name':name,'string':cut,'niceName':'L_{T} [450,-1), H_{T} [750,1000)'}
name, cut = nameAndCut((450,-1),(1000,-1),(5,5),btb=(0,0),presel=presel)
cut4 = {'name':name,'string':cut,'niceName':'L_{T} [450,-1), H_{T} [1000,-1)'}
name, cut = nameAndCut((450,-1),(500,750),(5,5),btb=(0,0),presel=presel)
cut5 = {'name':name,'string':cut,'niceName':'L_{T} [450,-1), H_{T} [500,750)'}

cuts = [cut1, cut2, cut3, cut4, cut5]

randomCut = 'weight*(singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&st>250&&st<350&&nJet30>=3&&htJet30j>500&&htJet30j<750&&nBJetMediumCSV30==0)'

name, cut = nameAndCut((250,350),(1000,-1),(5,5),btb=(0,0),presel=presel)
highFakeMetCut = {'name':name,'string':cut+'&&'+fakeMetSelection,'niceName':'E_{T}^{miss,fake} > 50 GeV || > E_{T}^{miss,gen}'}
lowFakeMetCut = {'name':name,'string':cut+'&&'+antiFakeMetSelection,'niceName':'E_{T}^{miss,fake} < 50 GeV && < E_{T}^{miss,gen}'}


def plot(samples, variable, cuts, signals=False, data=False, maximum=False, minimum=0., stacking=False, filling=True, setLogY=False, setLogX=False, titleText='CMS simulation', lumi='3', legend=True):
  if not type(samples)==type([]): samples = [samples]
  if not type(cuts)==type([]): cuts = [cuts]
  if signals:
    if not type(signals)==type([]): signals = [signals]
  can = ROOT.TCanvas('c','c',700,700)
  if data:
    marginForPad2 = 0.3
    bottomMargin = 0.
  else:
    marginForPad2 = 0.
    bottomMargin = 0.13
  pad1=ROOT.TPad("pad1","MyTitle",0.,marginForPad2,1.,1.)
  pad1.SetLeftMargin(0.15)
  pad1.SetBottomMargin(bottomMargin)
  pad1.Draw()
  pad1.cd()
  colorList = [ROOT.kBlue+1, ROOT.kCyan-9, ROOT.kOrange-4, ROOT.kGreen+1, ROOT.kRed+1]
  h = []
  totalH = ROOT.TH1F('totalH', 'totalH', *variable['binning'])
  nsamples = len(samples)
  ncuts = len(cuts)
  for isample, sample in enumerate(samples):
    for icut, cut in enumerate(cuts):
      i = isample*ncuts+icut
      if nsamples>1: legendName = sample['niceName']
      else: legendName = cut['niceName']
      h.append({'hist':ROOT.TH1F('h'+str(isample)+'_'+str(icut), legendName, *variable['binning']),'yield':0., 'legendName':legendName})
      if sample['weight']=='weight':weight='weight'
      else: weight=str(sample['weight'])
      sample['chain'].Draw(variable['name']+'>>h'+str(isample)+'_'+str(icut),weight+'*('+cut['string']+')','goff')
      totalH.Add(h[i]['hist'])
      h[i]['yield'] = h[i]['hist'].GetSumOfWeights()
      if minimum: h[i]['hist'].SetMinimum(minimum)
      if maximum: h[i]['hist'].SetMaximum(maximum)
      if filling:
        h[i]['hist'].SetLineColor(ROOT.kBlack)
        if len(samples)>1 or len(cuts)<2: h[i]['hist'].SetFillColor(sample['color'])
        else: h[i]['hist'].SetFillColor(colorList[icut])
      else:
        if len(samples)>1 or len(cuts)<2: h[i]['hist'].SetLineColor(sample['color'])
        else: h[i]['hist'].SetLineColor(colorList[icut])
      h[i]['hist'].SetLineWidth(2)
      h[i]['hist'].SetMarkerSize(0)
      h[i]['hist'].GetXaxis().SetTitle(variable['titleX'])
      h[i]['hist'].GetXaxis().SetNdivisions(508)
      #h[i]['hist'].GetXaxis().SetTitleSize(0.04)
      h[i]['hist'].GetYaxis().SetTitle(variable['titleY'])
      #h[i]['hist'].GetYaxis().SetTitleSize(0.04)
  h.sort(key=operator.itemgetter('yield'))
  legendNameLengthsSamples = [len(x['legendName']) for x in h]
  legendNameLengthsSignal = []
  if signals: legendNameLengthsSignal = [len(x['niceName']) for x in signals]
  legendNameLengths = legendNameLengthsSamples + legendNameLengthsSignal
  legendWidth = 0.013*max(legendNameLengths)+0.15
  if legend:
    height = 0.04*len(h)
    if signals: height += 0.04*len(signals)
    if data: height += 0.04
    leg = ROOT.TLegend(0.98-legendWidth,0.95-height,0.98,0.95)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetShadowColor(ROOT.kWhite)
    leg.SetBorderSize(1)
    leg.SetTextSize(0.035)
    for item in reversed(h):
      leg.AddEntry(item['hist'])
  if setLogY: pad1.SetLogy()
  if setLogX: pad1.SetLogx()
  if stacking:
    h_Stack = ROOT.THStack('h_Stack','Stack')
    for item in h:
      h_Stack.Add(item['hist'])
    if minimum: h_Stack.SetMinimum(minimum)
    if maximum: h_Stack.SetMaximum(maximum)
    h_Stack.Draw('hist')
    h_Stack.GetXaxis().SetTitle(variable['titleX'])
    h_Stack.GetXaxis().SetNdivisions(508)
    h_Stack.GetYaxis().SetTitle(variable['titleY'])
  else:
    first = True
    for item in reversed(h):
      if first:
        item['hist'].Draw('hist')
        first = False
      else:
        item['hist'].Draw('hist same')
  if signals:
    s = []
    for isignal,signal in enumerate(signals):
      s.append({'hist':ROOT.TH1F('s'+str(isignal), signal['niceName'], *variable['binning']),'yield':0., 'legendName':signal['niceName']})
      if signal['weight']=='weight':weight='weight'
      else: weight=str(signal['weight'])
      signal['chain'].Draw(variable['name']+'>>s'+str(isignal),weight+'*('+cut['string']+')','goff')
      s[isignal]['hist'].SetLineColor(signal['color'])
      s[isignal]['hist'].SetLineWidth(3)
      s[isignal]['hist'].SetMarkerSize(0)
      if legend: leg.AddEntry(s[isignal]['hist'])
      s[isignal]['hist'].Draw('same hist')
  if data:
    h.append({'hist':ROOT.TH1F('data','Data',*variable['binning']),'yield':0., 'legendName':'data'})
    data['chain'].Draw(variable['name']+'>>data',weight+'*('+cut['string']+')','goff')
    #h_Stack.Draw('hist')
    h[-1]['hist'].Draw('same e1p')
    if legend: leg.AddEntry(h[-1]['hist'])
    dataMCH = ROOT.TH1F('dataMC','DataMC',*variable['binning'])
    dataMCH.Sumw2()
    dataMCH = h[-1]['hist'].Clone()
    dataMCH.Divide(totalH)
    can.cd()
    pad2=ROOT.TPad("pad2","datavsMC",0.,0.,1.,.3)
    pad2.SetLeftMargin(0.15)
    pad2.SetBottomMargin(0.3)
    pad2.SetTopMargin(0.)
    pad2.SetGrid()
    pad2.Draw()
    pad2.cd()
    dataMCH.GetXaxis().SetTitle(variable['titleX'])
    dataMCH.GetXaxis().SetTitleSize(0.13)
    dataMCH.GetXaxis().SetLabelSize(0.13)
    dataMCH.GetXaxis().SetNdivisions(508)
    dataMCH.GetYaxis().SetTitle('data/MC')
    dataMCH.GetYaxis().SetTitleSize(0.13)
    dataMCH.GetYaxis().SetLabelSize(0.13)
    dataMCH.GetYaxis().SetTitleOffset(0.6)
    dataMCH.GetYaxis().SetNdivisions(508)
    dataMCH.SetMinimum(0.)
    dataMCH.SetMaximum(2.2)
    h.append({'hist':dataMCH, 'yield':0., 'legendName':'notInLegend'})
    dataMCH.Draw('same e1p')
    can.cd()
    pad1.cd()
  if titleText or lumi:
    latex1 = ROOT.TLatex()
    latex1.SetNDC()
    latex1.SetTextSize(0.04)
    latex1.SetTextAlign(11) # align right
  if titleText: latex1.DrawLatex(0.15,0.96,titleText)
  if lumi: latex1.DrawLatex(0.73,0.96,"L="+str(lumi)+"fb^{-1} (13TeV)")
  if legend: leg.Draw()
  can.Update()
  if stacking: return {'hist':h, 'canvas':can, 'legend':leg, 'stack':h_Stack}
  else: return {'hist':h, 'canvas':can, 'legend':leg}

#plot(samples,st,cuts)

