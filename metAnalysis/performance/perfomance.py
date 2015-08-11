import ROOT
from array import array
from math import sqrt, cosh, cos, sin
import os, copy, sys
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getObjDict
from Workspace.HEPHYPythonTools.xsec import xsec
from Workspace.RA4Analysis.helpers import *

from Workspace.RA4Analysis.cmgTuples_Spring15 import *

lumi=100.
small = True
samples=[ 
  {"name":"DY", "bins":[DYJetsToLL_M_50], "title":"Drell-Yan"}
]

nvtxBinning=[0,50]
qtBinning=range(0,100,10)
variables = [
#  {"name":"nVert", "func":lambda c:getVarValue(c,"nVert"), "title":"vertex multiplicity", "binning":nvtxBinning},
  {"name":"qt", "func":"qt", "title":"q_{T} (GeV)", "binning":qtBinning}
]
metVariables = [
  {'name':'type1','ptFunc':lambda c:getVarValue(c,"met_pt"), 'phiFunc':lambda c:getVarValue(c,"met_phi")}
]

for v in variables:
  v['bins']=[(v["binning"][i],v["binning"][i+1]) for i in range(len(v["binning"])-1)]
  v['uperp']={}
  v['upara']={}
  v['qt']={}
  v['histo']={}
  for mv in metVariables:
    hname = '_'.join(v['name'],mv['name'])
    v['histo'][mv['name']]=ROOT.TH1D('histo_'+hname, 'histo_'+hname, len(v['binning'])-1, array('d',v['binning']))

    v['upara'][mv['name']]={}
    v['uperp'][mv['name']]={}
    v['upara'][mv['name']]["scale"] = ROOT.TH1D(hname+'_upara_scale', hname+'_upara_scale',len(v['binning'])-1, array('d',v['binning']))
#    v['upara'][mv['name']]["scale"] = ROOT.TH1D(hname+'_upara_scale', hname+'_upara_scale',len(v['binning'])-1, array('d',v['binning']))
    v['upara'][mv['name']]["RMS"] = ROOT.TH1D(hname+'_upara_RMS', hname+'_upara_RMS',len(v['binning'])-1, array('d',v['binning']))
    v['uperp'][mv['name']]["RMS"] = ROOT.TH1D(hname+'_uperp_RMS', hname+'_uperp_RMS',len(v['binning'])-1, array('d',v['binning']))
    v['upara'][mv['name']]["RMScorr"] = ROOT.TH1D(hname+'_upara_RMScorr', hname+'_upara_RMScorr',len(v['binning'])-1, array('d',v['binning']))
    v['uperp'][mv['name']]["RMScorr"] = ROOT.TH1D(hname+'_uperp_RMScorr', hname+'_uperp_RMScorr',len(v['binning'])-1, array('d',v['binning']))
    for b in v['bins']:
      hname = v['name']+'_'.join([str(x) for x in b])
      v['uperp'][mv['name']][b] = ROOT.TH1D(hname+'_'+mv['name']+'_uperp', hname+'_'+mv['name']+'_uperp', 400,-200,200) 
      v['upara'][mv['name']][b] = ROOT.TH1D(hname+'_'+mv['name']+'_upara', hname+'_'+mv['name']+'_upara', 500,-400,100) 
      v['qt'][mv['name']][b] = ROOT.TH1D(hname+'_'+mv['name']+'_qt', hname+'_'+mv['name']+'_qt', 500,0,500) 
  
for s in samples:
  totalYield=0
  for b in s["bins"]:
    chunks, sumWeight = getChunks(b)
#    print "Chunks:" , chunks
    lumiScale = xsec[b['dbsName']]*lumi/float(sumWeight)

    b["lumiScale"] = lumiScale
    b["chain"]     = getChain(chunks,  histname="", treeName = b["treeName"])
    print b["name"],"xsec",xsec[b['dbsName']],"sumWeight",sumWeight

def findBin(v, varValue):
  for b in v['bins']:
    if varValue>=b[0] and varValue<b[1]:
      return b

def getMass(l0,l1):
  return sqrt(2.*l0['pt']*l1['pt']*(cosh(l0['eta']-l1['eta']) - cos(l0['phi']-l1['phi'])))

def looseMuID(l):
  return l["pt"]>=20 and l["eta"]<2.1 and l["mediumMuonId"]==1 and l["miniRelIso"]<0.4 and l["sip3d"]<4.0

#def mvaEleIdEta(l):
#  if abs(l["eta"]) < 0.8 and l["mvaIdPhys14"] > 0.35 : return True
#  elif abs(l["eta"]) > 0.8 and abs(l["eta"]) < 1.44 and l["mvaIdPhys14"] > 0.20 : return True
#  elif abs(l["eta"]) > 1.57 and l["mvaIdPhys14"] > -0.52 : return True
#  return False
#
#def looseEleID(l):
#  return l["pt"]>=20 and (abs(l["eta"])<1.44 or abs(l["eta"])>1.57) and abs(l["eta"])<2.4 and l["miniRelIso"]<0.4 and mvaEleIdEta(l) and l["lostHits"]<=1 and l["convVeto"] and l["sip3d"] < 4.0

def getMuons(c):
  leptons = [getObjDict(c, "LepGood_", ["pt", "eta", "phi", "dxy", "dz", "relIso03", "mediumMuonId", "pdgId", "miniRelIso", "sip3d"], i) for i in range(int(getVarValue(c,'nLepGood')))]
  return [l for l in leptons if abs(l["pdgId"])==13 and looseMuID(l)]

presel = "1"
dilepton = "Sum$(LepGood_pt>20&&LepGood_mediumMuonId==1)>=2" 

cut = "&&".join(['('+x+')' for x in [presel, dilepton]])
for s in samples:
  for b in s['bins']:
    b['chain'].Draw('>>eList', cut)
    eList = ROOT.gDirectory.Get('eList')
    nEvents = eList.GetN() if not small else 10000
    for nev in range(nEvents):
      if nev%1000==0:print "At %i / %i"%(nev, nEvents)
      b['chain'].GetEntry(eList.GetEntry(nev))
      muons = getMuons(b['chain'])
      if len(muons)!=2:continue
      l0, l1 = muons
      mll = getMass(l0,l1)
      if not abs(mll-90.2)<15.:continue
      qx = l0['pt']*cos(l0['phi']) + l1['pt']*cos(l1['phi'])  
      qy = l0['pt']*sin(l0['phi']) + l1['pt']*cos(l1['phi']) 
#      qphi = atan2(qy, qx)
      qt = sqrt(qx**2+qy**2)
#      print l0, l1
      for mv in metVariables:
        mv['pt'] = mv['ptFunc'](b['chain']) 
        mv['phi'] = mv['phiFunc'](b['chain'])
        ux = -mv['pt']*cos(mv['phi']) - qx 
        uy = -mv['pt']*sin(mv['phi']) - qy
        upara = (ux*qx+uy*qy)/qt
        uperp = (ux*qy-uy*qx)/qt
        weight = getVarValue(b['chain'], 'genWeight')*lumiScale
        for v in variables:
          if v['func']=='qt':varValue=qt
          else:
            varValue = v['func'](b['chain'])
          v['histo'][mv['name']].Fill(varValue, weight)         #Filling distribution of binning variable
          varBin = findBin(v, varValue)
          if varBin: 
            v['uperp'][mv['name']][varBin].Fill(uperp, weight) 
            v['upara'][mv['name']][varBin].Fill(upara, weight) 
            v['upara'][mv['name']][varBin].Fill(qt, weight) 
  del eList

