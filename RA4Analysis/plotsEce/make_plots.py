import ROOT
import pickle
import os,sys
from math import sqrt, cos, sin, atan2, acos, pi
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName, cmgMTClosestJetMET, cmgMTClosestBJetMET,  cmgMinDPhiJet, cmgMinDPhiBJet , cmgMTTopClosestJetMET , cmgHTOrthMET 
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v1_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v9_Phys14V3_HT400ST200_ForTTJetsUnc import *
from localInfo import username

#from binnedNBTagsFit import binnedNBTagsFit
ROOT.gROOT.Reset()
#ROOT.gROOT.LoadMacro("/afs/hephy.at/scratch/e/easilar/newWorkDir/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()


lepSel = 'hard'

lumi = 3 #fb-1
weight_str = '((weight/4)*'+str(lumi)+')'

htCut = [500,10000000000]
#stCut = [250,350]
stCut = [200,10000000000]
njetCut = [6,20]
nbtagCut = 0
mt2Cut = 0
jetPtCut = 80
dfCut =0

prepresel = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'
#prepresel = 'singleElectronic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'
#prepresel = 'singleMuonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'
#presel = prepresel+'mt2w>'+str(mt2Cut)+'&&deltaPhi_Wl>'+str(dfCut)+'&&htJet30j>='+str(htCut[0])+'&&htJet30j<'+str(htCut[1])+'&&st>='+str(stCut[0])+'&&st<'+str(stCut[1])+'&&nJet30>='+str(njetCut[0])+'&&nJet30<'+str(njetCut[1])+'&&nBJetMediumCMVA30=='+str(nbtagCut)
#presel = prepresel+'deltaPhi_Wl>'+str(dfCut)+'&&Jet_pt[1]>='+str(jetPtCut)+'&&htJet30j>='+str(htCut[0])+'&&htJet30j<'+str(htCut[1])+'&&met>='+str(stCut[0])+'&&met<'+str(stCut[1])+'&&nJet30>='+str(njetCut[0])+'&&nJet30<'+str(njetCut[1])+'&&nBJetMediumCMVA30>='+str(nbtagCut)
#presel = prepresel+"(1)"
presel = prepresel+'deltaPhi_Wl>'+str(dfCut)+'&&Jet_pt[1]>='+str(jetPtCut)+'&&htJet30j>='+str(htCut[0])+'&&htJet30j<'+str(htCut[1])+'&&st>='+str(stCut[0])+'&&st<'+str(stCut[1])+'&&nJet30>='+str(njetCut[0])+'&&nJet30<'+str(njetCut[1])+'&&nBJetMediumCSV30=='+str(nbtagCut)
#path = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/tests/"+"_".join(presel.split('&&')[4:])+"/"   #.replace('&&','_')+"/"
#path = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/tests/"+prepresel.split('&&')[0]+"/"   #.replace('&&','_')+"/"
path = "/afs/hephy.at/user/e/easilar/www/PHYS14v3/annote/plots/baseline/"+prepresel.split('&&')[0]+"/"    #.replace('&&','_')+"/"
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
{'label':'T5q^{4} 1.0/0.8/0.7','cname':'T5qqqqWW_mGo1000_mCh800_mLSP700','color':ROOT.kBlack  ,'chain':getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname='')},\
{'label':'T5q^{4} 1.2/1/0.8','cname':'T5qqqqWW_mGo1200_mCh1000_mLSP800','color':ROOT.kRed    ,'chain':getChain(T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel],histname='')},\
{'label':'T5q^{4} 1.5/0.8/0.1','cname':'T5qqqqWW_mGo1500_mCh800_mLSP100','color':ROOT.kYellow    ,'chain':getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname='')},\
#{'cname':'SMS_T1tttt_2J_mGl1500_mLSP100','color':ROOT.kMagenta    ,'chain':getChain(SMS_T1tttt_2J_mGl1500_mLSP100[lepSel],histname='')},\
#{'cname':'SMS_T1tttt_2J_mGl1200_mLSP800','color':ROOT.kCyan       ,'chain':getChain(SMS_T1tttt_2J_mGl1200_mLSP800[lepSel],histname='')},\
]

#for b in bkg_samples:
#  print 'sample:' ,b['cname'],'nevents:', b['chain'].GetEntries()
#for s in signal_samples:
#  print 'sample:' ,s['cname'],'nevents:', s['chain'].GetEntries()




