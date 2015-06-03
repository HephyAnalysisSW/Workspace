import ROOT
import os, sys, copy

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2 import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_softLepton import *
from Workspace.RA4Analysis.helpers import *
from rCShelpers import *


binning=[30,0,1500]

#prepresel = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&nBJetMediumCSV30==0&&htJet30j>500&&st>200&&nJet30>=6&&Jet_pt[2]>80'
prepresel = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[2]>80'

lepGen = 'all'
if lepGen == 'ele':
  presel = prepresel+'&&abs(LepGood_pdgId)==11'
elif lepGen == 'mu':
  presel = prepresel+'&&abs(LepGood_pdgId)==13'
else:
  presel = prepresel

#prepresel = 'singleLeptonic==1&&'#&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'
#presel = prepresel + 'Jet_pt[1]>80&&nJet30>=2&&nBJetMediumCMVA30==0&&st>=150&&st<=250'#&&htJet30j>500&&htJet30j<750'#&&htJet30j>=500&&st>=200&&deltaPhi_Wl>1&&mt2w>350'
#prepresel = 'singleLeptonic==1&&nLooseSoftLeptons==1&&nLooseHardLeptons==0&&nTightHardLeptons==0&&nBJetMediumCSV30==0&&htJet30j>500&&st>200&&nJet30>=2&&Jet_pt[2]>80'#&&abs(LepGood_pdgId)==11'
#presel='htJet25>400&&(abs(genPartAll_pdgId)==11||abs(genPartAll_pdgId)==13)&&(abs(genPartAll_motherId)==24||abs(genPartAll_motherId)==1000024)'
#presel='(abs(genLep_pdgId)==11||abs(genLep_pdgId)==13)&&(abs(genLep_motherId)==24||abs(genLep_motherId)==1000024)'
#presel='abs(genPartAll_pdgId)==1000022&&abs(genPartAll_motherId)==1000024'
#presel='abs(genPartAll_pdgId)==1000024'

st = {'varString': 'st','binning': [30,0,1500], 'name': 'S_{T} (GeV)', 'yLegend':"Number of Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV"}
met = {'varString': 'met_pt','binning': [20,0,1000], 'name': '#slash{E}_{T} (GeV)', 'yLegend':"Number of Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV"}
leptonPt = {'varString': 'leptonPt','binning': [40,0,800], 'name': 'p_{T}(l) (GeV)', 'yLegend':"Number of Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV"}
jetPt = {'varString': 'Jet_pt[1]','binning': [20,0,1600], 'name': 'p_{T}(leading Jet) (GeV)', 'yLegend':"Number of Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV"}
ht = {'varString': 'htJet30j','binning': [25,0,2500], 'name': 'H_{T} (GeV)', 'yLegend':"Number of Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV"}
deltaPhi = {'varString': 'deltaPhi_Wl','binning': [32,0,3.2], 'name': '#Delta#Phi(W,l)', 'yLegend':'Number of Events'}

var = deltaPhi

signalString='T5qqqqWW_softLep'

#varstring="genPartAll_pt"
legendName = var['name']
binning = var['binning']
varstring = var['varString']
plotDir='/afs/hephy.at/user/d/dspitzbart/www/SRplots/'

lepSel='hard'

stReg=[(250,350),(350,450),(450,-1)]#,(600,-1)]#,(350,450),(450,-1)]#,(450,-1)]#,(350,450),(450,-1)]#250),(250,350),(350,450),(450,-1)]
htReg=[(500,750),(750,1000),(1000,1250),(1250,-1)]#,(750,1000),(1000,1250),(1250,-1)]#,(1250,-1)]
jetReg = [(2,2),(3,3),(4,4),(5,5),(6,7),(8,-1)]#,(8,8)]#,(8,-1)]#,(6,-1)]#,(8,-1)]#,(6,-1),(8,-1)]
btb = (0,0)

