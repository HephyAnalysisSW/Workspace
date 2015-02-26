import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin
from rCShelpers import *
from math import sqrt, pi
from localInfo import username

prefix = 'singleLeptonic_fullBkg'
res = pickle.load(file('/data/'+username+'/results2014/rCS_0b/'+prefix+'_estimationResults_pkl'))

streg = [[(250, 350), 1.], [(350, 450), 1.], [(450,-1), 1.]]
htreg = [(500,750),(750,1000),(1000,1250),(1250,-1)]
njreg = [(5,5),(6,-1)]
nSTbins = len(streg)

print "Results"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
print ' \HT     & \\njet & \ST     &\multicolumn{6}{c|}{$tt+$Jets}&\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{6}{c|}{total bkg.}\\\%\hline'
print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}          \\\\\hline'
for i_htb, htb in enumerate(htreg):
  if i_htb!=0:print '\\hline'
  print '\multirow{'+str(2*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(htb)+'$\end{sideways}}'
  #print '& & \multicolumn{6}{c|}{$t\overline{t}$+Jets}&\multicolumn{6}{c|}{$W$+Jets}&\multicolumn{6}{c}{total}\\\\'
  #print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
  #      '$} & \multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}\\\\\\hline'
  for srNJet in njreg:
    print '&\multirow{'+str(nSTbins)+'}{*}{'+varBin(srNJet)+'}'
    for stb, dPhiCut in streg:
      if stb[1] == -1 : print '&'
      print '&$'+varBin(stb)+'$'
      print ' & '+getNumString(res[htb][stb][srNJet]['TT_pred'], res[htb][stb][srNJet]['TT_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['TT_truth'], res[htb][stb][srNJet]['TT_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_pred'], res[htb][stb][srNJet]['W_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_truth'], res[htb][stb][srNJet]['W_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['tot_pred'], res[htb][stb][srNJet]['tot_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['tot_truth'], res[htb][stb][srNJet]['tot_truth_err']) +'\\\\'
      if stb[1] == -1 : print '\\cline{2-21}' 

print '\\hline\end{tabular}}\end{center}\caption{ABCD}\label{tab:0b_rcscorr_Wbkg}\end{table}'


print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
print ' \HT     & \\njet & \ST     &\multicolumn{6}{c|}{$W+$ Jets}&\multicolumn{6}{c|}{$W-$ Jets}&\multicolumn{6}{c|}{$W$ Jets}\\\%\hline'
print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}          \\\\\hline'
for i_htb, htb in enumerate(htreg):
  if i_htb!=0:print '\\hline'
  print '\multirow{'+str(2*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(htb)+'$\end{sideways}}'
  for srNJet in njreg:
    print '&\multirow{'+str(nSTbins)+'}{*}{'+varBin(srNJet)+'}'
    for stb, dPhiCut in streg:
      if stb[1] == -1 : print '&'
      print '&$'+varBin(stb)+'$'
      print ' & '+getNumString(res[htb][stb][srNJet]['W_NegPdg_pred'], res[htb][stb][srNJet]['W_NegPdg_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_NegPdg_truth'], res[htb][stb][srNJet]['W_NegPdg_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_PosPdg_pred'], res[htb][stb][srNJet]['W_PosPdg_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_PosPdg_truth'], res[htb][stb][srNJet]['W_PosPdg_truth_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_pred'], res[htb][stb][srNJet]['W_pred_err'])\
           +' & '+getNumString(res[htb][stb][srNJet]['W_truth'], res[htb][stb][srNJet]['W_truth_err']) +'\\\\'
      if stb[1] == -1 : print '\\cline{2-21}' 
print '\\hline\end{tabular}}\end{center}\caption{Comparison of corrected \Rcs values in the \zeroTag region and low jet multiplicities, because of \ttbar+jets contamination and \Rcs values in the high \njet signal region, separately for \wpJets and \wmJets.}\label{tab:0b_rcscorr_Wbkg}\end{table}'

print 

# for i_htb, htb in enumerate(htreg):
#   if i_htb!=0:print '\\hline'
#   print '& & \multicolumn{6}{c|}{total (+ charge)}&\multicolumn{6}{c|}{total (- charge)}&\multicolumn{6}{c}{total}\\\\'
#   print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
#         '$} & \multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}\\\\\\hline'
#   for stb, dPhiCut in streg:
#     for srNJet in njreg:
#       print '$'+nJetBinName(srNJet)+'$ & $'+varBinName(stb, 'S_{T}')+'$'+' & '+getNumString(res[htb][stb][srNJet]['tot_NegPdg_pred'], res[htb][stb][srNJet]['tot_NegPdg_pred_err'])\
#            +' & '+getNumString(res[htb][stb][srNJet]['tot_NegPdg_truth'], res[htb][stb][srNJet]['tot_NegPdg_truth_err'])\
#            +' & '+getNumString(res[htb][stb][srNJet]['tot_PosPdg_pred'], res[htb][stb][srNJet]['tot_PosPdg_pred_err'])\
#            +' & '+getNumString(res[htb][stb][srNJet]['tot_PosPdg_truth'], res[htb][stb][srNJet]['tot_PosPdg_truth_err'])\
#            +' & '+getNumString(res[htb][stb][srNJet]['tot_pred'], res[htb][stb][srNJet]['tot_pred_err'])\
#            +' & '+getNumString(res[htb][stb][srNJet]['tot_truth'], res[htb][stb][srNJet]['tot_truth_err']) +'\\\\'
# print
# print 'residual Backgrounds'
# print
# for i_htb, htb in enumerate(htreg):
#   if i_htb!=0:print '\\hline'
#   print '& & \multicolumn{3}{c|}{other Background (+ charge)}&\multicolumn{3}{c|}{other Background (- charge)}&\multicolumn{3}{c}{other Background}\\\\'
#   print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+\
#         '$} & &\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{simulation}\\\\\\hline'
#   for stb, dPhiCut in streg:
#     for srNJet in njreg:
#       print '$'+nJetBinName(srNJet)+'$ & $'+varBinName(stb, 'S_{T}')+'$'+' & '+getNumString(res[htb][stb][srNJet]['Rest_NegPdg_truth'], res[htb][stb][srNJet]['Rest_NegPdg_truth_err'])\
#            +' & '+getNumString(res[htb][stb][srNJet]['Rest_PosPdg_truth'], res[htb][stb][srNJet]['Rest_PosPdg_truth_err'])\
#            +' & '+getNumString(res[htb][stb][srNJet]['Rest_truth'], res[htb][stb][srNJet]['Rest_truth_err']) +'\\\\'
# print

print "rCS(TT) comparison used for rCS(W) correction"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|rrr|rrr|rrr|}\\hline'
print ' \HT$[$GeV$]$     & \ST$[$GeV$]$     &\multicolumn{3}{c|}{1b,2/3j}&\multicolumn{3}{c|}{1b,tt,2/3j}&\multicolumn{3}{c|}{0b,tt,2/3j}\\\\\hline'
for i_htb, htb in enumerate(htreg):
  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
  for stb, dPhiCut in streg:
    print '&$'+varBin(stb)+'$&'
    for srNJet in njreg[:1]:
      #print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
       print   ' & '.join([getNumString(res[htb][stb][srNJet]['rCS_crNJet_1b']['rCS'], res[htb][stb][srNJet]['rCS_crNJet_1b']['rCSE_sim'],3), \
                      getNumString(res[htb][stb][srNJet]['rCS_crNJet_1b_onlyTT']['rCS'], res[htb][stb][srNJet]['rCS_crNJet_1b_onlyTT']['rCSE_sim'],3),\
                      getNumString(res[htb][stb][srNJet]['rCS_crNJet_0b_onlyTT']['rCS'], res[htb][stb][srNJet]['rCS_crNJet_0b_onlyTT']['rCSE_sim'],3)])+'\\\\'
    if stb[1] == -1 : print '\\hline'
print '\end{tabular}}\end{center}\caption{YYY}\label{tab:0b_rcscorr_Wbkg}\end{table}'
print

print "RCS corr comparison"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|rrr|rrr|rrr|}\\hline'
print ' \HT$[$GeV$]$     & \ST$[$GeV$]$     &\multicolumn{3}{c|}{0b,2/3j}&\multicolumn{3}{c|}{0b,W,2/3j}&\multicolumn{3}{c|}{0b,W,2/3j}\\\\\hline'
for i_htb, htb in enumerate(htreg):
  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
  for stb, dPhiCut in streg:
    print '&$'+varBin(stb)+'$&'
    #print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
    print   ' & '.join([getNumString(res[htb][stb][njreg[0]]['rCS_W_crNJet_0b_corr'],sqrt(res[htb][stb][njreg[0]]['rCS_Var_W_crNJet_0b_corr']),4), \
                    getNumString(res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW']['rCS'], res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW']['rCSE_sim'],4),\
                    getNumString(res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW']['rCS'], res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW']['rCSE_sim'],4)])+'\\\\'
    if stb[1] == -1 : print '\\hline'

