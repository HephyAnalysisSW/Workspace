import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v9_Phys14V3_HT400ST200_ForTTJetsUnc import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_fromArtur import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_WPolarization import *

from makeTTPrediction import makeTTPrediction
from makeWPrediction import makeWPrediction
from Workspace.HEPHYPythonTools.user import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import * 
from math import pi, sqrt
from Workspace.RA4Analysis.signalRegions import *

ROOT.TH1F().SetDefaultSumw2()

lepSel = 'hard'

cWJets  = getChain(WJetsHTToLNu_25ns,histname='')
cTTJets = getChain(TTJets_HTLO_25ns,histname='')
cRest = getChain([singleTop_25ns, DY_25ns, TTV_25ns],histname='')#no QCD
cBkg = getChain([WJetsHTToLNu_25ns, TTJets_HTLO_25ns, singleTop_25ns, DY_25ns, TTV_25ns],histname='')#no QCD
cData = getChain([WJetsHTToLNu_25ns, TTJets_HTLO_25ns, singleTop_25ns, DY_25ns, TTV_25ns] , histname='')

#cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')#no QCD
#cData = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]] , histname='')
#cData = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],  ttJets[lepSel] , histname='')#no QCD , ##to calculate signal contamination
#cData = cBkg

signalRegions = signalRegion3fb

small = False
if small: signalRegions = smallRegion

#DEFINE LUMI AND PLOTDIR
lumi = 3.
sampleLumi = 3.
debugReweighting = False

printDir = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/Spring15/25ns/templateFit/'
pickleDir = '/data/'+username+'/Spring15/25ns/PredictionAN_'+str(lumi)+'/'
QCDpickle = '/data/bla/QCD_pkl'

if not os.path.exists(pickleDir):
  os.makedirs(pickleDir)
if not os.path.exists(printDir):
  os.makedirs(printDir)

weight_str, weight_err_str = makeWeight(lumi, sampleLumi=sampleLumi, debug=debugReweighting)

samples={'W':cWJets, 'TT':cTTJets, 'Rest':cRest, 'Bkg':cBkg, 'Data': cData}
signal = False
if signal:
  allSignals=[
            {'name':'T5q^{4} 1.2/1.0/0.8', 'sample':T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel], 'weight':weight_str, 'color':ROOT.kBlack},
            {'name':'T5q^{4} 1.5/0.8/0.1', 'sample':T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],  'weight':weight_str, 'color':ROOT.kMagenta},
            {'name':'T5q^{4} 1.0/0.8/0.7', 'sample':T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],  'weight':weight_str, 'color':ROOT.kYellow},
  ]

  for s in allSignals:
    s['chain'] = getChain(s['sample'],histname='')

prefix = 'singleLeptonic_Spring15'
#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"#&&Flag_EcalDeadCellTriggerPrimitiveFilter&&acos(cos(Jet_phi[0]-met_phi))>0.45&&acos(cos(Jet_phi[1]-met_phi))>0.45"
#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80"
#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&Jet_pt[1]>80"
#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"#&&nBJetMediumCSV30==0"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter"
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"#&&nBJetMediumCSV30==0"
filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter" #strange filter settings!!
presel += filters


btagString = 'nBJetMediumCSV30'

bjreg = (0,0)

bins = {}

