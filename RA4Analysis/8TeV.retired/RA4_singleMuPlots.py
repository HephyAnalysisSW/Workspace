import ROOT
from array import array
from math import *
import os, copy
from simpleStatTools import niceNum
from Workspace.RA4Analysis.simplePlotsCommon import *
from funcs import *

import xsec
small = False

singleMuData={}
singleMuData["name"]     = "singleMuData";
singleMuData["dirname"] = "/data/schoef/pat_120816/data8TeV/"
singleMuData["bins"]    = [ 'SingleMu-Run2012A-PromptReco', 'SingleMu-Run2012B-PromptReco']
singleMuData["Chain"] = "Events"
singleMuData["Counter"] = "bool_EventCounter_passed_PAT.obj"

muHadData={}
muHadData["name"]     = "muHadData";
muHadData["dirname"] = "/data/schoef/pat_120816/data8TeV/"
muHadData["bins"]    = [ 'MuHad-Run2012A-PromptReco', 'MuHad-Run2012B-PromptReco']
muHadData["Chain"] = "Events"
muHadData["Counter"] = "bool_EventCounter_passed_PAT.obj"

allSamples = [singleMuData, muHadData]

targetLumi = 12000.

allVars=[]
allStacks=[]

signalColors = [ROOT.kBlack, ROOT.kBlue + 1, ROOT.kGreen + 2, ROOT.kOrange + 2]

## plots for studying preselection 
topIsLargest = True
minimum=10**(-0.5)

signalNumbers = []
presel = "pf-4j40"
preprefix     = "Mu-ht400"
#additionalCut = "met>100&&nbtags>=2&&ht>300"
additionalCut = "ht>400"
#additionalCut = ""

subdir = "/singleMu/"
doOnlyMET = True

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"

if presel == "pf-4j40":
  chainstring = "Events"
  commoncf = "jet3pt>40&&(singleMuonic&&nvetoMuons==1&&nvetoElectrons==0)&&leptonPt>45&&abs(leptonEta)<2.1"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= "RA4_"+presel+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"
  
for sample in allSamples:
  sample["Chain"] = chainstring


def getStack(varstring, binning, cutstring, signalNumbers, topIsLargest = False, varfunc = ""):
  SINGLEMU_DATA          = variable(varstring, binning, cutstring)
  SINGLEMU_DATA.sample   = singleMuData
  SINGLEMU_DATA.color    = dataColor
  SINGLEMU_DATA.legendText="singleMu Data"

  MUHAD_DATA          = variable(varstring, binning, cutstring)
  MUHAD_DATA.sample   = muHadData
  MUHAD_DATA.color    = ROOT.kRed
  MUHAD_DATA.legendText="MuHad Data"
  res = [SINGLEMU_DATA, MUHAD_DATA]
  res[0].dataMCRatio = [SINGLEMU_DATA, MUHAD_DATA]

  getLinesForStack(res, targetLumi)
  for var in res:
    var.legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res
#


met_stack = getStack(":met;#slash{E}_{T} (GeV);Number of Events / 25 GeV",[41,0,1025], commoncf, signalNumbers, topIsLargest)
met_stack[0].addOverFlowBin = "upper"
allStacks.append(met_stack)
  
#cleanMT095_stack  = getStack(":cleanMT095;m_{T} for cos(#Delta #phi(l, #slash{E}_{T})) > -0.95;Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest, cleanMTFunc(0.95))
#allStacks.append(cleanMT095_stack)
#
#cleanMT09_stack  = getStack(":cleanMT09;m_{T} for cos(#Delta #phi(l, #slash{E}_{T})) > -0.9;Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest, cleanMTFunc(0.9))
#allStacks.append(cleanMT09_stack)
#
#cleanMT08_stack  = getStack(":cleanMT08;m_{T} for cos(#Delta #phi(l, #slash{E}_{T})) > -0.8;Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest, cleanMTFunc(0.8))
#allStacks.append(cleanMT08_stack)
#
#mTbare_stack  = getStack(":mTbare;m_{T} with raw #slash{E}_{T};Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest, mTbare)
#allStacks.append(mTbare_stack)
#
#cosDeltaPhiLepMET_stack  = getStack(":xxx;cos(#Delta #phi(l, #slash{E}_{T}));Number of Events",[50,-1,1], commoncf, signalNumbers, topIsLargest, cosDeltaPhiLepMET)
#allStacks.append(cosDeltaPhiLepMET_stack)


#ht_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 25 GeV",[41,500,1525 ], commoncf, signalNumbers, topIsLargest)
#ht_stack[0].addOverFlowBin = "upper"
#allStacks.append(ht_stack)
#

#btag0mass_stack               = getStack(":btag0Mass;btag0Mass;Number of Events",[20,0,8.0], commoncf+"&&btag0>1.74", signalNumbers, topIsLargest)
#btag0mass_stack[0].addOverFlowBin = "upper"
#allStacks.append(btag0mass_stack)
#btag1mass_stack               = getStack(":btag1Mass;btag1Mass;Number of Events",[20,0,8.0], commoncf+"&&btag1>1.74", signalNumbers, topIsLargest)
#btag1mass_stack[0].addOverFlowBin = "upper"
#allStacks.append(btag1mass_stack)
#btag2mass_stack               = getStack(":btag2Mass;btag2Mass;Number of Events",[20,0,8.0], commoncf+"&&btag2>1.74", signalNumbers, topIsLargest)
#btag2mass_stack[0].addOverFlowBin = "upper"
#allStacks.append(btag2mass_stack)
#btag3mass_stack               = getStack(":btag3Mass;btag3Mass;Number of Events",[20,0,8.0], commoncf+"&&btag3>1.74", signalNumbers, topIsLargest)
#btag3mass_stack[0].addOverFlowBin = "upper"
#allStacks.append(btag3mass_stack)


#jlb_stack = getStack(":mht - leptonPt;JLB (GeV);Number of Events / 20 GeV",[52,-520,520], commoncf, signalNumbers, topIsLargest)
#jlb_stack[0].addOverFlowBin = "both"
#allStacks.append(jlb_stack)
#ptw_stack = getStack(":sqrt((metpx + leptonPt*cos(lepton_phi))**2 + (metpy + leptonPt*sin(lepton_phi))**2);(l+#slash{E})_{T}; Number of Events / 25 GeV",[21,0,525], commoncf, signalNumbers, topIsLargest)
#ptw_stack[0].addOverFlowBin = "upper"
#allStacks.append(ptw_stack)
#metiso_stack = getStack(":metiso;MET Iso from jets; Number of Events",[40,0,3.1415], commoncf, signalNumbers, topIsLargest)
#metiso_stack[0].addOverFlowBin = "upper"
#allStacks.append(metiso_stack)


