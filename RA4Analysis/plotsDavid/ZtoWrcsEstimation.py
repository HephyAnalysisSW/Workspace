import ROOT
import pickle
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.TH1F().SetDefaultSumw2()
from math import *
import os, copy, sys
from array import array
from random import randint

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.HEPHYPythonTools.user import *
from Workspace.RA4Analysis.helpers import *
from draw_helpers import *
from eleID_helper import *

small = True
#small = False
bunchCrossing = '25ns'

#LpInformation = pickle.load(file('/data/'+username+'/results2015/convertHistToPickle/njet2_nbtagEq0_Z-Wratio_Lp_pkl'))

def getWeight(sample,nEvents,target_lumi):
  weight = xsec[sample['dbsName']] * target_lumi/nEvents
  return weight

if bunchCrossing == '25ns':
  from Workspace.RA4Analysis.cmgTuples_Spring15_25ns import *
  targetLumi = 3000 #pb-1
  #Bkg chains 
  diLepBkg=[
             {'name':'DYJetsToLL_M_50_HT100to200_25ns', 'sample':DYJetsToLL_M_50_HT100to200_25ns, 'legendName':'DY HT100-200', 'color':ROOT.kRed, 'merge':'EWK'},
             {'name':'DYJetsToLL_M_50_HT200to400_25ns', 'sample':DYJetsToLL_M_50_HT200to400_25ns, 'legendName':'DY HT200-400', 'color':ROOT.kRed, 'merge':'EWK'},
             {'name':'DYJetsToLL_M_50_HT400to600_25ns', 'sample':DYJetsToLL_M_50_HT400to600_25ns, 'legendName':'DY HT400-600', 'color':ROOT.kRed, 'merge':'EWK'},
             {'name':'DYJetsToLL_M_50_HT600toInf_25ns', 'sample':DYJetsToLL_M_50_HT600toInf_25ns, 'legendName':'DY HT600-Inf', 'color':ROOT.kRed, 'merge':'EWK'}

  ]

  singleLepBkg=[
                 {'name':'WJetsToLNu_HT100to200_25ns', 'sample':WJetsToLNu_HT100to200_25ns, 'legendName':'W HT100-200', 'color':ROOT.kGreen+3, 'merge':'EWK'},
                 {'name':'WJetsToLNu_HT200to400_25ns', 'sample':WJetsToLNu_HT200to400_25ns, 'legendName':'W HT200-400', 'color':ROOT.kGreen, 'merge':'EWK'},
                 {'name':'WJetsToLNu_HT400to600_25ns', 'sample':WJetsToLNu_HT400to600_25ns, 'legendName':'W HT400-600', 'color':ROOT.kGreen-3, 'merge':'EWK'},
                 {'name':'WJetsToLNu_HT600to800_25ns', 'sample':WJetsToLNu_HT600to800_25ns, 'legendName':'W HT600-800', 'color':ROOT.kGreen-7, 'merge':'EWK'},
                 {'name':'WJetsToLNu_HT800to1200_25ns', 'sample':WJetsToLNu_HT800to1200_25ns, 'legendName':'W HT800-1200', 'color':ROOT.kGreen-7, 'merge':'EWK'},
                 {'name':'WJetsToLNu_HT1200to2500_25ns', 'sample':WJetsToLNu_HT1200to2500_25ns, 'legendName':'W HT1200-2500', 'color':ROOT.kGreen-7, 'merge':'EWK'},
                 {'name':'WJetsToLNu_HT2500toInf_25ns', 'sample':WJetsToLNu_HT2500toInf_25ns, 'legendName':'W HT2500-Inf', 'color':ROOT.kGreen-7, 'merge':'EWK'}
  ]

  maxN=2 if small else -1

  for sample in diLepBkg+singleLepBkg:#+diLepData+singleLepData:
    sample['chunks'], sample['norm'] = getChunks(sample['sample'], maxN=maxN)
    sample['chain'] = ROOT.TChain('tree')
    for chunk in sample['chunks']:
      sample['chain'].Add(chunk['file'])
    sample['weight'] = getWeight(sample['sample'],sample['norm'], targetLumi)

