import ROOT
import os, sys, copy
import pickle
from random import randint

#ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
#ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import *#getVarValue, getChain, deltaPhi, getYieldFromChain
from Workspace.HEPHYPythonTools.xsec import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.cmgTuples_v1_PHYS14V3 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_softLepton import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.eventShape import *
from draw_helpers import *
from localInfo import username

#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"
diMuonic = "(Sum$(genLep_pt>20&&abs(genLep_pdgId)==13&&abs(genLep_motherId)==23)==2)"
#muVeto = looseLeptonVeto('muon', minPt=10)
presel = diMuonic

ROOT.TH1F().SetDefaultSumw2()
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(2211)

getW = 'abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)<10'
para = ['pt','phi','pdgId','motherId']

def getMetXY(c):
  metPt = c.GetLeaf('met_pt').GetValue() 
  metPhi = c.GetLeaf('met_phi').GetValue()
  metX = metPt*cos(metPhi)
  metY = metPt*sin(metPhi)
  return metX, metY

def getDeltaPhiMetGenMet(c):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  return deltaPhiNA(metPhi,metGenPhi)

def getW(c):
  genPartAll = [getObjDict(c, 'genPartAll_', para, j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  W = filter(lambda w:abs(w['pdgId'])==24, genPartAll)
  WfromQ = filter(lambda w:abs(w['motherId'])<10, W)
  if len(WfromQ)>0:
    if len(WfromQ)>1: print 'this should not have happened'
    WPt = WfromQ[0]['pt']
    WPhi = WfromQ[0]['phi']
    return WPt, WPhi
  else: 
#    print len(WfromQ)
#    print 'W pt and phi taken as 0!'
    return float('nan'), float('nan')

def getGenZ(c):
  leadLepPt = c.GetLeaf('genLep_pt').GetValue(0)
  leadLepPhi = c.GetLeaf('genLep_phi').GetValue(0)
  leadLepEta = c.GetLeaf('genLep_eta').GetValue(0)
  subLepPt = c.GetLeaf('genLep_pt').GetValue(1)
  subLepPhi = c.GetLeaf('genLep_phi').GetValue(1)
  subLepEta = c.GetLeaf('genLep_eta').GetValue(1)
  x = leadLepPt*cos(leadLepPhi)+subLepPt*cos(subLepPhi)  
  y = leadLepPt*sin(leadLepPhi)+subLepPt*sin(subLepPhi)  
  invMass = sqrt(2.*leadLepPt*subLepPt*(cosh(leadLepEta-subLepEta)-cos(leadLepPhi-subLepPhi)))
  ZPt = sqrt(x*x + y*y)
  ZPhi = atan(y/x)
  if x<0:
    if y>0:
      ZPhi = pi + ZPhi
    if y<0:
      ZPhi = ZPhi - pi
  return ZPt, ZPhi, invMass, x, y, leadLepPt, leadLepPhi, subLepPt, subLepPhi  

def getRecoW(c):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metPt = c.GetLeaf('met_pt').GetValue()
  lepPt = c.GetLeaf('leptonPt').GetValue()
  lepPhi = c.GetLeaf('leptonPhi').GetValue()
  Wx = lepPt*cos(lepPhi)+metPt*cos(metPhi)
  Wy = lepPt*sin(lepPhi)+metPt*sin(metPhi)
  WPhi = atan(Wy/Wx)
  if Wx<0:
    if Wy>0:
      WPhi = pi + WPhi
    if Wy<0:
      WPhi = WPhi - pi
  WPt = sqrt(Wx**2+Wy**2)
  return WPt, WPhi

def getUv2(c, WPt, WPhi):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metPt = c.GetLeaf('met_pt').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  lepPt = c.GetLeaf('leptonPt').GetValue()
  lepPhi = c.GetLeaf('leptonPhi').GetValue()
  x = lepPt*cos(lepPhi)+metPt*cos(metPhi)
  y = lepPt*sin(lepPhi)+metPt*sin(metPhi)
  Upara = x*cos(WPhi)+y*sin(WPhi)
  Uperp = x*sin(WPhi)-y*cos(WPhi)
  return Upara, Uperp

def getU2(c, WPt, WPhi):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metPt = c.GetLeaf('met_pt').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  x = -metGenPt*cos(metGenPhi)+metPt*cos(metPhi)
  y = -metGenPt*sin(metGenPhi)+metPt*sin(metPhi)
  Upara = x*cos(WPhi)+y*sin(WPhi)
  Uperp = x*sin(WPhi)-y*cos(WPhi)
  fakeMet = sqrt(x*x + y*y)
  return Upara, Uperp, fakeMet


def getU(c, WPt, WPhi):
  #jets = cmgGetJets(c, ptMin=0., etaMax=999.)
  metPhi = c.GetLeaf('met_phi').GetValue()
  metPt = c.GetLeaf('met_pt').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  #genPartAll = [getObjDict(c, 'genPartAll_', para, j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  #W = filter(lambda w:abs(w['pdgId'])==24, genPartAll)
  #WfromQ = filter(lambda w:abs(w['motherId'])<10, W)
  #WPhi filter(lambda e:abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)<10, genPartAll)
  #WPt = c.GetLeaf('genPartAll_pt').GetValue()
  #WPhi = c.GetLeaf('genPartAll_phi').GetValue()
  #WPt = WfromQ[0]['pt']
  #WPhi = WfromQ[0]['phi']
  #print WPt, WPhi
  x = WPt*cos(WPhi)+metPt*cos(metPhi)-metGenPt*cos(metGenPhi)
  y = WPt*sin(WPhi)+metPt*sin(metPhi)-metGenPt*sin(metGenPhi)
  #for jet in jets:
  #  x += jet['pt']*cos(jet['phi'])
  #  y += jet['pt']*sin(jet['phi'])
  Upara = x*cos(WPhi)+y*sin(WPhi)
  Uperp = x*sin(WPhi)-y*cos(WPhi)
  return Upara, Uperp

def projectFakeMetToW(c):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metPt = c.GetLeaf('met_pt').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  WPt = c.GetLeaf('genPartAll_pt').GetValue()
  WPhi = c.GetLeaf('genPartAll_phi').GetValue()
  return (metPt*cos(metPhi)-metGenPt*cos(metGenPhi))*cos(WPhi)+(metPt*sin(metPhi)-metGenPt*sin(metGenPhi))*sin(WPhi)

def projectFakeMetToGenMet(c):
  metPhi = c.GetLeaf('met_phi').GetValue()
  metPt = c.GetLeaf('met_pt').GetValue()
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  return (metPt*cos(metPhi)-metGenPt*cos(metGenPhi))*cos(metGenPhi)+(metPt*sin(metPhi)-metGenPt*sin(metGenPhi))*sin(metGenPhi)

def getDeltaPhiJet(c):
  leadingNJets = cmgGetJets(c, ptMin=30., etaMax=999.)[:2]
  return deltaPhi(leadingNJets[0]['phi'],leadingNJets[1]['phi'])

def getWPtAndPhi(c):
  WPt = c.GetLeaf('genPartAll_pt').GetValue()
  WPhi = c.GetLeaf('genPartAll_phi').GetValue()
  return WPt, WPhi

target_lumi = 3000 #pb-1
def getWeight(sample,nEvents,target_lumi):
  weight = xsec[sample['dbsName']] * target_lumi/nEvents
  return weight

varstring="deltaPhi_Wl"
plotDir='/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCMG2/hard/Phys14V3/MetPerformanceZmumu_mimicMuToNu/'
#pickleDir='/data/dhandl/results2015/metStudyZmumu/'
prefix = ''

if not os.path.exists(plotDir):
  os.makedirs(plotDir)
#if not os.path.exists(pickleDir):
#  os.makedirs(pickleDir)


lepSel='hard'
#WJETS = getChain(WJetsHTToLNu[lepSel],histname='')
#cDY = getChain(DY[lepSel],histname='')
Bkg = [{'name':'DYJetsToLL_M50_HT100to200_PU20bx25', 'sample':DYJetsToLL_M50_HT100to200_PU20bx25, 'legendName':'DY HT100-200'},
       {'name':'DYJetsToLL_M50_HT200to400_PU20bx25', 'sample':DYJetsToLL_M50_HT200to400_PU20bx25, 'legendName':'DY HT200-400'},
       {'name':'DYJetsToLL_M50_HT400to600_PU20bx25', 'sample':DYJetsToLL_M50_HT400to600_PU20bx25, 'legendName':'DY HT400-600'},
       {'name':'DYJetsToLL_M50_HT600toInf_PU20bx25', 'sample':DYJetsToLL_M50_HT600toInf_PU20bx25, 'legendName':'DY HT600-Inf'}]

small = False
maxN=1 if small else -1

for sample in Bkg:
  sample['chunks'], sample['nEvents'] = getChunks(sample['sample'],treeName='treeProducerSusySingleLepton', maxN=maxN)
  sample['chain'] = ROOT.TChain('tree')
  for chunk in sample['chunks']:
    sample['chain'].Add(chunk['file'])
  sample['weight'] = getWeight(sample['sample'], sample['nEvents'], target_lumi)

stReg=[(250,350),(350,450),(450,-1)]#,(350,450),(450,-1)]
htReg=[(500,750),(750,1000),(1000,-1)]#,(750,1000),(1000,-1)]#,(1250,-1)]#,(1250,-1)]
jetReg = [(2,3),(4,4),(5,5),(6,7),(8,-1)]#,(8,-1)]#,(6,-1)]#,(8,-1)]#,(6,-1),(8,-1)]
btb = (0,0)

can1 = ROOT.TCanvas('c1','c1',800,600)

#hist = ROOT.TH1F('hist','hist',len(jetReg),0,len(jetReg))
#hist.Sumw2()

## Simple event loop
#for st in stReg:
#  print
#  print 'Processing ST bin',st
#  for ht in htReg:
#    print 'Processing HT bin',ht
#    for i_jet, jet in enumerate(jetReg):
#      metHist = ROOT.TH1F('metHist','metHist',50,0,500)
#      print 'Processing njet',jet
#      cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')
#      RMSself = 0.
#      totalWeight = 0.
#      WJETS.Draw('>>eList',cut)
#      elist = ROOT.gDirectory.Get("eList")
#      number_events = elist.GetN()
#      for i in range(number_events):
#        WJETS.GetEntry(elist.GetEntry(i))
#        #WPhi = getVarValue(WJETS,"genPartAll_phi")
#        weight=getVarValue(WJETS,"weight")
#        #WPt = getVarValue(WJETS,"genPartAll_pt")
#        #fakeMetOnW = projectFakeMetToGenMet(WJETS)
#        WPt, WPhi = getW(WJETS)
#        #print WPhi
#        if WPt>0.:
#          metHist.Fill(WPt,weight)
#      metHist.Draw()
#      can1.Print('/afs/hephy.at/user/d/dspitzbart/www/WjetKin/WPt'+cutname+'.png')
#      del metHist

## project onto W direction
#for st in stReg:
#  print
#  print 'Processing ST bin',st
#  for ht in htReg:
#    hist = ROOT.TH1F('hist','hist',len(jetReg),0,len(jetReg))
#    hist.Sumw2()
#    print 'Processing HT bin',ht
#    for i_jet, jet in enumerate(jetReg):
#      dPhiHist = ROOT.TH1F('dPhiHist','dPhiHist',64,-3.2,3.2)
#      dPhiHist.Sumw2()
#      print 'Processing njet',jet
#      cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')
#      RMSself = 0.
#      totalWeight = 0.
#      WJETS.Draw('>>eList','weight*('+cut+')')
#      elist = ROOT.gDirectory.Get("eList")
#      number_events = elist.GetN()
#      for i in range(number_events):
#        WJETS.GetEntry(elist.GetEntry(i))
#        weight=getVarValue(WJETS,"weight")
#        varvalue = getDeltaPhiMetGenMet(WJETS)
#        dPhiHist.Fill(varvalue,weight)
#        #RMSself += varvalue**2*weight
#        totalWeight += weight
#      dPhiHist.Draw()
#      RMS = dPhiHist.GetRMS()
#      #print RMS
#      dPhiHist.Fit('gaus','','same')
#      FitFunc = dPhiHist.GetFunction('gaus')
#      FitFunc.Draw('same')
#      can1.Print('/afs/hephy.at/user/d/dspitzbart/www/WjetKin/metDPhi'+cutname+'.png')
#      #RMSself = sqrt(RMSself/totalWeight)
#      #print RMSself
#      hist.SetBinContent(i_jet+1,RMS)
#      hist.SetBinError(i_jet+1,dPhiHist.GetRMSError())
#      hist.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))
#      del dPhiHist
#    hist.GetXaxis().SetTitle('jet multiplicity')
#    hist.GetYaxis().SetTitle('RMS')
#    hist.SetMaximum(1.5)
#    hist.SetMinimum(0.)
#    hist.SetMarkerSize(0)
#    hist.SetLineColor(ROOT.kAzure)
#    hist.SetLineWidth(2)
#    hist.Fit('pol1','','same')
#    FitFunc     = hist.GetFunction('pol1')
#    FitParD     = FitFunc.GetParameter(0)
#    FitParDError = FitFunc.GetParError(0)
#    FitParK = FitFunc.GetParameter(1)
#    FitParKError = FitFunc.GetParError(1)
#    FitFunc.SetLineColor(ROOT.kOrange+10)
#    FitFunc.SetLineStyle(2)
#    FitFunc.SetLineWidth(2)
#    
#    hist.Draw('e hist')
#    FitFunc.Draw('same')
#    can1.Print('/afs/hephy.at/user/d/dspitzbart/www/WjetKin/metRMS'+cutname+'.png')
#    del hist

#bins={}
## upara
#for st in stReg:
#  bins[st] = {}
#  print 'Processing ST bin',st
#  for ht in htReg:
#    bins[st][ht] = {}
#    UparaRMSH = ROOT.TH1F('UparaRMSH','UparaRMSH',len(jetReg),0,len(jetReg))
#    UparaMeanH = ROOT.TH1F('UparaMeanH','UparaMeanH',len(jetReg),0,len(jetReg))
#    UperpRMSH = ROOT.TH1F('UperpRMSH','UperpRMSH',len(jetReg),0,len(jetReg))
#    UperpMeanH = ROOT.TH1F('UperpMeanH','UperpMeanH',len(jetReg),0,len(jetReg))
#    print 'Processing HT bin',ht
#    for i_jet, jet in enumerate(jetReg):
#      bins[st][ht][jet] = {}
#      UparaHist = ROOT.TH1F('UparaHist','UparaHist',100,-500,500)
#      UperpHist = ROOT.TH1F('UperpHist','UperpHist',100,-500,500)
#      WPhiHist = ROOT.TH1F('WPhiHist','WPhiHist',32,-3.2,3.2)
#      WPtHist = ROOT.TH1F('WPtHist','WPtHist',50,0,500)
#      fakeMetHist = ROOT.TH1F('fakeMetHist','fakeMetHist',50,0,500)
#      RecoGenFracHist = ROOT.TH1F('RecoGenFracHist','RecogenFracHist',60,0,3)
#      UperpVSUpara = ROOT.TH2F('UperpVSUpara','UperpVSUpara',100,-500,500,100,-500,500)
#      genMetVSfakeMet = ROOT.TH2F('genMetVSfakeMet','genMetVSfakeMet',50,0,500,50,0,500)
##      UparaVSgenW = ROOT.TH2F('UparaVSgenW','UparaVSgenW',100,-500,500,100,-500,500)
##      UperpVSgenW = ROOT.TH2F('UperpVSgenW','UperpVSgenW',100,-500,500,100,-500,500)
#      print 'Processing njet',jet
#      cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')
#      WJETS.Draw('>>eList',cut)
#      elist = ROOT.gDirectory.Get("eList")
#      number_events = elist.GetN()
#      for i in range(number_events):
#        if i%10000==0:
#          print "At %i of %i in Wjets "%(i,number_events)
#        WJETS.GetEntry(elist.GetEntry(i))
#        weight=getVarValue(WJETS,"weight")
#        WPt, WPhi = getRecoW(WJETS)
#        if WPt>0:
#          WPtHist.Fill(WPt,weight)
#          WPhiHist.Fill(WPhi,weight)
#          Upara, Uperp, fakeMet = getU2(WJETS, WPt, WPhi)
#          UparaHist.Fill(Upara,weight)
#          UperpHist.Fill(Uperp,weight)
#          fakeMetHist.Fill(fakeMet,weight)
#          UperpVSUpara.Fill(Upara,Uperp,weight)
#          genMet = WJETS.GetLeaf('met_genPt').GetValue()
#          recoMet = WJETS.GetLeaf('met_pt').GetValue()
#          RecoGenFrac = recoMet/genMet
#          RecoGenFracHist.Fill(RecoGenFrac,weight)
#          genMetVSfakeMet.Fill(fakeMet,genMet,weight)
##          UparaVSgenW.Fill(WPt,Upara,weight)
##          UperpVSgenW.Fill(WPt,Uperp,weight)
#      UparaHist.Draw('e hist')
#      UparaHist.Fit('gaus','','same')
#      FitFunc = UparaHist.GetFunction('gaus')
#      FitFunc.Draw('same')
#      can1.Print(plotDir+prefix+'Upara_'+cutname+'.png')
#      can1.Print(plotDir+prefix+'Upara_'+cutname+'.root')
#      
#      UperpHist.Draw('e hist')
#      UperpHist.Fit('gaus','','same')
#      FitFunc = UperpHist.GetFunction('gaus')
#      FitFunc.Draw('same')
#      can1.Print(plotDir+prefix+'Uperp_'+cutname+'.png')
#      can1.Print(plotDir+prefix+'Uperp_'+cutname+'.root')
#      
#      UparaRMS = UparaHist.GetRMS()
#      UparaMean = UparaHist.GetMean()
#      UperpRMS = UperpHist.GetRMS()
#      UperpMean = UperpHist.GetMean()
#      bins[st][ht][jet].update({'UparaRMS':UparaRMS, 'UparaRMS_error':UparaHist.GetRMSError(), 'UparaMean':UparaMean, 'UparaMean_error':UparaHist.GetMeanError(),\
#                                'UperpRMS':UperpRMS, 'UperpRMS_error':UperpHist.GetRMSError(), 'UperpMean':UperpMean, 'UperpMean_error':UperpHist.GetMeanError()})
#      WPtHist.Draw('hist')
#      can1.Print(plotDir+prefix+'WPt_'+cutname+'.png')
#      can1.Print(plotDir+prefix+'WPt_'+cutname+'.root')
#      WPhiHist.Draw('hist')
#      can1.Print(plotDir+prefix+'WPhi_'+cutname+'.png')
#      can1.Print(plotDir+prefix+'WPhi_'+cutname+'.root')
#      fakeMetHist.Draw('hist')
#      can1.Print(plotDir+prefix+'fakeMet_'+cutname+'.png')
#      can1.Print(plotDir+prefix+'fakeMet_'+cutname+'.root')
#      RecoGenFracHist.Draw('hist')
#      can1.Print(plotDir+prefix+'RecoGenFrac_'+cutname+'.png')
#      can1.Print(plotDir+prefix+'RecoGenFrac_'+cutname+'.root')
#      UperpVSUpara.Draw('colz')
#      can1.SetLogz()
#      can1.Print(plotDir+prefix+'UperpVSUpara_'+cutname+'.png')
#      can1.Print(plotDir+prefix+'UperpVSUpara_'+cutname+'.root')
#      genMetVSfakeMet.Draw('colz')
#      can1.SetLogz()
#      can1.Print(plotDir+prefix+'genMetVSfakeMet_'+cutname+'.png')
#      can1.Print(plotDir+prefix+'genMetVSfakeMet_'+cutname+'.root')
##      UparaVSgenW.Draw('colz')
##      can1.Print(plotDir+'UparaVSgenW_'+cutname+'.png')
##      can1.Print(plotDir+'UparaVSgenW_'+cutname+'.root')
##      UperpVSgenW.Draw('colz')
##      can1.Print(plotDir+'UperpVSgenW_'+cutname+'.png')
##      can1.Print(plotDir+'UperpVSgenW_'+cutname+'.root')
#      UparaRMSH.SetBinContent(i_jet+1,UparaRMS)
#      UparaRMSH.SetBinError(i_jet+1,UparaHist.GetRMSError())
#      UparaRMSH.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))
#      UparaMeanH.SetBinContent(i_jet+1,UparaMean)
#      UparaMeanH.SetBinError(i_jet+1,UparaHist.GetMeanError())
#      UparaMeanH.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))
#      UperpRMSH.SetBinContent(i_jet+1,UperpRMS)
#      UperpRMSH.SetBinError(i_jet+1,UperpHist.GetRMSError())
#      UperpRMSH.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))
#      UperpMeanH.SetBinContent(i_jet+1,UperpMean)
#      UperpMeanH.SetBinError(i_jet+1,UperpHist.GetMeanError())
#      UperpMeanH.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))
#      del UparaHist,UperpHist,WPhiHist,WPtHist
#
#    UparaRMSH.GetXaxis().SetTitle('jet multiplicity')
#    UparaRMSH.GetYaxis().SetTitle('UparaRMS')
#    UparaRMSH.SetMaximum(80)
#    UparaRMSH.SetMinimum(0.)
#    UparaRMSH.SetMarkerSize(0)
#    UparaRMSH.SetLineColor(ROOT.kAzure)
#    UparaRMSH.SetLineWidth(2)
#    UparaRMSH.Fit('pol1','','same')
#    FitFunc     = UparaRMSH.GetFunction('pol1')
#    FitParD     = FitFunc.GetParameter(0)
#    FitParDError = FitFunc.GetParError(0)
#    FitParK = FitFunc.GetParameter(1)
#    FitParKError = FitFunc.GetParError(1)
#    FitFunc.SetLineColor(ROOT.kOrange+10)
#    FitFunc.SetLineStyle(2)
#    FitFunc.SetLineWidth(2)    
#    UparaRMSH.Draw('e hist')
#    FitFunc.Draw('same')
#    can1.Print(plotDir+prefix+'UparaRMS_'+cutname+'.png')
#    can1.Print(plotDir+prefix+'UparaRMS_'+cutname+'.root')
#    bins[st][ht].update({'UparaRMS_fitD':FitParD, 'UparaRMS_fitDerror':FitParDError, 'UparaRMS_fitK':FitParK, 'UparaRMS_fitKerror':FitParKError})
#    
#    UparaMeanH.GetXaxis().SetTitle('jet multiplicity')
#    UparaMeanH.GetYaxis().SetTitle('UparaMean')
#    UparaMeanH.SetMaximum(100.)
#    UparaMeanH.SetMinimum(-100.)
#    UparaMeanH.SetMarkerSize(0)
#    UparaMeanH.SetLineColor(ROOT.kAzure)
#    UparaMeanH.SetLineWidth(2)
#    UparaMeanH.Fit('pol1','','same')
#    FitFunc     = UparaMeanH.GetFunction('pol1')
#    FitParD     = FitFunc.GetParameter(0)
#    FitParDError = FitFunc.GetParError(0)
#    FitParK = FitFunc.GetParameter(1)
#    FitParKError = FitFunc.GetParError(1)
#    FitFunc.SetLineColor(ROOT.kOrange+10)
#    FitFunc.SetLineStyle(2)
#    FitFunc.SetLineWidth(2)
#    UparaMeanH.Draw('e hist')
#    FitFunc.Draw('same')
#    can1.Print(plotDir+prefix+'UparaMean_'+cutname+'.png')
#    can1.Print(plotDir+prefix+'UparaMean_'+cutname+'.root')
#    bins[st][ht].update({'UparaMean_fitD':FitParD, 'UparaMean_fitDerror':FitParDError, 'UparaMean_fitK':FitParK, 'UparaMean_fitKerror':FitParKError})
#
#    UperpRMSH.GetXaxis().SetTitle('jet multiplicity')
#    UperpRMSH.GetYaxis().SetTitle('UperpRMS')
#    UperpRMSH.SetMaximum(80)
#    UperpRMSH.SetMinimum(0.)
#    UperpRMSH.SetMarkerSize(0)
#    UperpRMSH.SetLineColor(ROOT.kAzure)
#    UperpRMSH.SetLineWidth(2)
#    UperpRMSH.Fit('pol1','','same')
#    FitFunc     = UperpRMSH.GetFunction('pol1')
#    FitParD     = FitFunc.GetParameter(0)
#    FitParDError = FitFunc.GetParError(0)
#    FitParK = FitFunc.GetParameter(1)
#    FitParKError = FitFunc.GetParError(1)
#    FitFunc.SetLineColor(ROOT.kOrange+10)
#    FitFunc.SetLineStyle(2)
#    FitFunc.SetLineWidth(2)
#    UperpRMSH.Draw('e hist')
#    FitFunc.Draw('same')
#    can1.Print(plotDir+prefix+'UperpRMS_'+cutname+'.png')
#    can1.Print(plotDir+prefix+'UperpRMS_'+cutname+'.root')
#    bins[st][ht].update({'UperpRMS_fitD':FitParD, 'UperpRMS_fitDerror':FitParDError, 'UperpRMS_fitK':FitParK, 'UperpRMS_fitKerror':FitParKError})
#
#    UperpMeanH.GetXaxis().SetTitle('jet multiplicity')
#    UperpMeanH.GetYaxis().SetTitle('UperpMean')
#    UperpMeanH.SetMaximum(100.)
#    UperpMeanH.SetMinimum(-100.)
#    UperpMeanH.SetMarkerSize(0)
#    UperpMeanH.SetLineColor(ROOT.kAzure)
#    UperpMeanH.SetLineWidth(2)
#    UperpMeanH.Fit('pol1','','same')
#    FitFunc     = UperpMeanH.GetFunction('pol1')
#    FitParD     = FitFunc.GetParameter(0)
#    FitParDError = FitFunc.GetParError(0)
#    FitParK = FitFunc.GetParameter(1)
#    FitParKError = FitFunc.GetParError(1)
#    FitFunc.SetLineColor(ROOT.kOrange+10)
#    FitFunc.SetLineStyle(2)
#    FitFunc.SetLineWidth(2)
#    UperpMeanH.Draw('e hist')
#    FitFunc.Draw('same')
#    can1.Print(plotDir+prefix+'UperpMean_'+cutname+'.png')
#    can1.Print(plotDir+prefix+'UperpMean_'+cutname+'.root')
#    bins[st][ht].update({'UperpMean_fitD':FitParD, 'UperpMean_fitDerror':FitParDError, 'UperpMean_fitK':FitParK, 'UperpMean_fitKerror':FitParKError})
#
#    pickle.dump(bins, file(pickleDir+'fitResult_metCorrection_pkl','w'))
#    del UparaRMSH,UparaMeanH,UperpRMSH,UperpMeanH

#Z to mumu
for ht in htReg:
  UparaRMSH = ROOT.TH1F('UparaRMSH','UparaRMSH',len(jetReg),0,len(jetReg))
  UparaMeanH = ROOT.TH1F('UparaMeanH','UparaMeanH',len(jetReg),0,len(jetReg))
  UperpRMSH = ROOT.TH1F('UperpRMSH','UperpRMSH',len(jetReg),0,len(jetReg))
  UperpMeanH = ROOT.TH1F('UperpMeanH','UperpMeanH',len(jetReg),0,len(jetReg))
  rcsHist = ROOT.TH1F('rcsHist','rcsHist',len(jetReg),0,len(jetReg))
  print 'Processing HT bin',ht
  for i_jet, jet in enumerate(jetReg):
    UparaHist = ROOT.TH1F('UparaHist','UparaHist',100,-500,500)
    UperpHist = ROOT.TH1F('UperpHist','UperpHist',100,-500,500)
    ZPhiHist = ROOT.TH1F('ZPhiHist','ZPhiHist',32,-3.2,3.2)
    ZPtHist = ROOT.TH1F('ZPtHist','ZPtHist',50,0,500)
    WPhiHist = ROOT.TH1F('WPhiHist','WPhiHist',32,-3.2,3.2)
    WPtHist = ROOT.TH1F('WPtHist','WPtHist',50,0,500)
    invMassHist = ROOT.TH1F('invMassHist','invMassHist',60,60,120)
    absUtHist = ROOT.TH1F('absUtHist','absUtHist',50,0,500)
    RecoGenFracHist = ROOT.TH1F('RecoGenFracHist','RecogenFracHist',60,0,3)
    dPhiHist = ROOT.TH1F('dPhiHist','dPhiHist',30,0,pi)
    dPhiDummy = ROOT.TH1F('dPhiDummy','dPhiDummy',2, array('d', [0,1.0,pi]))
    LtHist = ROOT.TH1F('LtHist','LtHist',50,0,500)
    genLtHist = ROOT.TH1F('genLtHist','genLtHist',50,0,500)
    UperpVSUpara = ROOT.TH2F('UperpVSUpara','UperpVSUpara',100,-500,500,100,-500,500)
    genMetVSfakeMet = ROOT.TH2F('genMetVSfakeMet','genMetVSfakeMet',50,0,500,50,0,500)
    print 'Processing njet',jet
    cutname = nameAndCut(None, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')[0]
    cut = presel+'&&'+htCut(ht, minPt=30, maxEta=2.4, njCorr=0.)+'&&'+ nBTagCut((0,0), minPt=30, maxEta=2.4, minCSVTag=0.814)+'&&'+nJetCut(jet, minPt=30, maxEta=2.4)

    for DY in Bkg:
      DY['chain'].Draw('>>eList',cut)
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      for i in range(number_events):
        if i%10000==0:
          print "At %i of %i in Drell-Yan events "%(i,number_events)
        DY['chain'].GetEntry(elist.GetEntry(i))

        ZPt, ZPhi, invMass, qtx, qty, leadLepPt, leadLepPhi, subLepPt, subLepPhi = getGenZ(DY['chain'])

        if invMass>120 or invMass<60: continue

        metPhi = DY['chain'].GetLeaf('met_phi').GetValue()
        metPt = DY['chain'].GetLeaf('met_pt').GetValue()

        #pick one of the two muons and mimic it as neutrino, and treat the event as  Wmunu 
        a = randint(0,1)
        if a:
          #take the leading muon
          genMetPt = leadLepPt 
          genMetPhi = leadLepPhi
          lepPt = subLepPt
          lepPhi = subLepPhi
          metX = metPt*cos(metPhi) + genMetPt*cos(genMetPhi)
          metY = metPt*sin(metPhi) + genMetPt*sin(genMetPhi)
          qtWx_corr =metX + lepPt*cos(lepPhi)
          qtWy_corr =metY + lepPt*sin(lepPhi)
        else:
          genMetPt = subLepPt
          genMetPhi = subLepPhi
          lepPt = leadLepPt
          lepPhi = leadLepPhi
          metX = metPt*cos(metPhi) + genMetPt*cos(genMetPhi)
          metY = metPt*sin(metPhi) + genMetPt*sin(genMetPhi)
          qtWx_corr =metX + lepPt*cos(lepPhi)
          qtWy_corr =metY + lepPt*sin(lepPhi)

        fakeMetPt = metPt
        fakeMetPhi = metPhi

        recoMetPt = sqrt(metX**2 + metY**2)
        recoMetPhi = atan(metY/metX)
        if metX<0:
          if metY>0:
            recoMetPhi = pi + recoMetPhi
          if metY<0:
            recoMetPhi = recoMetPhi - pi

        #calculate the pt and phi of mimic boson 
        WPt = sqrt(qtWx_corr**2 + qtWy_corr**2)
        WPhi = atan(qtWy_corr/qtWx_corr)
        if qtWx_corr<0:
          if qtWy_corr>0:
            WPhi = pi + WPhi
          if qtWy_corr<0:
            WPhi = WPhi - pi
        
#        utX = -metPt*cos(metPhi) - qtx
#        utY = -metPt*sin(metPhi) - qty
#        Upara = utX*cos(ZPhi) + utY*sin(ZPhi)
#        Uperp = utX*sin(ZPhi) - utY*cos(ZPhi)
        
#        x = -genMetPt*cos(genMetPhi)+recoMetPt*cos(recoMetPhi)
#        y = -genMetPt*sin(genMetPhi)+recoMetPt*sin(recoMetPhi)

        #project the fake Met in the W boson direction
        Upara = fakeMetPt*cos(fakeMetPhi)*cos(WPhi)+fakeMetPt*sin(fakeMetPhi)*sin(WPhi)
        Uperp = fakeMetPt*cos(fakeMetPhi)*sin(WPhi)-fakeMetPt*sin(fakeMetPhi)*cos(WPhi)
#        absUt = sqrt(utX*utX+utY*utY)
        RecoGenFrac = recoMetPt/genMetPt
        Lt = recoMetPt + lepPt
        genLt = genMetPt + lepPt
        dPhi = acos((lepPt+recoMetPt*cos(lepPhi-recoMetPhi))/sqrt(lepPt**2+recoMetPt**2+2*recoMetPt*lepPt*cos(lepPhi-recoMetPhi)))
        dPhiHist.Fill(dPhi,DY['weight'])
        dPhiDummy.Fill(dPhi,DY['weight'])
        ZPtHist.Fill(ZPt,DY['weight'])
        ZPhiHist.Fill(ZPhi,DY['weight'])
        WPtHist.Fill(WPt,DY['weight'])
        WPhiHist.Fill(WPhi,DY['weight'])
#        invMassHist.Fill(invMass,DY['weight'])
        UparaHist.Fill(Upara,DY['weight'])
        UperpHist.Fill(Uperp,DY['weight'])
#        absUtHist.Fill(absUt,DY['weight'])
        RecoGenFracHist.Fill(RecoGenFrac,DY['weight'])
        LtHist.Fill(Lt,DY['weight'])
        genLtHist.Fill(genLt,DY['weight'])
        genMetVSfakeMet.Fill(fakeMetPt,genMetPt,DY['weight'])
        UperpVSUpara.Fill(Upara,Uperp,DY['weight'])
    
    UparaHist.Draw('e hist')
    UparaHist.Fit('gaus','','same')
    FitFunc = UparaHist.GetFunction('gaus')
    FitFunc.Draw('same')
    can1.Print(plotDir+prefix+'Upara_'+cutname+'.png')
    can1.Print(plotDir+prefix+'Upara_'+cutname+'.root')
    
    UperpHist.Draw('e hist')
    UperpHist.Fit('gaus','','same')
    FitFunc = UperpHist.GetFunction('gaus')
    FitFunc.Draw('same')
    can1.Print(plotDir+prefix+'Uperp_'+cutname+'.png')
    can1.Print(plotDir+prefix+'Uperp_'+cutname+'.root')
    
    UparaRMS = UparaHist.GetRMS()
    UparaMean = UparaHist.GetMean()
    UperpRMS = UperpHist.GetRMS()
    UperpMean = UperpHist.GetMean()
    WPtHist.Draw('hist')
    can1.Print(plotDir+prefix+'WPt_'+cutname+'.png')
    can1.Print(plotDir+prefix+'WPt_'+cutname+'.root')
    WPhiHist.Draw('hist')
    can1.Print(plotDir+prefix+'WPhi_'+cutname+'.png')
    can1.Print(plotDir+prefix+'WPhi_'+cutname+'.root')
    ZPtHist.Draw('hist')
    can1.Print(plotDir+prefix+'ZPt_'+cutname+'.png')
    can1.Print(plotDir+prefix+'ZPt_'+cutname+'.root')
    ZPhiHist.Draw('hist')
    can1.Print(plotDir+prefix+'ZPhi_'+cutname+'.png')
    can1.Print(plotDir+prefix+'ZPhi_'+cutname+'.root')
#    invMassHist.Draw('hist')
#    can1.Print(plotDir+prefix+'invMass_'+cutname+'.png')
#    can1.Print(plotDir+prefix+'invMass_'+cutname+'.root')
    RecoGenFracHist.Draw('hist')
    can1.Print(plotDir+prefix+'RecoGenFrac_'+cutname+'.png')
    can1.Print(plotDir+prefix+'RecoGenFrac_'+cutname+'.root')
    dPhiHist.Draw('hist')
    can1.Print(plotDir+prefix+'dPhi_'+cutname+'.png')
    can1.Print(plotDir+prefix+'dPhi_'+cutname+'.root')
    LtHist.Draw('hist')
    can1.Print(plotDir+prefix+'Lt_'+cutname+'.png')
    can1.Print(plotDir+prefix+'Lt_'+cutname+'.root')
    genLtHist.Draw('hist')
    can1.Print(plotDir+prefix+'genLt_'+cutname+'.png')
    can1.Print(plotDir+prefix+'genLt_'+cutname+'.root')
    UperpVSUpara.Draw('colz')
    UperpVSUpara.GetXaxis().SetTitle('Upara')
    UperpVSUpara.GetYaxis().SetTitle('Uperp')
    can1.SetLogz()
    can1.Print(plotDir+prefix+'UperpVSUpara_'+cutname+'.png')
    can1.Print(plotDir+prefix+'UperpVSUpara_'+cutname+'.root')
    genMetVSfakeMet.Draw('colz')
    genMetVSfakeMet.GetXaxis().SetTitle('#slash{E}_{T}^{fake}')
    genMetVSfakeMet.GetYaxis().SetTitle('#slash{E}_{T}^{gen}')
    can1.SetLogz()
    can1.Print(plotDir+prefix+'genMetVSfakeMet_'+cutname+'.png')
    can1.Print(plotDir+prefix+'genMetVSfakeMet_'+cutname+'.root')

    if dPhiDummy.GetBinContent(1)>0:
      rcs = dPhiDummy.GetBinContent(2)/dPhiDummy.GetBinContent(1)
      if dPhiDummy.GetBinContent(2)>0:
        rcsE = rcs*sqrt(dPhiDummy.GetBinError(2)**2/dPhiDummy.GetBinContent(2)**2 +dPhiDummy.GetBinError(1)**2/dPhiDummy.GetBinContent(1)**2)
    rcsHist.SetBinContent(i_jet+1,rcs)
    rcsHist.SetBinError(i_jet+1,rcsE)
    rcsHist.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))

    UparaRMSH.SetBinContent(i_jet+1,UparaRMS)
    UparaRMSH.SetBinError(i_jet+1,UparaHist.GetRMSError())
    UparaRMSH.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))
    UparaMeanH.SetBinContent(i_jet+1,UparaMean)
    UparaMeanH.SetBinError(i_jet+1,UparaHist.GetMeanError())
    UparaMeanH.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))
    UperpRMSH.SetBinContent(i_jet+1,UperpRMS)
    UperpRMSH.SetBinError(i_jet+1,UperpHist.GetRMSError())
    UperpRMSH.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))
    UperpMeanH.SetBinContent(i_jet+1,UperpMean)
    UperpMeanH.SetBinError(i_jet+1,UperpHist.GetMeanError())
    UperpMeanH.GetXaxis().SetBinLabel(i_jet+1, nJetBinName(jet))
    del UparaHist,UperpHist,ZPhiHist,ZPtHist, dPhiDummy

  rcsHist.GetXaxis().SetTitle('jet multiplicity')
  rcsHist.GetYaxis().SetTitle('R_{CS}')
  rcsHist.SetMaximum(1.0)
  rcsHist.SetMinimum(0.0)
  rcsHist.SetMarkerSize(0)
  rcsHist.SetLineColor(ROOT.kAzure)
  rcsHist.SetLineWidth(2)
  rcsHist.Fit('pol1','','same')
  FitFunc     = rcsHist.GetFunction('pol1')
  FitParD     = FitFunc.GetParameter(0)
  FitParDError = FitFunc.GetParError(0)
  FitParK = FitFunc.GetParameter(1)
  FitParKError = FitFunc.GetParError(1)
  FitFunc.SetLineColor(ROOT.kOrange+10)
  FitFunc.SetLineStyle(2)
  FitFunc.SetLineWidth(2)
  rcsHist.Draw('e hist')
  FitFunc.Draw('same')
  can1.Print(plotDir+prefix+'rCS_'+cutname+'.png')
  can1.Print(plotDir+prefix+'rCS_'+cutname+'.root')

  UparaRMSH.GetXaxis().SetTitle('jet multiplicity')
  UparaRMSH.GetYaxis().SetTitle('UparaRMS')
  UparaRMSH.SetMaximum(80)
  UparaRMSH.SetMinimum(0.)
  UparaRMSH.SetMarkerSize(0)
  UparaRMSH.SetLineColor(ROOT.kAzure)
  UparaRMSH.SetLineWidth(2)
  UparaRMSH.Fit('pol1','','same')
  FitFunc     = UparaRMSH.GetFunction('pol1')
  FitParD     = FitFunc.GetParameter(0)
  FitParDError = FitFunc.GetParError(0)
  FitParK = FitFunc.GetParameter(1)
  FitParKError = FitFunc.GetParError(1)
  FitFunc.SetLineColor(ROOT.kOrange+10)
  FitFunc.SetLineStyle(2)
  FitFunc.SetLineWidth(2)    
  UparaRMSH.Draw('e hist')
  FitFunc.Draw('same')
  can1.Print(plotDir+prefix+'UparaRMS_'+cutname+'.png')
  can1.Print(plotDir+prefix+'UparaRMS_'+cutname+'.root')
