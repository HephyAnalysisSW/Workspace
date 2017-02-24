import ROOT
import pickle
from array import array
import operator
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.signalRegions import *
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.general_config import *
from math import sqrt, pi
ROOT.TH1F().SetDefaultSumw2()

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--mglu", dest="mglu", default=1000, action="store", help="mglu")
(options, args) = parser.parse_args()

#exec("tmp_mglu="+options.mglu)
#print type(tmp_mglu)
#mglu = tmp_mglu
#sig_dict = pickle.load(file('/data/easilar/Results2016/ICHEP/signal_Spring16/mglu'+str(mglu)+'Signals_12p88_pkl')) 

use_btagWeights = False
if use_btagWeights: 
  weight_str = weight_str_signal_plot+"*"+weight_0b
  nbtag = (0,-1)
else: 
  weight_str = weight_str_signal_plot
  nbtag = (0,0)

mglu = 1900
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&iso_Veto"  #&&flag_crazy_jets"

signal = SMS_T5qqqqVV_TuneCUETP8M1

signalRegions = signalRegions_Moriond2017
#signalRegions = signalRegions_Moriond2017_onebyone[0]

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


expand_dict = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/pickles/signals/mglu'+str(mglu)+'Signal_isoVetoCorrected_pkl'))

bin = {}
for srNJet in sorted(signalRegions):
  bin[srNJet]={}
  for stb in sorted(signalRegions[srNJet]):
    bin[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      bin[srNJet][stb][htb] = {}
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      print srNJet , stb , htb      

      #weight_str_ISR_up = weight_str+"*ISRSigUp"
      #weight_str_ISR_down = weight_str+"*ISRSigDown"
      name_bla, MB_cut               = nameAndCut(stb, htb, srNJet, btb=nbtag, presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      name_bla, MB_cut_jec_central   = nameAndCut(stb, htb, srNJet, btb=nbtag, presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = "jec_nBJet_central" , stVar = 'jec_LT_central', htVar = 'jec_ht_central', njetVar='jec_nJet_central')
      name_bla, MB_cut_jec_up        = nameAndCut(stb, htb, srNJet, btb=nbtag, presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = "jec_nBJet_up"      , stVar = 'jec_LT_up'     , htVar = 'jec_ht_up'     , njetVar='jec_nJet_up')
      name_bla, MB_cut_jec_down      = nameAndCut(stb, htb, srNJet, btb=nbtag, presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = "jec_nBJet_down"    , stVar = 'jec_LT_down'   , htVar = 'jec_ht_down'   , njetVar='jec_nJet_down')

      bin[srNJet][stb][htb]["signals"] = {}
      #for mglu in signal.keys() :
      for mglu in [mglu] :
        bin[srNJet][stb][htb]["signals"][mglu] = {}
        #for mlsp in signal[mglu].keys() :
        for mlsp in [100] :
          s_chain = getChain(signal[mglu][mlsp],histname='')
          bin[srNJet][stb][htb]["signals"][mglu][mlsp] = {\
          #"yield_MB_SR_orig":       getYieldFromChain(s_chain, MB_cut, weight = weight_str),"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut, weight = weight_str+"*"+weight_str)),\
          #"yield_MB_SR_ISR_up":     getYieldFromChain(s_chain, MB_cut_ISR, weight = weight_str_ISR_up)  ,"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut_ISR, weight = weight_str_ISR_up+"*"+weight_str_ISR_up)),\
          #"yield_MB_SR_ISR_down":   getYieldFromChain(s_chain, MB_cut_ISR, weight = weight_str_ISR_down),"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut_ISR, weight = weight_str_ISR_down+"*"+weight_str_ISR_down)),\
          "yield_MB_SR_jec_central":  getYieldFromChain(s_chain, MB_cut_jec_central, weight = weight_str),"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut_jec_central, weight = weight_str+"*"+weight_str)),\
          "yield_MB_SR_jec_up":       getYieldFromChain(s_chain, MB_cut_jec_up, weight = weight_str),"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut_jec_up, weight = weight_str+"*"+weight_str)),\
          "yield_MB_SR_jec_down":     getYieldFromChain(s_chain, MB_cut_jec_down, weight = weight_str),"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut_jec_down, weight = weight_str+"*"+weight_str)),\
                                                          }
          #print bin[srNJet][stb][htb]["signals"][mglu][mlsp]["yield_MB_SR_orig"]
          res = bin[srNJet][stb][htb]["signals"][mglu][mlsp]
          bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec"] = 0
          if not res["yield_MB_SR_jec_central"] == 0 :
            bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec_Up"] = ((res["yield_MB_SR_jec_up"]/res["yield_MB_SR_jec_central"])-1)
            bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec_Down"] = ((res["yield_MB_SR_jec_down"]/res["yield_MB_SR_jec_central"])-1)
            #sig_dict[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec"] = (abs(bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec_Down"])+abs(bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec_Up"]))/2
            bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec"] = (abs(bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec_Down"])+abs(bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec_Up"]))/2
          
          #sig_dict[srNJet][stb][htb][mglu][mlsp]["delta_ISR"] = 0
          #if not res["yield_MB_SR_orig"] == 0: 
          #  bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_ISR_Up"] = ((res["yield_MB_SR_ISR_up"]/res["yield_MB_SR_orig"])-1)
          #  bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_ISR_Down"] = ((res["yield_MB_SR_ISR_down"]/res["yield_MB_SR_orig"])-1)
          #  sig_dict[srNJet][stb][htb][mglu][mlsp]["delta_ISR"] = (abs(bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_ISR_Down"])+abs(bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_ISR_Up"]))/2

          #print "delta :" , sig_dict[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec"] #, sig_dict[srNJet][stb][htb][mglu][mlsp]["delta_ISR"] 
          expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec"] = bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec"]
          print "delta :" , expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_jec"] #, sig_dict[srNJet][stb][htb][mglu][mlsp]["delta_ISR"] 

pickle.dump(expand_dict,file('/afs/hephy.at/user/e/easilar/www/Moriond2017/sys/JEC/mglu'+str(mglu)+'Signals_JEC_expand_pkl','w'))