if not doOnlyMET:
  mT_stack  = getStack(":mT;m_{T} (GeV);Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest)
  mT_stack[0].addOverFlowBin = "upper"
  allStacks.append(mT_stack)

  rawmet_stack  = getStack(":rawmet; (GeV);Number of Events / 20 GeV",[27,0,540], commoncf, signalNumbers, topIsLargest, rawMET)
  rawmet_stack[0].addOverFlowBin = "upper"
  allStacks.append(rawmet_stack)

  ngoodVertices_stack = getStack(":ngoodVertices;Number of Vertices;Number of Events",[51,0,51], commoncf, [], topIsLargest)
  ngoodVertices_stack[0].addOverFlowBin = "upper"
  allStacks.append(ngoodVertices_stack)


  jet0_pt_stack                     = getStack(":jet0pt;p_{T} of leading jet (GeV);Number of Events / 40 GeV",[26,0,1040], commoncf, signalNumbers, topIsLargest)
  jet0_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet0_pt_stack)
  jet1_pt_stack                     = getStack(":jet1pt;p_{T} of 2^{nd} leading jet (GeV);Number of Events / 40 GeV",[26,0,1040], commoncf, signalNumbers, topIsLargest)
  jet1_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet1_pt_stack)
  jet2_pt_stack                     = getStack(":jet2pt;p_{T} of 3^{rd} leading jet (GeV);Number of Events / 40 GeV",[21,0,840], commoncf, signalNumbers, topIsLargest)
  jet2_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet2_pt_stack)
  jet3_pt_stack                     = getStack(":jet3pt;p_{T} of 4^{th} leading jet (GeV);Number of Events / 40 GeV",[21,00,840], commoncf+"&&jet3pt>0", signalNumbers, topIsLargest)
  jet3_pt_stack[0].addOverFlowBin = "upper"
  allStacks.append(jet3_pt_stack)

  kinMetSig_stack                   = getStack(":kinMetSig;S_{MET};Number of Events",[25,0,25], commoncf, signalNumbers, topIsLargest, kinMetSig)
  kinMetSig_stack[0].addOverFlowBin = "upper"
  allStacks.append(kinMetSig_stack)

  ht_stack                          = getStack(":ht;H_{T} (GeV);Number of Events / 100 GeV", [26,0, 2600], commoncf, signalNumbers, topIsLargest)
  ht_stack[0].addOverFlowBin = "upper"
  allStacks.append(ht_stack)

  m3_stack = getStack(":m3;M_{3} (GeV);Number of Events / 100 GeV",[26, 0, 2600], commoncf, signalNumbers, topIsLargest)
  m3_stack[0].addOverFlowBin = "upper"
  allStacks.append(m3_stack)

  leptonPt_stack = getStack("p_{T} (GeV):leptonPt;p_{T,lep.} (GeV);Number of Events / 30 GeV",[26,0,780], commoncf, signalNumbers, topIsLargest)
  leptonPt_stack[0].addOverFlowBin = "upper"
  allStacks.append(leptonPt_stack)

  leptonEta_stack                  = getStack(":leptonEta;|#eta^{#mu}|;Number of Events",[62,-3.1,3.1], commoncf, signalNumbers, topIsLargest)
  leptonEta_stack[0].addOverFlowBin = "both"
  allStacks.append(leptonEta_stack)
  
  ngoodElectrons_stack = getStack("ngoodElectrons :ngoodElectrons;Number of electrons;Number of Events",[5,0-.5,5-.5], commoncf.replace("singleMuonic&&nvetoMuons==1&&nvetoElectrons==0", "ngoodMuons==1&&nvetoMuons==1"), signalNumbers, topIsLargest)
  ngoodElectrons_stack[0].addOverFlowBin = "upper"
  allStacks.append(ngoodElectrons_stack)

  ngoodMuons_stack = getStack("ngoodMuons :ngoodMuons;Number of muons;Number of Events",[5,0-.5,5-.5], commoncf.replace("singleMuonic&&nvetoMuons==1", "ngoodMuons>0"), signalNumbers, topIsLargest)
  ngoodMuons_stack[0].addOverFlowBin = "upper"
  allStacks.append(ngoodMuons_stack)

  nvetoElectrons_stack = getStack("nvetoElectrons :nvetoElectrons;Number of veto electrons;Number of Events",[5,0-.5,5-.5], commoncf.replace("singleMuonic&&nvetoMuons==1&&nvetoElectrons==0","ngoodMuons==1&&nvetoMuons==1"), signalNumbers, topIsLargest)
  nvetoElectrons_stack[0].addOverFlowBin = "upper"
  allStacks.append(nvetoElectrons_stack)

  nvetoMuons_stack = getStack("nvetoMuons :nvetoMuons;Number of veto muons;Number of Events",[5,0-.5,5-.5], commoncf.replace("&&nvetoMuons==1",""), signalNumbers, topIsLargest)
  nvetoMuons_stack[0].addOverFlowBin = "upper"
  allStacks.append(nvetoMuons_stack)

  nbtags_stack = getStack(":nbtags;Number of b-tagged Jets;Number of Events",[10,0,10], commoncf, [], topIsLargest)
  nbtags_stack[0].addOverFlowBin = "upper"
  allStacks.append(nbtags_stack)

  njets_stack = getStack(":njets;Number of Jets;Number of Events",[20,0,20], commoncf.replace("jet2pt>40&&",""), [], topIsLargest)
  njets_stack[0].addOverFlowBin = "upper"
  allStacks.append(njets_stack)

