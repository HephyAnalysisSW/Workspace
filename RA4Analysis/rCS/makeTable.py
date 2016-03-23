import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from rCShelpers import *
import math
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *

from predictionConfig import *

useWcorrection = False
useTTcorrection = False
signal = False

withSystematics = True

prefix = 'singleLeptonic_Spring15_'
path = '/data/'+username+'/Results2016/Prediction_SFtemplates_fullSR_lep_data_2p3_BACKUP_APPROVAL/'
#path = '/data/'+username+'/Results2016/Prediction_SFtemplates_fullSR_lep_MC_SFnoPUreweight_2p25/'

#path = '/data/'+username+'/Results2016/Prediction_SFtemplates_validation_lep_data_2p3/'
#path = '/data/'+username+'/Results2016/Prediction_SFtemplates_fullSR_lep_data_2p1/'
#path = '/data/'+username+'/Results2015/Prediction_SFTemplate_MC_fullSR_lep_3.0/' 
#path2 = '/data/'+username+'/Results2015/Prediction_bweightTemplate_MC_reducedSR_lep_3.0/'

res = pickle.load(file(path+'resultsFinal_withSystematics_pkl'))
sys = res

#sig = pickle.load(file('/data/easilar/Spring15/25ns/allSignals_2p3_v2_pkl'))
#sig = pickle.load(file('/data/dspitzbart/Results2016/signal_unc_pkl'))
sig = pickle.load(file('/data/easilar/Spring15/25ns/allSignals_2p3_allSyst_pkl'))

qcdData = pickle.load(file('/data/dspitzbart/Results2016/QCDEstimation/20160212_QCDestimation_data2p25fb_pkl'))
qcdMC   = pickle.load(file('/data/dspitzbart/Results2016/QCDEstimation/20160212_QCDestimation_MC2p25fb_pkl'))

#mc = pickle.load(file(path+'resultsFinal_withSystematics_pkl'))

#res2 = pickle.load(file(path2+prefix+'_estimationResults_pkl'))

if useTTcorrection: kcs = pickle.load(file('/data/dspitzbart/Spring15/25ns/rCS_0b_3.0/correction_pkl'))
if useWcorrection:
  Wrcs_corr_PosPdg = pickle.load(file('/data/dspitzbart/Spring15/25ns/rCS_0b_3.0/correction_Wrcs_PosPdg_pkl'))
  Wrcs_corr_NegPdg = pickle.load(file('/data/dspitzbart/Spring15/25ns/rCS_0b_3.0/correction_Wrcs_NegPdg_pkl'))
  Wrcs_corr =        pickle.load(file('/data/dspitzbart/Spring15/25ns/rCS_0b_3.0/correction_Wrcs_pkl'))

#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80"

btagString = 'nBJetMediumCSV30'

lumi = 3.
weight_str, weight_err_str = makeWeight(lumi, sampleLumi=3., reWeight=MCweight)
lepSel = 'hard'

if signal:
  allSignals=[
            {'name':'T5q^{4} 1.2/1.0/0.8', 'sample':T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel], 'weight':weight_str, 'color':ROOT.kBlack},
            {'name':'T5q^{4} 1.5/0.8/0.1', 'sample':T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],  'weight':weight_str, 'color':ROOT.kMagenta},
            {'name':'T5q^{4} 1.0/0.8/0.7', 'sample':T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],  'weight':weight_str, 'color':ROOT.kYellow},
  ]

  for s in allSignals:
    s['chain'] = getChain(s['sample'],histname='')


#signalRegions = validationRegion
signalRegions = signalRegion3fb

#signalRegions = smallRegion
#signalRegions = {(5, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}}}}

#streg = [[(250, 350), 1.], [(350, 450), 1.], [(450,-1), 1.]]
#htreg = [(500,750),(750,1000),(1000,1250),(1250,-1)]
#njreg = [(5,5),(6,7),(8,-1)]
#nSTbins = len(streg)
#nJetBins = len(njreg)

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

#scaleFactor = 0.8
scaleFactor = 1

# signal regions table

print "signal regions table"
print
print '\\begin{table}[ht]\\begin{center}\\begin{tabular}{|c|c|c|c|}\\hline'
print ' \\njet     & \LT & \HT     & $\Delta\Phi$ \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & ' + str(signalRegions[srNJet][stb][htb]['deltaPhi']) +'\\\\'
      if htb[1] == -1 : print '\\cline{2-4}'
print '\\hline\end{tabular}\end{center}\caption{Signal regions for the 0b search}\label{tab:0b_signalRegions}\end{table}'



