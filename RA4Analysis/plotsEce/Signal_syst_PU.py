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
parser.add_option("--mglu", dest="mglu", default="1000", action="store", help="mglu")
(options, args) = parser.parse_args()

exec("tmp_mglu="+options.mglu)
print type(tmp_mglu)
mglu = tmp_mglu
print mglu

use_btagWeights = False
if use_btagWeights:
  weight_str      = weight_str_signal_plot+"*"+weight_0b+"*"+PU
  weight_str_Up   = weight_str_signal_plot+"*"+weight_0b+"*puReweight_true_Up"
  weight_str_Down = weight_str_signal_plot+"*"+weight_0b+"*puReweight_true_Down"
  nbtag = (0,-1)
else:
  weight_str = weight_str_signal_plot+"*"+PU
  weight_str_Up = weight_str_signal_plot+"*puReweight_true_Up"
  weight_str_Down = weight_str_signal_plot+"*puReweight_true_Down"
  nbtag = (0,0)

presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&iso_Veto"  #&&flag_crazy_jets"

signal = SMS_T5qqqqVV_TuneCUETP8M1

signalRegions = signalRegions_Moriond2017
#signalRegions = signalRegions_Moriond2017_onebyone[0]

mglu = 1900
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

expand_dict = pickle.load(file('/afs/hephy.at/user/e/easilar/www/Moriond2017/pickles/signals/mglu'+str(mglu)+'Signal_isoVetoCorrected_pkl'
))


bin = {}
for srNJet in sorted(signalRegions):
  bin[srNJet]={}
  for stb in sorted(signalRegions[srNJet]):
    bin[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      bin[srNJet][stb][htb] = {}
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      print srNJet , stb , htb      

      name_bla, MB_cut               = nameAndCut(stb, htb, srNJet, btb=nbtag, presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)

      bin[srNJet][stb][htb]["signals"] = {}
      #for mglu in signal.keys() :
      for mglu in [mglu] :
        bin[srNJet][stb][htb]["signals"][mglu] = {}
        #for mlsp in signal[mglu].keys() :
        for mlsp in [100] :
          s_chain = getChain(signal[mglu][mlsp],histname='')
          bin[srNJet][stb][htb]["signals"][mglu][mlsp] = {\
          "yield_MB_SR_orig":       getYieldFromChain(s_chain, MB_cut, weight = weight_str),"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut, weight = weight_str+"*"+weight_str)),\
          "yield_MB_SR_PU_up":     getYieldFromChain(s_chain, MB_cut, weight = weight_str_Up)  ,"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut, weight = weight_str_Up+"*"+weight_str_Up)),\
          "yield_MB_SR_PU_down":   getYieldFromChain(s_chain, MB_cut, weight = weight_str_Down),"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut, weight = weight_str_Down+"*"+weight_str_Down)),\
                                                          }
          print bin[srNJet][stb][htb]["signals"][mglu][mlsp]["yield_MB_SR_orig"]
          res = bin[srNJet][stb][htb]["signals"][mglu][mlsp]

          bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU"] = 0
          if not res["yield_MB_SR_orig"] == 0: 
            bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU_Up"] = ((res["yield_MB_SR_PU_up"]/res["yield_MB_SR_orig"])-1)
            bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU_Down"] = ((res["yield_MB_SR_PU_down"]/res["yield_MB_SR_orig"])-1)
            bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU"] = (abs(bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU_Down"])+abs(bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU_Up"]))/2

          print "delta :" , bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU"] 
          expand_dict[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU"] = bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU"]

pickle.dump(expand_dict,file('/afs/hephy.at/user/e/easilar/www/Moriond2017/sys/PU/mglu'+str(mglu)+'Signals_PUMor_pkl','w'))