print '\end{tabular}}\end{center}\caption{YYY}\label{tab:0b_rcscorr_Wbkg}\end{table}'
print


print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|rrr|rrr|rrr|}\\hline'
print ' \HT$[$GeV$]$     & \ST$[$GeV$]$     &\multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (- charge)}&\multicolumn{3}{c|}{$R_{CS,W^{-}_{jets}}(0b,==5j)$}&\multicolumn{3}{c|}{$R_{CS,W^{-}_{jets}}(0b,>=6j)$}\\\\\hline'
for i_htb, htb in enumerate(htreg):
  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
  for stb, dPhiCut in streg:
    print '&$'+varBin(stb)+'$&'
    #print '& & \multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (- charge)}&\multicolumn{3}{c|}{$R_{CS,W^{-}_{jets}}(0b,==5j)$}&\multicolumn{3}{c}{$R_{CS,W^{-}_{jets}}(0b,>=6j)$}\\\\hline'
    #print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
    print  ' & '.join([getNumString(res[htb][stb][njreg[0]]['rCS_W_PosPdg_crNJet_0b_corr'],sqrt(res[htb][stb][njreg[0]]['rCS_Var_W_PosPdg_crNJet_0b_corr']),4), \
                    getNumString(res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW_PosPdg']['rCS'], res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW_PosPdg']['rCSE_sim'],4),\
                    getNumString(res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW_PosPdg']['rCS'], res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW_PosPdg']['rCSE_sim'],4)])+'\\\\'
    if stb[1] == -1 : print '\\hline'
