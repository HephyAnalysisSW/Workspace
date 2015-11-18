import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import *# getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision

#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_fromArthur import *
from rCShelpers import *

from Workspace.RA4Analysis.signalRegions import *

from math import sqrt, pi, cosh
from array import array

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

def filterParticles(l, values, attribute):
  for a in l:
    for v in values:
      if abs(a[attribute])==v: yield a

def getWMass(c):
  para = ['pt','phi','eta','pdgId','motherId']
  genPartAll = [getObjDict(c, 'genPartAll_', para, j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  Neutrinos = []
  Leptons = []
  NeutrinosFromW = []
  NeutrinosFromTau = []
  LeptonsFromW = []
  LeptonsFromTau = []
  for Neutrino in filterParticles(genPartAll, [12,14], 'pdgId'):
    Neutrinos.append(Neutrino)
  for NeutrinoFromW in filterParticles(Neutrinos, [24], 'motherId'):
    NeutrinosFromW.append(NeutrinoFromW)
  #for NeutrinoFromTau in filterParticles(Neutrinos, [15], 'motherId'):
  #  NeutrinosFromTau.append(NeutrinoFromTau)
  for Lepton in filterParticles(genPartAll, [11,13], 'pdgId'):
    Leptons.append(Lepton)
  for LeptonFromW in filterParticles(Leptons, [24], 'motherId'):
    LeptonsFromW.append(LeptonFromW)
  #for LeptonFromTau in filterParticles(Leptons, [15], 'motherId'):
  #  LeptonsFromTau.append(LeptonFromTau)
  WMass = 0.
  if len(NeutrinosFromW)>0:
    if len(NeutrinosFromW)>1: print 'this should not have happened'
    if len(LeptonsFromW)>0:
      if len(LeptonsFromW)>1: print 'this should not have happened'
      LeptonPt = LeptonsFromW[0]['pt']
      LeptonPhi = LeptonsFromW[0]['phi']
      LeptonEta = LeptonsFromW[0]['eta']
      NeutrinoPt = NeutrinosFromW[0]['pt']
      NeutrinoPhi = NeutrinosFromW[0]['phi']
      NeutrinoEta = NeutrinosFromW[0]['eta']
      WMass = sqrt(2*LeptonPt*NeutrinoPt*(cosh(LeptonEta-NeutrinoEta)-cos(LeptonPhi-NeutrinoPhi)))
  #else: 
  #  print 'No promt neutrino found'
  #  if len(NeutrinosFromTau)>0:
  #    print 'But found', len(NeutrinosFromTau), 'neutrinos from tau'
  #    if len(NeutrinosFromTau)>1: print 'this should not have happened'
  #    if len(LeptonsFromTau)>0:
  #      if len(LeptonsFromTau)>1: print 'this should not have happened'
  #      LeptonPt =    LeptonsFromTau[0]['pt']
  #      LeptonPhi =   LeptonsFromTau[0]['phi']
  #      LeptonEta =   LeptonsFromTau[0]['eta']
  #      NeutrinoPt =  NeutrinosFromTau[0]['pt']
  #      NeutrinoPhi = NeutrinosFromTau[0]['phi']
  #      NeutrinoEta = NeutrinosFromTau[0]['eta']
  #      WMass = sqrt(2*LeptonPt*NeutrinoPt*(cosh(LeptonEta-NeutrinoEta)-cos(LeptonPhi-NeutrinoPhi)))
  #      print WMass
  if WMass < 1.:
    WMass = float('nan')
  return WMass

def getNeutrino(c):
  para = ['pt','phi','eta','pdgId','motherId']
  genPartAll = [getObjDict(c, 'genPartAll_', para, j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  #Neutrino = [i for i in genPartAll if (abs(i['pdgId'])==14 or abs(i['pdgId'])==12)]
  Neutrinos = []
  NeutrinosFromW = []
  for Neutrino in filterParticles(genPartAll, [12,14], 'pdgId'):
    Neutrinos.append(Neutrino)
  for NeutrinoFromW in filterParticles(Neutrinos, [24], 'motherId'):
    NeutrinosFromW.append(NeutrinoFromW)
  #Neutrino = filter(lambda w:(abs(w['pdgId'])==14 or abs(w['pdgId'])==12), genPartAll)
  #NeutrinoFromW = filter(lambda w:abs(w['motherId'])==24, Neutrino)
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  if len(NeutrinosFromW)>0:
    if len(NeutrinosFromW)>1: print 'this should not have happened'
    NeutrinoPt = NeutrinosFromW[0]['pt']
    NeutrinoPhi = NeutrinosFromW[0]['phi']
    return NeutrinoPt, NeutrinoPhi, metGenPt
  else: return 0., 0.

lepSel = 'hard'

#WJETS  = getChain(WJetsHTToLNu[lepSel],histname='')
WJETS  = getChain(WJetsHT_25ns,histname='')

streg = [[(450,-1), 1.]]#, [(350, 450), 1.],  [(450, -1), 1.] ]
htreg = [(500,750)]#,(750,1000),(1000,-1)]#,(1000,1250),(1250,-1)]#,(1250,-1)]
btreg = (0,0)
njreg = [(2,2),(3,3),(4,4),(5,5),(6,7),(8,-1)]#,(7,7),(8,8),(9,9)]
nbjreg = [(0,0),(1,1),(2,2)]

presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&(sqrt((-met_genPt*cos(met_genPhi)+met_pt*cos(met_phi))**2+(-met_genPt*sin(met_genPhi)+met_pt*sin(met_phi))**2)/met_genPt)<1'
colors = [ROOT.kBlue+2, ROOT.kBlue-7, ROOT.kCyan-9, ROOT.kCyan-2, ROOT.kGreen-6, ROOT.kOrange-4, ROOT.kOrange+8, ROOT.kRed+1]
first = True

can = ROOT.TCanvas('c1','c1',800,600)
can.SetLogy()
Whists = {}

triggers = "(HLT_EleHT350||HLT_MuHT350)"
filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_CSCTightHaloFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"
newpresel = presel

path = '/afs/hephy.at/user/d/dspitzbart/www/Spring15/deltaPhi_vs_Wmass/'

if not os.path.exists(path):
  os.makedirs(path)



#
#stb = (250,-1)
#htb = (500,-1)
#njb = (3,-1)
#btreg = (0,0)
#
#cname, cut = nameAndCut(stb,htb,njb, btb=btreg ,presel=newpresel)
#dPhiStr = 'deltaPhi_Wl'
#WJETS.Draw('>>eList',cut)
#elist = ROOT.gDirectory.Get("eList")
#number_events = elist.GetN()
#
#print 'Will loop over',number_events, 'events, patience please'
#
#WmassHist = ROOT.TH1F('Whist_lowMass','low W mass',100,0,1000)
#Whist_lowMass = ROOT.TH1F('Whist_lowMass','low W mass',16,0,3.2)
#Whist_highMass = ROOT.TH1F('Whist_lowMass','low W mass',16,0,3.2)
#Whist_lowMass.SetLineColor(ROOT.kBlue)
#Whist_highMass.SetLineColor(ROOT.kRed)

W_lowMass = {}
W_highMass ={}
signalRegions = signalRegion3fb

for srNJet in sorted(signalRegions):
  W_lowMass[srNJet] = {}
  W_highMass[srNJet] ={}
  for stb in sorted(signalRegions[srNJet]):
    W_lowMass[srNJet][stb] = {}
    W_highMass[srNJet][stb] ={}
    for htb in sorted(signalRegions[srNJet][stb]):
      print
      print '#############################################'
      print 'bin: \t njet \t\t LT \t\t HT'
      if len(str(srNJet))<7:
        print '\t',srNJet,'\t\t',stb,'\t',htb
      else:
        print '\t',srNJet,'\t',stb,'\t',htb
      print '#############################################'
      print
      cname, cut = nameAndCut(stb,htb,srNJet, btb=(0,0) ,presel=newpresel)
      W_lowMass[srNJet][stb][htb] = {}
      W_highMass[srNJet][stb][htb] = {}
      #W_lowMass[srNJet][stb][htb] = {'hist': ROOT.TH1F('Whist_lowMass'+cname,'low W mass',16,0,3.2)}
      #W_highMass[srNJet][stb][htb] = {'hist':ROOT.TH1F('Whist_highMass'+cname,'high W mass',16,0,3.2)}
      #W_lowMass[srNJet][stb][htb]['hist'].SetLineColor(ROOT.kBlue)
      #W_highMass[srNJet][stb][htb]['hist'].SetLineColor(ROOT.kRed)
      #W_lowMass[srNJet][stb][htb]['hist'].SetMarkerStyle(0)
      #W_highMass[srNJet][stb][htb]['hist'].SetMarkerStyle(0)
      #W_lowMass[srNJet][stb][htb]['hist'].Sumw2()
      #W_highMass[srNJet][stb][htb]['hist'].Sumw2()
      #
      #WJETS.Draw('deltaPhi_Wl>>Whist_lowMass'+cname,'weight*('+cut+'&&genPartAll_mass<100&&abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)!=24)')
      #WJETS.Draw('deltaPhi_Wl>>Whist_highMass'+cname,'weight*('+cut+'&&genPartAll_mass>=100&&abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)!=24)')
      #
      #highMassHighDPhiYield = 0.
      #lowMassHighDPhiYield = 0.
      #for i in range(6,17):
      #  highMassHighDPhiYield += W_highMass[srNJet][stb][htb]['hist'].GetBinContent(i)
      #  lowMassHighDPhiYield += W_lowMass[srNJet][stb][htb]['hist'].GetBinContent(i)
      #
      #W_lowMass[srNJet][stb][htb]['yield'] = W_lowMass[srNJet][stb][htb]['hist'].Integral()
      #W_highMass[srNJet][stb][htb]['yield'] = W_highMass[srNJet][stb][htb]['hist'].Integral()

      #W_lowMass[srNJet][stb][htb]['hist'].Scale(1/W_lowMass[srNJet][stb][htb]['hist'].Integral())
      #W_highMass[srNJet][stb][htb]['hist'].Scale(1/W_highMass[srNJet][stb][htb]['hist'].Integral())
      #
      #can = ROOT.TCanvas('c','c',700,700)
      #can.SetLogy()
      #
      #totalL = ROOT.TLegend(0.65,0.82,0.98,0.95)
      #totalL.SetFillColor(ROOT.kWhite)
      #totalL.SetShadowColor(ROOT.kWhite)
      #totalL.SetBorderSize(1)
      #totalL.AddEntry(W_lowMass[srNJet][stb][htb]['hist'])
      #totalL.AddEntry(W_highMass[srNJet][stb][htb]['hist'])
      #
      #W_lowMass[srNJet][stb][htb]['hist'].GetXaxis().SetTitle('#Delta#Phi (W,l)')
      #W_lowMass[srNJet][stb][htb]['hist'].GetYaxis().SetTitle('fraction')
      #
      #latex1 = ROOT.TLatex()
      #latex1.SetNDC()
      #latex1.SetTextSize(0.04)
      #latex1.SetTextAlign(11)
      #
      #W_lowMass[srNJet][stb][htb]['hist'].Draw('e hist')
      #W_highMass[srNJet][stb][htb]['hist'].Draw('e hist same')
      #totalL.Draw()
      #latex1.DrawLatex(0.35,0.92,'h/l:'+str(round(W_highMass[srNJet][stb][htb]['yield']/W_lowMass[srNJet][stb][htb]['yield'],2)))
      #latex1.DrawLatex(0.35,0.87,'h+#Delta#Phi>1 y:'+str(round(highMassHighDPhiYield,2)))
      #latex1.DrawLatex(0.35,0.82,'l+#Delta#Phi>1 y:'+str(round(lowMassHighDPhiYield,2)))
      #can.Print(path+cname+'WmassSplit100.png')
      #can.Print(path+cname+'WmassSplit100.root')
      deltaPhi=signalRegions[srNJet][stb][htb]['deltaPhi']
      W_lowMass[srNJet][stb][htb]['rcs_total'] = getRCS(WJETS, cut, deltaPhi)
      W_lowMass[srNJet][stb][htb]['yield_totalHighDPhi'] = getYieldFromChain(WJETS, cutString=cut+'&&deltaPhi_Wl>='+str(deltaPhi))
      W_lowMass[srNJet][stb][htb]['mass_ratio'] = getRCS(WJETS, cut+'&&abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)!=24', 100, cutVar='genPartAll_mass', varMax=1000000)
      W_lowMass[srNJet][stb][htb]['rcs'] = getRCS(WJETS, cut+'&&genPartAll_mass<100&&abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)!=24',deltaPhi)
      W_lowMass[srNJet][stb][htb]['yield_highDPhi'] = getYieldFromChain(WJETS, cutString=cut+'&&genPartAll_mass<100&&abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)!=24&&deltaPhi_Wl>='+str(deltaPhi))
      W_lowMass[srNJet][stb][htb]['yield_highDPhi_Var'] = getYieldFromChain(WJETS, cutString=cut+'&&genPartAll_mass<100&&abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)!=24&&deltaPhi_Wl>='+str(deltaPhi), weight = 'weight**2')

      W_highMass[srNJet][stb][htb]['rcs'] = getRCS(WJETS, cut+'&&genPartAll_mass>=100&&abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)!=24',deltaPhi)
      W_highMass[srNJet][stb][htb]['yield_highDPhi'] = getYieldFromChain(WJETS, cutString=cut+'&&genPartAll_mass>=100&&abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)!=24&&deltaPhi_Wl>='+str(deltaPhi))
      W_highMass[srNJet][stb][htb]['yield_highDPhi_Var'] = getYieldFromChain(WJETS, cutString=cut+'&&genPartAll_mass>=100&&abs(genPartAll_pdgId)==24&&abs(genPartAll_motherId)!=24&&deltaPhi_Wl>='+str(deltaPhi), weight = 'weight**2')
      
      print 'Yield highDPhi total', round(W_lowMass[srNJet][stb][htb]['yield_totalHighDPhi'],2), round(W_lowMass[srNJet][stb][htb]['yield_highDPhi']+W_highMass[srNJet][stb][htb]['yield_highDPhi'],2)
      

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

print "Results"
print
print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|}\\hline'
print ' \\njet & \ST & \HT     &\multicolumn{9}{c|}{$R_{CS}$} & \multicolumn{6}{c|}{yield $\Delta\Phi< x$} & \multicolumn{6}{c|}{yield $\Delta\Phi\geq x$} & \multicolumn{3}{c|}{ratio}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$ & \multicolumn{3}{c}{$m_{W}<100$} & \multicolumn{3}{c}{$m_{W}\geq100$} & \multicolumn{3}{c}{$m_{W}<100$} & \multicolumn{3}{c}{$m_{W}\geq100$} & \multicolumn{3}{c|}{total} & \multicolumn{3}{c}{$m_{W}<100$} & \multicolumn{3}{c|}{$m_{W}\geq100$} & \multicolumn{3}{c|}{$\\frac{m_{W}\geq100}{m_{W}<100}$}\\\ '
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
      W_lowMass_lowDPhi = W_lowMass[srNJet][stb][htb]['yield_highDPhi']/W_lowMass[srNJet][stb][htb]['rcs']['rCS']
      W_lowMass_lowDPhi_err = W_lowMass_lowDPhi*sqrt(W_lowMass[srNJet][stb][htb]['yield_highDPhi_Var']/W_lowMass[srNJet][stb][htb]['yield_highDPhi']**2 + W_lowMass[srNJet][stb][htb]['rcs']['rCSE_sim']**2/W_lowMass[srNJet][stb][htb]['rcs']['rCS']**2)
      W_highMass_lowDPhi = W_highMass[srNJet][stb][htb]['yield_highDPhi']/W_highMass[srNJet][stb][htb]['rcs']['rCS']
      W_highMass_lowDPhi_err = W_highMass_lowDPhi*sqrt(W_highMass[srNJet][stb][htb]['yield_highDPhi_Var']/W_highMass[srNJet][stb][htb]['yield_highDPhi']**2 + W_highMass[srNJet][stb][htb]['rcs']['rCSE_sim']**2/W_highMass[srNJet][stb][htb]['rcs']['rCS']**2)
      
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(W_lowMass[srNJet][stb][htb]['rcs']['rCS'], W_lowMass[srNJet][stb][htb]['rcs']['rCSE_sim'],3)\
          + ' & '+getNumString(W_highMass[srNJet][stb][htb]['rcs']['rCS'], W_highMass[srNJet][stb][htb]['rcs']['rCSE_sim'],3)\
          + ' & '+getNumString(W_lowMass[srNJet][stb][htb]['rcs_total']['rCS'], W_lowMass[srNJet][stb][htb]['rcs_total']['rCSE_sim'],3)\
          + ' & '+getNumString(W_lowMass_lowDPhi,W_lowMass_lowDPhi_err)\
          + ' & '+getNumString(W_highMass_lowDPhi,W_highMass_lowDPhi_err)\
          + ' & '+getNumString(W_lowMass[srNJet][stb][htb]['yield_highDPhi'], sqrt(W_lowMass[srNJet][stb][htb]['yield_highDPhi_Var']))\
          + ' & '+getNumString(W_highMass[srNJet][stb][htb]['yield_highDPhi'], sqrt(W_highMass[srNJet][stb][htb]['yield_highDPhi_Var']))\
          + ' & '+getNumString(W_lowMass[srNJet][stb][htb]['mass_ratio']['rCS'], W_lowMass[srNJet][stb][htb]['mass_ratio']['rCSE_sim'])+'\\\\ '
    if htb[1] == -1 : print '\\cline{2-27}'
print '\\hline\end{tabular}}\end{center}\caption{\Rcs values of different masses of W bosons, W+Jets background, 3$fb^{-1}$}\label{tab:0b_Wmass}\end{table}'


#for stb, dPhiCut in streg:
#  Whists[stb] = {}
#  for i_htb, htb in enumerate(htreg):
#    Whists[stb][htb] = {}
#    totalL = ROOT.TLegend(0.6,0.6,0.95,0.93)
#    totalL.SetFillColor(ROOT.kWhite)
#    totalL.SetShadowColor(ROOT.kWhite)
#    totalL.SetBorderSize(1)
#    for i_njb, njb in enumerate(njreg):
#      print 'Processing njet',njb
#      cname, cut = nameAndCut(stb,htb,njb, btb=btreg ,presel=presel)
#      dPhiStr = 'deltaPhi_Wl'
#      WJETS.Draw('>>eList',cut)
#      elist = ROOT.gDirectory.Get("eList")
#      number_events = elist.GetN()
#      Whists[stb][htb][njb] = {'hist':ROOT.TH1F('h'+str(i_njb),str(njb),50,0,500)}
#      Whists[stb][htb][njb]['hist'].Sumw2()
#      counter = 0.
#      total = 0.
#      for i in range(number_events):
#        WJETS.GetEntry(elist.GetEntry(i))
#        weight = getVarValue(WJETS,"weight")
#        deltaPhi = WJETS.GetLeaf(dPhiStr).GetValue()
#        WMass = getWMass(WJETS)
#        deltaPhi = WJETS.GetLeaf(dPhiStr).GetValue()
#        if WMass>100.:
#          #print WMass, deltaPhi, weight
#          if deltaPhi>1.:
#            counter += weight
#          total += weight
#        #if abs(neutrinoPt-genMetPt)<5:
#        #  h.Fill(deltaPhi, weight)
#        Whists[stb][htb][njb]['hist'].Fill(WMass, weight)
#      Whists[stb][htb][njb]['hist'].SetLineColor(colors[i_njb])
#      totalL.AddEntry(Whists[stb][htb][njb]['hist'])
#      print 'Ratio of deltaPhi>1 in M(W)>100', counter/(total-counter)
#      if first:
#        Whists[stb][htb][njb]['hist'].Draw('hist')
#        first = False
#      else: Whists[stb][htb][njb]['hist'].Draw('hist same')
      