#closure table
print "Closure table"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \LT & \HT     &\multicolumn{6}{c|}{$tt+$Jets}&\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{3}{c|}{Other EW bkg.}&\multicolumn{6}{c|}{total bkg.}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(res[srNJet][stb][htb]['TT_pred_final'], res[srNJet][stb][htb]['TT_pred_final_tot_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['TT_truth'], res[srNJet][stb][htb]['TT_truth_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['W_pred_final'], res[srNJet][stb][htb]['W_pred_final_tot_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['W_truth'], res[srNJet][stb][htb]['W_truth_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['Rest_truth'], res[srNJet][stb][htb]['Rest_truth_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['tot_pred_final'], res[srNJet][stb][htb]['tot_pred_final_tot_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['tot_truth'], res[srNJet][stb][htb]['tot_truth_err']) +'\\\\'
      if htb[1] == -1 : print '\\cline{2-24}'
print '\\hline\end{tabular}}\end{center}\caption{Closure table for the background in the 0-tag regions, 2.3fb$^{-1}$}\label{tab:0b_totalClosure}\end{table}'


#closure table
print "Closure table"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \LT & \HT     &\multicolumn{6}{c|}{$tt+$Jets}&\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{3}{c|}{Other EW bkg.}&\multicolumn{6}{c|}{total bkg.}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(res[srNJet][stb][htb]['TT_pred'], res[srNJet][stb][htb]['TT_pred_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['TT_truth'], res[srNJet][stb][htb]['TT_truth_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['W_pred'], res[srNJet][stb][htb]['W_pred_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['W_truth'], res[srNJet][stb][htb]['W_truth_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['Rest_truth'], res[srNJet][stb][htb]['Rest_truth_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['tot_pred'], res[srNJet][stb][htb]['tot_pred_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['tot_truth'], res[srNJet][stb][htb]['tot_truth_err']) +'\\\\'
      if htb[1] == -1 : print '\\cline{2-24}'
print '\\hline\end{tabular}}\end{center}\caption{Closure table for the background in the 0-tag regions without using kappa factors, 2.3fb$^{-1}$}\label{tab:0b_totalClosure}\end{table}'



#QCD closure table
print "Closure table"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|}\\hline'
print ' \\njet     & \LT & \HT     & \multicolumn{6}{c|}{QCD multijets} \\\%\hline'
print ' & $[$GeV$]$ & $[$GeV$]$ & \multicolumn{3}{c}{prediction} & \multicolumn{3}{c|}{simulation} \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      dPhi = signalRegions[srNJet][stb][htb]['deltaPhi']
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(qcdMC[srNJet][stb][htb][(0,0)][dPhi]['NQCDpred'], qcdMC[srNJet][stb][htb][(0,0)][dPhi]['NQCDpred_err'])\
           +' & '+getNumString(qcdMC[srNJet][stb][htb][(0,0)][dPhi]['NQCDSelMC'], qcdMC[srNJet][stb][htb][(0,0)][dPhi]['NQCDSelMC_err']) +'\\\\'
      if htb[1] == -1 : print '\\cline{2-9}'
print '\\hline\end{tabular}}\end{center}\caption{Closure table for the QCD background in the 0-tag regions, 2.25fb$^{-1}$}\label{tab:QCD0b_totalClosure}\end{table}'




#Rcs table for ttbar, makes only sense for MC

print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \LT & \HT & \multirow{2}{*}{bin name} & \multicolumn{3}{c|}{\multirow{2}{*}{$R_{CS}(\\textrm{4-5j, 1b})\cdot\kappa_{b}^{MC}$}} & \multicolumn{3}{c|}{\multirow{2}{*}{$R_{CS}(\\textrm{SR, 0b})$}} & \multicolumn{3}{c|}{$\kappa_{t\\bar{t}}$} & \multicolumn{3}{c|}{$\kappa_{b}^{MC}$}\\\%\hline'
print ' & $[$GeV$]$ & $[$GeV$]$ & & & & & & & & \multicolumn{3}{c|}{SR/SB} & \multicolumn{3}{c|}{0b/1b} \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & $'+signalRegions[srNJet][stb][htb]['tex'] +'$'
      print ' & '+getNumString(res[srNJet][stb][htb]['rCS_crLowNJet_1b_kappa']['rCS'],  res[srNJet][stb][htb]['rCS_crLowNJet_1b_kappa']['rCSE_sim'],4)\
           +' & '+getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyTT']['rCS'], res[srNJet][stb][htb]['rCS_srNJet_0b_onlyTT']['rCSE_sim'],4)\
           + '& '+getNumString(res[srNJet][stb][htb]['TT_kappa'], res[srNJet][stb][htb]['TT_kappa_err'])\
           + '& '+getNumString(res[srNJet][stb][htb]['TT_rCS_fits_MC']['k_0b/1b_btag'], res[srNJet][stb][htb]['TT_rCS_fits_MC']['k_0b/1b_btag_err']) + '\\\\'
      if htb[1] == -1 : print '\\cline{2-16}'
print '\\hline\end{tabular}}\end{center}\caption{Rcs table for $t\\bar{t}$+jets and the corresponding $\\kappa_{t\\bar{t}}$ value from simulation, 2.3fb$^{-1}$}\label{tab:0b_rcs_tt}\end{table}'


#Rcs table for W, makes only sense for MC

print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \LT & \HT & \multirow{2}{*}{bin name} & \multicolumn{3}{c|}{\multirow{2}{*}{$R_{CS}(\\textrm{3-4j,0b,$\\mu$,corr})$}} & \multicolumn{3}{c|}{\multirow{2}{*}{$R_{CS}(\\textrm{SR,0b})$}}&\multicolumn{3}{c|}{$\kappa_{W}$}\\\%\hline'
print ' & $[$GeV$]$ & $[$GeV$]$ & & & & & & & & \multicolumn{3}{c|}{SR/SB} \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & $'+signalRegions[srNJet][stb][htb]['tex'] +'$'
      print ' & '+getNumString(res[srNJet][stb][htb]['rCS_W_crNJet_0b_corr'],   sqrt(res[srNJet][stb][htb]['rCS_Var_W_crNJet_0b_corr']),4)\
           +' & '+getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW']['rCS'],  res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW']['rCSE_sim'],4)\
           + '& '+getNumString(res[srNJet][stb][htb]['W_kappa'], res[srNJet][stb][htb]['W_kappa_err']) + '\\\\'
      if htb[1] == -1 : print '\\cline{2-13}'
print '\\hline\end{tabular}}\end{center}\caption{Rcs table for W+jets and the corresponding $\\kappa_W$ value from simulation, 2.3fb$^{-1}$}\label{tab:0b_rcs_W}\end{table}'


#Rcs table for for sidebands data vs MC
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \LT & \HT & \multicolumn{6}{c|}{3-4j, 0b} & \multicolumn{6}{c|}{4-5j, 1b}\\\%\hline'
print ' & $[$GeV$]$ & $[$GeV$]$ & \multicolumn{3}{c}{data} & \multicolumn{3}{c|}{simulation} & \multicolumn{3}{c}{data} & \multicolumn{3}{c|}{simulation} \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(res[srNJet][stb][htb]['rCS_W_crNJet_0b_corr'],   sqrt(res[srNJet][stb][htb]['rCS_Var_W_crNJet_0b_corr']), 4)\
           +' & '+getNumString(res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_mu']['rCS'], res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_mu']['rCSE_sim'], 4)\
           +' & '+getNumString(res[srNJet][stb][htb]['rCS_crLowNJet_1b']['rCS'], res[srNJet][stb][htb]['rCS_crLowNJet_1b']['rCSE_pred'], 4)\
           + '& '+getNumString(res[srNJet][stb][htb]['rCS_crLowNJet_1b_onlyTT']['rCS'], res[srNJet][stb][htb]['rCS_crLowNJet_1b_onlyTT']['rCSE_sim'], 4) + '\\\\'
      if htb[1] == -1 : print '\\cline{2-15}'
print '\\hline\end{tabular}}\end{center}\caption{Rcs table for sidebands, comparing data with simulation, 2.3fb$^{-1}$}\label{tab:0b_rcs_W}\end{table}'


#Rcs table for for sidebands data vs MC
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|}\\hline'
print ' \\njet     & \LT & \HT & \multicolumn{6}{c|}{\Rcs} \\\%\hline'
print ' & $[$GeV$]$ & $[$GeV$]$ & \multicolumn{3}{c}{+ charge} & \multicolumn{3}{c|}{- charge} \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(res[srNJet][stb][htb]['rCS_W_NegPdg_crNJet_0b_truth']['rCS'], res[srNJet][stb][htb]['rCS_W_NegPdg_crNJet_0b_truth']['rCSE_sim'], 4)\
           +' & '+getNumString(res[srNJet][stb][htb]['rCS_W_PosPdg_crNJet_0b_truth']['rCS'], res[srNJet][stb][htb]['rCS_W_PosPdg_crNJet_0b_truth']['rCSE_sim'], 4) + '\\\\'
      if htb[1] == -1 : print '\\cline{2-9}'
print '\\hline\end{tabular}}\end{center}\caption{Rcs table for the sidebands split in +/- charged leptons, 2.3fb$^{-1}$}\label{tab:0b_rcs_W_charge}\end{table}'



#result table for PAS
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|l|rrr|rrr|rrr|rrr|rrr|}\\hline'

print ' \multirow{2}{*}{\\njet}     & \LT & \HT     & \multirow{2}{*}{Bin name} & \multicolumn{9}{c|}{expected T5q$^4$WW $m_{gl}$/$m_{\\ninozero}$ $[$TeV$]$} & \multicolumn{3}{c|}{\multirow{2}{*}{predicted}} & \multicolumn{3}{c|}{\multirow{2}{*}{observed}} \\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$ &  & \multicolumn{3}{c}{1.0/0.7} & \multicolumn{3}{c}{1.2/0.8} & \multicolumn{3}{c|}{1.5/0.1} & \multicolumn{3}{c|}{} & \multicolumn{3}{c|}{} \\\\\hline'


secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & $'+signalRegions[srNJet][stb][htb]['tex'] +'$'
      print ' & '+getNumString(sig[srNJet][stb][htb]['signals'][1000][700]['yield_MB_SR'], sig[srNJet][stb][htb]['signals'][1000][700]['stat_err_MB_SR'])\
           +' & '+getNumString(sig[srNJet][stb][htb]['signals'][1200][800]['yield_MB_SR'], sig[srNJet][stb][htb]['signals'][1200][800]['stat_err_MB_SR'])\
           +' & '+getNumString(sig[srNJet][stb][htb]['signals'][1500][100]['yield_MB_SR'], sig[srNJet][stb][htb]['signals'][1500][100]['stat_err_MB_SR'])\
           +' & '+getNumString(res[srNJet][stb][htb]['tot_pred_final'], res[srNJet][stb][htb]['tot_pred_final_tot_err'])
      if unblinded or validation:
        print ' & \multicolumn{3}{c|}{'+str(int(res[srNJet][stb][htb]['y_srNJet_0b_highDPhi']))+'} \\\\'
      else:
        print ' & \multicolumn{3}{c|}{blinded} \\\\'
      if htb[1] == -1 : print '\\cline{2-19}'
print '\\hline\end{tabular}}\end{center}\caption{Results table of the 0-tag regions, 2.3fb$^{-1}$}\label{tab:0b_results}\end{table}'



#results table
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \LT & \HT     & \multicolumn{3}{c|}{\multirow{2}{*}{simulated}} & \multicolumn{9}{c|}{expected T5q$^4$WW $m_{gl}$/$m_{\\ninozero}$ $[$TeV$]$} & \multicolumn{3}{c|}{\multirow{2}{*}{predicted}} & \multicolumn{3}{c|}{\multirow{2}{*}{observed}} \\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$ & \multicolumn{3}{c|}{} & \multicolumn{3}{c}{1.0/0.7} & \multicolumn{3}{c}{1.2/0.8} & \multicolumn{3}{c|}{1.5/0.1} & \multicolumn{3}{c|}{} & \multicolumn{3}{c|}{} \\\\\hline'

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(res[srNJet][stb][htb]['tot_truth'], res[srNJet][stb][htb]['tot_truth_err'])\
           +' & '+getNumString(sig[srNJet][stb][htb]['signals'][1000][700]['yield_MB_SR'], sig[srNJet][stb][htb]['signals'][1000][700]['stat_err_MB_SR'])\
           +' & '+getNumString(sig[srNJet][stb][htb]['signals'][1200][800]['yield_MB_SR'], sig[srNJet][stb][htb]['signals'][1200][800]['stat_err_MB_SR'])\
           +' & '+getNumString(sig[srNJet][stb][htb]['signals'][1500][100]['yield_MB_SR'], sig[srNJet][stb][htb]['signals'][1500][100]['stat_err_MB_SR'])\
           +' & '+getNumString(res[srNJet][stb][htb]['tot_pred_final'], res[srNJet][stb][htb]['tot_pred_final_tot_err'])
      if unblinded or validation:
        print ' & \multicolumn{3}{c|}{'+str(int(res[srNJet][stb][htb]['y_srNJet_0b_highDPhi']))+'} \\\\'
      else:
        print ' & \multicolumn{3}{c|}{blinded} \\\\'
      if htb[1] == -1 : print '\\cline{2-21}'
