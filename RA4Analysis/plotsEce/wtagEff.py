import ROOT
from Workspace.RA4Analysis.makeCompPlotDilep import DrawClosure
#from Workspace.RA4Analysis.makeNicePlot import DrawNicePlot
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.cmgObjectSelection import get_cmg_genPartsAll,get_cmg_genParts, get_cmg_fatJets, get_cmg_jets, get_cmg_index_and_DR, get_cmg_genLeps, get_cmg_recoMuons
from Workspace.RA4Analysis.objectSelection import getGoodJetsStage2,gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR,getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getGenLepsWithMatchInfo,getGenLeps, getMuons, getLooseMuStage2, getGenLep
#from Workspace.RA4Analysis.stage2Tuples import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v2_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.helpers import deltaPhi

from math import *
import os, sys
import pickle
from array import array
from localInfo import username
ROOT.gROOT.LoadMacro("/afs/hephy.at/scratch/e/easilar/CMSSW_7_2_3/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.TH1F.SetDefaultSumw2()
lepSel = 'hard'
#sample = getChain(WJetsHTToLNu[lepSel],histname='')
#sample = getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname='')
#sample = getChain(ttJets[lepSel],histname='')
#sample_name = "T5qqqqWW_mGo1500_mCh800_mLSP100"
#sample_name = "TTJets"
#sample_name = "WJets"
#c = sample
small = False
maxN = 10000

samples = [
{'flag':'bkg','cname':'QCD'      ,                        'label':'QCD'           ,                      'color':ROOT.kCyan-6  ,'chain':getChain(QCD[lepSel],histname='')         },\
{'flag':'bkg','cname':'TTVH'     ,                        'label':'t#bar{t}+W/Z/H',                      'color':ROOT.kOrange-3  ,'chain':getChain(TTVH[lepSel],histname='')        },\
{'flag':'bkg','cname':'DY'       ,                        'label':'DY+Jets'       ,                      'color':ROOT.kRed-6 ,'chain':getChain(DY[lepSel],histname='')          },\
{'flag':'bkg','cname':'singleTop',                        'label':'single top'    ,                      'color':ROOT.kViolet+5,'chain':getChain(singleTop[lepSel],histname='')   },\
{'flag':'bkg','cname':'WJets'    ,                        'label':'W+Jets'        ,                      'color':ROOT.kGreen-2 ,'chain':getChain(WJetsHTToLNu[lepSel],histname='')},\
{'flag':'bkg','cname':'TTJets'   ,                        'label':'t#bar{t}+Jets' ,                      'color':ROOT.kBlue-2 ,'chain':getChain(ttJets[lepSel],histname='')      },\
{'flag':'sig','cname':'T5qqqqWW_mGo1000_mCh800_mLSP700',  'label':'T5qqqqWW_mGo1000_mCh800_mLSP700'  ,   'color':ROOT.kBlack  ,'chain':getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname='')},\
{'flag':'sig','cname':'T5qqqqWW_mGo1200_mCh1000_mLSP800', 'label':'T5qqqqWW_mGo1200_mCh1000_mLSP800' ,   'color':ROOT.kRed    ,'chain':getChain(T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel],histname='')},\
{'flag':'sig','cname':'T5qqqqWW_mGo1500_mCh800_mLSP100',  'label':'T5qqqqWW_mGo1500_mCh800_mLSP100'  ,   'color':ROOT.kYellow    ,'chain':getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname='')},\
]

def findDaughters(genParts,index):
  w = genParts[index]
  #print "PdgID:" , w['pdgId']  
  dau = []
  for g in genParts:
    if g['motherId'] == w['pdgId'] and g['pdgId']!=w['pdgId']:
      if abs(g['pdgId'])>=1 and abs(g['pdgId'])<=6  :
        dau.append(g)
  return dau

import itertools
from itertools import *

def findRealDaus(daus , w):
  p = []
  trash = []
  for p1,p2 in list(combinations(daus, 2)):
    px = (p1['pt']*cos(p1['phi'])+p2['pt']*cos(p2['phi']))
    py = (p1['pt']*sin(p1['phi'])+p2['pt']*sin(p2['phi']))
    pt = sqrt(px**2+py**2)
    if abs(pt-w['pt'])/w['pt'] < 0.00001:
    #if pt == w['pt']:  
      p.append(p1)
      p.append(p2)
    else :
      trash.append(p1)
      trash.append(p2)
  return p


## this function is not complete
#def findFinalDaughters(daus,genParts,index):
#  w = genParts[index]
#  print "Starting W", w 
#  fdaus = []
#  while True:
#    for i in range(int(len(daus))): 
#      radiated=False
#      if daus[i]['pdgId'] == w['pdgId']:
#        radiated = True
#        break
#      if not radiated: break
#      print "appending final daughter:" , daus[i]
#      fdaus.append(daus[i]) 
#  return fdaus

#ngNuEFromW = "Sum$(abs(GenPart_pdgId)==12&&abs(GenPart_motherId)==24)"
#ngNuMuFromW = "Sum$(abs(GenPart_pdgId)==14&&abs(GenPart_motherId)==24)"
#ngNuTauFromW = "Sum$(abs(GenPart_pdgId)==16&&abs(GenPart_motherId)==24)"