print  
print '& & \multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (+ charge)}&\multicolumn{3}{c|}{$R_{CS,W^{+}_{jets}}(0b,==5j)$}&\multicolumn{3}{c|}{$R_{CS,W^{+}_{jets}}(0b,>=6j)$}\\\\\hline'
for i_htb, htb in enumerate(htreg):
  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
  for stb, dPhiCut in streg:
    print '&$'+varBin(stb)+'$&'
    #print '& & \multicolumn{3}{c|}{$R^{corr.}_{CS}(0b,2/3j)$ (+ charge)}&\multicolumn{3}{c|}{$R_{CS,W^{+}_{jets}}(0b,==5j)$}&\multicolumn{3}{c}{$R_{CS,W^{+}_{jets}}(0b,>=6j)$}\\\\hline'
    #print '$'+varBinName(htb, 'H_{T}')+'$&$'+varBinName(stb, 'S_{T}')+'$ & '+\
    print    ' & '.join([getNumString(res[htb][stb][njreg[0]]['rCS_W_NegPdg_crNJet_0b_corr'],sqrt(res[htb][stb][njreg[0]]['rCS_Var_W_NegPdg_crNJet_0b_corr']),4), \
                    getNumString(res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'], res[htb][stb][njreg[0]]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4),\
                    getNumString(res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW_NegPdg']['rCS'], res[htb][stb][njreg[1]]['rCS_srNJet_0b_onlyW_NegPdg']['rCSE_sim'],4)])+'\\\\'
    if stb[1] == -1 : print '\\hline'
