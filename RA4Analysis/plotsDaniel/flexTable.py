import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin
from rCShelpers import *
from math import sqrt, pi
from localInfo import username

prefix = 'singleLeptonic_Phys14V3'
res = pickle.load(file('/data/'+username+'/results2015/rCS_0b/'+prefix+'_estimationResults_pkl'))

streg = [(250, 350), (350, 450), (450,-1)]
htreg = [(500,750),(750,1000),(1000,1250),(1250,-1)]
njreg = [(5,5),(6,7),(8,-1)]
nSTbins = len(streg)
nHTbins = len(htreg)
nJetBins = len(njreg)


print "Results"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|c|c|c|}\\hline'
print ' \\njet     & \ST $[$GeV$]$ & \HT $[$GeV$]$ & Bkg & Model 1 & Model 2 & Model 3\\hline'
#print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'
for i_njb, njb in enumerate(njreg):
  print '\\hline'
  if i_njb!=0:print '\\hline'
  print '\multirow{'+str(nHTBins*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(njb)+'$\end{sideways}}'
  #print '& & \multicolumn{6}{c|}{$t\overline{t}$+Jets}&\multicolumn{6}{c|}{$W$+Jets}&\multicolumn{6}{c}{total}\\\\'
  #print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
  #      '$} & \multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}\\\\\\hline'
  for stb in streg:
    print '&\multirow{'+str(nHTbins)+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in htreg:
      if not first: print '&'
      first = False
      #if stb[1] == -1 : print '&'
      try:  
      print '&$'+varBin(stb)+'$'
      print ' & '+getNumString(res[htb][stb][srNJet]['TT_pred'], res[htb][stb][srNJet]['TT_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['TT_truth'], res[htb][stb][srNJet]['TT_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_pred'], res[htb][stb][srNJet]['W_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_truth'], res[htb][stb][srNJet]['W_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['tot_pred'], res[htb][stb][srNJet]['tot_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['tot_truth'], res[htb][stb][srNJet]['tot_truth_err']) +'\\\\'
      if stb[1] == -1 : print '\\cline{2-21}'
  #print '\\hline'
print '\\hline\end{tabular}}\end{center}\caption{ABCD}\label{tab:0b_rcscorr_Wbkg}\end{table}'
