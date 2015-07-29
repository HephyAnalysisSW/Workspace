import ROOT
import pickle
import os,sys
from math import sqrt, cos, sin, atan2, acos, pi
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName, cmgMTClosestJetMET, cmgMTClosestBJetMET,  cmgMinDPhiJet, cmgMinDPhiBJet , cmgMTTopClosestJetMET , cmgHTOrthMET 
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.HEPHYPythonTools.user import username

ROOT.gROOT.Reset()
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()


lepSel = 'hard'

lumi = 3 #fb-1
#lumi = 0.1 #fb-1
weight_str = '((weight/4)*'+str(lumi)+')'

htCut = [500,10000000000]
#stCut = [250,350]
stCut = [200,10000000000]
njetCut = [4,20]
nbtagCut = 0
mt2Cut = 0
jetPtCut = 80
dfCut =0

prepresel = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'
#prepresel = 'singleElectronic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'
#prepresel = 'singleMuonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'
presel = prepresel+'deltaPhi_Wl>'+str(dfCut)+'&&Jet_pt[1]>='+str(jetPtCut)+'&&htJet30j>='+str(htCut[0])+'&&htJet30j<'+str(htCut[1])+'&&st>='+str(stCut[0])+'&&st<'+str(stCut[1])+'&&nJet30>='+str(njetCut[0])+'&&nJet30<'+str(njetCut[1])+'&&nBJetMediumCSV30=='+str(nbtagCut)
#path = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/toConvener/dilep_split_TT/draw_onlyTTJets/"+prepresel.split('&&')[0]+"/"    #.replace('&&','_')+"/"
path = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/plotting_tests/"+prepresel.split('&&')[0]+"/"    #.replace('&&','_')+"/"
if not os.path.exists(path):
  os.makedirs(path)

bkg_samples = [
  {'cname':'QCD'      ,'label':'QCD'           ,'color':ROOT.kCyan-6      ,'chain':getChain(QCD[lepSel],histname='')         },\
  {'cname':'TTVH'     ,'label':'t#bar{t}+W/Z/H','color':ROOT.kOrange-3    ,'chain':getChain(TTVH[lepSel],histname='')        },\
  {'cname':'DY'       ,'label':'DY+Jets'       ,'color':ROOT.kRed-6       ,'chain':getChain(DY[lepSel],histname='')          },\
  {'cname':'singleTop','label':'single top'    ,'color':ROOT.kViolet+5,'chain':getChain(singleTop[lepSel],histname='')   },\
  {'cname':'WJets'    ,'label':'W+Jets'        ,'color':ROOT.kGreen-2 ,'chain':getChain(WJetsHTToLNu[lepSel],histname='')},\
  {'cname':'TTJets'   ,'label':'t#bar{t}+Jets' ,'color':ROOT.kBlue-2 ,'chain':getChain(ttJets[lepSel],histname='')      },\

]

signal_samples = [
{'label':'T5q^{4} 1.0/0.8/0.7','cname':'T5qqqqWW_mGo1000_mCh800_mLSP700','color':ROOT.kBlack  ,'chain':getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname='')},\
{'label':'T5q^{4} 1.2/1/0.8','cname':'T5qqqqWW_mGo1200_mCh1000_mLSP800','color':ROOT.kRed    ,'chain':getChain(T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel],histname='')},\
{'label':'T5q^{4} 1.5/0.8/0.1','cname':'T5qqqqWW_mGo1500_mCh800_mLSP100','color':ROOT.kYellow    ,'chain':getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname='')},\
]


ngNuEFromW = "Sum$(abs(genPartAll_pdgId)==12&&abs(genPartAll_motherId)==24)"
ngNuMuFromW = "Sum$(abs(genPartAll_pdgId)==14&&abs(genPartAll_motherId)==24)"
ngNuTauFromW = "Sum$(abs(genPartAll_pdgId)==16&&abs(genPartAll_motherId)==24)"

diLepEff   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11))==2"
diLepAcc   = ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0&&Sum$(genLep_pt>10&&(abs(genLep_eta)<2.1&&abs(genLep_pdgId)==13||abs(genLep_eta)<2.4&&abs(genLep_pdgId)==11))!=2"
l_H     =  "(("+ngNuEFromW+"+"+ngNuMuFromW+"==1&&"+ngNuTauFromW+"==0))"

diLep = "(("+ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0))"
diLep_inv = "(!("+ngNuEFromW+"+"+ngNuMuFromW+"==2&&"+ngNuTauFromW+"==0))"
rest = "(!("+diLep+"||"+l_H+"))"

sels = [\
{'label': 'TTJets Di-Leptonic'             , 'cut': presel+"&&"+diLep+'&&Jet_pt[1]>='+str(jetPtCut)     , 'color': ROOT.kAzure},\
{'label': 'TTJets Rest'                    , 'cut': diLep_inv+"&&"+presel , 'color': ROOT.kBlue-2},\
#{'label': 'Rest'                    , 'cut': presel+'&&'+rest+'&&'+'Jet_pt[1]>='+str(jetPtCut) , 'color': ROOT.kAzure},\
#{'label': 'Single-Leptonic'         , 'cut': presel+"&&"+l_H+'&&Jet_pt[1]>='+str(jetPtCut)       , 'color': ROOT.kAzure+5},\
]


