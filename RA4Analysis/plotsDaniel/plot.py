import ROOT
import os, sys, copy
import pickle, operator

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT400ST200_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Data25ns_0l import *
#from Workspace.RA4Analysis.cmgTuples_Data25ns_Artur import *

#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT400ST200_postProcessed_fromArthur import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT400ST200_postProcessed_btagWeight import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_btagWeight import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_fromArthur import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed_2 import *

from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2_postprocessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed_btag import *

#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT400ST200_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_postProcessed import *
from Workspace.HEPHYPythonTools.user import username

from helpers import *

def getBTagCutAndWeight(chain, btagcut, btagweight, cut, weight):
  if chain.GetBranchStatus(btagweight):
    return cut, weight+'*'+btagweight
  else:
    return cut+'&&'+btagcut, weight


lepSel = 'hard'
##50ns samples
#WJETS = {'name':'WJets', 'chain':getChain(WJetsToLNu_50ns,histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets'}
#TTJETS = {'name':'TTJets', 'chain':getChain(TTJets_50ns,histname=''), 'color':color('TTJets'),'weight':'weight', 'niceName':'t#bar{t} Jets'}
#DY = {'name':'DY', 'chain':getChain(DY_50ns,histname=''), 'color':color('DY'),'weight':'weight', 'niceName':'Drell Yan'}
#singleTop = {'name':'singleTop', 'chain':getChain(singleTop_50ns,histname=''), 'color':color('singleTop'),'weight':'weight', 'niceName':'single Top'}
#QCD = {'name':'QCD', 'chain':getChain(QCDMu_50ns,histname=''), 'color':color('QCD'),'weight':'weight', 'niceName':'QCD'}
#samples = [WJETS, TTJETS, DY, singleTop, QCD]


totalWeight = 'weight'#*puReweight_true*lepton_muSF_mediumID*lepton_muSF_miniIso02*lepton_muSF_sip3d*lepton_eleSF_cutbasedID*lepton_eleSF_miniIso01'
#25ns samples
WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu_25ns,histname=''), 'color':color('WJets'),'weight':totalWeight, 'niceName':'W+Jets', 'cut':''}
WJETS_2 = {'name':'WJets', 'chain':getChain(WJetsHTToLNu_25ns_2,histname=''), 'color':ROOT.kOrange,'weight':totalWeight, 'niceName':'W+Jets fix', 'cut':''}


TTJets = {'name':'TTJets', 'chain':getChain(TTJets_HTLO_25ns,histname=''), 'color':ROOT.kOrange,'weight':'weight', 'niceName':'t#bar{t}+Jets', 'cut':''}
TTJets_combined = {'name':'TTJets', 'chain':getChain(TTJets_combined,histname=''), 'color':color('TTJets')-2,'weight':totalWeight, 'niceName':'t#bar{t}+Jets', 'cut':''}
TTJets_combined_2 = {'name':'TTJets', 'chain':getChain(TTJets_combined_2,histname=''), 'color':ROOT.kMagenta,'weight':totalWeight, 'niceName':'t#bar{t}+Jets fix', 'cut':''}


TTJets_combined_singleLep = {'name':'TTJets', 'chain':TTJets_combined['chain'], 'color':color('TTJets')-2,'weight':totalWeight, 'niceName':'t#bar{t}+Jets 1l', 'cut':'(ngenLep+ngenTau)==1'}
TTJets_combined_diLep =     {'name':'TTJets', 'chain':TTJets_combined['chain'], 'color':color('TTJets'),'weight':totalWeight, 'niceName':'t#bar{t}+Jets 2l', 'cut':'(ngenLep+ngenTau)==2'}
TTJets_combined_had =       {'name':'TTJets', 'chain':TTJets_combined['chain'], 'color':color('TTJets')+2,'weight':totalWeight, 'niceName':'t#bar{t}+Jets 0l', 'cut':'(ngenLep+ngenTau)==0'}


DY = {'name':'DY', 'chain':getChain(DY_25ns,histname=''), 'color':color('DY'),'weight':totalWeight, 'niceName':'Drell Yan', 'cut':''}
singleTop = {'name':'singleTop', 'chain':getChain(singleTop_25ns,histname=''), 'color':color('singleTop'),'weight':totalWeight, 'niceName':'single Top', 'cut':''}
QCD = {'name':'QCD', 'chain':getChain(QCDHT_25ns,histname=''), 'color':color('QCD'),'weight':totalWeight, 'niceName':'QCD', 'cut':''}
TTVH = {'name':'TTVH', 'chain':getChain(TTV_25ns,histname=''), 'color':color('TTV'),'weight':totalWeight, 'niceName':'TTVH', 'cut':''}
Rest = {'name':'Rest', 'chain':getChain([TTV_25ns,singleTop_25ns,DY_25ns],histname=''), 'color':color('TTV'),'weight':totalWeight, 'niceName':'Rest EWK', 'cut':''}
Bkg = {'name':'Bkg', 'chain':getChain([TTJets_HTLO_25ns,WJetsHTToLNu_25ns,QCDHT_25ns,TTV_25ns,singleTop_25ns,DY_25ns],histname=''), 'color':color('TTV'),'weight':totalWeight, 'niceName':'total Bkg', 'cut':''}
EWK = {'name':'Bkg', 'chain':getChain([TTJets_HTLO_25ns,WJetsHTToLNu_25ns,TTV_25ns,singleTop_25ns,DY_25ns],histname=''), 'color':color('TTV'),'weight':totalWeight, 'niceName':'total Bkg', 'cut':''}
#diBoson = {'name':'diBoson', 'chain':getChain(diBosons_25ns,histname=''), 'color':ROOT.kMagenta,'weight':'weight', 'niceName':'diboson'}
samples = [WJETS, TTJets_combined, Rest, QCD]#, diBoson]
samplesTTcheck = [WJETS, TTJets_combined_singleLep, TTJets_combined_diLep, TTJets_combined_had, Rest, QCD]#, diBoson]

#samplesComp = [WJETS, TTJETS, singleTop, DY, QCD]

#EWK = {'name':'EWK', 'chain':getChain([WJetsHT_25ns,TTJets_HTLO_25ns,singleTop_25ns,DY_25ns,TTV_25ns],histname=''), 'color':color('DY'),'weight':'weight', 'niceName':'EWK'}

data = {'name':'data', 'chain':getChain([single_mu_Run2015D, single_ele_Run2015D],histname=''), 'color':ROOT.kBlack,'weight':'weight', 'niceName':'data', 'cut':''}


# older samples
#WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu[lepSel],histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets'}
#TTJETS = {'name':'TTJets', 'chain':getChain(ttJets[lepSel],histname=''), 'color':color('TTJets'),'weight':'weight', 'niceName':'t#bar{t} Jets'}
#DY = {}
#QCD = {}
#samples = [WJETS, TTJETS]#, DY, QCD]

##PHYS14 signals:
#T5qqqqWW_mGo1000_mCh800_mChi700 = {'name':'T5qqqqWW_mGo1000_mCh800_mChi700', 'chain':getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname=''), 'color':ROOT.kOrange+1,'weight':'weight*(3./4.)', 'niceName':'T5q^{4} 1.0/0.8/0.7'}
#T5qqqqWW_mGo1200_mCh1000_mChi800 = {'name':'T5qqqqWW_mGo1200_mCh1000_mChi800', 'chain':getChain(T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel],histname=''), 'color':ROOT.kRed+1,'weight':'weight*(3./4.)', 'niceName':'T5q^{4} 1.2/1.0/0.8'}
#T5qqqqWW_mGo1500_mCh800_mChi100 = {'name':'T5qqqqWW_mGo1500_mCh800_mChi100', 'chain':getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname=''), 'color':ROOT.kYellow+1,'weight':'weight*(3./4.)', 'niceName':'T5q^{4} 1.5/0.8/0.1'}
#WJETSPhys14 = {'name':'WJetsPhys14', 'chain':getChain(WJetsHTToLNu[lepSel],histname=''), 'color':ROOT.kOrange+1,'weight':'weight', 'niceName':'W Jets Phys14'}
#TTJETSPhys14 = {'name':'ttJetsPhys14', 'chain':getChain(ttJets[lepSel],histname=''), 'color':ROOT.kOrange+1,'weight':'weight', 'niceName':'t#bar{t} Jets Phys14'}


