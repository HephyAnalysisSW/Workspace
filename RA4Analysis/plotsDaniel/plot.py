import ROOT
import os, sys, copy
import pickle, operator

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_postProcessed import *



lepSel = 'hard'
#50ns samples
WJETS = {'name':'WJets', 'chain':getChain(WJetsToLNu_50ns[lepSel],histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets'}
TTJETS = {'name':'TTJets', 'chain':getChain(TTJets_50ns[lepSel],histname=''), 'color':color('TTJets'),'weight':'weight', 'niceName':'t#bar{t} Jets'}
DY = {'name':'DY', 'chain':getChain(DY_50ns[lepSel],histname=''), 'color':color('DY'),'weight':'weight', 'niceName':'Drell Yan'}
singleTop = {'name':'singleTop', 'chain':getChain(singleTop_50ns[lepSel],histname=''), 'color':color('singleTop'),'weight':'weight', 'niceName':'single Top'}
#QCD = {'name':'QCD', 'chain':getChain(QCDEle_50ns[lepSel],histname=''), 'color':color('QCD'),'weight':'weight', 'niceName':'QCD'}
samples = [WJETS, TTJETS, DY, singleTop]#, QCD]

##25ns samples
#WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu_25ns[lepSel],histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets'}
#TTJETS = {'name':'TTJets', 'chain':getChain(TTJets_25ns[lepSel],histname=''), 'color':color('TTJets'),'weight':'weight', 'niceName':'t#bar{t} Jets'}
#DY = {'name':'DY', 'chain':getChain(DY_25ns[lepSel],histname=''), 'color':color('DY'),'weight':'weight', 'niceName':'Drell Yan'}
#singleTop = {'name':'singleTop', 'chain':getChain(singleTop_25ns[lepSel],histname=''), 'color':color('singleTop'),'weight':'weight', 'niceName':'single Top'}
#QCD = {'name':'QCD', 'chain':getChain(QCDMu_25ns[lepSel],histname=''), 'color':color('QCD'),'weight':'weight', 'niceName':'QCD'}
#samples = [WJETS, TTJETS, singleTop, DY, QCD]

# older samples
#WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu[lepSel],histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets'}
#TTJETS = {'name':'TTJets', 'chain':getChain(ttJets[lepSel],histname=''), 'color':color('TTJets'),'weight':'weight', 'niceName':'t#bar{t} Jets'}
#DY = {}
#QCD = {}
#samples = [WJETS, TTJETS]#, DY, QCD]


dPhiJet1Met = {'name':'acos(cos(Jet_phi[0]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{1},#slash{E}_{T})', 'titleY':'Events'}
dPhiJet2Met = {'name':'acos(cos(Jet_phi[1]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{2},#slash{E}_{T})', 'titleY':'Events'}
dPhiJet3Met = {'name':'acos(cos(Jet_phi[2]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{3},#slash{E}_{T})', 'titleY':'Events'}
dPhiJet4Met = {'name':'acos(cos(Jet_phi[3]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{4},#slash{E}_{T})', 'titleY':'Events'}

dPhiJet1GenMet = {'name':'acos(cos(Jet_phi[0]-met_genPhi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{1},#slash{E}_{T}^{gen})', 'titleY':'Events'}
dPhiJet2GenMet = {'name':'acos(cos(Jet_phi[1]-met_genPhi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{2},#slash{E}_{T}^{gen})', 'titleY':'Events'}
dPhiJet3GenMet = {'name':'acos(cos(Jet_phi[2]-met_genPhi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{3},#slash{E}_{T}^{gen})', 'titleY':'Events'}


st = {'name':'st', 'binning':[30,0,1500], 'titleX':'L_{T} [GeV]', 'titleY':'Events'}
ht = {'name':'htJet30j', 'binning':[40,500,2500], 'titleX':'H_{T} [GeV]', 'titleY':'Events'}
njet = {'name':'nJet30', 'binning':[15,0,15], 'titleX':'n_{jets}', 'titleY':'Events'}
deltaPhi = {'name':'deltaPhi_Wl', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(W,l)', 'titleY':'Events'}
leptonPt = {'name':'leptonPt', 'binning':[40,0,1000], 'titleX':'p_{T} [GeV]', 'titleY':'Events'}
leadingJetPt = {'name':'Jet_pt[0]', 'binning':[40,0,2000], 'titleX':'p_{T} (leading jet) [GeV]', 'titleY':'Events'}


variables = [st]

presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"
newpresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"

newPreselCut = {'name':'presel','string':newpresel,'niceName':'Preselection'}

fakeMet = "sqrt((met_pt*cos(met_phi)-met_genPt*cos(met_genPhi))**2+(met_pt*sin(met_phi)-met_genPt*sin(met_genPhi))**2)"
fakeMetSelection = '('+fakeMet+'>50||'+fakeMet+'>met_genPt)'
antiFakeMetSelection = '('+fakeMet+'<50&&'+fakeMet+'<met_genPt)'

AFMCut = "acos(cos(Jet_phi[0]-met_phi))>0.45&&acos(cos(Jet_phi[1]-met_phi))>0.45"

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


def plot(samples, variable, cuts, data=False, maximum=False, minimum=0., stacking=False, filling=True, setLogY=False, setLogX=False, titleText='CMS simulation', lumi='3', legend=True):
  can = ROOT.TCanvas('c','c',700,600)
  colorList = [ROOT.kBlue+1, ROOT.kCyan-9, ROOT.kOrange-4, ROOT.kGreen+1, ROOT.kRed+1]
  h = []
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
      h[i]['hist'].GetXaxis().SetTitle(variable['titleX'])
      #h[i]['hist'].GetXaxis().SetTitleSize(0.04)
      h[i]['hist'].GetYaxis().SetTitle(variable['titleY'])
      #h[i]['hist'].GetYaxis().SetTitleSize(0.04)
  h.sort(key=operator.itemgetter('yield'))
  legendNameLengths = [len(x['legendName']) for x in h]
  legendWidth = 0.012*max(legendNameLengths)+0.15
  if legend:
    height = 0.06*len(h)
    leg = ROOT.TLegend(0.98-legendWidth,0.95-height,0.98,0.95)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetShadowColor(ROOT.kWhite)
    leg.SetBorderSize(1)
    leg.SetTextSize(0.04)
    for item in reversed(h):
      leg.AddEntry(item['hist'])
  if setLogY: can.SetLogy()
  if setLogX: can.SetLogx()
  if stacking:
    h_Stack = ROOT.THStack('h_Stack','Stack')
    for item in h:
      h_Stack.Add(item['hist'])
    if minimum: h_Stack.SetMinimum(minimum)
    if maximum: h_Stack.SetMaximum(maximum)
    h_Stack.Draw('hist')
    h_Stack.GetXaxis().SetTitle(variable['titleX'])
    h_Stack.GetYaxis().SetTitle(variable['titleY'])
  else:
    first = True
    for item in reversed(h):
      if first:
        item['hist'].Draw('hist')
        first = False
      else:
        item['hist'].Draw('hist same')
  if data:
    dataHist = ROOT.TH1F('data','Data',*variable['binning'])
    data.Draw(variable['name']+'>>data',cut['sting'])
    data.Draw('e1p same')
    h['data'] = dataHist
    leg.AddEntry(dataHist)
  if titleText or lumi:
    latex1 = ROOT.TLatex()
    latex1.SetNDC()
    latex1.SetTextSize(0.04)
    latex1.SetTextAlign(11) # align right
  if titleText: latex1.DrawLatex(0.17,0.96,titleText)
  if lumi: latex1.DrawLatex(0.75,0.96,"L="+str(lumi)+"fb^{-1} (13TeV)")
  if legend: leg.Draw()
  can.Update()
  if stacking: return {'hist':h, 'canvas':can, 'legend':leg, 'stack':h_Stack}
  else: return {'hist':h, 'canvas':can, 'legend':leg}

#plot(samples,st,cuts)

