import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *

signalRegions = signalRegions2016

dilepD = {}

for injb,srNJet in enumerate(sorted(signalRegions)):
  dilepD[srNJet] = {}
  for stb in sorted(signalRegions[srNJet]):
    dilepD[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):

      print
      print '#############################################'
      print '## * njet:',srNJet
      print '## * LT:  ',stb
      print '## * HT:  ',htb
      print '#############################################'
      print      
      
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      save_name, cut_DY_SR = nameAndCut(stb, htb, srNJet, btb=(0,0), presel="deltaPhi_Wl>"+str(deltaPhiCut), btagVar = "nBJetMediumCSV30")

      dilep = pickle.load(file('/data/easilar/Results2016/ICHEP/SYS/V1//unc_with_SRAll_'+save_name+'_pkl'))

      constant_err = (abs(dilep[srNJet][stb][htb]["delta_constant_Up"])+abs(dilep[srNJet][stb][htb]["delta_constant_Down"]))/2
      slope_err = (abs(dilep[srNJet][stb][htb]["delta_slope_Up"])+abs(dilep[srNJet][stb][htb]["delta_slope_Down"]))/2
      
      print 'const',constant_err
      print 'slope',slope_err
      
      errorsForTotal = [constant_err , slope_err]
      totalSyst_noKappa = 0
      for err in errorsForTotal: totalSyst_noKappa += err**2
      totalSyst_noKappa = sqrt(totalSyst_noKappa)

      print 'total',totalSyst_noKappa
      
      dilepD[srNJet][stb][htb] = totalSyst_noKappa
