import ROOT
from array import array
from math import *
import os, copy, sys
from Workspace.RA4Analysis.helpers import nJetBinName, nBTagBinName

#ROOT.TH1F().SetDefaultSumw2()
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks
import Workspace.HEPHYPythonTools.xsec as xsec
#from Workspace.RA4Analysis.simplePlotsCommon import *
from Workspace.RA4Analysis.helpers import *

from Workspace.RA4Analysis.cmgTuples_v5_Phys14 import WJetsToLNu_HT100to200_fromEOS, WJetsToLNu_HT200to400_fromEOS, WJetsToLNu_HT400to600_fromEOS, WJetsToLNu_HT600toInf_fromEOS, ttJets_fromEOS
ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kBlue-2, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
samples=[WJetsToLNu_HT100to200_fromEOS, WJetsToLNu_HT200to400_fromEOS, WJetsToLNu_HT400to600_fromEOS, WJetsToLNu_HT600toInf_fromEOS,ttJets_fromEOS]
totalYield=0
for s in samples:
  cs=getChunks(s, treeName="treeProducerSusySingleLepton")
  s.update(cs[0][0])
  s['chain']=ROOT.TChain('tree')
  s['chain'].Add(s['file'])
  s["weight"]=4000*xsec.xsec[s['dbsName']]/float(cs[1])
  nEntry=s['chain'].GetEntries()
  totalYield+=4000*xsec.xsec[s['dbsName']]/float(cs[1])*nEntry
  print s["name"],"xsec",xsec.xsec[s['dbsName']],"NSim",cs[1],"nEntry",nEntry, "yield:",4000*xsec.xsec[s['dbsName']]/float(cs[1])*nEntry
print "totalYield", totalYield

