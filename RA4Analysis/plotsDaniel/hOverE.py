import ROOT
from ROOT import RooFit as rf
import pickle 
import copy, os, sys
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.TH1F().SetDefaultSumw2()
ROOT.setTDRStyle()
ROOT.gStyle.SetMarkerStyle(1)
ROOT.gStyle.SetOptTitle(0)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *

from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_antiSel_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_Promtv2_antiSel_postprocessed import *

from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_antiSel import *
from Workspace.RA4Analysis.cmgTuples_Data_25ns_postProcessed_antiSel import *

def makeWeight(lumi=3., sampleLumi=3.,debug=False, reWeight='lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*TopPtWeight*0.94'):
  if debug:
    print 'No lumi-reweighting done!!'
    return 'weight', 'weight*weight'
  else:
    weight_str = '((weight/'+str(sampleLumi)+')*'+str(lumi)+'*'+reWeight+')'
    weight_err_str = '('+weight_str+'*'+weight_str+')'
  return weight_str, weight_err_str

lumi = 2.57
lumi15 = 2.25
sampleLumi = 3.0 #post processed sample already produced with 2.25fb-1
weight15_str, weight15_err_str = makeWeight(lumi15, sampleLumi)
weight_str, weight_err_str = makeWeight(lumi, sampleLumi, reWeight='(1)')


trigger = "&&((isData&&(HLT_EleHT350||HLT_MuHT350))||!isData)"
filters = "&&Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter "#&& veto_evt_list"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_eeBadScFilter"

presel = 'nLep==1&&nVeto==0&&leptonPt>25&&nEl==1&&Jet2_pt>80'
antiSelStr = presel+'&&Selected==(-1)'+trigger+filters
SelStr = presel+'&&Selected==1'+trigger+filters

cQCD16  = getChain(QCDHT_antiSel,histname='')
cEWK16  = getChain([WJetsHTToLNu_antiSel, TTJets_Lep_antiSel, singleTop_lep_antiSel, DY_madgraph_antiSel, TTV_antiSel],histname='')
cMC16  = getChain([QCDHT_antiSel,WJetsHTToLNu_antiSel, TTJets_Lep_antiSel, singleTop_lep_antiSel, DY_madgraph_antiSel, TTV_antiSel],histname='')
cData16 = getChain(single_ele_Run2016B_antiSel, histname='')

cQCD15  = getChain(QCDHT_25ns_antiSel,histname='')
cEWK15  = getChain([WJetsHTToLNu_25ns_antiSel, TTJets_combined_2_antiSel, singleTop_25ns_antiSel, DY_25ns_antiSel, TTV_25ns_antiSel],histname='')
cMC15  = getChain([QCDHT_25ns_antiSel,WJetsHTToLNu_25ns_antiSel, TTJets_combined_2_antiSel, singleTop_25ns_antiSel, DY_25ns_antiSel, TTV_25ns_antiSel],histname='')
cData15 = getChain(single_ele_Run2015D_antiSel, histname='')


hMC15 = ROOT.TH1F('hMC15','MC 2015',100,0,0.5)
hMC15.SetLineColor(ROOT.kOrange)

hData15 = ROOT.TH1F('hData15','Data 2015',100,0,0.5)
hData15.SetLineColor(ROOT.kRed)

hMC16 = ROOT.TH1F('hMC16','MC 2016',100,0,0.5)
hMC16.SetLineColor(ROOT.kGreen+1)

hData16 = ROOT.TH1F('hData16','Data 2016',100,0,0.5)
hData16.SetLineColor(ROOT.kBlue)

hists = [hMC15,hData15,hMC16,hData16]

for h in hists:
  h.SetLineWidth(2)

#antiSelStr = SelStr

#var = 'LepGood_hOverE[0]'
var = 'LepGood_miniRelIso[0]'

cData16.Draw(var+'>>hData16',antiSelStr)
cData15.Draw(var+'>>hData15',antiSelStr)
cMC16.Draw(var+'>>hMC16',weight_str+'*('+antiSelStr+')')
cMC15.Draw(var+'>>hMC15','weight*('+antiSelStr+')') # in 2015 antiSel postprocessing already weighted to 2.25 fb-1

leg = ROOT.TLegend(0.7,0.75,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.045)

can = ROOT.TCanvas('can','can',700,700)
can.SetLogy()

first = True
for h in hists:
  h.Scale(1/h.Integral())
  h.SetMaximum(1)
  h.SetMinimum(0.001)
  s = 'hist same'
  if first:
    s = 'hist'
    first = False
  leg.AddEntry(h)
  h.Draw(s)

leg.Draw()


