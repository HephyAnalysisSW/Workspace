import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin
from rCShelpers import *
import math
from localInfo import username
from Workspace.RA4Analysis.signalRegions import *

prefix = 'singleLeptonic_Phys14V3_'
#res = pickle.load(file('/data/'+username+'/results2015/rCS_0b/'+prefix+'_estimationResults_pkl'))
#res = pickle.load(file('/data/'+username+'/PHYS14v3/withCSV/rCS_0b/'+prefix+'_estimationResults_ttJet_unc_pkl'))

path = '/data/'+username+'/PHYS14v3/withCSV/rCS_0b_3.0fbSlidingWcorrectionMuonChannel/' 
res = pickle.load(file(path+prefix+'_estimationResults_pkl'))
kcs = pickle.load(file(path+'correction_pkl'))


#res1 = pickle.load(file('/data/'+username+'/PHYS14v3/withCSV/rCS_0b/'+prefix+'_ttjet_unc_estimationResults_pkl'))
#res = pickle.load(file('/data/'+username+'/PHYS14v3/withCSV/rCS_0b/'+prefix+'_restIsTTVH_estimationResults_pkl'))


#nSTbins = len(streg)
#nJetBins = len(njreg)

signalRegions = signalRegion3fb


#streg = [[(250, 350), 1.], [(350, 450), 1.], [(450,-1), 1.]]
#htreg = [(500,750),(750,1000),(1000,1250),(1250,-1)]
#njreg = [(5,5),(6,7),(8,-1)]
#nSTbins = len(streg)
#nJetBins = len(njreg)

#lengths = {}
#for srNJet in sorted(signalRegion2fb):
#  lengths[srNJet] = {}
#  for stb in sorted(signalRegion2fb[srNJet]):
#    lengths[srNJet][stb] = {'nST':len(signalRegion2fb[srNJet]), 'nHT':len(signalRegion2fb[srNJet][stb])}

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

##closure table
#print "Results"
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
#print ' \\njet     & \ST & \HT     &\multicolumn{6}{c|}{$tt+$Jets}&\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{3}{c|}{Other EW bkg.}&\multicolumn{6}{c|}{total bkg.}\\\%\hline'
#print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'
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
#      print '&$'+varBin(htb)+'$' 
#      print ' & '+getNumString(res[srNJet][stb][htb]['TT_pred'],  res[srNJet][stb][htb]['TT_pred_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['TT_truth'], res[srNJet][stb][htb]['TT_truth_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['W_pred'],   res[srNJet][stb][htb]['W_pred_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['W_truth'],  res[srNJet][stb][htb]['W_truth_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['Rest_truth'], res[srNJet][stb][htb]['Rest_truth_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['tot_pred'], res[srNJet][stb][htb]['tot_pred_err'])\
#           +' & '+getNumString(res[srNJet][stb][htb]['tot_truth'],res[srNJet][stb][htb]['tot_truth_err']) +'\\\\'
#      if htb[1] == -1 : print '\\cline{2-24}'
#print '\\hline\end{tabular}}\end{center}\caption{Closure table for the background in the 0-tag regions, 3$fb^{-1}$}\label{tab:0b_rcscorr_Wbkg}\end{table}'

#closure table with correction


print "Results"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \ST & \HT     &\multicolumn{6}{c|}{$tt+$Jets}&\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{3}{c|}{Other EW bkg.}&\multicolumn{6}{c|}{total bkg.}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'

pred = {}