print '\\hline\end{tabular}}\end{center}\caption{Results table of the 0-tag regions, 2.3fb$^{-1}$}\label{tab:0b_results}\end{table}'

# W closure table
#res = pickle.load(file(path+prefix+'_estimationResults_pkl_updated'))
#multiplier = {(5,5):2, (6,7):3, (8,-1):4}
#print
#print 'W closure table'
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
#print ' \\njet & \ST & \HT &\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{6}{c|}{$W-$ Jets}&\multicolumn{6}{c|}{$W$ Jets}\\\%\hline'
#print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'
#secondLine = False
#for srNJet in sorted(signalRegions):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      if not first: print '&'
#      first = False
#
#      print '&$'+varBin(htb)+'$'
#      print ' & '+getNumString(res[srNJet][stb][htb]['W_NegPdg_pred'], res[srNJet][stb][htb]['W_NegPdg_pred_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['W_NegPdg_truth']*scaleFactor, res[srNJet][stb][htb]['W_NegPdg_truth_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['W_PosPdg_pred'], res[srNJet][stb][htb]['W_PosPdg_pred_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['W_PosPdg_truth']*scaleFactor, res[srNJet][stb][htb]['W_PosPdg_truth_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['W_pred'],        res[srNJet][stb][htb]['W_pred_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['W_truth']*scaleFactor,        res[srNJet][stb][htb]['W_truth_err']) +'\\\\'
#      if htb[1] == -1 : print '\\cline{2-21}'
#print '\\hline\end{tabular}}\end{center}\caption{EFGH}\label{tab:0b_rcscorr_Wbkg}\end{table}'

## W closure table with systematics
##res = pickle.load(file(path+prefix+'_estimationResults_pkl_updated'))
##multiplier = {(5,5):2, (6,7):3, (8,-1):4}
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrrrr|rrr|rrrrr|rrr|rrrrr|rrr|}\\hline'
#print ' \\njet & \ST & \HT &\multicolumn{8}{c|}{$W+$ Jets}&\multicolumn{8}{c|}{$W-$ Jets}&\multicolumn{8}{c|}{$W$ Jets}\\\%\hline'
#print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{5}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{5}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{5}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'
#secondLine = False
#for srNJet in sorted(signalRegions):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      if not first: print '&'
#      first = False
#
#      print '&$'+varBin(htb)+'$'
#      print ' & '+getNumStringWithSyst(res[srNJet][stb][htb]['W_NegPdg_pred'], res[srNJet][stb][htb]['W_pred_errs_NegPdg']['syst'],res[srNJet][stb][htb]['W_pred_errs_NegPdg']['stat'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['W_NegPdg_truth'], res[srNJet][stb][htb]['W_NegPdg_truth_err'])\
#           +' & '+getNumStringWithSyst(res[srNJet][stb][htb]['W_PosPdg_pred'], res[srNJet][stb][htb]['W_pred_errs_PosPdg']['syst'], res[srNJet][stb][htb]['W_pred_errs_PosPdg']['stat'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['W_PosPdg_truth'], res[srNJet][stb][htb]['W_PosPdg_truth_err'])\
#           +' & '+getNumStringWithSyst(res[srNJet][stb][htb]['W_pred'], res[srNJet][stb][htb]['W_pred_errs']['syst'], res[srNJet][stb][htb]['W_pred_errs']['stat'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['W_truth'],        res[srNJet][stb][htb]['W_truth_err']) +'\\\\'
#      if htb[1] == -1 : print '\\cline{2-27}'
#print '\\hline\end{tabular}}\end{center}\caption{EFGH}\label{tab:0b_rcscorr_Wbkg}\end{table}'



print "Results"
print
print '\\begin{table}[ht]\\begin{center}\\begin{tabular}{|c|c|c|rrr|rrr|rrr|}\\hline'
print ' \\njet & \LT & \HT     &\multicolumn{3}{c|}{$\kappa_{b}^{MC}$} &\multicolumn{3}{c|}{$\kappa_{t \\bar{t}}$} &\multicolumn{3}{c|}{$\kappa_{W}$}\\\[6pt] '
print ' & $[$GeV$]$ & $[$GeV$]$ & \multicolumn{3}{c|}{ $\\frac{R_{CS}^{SB}(0b,t\\bar{t})}{R_{CS}^{SB}(1b,\\textrm{EWK})}$ } & \multicolumn{3}{c|}{$R_{CS}^{MB}/R_{CS}^{SB}$} & \multicolumn{3}{c|}{$R_{CS}^{MB}/R_{CS}^{SB}$}\\\[7pt] \\hline '
secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(res[srNJet][stb][htb]['TT_rCS_fits_MC']['k_0b/1b_btag'], res[srNJet][stb][htb]['TT_rCS_fits_MC']['k_0b/1b_btag_err'])\
           + '& '+getNumString(res[srNJet][stb][htb]['TT_kappa'], res[srNJet][stb][htb]['TT_kappa_err'])\
           + '& '+getNumString(res[srNJet][stb][htb]['W_kappa'], res[srNJet][stb][htb]['W_kappa_err']) +'\\\\ '
    if htb[1] == -1 : print '\\cline{2-12}'
print '\\hline\end{tabular}\end{center}\caption{Different correction factors for Monte Carlo based corrections, with their statistical errors. $\kappa_b$ corrects for the difference of $R_{CS}$ in the 1b sideband (SB) to the 0b mainbands (MB), while $\kappa_{t\\bar{t}}$ and $\kappa_W$ correct for a possible residual dependence of $R_{CS}$ on the number of jets, considering the sidebands of W+jets and $t\\bar{t}$+jets respectively.}\label{tab:0b_kappa}\end{table}'