for v in variables:
  for mv in metVariables:
    for b in v['bins']:
      upara_mean      = v['upara'][mv['name']][b].GetMean()
      upara_mean_err  = v['upara'][mv['name']][b].GetMeanError()
      uperp_mean      = v['uperp'][mv['name']][b].GetMean()
      uperp_mean_err  = v['uperp'][mv['name']][b].GetMeanError()
      upara_RMS      = v['upara'][mv['name']][b].GetRMS()
      upara_RMS_err  = v['upara'][mv['name']][b].GetRMSError()
      uperp_RMS      = v['uperp'][mv['name']][b].GetRMS()
      uperp_RMS_err  = v['uperp'][mv['name']][b].GetRMSError()
      qt_mean       = v['upara'][mv['name']][varBin].GetMean()
      qt_mean_err   = v['upara'][mv['name']][varBin].GetMeanError()
      scale         =  - upara_mean / qt_mean 
      scale_err     =  upara_mean / qt_mean * sqrt(upara_mean_err**2/upara_mean**2 + qt_mean_err**2/qt_mean**2)
      upara_RMS_scaleCorr       =  upara_RMS/scale
      upara_RMS_scaleCorr_err   =  upara_RMS/scale*sqrt(upara_RMS_err**2/upara_RMS**2 + scale_err**2/scale**2)
      uperp_RMS_scaleCorr       =  uperp_RMS/scale
      uperp_RMS_scaleCorr_err   =  uperp_RMS/scale*sqrt(uperp_RMS_err**2/uperp_RMS**2 + scale_err**2/scale**2)
      val = 0.5*(b[0]+b[1])
      nbin = v['upara'][mv['name']]["scale"].FindBin(val)
      v['upara'][mv['name']]["scale"].SetBinContent(nbin, scale)
      v['upara'][mv['name']]["scale"].SetBinContentError(nbin, scale_err)
      v['upara'][mv['name']]["RMS"].SetBinContent(nbin, upara_RMS)
      v['upara'][mv['name']]["RMS"].SetBinContentError(nbin, upara_RMS_err)
      v['upara'][mv['name']]["RMScorr"].SetBinContent(nbin, upara_RMS_scaleCorr)
      v['upara'][mv['name']]["RMScorr"].SetBinContentError(nbin, upara_RMS_scaleCorr_err)
      v['uperp'][mv['name']]["RMS"].SetBinContent(nbin, uperp_RMS)
      v['uperp'][mv['name']]["RMS"].SetBinContentError(nbin, uperp_RMS_err)
      v['uperp'][mv['name']]["RMScorr"].SetBinContent(nbin, uperp_RMS_scaleCorr)
      v['uperp'][mv['name']]["RMScorr"].SetBinContentError(nbin, uperp_RMS_scaleCorr_err)
 
# OBJ: TBranch LepOther_charge charge for Leptons after the preselection : 0 at: 0x4e11dc0
# OBJ: TBranch LepOther_tightId  POG Tight ID (for electrons it's configured in the analyzer) for Leptons after the preselection : 0 at: 0x4e129a0
# OBJ: TBranch LepOther_eleCutIdCSA14_25ns_v1  Electron cut-based id (POG CSA14_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight for Leptons after the preselection : 0 at: 0x4e135d0
# OBJ: TBranch LepOther_eleCutIdCSA14_50ns_v1  Electron cut-based id (POG CSA14_50ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight for Leptons after the preselection : 0 at: 0x4e14230
# OBJ: TBranch LepOther_dxy  d_{xy} with respect to PV, in cm (with sign) for Leptons after the preselection : 0 at: 0x4e14e90
# OBJ: TBranch LepOther_dz d_{z} with respect to PV, in cm (with sign) for Leptons after the preselection : 0 at: 0x4e15a50
# OBJ: TBranch LepOther_edxy #sigma(d_{xy}) with respect to PV, in cm for Leptons after the preselection : 0 at: 0x4e16610
# OBJ: TBranch LepOther_edz  #sigma(d_{z}) with respect to PV, in cm for Leptons after the preselection : 0 at: 0x4e171d0
# OBJ: TBranch LepOther_ip3d d_{3d} with respect to PV, in cm (absolute value) for Leptons after the preselection : 0 at: 0x4e17d90
# OBJ: TBranch LepOther_sip3d  S_{ip3d} with respect to PV (significance) for Leptons after the preselection : 0 at: 0x4e18960
# OBJ: TBranch LepOther_convVeto Conversion veto (always true for muons) for Leptons after the preselection : 0 at: 0x4d21d80
# OBJ: TBranch LepOther_lostHits Number of lost hits on inner track for Leptons after the preselection : 0 at: 0x4d229a0
# OBJ: TBranch LepOther_relIso03 PF Rel Iso, R=0.3, pile-up corrected for Leptons after the preselection : 0 at: 0x4d235c0
# OBJ: TBranch LepOther_relIso04 PF Rel Iso, R=0.4, pile-up corrected for Leptons after the preselection : 0 at: 0x4d241e0
# OBJ: TBranch LepOther_miniRelIso PF Rel miniRel, pile-up corrected for Leptons after the preselection : 0 at: 0x4d24e00
# OBJ: TBranch LepOther_tightCharge  Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, 2 if ptError/pt < 0.20, 0 otherwise  for Leptons after the preselection : 0 at: 0x4d25a20
# OBJ: TBranch LepOther_mcMatchId  Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake for Leptons after the preselection : 0 at: 0x4d266c0
# OBJ: TBranch LepOther_mcMatchAny Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom for Leptons after the preselection : 0 at: 0x4e249e0
# OBJ: TBranch LepOther_mcMatchTau True if the leptons comes from a tau for Leptons after the preselection : 0 at: 0x4e25630
# OBJ: TBranch LepOther_mcPt p_{T} of associated gen lepton for Leptons after the preselection : 0 at: 0x4e26250
# OBJ: TBranch LepOther_mediumMuonId Muon POG Medium id for Leptons after the preselection : 0 at: 0x4e26e10
# OBJ: TBranch LepOther_pdgId  pdgId for Leptons after the preselection : 0 at: 0x4e27a30
# OBJ: TBranch LepOther_pt pt for Leptons after the preselection : 0 at: 0x4e285d0
# OBJ: TBranch LepOther_eta  eta for Leptons after the preselection : 0 at: 0x4e29170
# OBJ: TBranch LepOther_phi  phi for Leptons after the preselection : 0 at: 0x4e29d10
# OBJ: TBranch LepOther_mass mass for Leptons after the preselection : 0 at: 0x4e2a8b0
# OBJ: TBranch LepOther_mvaIdPhys14  EGamma POG MVA ID for non-triggering electrons, Phys14 re-training; 1 for muons for Leptons after the preselection : 0 at: 0x4e2b450
# OBJ: TBranch LepOther_mvaTTH Lepton MVA (TTH version) for Leptons after the preselection : 0 at: 0x4e2c0a0
# OBJ: TBranch LepOther_mvaSusy  Lepton MVA (SUSY version) for Leptons after the preselection : 0 at: 0x4e2cc90
# OBJ: TBranch LepOther_jetPtRatio pt(lepton)/pt(nearest jet) for Leptons after the preselection : 0 at: 0x4e2d8a0
# OBJ: TBranch LepOther_jetPtRel pt of the lepton transverse to the jet axis (subtracting the lepton) for Leptons after the preselection : 0 at: 0x4e2e4b0
# OBJ: TBranch LepOther_jetBTagCSV CSV btag of nearest jet for Leptons after the preselection : 0 at: 0x4e2f0f0
# OBJ: TBranch LepOther_jetBTagCMVA  CMA btag of nearest jet for Leptons after the preselection : 0 at: 0x4e2fd00
# OBJ: TBranch LepOther_jetDR  deltaR(lepton, nearest jet) for Leptons after the preselection : 0 at: 0x4e30910

