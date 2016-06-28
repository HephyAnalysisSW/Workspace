import ROOT
import pickle
import operator
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_fromArtur import *
from Workspace.RA4Analysis.signalRegions import *
#from localInfo import username
from Workspace.HEPHYPythonTools.user import username

from math import sqrt, pi
ROOT.TH1F().SetDefaultSumw2()

weight_str = "((weight*2.25)/3)"
weight_str_bkg =  "0.94*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*puReweight_true_max4*TopPtWeight*weight*2.25/3"

def getFOM(Ysig ,Ysig_Var, Ybkg,  Ybkg_Var):
  if Ybkg>0.0:
    FOM = Ysig/sqrt(Ybkg+(0.2*Ybkg)**2)
    #FOM_Var = Ysig_Var/Ybkg + Ybkg_Var*((Ysig)/(2*Ybkg**(3/2)))**2
    return FOM#, FOM_Var
  else:
    return 'nan'

def getNumString(n,ne, acc=2, systematic=False):    ##For printing table 
  if type(n) is float and type(ne) is float:
    if systematic:
      return str(round(n,acc))+'&$\pm$&'+str(round(ne,acc))+'&$\pm$&'+str(round(0.2*n,acc))
    else:
      return str(round(n,acc))+'&$\pm$&'+str(round(ne,acc))
  #if type(n) is str and type(ne) is str: 
  else:
    return str(n) +'&$\pm$&'+ str(ne)

lepSel = 'hard'
#dPhiJJStr='acos((Jet_pt[1]+Jet_pt[0]*cos(Jet_phi[1]-Jet_phi[0]))/sqrt(Jet_pt[1]**2+Jet_pt[0]**2+2*Jet_pt[0]*Jet_pt[1]*cos(Jet_phi[1]-Jet_phi[0])))'
btag_str = 'nBJetMediumCSV30'
#cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel],DY[lepSel],TTVH[lepSel],singleTop[lepSel]],histname='')
cBkg = getChain([TTJets_combined,WJetsHTToLNu_25ns,singleTop_25ns, DY_25ns,TTV_25ns],histname='')
#cW = getChain(WJetsHTToLNu_25ns,histname='')
#cTT =getChain(TTJets_combined,histname='') 
cQCD = getChain(QCDHT_25ns,histname='')
#cS1200 = getChain(T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel],histname='')
#cS1500 = getChain(T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],histname='')
cS1000 = getChain(T5qqqqVV_mGluino_1000To1075_mLSP_1To950[1000][700],histname='')
cS1200 = getChain(T5qqqqVV_mGluino_1200To1275_mLSP_1to1150[1200][800],histname='')
cS1500 = getChain(T5qqqqVV_mGluino_1400To1550_mLSP_1To1275[1500][100],histname='')

btagString = "nBJetMediumCSV30"

presel_bkg = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter'
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80"
prefix = presel.split('&&')[0]+'_SRfinder_miniAODv2'

path = '/data/'+username+'/Spring15/25ns/SRfinder/'
if not os.path.exists(path):
  os.makedirs(path)

signalRegion3fbReduced = {(5, 5):  {(250, 350): {(500, -1):  {'deltaPhi': 1.0}},
                                    (350, 450): {(500, -1):  {'deltaPhi': 1.0}},
                                    (450, -1):  {(500, -1):  {'deltaPhi': 0.75}}},
                          (6, 7):  {(250, 350): {(500, 750): {'deltaPhi': 1.0},
                                                 (750, -1):  {'deltaPhi': 1.0}},
                                    (350, 450): {(500, 750): {'deltaPhi': 1.0},
                                                 (750, -1):  {'deltaPhi': 1.0}},
                                    (450, -1):  {(500, 750): {'deltaPhi': 0.75},
                                                 (750, -1):  {'deltaPhi': 0.75}}},
                          (8, -1): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
                                                 (750, -1):  {'deltaPhi': 1.0}},
                                    (350, -1):  {(500, -1):  {'deltaPhi': 0.75}}}}
#signalRegions = signalRegion3fbReduced
signalRegions = signalRegion3fb



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