#signals = [T5qqqqWW_mGo1000_mCh800_mChi700,T5qqqqWW_mGo1200_mCh1000_mChi800,T5qqqqWW_mGo1500_mCh800_mChi100]

dPhiJet1Met = {'name':'acos(cos(Jet_phi[0]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{1},#slash{E}_{T})', 'titleY':'Events'}
dPhiJet2Met = {'name':'acos(cos(Jet_phi[1]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{2},#slash{E}_{T})', 'titleY':'Events'}
dPhiJet3Met = {'name':'acos(cos(Jet_phi[2]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{3},#slash{E}_{T})', 'titleY':'Events'}
dPhiJet4Met = {'name':'acos(cos(Jet_phi[3]-met_phi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{4},#slash{E}_{T})', 'titleY':'Events'}

mindPhiJetMet2 = {'name':'min(acos(cos(Jet_phi[0]-met_phi)),acos(cos(Jet_phi[1]-met_phi)))', 'binning':[16,0,pi], 'titleX':'min(#Delta#Phi(j_{1,2},#slash{E}_{T}))', 'titleY':'Events', 'fileName':'mindPhiJet12Met'}
mindPhiJetMet3 = {'name':'min(min(acos(cos(Jet_phi[0]-met_phi)),acos(cos(Jet_phi[1]-met_phi))),acos(cos(Jet_phi[2]-met_phi)))', 'binning':[16,0,pi], 'titleX':'min(#Delta#Phi(j_{1,2,3},#slash{E}_{T}))', 'titleY':'Events', 'fileName':'mindPhiJet123Met'}
mindPhiJetMet4 = {'name':'min(min(acos(cos(Jet_phi[0]-met_phi)),acos(cos(Jet_phi[1]-met_phi))),min(acos(cos(Jet_phi[2]-met_phi)),acos(cos(Jet_phi[3]-met_phi))))', 'binning':[16,0,pi], 'titleX':'min(#Delta#Phi(j_{1,2,3,4},#slash{E}_{T}))', 'titleY':'Events', 'fileName':'mindPhiJet1234Met'}

dPhiJet1GenMet = {'name':'acos(cos(Jet_phi[0]-met_genPhi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{1},#slash{E}_{T}^{gen})', 'titleY':'Events'}
dPhiJet2GenMet = {'name':'acos(cos(Jet_phi[1]-met_genPhi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{2},#slash{E}_{T}^{gen})', 'titleY':'Events'}
dPhiJet3GenMet = {'name':'acos(cos(Jet_phi[2]-met_genPhi))', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(j_{3},#slash{E}_{T}^{gen})', 'titleY':'Events'}

singleLeptonic = {'name':'singleLeptonic', 'binning':[2,0,2], 'titleX':'single leptonic', 'titleY':'Events'}
nLooseHardLeptons = {'name':'nLooseHardLeptons', 'binning':[4,0,4], 'titleX':'nLooseHardLeptons', 'titleY':'Events'}
nTightHardLeptons = {'name':'nTightHardLeptons', 'binning':[4,0,4], 'titleX':'nTightHardLeptons', 'titleY':'Events'}
nLooseSoftLeptons = {'name':'nLooseSoftLeptons', 'binning':[4,0,4], 'titleX':'nLooseSoftLeptons', 'titleY':'Events'}
nBJetMediumCSV30 = {'name':'nBJetMediumCSV30', 'binning':[5,0,5], 'titleX':'nBJetMediumCSV30', 'titleY':'Events'}
nBJetMedium30 = {'name':'nBJetMedium30', 'binning':[5,0,5], 'titleX':'nBJetMedium30', 'titleY':'Events'}

st = {'name':'st', 'binning':[37,250,2100], 'titleX':'L_{T} [GeV]', 'titleY':'Events'}
ht = {'name':'htJet30j', 'binning':[52,500,3100], 'titleX':'H_{T} [GeV]', 'titleY':'Events'}
njet = {'name':'nJet30', 'binning':[15,0,15], 'titleX':'n_{jets}', 'titleY':'Events', 'filename':'nJet30'}
deltaPhi = {'name':'deltaPhi_Wl', 'binning':[32,0,3.2], 'titleX':'#Delta#Phi(W,l)', 'titleY':'Events'}
deltaPhiRB = {'name':'deltaPhi_Wl', 'binning':[16,0,3.2], 'titleX':'#Delta#Phi(W,l)', 'titleY':'Events'}

leptonPt = {'name':'leptonPt', 'binning':[40,0,1000], 'titleX':'p_{T} [GeV]', 'titleY':'Events'}
lepGoodPt = {'name':'LepGood_pt[0]', 'binning':[22,0,1100], 'titleX':'p_{T} [GeV] (lepton)', 'titleY':'Events', 'filename':'LepGood_pt[0]'}
lepGoodEta = {'name':'LepGood_eta[0]', 'binning':[30,-3.,3.], 'titleX':'#eta (lepton)', 'titleY':'Events', 'filename':'LepGood_eta[0]'}
leadingJetPt = {'name':'Jet_pt[0]', 'binning':[40,0,2000], 'titleX':'p_{T} (leading jet) [GeV]', 'titleY':'Events', 'filename':'Jet_pt[0]'}
leadingJetPhi = {'name':'Jet_phi[0]', 'binning':[32,-3.2,3.2], 'titleX':'#Phi (leading jet)', 'titleY':'Events', 'filename':'Jet_phi[0]'}
invMass = {'name':'sqrt(2*LepGood_pt[0]*LepGood_pt[1]*(cosh(LepGood_eta[0]-LepGood_eta[1])-cos(LepGood_phi[0]-LepGood_phi[1])))','binning':[50,0,500], 'titleX':'M [GeV]', 'titleY':'Events', 'filename':'invMass'}


met = {'name':'met_pt', 'binning':[22,0,1100], 'titleX':'E_{T}^{miss} [GeV]', 'titleY':'Events', 'filename':'MET_pt'}
metPhi = {'name':'met_phi', 'binning':[16,-3.2,3.2], 'titleX':'#Phi(E_{T}^{miss})', 'titleY':'Events', 'filename':'MET_phi'}
metRawPhi = {'name':'met_rawPhi', 'binning':[16,-3.2,3.2], 'titleX':'#Phi(E_{T}^{miss}) raw', 'titleY':'Events'}
metNoHF = {'binning': [20, 0, 1000], 'name': 'metNoHF_pt', 'titleX': 'E_{T}^{miss} NoHF [GeV]', 'titleY': 'Events'}
metNoHFPhi = {'binning': [16, -3.2, 3.2], 'name': 'metNoHF_phi', 'titleX': '#Phi(E_{T}^{miss}) NoHF', 'titleY': 'Events'}
#deltaPhiCMG = {'binning': [16, 0, 3.2], 'name': 'Sum$((acos((LepGood_pt+metNoHF_pt*cos(LepGood_phi-metNoHF_phi))/sqrt(LepGood_pt**2+metNoHF_pt**2+2*metNoHF_pt*LepGood_pt*cos(LepGood_phi-metNoHF_phi))))*'+electronId+')', 'titleX': '#Delta#Phi(W,l) NoHF', 'titleY': 'Events'}

#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500&&nBJetMediumCSV30==0"
#preselNoLtHt = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&nBJetMediumCSV30==0"
#
#newpresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&st>250&&nJet30>=2&&htJet30j>500&&Jet_pt[1]>80" ####changed here!!
#newpresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&st>250&&nJet30>=2&&htJet30j>500&&Jet_pt[1]>80&&deltaPhi_Wl<0.5"
#filters = "&&Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_eeBadScFilter&&Flag_CSCTightHaloFilter"
#newpresel += filters

triggers = "(HLT_EleHT350||HLT_MuHT350)"
filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_CSCTightHaloFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"
newpresel = presel

singleMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)==1)'
singleElectronic = '(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.5&&LepGood_miniRelIso<0.2&&LepGood_SPRING15_25ns_v1==4)==1)'

multiMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)>=1)'
multiElectronic = '(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.5&&LepGood_miniRelIso<0.2&&LepGood_SPRING15_25ns_v1==4)>=1)'

multiLeptonic = '('+multiMuonic+'||'+multiElectronic+')'

diMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)==2)'
diElectronic = '(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.5&&LepGood_miniRelIso<0.2&&LepGood_SPRING15_25ns_v1==4)==2)'
ZcutOut = '(sqrt(2*LepGood_pt[0]*LepGood_pt[1]*(cosh(LepGood_eta[0]-LepGood_eta[1])-cos(LepGood_phi[0]-LepGood_phi[1])))>110||sqrt(2*LepGood_pt[0]*LepGood_pt[1]*(cosh(LepGood_eta[0]-LepGood_eta[1])-cos(LepGood_phi[0]-LepGood_phi[1])))<70)'

diOF = '('+singleMuonic+'&&'+singleElectronic+')'
diSF = '('+diMuonic+'||'+diElectronic+')'
diLep = '('+diOF+'||'+diMuonic+'||'+diElectronic+')'
diLepNoZ = '('+diOF+'||('+diMuonic+'&&'+ZcutOut+')||('+diElectronic+'&&'+ZcutOut+'))'
diLepOS = '('+diOF+'||('+diMuonic+'&&'+ZcutOut+')||('+diElectronic+'&&'+ZcutOut+'))&&(LepGood_pdgId[0]!=LepGood_pdgId[1])'

preselDiLep = '((isData&&'+triggers+'&&'+filters+')||(!isData))&&('+diLep + '&&Jet_pt[1]>80&&(LepGood_pt[0]+met_pt)>250&&nJet30>2&&htJet30j>500)'
preselDiLepNoZ = '((isData&&'+triggers+'&&'+filters+')||(!isData))&&('+diLepNoZ + '&&Jet_pt[1]>80&&(LepGood_pt[0]+met_pt)>250&&nJet30>2&&htJet30j>500)' 
preselDiLepOS = '((isData&&'+triggers+'&&'+filters+')||(!isData))&&('+diLepOS + '&&Jet_pt[1]>80&&(LepGood_pt[0]+met_pt)>250&&nJet30>2&&htJet30j>500)'
preselDiLepOF = '((isData&&'+triggers+'&&'+filters+')||(!isData))&&('+diOF + '&&Jet_pt[1]>80&&(LepGood_pt[0]+met_pt)>250&&nJet30>2&&htJet30j>500)'
preselDiLepSF = '((isData&&'+triggers+'&&'+filters+')||(!isData))&&('+diSF + '&&Jet_pt[1]>80&&(LepGood_pt[0]+met_pt)>250&&nJet30>2&&htJet30j>500)'
preselDiMu = '((isData&&'+triggers+'&&'+filters+')||(!isData))&&('+diMuonic + '&&Jet_pt[1]>80&&(LepGood_pt[0]+met_pt)>250&&nJet30>2&&htJet30j>500)'
preselDiEle = '((isData&&'+triggers+'&&'+filters+')||(!isData))&&('+diElectronic + '&&Jet_pt[1]>80&&(LepGood_pt[0]+met_pt)>250&&nJet30>2&&htJet30j>500)'

preselMultiLep = '((isData&&'+triggers+'&&'+filters+')||(!isData))&&('+ multiLeptonic + '&&Jet_pt[1]>80&&(LepGood_pt[0]+met_pt)>250&&nJet30>2&&htJet30j>500)'

noCut = {'name':'empty', 'string':'(1)', 'niceName':'no cut'}

name, cut = nameAndCut((250,350),(500,750),(4,5),btb=(0,-1),presel=newpresel)
ttSBbin1 = {'name':name,'string':cut,'niceName':'Lowest SR'}
ttSBbin1mu = {'name':name,'string':cut+'&&abs(leptonPdg)==13','niceName':'Lowest SR'}
ttSBbin1ele = {'name':name,'string':cut+'&&abs(leptonPdg)==11','niceName':'Lowest SR'}

name, cut = nameAndCut((250,-1),(500,-1),(3,3),btb=(0,-1),presel=newpresel)
ttSBincl = {'name':name,'string':cut,'niceName':'Lowest SR'}
ttSBinclmu = {'name':name,'string':cut+'&&abs(leptonPdg)==13','niceName':'Lowest SR'}
ttSBinclele = {'name':name,'string':cut+'&&abs(leptonPdg)==11','niceName':'Lowest SR'}

name, cut = nameAndCut((250,350),(500,750),(4,5),btb=(0,-1),presel=preselDiLepNoZ)
ttSBbin1diLep = {'name':name,'string':cut,'niceName':'Lowest SR'}

name, cut = nameAndCut((250,-1),(500,-1),(4,5),btb=(0,-1),presel=preselDiLepNoZ)
ttSBincldiLep = {'name':name,'string':cut,'niceName':'Lowest SR'}

name, cut = nameAndCut((450,-1),(500,-1),(5,5),btb=(0,0),presel=newpresel)

bin1 = {'name':name,'string':cut+'&&deltaPhi_Wl>1.','niceName':'Lowest SR'}
bin3 = {'name':name,'string':cut,'niceName':'Lowest SR'}
posWeightBin = {'name':'posWeight', 'string':cut+'&&weight>0', 'niceName':'pos. weight'}
negWeightBin = {'name':'negWeight', 'string':cut+'&&weight<0', 'niceName':'neg. weight'}

posWeight = {'name':'posWeight', 'string':newpresel+'&&weight>0', 'niceName':'pos. weight'}
negWeight = {'name':'negWeight', 'string':newpresel+'&&weight<0', 'niceName':'neg. weight'}

#newPreselNoLtHt = {'name':'presel','string':preselNoLtHt,'niceName':'Preselection'}
newPreselCut = {'name':'presel','string':newpresel,'niceName':'Preselection'}
newPreselCutBlinded = {'name':'presel','string':newpresel+'&&deltaPhi_Wl<0.5','niceName':'Preselection'}
newPreselCutHadTT = {'name':'presel','string':newpresel+'&&(ngenLep+ngenTau)==0','niceName':'Preselection'}
newPreselCutSemiLepTT = {'name':'presel','string':newpresel+'&&(ngenLep+ngenTau)==1','niceName':'Preselection'}
newPreselCutDiLepTT = {'name':'presel','string':newpresel+'&&(ngenLep+ngenTau)==2','niceName':'Preselection'}

newPreselCutDiLep = {'name':'presel','string':preselDiLep,'niceName':'Preselection 2l'}
newPreselCutDiLepNoZ = {'name':'presel','string':preselDiLepNoZ,'niceName':'Preselection 2l'}

newPreselCutDiLepOS = {'name':'presel','string':preselDiLepOS,'niceName':'2l OS'}
newPreselCutDiLepOF = {'name':'presel','string':preselDiLepOF,'niceName':'2l OF'}
newPreselCutDiLepSF = {'name':'presel','string':preselDiLepSF,'niceName':'Preselection 2l'}
newPreselCutDiMu = {'name':'presel','string':preselDiMu,'niceName':'Preselection 2mu'}
newPreselCutDiEle = {'name':'presel','string':preselDiEle,'niceName':'Preselection 2e'}


