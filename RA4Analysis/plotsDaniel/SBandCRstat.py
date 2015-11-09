import ROOT
import pickle
import os,sys,math
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName, varBin
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v9_Phys14V3_HT400ST200_ForTTJetsUnc import *
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT400ST200_postProcessed_fromArthur import *

from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_btagWeight import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_fromArthur import *

#from makeTTPrediction import makeTTPrediction
#from makeWPrediction import makeWPrediction
from Workspace.HEPHYPythonTools.user import username
from math import pi, sqrt, isnan
from Workspace.RA4Analysis.signalRegions import *
from rCShelpers import *


ROOT.TH1F().SetDefaultSumw2()

lepSel = 'hard'

#cWJets  = getChain(WJetsHTToLNu_25ns,histname='')
#cTTJets = getChain(TTJets_LO_25ns,histname='')
#cEWK = getChain([WJetsHTToLNu_25ns,TTJets_LO_25ns,DY_25ns,singleTop_25ns],histname='')

cWJets  = getChain(WJetsHT_25ns,histname='')
cTTJets = getChain(TTJets_HTLO_25ns,histname='')
#DY = getChain(DY_25ns,histname='')
#singleTop = getChain(singleTop_25ns,histname='')
#TTV = getChain(TTV_25ns,histname='')
#cRest = getChain([singleTop_25ns, DY_25ns, TTV_25ns],histname='')#no QCD
cRest = getChain([singleTop_25ns, DY_25ns, TTV_25ns], histname='')
#cEWK =  getChain([WJetsHT_25ns, TTJets_HTLO_25ns, singleTop_25ns, DY_25ns, TTV_25ns], histname='')#no QCD
cData = getChain([SingleMuon_Run2015D, SingleElectron_Run2015D], histname='')

triggers = "(HLT_EleHT350||HLT_MuHT350)"
filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_CSCTightHaloFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"

btagString = 'nBJetMediumCSV30'

charges = [['posPDG','leptonPdg>0'],['negPDG','leptonPdg<0']]

stats ={}
signalRegions = signalRegion3fb

lumi = 1.26

def makeWeight(lumi=4., sampleLumi=3.,debug=False):
  if debug:
    print 'No lumi-reweighting done!!'
    return 'weight', 'weight*weight'
  else:
    weight_str = '(((weight)/'+str(sampleLumi)+')*'+str(lumi)+')'
    weight_err_str = '('+weight_str+'*'+weight_str+')'
  return weight_str, weight_err_str

weight_str, weight_err_str = makeWeight(lumi=lumi, sampleLumi=lumi)

