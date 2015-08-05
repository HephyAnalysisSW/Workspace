import ROOT
import os, sys, copy
import pickle

#ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
#ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import *#getVarValue, getChain, deltaPhi, getYieldFromChain
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *

#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_softLepton import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.eventShape import *

#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&deltaPhi_Wl>1."
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&Flag_EcalDeadCellTriggerPrimitiveFilter"#&&Jet_pt[0]<800"
#presel = "singleMuonic|singleElectronic&&njets>=2"

#def getVarValue(c, var, n=0):         #A general method to get the value of a variable from a chain after chain.GetEntry(i) has been called
#  varNameHisto = var
#  leaf = c.GetAlias(varNameHisto)
#  if leaf!='':
#    return c.GetLeaf(leaf).GetValue(n)
#  else:
#    return c.GetLeaf(var).GetValue(n)

ROOT.TH1F().SetDefaultSumw2()

getW = 'abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)<10'
para = ['pt','phi','pdgId','motherId']

def getMetPt(c):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metPt = c.GetLeaf('met_pt').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  dPhi = c.GetLeaf('deltaPhi_Wl').GetValue()
  x = -metGenPt*cos(metGenPhi)+metPt*cos(metPhi)
  y = -metGenPt*sin(metGenPhi)+metPt*sin(metPhi)
  fakeMet = sqrt(x*x + y*y)
  return metGenPt, fakeMet, dPhi, metPt, metPhi, metGenPhi

def getMetPtOS(c):
  metPhi = getVarValue(c, 'metphi')
  metPt = getVarValue(c, 'met')
  metGenPhi = getVarValue(c, 'genmetphi')
  metGenPt = getVarValue(c, 'genmet')
  lepPhi = getVarValue(c, 'leptonPhi')
  lepPt = getVarValue(c, 'leptonPhi')
  dPhi = acos((lepPt+metPt*cos(lepPhi-metPhi))/sqrt(lepPt**2+metPt**2+2*metPt*lepPt*cos(lepPhi-metPhi)))
  x = -metGenPt*cos(metGenPhi)+metPt*cos(metPhi)
  y = -metGenPt*sin(metGenPhi)+metPt*sin(metPhi)
  fakeMet = sqrt(x*x + y*y)
  return metGenPt, fakeMet, dPhi




def getdPhiMetJet(c):
  jets = cmgGetJets(c,ptMin=30,etaMax=2.4)
  met = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  JetPt = jets[0]['pt']
  JetPhi = jets[0]['phi']
#  dPhi = acos((met*JetPt*cos(metPhi-JetPhi))/(met*JetPt))
  dPhi = abs(cos(JetPhi-metPhi))
  return dPhi

