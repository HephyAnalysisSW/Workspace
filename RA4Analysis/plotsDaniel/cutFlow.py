import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
import Workspace.HEPHYPythonTools.xsec as xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain

#from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_antiSel_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_Promtv2_antiSel_postprocessed import *


from helpers import *

totalWeight = '(2.571/3.0)*weight'#*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*TopPtWeight*0.94'
#totalWeight = '(2.3/3.0)*weight*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*TopPtWeight*0.94*puReweight_true_max4'



#25ns samples
WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu,histname=''), 'weight':totalWeight, 'niceName':'W+Jets', 'cut':'(1)'}

TTJets = {'name':'TTJets', 'chain':getChain(TTJets_Lep,histname=''), 'weight':totalWeight, 'niceName':'t#bar{t}+Jets', 'cut':'(1)'}
#TTJets_singleLep = {'name':'TTJets 1l', 'chain':TTJets['chain'], 'weight':totalWeight, 'niceName':'t#bar{t}+Jets 1l', 'cut':'(ngenLep+ngenTau)==1'}
#TTJets_diLep =     {'name':'TTJets 2l', 'chain':TTJets['chain'], 'weight':totalWeight, 'niceName':'t#bar{t}+Jets 2l', 'cut':'(ngenLep+ngenTau)==2'}
#TTJets_had =       {'name':'TTJets 0l', 'chain':TTJets['chain'], 'weight':totalWeight, 'niceName':'t#bar{t}+Jets 0l', 'cut':'(ngenLep+ngenTau)==0'}

DY = {'name':'DY', 'chain':getChain(DY_madgraph,histname=''), 'weight':totalWeight, 'niceName':'Drell Yan', 'cut':'(1)'}
singleTop = {'name':'singleTop', 'chain':getChain(singleTop_lep,histname=''), 'weight':totalWeight, 'niceName':'t/#bar{t}', 'cut':'(1)'}
QCD = {'name':'QCD', 'chain':getChain(QCDHT,histname=''), 'weight':totalWeight, 'niceName':'QCD multijet', 'cut':'(1)'}
TTVH = {'name':'TTVH', 'chain':getChain(TTV,histname=''), 'weight':totalWeight, 'niceName':'t#bar{t}W', 'cut':'(1)'}

Data = {'name':'data', 'chain':getChain([single_ele_Run2016B,single_mu_Run2016B],histname=''), 'weight':totalWeight, 'niceName':'t#bar{t}W', 'cut':'(1)'}

#Rest = {'name':'Rest', 'chain':getChain([TTV_25ns,singleTop_25ns,DY_25ns],histname=''), 'weight':totalWeight, 'niceName':'other EWK', 'cut':'(1)'}
#Bkg = {'name':'Bkg', 'chain':getChain([TTJets_combined,WJetsHTToLNu_25ns,QCDHT_25ns,TTV_25ns,singleTop_25ns,DY_25ns],histname=''), 'weight':totalWeight, 'niceName':'total Bkg', 'cut':'(1)'}
#EWK = {'name':'Bkg', 'chain':getChain([TTJets_combined,WJetsHTToLNu_25ns,TTV_25ns,singleTop_25ns,DY_25ns],histname=''), 'weight':totalWeight, 'niceName':'total Bkg', 'cut':'(1)'}

singleLepton = {'cut':'singleLeptonic', 'name': 'one lepton'}
noVetoLepton = {'cut':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0', 'name': 'no veto lepton'}
njet = {'cut':'nJet30>4', 'name':'N_{jets}#geq 5'}
jetpt = {'cut':'Jet_pt[1]>80', 'name':'jet pt'}
HT = {'cut':'htJet30j>500', 'name':'H_{T} > 500'}
LT = {'cut':'st>250', 'name':'L_{T} > 250'}

entryPoint = {'cut':'(1)', 'name': 'entry'}
electronDataSet = {'cut':'((isData&&eleDataSet)||(!isData))','name':'ele data set'}
muonDataSet = {'cut':'((isData&&muonDataSet)||(!isData))','name':'muon data set'}

singleHardLep = {'cut':'nLep==1&&nVeto==0&&leptonPt>25', 'name':'1 hard l'}
singleHardEle = {'cut':'nLep==1&&nVeto==0&&leptonPt>25&&nEl==1', 'name':'1 hard e'}
singleHardMu = {'cut':'nLep==1&&nVeto==0&&leptonPt>25&&nMu==1', 'name':'1 hard mu'}

selected = {'cut':'Selected==1','name':'selected'}
antiselected = {'cut':'Selected==-1','name':'anti-selected'}
trigger = {'cut':'((isData&&(HLT_EleHT350||HLT_MuHT350))||!isData)', 'name':'trigger'}
XOR = {'cut':'((!isData&&nLep==1)||(isData&&((muonDataSet&&nMu==1)||(eleDataSet&&nEl==1))))', 'name':'XOR'}
singleEle = {'cut':'nEl==1','name':'single ele'}
filters = {'cut':'(isData&&(Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter &&Flag_CSCTightHaloFilter)||!isData)', 'name':'filters'}
njet = {'cut':'nJet30clean>=5','name':'>= 5 jets'}
ht = {'cut':'htJet30clean>=500','name':'HT>500'}
lt = {'cut':'Lt>=250','name':'LT>250'}
nbjet = {'cut':'nBJetMediumCSV30>=1','name':'multi b'}
jetpt2 = {'cut':'Jet2_pt>80', 'name':'2nd jet>80'}



cuts = [entryPoint,electronDataSet,singleHardEle,antiselected,trigger,XOR,filters,njet,jetpt2,ht,lt,nbjet]
#cuts = [entryPoint,electronDataSet,singleHardEle,selected,trigger,XOR,filters,njet,jetpt2,ht,lt,nbjet]
#cuts = [entryPoint,muonDataSet,singleHardMu,selected,trigger,XOR,filters,njet,jetpt2,ht,lt,nbjet]
#cuts = [singleLepton, noVetoLepton, njet, jetpt, HT, LT]

print 'anti Selected electrons'

flow = '(1)'
#samples = [TTJets_diLep, TTJets_singleLep, WJETS, QCD, singleTop, DY, TTVH, Bkg]
samples = [QCD, TTJets, WJETS, singleTop, DY, Data]


fmt = '{0:20}'
title = 'print fmt.format(\'cut\''
for i_s, s in enumerate(samples):
  fmt += ' {'+str(i_s+1)+':10}'
  title += ', \'' + samples[i_s]['name'] + '\''

title += ')'
print
print
exec(title)
#print fmt.format('', samples[0]['name'], samples[1]['name'], samples[2]['name'], samples[3]['name'], samples[4]['name'], samples[5]['name'], samples[6]['name'], samples[7]['name'])

for cut in cuts:
  flow += '&&' + cut['cut']
  #print cut['name']
  line = 'print fmt.format(\''+cut['name']+ '\''
  for sample in samples:
    if sample['name'].lower() == 'data':
      y = getYieldFromChain(sample['chain'], flow+'&&'+sample['cut'], weight='(1)')
    else:
      y = getYieldFromChain(sample['chain'], flow+'&&'+sample['cut'], totalWeight)
    line += ', \'' + str(round(y,1)) + '\''
  line += ')'
  exec(line)
    #print round(y,0)
