import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin
#from rCShelpers import *
from math import sqrt, pi
#from localInfo import username

prefix = 'singleMuonic_fullBkg'
res = pickle.load(file('/afs/hephy.at/user/d/dspitzbart/www/softLepYields/yields_withLimitAndSig.pkl'))

signal = 5


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

#print '\\begin{center}\\begin{longtable}{| p{2cm} | p{2.2cm} | p{1.6cm} | p{1.8cm} | p{2.cm} | p{2.2cm} | p{2.2cm} |}\\hline'
#print '\\ST & \\HT & \\njet & BackGND & ','\\multicolumn{3}{|c|}{$',res[0]['signalSampleNames'][signal],'$} \\\ \\hline'
#print '$[$GeV$]$ & $[$GeV$]$ & & Yield & Yield & Significance & Limit \\\ \\hline'
#print '\\endfirsthead'
#print '\\multicolumn{7}{c}'
#print '{\\tablename\\ \\thetable\\ -- \\textit{Continued from previous page}} \\\ \\hline'
#print '\\ST & \\HT & \\njet & BackGND & ','\\multicolumn{3}{|c|}{$',res[0]['signalSampleNames'][signal],'$} \\\ \\hline'
#print '$[$GeV$]$ & $[$GeV$]$ & & Yield & Yield & Significance & Limit \\\ \\hline'
#print '\\endhead'
#print '\\hline \\multicolumn{7}{r}{\\textit{Continued on next page}} \\\ '
#print '\\endfoot \\hline \\endlastfoot'

print '\\begin{center}\\begin{sidewaystable}\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}\\hline'
print '\\ST & \\HT & \\njet & BackGND & ','\\multicolumn{3}{|c|}{1000/325/300} & \\multicolumn{3}{|c|}{1000/315/300} & \\multicolumn{3}{|c|}{1000/310/300}  \\\ \\hline'
print '$[$GeV$]$ & $[$GeV$]$ & & Yield & Yield & Signif. & Limit & Yield & Signif. & Limit & Yield & Signif. & Limit \\\ \\hline'

for sample in res:
  print str(sample['st'])\
    +' & ' +str(sample['ht'])\
    +' & ' +str(sample['njet'])\
    +' & ' +str(round(sample['bkgYield'],3))
  for i in range(3):
    print ' & ' +str(round(sample['signalYields'][i],3))\
    +' & ' +str(round(sample['Significances'][i],3))\
    +' & ' +str(round(sample['Limits'][i],3))#+ '\\\ \\hline'
  print '\\\ \\hline'
print '\\end{tabular}\\caption{Yields, Significance and Limits for compressed Signals with $'+res[0]['variable']+' \geq '+str(res[0]['signalCut'])+'$}\\end{sidewaystable}\\end{center}'

print '\\begin{center}\\begin{sidewaystable}\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}\\hline'
print '\\ST & \\HT & \\njet & BackGND & ','\\multicolumn{3}{|c|}{1400/315/300} & \\multicolumn{3}{|c|}{1000/800/700} & \\multicolumn{3}{|c|}{800/305/300}  \\\ \\hline'
print '$[$GeV$]$ & $[$GeV$]$ & & Yield & Yield & Signif. & Limit & Yield & Signif. & Limit & Yield & Signif. & Limit \\\ \\hline'

for sample in res:
  print str(sample['st'])\
    +' & ' +str(sample['ht'])\
    +' & ' +str(sample['njet'])\
    +' & ' +str(round(sample['bkgYield'],3))
  for i in range(3,6):
    print ' & ' +str(round(sample['signalYields'][i],3))\
    +' & ' +str(round(sample['Significances'][i],3))\
    +' & ' +str(round(sample['Limits'][i],3))#+ '\\\ \\hline'
  print '\\\ \\hline'
print '\\end{tabular}\\caption{Yields, Significance and Limits for compressed Signals with $'+res[0]['variable']+' \geq '+str(res[0]['signalCut'])+'$}\\end{sidewaystable}\\end{center}'

#print '\\caption{$'+res[0]['signalSampleNames'][signal]+'$ with $'+res[0]['variable']+' \geq '+str(res[0]['signalCut'])+'$}\\end{longtable}\\end{center}'



#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|}\\hline'
#print ' \\ttJets     & 0b & 1b  & 1b/0b & 0b($\\Delta\Phi<0$) & 0b($\\Delta\Phi>0$) & 1b($\\Delta\Phi<0$) & 1b($\\Delta\Phi>0$) & \\Rcs(0b) & \\Rcs(1b)\\\\\hline'
##print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}     
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
#
#print '\\end{tabular}}\\end{center}\\caption{ABCD}\\end{table}'



