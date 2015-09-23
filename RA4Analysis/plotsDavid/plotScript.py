import ROOT
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
from math import *
import os, copy, sys
from array import array
from random import randint

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.HEPHYPythonTools.user import *
from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_postProcessed import *
from Workspace.RA4Analysis.helpers import *
from draw_helpers import *
from eleID_helper import *

dPhiStr = "acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))"

lumi=42.
sampleLumi=3000.

#Bkg chains 
allBkg=[
        #{'name':'QCD',       'sample':      },
        #{'name':'tt+Jets',   'sample':TTJets_50ns, 'legendName':'t#bar{t}+Jets'},
        #{'name':'DY',        'sample':DY_50ns, 'legendName':'DY', 'weight':'weight'},
        #{'name':'TTV',       'sample':     },
        #{'name':'single top', 'sample':singleTop_25ns   },
        {'name':'W+Jets',     'sample':WJetsToLNu_50ns, 'weight':'weight'},
      ]

for bkg in allBkg:
  bkg['chain'] = getChain(bkg['sample'],histname='')
  bkg['color'] = color(bkg['name'])
#  bkg['chain'].SetAlias('dPhi',dPhiStr)

#Data
#data=[
#     {'name':'DoubleMuon_Run2015B_17Jul2015', 'sample':DoubleMuon_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'Data'},
#     {'name':'DoubleMuon_Run2015B_PromptReco', 'sample':DoubleMuon_Run2015B_PromptReco, 'legendName':'Data', 'merge':'Data'},
#     {'name':'DoubleEG_Run2015B_17Jul2015', 'sample':DoubleEG_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'Data'},
#     {'name':'DoubleEG_Run2015B_PromptReco', 'sample':DoubleEG_Run2015B_PromptReco, 'legendName':'Data', 'merge':'Data'},
#]

#Signal chains
#allSignals=[
            #"SMS_T1tttt_2J_mGl1200_mLSP800",
            #"SMS_T1tttt_2J_mGl1500_mLSP100",
            #"SMS_T2tt_2J_mStop425_mLSP325",
            #"SMS_T2tt_2J_mStop500_mLSP325",
            #"SMS_T2tt_2J_mStop650_mLSP325",
            #"SMS_T2tt_2J_mStop850_mLSP100",
            #{'name':'T5q^{4} 1.2/1.0/0.8', 'sample':T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel], 'weight':'weight', 'color':ROOT.kBlack},
            #{'name':'T5q^{4} 1.5/0.8/0.1',  'sample':T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],  'weight':'weight', 'color':ROOT.kMagenta},
            #{'name':'T5q^{4} 1.0/0.8/0.7', 'sample':T5qqqqWW_mGo1000_mCh800_mChi700[lepSel], 'weight':'weight', 'color':ROOT.kBlue},
            #"T1ttbbWW_mGo1000_mCh725_mChi715",
            #"T1ttbbWW_mGo1000_mCh725_mChi720",
            #"T1ttbbWW_mGo1300_mCh300_mChi290",
            #"T1ttbbWW_mGo1300_mCh300_mChi295",
            #"T5ttttDeg_mGo1000_mStop300_mCh285_mChi280",
            #"T5ttttDeg_mGo1000_mStop300_mChi280",
            #"T5ttttDeg_mGo1300_mStop300_mCh285_mChi280",
            #"T5ttttDeg_mGo1300_mStop300_mChi280",
#]

#for s in allSignals:
#  s['chain'] = getChain(s['sample'],histname='')
#  s['chain'].SetAlias('dPhi',dPhiStr)