#diHad   = "("+ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==0"+")"
#hTau_H  = "("+ngNuEFromW+"+"+ngNuMuFromW+"==0&&"+ngNuTauFromW+"==1&&Sum$(genTau_nNuE+genTau_nNuMu==0&&genTau_nNuTau==1)==1"+")"
#allHad = "("+diHad+"||"+hTau_H+")"
#presel = "Sum$(abs(GenPart_pdgId)==14&&abs(GenPart_motherId)==24)==2&&Sum$(abs(GenPart_pdgId)==12&&abs(GenPart_motherId)==24)==0" #&&Sum$(abs(GenPart_pdgId)==16)==0"
#presel = allHad
#presel = diHad
htCut = [500,10000000000]
#stCut = [250,350]
stCut = [200,10000000000]
njetCut = [6,20]
nbtagCut = 0
mt2Cut = 0
jetPtCut = 80
dfCut =1


prepresel = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&'

#presel = prepresel+'deltaPhi_Wl>'+str(dfCut)+'&&Jet_pt[1]>='+str(jetPtCut)+'&&htJet30j>='+str(htCut[0])+'&&htJet30j<'+str(htCut[1])+'&&st>='+str(stCut[0])+'&&st<'+str(stCut[1])+'&&nJet30>='+str(njetCut[0])+'&&nJet30<'+str(njetCut[1])+'&&nBJetMediumCMVA30=='+str(nbtagCut)
presel = ""

path = '/afs/hephy.at/user/e/easilar/www/PHYS14v3/fatJet/Wtagging/Eff/'
if not os.path.exists(path):
  os.makedirs(path)

ptBins  = array('d', [float(x) for x in range(10, 50,10)+range(50,150,25)+range(150,200,50)+range(200,500,100)+range(500,2000,250)])
#ptBins  = array('d', [float(x) for x in range(0,200,200)+range(200,2000,200)+range(2000,3000,500)])
etaBins = array('d', [float(x)/10. for x in [-30,-25]+range(-21,22,6)+[25,30]])

w_Eff = ROOT.TH1F('w_Eff', 'w_Eff',len(ptBins)-1,ptBins)
num = ROOT.TH1F('num', 'W tag Efficiency',len(ptBins)-1,ptBins)
den = ROOT.TH1F('den', 'den',len(ptBins)-1,ptBins)

b = samples[8]  #High mass gap
c = b['chain']

c.Draw(">>eList",presel)
eList = ROOT.gDirectory.Get("eList")
number_events = eList.GetN()
#number_events = c.GetEntries()
if small:
  if number_events>maxN:
    number_events=maxN

number_events=min(number_events, eList.GetN())
for i in range(number_events):
  if (i%10000 == 0) and i>0 :
    print i,"/",number_events
  c.GetEntry(eList.GetEntry(i))
  #c.GetEntry(i)
  
  fatJets = get_cmg_fatJets(c)
  if b['flag'] == 'bkg' : genParts = get_cmg_genParts(c)
  if b['flag'] == 'sig' : genParts = get_cmg_genPartsAll(c)
  for g in range(len(genParts)):
    genPart = genParts[g]
    if abs(genPart['pdgId'])==24 :
      #print "I want the daughters of this w:" , genPart 
      idaus = findDaughters(genParts,g)
      if idaus:
        daus = findRealDaus(idaus,genPart)
        if daus:
          print "daus:" , daus
          assert len(daus) == 2
          den.Fill(genPart['pt'])
          gInd , gDR = get_cmg_index_and_DR(fatJets,genPart['phi'],genPart['eta'])
          #print "filling den"
          if gInd>=0 and  gDR<0.4 :
            fatJet = fatJets[gInd] 
            if fatJet['prunedMass']>60 and fatJet['prunedMass']<100 and (fatJet['tau2']/fatJet['tau1'])<0.5 : 
              #print "filling num"
              num.Fill(genPart['pt'])
              continue

can = ROOT.TCanvas("c","Eff",800,800)
can.cd()
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.035)
latex.SetTextAlign(11)
w_Eff = num.Clone()
w_Eff.Divide(den)
w_Eff.SetAxisRange(0, 1.0,"Y")
w_Eff.SetLineColor(ROOT.kBlack)
w_Eff.GetYaxis().SetTitle("W tag Eff")
w_Eff.GetXaxis().SetTitle("gen W P_{T}")
#w_Eff.GetXaxis().SetTitle("H_{T}")
w_Eff.Draw('C')

latex.DrawLatex(0.16,0.96,"CMS Simulation")
latex.DrawLatex(0.71,0.96,"L=4 fb^{-1} (13 TeV)")
latex.DrawLatex(0.3,0.8,b['cname'])

can.SaveAs(path+"/wtag_with04_Eff_wqq"+"_"+b['cname']+"newDaus.png")
can.SaveAs(path+"/wtag_with04_Eff_wqq"+"_"+b['cname']+"newDaus.root")
can.SaveAs(path+"/wtag_with04_Eff_wqq"+"_"+b['cname']+"newDaus.pdf")

print "Written",  path
