import ROOT
import pickle
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.TH1F().SetDefaultSumw2()
from math import *
import os, copy, sys
from array import array
from random import randint

from Workspace.HEPHYPythonTools.helpers import deltaPhi as delta_Phi
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.HEPHYPythonTools.user import *
from Workspace.RA4Analysis.helpers import *
from draw_helpers import *
from eleID_helper import *

#small = True
small = False
bunchCrossing = '50ns'
#bunchCrossing = '25ns'

#LpInformation = pickle.load(file('/data/'+username+'/results2015/convertHistToPickle/njet2_nbtagEq0_Z-Wratio_Lp_pkl'))

def getWeight(sample,nEvents,target_lumi):
  weight = xsec[sample['dbsName']] * target_lumi/nEvents
  return weight

if bunchCrossing == '50ns':
  from Workspace.RA4Analysis.cmgTuples_Data50ns_1l import *
  from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_postProcessed import *
  targetLumi = 42 #pb-1
  sampleLumi = 3000 #pb-1
  #Bkg chains 
  diLepBkg=[
  #          {'name':'TTJets_50ns', 'sample':TTJets_50ns, 'legendName':'t#bar{t}+jets', 'selection':'diLep', 'weight':'weight', 'color':ROOT.kBlue-2, 'merge':'ttbar'},
            {'name':'DY_50ns', 'sample':DY_50ns, 'legendName':'DY' , 'selection':'diLep', 'weight':'weight', 'color':ROOT.kRed-6, 'merge':'DY_inclusive', 'treeName':'Events'},
  #       {'name':'DYJetsToLL_M_50_HT100to200_50ns', 'sample':DYJetsToLL_M_50_HT100to200_50ns, 'legendName':'DY', 'color':ROOT.kRed-6, 'merge':'DY_HTbinned'},
  #       {'name':'DYJetsToLL_M_50_HT200to400_50ns', 'sample':DYJetsToLL_M_50_HT200to400_50ns, 'legendName':'DY', 'color':ROOT.kRed-6, 'merge':'DY_HTbinned'},
  #       {'name':'DYJetsToLL_M_50_HT400to600_50ns', 'sample':DYJetsToLL_M_50_HT400to600_50ns, 'legendName':'DY', 'color':ROOT.kRed-6, 'merge':'DY_HTbinned'},
  #       {'name':'DYJetsToLL_M_50_HT600toInf_50ns', 'sample':DYJetsToLL_M_50_HT600toInf_50ns, 'legendName':'DY', 'color':ROOT.kRed-6, 'merge':'DY_HTbinned'},
  ]
  
  singleLepBkg=[
                {'name':'WJetsToLNu_50ns', 'sample':WJetsToLNu_50ns, 'legendName':'W+jets', 'selection':'singleLep', 'weight':'weight', 'color':ROOT.kGreen-2, 'merge':'Wjets', 'treeName':'Events'},
  ]
  #Data
  diLepData=[
       #{'name':'DoubleMuon_Run2015B_17Jul2015', 'sample':DoubleMuon_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'Data'},
       {'name':'DoubleMuon_Run2015B_PromptReco', 'sample':DoubleMuon_Run2015B_PromptReco, 'legendName':'Data', 'selection':'diLep', 'treeName':'tree'},
       #{'name':'DoubleEG_Run2015B_17Jul2015', 'sample':DoubleEG_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'Data'},
       {'name':'DoubleEG_Run2015B_PromptReco', 'sample':DoubleEG_Run2015B_PromptReco, 'legendName':'Data', 'selection':'diLep', 'treeName':'tree'},
  ]
  singleLepData=[
       #{'name':'SingleMuon_Run2015B_17Jul2015', 'sample':SingleMuon_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'singleLepData'},
       {'name':'SingleMuon_Run2015B_PromptReco', 'sample':SingleMuon_Run2015B_PromptReco, 'legendName':'Data', 'selection':'singleLep', 'treeName':'tree'},
       #{'name':'SingleElectron_Run2015B_17Jul2015', 'sample':SingleElectron_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'singleLepData'},
       {'name':'SingleElectron_Run2015B_PromptReco', 'sample':SingleElectron_Run2015B_PromptReco, 'legendName':'Data', 'selection':'singleLep', 'treeName':'tree'},
  ]

  maxN=1 if small else -1
  
  for sample in diLepBkg+singleLepBkg+diLepData+singleLepData:
    sample['chain'] = getChain(sample['sample'],histname='',treeName=sample['treeName'])
  
#  for sample in diLepBkg+singleLepBkg:
#    sample['weight'] = getWeight(sample['sample'], sample['nEvents'], targetLumi)

if bunchCrossing == '25ns':
  from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *
  targetLumi = 3000 #pb-1
  #Bkg chains 
  diLepBkg=[
  #          {'name':'TTJets_25ns', 'sample':TTJets_25ns, 'legendName':'t#bar{t}+jets', 'selection':'diLep', 'color':ROOT.kBlue-2, 'weight':'weight'},
            {'name':'DY_25ns', 'sample':DY_25ns, 'legendName':'DY' , 'selection':'diLep', 'color':ROOT.kRed-6, 'weight':'weight', 'treeName':'Events'},
  ]

  singleLepBkg=[
                {'name':'WJetsHTToLNu_25ns', 'sample':WJetsHTToLNu_25ns, 'legendName':'W+jets', 'selection':'singleLep', 'color':ROOT.kGreen-2, 'weight':'weight', 'treeName':'Events'},
  ]