#BKG Samples
WJETS = getChain(WJetsHTToLNu[lepSel],histname='')
TTJETS = getChain(ttJets[lepSel],histname='')
TTVH = getChain(TTVH[lepSel],histname='')
SINGLETOP = getChain(singleTop[lepSel],histname='')
DY = getChain(DY[lepSel],histname='')
QCD = getChain(QCD[lepSel],histname='')

#SIG Samples
SIG1 = getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname='')
SIG2 = getChain(T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel],histname='')
SIG3 = getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname='')

#SIG1 = getChain(T5qqqqWWDeg_mGo1000_mCh325_mChi300[lepSel],histname='')
#SIG2 = getChain(T5qqqqWWDeg_mGo1000_mCh315_mChi300[lepSel],histname='')
#SIG3 = getChain(T5qqqqWWDeg_mGo1000_mCh310_mChi300[lepSel],histname='')
#SIG4 = getChain(T5qqqqWWDeg_mGo1400_mCh315_mChi300[lepSel],histname='')
#SIG5 = getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname='')
#SIG6 = getChain(T5qqqqWWDeg_mGo800_mCh305_mChi300[lepSel],histname='')


##not post processed signal
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
#
##not post processed bkg
##ttvh
#TTVH = ROOT.TChain('tree')
#TTVH.Add('/data/easilar/Phys14_V3/TTZJets/treeProducerSusySingleLepton/tree.root')
#TTVH.Add('/data/easilar/Phys14_V3/TTH/treeProducerSusySingleLepton/tree.root')
#TTVH.Add('/data/easilar/Phys14_V3/TTWJets/treeProducerSusySingleLepton/tree.root')
#
##tt jets
#TTJETS = ROOT.TChain('tree')
#TTJETS.Add('/data/easilar/Phys14_V3/TTJets/treeProducerSusySingleLepton/tree.root')
#
##w jets
#WJETS = ROOT.TChain('tree')
#WJETS.Add('/data/easilar/Phys14_V3/WJetsToLNu_HT100to200/treeProducerSusySingleLepton/tree.root')
#WJETS.Add('/data/easilar/Phys14_V3/WJetsToLNu_HT200to400/treeProducerSusySingleLepton/tree.root')
#WJETS.Add('/data/easilar/Phys14_V3/WJetsToLNu_HT400to600/treeProducerSusySingleLepton/tree.root')
#WJETS.Add('/data/easilar/Phys14_V3/WJetsToLNu_HT600toInf/treeProducerSusySingleLepton/tree.root')
#
##qcd
#QCD = ROOT.TChain('tree')
#QCD.Add('/data/easilar/Phys14_V3/QCD_HT_100To250/treeProducerSusySingleLepton/tree.root')
#QCD.Add('/data/easilar/Phys14_V3/QCD_HT_250To500/treeProducerSusySingleLepton/tree.root')
#QCD.Add('/data/easilar/Phys14_V3/QCD_HT_500To1000/treeProducerSusySingleLepton/tree.root')
#QCD.Add('/data/easilar/Phys14_V3/QCD_HT_1000ToInf/treeProducerSusySingleLepton/tree.root')
#
##drell yan
#DY = ROOT.TChain('tree')
#DY.Add('/data/easilar/Phys14_V3/DYJetsToLL_M50_HT100to200/treeProducerSusySingleLepton/tree.root')
#DY.Add('/data/easilar/Phys14_V3/DYJetsToLL_M50_HT200to400/treeProducerSusySingleLepton/tree.root')
#DY.Add('/data/easilar/Phys14_V3/DYJetsToLL_M50_HT400to600/treeProducerSusySingleLepton/tree.root')
#DY.Add('/data/easilar/Phys14_V3/DYJetsToLL_M50_HT600toInf/treeProducerSusySingleLepton/tree.root')
#
##single top
#SINGLETOP = ROOT.TChain('tree')
#SINGLETOP.Add('/data/easilar/Phys14_V3/TBarToLeptons_sch/treeProducerSusySingleLepton/tree.root')
#SINGLETOP.Add('/data/easilar/Phys14_V3/TBarToLeptons_tch/treeProducerSusySingleLepton/tree.root')
#SINGLETOP.Add('/data/easilar/Phys14_V3/TBar_tWch/treeProducerSusySingleLepton/tree.root')
#SINGLETOP.Add('/data/easilar/Phys14_V3/TToLeptons_sch/treeProducerSusySingleLepton/tree.root')
#SINGLETOP.Add('/data/easilar/Phys14_V3/TToLeptons_tch/treeProducerSusySingleLepton/tree.root')
#SINGLETOP.Add('/data/easilar/Phys14_V3/T_tWch/treeProducerSusySingleLepton/tree.root')



