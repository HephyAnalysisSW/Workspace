import ROOT
import os, sys, copy

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array

from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, deltaPhi
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.helpers import *
from rCShelpers import *
from Workspace.RA4Analysis.signalRegions import *
from localInfo import username

binning=[30,0,1500]

prepresel = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80'

bVar = 'nBJetMediumCSV30'

deltaPhiCut=1.
varstring='deltaPhi_Wl'
vartex = '#Delta#Phi(W,l)'
lepSel = 'hard'

targetLumi = 3. #fb^-1
sampleLumi = 4. #fb^-1

scaleFactor = targetLumi/sampleLumi

cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel], DY[lepSel], singleTop[lepSel], TTVH[lepSel]],histname='')
signal1 = getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname='')
signal2 = getChain(T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel],histname='')
signal3 = getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname='')

yields = []
yieldsDict = {}

signalRegions = signalRegion2fb

#Get the yields
for njb in signalRegions:
  yieldsDict[njb] = {}
  for stb in signalRegions[njb]:
    yieldsDict[njb][stb] = {}
    for htb in signalRegions[njb][stb]:
      twoBin=[0,signalRegions[njb][stb][htb]['deltaPhi'],3.2]
      bkgH = ROOT.TH1F('bkgH','',len(twoBin)-1, array('d', twoBin))
      sig1H = ROOT.TH1F('sig1H','',len(twoBin)-1, array('d', twoBin))
      sig2H = ROOT.TH1F('sig2H','',len(twoBin)-1, array('d', twoBin))
      sig3H = ROOT.TH1F('sig3H','',len(twoBin)-1, array('d', twoBin))
      name, cut = nameAndCut(stb, htb, njb, btb=(0,0), presel=prepresel, btagVar=bVar)
      cBkg.Draw(varstring+'>>bkgH','('+cut+')*weight')
      signal1.Draw(varstring+'>>sig1H','('+cut+')*weight')
      signal2.Draw(varstring+'>>sig2H','('+cut+')*weight')
      signal3.Draw(varstring+'>>sig3H','('+cut+')*weight')
      yBkg = bkgH.GetBinContent(2)*scaleFactor
      yS1 = sig1H.GetBinContent(2)*scaleFactor
      yS2 = sig2H.GetBinContent(2)*scaleFactor
      yS3 = sig3H.GetBinContent(2)*scaleFactor
      yieldsDict[njb][stb][htb] = {'Jets':njb, 'ST':stb, 'HT':htb, 'Bkg':yBkg, 'Model1':yS1, 'Model2':yS2, 'Model3':yS3}
      d = {'nJet':njb, 'HT':htb, 'ST':stb, 'B':yBkg, 'S1000':yS1, 'S1200':yS2, 'S1500':yS3, 'deltaPhi':signalRegions[njb][stb][htb]['deltaPhi']}
      print d
      yields.append(d)

path = '/data/'+username+'/lumi'+str(targetLumi)
yieldFile = open(path+'yields_pkl','w')
pickle.dump(yields,yieldFile)
yieldFile.close()


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

res = yieldsDict

print "Results"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|c|c|c|}\\hline'
print ' \\njet     & \ST $[$GeV$]$ & \HT $[$GeV$]$ & Bkg & Model 1 & Model 2 & Model 3\\\ \\hline'
#print '$[$GeV$]$&        &$[$GeV$]$&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation}&\multicolumn{3}{c}{prediction}&\multicolumn{3}{c|}{simulation} \\\\\hline'

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
      print '& $'+varBin(htb)+'$ &' +str(round(res[srNJet][stb][htb]['Bkg'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['Model1'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['Model2'],3))\
           +' & '+str(round(res[srNJet][stb][htb]['Model3'],3)) + '\\\\'
      if htb[1] == -1 : print '\\cline{2-7}'
print '\\hline\end{tabular}}\end{center}\caption{ABCD}\label{tab:0b_rcscorr_Wbkg}\end{table}'