#  if useConvertedTuples:
#    phibb_stack            =   getStack( ":phibb;phi(bb);Number of Events", [10,0,pi], commoncf, [], topIsLargest)
#    phibb_stack[0].addOverFlowBin = "both"
#    allStacks.append(phibb_stack)
#
#    mbl_stack              =   getStack( ":mbl;m(b,l);Number of Events / 30 GeV", [31,0,930], commoncf, [], topIsLargest)
#    mbl_stack[0].addOverFlowBin = "upper"
#    allStacks.append(mbl_stack)
#
#    mbb_stack              =   getStack( ":mbb;m(b,b);Number of Events / 50 GeV", [31,0,1550], commoncf, [], topIsLargest)
#    mbb_stack[0].addOverFlowBin = "upper"
#    allStacks.append(mbb_stack)
#
#    mbbzoomed_stack              =   getStack( ":mbb;m(b,b);Number of Events / 20 GeV", [21,0,420], commoncf, [], topIsLargest)
#    mbbzoomed_stack[0].addOverFlowBin = "upper"
#    allStacks.append(mbbzoomed_stack)
#
#
#  if not useConvertedTuples:
#    metiso_stack = getStack(":metiso;MET Iso from jets;Number of Events",[40,0,3.1415], commoncf, signalNumbers, topIsLargest)
#    metiso_stack[0].addOverFlowBin = "upper"
#    allStacks.append(metiso_stack)
#
#
#    leptonDeltaR_stack          = getStack(":leptonDeltaR;#Delta R(l,jets);Number of Events",[30,0,6.28], commoncf, signalNumbers, topIsLargest)
#    leptonDeltaR_stack[0].addOverFlowBin = "upper"
#    allStacks.append(leptonDeltaR_stack)
#
#    leptonDxy_stack                  = getStack(":leptonDxy;d_{xy};Number of Events / 10 #mu m",[40,0,0.04], commoncf, signalNumbers, topIsLargest)
#    leptonDxy_stack[0].addOverFlowBin = "upper"
#    allStacks.append(leptonDxy_stack)
#
#    leptonVertexDxy_stack                  = getStack(":leptonVertexDxy;d_{xy};Number of Events / 10 #mu m",[40,0,0.04], commoncf, signalNumbers, topIsLargest)
#    leptonVertexDxy_stack[0].addOverFlowBin = "upper"
#    allStacks.append(leptonVertexDxy_stack)
#
#    leptonVertexDz_stack            = getStack(":leptonVertexDz;d_{z, V};Number of Events / 10 #mu m",[40,-.201,.201], commoncf, signalNumbers, topIsLargest)
#    leptonVertexDz_stack[0].addOverFlowBin = "both"
#    allStacks.append(leptonVertexDz_stack)
#
#    leptonRelIso_stack               = getStack(":leptonRelIso;relIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#    leptonRelIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#    allStacks.append(leptonRelIso_stack)
#    leptonRelIso_zoomed_stack               = getStack(":leptonRelIso;relIso;Number of Events",[21,0,.21], commoncf, signalNumbers, topIsLargest)
#    leptonRelIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#    allStacks.append(leptonRelIso_zoomed_stack)
#  leptonEcalIso_stack               = getStack(":leptonEcalIso;EcalIso;Number of Events",[21,0,21], commoncf, signalNumbers, topIsLargest)
#  leptonEcalIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonEcalIso_stack)
#  leptonEcalIso_zoomed_stack               = getStack(":leptonEcalIso;EcalIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonEcalIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonEcalIso_zoomed_stack)
#  leptonHcalIso_stack               = getStack(":leptonHcalIso;HcalIso;Number of Events",[21,0,21], commoncf, signalNumbers, topIsLargest)
#  leptonHcalIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonHcalIso_stack)
#  leptonHcalIso_zoomed_stack               = getStack(":leptonHcalIso;HcalIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonHcalIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonHcalIso_zoomed_stack)
#  leptonTrackIso_stack               = getStack(":leptonTrackIso;trackIso;Number of Events",[21,0,21], commoncf, signalNumbers, topIsLargest)
#  leptonTrackIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonTrackIso_stack)
#  leptonTrackIso_zoomed_stack               = getStack(":leptonTrackIso;trackIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonTrackIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonTrackIso_zoomed_stack)
#
#  leptonPF03ChargedHadronIso_stack               = getStack(":leptonPF03ChargedHadronIso;PF03ChargedHadronIso;Number of Events",[21,0,21], commoncf, signalNumbers, topIsLargest)
#  leptonPF03ChargedHadronIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF03ChargedHadronIso_stack)
#  leptonPF03NeutralHadronIso_stack               = getStack(":leptonPF03NeutralHadronIso;PF03NeutralHadronIso;Number of Events",[21,0,21], commoncf, signalNumbers, topIsLargest)
#  leptonPF03NeutralHadronIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF03NeutralHadronIso_stack)
#  leptonPF03PhotonIso_stack               = getStack(":leptonPF03PhotonIso;PF03PhotonIso;Number of Events",[21,0,21], commoncf, signalNumbers, topIsLargest)
#  leptonPF03PhotonIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF03PhotonIso_stack)
#  leptonPF03PUChargedHadronIso_stack               = getStack(":leptonPF03PUChargedHadronIso;PF03PUChargedHadronIso;Number of Events",[21,0,21], commoncf, signalNumbers, topIsLargest)
#  leptonPF03PUChargedHadronIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF03PUChargedHadronIso_stack)
#  leptonPF03RelIso_stack               = getStack(":leptonPF03RelIso;PF03RelIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonPF03RelIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF03RelIso_stack)
#
#  leptonPF04ChargedHadronIso_stack               = getStack(":leptonPF04ChargedHadronIso;PF04ChargedHadronIso;Number of Events",[21,0,21], commoncf, signalNumbers, topIsLargest)
#  leptonPF04ChargedHadronIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF04ChargedHadronIso_stack)
#  leptonPF04NeutralHadronIso_stack               = getStack(":leptonPF04NeutralHadronIso;PF04NeutralHadronIso;Number of Events",[21,0,21], commoncf, signalNumbers, topIsLargest)
#  leptonPF04NeutralHadronIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF04NeutralHadronIso_stack)
#  leptonPF04PhotonIso_stack               = getStack(":leptonPF04PhotonIso;PF04PhotonIso;Number of Events",[21,0,21], commoncf, signalNumbers, topIsLargest)
#  leptonPF04PhotonIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF04PhotonIso_stack)
#  leptonPF04PUChargedHadronIso_stack               = getStack(":leptonPF04PUChargedHadronIso;PF04PUChargedHadronIso;Number of Events",[21,0,21], commoncf, signalNumbers, topIsLargest)
#  leptonPF04PUChargedHadronIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF04PUChargedHadronIso_stack)
#  leptonPF04RelIso_stack               = getStack(":leptonPF04RelIso;PF04RelIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonPF04RelIso_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF04RelIso_stack)
#
#  leptonPF03ChargedHadronIso_zoomed_stack               = getStack(":leptonPF03ChargedHadronIso;PF03ChargedHadronIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonPF03ChargedHadronIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF03ChargedHadronIso_zoomed_stack)
#  leptonPF03NeutralHadronIso_zoomed_stack               = getStack(":leptonPF03NeutralHadronIso;PF03NeutralHadronIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonPF03NeutralHadronIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF03NeutralHadronIso_zoomed_stack)
#  leptonPF03PhotonIso_zoomed_stack               = getStack(":leptonPF03PhotonIso;PF03PhotonIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonPF03PhotonIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF03PhotonIso_zoomed_stack)
#  leptonPF03PUChargedHadronIso_zoomed_stack               = getStack(":leptonPF03PUChargedHadronIso;PF03PUChargedHadronIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonPF03PUChargedHadronIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF03PUChargedHadronIso_zoomed_stack)
#  leptonPF03RelIso_zoomed_stack               = getStack(":leptonPF03RelIso;PF03RelIso;Number of Events",[21,0,0.21], commoncf, signalNumbers, topIsLargest)
#  leptonPF03RelIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF03RelIso_zoomed_stack)
#
#  leptonPF04ChargedHadronIso_zoomed_stack               = getStack(":leptonPF04ChargedHadronIso;PF04ChargedHadronIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonPF04ChargedHadronIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF04ChargedHadronIso_zoomed_stack)
#  leptonPF04NeutralHadronIso_zoomed_stack               = getStack(":leptonPF04NeutralHadronIso;PF04NeutralHadronIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonPF04NeutralHadronIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF04NeutralHadronIso_zoomed_stack)
#  leptonPF04PhotonIso_zoomed_stack               = getStack(":leptonPF04PhotonIso;PF04PhotonIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonPF04PhotonIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF04PhotonIso_zoomed_stack)
#  leptonPF04PUChargedHadronIso_zoomed_stack               = getStack(":leptonPF04PUChargedHadronIso;PF04PUChargedHadronIso;Number of Events",[21,0,2.1], commoncf, signalNumbers, topIsLargest)
#  leptonPF04PUChargedHadronIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF04PUChargedHadronIso_zoomed_stack)
#  leptonPF04RelIso_zoomed_stack               = getStack(":leptonPF04RelIso;PF04RelIso;Number of Events",[21,0,0.21], commoncf, signalNumbers, topIsLargest)
#  leptonPF04RelIso_zoomed_stack[0].data_histo.GetXaxis().SetLabelSize(0.04)
#  allStacks.append(leptonPF04RelIso_zoomed_stack)