for srNJet in signalRegions:
  bins[srNJet] = {}
  for stb in signalRegions[srNJet]:
    bins[srNJet][stb] ={}
    for htb in signalRegions[srNJet][stb]:
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      rd={}
      #join TT estimation results to dict
      makeTTPrediction(rd, samples, htb, stb, srNJet, presel, dPhiCut=deltaPhiCut, btagVarString = btagString, lumi=lumi, printDir=printDir)

      #join W estimation results to dict
      makeWPrediction(rd, samples, htb, stb, srNJet, presel, dPhiCut=deltaPhiCut, btagVarString = btagString, lumi=lumi, printDir=printDir)

      ##If you want to make prediction of one of the bkgs, comment out all the estimation of total Bkgs
      #estimate total background
      pred_total = rd['TT_pred'] + rd['W_pred'] + rd['Rest_truth']
      pred_total_PosPdg = 0.5*(rd['TT_pred']) + rd['W_PosPdg_pred'] + rd['Rest_PosPdg_truth']
      pred_total_NegPdg = 0.5*(rd['TT_pred']) + rd['W_NegPdg_pred'] + rd['Rest_NegPdg_truth']
      pred_total_err = sqrt(rd['TT_pred_err']**2 + rd['W_pred_err']**2 + rd['Rest_truth_err']**2)
      pred_total_PosPdg_err = sqrt((0.5*(rd['TT_pred_err']))**2 + rd['W_PosPdg_pred_err']**2 + rd['Rest_PosPdg_truth_err']**2)
      pred_total_NegPdg_err = sqrt((0.5*(rd['TT_pred_err']))**2 + rd['W_NegPdg_pred_err']**2 + rd['Rest_NegPdg_truth_err']**2)
      
      truth_total = rd['TT_truth'] + rd['W_truth'] + rd['Rest_truth']
      truth_total_PosPdg = 0.5*(rd['TT_truth']) + rd['W_PosPdg_truth'] + rd['Rest_PosPdg_truth']
      truth_total_NegPdg = 0.5*(rd['TT_truth']) + rd['W_NegPdg_truth'] + rd['Rest_NegPdg_truth']
      truth_total_err = sqrt(rd['TT_truth_err']**2 + rd['W_truth_err']**2 + rd['Rest_truth_err']**2)
      truth_total_PosPdg_err = sqrt((0.5*(rd['TT_truth_err']))**2 + rd['W_PosPdg_truth_err']**2 + rd['Rest_PosPdg_truth_err']**2)
      truth_total_NegPdg_err = sqrt((0.5*(rd['TT_truth_err']))**2 + rd['W_NegPdg_truth_err']**2 + rd['Rest_NegPdg_truth_err']**2)

      rd.update({\
                'tot_pred':pred_total,'tot_pred_err':pred_total_err,\
                'tot_PosPdg_pred':pred_total_PosPdg,'tot_PosPdg_pred_err':pred_total_PosPdg_err,\
                'tot_NegPdg_pred':pred_total_NegPdg,'tot_NegPdg_pred_err':pred_total_NegPdg_err,\
                'tot_truth':truth_total,'tot_truth_err':truth_total_err,\
                'tot_PosPdg_truth':truth_total_PosPdg,'tot_PosPdg_truth_err':truth_total_PosPdg_err,\
                'tot_NegPdg_truth':truth_total_NegPdg,'tot_NegPdg_truth_err':truth_total_NegPdg_err,\
                })

      name, cut =  nameAndCut(stb, htb, srNJet, btb=bjreg, presel=presel, btagVar = btagString)
      if signal:
        for s in allSignals:
          s['yield_NegPdg']     = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_str)
          s['yield_NegPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_err_str)
          s['FOM_NegPdg']       = getFOM(s['yield_NegPdg'],sqrt(s['yield_NegPdg_Var']),truth_total_NegPdg,truth_total_NegPdg_err) 
  
          s['yield_PosPdg']     = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_str)
          s['yield_PosPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_err_str)
          s['FOM_PosPdg']       = getFOM(s['yield_PosPdg'],sqrt(s['yield_PosPdg_Var']),truth_total_PosPdg,truth_total_PosPdg_err)

          s['yield']     = getYieldFromChain(s['chain'], cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_str)
          s['yield_Var'] = getYieldFromChain(s['chain'], cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_err_str)
          s['FOM']       = getFOM(s['yield'],sqrt(s['yield_Var']),truth_total_PosPdg,truth_total_PosPdg_err)

          rd.update({\
                      s['name']+'_yield_NegPdg':s['yield_NegPdg'],\
                      s['name']+'_yield_NegPdg_Var':s['yield_NegPdg_Var'],\
                      s['name']+'_FOM_NegPdg':s['FOM_NegPdg'],\
                      s['name']+'_yield_PosPdg':s['yield_PosPdg'],\
                      s['name']+'_yield_PosPdg_Var':s['yield_PosPdg_Var'],\
                      s['name']+'_FOM_PosPdg':s['FOM_PosPdg'],\
                      s['name']+'_yield':s['yield'],\
                      s['name']+'_yield_Var':s['yield_Var'],\
                      s['name']+'_FOM':s['FOM'],\
                    })

      bins[srNJet][stb][htb] = rd

pickle.dump(bins, file(pickleDir+prefix+'_estimationResults_pkl','w'))
print "written:" , pickleDir+prefix+'_estimationResults_pkl'