print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|c|}\\hline'
print ' \\njet & \ST       & \HT       &\multicolumn{3}{c|}{$total bkg$}&\multicolumn{3}{c|}{$T5q^{4} 1.0/0.7$}&\multicolumn{3}{c|}{$T5q^{4} 1.2/0.8$}&\multicolumn{3}{c|}{$T5q^{4} 1.5/0.1$}&\\DF \\\%\hline'
print '        & $[$GeV$]$ & $[$GeV$]$ &    \multicolumn{3}{c|}{simulation}&\multicolumn{3}{c|}{simulation}         & \multicolumn{3}{c|}{simulation}        &   \multicolumn{3}{c|}{simulation}  & \\\\\hline '
bin = {}
secondLine = False
for srNJet in sorted(signalRegions):
  bin[srNJet]={}
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      name, cut =  nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      nameb, cutb =  nameAndCut(stb, htb, srNJet, btb=(0,-1), presel=presel_bkg+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      namett, cut_Q =  nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel_bkg+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      B = getYieldFromChain(cBkg, cutb, weight = weight_str_bkg+"*(weightBTag0_SF)")
      B_Err = sqrt(getYieldFromChain(cBkg, cutb, weight = weight_str_bkg+"*"+weight_str_bkg+"*(weightBTag0_SF)"+"*(weightBTag0_SF)"))
      QCD = getYieldFromChain(cQCD, cut_Q, weight = weight_str_bkg)
      QCD_Err = sqrt(getYieldFromChain(cQCD, cut_Q, weight = weight_str_bkg+"*"+weight_str_bkg))
      B = B + QCD
      B_Err = B_Err**2+QCD_Err**2
      B_Err = sqrt(B_Err)
      S1200 = getYieldFromChain(cS1200, cut, weight = weight_str)
      S1200_Err = sqrt(getYieldFromChain(cS1200, cut, weight = weight_str+"*"+weight_str))
      S1500 = getYieldFromChain(cS1500, cut, weight = weight_str)
      S1500_Err = sqrt(getYieldFromChain(cS1500, cut, weight =weight_str+"*"+weight_str))
      S1000 = getYieldFromChain(cS1000, cut, weight = weight_str)
      S1000_Err = sqrt(getYieldFromChain(cS1000, cut, weight = weight_str+"*"+weight_str))
      FOM1200 = getFOM(S1200,S1200_Err, B, B_Err)
      FOM1500 = getFOM(S1500,S1500_Err, B, B_Err)
      FOM1000 = getFOM(S1000,S1000_Err, B, B_Err)
      print ' & '+getNumString(B, B_Err)\
           +' & '+getNumString(S1000,S1000_Err)\
           +' & '+getNumString(S1200,S1200_Err)\
           +' & '+getNumString(S1500,S1500_Err)\
           +' & '+str(deltaPhiCut)\
           +'\\\\'
      if htb[1] == -1 : print '\\cline{2-16}'
print
print '\\hline\end{tabular}}\end{center}\caption{signal contaminations}\end{table}'

#+' & '+getNumString(S1200,S1200_Err)\

#streg = [[(250, 350), 1.], [(350, 450), 1.],[(450, -1), 1.]]
#htreg = [(500,750), (750,1000), (1000,1250), (1250,-1)]
#njreg = [(5,5),(6,7),(8,-1)]
#btreg = (0,0) 

#bestS1200 = []
#bestS1500 = []
#SR = []
#for i_htb, htb in enumerate(htreg):
#  for stb, dPhiCut in streg:
#    for srNJet in njreg:
#
#        #name, cut = nameAndCut(stb, htb, srNJet, btb=btreg, presel=presel+'&&'+add, btagVar = 'nBJetMediumCMVA30')
#        name, cut = nameAndCut(stb, htb, srNJet, btb=btreg, presel=presel, btagVar = btag_str)
#        print 'HT: ',htb,'|ST: ',stb,'|nJets: ',srNJet#, '|additional: ',add
#        B = getYieldFromChain(cBkg, cut, weight = "weight")
#        B_Var = getYieldFromChain(cBkg, cut, weight = "weight*weight")
#        S1200 = getYieldFromChain(cS1200, cut, weight = "weight")
#        S1200_Var = getYieldFromChain(cS1200, cut, weight = "weight*weight")
#        S1500 = getYieldFromChain(cS1500, cut, weight = "weight")
#        S1500_Var = getYieldFromChain(cS1500, cut, weight = "weight*weight")
#        S1000 = getYieldFromChain(cS1000, cut, weight = "weight")
#        S1000_Var = getYieldFromChain(cS1000, cut, weight = "weight*weight")
#        FOM1200 = getFOM(S1200,S1200_Var, B, B_Var)
#        FOM1500 = getFOM(S1500,S1500_Var, B, B_Var)
#        FOM1000 = getFOM(S1000,S1000_Var, B, B_Var)
#
#        #SR.append({'FOM1200':FOM1200, 'FOM1500':FOM1500, 'S1200':S1200, 'S1200_Var':S1200_Var, 'S1500':S1500, 'S1500_Var':S1500_Var, 'B':B, 'B_Var':B_Var, 'ST':stb, 'HT':htb, 'nJet':srNJet, 'additional':add})
#        SR.append({'FOM1200':FOM1200, 'FOM1500':FOM1500,'FOM1000':FOM1000 ,'S1200':S1200, 'S1200_Var':S1200_Var, 'S1500':S1500, 'S1500_Var':S1500_Var,'S1000':S1000,'S1000_Var':S1000_Var, 'B':B, 'B_Var':B_Var, 'ST':stb, 'HT':htb, 'nJet':srNJet})

#htBins = list(set([s['HT'] for s in SR]))
#stBins = list(set([s['ST'] for s in SR]))
#nJetBins = list(set([s['nJet'] for s in SR]))

#result={}
#for htb in htBins:
#  result[htb]={}
#  for stb in stBins:
#    result[htb][stb]={}
#    for njb in nJetBins:
#      result[htb][stb][njb]={'yield':find...

#bestS1200 = SR
#bestS1200.sort(key=operator.itemgetter('FOM1200'), reverse=True)
#bestS1200=filter(lambda x:not x['FOM1200']=='nan', bestS1200)
#
#bestS1500 = SR
#bestS1500.sort(key=operator.itemgetter('FOM1500'), reverse=True)
#bestS1500=filter(lambda x:not x['FOM1500']=='nan', bestS1500)
#
#bestS1000 = SR
#bestS1000.sort(key=operator.itemgetter('FOM1000'), reverse=True)
#bestS1000=filter(lambda x:not x['FOM1000']=='nan', bestS1000)
#
#pickle.dump((bestS1200,bestS1500,bestS1000), file(path+prefix+'_pkl','w'))
#
#bestS1200, bestS1500 , bestS1000 = pickle.load(file(path+prefix+'_pkl'))
#
#print "signal yields (T5q^{4} 1.2/1.0/0.8)"
#print
##print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrrrr|c|}\\hline'
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrrrr|c|}\\hline'
##print ' \HT     & \\njet & \ST & Add Cut  & \multicolumn{3}{c|}{\TFiveqqqqHM} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
#print ' \HT     & \\njet & \ST  & \multicolumn{3}{c|}{\TFiveqqqqHM} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
##print '$[$GeV$]$    &        &$[$GeV$]$ & & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
#print '$[$GeV$]$    &        &$[$GeV$]$ &  \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
#for dict in bestS1200:
#  #print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+'\\'+str(dict['additional'])+'&'+getNumString(dict['S1200'],sqrt(dict['S1200_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1200'],3))+'\\\\\hline'
#  print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+getNumString(dict['S1200'],sqrt(dict['S1200_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1200'],3))+'\\\\\hline'
#print '\end{tabular}}\end{center}\caption{\TFiveqqqqHM}\end{table}'
#
#
#print "signal yields (T5q^{4} 1.5/0.8/0.1)"
#print
##print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrrrr|c|}\\hline'
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrrrr|c|}\\hline'
##print ' \HT     & \\njet & \ST  & Add Cut & \multicolumn{3}{c|}{\TFiveqqqqHL} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
#print ' \HT     & \\njet & \ST   & \multicolumn{3}{c|}{\TFiveqqqqHL} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
##print '$[$GeV$]$    &    &$[$GeV$]$ & & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
#print '$[$GeV$]$    &    &$[$GeV$]$ & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
#for dict in bestS1500:
#  #print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+str(dict['additional'])+'&'+getNumString(dict['S1500'],sqrt(dict['S1500_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1500'],3))+'\\\\\hline'
#  print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+getNumString(dict['S1500'],sqrt(dict['S1500_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1500'],3))+'\\\\\hline'
#print '\end{tabular}}\end{center}\caption{\TFiveqqqqHL}\end{table}'
#
#
#print "signal yields (T5q^{4} 1.0/0.8/0.7)"
#print
##print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrrrr|c|}\\hline'
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrrrr|c|}\\hline'
##print ' \HT     & \\njet & \ST  & Add Cut & \multicolumn{3}{c|}{\TFiveqqqqHL} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
#print ' \HT     & \\njet & \ST   & \multicolumn{3}{c|}{$T5q^{4} 1.0/0.8/0.7$} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
##print '$[$GeV$]$    &    &$[$GeV$]$ & & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
#print '$[$GeV$]$    &    &$[$GeV$]$ & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
#for dict in bestS1000:
#  #print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+str(dict['additional'])+'&'+getNumString(dict['S1500'],sqrt(dict['S1500_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1500'],3))+'\\\\\hline'
#  print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+getNumString(dict['S1000'],sqrt(dict['S1000_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1000'],3))+'\\\\\hline'
#print '\end{tabular}}\end{center}\caption{$T5q^{4} 1.0/0.8/0.7$}\end{table}'


