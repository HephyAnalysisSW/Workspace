import ROOT
import pickle
import operator
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v1_Phys14V3_HT400ST200 import *
from localInfo import username
from math import sqrt, pi
ROOT.TH1F().SetDefaultSumw2()

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
    return n +'&$\pm$&'+ ne

lepSel = 'hard'
dPhiJJStr='acos((Jet_pt[1]+Jet_pt[0]*cos(Jet_phi[1]-Jet_phi[0]))/sqrt(Jet_pt[1]**2+Jet_pt[0]**2+2*Jet_pt[0]*Jet_pt[1]*cos(Jet_phi[1]-Jet_phi[0])))'

cBkg = getChain([WJetsHTToLNu[lepSel], ttJets[lepSel]],histname='')
cS1200 = getChain(SMS_T5qqqqWW_Gl1200_Chi1000_LSP800[lepSel],histname='')
cS1500 = getChain(SMS_T5qqqqWW_Gl1500_Chi800_LSP100[lepSel],histname='')
cS1000 = getChain(T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],histname='')
cBkg.SetAlias('DFJJ',dPhiJJStr)
cS1200.SetAlias('DFJJ',dPhiJJStr)
cS1500.SetAlias('DFJJ',dPhiJJStr)
cS1000.SetAlias('DFJJ',dPhiJJStr)

presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&deltaPhi_Wl>1.0"
prefix = presel.split('&&')[0]+'_SRfinder_Phys14V3'
#prefix = presel.split('&&')[0]+'_SRfinder_Phys14V3_addCut'

path = '/data/'+username+'/results2015/SRfinder/'
if not os.path.exists(path):
  os.makedirs(path)

streg = [[(250, 350), 1.], [(350, 450), 1.],[(450, -1), 1.]]
htreg = [(500,750), (750,1000), (1000,1250), (1250,-1)]
njreg = [(5,5),(6,7),(8,-1)]
btreg = (0,0) 
addCut = ['DFJJ<2.0','DFJJ<1.5']

bestS1200 = []
bestS1500 = []
SR = []
for i_htb, htb in enumerate(htreg):
  for stb, dPhiCut in streg:
    for srNJet in njreg:
      #for add in addCut:

        #name, cut = nameAndCut(stb, htb, srNJet, btb=btreg, presel=presel+'&&'+add, btagVar = 'nBJetMediumCMVA30')
        name, cut = nameAndCut(stb, htb, srNJet, btb=btreg, presel=presel, btagVar = 'nBJetMediumCMVA30')
        print 'HT: ',htb,'|ST: ',stb,'|nJets: ',srNJet#, '|additional: ',add
        B = getYieldFromChain(cBkg, cut, weight = "weight")
        B_Var = getYieldFromChain(cBkg, cut, weight = "weight*weight")
        S1200 = getYieldFromChain(cS1200, cut, weight = "weight")
        S1200_Var = getYieldFromChain(cS1200, cut, weight = "weight*weight")
        S1500 = getYieldFromChain(cS1500, cut, weight = "weight")
        S1500_Var = getYieldFromChain(cS1500, cut, weight = "weight*weight")
        S1000 = getYieldFromChain(cS1000, cut, weight = "weight")
        S1000_Var = getYieldFromChain(cS1000, cut, weight = "weight*weight")
        FOM1200 = getFOM(S1200,S1200_Var, B, B_Var)
        FOM1500 = getFOM(S1500,S1500_Var, B, B_Var)
        FOM1000 = getFOM(S1000,S1000_Var, B, B_Var)

        #SR.append({'FOM1200':FOM1200, 'FOM1500':FOM1500, 'S1200':S1200, 'S1200_Var':S1200_Var, 'S1500':S1500, 'S1500_Var':S1500_Var, 'B':B, 'B_Var':B_Var, 'ST':stb, 'HT':htb, 'nJet':srNJet, 'additional':add})
        SR.append({'FOM1200':FOM1200, 'FOM1500':FOM1500,'FOM1000':FOM1000 ,'S1200':S1200, 'S1200_Var':S1200_Var, 'S1500':S1500, 'S1500_Var':S1500_Var,'S1000':S1000,'S1000_Var':S1000_Var, 'B':B, 'B_Var':B_Var, 'ST':stb, 'HT':htb, 'nJet':srNJet})

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