def muonSelectionStr(minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
  return "abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt)+"&&abs(LepGood_eta)<"+str(maxEta)+"&&LepGood_tightId>="+str(minID)+"&&LepGood_relIso03<"+str(minRelIso)
def electronSelectionStr(minPt=25, maxEta=2.4, minID=3, minRelIso=0.12):
  return "abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt)+"&&abs(LepGood_eta)<"+str(maxEta)+"&&LepGood_tightId>="+str(minID)+"&&LepGood_relIso03<"+str(minRelIso)

def exactlyOneTightMuon(minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
  return "(Sum$("+muonSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)+")==1)"
def exactlyOneTightElectron(minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
  return "(Sum$("+electronSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)+")==1)"
 
def exactlyOneTightLepton(lepton="muon", minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
#  return "(Sum$((abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt)+"&&abs(LepGood_eta)<"+str(maxEta)+"&&LepGood_tightId>="+str(minIDs[0])+"&&LepGood_relIso03<"+str(minRelIsos[0])+")"\
#         +   "||(abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt)+"&&abs(LepGood_eta)<"+str(maxEta)+"&&LepGood_tightId>="+str(minIDs[1])+"&&LepGood_relIso03<"+str(minRelIsos[1])+"))==1)"
  if lepton.lower()=="muon":
    return exactlyOneTightMuon(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
  if lepton.lower()=="electron":
    return exactlyOneTightElectron(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
def looseLeptonVeto(minPt=10, muMultiplicity=1, eleMultiplicity=0):
  return "(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>"+str(minPt)+")=="+str(muMultiplicity)+"&&Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>"+str(minPt)+")=="+str(eleMultiplicity)+")"

def nBTagStr(minPt=30, maxEta=2.4, minCMVATag=0.732):
  return "Sum$(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id&&Jet_btagCMVA>"+str(minCMVATag)+")"
def nBTagRequ(n, minPt=30, maxEta=2.4, minCMVATag=0.732):
  return "("+nBTagStr(minPt=minPt,maxEta=maxEta,minCMVATag=minCMVATag)+"=="+str(n)+")"
#def nBTagRequ(n, minPt=30, maxEta=2.4, minCMVATag=0.732):
#  return "(Sum$(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id&&Jet_btagCMVA>"+str(minCMVATag)+")=="+str(n)+")"
def nJetCut(njb, minPt=30, maxEta=2.4):
  if type(njb)==type(0):
    return "(Sum$(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id)>="+str(njb)+")"
  if type(njb)==type([]) or type(njb)==type(()):
    if len(njb)>1 and njb[1]>0:
      return "(Sum$(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id)>="+str(njb[0])+"&&Sum$(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id)<="+str(njb[1])+")"
    else: 
      return nJetCut(njb[0], minPt=minPt, maxEta=maxEta)
    
def htCut(htb, minPt=30, maxEta=2.4):
  if type(htb)==type(0):
    return "(Sum$(Jet_pt*(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id))>"+str(htb)+")"
  if type(htb)==type([]) or type(htb)==type(()):
    if len(htb)>1 and htb[1]>0:
      return "(Sum$(Jet_pt*(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id))>"+str(htb[0])+"&&Sum$(Jet_pt*(Jet_pt>"+str(minPt)+"&&abs(Jet_eta)<"+str(maxEta)+"&&Jet_id))<="+str(htb[1])+")"
    else:
      return  htCut(htb[0], minPt=minPt, maxEta=maxEta)

def stCut(stb, lepton="muon", minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
  if lepton.lower()=="muon":
    lStr = muonSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
  if lepton.lower()=="electron":
    lStr = electronSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
  if type(stb)==type(0):
    return   "(Sum$((LepGood_pt+met_pt)*("+lStr+")>"+str(stb)+")==1)"
  if type(stb)==type([]) or type(stb)==type(()):
    if len(stb)>1 and stb[1]>0:
      return   "(Sum$((LepGood_pt+met_pt)*("+lStr+")>"+str(stb[0])+")==1&&"\
              +"Sum$((LepGood_pt+met_pt)*("+lStr+")<="+str(stb[1])+")==1 )"
    else:
      return  muSTCut(stb[0], minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)

def dPhiCut(minDPhi,lepton="muon", minPt=25, maxEta=2.4, minID=1, minRelIso=0.12):
  if lepton.lower()=="muon":
    lStr = muonSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
  if lepton.lower()=="electron":
    lStr = electronSelectionStr(minPt=minPt, maxEta=maxEta, minID=minID, minRelIso=minRelIso)
  return  "(Sum$(acos((LepGood_pt + met_pt*cos(LepGood_phi - met_phi))/sqrt(LepGood_pt**2 + met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi)))"\
         +"*("+lStr+")>"+str(minDPhi)+")==1)"

htb= (400)
stb= 250
prefix=""

leptonMinPt=25

#lepton="muon"; muMultiplicity=1; eleMultiplicity=0; minID=1; minRelIso=0.12
lepton="electron"; muMultiplicity=0; eleMultiplicity=1; minID=3; minRelIso=0.14

minRelIso=0.25

plots={}
njet_bins = [(2,3), (4,4),(5,5),(6,-1)]
nbtag_bins = [0,1,2,3,4,5]
for njb in njet_bins: 
  #njb= 5

  cut= "&&".join([
      exactlyOneTightLepton(lepton=lepton, minPt=leptonMinPt, maxEta=2.4, minID=minID, minRelIso=minRelIso),\
      looseLeptonVeto(minPt=10, muMultiplicity=muMultiplicity, eleMultiplicity=eleMultiplicity), \
      nJetCut(njb=njb, minPt=30, maxEta=2.4), \
      htCut  (htb=htb, minPt=30, maxEta=2.4), \
      stCut(lepton=lepton, stb=stb, minPt=leptonMinPt, maxEta=2.4, minID=minID, minRelIso=minRelIso), \
      ])

  rCS_vs_nbtag = ROOT.TProfile('profile_rCS','', len(nbtag_bins)-1, array('d',nbtag_bins), 0, 1)
  print "njb", njb,"cut:", cut
  #rCS_vs_nbtag.Reset()
  ttJets_fromEOS['chain'].Draw(dPhiCut(minDPhi=1, lepton=lepton,minPt=leptonMinPt, maxEta=2.4, minID=minID, minRelIso=minRelIso)+":"+nBTagStr(minPt=30, maxEta=2.4, minCMVATag=0.732)+'>>profile_rCS',cut,'goff') 
  plots[njb]=ROOT.gDirectory.Get('profile_rCS').Clone()

opt=""
#c1 = ROOT.TCanvas()
l=ROOT.TLegend(0.7,0.7,1.0,1.0)
l.SetFillColor(ROOT.kWhite)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)
for i_njb,njb in enumerate(njet_bins):
  ROOT.gStyle.SetOptStat(0)
  plots[njb].GetYaxis().SetRangeUser(0,0.2)
  plots[njb].SetLineColor(ROOT_colors[i_njb])
  plots[njb].Draw(opt)
  l.AddEntry(plots[njb], nJetBinName(njb))
  if opt=="":
    opt="same"

l.Draw()

