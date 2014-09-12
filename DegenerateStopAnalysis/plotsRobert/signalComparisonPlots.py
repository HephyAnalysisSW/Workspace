import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

paths = ['../../HEPHYPythonTools/python', '../../HEPHYPythonTools/plots', '../../RA4Analysis/plots', '../python']
#path = os.path.abspath('../../HEPHYPythonTools/python')
for path in [os.path.abspath(p) for p in paths]:
  if not path in sys.path:
    sys.path.insert(1, path)

from simplePlotsCommon import *
from funcs import *
from helpers import passPUJetID
import xsec
small = False
doOnlyOne = True
targetLumi = 19375.
lumiScale = 1.

#FastSim = {}
#FastSim["bins"] = ["S300N270"]
#FastSim["name"] = "S300N270"
#
#FullSim = {}
#FullSim["bins"] = ["S300N270FullSim"]
#FullSim["name"] = "S300N270FullSim"

chmode = "copy"

from defaultConvertedTuples import stop300lsp270g200FastSim, stop300lsp270g175FastSim, stop200lsp170g100FastSim, stop300lsp240g150FastSim, stop300lsp270FastSim
from defaultConvertedTuples import stop300lsp270g200FullSim, stop300lsp270g175FullSim, stop200lsp170g100FullSim, stop300lsp240g150FullSim, stop300lsp270FullSim

stop300lsp270g200FastSim["legendText"]  = "FastS., m_{#tilde t} = 300, m_{LSP} = 270, g=200"
stop300lsp270g175FastSim["legendText"]  = "FastS., m_{#tilde t} = 300, m_{LSP} = 270, g=175"
stop300lsp270FastSim["legendText"]      = "FastS., m_{#tilde t} = 300, m_{LSP} = 270"
stop300lsp240g150FastSim["legendText"]  = "FastS., m_{#tilde t} = 300, m_{LSP} = 240, g=150"
stop200lsp170g100FastSim["legendText"]  = "FastS., m_{#tilde t} = 200, m_{LSP} = 170, g=100"

stop300lsp270g200FullSim["legendText"]  = "FullS., m_{#tilde t} = 300, m_{LSP} = 270, g=200"
stop300lsp270g175FullSim["legendText"]  = "FullS., m_{#tilde t} = 300, m_{LSP} = 270, g=175"
stop300lsp270FullSim["legendText"]      = "FullS., m_{#tilde t} = 300, m_{LSP} = 270"
stop300lsp240g150FullSim["legendText"]  = "FullS., m_{#tilde t} = 300, m_{LSP} = 240, g=150"
stop200lsp170g100FullSim["legendText"]  = "FullS., m_{#tilde t} = 200, m_{LSP} = 170, g=100"


stop300lsp270g200FullSim["color"]     = ROOT.kBlack
stop300lsp270g175FullSim["color"]     = ROOT.kRed - 3
stop200lsp170g100FullSim["color"]     = ROOT.kGreen - 3
stop300lsp240g150FullSim["color"]     = ROOT.kBlue - 4
stop300lsp270g200FastSim["color"]     = ROOT.kBlack
stop300lsp270g175FastSim["color"]     = ROOT.kRed - 3
stop200lsp170g100FastSim["color"]     = ROOT.kGreen - 3
stop300lsp240g150FastSim["color"]     = ROOT.kBlue - 4

stop300lsp270FullSim["color"]     = ROOT.kRed - 3
stop300lsp270FastSim["color"]     = ROOT.kBlue - 4

fastSimSamples = [stop200lsp170g100FastSim, stop300lsp270FastSim, stop300lsp240g150FastSim]
fullSimSamples = [stop200lsp170g100FullSim, stop300lsp270FullSim, stop300lsp240g150FullSim]

for s in fastSimSamples:
  s['style'] = "l11"
for s in fullSimSamples:
  s['style'] = "l11"

signals = [stop300lsp270FullSim, stop300lsp270FastSim] 
allSamples = signals
#  if sample['name'].lower().count('data'):
#    sample["weight"] = "weight"
#  else:
#    sample["weight"] = defWeight

allVars=[]
allStacks=[]

## plots for studying preselection 

minimum=10**(-0.5)

#presel = "refSel"
presel = "refSel"
preprefix     = "sigComp"
additionalCut = ""
#additionalCut = "met>250"


subdir = "/pngMJFullVSFast/"

normalizeToData = False

chainstring = "empty"
commoncf = "(0)"
prefix="empty_"
if presel == "refSel":
  hadRefSel = "isrJetPt>110&&isrJetBTBVetoPassed&&njet60<=2"
  softIsolatedMu = "softIsolatedMuPt>5"
  hardlepVeto = "nHardElectrons==0&&nHardMuonsRelIso02==0"
  commoncf = hadRefSel+"&&"+softIsolatedMu+"&&"+hardlepVeto
#  commoncf="njet<=3"
  chainstring = "Events"
if presel == "inclusive":
  commoncf="(1)"
#  commoncf="njet<=3"
  chainstring = "Events"

if additionalCut!="":
  commoncf+="&&"+additionalCut

