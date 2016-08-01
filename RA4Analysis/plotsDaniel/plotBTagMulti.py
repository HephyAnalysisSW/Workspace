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

ROOT.gStyle.SetErrorX(0.5)

def Draw_CMS_header():
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextAlign(31)
   tex.SetTextFont(42)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(0.96,0.96,"12.9 fb^{-1} (13 TeV)")
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextFont(61)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(0.18,0.96,"CMS")
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextFont(52)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(0.26,0.96,"Preliminary")
   return

def Set_axis_pad2(histo):
   histo.GetXaxis().SetLabelFont(42)
   histo.GetXaxis().SetLabelOffset(0.007)
   histo.GetXaxis().SetLabelSize(0.11)
   histo.GetXaxis().SetTitleSize(0.14)
   histo.GetXaxis().SetTitleOffset(0.9)
   histo.GetXaxis().SetTitleFont(42)
   histo.GetYaxis().SetTitle("Data/Pred.")
   histo.GetYaxis().SetDecimals()
   histo.GetYaxis().SetNdivisions(505)
   histo.GetYaxis().SetLabelFont(42)
   histo.GetYaxis().SetLabelOffset(0.007)
   histo.GetYaxis().SetLabelSize(0.11)
   histo.GetYaxis().SetTitleSize(0.14)
   histo.GetYaxis().SetTitleOffset(0.52)
   histo.GetYaxis().SetTitleFont(42)
   histo.GetZaxis().SetLabelFont(42)
   histo.GetZaxis().SetLabelOffset(0.007)
   histo.GetZaxis().SetLabelSize(0.05)
   histo.GetZaxis().SetTitleSize(0.06)
   histo.GetZaxis().SetTitleFont(42)
   return

def Set_axis_pad1(histo):
   histo.GetXaxis().SetLabelFont(42)
   histo.GetXaxis().SetLabelOffset(0.007)
   histo.GetXaxis().SetLabelSize(0.05)
   histo.GetXaxis().SetTitleSize(0.06)
   histo.GetXaxis().SetTitleOffset(0.9)
   histo.GetXaxis().SetTitleFont(42)
   histo.GetYaxis().SetLabelFont(42)
   histo.GetYaxis().SetLabelOffset(0.007)
   histo.GetYaxis().SetLabelSize(0.05)
   histo.GetYaxis().SetTitleSize(0.06)
   histo.GetYaxis().SetTitleOffset(1.35)
   histo.GetYaxis().SetTitleFont(42)
   histo.GetZaxis().SetLabelFont(42)
   histo.GetZaxis().SetLabelOffset(0.007)
   histo.GetZaxis().SetLabelSize(0.05)
   histo.GetZaxis().SetTitleSize(0.06)
   histo.GetZaxis().SetTitleFont(42)
   return