#  lp_var = "-1 + 2*((leptonPt*cos(lepton_phi) + metpx)*(leptonPt*cos(lepton_phi)) + (leptonPt*sin(lepton_phi) + metpy)*(leptonPt*sin(lepton_phi)) )/((leptonPt*cos(lepton_phi) + metpx)**2 + (leptonPt*sin(lepton_phi) + metpy)**2)"
#  lp_stack = getStack(":"+lp_var+";L_{P};Number of Events",[42,-2.1,2.1], commoncf, signalNumbers, topIsLargest)
#  lp_stack[0].addOverFlowBin = "both"
#  allStacks.append(lp_stack)
#
#  lpMHT_var = "-1 + 2*((mhtpx)*(leptonPt*cos(lepton_phi)) + (mhtpy)*(leptonPt*sin(lepton_phi)) )/(mht**2)"
#  lpMHT_stack = getStack(":"+lpMHT_var+";L_{P, MHT};Number of Events",[42,-2.1,2.1], commoncf, signalNumbers, topIsLargest)
#  lpMHT_stack[0].addOverFlowBin = "both"
#  allStacks.append(lpMHT_stack)
#
#  edAngle_var = "(sqrt(16.0*leptonPt**2*((leptonPt*cos(lepton_phi) + metpx)**2 + (leptonPt*sin(lepton_phi) + metpy)**2)/(80.4**4) + 8.0*leptonPt**2/(80.4**2) - 1) - 2.0/(80.4**2)*sqrt(((leptonPt*cos(lepton_phi) + metpx)**2 + (leptonPt*sin(lepton_phi) + metpy)**2)*(80.4**2 + (leptonPt*cos(lepton_phi) + metpx)**2 + (leptonPt*sin(lepton_phi) + metpy)**2)))/(1. + (2./80.4**2)*((leptonPt*cos(lepton_phi) + metpx)**2 + (leptonPt*sin(lepton_phi) + metpy)**2))"
#  edAngle_stack = getStack(":"+edAngle_var+";#alpha_{Ed};Number of Events",[42,-2.1, 2.1], commoncf, signalNumbers, topIsLargest)
#  edAngle_stack[0].addOverFlowBin = "both"
#  allStacks.append(edAngle_stack)
#
#  edMHTAngle_var = "(sqrt(16.0*leptonPt**2*(mht**2)/(80.4**4) + 8.0*leptonPt**2/(80.4**2) - 1) - 2.0/(80.4**2)*sqrt((mht**2)*(80.4**2 + mht**2)))/(1. + (2./80.4**2)*(mht**2))"
#  edMHTAngle_stack = getStack(":"+edMHTAngle_var+";#alpha_{Ed,MHT};Number of Events",[42,-2.1, 2.1], commoncf, signalNumbers, topIsLargest)
#  edMHTAngle_stack[0].addOverFlowBin = "both"
#  allStacks.append(edMHTAngle_stack)

for stack in allStacks:
  stack[0].minimum = minimum