prefix= "MonoJet_"+presel+"_"+chmode+"_"
if preprefix!="":
  prefix = preprefix+"_"+presel+"_"+chmode+"_"

for sample in allSamples:
  sample["Chain"] = chainstring
  sample["dirname"]  = "/data/schoef/monoJetTuples_v2/"+chmode+"/"


def getStack(varstring, binning, cutstring, signals = False, varfunc = ""):
  res = []
  for s in signals:
    sMC          = variable(varstring, binning, cutstring)
    sMC.sample   = s
    sMC.color      = s['color']
    sMC.legendText = s["legendText"]
    sMC.style      = s['style'] 
    res.append(sMC)
    if s['name'].lower().count('fast'):
      sMC.data_histo.SetLineStyle(2)
#  res = [FastS, FullS]

  res[0].dataMCRatio = [res[0],res[1]]
  res[0].ratioVarName = "Full / Fast"

  getLinesForStack(res, targetLumi)
  nhistos = len(res)
  for var in res:
    var.legendCoordinates=[0.51,0.95 - -0.08*3 ,.98,.95]
    var.scale = lumiScale
#    var.legendCoordinates=[0.64,0.95 - 0.05*nhistos,.98,.95] #for signalnumbers = [0,1]
  if varfunc!="":
    for var in res:
      var.varfunc = varfunc
  return res


isrJetPt_stack = getStack(":isrJetPt;p_{T} of ISR jet;Number of Events / 50 GeV",[50,0,1000], commoncf, signals)
isrJetPt_stack[0].addOverFlowBin = "upper"
allStacks.append(isrJetPt_stack)

softIsolatedMuNormChi2_stack = getStack(":softIsolatedMuNormChi2;#chi^{2} of global muon track;Number of Events",[30,0,30], commoncf, signals)
softIsolatedMuNormChi2_stack[0].addOverFlowBin = "both"
allStacks.append(softIsolatedMuNormChi2_stack)

softIsolatedMuNValMuonHits_stack = getStack(":softIsolatedMuNValMuonHits;valid hits;Number of Events",[60,0,60], commoncf, signals)
softIsolatedMuNValMuonHits_stack[0].addOverFlowBin = "both"
allStacks.append(softIsolatedMuNValMuonHits_stack)

softIsolatedMuNumMatchedStations_stack = getStack(":softIsolatedMuNumMatchedStations;matched stations;Number of Events",[8,0,8], commoncf, signals)
softIsolatedMuNumMatchedStations_stack[0].addOverFlowBin = "both"
allStacks.append(softIsolatedMuNumMatchedStations_stack)

softIsolatedMuPixelHits_stack = getStack(":softIsolatedMuPixelHits;Pixel hits;Number of Events",[10,0,10], commoncf, signals)
softIsolatedMuPixelHits_stack[0].addOverFlowBin = "both"
allStacks.append(softIsolatedMuPixelHits_stack)

softIsolatedMuPixelHits_lowDz_stack = getStack(":softIsolatedMuPixelHits;Pixel hits;Number of Events",[10,0,10], commoncf+"&&softIsolatedMuDz<0.2", signals)
softIsolatedMuPixelHits_lowDz_stack[0].addOverFlowBin = "both"
allStacks.append(softIsolatedMuPixelHits_lowDz_stack)

softIsolatedMuPixelHits_highDz_stack = getStack(":softIsolatedMuPixelHits;Pixel hits;Number of Events",[10,0,10], commoncf+"&&softIsolatedMuDz>=0.2", signals)
softIsolatedMuPixelHits_highDz_stack[0].addOverFlowBin = "both"
allStacks.append(softIsolatedMuPixelHits_highDz_stack)

softIsolatedMuNumtrackerLayerWithMeasurement_stack = getStack(":softIsolatedMuNumtrackerLayerWithMeasurement;tracker layer w. meas.;Number of Events",[20,0,20], commoncf, signals)
softIsolatedMuNumtrackerLayerWithMeasurement_stack[0].addOverFlowBin = "both"
allStacks.append(softIsolatedMuNumtrackerLayerWithMeasurement_stack)

softIsolatedMuIsGlobal_stack = getStack(":softIsolatedMuIsGlobal;isGlobal;Number of Events",[2,0,2], commoncf, signals)
softIsolatedMuIsGlobal_stack[0].addOverFlowBin = "both"
allStacks.append(softIsolatedMuIsGlobal_stack)

softIsolatedMuIsTracker_stack = getStack(":softIsolatedMuIsTracker;isTracker;Number of Events",[2,0,2], commoncf, signals)
softIsolatedMuIsTracker_stack[0].addOverFlowBin = "both"
allStacks.append(softIsolatedMuIsTracker_stack)

softIsolatedMuDz_stack = getStack(":softIsolatedMuDz;d_{z} of soft isolated muon;Number of Events",[40,0,20], commoncf, signals)
softIsolatedMuDz_stack[0].addOverFlowBin = "both"
allStacks.append(softIsolatedMuDz_stack)