WJets = {'name':'WJets', 'chain':getChain(WJetsHTToLNu,histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W + jets'}
TTJets = {'name':'TTJets', 'chain':getChain(TTJets_Comb,histname=''), 'color':color('TTJets')-2,'weight':'weight', 'niceName':'t#bar{t} + jets'}
DY = {'name':'DY', 'chain':getChain(DY_HT,histname=''), 'color':color('DY'),'weight':'weight', 'niceName':'DY + jets'}
singleTop = {'name':'singleTop', 'chain':getChain(singleTop_lep,histname=''), 'color':color('singleTop'),'weight':'weight', 'niceName':'t/#bar{t}'}
QCD = {'name':'QCD', 'chain':getChain(QCDHT,histname=''), 'color':color('QCD'),'weight':'weight', 'niceName':'QCD'}
TTVH = {'name':'TTVH', 'chain':getChain(TTV,histname=''), 'color':color('TTV'),'weight':'weight', 'niceName':'t#bar{t}V'}
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

can = ROOT.TCanvas('c','c',564,232,600,600)
bottomMargin = 0.
marginForPad2 = 0.3
can.SetHighLightColor(2)
can.Range(0,0,1,1)
can.SetFillColor(0)
can.SetBorderMode(0)
can.SetBorderSize(2)
can.SetTickx(1)
can.SetTicky(1)
can.SetLeftMargin(0.18)
can.SetRightMargin(0.04)
can.SetTopMargin(0.05)
can.SetBottomMargin(0.13)
can.SetFrameFillStyle(0)
can.SetFrameBorderMode(0)
can.SetFrameFillStyle(0)
can.SetFrameBorderMode(0)
can.cd()



pad1=ROOT.TPad("pad1","MyTitle",0,0.31,1,1)
pad1.Draw()
pad1.cd()
pad1.SetFillColor(0)
pad1.SetBorderMode(0)
pad1.SetBorderSize(2)
pad1.SetLogy()
pad1.SetTickx(1)
pad1.SetTicky(1)
pad1.SetLeftMargin(0.18)
pad1.SetRightMargin(0.04)
pad1.SetTopMargin(0.055)
pad1.SetBottomMargin(0)
pad1.SetFrameFillStyle(0)
pad1.SetFrameBorderMode(0)
pad1.SetFrameFillStyle(0)
pad1.SetFrameBorderMode(0)
pad1.SetLogy()



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
  h.Scale(0.9)
  total_SF_H.Add(h)
  Set_axis_pad1(h)
total_SF_H.Add(bkg_H[-1])

#data_H = getPlotFromChain(data['chain'], var, binning, cutString = datapresel, weight = '(1)', addOverFlowBin='upper')
data_H = ROOT.TH1F('data','data',4,0,4)
for a in range(3):
  y = getYieldFromChain(data['chain'], datapresel+'&&nBJetMediumCSV30=='+str(a))
  data_H.SetBinContent(a+1,y)
  data_H.SetBinError(a+1, sqrt(y))
y = getYieldFromChain(data['chain'], datapresel+'&&nBJetMediumCSV30>=3')
data_H.SetBinContent(4,y)
data_H.SetBinError(4, sqrt(y))

h_Stack = ROOT.THStack('h_Stack','Stack')
h_Stack_SF = ROOT.THStack('h_Stack_SF','Stack')

for h in reversed(bkg_H):
  h_Stack.Add(h)

bkg_H[-1].SetFillColorAlpha(QCD['color'],0.8)
bkg_H[-1].SetLineColor(QCD['color'])
bkg_H[-1].SetLineColor(ROOT.kBlack)
bkg_H[-1].SetLineWidth(2)

data_H.SetMarkerStyle(20)
data_H.SetMarkerSize(1.1)

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
#h_Stack_SF.GetYaxis().SetTitleOffset(1.05)
#h_Stack_SF.GetYaxis().SetLabelSize(0.06)

pad1.SetLogy()

#h_Stack_SF.GetYaxis().SetLabelSize(0.06)

total_SF_H.Draw('hist')
#total_H.Draw('hist same')
h_Stack_SF.Draw('hist')

Set_axis_pad1(data_H)
#data_H.GetYaxis().SetLabelSize(0.04)
data_H.SetMarkerStyle(20)
data_H.SetMarkerSize(1.1)
data_H.Draw('E1 same')

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

Draw_CMS_header()
pad1.RedrawAxis()

can.cd()
pad2 = ROOT.TPad("pad2", "pad2",  0, 0, 1, 0.31)
pad2.Draw()
pad2.cd()
pad2.SetFillColor(0)
pad2.SetFillStyle(4000)
pad2.SetBorderMode(0)
pad2.SetBorderSize(2)
pad2.SetTickx(1)
pad2.SetTicky(1)
pad2.SetLeftMargin(0.18)
pad2.SetRightMargin(0.04)
pad2.SetTopMargin(0)
pad2.SetBottomMargin(0.3)
pad2.SetFrameFillStyle(0)
pad2.SetFrameBorderMode(0)
pad2.SetFrameFillStyle(0)
pad2.SetFrameBorderMode(0)



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
dataMC_SF_H.SetMinimum(0.05)
dataMC_SF_H.SetMaximum(1.95)
#dataMC_SF_H.SetMarkerColor(ROOT.kRed+1)
#dataMC_SF_H.SetMarkerStyle(22)
#dataMC_SF_H.SetMarkerSize(1.4)
#dataMCH.Draw('e1p')

Set_axis_pad2(dataMC_SF_H)

dataMC_SF_H.GetXaxis().SetLabelSize(0.18)
#dataMC_SF_H.SetMarkerStyle(23)
#dataMC_SF_H.SetMarkerSize(1.4)
dataMC_SF_H.Draw('E1')
one.Draw('hist same')
dataMC_SF_H.Draw('E1 same')

can.cd()
pad1.cd()

#latex1 = ROOT.TLatex()
#latex1.SetNDC()
#latex1.SetTextSize(0.04)
#latex1.SetTextAlign(11)
#
#latex1.DrawLatex(0.13,0.96,'CMS #bf{#it{Preliminary}}')
#latex1.DrawLatex(0.79,0.96,"12.9fb^{-1} (13TeV)")

can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/nbjet_nJet5_v2.png')
can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/nbjet_nJet5_v2.pdf')
can.Print('/afs/hephy.at/user/d/dspitzbart/www/Results2016B/nbjet_nJet5_v2.root')

