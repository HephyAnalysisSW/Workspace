import ROOT
from math import *
import os, sys
import pickle
from array import array
#from localInfo import username
username = "easilar"

#ROOT.gROOT.LoadMacro("/afs/hephy.at/scratch/e/easilar/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
#ROOT.setTDRStyle()
#ROOT.TH1F.SetDefaultSumw2()
#c = ROOT.TChain('tree')
#c.Add('root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/easilar/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/test1_REST_vienna_crab/T5qqqqWW_mGo1500_mCh800_mChi100/150425_201029/0000/susySingleLepton_1.root')

def getChain(path_files):
  c = ROOT.TChain('tree')
  c.Add('root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/easilar/babies/CMGTools-from-CMSSW_7_2_3_LocalDevelopments/'+path_files+'*.root')
  return c

#presel = '1'
singleLeptonic = 'nLepGood==1&&nLepOther==0'
#presel = 'htJet40j>500&&nJet40>0&&Jet_pt[1]>80&&LepGood_pt[0]+met_pt>200&&sum$(Jet_btagCMVA<0.732&&abs(Jet_eta)<2.4)==0'+'&&'+singleLeptonic
presel = 'Sum$(Jet_pt)>500&&nJet30>6&&Sum$(Jet_btagCMVA>0.732)==0&&Jet_pt[1]>80&&LepGood_pt[0]+met_pt>200'+'&&'+singleLeptonic

path = '/afs/hephy.at/user/e/easilar/www/fatJet/tests/'
if not os.path.exists(path):
  os.makedirs(path)

signals = [
{'cname':'T5qqqqWW_mGo1500_mCh800_mChi100' ,'label':'T5qqqqWW_mGo1500_mCh800_mLsp100' ,'chain':getChain(path_files='test1_REST_vienna_crab/T5qqqqWW_mGo1500_mCh800_mChi100/150425_201029/0000/'),'color':ROOT.kBlack},\
{'cname':'T5qqqqWW_mGo1200_mCh1000_mChi800','label':'T5qqqqWW_mGo1200_mCh1000_mLsp800','chain':getChain(path_files='test1_REST_vienna_crab/T5qqqqWW_mGo1200_mCh1000_mChi800/150425_201053/0000/'),'color':ROOT.kYellow},\
{'cname':'T5qqqqWW_mGo1000_mCh800_mChi700' ,'label':'T5qqqqWW_mGo1000_mCh800_mLsp700' ,'chain':getChain(path_files='test1_REST_vienna_crab/T5qqqqWW_mGo1000_mCh800_mChi700/150425_201117/0000/'),'color':ROOT.kRed},\
]
bkg = [
{'cname':'WJETS1','label':'WJETS','chain':getChain(path_files='test1_WJETS_vienna_crab/WJetsToLNu_HT100to200/150424_210540/0000/'),'color':ROOT.kAzure+10},\
{'cname':'WJETS2','label':'WJETS','chain':getChain(path_files='test1_WJETS_vienna_crab/WJetsToLNu_HT200to400/150424_210604/0000/'),'color':ROOT.kAzure+10},\
{'cname':'WJETS3','label':'WJETS','chain':getChain(path_files='test1_WJETS_vienna_crab/WJetsToLNu_HT400to600/150424_210628/0000/'),'color':ROOT.kAzure+10},\
{'cname':'WJETS4','label':'WJETS','chain':getChain(path_files='test1_WJETS_vienna_crab/WJetsToLNu_HT600toInf/150424_210652/0000/'),'color':ROOT.kAzure+10},\
{'cname':'TTJets','label':'TTJets','chain':getChain(path_files='test7_vienna_crab/TTJets/150423_124339/0000/'),'color':ROOT.kAzure},\
]
plots = [
{'logy':'False' , 'var':'nFatJet',                    'varname':'nFatJets',                   'bin':20,       'lowlimit':0,  'limit':20},\
{'logy':'true' , 'var':'FatJet_pt[0]',               'varname':'FatJet_pt[0]',                'bin':100,       'lowlimit':0,  'limit':2000},\
{'logy':'True' , 'var':'FatJet_prunedMass',          'varname':'FatJet_prunedMass',          'bin':100,       'lowlimit':0,  'limit':300},\
{'logy':'True' , 'var':'FatJet_trimmedMass',         'varname':'FatJet_trimmedMass',          'bin':100,       'lowlimit':0,  'limit':300},\
{'logy':'True' , 'var':'FatJet_filteredMass',        'varname':'FatJet_filteredMass',          'bin':100,       'lowlimit':0,  'limit':300},\
{'logy':'True' , 'var':'FatJet_tau1',                'varname':'FatJet_tau1',          'bin':100,       'lowlimit':0,  'limit':1},\
{'logy':'True' , 'var':'FatJet_tau2',                'varname':'FatJet_tau2',          'bin':100,       'lowlimit':0,  'limit':1},\
{'logy':'True' , 'var':'FatJet_tau3',                'varname':'FatJet_tau3',          'bin':100,       'lowlimit':0,  'limit':1},\
{'logy':'True' , 'var':'FatJet_tau3/FatJet_tau1',    'varname':'FatJet_tau3_1',          'bin':100,       'lowlimit':0,  'limit':1},\
{'logy':'True' , 'var':'FatJet_tau3/FatJet_tau2',    'varname':'FatJet_tau3_2',          'bin':100,       'lowlimit':0,  'limit':1},\
{'logy':'True' , 'var':'FatJet_tau2/FatJet_tau1',    'varname':'FatJet_tau2_1',          'bin':100,       'lowlimit':0,  'limit':1},\
{'logy':'False' , 'var':'Sum$(FatJet_prunedMass>70&&FatJet_prunedMass<100&&(FatJet_tau2/FatJet_tau1)<0.5)',    'varname':'nWtagged',          'bin':5,       'lowlimit':0,  'limit':5},\

]


