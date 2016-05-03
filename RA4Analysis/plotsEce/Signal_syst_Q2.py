import ROOT
import pickle
from array import array
import operator
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.signalRegions import *
from Workspace.HEPHYPythonTools.user import username
from math import sqrt, pi
ROOT.TH1F().SetDefaultSumw2()


#sig_dict = pickle.load(file('/data/dspitzbart/Results2016/signal_unc_pkl'))
sig_dict = pickle.load(file('/data/easilar/Spring15/25ns/allSignals_2p25_syst_pkl'))

weight_str = "((weight*2.25)/3)"+'*weightBTag0_SF*reweightLeptonFastSimSF'
#weight_str = "((weight*2.25)/3)"
weight_str_list = [] 
for weight_idx in [1,2,3,4,6,8] : 
  weight_str_list.append(weight_str+"*LHEweight_wgt["+str(weight_idx)+"]")

btagString = "nBJetMediumCSV30"

presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80"

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

bla , MC_tot_cut = nameAndCut((0,-1), (0,-1), (0,-1), btb=(0,-1), presel="(1)" , btagVar = btagString)

all_signals = {}
for sig in allSignals:
  print sig
  exec("signal="+sig)
  for mglu in signal.keys() :
    all_signals[mglu] = {}
    for mlsp in signal[mglu].keys() :
      all_signals[mglu][mlsp] = {}
      s_chain = getChain(signal[mglu][mlsp],histname='')
      full_yield = getYieldFromChain(s_chain, MC_tot_cut, weight = weight_str+"*LHEweight_original")
      #print full_yield
      SR_sum_yield={}
      for weight in weight_str_list:
        SR_sum_yield[weight] = getYieldFromChain(s_chain, MC_tot_cut, weight = weight) 
        all_signals[mglu][mlsp]["scale_"+weight] = full_yield / SR_sum_yield[weight]
        #print "scale "  , all_signals[mglu][mlsp]["scale_"+weight]

print "this will be much slower ... :( "

for srNJet in sorted(signalRegions):
  for stb in sorted(signalRegions[srNJet]):
    for htb in sorted(signalRegions[srNJet][stb]):
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      print srNJet , stb , htb      
      for sig in allSignals:
        exec("signal="+sig)
        bla , MB_cut_SR = nameAndCut(stb, htb, srNJet ,btb=(0,-1), presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut) , btagVar = btagString)
        for mglu in signal.keys() :
          for mlsp in signal[mglu].keys() :
            s_chain = getChain(signal[mglu][mlsp],histname='')
            original_yield = getYieldFromChain(s_chain, MB_cut_SR, weight = weight_str+"*LHEweight_original")
            delta_list = []
            delta_max = 0
            delta_min = 0
            if not original_yield ==0:
              for weight in weight_str_list: 
                scl_yield = getYieldFromChain(s_chain, MB_cut_SR, weight = weight)*all_signals[mglu][mlsp]["scale_"+weight]
                delta_list.append((scl_yield-original_yield)/original_yield)
              delta_max = max(delta_list)
              delta_min = min(delta_list) 
              #print delta_max , delta_min
            sig_dict[srNJet][stb][htb][mglu][mlsp]["delta_Q2"] = (abs(delta_max)+abs(delta_min))/2
            #print sig_dict[srNJet][stb][htb][mglu][mlsp]["delta_Q2"]
pickle.dump(sig_dict,file('/data/easilar/Spring15/25ns/allSignals_2p25_syst_extended_Q2_fixed_pkl','w'))