#defining ht, st and njets for SR
streg = [(200,400)]#,(350,450),(450,-1)]                         
htreg = [(350,-1)]#,(750,1000),(1000,1250),(1250,-1)]
njreg = [(2,-1)]
btb = [(0,0)]
#diMuonic = '(Sum$(abs(LepGood_pdgId)==13&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)==2)'
diMuonic = '((Sum$(abs(genLep_pdgId)==13&&genLep_pt>10&&abs(genLep_eta)<2.5&&abs(genLep_motherId)==23)==2)&&ngenLep==2)'
#diElectronic = "(Sum$(abs(LepGood_pdgId)==11&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0)==2)"
diElectronic = "((Sum$(abs(genLep_pdgId)==11&&genLep_pt>10&&abs(genLep_eta)<2.5&&abs(genLep_motherId)==23)==2)&&ngenLep==2)"
#singleMuonic = '(Sum$(abs(LepGood_pdgId)==13&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)==1)'
singleMuonic = '((Sum$(abs(genLep_pdgId)==13&&genLep_pt>10&&abs(genLep_eta)<2.5&&abs(genLep_motherId)==24)==1)&&ngenLep==1)'
#singleElectronic = "(Sum$(abs(LepGood_pdgId)==11&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0)==1)"
singleElectronic = "((Sum$(abs(genLep_pdgId)==11&&genLep_pt>10&&abs(genLep_eta)<2.5&&abs(genLep_motherId)==24)==1)&&ngenLep==1)"
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

def getGenZ(c):
  a=randint(0,1)
  leadLep = ROOT.TLorentzVector()
  subLep = ROOT.TLorentzVector()
  Z = ROOT.TLorentzVector()
  Lep0Pt = c.GetLeaf('genLep_pt').GetValue(0)
  Lep0Eta = c.GetLeaf('genLep_eta').GetValue(0)
  Lep0Phi = c.GetLeaf('genLep_phi').GetValue(0)
  Lep0Mass = c.GetLeaf('genLep_mass').GetValue(0)
  Lep1Pt = c.GetLeaf('genLep_pt').GetValue(1)
  Lep1Eta = c.GetLeaf('genLep_eta').GetValue(1)
  Lep1Phi = c.GetLeaf('genLep_phi').GetValue(1)
  Lep1Mass = c.GetLeaf('genLep_mass').GetValue(1)
  #if Lep0Pt>Lep1Pt:
  if a:
    leadLep.SetPtEtaPhiM(Lep0Pt,Lep0Eta,Lep0Phi,Lep0Mass)
    subLep.SetPtEtaPhiM(Lep1Pt,Lep1Eta,Lep1Phi,Lep1Mass)
  #elif Lep1Pt>Lep0Pt:
  else:
    leadLep.SetPtEtaPhiM(Lep1Pt,Lep1Eta,Lep1Phi,Lep1Mass)
    subLep.SetPtEtaPhiM(Lep0Pt,Lep0Eta,Lep0Phi,Lep0Mass)
  Z = leadLep + subLep
  Lp = (leadLep.Pt()/Z.Pt())*((leadLep.Pt()+subLep.Pt()*cos(leadLep.Phi()-subLep.Phi()))/Z.Pt())
  dPhi = acos((leadLep.Pt()+subLep.Pt()*cos(leadLep.Phi()-subLep.Phi()))/Z.Pt())
  return leadLep, subLep, Z, Lp, dPhi 

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
    leadLepPt = c.GetLeaf('genLep_pt').GetValue(0)
    leadLepEta = c.GetLeaf('genLep_eta').GetValue(0)
    leadLepPhi = c.GetLeaf('genLep_phi').GetValue(0)
    leadLepMass = c.GetLeaf('genLep_mass').GetValue(0)
    nuPt = nuFromW[0]['pt']
    nuEta = nuFromW[0]['eta']
    nuPhi = nuFromW[0]['phi']
    nuMass = nuFromW[0]['mass']
    leadLep.SetPtEtaPhiM(leadLepPt,leadLepEta,leadLepPhi,leadLepMass)
    nu.SetPtEtaPhiM(nuPt,nuEta,nuPhi,nuMass)
    W = leadLep + nu
    Lp = (leadLep.Pt()/W.Pt())*((leadLep.Pt()+nu.Pt()*cos(leadLep.Phi()-nu.Phi()))/W.Pt())
    dPhi = acos((leadLep.Pt()+nu.Pt()*cos(leadLep.Phi()-nu.Phi()))/W.Pt())
    return leadLep, nu, W, Lp, dPhi

def getleadingJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  Jet0 = jets[0]['pt']
  return Jet0

def getsecondJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  Jet1 = jets[1]['pt']
  return Jet1

def getPlot(hist1,hist2,legend,legEntry1,legEntry2,Xtitle='',Ytitle='# of Events'):
  h1=hist1.Clone()
  h2=hist2.Clone()
  h1.SetLineColor(ROOT.kBlue)
  h1.SetLineStyle(7)
  h1.SetLineWidth(2)
  h1.SetMarkerStyle(0)
  h1.GetXaxis().SetTitle(Xtitle)
  h1.GetYaxis().SetTitle(Ytitle)
  h1.GetXaxis().SetLabelSize(0.04)
  h1.GetYaxis().SetLabelSize(0.04)
  legend.AddEntry(h1,legEntry1)
  h1.SetMinimum(0.08)
  h1.SetMaximum(100*h1.GetMaximum())
  h2.SetLineColor(ROOT.kRed)
  h2.SetLineStyle(1)
  h2.SetLineWidth(2)
  h2.SetMarkerStyle(0)
  h2.GetXaxis().SetTitle(Xtitle)
  h2.GetYaxis().SetTitle(Ytitle)
  h2.GetXaxis().SetLabelSize(0.04)
  h2.GetYaxis().SetLabelSize(0.04)
  legend.AddEntry(h2,legEntry2)
  h2.SetMinimum(0.08)
  h2.SetMaximum(100*h2.GetMaximum())
  return h1,h2,legend

def getRatioPlot(hist1,hist2,Xtitle='',Ytitle='Z/W'):
  h1=hist1.Clone()
  h2=hist2.Clone()
  h1.Sumw2()
  h2.Sumw2()
  h1.Scale(1./h1.Integral())
  h2.Scale(1./h2.Integral())
  h1.SetMinimum(-0.4)
  h1.SetMaximum(2.4)
  h1.SetStats(0)
  h1.Divide(h2)
  h1.SetMarkerStyle(20)
  h1.SetLineColor(ROOT.kBlack)
  h1.SetLineStyle(1)
  h1.SetLineWidth(1)
  h1.GetXaxis().SetTitle(Xtitle)
  h1.GetYaxis().SetTitle(Ytitle)
  h1.GetYaxis().SetNdivisions(505)
  h1.GetYaxis().SetTitleSize(23)
  h1.GetYaxis().SetTitleFont(43)
  h1.GetYaxis().SetTitleOffset(1.8)
  h1.GetYaxis().SetLabelFont(43)
  h1.GetYaxis().SetLabelSize(20)
  h1.GetYaxis().SetLabelOffset(0.015)
  h1.GetXaxis().SetNdivisions(510)
  h1.GetXaxis().SetTitleSize(23)
  h1.GetXaxis().SetTitleFont(43)
  h1.GetXaxis().SetTitleOffset(3.4)
  h1.GetXaxis().SetLabelFont(43)
  h1.GetXaxis().SetLabelSize(20)
  h1.GetXaxis().SetLabelOffset(0.04)          
  return h1

histos = {}
histos['mergeDY'] = {}
histos['data'] = {}
histos['singleLep'] = {}
histos['diLep'] = {}
h_ratio = {}