#  bins[st][ht].update({'UparaRMS_fitD':FitParD, 'UparaRMS_fitDerror':FitParDError, 'UparaRMS_fitK':FitParK, 'UparaRMS_fitKerror':FitParKError})
  
  UparaMeanH.GetXaxis().SetTitle('jet multiplicity')
  UparaMeanH.GetYaxis().SetTitle('UparaMean')
  UparaMeanH.SetMaximum(100.)
  UparaMeanH.SetMinimum(-100.)
  UparaMeanH.SetMarkerSize(0)
  UparaMeanH.SetLineColor(ROOT.kAzure)
  UparaMeanH.SetLineWidth(2)
  UparaMeanH.Fit('pol1','','same')
  FitFunc     = UparaMeanH.GetFunction('pol1')
  FitParD     = FitFunc.GetParameter(0)
  FitParDError = FitFunc.GetParError(0)
  FitParK = FitFunc.GetParameter(1)
  FitParKError = FitFunc.GetParError(1)
  FitFunc.SetLineColor(ROOT.kOrange+10)
  FitFunc.SetLineStyle(2)
  FitFunc.SetLineWidth(2)
  UparaMeanH.Draw('e hist')
  FitFunc.Draw('same')
  can1.Print(plotDir+prefix+'UparaMean_'+cutname+'.png')
  can1.Print(plotDir+prefix+'UparaMean_'+cutname+'.root')
