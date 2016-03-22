import ROOT
import pickle
from array import array
import operator
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.signalRegions import *
from Workspace.HEPHYPythonTools.user import username
from math import sqrt, pi
from general_config import *
ROOT.TH1F().SetDefaultSumw2()

#weight_str = "((weight*2.25)/3)"
weight_str = weight_str_signal_CV

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
btag_str = 'nBJetMediumCSV30'
cBkg = getChain([WJetsHTToLNu_25ns,TTJets_combined,singleTop_25ns, DY_25ns,TTV_25ns,QCDHT_25ns],histname='')


btagString = "nBJetMediumCSV30"

presel_bkg = 'singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_eeBadScFilter&&Flag_EcalDeadCellTriggerPrimitiveFilter'
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&JetForMET_pt[0]<3000"
prefix = presel.split('&&')[0]+'_SRfinder_miniAODv2'

path = '/afs/hephy.at/user/e/easilar/www/MC/Spring15/25ns/SRFinder/plots/'
if not os.path.exists(path):
  os.makedirs(path)

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


bin = {}
for srNJet in sorted(signalRegions):
  bin[srNJet]={}
  for stb in sorted(signalRegions[srNJet]):
    bin[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      bin[srNJet][stb][htb] = {}
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      name, c_MB_SR =  nameAndCut(stb, htb, srNJet,     btb=(0,-1), presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      dummy, c_MB_CR =  nameAndCut(stb, htb, srNJet,    btb=(0,-1), presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      dummy, c_SB_tt_CR =  nameAndCut(stb, htb, (4,5),  btb=(0,-1), presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      dummy, c_SB_W_CR =  nameAndCut(stb, htb, (3,4),   btb=(0,-1), presel=presel+"&&deltaPhi_Wl<"+str(deltaPhiCut), btagVar = btagString)
      dummy, c_SB_tt_SR =  nameAndCut(stb, htb, (4,5),  btb=(0,-1), presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      dummy, c_SB_W_SR =  nameAndCut(stb, htb, (3,4),   btb=(0,-1), presel=presel+"&&deltaPhi_Wl>"+str(deltaPhiCut), btagVar = btagString)
      bin[srNJet][stb][htb]["signals"] = {}
      for signal in allSignals:
        #print sig
        #exec("signal="+sig)
        for mglu in signal.keys() :
          bin[srNJet][stb][htb]["signals"][mglu] = {}
          for mlsp in signal[mglu].keys() :
            s_chain = getChain(signal[mglu][mlsp],histname='')
            bin[srNJet][stb][htb]["signals"][mglu][mlsp] = {"yield_MB_SR":  getYieldFromChain(s_chain, c_MB_SR,     weight = weight_str+"*weightBTag0_SF")      ,"stat_err_MB_SR":   sqrt(getYieldFromChain(s_chain, c_MB_SR, weight = weight_str+"*"+weight_str+"*weightBTag0_SF*weightBTag0_SF")),\
                                                          "yield_MB_CR":    getYieldFromChain(s_chain, c_MB_CR,     weight = weight_str+"*weightBTag0_SF")      ,"stat_err_MB_CR":   sqrt(getYieldFromChain(s_chain, c_MB_CR, weight    = weight_str+"*"+weight_str+"*weightBTag0_SF*weightBTag0_SF"))             ,\
                                                          "yield_SB_tt_SR": getYieldFromChain(s_chain, c_SB_tt_SR,  weight = weight_str+"*weightBTag1_SF")      ,"stat_err_SB_tt_SR":sqrt(getYieldFromChain(s_chain, c_SB_tt_SR, weight = weight_str+"*"+weight_str+"*weightBTag1_SF*weightBTag1_SF"))          ,\
                                                          "yield_SB_tt_CR": getYieldFromChain(s_chain, c_SB_tt_CR,  weight = weight_str+"*weightBTag1_SF")      ,"stat_err_SB_tt_CR":sqrt(getYieldFromChain(s_chain, c_SB_tt_CR, weight = weight_str+"*"+weight_str+"*weightBTag1_SF*weightBTag1_SF"))          ,\
                                                          "yield_SB_W_SR":  getYieldFromChain(s_chain, c_SB_W_SR,   weight = weight_str+"*weightBTag0_SF")      ,"stat_err_SB_W_SR": sqrt(getYieldFromChain(s_chain, c_SB_W_SR, weight     = weight_str+"*"+weight_str+"*weightBTag0_SF*weightBTag0_SF"))              ,\
                                                          "yield_SB_W_CR":  getYieldFromChain(s_chain, c_SB_W_CR,   weight = weight_str+"*weightBTag0_SF")      ,"stat_err_SB_W_CR": sqrt(getYieldFromChain(s_chain, c_SB_W_CR, weight     = weight_str+"*"+weight_str+"*weightBTag0_SF*weightBTag0_SF"))               \
                                                          }
      bin[srNJet][stb][htb]['name']=name

pickle.dump(bin,file('/data/easilar/Spring15/25ns/allSignals_2p3_pkl','w'))

#print bin
#for srNJet in sorted(signalRegions):
#  for stb in sorted(signalRegions[srNJet]):
#    for htb in sorted(signalRegions[srNJet][stb]):
#      cb = ROOT.TCanvas("cb","cb",800,800)
#      cb.cd()
#      #cb.SetLeftMargin(2)
#      #cb.SetBottomMargin(10)
#      ##cb.SetGrid()
#      latex = ROOT.TLatex()
#      latex.SetNDC()
#      latex.SetTextSize(0.04)
#      latex.SetTextAlign(11)
#      leg = ROOT.TLegend(0.55,0.65,0.8,0.75)
#      leg.SetBorderSize(1)
#      h_fom1000 = ROOT.TH1F('hfom1000', 'h_fom1000',len(deltaPhiCuts)-1,deltaPhiCuts)
#      h_fom1200 = ROOT.TH1F('hfom1200', 'h_fom1200',len(deltaPhiCuts)-1,deltaPhiCuts)
#      h_fom1500 = ROOT.TH1F('hfom1500', 'h_fom1500',len(deltaPhiCuts)-1,deltaPhiCuts)
#      h_fom1000.SetMinimum(0)
#      h_fom1200.SetMinimum(0)
#      h_fom1500.SetMinimum(0)
#      h_fom1000.SetMaximum(5)
#      h_fom1200.SetMaximum(5)
#      h_fom1500.SetMaximum(5)
#      index =0
#      for deltaPhiCut in deltaPhiCuts:
#        index += 1
#        h_fom1000.SetBinContent(index,bin[srNJet][stb][htb][deltaPhiCut]['FOM1000'])
#        h_fom1200.SetBinContent(index,bin[srNJet][stb][htb][deltaPhiCut]['FOM1200'])
#        h_fom1500.SetBinContent(index,bin[srNJet][stb][htb][deltaPhiCut]['FOM1500'])
#      h_fom1000.SetLineColor(ROOT.kRed) 
#      h_fom1200.SetLineColor(ROOT.kBlue)
#      h_fom1500.SetLineColor(ROOT.kBlack)
#      h_fom1000.Draw("histo")    
#      h_fom1200.Draw("histo same")
#      h_fom1500.Draw("histo same")
#      leg.AddEntry(h_fom1000, "1000" ,"l")
#      leg.AddEntry(h_fom1200, "1200" ,"l")
#      leg.AddEntry(h_fom1500, "1500" ,"l")
#      leg.Draw()
#      cb.SetGridx()
#      cb.Draw()
#      cb.SaveAs(path+bin[srNJet][stb][htb]['name']+'_fom.png')
#      cb.SaveAs(path+bin[srNJet][stb][htb]['name']+'_fom.pdf')
#      cb.SaveAs(path+bin[srNJet][stb][htb]['name']+'_fom.root')













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