#  #Data
#  diLepData=[
#       #{'name':'DoubleMuon_Run2015B_17Jul2015', 'sample':DoubleMuon_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'Data'},
#       {'name':'DoubleMuon_Run2015B_PromptReco', 'sample':DoubleMuon_Run2015B_PromptReco, 'legendName':'Data', 'selection':'diLep'},
#       #{'name':'DoubleEG_Run2015B_17Jul2015', 'sample':DoubleEG_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'Data'},
#       {'name':'DoubleEG_Run2015B_PromptReco', 'sample':DoubleEG_Run2015B_PromptReco, 'legendName':'Data', 'selection':'diLep'},
#  ]
#  singleLepData=[
#       #{'name':'SingleMuon_Run2015B_17Jul2015', 'sample':SingleMuon_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'singleLepData'},
#       {'name':'SingleMuon_Run2015B_PromptReco', 'sample':SingleMuon_Run2015B_PromptReco, 'legendName':'Data', 'selection':'singleLep'},
#       #{'name':'SingleElectron_Run2015B_17Jul2015', 'sample':SingleElectron_Run2015B_17Jul2015, 'legendName':'Data', 'merge':'singleLepData'},
#       {'name':'SingleElectron_Run2015B_PromptReco', 'sample':SingleElectron_Run2015B_PromptReco, 'legendName':'Data', 'selection':'singleLep'},
#  ]

  for sample in diLepBkg+singleLepBkg:#+diLepData+singleLepData:
    sample['chain'] = getChain(sample['sample'],histname='',treeName=sample['treeName']) 

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
  #s['chain'] = getChain(s['sample'],histname='')
  #s['chain'].SetAlias('dPhi',dPhiStr)

#defining ht, st and njets for SR
streg = [(200,400)]#,(350,450),(450,-1)]                         
htreg = [(200,-1)]#,(750,1000),(1000,1250),(1250,-1)]
njreg = [(2,-1)]
btb = [(0,0)]
#diMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt[0]>=25&&LepGood_pt[1]>=20&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0&&((LepGood_charge[0]+LepGood_charge[1])==0))==2)'
diMuonic = '((Sum$(abs(genLep_pdgId)==13&&abs(genLep_motherId)==23)==2)&&ngenLep==2)'
#diElectronic = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt[0]>=25&&LepGood_pt[1]>=20&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0&&((LepGood_charge[0]+LepGood_charge[1])==0))==2)"
diElectronic = "((Sum$(abs(genLep_pdgId)==11&&abs(genLep_motherId)==23)==2)&&ngenLep==2)"
#singleMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)==1)'
singleMuonic = '(Sum$(abs(genLep_pdgId)==13&&abs(genLep_motherId)==24)==1)'
#singleMuonic = '(Sum$(genLep_pdgId==13&&genLep_motherId==(-24)&&genLep_pt>=25&&abs(genLep_eta)<2.4)==1)'
#singleElectronic = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0)==1)"
singleElectronic = "(Sum$(abs(genLep_pdgId)==11&&abs(genLep_motherId)==24)==1)"
#singleElectronic = "(Sum$(genLep_pdgId==11&&genLep_motherId==(-24)&&genLep_pt>=25&&abs(genLep_eta)<2.4)==1)"
diLepPresel = '('+diMuonic+'||'+diElectronic+')'
singleLepPresel = '('+singleMuonic+'||'+singleElectronic+')'
preprefix = 'ZtoWclosure_MCstudy'
wwwDir = saveDir+'RunII/Spring15_'+bunchCrossing+'/'+preprefix+'/'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

def getLt(c):
  leadLepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  met = c.GetLeaf('met_pt').GetValue()
  Lt = met + leadLepPt
  return Lt

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

def getInvMass(c):
  leadLepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  leadLepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  leadLepEta = c.GetLeaf('LepGood_eta').GetValue(0)
  subLepPt = c.GetLeaf('LepGood_pt').GetValue(1)
  subLepPhi = c.GetLeaf('LepGood_phi').GetValue(1)
  subLepEta = c.GetLeaf('LepGood_eta').GetValue(1)
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

def getZLp(c):
  lepPt = c.GetLeaf('LepGood_pt').GetValue(1)
  lepPhi = c.GetLeaf('LepGood_phi').GetValue(1)
  nuPt = c.GetLeaf('LepGood_pt').GetValue(0)
  nuPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  Lp = (lepPt/sqrt(lepPt**2+nuPt**2+2*lepPt*nuPt*cos(lepPhi-nuPhi)))*((lepPt+nuPt*cos(lepPhi-nuPhi))/sqrt(lepPt**2+nuPt**2+2*lepPt*nuPt*cos(lepPhi-nuPhi)))
  return Lp