wjets = {"name":"W + Jets", "chain":WJETS, "weight":"weight", "color":color('wjets')}
ttjets = {"name":"t#bar{t} + Jets", "chain":TTJETS, "weight":"weight", "color":color('ttjets')}
ttvh = {"name":"TTVH", "chain":TTVH, "weight":"weight", "color":color('ttvh')}
singletop = {"name":"single top", "chain":SINGLETOP, "weight":"weight", "color":color('singletop')}
dy = {"name":"Drell Yan", "chain":DY, "weight":"weight", "color":color('dy')}
qcd = {"name":"QCD", "chain":QCD, "weight":"weight", "color":color('qcd')}

signal1 = {'name':'T5qqqqWW_mGo1000_mCh800_mChi700', 'legendName': 'T5qqqqWW (1.0/0.8/0.7)', 'chain':SIG1, 'weight':'weight', 'color':ROOT.kRed-7, "histo":ROOT.TH1F("Signal 1", "sqrt(s)", *binning), 'niceName':'T5qqqqWW m_{\\tilde{g}}=1000, m_{\\tilde{\\chi}_{1}^{+}}=800, m_{\\tilde{\\chi}_{1}^{0}}=700'}
signal2 = {'name':'T5qqqqWW_mGo1200_mCh1000_mChi800', 'legendName': 'T5qqqqWW (1.2/1.0/0.8)', 'chain':SIG2, 'weight':'weight', 'color':ROOT.kRed-3, "histo":ROOT.TH1F("Signal 2", "sqrt(s)", *binning), 'niceName':'T5qqqqWW m_{\\tilde{g}}=1200, m_{\\tilde{\\chi}_{1}^{+}}=1000, m_{\\tilde{\\chi}_{1}^{0}}=800'}
signal3 = {'name':'T5qqqqWW_mGo1500_mCh800_mChi100', 'legendName': 'T5qqqqWW (1.5/0.8/0.1)', 'chain':SIG3, 'weight':'weight', 'color':ROOT.kRed+2, "histo":ROOT.TH1F("Signal 3", "sqrt(s)", *binning), 'niceName':'T5qqqqWW m_{\\tilde{g}}=1500, m_{\\tilde{\\chi}_{1}^{+}}=800, m_{\\tilde{\\chi}_{1}^{0}}=100'}