##closure table, calculate old corrections and errors (phys14)
#print 
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
#print ' \\njet     & \ST & \HT     &\multicolumn{6}{c|}{$tt+$Jets}&\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{3}{c|}{Other EW bkg.}&\multicolumn{6}{c|}{total bkg.}\\\%\hline'
#print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'
#
#pred = {}
#multiplier = {(5,5):2, (6,7):3, (8,-1):4}
#
#secondLine = False
#for srNJet in sorted(signalRegions):
#  pred[srNJet] = {}
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    pred[srNJet][stb] = {}
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      pred[srNJet][stb][htb] = {}
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$'
#      
#      #rCS_srPredErrorCandidatesTT = [abs(1 - (res[srNJet][stb][htb]['rCS_crLowNJet_1b']['rCS']*kcs['tt'][stb][htb]['FitRatio']/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyTT']['rCS'])),\
#      #      res[srNJet][stb][htb]['rCS_srNJet_0b_onlyTT']['rCSE_sim']/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyTT']['rCS']]
#      #rCS_srPredErrorTT = max(rCS_srPredErrorCandidatesTT)
#      
#      ttPredictionVar = kcs['tt'][srNJet][stb][htb]['FitRatio']**2*res[srNJet][stb][htb]['TT_pred_err']**2 + kcs['tt'][srNJet][stb][htb]['FitRatioError']**2*res[srNJet][stb][htb]['TT_pred']**2
#      ttPredictionPosPdgVar = kcs['tt'][srNJet][stb][htb]['FitRatio']**2*(0.5*res[srNJet][stb][htb]['TT_pred_err'])**2 + kcs['tt'][srNJet][stb][htb]['FitRatioError']**2*(0.5*res[srNJet][stb][htb]['TT_pred'])**2
#      ttPredictionNegPdgVar = ttPredictionPosPdgVar
#      
#      # calculate disagreement between mu/ele+mu rcs values
#      ratio = res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_mu']['rCS']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW']['rCS']
#      if math.isnan(ratio): ratio = 0.
#      ratioPosPdg = res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_mu_PosPdg']['rCS']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_PosPdg']['rCS']
#      if math.isnan(ratioPosPdg): ratioPosPdg = 0.
#      ratioNegPdg = res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_mu_NegPdg']['rCS']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_NegPdg']['rCS']
#      if math.isnan(ratioNegPdg): ratioNegPdg = 0.
#
#      # take max of disagreement and stat. limit of ele+mu
#      WratioErr = max([abs(1-ratio),res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW']['rCSE_sim']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW']['rCS']])
#      WratioPosPdgErr = max([abs(1-ratioPosPdg),res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_PosPdg']['rCSE_sim']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_PosPdg']['rCS']])
#      WratioNegPdgErr = max([abs(1-ratioNegPdg),res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_NegPdg']['rCSE_sim']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_NegPdg']['rCS']])
#
#      #calculate total error for W jets with propagation
#      W_PosPdg_pred_rcs = res[srNJet][stb][htb]['rCS_W_PosPdg_crNJet_0b_corr'] + Wrcs_corr_PosPdg[srNJet][stb][htb]['K'] * multiplier[srNJet]
#      W_PosPdg_pred_rcs_Var = res[srNJet][stb][htb]['rCS_Var_W_PosPdg_crNJet_0b_corr'] + (Wrcs_corr_PosPdg[srNJet][stb][htb]['Kerr'] * multiplier[srNJet])**2
#      #W_PosPdg_pred = res[srNJet][stb][htb]['W_PosPdg_pred']
#      W_PosPdg_pred = res[srNJet][stb][htb]['yW_PosPdg_srNJet_0b_lowDPhi'] * W_PosPdg_pred_rcs
#      W_PosPdg_slope_Var = (res[srNJet][stb][htb]['W_PosPdg_pred'] - W_PosPdg_pred)**2
#      W_PosPdg_pred_statVar = res[srNJet][stb][htb]['yW_PosPdg_Var_srNJet_0b_lowDPhi'] * W_PosPdg_pred_rcs**2 + W_PosPdg_pred_rcs_Var * res[srNJet][stb][htb]['yW_PosPdg_srNJet_0b_lowDPhi']**2
#      W_PosPdg_Var = W_PosPdg_pred_statVar + (WratioPosPdgErr*W_PosPdg_pred)**2 + W_PosPdg_slope_Var
#
#      W_NegPdg_pred_rcs = res[srNJet][stb][htb]['rCS_W_NegPdg_crNJet_0b_corr'] + Wrcs_corr_NegPdg[srNJet][stb][htb]['K'] * multiplier[srNJet]
#      W_NegPdg_pred_rcs_Var = res[srNJet][stb][htb]['rCS_Var_W_NegPdg_crNJet_0b_corr'] + (Wrcs_corr_NegPdg[srNJet][stb][htb]['Kerr'] * multiplier[srNJet])**2
#      #W_NegPdg_pred = res[srNJet][stb][htb]['W_NegPdg_pred']
#      W_NegPdg_pred = res[srNJet][stb][htb]['yW_NegPdg_srNJet_0b_lowDPhi'] * W_NegPdg_pred_rcs
#      W_NegPdg_slope_Var = (res[srNJet][stb][htb]['W_NegPdg_pred'] - W_NegPdg_pred)**2
#      W_NegPdg_pred_statVar = res[srNJet][stb][htb]['yW_NegPdg_Var_srNJet_0b_lowDPhi'] * W_NegPdg_pred_rcs**2 + W_NegPdg_pred_rcs_Var * res[srNJet][stb][htb]['yW_NegPdg_srNJet_0b_lowDPhi']**2
#      W_NegPdg_Var = W_NegPdg_pred_statVar + (WratioNegPdgErr*W_NegPdg_pred)**2 + W_NegPdg_slope_Var
#
#      W_pred_rcs = res[srNJet][stb][htb]['rCS_W_crNJet_0b_corr'] + Wrcs_corr[srNJet][stb][htb]['K'] * multiplier[srNJet]
#      W_pred_rcs_Var = res[srNJet][stb][htb]['rCS_Var_W_crNJet_0b_corr'] + (Wrcs_corr[srNJet][stb][htb]['Kerr'] * multiplier[srNJet])**2
#      #W_pred = res[srNJet][stb][htb]['W_pred']
#      W_pred = res[srNJet][stb][htb]['yW_srNJet_0b_lowDPhi'] * W_pred_rcs
#      W_slope_Var = (res[srNJet][stb][htb]['W_pred'] - W_pred)**2
#      W_pred_statVar = res[srNJet][stb][htb]['yW_Var_srNJet_0b_lowDPhi'] * W_pred_rcs**2 + W_pred_rcs_Var * res[srNJet][stb][htb]['yW_srNJet_0b_lowDPhi']**2
#      W_Var = W_pred_statVar + (WratioErr*W_pred)**2 + W_slope_Var
#      
#      TT_pred = res[srNJet][stb][htb]['TT_pred']*kcs['tt'][srNJet][stb][htb]['FitRatio']
#            
#      totalPrediction = TT_pred + W_pred + res[srNJet][stb][htb]['Rest_truth']
#      totalPredictionPosPdg = 0.5*TT_pred + W_PosPdg_pred + res[srNJet][stb][htb]['Rest_PosPdg_truth']
#      totalPredictionNegPdg = 0.5*TT_pred + W_NegPdg_pred + res[srNJet][stb][htb]['Rest_NegPdg_truth']
#      totalPredictionError = sqrt(ttPredictionVar + W_Var + res[srNJet][stb][htb]['Rest_truth_err']**2)
#      totalPredictionPosPdgError = sqrt(ttPredictionPosPdgVar + W_PosPdg_Var + res[srNJet][stb][htb]['Rest_PosPdg_truth_err']**2)
#      totalPredictionNegPdgError = sqrt(ttPredictionNegPdgVar + W_NegPdg_Var + res[srNJet][stb][htb]['Rest_NegPdg_truth_err']**2)
#      
#      
#      print ' & '+getNumString(TT_pred, sqrt(ttPredictionVar))\
#           +' & '+getNumString(res[srNJet][stb][htb]['TT_truth'], res[srNJet][stb][htb]['TT_truth_err'])\
#           +' & '+getNumString(W_pred,   sqrt(W_Var))\
#           +' & '+getNumString(res[srNJet][stb][htb]['W_truth'],  res[srNJet][stb][htb]['W_truth_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['Rest_truth'], res[srNJet][stb][htb]['Rest_truth_err'])\
#           +' & '+getNumString(totalPrediction, totalPredictionError)\
#           +' & '+getNumString(res[srNJet][stb][htb]['tot_truth'],res[srNJet][stb][htb]['tot_truth_err']) +'\\\\'
#      if htb[1] == -1 : print '\\cline{2-24}'
#      
#      TTclosure       = max([abs(UncertaintyDivision((TT_pred - res[srNJet][stb][htb]['TT_truth']),TT_pred)), UncertaintyDivision(res[srNJet][stb][htb]['TT_truth_err'],res[srNJet][stb][htb]['TT_truth'])])
#      TTclosurePosPdg = TTclosure
#      TTclosureNegPdg = TTclosure
#      
#      Wclosure       = max([abs(UncertaintyDivision((W_pred - res[srNJet][stb][htb]['W_truth']),W_pred)), UncertaintyDivision(res[srNJet][stb][htb]['W_truth_err'],res[srNJet][stb][htb]['W_truth'])]) 
#      WclosurePosPdg = max([abs(UncertaintyDivision((W_PosPdg_pred - res[srNJet][stb][htb]['W_PosPdg_truth']),W_PosPdg_pred)), UncertaintyDivision(res[srNJet][stb][htb]['W_PosPdg_truth_err'],res[srNJet][stb][htb]['W_PosPdg_truth'])])
#      WclosureNegPdg = max([abs(UncertaintyDivision((W_NegPdg_pred - res[srNJet][stb][htb]['W_NegPdg_truth']),W_NegPdg_pred)), UncertaintyDivision(res[srNJet][stb][htb]['W_NegPdg_truth_err'],res[srNJet][stb][htb]['W_NegPdg_truth'])])
#      
#      totNonClosure = abs(UncertaintyDivision((totalPrediction - res[srNJet][stb][htb]['tot_truth']),totalPrediction))
#      totStatUncSim = UncertaintyDivision(res[srNJet][stb][htb]['tot_truth_err'],res[srNJet][stb][htb]['tot_truth'])
#      totalClosure       = max([totNonClosure, totStatUncSim])
#
#      totNonClosurePosPdg = abs(UncertaintyDivision((totalPredictionPosPdg - res[srNJet][stb][htb]['tot_PosPdg_truth']),totalPredictionPosPdg))
#      totStatUncSimPosPdg = UncertaintyDivision(res[srNJet][stb][htb]['tot_PosPdg_truth_err'],res[srNJet][stb][htb]['tot_PosPdg_truth'])
#      totalClosurePosPdg = max([totNonClosurePosPdg, totStatUncSimPosPdg])
#      
#      totNonClosureNegPdg = abs(UncertaintyDivision((totalPredictionNegPdg - res[srNJet][stb][htb]['tot_NegPdg_truth']),totalPredictionNegPdg))
#      totStatUncSimNegPdg = UncertaintyDivision(res[srNJet][stb][htb]['tot_NegPdg_truth_err'],res[srNJet][stb][htb]['tot_NegPdg_truth'])
#      totalClosureNegPdg = max([totNonClosureNegPdg, totStatUncSimNegPdg])
#      
#      res[srNJet][stb][htb].update({'tot_clos':totalClosure, 'tot_clos_PosPdg':totalClosurePosPdg, 'tot_clos_NegPdg':totalClosureNegPdg,\
#                                    'tot_onlyNonClos':totNonClosure, 'tot_StatUncSim':totStatUncSim, 'tot_onlyNonClos_PosPdg':totNonClosurePosPdg, 'tot_StatUncSim_PosPdg':totStatUncSimPosPdg,\
#                                    'tot_onlyNonClos_NegPdg':totNonClosureNegPdg, 'tot_StatUncSim_NegPdg':totStatUncSimNegPdg,\
#                                    'TT_clos':TTclosure, 'TT_clos_PosPdg':TTclosurePosPdg, 'TT_clos_NegPdg':TTclosureNegPdg, 'W_clos':Wclosure, 'W_clos_PosPdg':WclosurePosPdg, 'W_clos_NegPdg':WclosureNegPdg,\
#                                    'W_ratio_err':WratioErr, 'W_ratio_PosPdg_err':WratioPosPdgErr, 'W_ratio_NegPdg_err':WratioNegPdgErr})
#      res[srNJet][stb][htb]['tot_pred'] = totalPrediction
#      res[srNJet][stb][htb]['tot_pred_err'] = totalPredictionError
#      res[srNJet][stb][htb]['tot_PosPdg_pred'] = totalPredictionPosPdg
#      res[srNJet][stb][htb]['tot_PosPdg_pred_err'] = totalPredictionPosPdgError
#      res[srNJet][stb][htb]['tot_NegPdg_pred'] = totalPredictionNegPdg
#      res[srNJet][stb][htb]['tot_NegPdg_pred_err'] = totalPredictionNegPdgError
#      res[srNJet][stb][htb]['TT_pred'] = TT_pred
#      res[srNJet][stb][htb]['TT_pred_err'] = sqrt(ttPredictionVar)
#      res[srNJet][stb][htb]['W_pred'] = W_pred
#      res[srNJet][stb][htb]['W_PosPdg_pred'] = W_PosPdg_pred
#      res[srNJet][stb][htb]['W_NegPdg_pred'] = W_NegPdg_pred
#      res[srNJet][stb][htb]['W_pred_err'] = sqrt(W_Var)
#      res[srNJet][stb][htb]['W_PosPdg_pred_err'] = sqrt(W_PosPdg_Var)
#      res[srNJet][stb][htb]['W_NegPdg_pred_err'] = sqrt(W_NegPdg_Var)
#      
#      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
#      name, cut =  nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = btagString)
#      if signal:
#        for s in allSignals:
#          s['yield_NegPdg']     = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_str)
#          s['yield_NegPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_err_str)
#          s['yield_PosPdg']     = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_str)
#          s['yield_PosPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_err_str)
#          s['yield']     = getYieldFromChain(s['chain'], cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_str)
#          s['yield_Var'] = getYieldFromChain(s['chain'], cut+"&&deltaPhi_Wl>"+str(deltaPhiCut), weight = weight_err_str)
#
#          res[srNJet][stb][htb].update({\
#                      s['name']+'_yield_NegPdg':s['yield_NegPdg'],\
#                      s['name']+'_yield_NegPdg_Var':s['yield_NegPdg_Var'],\
#                      s['name']+'_yield_PosPdg':s['yield_PosPdg'],\
#                      s['name']+'_yield_PosPdg_Var':s['yield_PosPdg_Var'],\
#                      s['name']+'_yield':s['yield'],\
#                      s['name']+'_yield_Var':s['yield_Var'],\
#                    })
#print '\\hline\end{tabular}}\end{center}\caption{Closure table for the background with applied correction factors for \\ttJets, 0-tag regions, 3$fb^{-1}$}\label{tab:0b_rcscorr_Wbkg}\end{table}'
#
#pickle.dump(res, file(path+prefix+'_estimationResults_pkl_updated','w'))
##print "written pkl :" , path+prefix+'_estimationResults_pkl_updated'