#  bins[st][ht].update({'UparaMean_fitD':FitParD, 'UparaMean_fitDerror':FitParDError, 'UparaMean_fitK':FitParK, 'UparaMean_fitKerror':FitParKError})

  UperpRMSH.GetXaxis().SetTitle('jet multiplicity')
  UperpRMSH.GetYaxis().SetTitle('UperpRMS')
  UperpRMSH.SetMaximum(80)
  UperpRMSH.SetMinimum(0.)
  UperpRMSH.SetMarkerSize(0)
  UperpRMSH.SetLineColor(ROOT.kAzure)
  UperpRMSH.SetLineWidth(2)
  UperpRMSH.Fit('pol1','','same')
  FitFunc     = UperpRMSH.GetFunction('pol1')
  FitParD     = FitFunc.GetParameter(0)
  FitParDError = FitFunc.GetParError(0)
  FitParK = FitFunc.GetParameter(1)
  FitParKError = FitFunc.GetParError(1)
  FitFunc.SetLineColor(ROOT.kOrange+10)
  FitFunc.SetLineStyle(2)
  FitFunc.SetLineWidth(2)
  UperpRMSH.Draw('e hist')
  FitFunc.Draw('same')
  can1.Print(plotDir+prefix+'UperpRMS_'+cutname+'.png')
  can1.Print(plotDir+prefix+'UperpRMS_'+cutname+'.root')