if not doOnlyMET:
  btag0_stack                   = getStack(":btag0;highest SSV_{HE};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
  allStacks.append(btag0_stack)
  btag1_stack                   = getStack(":btag1;2^{nd} highest SSV_{HE};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
  allStacks.append(btag1_stack)
#  btag2_stack                   = getStack(":btag2;n^{2}-leading SSV_{HE};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
#  btag2_stack[0].minimum = 10**(-2)
#  allStacks.append(btag2_stack)
  #jet0btag_stack                   = getStack(":jet0btag;SSV_{HE} of j_{0};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
  #jet0btag_stack[0].minimum = 10**(-2)
  #jet0btag_stack[0].legendCoordinates[0] = 0.25
  #jet0btag_stack[0].legendCoordinates[2] = 0.25+0.23
  #allStacks.append(jet0btag_stack)
  #jet1btag_stack                   = getStack(":jet1btag;SSV_{HE} of j_{1};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
  #jet1btag_stack[0].minimum = 10**(-2)
  #jet1btag_stack[0].legendCoordinates[0] = 0.25
  #jet1btag_stack[0].legendCoordinates[2] = 0.25+0.23
  #allStacks.append(jet1btag_stack)
  #jet2btag_stack                   = getStack(":jet2btag;SSV_{HE} of j_{2};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
  #jet2btag_stack[0].minimum = 10**(-2)
  #jet2btag_stack[0].legendCoordinates[0] = 0.25
  #jet2btag_stack[0].legendCoordinates[2] = 0.25+0.23
  #allStacks.append(jet2btag_stack)
  #jet3btag_stack                   = getStack(":jet3btag;SSV_{HE} of j_{2};Number of Events",[30,-1,6.], commoncf, signalNumbers, topIsLargest)
  #jet3btag_stack[0].minimum = 10**(-2)
  #jet3btag_stack[0].legendCoordinates[0] = 0.25
  #jet3btag_stack[0].legendCoordinates[2] = 0.25+0.23
  #allStacks.append(jet3btag_stack)

#for stack in allStacks:
#  for var in stack:
#    var.addOverFlowBin = "both"

#reweightingHistoFile = "PU/reweightingHisto_Summer2012-S10-Run2012ABC-PromptReco_JSONForSUSY.root"
#if useConvertedTuples:
reweightingHistoFile = ""

execfile("simplePlotsLoopKernel.py")
#execfile("simplePlotsKernel.py")

#c1 = ROOT.TCanvas("ROOT.c1","drawHistos",200,10,500,500)
#htmp=ngoodVertices_stack[-1].data_histo.Clone()
#htmp.Scale(1./htmp.Integral())
#htmp2 = ngoodVertices_stack[0].data_histo.Clone()
#htmp2.Scale(1./htmp2.Integral())
#htmp.Divide(htmp2)
#htmp.Draw()
#c1.Print("/afs/hephy.at/user/s/schoefbeck/www/8TeV/reweightingHisto_Summer2012-53X.png")
#tf = ROOT.TFile("/afs/hephy.at/user/s/schoefbeck/www/8TeV/reweightingHisto_Summer2012-53X.root", "recreate")
#tf.cd()
#htmp.Write()
#tf.Close()
#del c1
normalizeToData = False
if normalizeToData:
  for stack in allStacks:
    for var in stack[:-1]:
      var.normalizeTo = stack[-1]
      var.normalizeWhat = stack[0]
    stack[-1].normalizeTo=""
    stack[-1].normalizeWhat=""
else:
  for stack in allStacks:
    for var in stack:
      var.normalizeTo = ""
      var.normalizeWhat = "" 

defaultLines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1},  #sqrt{s} = 8 TeV"]]
for stack in allStacks:
  stack[0].maximum = 4*10**4 # 10.*stack[-1].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
  stack[0].legendCoordinates=[0.61,0.95 - 0.08*5,.98,.95]
  stack[0].lines = defaultLines 

#cosDeltaPhiLepMET_stack[0].maximum = 4*10**6

drawNMStacks(1,1,[met_stack],             subdir+prefix+"met", False)
#drawNMStacks(1,1,[mTbare_stack],              subdir+prefix+"mTbare", False)
#drawNMStacks(1,1,[cleanMT09_stack],              subdir+prefix+"cleanMT09", False)
#drawNMStacks(1,1,[cleanMT095_stack],              subdir+prefix+"cleanMT095", False)
#drawNMStacks(1,1,[cleanMT08_stack],              subdir+prefix+"cleanMT08", False)
#drawNMStacks(1,1,[cosDeltaPhiLepMET_stack],              subdir+prefix+"cosDeltaPhiLepMET", False)

if not doOnlyMET:
  drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT", False)
  drawNMStacks(1,1,[rawmet_stack],              subdir+prefix+"rawMET", False)
  drawNMStacks(1,1,[ngoodVertices_stack],             subdir+prefix+"ngoodVertices", False)
  drawNMStacks(1,1,[kinMetSig_stack],       subdir+prefix+"kinMetSig", False)
  drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht", False)
#  drawNMStacks(1,1,[ht2had_stack],          subdir+prefix+"ht2had", False)
#  drawNMStacks(1,1,[ht2_stack],             subdir+prefix+"ht2", False)
  drawNMStacks(1,1,[jet0_pt_stack],         subdir+prefix+"jet0_pt", False)
  drawNMStacks(1,1,[jet1_pt_stack],         subdir+prefix+"jet1_pt", False)
  drawNMStacks(1,1,[jet2_pt_stack],         subdir+prefix+"jet2_pt", False)
  drawNMStacks(1,1,[jet3_pt_stack],         subdir+prefix+"jet3_pt", False)
  drawNMStacks(1,1,[m3_stack],              subdir+prefix+"m3", False)
  drawNMStacks(1,1,[leptonPt_stack],       subdir+prefix+"leptonPt", False)
  drawNMStacks(1,1,[leptonEta_stack],                  subdir+prefix+"leptonEta", False)
  drawNMStacks(1,1,[ngoodElectrons_stack],  subdir+prefix+"ngoodElectrons", False)
  drawNMStacks(1,1,[ngoodMuons_stack],  subdir+prefix+"ngoodMuons", False)
  drawNMStacks(1,1,[nvetoElectrons_stack],  subdir+prefix+"nvetoElectrons", False)
  drawNMStacks(1,1,[nvetoMuons_stack],  subdir+prefix+"nvetoMuons", False)
  drawNMStacks(1,1,[nbtags_stack],             subdir+prefix+"nbtags", False)
  drawNMStacks(1,1,[njets_stack],             subdir+prefix+"njets", False)
  drawNMStacks(1,1,[btag0_stack],            subdir+prefix+"btag0", False)
  drawNMStacks(1,1,[btag1_stack],            subdir+prefix+"btag1", False)
  if useConvertedTuples:
    drawNMStacks(1,1,[phibb_stack],            subdir+prefix+"phibb", False)
    drawNMStacks(1,1,[mbl_stack],            subdir+prefix+"mbl", False)
    drawNMStacks(1,1,[mbb_stack],            subdir+prefix+"mbb", False)
    drawNMStacks(1,1,[mbbzoomed_stack],            subdir+prefix+"mbbzoomed", False)
  if not useConvertedTuples:
    drawNMStacks(1,1,[metiso_stack],             subdir+prefix+"metiso", False)
    drawNMStacks(1,1,[leptonRelIso_stack],               subdir+prefix+"leptonRelIso", False)
    drawNMStacks(1,1,[leptonRelIso_zoomed_stack],               subdir+prefix+"leptonRelIso_zoomed", False)
#  drawNMStacks(1,1,[leptonEcalIso_stack],               subdir+prefix+"leptonEcalIso", False)
#  drawNMStacks(1,1,[leptonEcalIso_zoomed_stack],               subdir+prefix+"leptonEcalIso_zoomed", False)
#  drawNMStacks(1,1,[leptonHcalIso_stack],               subdir+prefix+"leptonHcalIso", False)
#  drawNMStacks(1,1,[leptonHcalIso_zoomed_stack],               subdir+prefix+"leptonHcalIso_zoomed", False)
#  drawNMStacks(1,1,[leptonTrackIso_stack],               subdir+prefix+"leptonTrackIso", False)
#  drawNMStacks(1,1,[leptonTrackIso_zoomed_stack],               subdir+prefix+"leptonTrackIso_zoomed", False)
#  drawNMStacks(1,1,[leptonPF03ChargedHadronIso_stack], subdir+prefix+"leptonPF03ChargedHadronIso", False)
#  drawNMStacks(1,1,[leptonPF03NeutralHadronIso_stack], subdir+prefix+"leptonPF03NeutralHadronIso", False)
#  drawNMStacks(1,1,[leptonPF03PhotonIso_stack], subdir+prefix+"leptonPF03PhotonIso", False)
#  drawNMStacks(1,1,[leptonPF03PUChargedHadronIso_stack], subdir+prefix+"leptonPF03PUChargedHadronIso", False)
#  drawNMStacks(1,1,[leptonPF03RelIso_stack], subdir+prefix+"leptonPF03RelIso", False)
#  drawNMStacks(1,1,[leptonPF03ChargedHadronIso_zoomed_stack], subdir+prefix+"leptonPF03ChargedHadronIso_zoomed", False)
#  drawNMStacks(1,1,[leptonPF03NeutralHadronIso_zoomed_stack], subdir+prefix+"leptonPF03NeutralHadronIso_zoomed", False)
#  drawNMStacks(1,1,[leptonPF03PhotonIso_zoomed_stack], subdir+prefix+"leptonPF03PhotonIso_zoomed", False)
#  drawNMStacks(1,1,[leptonPF03PUChargedHadronIso_zoomed_stack], subdir+prefix+"leptonPF03PUChargedHadronIso_zoomed", False)
#  drawNMStacks(1,1,[leptonPF03RelIso_zoomed_stack], subdir+prefix+"leptonPF03RelIso_zoomed", False)
#  drawNMStacks(1,1,[leptonPF04ChargedHadronIso_stack], subdir+prefix+"leptonPF04ChargedHadronIso", False)
#  drawNMStacks(1,1,[leptonPF04NeutralHadronIso_stack], subdir+prefix+"leptonPF04NeutralHadronIso", False)
#  drawNMStacks(1,1,[leptonPF04PhotonIso_stack], subdir+prefix+"leptonPF04PhotonIso", False)
#  drawNMStacks(1,1,[leptonPF04PUChargedHadronIso_stack], subdir+prefix+"leptonPF04PUChargedHadronIso", False)
#  drawNMStacks(1,1,[leptonPF04RelIso_stack], subdir+prefix+"leptonPF04RelIso", False)
#  drawNMStacks(1,1,[leptonPF04ChargedHadronIso_zoomed_stack], subdir+prefix+"leptonPF04ChargedHadronIso_zoomed", False)
#  drawNMStacks(1,1,[leptonPF04NeutralHadronIso_zoomed_stack], subdir+prefix+"leptonPF04NeutralHadronIso_zoomed", False)
#  drawNMStacks(1,1,[leptonPF04PhotonIso_zoomed_stack], subdir+prefix+"leptonPF04PhotonIso_zoomed", False)
#  drawNMStacks(1,1,[leptonPF04PUChargedHadronIso_zoomed_stack], subdir+prefix+"leptonPF04PUChargedHadronIso_zoomed", False)
#  drawNMStacks(1,1,[leptonPF04RelIso_zoomed_stack], subdir+prefix+"leptonPF04RelIso_zoomed", False)

    drawNMStacks(1,1,[leptonDeltaR_stack],               subdir+prefix+"leptonDeltaR", False)
    drawNMStacks(1,1,[leptonDxy_stack],                  subdir+prefix+"leptonDxy", False)
    drawNMStacks(1,1,[leptonVertexDxy_stack],                  subdir+prefix+"leptonVertexDxy", False)
    drawNMStacks(1,1,[leptonVertexDz_stack],            subdir+prefix+"leptonVertexDz", False)
#  drawNMStacks(1,1,[lp_stack],              subdir+prefix+"lp", False)
#  drawNMStacks(1,1,[edAngle_stack],              subdir+prefix+"edAngle", False)
#  drawNMStacks(1,1,[lpMHT_stack],              subdir+prefix+"lpMHT", False)
#  drawNMStacks(1,1,[edMHTAngle_stack],              subdir+prefix+"edMHTAngle", False)
#drawNMStacks(1,1,[btag2_stack],            subdir+prefix+"btag2", False)
#drawNMStacks(1,1,[jet0btag_stack],         subdir+prefix+"jet0btag", False)
#drawNMStacks(1,1,[jet1btag_stack],         subdir+prefix+"jet1btag", False)
#drawNMStacks(1,1,[jet2btag_stack],         subdir+prefix+"jet2btag", False)
#drawNMStacks(1,1,[jet3btag_stack],         subdir+prefix+"jet3btag", False)

for stack in allStacks:
  stack[0].maximum = 1.3*stack[-1].data_histo.GetMaximum()
  stack[0].logy = False
  stack[0].minumum=0

#cosDeltaPhiLepMET_stack[0].maximum = 2*cosDeltaPhiLepMET_stack[-1].data_histo.GetMaximum() 

#drawNMStacks(1,1,[ht_stack],             subdir+prefix+"ht_lin", False)
#drawNMStacks(1,1,[btag0mass_stack], subdir+prefix+"btag0mass_stack_lin", False)
#drawNMStacks(1,1,[btag1mass_stack], subdir+prefix+"btag1mass_stack_lin", False)
#drawNMStacks(1,1,[btag2mass_stack], subdir+prefix+"btag2mass_stack_lin", False)
#drawNMStacks(1,1,[btag3mass_stack], subdir+prefix+"btag3mass_stack_lin", False)
#drawNMStacks(1,1,[njets_stack],             subdir+prefix+"njets_lin", False)
#drawNMStacks(1,1,[leptonRelIso_highnjet_stack], subdir+prefix+"relIso_highnjet_lin", False) 
#drawNMStacks(1,1,[leptonRelIso_lownjet_stack], subdir+prefix+"relIso_lownjet_lin", False) 
#drawNMStacks(1,1,[lepton_EcalIso_highnjet_stack], subdir+prefix+"EcalIso_highnjet_lin", False) 
#drawNMStacks(1,1,[lepton_EcalIso_lownjet_stack], subdir+prefix+"EcalIso_lownjet_lin", False) 
#drawNMStacks(1,1,[lepton_HcalIso_highnjet_stack], subdir+prefix+"HcalIso_highnjet_lin", False) 
#drawNMStacks(1,1,[lepton_HcalIso_lownjet_stack], subdir+prefix+"HcalIso_lownjet_lin", False) 
#drawNMStacks(1,1,[lepton_TrackIso_highnjet_stack], subdir+prefix+"TrackIso_highnjet_lin", False) 
#drawNMStacks(1,1,[lepton_TrackIso_lownjet_stack], subdir+prefix+"TrackIso_lownjet_lin", False) 
#drawNMStacks(1,1,[leptonDeltaR_stack], subdir+prefix+"deltaR_lin", False) 
#drawNMStacks(1,1,[leptonDeltaR_highnjet_stack], subdir+prefix+"deltaR_highnjet_lin", False) 
#drawNMStacks(1,1,[leptonDeltaR_lownjet_stack], subdir+prefix+"deltaR_lownjet_lin", False) 
#drawNMStacks(1,1,[ngoodUncleanedJets_stack],  subdir+prefix+"ngoodUncleanedJets_lin", False) 
#drawNMStacks(1,1,[ngoodEleCleanedJets_stack], subdir+prefix+"ngoodEleCleanedJets_lin", False) 
#drawNMStacks(1,1,[nbtags_stack],             subdir+prefix+"nbtags_lin", False)
#drawNMStacks(1,1,[metratio_stack],             subdir+prefix+"metratio_lin", False)
#drawNMStacks(1,1,[lepton_RPratioPt_stack],             subdir+prefix+"lepton_RPratioPt_stack_lin", False)
#drawNMStacks(1,1,[metiso_stack],             subdir+prefix+"metiso_lin", False)
#drawNMStacks(1,1,[jlb_stack],             subdir+prefix+"jlb_lin", False)
#drawNMStacks(1,1,[lepton_coarseEta_stack],                  subdir+prefix+"lepton_coarseEta", False)
#drawNMStacks(1,1,[jet0_JEC_stack],         subdir+prefix+"jet0_JEC_lin", False)
#drawNMStacks(1,1,[jet1_JEC_stack],         subdir+prefix+"jet1_JEC_lin", False)
#drawNMStacks(1,1,[jet2_JEC_stack],         subdir+prefix+"jet2_JEC_lin", False)
#drawNMStacks(1,1,[jet3_JEC_stack],         subdir+prefix+"jet3_JEC_lin", False)
drawNMStacks(1,1,[met_stack],             subdir+prefix+"met_lin", False)
#drawNMStacks(1,1,[mTbare_stack],              subdir+prefix+"mTbare_lin", False)
#drawNMStacks(1,1,[cleanMT09_stack],              subdir+prefix+"cleanMT09_lin", False)
#drawNMStacks(1,1,[cleanMT095_stack],              subdir+prefix+"cleanMT095_lin", False)
#drawNMStacks(1,1,[cleanMT08_stack],              subdir+prefix+"cleanMT08_lin", False)
#drawNMStacks(1,1,[cosDeltaPhiLepMET_stack],              subdir+prefix+"cosDeltaPhiLepMET_lin", False)

if not doOnlyMET:
  drawNMStacks(1,1,[mT_stack],              subdir+prefix+"mT_lin", False)
  drawNMStacks(1,1,[rawmet_stack],              subdir+prefix+"rawMET_lin", False)
  drawNMStacks(1,1,[ngoodVertices_stack],             subdir+prefix+"ngoodVertices_lin", False)
  drawNMStacks(1,1,[kinMetSig_stack],       subdir+prefix+"kinMetSig_lin", False)
  drawNMStacks(1,1,[ht_stack],              subdir+prefix+"ht_lin", False)
#  drawNMStacks(1,1,[ht2had_stack],          subdir+prefix+"ht2had_lin", False)
#  drawNMStacks(1,1,[ht2_stack],             subdir+prefix+"ht2_lin", False)
  drawNMStacks(1,1,[jet0_pt_stack],         subdir+prefix+"jet0_pt_lin", False)
  drawNMStacks(1,1,[jet1_pt_stack],         subdir+prefix+"jet1_pt_lin", False)
  drawNMStacks(1,1,[jet2_pt_stack],         subdir+prefix+"jet2_pt_lin", False)
  drawNMStacks(1,1,[jet3_pt_stack],         subdir+prefix+"jet3_pt_lin", False)
  drawNMStacks(1,1,[m3_stack],              subdir+prefix+"m3_lin", False)
  drawNMStacks(1,1,[leptonPt_stack],       subdir+prefix+"leptonPt_lin", False)
  drawNMStacks(1,1,[leptonEta_stack],                  subdir+prefix+"leptonEta_lin", False)
#  drawNMStacks(1,1,[ptw_stack],             subdir+prefix+"ptw_lin", False)
  drawNMStacks(1,1,[ngoodElectrons_stack],  subdir+prefix+"ngoodElectrons_lin", False)
  drawNMStacks(1,1,[ngoodMuons_stack],  subdir+prefix+"ngoodMuons_lin", False)
  drawNMStacks(1,1,[nvetoElectrons_stack],  subdir+prefix+"nvetoElectrons_lin", False)
  drawNMStacks(1,1,[nvetoMuons_stack],  subdir+prefix+"nvetoMuons_lin", False)
  drawNMStacks(1,1,[nbtags_stack],             subdir+prefix+"nbtags_lin", False)
  drawNMStacks(1,1,[njets_stack],             subdir+prefix+"njets_lin", False)
#  if useConvertedTuples:
#    drawNMStacks(1,1,[phibb_stack],            subdir+prefix+"phibb_lin", False)
#    drawNMStacks(1,1,[mbl_stack],            subdir+prefix+"mbl_lin", False)
#    drawNMStacks(1,1,[mbb_stack],            subdir+prefix+"mbb_lin", False)
#    drawNMStacks(1,1,[mbbzoomed_stack],            subdir+prefix+"mbbzoomed_lin", False)
#  if not useConvertedTuples:
#    drawNMStacks(1,1,[metiso_stack],             subdir+prefix+"metiso_lin", False)
#    drawNMStacks(1,1,[leptonRelIso_stack],               subdir+prefix+"leptonRelIso_lin", False)
#    drawNMStacks(1,1,[leptonRelIso_zoomed_stack],               subdir+prefix+"leptonRelIso_zoomed_lin", False)
#    drawNMStacks(1,1,[leptonDeltaR_stack], subdir+prefix+"deltaR_lin", False) 
  #  drawNMStacks(1,1,[leptonEcalIso_stack],               subdir+prefix+"leptonEcalIso_lin", False)
  #  drawNMStacks(1,1,[leptonEcalIso_zoomed_stack],               subdir+prefix+"leptonEcalIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonHcalIso_stack],               subdir+prefix+"leptonHcalIso_lin", False)
  #  drawNMStacks(1,1,[leptonHcalIso_zoomed_stack],               subdir+prefix+"leptonHcalIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonTrackIso_stack],               subdir+prefix+"leptonTrackIso_lin", False)
  #  drawNMStacks(1,1,[leptonTrackIso_zoomed_stack],               subdir+prefix+"leptonTrackIso_zoomed_lin", False)
  #
  #  drawNMStacks(1,1,[leptonPF03ChargedHadronIso_stack], subdir+prefix+"leptonPF03ChargedHadronIso_lin", False)
  #  drawNMStacks(1,1,[leptonPF03NeutralHadronIso_stack], subdir+prefix+"leptonPF03NeutralHadronIso_lin", False)
  #  drawNMStacks(1,1,[leptonPF03PhotonIso_stack], subdir+prefix+"leptonPF03PhotonIso_lin", False)
  #  drawNMStacks(1,1,[leptonPF03PUChargedHadronIso_stack], subdir+prefix+"leptonPF03PUChargedHadronIso_lin", False)
  #  drawNMStacks(1,1,[leptonPF03RelIso_stack], subdir+prefix+"leptonPF03RelIso_lin", False)
  #  drawNMStacks(1,1,[leptonPF03ChargedHadronIso_zoomed_stack], subdir+prefix+"leptonPF03ChargedHadronIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonPF03NeutralHadronIso_zoomed_stack], subdir+prefix+"leptonPF03NeutralHadronIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonPF03PhotonIso_zoomed_stack], subdir+prefix+"leptonPF03PhotonIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonPF03PUChargedHadronIso_zoomed_stack], subdir+prefix+"leptonPF03PUChargedHadronIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonPF03RelIso_zoomed_stack], subdir+prefix+"leptonPF03RelIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonPF04ChargedHadronIso_stack], subdir+prefix+"leptonPF04ChargedHadronIso_lin", False)
  #  drawNMStacks(1,1,[leptonPF04NeutralHadronIso_stack], subdir+prefix+"leptonPF04NeutralHadronIso_lin", False)
  #  drawNMStacks(1,1,[leptonPF04PhotonIso_stack], subdir+prefix+"leptonPF04PhotonIso_lin", False)
  #  drawNMStacks(1,1,[leptonPF04PUChargedHadronIso_stack], subdir+prefix+"leptonPF04PUChargedHadronIso_lin", False)
  #  drawNMStacks(1,1,[leptonPF04RelIso_stack], subdir+prefix+"leptonPF04RelIso_lin", False)
  #  drawNMStacks(1,1,[leptonPF04ChargedHadronIso_zoomed_stack], subdir+prefix+"leptonPF04ChargedHadronIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonPF04NeutralHadronIso_zoomed_stack], subdir+prefix+"leptonPF04NeutralHadronIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonPF04PhotonIso_zoomed_stack], subdir+prefix+"leptonPF04PhotonIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonPF04PUChargedHadronIso_zoomed_stack], subdir+prefix+"leptonPF04PUChargedHadronIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonPF04RelIso_zoomed_stack], subdir+prefix+"leptonPF04RelIso_zoomed_lin", False)
  #  drawNMStacks(1,1,[leptonDeltaR_stack],               subdir+prefix+"leptonDeltaR_lin", False)
  #  drawNMStacks(1,1,[leptonDxy_stack],                  subdir+prefix+"leptonDxy_lin", False)
  #  drawNMStacks(1,1,[leptonVertexDxy_stack],                  subdir+prefix+"leptonVertexDxy_lin", False)
  #  drawNMStacks(1,1,[leptonVertexDz_stack],            subdir+prefix+"leptonVertexDz_lin", False)

  #  drawNMStacks(1,1,[lp_stack],              subdir+prefix+"lp_lin", False)
  #  drawNMStacks(1,1,[edAngle_stack],              subdir+prefix+"edAngle_lin", False)
  #  drawNMStacks(1,1,[lpMHT_stack],              subdir+prefix+"lpMHT_lin", False)
  #  drawNMStacks(1,1,[edMHTAngle_stack],              subdir+prefix+"edMHTAngle_lin", False)
