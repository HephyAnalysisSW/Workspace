# This is an attempt to rebuild the background estimation for 0b in a cleaner and faster way
# without all the overhead which kept on increasing
# Not everything is implemented yet, but the core is running nice and fast
#

import ROOT
import pickle
import os,sys
from math import pi, sqrt
#import contextlib


from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.HEPHYPythonTools.asym_float import *
from Workspace.RA4Analysis.helpers import *

from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.binnedNBTagsFit import binnedNBTagsFit
from Workspace.RA4Analysis.rCShelpers import *
from Workspace.RA4Analysis.signalRegions import *

from getTTRcs import getTTRcs
from getWRcs import getWRcs

# Import configuration
from sys import argv
if len(argv)>1:
  configFile = argv[1]
else:
  configFile = 'predictionConfig'
exec('from '+configFile+' import *')
print 'Imported configuration from '+configFile+'.py'


# Set defaults
ROOT.TH1F().SetDefaultSumw2()

weight_str, weight_err_str = makeWeight(lumi, sampleLumi=sampleLumi, reWeight=MCweight)
samples={'W':cWJets, 'TT':cTTJets, 'Rest':cRest, 'Bkg':cBkg, 'Data': cData}


if isData: dataSetString = 'data'
else: dataSetString = 'MC'
if QCDestimate: qcdstring = QCDpickle
else: qcdstring = 'not used'
if useBTagWeights: btagweightstring = 'b-tag weights used with suffix:'+btagWeightSuffix
else: btagweightstring = 'b-tag weights not used'
if unblinded: blindingstring = 'Results will be shown UNBLINDED'
elif validation: blindingstring = 'Results will be shown for validation, please check that SR are chosen accordingly'
else: blindingstring = 'We are still blinded, data yields in SR will not be shown!'
if templateBootstrap: bootstrapMessage='Using template-uncertainties obtained from bootstrapping'
else: bootstrapMessage='Not using additional template uncertainties'

print
print 'Starting prediction with', dataSetString
print blindingstring
print
print 'Signal regions:', signalRegions
print
print 'Datalumi, templatelumi, samplelumi:',lumi,templateLumi,sampleLumi
print 'W sideband:',wjetsSB
print 'b-tag multiplicity:',bjreg
print 'QCD estimation:', qcdstring
print btagweightstring
print 'Result will be saved in:', pickleDir
print 'Plots will be saved in:', printDir
print 'Templates will be saved in:', templateDir
print bootstrapMessage
print 'Preselection to be used:'
print presel
print
print 'That is all for now, see you in a few hours!'
print

fmt = '{0:15} {1:<15}'

configs = {}

configs['isData']           = isData
configs['useBTagWeights']   = useBTagWeights
configs['btagWeightSuffix'] = btagWeightSuffix
configs['weight_str']       = weight_str
configs['weight_err_str']   = weight_err_str
configs['ttjetsSB']         = ttjetsSB
configs['wjetsSB']          = wjetsSB
configs['templateDir']      = templateDir
configs['nBTagVar']         = nBTagVar
configs['templateWeights']  = templateWeights
configs['templateWeightSuffix'] = templateWeightSuffix
configs['lumi']             = lumi
configs['templateLumi']     = templateLumi
configs['loadTemplate']     = loadTemplate
configs['printDir']         = printDir
configs['dPhiStr']          = dPhiStr
configs['templateBootstrap']= templateBootstrap


zero = asym_float(0.,0.)
SBfits = {}
QCD_placeHolder = {}
for nb in [(0,0),(1,1),(2,-1)]:
  QCD_placeHolder[nb] = zero