bestS1200 = SR
bestS1200.sort(key=operator.itemgetter('FOM1200'), reverse=True)
bestS1200=filter(lambda x:not x['FOM1200']=='nan', bestS1200)

bestS1500 = SR
bestS1500.sort(key=operator.itemgetter('FOM1500'), reverse=True)
bestS1500=filter(lambda x:not x['FOM1500']=='nan', bestS1500)

bestS1000 = SR
bestS1000.sort(key=operator.itemgetter('FOM1000'), reverse=True)
bestS1000=filter(lambda x:not x['FOM1000']=='nan', bestS1000)

pickle.dump((bestS1200,bestS1500,bestS1000), file(path+prefix+'_pkl','w'))

bestS1200, bestS1500 , bestS1000 = pickle.load(file('/data/'+username+'/results2015/SRfinder/'+prefix+'_pkl'))

print "signal yields (T5q^{4} 1.2/1.0/0.8)"
print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrrrr|c|}\\hline'
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrrrr|c|}\\hline'
#print ' \HT     & \\njet & \ST & Add Cut  & \multicolumn{3}{c|}{\TFiveqqqqHM} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
print ' \HT     & \\njet & \ST  & \multicolumn{3}{c|}{\TFiveqqqqHM} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
#print '$[$GeV$]$    &        &$[$GeV$]$ & & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
print '$[$GeV$]$    &        &$[$GeV$]$ &  \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
for dict in bestS1200:
  #print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+'\\'+str(dict['additional'])+'&'+getNumString(dict['S1200'],sqrt(dict['S1200_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1200'],3))+'\\\\\hline'
  print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+getNumString(dict['S1200'],sqrt(dict['S1200_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1200'],3))+'\\\\\hline'
print '\end{tabular}}\end{center}\caption{\TFiveqqqqHM}\end{table}'


print "signal yields (T5q^{4} 1.5/0.8/0.1)"
print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrrrr|c|}\\hline'
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrrrr|c|}\\hline'
#print ' \HT     & \\njet & \ST  & Add Cut & \multicolumn{3}{c|}{\TFiveqqqqHL} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
print ' \HT     & \\njet & \ST   & \multicolumn{3}{c|}{\TFiveqqqqHL} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
#print '$[$GeV$]$    &    &$[$GeV$]$ & & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
print '$[$GeV$]$    &    &$[$GeV$]$ & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
for dict in bestS1500:
  #print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+str(dict['additional'])+'&'+getNumString(dict['S1500'],sqrt(dict['S1500_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1500'],3))+'\\\\\hline'
  print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+getNumString(dict['S1500'],sqrt(dict['S1500_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1500'],3))+'\\\\\hline'
print '\end{tabular}}\end{center}\caption{\TFiveqqqqHL}\end{table}'


print "signal yields (T5q^{4} 1.0/0.8/0.7)"
print
#print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|c|rrr|rrrrr|c|}\\hline'
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrrrr|c|}\\hline'
#print ' \HT     & \\njet & \ST  & Add Cut & \multicolumn{3}{c|}{\TFiveqqqqHL} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
print ' \HT     & \\njet & \ST   & \multicolumn{3}{c|}{$T5q^{4} 1.0/0.8/0.7$} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
#print '$[$GeV$]$    &    &$[$GeV$]$ & & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
print '$[$GeV$]$    &    &$[$GeV$]$ & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{$\\frac{S}{\sqrt{B+(0.2B)^2}}$} \\\\\hline'
for dict in bestS1000:
  #print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+str(dict['additional'])+'&'+getNumString(dict['S1500'],sqrt(dict['S1500_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1500'],3))+'\\\\\hline'
  print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+getNumString(dict['S1000'],sqrt(dict['S1000_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1000'],3))+'\\\\\hline'
print '\end{tabular}}\end{center}\caption{$T5q^{4} 1.0/0.8/0.7$}\end{table}'



