import ROOT
import pickle
from array import array
import operator
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2_postProcessed import *
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
sig_dict = pickle.load(file('/data/easilar/Results2016/ICHEP/signal_Spring16/mglu'+str(mglu)+'Signals_12p88_pkl')) 
#print sig_dict[(5,5)][(250, 350)][(750, -1)]["signals"][mglu].keys()
weight_str    = '*'.join([trigger_scale,lepton_Scale_signal,weight_0b,PU,reweight])
weight_str_Up = '*'.join([trigger_scale,lepton_Scale_signal,weight_0b,"puReweight_true_Up",reweight])
weight_str_Down = '*'.join([trigger_scale,lepton_Scale_signal,weight_0b,"puReweight_true_Down",reweight])

btagString = "nBJetMediumCSV30"

presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&flag_crazy_jets"

signal = SMS_T5qqqqVV_TuneCUETP8M1

signalRegions = signalRegions2016

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


bin = {}
for srNJet in sorted(signalRegions):
  bin[srNJet]={}
  for stb in sorted(signalRegions[srNJet]):
    bin[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      bin[srNJet][stb][htb] = {}
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      print srNJet , stb , htb      

      name_bla, MB_cut               = nameAndCut(stb, htb, srNJet, btb=(0,-1), presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)

      bin[srNJet][stb][htb]["signals"] = {}
      #for mglu in signal.keys() :
      for mglu in [mglu] :
        bin[srNJet][stb][htb]["signals"][mglu] = {}
        for mlsp in signal[mglu].keys() :
        #for mlsp in [100] :
          s_chain = getChain(signal[mglu][mlsp],histname='')
          bin[srNJet][stb][htb]["signals"][mglu][mlsp] = {\
          "yield_MB_SR_orig":       getYieldFromChain(s_chain, MB_cut, weight = weight_str),"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut, weight = weight_str+"*"+weight_str)),\
          "yield_MB_SR_PU_up":     getYieldFromChain(s_chain, MB_cut, weight = weight_str_Up)  ,"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut, weight = weight_str_Up+"*"+weight_str_Up)),\
          "yield_MB_SR_PU_down":   getYieldFromChain(s_chain, MB_cut, weight = weight_str_Down),"err_MB_SR":sqrt(getYieldFromChain(s_chain, MB_cut, weight = weight_str_Down+"*"+weight_str_Down)),\
                                                          }
          print bin[srNJet][stb][htb]["signals"][mglu][mlsp]["yield_MB_SR_orig"]
          res = bin[srNJet][stb][htb]["signals"][mglu][mlsp]

          sig_dict[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU"] = 0
          if not res["yield_MB_SR_orig"] == 0: 
            bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU_Up"] = ((res["yield_MB_SR_PU_up"]/res["yield_MB_SR_orig"])-1)
            bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU_Down"] = ((res["yield_MB_SR_PU_down"]/res["yield_MB_SR_orig"])-1)
            sig_dict[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU"] = (abs(bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU_Down"])+abs(bin[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU_Up"]))/2

          print "delta :" , sig_dict[srNJet][stb][htb]["signals"][mglu][mlsp]["delta_PU"] 

pickle.dump(sig_dict,file('/data/easilar/Results2016/ICHEP/signal_Spring16/mglu'+str(mglu)+'Signals_PUuncUpdated_12p88_pkl','w'))