newPreselCutMultiLep = {'name':'presel','string':preselMultiLep, 'niceName':'#geq 1 lepton'}

newPreselCutSingleMuAN = {'name':'presel','string':newpresel+'&&singleMuonic','niceName':'Preselection'}
newPreselCutSingleEleAN = {'name':'presel','string':newpresel+'&&singleElectronic','niceName':'Preselection'}

name_ttSB, cut_ttSB = nameAndCut((250,-1),(500,-1),(4,5),btb=(1,1),presel=newpresel)
name_ttSBnoB, cut_ttSBnoB = nameAndCut((250,-1),(500,-1),(4,5),btb=None,presel=newpresel)
ttSB = {'name':'tt SB', 'string':cut_ttSB, 'niceName':'t#bar{t} SB'}
ttSBnoB = {'name':'tt SB', 'string':cut_ttSBnoB, 'niceName':'t#bar{t} SB'}

name_WSB, cut_WSB = nameAndCut((250,-1),(500,-1),(3,4),btb=(0,0),presel=newpresel)
name_WSBnoB, cut_WSBnoB = nameAndCut((250,-1),(500,-1),(3,4),btb=None,presel=newpresel)
WSB = {'name':'W SB', 'string':cut_WSB, 'niceName':'W SB'}
WSBnoB = {'name':'W SB', 'string':cut_WSBnoB, 'niceName':'W SB'}

name, cut = nameAndCut((250,350),(500,-1),(4,5),btb=(1,1),presel=newpresel)
cut1 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}

name, cut = nameAndCut((250,350),(500,-1),(3,4),btb=(0,0),presel=newpresel)
cut2 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}

Flag_EcalDeadCellTriggerPrimitiveFilter = {'name':'ecalFilterCut','string':newpresel+'&&Flag_EcalDeadCellTriggerPrimitiveFilter','niceName':'EcalDeadCellFilter'}
Flag_HBHENoiseFilter  = {'name':'ecalFilterCut','string':newpresel+'&&Flag_HBHENoiseFilter','niceName':'HBHENoiseFilter'}
Flag_CSCTightHaloFilter = {'name':'ecalFilterCut','string':newpresel+'&&Flag_CSCTightHaloFilter','niceName':'CSCTightHaloFilter'}
Flag_goodVertices = {'name':'ecalFilterCut','string':newpresel+'&&Flag_goodVertices','niceName':'goodVertices'}
Flag_eeBadScFilter = {'name':'ecalFilterCut','string':newpresel+'&&Flag_eeBadScFilter','niceName':'eeBadScFilter'}
allFiltersNoEcal = {'name':'ecalFilterCut','string':newpresel+'&&Flag_eeBadScFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter','niceName':'All but EcalDeadCell filter'}
allFilters = {'name':'ecalFilterCut','string':newpresel+'&&Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_eeBadScFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter','niceName':'All filters'}

filterCutList = [Flag_EcalDeadCellTriggerPrimitiveFilter,Flag_HBHENoiseFilter,Flag_CSCTightHaloFilter,Flag_goodVertices,Flag_eeBadScFilter,allFiltersNoEcal,allFilters]

fakeMet = "sqrt((met_pt*cos(met_phi)-met_genPt*cos(met_genPhi))**2+(met_pt*sin(met_phi)-met_genPt*sin(met_genPhi))**2)"
fakeMetSelection = '('+fakeMet+'>50||'+fakeMet+'>met_genPt)'
antiFakeMetSelection = '('+fakeMet+'<50&&'+fakeMet+'<met_genPt)'

AFMCut = {'name':'AFMCut','string':newpresel+"&&acos(cos(Jet_phi[0]-met_phi))>0.45&&acos(cos(Jet_phi[1]-met_phi))>0.45", 'niceName':'E_{T}^{miss} veto'}


#name, cut = nameAndCut((250,350),(1000,-1),(5,5),btb=(0,0),presel=newpresel)
#cut1 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [1000,-1)'}
#name, cut = nameAndCut((350,450),(750,1000),(5,5),btb=(0,0),presel=presel)
#cut2 = {'name':name,'string':cut,'niceName':'L_{T} [350,450), H_{T} [750,1000)'}
#name, cut = nameAndCut((450,-1),(750,1000),(5,5),btb=(0,0),presel=presel)
#cut3 = {'name':name,'string':cut,'niceName':'L_{T} [450,-1), H_{T} [750,1000)'}
#name, cut = nameAndCut((450,-1),(1000,-1),(5,5),btb=(0,0),presel=presel)
#cut4 = {'name':name,'string':cut,'niceName':'L_{T} [450,-1), H_{T} [1000,-1)'}
#name, cut = nameAndCut((450,-1),(500,750),(5,5),btb=(0,0),presel=presel)
#cut5 = {'name':name,'string':cut,'niceName':'L_{T} [450,-1), H_{T} [500,750)'}
#
#cuts = [cut1, cut2, cut3, cut4, cut5]

randomCut = 'weight*(singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&st>250&&st<350&&nJet30>=3&&htJet30j>500&&htJet30j<750&&nBJetMediumCSV30==0)'

name, cut = nameAndCut((250,350),(1000,-1),(5,5),btb=(0,0),presel=presel)
highFakeMetCut = {'name':name,'string':cut+'&&'+fakeMetSelection,'niceName':'E_{T}^{miss,fake} > 50 GeV || > E_{T}^{miss,gen}'}
lowFakeMetCut = {'name':name,'string':cut+'&&'+antiFakeMetSelection,'niceName':'E_{T}^{miss,fake} < 50 GeV && < E_{T}^{miss,gen}'}

##path25ns = '/data/easilar/cmgTuples/crab/Summer15_25nsV2MC_Data/'
##SingleElectron_Run2015C = {'name':'SingleElectron_Run2015C-PromptReco-v1', 'dir':path25ns+'SingleElectron_Run2015C/'}
##SingleMuon_Run2015C = {'name':'SingleMuon_Run2015C-PromptReco-v1', 'dir':path25ns+'SingleMuon_Run2015C/'}
##SingleMuonData = SingleMuon_Run2015D_PromptReco
#SingleMuonData = SingleMuon_Run2015D
##SingleElectronData = SingleElectron_Run2015D_PromptReco
#
##samples25ns = [SingleElectronData,SingleMuonData,MuonEG_Run2015D_PromptReco,DoubleEG_Run2015D_PromptReco,DoubleMuon_Run2015D_PromptReco,JetHT_Run2015D_PromptReco,MET_Run2015D_PromptReco]
#
#samples25ns = [SingleMuonData]
#
##dataSamples = samples25ns
##for s in dataSamples:
##  s['chunkString'] = s['name']
##  s.update({
##    "rootFileLocation":"tree.root",
##    "skimAnalyzerDir":"",
##    "treeName":"tree",
##    'isData':True,
##    #'dir' : data_path
##  })
#
#dSamples = []
##for sample in dataSamples:
#for sample in samples25ns:
#  dSamples.append({'name':sample['name'],'sample':sample})
#data = ROOT.TChain('tree')
#for sample in dSamples:
#  sample['chunks'], sample['nEvents'] = getChunks(sample['sample'])
#  for chunk in sample['chunks']:
#    data.Add(chunk['file'])

ele_MVAID_cuts_tight={'eta08':0.73 , 'eta104':0.57,'eta204': 0.05}
ele_MVAID_cuts_vloose = {'eta08':-0.11 , 'eta104':-0.35, 'eta204': -0.55}

ele_MVAID_cutstr_tight= "((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_tight['eta08'])+")"\
                       +"||((abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.44)&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_tight['eta104'])+")"\
                       +"||((abs(LepGood_eta)>=1.57)&&LepGood_mvaIdPhys14>"+str(ele_MVAID_cuts_tight['eta204'])+"))"
