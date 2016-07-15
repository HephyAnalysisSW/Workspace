import ROOT
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
#from rCShelpers import *
import math
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *

from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_antiSel_postProcessed import *


ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

#weight_str, weight_err_str = makeWeight(lumi, sampleLumi, reWeight=MCweight)

weight_str = 'weight'#*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*TopPtWeight*0.94'

triggers = "(HLT_EleHT350||HLT_MuHT350)"
filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter "#&& veto_evt_list"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"
presel += "&&singleMuonic"

presel = 'nLep==1&&nVeto==0&&leptonPt>25&&nEl==1&&Jet2_pt>80'
antiSelStr = presel+'&&Selected==(-1)'
SelStr = presel+'&&Selected==1'


njet = (5,5)
nbjet = (0,0)

ltbins = [(250,350), (350,450), (450,-1)]
htbins = [(500,750), (750,1000), (1000,-1)]
njetbins = [(3,3),(4,4),(5,5),(6,7),(8,-1)]


#nbins = len(ltbins)*len(htbins)
nbins = len(njetbins)

binning = [nbins,0,nbins]

# samples
TTJets_combined = {'name':'TTJets', 'chain':getChain(TTJets_Comb_antiSel,histname=''), 'color':color('TTJets')-2, 'niceName':'t#bar{t}+Jets', 'cut':''}
WJETS           = {'name':'WJets', 'chain':getChain(WJetsHTToLNu_antiSel,histname=''), 'color':color('WJets'), 'niceName':'W+Jets', 'cut':''}
DY              = {'name':'DY', 'chain':getChain(DY_HT_antiSel,histname=''), 'color':color('DY'), 'niceName':'Drell Yan', 'cut':''}
singleTop       = {'name':'singleTop', 'chain':getChain(singleTop_lep_antiSel,histname=''), 'color':color('singleTop'), 'niceName':'t/#bar{t}', 'cut':''}
QCD             = {'name':'QCD', 'chain':getChain(QCDHT_antiSel,histname=''), 'color':color('QCD'), 'niceName':'QCD multijet', 'cut':''}
TTV            = {'name':'TTV', 'chain':getChain(TTV_antiSel,histname=''), 'color':color('TTV'), 'niceName':'t#bar{t}W', 'cut':''}

#samples 2015
TTJets_combined = {'name':'TTJets', 'chain':getChain(TTJets_combined_2_antiSel,histname=''), 'color':color('TTJets')-2, 'niceName':'t#bar{t}+Jets', 'cut':''}
WJETS           = {'name':'WJets', 'chain':getChain(WJetsHTToLNu_25ns_antiSel,histname=''), 'color':color('WJets'), 'niceName':'W+Jets', 'cut':''}
DY              = {'name':'DY', 'chain':getChain(DY_25ns_antiSel,histname=''), 'color':color('DY'), 'niceName':'Drell Yan', 'cut':''}
singleTop       = {'name':'singleTop', 'chain':getChain(singleTop_25ns_antiSel,histname=''), 'color':color('singleTop'), 'niceName':'t/#bar{t}', 'cut':''}
QCD             = {'name':'QCD', 'chain':getChain(QCDHT_25ns_antiSel,histname=''), 'color':color('QCD'), 'niceName':'QCD multijet', 'cut':''}
TTV            = {'name':'TTV', 'chain':getChain(TTV_25ns_antiSel,histname=''), 'color':color('TTV'), 'niceName':'t#bar{t}W', 'cut':''}


samples = [QCD, TTJets_combined, WJETS, DY, singleTop, TTV]
for s in samples:
  s['hist'] = ROOT.TH1F(s['name'], s['name'], *binning)
  s['hist'].SetFillColor(s['color'])
  s['hist'].SetLineColor(s['color'])
  s['hist'].SetLineWidth(2)

i = 1

ltbins = [(250,350)]
ht = (500,-1)

for ilt,lt in enumerate(ltbins):
  #for iht,ht in enumerate(htbins):
  for injet, njet in enumerate(njetbins):
    total = 0.
    totalHDP = 0.
    for s in samples:
      #n,cut = nameAndCut(lt, ht, njet, btb=nbjet, presel=presel)
      n,cut = nameAndCut(lt, ht, njet, btb=nbjet, presel=antiSelStr, charge="", btagVar = 'nBJetMediumCSV30', stVar = 'Lt', htVar = 'htJet30clean', njetVar='nJet30clean')
      y = getYieldFromChain(s['chain'], cut, weight_str)
      if ht[0]>900: dPhiCut = 0.75
      else: dPhiCut = 1.
      yHDP = getYieldFromChain(s['chain'], cut+'&&deltaPhi_Wl>'+str(dPhiCut), weight_str)
      total = total + y
      totalHDP = totalHDP + yHDP
      s['hist'].SetBinContent(i,y)
    print i, lt, ht, round(total,1), dPhiCut, round(totalHDP,2)
    for s in samples:
      #s['hist'].SetBinContent(i,s['hist'].GetBinContent(i)/total)
      s['hist'].GetXaxis().SetBinLabel(i, str(njet))
      #s['hist'].GetXaxis().SetBinLabel(i, '#splitline{LT'+str(ilt+1)+'}{HT'+str(iht+1)+'}')
    i = i+1
    

can = ROOT.TCanvas('can','can',700,700)

stack = ROOT.THStack()
ymin = 0.95-len(samples)*0.035
leg = ROOT.TLegend(0.7,ymin,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.035)

for s in samples:
  stack.Add(s['hist'])
  leg.AddEntry(s['hist'],s['niceName'],'f')

stack.SetMaximum(1.3)
stack.SetMinimum(0)

stack.Draw()
leg.Draw()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)
latex1.DrawLatex(0.17,0.96,'CMS #bf{#it{preliminary}}')
latex1.DrawLatex(0.79,0.96,"MC (13TeV)")

filestr = '/afs/hephy.at/user/d/dspitzbart/www/Spring16/composition/QCD/antiselected_abs'

can.Print(filestr+'.png')
can.Print(filestr+'.pdf')
can.Print(filestr+'.root')