#  bins[st][ht].update({'UperpRMS_fitD':FitParD, 'UperpRMS_fitDerror':FitParDError, 'UperpRMS_fitK':FitParK, 'UperpRMS_fitKerror':FitParKError})

  UperpMeanH.GetXaxis().SetTitle('jet multiplicity')
  UperpMeanH.GetYaxis().SetTitle('UperpMean')
  UperpMeanH.SetMaximum(100.)
  UperpMeanH.SetMinimum(-100.)
  UperpMeanH.SetMarkerSize(0)
  UperpMeanH.SetLineColor(ROOT.kAzure)
  UperpMeanH.SetLineWidth(2)
  UperpMeanH.Fit('pol1','','same')
  FitFunc     = UperpMeanH.GetFunction('pol1')
  FitParD     = FitFunc.GetParameter(0)
  FitParDError = FitFunc.GetParError(0)
  FitParK = FitFunc.GetParameter(1)
  FitParKError = FitFunc.GetParError(1)
  FitFunc.SetLineColor(ROOT.kOrange+10)
  FitFunc.SetLineStyle(2)
  FitFunc.SetLineWidth(2)
  UperpMeanH.Draw('e hist')
  FitFunc.Draw('same')
  can1.Print(plotDir+prefix+'UperpMean_'+cutname+'.png')
  can1.Print(plotDir+prefix+'UperpMean_'+cutname+'.root')
#  bins[st][ht].update({'UperpMean_fitD':FitParD, 'UperpMean_fitDerror':FitParDError, 'UperpMean_fitK':FitParK, 'UperpMean_fitKerror':FitParKError})

#  pickle.dump(bins, file(pickleDir+'fitResult_metCorrection_pkl','w'))
  del UparaRMSH,UparaMeanH,UperpRMSH,UperpMeanH