#res = pickle.load(file(path+prefix+'_estimationResults_pkl_updated'))

##closure table with correction
#print 
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
#print ' \\njet     & \ST & \HT     &\multicolumn{6}{c|}{total bkg.}&\multicolumn{3}{c|}{$T5q^4~1.0/0.8/0.7$}&\multicolumn{3}{c|}{$T5q^4~1.2/1.0/0.8$}&\multicolumn{3}{c|}{$T5q^4~1.5/0.8/0.1$}\\\%\hline'
#print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation} \\\\\hline'
#
#pred = {}
#
#secondLine = False
#for srNJet in sorted(signalRegions):
#  pred[srNJet] = {}
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    pred[srNJet][stb] = {}
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      pred[srNJet][stb][htb] = {}
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$'
#      print ' & '+getNumString(res[srNJet][stb][htb]['tot_pred'], res[srNJet][stb][htb]['tot_pred_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['tot_truth'], res[srNJet][stb][htb]['tot_truth_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['T5q^{4} 1.0/0.8/0.7_yield'], sqrt(res[srNJet][stb][htb]['T5q^{4} 1.0/0.8/0.7_yield_Var']))\
#           +' & '+getNumString(res[srNJet][stb][htb]['T5q^{4} 1.2/1.0/0.8_yield'], sqrt(res[srNJet][stb][htb]['T5q^{4} 1.2/1.0/0.8_yield_Var']))\
#           +' & '+getNumString(res[srNJet][stb][htb]['T5q^{4} 1.5/0.8/0.1_yield'], sqrt(res[srNJet][stb][htb]['T5q^{4} 1.5/0.8/0.1_yield_Var'])) +'\\\\'
#      if htb[1] == -1 : print '\\cline{2-18}'
#print '\\hline\end{tabular}}\end{center}\caption{Closure table for the background with applied correction factors for \\ttJets, 0-tag regions, 3$fb^{-1}$}\label{tab:0b_rcscorr_Wbkg}\end{table}'

## Closure error table
#res = pickle.load(file(path+prefix+'_estimationResults_pkl_updated'))
#multiplier = {(5,5):2, (6,7):3, (8,-1):4}
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|}\\hline'
#print ' \\njet & \ST & \HT &\multicolumn{6}{c|}{total}&\multicolumn{6}{c|}{total}\\\%\hline'
#print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{non-closure}&\multicolumn{3}{c|}{stat. of sim} \\\\\hline'
#secondLine = False
#for srNJet in sorted(signalRegions):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      if not first: print '&'
#      first = False
#
#      print '&$'+varBin(htb)+'$'
#      print ' & '+getNumString(res[srNJet][stb][htb]['tot_pred'], res[srNJet][stb][htb]['tot_pred_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['tot_truth'], res[srNJet][stb][htb]['tot_truth_err'])\
#           +' & '+getNumString(1.0, res[srNJet][stb][htb]['tot_onlyNonClos'])\
#           +' & '+getNumString(1.0, res[srNJet][stb][htb]['tot_StatUncSim'])+'\\\\'
#      if htb[1] == -1 : print '\\cline{2-15}'
#print '\\hline\end{tabular}}\end{center}\caption{closure errors}\label{tab:0b_rcscorr_Wbkg}\end{table}'


##Table for systematics prediction for W jets as a result of mu/ele+mu differences
#print "Results"
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|c|c|}\\hline'
#print ' \\njet     & \ST & \HT     &\multicolumn{3}{c|}{sys. Unc., W est.}\\\%\hline'
#print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{1}{c}{pos}&\multicolumn{1}{c}{neg}&total \\\\\hline'
#
#pred = {}
#secondLine = False
#for srNJet in sorted(signalRegions):
#  pred[srNJet] = {}
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    pred[srNJet][stb] = {}
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      ratio = res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_mu']['rCS']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW']['rCS']
#      if math.isnan(ratio): ratio = 0.
#      ratioPosPdg = res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_mu_PosPdg']['rCS']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_PosPdg']['rCS']
#      if math.isnan(ratioPosPdg): ratioPosPdg = 0.
#      ratioNegPdg = res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_mu_NegPdg']['rCS']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_NegPdg']['rCS']
#      if math.isnan(ratioNegPdg): ratioNegPdg = 0.
#
#      # take max of disagreement and stat. limit of ele+mu
#      WratioErr = max([abs(1-ratio),res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW']['rCSE_sim']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW']['rCS']])
#      WratioPosPdgErr = max([abs(1-ratioPosPdg),res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_PosPdg']['rCSE_sim']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_PosPdg']['rCS']])
#      WratioNegPdgErr = max([abs(1-ratioNegPdg),res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_NegPdg']['rCSE_sim']/res[srNJet][stb][htb]['rCS_crLowNJet_0b_onlyW_NegPdg']['rCS']])
#  
#      pred[srNJet][stb][htb] = {}
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$'
#      print ' & ' + str(round(WratioNegPdgErr,2)) + '&'  + str(round(WratioPosPdgErr,2)) + '&' + str(round(WratioErr,2)) +'\\\\'
#      if htb[1] == -1 : print '\\cline{2-6}'
#print '\\hline\end{tabular}}\end{center}\caption{Closure table for the background with applied correction factors for \\ttJets, 0-tag regions, 3$fb^{-1}$}\label{tab:0b_rcscorr_Wbkg}\end{table}'