def getGenZdPhi(c):
  lepton1 = getObjDict(sample['chain'], 'genLep_', ['pt','eta','phi','mass','pdgId','motherId'], 0)
  lepton2 = getObjDict(sample['chain'], 'genLep_', ['pt','eta','phi','mass','pdgId','motherId'], 1)
  if lepton1['pt'] > lepton2['pt']:
    leadLep = lepton1
    subLep = lepton2
  else:
    leadLep = lepton2
    subLep = lepton1
  #leading lepton becomes neutrino
  nuPt = leadLep['pt']
  nuPhi = leadLep['phi']
  lepPt = subLep['pt']
  lepPhi = subLep['phi']  
  dPhi = acos((lepPt+nuPt*cos(lepPhi-nuPhi))/sqrt(lepPt**2+nuPt**2+2*lepPt*nuPt*cos(lepPhi-nuPhi)))
  return dPhi

def getGenZPt(c):
  leadLepPt = c.GetLeaf('genLep_pt').GetValue(0)
  leadLepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  subLepPt = c.GetLeaf('genLep_pt').GetValue(1)
  subLepPhi = c.GetLeaf('genLep_phi').GetValue(1)
  Zpt = sqrt(leadLepPt**2+subLepPt**2+2*leadLepPt*subLepPt*cos(leadLepPhi-subLepPhi))
  return Zpt

def getGenZLp(c):
  lepton1 = getObjDict(sample['chain'], 'genLep_', ['pt','eta','phi','mass','pdgId','motherId'], 0)
  lepton2 = getObjDict(sample['chain'], 'genLep_', ['pt','eta','phi','mass','pdgId','motherId'], 1)
  if lepton1['pt'] > lepton2['pt']:
    leadLep = lepton1
    subLep = lepton2
  else:
    leadLep = lepton2
    subLep = lepton1
  #leading lepton becomes neutrino
  nuPt = leadLep['pt']
  nuPhi = leadLep['phi']
  lepPt = subLep['pt']
  lepPhi = subLep['phi']
  Lp = (lepPt/sqrt(lepPt**2+nuPt**2+2*lepPt*nuPt*cos(lepPhi-nuPhi)))*((lepPt+nuPt*cos(lepPhi-nuPhi))/sqrt(lepPt**2+nuPt**2+2*lepPt*nuPt*cos(lepPhi-nuPhi)))
  return Lp

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

def getGenZ(c):
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
#  leadX = leadLepPt * cos(leadLepPhi)
#  leadY = leadLepPt * sin(leadLepPhi)
#  leadZ = leadLepPt * sinh(leadLepEta)
#  subX = subLepPt * cos(subLepPhi)
#  subY = subLepPt * sin(subLepPhi)
#  subZ = subLepPt * sinh(subLepEta)
#  cosdPhi = (leadX*subX + leadY*subY + leadZ*subZ)/(sqrt(leadX**2 + leadY**2 + leadZ**2) * sqrt(subX**2 + subY**2 + subZ**2))
  leadLep.SetPtEtaPhiM(leadLepPt,leadLepEta,leadLepPhi,leadLepMass)
  subLep.SetPtEtaPhiM(subLepPt,subLepEta,subLepPhi,subLepMass)
  Z = leadLep + subLep
  return leadLepPt 

def getGenZptRatio(c):
  lepPt = c.GetLeaf('genLep_pt').GetValue(1)
  lepPhi = c.GetLeaf('genLep_phi').GetValue(1)
  nuPt = c.GetLeaf('genLep_pt').GetValue(0)
  nuPhi = c.GetLeaf('genLep_phi').GetValue(0)
  return (lepPt/sqrt(lepPt**2+nuPt**2+2*lepPt*nuPt*cos(lepPhi-nuPhi)))

def getWdPhi(c):
  lepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  lepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  metPt = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  dPhi = acos((lepPt+metPt*cos(lepPhi-metPhi))/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))
  return dPhi

def getWLp(c):
  lepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  lepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  metPt = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  Lp = (lepPt/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))*((lepPt+metPt*cos(lepPhi-metPhi))/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))
  return Lp

def getGenWdPhi(c):
  lepPt = c.GetLeaf('genLep_pt').GetValue(0)
  lepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  metPt = c.GetLeaf('met_genPt').GetValue()
  metPhi = c.GetLeaf('met_genPhi').GetValue()
  dPhi = acos((lepPt+metPt*cos(lepPhi-metPhi))/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))
  return dPhi

def getGenWPt(c):
  lepPt = c.GetLeaf('genLep_pt').GetValue(0)
  lepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  metPt = c.GetLeaf('met_genPt').GetValue()
  metPhi = c.GetLeaf('met_genPhi').GetValue()
  Wpt = sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi))
  return Wpt

def getGenWLp(c):
  lepPt = c.GetLeaf('genLep_pt').GetValue(0)
  lepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  metPt = c.GetLeaf('met_genPt').GetValue()
  metPhi = c.GetLeaf('met_genPhi').GetValue()
  Lp = (lepPt/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))*((lepPt+metPt*cos(lepPhi-metPhi))/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))
  return Lp
 