#signal1 = {'name':'T5qqqqWWDeg_mGo1000_mCh325_mChi300', 'chain':SIG1, 'weight':'weight', 'color':ROOT.kRed-7, "histo":ROOT.TH1F("Signal 1", "sqrt(s)", *binning), 'niceName':'T5qqqqWW m_{\\tilde{g}}=1000, m_{\\tilde{\\chi}_{1}^{+}}=325, m_{\\tilde{\\chi}_{1}^{0}}=300'}
#signal2 = {'name':'T5qqqqWWDeg_mGo1000_mCh315_mChi300', 'chain':SIG2, 'weight':'weight', 'color':ROOT.kRed-3, "histo":ROOT.TH1F("Signal 2", "sqrt(s)", *binning), 'niceName':'T5qqqqWW m_{\\tilde{g}}=1000, m_{\\tilde{\\chi}_{1}^{+}}=315, m_{\\tilde{\\chi}_{1}^{0}}=300'}
#signal3 = {'name':'T5qqqqWWDeg_mGo1000_mCh310_mChi300', 'chain':SIG3, 'weight':'weight', 'color':ROOT.kRed+2, "histo":ROOT.TH1F("Signal 3", "sqrt(s)", *binning), 'niceName':'T5qqqqWW m_{\\tilde{g}}=1000, m_{\\tilde{\\chi}_{1}^{+}}=310, m_{\\tilde{\\chi}_{1}^{0}}=300'}
#signal4 = {'name':'T5qqqqWWDeg_mGo1400_mCh315_mChi300', 'chain':SIG4, 'weight':'weight', 'color':ROOT.kBlack, "histo":ROOT.TH1F("Signal 4", "sqrt(s)", *binning), 'niceName':'T5qqqqWW m_{\\tilde{g}}=1400, m_{\\tilde{\\chi}_{1}^{+}}=315, m_{\\tilde{\\chi}_{1}^{0}}=300'}
#signal5 = {'name':'T5qqqqWW_mGo1000_mCh800_mChi700', 'chain':SIG5, 'weight':'weight', 'color':ROOT.kMagenta+1, "histo":ROOT.TH1F("Signal 5", "sqrt(s)", *binning),'niceName':'T5qqqqWW m_{\\tilde{g}}=1000, m_{\\tilde{\\chi}_{1}^{+}}=800, m_{\\tilde{\\chi}_{1}^{0}}=700'}
#signal6 = {'name':'T5qqqqWWDeg_mGo800_mCh305_mChi300', 'chain':SIG6, 'weight':'weight', 'color':ROOT.kCyan+2, "histo":ROOT.TH1F("Signal 6", "sqrt(s)", *binning), 'niceName':'T5qqqqWW m_{\\tilde{g}}=800,  m_{\\tilde{\\chi}_{1}^{+}}=305, m_{\\tilde{\\chi}_{1}^{0}}=300'}




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
#sigSamples.append(signal4)
#sigSamples.append(signal5)
#sigSamples.append(signal6)


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
bkgSamples.append(wjets)
bkgSamples.append(singletop)
bkgSamples.append(ttjets)

#h_Stack = ROOT.THStack('h_Stack',varstring)
#h_Stack_S = ROOT.THStack('h_Stack_S',varstring)
#
#can1 = ROOT.TCanvas(varstring,varstring,800,700)
#
#h1=ROOT.TH1F("MCDataCombined","MCDataCombined", *binning)
#h3=ROOT.TH1F("MCDataCombined","MCDataCombined", *binning)
#
#l = ROOT.TLegend(0.6,0.65,.95,.95)
#l.SetFillColor(0)
#l.SetShadowColor(ROOT.kWhite)
#l.SetBorderSize(1)

allRCS = []