ele_MVAID_cutstr_vloose= "((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_vloose['eta08'])+")"\
                       +"||((abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.44)&&LepGood_mvaIdPhys14>"+ str(ele_MVAID_cuts_vloose['eta104'])+")"\
                       +"||((abs(LepGood_eta)>=1.57)&&LepGood_mvaIdPhys14>"+str(ele_MVAID_cuts_vloose['eta204'])+"))"

ele_MVAID_Spring15_cuts_tight={'eta08':0.87 , 'eta104':0.60,'eta204': 0.17}
ele_MVAID_Spring15_cuts_vloose = {'eta08':-0.16 , 'eta104':-0.65, 'eta204': -0.74}

ele_MVAID_Spring15_cutstr_tight= "((abs(LepGood_eta)<0.8&&LepGood__Spring15mvaIdSpring15>"+ str(ele_MVAID_Spring15_cuts_tight['eta08'])+")"\
                       +"||((abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.479)&&LepGood_mvaIdSpring15>"+ str(ele_MVAID_Spring15_cuts_tight['eta104'])+")"\
                       +"||((abs(LepGood_eta)>=1.479&&abs(LepGood_eta)<2.5)&&LepGood_mvaIdSpring15>"+str(ele_MVAID_Spring15_cuts_tight['eta204'])+"))"
ele_MVAID_Spring15_cutstr_vloose= "((abs(LepGood_eta)<0.8&&LepGood_mvaIdSpring15>"+ str(ele_MVAID_Spring15_cuts_vloose['eta08'])+")"\
                       +"||((abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.479)&&LepGood_mvaIdSpring15>"+ str(ele_MVAID_Spring15_cuts_vloose['eta104'])+")"\
                       +"||((abs(LepGood_eta)>=1.479&&abs(LepGood_eta)<2.5)&&LepGood_mvaIdSpring15>"+str(ele_MVAID_Spring15_cuts_vloose['eta204'])+"))"

singleMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)==1)'
diMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)==2)'
#singleMuonic = '(Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4)==1)'
singleElectronic = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.5&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0)==1)"
#singleElectronic = "(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4)==1)"
vetoElectron = '(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt<=10&&abs(LepGood_eta)<2.5&&LepGood_miniRelIso<0.4&&'+ele_MVAID_cutstr_vloose+')==0)'
#singleLeptonic = 'Sum$((abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)||(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.5&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0))==1'
singleLeptonic = "Sum$((abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)||(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.5&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0))==1"


electronId = "(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.5&&LepGood_miniRelIso<0.1&&"+ele_MVAID_cutstr_tight+"&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0)"
muonId = '(abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)'

LeptonId = '('+electronId+'||'+muonId+')'
LeptonReq = singleLeptonic
#LeptonId = muonId
#LeptonReq = singleMuonic

leptonVeto = '((abs(LepGood_pdgId)==11&&((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10&&abs(LepGood_eta)<2.4))==0&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<2.5))==1))\
             ||(abs(LepGood_pdgId)==13&&((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10&&abs(LepGood_eta)<2.4))==1&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<2.5))==0)))'

leptonVetoNoEta = '((abs(LepGood_pdgId)==11&&((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10))==0&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10))==1))\
             ||(abs(LepGood_pdgId)==13&&((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10))==1&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10))==0)))'

stStrMetNoHF = 'Sum$((LepGood_pt+metNoHF_pt)*'+LeptonId+')'
stStr = 'Sum$(LepGood_pt[0]+met_pt)'
stStrSimple = 'Sum$(LepGood_pt[0]+metNoHF_pt)'
htStr = 'Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))'
btagStr = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.890)'

htComp = {'name':htStr, 'binning':[52,500,3100], 'titleX':'H_{T} [GeV]', 'titleY':'Events', 'filename':'HT'}
stComp = {'name':stStr, 'binning':[37,250,2100], 'titleX':'L_{T} [GeV]', 'titleY':'Events', 'filename':'LT'}
nbjetComp = {'name':btagStr, 'binning':[6,0,6], 'titleX':'n_{b-jets}', 'titleY':'Events', 'filename':'nBJetMedium'}

#datapresel = '('+singleMuonic+'||'+singleElectronic+')&&nJet30>2&&nBJetMedium30>=0&&'+htStr+'>500&&'+stStr+'>200'
#trigger = "&&((HLT_ElNoIso||HLT_EleHT350)||(HLT_MuHT350||HLT_Mu50NoIso))"
#trigger = "&&((HLT_ElNoIso||HLT_EleHT350MET70)||(HLT_MuHT350MET70||HLT_Mu50NoIso))"
#trigger = "&&(HLT_EleHT350||HLT_MuHT350)"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilterMinZeroPatched&&Flag_goodVertices&&Flag_eeBadScFilter"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilterMinZeroPatched&&Flag_goodVertices&&Flag_eeBadScFilter"#&&Flag_EcalDeadCellTriggerPrimitiveFilter"

##datapresel = LeptonReq+'&&'+leptonVeto+'&&nJet30>=2&&nBJetMedium30>=0&&'+htStr+'>500&&'+stStr+'>250'
#datapresel = LeptonReq+'&&'+leptonVeto+'&&nJet30>=2&&'+htStr+'>500&&'+stStr+'>250'
#datacut = datapresel+trigger+filters
#dataDict = {'chain':data, 'cut':datacut,'name':'data'}

#data = {'name':'data', 'chain':getChain([SingleElectron_Run2015D,SingleMuon_Run2015D],histname=''), 'cut':newpresel+'&&SingleElectronic'+trigger}

deltaPhiCMG_NoHF = {'binning': [30, 0, 3.2], 'name': 'Sum$((acos((LepGood_pt+metNoHF_pt*cos(LepGood_phi-metNoHF_phi))/sqrt(LepGood_pt**2+metNoHF_pt**2+2*metNoHF_pt*LepGood_pt*cos(LepGood_phi-metNoHF_phi))))*'+LeptonId+')', 'titleX': '#Delta#Phi(W,l) NoHF', 'titleY': 'Events'}
#deltaPhiCMG = {'binning': [32, 0, 3.2], 'name': 'Sum$((acos((LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi))))*'+LeptonId+')', 'titleX': '#Delta#Phi(W,l) NoHF', 'titleY': 'Events', 'filename':'deltaPhi_Wl', 'binningIsExplicit':True}
deltaPhiCMG = {'binning': [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.1,1.3,1.5,1.8,2.2,2.6,3.2], 'name': 'Sum$((acos((LepGood_pt+met_pt*cos(LepGood_phi-met_phi))/sqrt(LepGood_pt**2+met_pt**2+2*met_pt*LepGood_pt*cos(LepGood_phi-met_phi))))*'+LeptonId+')', 'titleX': '#Delta#Phi(W,l) NoHF', 'titleY': 'Events', 'filename':'deltaPhi_Wl', 'binningIsExplicit':True}

dataPlotList = [stComp, htComp, deltaPhiCMG, met, njet, leadingJetPt, lepGoodPt, lepGoodEta, nbjetComp]

#for d in dataPlotList:
#  t = plot(samples,leadingJetPt,newPreselCut, data=dataDict,filling=True,stacking=True,minimum=0.08, maximum=2000, MClumiScale=205./3000., setLogY=True, lumi=0.205, titleText='CMS preliminary')
#  savePlot(t, d['titleX'])