plots = [
{'ndiv':'False','yaxis':'Events','xaxis':'N_{Jets}','logy':'True' , 'var':'nJet30',                      'varname':'nJet30',                   'binlabel':1,  'bin':11,       'lowlimit':4,  'limit':15},\
{'ndiv':'False','yaxis':'Events','xaxis':'N_{bJetsCSV}','logy':'True' , 'var':'nBJetMediumCSV30',           'varname':'nBJetMediumCSV30',      'binlabel':1,  'bin':8,       'lowlimit':0,  'limit':8},\
{'ndiv':'False','yaxis':'Events','xaxis':'#Delta#Phi(W,l)','logy':'True' , 'var':'deltaPhi_Wl',                 'varname':'deltaPhi_Wl',       'binlabel':1,  'bin':30,       'lowlimit':0,  'limit':pi},\


{'ndiv':'True','yaxis':'Events /','xaxis':'S_{T}','logy':'True' , 'var':'st',                          'varname':'st',                  'binlabel':50,  'bin':36,       'lowlimit':200,  'limit':2000},\
{'ndiv':'True','yaxis':'Events /','xaxis':'H_{T}','logy':'True' , 'var':'htJet30j',                    'varname':'htJet30j',            'binlabel':50,  'bin':50,       'lowlimit':500,  'limit':3000},\
{'ndiv':'True','yaxis':'Events /','xaxis':'p_{T}(leading jet)','logy':'True' , 'var':'Jet_pt[0]',               'varname':'Jet_pt[0]',  'binlabel':30,  'bin':67,       'lowlimit':0,  'limit':2010},\
{'ndiv':'True','yaxis':'Events /','xaxis':'#slash{E}_{T}','logy':'True' , 'var':'met',                         'varname':'met',         'binlabel':50,  'bin':28,       'lowlimit':0,  'limit':1400},\
{'ndiv':'True','yaxis':'Events /','xaxis':'p_{T}(l)','logy':'True' , 'var':'leptonPt',                 'varname':'leptonPt',      'binlabel':25,  'bin':40,       'lowlimit':0,  'limit':1000},\


]


for p in plots:
  can = ROOT.TCanvas(p['varname'],p['varname'],600,600)
  can.cd()
  htmp = ROOT.TH1F('htmp','htmp',p['bin'],p['lowlimit'],p['limit'])
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.035)
  latex.SetTextAlign(11)
  h_Stack = ROOT.THStack('h_Stack',p['varname'])
  h_Stack_S = ROOT.THStack('h_Stack_S','h_Stack_S')
  leg = ROOT.TLegend(0.6,0.6,0.95,0.95)
  leg.SetBorderSize(1) 
  print p['varname']
  for b in bkg_samples:
    print b['cname']  , b['chain']
    chain = b['chain']
    if b['cname'] == 'TTJets' : 
      for sel in sels:
        histo = 'h_'+b['cname']+sel['label']
        histoname = histo
        print histoname
        histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'],p['lowlimit'],p['limit'])
        print sel['cut']
        chain.Draw(p['var']+'>>'+str(histoname),weight_str+'*('+sel['cut']+')')              
        color = sel['color']
        histo.SetFillColor(color)
        histo.SetLineWidth(2)
        histo.SetMinimum(.1)
        h_Stack.Add(histo)
        leg.AddEntry(histo, sel['label'],"f")
        del histo
    else:
      color = b['color']
      print color
      print b['cname']  , b['chain']
      histo = 'h_'+b['cname']
      histoname = histo
      print histoname
      histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'],p['lowlimit'],p['limit'])
      print presel
      chain.Draw(p['var']+'>>'+str(histoname),weight_str+'*('+presel+')')
      print histo
      histo.SetFillColor(color)
      #histo.SetLineColor(color)      
      histo.SetLineWidth(2)
      histo.SetMinimum(.1)
      #print "integral" , histo.Integral()
      h_Stack.Add(histo)
      leg.AddEntry(histo, b['label'],"f")
      del histo  
  for s in signal_samples: 
    color = s['color']
    histo = 'h_'+s['cname']
    chain = s['chain']
    histoname = histo
    print histoname
    histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'],p['lowlimit'],p['limit'])
    chain.Draw(p['var']+'>>'+str(histoname),weight_str+'*('+presel+')')
    print histo
    histo.SetLineColor(color)
    histo.SetLineWidth(4)
    histo.SetMinimum(0.1)
    h_Stack_S.Add(histo)
    print "integral" , histo.Integral()
    leg.AddEntry(histo, s['label'],"l") 

  #h_Stack.SetMaximum((h_Stack.GetMaximum())*50)
  h_Stack.SetMaximum(5000)
  h_Stack.SetMinimum(0.1)
  h_Stack.Draw() 
  h_Stack_S.Draw('noStacksame')
  Xaxis1 = h_Stack.GetXaxis()
  Yaxis1 = h_Stack.GetYaxis()
  Xaxis = h_Stack_S.GetXaxis()
  Yaxis = h_Stack_S.GetYaxis()
  Xaxis1.SetTitle(p['xaxis'])
  Xaxis.SetTitle(p['xaxis'])

  if p['ndiv'] == 'True': 
    Xaxis1.SetNdivisions(505)
    Xaxis.SetNdivisions(505) 
    Yaxis1.SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
    Yaxis.SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
  else : 
    Yaxis1.SetTitle(p['yaxis'])
    Yaxis.SetTitle(p['yaxis'])


  can.SetLogy()
  

  leg.SetFillColor(0)
  latex.DrawLatex(0.16,0.96,"CMS Simulation")
  latex.DrawLatex(0.71,0.96,"L=3 fb^{-1} (13 TeV)")
  can.RedrawAxis()
  leg.Draw()
  can.Draw()
  can.SaveAs(path+p['varname']+'.png')
  can.SaveAs(path+p['varname']+'.pdf')
  can.SaveAs(path+p['varname']+'.root')
  del can