secondLine = False
for srNJet in sorted(signalRegions):
  pred[srNJet] = {}
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    pred[srNJet][stb] = {}
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      pred[srNJet][stb][htb] = {}
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      rCS_srPredErrorCandidatesTT = [abs(1 - res[srNJet][stb][htb]['rCS_crLowNJet_1b']['rCS']*kcs['tt'][stb][htb]['FitRatio']/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyTT']['rCS']),\
            res[srNJet][stb][htb]['rCS_srNJet_0b_onlyTT']['rCSE_sim']/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyTT']['rCS']]
      rCS_srPredErrorTT = max(rCS_srPredErrorCandidatesTT)
      rCS_srPredErrorCandidatesW = [abs(1 - res[srNJet][stb][htb]['rCS_W_crNJet_0b_corr']/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW']['rCS']),\
            res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW']['rCSE_sim']/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW']['rCS']]
      rCS_srPredErrorW = max(rCS_srPredErrorCandidatesW)
      #res[srNJet][stb][htb].update({'relClosureError':rCS_srPredError})
      ttPredictionVar = kcs['tt'][stb][htb]['FitRatio']**2*res[srNJet][stb][htb]['TT_pred_err']**2 + kcs['tt'][stb][htb]['FitRatioError']**2*res[srNJet][stb][htb]['TT_pred']**2
      ttPredictionPosPdgVar = kcs['tt'][stb][htb]['FitRatio']**2*(0.5*res[srNJet][stb][htb]['TT_pred_err'])**2 + kcs['tt'][stb][htb]['FitRatioError']**2*(0.5*res[srNJet][stb][htb]['TT_pred'])**2
      ttPredictionNegPdgVar = ttPredictionPosPdgVar
      ratio = res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_Ratio']
      if math.isnan(ratio): ratio = 0.
      ratioPosPdg = res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg_Ratio']
      if math.isnan(ratioPosPdg): ratioPosPdg = 0.
      ratioNegPdg = res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg_Ratio']
      if math.isnan(ratioNegPdg): ratioNegPdg = 0.
      WPredictionVar = res[srNJet][stb][htb]['W_pred_err']**2+(abs(1-ratio)*res[srNJet][stb][htb]['W_pred'])**2
      WPredictionPosPdgVar = res[srNJet][stb][htb]['W_PosPdg_pred_err']**2+(abs(1-ratioPosPdg)*res[srNJet][stb][htb]['W_PosPdg_pred'])**2
      WPredictionNegPdgVar = res[srNJet][stb][htb]['W_NegPdg_pred_err']**2+(abs(1-ratioNegPdg)*res[srNJet][stb][htb]['W_NegPdg_pred'])**2
      
      totalPrediction = res[srNJet][stb][htb]['TT_pred']*kcs['tt'][stb][htb]['FitRatio'] + res[srNJet][stb][htb]['W_pred'] + res[srNJet][stb][htb]['Rest_truth']
      totalPredictionPosPdg = 0.5*res[srNJet][stb][htb]['TT_pred']*kcs['tt'][stb][htb]['FitRatio'] + res[srNJet][stb][htb]['W_PosPdg_pred'] + res[srNJet][stb][htb]['Rest_PosPdg_truth']
      totalPredictionNegPdg = 0.5*res[srNJet][stb][htb]['TT_pred']*kcs['tt'][stb][htb]['FitRatio'] + res[srNJet][stb][htb]['W_NegPdg_pred'] + res[srNJet][stb][htb]['Rest_NegPdg_truth']
      totalPredictionError = sqrt(ttPredictionVar + WPredictionVar + res[srNJet][stb][htb]['Rest_truth_err']**2)
      totalPredictionPosPdgError = sqrt(ttPredictionPosPdgVar + WPredictionPosPdgVar + res[srNJet][stb][htb]['Rest_PosPdg_truth_err']**2)
      totalPredictionNegPdgError = sqrt(ttPredictionNegPdgVar + WPredictionNegPdgVar + res[srNJet][stb][htb]['Rest_NegPdg_truth_err']**2)
      
      
      print ' & '+getNumString(res[srNJet][stb][htb]['TT_pred']*kcs['tt'][stb][htb]['FitRatio'], sqrt(ttPredictionVar))\
           +' & '+getNumString(res[srNJet][stb][htb]['TT_truth'], res[srNJet][stb][htb]['TT_truth_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['W_pred'],   sqrt(WPredictionVar))\
           +' & '+getNumString(res[srNJet][stb][htb]['W_truth'],  res[srNJet][stb][htb]['W_truth_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['Rest_truth'], res[srNJet][stb][htb]['Rest_truth_err'])\
           +' & '+getNumString(totalPrediction, totalPredictionError)\
           +' & '+getNumString(res[srNJet][stb][htb]['tot_truth'],res[srNJet][stb][htb]['tot_truth_err']) +'\\\\'
      if htb[1] == -1 : print '\\cline{2-24}'
      #pred[srNJet][stb][htb].update({'relClosureErrorTT':rCS_srPredErrorTT, 'relClosureErrorW':rCS_srPredErrorW, 'tot_pred':totalPrediction, 'tot_pred_err':totalPredictionError, 'tot_PosPdg_pred': totalPredictionPosPdg,\
      #                                'tot_PosPdg_pred_err':totalPredictionPosPdgError, 'tot_NegPdg_pred':totalPredictionNegPdg, 'tot_NegPdg_pred_err':totalPredictionNegPdgError})
      res[srNJet][stb][htb].update({'relClosureErrorTT':rCS_srPredErrorTT, 'relClosureErrorW':rCS_srPredErrorW})
      res[srNJet][stb][htb]['tot_pred'] = totalPrediction
      res[srNJet][stb][htb]['tot_pred_err'] = totalPredictionError
      res[srNJet][stb][htb]['tot_PosPdg_pred'] = totalPredictionPosPdg
      res[srNJet][stb][htb]['tot_PosPdg_pred_err'] = totalPredictionPosPdgError
      res[srNJet][stb][htb]['tot_NegPdg_pred'] = totalPredictionNegPdg
      res[srNJet][stb][htb]['tot_NegPdg_pred_err'] = totalPredictionNegPdgError
      
print '\\hline\end{tabular}}\end{center}\caption{Closure table for the background with applied correction factors for \\ttJets, 0-tag regions, 3$fb^{-1}$}\label{tab:0b_rcscorr_Wbkg}\end{table}'
pickle.dump(res, file(path+prefix+'_estimationResults_pkl_updated','w'))


# W closure table
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
print ' \\njet & \ST & \HT &\multicolumn{6}{c|}{$W-$ Jets}&\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{6}{c|}{$W$ Jets}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'
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
      
#      muToElePlusMuErrorPosPdg = (res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu_PosPdg']['rCS']/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCS'])\
#                *sqrt(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu_PosPdg']['rCSE_sim']**2/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu_PosPdg']['rCS']**2\
#                +res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCSE_sim']**2/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCS']**2)
#
#      muToElePlusMuErrorNegPdg = (res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu_NegPdg']['rCS']/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'])\
#                *sqrt(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu_NegPdg']['rCSE_sim']**2/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu_NegPdg']['rCS']**2\
#                +res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim']**2/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCS']**2)
#
#      muToElePlusMuError = (res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu']['rCS']/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW']['rCS'])\
#                *sqrt(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu']['rCSE_sim']**2/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_mu']['rCS']**2\
#                +res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW']['rCSE_sim']**2/res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW']['rCS']**2)
      
      ratio = res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_Ratio']
      if math.isnan(ratio): ratio = 0.
      ratioPosPdg = res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg_Ratio']
      if math.isnan(ratioPosPdg): ratioPosPdg = 0.
      ratioNegPdg = res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg_Ratio']
      if math.isnan(ratioNegPdg): ratioNegPdg = 0.
      WPredictionVar = res[srNJet][stb][htb]['W_pred_err']**2+(abs(1-ratio)*res[srNJet][stb][htb]['W_pred'])**2
      WPredictionPosPdgVar = res[srNJet][stb][htb]['W_PosPdg_pred_err']**2+(abs(1-ratioPosPdg)*res[srNJet][stb][htb]['W_PosPdg_pred'])**2
      WPredictionNegPdgVar = res[srNJet][stb][htb]['W_NegPdg_pred_err']**2+(abs(1-ratioNegPdg)*res[srNJet][stb][htb]['W_NegPdg_pred'])**2
      
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(res[srNJet][stb][htb]['W_NegPdg_pred'],  sqrt(WPredictionNegPdgVar))\
           +' & '+getNumString(res[srNJet][stb][htb]['W_NegPdg_truth'], res[srNJet][stb][htb]['W_NegPdg_truth_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['W_PosPdg_pred'],  sqrt(WPredictionPosPdgVar))\
           +' & '+getNumString(res[srNJet][stb][htb]['W_PosPdg_truth'], res[srNJet][stb][htb]['W_PosPdg_truth_err'])\
           +' & '+getNumString(res[srNJet][stb][htb]['W_pred'],         sqrt(WPredictionVar))\
           +' & '+getNumString(res[srNJet][stb][htb]['W_truth'],        res[srNJet][stb][htb]['W_truth_err']) +'\\\\'
      if htb[1] == -1 : print '\\cline{2-21}'
print '\\hline\end{tabular}}\end{center}\caption{EFGH}\label{tab:0b_rcscorr_Wbkg}\end{table}'




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


## W Prediction table 1 not needed atm
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


# W Prediction table 2
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|c|}\\hline'
print ' \\njet & \ST & \HT &\multicolumn{6}{c|}{$R^{corr.}_{CS}(0b,2/3j)$}&\multicolumn{6}{c|}{$R_{CS,W_{jets}}(0b)$} & $\Delta\Phi(W,l)$\\\%\hline'
print '  & $[$GeV$]$ & $[$GeV$]$ & \multicolumn{3}{c}{pos. charge} & \multicolumn{3}{c|}{neg. charge} & \multicolumn{3}{c}{pos. charge} & \multicolumn{3}{c|}{neg. charge} & \\\\\hline '

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
      print '&$'+varBin(htb)+'$&'
#for i_htb, htb in enumerate(htreg):
#  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
#  for stb, dPhiCut in streg:
#    print '&$'+varBin(stb)+'$&'
#    #print '& & \multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (- charge)}&\multicolumn{3}{c|}{$R_{CS,W^{-}_{jets}}(0b,==5j)$}&\multicolumn{3}{c}{$R_{CS,W^{-}_{jets}}(0b,>=6j)$}\\\\hline'
#    #print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
      print  ' & '.join([getNumString(res[srNJet][stb][htb]['rCS_W_PosPdg_crNJet_0b_corr'], sqrt(res[srNJet][stb][htb]['rCS_Var_W_PosPdg_crNJet_0b_corr']),4), \
                    getNumString(res[srNJet][stb][htb]['rCS_W_NegPdg_crNJet_0b_corr'],    sqrt(res[srNJet][stb][htb]['rCS_Var_W_NegPdg_crNJet_0b_corr']),4), \
                    getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCS'],   res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_PosPdg']['rCSE_sim'],4),\
                    getNumString(res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'],   res[srNJet][stb][htb]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4),\
                    str(signalRegions[srNJet][stb][htb]['deltaPhi'])])+'\\\\'
      if htb[1] == -1 : print '\\cline{2-16}'
print
print '\\hline\end{tabular}}\end{center}\caption{hooli XYZ}\end{table}'

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

