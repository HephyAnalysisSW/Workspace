import ROOT
import pickle
import os,sys
from math import sqrt, cos, sin, atan2, acos, pi
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName, cmgMTClosestJetMET, cmgMTClosestBJetMET,  cmgMinDPhiJet, cmgMinDPhiBJet , cmgMTTopClosestJetMET , cmgHTOrthMET 
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150 import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400_withDF import *
from localInfo import username
from binnedNBTagsFit import binnedNBTagsFit
ROOT.gROOT.Reset()
#ROOT.gROOT.LoadMacro("/afs/hephy.at/scratch/e/easilar/newWorkDir/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
#ROOT.setTDRStyle()
ROOT.gROOT.Reset()


lepSel = 'hard'

htCut = [500,10000000]
#stCut = [250,350]
metCut = [450,10000000]
njetCut = [8,16]
nbtagCut = 0
mt2Cut = 0
jetPtCut = 80
dfCut =0
prepresel = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'
#presel = prepresel+'mt2w>'+str(mt2Cut)+'&&deltaPhi_Wl>'+str(dfCut)+'&&htJet30j>='+str(htCut[0])+'&&htJet30j<'+str(htCut[1])+'&&st>='+str(stCut[0])+'&&st<'+str(stCut[1])+'&&nJet30>='+str(njetCut[0])+'&&nJet30<'+str(njetCut[1])+'&&nBJetMediumCMVA30=='+str(nbtagCut)
#presel = prepresel+'deltaPhi_Wl>'+str(dfCut)+'&&Jet_pt[1]>='+str(jetPtCut)+'&&htJet30j>='+str(htCut[0])+'&&htJet30j<'+str(htCut[1])+'&&met>='+str(metCut[0])+'&&met<'+str(metCut[1])+'&&nJet30>='+str(njetCut[0])+'&&nJet30<'+str(njetCut[1])+'&&nBJetMediumCMVA30>='+str(nbtagCut)
presel = prepresel+'deltaPhi_Wl>'+str(dfCut)+'&&Jet_pt[1]>='+str(jetPtCut)+'&&htJet30j>='+str(htCut[0])+'&&htJet30j<'+str(htCut[1])+'&&st>='+str(metCut[0])+'&&st<'+str(metCut[1])+'&&nJet30>='+str(njetCut[0])+'&&nJet30<'+str(njetCut[1])+'&&nBJetMediumCMVA30=='+str(nbtagCut)
path = "/afs/hephy.at/user/e/easilar/www/signal_Bkg_taureject/"+"_".join(presel.split('&&')[4:])+"/"   #.replace('&&','_')+"/"
if not os.path.exists(path):
  os.makedirs(path)

bkg_samples = [
{'cname':'QCD'      ,'label':'QCD'           ,'color':ROOT.kCyan-6  ,'chain':getChain(QCD[lepSel],histname='')         },\
{'cname':'TTVH'     ,'label':'t#bar{t}+W/Z/H','color':ROOT.kOrange-3  ,'chain':getChain(TTVH[lepSel],histname='')        },\
{'cname':'DY'       ,'label':'DY+Jets'       ,'color':ROOT.kRed-6 ,'chain':getChain(DY[lepSel],histname='')          },\
{'cname':'singleTop','label':'single top'    ,'color':ROOT.kViolet+5,'chain':getChain(singleTop[lepSel],histname='')   },\
{'cname':'WJets'    ,'label':'W+Jets'        ,'color':ROOT.kGreen-2 ,'chain':getChain(WJetsHTToLNu[lepSel],histname='')},\
{'cname':'TTJets'   ,'label':'t#bar{t}+Jets' ,'color':ROOT.kBlue-2 ,'chain':getChain(ttJets[lepSel],histname='')      },\
]

signal_samples = [
{'cname':'SMS_T5qqqqWW_Gl1200_Chi1000_LSP800','color':ROOT.kBlack  ,'chain':getChain(SMS_T5qqqqWW_Gl1200_Chi1000_LSP800[lepSel],histname='')},\
{'cname':'SMS_T5qqqqWW_Gl1500_Chi800_LSP100','color':ROOT.kRed    ,'chain':getChain(SMS_T5qqqqWW_Gl1500_Chi800_LSP100[lepSel],histname='')},\
]

plots = [
  {'var':'mt2w',                        'varname':'mt2w',                   'bin':30,       'lowlimit':50, 'limit':500},\
  {'var':'st',                          'varname':'st',                     'bin':30,       'lowlimit':0,  'limit':1400},\
  {'var':'htJet30j',                    'varname':'htJet30j',               'bin':30,       'lowlimit':0,  'limit':2000},\
  {'var':'nJet30',                      'varname':'nJet30',                 'bin':15,       'lowlimit':0,  'limit':15},\
  {'var':'nBJetMediumCMVA30',           'varname':'nBJetMediumCMVA30',      'bin':15,       'lowlimit':0,  'limit':15},\
  {'var':'nTauGood',                    'varname':'nTau',                   'bin':5,       'lowlimit':0,  'limit':5},\
  {'var':'deltaPhi_Wl',                 'varname':'deltaPhi_Wl',            'bin':30,       'lowlimit':0,  'limit':pi},\
  {'var':'met',                         'varname':'met',                    'bin':30,       'lowlimit':0,  'limit':1400},\
  {'var':'leptonPt[0]',                 'varname':'leptonPt[0]',            'bin':100,       'lowlimit':0,  'limit':1000},\
  {'var':'Jet_pt[0]+Jet_pt[1]',         'varname':'Jet_pt[0]+Jet_pt[1]',    'bin':30,       'lowlimit':0,  'limit':2000},\
  {'var':'Jet_eta[0]*Jet_eta[1]',       'varname':'Jet_eta[0]*Jet_eta[1]',  'bin':30,       'lowlimit':-8,  'limit':8},\
]
#p = plots[0]
#print p 
#can.Draw()

#color = 0
#s=signal_samples[0]
#bkg_samples[0]['chain'].GetListOfBranches().ls()
#b= bkg_samples[0]
for p in plots:
  can = ROOT.TCanvas(p['varname'],p['varname'],600,600)
  can.cd()
  h_Stack = ROOT.THStack('h_Stack',p['varname'])
  h_Stack_S = ROOT.THStack('h_Stack_S','h_Stack_S')
  leg = ROOT.TLegend(0.6,0.8,1,1)
  print p['varname']
  for b in bkg_samples:
    color = b['color']
    print color
    print b['cname']  , b['chain']
    histo = 'h_'+b['cname']
    chain = b['chain']
    histoname = histo
    print histoname
    histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'],p['lowlimit'],p['limit'])
    print presel
    chain.Draw(p['var']+'>>'+str(histoname),'weight*('+presel+')')
    print histo
    histo.SetFillColor(color)
    histo.SetMinimum(.000001)
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
    chain.Draw(p['var']+'>>'+str(histoname),'weight*('+presel+')')
    print histo
    histo.SetLineColor(color)
    histo.SetLineWidth(3)
    histo.SetMinimum(.000001)
    h_Stack_S.Add(histo)
    #histo.Draw('same')
    leg.AddEntry(histo, s['cname'],"l")  
  h_Stack.Draw()  
  h_Stack_S.Draw('noStacksame')
  leg.SetFillColor(0)
  leg.Draw()
  can.SetLogy()
  #can.Update()
  can.SaveAs(path+p['varname']+'.png')
  can.SaveAs(path+p['varname']+'.pdf')
  can.SaveAs(path+p['varname']+'.root')
  del can