#defining ht, st and njets for SR
streg = [(250,350),(350,450),(450,-1)]                         
htreg = [(500,750)]#,(750,1000),(1000,1250),(1250,-1)]
njreg = [(5,5),(6,-1),(6,7),(8,-1)]
btb = (0,0)
#diMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt[0]>=25&&LepGood_pt[1]>=20&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_tightId==1&&LepGood_sip3d<4.0&&((LepGood_charge[0]+LepGood_charge[1])==0))==2)'
#diMuonic = '(Sum$(abs(genLep_pdgId)==13&&genLep_pt[0]>=25&&genLep_pt[1]>=20&&abs(genLep_eta)<2.4&&abs(genLep_motherId)==23&&((genLep_charge[0]+genLep_charge[1])==0))==2)'
#diElectronic = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt[0]>=25&&LepGood_pt[1]>=20&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits<=1&&LepGood_convVeto&&LepGood_sip3d<4.0&&LepGood_tightId>=3&&((LepGood_charge[0]+LepGood_charge[1])==0))==2)"
#diElectronic = "(Sum$(abs(genLep_pdgId)==11&&genLep_pt[0]>=25&&genLep_pt[1]>=20&&abs(genLep_eta)<2.4&&abs(genLep_motherId)==23&&((genLep_charge[0]+genLep_charge[1])==0))==2)"
#singleMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)==1)'
singleMuonic = '(Sum$(abs(genLep_pdgId)==13&&abs(genLep_motherId)==24&&genLep_pt>=25&&abs(genLep_eta)<2.4)==1)'
#singleElectronic = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0)==1)"
singleElectronic = "(Sum$(abs(genLep_pdgId)==11&&abs(genLep_motherId)==24&&genLep_pt>=25&&abs(genLep_eta)<2.4)==1)"
#presel = '('+diMuonic+'||'+diElectronic+')'
presel = '('+singleMuonic+'||'+singleElectronic+')'
#preprefix = 'diLeptonic_nj2_recoZ'
preprefix = 'singleLeptonic_nj2_genW'
wwwDir = saveDir+'RunII/Spring15_50ns/'+preprefix+'/'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

#use small to check some changes faster
small = True
if small:
  streg = [(350,-1)]
  htreg = [(200,-1)]
  njreg = [(2,-1)]
  btb   = (0,0)

allVariables = []

def getleadingJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  Jet0 = jets[0]['pt']
  return Jet0

def getsecondJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  Jet1 = jets[1]['pt']
  return Jet1