## tt Prediction table
#print
#print "rCS(TT) comparison used for tt estimation"
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|c|}\\hline'
#print ' $n_{jet}$  & \ST$[$GeV$]$ & \HT$[$GeV$]$   &\multicolumn{3}{c|}{$R_{CS}(1b,4/5j)$}&\multicolumn{3}{c|}{$R_{CS,tt}(1b,4/5j)$}&\multicolumn{3}{c|}{$R_{CS,tt}(0b)$}& $\Delta\Phi(W,l)$\\\\\hline'
#secondLine = False
#for srNJet in sorted(signalRegions):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$&'
#      print   ' & '.join([getNumString(res[srNJet][stb][htb]['rCS_crLowNJet_1b']['rCS'],    res[srNJet][stb][htb]['rCS_crLowNJet_1b']['rCSE_sim'],acc=3), \
#                      getNumString(res[srNJet][stb][htb]['rCS_crLowNJet_1b_onlyTT']['rCS'], res[srNJet][stb][htb]['rCS_crLowNJet_1b_onlyTT']['rCSE_sim'],acc=3),\
#                      getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyTT']['rCS'],    res[srNJet][stb][htb]['rCS_srNJet_0b_onlyTT']['rCSE_sim'],acc=3),\
#                      str(signalRegions[srNJet][stb][htb]['deltaPhi'])])+'\\\\'
#      if htb[1] == -1 : print '\\cline{2-13}'
#print '\\hline\end{tabular}}\end{center}\caption{rCS(TT) comparison used for tt estimation}\end{table}'


### W Prediction table 1 not needed atm
#print "rCS(TT) comparison used for rCS(W) correction"
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|c|}\\hline'
#print ' \\njet & \ST$[$GeV$]$     & \HT$[$GeV$]$     &\multicolumn{3}{c|}{$R_{CS}(1b,2/3j)$}&\multicolumn{3}{c|}{$R_{CS,tt}(1b,2/3j)$}&\multicolumn{3}{c|}{$R_{CS,tt}(0b,2/3j)$} & $\Delta\Phi(W,l)$\\\\\hline'
#secondLine = False
#for srNJet in sorted(signalRegions):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$&'
##for i_htb, htb in enumerate(htreg):
##  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
##  for stb, dPhiCut in streg:
##    print '&$'+varBin(stb)+'$&'
##    for srNJet in njreg[:1]:
#      #print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
#      print   ' & '.join([getNumString(res[srNJet][stb][htb]['rCS_crNJet_1b']['rCS'],   res[srNJet][stb][htb]['rCS_crNJet_1b']['rCSE_sim'],3), \
#                      getNumString(res[srNJet][stb][htb]['rCS_crNJet_1b_onlyTT']['rCS'], res[srNJet][stb][htb]['rCS_crNJet_1b_onlyTT']['rCSE_sim'],3),\
#                      getNumString(res[srNJet][stb][htb]['rCS_crNJet_0b_onlyTT']['rCS'], res[srNJet][stb][htb]['rCS_crNJet_0b_onlyTT']['rCSE_sim'],3)]),\
#                      '&',str(signalRegions[srNJet][stb][htb]['deltaPhi'])+'\\\\'
#      if htb[1] == -1 : print '\\cline{2-13}'
#print '\\hline\end{tabular}}\end{center}\caption{}\end{table}'
#print


## W Prediction table 2
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|c|}\\hline'
#print ' \\njet & \ST & \HT &\multicolumn{6}{c|}{$R^{corr.}_{CS}(0b,2/3j)$}&\multicolumn{6}{c|}{$R_{CS,W_{jets}}(0b)$} & $\Delta\Phi(W,l)$\\\%\hline'
#print '  & $[$GeV$]$ & $[$GeV$]$ & \multicolumn{3}{c}{neg. charge} & \multicolumn{3}{c|}{pos. charge} & \multicolumn{3}{c}{pos. charge} & \multicolumn{3}{c|}{neg. charge} & \\\\\hline '
#
#secondLine = False
#for srNJet in sorted(signalRegions):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$&'
##for i_htb, htb in enumerate(htreg):
##  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
##  for stb, dPhiCut in streg:
##    print '&$'+varBin(stb)+'$&'
##    #print '& & \multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (- charge)}&\multicolumn{3}{c|}{$R_{CS,W^{-}_{jets}}(0b,==5j)$}&\multicolumn{3}{c}{$R_{CS,W^{-}_{jets}}(0b,>=6j)$}\\\\hline'
##    #print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
#      print  ' & '.join([getNumString(res[srNJet][stb][htb]['rCS_W_PosPdg_crNJet_0b_corr'], sqrt(res[srNJet][stb][htb]['rCS_Var_W_PosPdg_crNJet_0b_corr']),4), \
#                    getNumString(res[srNJet][stb][htb]['rCS_W_NegPdg_crNJet_0b_corr'],    sqrt(res[srNJet][stb][htb]['rCS_Var_W_NegPdg_crNJet_0b_corr']),4), \
#                    getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCS'],   res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCSE_sim'],4),\
#                    getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'],   res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4),\
#                    str(signalRegions[srNJet][stb][htb]['deltaPhi'])])+'\\\\'
#      if htb[1] == -1 : print '\\cline{2-16}'
#print
#print '\\hline\end{tabular}}\end{center}\caption{hooli XYZ}\end{table}'

## W Prediction RCS table stability check
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
#print ' \\njet & \ST & \HT & \multicolumn{9}{c|}{pos. PDG} & \multicolumn{9}{c|}{neg. PDG} & \multicolumn{9}{c|}{all}\\\%\hline'
#print '  & $[$GeV$]$ & $[$GeV$]$ & \multicolumn{3}{c}{ele} & \multicolumn{3}{c}{mu} & \multicolumn{3}{c|}{both} & \multicolumn{3}{c}{ele} & \multicolumn{3}{c}{mu} & \multicolumn{3}{c|}{both}& \multicolumn{3}{c}{ele} & \multicolumn{3}{c}{mu} & \multicolumn{3}{c|}{both} \\\\\hline '
#
#secondLine = False
#for srNJet in sorted(signalRegions):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$&'
##for i_htb, htb in enumerate(htreg):
##  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
##  for stb, dPhiCut in streg:
##    print '&$'+varBin(stb)+'$&'
##    #print '& & \multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (- charge)}&\multicolumn{3}{c|}{$R_{CS,W^{-}_{jets}}(0b,==5j)$}&\multicolumn{3}{c}{$R_{CS,W^{-}_{jets}}(0b,>=6j)$}\\\\hline'
##    #print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
#      print  ' & '.join([getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_ele_PosPdg']['rCS'], res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_ele_PosPdg']['rCSE_sim'],4), \
#                         getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu_PosPdg']['rCS'],  res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu_PosPdg']['rCSE_sim'],4), \
#                         getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCS'],     res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCSE_sim'],4),\
#                         getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_ele_NegPdg']['rCS'], res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_ele_NegPdg']['rCSE_sim'],4), \
#                         getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu_NegPdg']['rCS'],  res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu_NegPdg']['rCSE_sim'],4), \
#                         getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'],     res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4),\
#                         getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_ele']['rCS'], res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_ele']['rCSE_sim'],4), \
#                         getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu']['rCS'],  res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu']['rCSE_sim'],4), \
#                         getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW']['rCS'],     res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW']['rCSE_sim'],4)])+'\\\\'
#      if htb[1] == -1 : print '\\cline{2-30}'
#print
#print '\\hline\end{tabular}}\end{center}\caption{RCS stability for W jets}\end{table}'

#secondLine = False
#for srNJet in sorted(signalRegions):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$&'
#      print  ' & '.join([getNumString(res[srNJet][stb][htb]['rCS_W_PosPdg_crNJet_0b_corr'], sqrt(res[srNJet][stb][htb]['rCS_Var_W_PosPdg_crNJet_0b_corr']),4), \
#                    getNumString(res[srNJet][stb][htb]['rCS_W_NegPdg_crNJet_0b_corr'],    sqrt(res[srNJet][stb][htb]['rCS_Var_W_NegPdg_crNJet_0b_corr']),4), \
#                    getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCS'],   res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCSE_sim'],4),\
#                    getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'],   res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4),\
#                    str(signalRegions[srNJet][stb][htb]['deltaPhi'])])+'\\\\'
#      if htb[1] == -1 : print '\\cline{2-16}'
#print
#print '\\hline\end{tabular}}\end{center}\caption{hooli XYZ}\end{table}'


##########################################################################
##########################################################################
########################in progress / old stuff ##########################
##########################################################################
##########################################################################


#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
#print ' \HT     & \\njet & \ST     &\multicolumn{6}{c|}{$tt+$Jets}&\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{3}{c|}{Other EW bkg.}&\multicolumn{6}{c|}{total bkg.}\\\%\hline'
#print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'
#secondLine = False
#for srNJet in sorted(signalRegions):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(stb)+'$'
#      print ' & '+getNumString(res[htb][stb][srNJet]['TT_pred'], res[htb][stb][srNJet]['TT_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['TT_truth'], res[htb][stb][srNJet]['TT_truth_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['W_pred'], res[htb][stb][srNJet]['W_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['W_truth'], res[htb][stb][srNJet]['W_truth_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['Rest_truth'], res[htb][stb][srNJet]['Rest_truth_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['tot_pred'], res[htb][stb][srNJet]['tot_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['tot_truth'], res[htb][stb][srNJet]['tot_truth_err']) +'\\\\'
#      if stb[1] == -1 : print '\\cline{2-24}'
#  #print '\\hline'
#print '\\hline\end{tabular}}\end{center}\caption{ABCD}\label{tab:0b_rcscorr_Wbkg}\end{table}'