def plot(samples, variable, cuts, signals=False, data=False, maximum=False, minimum=0., stacking=False, filling=True, setLogY=False, setLogX=False, titleText='simulation', lumi='3', legend=True, MClumiScale=1., drawError=False, MCscale=True, btagcut='nBJetMediumCSV30==0', btagweight='weightBTag0_SF'):
  if 'binningIsExplicit' in variable: binningIsExplicit = variable['binningIsExplicit']
  else: binningIsExplicit = False
  totalChain = ROOT.TChain('tree')
  for s in samples:
    totalChain.Add(s['chain'])
  if not type(samples)==type([]): samples = [samples]
  if not type(cuts)==type([]): cuts = [cuts]
  if signals:
    if not type(signals)==type([]): signals = [signals]
  can = ROOT.TCanvas('c','c',700,700)
  bottomMargin = 0.13
  if data:
    marginForPad2 = 0.3
    bottomMargin = 0.
  else:
    marginForPad2 = 0.
    bottomMargin = 0.13
  pad1=ROOT.TPad("pad1","MyTitle",0.,marginForPad2,1.,1.)
  pad1.SetLeftMargin(0.11)
  pad1.SetBottomMargin(bottomMargin)
  pad1.Draw()
  pad1.cd()
  colorList = [ROOT.kBlue+1, ROOT.kCyan-9, ROOT.kOrange-4, ROOT.kGreen+1, ROOT.kRed+1]
  h = []
  if binningIsExplicit: totalH = ROOT.TH1F('totalH', 'totalH', len(variable['binning'])-1, array('d', variable['binning']))
  else: totalH = ROOT.TH1F('totalH', 'totalH', *variable['binning'])
  nsamples = len(samples)
  ncuts = len(cuts)
  if data:
    #dataCutString = preselMultiLep
    #if data['cut']:
    #  dataCutString = cuts[0]['string'] +'&&'+ data['cut']
    #  print dataCutString
    #else: dataCutString = cuts[0]['string']
    dataCutString, dataweight = getBTagCutAndWeight(data['chain'], btagcut, btagweight, cuts[0]['string'], '(1)')
    dataYield, dataYieldError = getYieldFromChain(data['chain'],cutString=dataCutString,weight='(1)', returnError=True)
  if ncuts == 1 and data and MCscale:
    #if data['cut']: dataCutString = data['cut']
    #else: dataCutString = cuts[0]['string']
    #dataYield = getYieldFromChain(data['chain'],cutString=dataCutString,weight='(1)')
    #MCYield, MCYieldError = getYieldFromChain(totalChain,cutString=cuts[0]['string'],weight=str(MClumiScale)+'*''weight', returnError=True)
    MCYield = 0
    MCYieldError = 0
    for s in samples:
      normCut, normWeight = getBTagCutAndWeight(s['chain'], btagcut, btagweight, cuts[0]['string'], s['weight']+'*'+str(MClumiScale))
      if s['cut']:
        normCut = normCut + '&&' + s['cut']
        #print ' - cut:', sample['name']
      #print normCut, normWeight
      a, b = getYieldFromChain(s['chain'],cutString=normCut,weight=normWeight, returnError=True)
      #print a, b
      MCYield += a
      MCYieldError += b**2
    MCYieldError = sqrt(MCYieldError)
    #MCYield, MCYieldError = getYieldFromChain(totalChain,cutString=preselMultiLep,weight=str(MClumiScale)+'*weight', returnError=True)
    print 'Yield Data:\t', dataYield
    print 'Yield MC:\t', round(MCYield,1)
    MCscale = dataYield/MCYield
    MCscaleError = dataYield/MCYield*sqrt(MCYieldError**2/dataYield**2+dataYieldError**2/MCYield**2)
    print 'Area norm. factor:',round(MCscale,3),'+/-',round(MCscaleError,3)
  else: MCscale=1.
  for isample, sample in enumerate(samples):
    for icut, cut in enumerate(cuts):
      print
      i = isample*ncuts+icut
      if nsamples>1: legendName = sample['niceName']
      else: legendName = cut['niceName']
      if binningIsExplicit: h.append({'hist':ROOT.TH1F('h'+str(isample)+'_'+str(icut), legendName, len(variable['binning'])-1, array('d', variable['binning'])),'yield':0., 'legendName':legendName})
      else: h.append({'hist':ROOT.TH1F('h'+str(isample)+'_'+str(icut), legendName, *variable['binning']),'yield':0., 'legendName':legendName})
      normCut, normWeight = getBTagCutAndWeight(sample['chain'], btagcut, btagweight, cut['string'], sample['weight'])
      #print 'Will apply the following cuts and weight for sample',sample['name']
      #print 'Weight:'
      #if sample['weight']=='weight':
      #  weight='weight'
      #  print ' - chained weight'
      #else:
      #  weight=str(sample['weight'])
      #  print ' - weight:', weight
      print normWeight
      if sample['cut']:
        normCut = normCut + '&&' + sample['cut']
        print ' - cut:', sample['name']
      #else:
      #  useCut = cut['string']
      #  print ' - global cut'
      sample['chain'].Draw(variable['name']+'>>h'+str(isample)+'_'+str(icut),str(MCscale*MClumiScale)+'*'+normWeight+'*('+normCut+')','goff')
      totalH.Add(h[i]['hist'])
      h[i]['yield'] = h[i]['hist'].GetSumOfWeights()
      if minimum: h[i]['hist'].SetMinimum(minimum)
      if maximum: h[i]['hist'].SetMaximum(maximum)
      if filling:
        h[i]['hist'].SetLineColor(ROOT.kBlack)
        if len(samples)>1 or len(cuts)<2: h[i]['hist'].SetFillColor(sample['color'])
        else: h[i]['hist'].SetFillColor(colorList[icut])
      else:
        if len(samples)>1 or len(cuts)<2: h[i]['hist'].SetLineColor(sample['color'])
        else: h[i]['hist'].SetLineColor(colorList[icut])
      h[i]['hist'].SetLineWidth(2)
      h[i]['hist'].SetMarkerSize(0)
      h[i]['hist'].GetXaxis().SetTitle(variable['titleX'])
      h[i]['hist'].GetXaxis().SetNdivisions(508)
      #h[i]['hist'].GetXaxis().SetTitleSize(0.04)
      h[i]['hist'].GetYaxis().SetTitle(variable['titleY'])
      #h[i]['hist'].GetYaxis().SetTitleSize(0.04)
  h.sort(key=operator.itemgetter('yield'))
  legendNameLengthsSamples = [len(x['legendName']) for x in h]
  legendNameLengthsSignal = []
  if signals: legendNameLengthsSignal = [len(x['niceName']) for x in signals]
  legendNameLengths = legendNameLengthsSamples + legendNameLengthsSignal
  legendWidth = 0.015*max(legendNameLengths)+0.03
  if legend:
    height = 0.04*len(h)
    if data: height+=0.04
    if signals: height += 0.04*len(signals)
    if data: height += 0.04
    leg = ROOT.TLegend(0.98-legendWidth,0.95-height,0.98,0.95)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetShadowColor(ROOT.kWhite)
    leg.SetBorderSize(1)
    leg.SetTextSize(0.035)
    for item in reversed(h):
      leg.AddEntry(item['hist'],'','f')
  if setLogY: pad1.SetLogy()
  if setLogX: pad1.SetLogx()
  if stacking:
    h_Stack = ROOT.THStack('h_Stack','Stack')
    for item in h:
      h_Stack.Add(item['hist'])
    if minimum: h_Stack.SetMinimum(minimum)
    if maximum: h_Stack.SetMaximum(maximum)
    h_Stack.Draw('hist')
    h_Stack.GetXaxis().SetTitle(variable['titleX'])
    h_Stack.GetXaxis().SetNdivisions(508)
    h_Stack.GetYaxis().SetTitle(variable['titleY'])
    h_Stack.GetYaxis().SetTitleOffset(0.9)
  else:
    first = True
    for item in reversed(h):
      if first:
        if drawError:
          item['hist'].Draw('e hist')
        else:
          item['hist'].Draw('hist')
        first = False
      else:
        if drawError:
          item['hist'].Draw('e hist same')
        else:
          item['hist'].Draw('hist same')
  s = []
  if signals:
    for isignal,signal in enumerate(signals):
      if binningIsExplicit: s.append({'hist':ROOT.TH1F('s'+str(isignal), signal['niceName'], len(variable['binning'])-1, array('d', variable['binning'])),'yield':0., 'legendName':signal['niceName']})
      else: s.append({'hist':ROOT.TH1F('s'+str(isignal), signal['niceName'], *variable['binning']),'yield':0., 'legendName':signal['niceName']})
      #if signal['weight']=='weight':weight='weight*(3./4.)'
      #else: weight=str(signal['weight'])
      signal['chain'].Draw(variable['name']+'>>s'+str(isignal),weight+'*('+cut['string']+')','goff')
      s[isignal]['hist'].SetLineColor(signal['color'])
      s[isignal]['hist'].SetLineWidth(3)
      s[isignal]['hist'].SetMarkerSize(0)
      if legend: leg.AddEntry(s[isignal]['hist'])
      if drawError: s[isignal]['hist'].Draw('e same hist')
      else: s[isignal]['hist'].Draw('same hist')
  if data:
    if binningIsExplicit: h.append({'hist':ROOT.TH1F('data','Data',len(variable['binning'])-1, array('d', variable['binning'])),'yield':dataYield, 'legendName':'data'})
    else: h.append({'hist':ROOT.TH1F('data','Data',*variable['binning']),'yield':dataYield, 'legendName':'data'})
    #if data['cut']: cutstring = data['cut']
    #else: cutstring = cut['string']
    #if data['var']: variable = data['var']
    normCut, normWeight = getBTagCutAndWeight(data['chain'], btagcut, btagweight, cut['string'], (1))
    data['chain'].Draw(variable['name']+'>>data',normCut,'goff')
    #h_Stack.Draw('hist')
    h[-1]['hist'].Draw('same e1p')
    if legend: leg.AddEntry(h[-1]['hist'])
    if binningIsExplicit: dataMCH = ROOT.TH1F('dataMC','DataMC',len(variable['binning'])-1, array('d', variable['binning']))
    else: dataMCH = ROOT.TH1F('dataMC','DataMC',*variable['binning'])
    dataMCH.Sumw2()
    dataMCH = h[-1]['hist'].Clone()
    dataMCH.Divide(totalH)
    can.cd()
    pad2=ROOT.TPad("pad2","datavsMC",0.,0.,1.,.3)
    pad2.SetLeftMargin(0.11)
    pad2.SetBottomMargin(0.3)
    pad2.SetTopMargin(0.)
    pad2.SetGrid()
    pad2.Draw()
    pad2.cd()
    dataMCH.GetXaxis().SetTitle(variable['titleX'])
    dataMCH.GetXaxis().SetTitleSize(0.13)
    dataMCH.GetXaxis().SetLabelSize(0.13)
    dataMCH.GetXaxis().SetNdivisions(508)
    dataMCH.GetYaxis().SetTitle('data/MC')
    dataMCH.GetYaxis().SetTitleSize(0.13)
    dataMCH.GetYaxis().SetLabelSize(0.13)
    dataMCH.GetYaxis().SetTitleOffset(0.4)
    dataMCH.GetYaxis().SetNdivisions(508)
    dataMCH.SetMinimum(0.1)
    dataMCH.SetMaximum(2.2)
    h.append({'hist':dataMCH, 'yield':0., 'legendName':'notInLegend'})
    dataMCH.Draw('same e1p')
    pad2.RedrawAxis()
    can.cd()
    pad1.cd()
  if titleText or lumi:
    latex1 = ROOT.TLatex()
    latex1.SetNDC()
    latex1.SetTextSize(0.04)
    latex1.SetTextAlign(11) # align right
  if titleText: latex1.DrawLatex(0.11,0.96,'CMS #bf{#it{'+titleText+'}}')
  if MCscale and (MCscale>1.001 or MCscale<0.99) :
    latex1.DrawLatex(0.82, 0.95-height-0.04,'#bf{MC scale:}')
    latex1.DrawLatex(0.82, 0.95-height-0.04*2, str(round(MCscale,2))+'\pm'+str(round(MCscaleError,2)))
  if lumi: latex1.DrawLatex(0.77,0.96,"L="+str(lumi)+"fb^{-1} (13TeV)")
  if legend: leg.Draw()
  can.Update()
  if stacking: return {'hist':h, 'canvas':can, 'legend':leg, 'stack':h_Stack, 'signals':s}
  else: return {'hist':h, 'canvas':can, 'legend':leg, 'signals':s}