print
print '\end{tabular}}\end{center}\caption{YYY}\label{tab:0b_rcscorr_Wbkg}\end{table}'


print 
print "rCS(TT) comparison used for tt estimation"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|}\\hline'
print ' \HT$[$GeV$]$ & $n_{jet}$  & \ST$[$GeV$]$     &\multicolumn{3}{c|}{1b,4/5j}&\multicolumn{3}{c|}{1b,tt,4/5j}&\multicolumn{3}{c|}{0b,tt,4/5j}\\\\\hline'
for i_htb, htb in enumerate(htreg):
  if i_htb!=0:print '\\hline'
  print '\multirow{'+str(nSTbins)+'}{*}{$'+varBin(htb)+'$}'
#  print '& & \multicolumn{6}{c|}{$t\overline{t}$+Jets}&\multicolumn{6}{c|}{$W$+Jets}&\multicolumn{6}{c}{total}\\\\'
  #print '\multicolumn{2}{c|}{$'+varBinName(htb, 'H_{T}')+"$}&"\
  #    + "\multicolumn{3}{c|}{$R_{CS}(1b,4/5j)$}&\multicolumn{3}{c|}{$R_{CS,t\overline{t}}(1b,4/5j)$}&\multicolumn{3}{c}{$R_{CS,t\overline{t}}(0b)$}\\\\\\hline"
  for srNJet in njreg:
    print '&\multirow{'+str(nSTbins)+'}{*}{'+varBin(srNJet)+'}'
    for stb, dPhiCut in streg:
      print '&$'+varBin(stb)+'$&'
      #print '$'+nJetBinName(srNJet)+'$ & $'+varBinName(stb, 'S_{T}')+'$'+' & '+\
      print   ' & '.join([getNumString(res[htb][stb][srNJet]['rCS_crLowNJet_1b']['rCS'], res[htb][stb][srNJet]['rCS_crLowNJet_1b']['rCSE_sim'],acc=3), \
                      getNumString(res[htb][stb][srNJet]['rCS_crLowNJet_1b_onlyTT']['rCS'], res[htb][stb][srNJet]['rCS_crLowNJet_1b_onlyTT']['rCSE_sim'],acc=3),\
                      getNumString(res[htb][stb][srNJet]['rCS_srNJet_0b_onlyTT']['rCS'], res[htb][stb][srNJet]['rCS_srNJet_0b_onlyTT']['rCSE_sim'],acc=3)])+'\\\\'
      if stb[1] == -1 : print '\\hline'
print '\end{tabular}}\end{center}\caption{rCS(TT) comparison used for tt estimation}\label{tab:0b_rcscorr_Wbkg}\end{table}'

# print "signal yields (+charge)"
# print
# for i_htb, htb in enumerate(htreg):
#   for stb, dPhiCut in streg:
#     for srNJet in njreg:
#       rCS_sr_Name_0b = nameAndCut(stb,htb,srNJet,btb=(0,0), presel=presel, btagVar = 'nBTagCMVA')#for Check 
#       strings=[]
#       for s in signals:
#         sig =     getYieldFromChain(s['chain'], 'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+'>'+str(dPhiCut), weight = "weight")
#         sigErr  = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+'>'+str(dPhiCut), weight = "weight*weight")
#         strings.append( getNumString(sig, sigErr, 3) )
#       print " , ".join(strings), rCS_sr_Name_0b
# print
# print "signal yields (-charge)"
# print
# for i_htb, htb in enumerate(htreg):
#   for stb in streg:
#     for srNJet in njreg:
#       rCS_sr_Name_0b = nameAndCut(stb,htb,srNJet,btb=(0,0), presel=presel, btagVar = 'nBTagCMVA')#for Check 
#       strings=[]
#       for s in signals:
#         sig =     getYieldFromChain(s['chain'], 'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+'>'+str(dPhiCut), weight = "weight")
#         sigErr  = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+rCS_sr_Cut_0b+"&&"+dPhiStr+'>'+str(dPhiCut), weight = "weight*weight")
#         strings.append( getNumString(sig, sigErr, 3) )
#       print " , ".join(strings), rCS_sr_Name_0b
# print