def getHt(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  ht=0
  for j in jets:
    ht += j['pt']
  return ht

def getNJets(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  return len(jets)

def getLeadLep(c):
  leadLep = c.GetLeaf('LepGood_pt').GetValue(0)
  return leadLep

def getLt(c):
  leadLepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  met = c.GetLeaf('met_pt').GetValue()
  Lt = met + leadLepPt
  return Lt

def getInvMass(c):
  leadLepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  leadLepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  leadLepEta = c.GetLeaf('LepGood_eta').GetValue(0)
  subLepPt = c.GetLeaf('LepGood_pt').GetValue(1)
  subLepPhi = c.GetLeaf('LepGood_phi').GetValue(1)
  subLepEta = c.GetLeaf('LepGood_eta').GetValue(1)
  invMass = sqrt(2*leadLepPt*subLepPt*(cosh(leadLepEta-subLepEta)-cos(leadLepPhi-subLepPhi)))
  return invMass

def getGenInvMass(c):
  leadLepPt = c.GetLeaf('genLep_pt').GetValue(0)
  leadLepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  leadLepEta = c.GetLeaf('genLep_eta').GetValue(0)
  subLepPt = c.GetLeaf('genLep_pt').GetValue(1)
  subLepPhi = c.GetLeaf('genLep_phi').GetValue(1)
  subLepEta = c.GetLeaf('genLep_eta').GetValue(1)
  invMass = sqrt(2*leadLepPt*subLepPt*(cosh(leadLepEta-subLepEta)-cos(leadLepPhi-subLepPhi)))
  return invMass

def getZdPhi(c):
  a=randint(0,1)
  if a:
    #subleading lepton becomes neutrino
    lepPt = c.GetLeaf('LepGood_pt').GetValue(0)
    lepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
    nuPt = c.GetLeaf('LepGood_pt').GetValue(1)
    nuPhi = c.GetLeaf('LepGood_phi').GetValue(1)
  else:
    #leading lepton becomes neutrino
    lepPt = c.GetLeaf('LepGood_pt').GetValue(1)
    lepPhi = c.GetLeaf('LepGood_phi').GetValue(1)
    nuPt = c.GetLeaf('LepGood_pt').GetValue(0)
    nuPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  #metPt = c.GetLeaf('met_pt').GetValue()
  #metPhi = c.GetLeaf('met_phi').GetValue()
  #metCorrX = metPt*cos(metPhi) + nuPt*cos(nuPhi)
  #metCorrY = metPt*sin(metPhi) + nuPt*sin(nuPhi)
  #metCorrPt = sqrt(metCorrX**2 + metCorrY**2)
  #metCorrPhi = atan2(metCorrY,metCorrX)
  #dPhi = acos((lepPt+metCorrPt*cos(lepPhi-metCorrPhi))/sqrt(lepPt**2+metCorrPt**2+2*lepPt*metCorrPt*cos(lepPhi-metCorrPhi)))
  dPhi = acos((lepPt+nuPt*cos(lepPhi-nuPhi))/sqrt(lepPt**2+nuPt**2+2*lepPt*nuPt*cos(lepPhi-nuPhi)))
  return dPhi

def getZPt(c):
  leadLepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  leadLepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  subLepPt = c.GetLeaf('LepGood_pt').GetValue(1)
  subLepPhi = c.GetLeaf('LepGood_phi').GetValue(1)
  Zpt = sqrt(leadLepPt**2+subLepPt**2+2*leadLepPt*subLepPt*cos(leadLepPhi-subLepPhi))
  return Zpt

def getZPhi(c):
  leadLepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  leadLepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  subLepPt = c.GetLeaf('LepGood_pt').GetValue(1)
  subLepPhi = c.GetLeaf('LepGood_phi').GetValue(1)
  x = leadLepPt*cos(leadLepPhi)+subLepPt*cos(subLepPhi)
  y = leadLepPt*sin(leadLepPhi)+subLepPt*sin(subLepPhi)
  Zphi = atan2(y,x)
  return Zphi

def getZEta(c):
  leadLep = ROOT.TLorentzVector()
  subLep = ROOT.TLorentzVector()
  Z = ROOT.TLorentzVector()
  leadLepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  leadLepEta = c.GetLeaf('LepGood_eta').GetValue(0)
  leadLepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  leadLepMass = c.GetLeaf('LepGood_mass').GetValue(0)
  subLepPt = c.GetLeaf('LepGood_pt').GetValue(1)
  subLepEta = c.GetLeaf('LepGood_eta').GetValue(1)
  subLepPhi = c.GetLeaf('LepGood_phi').GetValue(1)
  subLepMass = c.GetLeaf('LepGood_mass').GetValue(1)
  leadLep.SetPtEtaPhiM(leadLepPt,leadLepEta,leadLepPhi,leadLepMass)
  subLep.SetPtEtaPhiM(subLepPt,subLepEta,subLepPhi,subLepMass)
  Z = leadLep + subLep
  return Z.Eta()

def getGenZdPhi(c):
  a=randint(0,1)
  if a:
    #subleading lepton becomes neutrino
    lepPt = c.GetLeaf('genLep_pt').GetValue(0)
    lepPhi = c.GetLeaf('genLep_phi').GetValue(0)
    nuPt = c.GetLeaf('genLep_pt').GetValue(1)
    nuPhi = c.GetLeaf('genLep_phi').GetValue(1)
  else:
    #leading lepton becomes neutrino
    lepPt = c.GetLeaf('genLep_pt').GetValue(1)
    lepPhi = c.GetLeaf('genLep_phi').GetValue(1)
    nuPt = c.GetLeaf('genLep_pt').GetValue(0)
    nuPhi = c.GetLeaf('genLep_phi').GetValue(0)
  #metPt = c.GetLeaf('met_pt').GetValue()
  #metPhi = c.GetLeaf('met_phi').GetValue()
  #metCorrX = metPt*cos(metPhi) + nuPt*cos(nuPhi)
  #metCorrY = metPt*sin(metPhi) + nuPt*sin(nuPhi)
  #metCorrPt = sqrt(metCorrX**2 + metCorrY**2)
  #metCorrPhi = atan2(metCorrY,metCorrX)
  #dPhi = acos((lepPt+metCorrPt*cos(lepPhi-metCorrPhi))/sqrt(lepPt**2+metCorrPt**2+2*lepPt*metCorrPt*cos(lepPhi-metCorrPhi)))
  dPhi = acos((lepPt+nuPt*cos(lepPhi-nuPhi))/sqrt(lepPt**2+nuPt**2+2*lepPt*nuPt*cos(lepPhi-nuPhi)))
  return dPhi

def getGenZPt(c):
  leadLepPt = c.GetLeaf('genLep_pt').GetValue(0)
  leadLepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  subLepPt = c.GetLeaf('genLep_pt').GetValue(1)
  subLepPhi = c.GetLeaf('genLep_phi').GetValue(1)
  Zpt = sqrt(leadLepPt**2+subLepPt**2+2*leadLepPt*subLepPt*cos(leadLepPhi-subLepPhi))
  return Zpt 

def getGenZPhi(c):
  leadLepPt = c.GetLeaf('genLep_pt').GetValue(0)
  leadLepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  subLepPt = c.GetLeaf('genLep_pt').GetValue(1)
  subLepPhi = c.GetLeaf('genLep_phi').GetValue(1)
  x = leadLepPt*cos(leadLepPhi)+subLepPt*cos(subLepPhi)
  y = leadLepPt*sin(leadLepPhi)+subLepPt*sin(subLepPhi)
  Zphi = atan2(y,x)
  return Zphi

def getGenZEta(c):
  leadLep = ROOT.TLorentzVector()
  subLep = ROOT.TLorentzVector()
  Z = ROOT.TLorentzVector()
  leadLepPt = c.GetLeaf('genLep_pt').GetValue(0)
  leadLepEta = c.GetLeaf('genLep_eta').GetValue(0)
  leadLepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  leadLepMass = c.GetLeaf('genLep_mass').GetValue(0)
  subLepPt = c.GetLeaf('genLep_pt').GetValue(1)
  subLepEta = c.GetLeaf('genLep_eta').GetValue(1)
  subLepPhi = c.GetLeaf('genLep_phi').GetValue(1)
  subLepMass = c.GetLeaf('genLep_mass').GetValue(1)
  leadLep.SetPtEtaPhiM(leadLepPt,leadLepEta,leadLepPhi,leadLepMass)
  subLep.SetPtEtaPhiM(subLepPt,subLepEta,subLepPhi,subLepMass)
  Z = leadLep + subLep
  return Z.Eta()

def getWdPhi(c):
  lepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  lepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  metPt = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  dPhi = acos((lepPt+metPt*cos(lepPhi-metPhi))/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))
  return dPhi

def getWPt(c):
  LepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  LepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  metPt = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  Wpt = sqrt(LepPt**2+metPt**2+2*LepPt*metPt*cos(LepPhi-metPhi))
  return Wpt

def getWPhi(c):
  LepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  LepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  metPt = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  x = LepPt*cos(LepPhi)+metPt*cos(metPhi)
  y = LepPt*sin(LepPhi)+metPt*sin(metPhi)
  Wphi = atan2(y,x)
  return Wphi

def getGenWdPhi(c):
  lepPt = c.GetLeaf('genLep_pt').GetValue(0)
  lepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  metPt = c.GetLeaf('met_genPt').GetValue()
  metPhi = c.GetLeaf('met_genPhi').GetValue()
  dPhi = acos((lepPt+metPt*cos(lepPhi-metPhi))/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))
  return dPhi