def plotInSignalRegions(samples, presel, data=False, fixedNJet=None, btb=None, signalRegions=signalRegion3fb, legend=True, stacking=True, fractions=True, minimum=0, maximum=0, MClumiScale=2.2/3., MCscale=1, titleText='preliminary', lumi=2.2, btagcut='nBJetMediumCSV30==0', btagweight='weightBTag0_SF'):
  can = ROOT.TCanvas('c','c',700,700)
  totalChain = ROOT.TChain('tree')
  for s in samples:
    totalChain.Add(s['chain'])
  bottomMargin = 0.13
  if data:
    marginForPad2 = 0.3
    bottomMargin = 0.
  else:
    marginForPad2 = 0.
    bottomMargin = 0.13
  pad1=ROOT.TPad("pad1","MyTitle",0.,marginForPad2,1.,1.)
  pad1.SetLeftMargin(0.11)
  pad1.SetBottomMargin(bottomMargin)
  pad1.Draw()
  pad1.cd()
  pad1.SetLogy()
  if data:
    dataYield, dataYieldError = getYieldFromChain(data['chain'],cutString=preselMultiLep,weight='(1)', returnError=True)
  if data and MCscale==1:
    MCYield, MCYieldError = getYieldFromChain(totalChain,cutString=preselMultiLep,weight=str(MClumiScale)+'*'+totalWeight, returnError=True)
    print 'Yield Data:\t', dataYield
    print 'Yield MC:\t', round(MCYield,1)
    MCscale = dataYield/MCYield
    MCscaleError = dataYield/MCYield*sqrt(MCYieldError**2/dataYield**2+dataYieldError**2/MCYield**2)
  else:
    MCscale = MCscale
    MCscaleError = 0
  print 'Will scale MC with factor:',getValErrString(MCscale,MCscaleError)
  h = []
  bins = 0
  for srNJet in sorted(signalRegions):
    rows = 0
    for stb in sorted(signalRegions[srNJet]):
      rows += len(signalRegions[srNJet][stb])
    bins += rows
  #print bins

  for isample, sample in enumerate(samples):
    legendName = sample['niceName']
    h.append({'hist':ROOT.TH1F('h'+str(isample), legendName, bins, 0, bins),'yield':0., 'legendName':legendName})
    h[-1]['hist'].SetFillColor(sample['color'])
  if data:
    dataD ={'hist':ROOT.TH1F('data','Data',bins, 0, bins),'yield':dataYield, 'legendName':'data'}
  totalH = ROOT.TH1F('totalH', 'totalH', bins, 0, bins)
  dataMCH = ROOT.TH1F('dataMC','DataMC', bins, 0, bins)
  i = 1
  for i_njb, njb in enumerate(sorted(signalRegions)):
    for stb in sorted(signalRegions[njb]):
      for htb in sorted(signalRegions[njb][stb]):
        if fixedNJet is not None: njets=fixedNJet
        else: njets=njb
        #print njets
        name, cut = nameAndCut(stb,htb,njets,btb=btb,presel=presel['string'])
        print 'Processing cut:', name
        totalY = [0,0]
        for isample, sample in enumerate(samples):
          print 'Sample', sample['name']
          normCut, normWeight = getBTagCutAndWeight(sample['chain'], btagcut, btagweight, cut, sample['weight']+'*'+str(MClumiScale*MCscale))
          #weight = sample['weight']+'*'+str(MCscale*MClumiScale)
          ##print weight
          ##print weight
          #if sample['cut']:
          #  totalCut = cut + '&&' + sample['cut']
          #  #print sample['cut']
          #else: totalCut = cut
          ##print totalCut
          y = getYieldFromChain(sample['chain'], normCut, normWeight, returnError=True)
          ySemi = getYieldFromChain(sample['chain'], normCut+'&&(ngenLep+ngenTau)==1', normWeight, returnError=True)
          yDi = getYieldFromChain(sample['chain'], normCut+'&&(ngenLep+ngenTau)==2', normWeight, returnError=True)
          if ySemi[0]>0:
            fracSemi = getPropagatedError(ySemi[0],ySemi[1],y[0],y[1], returnCalcResult=True)
          else: fracSemi = (0,0)
          print 'Fraction Semileptonic', fracSemi
          if yDi[0]>0:
            fracDi = getPropagatedError(yDi[0],yDi[1],y[0],y[1], returnCalcResult=True)
          else: fracDi = (0,0)
          print 'Fraction Dileptonic', fracDi
          h[isample]['hist'].SetBinContent(i, y[0])
          h[isample]['hist'].SetBinError(i, y[1])
          h[isample]['yield'] += y[0]
          #print y[0]
          totalY[0] += y[0]
          totalY[1] += y[1]
        totalH.SetBinContent(i,totalY[0])
        totalH.SetBinError(i,totalY[1])
        if data:
          #if data['cut']:
          #  totalCut = cut + '&&' + data['cut']
          #  #print data['cut']
          #else: totalCut = cut
          normCut, normWeight = getBTagCutAndWeight(data['chain'], btagcut, btagweight, cut, '(1)')
          y = getYieldFromChain(data['chain'], normCut, weight='(1)', returnError=True)
          print 'Data yield:', y
          if y[0]>0:
            ratio = getPropagatedError(y[0],y[1],totalH.GetBinContent(i),totalH.GetBinError(i), returnCalcResult=True)
          else:
            ratio = (0,totalH.GetBinError(i)/totalH.GetBinContent(i))
          print 'Data/MC:', getValErrString(ratio[0],ratio[1])
          dataD['hist'].SetBinContent(i, y[0]) 
          dataD['hist'].SetBinError(i, y[1]) 
          dataD['yield'] += y[0]
          dataMCH.SetBinContent(i, ratio[0])
          dataMCH.SetBinError(i, ratio[1])
        i+=1
  
  legendNameLengthsSamples = [len(x['legendName']) for x in h]
  legendNameLengths = legendNameLengthsSamples
  legendWidth = 0.015*max(legendNameLengths)+0.03
  if legend:
    height = 0.04*len(h)
    if data: height+=0.08
    leg = ROOT.TLegend(0.98-legendWidth,0.95-height,0.98,0.95)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetShadowColor(ROOT.kWhite)
    leg.SetBorderSize(1)
    leg.SetTextSize(0.035)
    for item in reversed(h):
      leg.AddEntry(item['hist'],'','f')
  
  h.sort(key=operator.itemgetter('yield'))
  frac = []
  if stacking:
    h_Stack = ROOT.THStack('h_Stack','Stack')
    for item in h:
      h_Stack.Add(item['hist'])
      frac.append(item['hist'].Clone())
      frac[-1].Divide(totalH)
    if minimum: h_Stack.SetMinimum(minimum)
    if maximum: h_Stack.SetMaximum(maximum)
    h_Stack.Draw('hist')
    h_Stack.GetYaxis().SetTitle('Events')
    h_Stack.GetYaxis().SetTitleOffset(0.9)
  
  if fractions and data:
    h_Stack_frac = ROOT.THStack('h_Stack_frac','Stack')
    for f in reversed(frac):
      f.SetFillStyle(3001)
      h_Stack_frac.Add(f)
      #f.Draw('hist same')

  if data:
    dataD['hist'].Draw('same e1p')
    if legend: leg.AddEntry(dataD['hist'], '', 'e1p')
    can.cd()
    pad2=ROOT.TPad("pad2","datavsMC",0.,0.,1.,.3)
    pad2.SetLeftMargin(0.11)
    pad2.SetBottomMargin(0.3)
    pad2.SetTopMargin(0.)
    pad2.SetGrid()
    pad2.Draw()
    pad2.cd()
    setNiceBinLabel(dataMCH)
    dataMCH.GetXaxis().SetTitleSize(0.13)
    dataMCH.GetXaxis().SetLabelSize(0.13)
    dataMCH.GetXaxis().SetNdivisions(508)
    dataMCH.GetYaxis().SetTitle('data/MC')
    dataMCH.GetYaxis().SetTitleSize(0.13)
    dataMCH.GetYaxis().SetLabelSize(0.13)
    dataMCH.GetYaxis().SetTitleOffset(0.4)
    dataMCH.GetYaxis().SetNdivisions(508)
    dataMCH.SetMinimum(0.01)
    dataMCH.SetMaximum(2.2)
    #h_Stack_frac.Draw('hist same')
    h.append({'hist':dataMCH, 'yield':0., 'legendName':'notInLegend'})
    h.append(dataD)
    dataMCH.Draw('same e1p')
    h_Stack_frac.Draw('hist same')
    dataMCH.Draw('same e1p')
    pad2.RedrawAxis()
    pad2.SetGrid()
    can.cd()
    pad1.cd()
  
  leg.Draw()

  if titleText or lumi:
    latex1 = ROOT.TLatex()
    latex1.SetNDC()
    latex1.SetTextSize(0.04)
    latex1.SetTextAlign(11) # align right
  if titleText: latex1.DrawLatex(0.11,0.96,'CMS #bf{#it{'+titleText+'}}')
  if MCscale and (MCscale>1.001 or MCscale<0.99) :
    latex1.DrawLatex(0.82, 0.95-height-0.04,'#bf{MC scale:}')
    latex1.DrawLatex(0.82, 0.95-height-0.04*2, str(round(MCscale,2))+'\pm'+str(round(MCscaleError,2)))
  if lumi: latex1.DrawLatex(0.77,0.96,"L="+str(lumi)+"fb^{-1} (13TeV)")

  #if data:
  #  h.append(dataD)
  #  h.append(dataMCH)
  can.Update()
  if stacking: return {'hist':h, 'canvas':can, 'legend':leg, 'stack':h_Stack, 'total':totalH, 'frac_stack':h_Stack_frac, 'fracs':frac}
  else: return {'hist':h, 'canvas':can, 'legend':leg}

def savePlot(plotDict, path, filename, fileType=['pdf','root','png']):
  wwwDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/'
  if not os.path.exists(wwwDir+path):
    os.makedirs(wwwDir+path)
  for t in fileType:
    plotDict['canvas'].Print(wwwDir+path+filename+'.'+t)

def createDefaultDataPlots(dataList):
  for a in dataList:
    t = plot(samples,a,newPreselCut, data=dataDict,filling=True,stacking=True,minimum=0.08, maximum=2000, MClumiScale=204./3000., setLogY=True, lumi=0.204, titleText='preliminary')
    savePlot(t, 'data/25ns/204pbV3/',a['filename'])
#plot(samples,st,cuts)

#vars = [st,ht,njet,deltaPhi,leptonPt,leadingJetPt]
#
#for v in vars:
#  t = plot(samples,v,newPreselCut, signals=signals,filling=True,stacking=True,minimum=0.008, maximum=5000, setLogY=True)
#  t['canvas'].Print('/afs/hephy.at/user/d/dspitzbart/www/Spring15/25ns/'+v['name']+'.png')
#  t['canvas'].Print('/afs/hephy.at/user/d/dspitzbart/www/Spring15/25ns/'+v['name']+'.root')
