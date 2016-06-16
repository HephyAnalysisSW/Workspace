import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin
from rCShelpers import *
from math import sqrt, pi
#from Workspace.HEPHYPythonTools.user import username

prefix = 'singleLeptonic_Phys14V3'
#res = pickle.load(file('/data/'+username+'/results2015/rCS_0b/'+prefix+'_estimationResults_pkl'))

#signalregions = 

#streg = [(250, 350), (350, 450), (450,-1)]
#htreg = [(500,750),(750,1000),(1000,1250),(1250,-1)]
#njreg = [(5,5),(6,7),(8,-1)]
#nSTbins = len(streg)
#nHTbins = len(htreg)
#nJetBins = len(njreg)
#
#
#print "Results"
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|c|c|c|}\\hline'
#print ' \\njet     & \ST $[$GeV$]$ & \HT $[$GeV$]$ & Bkg & Model 1 & Model 2 & Model 3\\\ \\hline'
##print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'
#for i_njb, njb in enumerate(njreg):
#  print '\\hline'
#  if i_njb!=0:print '\\hline'
#  print '\multirow{'+str(nHTbins*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(njb)+'$\end{sideways}}'
#  #print '& & \multicolumn{6}{c|}{$t\overline{t}$+Jets}&\multicolumn{6}{c|}{$W$+Jets}&\multicolumn{6}{c}{total}\\\\'
#  #print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
#  #      '$} & \multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}\\\\\\hline'
#  for stb in streg:
#    print '&\multirow{'+str(nHTbins)+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in htreg:
#      if not first: print '&'
#      first = False
#      ##if stb[1] == -1 : print '&'
#      #flag = True
#      #try:
#      #  res[njb][stb][htb]
#      #except Exception:
#      #  flag = False
#      print '&$'+varBin(htb)+'$'
#      print ' & '+str(round(res[njb][htb][stb]['Bkg'],3))\
#           +' & '+str(round(res[njb][htb][stb]['Model1'],3))\
#           +' & '+str(round(res[njb][htb][stb]['Model2'],3))\
#           +' & '+str(round(res[njb][htb][stb]['Model3'],3)) + '\\\\'
#      if htb[1] == -1 : print '\\cline{2-7}'
#  #print '\\hline'
#print '\\hline\end{tabular}}\end{center}\caption{ABCD}\label{tab:0b_rcscorr_Wbkg}\end{table}'

signalRegions = regionsHTcomb

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

res = signalRegions

#closure table
print "Closure table"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rr|rr|rr|}\\hline'
print ' \\njet     & \LT & \HT     & Bkg & \multicolumn{2}{c|}{1.0/0.7}&\multicolumn{2}{c|}{1.2/0.8}&\multicolumn{2}{c|}{1.5/0.1}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$ & & yield & FOM & yield & FOM & yield & FOM  \\\\\hline'

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
      print ' & '+str(round(res[srNJet][stb][htb]['B'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['S1000'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['FOM_S10'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['S1200'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['FOM_S12'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['S1500'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['FOM_S15'],3)) + '\\\\'

      if htb[1] == -1 : print '\\cline{2-10}'
print '\\hline\end{tabular}}\end{center}\caption{Yields and FOMs in signal regions, 10fb$^{-1}$}\end{table}'



print "Closure table"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rr|rr|rr|}\\hline'
print ' \\njet     & \LT & \HT     &  \multicolumn{2}{c|}{MB}&\multicolumn{2}{c|}{TT SB}&\multicolumn{2}{c|}{W SB}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$ & CR & SR & CR & SR & CR & SR  \\\\\hline'

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
      print ' & '+str(round(res[srNJet][stb][htb]['BCR'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['B'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['TTSB_CR'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['TTSB_SR'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['WSB_CR'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['WSB_SR'],3)) + '\\\\'

      if htb[1] == -1 : print '\\cline{2-9}'
print '\\hline\end{tabular}}\end{center}\caption{Yields in sideband regions, 10fb$^{-1}$}\end{table}'


