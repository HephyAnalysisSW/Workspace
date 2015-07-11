import ROOT
import os, sys, copy
import pickle

#ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
#ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import *#getVarValue, getChain, deltaPhi, getYieldFromChain
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_softLepton import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.eventShape import *

presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"

ROOT.TH1F().SetDefaultSumw2()

getW = 'abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)<10'
para = ['pt','phi','pdgId','motherId']

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
  else: return 0., 0.
  
def getWv2(c):
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  lepPt = c.GetLeaf('leptonPt').GetValue()
  lepPhi = c.GetLeaf('leptonPhi').GetValue()
  Wx = lepPt*cos(lepPhi)+metGenPt*cos(metGenPhi)
  Wy = lepPt*sin(lepPhi)+metGenPt*sin(metGenPhi)
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
  x = -metGenPhi*cos(metGenPhi)+metPt*cos(metPhi)
  y = -metGenPhi*sin(metGenPhi)+metPt*sin(metPhi)
  Upara = x*cos(WPhi)+y*sin(WPhi)
  Uperp = x*sin(WPhi)-y*cos(WPhi)
  return Upara, Uperp


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

varstring="deltaPhi_Wl"
plotDir='/afs/hephy.at/user/d/dspitzbart/www/WjetKinFakeMetOnW/'

if not os.path.exists(plotDir):
  os.makedirs(plotDir)


lepSel='hard'
WJETS = getChain(WJetsHTToLNu[lepSel],histname='')

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

# upara
for st in stReg:
  print
  print 'Processing ST bin',st
  for ht in htReg:
    UparaRMSH = ROOT.TH1F('UparaRMSH','UparaRMSH',len(jetReg),0,len(jetReg))
    UparaMeanH = ROOT.TH1F('UparaMeanH','UparaMeanH',len(jetReg),0,len(jetReg))
    UperpRMSH = ROOT.TH1F('UperpRMSH','UperpRMSH',len(jetReg),0,len(jetReg))
    UperpMeanH = ROOT.TH1F('UperpMeanH','UperpMeanH',len(jetReg),0,len(jetReg))
    print 'Processing HT bin',ht
    for i_jet, jet in enumerate(jetReg):
      UparaHist = ROOT.TH1F('UparaHist','UparaHist',100,-500,500)
      UperpHist = ROOT.TH1F('UperpHist','UperpHist',100,-500,500)
      WPhiHist = ROOT.TH1F('WPhiHist','WPhiHist',32,-3.2,3.2)
      WPtHist = ROOT.TH1F('WPtHist','WPtHist',50,0,500)
      print 'Processing njet',jet
      cutname, cut = nameAndCut(st, ht, jet, btb=btb, presel=presel, btagVar = 'nBJetMediumCSV30')
      WJETS.Draw('>>eList',cut)
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      for i in range(number_events):
        WJETS.GetEntry(elist.GetEntry(i))
        weight=getVarValue(WJETS,"weight")
        WPt, WPhi = getW(WJETS)
        if WPt>0:
          WPtHist.Fill(WPt,weight)
          WPhiHist.Fill(WPhi,weight)
          Upara, Uperp = getU2(WJETS, WPt, WPhi)
          UparaHist.Fill(Upara,weight)
          UperpHist.Fill(Uperp,weight)
      UparaHist.Draw('e hist')
      UparaHist.Fit('gaus','','same')
      FitFunc = UparaHist.GetFunction('gaus')
      FitFunc.Draw('same')
      can1.Print(plotDir+'Upara_'+cutname+'.png')
      can1.Print(plotDir+'Upara_'+cutname+'.root')

      
      UperpHist.Draw('e hist')
      UperpHist.Fit('gaus','','same')
      FitFunc = UperpHist.GetFunction('gaus')
      FitFunc.Draw('same')
      can1.Print(plotDir+'Uperp_'+cutname+'.png')
      can1.Print(plotDir+'Uperp_'+cutname+'.root')
      
      UparaRMS = UparaHist.GetRMS()
      UparaMean = UparaHist.GetMean()
      UperpRMS = UperpHist.GetRMS()
      UperpMean = UperpHist.GetMean()
      WPtHist.Draw('hist')
      can1.Print(plotDir+'WPt_'+cutname+'.png')
      can1.Print(plotDir+'WPt_'+cutname+'.root')
      WPhiHist.Draw('hist')
      can1.Print(plotDir+'WPhi_'+cutname+'.png')
      can1.Print(plotDir+'WPhi_'+cutname+'.root')
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
      del UparaHist,UperpHist,WPhiHist,WPtHist

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
    can1.Print(plotDir+'UparaRMS_'+cutname+'.png')
    can1.Print(plotDir+'UparaRMS_'+cutname+'.root')
    
    UparaMeanH.GetXaxis().SetTitle('jet multiplicity')
    UparaMeanH.GetYaxis().SetTitle('UparaMean')
    UparaMeanH.SetMaximum(500.)
    UparaMeanH.SetMinimum(-500.)
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
    can1.Print(plotDir+'UparaMean_'+cutname+'.png')
    can1.Print(plotDir+'UparaMean_'+cutname+'.root')

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
    can1.Print(plotDir+'UperpRMS_'+cutname+'.png')
    can1.Print(plotDir+'UperpRMS_'+cutname+'.root')

    UperpMeanH.GetXaxis().SetTitle('jet multiplicity')
    UperpMeanH.GetYaxis().SetTitle('UperpMean')
    UperpMeanH.SetMaximum(500.)
    UperpMeanH.SetMinimum(-500.)
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
    can1.Print(plotDir+'UperpMean_'+cutname+'.png')
    can1.Print(plotDir+'UperpMean_'+cutname+'.root')

    del UparaRMSH,UparaMeanH,UperpRMSH,UperpMeanH



