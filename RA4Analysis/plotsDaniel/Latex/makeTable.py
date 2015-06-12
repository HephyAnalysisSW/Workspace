import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin
#from rCShelpers import *
from math import sqrt, pi
#from localInfo import username

prefix = 'singleMuonic_fullBkg'
res = pickle.load(file('/afs/hephy.at/user/d/dspitzbart/www/subBkgWhard/500htJet30j/150st/nJet30LEq8/yields.pkl'))

streg = [[(250, 350), 1.], [(350, 450), 1.], [(450,-1), 1.]]
htreg = [(500,750),(750,1000),(1000,1250),(1250,-1)]
njreg = [(5,5),(6,-1)]
nSTbins = len(streg)

print "Results"
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
#print ' \HT     & \\njet & \ST     &\multicolumn{6}{c|}{$tt+$Jets}&\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{6}{c|}{total bkg.}\\\%\hline'
#print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}          \\\\\hline'
#for i_htb, htb in enumerate(htreg):
#  if i_htb!=0:print '\\hline'
#  print '\multirow{'+str(2*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(htb)+'$\end{sideways}}'
#  #print '& & \multicolumn{6}{c|}{$t\overline{t}$+Jets}&\multicolumn{6}{c|}{$W$+Jets}&\multicolumn{6}{c}{total}\\\\'
#  #print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
#  #      '$} & \multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}\\\\\\hline'
#  for srNJet in njreg:
#    print '&\multirow{'+str(nSTbins)+'}{*}{'+varBin(srNJet)+'}'
#    for stb, dPhiCut in streg:
#      if stb[1] == -1 : print '&'
#      print '&$'+varBin(stb)+'$'
#      print ' & '+getNumString(res[htb][stb][srNJet]['TT_pred'], res[htb][stb][srNJet]['TT_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['TT_truth'], res[htb][stb][srNJet]['TT_truth_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['W_pred'], res[htb][stb][srNJet]['W_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['W_truth'], res[htb][stb][srNJet]['W_truth_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['tot_pred'], res[htb][stb][srNJet]['tot_pred_err'])\
#           +' & '+getNumString(res[htb][stb][srNJet]['tot_truth'], res[htb][stb][srNJet]['tot_truth_err']) +'\\\\'
#      if stb[1] == -1 : print '\\cline{2-21}' 
#
#print '\\hline\end{tabular}}\end{center}\caption{ABCD}\label{tab:0b_rcscorr_Wbkg}\end{table}'

print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|c|c|c|c|c|rrr|rrr|}\\hline'
print ' \\njet & \\ttJets  & 0b & 1b  & 0b/1b & 0b($\\Delta\Phi<0$) & 0b($\\Delta\Phi>0$) & 1b($\\Delta\Phi<0$) & 1b($\\Delta\Phi>0$) & \multicolumn{3}{c|}{\\Rcs(0b)} & \multicolumn{3}{c|}{\\Rcs(1b)}\\\\\hline'
#print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}     

numberOfSubBkg = 3
entries = len(res)
i=0
multiKey = 0

while i < entries:
  if res[i+1]['totalYield']>0:
    norm = res[i]['totalYield']/res[i+1]['totalYield']
  else:
    norm = 1.
  if multiKey == 0:
    print '\\hline\multirow{'+str(numberOfSubBkg+1)+'}{*}{\\begin{sideways}$'+varBin(res[i]['njets'])+'$\end{sideways}}'
  print ' &' + res[i]['title']\
    +' & ' +str(round(res[i]['totalYield'],2))\
    +' & ' +str(round(res[i+1]['totalYield'],2))\
    +' & ' +str(round(norm,2))\
    +' & ' +str(round(res[i]['controlYield'],2))\
    +' & ' +str(round(res[i]['signalYield'],2))\
    +' & ' +str(round(res[i+1]['controlYield'],2))\
    +' & ' +str(round(res[i+1]['signalYield'],2))\
    +' & ' +str(round(res[i]['rcs'],3)) + ' & $\pm$ & ' + str(round(res[i]['rcsError'],3))\
    +' & ' +str(round(res[i+1]['rcs'],3))+ ' & $\pm$ & ' + str(round(res[i+1]['rcsError'],3)) + '\\\\'    
  i = i+2
  multiKey = multiKey + 1
  if multiKey == numberOfSubBkg+1:
    multiKey = 0
    print '\\hline'
  else:
    print '\\cline{2-15}'

#
#for bkg in res:
#  print bkg['title']\
#    +' & ' +str(round(bkg['yield0bTotal'],2))\
#    +' & ' +str(round(bkg['yield1bTotal'],2))\
#    +' & ' +str(round(bkg['norm'],2))\
#    +' & ' +str(round(bkg['yield0bC'],2))\
#    +' & ' +str(round(bkg['yield0bS'],2))\
#    +' & ' +str(round(bkg['yield1bC'],2))\
#    +' & ' +str(round(bkg['yield1bS'],2))\
#    +' & ' +str(round(bkg['rcs0b'],4))\
#    +' & ' +str(round(bkg['rcs1b'],4))+'\\\\\hline'

print '\end{tabular}}\end{center}\caption{ABCD}\end{table}'



