import ROOT
import os, sys, copy
import pickle, operator

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *

from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_Promtv2_postprocessed import * #2016 data


from Workspace.HEPHYPythonTools.user import username


WJets = {'name':'WJets', 'chain':getChain(WJetsHTToLNu,histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W+jets'}
TTJets = {'name':'TTJets', 'chain':getChain(TTJets_Comb,histname=''), 'color':color('TTJets')-2,'weight':'weight', 'niceName':'t#bar{t}+jets'}
DY = {'name':'DY', 'chain':getChain(DY_HT,histname=''), 'color':color('DY'),'weight':'weight', 'niceName':'Drell Yan'}
singleTop = {'name':'singleTop', 'chain':getChain(singleTop_lep,histname=''), 'color':color('singleTop'),'weight':'weight', 'niceName':'t/#bar{t}+jets'}
QCD = {'name':'QCD', 'chain':getChain(QCDHT,histname=''), 'color':color('QCD'),'weight':'weight', 'niceName':'QCD multijet'}
TTVH = {'name':'TTVH', 'chain':getChain(TTV,histname=''), 'color':color('TTV'),'weight':'weight', 'niceName':'t#bar{t}W+jets'}
diBoson = {'name':'diBoson', 'chain':getChain(diBoson, histname=''), 'color':ROOT.kRed+3,'weight':'weight', 'niceName':'WW/WZ/ZZ'}
rest = {'name':'other', 'chain':getChain([DY_HT,singleTop_lep,TTV],histname=''), 'color':color('ttv'),'weight':'weight', 'niceName':'other'}
samples = [WJets, TTJets, DY, singleTop, TTVH, diBoson, QCD]
#EWK = [WJets, TTJets, rest]
EWK = [WJets, TTJets, DY, singleTop, TTVH, diBoson]

muTriggerEff = '0.926'
eleTriggerErr = '0.963'

signalpresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>4&&htJet30j>500"
signalweight = '12.88/3.*weight*puReweight_true_max4*(singleMuonic*'+muTriggerEff+' + singleElectronic*'+eleTriggerErr+')*reweightLeptonFastSimSF'

#T5qqqqWW_mGo1000_mChi700 = {'name':'T5qqqqWW_mGo1000_mChi700', 'chain':getChain(T5qqqqVV_mGluino_1000To1075_mLSP_1To950[1000][700], histname=''), 'color':ROOT.kAzure+9, 'weight':signalweight, 'niceName':'T5q^{4}WW 1.0/0.7'}
#T5qqqqWW_mGo1200_mChi800 = {'name':'T5qqqqWW_mGo1200_mChi800', 'chain':getChain(T5qqqqVV_mGluino_1200To1275_mLSP_1to1150[1200][800],histname=''), 'color':ROOT.kMagenta+2,    'weight':signalweight, 'niceName':'T5q^{4}WW 1.2/0.8'}
#T5qqqqWW_mGo1500_mChi100 = {'name':'T5qqqqWW_mGo1500_mChi100', 'chain':getChain(T5qqqqVV_mGluino_1400To1550_mLSP_1To1275[1500][100],histname=''), 'color':ROOT.kRed+1, 'weight':signalweight, 'niceName':'T5q^{4}WW 1.5/0.1'}
T5qqqqWW_mGo1200_mChi800 = {'name':'T5qqqqWW_mGo1200_mChi800', 'chain':getChain(allSignals[0][1200][800], histname=''), 'color':ROOT.kAzure+9, 'weight':signalweight, 'niceName':'T5qqqqWW 1.2/0.8'}
T5qqqqWW_mGo1400_mChi1000 = {'name':'T5qqqqWW_mGo1400_mChi1000', 'chain':getChain(allSignals[0][1400][1000],histname=''), 'color':ROOT.kMagenta+2,    'weight':signalweight, 'niceName':'T5qqqqWW 1.4/1.0'}
T5qqqqWW_mGo1600_mChi100 = {'name':'T5qqqqWW_mGo1600_mChi100', 'chain':getChain(allSignals[0][1600][100],histname=''), 'color':ROOT.kRed+1, 'weight':signalweight, 'niceName':'T5qqqqWW 1.6/0.1'}

signals = [T5qqqqWW_mGo1200_mChi800,T5qqqqWW_mGo1400_mChi1000,T5qqqqWW_mGo1600_mChi100]

data = {'name':'data', 'chain':getChain([single_mu_Run2016B, single_ele_Run2016B, single_mu_Run2016C, single_ele_Run2016C, single_mu_Run2016D, single_ele_Run2016D],histname=''), 'color':ROOT.kBlack,'weight':'weight', 'niceName':'data', 'cut':False}


mcpresel = '!isData&&singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>4&&htJet30j>500 && Flag_badChargedHadronFilter && Flag_badMuonFilter'

triggers = "((HLT_EleHT350||HLT_EleHT400||HLT_Ele105)||(HLT_MuHT350||HLT_MuHT400))"
filters = "(Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_goodVertices && Flag_eeBadScFilter &&  Flag_globalTightHalo2016Filter && Flag_badChargedHadronFilter && Flag_badMuonFilter)"
datapresel = "isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+'&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>4&&htJet30j>500'

MCweight = '12.88/3.*weight*TopPtWeight*puReweight_true_max4*(singleMuonic*'+muTriggerEff+' + singleElectronic*'+eleTriggerErr+')*lepton_muSF_HIP*lepton_muSF_mediumID*lepton_muSF_miniIso02*lepton_muSF_sip3d*lepton_eleSF_cutbasedID*lepton_eleSF_miniIso01*lepton_eleSF_gsf'

bTagWeightSuffices = ['0_SF', '1_SF', '2_SF', '3p_SF']

can = ROOT.TCanvas('c','c',700,700)
bottomMargin = 0.
marginForPad2 = 0.3

pad1=ROOT.TPad("pad1","MyTitle",0.,marginForPad2,1.,1.)
pad1.SetLeftMargin(0.13)
pad1.SetBottomMargin(bottomMargin)
pad1.Draw()
pad1.cd()


TT_SF_H   = ROOT.TH1F('TT_SF_H','',4,0,4) 
TT_H      = ROOT.TH1F('TT_H','',4,0,4)
W_SF_H    = ROOT.TH1F('W_SF_H','',4,0,4)
W_H       = ROOT.TH1F('W_H','',4,0,4)
DY_SF_H   = ROOT.TH1F('DY_SF_H','',4,0,4)
DY_H      = ROOT.TH1F('DY_H','',4,0,4)
singleTop_SF_H    = ROOT.TH1F('singleTop_SF_H','',4,0,4)
singleTop_H       = ROOT.TH1F('singleTop_H','',4,0,4)
TTVH_SF_H   = ROOT.TH1F('TTVH_SF_H','',4,0,4)
diBoson_SF_H   = ROOT.TH1F('diBoson_SF_H','',4,0,4)

TTVH_H      = ROOT.TH1F('TTVH_H','',4,0,4)

rest_SF_H = ROOT.TH1F('rest_SF_H','',4,0,4)
rest_H    = ROOT.TH1F('rest_H','',4,0,4)
QCD_H     = ROOT.TH1F('QCD_H','',4,0,4)

S1_H      = ROOT.TH1F('S1_H','T5q^{4}WW 1.0/0.7',4,0,4)
S2_H      = ROOT.TH1F('S2_H','T5q^{4}WW 1.2/0.8',4,0,4)
S3_H      = ROOT.TH1F('S3_H','T5q^{4}WW 1.5/0.1',4,0,4)

T5qqqqWW_mGo1200_mChi800_H = ROOT.TH1F('T5qqqqWW_mGo1200_mChi800_H','T5qqqqWW 1.2/0.8 x10',10,0,10)
T5qqqqWW_mGo1400_mChi1000_H = ROOT.TH1F('T5qqqqWW_mGo1400_mChi1000_H','T5qqqqWW 1.4/1.0 x10',10,0,10)
T5qqqqWW_mGo1600_mChi100_H = ROOT.TH1F('T5qqqqWW_mGo1600_mChi100_H','T5qqqqWW 1.6/0.1 x10',10,0,10)



signal_SF_H2 = [T5qqqqWW_mGo1200_mChi800_H,T5qqqqWW_mGo1400_mChi1000_H,T5qqqqWW_mGo1600_mChi100_H]


EWK_SF_H = [W_SF_H, TT_SF_H, DY_SF_H, singleTop_SF_H, TTVH_SF_H, diBoson_SF_H]
signal_SF_H = [S1_H, S2_H, S3_H]

total_SF_H  = ROOT.TH1F('total_SF_H','',4,0,4)
total_H     = ROOT.TH1F('total_H','',4,0,4)
total_H.Sumw2()
total_SF_H.Sumw2()

presel = signalpresel
alpha = 1.
signalScale = 10

for i,suffix in enumerate(bTagWeightSuffices):
  for j,sample in enumerate(EWK):
    y, y_e = getYieldFromChain(sample['chain'], mcpresel, weight=MCweight+'*weightBTag'+suffix, returnError=True)
    EWK_SF_H[j].SetBinContent(i+1,y)
    EWK_SF_H[j].SetBinError(i+1,y_e)
    EWK_SF_H[j].SetFillColorAlpha(sample['color'], alpha)
    EWK_SF_H[j].SetLineColor(sample['color'])
    EWK_SF_H[j].SetLineColor(ROOT.kBlack)
    EWK_SF_H[j].SetLineWidth(2)
  for j, sample in enumerate(signals):
    y, y_e = getYieldFromChain(sample['chain'], signalpresel, weight=signalweight+'*weightBTag'+suffix, returnError=True)
    signal_SF_H[j].SetBinContent(i+1,y)
    signal_SF_H[j].SetBinError(i+1,y_e)
    signal_SF_H[j].SetLineColor(sample['color'])
    signal_SF_H[j].SetLineWidth(4)
  for j, sample in enumerate(signals):
    y, y_e = getYieldFromChain(sample['chain'], signalpresel, weight=signalweight+'*weightBTag'+suffix, returnError=True)
    signal_SF_H2[j].SetBinContent(i+1,y)
    signal_SF_H2[j].SetBinError(i+1,y_e)
    signal_SF_H2[j].SetLineColor(sample['color'])
    signal_SF_H2[j].SetLineWidth(4)
    signal_SF_H2[j].SetMarkerColor(sample['color'])
    signal_SF_H2[j].SetMarkerSize(0)
    

for i in range(4,10):
  for j, sample in enumerate(signals):
    signal_SF_H2[j].SetBinContent(i+1,0)
    signal_SF_H2[j].SetBinError(i+1,0)

path = '/afs/hephy.at/user/d/dspitzbart/www/Results2016B/'
for s in signal_SF_H2:
  s.Scale(signalScale)
  ROOT.TFile(path+'hists.root','new')
  


bkg_H = []
binning = [4,0,4]
var = 'nBJetMediumCSV30'

for i,sample in enumerate(samples):
  bkg_H.append(getPlotFromChain(sample['chain'], var, binning, cutString = mcpresel, weight = MCweight, addOverFlowBin='upper'))
  total_H.Add(bkg_H[-1])

for h in EWK_SF_H:
  total_SF_H.Add(h)
total_SF_H.Add(bkg_H[-1])

data_H = getPlotFromChain(data['chain'], var, binning, cutString = datapresel, weight = '(1)', addOverFlowBin='upper')

h_Stack = ROOT.THStack('h_Stack','Stack')
h_Stack_SF = ROOT.THStack('h_Stack_SF','Stack')

for h in reversed(bkg_H):
  h_Stack.Add(h)

bkg_H[-1].SetFillColorAlpha(QCD['color'],0.8)
bkg_H[-1].SetLineColor(QCD['color'])
bkg_H[-1].SetLineColor(ROOT.kBlack)
bkg_H[-1].SetLineWidth(2)

data_H.SetMarkerSize(1.2)
data_H.SetLineWidth(2)

h_Stack_SF.Add(TTVH_SF_H)
h_Stack_SF.Add(diBoson_SF_H)
h_Stack_SF.Add(singleTop_SF_H)
h_Stack_SF.Add(DY_SF_H)
#h_Stack_SF.Add(TT_SF_H)
h_Stack_SF.Add(bkg_H[-1])
h_Stack_SF.Add(TT_SF_H)
h_Stack_SF.Add(W_SF_H)

total_H.SetLineColor(ROOT.kRed+1)
total_H.SetLineWidth(2)
total_H.SetMarkerStyle(22)
total_H.SetMarkerSize(1.2)
total_H.SetMarkerColor(ROOT.kRed+1)


total_SF_H.SetLineColor(ROOT.kGray+1)
total_SF_H.SetLineWidth(2)

#leg = ROOT.TLegend(0.98-0.282,0.59,0.98,0.95)
leg = ROOT.TLegend(0.65,0.58,0.93,0.925)
leg.SetBorderSize(1)
leg.SetFillColor(0)
leg.SetLineColor(0)
#leg.SetFillColor(ROOT.kWhite)
#leg.SetShadowColor(ROOT.kWhite)
#leg.SetBorderSize(1)
#leg.SetTextSize(0.035)

leg.AddEntry(data_H,'Data')
leg.AddEntry(W_SF_H, WJets['niceName'], 'f')
leg.AddEntry(TT_SF_H, TTJets['niceName'], 'f')
leg.AddEntry(bkg_H[-1], QCD['niceName'], 'f')
leg.AddEntry(DY_SF_H, DY['niceName'], 'f')
leg.AddEntry(singleTop_SF_H, singleTop['niceName'], 'f')
leg.AddEntry(diBoson_SF_H, diBoson['niceName'],'f')
leg.AddEntry(TTVH_SF_H, TTVH['niceName'], 'f')

#leg3 = ROOT.TLegend(0.98-0.4-0.25,0.92-3*0.037,0.98-0.282-0.02,0.92)
leg3 = ROOT.TLegend(0.3,0.8,0.6,0.925)
leg3.SetFillColor(ROOT.kWhite)
leg3.SetShadowColor(ROOT.kWhite)
leg.SetLineColor(0)
leg3.SetBorderSize(0)
#leg3.SetTextSize(0.035)
leg3.AddEntry(T5qqqqWW_mGo1200_mChi800_H)
leg3.AddEntry(T5qqqqWW_mGo1400_mChi1000_H)
leg3.AddEntry(T5qqqqWW_mGo1600_mChi100_H)


h_Stack_SF.SetMinimum(10.)
h_Stack_SF.SetMaximum(1000000.)
h_Stack_SF.Draw('hist')
#h_Stack.GetXaxis().SetTitle(variable['titleX'])
#h_Stack.GetXaxis().SetNdivisions(508)
h_Stack_SF.GetYaxis().SetTitle('Events')
h_Stack_SF.GetYaxis().SetTitleOffset(1.05)
#h_Stack_SF.GetYaxis().SetLabelSize(0.06)

pad1.SetLogy()

h_Stack_SF.GetYaxis().SetLabelSize(0.06)

total_SF_H.Draw('hist')
#total_H.Draw('hist same')
h_Stack_SF.Draw('hist')
data_H.Draw('e1p same')

for s in signal_SF_H:
  s.Scale(signalScale)

S1_H.Draw('hist same')
S2_H.Draw('hist same')
S3_H.Draw('hist same')

leg.Draw()
leg3.Draw()


dataMCH = ROOT.TH1F('dataMCH','DataMC',*binning)
dataMC_SF_H = ROOT.TH1F('dataMC_SF_H','DataMC',*binning)

one = ROOT.TH1F('one','one',*binning)
for i in range(1,5):
  one.SetBinContent(i,1)

one.SetLineColor(ROOT.kBlue)
one.SetLineWidth(2)

dataMCH.Sumw2()
#total_H.Sumw2()
dataMCH = data_H.Clone()
dataMCH.Divide(total_H)

dataMC_SF_H.Sumw2()
dataMC_SF_H = data_H.Clone()
dataMC_SF_H.Divide(total_SF_H)

can.cd()
pad2=ROOT.TPad("pad2","datavsMC",0.,0.,1.,.3)
pad2.SetLeftMargin(0.13)
pad2.SetBottomMargin(0.3)
pad2.SetTopMargin(0.)
#pad2.SetGrid()
pad2.Draw()
pad2.cd()

for i in range(3):
  dataMC_SF_H.GetXaxis().SetBinLabel(i+1,str(i))
dataMC_SF_H.GetXaxis().SetBinLabel(4,'#geq3')
dataMC_SF_H.GetXaxis().SetTitle('n_{b-jets}')
dataMC_SF_H.GetXaxis().SetTitleSize(0.13)
dataMC_SF_H.GetXaxis().SetLabelSize(0.23)
dataMC_SF_H.GetXaxis().SetNdivisions(508)
dataMC_SF_H.GetYaxis().SetTitle('Data/Pred.')
dataMC_SF_H.GetYaxis().SetTitleSize(0.13)
dataMC_SF_H.GetYaxis().SetLabelSize(0.13)
dataMC_SF_H.GetYaxis().SetTitleOffset(0.5)
dataMC_SF_H.GetYaxis().SetNdivisions(508)
dataMC_SF_H.SetMinimum(0.)
dataMC_SF_H.SetMaximum(2.2)
#dataMC_SF_H.SetMarkerColor(ROOT.kRed+1)
#dataMC_SF_H.SetMarkerStyle(22)
#dataMC_SF_H.SetMarkerSize(1.4)
#dataMCH.Draw('e1p')

#dataMC_SF_H.SetMarkerStyle(23)
#dataMC_SF_H.SetMarkerSize(1.4)
dataMC_SF_H.Draw('e1p')
one.Draw('hist same')

can.cd()
pad1.cd()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.13,0.96,'CMS #bf{#it{Preliminary}}')
latex1.DrawLatex(0.79,0.96,"12.9fb^{-1} (13TeV)")

can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/nbjet_nJet5.png')
can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/nbjet_nJet5.pdf')
can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/nbjet_nJet5.root')