##print
##print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|c|}\\hline'
##print ' \HT     & \\njet & \ST     &$tt+$Jets&$W+$ Jets&'
##print '$[$GeV$]$&        &$[$GeV$]$&         &         &\\\\\hline'
##for i_htb, htb in enumerate(htreg):
##  print '\\hline'
##  if i_htb!=0:print '\\hline'
##  print '\multirow{'+str(nJetBins*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(htb)+'$\end{sideways}}'
##  for srNJet in njreg:
##    print '&\multirow{'+str(nSTbins)+'}{*}{$'+varBin(srNJet)+'$}'
##    first = True
##    for stb, dPhiCut in streg:
##      if not first: print '&'
##      first = False
##      #if stb[1] == -1 : print '&'
##      print '&$'+varBin(stb)+'$'
##      print 'ohne:',res[htb][stb][srNJet]['W_pred'],res[htb][stb][srNJet]['W_truth'],'unc:', res1[htb][stb][srNJet]['W_pred'],res1[htb][stb][srNJet]['W_truth']
##      print ' & '+str(format(abs(abs(float(float(res1[htb][stb][srNJet]['TT_pred']-res1[htb][stb][srNJet]['TT_truth'])/float(res1[htb][stb][srNJet]['TT_pred']))/(float(float(res[htb][stb][srNJet]['TT_pred']-res[htb][stb][srNJet]['TT_truth'])/float(res[htb][stb][srNJet]['TT_pred']))))-1),'.5f'))\
##           +' & '+str(format(abs(abs(float(float(res1[htb][stb][srNJet]['W_pred']-res1[htb][stb][srNJet]['W_truth'])/float(res1[htb][stb][srNJet]['W_pred']))/(float(float(res[htb][stb][srNJet]['W_pred']-res[htb][stb][srNJet]['W_truth'])/float(res[htb][stb][srNJet]['W_pred']))))-1),'.5f')) +'\\\\'
##      if stb[1] == -1 : print '\\cline{2-5}'
##  #print '\\hline'
##print '\\hline\end{tabular}}\end{center}\caption{ttJets unc}\label{tab:ttJets unc}\end{table}'
##
##
##print
##print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
##print ' \HT     & \\njet & \ST     &\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{6}{c|}{$W-$ Jets}&\multicolumn{6}{c|}{$W$ Jets}\\\%\hline'
##print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'
##secondLine = False
##for srNJet in sorted(signalRegions):
##  print '\\hline'
##  if secondLine: print '\\hline'
##  secondLine = True
##  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
##  for stb in sorted(signalRegions[srNJet]):
##    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
##    first = True
##    for htb in sorted(signalRegions[srNJet][stb]):
##      if not first: print '&'
##      first = False
##      #if stb[1] == -1 : print '&'
##      print '&$'+varBin(stb)+'$'
##      print ' & '+getNumString(res[htb][stb][srNJet]['W_NegPdg_pred'], res[htb][stb][srNJet]['W_NegPdg_pred_err'])\
##           +' & '+getNumString(res[htb][stb][srNJet]['W_NegPdg_truth'], res[htb][stb][srNJet]['W_NegPdg_truth_err'])\
##           +' & '+getNumString(res[htb][stb][srNJet]['W_PosPdg_pred'], res[htb][stb][srNJet]['W_PosPdg_pred_err'])\
##           +' & '+getNumString(res[htb][stb][srNJet]['W_PosPdg_truth'], res[htb][stb][srNJet]['W_PosPdg_truth_err'])\
##           +' & '+getNumString(res[htb][stb][srNJet]['W_pred'], res[htb][stb][srNJet]['W_pred_err'])\
##           +' & '+getNumString(res[htb][stb][srNJet]['W_truth'], res[htb][stb][srNJet]['W_truth_err']) +'\\\\'
##      if stb[1] == -1 : print '\\cline{2-21}'
##print '\\hline\end{tabular}}\end{center}\caption{EFGH}\label{tab:0b_rcscorr_Wbkg}\end{table}'


#for i_htb, htb in enumerate(htreg):
#  print '\\hline'
#  if i_htb!=0:print '\\hline'
#  print '\multirow{'+str(nJetBins*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(htb)+'$\end{sideways}}'
#  #print '& & \multicolumn{6}{c|}{$t\overline{t}$+Jets}&\multicolumn{6}{c|}{$W$+Jets}&\multicolumn{6}{c}{total}\\\\'
#  #print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
#  #      '$} & \multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}\\\\\\hline'
#  for srNJet in njreg:
#    print '&\multirow{'+str(nSTbins)+'}{*}{$'+varBin(srNJet)+'$}'
#    first = True
#    for stb, dPhiCut in streg:
#      if not first: print '&'
#      first = False
#      #if stb[1] == -1 : print '&'
#      print '&$'+varBin(stb)+'$'
#      print ' & '+getNumString(res[htb][stb][srNJet]['TT_pred'], res[htb][stb][srNJet]['TT_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['TT_truth'], res[htb][stb][srNJet]['TT_truth_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['W_pred'], res[htb][stb][srNJet]['W_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['W_truth'], res[htb][stb][srNJet]['W_truth_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['tot_pred'], res[htb][stb][srNJet]['tot_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['tot_truth'], res[htb][stb][srNJet]['tot_truth_err']) +'\\\\'
#      if stb[1] == -1 : print '\\cline{2-21}'
#  #print '\\hline'
#print '\\hline\end{tabular}}\end{center}\caption{ABCD}\label{tab:0b_rcscorr_Wbkg}\end{table}'
#
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
#print ' \HT     & \\njet & \ST     &\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{6}{c|}{$W-$ Jets}&\multicolumn{6}{c|}{$W$ Jets}\\\%\hline'
#print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'
#for i_htb, htb in enumerate(htreg):
#  print '\\hline'
#  if i_htb!=0:print '\\hline'
#  print '\multirow{'+str(nJetBins*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(htb)+'$\end{sideways}}'
#  for srNJet in njreg:
#    print '&\multirow{'+str(nSTbins)+'}{*}{$'+varBin(srNJet)+'$}'
#    first = True
#    for stb, dPhiCut in streg:
#      if not first: print '&'
#      first = False
#      #if stb[1] == -1 : print '&'
#      print '&$'+varBin(stb)+'$'
#      print ' & '+getNumString(res[htb][stb][srNJet]['W_NegPdg_pred'], res[htb][stb][srNJet]['W_NegPdg_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['W_NegPdg_truth'], res[htb][stb][srNJet]['W_NegPdg_truth_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['W_PosPdg_pred'], res[htb][stb][srNJet]['W_PosPdg_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['W_PosPdg_truth'], res[htb][stb][srNJet]['W_PosPdg_truth_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['W_pred'], res[htb][stb][srNJet]['W_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['W_truth'], res[htb][stb][srNJet]['W_truth_err']) +'\\\\'
#      if stb[1] == -1 : print '\\cline{2-21}'
#print '\\hline\end{tabular}}\end{center}\caption{EFGH}\label{tab:0b_rcscorr_Wbkg}\end{table}'


#
#print "RCS corr comparison"
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|rrr|rrr|rrr|rrr|}\\hline'
#print ' \HT$[$GeV$]$     & \ST$[$GeV$]$     &\multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$}&\multicolumn{3}{c|}{$R_{CS,W_{jets}}(0b,5j)$}&\multicolumn{3}{c|}{$R_{CS,W_{jets}}(0b,6/7j)$}&\multicolumn{3}{c|}{$R_{CS,W_{jets}}(0b,\geq8j)$}\\\\\hline'
#for i_htb, htb in enumerate(htreg):
#  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
#  for stb, dPhiCut in streg:
#    print '&$'+varBin(stb)+'$&'
#    #print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
#    print   ' & '.join([getNumString(res[htb][stb][njreg[0]]['rCS_W_crNJet_0b_corr'],sqrt(res[htb][stb][njreg[0]]['rCS_Var_W_crNJet_0b_corr']),4), \
#                    getNumString(res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW']['rCS'], res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW']['rCSE_sim'],4),\
#                    getNumString(res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW']['rCS'], res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW']['rCSE_sim'],4),\
#                    getNumString(res[htb][stb][njreg[2]]['rCS_srNJet_0b_onlyW']['rCS'], res[htb][stb][njreg[2]]['rCS_srNJet_0b_onlyW']['rCSE_sim'],4)])+'\\\\'
#    if stb[1] == -1 : print '\\hline'
#                    
#print '\end{tabular}}\end{center}\caption{}\end{table}'
#print

