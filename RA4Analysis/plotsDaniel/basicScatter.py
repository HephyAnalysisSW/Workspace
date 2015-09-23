import ROOT
import os, sys, copy
import pickle

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *

from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.eventShape import *

#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&deltaPhi_Wl>1."
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"#&&Flag_EcalDeadCellTriggerPrimitiveFilter"#&&Jet_pt[0]<800"
#presel = "singleMuonic|singleElectronic&&njets>=2"

ROOT.TH1F().SetDefaultSumw2()

path25ns = '/data/easilar/cmgTuples/crab/Summer15_25nsV2MC_Data/'

SingleElectron_Run2015C = {'name':'SingleElectron_Run2015C-PromptReco-v1', 'dir':path25ns+'SingleElectron_Run2015C/'}
SingleMuon_Run2015C = {'name':'SingleMuon_Run2015C-PromptReco-v1', 'dir':path25ns+'SingleMuon_Run2015C/'}

samples25ns = [SingleElectron_Run2015C,SingleMuon_Run2015C]

path50ns = '/data/easilar/cmgTuples/crab_Spring15/Summer15_50nsV4_Data/'

SingleElectron_Run2015B = {'name':'cmgTuples_SingleElectron_Run2015B-PromptReco-v1_Summer15_50nsV4', 'dir':path50ns+'SingleElectron_Run2015B-PromptReco-v1/'}
SingleMuon_Run2015B = {'name':'cmgTuples_SingleMuon_Run2015B-PromptReco-v1_Summer15_50nsV4', 'dir':path50ns+'SingleMuon_Run2015B-PromptReco-v1/'}

samples50ns = [SingleElectron_Run2015B,SingleMuon_Run2015B]

dataSamples = samples25ns
for s in dataSamples:
  s['chunkString'] = s['name']
  s.update({ 
    "rootFileLocation":"tree.root",
    "skimAnalyzerDir":"",
    "treeName":"tree",
    'isData':True,
    #'dir' : data_path
  })

samples = []
for sample in dataSamples:
  samples.append({'name':sample['name'],'sample':sample})

data = ROOT.TChain('tree')
for sample in samples:
  sample['chunks'], sample['nEvents'] = getChunks(sample['sample'])
  for chunk in sample['chunks']:
    data.Add(chunk['file'])

ele_MVAID_cuts_tight={'eta08':0.73 , 'eta104':0.57,'eta204': 0.05}
ele_MVAID_cutstr_tight= "((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_tight['eta08'])+")"\
                       +"||((abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.44)&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_tight['eta104'])+")"\
                       +"||((abs(LepGood_eta)>=1.57)&&LepGood_mvaIdPhys14>"+str(ele_MVAID_cuts_tight['eta204'])+"))"

singleMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)==1)'
#singleMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4)==1)'
singleElectronic = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0)==1)"
#singleElectronic = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4)==1)"
htStr = 'Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))'
electronId = "(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0)"
stStr = 'Sum$((LepGood_pt+metNoHF_pt)*'+electronId+')'


presel = singleElectronic+'&&nJet30>1&&nBJetMedium30>=0&&'+htStr+'>500&&'+stStr+'>250'
#presel = singleElectronic+'&&nJet30>1&&nBJetMedium30>=0&&'+htStr+'>500&&'+stStr+'>250'
#presel = singleMuonic+'&&nJet30>1&&nBJetMedium30==0&&'+htStr+'>500&&'+stStr+'>250'


getW = 'abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)<10'
para = ['pt','phi','pdgId','motherId']

def getDeltaPhi(c):
  metPhi = getVarValue(c, 'metNoHF_phi')
  metPt = getVarValue(c, 'metNoHF_pt')
  lepPhi = getVarValue(c, 'LepGood_phi')
  lepPt = getVarValue(c, 'LepGood_pt')
  dPhi = acos((lepPt+metPt*cos(lepPhi-metPhi))/sqrt(lepPt**2+metPt**2+2*metPt*lepPt*cos(lepPhi-metPhi)))
  return dPhi

def getdPhiMetJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  met = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  JetPt = jets[0]['pt']
  JetPhi = jets[0]['phi']
  dPhi = abs(cos(JetPhi-metPhi))
  return dPhi

varstring="deltaPhi_Wl"
plotDir='/afs/hephy.at/user/d/dspitzbart/www/data/25ns/METvsLep/'

if not os.path.exists(plotDir):
  os.makedirs(plotDir)


lepSel='hard'
#c = getChain(DY[lepSel],histname='')
#c = getChain(WJetsHTToLNuLow[lepSel],histname='')
#c = getChain(WJetsHTToLNu[lepSel],histname='')
c = data

## for old samples
#c=ROOT.TChain('Events')
#c.Add('/data/rschoefbeck/data/rschoefbeck/pat_240614/*.root')


