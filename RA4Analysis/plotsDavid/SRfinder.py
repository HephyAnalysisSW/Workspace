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
cBkg.SetAlias('dPhiJJ',dPhiJJStr)
cS1200.SetAlias('dPhiJJ',dPhiJJStr)
cS1500.SetAlias('dPhiJJ',dPhiJJStr)

prefix = 'singleMuonic_SRfinder_Phys14V3'
presel = "singleMuonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&deltaPhi_Wl>1.0"
path = '/data/'+username+'/results2015/SRfinder/'
if not os.path.exists(path):
  os.makedirs(path)

streg = [[(200,-1), 1.], [(250, -1), 1.], [(350, -1), 1.], [(450, -1), 1.], [(200,250), 1.], [(250, 350), 1.], [(350, 450), 1.]]
htreg = [(400,-1), (500,-1), (750,-1), (1000,-1), (1250,-1), (500,750), (750,1000), (1000,1250)]
njreg = [(5,5),(6,7),(6,-1),(8,-1)]
btreg = (0,0) 
#addCut = ['dPhiJJ<2.0','dPhiJJ<1.5']

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
      FOM1200 = getFOM(S1200,S1200_Var, B, B_Var)
      FOM1500 = getFOM(S1500,S1500_Var, B, B_Var)

      SR.append({'FOM1200':FOM1200, 'FOM1500':FOM1500, 'S1200':S1200, 'S1200_Var':S1200_Var, 'S1500':S1500, 'S1500_Var':S1500_Var, 'B':B, 'B_Var':B_Var, 'ST':stb, 'HT':htb, 'nJet':srNJet})#, 'additional':add})

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

pickle.dump((bestS1200,bestS1500), file(path+prefix+'_pkl','w'))

bestS1200, bestS1500 = pickle.load(file('/data/'+username+'/results2015/SRfinder/'+prefix+'_pkl'))

print "signal yields (T5q^{4} 1.2/1.0/0.8)"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrrrr|c|}\\hline'
print ' \HT     & \\njet & \ST   & \multicolumn{3}{c|}{\TFiveqqqqHM} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
print '$[$GeV$]$    &        &$[$GeV$]$  & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{\frac{S}{\sqrt{B+(0.2B)^2}}} \\\\\hline'
for dict in bestS1200:
  print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+getNumString(dict['S1200'],sqrt(dict['S1200_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1200'],3))+'\\\\\hline'
print '\end{tabular}}\end{center}\caption{\TFiveqqqqHM}\end{table}'

print "signal yields (T5q^{4} 1.5/0.8/0.1)"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrrrr|c|}\\hline'
print ' \HT     & \\njet & \ST     & \multicolumn{3}{c|}{\TFiveqqqqHL} & \multicolumn{5}{c|}{B (only W, tt)}&\multicolumn{1}{c|}{FOM}\\\\ %\hline'
print '$[$GeV$]$    &        &$[$GeV$]$  & \multicolumn{3}{c|}{}             & \multicolumn{5}{c|}{}              &\multicolumn{1}{c|}{\frac{S}{\sqrt{B+(0.2B)^2}}} \\\\\hline'
for dict in bestS1500:
  print str(dict['HT'])+'&'+str(dict['nJet'])+'&'+str(dict['ST'])+'&'+getNumString(dict['S1500'],sqrt(dict['S1500_Var']),acc=3)+'&'+getNumString(dict['B'],sqrt(dict['B_Var']),acc=3,systematic=True)+'&'+str(round(dict['FOM1500'],3))+'\\\\\hline'
print '\end{tabular}}\end{center}\caption{\TFiveqqqqHL}\end{table}'