#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|}\\hline'
#print ' \\njet & \ST & \HT &\multicolumn{3}{c|}{$R^{corr.}_{CS}$(0b,2/3j)}&\multicolumn{6}{c|}{$R_{CS,W^{-}_{jets}}(0b,5j)$}&\multicolumn{3}{c|}{$R_{CS,W^{-}_{jets}}(0b,6/7j)$}&\multicolumn{3}{c|}{$R_{CS,W^{-}_{jets}}(0b,\geq8j)$}\\\\\hline'


#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|c|}\\hline'
#print ' \\njet & \ST & \HT &\multicolumn{6}{c|}{$R^{corr.}_{CS}(0b,2/3j)$}&\multicolumn{6}{c|}{$R_{CS,W_{jets}}(0b)$} & $\Delta\Phi(W,l)$\\\%\hline'
#print '  & $[$GeV$]$ & $[$GeV$]$ & \multicolumn{3}{c}{pos. charge} & \multicolumn{3}{c|}{neg. charge} & \multicolumn{3}{c}{pos. charge} & \multicolumn{3}{c|}{neg. charge} & \\\\\hline '
#
#secondLine = False
#for srNJet in sorted(signalRegions):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegions[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegions[srNJet][stb]):
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$&'
##for i_htb, htb in enumerate(htreg):
##  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
##  for stb, dPhiCut in streg:
##    print '&$'+varBin(stb)+'$&'
##    #print '& & \multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (- charge)}&\multicolumn{3}{c|}{$R_{CS,W^{-}_{jets}}(0b,==5j)$}&\multicolumn{3}{c}{$R_{CS,W^{-}_{jets}}(0b,>=6j)$}\\\\hline'
##    #print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
#      print  ' & '.join([getNumString(res[srNJet][stb][htb]['rCS_W_PosPdg_crNJet_0b_corr'], sqrt(res[srNJet][stb][htb]['rCS_Var_W_PosPdg_crNJet_0b_corr']),4), \
#                    getNumString(res[srNJet][stb][htb]['rCS_W_NegPdg_crNJet_0b_corr'],    sqrt(res[srNJet][stb][htb]['rCS_Var_W_NegPdg_crNJet_0b_corr']),4), \
#                    getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCS'],   res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCSE_sim'],4),\
#                    getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'],   res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4),\
#                    str(signalRegions[srNJet][stb][htb]['deltaPhi'])])+'\\\\'
#      if htb[1] == -1 : print '\\cline{2-16}'
#print
##print '& & & \multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (+ charge)}&\multicolumn{3}{c|}{$R_{CS,W^{+}_{jets}}(0b,5j)$}&\multicolumn{3}{c|}{$R_{CS,W^{+}_{jets}}(0b,6/7j)$}&\multicolumn{3}{c|}{$R_{CS,W^{+}_{jets}}(0b,\geq8j)$}\\\\\hline'
#
##secondLine = False
##for srNJet in sorted(signalRegions):
##  print '\\hline'
##  if secondLine: print '\\hline'
##  secondLine = True
##  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
##  for stb in sorted(signalRegions[srNJet]):
##    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
##    first = True
##    for htb in sorted(signalRegions[srNJet][stb]):
##      if not first: print '&'
##      first = False
##      print '&$'+varBin(htb)+'$&'
###for i_htb, htb in enumerate(htreg):
###  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
###  for stb, dPhiCut in streg:
###    print '&$'+varBin(stb)+'$&'
###    #print '& & \multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (+ charge)}&\multicolumn{3}{c|}{$R_{CS,W^{+}_{jets}}(0b,==5j)$}&\multicolumn{3}{c}{$R_{CS,W^{+}_{jets}}(0b,>=6j)$}\\\\hline'
###    #print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
##    print    ' & '.join([getNumString(res[htb][stb][njreg[0]]['rCS_W_NegPdg_crNJet_0b_corr'],sqrt(res[htb][stb][njreg[0]]['rCS_Var_W_NegPdg_crNJet_0b_corr']),4), \
##                    getNumString(res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'], res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4),\
##                    getNumString(res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'], res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4),\
##                    getNumString(res[htb][stb][njreg[2]]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'], res[htb][stb][njreg[2]]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4)])+'\\\\'
##    if htb[1] == -1 : print '\\hline'
##print
#print '\\hline\end{tabular}}\end{center}\caption{hooli XYZ}\end{table}'



### NOT TESTED ###

#print "signal yields (+charge)"
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|}\\hline'
#print ' \HT     & \\njet & \ST     & \multicolumn{6}{c|}{\TFiveqqqqHM (+ charge)} & \multicolumn{6}{c|}{\TFiveqqqqHL (+ charge)}\\\\ %\hline'
#print '[GeV]&        &[GeV]&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{FOM} &\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{FOM} \\\\\hline'
#for i_htb, htb in enumerate(htreg):
#  if i_htb!=0:print '\\hline'
#  print '\multirow{'+str(2*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(htb)+'$\end{sideways}}'
#  for srNJet in njreg:
#    print '&\multirow{'+str(nSTbins)+'}{*}{'+varBin(srNJet)+'}&'
#    for stb, dPhiCut in streg:
#      print '$'+varBin(stb)+'$'
##      name, cut =  nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = 'nBJetMediumCMVA30')
##      for s in allSignals:
##        s['yield_NegPdg']     = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>1.0", weight = "weight")
##        s['yield_NegPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>1.0", weight = "weight*weight")
#      print ' & '.join([getNumString(res[htb][stb][srNJet]['T5q^{4} 1.2/1.0/0.8_yield_NegPdg'], sqrt(res[htb][stb][srNJet]['T5q^{4} 1.2/1.0/0.8_yield_NegPdg_Var']), acc=3),
#                          getNumString(res[htb][stb][srNJet]['T5q^{4} 1.2/1.0/0.8_FOM_NegPdg']['FOM'], res[htb][stb][srNJet]['T5q^{4} 1.2/1.0/0.8_FOM_NegPdg']['FOM_Err'], acc=3),
#                          getNumString(res[htb][stb][srNJet]['T5q^{4} 1.5/0.8/0.1_yield_NegPdg'], sqrt(res[htb][stb][srNJet]['T5q^{4} 1.5/0.8/0.1_yield_NegPdg_Var']), acc=3),
#                          getNumString(res[htb][stb][srNJet]['T5q^{4} 1.5/0.8/0.1_FOM_NegPdg']['FOM'], res[htb][stb][srNJet]['T5q^{4} 1.5/0.8/0.1_FOM_NegPdg']['FOM_Err'], acc=3)])+'\\\\'
##      print '\\\\'
#      if stb[1] != -1 :print '&&'
#      if stb[1] == -1 : print '\\cline{2-15}'
#print '\\hline\end{tabular}}\end{center}\caption{+ charge}\end{table}'
#
#print "signal yields (-charge)"
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|}\\hline'
#print ' \HT     & \\njet & \ST     &\multicolumn{6}{c|}{\TFiveqqqqHM (- charge)}&\multicolumn{6}{c|}{\TFiveqqqqHL (- charge)}\\\%\hline'
#print '[GeV]&        &[GeV]&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{FOM} &\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{FOM} \\\\\hline'
#for i_htb, htb in enumerate(htreg):
#  if i_htb!=0:print '\\hline'
#  print '\multirow{'+str(2*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(htb)+'$\end{sideways}}'
#  for srNJet in njreg:
#    print '&\multirow{'+str(nSTbins)+'}{*}{'+varBin(srNJet)+'}&'
#    for stb, dPhiCut in streg:
#      print '$'+varBin(stb)+'$'
##      name, cut =  nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = 'nBJetMediumCMVA30')
##      for s in allSignals:
##        s['yield_PosPdg']     = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>1.0", weight = "weight")
##        s['yield_PosPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>1.0", weight = "weight*weight")
#      print ' & '.join([getNumString(res[htb][stb][srNJet]['T5q^{4} 1.2/1.0/0.8_yield_PosPdg'], sqrt(res[htb][stb][srNJet]['T5q^{4} 1.2/1.0/0.8_yield_PosPdg_Var']), acc=3),
#                          getNumString(res[htb][stb][srNJet]['T5q^{4} 1.2/1.0/0.8_FOM_PosPdg']['FOM'], res[htb][stb][srNJet]['T5q^{4} 1.2/1.0/0.8_FOM_PosPdg']['FOM_Err'], acc=3),
#                          getNumString(res[htb][stb][srNJet]['T5q^{4} 1.5/0.8/0.1_yield_PosPdg'], sqrt(res[htb][stb][srNJet]['T5q^{4} 1.5/0.8/0.1_yield_PosPdg_Var']), acc=3),
#                          getNumString(res[htb][stb][srNJet]['T5q^{4} 1.5/0.8/0.1_FOM_PosPdg']['FOM'], res[htb][stb][srNJet]['T5q^{4} 1.5/0.8/0.1_FOM_PosPdg']['FOM_Err'], acc=3)])+'\\\\'
##      print '\\\\'
#      if stb[1] != -1 :print '&&'
#      if stb[1] == -1 : print '\\cline{2-15}'
#print '\\hline\end{tabular}}\end{center}\caption{- charge}\end{table}'