bins = {}
for srNJet in signalRegions:
  bins[srNJet] = {}
  for stb in signalRegions[srNJet]:
    if not SBfits.has_key(stb): SBfits[stb] = {}
    bins[srNJet][stb] ={}
    for htb in signalRegions[srNJet][stb]:
      if not SBfits[stb].has_key(htb): SBfits[stb][htb] = {}
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      rd={}
      rd['deltaPhiCut'] = deltaPhiCut
      print
      print '#################################################'
      print '## Prediction for SR',str(srNJet),str(stb),str(htb)
      print '## Using a dPhi cut value of',str(deltaPhiCut)
      print '#################################################'
      print

      print 'Performing b-tag multiplicity fit in the control region'

      MB_name,    MB_cut        = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = nBTagVar)
      MB_name,    MB_cut_0b     = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = nBTagVar)
      MB_name_MC, MB_cut_MC     = nameAndCut(stb, htb, srNJet, btb=None, presel=presel_MC, btagVar = nBTagVar)
      MB_name_MC, MB_cut_0b_MC  = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel_MC, btagVar = nBTagVar)

      # Copy the important parts of the QCD estimate for the MB CR
      QCD_dict = {}
      if QCDestimate:
        QCD_dictEnt = QCDestimate[srNJet][stb][htb]
        for nb in [(0,0),(1,1),(2,-1)]:
          if QCDup: QCD_dict[nb] = asym_float(QCD_dictEnt[nb][deltaPhiCut]['NQCDpred'] + QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'], QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'])
          elif QCDdown:
            if (QCD_dictEnt[nb][deltaPhiCut]['NQCDpred']-QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'])>0:
              QCD_dict[nb] = asym_float(QCD_dictEnt[nb][deltaPhiCut]['NQCDpred'] - QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'], QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'])
            else: 
              QCD_dict[nb] = asym_float(0., QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'])
          else: 
            QCD_dict[nb] = asym_float(QCD_dictEnt[nb][deltaPhiCut]['NQCDpred'], QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'])
      else:
        QCD_dict = QCD_placeHolder

      # define cuts for b-tag multi fit, open b-tag requirement
      MB_CR_name    = MB_name + '_dPhi'+str(deltaPhiCut)
      MB_CR_cut     = MB_cut + "&&"+dPhiStr+"<"+str(deltaPhiCut)
      MB_CR_cut_MC  = MB_cut_MC + "&&"+dPhiStr+"<"+str(deltaPhiCut)
      
      # make fit in MB CR, suppress stdout if not needed
      fit_MB_CR = {}
      old_stdout = sys.stdout
      sys.stdout = open(os.devnull, "w")
      try:
        binnedNBTagsFit(MB_CR_cut, MB_CR_cut_MC, MB_CR_name, samples, configs, QCD_dict=QCD_dict, res=fit_MB_CR)
      finally:
        sys.stdout.close()
        sys.stdout = old_stdout
      
      print 'Finished the b-tag fit'

      rd['fit_MB_CR'] = fit_MB_CR

      # Copy the important parts of the QCD estimate for the TTJets SB      
      if QCDestimate:
        QCD_dictEnt = QCDestimate[ttjetsSB][stb][htb]
        for nb in [(0,0),(1,1),(2,-1)]:
          if QCDup: QCD_dict[nb] = asym_float(QCD_dictEnt[nb][deltaPhiCut]['NQCDpred'] + QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'], QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'])
          elif QCDdown:
            if (QCD_dictEnt[nb][deltaPhiCut]['NQCDpred']-QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'])>0:
              QCD_dict[nb] = asym_float(QCD_dictEnt[nb][deltaPhiCut]['NQCDpred'] - QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'], QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'])
            else:
              QCD_dict[nb] = asym_float(0., QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'])
          else:
            QCD_dict[nb] = asym_float(QCD_dictEnt[nb][deltaPhiCut]['NQCDpred'], QCD_dictEnt[nb][deltaPhiCut]['NQCDpred_err'])
      else:
        QCD_dict = QCD_placeHolder
      print
      print 'Getting Rcs for W+jets'
      WRcs  = getWRcs(samples, htb, stb, srNJet, presel, presel_MC, configs, deltaPhiCut=deltaPhiCut, SBfits=SBfits)
      print
      print 'Getting Rcs for tt+jets'
      TTRcs = getTTRcs(samples, htb, stb, srNJet, presel, presel_MC, configs, deltaPhiCut=deltaPhiCut, QCD_dict=QCD_dict)
      
      if templateBootstrap:
        TTBootstrap       = asym_float(1.,templateBootstrap['TTJets'][srNJet][stb][htb])
        WBootstrap_PosPdg = asym_float(1.,templateBootstrap['WJets_PosPdg'][srNJet][stb][htb])
        WBootstrap_NegPdg = asym_float(1.,templateBootstrap['WJets_NegPdg'][srNJet][stb][htb])
      else:
        TTBootstrap       = asym_float(1.,0.)
        WBootstrap_PosPdg = asym_float(1.,0.)
        WBootstrap_NegPdg = asym_float(1.,0.)
      
      # Key part, getting the predicted yields with Rcs * N_CR(fit)
      W_pred  = WRcs['W_Rcs_pred'] * (fit_MB_CR['W_PosPdg']*WBootstrap_PosPdg + fit_MB_CR['W_NegPdg']*WBootstrap_NegPdg)
      TT_pred = TTRcs['TT_Rcs_pred'] * fit_MB_CR['TT_AllPdg'] * TTBootstrap
      
      # get missing MC truth yields, save results
      MC_SR_cut = MB_cut_0b + "&&"+dPhiStr+">="+str(deltaPhiCut)
      if useBTagWeights:
        MB_SR_cut_MC  = MB_cut_MC + "&&"+dPhiStr+">="+str(deltaPhiCut)
        weight_str_0b = weight_str + '*weightBTag0'+btagWeightSuffix
      else:
        MB_SR_cut_MC  = MB_cut_0b_MC + "&&"+dPhiStr+">="+str(deltaPhiCut)
        weight_str_0b = weight_str
        
      Rest_truth  = asym_float(*getYieldFromChain(cRest, MB_SR_cut_MC, weight_str_0b, returnError=True))
      total_truth = asym_float(getYieldFromChain(cData, MC_SR_cut, '(1)'), forcePoisson=True)
      total_pred  = W_pred + TT_pred + Rest_truth
      

      print
      print 'Prediction result'
      print '-----------------'
      print fmt.format('W+jets',W_pred.round())
      print fmt.format('tt+jets',TT_pred.round())
      print fmt.format('Rest',Rest_truth.round())
      print fmt.format('total',total_pred.round())
      print
      print fmt.format('observed',total_truth.round())
      #print fmt.format('Rest',round(rest,2))
      print
      
      rd['W_pred']      = W_pred
      rd['TT_pred']     = TT_pred
      rd['Rest_truth']  = Rest_truth
      rd['tot_pred']    = total_pred
      rd['tot_truth']   = total_truth
      
      bins[srNJet][stb][htb] = rd


pickle.dump(bins, file(pickleDir+prefix+'_estimationResults_pkl','w'))
print "written:" , pickleDir+prefix+'_estimationResults_pkl'