plots = [
#{'xaxis':'M_{T2W}','logy':'True' ,'var':'mt2w',                       'varname':'mt2w',                   'bin':30,       'lowlimit':50, 'limit':500},\
{'yaxis':'Events / 30 GeV','xaxis':'S_{T}','logy':'True' , 'var':'st',                          'varname':'st',                     'bin':30,       'lowlimit':200,  'limit':1400},\
{'yaxis':'Events / 30 GeV','xaxis':'H_{T}','logy':'True' , 'var':'htJet30j',                    'varname':'htJet30j',               'bin':30,       'lowlimit':500,  'limit':2000},\
{'yaxis':'Events','xaxis':'N_{Jets}','logy':'True' , 'var':'nJet30',                      'varname':'nJet30',                 'bin':10,       'lowlimit':6,  'limit':15},\
#{'xaxis':'N_{bJetsCMVA}','logy':'True' , 'var':'nBJetMediumCMVA30',           'varname':'nBJetMediumCMVA30',      'bin':15,       'lowlimit':0,  'limit':15},\
{'yaxis':'Events','xaxis':'N_{bJetsCSV}','logy':'True' , 'var':'nBJetMediumCSV30',           'varname':'nBJetMediumCSV30',      'bin':8,       'lowlimit':0,  'limit':8},\
#{'xaxis':'N_{tau}','logy':'True' , 'var':'nTauGood',                    'varname':'nTau',                   'bin':5,       'lowlimit':0,  'limit':5},\
{'yaxis':'Events','xaxis':'#Delta#Phi(W,l)','logy':'True' , 'var':'deltaPhi_Wl',                 'varname':'deltaPhi_Wl',            'bin':30,       'lowlimit':0,  'limit':pi},\
{'yaxis':'Events / 30 GeV','xaxis':'#slash{E}_{T}','logy':'True' , 'var':'met',                         'varname':'met',                    'bin':30,       'lowlimit':0,  'limit':1400},\
{'yaxis':'Events / 30 GeV','xaxis':'P_{T}(l)','logy':'True' , 'var':'leptonPt[0]',                 'varname':'leptonPt[0]',            'bin':30,       'lowlimit':0,  'limit':1000},\
##{'xaxis':'','logy':'True' , 'var':'Jet_pt[0]+Jet_pt[1]',         'varname':'Jet_pt[0]+Jet_pt[1]',    'bin':30,       'lowlimit':0,  'limit':2000},\
##{'xaxis':'','logy':'True' , 'var':'Jet_eta[0]*Jet_eta[1]',       'varname':'Jet_eta[0]*Jet_eta[1]',  'bin':30,       'lowlimit':-8,  'limit':8},\
#{'xaxis':'nFatJet','logy':'True' , 'var':'nFatJet',                    'varname':'nFatJets',                   'bin':20,       'lowlimit':0,  'limit':20},\
#{'xaxis':'FatJet_pt[0]','logy':'True' , 'var':'FatJet_pt[0]',               'varname':'FatJet_pt[0]',                'bin':100,       'lowlimit':0,  'limit':2000},\
{'yaxis':'Events / 30 GeV','xaxis':'P_{T}(1. jet)','logy':'True' , 'var':'Jet_pt[0]',               'varname':'Jet_pt[0]',                'bin':30,       'lowlimit':0,  'limit':2000},\
#{'xaxis':'prunedMass','logy':'True' , 'var':'FatJet_prunedMass',          'varname':'FatJet_prunedMass',          'bin':100,       'lowlimit':0,  'limit':300},\
#{'xaxis':'trimmedMass','logy':'True' , 'var':'FatJet_trimmedMass',         'varname':'FatJet_trimmedMass',          'bin':100,       'lowlimit':0,  'limit':300},\
#{'xaxis':'filteredMass','logy':'True' , 'var':'FatJet_filteredMass',        'varname':'FatJet_filteredMass',          'bin':100,       'lowlimit':0,  'limit':300},\
#{'xaxis':'FatJet_tau1','logy':'True' , 'var':'FatJet_tau1',                'varname':'FatJet_tau1',          'bin':100,       'lowlimit':0,  'limit':1},\
#{'xaxis':'FatJet_tau2','logy':'True' , 'var':'FatJet_tau2',                'varname':'FatJet_tau2',          'bin':100,       'lowlimit':0,  'limit':1},\
#{'xaxis':'FatJet_tau3','logy':'True' , 'var':'FatJet_tau3',                'varname':'FatJet_tau3',          'bin':100,       'lowlimit':0,  'limit':1},\
#{'xaxis':'#tau3/#tau1','logy':'True' , 'var':'FatJet_tau3/FatJet_tau1',    'varname':'FatJet_tau3_1',          'bin':100,       'lowlimit':0,  'limit':1},\
#{'xaxis':'#tau3/#tau2','logy':'True' , 'var':'FatJet_tau3/FatJet_tau2',    'varname':'FatJet_tau3_2',          'bin':100,       'lowlimit':0,  'limit':1},\
#{'xaxis':'#tau2/#tau1','logy':'True' , 'var':'FatJet_tau2/FatJet_tau1',    'varname':'FatJet_tau2_1',          'bin':100,       'lowlimit':0,  'limit':1},\
#{'xaxis':'nWtagged','logy':'True' , 'var':'Sum$(FatJet_prunedMass>60&&FatJet_prunedMass<100&&(FatJet_tau2/FatJet_tau1)<0.5)',    'varname':'nWtagged',          'bin':5,       'lowlimit':0,  'limit':5},\
#{'xaxis':'nWdaughters','logy':'True' , 'var':'Sum$(abs(genPartAll_motherId)==24)',    'varname':'nWdaughters',          'bin':20,       'lowlimit':0,  'limit':20},\
#{'xaxis':'WdaughtersPdgId','logy':'True' , 'var':'GenPart_pdgId',    'varname':'nWdaughtersPdgId',          'bin':61,       'lowlimit':-30,  'limit':30},\
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
  htmp = ROOT.TH1F('htmp','htmp',p['bin'],p['lowlimit'],p['limit'])
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.035)
  latex.SetTextAlign(11)
  h_Stack = ROOT.THStack('h_Stack',p['varname'])
  h_Stack_S = ROOT.THStack('h_Stack_S','h_Stack_S')
  leg = ROOT.TLegend(0.65,0.65,0.95,0.95)
  leg.SetBorderSize(1) 
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
    chain.Draw(p['var']+'>>'+str(histoname),weight_str+'*('+presel+')')
    print histo
    histo.SetFillColor(color)
    #histo.SetLineColor(color)
    histo.SetLineWidth(2)
    histo.SetMinimum(.1)
    histo.GetXaxis().SetTitle(p['xaxis'])
    histo.GetXaxis().SetNdivisions(505)
    histo.GetYaxis().SetTitle(p['yaxis'])
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
    histo.GetXaxis().SetTitle(p['xaxis'])
    histo.GetXaxis().SetNdivisions(505)
    histo.GetYaxis().SetTitle(p['yaxis'])
    #histo.GetYaxis().SetTitle('Events')
    h_Stack_S.Add(histo)
    #histo.Draw('same')
    print "integral" , histo.Integral()
    leg.AddEntry(histo, s['label'],"l") 

  #h_Stack.SetMaximum((h_Stack.GetMaximum())*50)
  h_Stack.SetMaximum(1000)
  h_Stack.SetMinimum(0.1)
  #h_Stack_S.GetXaxis().SetTitle(p['xaxis'])
  #h_Stack_S.GetYaxis().SetTitle("Number of Events")
  #ROOT.gStyle.SetTitle(p['xaxis'],"x")
  #h_Stack.Draw('noStack')
  h_Stack.Draw() 
  Xaxis1 = h_Stack.GetXaxis()
  Yaxis1 = h_Stack.GetYaxis()
  Xaxis1.SetTitle(p['xaxis'])
  Yaxis1.SetTitle(p['yaxis'])
  #Yaxis1.SetTitle('Events')
  h_Stack_S.Draw('noStacksame')
  Xaxis = h_Stack_S.GetXaxis()
  Yaxis = h_Stack_S.GetYaxis()
  Xaxis.SetTitle(p['xaxis'])
  Xaxis.SetNdivisions(505) 
  Yaxis.SetTitle(p['yaxis'])
  #Yaxis.SetTitle('Events')
  #h_Stack_S.Draw('noStacksame')
  if p['logy']=="True": can.SetLogy()
  #htmp.GetXaxis().SetTitle(p['xaxis'])
  #htmp.GetYaxis().SetTitle('Events/Bin') 
  #htmp.SetTitle('')
  #htmp.Draw('same')
  leg.SetFillColor(0)
  latex.DrawLatex(0.16,0.96,"CMS Simulation")
  latex.DrawLatex(0.71,0.96,"L=3 fb^{-1} (13 TeV)")
  #latex.DrawLatex(0.8,0.05,p['xaxis'])
  #can.Update()
  can.RedrawAxis()
  leg.Draw()
  can.Draw()
  can.SaveAs(path+p['varname']+'.png')
  can.SaveAs(path+p['varname']+'.pdf')
  can.SaveAs(path+p['varname']+'.root')
  del can

