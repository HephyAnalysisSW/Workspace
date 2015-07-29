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

streg = [(250, 350), (350, 450), (450,-1)]
htreg = [(500,750),(750,1000),(1000,1250),(1250,-1)]
njreg = [(5,5),(6,7),(8,-1)]
nSTbins = len(streg)
nHTbins = len(htreg)
nJetBins = len(njreg)


print "Results"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|c|c|c|}\\hline'
print ' \\njet     & \ST $[$GeV$]$ & \HT $[$GeV$]$ & Bkg & Model 1 & Model 2 & Model 3\\\ \\hline'
#print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'
for i_njb, njb in enumerate(njreg):
  print '\\hline'
  if i_njb!=0:print '\\hline'
  print '\multirow{'+str(nHTbins*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(njb)+'$\end{sideways}}'
  #print '& & \multicolumn{6}{c|}{$t\overline{t}$+Jets}&\multicolumn{6}{c|}{$W$+Jets}&\multicolumn{6}{c}{total}\\\\'
  #print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
  #      '$} & \multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}\\\\\\hline'
  for stb in streg:
    print '&\multirow{'+str(nHTbins)+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in htreg:
      if not first: print '&'
      first = False
      ##if stb[1] == -1 : print '&'
      #flag = True
      #try:
      #  res[njb][stb][htb]
      #except Exception:
      #  flag = False
      print '&$'+varBin(htb)+'$'
      print ' & '+str(round(res[njb][htb][stb]['Bkg'],3))\
           +' & '+str(round(res[njb][htb][stb]['Model1'],3))\
           +' & '+str(round(res[njb][htb][stb]['Model2'],3))\
           +' & '+str(round(res[njb][htb][stb]['Model3'],3)) + '\\\\'
      if htb[1] == -1 : print '\\cline{2-7}'
  #print '\\hline'
print '\\hline\end{tabular}}\end{center}\caption{ABCD}\label{tab:0b_rcscorr_Wbkg}\end{table}'
