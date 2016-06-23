import ROOT
import pickle
from array import array
import operator
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Data25ns_Promtv2_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *
from Workspace.RA4Analysis.signalRegions import *
from Workspace.RA4Analysis.rCShelpers import *
from Workspace.HEPHYPythonTools.user import username
from cutFlow_helper import *
from general_config import *

ROOT.TH1F().SetDefaultSumw2()

sample_lumi =3000
#lumi = 804##pb
reweight      = '(weight*'+str(lumi)+')/'+str(sample_lumi)

btagString = "nBJetMediumCSV30"
maxN = -1
#input_pickle_dir = '/data/dspitzbart/Results2016/Prediction_SFtemplates_validation_lep_MC_SF_2p3/singleLeptonic_Spring15__estimationResults_pkl'
#res = pickle.load(file(input_pickle_dir))
#DL = pickle.load(file('/data/easilar/Spring15/25ns/DL_syst_pkl'))
DL = pickle.load(file('/data/easilar/Results2016/ICHEP/DiLep_SYS/V1/DL_syst_0b_pkl'))
lepSels = [
{'cut':'((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 #'chain': getChain([single_ele_Run2015D,single_mu_Run2015D],maxN=maxN,histname="",treeName="Events") ,\
 'trigWeight': "0.94" ,\
  'label':'_lep_', 'str':'1 $lep$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
]

lepSel = lepSels[0]
#signalRegion3fb = {(8, -1):  {(250, 350): {(500, 750):  {'deltaPhi': 1.0}}}}
signalRegions = signalRegion3fb
#signalRegions = validationRegionAll
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

#constant = abs(DL[(4,-1)][(250,-1)][(500,-1)]["constant"]-1) 
#nJetMean = DL[(4,-1)][(250,-1)][(500,-1)]["nJetMean"] 
#slope    = DL[(4,-1)][(250,-1)][(500,-1)]["slope"] 
constant = 0.35
nJetMean = 5.24
slope    = 0.04 

constant_weight = "("+str(constant)+")"
slope_weight = "((nJet30-"+str(nJetMean)+")*"+str(slope)+")"

calc_errs = [\
{"name":"slope","weight":slope_weight},\
{"name":"constant","weight":constant_weight}
]

presel = presel = "&&".join([lepSel['cut'],lepSel['veto'],filters])
#c_tt = {"sample":"ttJets", "chain":getChain(TTJets_Lep, maxN=maxN,histname="",treeName="Events"), "weight1b":"weightBTag1_SF" , "weight0b":"weightBTag0_SF" ,"cut":(0,-1) , "name":TTJets_Comp, "tex":"ttbar + jets",'color':ROOT.kBlue-4}
c_tt = {"sample":"ttJets", "chain":getChain(TTJets_Lep, maxN=maxN,histname="",treeName="Events"), "weight1b":"(1)" , "weight0b":"(1)" ,"cut_1b":(1,1) ,"cut_0b":(0,0) ,"name":TTJets_Lep, "tex":"ttbar + jets",'color':ROOT.kBlue-4}
c_DY = {"sample":"DY", "chain":getChain(DY_amc, maxN=maxN,histname="",treeName="Events"),  "weight":"(1)" ,"cut":(0,0) , "name":DY_amc, "tex":"DY",'color':ROOT.kRed-6}
cRest = getChain([TTV,singleTop_lep],histname='') #no QCD
cW = getChain([WJetsHTToLNu],histname='')
#common_weight = lepSel['trigWeight']+"*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*puReweight_true_max4*TopPtWeight*weight*2.3/3"
common_weight = reweight

res = {}
for srNJet in sorted(signalRegions):
  res[srNJet] = {}
  for stb in sorted(signalRegions[srNJet]):
    res[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      res[srNJet][stb][htb] = {}
      print srNJet , stb , htb
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      name,     cut_DY_SR =  nameAndCut(stb, htb, srNJet, btb=c_DY["cut"], presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      print name
      name_bla, tt_SB_cut = nameAndCut(stb, htb, (3,4), btb=c_tt["cut_1b"], presel=presel, btagVar = btagString)
      name_bla, tt_SB_cut_CR = nameAndCut(stb, htb, (3,4), btb=c_tt["cut_1b"], presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      name_bla, tt_SB_cut_SR = nameAndCut(stb, htb, (3,4), btb=c_tt["cut_1b"], presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      name_bla, tt_MB_cut = nameAndCut(stb, htb, srNJet, btb=c_tt["cut_0b"], presel=presel, btagVar = btagString)
      name_bla, tt_MB_cut_CR =nameAndCut(stb, htb, srNJet, btb=c_tt["cut_0b"], presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString) 
      name_bla, tt_MB_cut_SR =nameAndCut(stb, htb, srNJet, btb=c_tt["cut_0b"], presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString) 

      name_bla, W_SB_cut = nameAndCut(stb, htb, (3,4), btb=c_tt["cut_0b"], presel=presel, btagVar = btagString)
      name_bla, W_SB_cut_CR = nameAndCut(stb, htb, (3,4), btb=c_tt["cut_0b"], presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      name_bla, W_SB_cut_SR = nameAndCut(stb, htb, (3,4), btb=c_tt["cut_0b"], presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)


      name_bla, W_MB_cut = nameAndCut(stb, htb, srNJet, btb=c_tt["cut_0b"], presel=presel, btagVar = btagString)
      name_bla, W_MB_cut_CR = nameAndCut(stb, htb, srNJet, btb=c_tt["cut_0b"], presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      name_bla, W_MB_cut_SR = nameAndCut(stb, htb, srNJet, btb=c_tt["cut_0b"], presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)



      name_bla, DY_SB_cut =  nameAndCut(stb, htb, (3,4), btb=c_DY["cut"], presel=presel, btagVar = btagString)
      name_bla, DY_SB_cut_CR =  nameAndCut(stb, htb, (3,4), btb=c_DY["cut"], presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      name_bla, DY_SB_cut_SR =  nameAndCut(stb, htb, (3,4), btb=c_DY["cut"], presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      name_bla, DY_MB_cut =  nameAndCut(stb, htb, srNJet, btb=c_DY["cut"], presel=presel, btagVar = btagString)
      name_bla, DY_MB_cut_CR =  nameAndCut(stb, htb, srNJet, btb=c_DY["cut"], presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      name_bla, DY_MB_cut_SR =  nameAndCut(stb, htb, srNJet, btb=c_DY["cut"], presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)

      
      ## RCS for SB and MB#
      rCS_tt_SB_diLep = getRCS(c_tt['chain'],"(ngenLep+ngenTau)==2&&"+tt_SB_cut ,  deltaPhiCut,weight = common_weight+"*"+c_tt['weight1b'])
      rCS_tt_SB_rest  = getRCS(c_tt['chain'],"(ngenLep+ngenTau)!=2&&"+tt_SB_cut ,  deltaPhiCut,weight = common_weight+"*"+c_tt['weight1b'])

      rCS_DY_SB_diLep = getRCS(c_DY['chain'],"(ngenLep+ngenTau)==2&&"+DY_SB_cut ,  deltaPhiCut,weight = common_weight)
      rCS_DY_SB_rest  = getRCS(c_DY['chain'],"(ngenLep+ngenTau)!=2&&"+DY_SB_cut ,  deltaPhiCut,weight = common_weight)
      rCS_W_SB        = getRCS(cW,W_SB_cut ,  deltaPhiCut,weight = common_weight+"*"+c_tt["weight0b"])
      rCS_Rest_SB     = getRCS(cRest,DY_SB_cut ,  deltaPhiCut,weight = common_weight)

      rCS_DY_MB_diLep = getRCS(c_DY['chain'],"(ngenLep+ngenTau)==2&&"+DY_MB_cut ,  deltaPhiCut,weight = common_weight)
      rCS_DY_MB_rest  = getRCS(c_DY['chain'],"(ngenLep+ngenTau)!=2&&"+DY_MB_cut ,  deltaPhiCut,weight = common_weight)
      rCS_W_MB        = getRCS(cW,W_MB_cut ,  deltaPhiCut,weight = common_weight+"*"+c_tt["weight0b"])
      rCS_Rest_MB     = getRCS(cRest,DY_MB_cut ,  deltaPhiCut,weight = common_weight)

      rCS_tt_MB_diLep = getRCS(c_tt['chain'],"(ngenLep+ngenTau)==2&&"+tt_MB_cut ,  deltaPhiCut,weight = common_weight+"*"+c_tt['weight0b'])
      rCS_tt_MB_rest  = getRCS(c_tt['chain'],"(ngenLep+ngenTau)!=2&&"+tt_MB_cut ,  deltaPhiCut,weight = common_weight+"*"+c_tt['weight0b'])

      print "rCS_tt_SB_diLep  ",rCS_tt_SB_diLep
      print "rCS_tt_SB_rest"   ,rCS_tt_SB_rest
      print "rCS_DY_SB_diLep  ",rCS_DY_SB_diLep
      print "rCS_DY_SB_restp  ",rCS_DY_SB_rest
      print "rCS_W_SB      "   ,rCS_W_SB
      print "rCS_Rest_SB   "   ,rCS_Rest_SB
      print "rCS_DY_MB_diLep  ",rCS_DY_MB_diLep
      print "rCS_DY_MB_restp  ",rCS_DY_MB_rest
      print "rCS_W_MB        " ,rCS_W_MB
      print "rCS_Rest_MB     " ,rCS_Rest_MB
      print "rCS_tt_MB_diLep " ,rCS_tt_MB_diLep
      print "rCS_tt_MB_rest  " ,rCS_tt_MB_rest

      rCS_tt_SB_diLep=max(0,rCS_tt_SB_diLep['rCS'])
      rCS_tt_SB_rest =max(0,rCS_tt_SB_rest['rCS'])
      rCS_DY_SB_diLep=max(0,rCS_DY_SB_diLep['rCS'])
      rCS_DY_SB_rest =max(0,rCS_DY_SB_rest['rCS'])
      rCS_W_SB       =max(0,rCS_W_SB['rCS'])
      rCS_Rest_SB    =max(0,rCS_Rest_SB['rCS'])
      rCS_DY_MB_diLep=max(0,rCS_DY_MB_diLep['rCS'])
      rCS_DY_MB_rest =max(0,rCS_DY_MB_rest['rCS'])
      rCS_W_MB       =max(0,rCS_W_MB['rCS'])
      rCS_Rest_MB    =max(0,rCS_Rest_MB['rCS'])
      rCS_tt_MB_diLep=max(0,rCS_tt_MB_diLep['rCS'])
      rCS_tt_MB_rest =max(0,rCS_tt_MB_rest['rCS'])


      for calc in calc_errs:

        variations = [("Up","+"),("Down","-")]
        for variation in variations:

          ####fractions  MB ######
          yield_diLep_tt_MB_in_CR                   = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+tt_MB_cut_CR, weight = common_weight+"*"+c_tt['weight0b'])) 
          yield_diLep_tt_MB_in_CR_constant_Up       = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+tt_MB_cut_CR, weight = common_weight+"*"+c_tt['weight0b']+"*(1"+variation[1]+calc["weight"]+")")) 
          
          print "yield_diLep_tt_MB_in_CR" , yield_diLep_tt_MB_in_CR
          print "yield_diLep_tt_MB_in_CR_constant_Up   " , yield_diLep_tt_MB_in_CR_constant_Up   

          yield_diLep_tt_MB_in_SR                   = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+tt_MB_cut_SR, weight = common_weight+"*"+c_tt['weight0b']))
          yield_diLep_tt_MB_in_SR_constant_Up       = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+tt_MB_cut_SR, weight = common_weight+"*"+c_tt['weight0b']+"*(1"+variation[1]+calc["weight"]+")"))

          yield_rest_tt_MB_in_CR = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)!=2&&"+tt_MB_cut_CR, weight = common_weight+"*"+c_tt['weight0b'])) 
          yield_rest_tt_MB_in_SR = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)!=2&&"+tt_MB_cut_SR, weight = common_weight+"*"+c_tt['weight0b'])) 

          yield_diLep_DY_MB_in_CR                   = max(0,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_MB_cut_CR, weight = common_weight))
          yield_diLep_DY_MB_in_CR_constant_Up       = max(0,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_MB_cut_CR, weight = common_weight+"*(1"+variation[1]+calc["weight"]+")"))

          print "yield_diLep_DY_MB_in_CR              " ,yield_diLep_DY_MB_in_CR              
          print "yield_diLep_DY_MB_in_CR_constant_Up  " ,yield_diLep_DY_MB_in_CR_constant_Up  


          yield_diLep_DY_MB_in_SR                   = max(0.0000001,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_MB_cut_SR, weight = common_weight))
          yield_diLep_DY_MB_in_SR_constant_Up       = max(0.0000001,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_MB_cut_SR, weight = common_weight+"*(1"+variation[1]+calc["weight"]+")"))

          yield_rest_DY_MB_in_CR                    = max(0.0000001,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)!=2&&"+DY_MB_cut_CR, weight = common_weight))

          yield_rest_EWK_MB_in_CR                   = max(0.0000001,getYieldFromChain(cRest, DY_MB_cut_CR, weight = common_weight))
          yield_rest_W_MB_in_CR                     = max(0.0000001,getYieldFromChain(cW   , W_MB_cut_CR, weight = common_weight+"*"+c_tt["weight0b"]))

          yield_rest_DY_MB_in_SR                    = max(0.0000001,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)!=2&&"+DY_MB_cut_SR, weight = common_weight))

          yield_rest_EWK_MB_in_SR                   = max(0.0000001,getYieldFromChain(cRest, DY_MB_cut_SR, weight = common_weight))
          yield_rest_W_MB_in_SR                     = max(0.0000001,getYieldFromChain(cW   , W_MB_cut_SR, weight = common_weight+"*"+c_tt["weight0b"]))




          den_tot_MB_in_CR = yield_diLep_tt_MB_in_CR + yield_rest_tt_MB_in_CR + yield_diLep_DY_MB_in_CR + yield_rest_DY_MB_in_CR + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR 
          den_tot_MB_in_CR_constant_Up   = yield_diLep_tt_MB_in_CR_constant_Up   + yield_rest_tt_MB_in_CR + yield_diLep_DY_MB_in_CR_constant_Up   + yield_rest_DY_MB_in_CR + yield_rest_EWK_MB_in_CR + yield_rest_W_MB_in_CR 

          yield_tt_MB_in_CR = yield_diLep_tt_MB_in_CR + yield_rest_tt_MB_in_CR
          yield_tt_MB_in_CR_constant_Up   = yield_diLep_tt_MB_in_CR_constant_Up   + yield_rest_tt_MB_in_CR

          frac_tt_MB_in_CR = yield_tt_MB_in_CR / den_tot_MB_in_CR
          frac_tt_MB_in_CR_constant_Up   = yield_tt_MB_in_CR_constant_Up   / den_tot_MB_in_CR_constant_Up  

          frac_diLep_tt_MB_in_CR               = yield_diLep_tt_MB_in_CR               /(yield_rest_tt_MB_in_CR +  yield_diLep_tt_MB_in_CR              )
          frac_diLep_tt_MB_in_CR_constant_Up   = yield_diLep_tt_MB_in_CR_constant_Up   /(yield_rest_tt_MB_in_CR +  yield_diLep_tt_MB_in_CR_constant_Up  )
          frac_rest_tt_MB_in_CR = 1 - frac_diLep_tt_MB_in_CR 
          frac_rest_tt_MB_in_CR_constant_Up   = 1 - frac_diLep_tt_MB_in_CR_constant_Up   
          rCS_tt_MB_full = frac_diLep_tt_MB_in_CR*rCS_tt_MB_diLep + frac_rest_tt_MB_in_CR*rCS_tt_MB_rest
          rCS_tt_MB_full_constant_Up   = frac_diLep_tt_MB_in_CR_constant_Up  *rCS_tt_MB_diLep + frac_rest_tt_MB_in_CR_constant_Up  *rCS_tt_MB_rest

           
          print "frac_diLep_tt_MB_in_CR              " ,frac_diLep_tt_MB_in_CR              
          print "frac_diLep_tt_MB_in_CR_"+calc['name']+'_'+variation[0] ,frac_diLep_tt_MB_in_CR_constant_Up  

          print "yield_rest_tt_MB_in_CR " , yield_rest_tt_MB_in_CR 
          print "yield_rest_tt_MB_in_SR " , yield_rest_tt_MB_in_SR 
          print "yield_diLep_DY_MB_in_SR               " , yield_diLep_DY_MB_in_SR               
          print "yield_diLep_DY_MB_in_SR_"+calc['name']+'_'+variation[0] , yield_diLep_DY_MB_in_SR_constant_Up   
          print "yield_diLep_tt_MB_in_SR                " ,yield_diLep_tt_MB_in_SR                
          print "yield_diLep_tt_MB_in_SR_"+calc['name']+'_'+variation[0] ,yield_diLep_tt_MB_in_SR_constant_Up    

          print "yield_rest_DY_MB_in_SR  " ,yield_rest_DY_MB_in_SR  
          print "yield_rest_EWK_MB_in_SR " ,yield_rest_EWK_MB_in_SR 
          print "yield_rest_W_MB_in_SR   " ,yield_rest_W_MB_in_SR   
          print "yield_rest_DY_MB_in_CR  " ,yield_rest_DY_MB_in_CR  
          print "yield_rest_EWK_MB_in_CR " ,yield_rest_EWK_MB_in_CR 
          print "yield_rest_W_MB_in_CR   " ,yield_rest_W_MB_in_CR   



  #####  
          yield_DY_MB_in_CR = yield_diLep_DY_MB_in_CR + yield_rest_DY_MB_in_CR
          yield_DY_MB_in_CR_constant_Up   = yield_diLep_DY_MB_in_CR_constant_Up   + yield_rest_DY_MB_in_CR

          frac_DY_MB_in_CR = yield_DY_MB_in_CR / den_tot_MB_in_CR
          frac_DY_MB_in_CR_constant_Up   = yield_DY_MB_in_CR_constant_Up   / den_tot_MB_in_CR_constant_Up

          frac_diLep_DY_MB_in_CR               = yield_diLep_DY_MB_in_CR               /(yield_rest_DY_MB_in_CR +  yield_diLep_DY_MB_in_CR              )
          frac_diLep_DY_MB_in_CR_constant_Up   = yield_diLep_DY_MB_in_CR_constant_Up   /(yield_rest_DY_MB_in_CR +  yield_diLep_DY_MB_in_CR_constant_Up  )
          frac_rest_DY_MB_in_CR = 1 - frac_diLep_DY_MB_in_CR
          frac_rest_DY_MB_in_CR_constant_Up   = 1 - frac_diLep_DY_MB_in_CR_constant_Up
          rCS_DY_MB_full = frac_diLep_DY_MB_in_CR*rCS_DY_MB_diLep + frac_rest_DY_MB_in_CR*rCS_DY_MB_rest
          rCS_DY_MB_full_constant_Up   = frac_diLep_DY_MB_in_CR_constant_Up  *rCS_DY_MB_diLep + frac_rest_DY_MB_in_CR_constant_Up  *rCS_DY_MB_rest
  #####  

          frac_W_MB_in_CR = yield_rest_W_MB_in_CR / den_tot_MB_in_CR 
          frac_W_MB_in_CR_constant_Up   = yield_rest_W_MB_in_CR / den_tot_MB_in_CR_constant_Up   

          frac_EWK_MB_in_CR = yield_rest_EWK_MB_in_CR / den_tot_MB_in_CR 
          frac_EWK_MB_in_CR_constant_Up   = yield_rest_EWK_MB_in_CR / den_tot_MB_in_CR_constant_Up   

          rCS_tot_MB_full = frac_tt_MB_in_CR*rCS_tt_MB_full + frac_DY_MB_in_CR*rCS_DY_MB_full + frac_W_MB_in_CR*rCS_W_MB + frac_EWK_MB_in_CR*rCS_Rest_MB
          rCS_tot_MB_full_constant_Up   = frac_tt_MB_in_CR_constant_Up    *  rCS_tt_MB_full_constant_Up   + frac_DY_MB_in_CR_constant_Up  *rCS_DY_MB_full_constant_Up   + frac_W_MB_in_CR_constant_Up  *rCS_W_MB + frac_EWK_MB_in_CR_constant_Up  *rCS_Rest_MB


          MB_SR_tot_yield = yield_diLep_DY_MB_in_SR + yield_diLep_tt_MB_in_SR + yield_rest_tt_MB_in_SR + yield_rest_DY_MB_in_SR + yield_rest_W_MB_in_SR + yield_rest_EWK_MB_in_SR 
          print "CHECK RCS :" , "MB SR tot yields :" , MB_SR_tot_yield
          MB_CR_tot_yield = yield_diLep_DY_MB_in_CR + yield_diLep_tt_MB_in_CR + yield_rest_tt_MB_in_CR + yield_rest_DY_MB_in_CR + yield_rest_W_MB_in_CR + yield_rest_EWK_MB_in_CR 
          print "CHECK RCS :" , "MB CR tot yields :" ,  MB_CR_tot_yield
          print "CHECK RCS MB :" ,  MB_SR_tot_yield/MB_CR_tot_yield




          ###to calculate SB####

          yield_diLep_tt_SB_in_CR                   = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+tt_SB_cut_CR, weight = common_weight+"*"+c_tt['weight0b'])) 
          yield_diLep_tt_SB_in_CR_constant_Up       = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+tt_SB_cut_CR, weight = common_weight+"*"+c_tt['weight0b']+"*(1"+variation[1]+calc["weight"]+")")) 
          
          yield_rest_tt_SB_in_CR = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)!=2&&"+tt_SB_cut_CR, weight = common_weight+"*"+c_tt['weight0b'])) 

          yield_diLep_DY_SB_in_CR                   = max(0,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_SB_cut_CR, weight = common_weight))
          yield_diLep_DY_SB_in_CR_constant_Up       = max(0,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_SB_cut_CR, weight = common_weight+"*(1"+variation[1]+calc["weight"]+")"))

          yield_rest_DY_SB_in_CR                    = max(0,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)!=2&&"+DY_SB_cut_CR, weight = common_weight))

          yield_rest_EWK_SB_in_CR                   = max(0,getYieldFromChain(cRest, DY_SB_cut_CR, weight = common_weight))
          yield_rest_W_SB_in_CR                     = max(0,getYieldFromChain(cW   , W_SB_cut_CR, weight = common_weight+"*"+c_tt["weight0b"]))

          den_tot_SB_in_CR = yield_diLep_tt_SB_in_CR + yield_rest_tt_SB_in_CR + yield_diLep_DY_SB_in_CR + yield_rest_DY_SB_in_CR + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR 
          den_tot_SB_in_CR_constant_Up   = yield_diLep_tt_SB_in_CR_constant_Up   + yield_rest_tt_SB_in_CR + yield_diLep_DY_SB_in_CR_constant_Up   + yield_rest_DY_SB_in_CR + yield_rest_EWK_SB_in_CR + yield_rest_W_SB_in_CR 

          yield_tt_SB_in_CR = yield_diLep_tt_SB_in_CR + yield_rest_tt_SB_in_CR
          yield_tt_SB_in_CR_constant_Up   = yield_diLep_tt_SB_in_CR_constant_Up   + yield_rest_tt_SB_in_CR

          frac_tt_SB_in_CR = yield_tt_SB_in_CR / den_tot_SB_in_CR
          frac_tt_SB_in_CR_constant_Up   = yield_tt_SB_in_CR_constant_Up   / den_tot_SB_in_CR_constant_Up  

          frac_diLep_tt_SB_in_CR               = yield_diLep_tt_SB_in_CR               /(yield_rest_tt_SB_in_CR +  yield_diLep_tt_SB_in_CR              )
          frac_diLep_tt_SB_in_CR_constant_Up   = yield_diLep_tt_SB_in_CR_constant_Up   /(yield_rest_tt_SB_in_CR +  yield_diLep_tt_SB_in_CR_constant_Up  )
          frac_rest_tt_SB_in_CR = 1 - frac_diLep_tt_SB_in_CR 
          frac_rest_tt_SB_in_CR_constant_Up   = 1 - frac_diLep_tt_SB_in_CR_constant_Up   
          rCS_tt_SB_full = frac_diLep_tt_SB_in_CR*rCS_tt_SB_diLep + frac_rest_tt_SB_in_CR*rCS_tt_SB_rest
          rCS_tt_SB_full_constant_Up   = frac_diLep_tt_SB_in_CR_constant_Up  *rCS_tt_SB_diLep + frac_rest_tt_SB_in_CR_constant_Up  *rCS_tt_SB_rest

  #####  
          yield_DY_SB_in_CR = yield_diLep_DY_SB_in_CR + yield_rest_DY_SB_in_CR
          yield_DY_SB_in_CR_constant_Up   = yield_diLep_DY_SB_in_CR_constant_Up   + yield_rest_DY_SB_in_CR

          frac_DY_SB_in_CR = yield_DY_SB_in_CR / den_tot_SB_in_CR
          frac_DY_SB_in_CR_constant_Up   = yield_DY_SB_in_CR_constant_Up   / den_tot_SB_in_CR_constant_Up

          frac_diLep_DY_SB_in_CR               = yield_diLep_DY_SB_in_CR               /(yield_rest_DY_SB_in_CR +  yield_diLep_DY_SB_in_CR              )
          frac_diLep_DY_SB_in_CR_constant_Up   = yield_diLep_DY_SB_in_CR_constant_Up   /(yield_rest_DY_SB_in_CR +  yield_diLep_DY_SB_in_CR_constant_Up  )
          frac_rest_DY_SB_in_CR = 1 - frac_diLep_DY_SB_in_CR
          frac_rest_DY_SB_in_CR_constant_Up   = 1 - frac_diLep_DY_SB_in_CR_constant_Up
          rCS_DY_SB_full = frac_diLep_DY_SB_in_CR*rCS_DY_SB_diLep + frac_rest_DY_SB_in_CR*rCS_DY_SB_rest
          rCS_DY_SB_full_constant_Up   = frac_diLep_DY_SB_in_CR_constant_Up  *rCS_DY_SB_diLep + frac_rest_DY_SB_in_CR_constant_Up  *rCS_DY_SB_rest
  #####  

          frac_W_SB_in_CR = yield_rest_W_SB_in_CR / den_tot_SB_in_CR 
          frac_W_SB_in_CR_constant_Up   = yield_rest_W_SB_in_CR / den_tot_SB_in_CR_constant_Up   

          frac_EWK_SB_in_CR = yield_rest_EWK_SB_in_CR / den_tot_SB_in_CR 
          frac_EWK_SB_in_CR_constant_Up   = yield_rest_EWK_SB_in_CR / den_tot_SB_in_CR_constant_Up   

          rCS_tot_SB_full = frac_tt_SB_in_CR*rCS_tt_SB_full + frac_DY_SB_in_CR*rCS_DY_SB_full + frac_W_SB_in_CR*rCS_W_SB + frac_EWK_SB_in_CR*rCS_Rest_SB
          rCS_tot_SB_full_constant_Up   = frac_tt_SB_in_CR_constant_Up    *  rCS_tt_SB_full_constant_Up   + frac_DY_SB_in_CR_constant_Up  *rCS_DY_SB_full_constant_Up   + frac_W_SB_in_CR_constant_Up  *rCS_W_SB + frac_EWK_SB_in_CR_constant_Up  *rCS_Rest_SB



          yield_diLep_DY_SB_in_SR                   = max(0,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_SB_cut_SR, weight = common_weight))
          yield_diLep_DY_SB_in_SR_constant_Up       = max(0,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)==2&&"+DY_SB_cut_SR, weight = common_weight+"*(1"+variation[1]+calc["weight"]+")"))



          yield_rest_DY_SB_in_SR                    = max(0,getYieldFromChain(c_DY['chain'], "(ngenLep+ngenTau)!=2&&"+DY_SB_cut_SR, weight = common_weight))

          yield_rest_EWK_SB_in_SR                   = max(0,getYieldFromChain(cRest, DY_SB_cut_SR, weight = common_weight))
          yield_rest_W_SB_in_SR                     = max(0,getYieldFromChain(cW   , W_SB_cut_SR, weight = common_weight+"*"+c_tt["weight0b"]))



          yield_rest_tt_SB_in_SR = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)!=2&&"+tt_SB_cut_SR, weight = common_weight+"*"+c_tt['weight0b'])) 



          yield_diLep_tt_SB_in_SR                   = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+tt_SB_cut_SR, weight = common_weight+"*"+c_tt['weight0b']))
          yield_diLep_tt_SB_in_SR_constant_Up       = max(0,getYieldFromChain(c_tt['chain'], "(ngenLep+ngenTau)==2&&"+tt_SB_cut_SR, weight = common_weight+"*"+c_tt['weight0b']+"*(1"+variation[1]+calc["weight"]+")"))


          SB_SR_tot_yield = yield_diLep_DY_SB_in_SR + yield_diLep_tt_SB_in_SR + yield_rest_tt_SB_in_SR + yield_rest_DY_SB_in_SR + yield_rest_W_SB_in_SR + yield_rest_EWK_SB_in_SR 
          print "CHECK RCS :" , "SB SR tot yields :" , SB_SR_tot_yield
          SB_CR_tot_yield = yield_diLep_DY_SB_in_CR + yield_diLep_tt_SB_in_CR + yield_rest_tt_SB_in_CR + yield_rest_DY_SB_in_CR + yield_rest_W_SB_in_CR + yield_rest_EWK_SB_in_CR 
          print "CHECK RCS :" , "SB CR tot yields :" , SB_CR_tot_yield
          print "CHECK RCS SB :" ,  SB_SR_tot_yield/SB_CR_tot_yield



          print "yield_diLep_tt_SB_in_CR               " , yield_diLep_tt_SB_in_CR
          print "yield_diLep_tt_SB_in_CR_"+calc['name']+'_'+variation[0] , yield_diLep_tt_SB_in_CR_constant_Up


          print "yield_diLep_DY_SB_in_CR              " ,yield_diLep_DY_SB_in_CR
          print "yield_diLep_DY_SB_in_CR_"+calc['name']+'_'+variation[0] ,yield_diLep_DY_SB_in_CR_constant_Up

          print "yield_rest_tt_SB_in_CR " , yield_rest_tt_SB_in_CR 
          print "yield_rest_tt_SB_in_SR " , yield_rest_tt_SB_in_SR 
          print "yield_diLep_DY_SB_in_SR               " , yield_diLep_DY_SB_in_SR               
          print "yield_diLep_DY_SB_in_SR_"+calc['name']+'_'+variation[0] , yield_diLep_DY_SB_in_SR_constant_Up   
          print "yield_diLep_tt_SB_in_SR                " ,yield_diLep_tt_SB_in_SR                     
          print "yield_diLep_tt_SB_in_SR_"+calc['name']+'_'+variation[0] ,yield_diLep_tt_SB_in_SR_constant_Up         
                                                                                                        
          print "yield_rest_DY_SB_in_SR  " ,yield_rest_DY_SB_in_SR                                      
          print "yield_rest_EWK_SB_in_SR " ,yield_rest_EWK_SB_in_SR                                     
          print "yield_rest_W_SB_in_SR   " ,yield_rest_W_SB_in_SR                                       
          print "yield_rest_DY_SB_in_CR  " ,yield_rest_DY_SB_in_CR                                      
          print "yield_rest_EWK_SB_in_CR " ,yield_rest_EWK_SB_in_CR                                     
          print "yield_rest_W_SB_in_CR   " ,yield_rest_W_SB_in_CR   


          print "rCS_tot_MB_full" , rCS_tot_MB_full , "rCS_tot_SB_full" , rCS_tot_SB_full
          print "rCS_tot_MB_full_"+calc['name']+'_'+variation[0] , rCS_tot_MB_full_constant_Up   , "rCS_tot_SB_full_"+calc['name']+'_'+variation[0] , rCS_tot_SB_full_constant_Up  

          res[srNJet][stb][htb]['kappa_original']        =  rCS_tot_MB_full / rCS_tot_SB_full 
          res[srNJet][stb][htb]['kappa_'+calc['name']+'_'+variation[0]]     =  rCS_tot_MB_full_constant_Up   / rCS_tot_SB_full_constant_Up    
          print "kappa:" , res[srNJet][stb][htb]['kappa_original'] , res[srNJet][stb][htb]['kappa_'+calc['name']+'_'+variation[0]] 


          res[srNJet][stb][htb]['delta_'+calc['name']+'_'+variation[0]] = ((res[srNJet][stb][htb]['kappa_'+calc['name']+'_'+variation[0]]/res[srNJet][stb][htb]['kappa_original'])-1)
          print calc['name']+'_'+variation[0] , res[srNJet][stb][htb]['delta_'+calc['name']+'_'+variation[0]]

pickle.dump(res,file('/data/easilar/Results2016/ICHEP/DiLep_SYS/V1/unc_with_SRAll_pkl','w'))



