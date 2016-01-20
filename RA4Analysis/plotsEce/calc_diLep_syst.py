import ROOT
import pickle
from array import array
import operator
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.signalRegions import *
from Workspace.RA4Analysis.rCShelpers import *
from Workspace.HEPHYPythonTools.user import username
from cutFlow_helper import *

ROOT.TH1F().SetDefaultSumw2()

weight_str = "((weight*2.3)/3)"


btagString = "nBJetMediumCSV30"
maxN = -1
input_pickle_dir = '/data/dspitzbart/Results2016/Prediction_SFtemplates_validation_lep_MC_SF_2p3/singleLeptonic_Spring15__estimationResults_pkl'
res = pickle.load(file(input_pickle_dir))
DL = pickle.load(file('/data/easilar/Spring15/25ns/DL_syst_pkl'))
lepSels = [
{'cut':'((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 #'chain': getChain([single_ele_Run2015D,single_mu_Run2015D],maxN=maxN,histname="",treeName="Events") ,\
 'trigWeight': "0.94" ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
]

lepSel = lepSels[0]
#signalRegion3fb = {(8, -1):  {(250, 350): {(500, 750):  {'deltaPhi': 1.0}}}}
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
c_tt = {"sample":"ttJets", "chain":getChain(TTJets_combined, maxN=maxN,histname="",treeName="Events"), "weight1b":"weightBTag1_SF" , "weight0b":"weightBTag0_SF" ,"cut":(0,-1) , "name":TTJets_combined, "tex":"ttbar + jets",'color':ROOT.kBlue-4}
c_DY = {"sample":"DY", "chain":getChain(DY_25ns, maxN=maxN,histname="",treeName="Events"),  "weight":"(1)" ,"cut":(0,0) , "name":DY_25ns, "tex":"DY",'color':ROOT.kRed-6}
cRest = getChain([singleTop_25ns,TTV_25ns],histname='') #no QCD
cW = getChain([WJetsHTToLNu_25ns],histname='')
common_weight = lepSel['trigWeight']+"*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*puReweight_true_max4*TopPtWeight*weight*2.3/3"

for srNJet in sorted(signalRegions):
#for srNJet in [(6,7)]:
  for stb in sorted(signalRegions[srNJet]):
  #for stb in [(350,450)]:
    for htb in sorted(signalRegions[srNJet][stb]):
      print srNJet, stb , htb
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      name_bla, cut_tt =  nameAndCut(stb, htb, srNJet, btb=c_tt["cut"], presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      name_bla, cut_tt_CR =  nameAndCut(stb, htb, srNJet, btb=c_tt["cut"], presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      name,     cut_DY =  nameAndCut(stb, htb, srNJet, btb=c_DY["cut"], presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      name_bla, DY_SB_cut =  nameAndCut(stb, htb, (3,4), btb=c_DY["cut"], presel=presel, btagVar = btagString)
      name_bla, DY_SB_cut_CR =  nameAndCut(stb, htb, (3,4), btb=c_DY["cut"], presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      name_bla, DY_MB_cut =  nameAndCut(stb, htb, srNJet, btb=c_DY["cut"], presel=presel, btagVar = btagString)
      name_bla, DY_MB_cut_CR =  nameAndCut(stb, htb, srNJet, btb=c_DY["cut"], presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      name_bla, tt_SB_cut = nameAndCut(stb, htb, (3,4), btb=c_tt["cut"], presel=presel, btagVar = btagString)
      name_bla, tt_SB_cut_CR = nameAndCut(stb, htb, (3,4), btb=c_tt["cut"], presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      name_bla, tt_MB_cut = nameAndCut(stb, htb, srNJet, btb=c_tt["cut"], presel=presel, btagVar = btagString)
      ## WJets KAPPPPAAAAA#

      rCS_DY_MB_diLep = max(0,getRCS(c_DY['chain'],"(ngenLep+ngenTau)==2&&"+DY_MB_cut ,  deltaPhiCut,weight = common_weight)['rCS'])
      rCS_DY_MB_rest  = max(0,getRCS(c_DY['chain'],"(ngenLep+ngenTau)!=2&&"+DY_MB_cut ,  deltaPhiCut,weight = common_weight)['rCS'])
      rCS_W_MB  = max(0,getRCS(cW,tt_MB_cut ,  deltaPhiCut,weight = common_weight+"*"+c_tt["weight0b"])['rCS'])
      rCS_Rest_MB  = max(0,getRCS(cRest,DY_MB_cut ,  deltaPhiCut,weight = common_weight)['rCS'])

      rCS_DY_SB_diLep = max(0,getRCS(c_DY['chain'],"(ngenLep+ngenTau)==2&&"+DY_SB_cut ,  deltaPhiCut,weight = common_weight)['rCS'])
      rCS_DY_SB_rest  = max(0,getRCS(c_DY['chain'],"(ngenLep+ngenTau)!=2&&"+DY_SB_cut ,  deltaPhiCut,weight = common_weight)['rCS'])
      rCS_W_SB  = max(0,getRCS(cW,tt_SB_cut ,  deltaPhiCut,weight = common_weight+"*"+c_tt["weight0b"])['rCS'])
      rCS_Rest_SB  = max(0,getRCS(cRest,DY_SB_cut ,  deltaPhiCut,weight = common_weight)['rCS'])

      ###to calculate MB###
      yield_diLep_DY_MB_in_CR = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_MB_cut_CR, weight = common_weight) 
      yield_diLep_DY_MB_in_CR_constant_Up       = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_MB_cut_CR, weight = common_weight+"*(1+0.31)") 
      yield_diLep_DY_MB_in_CR_constant_Down     = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_MB_cut_CR, weight = common_weight+"*(1-0.31)") 
      yield_diLep_DY_MB_in_CR_slope_Up          = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_MB_cut_CR, weight = common_weight+"*(1+((nJet30-5.2)*0.14))") 
      yield_diLep_DY_MB_in_CR_slope_down        = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_MB_cut_CR, weight = common_weight+"*(1-((nJet30-5.2)*0.14))") 
      yield_rest_DY_MB_in_CR  = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)!=2&&"+DY_MB_cut_CR, weight = common_weight) 
      yield_rest_EWK_MB_in_CR = getYieldFromChain(cRest, DY_MB_cut_CR, weight = common_weight) 
      yield_rest_W_MB_in_CR   = getYieldFromChain(cW   , cut_tt_CR, weight = common_weight+"*"+c_tt["weight0b"]) 
      frac_diLep_DY_MB_in_CR               = yield_diLep_DY_MB_in_CR               /(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR              )
      frac_diLep_DY_MB_in_CR_constant_Up   = yield_diLep_DY_MB_in_CR_constant_Up   /(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_constant_Up  )
      frac_diLep_DY_MB_in_CR_constant_Down = yield_diLep_DY_MB_in_CR_constant_Down /(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_constant_Down)
      frac_diLep_DY_MB_in_CR_slope_Up      = yield_diLep_DY_MB_in_CR_slope_Up      /(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_slope_Up     )
      frac_diLep_DY_MB_in_CR_slope_down    = yield_diLep_DY_MB_in_CR_slope_down    /(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_slope_down   )
      frac_rest_DY_MB_in_CR = 1 - frac_diLep_DY_MB_in_CR 
      frac_rest_DY_MB_in_CR_constant_Up   = 1 - frac_diLep_DY_MB_in_CR_constant_Up   
      frac_rest_DY_MB_in_CR_constant_Down = 1 - frac_diLep_DY_MB_in_CR_constant_Down 
      frac_rest_DY_MB_in_CR_slope_Up      = 1 - frac_diLep_DY_MB_in_CR_slope_Up      
      frac_rest_DY_MB_in_CR_slope_down    = 1 - frac_diLep_DY_MB_in_CR_slope_down    
      frac_DY_MB_in_CR               = (yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR              )/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR              + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_DY_MB_in_CR_constant_Up   = (yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_constant_Up  )/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_constant_Up  + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_DY_MB_in_CR_constant_Down = (yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_constant_Down)/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_constant_Down+ yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_DY_MB_in_CR_slope_Up      = (yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_slope_Up     )/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_slope_Up     + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_DY_MB_in_CR_slope_down    = (yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_slope_down   )/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_slope_down   + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_W_MB_in_CR               = (yield_rest_W_MB_in_CR)/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR              + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_W_MB_in_CR_constant_Up   = (yield_rest_W_MB_in_CR)/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_constant_Up  + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_W_MB_in_CR_constant_Down = (yield_rest_W_MB_in_CR)/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_constant_Down+ yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_W_MB_in_CR_slope_Up      = (yield_rest_W_MB_in_CR)/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_slope_Up     + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_W_MB_in_CR_slope_down    = (yield_rest_W_MB_in_CR)/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_slope_down   + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_Rest_MB_in_CR               = (yield_rest_EWK_MB_in_CR)/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR              + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_Rest_MB_in_CR_constant_Up   = (yield_rest_EWK_MB_in_CR)/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_constant_Up  + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_Rest_MB_in_CR_constant_Down = (yield_rest_EWK_MB_in_CR)/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_constant_Down+ yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_Rest_MB_in_CR_slope_Up      = (yield_rest_EWK_MB_in_CR)/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_slope_Up     + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      frac_Rest_MB_in_CR_slope_down    = (yield_rest_EWK_MB_in_CR)/(yield_rest_DY_MB_in_CR + yield_diLep_DY_MB_in_CR_slope_down   + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR )
      print "fractions DY  MB original diLep:" , frac_diLep_DY_MB_in_CR 
      print "fractions DY  MB up costant up  diLep:" , frac_diLep_DY_MB_in_CR_constant_Up , "slope Up :" , frac_diLep_DY_MB_in_CR_slope_Up 
      print "fractions DY  MB up costant down diLep:" , frac_diLep_DY_MB_in_CR_constant_Down , "slope Down :" , frac_diLep_DY_MB_in_CR_slope_down 
      rCS_DY_MB_full = frac_diLep_DY_MB_in_CR*rCS_DY_MB_diLep + frac_rest_DY_MB_in_CR*rCS_DY_MB_rest
      rCS_DY_MB_full_constant_Up   = frac_diLep_DY_MB_in_CR_constant_Up  *rCS_DY_MB_diLep + frac_rest_DY_MB_in_CR_constant_Up  *rCS_DY_MB_rest
      rCS_DY_MB_full_constant_Down = frac_diLep_DY_MB_in_CR_constant_Down*rCS_DY_MB_diLep + frac_rest_DY_MB_in_CR_constant_Down*rCS_DY_MB_rest
      rCS_DY_MB_full_slope_Up      = frac_diLep_DY_MB_in_CR_slope_Up     *rCS_DY_MB_diLep + frac_rest_DY_MB_in_CR_slope_Up     *rCS_DY_MB_rest
      rCS_DY_MB_full_slope_down    = frac_diLep_DY_MB_in_CR_slope_down   *rCS_DY_MB_diLep + frac_rest_DY_MB_in_CR_slope_down   *rCS_DY_MB_rest
      rCS_EWK_MB_full = frac_DY_MB_in_CR*rCS_DY_MB_full + frac_W_MB_in_CR*rCS_W_MB + frac_Rest_MB_in_CR*rCS_Rest_MB
      rCS_EWK_MB_full_constant_Up   = frac_DY_MB_in_CR_constant_Up  *rCS_DY_MB_full_constant_Up   + frac_W_MB_in_CR_constant_Up  *rCS_W_MB + frac_Rest_MB_in_CR_constant_Up  *rCS_Rest_MB
      rCS_EWK_MB_full_constant_Down = frac_DY_MB_in_CR_constant_Down*rCS_DY_MB_full_constant_Down + frac_W_MB_in_CR_constant_Down*rCS_W_MB + frac_Rest_MB_in_CR_constant_Down*rCS_Rest_MB
      rCS_EWK_MB_full_slope_Up      = frac_DY_MB_in_CR_slope_Up     *rCS_DY_MB_full_slope_Up      + frac_W_MB_in_CR_slope_Up     *rCS_W_MB + frac_Rest_MB_in_CR_slope_Up     *rCS_Rest_MB
      rCS_EWK_MB_full_slope_down    = frac_DY_MB_in_CR_slope_down   *rCS_DY_MB_full_slope_down    + frac_W_MB_in_CR_slope_down   *rCS_W_MB + frac_Rest_MB_in_CR_slope_down   *rCS_Rest_MB
      print "rCS_EWK_MB_full:" , rCS_EWK_MB_full , "rCS_DY_MB_full" , rCS_DY_MB_full , "rCS_W_MB" , rCS_W_MB , "rCS_Rest_MB" , rCS_Rest_MB
      print "rCS_EWK_MB_full_constant_Up" , rCS_EWK_MB_full_constant_Up
      
      ###to calculate SB####
      yield_diLep_DY_SB_in_CR = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_SB_cut_CR, weight = common_weight) 
      yield_diLep_DY_SB_in_CR_constant_Up       = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_SB_cut_CR, weight = common_weight+"*(1+0.31)") 
      yield_diLep_DY_SB_in_CR_constant_Down     = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_SB_cut_CR, weight = common_weight+"*(1-0.31)") 
      yield_diLep_DY_SB_in_CR_slope_Up          = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_SB_cut_CR, weight = common_weight+"*(1+((nJet30-5.2)*0.14))") 
      yield_diLep_DY_SB_in_CR_slope_down        = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_SB_cut_CR, weight = common_weight+"*(1-((nJet30-5.2)*0.14))") 
      yield_rest_DY_SB_in_CR  = getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)!=2&&"+DY_SB_cut_CR, weight = common_weight) 
      yield_rest_EWK_SB_in_CR = getYieldFromChain(cRest, DY_SB_cut_CR, weight = common_weight) 
      yield_rest_W_SB_in_CR   = getYieldFromChain(cW   , cut_tt_CR, weight = common_weight+"*"+c_tt["weight0b"]) 
      frac_diLep_DY_SB_in_CR               = yield_diLep_DY_SB_in_CR               /(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR              )
      frac_diLep_DY_SB_in_CR_constant_Up   = yield_diLep_DY_SB_in_CR_constant_Up   /(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_constant_Up  )
      frac_diLep_DY_SB_in_CR_constant_Down = yield_diLep_DY_SB_in_CR_constant_Down /(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_constant_Down)
      frac_diLep_DY_SB_in_CR_slope_Up      = yield_diLep_DY_SB_in_CR_slope_Up      /(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_slope_Up     )
      frac_diLep_DY_SB_in_CR_slope_down    = yield_diLep_DY_SB_in_CR_slope_down    /(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_slope_down   )
      frac_rest_DY_SB_in_CR = 1 - frac_diLep_DY_SB_in_CR 
      frac_rest_DY_SB_in_CR_constant_Up   = 1 - frac_diLep_DY_SB_in_CR_constant_Up   
      frac_rest_DY_SB_in_CR_constant_Down = 1 - frac_diLep_DY_SB_in_CR_constant_Down 
      frac_rest_DY_SB_in_CR_slope_Up      = 1 - frac_diLep_DY_SB_in_CR_slope_Up      
      frac_rest_DY_SB_in_CR_slope_down    = 1 - frac_diLep_DY_SB_in_CR_slope_down    
      frac_DY_SB_in_CR               = (yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR              )/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR              + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_DY_SB_in_CR_constant_Up   = (yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_constant_Up  )/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_constant_Up  + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_DY_SB_in_CR_constant_Down = (yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_constant_Down)/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_constant_Down+ yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_DY_SB_in_CR_slope_Up      = (yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_slope_Up     )/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_slope_Up     + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_DY_SB_in_CR_slope_down    = (yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_slope_down   )/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_slope_down   + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_W_SB_in_CR               = (yield_rest_W_SB_in_CR)/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR              + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_W_SB_in_CR_constant_Up   = (yield_rest_W_SB_in_CR)/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_constant_Up  + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_W_SB_in_CR_constant_Down = (yield_rest_W_SB_in_CR)/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_constant_Down+ yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_W_SB_in_CR_slope_Up      = (yield_rest_W_SB_in_CR)/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_slope_Up     + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_W_SB_in_CR_slope_down    = (yield_rest_W_SB_in_CR)/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_slope_down   + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_Rest_SB_in_CR               = (yield_rest_EWK_SB_in_CR)/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR              + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_Rest_SB_in_CR_constant_Up   = (yield_rest_EWK_SB_in_CR)/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_constant_Up  + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_Rest_SB_in_CR_constant_Down = (yield_rest_EWK_SB_in_CR)/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_constant_Down+ yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_Rest_SB_in_CR_slope_Up      = (yield_rest_EWK_SB_in_CR)/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_slope_Up     + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      frac_Rest_SB_in_CR_slope_down    = (yield_rest_EWK_SB_in_CR)/(yield_rest_DY_SB_in_CR + yield_diLep_DY_SB_in_CR_slope_down   + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR )
      print "fractions DY  SB original diLep:" , frac_diLep_DY_SB_in_CR 
      print "fractions DY  SB up costant up  diLep:" , frac_diLep_DY_SB_in_CR_constant_Up , "slope Up :" , frac_diLep_DY_SB_in_CR_slope_Up 
      print "fractions DY  SB up costant down diLep:" , frac_diLep_DY_SB_in_CR_constant_Down , "slope Down :" , frac_diLep_DY_SB_in_CR_slope_down 
      rCS_DY_SB_full = frac_diLep_DY_SB_in_CR*rCS_DY_SB_diLep + frac_rest_DY_SB_in_CR*rCS_DY_SB_rest
      rCS_DY_SB_full_constant_Up   = frac_diLep_DY_SB_in_CR_constant_Up  *rCS_DY_SB_diLep + frac_rest_DY_SB_in_CR_constant_Up  *rCS_DY_SB_rest
      rCS_DY_SB_full_constant_Down = frac_diLep_DY_SB_in_CR_constant_Down*rCS_DY_SB_diLep + frac_rest_DY_SB_in_CR_constant_Down*rCS_DY_SB_rest
      rCS_DY_SB_full_slope_Up      = frac_diLep_DY_SB_in_CR_slope_Up     *rCS_DY_SB_diLep + frac_rest_DY_SB_in_CR_slope_Up     *rCS_DY_SB_rest
      rCS_DY_SB_full_slope_down    = frac_diLep_DY_SB_in_CR_slope_down   *rCS_DY_SB_diLep + frac_rest_DY_SB_in_CR_slope_down   *rCS_DY_SB_rest
      rCS_EWK_SB_full = frac_DY_SB_in_CR*rCS_DY_SB_full + frac_W_SB_in_CR*rCS_W_SB + frac_Rest_SB_in_CR*rCS_Rest_SB
      rCS_EWK_SB_full_constant_Up   = frac_DY_SB_in_CR_constant_Up  *rCS_DY_SB_full_constant_Up   + frac_W_SB_in_CR_constant_Up  *rCS_W_SB + frac_Rest_SB_in_CR_constant_Up  *rCS_Rest_SB
      rCS_EWK_SB_full_constant_Down = frac_DY_SB_in_CR_constant_Down*rCS_DY_SB_full_constant_Down + frac_W_SB_in_CR_constant_Down*rCS_W_SB + frac_Rest_SB_in_CR_constant_Down*rCS_Rest_SB
      rCS_EWK_SB_full_slope_Up      = frac_DY_SB_in_CR_slope_Up     *rCS_DY_SB_full_slope_Up      + frac_W_SB_in_CR_slope_Up     *rCS_W_SB + frac_Rest_SB_in_CR_slope_Up     *rCS_Rest_SB
      rCS_EWK_SB_full_slope_down    = frac_DY_SB_in_CR_slope_down   *rCS_DY_SB_full_slope_down    + frac_W_SB_in_CR_slope_down   *rCS_W_SB + frac_Rest_SB_in_CR_slope_down   *rCS_Rest_SB
      print "rCS_DY_SB_full" , rCS_DY_SB_full , "frac_W_SB_in_CR", frac_W_SB_in_CR , "frac_Rest_SB_in_CR" , frac_Rest_SB_in_CR , "rCS_W_SB" , rCS_W_SB , "rCS_Rest_SB" , rCS_Rest_SB
      print "rCS_EWK_SB_full" , rCS_EWK_SB_full
      print "rCS_EWK_SB_full_constant_Up" , rCS_EWK_SB_full_constant_Up




      ################## kappa wJets ### 
      res[srNJet][stb][htb]['kappa_original']        =  rCS_EWK_MB_full               / rCS_EWK_SB_full 
      res[srNJet][stb][htb]['kappa_constant_Up']     =  rCS_EWK_MB_full_constant_Up   / rCS_EWK_SB_full_constant_Up    
      res[srNJet][stb][htb]['kappa_constant_Down']   =  rCS_EWK_MB_full_constant_Down / rCS_EWK_SB_full_constant_Down  
      res[srNJet][stb][htb]['kappa_slope_Up']        =  rCS_EWK_MB_full_slope_Up      / rCS_EWK_SB_full_slope_Up       
      res[srNJet][stb][htb]['kappa_slope_Down']      =  rCS_EWK_MB_full_slope_down    / rCS_EWK_SB_full_slope_down     
      print "kappa:" , res[srNJet][stb][htb]['kappa_original'] , res[srNJet][stb][htb]['kappa_constant_Up'] , res[srNJet][stb][htb]['kappa_constant_Down']
      print "kappa:" , res[srNJet][stb][htb]['kappa_original'] , res[srNJet][stb][htb]['kappa_slope_Up'] , res[srNJet][stb][htb]['kappa_slope_Down']


      res[srNJet][stb][htb]['delta_constant_Up'] = ((res[srNJet][stb][htb]['kappa_constant_Up']/res[srNJet][stb][htb]['kappa_original'])-1)
      res[srNJet][stb][htb]['delta_constant_Down'] = ((res[srNJet][stb][htb]['kappa_constant_Down']/res[srNJet][stb][htb]['kappa_original'])-1)
      res[srNJet][stb][htb]['delta_slope_Up'] = ((res[srNJet][stb][htb]['kappa_slope_Up']/res[srNJet][stb][htb]['kappa_original'])-1)
      res[srNJet][stb][htb]['delta_slope_Down'] = ((res[srNJet][stb][htb]['kappa_slope_Down']/res[srNJet][stb][htb]['kappa_original'])-1)
      print "constant Up" , res[srNJet][stb][htb]['delta_constant_Up'] , "down:" , res[srNJet][stb][htb]['delta_constant_Down']
      print "slope Up" , res[srNJet][stb][htb]['delta_slope_Up'] , "down:" , res[srNJet][stb][htb]['delta_slope_Down']

pickle.dump(res,file('/data/easilar/Spring15/25ns/extended_with_truth_counts_Wkappa_pkl','w'))