for i_htb, htb in enumerate(htreg):
  for stb in streg:
    for srNJet in njreg:
      for b in btb:
        print 'Var region => ht: ',htb,'NJet: ',srNJet,'B-tag:',b

        histLep1Pt = ROOT.TH1F('leadLep_pt','leadLep_pt',25,0,500)
        histLep2Pt = ROOT.TH1F('subLep_pt','subLep_pt',25,0,500) 
        histLep1Eta= ROOT.TH1F('leadLep_eta','leadLep_eta',80,-4,4)
        histLep2Eta = ROOT.TH1F('subLep_eta','subLep_eta',80,-4,4) 
        histLep1Phi= ROOT.TH1F('leadLep_phi','leadLep_phi',60,-pi,pi)
        histLep2Phi = ROOT.TH1F('subLep_phi','subLep_phi',60,-pi,pi) 
        histLep1Mass= ROOT.TH1F('leadLep_mass','leadLep_mass',100,0,1)
        histLep2Mass = ROOT.TH1F('subLep_mass','subLep_mass',100,0,1) 
        histHardZPt = ROOT.TH1F('hardZ_pt','hardZ_pt',25,0,500)
        histSoftZPt = ROOT.TH1F('softZ_pt','softZ_pt',25,0,500)
        histHardZEta= ROOT.TH1F('hardZ_eta','hardZ_eta',80,-4,4)
        histSoftZEta= ROOT.TH1F('softZ_eta','softZ_eta',80,-4,4)
        histHardZPhi= ROOT.TH1F('hardZ_phi','hardZ_phi',60,-pi,pi)
        histSoftZPhi= ROOT.TH1F('softZ_phi','softZ_phi',60,-pi,pi)
        histHardZMass= ROOT.TH1F('hardZ_mass','hardZ_mass',100,0,1)
        histSoftZMass= ROOT.TH1F('softZ_mass','softZ_mass',100,0,1)
        histZPt= ROOT.TH1F('Z_pt','Z_pt',25,0,500)
        histZEta= ROOT.TH1F('Z_eta','Z_eta',80,-4,4)
        histZPhi= ROOT.TH1F('Z_phi','Z_phi',60,-pi,pi)
        histZMass= ROOT.TH1F('Z_mass','Z_mass',100,0,100)
        histZLp= ROOT.TH1F('Z_Lp','Z_Lp',40,-1.5,2.5)
        histZdPhi= ROOT.TH1F('Z_dPhi','Z_dPhi',30,0,pi)
        histLepPt = ROOT.TH1F('Lep_pt','Lep_pt',25,0,500)
        histNuPt = ROOT.TH1F('nu_pt','nu_pt',25,0,500)
        histLepEta= ROOT.TH1F('Lep_eta','Lep_eta',80,-4,4)
        histNuEta = ROOT.TH1F('nu_eta','nu_eta',80,-4,4)
        histLepPhi= ROOT.TH1F('Lep_phi','Lep_phi',60,-pi,pi)
        histNuPhi = ROOT.TH1F('nu_phi','nu_phi',60,-pi,pi)
        histLepMass= ROOT.TH1F('Lep_mass','Lep_mass',100,0,1)
        histNuMass = ROOT.TH1F('nu_mass','nu_mass',100,0,1)
        histHardPt = ROOT.TH1F('hard_pt','hard_pt',25,0,500)
        histSoftPt = ROOT.TH1F('soft_pt','soft_pt',25,0,500)
        histHardEta= ROOT.TH1F('hard_eta','hard_eta',80,-4,4)
        histSoftEta= ROOT.TH1F('soft_eta','soft_eta',80,-4,4)
        histHardPhi= ROOT.TH1F('hard_phi','hard_phi',60,-pi,pi)
        histSoftPhi= ROOT.TH1F('soft_phi','soft_phi',60,-pi,pi)
        histHardMass= ROOT.TH1F('hard_mass','hard_mass',100,0,1)
        histSoftMass= ROOT.TH1F('soft_mass','soft_mass',100,0,1)
        histWPt= ROOT.TH1F('W_pt','W_pt',25,0,500)
        histWEta= ROOT.TH1F('W_eta','W_eta',80,-4,4)
        histWPhi= ROOT.TH1F('W_phi','W_phi',60,-pi,pi)
        histWMass= ROOT.TH1F('W_mass','W_mass',100,0,100)
        histWLp= ROOT.TH1F('W_Lp','W_Lp',40,-1.5,2.5)
        histWdPhi= ROOT.TH1F('W_dPhi','W_dPhi',30,0,pi)

        for sample in diLepBkg: #Loop over samples
          histos['diLep'][sample['name']] = {}

          diLepNamestr = nameAndCut(None, htb, None, btb=None, presel=diLepPresel, btagVar = 'nBJetMediumCMVA30')[0]
          diLepCut = '('+diLepPresel+'&&'+htCut(htb, minPt=30., maxEta=2.4, njCorr=0.)+')'

          sample["chain"].Draw(">>eList",diLepCut) #Get the event list 'eList' which has all the events satisfying the cut
          elist = ROOT.gDirectory.Get("eList")
          number_events = elist.GetN()
          print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
          
          #Event loop
          for i in range(number_events): #Loop over those events
            if i%10000==0:
              print "At %i of %i for sample %s"%(i,number_events,sample['name'])
    
            sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
            
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

            jets = cmgGetJets(sample['chain'],ptMin=25.)
            leadLep, subLep, Z, Lp, dPhi = getGenZ(sample['chain'])
            minDR = []
            htJet30 = 0.
            for i, j in enumerate(jets):
              leadLepDR = sqrt(deltaPhi(leadLep.Phi(),j['phi'])**2 + (leadLep.Eta()-j['eta'])**2)
              subLepDR = sqrt(deltaPhi(subLep.Phi(),j['phi'])**2 + (subLep.Eta()-j['eta'])**2)
              minDR.append((leadLepDR,subLepDR,j['pt'],j['eta']))
              if (abs(j['eta'])<2.4) and (j['pt']>30.):
                htJet30 += j['pt']
            leadCleanJet = min(minDR,key=lambda x:x[0])
            subCleanJet = min(minDR,key=lambda x:x[1])
            if (leadCleanJet[0]<0.4) and (leadCleanJet[2]>30.) and (abs(leadCleanJet[3])<2.4) and ((htJet30-leadCleanJet[2]) < htb[0]): continue
            if (subCleanJet[1]<0.4) and (subCleanJet[2]>30.) and (abs(subCleanJet[3])<2.4) and ((htJet30-subCleanJet[2]) < htb[0]): continue

            if leadLep.Pt()>subLep.Pt():
              hardZ = leadLep
              softZ = subLep
            elif subLep.Pt()>leadLep.Pt():
              hardZ = subLep
              softZ = leadLep
            histLep1Pt.Fill(leadLep.Pt(),weight)
            histLep2Pt.Fill(subLep.Pt(),weight)
            histLep1Eta.Fill(leadLep.Eta(),weight)
            histLep2Eta.Fill(subLep.Eta(),weight)
            histLep1Phi.Fill(leadLep.Phi(),weight)
            histLep2Phi.Fill(subLep.Phi(),weight)
            histLep1Mass.Fill(leadLep.M(),weight)
            histLep2Mass.Fill(subLep.M(),weight)
            histHardZPt.Fill(hardZ.Pt(),weight)
            histSoftZPt.Fill(softZ.Pt(),weight)
            histHardZEta.Fill(hardZ.Eta(),weight)
            histSoftZEta.Fill(softZ.Eta(),weight)
            histHardZPhi.Fill(hardZ.Phi(),weight)
            histSoftZPhi.Fill(softZ.Phi(),weight)
            histHardZMass.Fill(hardZ.M(),weight)
            histSoftZMass.Fill(softZ.M(),weight)
            histZLp.Fill(Lp,weight)
            histZdPhi.Fill(dPhi,weight)
            histZPt.Fill(Z.Pt(),weight)
            histZEta.Fill(Z.Eta(),weight)
            histZPhi.Fill(Z.Phi(),weight)
            histZMass.Fill(Z.M(),weight)

          del elist
 
        for sample in singleLepBkg: #Loop over samples
  
          singleLepNamestr = nameAndCut(None, htb, None, btb=None, presel=singleLepPresel, btagVar = 'nBJetMediumCMVA30')[0]
          singleLepCut = '('+singleLepPresel+'&&'+htCut(htb, minPt=30., maxEta=2.4, njCorr=0.)+')'

          sample["chain"].Draw(">>eList",singleLepCut) #Get the event list 'eList' which has all the events satisfying the cut
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
                weight = (sampleWeight/sampleLumi)*targetLumi
              else:
                genWeight = sample['chain'].GetLeaf('genWeight').GetValue()
                weight = sample['weight'] * genWeight

            jets = cmgGetJets(sample['chain'],ptMin=25.)
            Lep, Nu, W, Lp, dPhi = getGenW(sample['chain'])
            minDR = []
            htJet30 = 0.
            for i, j in enumerate(jets):
              LepDR = sqrt(deltaPhi(Lep.Phi(),j['phi'])**2 + (Lep.Eta()-j['eta'])**2)
              minDR.append((LepDR,j['pt'],j['eta']))
              if (abs(j['eta'])<2.4) and (j['pt']>30.):
                htJet30 += j['pt']
            cleanJet = min(minDR,key=lambda x:x[0])
            if (cleanJet[0]<0.4) and (cleanJet[1]>30.) and (abs(cleanJet[2])<2.4) and ((htJet30-cleanJet[1]) < htb[0]): continue

            if Lep.Pt()>Nu.Pt():
              hard = Lep
              soft = Nu
            elif Nu.Pt()>Lep.Pt():
              hard = Nu
              soft = Lep
            histLepPt.Fill(Lep.Pt(),weight)
            histNuPt.Fill(Nu.Pt(),weight)
            histLepEta.Fill(Lep.Eta(),weight)
            histNuEta.Fill(Nu.Eta(),weight)
            histLepPhi.Fill(Lep.Phi(),weight)
            histNuPhi.Fill(Nu.Phi(),weight)
            histLepMass.Fill(Lep.M(),weight)
            histNuMass.Fill(Nu.M(),weight)
            histHardPt.Fill(hard.Pt(),weight)
            histSoftPt.Fill(soft.Pt(),weight)
            histHardEta.Fill(hard.Eta(),weight)
            histSoftEta.Fill(soft.Eta(),weight)
            histHardPhi.Fill(hard.Phi(),weight)
            histSoftPhi.Fill(soft.Phi(),weight)
            histHardMass.Fill(hard.M(),weight)
            histSoftMass.Fill(soft.M(),weight)
            histWPt.Fill(W.Pt(),weight)
            histWEta.Fill(W.Eta(),weight)
            histWPhi.Fill(W.Phi(),weight)
            histWMass.Fill(W.M(),weight)
            histWLp.Fill(Lp,weight)
            histWdPhi.Fill(dPhi,weight)

          del elist
         
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

        #plot Lp
        pt1,pt2,leg = getPlot(histZLp,histWLp,l,'Z#rightarrow ll','W+jets','L_{p}','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()
        
        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")
        
        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histZLp,histWLp,'L_{p}','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Lp.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Lp.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Lp.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()
        l.Clear()

        #plot dPhi
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histZdPhi,histWdPhi,l,'Z#rightarrow ll','W+jets','#Delta#Phi','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()
        
        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")
        
        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histZdPhi,histWdPhi,'#Delta#Phi','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_dPhi.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_dPhi.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_dPhi.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()
        l.Clear()

        #plot bosonPt
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histZPt,histWPt,l,'Z#rightarrow ll','W+jets','p_{T}','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histZPt,histWPt,'p_{T}','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Pt.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Pt.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Pt.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()
        l.Clear()

        #plot bosonEta
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histZEta,histWEta,l,'Z#rightarrow ll','W+jets','#eta','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histZEta,histWEta,'#eta','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_eta.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_eta.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_eta.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()
        l.Clear()

        #plot Phi
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histZPhi,histWPhi,l,'Z#rightarrow ll','W+jets','#Phi','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histZPhi,histWPhi,'#Phi','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Phi.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Phi.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Phi.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()
        l.Clear()

        #plot mass
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histZMass,histWMass,l,'Z#rightarrow ll','W+jets','m','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histZMass,histWMass,'m','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Mass.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Mass.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_Mass.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()
        l.Clear()

        #plot pt
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histHardZPt,histHardPt,l,'Z#rightarrow ll (1st)','W+jets (1st)','p_{T}','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histHardZPt,histHardPt,'p_{T}','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stPt.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stPt.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stPt.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()
        l.Clear()

        #plot pt2
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histSoftZPt,histSoftPt,l,'Z#rightarrow ll (2nd)','W+jets (2nd)','p_{T}','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histSoftZPt,histSoftPt,'p_{T}','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndPt.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndPt.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndPt.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()
        l.Clear()

        #plot eta
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histHardZEta,histHardEta,l,'Z#rightarrow ll (1st)','W+jets (1st)','#eta','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histHardZEta,histHardEta,'#eta','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stEta.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stEta.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stEta.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()
        l.Clear()

        #plot eta2
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histSoftZEta,histSoftEta,l,'Z#rightarrow ll (2nd)','W+jets (2nd)','#eta','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histSoftZEta,histSoftEta,'#eta','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndEta.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndEta.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndEta.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()
        l.Clear()

        #plot phi
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histHardZPhi,histHardPhi,l,'Z#rightarrow ll (1st)','W+jets (1st)','#Phi','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histHardZPhi,histHardPhi,'#Phi','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stPhi.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stPhi.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stPhi.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()

        #plot phi2
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histSoftZPhi,histSoftPhi,l,'Z#rightarrow ll (2nd)','W+jets (2nd)','#Phi','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histSoftZPhi,histSoftPhi,'#Phi','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndPhi.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndPhi.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndPhi.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()

        #plot mass
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histHardZMass,histHardMass,l,'Z#rightarrow ll (1st)','W+jets (1st)','m','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histHardZMass,histHardMass,'m','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stMass.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stMass.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_1stMass.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()

        #plot mass2
        canvas.cd()
        pad1 = ROOT.TPad('Pad','Pad',0.,0.3,1.,1.)
        pad1.SetBottomMargin(0.01)
        pad1.SetLogy()
        pad1.Draw()
        pad1.cd()
        pt1,pt2,leg = getPlot(histSoftZMass,histSoftMass,l,'Z#rightarrow ll (2nd)','W+jets (2nd)','m','# of Events')
        pt1.Draw('hist e')
        pt2.Draw('hist same e')
        leg.Draw()

        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

        canvas.cd()
        pad2 = ROOT.TPad("Ratio_pad","Ratio_pad",0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        ratio = getRatioPlot(histSoftZMass,histSoftMass,'m','# of Events')
        ratio.Draw('ep')
        canvas.cd()
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndMass.png')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndMass.root')
        canvas.Print(wwwDir+'ht350_genLevel_Z-Wclosure_2ndMass.pdf')
        del pt1,pt2,leg,ratio
        canvas.Clear()


#        canvas2 = ROOT.TCanvas('normalization','normalization')
#        canvas2.SetLogy()
#        p1 = ROOT.TPad('norm_Pad','norm_Pad',0.,0.,1.,1.)
#        p1.Draw()
#        p1.cd()
#
#        h_ratio['normDiLep'] = histo_diLep.Clone()
#        h_ratio['normDiLep'].Sumw2()
#        h_ratio['normDiLep'].SetMinimum(0.0008)
#        h_ratio['normDiLep'].SetMaximum(0.3)
#        h_ratio['normDiLep'].Scale(1./h_ratio['normDiLep'].Integral())
#        
#        h_ratio['normDiLep'].Draw('hist e')
#        histo_dummy.Draw('hist e same')
#        h_ratio['normDiLep'].GetXaxis().SetTitle('p_{T}(1st)')
#        h_ratio['normDiLep'].GetYaxis().SetTitle('a.u.')
#        l.Draw()
#        text.DrawLatex(0.15,.96,"CMS #bf{#it{Preliminary}}")
#        text.DrawLatex(0.67,0.96,"#bf{L="+str(targetLumi)+" pb^{-1} (13 TeV)}")

#        canvas2.cd()
#        canvas2.Print(wwwDir+namestr+'deltaPhi_NormPlot.root')
#        canvas2.Print(wwwDir+namestr+'deltaPhi_NormPlot.pdf')
#        canvas2.Print(wwwDir+namestr+'deltaPhi_NormPlot.png')
#        canvas2.Clear()