def getZ(c):
  para = ['pt','phi','eta','pdgId','motherId']
  genPartAll = [getObjDict(c, 'genPartAll_', para, j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  Leptons = []
  LeptonsFromZ = []
  ZMass = 0.
  LeptonPt = 0.
  LeptonPhi = 0.
  LeptonEta = 0.
  NeutrinoPt = 0.
  NeutrinoPhi = 0.
  NeutrinoEta = 0.
  for Lepton in filterParticles(genPartAll, [11,13], 'pdgId'):
    Leptons.append(Lepton)
  for LeptonFromZ in filterParticles(Leptons, [23], 'motherId'):
    LeptonsFromZ.append(LeptonFromZ)
  if len(LeptonsFromZ)>1:
    if len(LeptonsFromZ)>2: print 'this should not have happened'
    a = random.randint(0, 1)
    b = abs(1-a)
    LeptonPt = LeptonsFromZ[a]['pt']
    LeptonPhi = LeptonsFromZ[a]['phi']
    LeptonEta = LeptonsFromZ[a]['eta']
    NeutrinoPt =  LeptonsFromZ[b]['pt']
    NeutrinoPhi = LeptonsFromZ[b]['phi']
    NeutrinoEta = LeptonsFromZ[b]['eta']
    ZMass = sqrt(2*LeptonPt*NeutrinoPt*(cosh(LeptonEta-NeutrinoEta)-cos(LeptonPhi-NeutrinoPhi)))
  if ZMass < 1.:
    ZMass = float('nan')
  return LeptonPt, LeptonPhi, NeutrinoPt, NeutrinoPhi, ZMass


varstring="deltaPhi_Wl"
plotDir='/afs/hephy.at/user/d/dspitzbart/www/Spring15/WjetScatterDPhiJetMetCut/'

if not os.path.exists(plotDir):
  os.makedirs(plotDir)


lepSel='hard'
#c = getChain(DY[lepSel],histname='')
c = getChain(WJetsHTToLNu[lepSel],histname='')

## for old samples
#c=ROOT.TChain('Events')
#c.Add('/data/rschoefbeck/data/rschoefbeck/pat_240614/*.root')


stReg=[(250,350)]#,(350,450),(450,-1)]#,(350,450),(450,-1)]
htReg=[(1000,-1)]#,(750,1000),(1000,-1)]#,(1250,-1)]#,(1250,-1)]
jetReg = [(2,3),(4,4),(5,5),(6,7),(8,-1)]#,(8,-1)]#,(6,-1)]#,(8,-1)]#,(6,-1),(8,-1)]
btb = (0,0)

colors = [ROOT.kBlue+2, ROOT.kBlue-4, ROOT.kBlue-7, ROOT.kBlue-9, ROOT.kCyan-9, ROOT.kCyan-6, ROOT.kCyan-2,ROOT.kGreen+3,ROOT.kGreen-2,ROOT.kGreen-6,ROOT.kGreen-7, ROOT.kOrange-4, ROOT.kOrange+1, ROOT.kOrange+8, ROOT.kRed, ROOT.kRed+1]

can1 = ROOT.TCanvas('c1','c1',800,600)
count = {}

for st in stReg:
  count[st] = {}
  print
  print 'Processing ST bin',st
  for ht in htReg:
    count[st][ht] = {}
    #UparaRMSH = ROOT.TH1F('UparaRMSH','UparaRMSH',len(jetReg),0,len(jetReg))
    #UparaMeanH = ROOT.TH1F('UparaMeanH','UparaMeanH',len(jetReg),0,len(jetReg))
    #UperpRMSH = ROOT.TH1F('UperpRMSH','UperpRMSH',len(jetReg),0,len(jetReg))
    #UperpMeanH = ROOT.TH1F('UperpMeanH','UperpMeanH',len(jetReg),0,len(jetReg))
    print 'Processing HT bin',ht
    for i_jet, jet in enumerate(jetReg):
      #UparaHist = ROOT.TH1F('UparaHist','UparaHist',100,-500,500)
      #UperpHist = ROOT.TH1F('UperpHist','UperpHist',100,-500,500)
      #WPhiHist = ROOT.TH1F('WPhiHist','WPhiHist',32,-3.2,3.2)
      #WPtHist = ROOT.TH1F('WPtHist','WPtHist',50,0,500)
      print 'Processing njet',jet
      cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')
      #cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nbtags', stVar='(leptonPt+met)', htVar='ht', njetVar='njets')
      c.Draw('>>eList',cut)
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      totWeight = 0.
      low = 0.
      points = []
      points.append(ROOT.TGraph())
      if st[0]>300:
        points[0].SetPoint(1,750.,750.)
      elif st[0]>400:
        points[ 0].SetPoint(1,1000.,1000.)
      else:
        points[0].SetPoint(1,500.,500.)
      points[0].GetXaxis().SetTitle('E_{T miss,fake}')
      points[0].GetYaxis().SetTitle('E_{T miss,gen}')
      points[0].SetMarkerSize(0)
      points[0].Draw('ap')
      print 'run, lumi, evt, fakeMet, genMet, genMetPhi, recoMet, recoMetPhi, leptonPt, leptonPhi, leptonEta, st, deltaPhi'
      for i in range(number_events):
        c.GetEntry(elist.GetEntry(i))
        weight=getVarValue(c,"weight")
        run=getVarValue(c,"run")
        lumi=getVarValue(c,"lumi")
        evt=getVarValue(c,"evt")
        leptonPt = getVarValue(c,"leptonPt")
        leptonPhi = getVarValue(c,"leptonPhi")
        leptonEta = getVarValue(c,"leptonEta")
        stValue = getVarValue(c,"st")
        #dPhiJetMet = getdPhiMetJet(c)
        dPhiJetMet = cmgMinDPhiJet(c, nJets=2)
        #dPhi = getVarValue(c,"deltaPhi_Wl")
        #totWeight += weight
        met, fakeMet, dPhi, metPt, metPhi, metGenPhi = getMetPt(c)
        #points.append(ROOT.TGraph())
        #print dPhi
        if met > 0.:
          points.append(ROOT.TGraph())
          if dPhi>1. and dPhiJetMet>0.45:# and dPhiJetMet<0.9:
            totWeight += weight
            if fakeMet/met>1.:# and fakeMet<50.:
              low+=weight
              #if dPhiJetMet<0.9:
              print int(run), int(lumi), int(evt), fakeMet, met, metGenPhi, metPt, metPhi, leptonPt, leptonPhi, leptonEta, stValue, dPhi
            points[-1].SetPoint(0,fakeMet,met)
            points[-1].SetMarkerStyle(8)
            #pointSize = 0.2+weight*15
            pointSize=0.5
            points[-1].SetMarkerSize(pointSize)
            for a in range(0,16):
              if dPhi*5<a:
                points[-1].SetMarkerColor(colors[a])
                break
            points[-1].Draw('p same')
      #UparaHist.Draw('e hist')
      #UparaHist.Fit('gaus','','same')
      #FitFunc = UparaHist.GetFunction('gaus')
      #FitFunc.Draw('same')
      can1.Print(plotDir+'scatter_'+cutname+'.png')
      can1.Print(plotDir+'scatter_'+cutname+'.root')
      #can1.Print(plotDir+'scatterDeltaPhiG1_'+cutname+'.png')
      #can1.Print(plotDir+'scatterDeltaPhiG1_'+cutname+'.root')
      if totWeight>0:
        frac = 1.*low/totWeight
      else:
        frac = 1.
      count[st][ht][jet] = {'rightLow':low,'total':totWeight, 'fraction':frac}
      print 'right low', low, 'total', totWeight, 'fraction', frac

leg = []
leg.append(ROOT.TGraph())
leg[0].SetPoint(1,10.,15.)
leg[0].Draw('ap')
for a in range(0,16):
  leg.append(ROOT.TGraph())
  leg[-1].SetMarkerColor(colors[a])
  leg[-1].SetMarkerStyle(8)
  leg[-1].SetMarkerSize(4)
  leg[-1].SetPoint(0,10.,a)
  leg[-1].Draw('p same')

can1.Print(plotDir+'colorLegend.png')
can1.Print(plotDir+'colorLegend.root')
