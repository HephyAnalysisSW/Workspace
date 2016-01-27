import ROOT
import pickle
from array import array
import operator
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.signalRegions import *
from Workspace.HEPHYPythonTools.user import username
from cutFlow_helper import *

ROOT.TH1F().SetDefaultSumw2()

weight_str = "((weight*2.25)/3)"

def getNumString(n,ne, acc=2, systematic=False):    ##For printing table 
  if type(n) is float and type(ne) is float:
    if systematic:
      return str(round(n,acc))+'&$\pm$&'+str(round(ne,acc))+'&$\pm$&'+str(round(0.2*n,acc))
    else:
      return str(round(n,acc))+'&$\pm$&'+str(round(ne,acc))
  #if type(n) is str and type(ne) is str: 
  else:
    return n +'&$\pm$&'+ ne

btagString = "nBJetMediumCSV30"
maxN = -1
input_pickle_dir = '/data/dspitzbart/Results2016/Prediction_SFtemplates_validation_lep_MC_SF_2p3/singleLeptonic_Spring15__estimationResults_pkl_kappa_corrected'
res = pickle.load(file(input_pickle_dir))
DL = pickle.load(file('/data/easilar/Spring15/25ns/DL_syst_pkl'))
lepSels = [
{'cut':'((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 #'chain': getChain([single_ele_Run2015D,single_mu_Run2015D],maxN=maxN,histname="",treeName="Events") ,\
 'trigWeight': "0.94" ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
]

lepSel = lepSels[0]
signalRegions = signalRegion3fb

rowsNJet = {}
rowsSt = {}
for srNJet in sorted(signalRegions):
  rowsNJet[srNJet] = {}
  rowsSt[srNJet] = {}
  rows = 0
  for stb in sorted(signalRegions[srNJet]):
    rows += len(signalRegions[srNJet][stb])
    rowsSt[srNJet][stb] = {'n':len(signalRegions[srNJet][stb])}
  rowsNJet[srNJet] = {'nST':len(signalRegions[srNJet]), 'n':rows}

presel = presel = "&&".join([lepSel['cut'],lepSel['veto'],filters])
c_tt = {"sample":"ttJets", "chain":getChain(TTJets_combined, maxN=maxN,histname="",treeName="Events"),  "weight":"weightBTag0_SF" ,"cut":(0,-1) , "name":TTJets_combined, "tex":"ttbar + jets",'color':ROOT.kBlue-4}
c_DY = {"sample":"DY", "chain":getChain(DY_25ns, maxN=maxN,histname="",treeName="Events"),  "weight":"(1)" ,"cut":(0,0) , "name":DY_25ns, "tex":"DY",'color':ROOT.kRed-6}
cRest = getChain([singleTop_25ns,TTV_25ns],histname='') #no QCD
cW = getChain([WJetsHTToLNu_25ns],histname='')
weight_str_tt =  lepSel['trigWeight']+"*"+c_tt['weight']+"*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*puReweight_true_max4*TopPtWeight*weight*2.3/3"
weight_str_DY =  lepSel['trigWeight']+"*"+c_DY['weight']+"*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*puReweight_true_max4*TopPtWeight*weight*2.3/3"
#weight_str_tt =  c_tt['weight']+"*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*weight*2.3/3"
#weight_str_DY =  c_DY['weight']+"*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*weight*2.3/3"

for srNJet in sorted(signalRegions):
  for stb in sorted(signalRegions[srNJet]):
    for htb in sorted(signalRegions[srNJet][stb]):
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      name_bla, cut_tt =  nameAndCut(stb, htb, srNJet, btb=c_tt["cut"], presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      name, cut_DY =  nameAndCut(stb, htb, srNJet, btb=c_DY["cut"], presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      c_tt['yield_diLep'] = getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+cut_tt, weight = weight_str_tt)
      c_tt['yield_diLep_constant_Up'] = getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+cut_tt, weight = weight_str_tt+"*(1+"+str(DL[srNJet][stb][htb]["constant"])+")")
      c_tt['yield_diLep_constant_Down'] = getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+cut_tt, weight = weight_str_tt+"*(1-"+str(DL[srNJet][stb][htb]["constant"])+")")
      c_tt['yield_diLep_slope_Up'] = getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+cut_tt, weight = weight_str_tt+"*(1+(nJet30-"+str(DL[srNJet][stb][htb]["nJetMean"])+")*"+str(DL[srNJet][stb][htb]["slope"])+")")
      c_tt['yield_diLep_slope_Down'] = getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+cut_tt, weight = weight_str_tt+"*(1-(nJet30-"+str(DL[srNJet][stb][htb]["nJetMean"])+")*"+str(DL[srNJet][stb][htb]["slope"])+")")
      c_tt['yield_rest'] = getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)!=2&&"+cut_tt, weight = weight_str_tt)
      print "tt yield:" , c_tt['yield_diLep']+c_tt['yield_rest']
      c_DY['yield'] = getYieldFromChain(c_DY['chain'], cut_DY , weight = weight_str_DY)
      print "DY yield:" , c_DY['yield'] 
      c_DY['yield_constant_Up'] = getYieldFromChain(c_DY['chain'], cut_DY , weight = weight_str_DY+"*(1+"+str(DL[srNJet][stb][htb]["constant"])+")")
      c_DY['yield_constant_Down'] = getYieldFromChain(c_DY['chain'], cut_DY , weight = weight_str_DY+"*(1-"+str(DL[srNJet][stb][htb]["constant"])+")")
      c_DY['yield_slope_Up'] = getYieldFromChain(c_DY['chain'], cut_DY , weight = weight_str_DY+"*(1+(nJet30-"+str(DL[srNJet][stb][htb]["nJetMean"])+")*"+str(DL[srNJet][stb][htb]["slope"])+")")
      c_DY['yield_slope_Down'] = getYieldFromChain(c_DY['chain'], cut_DY , weight = weight_str_DY+"*(1-(nJet30-"+str(DL[srNJet][stb][htb]["nJetMean"])+")*"+str(DL[srNJet][stb][htb]["slope"])+")")
      rest_yield = getYieldFromChain(cRest, cut_DY , weight = weight_str_DY)
      print "rest yield:" , rest_yield
      w_yield = getYieldFromChain(cW, cut_tt , weight = weight_str_tt)
      print "w yield:" , w_yield
      res[srNJet][stb][htb]['tot_original'] = c_tt['yield_diLep'] + c_tt['yield_rest'] + c_DY['yield'] + rest_yield + w_yield
      res[srNJet][stb][htb]['tot_constant_Up'] =   c_tt['yield_diLep_constant_Up'] +   c_tt['yield_rest'] + c_DY['yield_constant_Up'] + rest_yield + w_yield
      res[srNJet][stb][htb]['tot_constant_Down'] = c_tt['yield_diLep_constant_Down'] + c_tt['yield_rest'] + c_DY['yield_constant_Down'] + rest_yield + w_yield
      res[srNJet][stb][htb]['tot_slope_Up'] =   c_tt['yield_diLep_slope_Up']   + c_tt['yield_rest'] + c_DY['yield_slope_Up'] + rest_yield + w_yield
      res[srNJet][stb][htb]['tot_slope_Down'] = c_tt['yield_diLep_slope_Down'] + c_tt['yield_rest'] + c_DY['yield_slope_Down'] + rest_yield + w_yield
      res[srNJet][stb][htb]['kappa_original'] = res[srNJet][stb][htb]['tot_original']/res[srNJet][stb][htb]['tot_pred']
      res[srNJet][stb][htb]['kappa_constant_Up'] = res[srNJet][stb][htb]['tot_constant_Up']/res[srNJet][stb][htb]['tot_pred']
      res[srNJet][stb][htb]['kappa_constant_Down'] = res[srNJet][stb][htb]['tot_constant_Down']/res[srNJet][stb][htb]['tot_pred']
      res[srNJet][stb][htb]['kappa_slope_Up'] = res[srNJet][stb][htb]['tot_slope_Up']/res[srNJet][stb][htb]['tot_pred']
      res[srNJet][stb][htb]['kappa_slope_Down'] = res[srNJet][stb][htb]['tot_slope_Down']/res[srNJet][stb][htb]['tot_pred']
      print res[srNJet][stb][htb]['tot_original'] , res[srNJet][stb][htb]['tot_pred'] , res[srNJet][stb][htb]['kappa_original']
      res[srNJet][stb][htb]['delta_constant_Up'] = ((res[srNJet][stb][htb]['kappa_constant_Up']/res[srNJet][stb][htb]['kappa_original'])-1)
      res[srNJet][stb][htb]['delta_constant_Down'] = ((res[srNJet][stb][htb]['kappa_constant_Down']/res[srNJet][stb][htb]['kappa_original'])-1)
      res[srNJet][stb][htb]['delta_slope_Up'] = ((res[srNJet][stb][htb]['kappa_slope_Up']/res[srNJet][stb][htb]['kappa_original'])-1)
      res[srNJet][stb][htb]['delta_slope_Down'] = ((res[srNJet][stb][htb]['kappa_slope_Down']/res[srNJet][stb][htb]['kappa_original'])-1)
      print "constant Up" , res[srNJet][stb][htb]['delta_constant_Up'] , "down:" , res[srNJet][stb][htb]['delta_constant_Down']
      print "slope Up" , res[srNJet][stb][htb]['delta_slope_Up'] , "down:" , res[srNJet][stb][htb]['delta_slope_Down']

pickle.dump(res,file('/data/easilar/Spring15/25ns/extended_with_truth_counts_pkl','w'))



