import ROOT
import pickle
import copy, os, sys

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *
from Workspace.HEPHYPythonTools.user import username
from math import *

#signalRegion = signalRegion3fb

signalRegion = {(3, 4): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #3-4jets QCD and W+jets control region
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (4, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #4-5jets TTbar control region
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (5, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}},  #signal regions
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0}}},
                (6, 7): {(250, 350): {(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                          (450, -1): {(500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (8, -1): {(250, 350):{(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                          (350, 450):{(500, -1):   {'deltaPhi': 0.75}},
                          (450, -1): {(500, -1):   {'deltaPhi': 0.75}}}
}

#signalRegion = {(3, 4): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}, #QCD CR
#                (4, 5): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}, #TTbar CR 1b 
#                (5, 5): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}, #SR 
#                (6,-1): {(250, -1): {(500, -1):   {'deltaPhi': 0.5}}}} #SR 
btreg = [(0,0), (1,1), (2,2)] #1b and 2b estimates are needed for the btag fit

#add the path where the pickle files are located
path = '/data/'+username+'/results2015/QCDEstimation/'
pickleFile = '20151028_QCDestimation_pkl'
bins = pickle.load(file(path+pickleFile))

def getNumString(n,ne, acc=2):    ##For printing table 
  if type(n) is float and type(ne) is float:
    return str(round(n,acc))+'&$\pm$&'+str(round(ne,acc))
  #if type(n) is str and type(ne) is str: 
  else:
    return n +'&$\pm$&'+ ne

def getQCDfraction(Bkg, Bkg_err, QCD, QCD_err):
  if Bkg>0:
    res = QCD/Bkg
    if QCD>0:
      res_err = res*sqrt(Bkg_err**2/Bkg**2 + QCD_err**2/QCD**2)
      return res, res_err
    else:
      res_err = float('nan')
      return res, res_err
  else:
    res = float('nan')
    res_err = float('nan')
    return res, res_err

#side band for tt+jets estimation 4-5j, 1b
ttCRbtb = (1,1)

#get the ratios from the Lp template fit
#side band for QCD estimation 3-4j, 0b
CR = (3,4)  
btb = (0,0)
ratio={}
for srNJet in sorted(signalRegion):
  ratio[srNJet] = {}
  for stb in sorted(signalRegion[srNJet]):
    ratio[srNJet][stb] = {}
    for htb in sorted(signalRegion[srNJet][stb]):
      #res = pickle.load(file(path+'QCDyieldFromTemplateFit_'+nameAndCut(stb, htb, CR, btb=btb, presel="(1)", charge="", btagVar = 'nBJetMediumCSV30')[0]+'_pkl'))
      res = pickle.load(file(path+pickleFile))
      ratio[srNJet][stb][htb] = {'F_seltoantisel':res[CR][stb][htb][btb]['F_seltoantisel'], 'F_seltoantisel_err':res[CR][stb][htb][btb]['F_seltoantisel_err'],\
                                 'NQCDSelMC':res[CR][stb][htb][btb]['NQCDSelMC'], 'NQCDSelMC_err':res[CR][stb][htb][btb]['NQCDSelMC_err'],\
                                 'NQCDFit':res[CR][stb][htb][btb]['QCD']['yield'], 'NQCDFit_err':sqrt(res[CR][stb][htb][btb]['QCD']['yieldVar']),\
                                 'NDATASel':res[CR][stb][htb][btb]['NDATASel'], 'NDATASel_err':res[CR][stb][htb][btb]['NDATASel_err']}

#nAntiSel = pickle.load(file(path+'RcsQCD3fb-1_pkl'))
#nCRAntiSel = pickle.load(file(path+'RcsQCD_4-5j_1b_3fb-1_pkl'))

rowsNJet = {}
rowsSt = {}
for srNJet in sorted(signalRegion):
  rowsNJet[srNJet] = {}
  rowsSt[srNJet] = {}
  rows = 0
  for stb in sorted(signalRegion[srNJet]):
    rows += len(signalRegion[srNJet][stb])
    rowsSt[srNJet][stb] = {'n':len(signalRegion[srNJet][stb])}
  rowsNJet[srNJet] = {'nST':len(signalRegion[srNJet]), 'n':rows}

#print only yields and ratios from the CR
print " QCD estimation and ratios in CR"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|}\\hline'
print ' \\njet     & \ST & \HT     &\multicolumn{9}{c|}{QCD multijets}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}&\multicolumn{3}{c|}{$F_{sel-to-antisel}$}\\\\\hline'
print '\multirow{'+str(len(ratio))+'}{*}{\\begin{sideways}$'+varBin(CR)+'$\end{sideways}}'
for njb in sorted(ratio):
  for stb in sorted(ratio[njb]):
    print '&\multirow{'+str(len(ratio[njb]))+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(ratio[njb][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(ratio[njb][stb][htb]['NQCDFit'],ratio[njb][stb][htb]['NQCDFit_err'])\
           +' & '+getNumString(ratio[njb][stb][htb]['NQCDSelMC'],ratio[njb][stb][htb]['NQCDSelMC_err'])\
           +' & '+getNumString(ratio[njb][stb][htb]['F_seltoantisel'],ratio[njb][stb][htb]['F_seltoantisel_err'])+'\\\\'
print '\\hline\end{tabular}}\end{center}\caption{Closure and Ratio for QCD background in the CR, 0-tag regions, 3$fb^{-1}$}\label{tab:0b_QCDpredCR}\end{table}'

#print 'Results QCD in 4-5j, 1b CR'
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|}\\hline'
#print ' \\njet     & \ST & \HT     &\multicolumn{6}{c|}{QCD multijets in 4-5j,1b CR}\\\%\hline'
#print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}\\\\\hline'
##print yields in the CR 4-5j,1b
#print '\\hline'
#secondLine = False
#for srNJet in sorted(signalRegion):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{13}{*}{\\begin{sideways}$[4,5]$\end{sideways}}'
#  for stb in sorted(signalRegion[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegion[srNJet][stb]):
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$'
#      print ' & '+getNumString(ratio[srNJet][stb][htb]['F_seltoantisel']*bins[srNJet][stb][htb][ttCRbtb]['NDATAAntiSel'],\
#                 sqrt((ratio[srNJet][stb][htb]['F_seltoantisel_err']**2*bins[srNJet][stb][htb][ttCRbtb]['NDATAAntiSel']**2)+(bins[srNJet][stb][htb][ttCRbtb]['NDATAAntiSel_err']**2*ratio[srNJet][stb][htb]['F_seltoantisel']**2)))\
#           +' & '+getNumString(bins[srNJet][stb][htb][ttCRbtb]['NQCDSelMC'], bins[srNJet][stb][htb][ttCRbtb]['NQCDSelMC_err'])\
#print '\\hline\end{tabular}}\end{center}\caption{Closure table for QCD background , 0-tag regions, 3$fb^{-1}$}\label{tab:0b_QCDpred}\end{table}'

#print RCS factors in the CR 4-5j, 1b
#print 'RCS in CR 4-5j,1b'
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrr|}\\hline'
#print ' \\njet     & \ST & \HT & \DF    &\multicolumn{6}{c|}{Transfer factors in 4-5j,1b CR}\\\%\hline'
#print ' & $[$GeV$]$ &$[$GeV$]$& &\multicolumn{3}{c}{$R^{antiselected}_{CS}$}&\multicolumn{3}{c|}{$R^{selected}_{CS}$}\\\\\hline'
#print '\\hline'
#secondLine = False
#for srNJet in sorted(signalRegion):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{13}{*}{\\begin{sideways}$[4,5]$\end{sideways}}'
#  for stb in sorted(signalRegion[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegion[srNJet][stb]):
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$ &'+str(signalRegion[srNJet][stb][htb]['deltaPhi'])
#      print ' & '+getNumString(bins[srNJet][stb][htb][ttCRbtb]['rCSantiSelectedDATA']['rCS'], bins[srNJet][stb][htb][ttCRbtb]['rCSantiSelectedDATA']['rCSE_pred'],3)\
#           +' & '+getNumString(bins[srNJet][stb][htb][ttCRbtb]['rCSselectedData']['rCS'], bins[srNJet][stb][htb][ttCRbtb]['rCSselectedDATA']['rCSE_pred'],3)+'\\\\'
#print '\\hline\end{tabular}}\end{center}\caption{$R^{QCD}_{CS} $ factors from anti-selected Data in the 4-5j, 1b CR}\label{tab:1b_QCDrcs}\end{table}'

#print QCD yields in low dPhi region to correct RCS_EWK in the CR 4-5j, 1b
#print '$N^{QCD}_{selected}(low \DF)$ in CR 4-5j,1b'
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|}\\hline'
#print ' \\njet     & \ST & \HT & \DF    &\multicolumn{3}{c|}{$N^{QCD}_{selected}(low \DF)$ in 4-5j,1b CR}\\\%\hline'
#print ' & $[$GeV$]$ &$[$GeV$]$& &\multicolumn{3}{c}{prediction}\\\\\hline'
#print '\\hline'
#secondLine = False
#for srNJet in sorted(signalRegion):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{13}{*}{\\begin{sideways}$[4,5]$\end{sideways}}'
#  for stb in sorted(signalRegion[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegion[srNJet][stb]):
#      if not first: print '&'
#      first = False
##      nQCDpred = ratio[srNJet][stb][htb]['F_seltoantisel']*bins[srNJet][stb][htb][ttCRbtb]['NDATAAntiSel']
##      nQCDpred_err = sqrt((ratio[srNJet][stb][htb]['F_seltoantisel_err']**2*bins[srNJet][stb][htb][ttCRbtb]['NDATAAntiSel']**2)\
##                         +(bins[srNJet][stb][htb][ttCRbtb]['NDATAAntiSel_err']**2*ratio[srNJet][stb][htb]['F_seltoantisel']**2))
##      res = nQCDpred/(bins[srNJet][stb][htb][ttCRbtb]['rCSantiSelectedDATA']['rCS']+1)
##      res_err = res * sqrt(nQCDpred_err**2/nQCDpred**2 + bins[srNJet][stb][htb][ttCRbtb]['rCSantiSelectedDATA']['rCSE_pred']**2/(bins[srNJet][stb][htb][ttCRbtb]['']+1)**2)
#      print '&$'+varBin(htb)+'$ &'+str(signalRegion[srNJet][stb][htb]['deltaPhi'])
#      print ' & '+getNumString(bins[srNJet][stb][htb][ttCRbtb]['NQCDpred_lowdPhi'], bins[srNJet][stb][htb][ttCRbtb]['NQCDpred_lowdPhi_err'])+'\\\\'
##           +' & '+getNumString(bins[srNJet][stb][htb][ttCRbtb]['NQCDSelLowdPhi'], bins[srNJet][stb][htb][ttCRbtb]['NQCDSelLowdPhi_err'])+'\\\\'
#print '\\hline\end{tabular}}\end{center}\caption{$N^{QCD}_{selected}(low \DF)$ to correct $R^{EWK}_{CS}$  in the 4-5j, 1b CR}\label{tab:1b_QCDlowdPhi}\end{table}'


print "Results QCD estimation"
print
print '\\begin{table}[ht]\\begin{center}\\begin{tabular}{|c|c|c|rrr|rrr|r|}\\hline'
print ' \\njet     & \ST & \HT     &\multicolumn{7}{c|}{QCD multijets}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c}{simulation}&closure\\\\\hline'
#first print yields in the CR 3-4j
#print '\\hline'
#print '\multirow{'+str(len(ratio))+'}{*}{\\begin{sideways}$'+varBin(CR)+'$\end{sideways}}'
#for njb in sorted(ratio):
#  for stb in sorted(ratio[njb]):
#    print '&\multirow{'+str(len(ratio[njb]))+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(ratio[njb][stb]):
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$'
#      print ' & '+getNumString(ratio[njb][stb][htb]['NQCDFit'],ratio[njb][stb][htb]['NQCDFit_err'])\
#           +' & '+getNumString(ratio[njb][stb][htb]['NQCDSelMC'],ratio[njb][stb][htb]['NQCDSelMC_err'])\
#           +' & '+getNumString(res,res_err)+'\\\\'
#print predicted yields in the SR
secondLine = False
for srNJet in sorted(signalRegion):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegion[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegion[srNJet][stb]):
      if not first: print '&'
      first = False
      res = abs(bins[srNJet][stb][htb][(0,0)]['NQCDpred']-bins[srNJet][stb][htb][(0,0)]['NQCDSelMC'])/bins[srNJet][stb][htb][(0,0)]['NQCDpred']
      print '&$'+varBin(htb)+'$'
      #print ' & '+getNumString(ratio[srNJet][stb][htb]['F_seltoantisel']*nAntiSel[srNJet][stb][htb][btb]['NdataAntiSel'],\
      #           sqrt((ratio[srNJet][stb][htb]['F_seltoantisel_err']**2*nAntiSel[srNJet][stb][htb][btb]['NdataAntiSel']**2)+(nAntiSel[srNJet][stb][htb][btb]['NdataAntiSel_err']**2*ratio[srNJet][stb][htb]['F_seltoantisel']**2)))\
      print ' & '+getNumString(bins[srNJet][stb][htb][(0,0)]['NQCDpred'],bins[srNJet][stb][htb][(0,0)]['NQCDpred_err'])\
           +' & '+getNumString(bins[srNJet][stb][htb][(0,0)]['NQCDSelMC'], bins[srNJet][stb][htb][(0,0)]['NQCDSelMC_err'])\
           +' & '+str(round(res,2))+'\\\\'
#      if htb[1] == -1 : print '\\cline{2-9}'

print '\\hline\end{tabular}\end{center}\caption{Closure table for QCD background , 0-tag regions, 3$fb^{-1}$}\label{tab:0b_QCDpred}\end{table}'

#print "Results $R^{QCD}_{CS} $"
#print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrr|}\\hline'
#print ' \\njet     & \ST & \HT & $\Delta\Phi_{cut} $   &\multicolumn{3}{c|}{$R^{antiselected}_{CS}$}&\multicolumn{3}{c|}{$R^{selected}_{CS}$}\\\%\hline'
#print ' & $[$GeV$]$ &$[$GeV$]$& &\multicolumn{3}{c|}{}&\multicolumn{3}{c|}{}\\\\\hline'
#print '\\hline'
##print predicted yields in the SR
#secondLine = False
#for srNJet in sorted(signalRegion):
#  print '\\hline'
#  if secondLine: print '\\hline'
#  secondLine = True
#  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#  for stb in sorted(signalRegion[srNJet]):
#    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#    first = True
#    for htb in sorted(signalRegion[srNJet][stb]):
#      if not first: print '&'
#      first = False
#      print '&$'+varBin(htb)+'$ &'+str(signalRegion[srNJet][stb][htb]['deltaPhi'])
#      print ' & '+getNumString(nAntiSel[srNJet][stb][htb][btb]['RcsQCDantisel'],nAntiSel[srNJet][stb][htb][btb]['RcsQCDantiselErr_sim'],3)\
#           +' & '+getNumString(nAntiSel[srNJet][stb][htb][btb]['RcsSel'],nAntiSel[srNJet][stb][htb][btb]['RcsSelErr_sim'],3)+'\\\\'
##      if htb[1] == -1 : print '\\cline{2-9}'
#print '\\hline\end{tabular}}\end{center}\caption{$R^{QCD}_{CS} $ factors from anti-selected Data , 0-tag regions, 3$fb^{-1}$}\label{tab:0b_rcs}\end{table}'