for p in plots:
  can = ROOT.TCanvas(p['varname'],p['varname'],600,600)
  can.cd()
  h_Stack = ROOT.THStack('h_Stack',p['varname'])
  h_Stack_S = ROOT.THStack('h_Stack_S','h_Stack_S')
  leg = ROOT.TLegend(0.6,0.8,1,1)
  print p['varname']
  for b in bkg:
    color = b['color']
    print color
    print b['cname']  , b['chain']
    histo = 'h_'+b['cname']
    chain = b['chain']
    histoname = histo
    nEvents = chain.GetEntries()
    print histoname
    histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'],p['lowlimit'],p['limit'])
    print presel
    chain.Draw(p['var']+'>>'+str(histoname), '((xsec*4000)/'+str(nEvents)+')*('+presel+')')
    print histo
    histo.SetFillColor(color)
    histo.SetMinimum(.000001)
    h_Stack.Add(histo)
    leg.AddEntry(histo, b['label'],"f")
    del histo
  for s in signals:
    color = s['color']
    histo = 'h_'+s['cname']
    chain = s['chain']
    histoname = histo
    print histoname
    nEvents = chain.GetEntries()
    histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'],p['lowlimit'],p['limit'])
    #chain.Draw(p['var']+'>>'+str(histoname),str(weight)+'*('+presel+')')
    chain.Draw(p['var']+'>>'+str(histoname), '((xsec*4000)/'+str(nEvents)+')*('+presel+')')
    print histo
    histo.SetLineColor(color)
    histo.SetLineWidth(3)
    histo.SetLineWidth(3)
    histo.SetMinimum(.000001)
    h_Stack_S.Add(histo)
    #histo.Draw('same')
    leg.AddEntry(histo, s['cname'],"l")
  h_Stack.Draw()
  h_Stack_S.Draw('noStacksame')
  leg.SetFillColor(0)
  leg.Draw()
  if p['logy']: can.SetLogy()
  #can.Update()
  can.SaveAs(path+p['varname']+'.png')
  can.SaveAs(path+p['varname']+'.pdf')
  can.SaveAs(path+p['varname']+'.root')
  del can