def getGenWEta(c):
  genPartAll = [getObjDict(c, 'genPartAll_', ['pt','eta','phi','mass','pdgId','motherId'], j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  neutrino = filter(lambda n:abs(n['pdgId']) in [12,14], genPartAll)
  nuFromW = filter(lambda w:abs(w['motherId'])==24, neutrino)
  if len(nuFromW)>0:
    if len(nuFromW)>1: print 'this should not have happened'
    if abs(nuFromW[0]['pdgId'])-abs(c.GetLeaf('genLep_pdgId').GetValue(0))>1.: print 'this should not have happened'
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

def getGenWptRatio(c):
  lepPt = c.GetLeaf('genLep_pt').GetValue(0)
  lepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  metPt = c.GetLeaf('met_genPt').GetValue()
  metPhi = c.GetLeaf('met_genPhi').GetValue()
  return (lepPt/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))

def getGenW(c):
  genPartAll = [getObjDict(c, 'genPartAll_', ['pt','eta','phi','mass','pdgId','motherId'], j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  neutrino = filter(lambda n:abs(n['pdgId']) in [12,14], genPartAll)
  nuFromW = filter(lambda w:abs(w['motherId'])==24, neutrino)
  if len(nuFromW)>0:
    if len(nuFromW)>1: print 'this should not have happened'
    if abs(nuFromW[0]['pdgId'])-abs(c.GetLeaf('genLep_pdgId').GetValue(0))>1.: print 'this should not have happened'
    leadLep = ROOT.TLorentzVector()
    nu = ROOT.TLorentzVector()
    W = ROOT.TLorentzVector()
    lepPt = c.GetLeaf('genLep_pt').GetValue(0)
    lepEta = c.GetLeaf('genLep_eta').GetValue(0)
    lepPhi = c.GetLeaf('genLep_phi').GetValue(0)
    lepMass = c.GetLeaf('genLep_mass').GetValue(0)
    nuPt = nuFromW[0]['pt']
    nuEta = nuFromW[0]['eta']
    nuPhi = nuFromW[0]['phi']
    nuMass = nuFromW[0]['mass']
#    leadLep.SetPtEtaPhiM(lepPt,lepEta,lepPhi,lepMass)
#    nu.SetPtEtaPhiM(nuPt,nuEta,nuPhi,nuMass)
#    W = leadLep + nu
#  if lepPt < nuPt:
#    return Pt
#  else:
#    return nuPt
    dPhi = acos((lepPt+nuPt*cos(lepPhi-nuPhi))/sqrt(lepPt**2+nuPt**2+2*lepPt*nuPt*cos(lepPhi-nuPhi)))
    return dPhi

def getleadingJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  Jet0 = jets[0]['pt']
  return Jet0

def getsecondJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  Jet1 = jets[1]['pt']
  return Jet1


diLepVariables = []

diLepmet = {'name':'mymet', 'varString':"met_pt", 'legendName':'#slash{E}_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[32,0,800]}
diLepht = {'name':'myht', 'varFunc':getHt, 'legendName':'H_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
diLepLt = {'name':'mylt', 'varFunc':getLt, 'legendName':'L_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
diLepnJets = {'name':'mynJets', 'varFunc':getNJets, 'legendName':'Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
diLepdPhi = {'name':'mydeltaPhi', 'varFunc':getGenZdPhi, 'legendName':'#Delta#Phi(Boson,l)','binning':[30,0,pi], 'Ytitle':'# of Events'}#, 'binningIsExplicit':True}
diLepLp = {'name':'myLp', 'varFunc':getGenZLp, 'legendName':'L_{P}', 'Ytitle':'# of Events', 'binning':[60,-2.5,3.5]}
diLeplMomentum = {'name':'myleptonPt', 'varFunc':getLeadLep, 'legendName':'p_{T}(lead. l)', 'Ytitle':'# of Events / 25GeV', 'binning':[40,0,1000]}
diLepZmomentum = {'name':'myZPt', 'varFunc':getZPt, 'legendName':'p_{T}(Z)', 'Ytitle':'# of Events / 25GeV', 'binning':[40,0,1000]}
diLepZphi = {'name':'myZPhi', 'varFunc':getZPhi, 'legendName':'#phi(Z)', 'Ytitle':'# of Events', 'binning':[40,-pi,pi]}
diLepinvMassVar = {'name':'myInvMass', 'varFunc':getInvMass, 'legendName':'m_{ll}', 'Ytitle':'# of Events / 1GeV', 'binning':[30,76,106]}
diLepleadingJet = {'name':'myleadingJet', 'varFunc':getleadingJet, 'legendName':'p_{T}(leading Jet)', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
diLepsecondJet = {'name':'mysecondJet', 'varFunc':getsecondJet, 'legendName':'p_{T}(J_{2})', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
#diLepBJets = {'name':'mynBJets', 'varString':'nBJetMediumCMVA30', 'legendName':'B Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
diVar = {'name':'myVar', 'varFunc':getGenZdPhi, 'legendName':'L_{P}', 'Ytitle':'# of Events', 'binning':[30,0,pi]}

#diLepVariables.append(met)
#diLepVariables.append(ht)
#diLepVariables.append(Lt)
#diLepVariables.append(nJets)
diLepVariables.append(diVar)
#diLepVariables.append(lMomentum)
#diLepVariables.append(Zmomentum)
#diLepVariables.append(Zphi)
#diLepVariables.append(invMassVar)
#diLepVariables.append(leadingJet)
#diLepVariables.append(secondJet)
#diLepVariables.append(nBJets)

singleLepVariables = []

singleLepmet = {'name':'mymet', 'varString':"met_pt", 'legendName':'#slash{E}_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[32,0,800]}
singleLepht = {'name':'myht', 'varFunc':getHt, 'legendName':'H_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
singleLepLt = {'name':'mylt', 'varFunc':getLt, 'legendName':'L_{T}', 'Ytitle':'# of Events / 25GeV', 'binning':[64,0,1600]}
singleLepnJets = {'name':'mynJets', 'varFunc':getNJets, 'legendName':'Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
singleLepdPhi = {'name':'mydeltaPhi', 'varFunc':getGenWdPhi, 'legendName':'#Delta#Phi(W,l)','binning':[30,0,pi], 'Ytitle':'# of Events'}#, 'binningIsExplicit':True}
singleLeplMomentum = {'name':'myleptonPt', 'varFunc':getLeadLep, 'legendName':'p_{T}(lead. l)', 'Ytitle':'# of Events / 25GeV', 'binning':[40,0,1000]}
singleLepZmomentum = {'name':'myZPt', 'varFunc':getZPt, 'legendName':'p_{T}(Z)', 'Ytitle':'# of Events / 25GeV', 'binning':[40,0,1000]}
singleLepZphi = {'name':'myZPhi', 'varFunc':getZPhi, 'legendName':'#phi(Z)', 'Ytitle':'# of Events', 'binning':[40,-pi,pi]}
singleLepinvMassVar = {'name':'myInvMass', 'varFunc':getInvMass, 'legendName':'m_{ll}', 'Ytitle':'# of Events / 1GeV', 'binning':[30,76,106]}
singleLepleadingJet = {'name':'myleadingJet', 'varFunc':getleadingJet, 'legendName':'p_{T}(leading Jet)', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
singleLepsecondJet = {'name':'mysecondJet', 'varFunc':getsecondJet, 'legendName':'p_{T}(J_{2})', 'Ytitle':'# of Events / 50GeV', 'binning':[32,0,1600]}
#singleLepnBJets = {'name':'mynBJets', 'varString':'nBJetMediumCMVA30', 'legendName':'B Jets', 'Ytitle':'# of Events', 'binning':[17,-0.5,16.5]}
singleVar = {'name':'myVar', 'varFunc':getGenW, 'legendName':'L_{P}', 'Ytitle':'# of Events', 'binning':[30,0,pi]}

#singleLepVariables.append(met)
#singleLepVariables.append(ht)
#singleLepVariables.append(Lt)
#singleLepVariables.append(nJets)
singleLepVariables.append(singleVar)
#singleLepVariables.append(lMomentum)
#singleLepVariables.append(Zmomentum)
#singleLepVariables.append(Zphi)
#singleLepVariables.append(invMassVar)
#singleLepVariables.append(leadingJet)
#singleLepVariables.append(secondJet)
#singleLepVariables.append(nBJets)

histos = {}
histos['mergeDY'] = {}
histos['data'] = {}
histos['singleLep'] = {}
histos['diLep'] = {}
h_ratio = {}

deltaPhi = {}
deltaPhi['singleLep'] = {}
deltaPhi['diLep'] = {}

for i_htb, htb in enumerate(htreg):
  for stb in streg:
    for srNJet in njreg:
      for b in btb:
        print 'Var region => ht: ',htb,'NJet: ',srNJet,'B-tag:',b

        deltaPhi['diLep']['lowDP'] = 0
        deltaPhi['diLep']['lowDPvar'] = 0
        deltaPhi['diLep']['highDP'] = 0
        deltaPhi['diLep']['highDPvar'] = 0
        deltaPhi['singleLep']['lowDP'] = 0
        deltaPhi['singleLep']['lowDPvar'] = 0
        deltaPhi['singleLep']['highDP'] = 0
        deltaPhi['singleLep']['highDPvar'] = 0

        for sample in diLepBkg: #Loop over samples
          histos['diLep'][sample['name']] = {}

          for var in diLepVariables:
            if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
              histos['diLep'][sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name']+'_diLep', sample['name']+'_'+var['name']+'_diLep', len(var['binning'])-1, array('d', var['binning']))
            else:
              histos['diLep'][sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name']+'_diLep', sample['name']+'_'+var['name']+'_diLep', *var['binning'])
            histos['diLep'][sample['name']][var['name']].Reset()
            
          diLepNamestr, diLepCut = nameAndCut(None, None, None, btb=None, presel=diLepPresel)
          #diLepCut = diLepPresel#+'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nBTagCut(b, minPt=30, maxEta=2.4, minCSVTag=0.890)#+'&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)#+'&&'+nJetCut(2, minPt=30, maxEta=2.4)

          sample["chain"].Draw(">>eList",diLepCut) #Get the event list 'eList' which has all the events satisfying the cut
          elist = ROOT.gDirectory.Get("eList")
          number_events = elist.GetN()
          print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
          
          #Event loop
          for i in range(number_events): #Loop over those events
            if i%10000==0:
              print "At %i of %i for sample %s"%(i,number_events,sample['name'])

            sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
            #invMass = getInvMass(sample['chain'])
            #if abs(invMass-91.)>15: continue
            #Lt = getLt(sample['chain'])
            #if Lt<stb[0]: continue
            #if stb[1]>0 and Lt>stb[1]: continue

#            Lp = getGenZLp(sample['chain'])
#            reweight = LpInformation[0]['BinContent']
#            for bin in LpInformation:
#              if Lp > bin['BinLowEdge']: 
#                reweight = bin['BinContent']
            weight = 1
            if sample.has_key('weight'):
              if type(sample['weight'])==type(''):
                sampleWeight = getVarValue(sample['chain'], sample['weight'])
                weight = (sampleWeight/sampleLumi)*targetLumi# * (1./reweight)
              else:
                genWeight = sample['chain'].GetLeaf('genWeight').GetValue()
                weight = sample['weight'] * genWeight
#            if sample.has_key('merge'):
#              if sample['merge']=='Data':
#            dPhi = getGenZdPhi(sample['chain'])
#            if dPhi<1.0:
#              deltaPhi['diLep']['lowDP'] += weight
#              deltaPhi['diLep']['lowDPvar'] += weight*weight
#            else:
#              deltaPhi['diLep']['highDP'] += weight
#              deltaPhi['diLep']['highDPvar'] += weight*weight
            for var in diLepVariables:
              assert (var.has_key('varString') or var.has_key('varFunc')), "Error: Did not specify 'varString' or 'varFunc' for var %s" % repr(var)
              assert not (var.has_key('varString') and var.has_key('varFunc')), "Error: Specified both 'varString' and 'varFunc' for var %s" % repr(var)
              varValue = getVarValue(sample["chain"], var['varString']) if var.has_key('varString') else var['varFunc'](sample["chain"])
              histos['diLep'][sample['name']][var['name']].Fill(varValue, weight)
          del elist
 
        for sample in singleLepBkg: #Loop over samples
          histos['singleLep'][sample['name']] = {}

          for var in singleLepVariables:
            if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
              histos['singleLep'][sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name']+'_singleLep', sample['name']+'_'+var['name']+'_singleLep', len(var['binning'])-1, array('d', var['binning']))
            else:
              histos['singleLep'][sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name']+'_singleLep', sample['name']+'_'+var['name']+'_singleLep', *var['binning'])
            histos['singleLep'][sample['name']][var['name']].Reset()
            
          singleLepNamestr,singleLepCut = nameAndCut(None, None, None, btb=None, presel=singleLepPresel)
          #singleLepCut = singleLepPresel#+'&&'+nJetCut(srNJet, minPt=30, maxEta=2.4)+'&&'+nBTagCut(b, minPt=30, maxEta=2.4, minCSVTag=0.890)#+'&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)#+'&&'+nJetCut(2, minPt=30, maxEta=2.4)

          sample["chain"].Draw(">>eList",singleLepCut) #Get the event list 'eList' which has all the events satisfying the cut
          elist = ROOT.gDirectory.Get("eList")
          number_events = elist.GetN()
          print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
          
          #Event loop
          for i in range(number_events): #Loop over those events
            if i%10000==0:
              print "At %i of %i for sample %s"%(i,number_events,sample['name'])

            sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
            #invMass = getInvMass(sample['chain'])
            #if abs(invMass-91.)>15: continue
            #Lt = getLt(sample['chain'])
            #if Lt<stb[0]: continue
            #if stb[1]>0 and Lt>stb[1]: continue
            weight = 1           
            if sample.has_key('weight'):
              if type(sample['weight'])==type(''):
                sampleWeight = getVarValue(sample['chain'], sample['weight'])
                weight = (sampleWeight/sampleLumi)*targetLumi
              else:
                genWeight = sample['chain'].GetLeaf('genWeight').GetValue()
                weight = sample['weight'] * genWeight
#            dPhi = getGenWdPhi(sample['chain'])
#            if dPhi<1.0:
#              deltaPhi['singleLep']['lowDP'] += weight
#              deltaPhi['singleLep']['lowDPvar'] += weight*weight
#            else:
#              deltaPhi['singleLep']['highDP'] += weight
#              deltaPhi['singleLep']['highDPvar'] += weight*weight
            for var in singleLepVariables:
              assert (var.has_key('varString') or var.has_key('varFunc')), "Error: Did not specify 'varString' or 'varFunc' for var %s" % repr(var)
              assert not (var.has_key('varString') and var.has_key('varFunc')), "Error: Specified both 'varString' and 'varFunc' for var %s" % repr(var)
              varValue = getVarValue(sample["chain"], var['varString']) if var.has_key('varString') else var['varFunc'](sample["chain"])
              histos['singleLep'][sample['name']][var['name']].Fill(varValue, weight)
          del elist
         
          #for sample in signals:
          #  for var in allVariables:
          #    if histos[sample['name']][var['name']].Integral()>0:
          #      histos[sample['name']][var['name']].Scale(histos['TTJets'][var['name']].Integral()/histos[sample['name']][var['name']].Integral())

        #plotting
        canvas = ROOT.TCanvas('closure','closure')
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        l = ROOT.TLegend(0.8,0.85,0.98,0.95)
        l.SetFillColor(0)
        l.SetBorderSize(1)
        l.SetShadowColor(ROOT.kWhite)
 
        text = ROOT.TLatex()
        text.SetNDC()
        text.SetTextSize(0.045)
        text.SetTextAlign(11) 

        if bunchCrossing=='50ns':
          histo_diLep = histos['diLep']['DY_50ns']['myVar'].Clone()
          #histo_diLep.Add(histos['diLep']['TTJets_50ns']['myVar'])
          wjetsStr = 'WJetsToLNu_50ns'
        elif bunchCrossing=='25ns':
          histo_diLep = histos['diLep']['DY_25ns']['myVar'].Clone()
          #histo_diLep.Add(histos['diLep']['TTJets_25ns']['myVar'])
          wjetsStr = 'WJetsHTToLNu_25ns'
        histo_diLep.SetLineColor(ROOT.kBlue)
        histo_diLep.SetLineStyle(7)
        histo_diLep.SetLineWidth(2)
        histo_diLep.SetMarkerStyle(0)
        histo_diLep.GetXaxis().SetTitle('#Delta#Phi')
        histo_diLep.GetYaxis().SetTitle('# of Events')# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
        histo_diLep.GetXaxis().SetLabelSize(0.04)
        histo_diLep.GetYaxis().SetLabelSize(0.04)
        l.AddEntry(histo_diLep,'Z #rightarrow W')
        histo_diLep.Draw('hist e')
        histo_diLep.SetMinimum(0.08)
        histo_diLep.SetMaximum(100*histo_diLep.GetMaximum())

        histos['singleLep'][wjetsStr]['myVar'].SetLineColor(ROOT.kRed)
        histos['singleLep'][wjetsStr]['myVar'].SetLineWidth(2)
        histos['singleLep'][wjetsStr]['myVar'].SetMarkerStyle(0)
        histos['singleLep'][wjetsStr]['myVar'].GetXaxis().SetTitle('#Delta#Phi')
        histos['singleLep'][wjetsStr]['myVar'].GetYaxis().SetTitle('# of Events')# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
        histos['singleLep'][wjetsStr]['myVar'].GetXaxis().SetLabelSize(0.04)
        histos['singleLep'][wjetsStr]['myVar'].GetYaxis().SetLabelSize(0.04)
        l.AddEntry(histos['singleLep'][wjetsStr]['myVar'],'W+jets')
        histos['singleLep'][wjetsStr]['myVar'].Draw('hist same e')
        histos['singleLep'][wjetsStr]['myVar'].SetMinimum(0.08)
        histos['singleLep'][wjetsStr]['myVar'].SetMaximum(100*histos['singleLep'][wjetsStr]['myVar'].GetMaximum())
        l.Draw()
        
#        if deltaPhi['diLep']['lowDP']>0:
#          rcsDiLep = float(deltaPhi['diLep']['highDP'])/float(deltaPhi['diLep']['lowDP'])
#          if deltaPhi['diLep']['highDP']>0:
#            rcsE_sim_DiLep = rcsDiLep*sqrt(float(deltaPhi['diLep']['lowDPvar'])/float(deltaPhi['diLep']['lowDP'])**2+float(deltaPhi['diLep']['highDPvar'])/float(deltaPhi['diLep']['highDP'])**2)
#            rcsE_pred_DiLep = rcsDiLep*sqrt(1./deltaPhi['diLep']['lowDP']+1./deltaPhi['diLep']['highDP'])
#          else:
#            rcsDiLep=float('nan')
#            rcsE_pred_DiLep=float('nan')
#            rcsE_sim_DiLep=float('nan')
#        else:
#          rcsDiLep=float('nan')
#          rcsE_pred_DiLep=float('nan')
#          rcsE_sim_DiLep=float('nan')
#        if deltaPhi['singleLep']['lowDP']>0:
#          rcsSingleLep = float(deltaPhi['singleLep']['highDP'])/float(deltaPhi['singleLep']['lowDP'])
#          if deltaPhi['singleLep']['highDP']>0:
#            rcsE_sim_SingleLep = rcsSingleLep*sqrt(float(deltaPhi['singleLep']['lowDPvar'])/float(deltaPhi['singleLep']['lowDP'])**2+float(deltaPhi['singleLep']['highDPvar'])/float(deltaPhi['singleLep']['highDP'])**2)
#            rcsE_pred_SingleLep = rcsSingleLep*sqrt(1./deltaPhi['singleLep']['lowDP']+1./deltaPhi['singleLep']['highDP'])
#          else:
#            rcsSingleLep=float('nan')
#            rcsE_pred_SingleLep=float('nan')
#            rcsE_sim_SingleLep=float('nan')
#        else:
#          rcsSingleLep=float('nan')
#          rcsE_pred_SingleLep=float('nan')
#          rcsE_sim_SingleLep=float('nan')
#        rCStext = ROOT.TLatex()
#        rCStext.SetNDC()
#        rCStext.SetTextSize(0.035)
#        rCStext.SetTextAlign(11)
#        rCStext.DrawLatex(0.20,0.88,'#bf{R^{Z#rightarrow W}_{CS} = '+str(round(rcsDiLep,4))+'#pm'+str(round(rcsE_sim_DiLep,4))+'}')
#        rCStext.DrawLatex(0.20,0.82,'#bf{R^{W}_{CS} = '+str(round(rcsSingleLep,4))+'#pm'+str(round(rcsE_sim_SingleLep,4))+'}')
  
        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")
        
        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
          
        h_ratio['deltaPhi'] = histo_diLep.Clone()
        h_ratio['deltaPhi'].Sumw2()
        h_ratio['deltaPhi'].Scale(1./h_ratio['deltaPhi'].Integral())
        h_ratio['deltaPhi'].SetMinimum(-0.4)
        h_ratio['deltaPhi'].SetMaximum(2.4)
        h_ratio['deltaPhi'].SetStats(0)
        #histo_diLepDummy = histo_diLep.Clone()
        #histo_diLepDummy.Scale(1./histo_diLep.Integral())
        #h_ratio['deltaPhi'].Add(histo_diLepDummy,-1.)
        histo_dummy = histos['singleLep'][wjetsStr]['myVar'].Clone()
        histo_dummy.Scale(1./histo_dummy.Integral())
        h_ratio['deltaPhi'].Divide(histo_dummy)
        h_ratio['deltaPhi'].SetMarkerStyle(20)
        h_ratio['deltaPhi'].SetLineColor(ROOT.kBlack)
        h_ratio['deltaPhi'].SetLineStyle(1)
        h_ratio['deltaPhi'].SetLineWidth(1)
        h_ratio['deltaPhi'].Draw("ep")
        h_ratio['deltaPhi'].GetXaxis().SetTitle('#Delta#Phi')
        h_ratio['deltaPhi'].GetYaxis().SetTitle("Z/W")
        h_ratio['deltaPhi'].GetYaxis().SetNdivisions(505)
        h_ratio['deltaPhi'].GetYaxis().SetTitleSize(23)
        h_ratio['deltaPhi'].GetYaxis().SetTitleFont(43)
        h_ratio['deltaPhi'].GetYaxis().SetTitleOffset(1.8)
        h_ratio['deltaPhi'].GetYaxis().SetLabelFont(43)
        h_ratio['deltaPhi'].GetYaxis().SetLabelSize(20)
        h_ratio['deltaPhi'].GetYaxis().SetLabelOffset(0.015)
        h_ratio['deltaPhi'].GetXaxis().SetNdivisions(510)
        h_ratio['deltaPhi'].GetXaxis().SetTitleSize(23)
        h_ratio['deltaPhi'].GetXaxis().SetTitleFont(43)
        h_ratio['deltaPhi'].GetXaxis().SetTitleOffset(3.4)
        h_ratio['deltaPhi'].GetXaxis().SetLabelFont(43)
        h_ratio['deltaPhi'].GetXaxis().SetLabelSize(20)
        h_ratio['deltaPhi'].GetXaxis().SetLabelOffset(0.04)
          
        canvas.cd()
        canvas.Print(wwwDir+'genLevel_1stLepNu_Z-Wclosure_dPhi.png')
        canvas.Print(wwwDir+'genLevel_1stLepNu_Z-Wclosure_dPhi.root')
        canvas.Print(wwwDir+'genLevel_1stLepNu_Z-Wclosure_dPhi.pdf')
        canvas.Clear()

        canvas2 = ROOT.TCanvas('normalization','normalization')
        canvas2.SetLogy()
        p1 = ROOT.TPad('norm_Pad','norm_Pad',0.,0.,1.,1.)
        p1.Draw()
        p1.cd()

        h_ratio['normDiLep'] = histo_diLep.Clone()
        h_ratio['normDiLep'].Sumw2()
        h_ratio['normDiLep'].SetMinimum(0.0008)
        h_ratio['normDiLep'].SetMaximum(0.3)
        h_ratio['normDiLep'].Scale(1./h_ratio['normDiLep'].Integral())
        
        h_ratio['normDiLep'].Draw('hist e')
        histo_dummy.Draw('hist e same')
        h_ratio['normDiLep'].GetXaxis().SetTitle('#Delta#Phi')
        h_ratio['normDiLep'].GetYaxis().SetTitle('a.u.')
        l.Draw()
        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas2.cd()
        canvas2.Print(wwwDir+'genLevel_1stLepNu_Z-Wclosure_normalized_dPhi.root')
        canvas2.Print(wwwDir+'genLevel_1stLepNu_Z-Wclosure_normalized_dPhi.pdf')
        canvas2.Print(wwwDir+'genLevel_1stLepNu_Z-Wclosure_normalized_dPhi.png')
        canvas2.Clear()

