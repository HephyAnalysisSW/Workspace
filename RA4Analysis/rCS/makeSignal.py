import ROOT
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName,varBin
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400ST150_withDF import *
from makeTTPrediction import makeTTPrediction
from makeWPrediction import makeWPrediction
from localInfo import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import *
from math import pi, sqrt

lepSel = 'hard'

ROOT.TH1F().SetDefaultSumw2()

presel = "singleMuonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0"

streg = [[(250, 350), 1.], [(350, 450), 1.], [(450, -1), 1.]]
htreg = [(500,750), (750,1000), (1000,1250), (1250,-1)]
njreg = [(5,5),(6,-1)]
nSTbins = len(streg)

allSignals=[
            #"SMS_T1tttt_2J_mGl1200_mLSP800",
            #"SMS_T1tttt_2J_mGl1500_mLSP100",
            #"SMS_T2tt_2J_mStop425_mLSP325",
            #"SMS_T2tt_2J_mStop500_mLSP325",
            #"SMS_T2tt_2J_mStop650_mLSP325",
            #"SMS_T2tt_2J_mStop850_mLSP100",
            {'name':'T5q^{4} 1.2/1.0/0.8', 'sample':SMS_T5qqqqWW_Gl1200_Chi1000_LSP800[lepSel], 'weight':'weight', 'color':ROOT.kBlack},
            {'name':'T5q^{4} 1.5/0.8/0.1',  'sample':SMS_T5qqqqWW_Gl1500_Chi800_LSP100[lepSel],  'weight':'weight', 'color':ROOT.kMagenta},
            #"T1ttbbWW_mGo1000_mCh725_mChi715",
            #"T1ttbbWW_mGo1000_mCh725_mChi720",
            #"T1ttbbWW_mGo1300_mCh300_mChi290",
            #"T1ttbbWW_mGo1300_mCh300_mChi295",
            #"T5ttttDeg_mGo1000_mStop300_mCh285_mChi280",
            #"T5ttttDeg_mGo1000_mStop300_mChi280",
            #"T5ttttDeg_mGo1300_mStop300_mCh285_mChi280",
            #"T5ttttDeg_mGo1300_mStop300_mChi280",
]

for s in allSignals:
  s['chain'] = getChain(s['sample'],histname='')


print "signal yields (+charge)"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|}\\hline'
print ' \HT     & \\njet & \ST     &\multicolumn{3}{c|}{\TFiveqqqqHM (+ charge)}&\multicolumn{3}{c|}{\TFiveqqqqHL (+ charge)}\\\%\hline'
print '[GeV]&        &[GeV]&\multicolumn{3}{c|}{} &\multicolumn{3}{c|}{} \\\\\hline'
for i_htb, htb in enumerate(htreg):
  if i_htb!=0:print '\\hline'
  print '\multirow{'+str(2*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(htb)+'$\end{sideways}}'
  for srNJet in njreg:
    print '&\multirow{'+str(nSTbins)+'}{*}{'+varBin(srNJet)+'}'
    for stb, dPhiCut in streg:
      if stb[1] == -1 : print '&'
      print '&$'+varBin(stb)+'$'
      name, cut =  nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = 'nBJetMediumCMVA30')
      for s in allSignals:
        s['yield_NegPdg']     = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>1.0", weight = "weight")
        s['yield_NegPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg<0&&'+cut+"&&deltaPhi_Wl>1.0", weight = "weight*weight")
        print ' & '+getNumString(s['yield_NegPdg'], sqrt(s['yield_NegPdg_Var']), acc=3)
      print '\\\\'
      if stb[1] == -1 : print '\\cline{2-9}'
print '\\hline\end{tabular}}\end{center}\caption{+ charge}\end{table}'

print "signal yields (-charge)"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|}\\hline'
print ' \HT     & \\njet & \ST     &\multicolumn{3}{c|}{\TFiveqqqqHM (- charge)}&\multicolumn{3}{c|}{\TFiveqqqqHL (- charge)}\\\%\hline'
print '[GeV]&        &[GeV]&\multicolumn{3}{c|}{} &\multicolumn{3}{c|}{} \\\\\hline'
for i_htb, htb in enumerate(htreg):
  if i_htb!=0:print '\\hline'
  print '\multirow{'+str(2*nSTbins)+'}{*}{\\begin{sideways}$'+varBin(htb)+'$\end{sideways}}'
  for srNJet in njreg:
    print '&\multirow{'+str(nSTbins)+'}{*}{'+varBin(srNJet)+'}'
    for stb, dPhiCut in streg:
      if stb[1] == -1 : print '&'
      print '&$'+varBin(stb)+'$'
      name, cut =  nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = 'nBJetMediumCMVA30')
      for s in allSignals:
        s['yield_PosPdg']     = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>1.0", weight = "weight")
        s['yield_PosPdg_Var'] = getYieldFromChain(s['chain'], 'leptonPdg>0&&'+cut+"&&deltaPhi_Wl>1.0", weight = "weight*weight")
        print ' & '+getNumString(s['yield_PosPdg'], sqrt(s['yield_PosPdg_Var']), acc=3)
      print '\\\\'
      if stb[1] == -1 : print '\\cline{2-9}'
print '\\hline\end{tabular}}\end{center}\caption{- charge}\end{table}'
