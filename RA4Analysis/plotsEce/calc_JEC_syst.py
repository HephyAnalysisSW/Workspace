import ROOT
import pickle
from array import array
import operator
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
#from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_Moriond2017_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Summer16_Moriond2017_MiniAODv2_postProcessed import *
from Workspace.RA4Analysis.rCShelpers import *
from Workspace.RA4Analysis.signalRegions import *
from Workspace.HEPHYPythonTools.user import username
#from cutFlow_helper import *
from Workspace.RA4Analysis.general_config import *


ROOT.TH1D().SetDefaultSumw2()

maxN = -1

lepSels = [
{'cut':'singleMuonic' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele,single_mu,met],histname="",treeName="Events"),\
  'label':'_mu_', 'str':'1 $\\mu$' ,'trigger': trigger,'trigger_xor':trigger_xor },\
{'cut':'singleElectronic' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele,single_mu,met],histname="",treeName="Events") ,\
  'label':'_ele_', 'str':'1 $\\e$' , 'trigger': trigger, 'trigger_xor': trigger_xor},\
{'cut':'singleLeptonic' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain([single_ele,single_mu,met],histname="",treeName="Events") ,\
  'label':'_lep_', 'str':'1 $\\lep$' , 'trigger': trigger, 'trigger_xor': trigger_xor},\
]

lepSel = lepSels[2]
signalRegions = signalRegions_Moriond2017
btagString = btagVarString

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

presel = "&&".join([lepSel['cut'],lepSel['veto'],"Jet_pt[1]>80",filters,"(iso_Veto)"])
cBkg = getChain([WJetsHTToLNu, TTJets_Comb, singleTop_lep, DY_HT, TTV,diBoson], histname='')
#lep_weight = "lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID"
#weight_str =  "*".join([lep_weight,lepSel['trigWeight'],"weightBTag0_SF","puReweight_true_max4*TopPtWeight*weight*2.25/3"])
weight_str = weight_str_plot
print "base weight" , weight_str