for srNJet in sorted(signalRegions):
  stats[srNJet] = {}
  for stb in sorted(signalRegions[srNJet]):
    stats[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      stats[srNJet][stb][htb] = {}
      print
      print '#############################################'
      print 'bin: \t njet \t\t LT \t\t HT'
      if len(str(srNJet))<7:
        print '\t',srNJet,'\t\t',stb,'\t',htb
      else:
        print '\t',srNJet,'\t',stb,'\t',htb
      print '#############################################'
      print
      deltaPhi = signalRegions[srNJet][stb][htb]['deltaPhi']
      for nc,charge in charges:
        print nc
        CRname, CR = nameAndCut(stb,htb,srNJet, btb=(0,0) ,presel=presel+'&&'+charge)
        CRname1b, CR1b = nameAndCut(stb,htb,srNJet, btb=(1,1) ,presel=presel+'&&'+charge)
        CRname2b, CR2b = nameAndCut(stb,htb,srNJet, btb=(2,2) ,presel=presel+'&&'+charge)

        SBTTname, SBTT = nameAndCut(stb,htb,(4,5), btb=(1,1) ,presel=presel)
        SBWname, SBW = nameAndCut(stb,htb,(3,4), btb=(0,0) ,presel=presel+'&&'+charge+'&&abs(leptonPdg)==13')
  
        stats[srNJet][stb][htb][nc] = {}
        stats[srNJet][stb][htb][nc]['CR'] = {}
        stats[srNJet][stb][htb][nc]['CR']['data'] =        getYieldFromChain(cData,  cutString=CR+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        stats[srNJet][stb][htb][nc]['CR']['data_err'] =    sqrt(getYieldFromChain(cData,  cutString=CR+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        stats[srNJet][stb][htb][nc]['CR']['data1b'] =        getYieldFromChain(cData,  cutString=CR1b+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        stats[srNJet][stb][htb][nc]['CR']['data1b_err'] =    sqrt(getYieldFromChain(cData,  cutString=CR1b+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        stats[srNJet][stb][htb][nc]['CR']['data2b'] =        getYieldFromChain(cData,  cutString=CR2b+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        stats[srNJet][stb][htb][nc]['CR']['data2b_err'] =    sqrt(getYieldFromChain(cData,  cutString=CR2b+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['CR']['W'] =        getYieldFromChain(cWJets,  cutString=CR+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['CR']['W_err'] =    sqrt(getYieldFromChain(cWJets,  cutString=CR+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['CR']['TT'] =       getYieldFromChain(cTTJets, cutString=CR+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['CR']['TT_err'] =   sqrt(getYieldFromChain(cTTJets, cutString=CR+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['CR']['Rest'] =     getYieldFromChain(cRest,   cutString=CR+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['CR']['Rest_err'] = sqrt(getYieldFromChain(cRest,   cutString=CR+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        
        #print 'CR: W, tt, Rest'
        #print stats[srNJet][stb][htb][nc]['CR']['W'], stats[srNJet][stb][htb][nc]['CR']['TT'], stats[srNJet][stb][htb][nc]['CR']['Rest']
        
        stats[srNJet][stb][htb][nc]['SBTT'] = {}
        stats[srNJet][stb][htb][nc]['SBTT']['highDPhi'] = {}
        stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi'] = {}
        stats[srNJet][stb][htb][nc]['SBTT']['highDPhi']['data'] =        getYieldFromChain(cData,  cutString=SBTT+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_str)
        stats[srNJet][stb][htb][nc]['SBTT']['highDPhi']['data_err'] =    sqrt(getYieldFromChain(cData,  cutString=SBTT+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBTT']['highDPhi']['W'] =        getYieldFromChain(cWJets,  cutString=SBTT+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBTT']['highDPhi']['W_err'] =    sqrt(getYieldFromChain(cWJets,  cutString=SBTT+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBTT']['highDPhi']['TT'] =       getYieldFromChain(cTTJets, cutString=SBTT+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBTT']['highDPhi']['TT_err'] =   sqrt(getYieldFromChain(cTTJets, cutString=SBTT+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBTT']['highDPhi']['Rest'] =     getYieldFromChain(cRest,   cutString=SBTT+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBTT']['highDPhi']['Rest_err'] = sqrt(getYieldFromChain(cRest,   cutString=SBTT+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_err_str))
        
        #print 'SB TT high delta Phi: W, tt, Rest'
        #print stats[srNJet][stb][htb][nc]['SBTT']['highDPhi']['W'], stats[srNJet][stb][htb][nc]['SBTT']['highDPhi']['TT'], stats[srNJet][stb][htb][nc]['SBTT']['highDPhi']['Rest']
        stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['data'] =        getYieldFromChain(cData,  cutString=SBTT+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['data_err'] =    sqrt(getYieldFromChain(cData,  cutString=SBTT+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['W'] =        getYieldFromChain(cWJets,  cutString=SBTT+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['W_err'] =    sqrt(getYieldFromChain(cWJets,  cutString=SBTT+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['TT'] =       getYieldFromChain(cTTJets, cutString=SBTT+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['TT_err'] =   sqrt(getYieldFromChain(cTTJets, cutString=SBTT+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['Rest'] =     getYieldFromChain(cRest,   cutString=SBTT+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['Rest_err'] = sqrt(getYieldFromChain(cRest,   cutString=SBTT+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        
        #print 'SB TT low delta Phi: W, tt, Rest'
        #print stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['W'], stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['TT'], stats[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['Rest']
        
        stats[srNJet][stb][htb][nc]['SBW'] = {}
        stats[srNJet][stb][htb][nc]['SBW']['highDPhi'] = {}
        stats[srNJet][stb][htb][nc]['SBW']['lowDPhi'] = {}
        stats[srNJet][stb][htb][nc]['SBW']['highDPhi']['data'] =        getYieldFromChain(cData,  cutString=SBW+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_str)
        stats[srNJet][stb][htb][nc]['SBW']['highDPhi']['data_err'] =    sqrt(getYieldFromChain(cData,  cutString=SBW+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBW']['highDPhi']['W'] =        getYieldFromChain(cWJets,  cutString=SBW+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBW']['highDPhi']['W_err'] =    sqrt(getYieldFromChain(cWJets,  cutString=SBW+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBW']['highDPhi']['TT'] =       getYieldFromChain(cTTJets, cutString=SBW+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBW']['highDPhi']['TT_err'] =   sqrt(getYieldFromChain(cTTJets, cutString=SBW+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBW']['highDPhi']['Rest'] =     getYieldFromChain(cRest,   cutString=SBW+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBW']['highDPhi']['Rest_err'] = sqrt(getYieldFromChain(cRest,   cutString=SBW+'&&deltaPhi_Wl>='+str(deltaPhi), weight=weight_err_str))

        #print 'SB W high delta Phi: W, tt, Rest'
        #print stats[srNJet][stb][htb][nc]['SBW']['highDPhi']['W'], stats[srNJet][stb][htb][nc]['SBW']['highDPhi']['TT'], stats[srNJet][stb][htb][nc]['SBW']['highDPhi']['Rest']
        
        stats[srNJet][stb][htb][nc]['SBW']['lowDPhi']['data'] =        getYieldFromChain(cData,  cutString=SBW+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        stats[srNJet][stb][htb][nc]['SBW']['lowDPhi']['data_err'] =    sqrt(getYieldFromChain(cData,  cutString=SBW+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBW']['lowDPhi']['W'] =        getYieldFromChain(cWJets,  cutString=SBW+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBW']['lowDPhi']['W_err'] =    sqrt(getYieldFromChain(cWJets,  cutString=SBW+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBW']['lowDPhi']['TT'] =       getYieldFromChain(cTTJets, cutString=SBW+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBW']['lowDPhi']['TT_err'] =   sqrt(getYieldFromChain(cTTJets, cutString=SBW+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        #stats[srNJet][stb][htb][nc]['SBW']['lowDPhi']['Rest'] =     getYieldFromChain(cRest,   cutString=SBW+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_str)
        #stats[srNJet][stb][htb][nc]['SBW']['lowDPhi']['Rest_err'] = sqrt(getYieldFromChain(cRest,   cutString=SBW+'&&deltaPhi_Wl<'+str(deltaPhi), weight=weight_err_str))
        
        #print 'SB W low delta Phi: W, tt, Rest'
        #print stats[srNJet][stb][htb][nc]['SBW']['lowDPhi']['W'], stats[srNJet][stb][htb][nc]['SBW']['lowDPhi']['TT'], stats[srNJet][stb][htb][nc]['SBW']['lowDPhi']['Rest']


#res = pickle.load(file('/data/dspitzbart/Spring15/Stat_SBandCR_pkl'))
#
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

#for nc,charge in charges:
#  print
#  print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
#  print ' \\njet     & \ST & \HT     &\multicolumn{9}{c|}{CR}&\multicolumn{9}{c|}{SB for $tt+$Jets, 1b, $\Delta\Phi<x$}&\multicolumn{9}{c|}{SB for $tt+$Jets, 1b, $\Delta\Phi\geq x$}\\\%\hline'
#  print ' & $[$GeV$]$ &$[$GeV$]$'\
#          +'& \multicolumn{3}{c}{$W+$ Jets} & \multicolumn{3}{c}{$tt+$Jets} & \multicolumn{3}{c|}{Rest}'\
#          +'& \multicolumn{3}{c}{$W+$ Jets} & \multicolumn{3}{c}{$tt+$Jets} & \multicolumn{3}{c|}{Rest}'\
#          +'& \multicolumn{3}{c}{$W+$ Jets} & \multicolumn{3}{c}{$tt+$Jets} & \multicolumn{3}{c|}{Rest}\\\\\hline'
#  
#  secondLine = False
#  for srNJet in sorted(signalRegions):
#    print '\\hline'
#    if secondLine: print '\\hline'
#    secondLine = True
#    print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#    for stb in sorted(signalRegions[srNJet]):
#      print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#      first = True
#      for htb in sorted(signalRegions[srNJet][stb]):
#        if not first: print '&'
#        first = False
#        print '&$'+varBin(htb)+'$'
#        print ' & '+getNumString(res[srNJet][stb][htb][nc]['CR']['W'],    res[srNJet][stb][htb][nc]['CR']['W_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['CR']['TT'],   res[srNJet][stb][htb][nc]['CR']['TT_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['CR']['Rest'], res[srNJet][stb][htb][nc]['CR']['Rest_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['W'],     res[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['W_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['TT'],    res[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['TT_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['Rest'],  res[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['Rest_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBTT']['highDPhi']['W'],    res[srNJet][stb][htb][nc]['SBTT']['highDPhi']['W_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBTT']['highDPhi']['TT'],   res[srNJet][stb][htb][nc]['SBTT']['highDPhi']['TT_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBTT']['highDPhi']['Rest'], res[srNJet][stb][htb][nc]['SBTT']['highDPhi']['Rest_err']) +'\\\\'
#        if htb[1] == -1 : print '\\cline{2-30}'
#  print '\\hline\end{tabular}}\end{center}\caption{Statistics for CR and SB, '+nc+', 1.26$fb^{-1}$}\label{tab:statCheck}\end{table}'
#
#for nc,charge in charges:
#  print
#  print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
#  print ' \\njet     & \ST & \HT     & \multicolumn{9}{c|}{SB for $W+$Jets, 0b, $\Delta\Phi<x$} & \multicolumn{9}{c|}{SB for $W+$Jets, 0b, $\Delta\Phi\geq x$}\\\%\hline'
#  print ' & $[$GeV$]$ &$[$GeV$]$'\
#          +'& \multicolumn{3}{c}{$W+$ Jets} & \multicolumn{3}{c}{$tt+$Jets} & \multicolumn{3}{c|}{Rest}'\
#          +'& \multicolumn{3}{c}{$W+$ Jets} & \multicolumn{3}{c}{$tt+$Jets} & \multicolumn{3}{c|}{Rest}\\\\\hline'
#
#  secondLine = False
#  for srNJet in sorted(signalRegions):
#    print '\\hline'
#    if secondLine: print '\\hline'
#    secondLine = True
#    print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#    for stb in sorted(signalRegions[srNJet]):
#      print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#      first = True
#      for htb in sorted(signalRegions[srNJet][stb]):
#        if not first: print '&'
#        first = False
#        print '&$'+varBin(htb)+'$'
#        print ' & '+getNumString(res[srNJet][stb][htb][nc]['SBW']['lowDPhi']['W'],     res[srNJet][stb][htb][nc]['SBW']['lowDPhi']['W_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBW']['lowDPhi']['TT'],    res[srNJet][stb][htb][nc]['SBW']['lowDPhi']['TT_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBW']['lowDPhi']['Rest'],  res[srNJet][stb][htb][nc]['SBW']['lowDPhi']['Rest_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBW']['highDPhi']['W'],    res[srNJet][stb][htb][nc]['SBW']['highDPhi']['W_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBW']['highDPhi']['TT'],   res[srNJet][stb][htb][nc]['SBW']['highDPhi']['TT_err'])\
#             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBW']['highDPhi']['Rest'], res[srNJet][stb][htb][nc]['SBW']['highDPhi']['Rest_err']) +'\\\\'
#        if htb[1] == -1 : print '\\cline{2-21}'
#  print '\\hline\end{tabular}}\end{center}\caption{Statistics for CR and SB, '+nc+', 1.26$fb^{-1}$}\label{tab:statCheck}\end{table}'
#

res = stats

for nc,charge in charges:
  print
  print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
  print ' \\njet     & \ST & \HT   & \multicolumn{9}{c|}{CR}  & \multicolumn{6}{c|}{SB for $tt+$Jets, 1b} & \multicolumn{6}{c|}{SB for $W+$Jets, 0b} \\\%\hline'
  print ' & $[$GeV$]$ &$[$GeV$]$'\
          +'& \multicolumn{3}{c}{0b} & \multicolumn{3}{c}{1b} & \multicolumn{3}{c|}{2b} & \multicolumn{3}{c}{$\Delta\Phi<x$} & \multicolumn{3}{c|}{$\Delta\Phi\geq x$}'\
          +'& \multicolumn{3}{c}{$\Delta\Phi<x$} & \multicolumn{3}{c|}{$\Delta\Phi\geq x$}\\\\\hline'

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
        print ' & '+getNumString(res[srNJet][stb][htb][nc]['CR']['data'],    res[srNJet][stb][htb][nc]['CR']['data_err'])\
             +' & '+getNumString(res[srNJet][stb][htb][nc]['CR']['data1b'],    res[srNJet][stb][htb][nc]['CR']['data1b_err'])\
             +' & '+getNumString(res[srNJet][stb][htb][nc]['CR']['data2b'],    res[srNJet][stb][htb][nc]['CR']['data2b_err'])\
             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['data'],     res[srNJet][stb][htb][nc]['SBTT']['lowDPhi']['data_err'])\
             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBTT']['highDPhi']['data'],    res[srNJet][stb][htb][nc]['SBTT']['highDPhi']['data_err'])\
             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBW']['lowDPhi']['data'],    res[srNJet][stb][htb][nc]['SBW']['lowDPhi']['data_err'])\
             +' & '+getNumString(res[srNJet][stb][htb][nc]['SBW']['highDPhi']['data'],    res[srNJet][stb][htb][nc]['SBW']['highDPhi']['data_err'])+'\\\\'
        if htb[1] == -1 : print '\\cline{2-24}'
  print '\\hline\end{tabular}}\end{center}\caption{Statistics for CR and SB in data, '+nc+', 1.26$fb^{-1}$}\label{tab:statCheck}\end{table}'

QCDpickle = '/data/dhandl/results2015/QCDEstimation/20151106_QCDestimation_pkl'
QCD = pickle.load(file(QCDpickle))

for nc,charge in charges:
  print
  print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
  print ' \\njet     & \ST & \HT   & \multicolumn{9}{c|}{CR}  & \multicolumn{9}{c|}{QCD in CR}  \\\%\hline'
  print ' & $[$GeV$]$ &$[$GeV$]$'\
          +'& \multicolumn{3}{c}{0b} & \multicolumn{3}{c}{1b} & \multicolumn{3}{c|}{2b} & \multicolumn{3}{c}{0b} & \multicolumn{3}{c}{1b} & \multicolumn{3}{c|}{2b}\\\\\hline'

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
        QCD0 = QCD[srNJet][stb][htb][(0,0)]['NQCDpred_lowdPhi']/2
        QCD0err = QCD[srNJet][stb][htb][(0,0)]['NQCDpred_lowdPhi_err']/2
        if isnan(QCD0): QCD0 = QCD[srNJet][stb][htb][(0,0)]['NQCDpred']/2
        if isnan(QCD0err): QCD0err = QCD0
        
        QCD1 = QCD[srNJet][stb][htb][(1,1)]['NQCDpred_lowdPhi']/2
        QCD1err = QCD[srNJet][stb][htb][(1,1)]['NQCDpred_lowdPhi_err']/2
        if isnan(QCD1): QCD1 = QCD[srNJet][stb][htb][(1,1)]['NQCDpred']/2
        if isnan(QCD1err): QCD1err = QCD1
        
        QCD2 = QCD[srNJet][stb][htb][(2,2)]['NQCDpred_lowdPhi']/2
        QCD2err = QCD[srNJet][stb][htb][(2,2)]['NQCDpred_lowdPhi_err']/2
        if isnan(QCD2): QCD2 = QCD[srNJet][stb][htb][(2,2)]['NQCDpred']/2
        if isnan(QCD2err): QCD2err = QCD2
        
        print '&$'+varBin(htb)+'$'
        print ' & '+getNumString(res[srNJet][stb][htb][nc]['CR']['data'],    res[srNJet][stb][htb][nc]['CR']['data_err'])\
             +' & '+getNumString(res[srNJet][stb][htb][nc]['CR']['data1b'],    res[srNJet][stb][htb][nc]['CR']['data1b_err'])\
             +' & '+getNumString(res[srNJet][stb][htb][nc]['CR']['data2b'],    res[srNJet][stb][htb][nc]['CR']['data2b_err'])\
             +' & '+getNumString(QCD0, QCD0err)\
             +' & '+getNumString(QCD1, QCD1err)\
             +' & '+getNumString(QCD2, QCD2err)+'\\\\'
        if htb[1] == -1 : print '\\cline{2-21}'
  print '\\hline\end{tabular}}\end{center}\caption{Statistics for CR and SB in data, '+nc+', 1.26$fb^{-1}$}\label{tab:statCheck}\end{table}'