stReg=[(250,-1)]#,(350,450),(450,-1)]#,(350,450),(450,-1)]
htReg=[(500,-1)]#,(1000,-1)]#,(1250,-1)]#,(1250,-1)]
jetReg = [(2,-1)]#,(3,3),(4,4),(5,5),(6,7),(8,-1)]#,(8,-1)]#,(6,-1)]#,(8,-1)]#,(6,-1),(8,-1)]
btb = (0,-1)

colors = [ROOT.kBlue+2, ROOT.kBlue-4, ROOT.kBlue-7, ROOT.kBlue-9, ROOT.kCyan-9, ROOT.kCyan-6, ROOT.kCyan-2,ROOT.kGreen+3,ROOT.kGreen-2,ROOT.kGreen-6,ROOT.kGreen-7, ROOT.kOrange-4, ROOT.kOrange+1, ROOT.kOrange+8, ROOT.kRed, ROOT.kRed+1]

can1 = ROOT.TCanvas('c1','c1',800,700)
count = {}

for st in stReg:
  count[st] = {}
  print
  print 'Processing ST bin',st
  for ht in htReg:
    count[st][ht] = {}
    print 'Processing HT bin',ht
    for i_jet, jet in enumerate(jetReg):
      print 'Processing njet',jet
      cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')
      #cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nbtags', stVar='(leptonPt+met)', htVar='ht', njetVar='njets')
      c.Draw('>>eList',presel)
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      totWeight = 0.
      maxX = 3.5
      maxY = 3.5
      helper = ROOT.TGraph()
      helper.SetMarkerSize(0.)
      helper.SetMarkerStyle(1)
      helper.SetPoint(1,maxX,maxY)
      helper.Draw('ap')
      helper.GetXaxis().SetTitle('E_{T}^{miss}')
      helper.GetYaxis().SetTitle('p_{T} lep.')
      #helper.GetXaxis().SetRangeUser(0.,4.)
      #helper.GetYaxis().SetRangeUser(0.,4.)
      
      points = ROOT.TGraph()
      #points.SetPoint(0,0.,0.)
      points.SetMarkerSize(0.8)
      points.SetMarkerStyle(20)
      points.SetMarkerColor(ROOT.kOrange+1)
      #points.Draw('ap')
      for i in range(number_events):
        c.GetEntry(elist.GetEntry(i))
        #weight=getVarValue(c,"weight")
        run=getVarValue(c,"run")
        lumi=getVarValue(c,"lumi")
        evt=getVarValue(c,"evt")
        metPt = getVarValue(c,"metNoHF_pt")
        #leptonPt = getVarValue(c,"LepGood_pt")
        #leptonPt = getVarValue(c,"leptonPt")
        #leptonPhi = getVarValue(c,"leptonPhi")
        #leptonEta = getVarValue(c,"leptonEta")
        jets = cmgGetJets(c, ptMin=30., etaMax=2.4)
        lep = getObjDict(c, 'LepGood_', ['pt','phi','eta'], 0)
        leptonPt = lep['pt']
        deltaR = findClosestObject(jets, lep, sortFunc=lambda o1, o2: deltaR2(o1,o2))
        deltaPhi = getDeltaPhi(c)
        #stValue = getVarValue(c,"st")
        points.SetPoint(i,sqrt(deltaR['distance']),deltaPhi)
        #points.SetPoint(i,metPt,leptonPt)
        #print leptonPt+metPt
      #points.Draw('ap')
      #points.GetXaxis().SetTitle('min #DeltaR(j,l)')
      #points.GetYaxis().SetTitle('#Delta#Phi (W,l)')
      #points.SetMinimum(0.)
      #points.SetMinimum(4.)
      #points.GetXaxis().SetRangeUser(0.,4.)
      #points.GetYaxis().SetRangeUser(0.,4.)
      points.Draw('p same')
      #can1.Update()
      can1.Print(plotDir+'scatter_tighterSel_'+cutname+'.png')
      can1.Print(plotDir+'scatter_tighterSel_'+cutname+'.root')
      can1.Print(plotDir+'scatter_tighterSel_'+cutname+'.pdf')

#leg = []
#leg.append(ROOT.TGraph())
#leg[0].SetPoint(1,10.,15.)
#leg[0].Draw('ap')
#for a in range(0,16):
#  leg.append(ROOT.TGraph())
#  leg[-1].SetMarkerColor(colors[a])
#  leg[-1].SetMarkerStyle(8)
#  leg[-1].SetMarkerSize(4)
#  leg[-1].SetPoint(0,10.,a)
#  leg[-1].Draw('p same')
#
#can1.Print(plotDir+'colorLegend.png')
#can1.Print(plotDir+'colorLegend.root')