for st in stReg:
  for ht in htReg:
    for jet in jetReg:
      
      cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')
      rcs = getRCS(WJETS,cut,1.0)
      #print rcs
      allRCS.append({'ST':st,'HT':ht,'njets':jet,'rcs':rcs['rCS']})
      h_Stack = ROOT.THStack('h_Stack',varstring)
      h_Stack_S = ROOT.THStack('h_Stack_S',varstring)
      
      can1 = ROOT.TCanvas(varstring,varstring,800,700)
      
      h1=ROOT.TH1F("MCDataCombined","MCDataCombined", *binning)
      h3=ROOT.TH1F("MCDataCombined","MCDataCombined", *binning)
      
      l = ROOT.TLegend(0.6,0.65,.95,.95)
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
        tot_lumi = 4000
        nevents = chain.GetEntries()
        #weight = "("+str(tot_lumi)+"*xsec)/"+str(nevents)
        #print 'Weight:', weight
        chain.Draw(varstring+'>>'+str(histoname),'weight*('+cut+')')#insert 'weight*('+
        histo.SetLineColor(ROOT.kBlack)
        histo.SetLineWidth(1)
        histo.SetMarkerSize(0)
        histo.SetMarkerStyle(0)
        histo.SetTitleSize(20)
        histo.GetXaxis().SetTitle(legendName)
        histo.GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
        histo.GetXaxis().SetLabelSize(0.04)
        histo.GetYaxis().SetLabelSize(0.04)
        histo.GetYaxis().SetTitleOffset(0.8)
        histo.GetYaxis().SetTitleSize(0.05)
        histo.SetFillColor(sample["color"])
        histo.SetFillStyle(1001)
        histo.SetMinimum(.008)
        h_Stack.Add(histo)
        print sample["name"], "Histogram has ", histo.GetSumOfWeights(), " entries"
        h1.Add(histo)
        l.AddEntry(histo, sample["name"])
      
      for sample in sigSamples:
        chain = sample["chain"]
        print chain
        histo = 'h_'+sample["name"]
        histoname = histo
        print histoname
        histo = ROOT.TH1F(str(histo), sample['legendName'],*binning)
        print histo
        color = sample["color"]
        print color
        tot_lumi = 4000
        nevents = chain.GetEntries()
        #weight = "("+str(tot_lumi)+"*xsec)/"+str(nevents)
        #print 'Weight:', weight
        chain.Draw(varstring+'>>'+str(histoname),'weight*('+cut+')')#'weight*('+
        histo.SetLineColor(color)
        histo.SetLineWidth(2)
        histo.SetMarkerSize(0)
        histo.SetMarkerStyle(0)
        histo.SetTitleSize(20)
        histo.GetXaxis().SetTitle(legendName)
        histo.GetXaxis().SetLabelSize(0.04)
        histo.GetXaxis().SetTitleOffset(0.3)
        histo.GetXaxis().SetTitleSize(0.06)
        histo.GetYaxis().SetTitle("Events")
        histo.GetYaxis().SetLabelSize(0.04)
        histo.GetYaxis().SetTitleOffset(0.3)
        histo.GetYaxis().SetTitleSize(0.06)
        histo.SetFillColor(0)
        histo.SetMinimum(.008)
        h_Stack_S.Add(histo)
        h3.Add(histo)
        l.AddEntry(histo)
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
      
      histo.GetXaxis().SetTitle(legendName)
      histo.GetXaxis().SetLabelSize(0.04)
      histo.GetXaxis().SetTitleOffset(0.3)
      histo.GetXaxis().SetTitleSize(0.15)
      
      histo.GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
      histo.GetYaxis().SetLabelSize(0.04)
      histo.GetYaxis().SetTitleOffset(0.3)
      histo.GetYaxis().SetTitleSize(0.15)
      
      
      
      h_Stack.Draw()
      h_Stack.SetMaximum(1100)
      h_Stack.SetMinimum(0.008)
      h_Stack_S.Draw('noStacksame')
      #h_Stack_S.Draw('noStack')
      h_Stack.GetYaxis().SetTitle(var['yLegend']) #add _S if no bkg
      h_Stack.GetYaxis().SetLabelSize(0.05)
      h_Stack.GetYaxis().SetTitleOffset(1.3)
      h_Stack.GetYaxis().SetTitleSize(0.05)
      h_Stack.GetXaxis().SetTitle(legendName)
      h_Stack.GetXaxis().SetLabelSize(0.05)
      h_Stack.GetXaxis().SetTitleOffset(1.1)
      h_Stack.GetXaxis().SetTitleSize(0.05)
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
      latex1 = ROOT.TLatex()
      latex1.SetNDC()
      latex1.SetTextSize(0.035)
      latex1.SetTextAlign(11) # align right
      latex1.DrawLatex(0.16,0.96,'CMS Simulation')
      latex1.DrawLatex(0.75,0.96,'L=4fb^{-1} (13TeV)')
      
      
      can1.Print(plotDir+varstring+'_'+cutname+'_'+lepGen+'.png')
      can1.Print(plotDir+varstring+'_'+cutname+'_'+lepGen+'.pdf')
      can1.Print(plotDir+varstring+'_'+cutname+'_'+lepGen+'.root')
      
      
      
      #can1.SetLogy()
      