bin = {}
for srNJet in sorted(signalRegions):
  bin[srNJet]={} 
  for stb in sorted(signalRegions[srNJet]):
    bin[srNJet][stb]={}
    for htb in sorted(signalRegions[srNJet][stb]):
      bin[srNJet][stb][htb]={}
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      cut_SR = "deltaPhi_Wl>"+str(deltaPhiCut)
      cut_CR = "deltaPhi_Wl<"+str(deltaPhiCut)
      name_bla, SB_cut    = nameAndCut(stb, htb, (3,4), btb=(0,0), presel=presel, btagVar = btagString)
      #name_bla, SB_cut_CR = nameAndCut(stb, htb, (3,4), btb=(0,-1), presel=presel+"&&"+cut_CR, btagVar = btagString)
      #name_bla, SB_cut_SR = nameAndCut(stb, htb, (3,4), btb=(0,-1), presel=presel+"&&"+cut_SR, btagVar = btagString)
      name    , MB_cut    = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = btagString)
      #name_bla, MB_cut_CR = nameAndCut(stb, htb, srNJet, btb=(0,-1), presel=presel+"&&"+cut_CR, btagVar = btagString)
      #name_bla, MB_cut_SR = nameAndCut(stb, htb, srNJet, btb=(0,-1), presel=presel+"&&"+cut_SR, btagVar = btagString)

      name_bla, SB_cut_jec_central   = nameAndCut(stb, htb, (3,4),  btb=(0,0), presel=presel, btagVar = "jec_nBJet_central" , stVar = 'jec_LT_central', htVar = 'jec_ht_central', njetVar='jec_nJet_central')
      name_bla, MB_cut_jec_central   = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = "jec_nBJet_central" , stVar = 'jec_LT_central', htVar = 'jec_ht_central', njetVar='jec_nJet_central')

      name_bla, SB_cut_jec_up   = nameAndCut(stb, htb, (3,4), btb=(0,0), presel=presel, btagVar = "jec_nBJet_up" , stVar = 'jec_LT_up', htVar = 'jec_ht_up', njetVar='jec_nJet_up')
      name_bla, MB_cut_jec_up   = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = "jec_nBJet_up" , stVar = 'jec_LT_up', htVar = 'jec_ht_up', njetVar='jec_nJet_up')

      name_bla, SB_cut_jec_down   = nameAndCut(stb, htb, (3,4), btb=(0,0), presel=presel, btagVar = "jec_nBJet_down" , stVar = 'jec_LT_down', htVar = 'jec_ht_down', njetVar='jec_nJet_down')
      name_bla, MB_cut_jec_down   = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = "jec_nBJet_down" , stVar = 'jec_LT_down', htVar = 'jec_ht_down', njetVar='jec_nJet_down')

      print name

      rCS_bkg_SB     = max(0,getRCS(cBkg, SB_cut ,  deltaPhiCut,weight = weight_str)['rCS']) 
      rCS_bkg_MB     = max(0,getRCS(cBkg, MB_cut ,  deltaPhiCut,weight = weight_str)['rCS'])
      print rCS_bkg_SB , rCS_bkg_MB
      bin[srNJet][stb][htb]['kappa_original'] = rCS_bkg_MB/rCS_bkg_SB
      print "kappa orig:" , bin[srNJet][stb][htb]['kappa_original']

      rCS_bkg_SB_jec_central    = max(0,getRCS(cBkg, SB_cut_jec_central,  deltaPhiCut,weight = weight_str)['rCS']) 
      rCS_bkg_MB_jec_central    = max(0,getRCS(cBkg, MB_cut_jec_central,  deltaPhiCut,weight = weight_str)['rCS'])
      print rCS_bkg_SB_jec_central , rCS_bkg_MB_jec_central
      bin[srNJet][stb][htb]['kappa_central'] = rCS_bkg_SB_jec_central/rCS_bkg_MB_jec_central
      print "kappa central :" , bin[srNJet][stb][htb]['kappa_central']

      rCS_bkg_SB_jec_up    = max(0,getRCS(cBkg, SB_cut_jec_up,  deltaPhiCut,weight = weight_str)['rCS']) 
      rCS_bkg_MB_jec_up    = max(0,getRCS(cBkg, MB_cut_jec_up,  deltaPhiCut,weight = weight_str)['rCS'])
      print rCS_bkg_SB_jec_up , rCS_bkg_MB_jec_up
      bin[srNJet][stb][htb]['kappa_up'] = rCS_bkg_SB_jec_up/rCS_bkg_MB_jec_up
      print "kappa up :" , bin[srNJet][stb][htb]['kappa_up']

      rCS_bkg_SB_jec_down    = max(0,getRCS(cBkg, SB_cut_jec_down,  deltaPhiCut,weight = weight_str)['rCS']) 
      rCS_bkg_MB_jec_down    = max(0,getRCS(cBkg, MB_cut_jec_down,  deltaPhiCut,weight = weight_str)['rCS'])
      print rCS_bkg_SB_jec_down , rCS_bkg_MB_jec_down
      bin[srNJet][stb][htb]['kappa_down'] = rCS_bkg_SB_jec_down/rCS_bkg_MB_jec_down
      print "kappa down :" , bin[srNJet][stb][htb]['kappa_down']

      #bin[srNJet][stb][htb]['delta_Up'] = ((bin[srNJet][stb][htb]['kappa_up']/bin[srNJet][stb][htb]['kappa_original'])-1) 
      #print "delta up:" , bin[srNJet][stb][htb]['delta_Up']

      #bin[srNJet][stb][htb]['delta_down'] = ((bin[srNJet][stb][htb]['kappa_down']/bin[srNJet][stb][htb]['kappa_original'])-1) 
      #print "delta down:" , bin[srNJet][stb][htb]['delta_down']

      bin[srNJet][stb][htb]['delta_Up_central'] = ((bin[srNJet][stb][htb]['kappa_up']/bin[srNJet][stb][htb]['kappa_central'])-1) 
      print "delta up central:" , bin[srNJet][stb][htb]['delta_Up_central']

      bin[srNJet][stb][htb]['delta_Down_central'] = ((bin[srNJet][stb][htb]['kappa_down']/bin[srNJet][stb][htb]['kappa_central'])-1) 
      print "delta down_central:" , bin[srNJet][stb][htb]['delta_Down_central']

sys_dir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/sys/JEC/'
if not os.path.exists(sys_dir):
  os.makedirs(sys_dir)
pickle.dump(bin,file(sys_dir+'unc_on_JEC_SRAll_pkl','w'))