def getGenWPt(c):
  LepPt = c.GetLeaf('genLep_pt').GetValue(0)
  LepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  metPt = c.GetLeaf('met_genPt').GetValue()
  metPhi = c.GetLeaf('met_genPhi').GetValue()
  Wpt = sqrt(LepPt**2+metPt**2+2*LepPt*metPt*cos(LepPhi-metPhi))
  return Wpt

def getGenWPhi(c):
  LepPt = c.GetLeaf('genLep_pt').GetValue(0)
  LepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  metPt = c.GetLeaf('met_genPt').GetValue()
  metPhi = c.GetLeaf('met_genPhi').GetValue()
  x = LepPt*cos(LepPhi)+metPt*cos(metPhi)
  y = LepPt*sin(LepPhi)+metPt*sin(metPhi)
  Wphi = atan2(y,x)
  return Wphi

def getGenWEta(c):
  genPartAll = [getObjDict(c, 'genPartAll_', ['pt','eta','phi','mass','pdgId','motherId'], j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  neutrino = filter(lambda n:abs(n['pdgId']) in [12,14], genPartAll)
  nuFromW = filter(lambda w:abs(w['motherId'])==24, neutrino)
  if len(nuFromW)>0:
    if len(nuFromW)>1: print 'this should not have happened' 
    if abs(nuFromW[0]['pdgId'])-abs(c.GetLeaf('genLep_pdgId').GetValue())>1.: print 'this should not have happened'
    leadLep = ROOT.TLorentzVector()
    nu = ROOT.TLorentzVector()
    W = ROOT.TLorentzVector()
    leadLepPt = c.GetLeaf('genLep_pt').GetValue(0)
    leadLepEta = c.GetLeaf('genLep_eta').GetValue(0)
    leadLepPhi = c.GetLeaf('genLep_phi').GetValue(0)
    leadLepMass = c.GetLeaf('genLep_mass').GetValue(0)
    nuPt = nuFromW[0]['pt'] 
    nuEta = nuFromW[0]['eta']
    nuPhi = nuFromW[0]['phi']
    nuMass = nuFromW[0]['mass']
    #print nuPt, c.GetLeaf('met_genPt').GetValue()
    leadLep.SetPtEtaPhiM(leadLepPt,leadLepEta,leadLepPhi,leadLepMass)
    nu.SetPtEtaPhiM(nuPt,nuEta,nuPhi,nuMass)
    W = leadLep + nu
    return W.Eta()

def getZpol(c):
  Zpt = getZPt(c)
  lpt = c.GetLeaf('LepGood_pt').GetValue(0)
  return lpt/Zpt

def getGenZpol(c):
  genZpt = getGenZPt(c)
  lpt = c.GetLeaf('genLep_pt').GetValue(0)
  return lpt/genZpt

def getWpol(c):
  Wpt = getWPt(c)
  lpt = c.GetLeaf('LepGood_pt').GetValue(0)
  return lpt/Wpt

def getGenWpol(c):
  genWpt = getGenWPt(c)
  lpt = c.GetLeaf('genLep_pt').GetValue(0)
  return lpt/genWpt

met = {'name':'mymet', 'varString':"met_genPt", 'legendName':'#slash{E}_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
ht = {'name':'myht', 'varFunc':getHt, 'legendName':'H_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
St = {'name':'myst', 'varFunc':getLt, 'legendName':'L_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
nJets = {'name':'mynJets', 'varFunc':getNJets, 'legendName':'Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
invMass = {'name':'myInvMass', 'varFunc':getInvMass, 'legendName':'m(ll)', 'Ytitle':'# of Events', 'binning':[30,76,106]}
dPhi = {'name':'mydeltaPhi', 'varFunc':getWdPhi, 'legendName':'#Delta#Phi(Z,l)','binning':[20,0,pi], 'Ytitle':'# of Events'}#, 'binningIsExplicit':True} 
Zpt = {'name':'myWpt', 'varFunc':getWPt, 'legendName':'p_{T}(W)','binning':[32,0,800], 'Ytitle':'# of Events'}
Zphi = {'name':'myWphi', 'varFunc':getWPhi, 'legendName':'#phi(W)','binning':[40,-pi,-pi], 'Ytitle':'# of Events'} 
Zeta = {'name':'myWeta', 'varFunc':getGenWEta, 'legendName':'#eta(W)','binning':[40,-5,5], 'Ytitle':'# of Events'} 
Zpol = {'name':'myWpol', 'varFunc':getWpol, 'legendName':'p_{T}(l)/p_{T}(W)','binning':[80,0,20], 'Ytitle':'# of Events'} 
lMomentum = {'name':'myleptonPt', 'varString':'leptonPt', 'legendName':'p_{T}(l)', 'Ytitle':'# of Events / 25GeV', 'binning':[40,0,1000]}
leadingJet = {'name':'myleadingJet', 'varFunc':getleadingJet, 'legendName':'p_{T}(leading Jet)', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
secondJet = {'name':'mysecondJet', 'varFunc':getsecondJet, 'legendName':'p_{T}(J_{2})', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}

allVariables.append(met)
allVariables.append(ht)
allVariables.append(St)
allVariables.append(nJets)
#allVariables.append(invMass)
allVariables.append(dPhi)
#allVariables.append(lMomentum)
allVariables.append(Zpt)
allVariables.append(Zphi)
allVariables.append(Zpol)
allVariables.append(Zeta)
#allVariables.append(leadingJet)
#allVariables.append(secondJet)

histos = {}
h_ratio = {}

for i_htb, htb in enumerate(htreg):
  for stb in streg:
    for srNJet in njreg:
      print 'Var region => ht: ',htb,'st: ',stb #'NJet: ',srNJet
      #for sig in allSignals:            
      #  h_ratio[sig['name']] = {}     
      for sample in allBkg:# + allSignals: #Loop over samples
        histos[sample['name']] = {}

        for var in allVariables:
          if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
            histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], len(var['binning'])-1, array('d', var['binning']))
          else:
            histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], *var['binning'])
          histos[sample['name']][var['name']].Reset()
          #sample['chain'].Draw("Sum$(isoTrack_pt<15&&abs(isoTrack_pdgId)==211&&abs(isoTrack_dz)<0.05)"+">>"+sample["name"]+"_"+var["name"])
          #sample['chain'].Draw(var['varString']+">>"+sample['name']+'_'+var['name'], sample["weight"]+"*("+cut+")")
          
        namestr = nameAndCut(None, None, srNJet, btb=btb, presel=presel, btagVar = 'nBJetMediumCMVA30')[0]
        cut = presel+'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.890)#+'&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)#+'&&'+nJetCut(2, minPt=30, maxEta=2.4)
        
        sample["chain"].Draw(">>eList",cut) #Get the event list 'eList' which has all the events satisfying the cut
        elist = ROOT.gDirectory.Get("eList")
        number_events = elist.GetN()
        print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
        
        #Event loop
        for i in range(number_events): #Loop over those events
          if i%10000==0:
            print "At %i of %i for sample %s"%(i,number_events,sample['name'])

          sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
          weight = 1
          if sample.has_key('weight'):
            if type(sample['weight'])==type(''):
              sampleWeight = getVarValue(sample['chain'], sample['weight'])
              weight = (sampleWeight/sampleLumi)*lumi
            else:
              weight = sample['weight']

          for var in allVariables:
            assert (var.has_key('varString') or var.has_key('varFunc')), "Error: Did not specify 'varString' or 'varFunc' for var %s" % repr(var)
            assert not (var.has_key('varString') and var.has_key('varFunc')), "Error: Specified both 'varString' and 'varFunc' for var %s" % repr(var)
            varValue = getVarValue(sample["chain"], var['varString']) if var.has_key('varString') else var['varFunc'](sample["chain"])
            histos[sample['name']][var['name']].Fill(varValue, weight)
        del elist
        
        #for sample in signals:
        #  for var in allVariables:
        #    if histos[sample['name']][var['name']].Integral()>0:
        #      histos[sample['name']][var['name']].Scale(histos['TTJets'][var['name']].Integral()/histos[sample['name']][var['name']].Integral())
        
        #Define and stack the histograms...
      for var in allVariables:
        canvas = ROOT.TCanvas(var['name']+' Window',var['name']+' Window')
        pad1 = ROOT.TPad(var['name']+' Pad',var['name']+' Pad',0.,0.,1.,1.)
        #pad1.SetBottomMargin(0)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        l = ROOT.TLegend(0.65,0.85,0.98,0.95)
        l.SetFillColor(0)
        l.SetBorderSize(1)
        l.SetShadowColor(ROOT.kWhite)
        stack = ROOT.THStack('stack','Stacked Histograms')
       
#        lines = [{'pos':(0.15, 0.95),'text':'CMS Simulation',        'options':{'size':0.045}},\
#                 {'pos':(0.7, 0.95), 'text':'L=4fb{}^{-1} (13 TeV)', 'options':{'size':0.045}}]
        text = ROOT.TLatex()
        text.SetNDC()
        text.SetTextSize(0.045)
        text.SetTextAlign(11) 

        for sample in allBkg:
          histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
          histos[sample['name']][var['name']].SetFillColor(sample['color'])
          histos[sample['name']][var['name']].SetMarkerStyle(0)
          histos[sample['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
          histos[sample['name']][var['name']].GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
          histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.04)
          histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
          stack.Add(histos[sample['name']][var['name']])
          l.AddEntry(histos[sample['name']][var['name']], sample['name'],'f')
       
        stack.Draw('hist')
        stack.GetXaxis().SetTitle(var['legendName'])
        stack.GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
        stack.SetMinimum(10**(-1))
        stack.SetMaximum(100*stack.GetMaximum())
 
        #for extra in extraSamples:
        #  histos[extra['name']][var['name']].SetMarkerStyle(21)
        #  histos[extra['name']][var['name']].Draw('same E')
        #  l.AddEntry(histos[extra['name']][var['name']],extra['name'])
       
        #for sig in allSignals:
        #  histos[sig['name']][var['name']].SetLineColor(sig['color'])
        #  histos[sig['name']][var['name']].SetLineWidth(2)
        #  histos[sig['name']][var['name']].SetFillColor(0)
        #  histos[sig['name']][var['name']].SetMarkerStyle(0)
        #  histos[sig['name']][var['name']].Draw('same')
        #  l.AddEntry(histos[sig['name']][var['name']], sig['name'])
       
        l.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.6,0.96,"#bf{L="+str(lumi)+" pb^{-1} (13 TeV)}")
        
#        canvas.cd()
#        pad2 = ROOT.TPad(var['name']+" Ratio",var['name']+" Ratio",0.,0.,1.,0.3)
#        pad2.SetTopMargin(0)
#        pad2.SetBottomMargin(0.3)
#        pad2.Draw()
#        pad2.cd()
#        
#        if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
#          histo_merge = ROOT.TH1F(var['name']+" Ratio",var['name']+" Ratio", len(var['binning'])-1, array('d', var['binning']))
#        else:
#          histo_merge = ROOT.TH1F(var['name']+" Ratio",var['name']+" Ratio", *var['binning'])
#        histo_merge.Merge(stack.GetHists())
#
#        for sig in allSignals:
#          h_ratio[sig['name']][var['name']] = histos[sig['name']][var['name']].Clone()
#          h_ratio[sig['name']][var['name']].SetLineColor(sig['color'])
#          h_ratio[sig['name']][var['name']].SetLineWidth(2)
#        # h_ratio[sig['name']][var['name']].SetMinimum(0.0)
#       #  h_ratio[sig['name']][var['name']].SetMaximum(0.02)
#          h_ratio[sig['name']][var['name']].Sumw2()
#          h_ratio[sig['name']][var['name']].SetStats(0)
#          h_ratio[sig['name']][var['name']].Divide(histo_merge)
#          h_ratio[sig['name']][var['name']].SetMarkerStyle(21)
#          h_ratio[sig['name']][var['name']].Draw("ep")
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitle(var['legendName'])
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitle("Signal/Bkg")
#          h_ratio[sig['name']][var['name']].GetYaxis().SetNdivisions(505)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitleSize(23)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitleFont(43)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetTitleOffset(1.8)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetLabelFont(43)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetLabelSize(20)
#          h_ratio[sig['name']][var['name']].GetYaxis().SetLabelOffset(0.015)
#        #  h_ratio[sig['name']][var['name']].GetXaxis().SetNdivisions(510)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitleSize(23)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitleFont(43)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetTitleOffset(3.4)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetLabelFont(43)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetLabelSize(20)
#          h_ratio[sig['name']][var['name']].GetXaxis().SetLabelOffset(0.04)
          
          #h_ratio2 = histos['T5Full_1500_800_100'][var['name']].Clone('h_ratio2')
          #h_ratio2.SetLineColor(signal1500['color'])
          #h_ratio2.SetLineWidth(2)
          #h_ratio2.Sumw2()
          #h_ratio2.SetStats(0)
          #h_ratio2.Divide(histo_merge)
          #h_ratio2.SetMarkerStyle(21)
          #h_ratio2.SetMarkerColor(ROOT.kBlue+2)
          #h_ratio2.Draw("same")
         
        canvas.cd()
        canvas.Print(wwwDir+namestr+'_'+var['name']+'.png')
        canvas.Print(wwwDir+namestr+'_'+var['name']+'.root')
        canvas.Print(wwwDir+namestr+'_'+var['name']+'.pdf')
        canvas.Clear()