softIsolatedMuDz_zoomed_stack = getStack(":softIsolatedMuDz;d_{z} of soft isolated muon;Number of Events",[40,0,2], commoncf, signals)
softIsolatedMuDz_zoomed_stack[0].addOverFlowBin = "both"
allStacks.append(softIsolatedMuDz_zoomed_stack)


if not doOnlyOne:
  isrJetEta_stack = getStack(":isrJetEta;#eta of ISR jet;Number of Events",[20,-5,5], commoncf, signals)
  isrJetEta_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetEta_stack)

  isrJetPhi_stack = getStack(":isrJetPhi;#phi of ISR jet;Number of Events",[20,-pi,pi], commoncf, signals)
  isrJetPhi_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetPhi_stack)

  isrJetPdg_stack = getStack(":isrJetPdg;pdgId of ISR jet;Number of Events",[44,-22,22], commoncf, signals)
  isrJetPdg_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetPdg_stack)

  isrJetBtag_stack = getStack(":isrJetBtag;CSV b-tag of ISR jet;Number of Events",[20,-1,1], commoncf, signals)
  isrJetBtag_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetBtag_stack)

  isrJetChef_stack = getStack(":isrJetChef;Chef of ISR jet;Number of Events",[20,0,1], commoncf, signals)
  isrJetChef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetChef_stack)

  isrJetNhef_stack = getStack(":isrJetNhef;Nhef of ISR jet;Number of Events",[20,0,1], commoncf, signals)
  isrJetNhef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetNhef_stack)

  isrJetCeef_stack = getStack(":isrJetCeef;Ceef of ISR jet;Number of Events",[20,0,1], commoncf, signals)
  isrJetCeef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetCeef_stack)

  isrJetNeef_stack = getStack(":isrJetNeef;Neef of ISR jet;Number of Events",[20,0,1], commoncf, signals)
  isrJetNeef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetNeef_stack)

  isrJetHFhef_stack = getStack(":isrJetHFhef;HFhef of ISR jet;Number of Events",[20,0,1], commoncf, signals)
  isrJetHFhef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetHFhef_stack)

  isrJetHFeef_stack = getStack(":isrJetHFeef;HFeef of ISR jet;Number of Events",[20,0,1], commoncf, signals)
  isrJetHFeef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetHFeef_stack)

  isrJetMuef_stack = getStack(":isrJetMuef;Muef of ISR jet;Number of Events",[20,0,1], commoncf, signals)
  isrJetMuef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetMuef_stack)

  isrJetElef_stack = getStack(":isrJetElef;Elef of ISR jet;Number of Events",[20,0,1], commoncf, signals)
  isrJetElef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetElef_stack)

  isrJetPhef_stack = getStack(":isrJetPhef;Phef of ISR jet;Number of Events",[20,0,1], commoncf, signals)
  isrJetPhef_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetPhef_stack)

  isrJetPt_barrel_stack = getStack(":isrJetPt;p_{T} of ISR jet;Number of Events / 50 GeV",[50,0,1000], commoncf+"&&abs(isrJetEta)<=1.479", signals)
  isrJetPt_barrel_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetPt_barrel_stack)

  isrJetChef_barrel_stack = getStack(":isrJetChef;Chef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)<=1.479", signals)
  isrJetChef_barrel_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetChef_barrel_stack)

  isrJetNhef_barrel_stack = getStack(":isrJetNhef;Nhef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)<=1.479", signals)
  isrJetNhef_barrel_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetNhef_barrel_stack)

  isrJetCeef_barrel_stack = getStack(":isrJetCeef;Ceef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)<=1.479", signals)
  isrJetCeef_barrel_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetCeef_barrel_stack)

  isrJetNeef_barrel_stack = getStack(":isrJetNeef;Neef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)<=1.479", signals)
  isrJetNeef_barrel_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetNeef_barrel_stack)

  isrJetHFhef_barrel_stack = getStack(":isrJetHFhef;HFhef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)<=1.479", signals)
  isrJetHFhef_barrel_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetHFhef_barrel_stack)

  isrJetHFeef_barrel_stack = getStack(":isrJetHFeef;HFeef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)<=1.479", signals)
  isrJetHFeef_barrel_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetHFeef_barrel_stack)

  isrJetMuef_barrel_stack = getStack(":isrJetMuef;Muef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)<=1.479", signals)
  isrJetMuef_barrel_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetMuef_barrel_stack)

  isrJetElef_barrel_stack = getStack(":isrJetElef;Elef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)<=1.479", signals)
  isrJetElef_barrel_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetElef_barrel_stack)

  isrJetPhef_barrel_stack = getStack(":isrJetPhef;Phef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)<=1.479", signals)
  isrJetPhef_barrel_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetPhef_barrel_stack)

  isrJetPt_endcap_stack = getStack(":isrJetPt;p_{T} of ISR jet;Number of Events / 50 GeV",[50,0,1000], commoncf+"&&abs(isrJetEta)>1.479", signals)
  isrJetPt_endcap_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetPt_endcap_stack)

  isrJetChef_endcap_stack = getStack(":isrJetChef;Chef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)>1.479", signals)
  isrJetChef_endcap_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetChef_endcap_stack)

  isrJetNhef_endcap_stack = getStack(":isrJetNhef;Nhef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)>1.479", signals)
  isrJetNhef_endcap_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetNhef_endcap_stack)

  isrJetCeef_endcap_stack = getStack(":isrJetCeef;Ceef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)>1.479", signals)
  isrJetCeef_endcap_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetCeef_endcap_stack)

  isrJetNeef_endcap_stack = getStack(":isrJetNeef;Neef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)>1.479", signals)
  isrJetNeef_endcap_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetNeef_endcap_stack)

  isrJetHFhef_endcap_stack = getStack(":isrJetHFhef;HFhef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)>1.479", signals)
  isrJetHFhef_endcap_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetHFhef_endcap_stack)

  isrJetHFeef_endcap_stack = getStack(":isrJetHFeef;HFeef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)>1.479", signals)
  isrJetHFeef_endcap_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetHFeef_endcap_stack)

  isrJetMuef_endcap_stack = getStack(":isrJetMuef;Muef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)>1.479", signals)
  isrJetMuef_endcap_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetMuef_endcap_stack)

  isrJetElef_endcap_stack = getStack(":isrJetElef;Elef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)>1.479", signals)
  isrJetElef_endcap_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetElef_endcap_stack)

  isrJetPhef_endcap_stack = getStack(":isrJetPhef;Phef of ISR jet;Number of Events",[20,0,1], commoncf+"&&abs(isrJetEta)>1.479", signals)
  isrJetPhef_endcap_stack[0].addOverFlowBin = "upper"
  allStacks.append(isrJetPhef_endcap_stack)

  nHardMuonsRelIso02_stack = getStack(":nHardMuonsRelIso02;n_{#mu};Number of Events ",[5,0,5], hadRefSel+"&&"+softIsolatedMu, signals)
  nHardMuonsRelIso02_stack[0].addOverFlowBin = "upper"
  allStacks.append(nHardMuonsRelIso02_stack)

  nHardMuons_stack = getStack(":nHardMuons;n_{#mu};Number of Events ",[5,0,5], hadRefSel+"&&"+softIsolatedMu, signals)
  nHardMuons_stack[0].addOverFlowBin = "upper"
  allStacks.append(nHardMuons_stack)

  nHardElectrons_stack = getStack(":nHardElectrons;n_{e};Number of Events ",[5,0,5], hadRefSel+"&&"+softIsolatedMu, signals)
  nHardElectrons_stack[0].addOverFlowBin = "upper"
  allStacks.append(nHardElectrons_stack)

  nHardTaus_stack = getStack(":nHardTaus;n_{#tau};Number of Events ",[5,0,5], commoncf, signals)
  nHardTaus_stack[0].addOverFlowBin = "upper"
  allStacks.append(nHardTaus_stack)

  njet_stack = getStack(":njet;n_{jet};Number of Events / 50 GeV",[10,0,10], commoncf.replace('&&njet60<=2',''), signals)
  njet_stack[0].addOverFlowBin = "upper"
  allStacks.append(njet_stack)

  njet60_stack = getStack(":njet60;n_{jet};Number of Events / 50 GeV",[10,0,10], commoncf.replace('&&njet60<=2',''), signals)
  njet60_stack[0].addOverFlowBin = "upper"
  allStacks.append(njet60_stack)
  

  ht_stack = getStack(":ht;H_{T} (GeV);Number of Events / 25 GeV",[40,0,1000], commoncf, signals)
  ht_stack[0].addOverFlowBin = "upper"
  allStacks.append(ht_stack)

  type1phiMet_stack = getStack(":type1phiMet;#slash{E}_{T} (GeV);Number of Events / 25 GeV",[40,0,1000], commoncf.replace('&&type1phiMet>250',''), signals)
  type1phiMet_stack[0].addOverFlowBin = "upper"
  allStacks.append(type1phiMet_stack)

  type1phiMetphi_stack = getStack(":type1phiMetphi;#phi(#slash{E}_{T});Number of Events",[40,-pi,pi], commoncf.replace('&&type1phiMetphi>250',''), signals)
  type1phiMetphi_stack[0].addOverFlowBin = "upper"
  allStacks.append(type1phiMetphi_stack)

  genmetphi_stack = getStack(":genmetphi;#phi(gen-#slash{E}_{T});Number of Events",[40,-pi, pi], commoncf.replace('&&genmetphi>250',''), signals)
  genmetphi_stack[0].addOverFlowBin = "upper"
  allStacks.append(genmetphi_stack)

  genmet_stack = getStack(":genmet;#slash{E}_{T} (GeV);Number of Events / 25 GeV",[40,0,1000], commoncf.replace('&&genmet>250',''), signals)
  genmet_stack[0].addOverFlowBin = "upper"
  genmet_stack[0].data_histo.GetXaxis().SetLabelSize(0.02)
  allStacks.append(genmet_stack)
  
  def fakeMETx(c): return c.GetLeaf('type1phiMet').GetValue()*cos(c.GetLeaf('type1phiMetphi').GetValue()) - c.GetLeaf('genmet').GetValue()*cos(c.GetLeaf('genmetphi').GetValue())
  fakeMETx_stack = getStack("xxx:;fake-#slash{E}_{x} (GeV);Number of Events / 4 GeV",[50,-100,100], commoncf, signals, varfunc = fakeMETx )
  fakeMETx_stack[0].addOverFlowBin = "upper"
  fakeMETx_stack[0].data_histo.GetXaxis().SetLabelSize(0.02)
  allStacks.append(fakeMETx_stack)

  def fakeMETy(c): return c.GetLeaf('type1phiMet').GetValue()*sin(c.GetLeaf('type1phiMetphi').GetValue()) - c.GetLeaf('genmet').GetValue()*sin(c.GetLeaf('genmetphi').GetValue())
  fakeMETy_stack = getStack("yyy:;fake-#slash{E}_{y} (GeV);Number of Events / 4 GeV",[50,-100,100], commoncf, signals, varfunc = fakeMETy )
  fakeMETy_stack[0].addOverFlowBin = "upper"
  fakeMETy_stack[0].data_histo.GetXaxis().SetLabelSize(0.02)
  allStacks.append(fakeMETy_stack)

  genmet_reversed_stack = copy.deepcopy(genmet_stack) 
  genmet_reversed_stack.reverse()
  genmet_reversed_stack[0].addOverFlowBin = "upper"
  genmet_reversed_stack[0].data_histo.GetXaxis().SetLabelSize(0.02)
  allStacks.append(genmet_reversed_stack)
    
  ngoodVertices_stack = getStack(":ngoodVertices;Number of Vertices;Number of Events",[51,0,51], commoncf, signals)
  ngoodVertices_stack[0].addOverFlowBin = "upper"
  allStacks.append(ngoodVertices_stack)

  softIsolatedMuPt_stack = getStack(":softIsolatedMuPt;p_{T} of soft isolated muon;Number of Events / 1 GeV",[25,0,25], commoncf, signals)
  softIsolatedMuPt_stack[0].addOverFlowBin = "upper"
  allStacks.append(softIsolatedMuPt_stack)

  softIsolatedMuEta_stack = getStack(":softIsolatedMuEta;#eta of soft isolated muon;Number of Events",[20,-4,4], commoncf, signals)
  softIsolatedMuEta_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuEta_stack)

  softIsolatedMuPhi_stack = getStack(":softIsolatedMuPhi;#phi of soft isolated muon;Number of Events",[20,-4,4], commoncf, signals)
  softIsolatedMuPhi_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuPhi_stack)

  softIsolatedMuCharge_stack = getStack(":XXX;charge of soft isolated muon;Number of Events",[3,-1,2], commoncf, signals, lambda c: c.GetLeaf('softIsolatedMuPdg').GetValue()/abs(c.GetLeaf('softIsolatedMuPdg').GetValue()))
  softIsolatedMuCharge_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuCharge_stack)

  softIsolatedMuRelIso_stack = getStack(":softIsolatedMuRelIso;I_{rel.} of soft isolated muon;Number of Events",[24,0,1.2], commoncf, signals)
  softIsolatedMuRelIso_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuRelIso_stack)

  softIsolatedMuAbsIso_stack = getStack(":XXX;I_{abs.} of soft isolated muon;Number of Events",[30,0,12], commoncf, signals, lambda c: c.GetLeaf('softIsolatedMuRelIso').GetValue()*c.GetLeaf('softIsolatedMuPt').GetValue())
  softIsolatedMuAbsIso_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuAbsIso_stack)

  softIsolatedMuRelIso_barrel_stack = getStack(":softIsolatedMuRelIso;I_{rel.} of soft isolated muon;Number of Events",[24,0,1.2], commoncf+"&&abs(softIsolatedMuEta)<=1.1", signals)
  softIsolatedMuRelIso_barrel_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuRelIso_barrel_stack)

  softIsolatedMuAbsIso_barrel_stack = getStack(":XXX;I_{abs.} of soft isolated muon;Number of Events",[30,0,12], commoncf+"&&abs(softIsolatedMuEta)<=1.1", signals, lambda c: c.GetLeaf('softIsolatedMuRelIso').GetValue()*c.GetLeaf('softIsolatedMuPt').GetValue())
  softIsolatedMuAbsIso_barrel_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuAbsIso_barrel_stack)

  softIsolatedMuRelIso_endcap_stack = getStack(":softIsolatedMuRelIso;I_{rel.} of soft isolated muon;Number of Events",[24,0,1.2], commoncf+"&&abs(softIsolatedMuEta)>1.1", signals)
  softIsolatedMuRelIso_endcap_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuRelIso_endcap_stack)

  softIsolatedMuAbsIso_endcap_stack = getStack(":XXX;I_{abs.} of soft isolated muon;Number of Events",[30,0,12], commoncf+"&&abs(softIsolatedMuEta)>1.1", signals, lambda c: c.GetLeaf('softIsolatedMuRelIso').GetValue()*c.GetLeaf('softIsolatedMuPt').GetValue())
  softIsolatedMuAbsIso_endcap_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuAbsIso_endcap_stack)

  softIsolatedMuDxy_stack = getStack(":softIsolatedMuDxy;d_{xy} of soft isolated muon;Number of Events",[40,0,.04], commoncf, signals)
  softIsolatedMuDxy_stack[0].addOverFlowBin = "both"
  allStacks.append(softIsolatedMuDxy_stack)


  isrJetFull53XPUJetIDTight_stack = getStack(":isrJetFull53XPUJetIDTight;isrJetFull53XPUJetIDTight;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Tight'))
  allStacks.append(isrJetFull53XPUJetIDTight_stack)
  isrJetFull53XPUJetIDMedium_stack = getStack(":isrJetFull53XPUJetIDMedium;isrJetFull53XPUJetIDMedium;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Medium'))
  allStacks.append(isrJetFull53XPUJetIDMedium_stack)
  isrJetFull53XPUJetIDLoose_stack = getStack(":isrJetFull53XPUJetIDLoose;isrJetFull53XPUJetIDLoose;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetFull53XPUJetIDFlag').GetValue()),'Loose'))
  allStacks.append(isrJetFull53XPUJetIDLoose_stack)

  isrJetMET53XPUJetIDTight_stack = getStack(":isrJetMET53XPUJetIDTight;isrJetMET53XPUJetIDTight;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Tight'))
  allStacks.append(isrJetMET53XPUJetIDTight_stack)
  isrJetMET53XPUJetIDMedium_stack = getStack(":isrJetMET53XPUJetIDMedium;isrJetMET53XPUJetIDMedium;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Medium'))
  allStacks.append(isrJetMET53XPUJetIDMedium_stack)
  isrJetMET53XPUJetIDLoose_stack = getStack(":isrJetMET53XPUJetIDLoose;isrJetMET53XPUJetIDLoose;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetMET53XPUJetIDFlag').GetValue()),'Loose'))
  allStacks.append(isrJetMET53XPUJetIDLoose_stack)
  
  isrJetCutBasedPUJetIDTight_stack = getStack(":isrJetCutBasedPUJetIDTight;isrJetCutBasedPUJetIDTight;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Tight'))
  allStacks.append(isrJetCutBasedPUJetIDTight_stack)
  isrJetCutBasedPUJetIDMedium_stack = getStack(":isrJetCutBasedPUJetIDMedium;isrJetCutBasedPUJetIDMedium;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Medium'))
  allStacks.append(isrJetCutBasedPUJetIDMedium_stack)
  isrJetCutBasedPUJetIDLoose_stack = getStack(":isrJetCutBasedPUJetIDLoose;isrJetCutBasedPUJetIDLoose;Number of Events",[2,0,2], commoncf, signals,lambda c: passPUJetID(int(c.GetLeaf('isrJetCutBasedPUJetIDFlag').GetValue()),'Loose'))
  allStacks.append(isrJetCutBasedPUJetIDLoose_stack)


for stack in allStacks:
  stack[0].minimum = minimum
#for stack in allStacks:
#  for var in stack:
#    var.addOverFlowBin = "both"
#reweightingHistoFile = "PU/reweightingHisto_Summer2012-S10-Run2012AB-Jul13ReReco.root"
reweightingHistoFile = ""

execfile("../../RA4Analysis/plots/simplePlotsLoopKernel.py")

#if normalizeToData:
#  for stack in allStacks:
#    for var in stack[:-1]:
#      var.normalizeTo = stack[-1]
#      var.normalizeWhat = stack[0]
#    stack[-1].normalizeTo=""
#    stack[-1].normalizeWhat=""
#else:
#  for stack in allStacks:
#    for var in stack:
#      var.normalizeTo = ""
#      var.normalizeWhat = "" 

for stack in allStacks:
  stack[0].maximum = 4*10**4 # 10.*stack[-1].data_histo.GetMaximum()
  stack[0].logy = True
  stack[0].minimum = minimum
#  stack[0].legendCoordinates=[0.76,0.95 - 0.3,.98,.95]
#  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS preliminary}"], [0.2,0.85,str(int(round(targetLumi)))+" pb^{-1},  #sqrt{s} = 7 TeV"]]
  stack[0].legendCoordinates=[0.51,0.95 - 0.08*3 ,.98,.95]
  stack[0].lines = [[0.2, 0.9, "#font[22]{CMS Collaboration}"], [0.2,0.85,str(int(round(targetLumi/10.))/100.)+" fb^{-1}"],[0.2,0.8,  "#sqrt{s} = 8 TeV"]]


drawNMStacks(1,1,[isrJetPt_stack],             subdir+prefix+"isrJetPt", False)
drawNMStacks(1,1,[softIsolatedMuNormChi2_stack                       ]   , subdir+prefix+"softIsolatedMuNormChi2", False)
drawNMStacks(1,1,[softIsolatedMuNValMuonHits_stack                   ]   , subdir+prefix+"softIsolatedMuNValMuonHits", False)
drawNMStacks(1,1,[softIsolatedMuNumMatchedStations_stack             ]   , subdir+prefix+"softIsolatedMuNumMatchedStations", False)
drawNMStacks(1,1,[softIsolatedMuPixelHits_stack                      ]   , subdir+prefix+"softIsolatedMuPixelHits", False)
drawNMStacks(1,1,[softIsolatedMuPixelHits_lowDz_stack                      ]   , subdir+prefix+"softIsolatedMuPixelHits_lowDz", False)
drawNMStacks(1,1,[softIsolatedMuPixelHits_highDz_stack                      ]   , subdir+prefix+"softIsolatedMuPixelHits_highDz", False)
drawNMStacks(1,1,[softIsolatedMuNumtrackerLayerWithMeasurement_stack ]   , subdir+prefix+"softIsolatedMuNumtrackerLayerWithMeasurement", False)
drawNMStacks(1,1,[softIsolatedMuIsGlobal_stack                       ]   , subdir+prefix+"softIsolatedMuIsGlobal", False)
drawNMStacks(1,1,[softIsolatedMuIsTracker_stack                       ]   , subdir+prefix+"softIsolatedMuIsTracker", False)
drawNMStacks(1,1,[softIsolatedMuDz_stack],            subdir+prefix+"softIsolatedMuDz", False)
drawNMStacks(1,1,[softIsolatedMuDz_zoomed_stack],            subdir+prefix+"softIsolatedMuDz_zoomed", False)


if not doOnlyOne:
  drawNMStacks(1,1,[isrJetEta_stack],             subdir+prefix+"isrJetEta", False)
  drawNMStacks(1,1,[isrJetPhi_stack],             subdir+prefix+"isrJetPhi", False)
  drawNMStacks(1,1,[isrJetPdg_stack],             subdir+prefix+"isrJetPdg", False)
  drawNMStacks(1,1,[isrJetBtag_stack],            subdir+prefix+"isrJetBtag", False)
  drawNMStacks(1,1,[isrJetChef_stack],            subdir+prefix+"isrJetChef", False)
  drawNMStacks(1,1,[isrJetNhef_stack],            subdir+prefix+"isrJetNhef", False)
  drawNMStacks(1,1,[isrJetCeef_stack],            subdir+prefix+"isrJetCeef", False)
  drawNMStacks(1,1,[isrJetNeef_stack],            subdir+prefix+"isrJetNeef", False)
  drawNMStacks(1,1,[isrJetHFhef_stack],           subdir+prefix+"isrJetHFhef", False)
  drawNMStacks(1,1,[isrJetHFeef_stack],           subdir+prefix+"isrJetHFeef", False)
  drawNMStacks(1,1,[isrJetMuef_stack],            subdir+prefix+"isrJetMuef", False)
  drawNMStacks(1,1,[isrJetElef_stack],            subdir+prefix+"isrJetElef", False)
  drawNMStacks(1,1,[isrJetPhef_stack],            subdir+prefix+"isrJetPhef", False)

  drawNMStacks(1,1,[isrJetPt_barrel_stack],              subdir+prefix+"barrel_isrJetPt", False)
  drawNMStacks(1,1,[isrJetChef_barrel_stack],            subdir+prefix+"barrel_isrJetChef", False)
  drawNMStacks(1,1,[isrJetNhef_barrel_stack],            subdir+prefix+"barrel_isrJetNhef", False)
  drawNMStacks(1,1,[isrJetCeef_barrel_stack],            subdir+prefix+"barrel_isrJetCeef", False)
  drawNMStacks(1,1,[isrJetNeef_barrel_stack],            subdir+prefix+"barrel_isrJetNeef", False)
  drawNMStacks(1,1,[isrJetHFhef_barrel_stack],           subdir+prefix+"barrel_isrJetHFhef", False)
  drawNMStacks(1,1,[isrJetHFeef_barrel_stack],           subdir+prefix+"barrel_isrJetHFeef", False)
  drawNMStacks(1,1,[isrJetMuef_barrel_stack],            subdir+prefix+"barrel_isrJetMuef", False)
  drawNMStacks(1,1,[isrJetElef_barrel_stack],            subdir+prefix+"barrel_isrJetElef", False)
  drawNMStacks(1,1,[isrJetPhef_barrel_stack],            subdir+prefix+"barrel_isrJetPhef", False)

  drawNMStacks(1,1,[isrJetPt_endcap_stack],              subdir+prefix+"endcap_isrJetPt", False)
  drawNMStacks(1,1,[isrJetChef_endcap_stack],            subdir+prefix+"endcap_isrJetChef", False)
  drawNMStacks(1,1,[isrJetNhef_endcap_stack],            subdir+prefix+"endcap_isrJetNhef", False)
  drawNMStacks(1,1,[isrJetCeef_endcap_stack],            subdir+prefix+"endcap_isrJetCeef", False)
  drawNMStacks(1,1,[isrJetNeef_endcap_stack],            subdir+prefix+"endcap_isrJetNeef", False)
  drawNMStacks(1,1,[isrJetHFhef_endcap_stack],           subdir+prefix+"endcap_isrJetHFhef", False)
  drawNMStacks(1,1,[isrJetHFeef_endcap_stack],           subdir+prefix+"endcap_isrJetHFeef", False)
  drawNMStacks(1,1,[isrJetMuef_endcap_stack],            subdir+prefix+"endcap_isrJetMuef", False)
  drawNMStacks(1,1,[isrJetElef_endcap_stack],            subdir+prefix+"endcap_isrJetElef", False)
  drawNMStacks(1,1,[isrJetPhef_endcap_stack],            subdir+prefix+"endcap_isrJetPhef", False)


  drawNMStacks(1,1,[softIsolatedMuPt_stack],             subdir+prefix+"softIsolatedMuPt", False)
  drawNMStacks(1,1,[nHardMuonsRelIso02_stack],             subdir+prefix+"nHardMuonsRelIso02", False)
  drawNMStacks(1,1,[nHardMuons_stack],             subdir+prefix+"nHardMuons", False)
  drawNMStacks(1,1,[nHardElectrons_stack],             subdir+prefix+"nHardElectrons", False)
  drawNMStacks(1,1,[nHardTaus_stack],             subdir+prefix+"nHardTaus", False)
  drawNMStacks(1,1,[njet_stack],             subdir+prefix+"njet", False)
  drawNMStacks(1,1,[njet60_stack],             subdir+prefix+"njet60", False)
  drawNMStacks(1,1,[type1phiMet_stack],             subdir+prefix+"type1phiMet", False)
  drawNMStacks(1,1,[type1phiMetphi_stack],             subdir+prefix+"type1phiMetphi", False)
  drawNMStacks(1,1,[genmetphi_stack],             subdir+prefix+"genmetphi", False)
  drawNMStacks(1,1,[ht_stack],             subdir+prefix+"ht", False)
  drawNMStacks(1,1,[genmet_stack],             subdir+prefix+"genmet", False)
  drawNMStacks(1,1,[genmet_reversed_stack],             subdir+prefix+"genmet_reversed", False)
  drawNMStacks(1,1,[ngoodVertices_stack],             subdir+prefix+"ngoodVertices", False)
  drawNMStacks(1,1,[fakeMETx_stack],             subdir+prefix+"fakeMETx", False)
  drawNMStacks(1,1,[fakeMETy_stack],             subdir+prefix+"fakeMETy", False)

  drawNMStacks(1,1,[softIsolatedMuPt_stack],            subdir+prefix+"softIsolatedMuPt", False)
  drawNMStacks(1,1,[softIsolatedMuEta_stack],            subdir+prefix+"softIsolatedMuEta", False)
  drawNMStacks(1,1,[softIsolatedMuPhi_stack],            subdir+prefix+"softIsolatedMuPhi", False)
  drawNMStacks(1,1,[softIsolatedMuCharge_stack],            subdir+prefix+"softIsolatedMuCharge", False)
  drawNMStacks(1,1,[softIsolatedMuRelIso_stack],            subdir+prefix+"softIsolatedMuRelIso", False)
  drawNMStacks(1,1,[softIsolatedMuAbsIso_stack],            subdir+prefix+"softIsolatedMuAbsIso", False)
  drawNMStacks(1,1,[softIsolatedMuRelIso_barrel_stack],            subdir+prefix+"barrel_softIsolatedMuRelIso", False)
  drawNMStacks(1,1,[softIsolatedMuAbsIso_barrel_stack],            subdir+prefix+"barrel_softIsolatedMuAbsIso", False)
  drawNMStacks(1,1,[softIsolatedMuRelIso_endcap_stack],            subdir+prefix+"endcap_softIsolatedMuRelIso", False)
  drawNMStacks(1,1,[softIsolatedMuAbsIso_endcap_stack],            subdir+prefix+"endcap_softIsolatedMuAbsIso", False)
  drawNMStacks(1,1,[softIsolatedMuDxy_stack],            subdir+prefix+"softIsolatedMuDxy", False)

  drawNMStacks(1,1,[isrJetFull53XPUJetIDTight_stack], subdir+prefix+"isrJetFull53XPUJetIDTight", False)
  drawNMStacks(1,1,[isrJetFull53XPUJetIDMedium_stack], subdir+prefix+"isrJetFull53XPUJetIDMedium", False)
  drawNMStacks(1,1,[isrJetFull53XPUJetIDLoose_stack], subdir+prefix+"isrJetFull53XPUJetIDLoose", False)
  drawNMStacks(1,1,[isrJetMET53XPUJetIDTight_stack], subdir+prefix+"isrJetMET53XPUJetIDTight", False)
  drawNMStacks(1,1,[isrJetMET53XPUJetIDMedium_stack], subdir+prefix+"isrJetMET53XPUJetIDMedium", False)
  drawNMStacks(1,1,[isrJetMET53XPUJetIDLoose_stack], subdir+prefix+"isrJetMET53XPUJetIDLoose", False)
  drawNMStacks(1,1,[isrJetCutBasedPUJetIDTight_stack], subdir+prefix+"isrJetCutBasedPUJetIDTight", False)
  drawNMStacks(1,1,[isrJetCutBasedPUJetIDMedium_stack], subdir+prefix+"isrJetCutBasedPUJetIDMedium", False)
  drawNMStacks(1,1,[isrJetCutBasedPUJetIDLoose_stack], subdir+prefix+"isrJetCutBasedPUJetIDLoose", False)