#OBJ: TObjArray  TObjArray An array of objects : 0
# OBJ: TBranch run run/i : 0 at: 0x4d38c60
# OBJ: TBranch lumi  lumi/i : 0 at: 0x4d44c20
# OBJ: TBranch evt evt/l : 0 at: 0x4d45270
# OBJ: TBranch isData  isData/I : 0 at: 0x4d47530
# OBJ: TBranch xsec  xsec/F : 0 at: 0x4d47d30
# OBJ: TBranch puWeight  puWeight/F : 0 at: 0x4d49f10
# OBJ: TBranch nTrueInt  nTrueInt/I : 0 at: 0x4d4a710
# OBJ: TBranch genWeight genWeight/F : 0 at: 0x4d4af10
# OBJ: TBranch rho kt6PFJets rho : 0 at: 0x4d4b710
# OBJ: TBranch nVert Number of good vertices : 0 at: 0x4d4bf10
# OBJ: TBranch nJet25  Number of jets with pt > 25 : 0 at: 0x4d4c710
# OBJ: TBranch nBJetLoose25  Number of jets with pt > 25 passing CSV loose : 0 at: 0x4d4cf10
# OBJ: TBranch nBJetMedium25 Number of jets with pt > 25 passing CSV medium : 0 at: 0x4d4d730
# OBJ: TBranch nBJetTight25  Number of jets with pt > 25 passing CSV tight : 0 at: 0x4d4df90
# OBJ: TBranch nJet30  Number of jets with pt > 30, |eta|<2.4 : 0 at: 0x4d4e7f0
# OBJ: TBranch nJet30a Number of jets with pt > 30, |eta|<4.7 : 0 at: 0x4d4f050
# OBJ: TBranch nBJetLoose30  Number of jets with pt > 30 passing CSV loose : 0 at: 0x4d4f8b0
# OBJ: TBranch nBJetMedium30 Number of jets with pt > 30 passing CSV medium : 0 at: 0x4d50110
# OBJ: TBranch nBJetTight30  Number of jets with pt > 30 passing CSV tight : 0 at: 0x4d50970
# OBJ: TBranch nJet40  Number of jets with pt > 40, |eta|<2.4 : 0 at: 0x4d511d0
# OBJ: TBranch nJet40a Number of jets with pt > 40, |eta|<4.7 : 0 at: 0x4d51a30
# OBJ: TBranch nBJetLoose40  Number of jets with pt > 40 passing CSV loose : 0 at: 0x4d52290
# OBJ: TBranch nBJetMedium40 Number of jets with pt > 40 passing CSV medium : 0 at: 0x4d52af0
# OBJ: TBranch nBJetTight40  Number of jets with pt > 40 passing CSV tight : 0 at: 0x4d53350
# OBJ: TBranch nLepGood20  Number of leptons with pt > 20 : 0 at: 0x4d53bb0
# OBJ: TBranch nLepGood15  Number of leptons with pt > 15 : 0 at: 0x4d54400
# OBJ: TBranch nLepGood10  Number of leptons with pt > 10 : 0 at: 0x4d54c50
# OBJ: TBranch GenSusyMScan1 Susy mass 1 in scan : 0 at: 0x4d554a0
# OBJ: TBranch GenSusyMScan2 Susy mass 2 in scan : 0 at: 0x4d55cf0
# OBJ: TBranch GenSusyMScan3 Susy mass 3 in scan : 0 at: 0x4d56540
# OBJ: TBranch GenSusyMScan4 Susy mass 4 in scan : 0 at: 0x4d56d90
# OBJ: TBranch GenSusyMGluino  Susy Gluino mass : 0 at: 0x4d575e0
# OBJ: TBranch GenSusyMGravitino Susy Gravitino mass : 0 at: 0x4d57e30
# OBJ: TBranch GenSusyMStop  Susy Stop mass : 0 at: 0x4d58710
# OBJ: TBranch GenSusyMSbottom Susy Sbottom mass : 0 at: 0x4d58f30
# OBJ: TBranch GenSusyMStop2 Susy Stop2 mass : 0 at: 0x4d597e0
# OBJ: TBranch GenSusyMSbottom2  Susy Sbottom2 mass : 0 at: 0x4d5a020
# OBJ: TBranch GenSusyMSquark  Susy Squark mass : 0 at: 0x4d5a900
# OBJ: TBranch GenSusyMNeutralino  Susy Neutralino mass : 0 at: 0x4d5b150
# OBJ: TBranch GenSusyMNeutralino2 Susy Neutralino2 mass : 0 at: 0x4d5ba30
# OBJ: TBranch GenSusyMNeutralino3 Susy Neutralino3 mass : 0 at: 0x4d5c310
# OBJ: TBranch GenSusyMNeutralino4 Susy Neutralino4 mass : 0 at: 0x4d5cbf0
# OBJ: TBranch GenSusyMChargino  Susy Chargino mass : 0 at: 0x4d5d4d0
# OBJ: TBranch GenSusyMChargino2 Susy Chargino2 mass : 0 at: 0x4d5ddb0
# OBJ: TBranch htJet25 H_{T} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV) : 0 at: 0x4d5e690
# OBJ: TBranch mhtJet25  H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV) : 0 at: 0x4d5ef10
# OBJ: TBranch htJet40j  H_{T} computed from only jets (with |eta|<2.4, pt > 40 GeV) : 0 at: 0x4d5f790
# OBJ: TBranch htJet40 H_{T} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV) : 0 at: 0x4d60000
# OBJ: TBranch mhtJet40  H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV) : 0 at: 0x4d60880
# OBJ: TBranch nSoftBJetLoose25  Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with loose sv mva : 0 at: 0x4d61100
# OBJ: TBranch nSoftBJetMedium25 Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with medium sv mva : 0 at: 0x4d61a20
# OBJ: TBranch nSoftBJetTight25  Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with tight sv mva : 0 at: 0x4d62340
# OBJ: TBranch HLT_HT900 OR of ['HLT_PFHT900_v*'] : 0 at: 0x4d62c60
# OBJ: TBranch HLT_MuHT400B  OR of ['HLT_Mu15_IsoVVVL_BTagCSV07_PFHT400_v*'] : 0 at: 0x4d634b0
# OBJ: TBranch HLT_MuHad OR of ['HLT_Mu15_IsoVVVL_PFHT600_v*', 'HLT_Mu15_IsoVVVL_PFHT400_PFMET70_v*', 'HLT_PFMET120_NoiseCleaned_Mu5_v*', 'HLT_Mu15_IsoVVVL_BTagCSV07_PFHT400_v*'] : 0 at: 0x4d63d10
# OBJ: TBranch HLT_MuMET120  OR of ['HLT_PFMET120_NoiseCleaned_Mu5_v*'] : 0 at: 0x4d645e0
# OBJ: TBranch HLT_Mu45NoIso OR of ['HLT_Mu45_eta2p1_v*'] : 0 at: 0x4d64e40
# OBJ: TBranch HLT_HT350 OR of ['HLT_PFHT350_v*'] : 0 at: 0x4d65690
# OBJ: TBranch HLT_HT600 OR of ['HLT_PFHT600_v*'] : 0 at: 0x4d65ee0
# OBJ: TBranch HLT_HTMET OR of ['HLT_PFHT350_PFMET120_NoiseCleaned_v*'] : 0 at: 0x4d66730
# OBJ: TBranch HLT_Had OR of ['HLT_PFHT900_v*', 'HLT_PFMET170_NoiseCleaned_v*', 'HLT_PFHT350_PFMET120_NoiseCleaned_v*'] : 0 at: 0x4d66f90
# OBJ: TBranch HLT_MuHT400MET70  OR of ['HLT_Mu15_IsoVVVL_PFHT400_PFMET70_v*'] : 0 at: 0x4d67830
# OBJ: TBranch HLT_SingleMu  OR of ['HLT_IsoMu27_v*'] : 0 at: 0x4d68120
# OBJ: TBranch HLT_SingleEl  OR of ['HLT_Ele32_eta2p1_WP75_Gsf_v*', 'HLT_Ele32_eta2p1_WPLoose_Gsf_v*', 'HLT_Ele32_eta2p1_WPTight_Gsf_v*'] : 0 at: 0x4d68970
# OBJ: TBranch HLT_MET170  OR of ['HLT_PFMET170_NoiseCleaned_v*'] : 0 at: 0x4d69210
# OBJ: TBranch HLT_EleHT400MET70 OR of ['HLT_Ele15_IsoVVVL_PFHT400_PFMET70_v*'] : 0 at: 0x4d69a70
# OBJ: TBranch HLT_EleHT600  OR of ['HLT_Ele15_IsoVVVL_PFHT600_v*'] : 0 at: 0x4d6a360
# OBJ: TBranch HLT_ElHad OR of ['HLT_Ele15_IsoVVVL_PFHT600_v*', 'HLT_Ele15_IsoVVVL_PFHT400_PFMET70_v*', 'HLT_Ele27_eta2p1_WP85_Gsf_HT200_v*', 'HLT_Ele15_IsoVVVL_BTagtop8CSV07_PFHT400_v*'] : 0 at: 0x4d6abc0
# OBJ: TBranch HLT_ElHT400B  OR of ['HLT_Ele15_IsoVVVL_BTagtop8CSV07_PFHT400_v*'] : 0 at: 0x4d6b4a0
# OBJ: TBranch HLT_ElNoIso OR of ['HLT_Ele105_CaloIdVT_GsfTrkIdT_v*'] : 0 at: 0x4d6bd10
# OBJ: TBranch HLT_MuHT600 OR of ['HLT_Mu15_IsoVVVL_PFHT600_v*'] : 0 at: 0x4d6c570
# OBJ: TBranch HLT_EleHT200  OR of ['HLT_Ele27_eta2p1_WP85_Gsf_HT200_v*'] : 0 at: 0x4d6cdd0
# OBJ: TBranch HLT_Mu50NoIso OR of ['HLT_Mu50_v*'] : 0 at: 0x4d6d630
# OBJ: TBranch Flag_EcalDeadCellTriggerPrimitiveFilter OR of ['Flag_EcalDeadCellTriggerPrimitiveFilter'] : 0 at: 0x4d6de80
# OBJ: TBranch Flag_trkPOG_manystripclus53X  OR of ['Flag_trkPOG_manystripclus53X'] : 0 at: 0x4d6e7b0
# OBJ: TBranch Flag_ecalLaserCorrFilter  OR of ['Flag_ecalLaserCorrFilter'] : 0 at: 0x4d6f0a0
# OBJ: TBranch Flag_trkPOG_toomanystripclus53X OR of ['Flag_trkPOG_toomanystripclus53X'] : 0 at: 0x4d6f990
# OBJ: TBranch Flag_hcalLaserEventFilter OR of ['Flag_hcalLaserEventFilter'] : 0 at: 0x4d70280
# OBJ: TBranch Flag_trkPOG_logErrorTooManyClusters OR of ['Flag_trkPOG_logErrorTooManyClusters'] : 0 at: 0x4d70b70
# OBJ: TBranch Flag_trkPOGFilters  OR of ['Flag_trkPOGFilters'] : 0 at: 0x4d71490
# OBJ: TBranch Flag_trackingFailureFilter  OR of ['Flag_trackingFailureFilter'] : 0 at: 0x4d71d70
# OBJ: TBranch Flag_CSCTightHaloFilter OR of ['Flag_CSCTightHaloFilter'] : 0 at: 0x4d72660
# OBJ: TBranch Flag_HBHENoiseFilter  OR of ['Flag_HBHENoiseFilter'] : 0 at: 0x4d72f50
# OBJ: TBranch Flag_goodVertices OR of ['Flag_goodVertices'] : 0 at: 0x4d73830
# OBJ: TBranch Flag_METFilters OR of ['Flag_METFilters'] : 0 at: 0x4d74110
# OBJ: TBranch Flag_eeBadScFilter  OR of ['Flag_eeBadScFilter'] : 0 at: 0x4d749c0
# OBJ: TBranch met_pt  met_pt/F : 0 at: 0x4d752a0
# OBJ: TBranch met_eta met_eta/F : 0 at: 0x4d75ac0
# OBJ: TBranch met_phi met_phi/F : 0 at: 0x4d762e0
# OBJ: TBranch met_mass  met_mass/F : 0 at: 0x4d76b00
# OBJ: TBranch met_sumEt met_sumEt/F : 0 at: 0x4d77320
# OBJ: TBranch met_genPt met_genPt/F : 0 at: 0x4d77b40
# OBJ: TBranch met_genPhi  met_genPhi/F : 0 at: 0x4d78360
# OBJ: TBranch met_genEta  met_genEta/F : 0 at: 0x4d78b80
# OBJ: TBranch nFatJet nFatJet/I : 0 at: 0x4d793a0
# OBJ: TBranch FatJet_id POG Loose jet ID for AK8 jets, sorted by pt : 0 at: 0x4d79bc0
# OBJ: TBranch FatJet_puId puId (full MVA, loose WP, 5.3.X training on AK5PFchs: the only thing that is available now) for AK8 jets, sorted by pt : 0 at: 0x4d7a760
# OBJ: TBranch FatJet_btagCSV  CSV-IVF v2 discriminator for AK8 jets, sorted by pt : 0 at: 0x4d7b350
# OBJ: TBranch FatJet_btagCMVA CMVA discriminator for AK8 jets, sorted by pt : 0 at: 0x4d7bf00
# OBJ: TBranch FatJet_rawPt  p_{T} before JEC for AK8 jets, sorted by pt : 0 at: 0x4d7cae0
# OBJ: TBranch FatJet_mcPt p_{T} of associated gen jet for AK8 jets, sorted by pt : 0 at: 0x4d7d680
# OBJ: TBranch FatJet_mcFlavour  parton flavour (physics definition, i.e. including b's from shower) for AK8 jets, sorted by pt : 0 at: 0x4d7e230
# OBJ: TBranch FatJet_mcMatchId  Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake for AK8 jets, sorted by pt : 0 at: 0x4d7ee60
# OBJ: TBranch FatJet_corr_JECUp corr_JECUp for AK8 jets, sorted by pt : 0 at: 0x4d7fae0
# OBJ: TBranch FatJet_corr_JECDown corr_JECDown for AK8 jets, sorted by pt : 0 at: 0x4d806e0
# OBJ: TBranch FatJet_corr corr for AK8 jets, sorted by pt : 0 at: 0x4d812e0
# OBJ: TBranch FatJet_pt pt for AK8 jets, sorted by pt : 0 at: 0x4d81e70
# OBJ: TBranch FatJet_eta  eta for AK8 jets, sorted by pt : 0 at: 0x4d82a00
# OBJ: TBranch FatJet_phi  phi for AK8 jets, sorted by pt : 0 at: 0x4d83590
# OBJ: TBranch FatJet_mass mass for AK8 jets, sorted by pt : 0 at: 0x4d84120
# OBJ: TBranch FatJet_prunedMass pruned mass for AK8 jets, sorted by pt : 0 at: 0x4d84cb0
# OBJ: TBranch FatJet_trimmedMass  trimmed mass for AK8 jets, sorted by pt : 0 at: 0x4d858b0
# OBJ: TBranch FatJet_filteredMass filtered mass for AK8 jets, sorted by pt : 0 at: 0x4d864b0
# OBJ: TBranch FatJet_tau1 1-subjettiness for AK8 jets, sorted by pt : 0 at: 0x4d870b0
# OBJ: TBranch FatJet_tau2 2-subjettiness for AK8 jets, sorted by pt : 0 at: 0x4d87c50
# OBJ: TBranch FatJet_tau3 3-subjettiness for AK8 jets, sorted by pt : 0 at: 0x4d887f0
# OBJ: TBranch FatJet_topMass  CA8 jet topMass for AK8 jets, sorted by pt : 0 at: 0x4d89390
# OBJ: TBranch FatJet_minMass  CA8 jet minMass for AK8 jets, sorted by pt : 0 at: 0x4d89f30
# OBJ: TBranch FatJet_nSubJets CA8 jet nSubJets for AK8 jets, sorted by pt : 0 at: 0x4d8aad0
# OBJ: TBranch nisoTrack nisoTrack/I : 0 at: 0x4d8b6b0
# OBJ: TBranch isoTrack_pdgId  pdgId for isoTrack, sorted by pt : 0 at: 0x4d8bed0
# OBJ: TBranch isoTrack_pt pt for isoTrack, sorted by pt : 0 at: 0x4d8ccb0
# OBJ: TBranch isoTrack_eta  eta for isoTrack, sorted by pt : 0 at: 0x4d8da80
# OBJ: TBranch isoTrack_phi  phi for isoTrack, sorted by pt : 0 at: 0x4d8e850
# OBJ: TBranch isoTrack_mass mass for isoTrack, sorted by pt : 0 at: 0x4d8f620
# OBJ: TBranch isoTrack_charge charge for isoTrack, sorted by pt : 0 at: 0x4d903f0
# OBJ: TBranch isoTrack_dz d_{z} of lead track with respect to PV, in cm (with sign) for isoTrack, sorted by pt : 0 at: 0x4d91210
# OBJ: TBranch isoTrack_absIso abs charged iso with condition for isolation such that Min(0.2*pt, 8 GeV) for isoTrack, sorted by pt : 0 at: 0x4d92020
# OBJ: TBranch isoTrack_mcMatchId  Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake for isoTrack, sorted by pt : 0 at: 0x4d92e80
# OBJ: TBranch ngenPartAll ngenPartAll/I : 0 at: 0x4d93d70
# OBJ: TBranch genPartAll_motherId pdgId of the mother of the particle for all pruned genparticles : 0 at: 0x4d94590
# OBJ: TBranch genPartAll_grandmotherId  pdgId of the grandmother of the particle for all pruned genparticles : 0 at: 0x4d9aac0
# OBJ: TBranch genPartAll_charge charge for all pruned genparticles : 0 at: 0x4da1000
# OBJ: TBranch genPartAll_status status for all pruned genparticles : 0 at: 0x4da7510
# OBJ: TBranch genPartAll_pdgId  pdgId for all pruned genparticles : 0 at: 0x4dada20
# OBJ: TBranch genPartAll_pt pt for all pruned genparticles : 0 at: 0x4db3f00
# OBJ: TBranch genPartAll_eta  eta for all pruned genparticles : 0 at: 0x4dba370
# OBJ: TBranch genPartAll_phi  phi for all pruned genparticles : 0 at: 0x4dc07e0
# OBJ: TBranch genPartAll_mass mass for all pruned genparticles : 0 at: 0x4dc6c50
# OBJ: TBranch genPartAll_nDaughters index of the daughters in the genParticles for all pruned genparticles : 0 at: 0x4dcd110
# OBJ: TBranch genPartAll_nMothers index of the mother in the genParticles for all pruned genparticles : 0 at: 0x4dd3650
# OBJ: TBranch genPartAll_motherIndex1 index of the first mother in the genParticles for all pruned genparticles : 0 at: 0x4dd9b90
# OBJ: TBranch genPartAll_daughterIndex1 index of the first mother in the genParticles for all pruned genparticles : 0 at: 0x4de00d0
# OBJ: TBranch genPartAll_motherIndex2 index of the last mother in the genParticles for all pruned genparticles : 0 at: 0x4de6650
# OBJ: TBranch genPartAll_daughterIndex2 index of the last mother in the genParticles for all pruned genparticles : 0 at: 0x4decb90
# OBJ: TBranch ngenTau ngenTau/I : 0 at: 0x4df3110
# OBJ: TBranch genTau_motherId pdgId of the mother of the particle for Generated leptons (tau) from W/Z decays : 0 at: 0x4df3930
# OBJ: TBranch genTau_grandmotherId  pdgId of the grandmother of the particle for Generated leptons (tau) from W/Z decays : 0 at: 0x4df4610
# OBJ: TBranch genTau_sourceId origin of the particle (heaviest ancestor): 6=t, 25=h, 23/24=W/Z for Generated leptons (tau) from W/Z decays : 0 at: 0x4df5320
# OBJ: TBranch genTau_charge charge for Generated leptons (tau) from W/Z decays : 0 at: 0x4df6020
# OBJ: TBranch genTau_status status for Generated leptons (tau) from W/Z decays : 0 at: 0x4df6cb0
# OBJ: TBranch genTau_pdgId  pdgId for Generated leptons (tau) from W/Z decays : 0 at: 0x4df7940
# OBJ: TBranch genTau_pt pt for Generated leptons (tau) from W/Z decays : 0 at: 0x4df85d0
# OBJ: TBranch genTau_eta  eta for Generated leptons (tau) from W/Z decays : 0 at: 0x4df9250
# OBJ: TBranch genTau_phi  phi for Generated leptons (tau) from W/Z decays : 0 at: 0x4df9ed0
# OBJ: TBranch genTau_mass mass for Generated leptons (tau) from W/Z decays : 0 at: 0x4dfab50
# OBJ: TBranch genTau_MEx  neutrino x momentum from gen-tau for Generated leptons (tau) from W/Z decays : 0 at: 0x4dfb7e0
# OBJ: TBranch genTau_MEy  neutrino y momentum from gen-tau for Generated leptons (tau) from W/Z decays : 0 at: 0x4dfc480
# OBJ: TBranch genTau_nNuE nuE multiplicity in tau decay for Generated leptons (tau) from W/Z decays : 0 at: 0x4dfd120
# OBJ: TBranch genTau_nNuMu  nuMu multiplicity in tau decay for Generated leptons (tau) from W/Z decays : 0 at: 0x4dfddc0
# OBJ: TBranch genTau_nNuTau nuTau multiplicity in tau decay for Generated leptons (tau) from W/Z decays : 0 at: 0x4dfea60
# OBJ: TBranch genTau_MEpar  neutrino momentum from gen-tau, parallel to gen-tau for Generated leptons (tau) from W/Z decays : 0 at: 0x4dff700
# OBJ: TBranch genTau_MEperp neutrino momentum from gen-tau, perp. to gen-tau for Generated leptons (tau) from W/Z decays : 0 at: 0x4e003b0
# OBJ: TBranch nGenPart  nGenPart/I : 0 at: 0x4e01060
# OBJ: TBranch GenPart_motherId  pdgId of the mother of the particle for Hard scattering particles, with ancestry and links : 0 at: 0x4e01880
# OBJ: TBranch GenPart_grandmotherId pdgId of the grandmother of the particle for Hard scattering particles, with ancestry and links : 0 at: 0x4e02fd0
# OBJ: TBranch GenPart_sourceId  origin of the particle (heaviest ancestor): 6=t, 25=h, 23/24=W/Z for Hard scattering particles, with ancestry and links : 0 at: 0x4e04720
# OBJ: TBranch GenPart_charge  charge for Hard scattering particles, with ancestry and links : 0 at: 0x4e05e90
# OBJ: TBranch GenPart_status  status for Hard scattering particles, with ancestry and links : 0 at: 0x4e07560
# OBJ: TBranch GenPart_pdgId pdgId for Hard scattering particles, with ancestry and links : 0 at: 0x4e08c30
# OBJ: TBranch GenPart_pt  pt for Hard scattering particles, with ancestry and links : 0 at: 0x4e0a300
# OBJ: TBranch GenPart_eta eta for Hard scattering particles, with ancestry and links : 0 at: 0x4e0b9d0
# OBJ: TBranch GenPart_phi phi for Hard scattering particles, with ancestry and links : 0 at: 0x4e0d0a0
# OBJ: TBranch GenPart_mass  mass for Hard scattering particles, with ancestry and links : 0 at: 0x4e0e770
# OBJ: TBranch GenPart_motherIndex index of the mother in the generatorSummary for Hard scattering particles, with ancestry and links : 0 at: 0x4e0fe40
# OBJ: TBranch nLepOther nLepOther/I : 0 at: 0x4e115a0
# OBJ: TBranch LepOther_charge charge for Leptons after the preselection : 0 at: 0x4e11dc0
# OBJ: TBranch LepOther_tightId  POG Tight ID (for electrons it's configured in the analyzer) for Leptons after the preselection : 0 at: 0x4e129a0
# OBJ: TBranch LepOther_eleCutIdCSA14_25ns_v1  Electron cut-based id (POG CSA14_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight for Leptons after the preselection : 0 at: 0x4e135d0
# OBJ: TBranch LepOther_eleCutIdCSA14_50ns_v1  Electron cut-based id (POG CSA14_50ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight for Leptons after the preselection : 0 at: 0x4e14230
# OBJ: TBranch LepOther_dxy  d_{xy} with respect to PV, in cm (with sign) for Leptons after the preselection : 0 at: 0x4e14e90
# OBJ: TBranch LepOther_dz d_{z} with respect to PV, in cm (with sign) for Leptons after the preselection : 0 at: 0x4e15a50
# OBJ: TBranch LepOther_edxy #sigma(d_{xy}) with respect to PV, in cm for Leptons after the preselection : 0 at: 0x4e16610
# OBJ: TBranch LepOther_edz  #sigma(d_{z}) with respect to PV, in cm for Leptons after the preselection : 0 at: 0x4e171d0
# OBJ: TBranch LepOther_ip3d d_{3d} with respect to PV, in cm (absolute value) for Leptons after the preselection : 0 at: 0x4e17d90
# OBJ: TBranch LepOther_sip3d  S_{ip3d} with respect to PV (significance) for Leptons after the preselection : 0 at: 0x4e18960
# OBJ: TBranch LepOther_convVeto Conversion veto (always true for muons) for Leptons after the preselection : 0 at: 0x4d21d80
# OBJ: TBranch LepOther_lostHits Number of lost hits on inner track for Leptons after the preselection : 0 at: 0x4d229a0
# OBJ: TBranch LepOther_relIso03 PF Rel Iso, R=0.3, pile-up corrected for Leptons after the preselection : 0 at: 0x4d235c0
# OBJ: TBranch LepOther_relIso04 PF Rel Iso, R=0.4, pile-up corrected for Leptons after the preselection : 0 at: 0x4d241e0
# OBJ: TBranch LepOther_miniRelIso PF Rel miniRel, pile-up corrected for Leptons after the preselection : 0 at: 0x4d24e00
# OBJ: TBranch LepOther_tightCharge  Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, 2 if ptError/pt < 0.20, 0 otherwise  for Leptons after the preselection : 0 at: 0x4d25a20
# OBJ: TBranch LepOther_mcMatchId  Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake for Leptons after the preselection : 0 at: 0x4d266c0
# OBJ: TBranch LepOther_mcMatchAny Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom for Leptons after the preselection : 0 at: 0x4e249e0
# OBJ: TBranch LepOther_mcMatchTau True if the leptons comes from a tau for Leptons after the preselection : 0 at: 0x4e25630
# OBJ: TBranch LepOther_mcPt p_{T} of associated gen lepton for Leptons after the preselection : 0 at: 0x4e26250
# OBJ: TBranch LepOther_mediumMuonId Muon POG Medium id for Leptons after the preselection : 0 at: 0x4e26e10
# OBJ: TBranch LepOther_pdgId  pdgId for Leptons after the preselection : 0 at: 0x4e27a30
# OBJ: TBranch LepOther_pt pt for Leptons after the preselection : 0 at: 0x4e285d0
# OBJ: TBranch LepOther_eta  eta for Leptons after the preselection : 0 at: 0x4e29170
# OBJ: TBranch LepOther_phi  phi for Leptons after the preselection : 0 at: 0x4e29d10
# OBJ: TBranch LepOther_mass mass for Leptons after the preselection : 0 at: 0x4e2a8b0
# OBJ: TBranch LepOther_mvaIdPhys14  EGamma POG MVA ID for non-triggering electrons, Phys14 re-training; 1 for muons for Leptons after the preselection : 0 at: 0x4e2b450
# OBJ: TBranch LepOther_mvaTTH Lepton MVA (TTH version) for Leptons after the preselection : 0 at: 0x4e2c0a0
# OBJ: TBranch LepOther_mvaSusy  Lepton MVA (SUSY version) for Leptons after the preselection : 0 at: 0x4e2cc90
# OBJ: TBranch LepOther_jetPtRatio pt(lepton)/pt(nearest jet) for Leptons after the preselection : 0 at: 0x4e2d8a0
# OBJ: TBranch LepOther_jetPtRel pt of the lepton transverse to the jet axis (subtracting the lepton) for Leptons after the preselection : 0 at: 0x4e2e4b0
# OBJ: TBranch LepOther_jetBTagCSV CSV btag of nearest jet for Leptons after the preselection : 0 at: 0x4e2f0f0
# OBJ: TBranch LepOther_jetBTagCMVA  CMA btag of nearest jet for Leptons after the preselection : 0 at: 0x4e2fd00
# OBJ: TBranch LepOther_jetDR  deltaR(lepton, nearest jet) for Leptons after the preselection : 0 at: 0x4e30910
# OBJ: TBranch nJet  nJet/I : 0 at: 0x4e314c0
# OBJ: TBranch Jet_area  Catchment area of jet for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e31ce0
# OBJ: TBranch Jet_qgl QG Likelihood for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e32b10
# OBJ: TBranch Jet_ptd QG input variable: ptD for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e33930
# OBJ: TBranch Jet_axis2 QG input variable: axis2 for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e34760
# OBJ: TBranch Jet_mult  QG input variable: total multiplicity for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e355b0
# OBJ: TBranch Jet_partonId  parton flavour (manually matching to status 23 particles) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e363f0
# OBJ: TBranch Jet_partonMotherId  parton flavour (manually matching to status 23 particles) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e37270
# OBJ: TBranch Jet_nLeptons  Number of associated leptons for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e38150
# OBJ: TBranch Jet_id  POG Loose jet ID for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e38fb0
# OBJ: TBranch Jet_puId  puId (full MVA, loose WP, 5.3.X training on AK5PFchs: the only thing that is available now) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e39de0
# OBJ: TBranch Jet_btagCSV CSV-IVF v2 discriminator for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e3ac50
# OBJ: TBranch Jet_btagCMVA  CMVA discriminator for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e3bab0
# OBJ: TBranch Jet_rawPt p_{T} before JEC for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e3c910
# OBJ: TBranch Jet_mcPt  p_{T} of associated gen jet for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e3d760
# OBJ: TBranch Jet_mcFlavour parton flavour (physics definition, i.e. including b's from shower) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e3e590
# OBJ: TBranch Jet_mcMatchId Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e3f420
# OBJ: TBranch Jet_corr_JECUp  corr_JECUp for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e402f0
# OBJ: TBranch Jet_corr_JECDown  corr_JECDown for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e41140
# OBJ: TBranch Jet_corr  corr for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e41ff0
# OBJ: TBranch Jet_pt  pt for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e42e10
# OBJ: TBranch Jet_eta eta for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e43c30
# OBJ: TBranch Jet_phi phi for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e44a50
# OBJ: TBranch Jet_mass  mass for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e45870
# OBJ: TBranch Jet_mcMatchFlav Flavour of associated parton from hard scatter (if any) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e46690
# OBJ: TBranch Jet_chHEF chargedHadronEnergyFraction (relative to uncorrected jet energy) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e47550
# OBJ: TBranch Jet_neHEF neutralHadronEnergyFraction (relative to uncorrected jet energy) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e483d0
# OBJ: TBranch Jet_phEF  photonEnergyFraction (relative to corrected jet energy) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e49250
# OBJ: TBranch Jet_eEF electronEnergyFraction (relative to corrected jet energy) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e4a0a0
# OBJ: TBranch Jet_muEF  muonEnergyFraction (relative to corrected jet energy) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e4aef0
# OBJ: TBranch Jet_HFHEF HFHadronEnergyFraction (relative to corrected jet energy) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e4bd40
# OBJ: TBranch Jet_HFEMEF  HFEMEnergyFraction (relative to corrected jet energy) for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e4cbb0
# OBJ: TBranch Jet_chHMult chargedHadronMultiplicity from PFJet.h for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e4da30
# OBJ: TBranch Jet_neHMult neutralHadronMultiplicity from PFJet.h for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e4e8a0
# OBJ: TBranch Jet_phMult  photonMultiplicity from PFJet.h for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e4f710
# OBJ: TBranch Jet_eMult electronMultiplicity from PFJet.h for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e50570
# OBJ: TBranch Jet_muMult  muonMultiplicity from PFJet.h for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e513d0
# OBJ: TBranch Jet_HFHMult HFHadronMultiplicity from PFJet.h for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e52230
# OBJ: TBranch Jet_HFEMMult  HFEMMultiplicity from PFJet.h for Cental jets after full selection and cleaning, sorted by pt : 0 at: 0x4e530a0
# OBJ: TBranch nSV nSV/I : 0 at: 0x4e53f00
# OBJ: TBranch SV_pt pt for SVs from IVF : 0 at: 0x4e54720
# OBJ: TBranch SV_eta  eta for SVs from IVF : 0 at: 0x4e55340
# OBJ: TBranch SV_phi  phi for SVs from IVF : 0 at: 0x4e55f60
# OBJ: TBranch SV_mass mass for SVs from IVF : 0 at: 0x4e56b80
# OBJ: TBranch SV_charge charge for SVs from IVF : 0 at: 0x4e577a0
# OBJ: TBranch SV_ntracks  Number of tracks (with weight > 0.5) for SVs from IVF : 0 at: 0x4e583c0
# OBJ: TBranch SV_chi2 Chi2 of the vertex fit for SVs from IVF : 0 at: 0x4e59020
# OBJ: TBranch SV_ndof Degrees of freedom of the fit, ndof = (2*ntracks - 3) for SVs from IVF : 0 at: 0x4e59c50
# OBJ: TBranch SV_dxy  Transverse distance from the PV [cm] for SVs from IVF : 0 at: 0x4e5a8a0
# OBJ: TBranch SV_edxy Uncertainty on the transverse distance from the PV [cm] for SVs from IVF : 0 at: 0x4e5b4e0
# OBJ: TBranch SV_ip3d 3D distance from the PV [cm] for SVs from IVF : 0 at: 0x4e5c130
# OBJ: TBranch SV_eip3d  Uncertainty on the 3D distance from the PV [cm] for SVs from IVF : 0 at: 0x4e5cd60
# OBJ: TBranch SV_sip3d  S_{ip3d} with respect to PV (absolute value) for SVs from IVF : 0 at: 0x4e5d9b0
# OBJ: TBranch SV_cosTheta Cosine of the angle between the 3D displacement and the momentum for SVs from IVF : 0 at: 0x4e5e5f0
# OBJ: TBranch SV_mva  MVA discriminator for SVs from IVF : 0 at: 0x4e5f280
# OBJ: TBranch SV_jetPt  pT of associated jet for SVs from IVF : 0 at: 0x4e5feb0
# OBJ: TBranch SV_jetBTagCSV CSV b-tag of associated jet for SVs from IVF : 0 at: 0x4e60ae0
# OBJ: TBranch SV_jetBTagCMVA  CMVA b-tag of associated jet for SVs from IVF : 0 at: 0x4e61740
# OBJ: TBranch SV_mcMatchNTracks Number of mc-matched tracks in SV for SVs from IVF : 0 at: 0x4e623a0
# OBJ: TBranch SV_mcMatchNTracksHF Number of mc-matched tracks from b/c in SV for SVs from IVF : 0 at: 0x4e63070
# OBJ: TBranch SV_mcMatchFraction  Fraction of mc-matched tracks from b/c matched to a single hadron (or -1 if mcMatchNTracksHF < 2) for SVs from IVF : 0 at: 0x4e63d40
# OBJ: TBranch SV_mcFlavFirst  Flavour of last ancestor with maximum number of matched daughters for SVs from IVF : 0 at: 0x4e64a50
# OBJ: TBranch SV_mcFlavHeaviest Flavour of heaviest hadron with maximum number of matched daughters for SVs from IVF : 0 at: 0x4e656e0
# OBJ: TBranch SV_maxDxyTracks highest |dxy| of vertex tracks for SVs from IVF : 0 at: 0x4e663d0
# OBJ: TBranch SV_secDxyTracks second highest |dxy| of vertex tracks for SVs from IVF : 0 at: 0x4e67070
# OBJ: TBranch SV_maxD3dTracks highest |ip3D| of vertex tracks for SVs from IVF : 0 at: 0x4e67d20
# OBJ: TBranch SV_secD3dTracks second highest |ip3D| of vertex tracks for SVs from IVF : 0 at: 0x4e689d0
# OBJ: TBranch nLepGood  nLepGood/I : 0 at: 0x4e69680
# OBJ: TBranch LepGood_charge  charge for Leptons after the preselection : 0 at: 0x4e69ea0
# OBJ: TBranch LepGood_tightId POG Tight ID (for electrons it's configured in the analyzer) for Leptons after the preselection : 0 at: 0x4e6abd0
# OBJ: TBranch LepGood_eleCutIdCSA14_25ns_v1 Electron cut-based id (POG CSA14_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight for Leptons after the preselection : 0 at: 0x4e6b970
# OBJ: TBranch LepGood_eleCutIdCSA14_50ns_v1 Electron cut-based id (POG CSA14_50ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight for Leptons after the preselection : 0 at: 0x4e6c760
# OBJ: TBranch LepGood_dxy d_{xy} with respect to PV, in cm (with sign) for Leptons after the preselection : 0 at: 0x4e6d550
# OBJ: TBranch LepGood_dz  d_{z} with respect to PV, in cm (with sign) for Leptons after the preselection : 0 at: 0x4e6e2a0
# OBJ: TBranch LepGood_edxy  #sigma(d_{xy}) with respect to PV, in cm for Leptons after the preselection : 0 at: 0x4e6eff0
# OBJ: TBranch LepGood_edz #sigma(d_{z}) with respect to PV, in cm for Leptons after the preselection : 0 at: 0x4e6fd40
# OBJ: TBranch LepGood_ip3d  d_{3d} with respect to PV, in cm (absolute value) for Leptons after the preselection : 0 at: 0x4e70a90
# OBJ: TBranch LepGood_sip3d S_{ip3d} with respect to PV (significance) for Leptons after the preselection : 0 at: 0x4e717f0
# OBJ: TBranch LepGood_convVeto  Conversion veto (always true for muons) for Leptons after the preselection : 0 at: 0x4e72540
# OBJ: TBranch LepGood_lostHits  Number of lost hits on inner track for Leptons after the preselection : 0 at: 0x4e732f0
# OBJ: TBranch LepGood_relIso03  PF Rel Iso, R=0.3, pile-up corrected for Leptons after the preselection : 0 at: 0x4e740a0
# OBJ: TBranch LepGood_relIso04  PF Rel Iso, R=0.4, pile-up corrected for Leptons after the preselection : 0 at: 0x4e74e50
# OBJ: TBranch LepGood_miniRelIso  PF Rel miniRel, pile-up corrected for Leptons after the preselection : 0 at: 0x4e75c00
# OBJ: TBranch LepGood_tightCharge Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, 2 if ptError/pt < 0.20, 0 otherwise  for Leptons after the preselection : 0 at: 0x4e769b0
# OBJ: TBranch LepGood_mcMatchId Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake for Leptons after the preselection : 0 at: 0x4e777e0
# OBJ: TBranch LepGood_mcMatchAny  Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom for Leptons after the preselection : 0 at: 0x4e785f0
# OBJ: TBranch LepGood_mcMatchTau  True if the leptons comes from a tau for Leptons after the preselection : 0 at: 0x4e793f0
# OBJ: TBranch LepGood_mcPt  p_{T} of associated gen lepton for Leptons after the preselection : 0 at: 0x4e7a1a0
# OBJ: TBranch LepGood_mediumMuonId  Muon POG Medium id for Leptons after the preselection : 0 at: 0x4e7aef0
# OBJ: TBranch LepGood_pdgId pdgId for Leptons after the preselection : 0 at: 0x4e7bc90
# OBJ: TBranch LepGood_pt  pt for Leptons after the preselection : 0 at: 0x4e7c9c0
# OBJ: TBranch LepGood_eta eta for Leptons after the preselection : 0 at: 0x4e7d6f0
# OBJ: TBranch LepGood_phi phi for Leptons after the preselection : 0 at: 0x4e7e420
# OBJ: TBranch LepGood_mass  mass for Leptons after the preselection : 0 at: 0x4e7f150
# OBJ: TBranch LepGood_mvaIdPhys14 EGamma POG MVA ID for non-triggering electrons, Phys14 re-training; 1 for muons for Leptons after the preselection : 0 at: 0x4e7fe80
# OBJ: TBranch LepGood_mvaTTH  Lepton MVA (TTH version) for Leptons after the preselection : 0 at: 0x4e80c60
# OBJ: TBranch LepGood_mvaSusy Lepton MVA (SUSY version) for Leptons after the preselection : 0 at: 0x4e819a0
# OBJ: TBranch LepGood_jetPtRatio  pt(lepton)/pt(nearest jet) for Leptons after the preselection : 0 at: 0x4e82720
# OBJ: TBranch LepGood_jetPtRel  pt of the lepton transverse to the jet axis (subtracting the lepton) for Leptons after the preselection : 0 at: 0x4e834c0
# OBJ: TBranch LepGood_jetBTagCSV  CSV btag of nearest jet for Leptons after the preselection : 0 at: 0x4e84290
# OBJ: TBranch LepGood_jetBTagCMVA CMA btag of nearest jet for Leptons after the preselection : 0 at: 0x4e85030
# OBJ: TBranch LepGood_jetDR deltaR(lepton, nearest jet) for Leptons after the preselection : 0 at: 0x4e85dd0
# OBJ: TBranch ngenLepFromTau  ngenLepFromTau/I : 0 at: 0x4e86b10
# OBJ: TBranch genLepFromTau_motherId  pdgId of the mother of the particle for Generated leptons (e/mu) from decays of taus from W/Z/h decays : 0 at: 0x4e87360
# OBJ: TBranch genLepFromTau_grandmotherId pdgId of the grandmother of the particle for Generated leptons (e/mu) from decays of taus from W/Z/h decays : 0 at: 0x4e87fb0
# OBJ: TBranch genLepFromTau_sourceId  origin of the particle (heaviest ancestor): 6=t, 25=h, 23/24=W/Z for Generated leptons (e/mu) from decays of taus from W/Z/h decays : 0 at: 0x4e88c00
# OBJ: TBranch genLepFromTau_charge  charge for Generated leptons (e/mu) from decays of taus from W/Z/h decays : 0 at: 0x4e89870
# OBJ: TBranch genLepFromTau_status  status for Generated leptons (e/mu) from decays of taus from W/Z/h decays : 0 at: 0x4e8a4a0
# OBJ: TBranch genLepFromTau_pdgId pdgId for Generated leptons (e/mu) from decays of taus from W/Z/h decays : 0 at: 0x4e8b0d0
# OBJ: TBranch genLepFromTau_pt  pt for Generated leptons (e/mu) from decays of taus from W/Z/h decays : 0 at: 0x4e8bd00
# OBJ: TBranch genLepFromTau_eta eta for Generated leptons (e/mu) from decays of taus from W/Z/h decays : 0 at: 0x4e8c930
# OBJ: TBranch genLepFromTau_phi phi for Generated leptons (e/mu) from decays of taus from W/Z/h decays : 0 at: 0x4e8d560
# OBJ: TBranch genLepFromTau_mass  mass for Generated leptons (e/mu) from decays of taus from W/Z/h decays : 0 at: 0x4e8e190
# OBJ: TBranch genLepFromTau_motherIndex index of the mother in the generatorSummary for Generated leptons (e/mu) from decays of taus from W/Z/h decays : 0 at: 0x4e8edc0
# OBJ: TBranch nGenJet nGenJet/I : 0 at: 0x4e8fa10
# OBJ: TBranch GenJet_pt pt for Gen Jets, sorted by pt : 0 at: 0x4e90230
# OBJ: TBranch GenJet_eta  eta for Gen Jets, sorted by pt : 0 at: 0x4e91640
# OBJ: TBranch GenJet_phi  phi for Gen Jets, sorted by pt : 0 at: 0x4e92a50
# OBJ: TBranch GenJet_mass mass for Gen Jets, sorted by pt : 0 at: 0x4e93e60
# OBJ: TBranch GenJet_nConstituents  Number of Constituents for Gen Jets, sorted by pt : 0 at: 0x4e95270
# OBJ: TBranch nTauGood  nTauGood/I : 0 at: 0x4e96700
# OBJ: TBranch TauGood_charge  charge for Taus after the preselection : 0 at: 0x4e96f20
# OBJ: TBranch TauGood_decayMode decayMode for Taus after the preselection : 0 at: 0x4e97ac0
# OBJ: TBranch TauGood_idDecayMode idDecayMode for Taus after the preselection : 0 at: 0x4e986c0
# OBJ: TBranch TauGood_idDecayModeNewDMs idDecayModeNewDMs for Taus after the preselection : 0 at: 0x4e992c0
# OBJ: TBranch TauGood_dxy d_{xy} of lead track with respect to PV, in cm (with sign) for Taus after the preselection : 0 at: 0x4e99ee0
# OBJ: TBranch TauGood_dz  d_{z} of lead track with respect to PV, in cm (with sign) for Taus after the preselection : 0 at: 0x4e9aab0
# OBJ: TBranch TauGood_idMVA 1,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the MVA3oldDMwLT discriminator for Taus after the preselection : 0 at: 0x4e9b680
# OBJ: TBranch TauGood_idMVANewDM  1,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the MVA3newDMwLT discriminator for Taus after the preselection : 0 at: 0x4e9c280
# OBJ: TBranch TauGood_idCI3hit  1,2,3 if the tau passes the loose, medium, tight WP of the By<X>CombinedIsolationDBSumPtCorr3Hits discriminator for Taus after the preselection : 0 at: 0x4e9cee0
# OBJ: TBranch TauGood_idAntiMu  1,2 if the tau passes the loose/tight WP of the againstMuon<X>3 discriminator for Taus after the preselection : 0 at: 0x4e9db40
# OBJ: TBranch TauGood_idAntiE 1,2,3,4,5 if the tau passes the v loose, loose, medium, tight, v tight WP of the againstElectron<X>MVA5 discriminator for Taus after the preselection : 0 at: 0x4e9e780
# OBJ: TBranch TauGood_isoCI3hit byCombinedIsolationDeltaBetaCorrRaw3Hits raw output discriminator for Taus after the preselection : 0 at: 0x4e9f3d0
# OBJ: TBranch TauGood_mcMatchId Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake for Taus after the preselection : 0 at: 0x4ea0010
# OBJ: TBranch TauGood_pdgId pdgId for Taus after the preselection : 0 at: 0x4ea0c90
# OBJ: TBranch TauGood_pt  pt for Taus after the preselection : 0 at: 0x4ea1830
# OBJ: TBranch TauGood_eta eta for Taus after the preselection : 0 at: 0x4ea23d0
# OBJ: TBranch TauGood_phi phi for Taus after the preselection : 0 at: 0x4ea2f70
# OBJ: TBranch TauGood_mass  mass for Taus after the preselection : 0 at: 0x4ea3b10
# OBJ: TBranch ngenLep ngenLep/I : 0 at: 0x4ea46b0
# OBJ: TBranch genLep_motherId pdgId of the mother of the particle for Generated leptons (e/mu) from W/Z decays : 0 at: 0x4ea4ed0
# OBJ: TBranch genLep_grandmotherId  pdgId of the grandmother of the particle for Generated leptons (e/mu) from W/Z decays : 0 at: 0x4ea5d80
# OBJ: TBranch genLep_sourceId origin of the particle (heaviest ancestor): 6=t, 25=h, 23/24=W/Z for Generated leptons (e/mu) from W/Z decays : 0 at: 0x4ea6c50
# OBJ: TBranch genLep_charge charge for Generated leptons (e/mu) from W/Z decays : 0 at: 0x4ea7b10
# OBJ: TBranch genLep_status status for Generated leptons (e/mu) from W/Z decays : 0 at: 0x4ea8960
# OBJ: TBranch genLep_pdgId  pdgId for Generated leptons (e/mu) from W/Z decays : 0 at: 0x4ea97b0
# OBJ: TBranch genLep_pt pt for Generated leptons (e/mu) from W/Z decays : 0 at: 0x4eaa600
# OBJ: TBranch genLep_eta  eta for Generated leptons (e/mu) from W/Z decays : 0 at: 0x4eab440
# OBJ: TBranch genLep_phi  phi for Generated leptons (e/mu) from W/Z decays : 0 at: 0x4eac290
# OBJ: TBranch genLep_mass mass for Generated leptons (e/mu) from W/Z decays : 0 at: 0x4ead0e0
# OBJ: TBranch genLep_motherIndex  index of the mother in the generatorSummary for Generated leptons (e/mu) from W/Z decays : 0 at: 0x4eadf30
#
