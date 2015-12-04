import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from rCShelpers import *
import math
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

def sign(a):
  return (a > 0) - (a < 0)

useWcorrection = False
useTTcorrection = False
signal = False

prefix = 'singleLeptonic_Spring15_'
#path1 = '/data/'+username+'/Results2015/Prediction_bweightTemplate_data_reducedSR_lep_1.26/'
#path2 = '/data/'+username+'/Results2015/Prediction_bweightTemplate_MC_reducedSR_lep_3.0/'

pdata1 = '/data/'+username+'/Results2015/Prediction_data_newSR_lep_SFtemplates_1.55/'
pmc1 = '/data/'+username+'/Results2015/Prediction_MCwSF_newSR_lep_SFtemplates_1.55/'
pdata2 = '/data/'+username+'/Results2015/Prediction_data_newSR_lep_SFtemplates_1.26/'
#path1 = '/data/'+username+'/Results2015/Prediction_SFTemplate_MC_fullSR_lep_3.0/'
#path2 = '/data/'+username+'/Results2015/Prediction_SFTemplate_MC_fullSR_lep_3.0_b_Up/'
#path3 = '/data/'+username+'/Results2015/Prediction_SFTemplate_MC_fullSR_lep_3.0_b_Down/'
#path4 = '/data/'+username+'/Results2015/Prediction_SFTemplate_MC_fullSR_lep_3.0_light_Up/'
#path5 = '/data/'+username+'/Results2015/Prediction_SFTemplate_MC_fullSR_lep_3.0_light_Down/'

data1 = pickle.load(file(pdata1+prefix+'_estimationResults_pkl'))
data2 = pickle.load(file(pdata2+prefix+'_estimationResults_pkl'))
mc1 = pickle.load(file(pmc1+prefix+'_estimationResults_pkl'))
#nominal = pickle.load(file(path1+prefix+'_estimationResults_pkl_kappa_corrected'))
#b_up = pickle.load(file(path2+prefix+'_estimationResults_pkl_kappa_corrected'))
#b_down = pickle.load(file(path3+prefix+'_estimationResults_pkl_kappa_corrected'))
#light_up = pickle.load(file(path4+prefix+'_estimationResults_pkl_kappa_corrected'))
#light_down = pickle.load(file(path5+prefix+'_estimationResults_pkl_kappa_corrected'))

pkls = [data1,data2,mc1]
#pkls = [res1,res2,res3,res4,res5]
#pkls = [nominal, b_up, b_down, light_up, light_down]

if useTTcorrection: kcs = pickle.load(file('/data/dspitzbart/Spring15/25ns/rCS_0b_3.0/correction_pkl'))
if useWcorrection:
  Wrcs_corr_PosPdg = pickle.load(file('/data/dspitzbart/Spring15/25ns/rCS_0b_3.0/correction_Wrcs_PosPdg_pkl'))
  Wrcs_corr_NegPdg = pickle.load(file('/data/dspitzbart/Spring15/25ns/rCS_0b_3.0/correction_Wrcs_NegPdg_pkl'))
  Wrcs_corr =        pickle.load(file('/data/dspitzbart/Spring15/25ns/rCS_0b_3.0/correction_Wrcs_pkl'))

#presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80"
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80"

btagString = 'nBJetMediumCSV30'

lumi = 3.
weight_str, weight_err_str = makeWeight(lumi, sampleLumi=3.)
lepSel = 'hard'

if signal:
  allSignals=[
            {'name':'T5q^{4} 1.2/1.0/0.8', 'sample':T5qqqqWW_mGo1200_mCh1000_mChi800[lepSel], 'weight':weight_str, 'color':ROOT.kBlack},
            {'name':'T5q^{4} 1.5/0.8/0.1', 'sample':T5qqqqWW_mGo1500_mCh800_mChi100[lepSel],  'weight':weight_str, 'color':ROOT.kMagenta},
            {'name':'T5q^{4} 1.0/0.8/0.7', 'sample':T5qqqqWW_mGo1000_mCh800_mChi700[lepSel],  'weight':weight_str, 'color':ROOT.kYellow},
  ]

  for s in allSignals:
    s['chain'] = getChain(s['sample'],histname='')


signalRegions = signalRegion3fbReduced
#signalRegions = signalRegionCRonly

rowsNJet = {}
rowsSt = {}
bins = 0
for srNJet in sorted(signalRegions):
  rowsNJet[srNJet] = {}
  rowsSt[srNJet] = {}
  rows = 0
  for stb in sorted(signalRegions[srNJet]):
    rows += len(signalRegions[srNJet][stb])
    rowsSt[srNJet][stb] = {'n':len(signalRegions[srNJet][stb])}
  rowsNJet[srNJet] = {'nST':len(signalRegions[srNJet]), 'n':rows}
  bins += rows

scaleFactor = 0.8
#scaleFactor = 1
SRkey = 'fit_srNJet_lowDPhi'
CRkey = 'fit_crNJet_lowDPhi'
keys = [['CR',CRkey],['SR',SRkey]]

for res in pkls:
  for keyName, fitkey in keys:
    for srNJet in sorted(signalRegions):
      for stb in sorted(signalRegions[srNJet]):
        for htb in sorted(signalRegions[srNJet][stb]):
          ttPred = res[srNJet][stb][htb][fitkey]['TT_AllPdg']['template'].GetBinContent(1)*res[srNJet][stb][htb][fitkey]['TT_AllPdg']['yield']
          ttPredVar = res[srNJet][stb][htb][fitkey]['TT_AllPdg']['template'].GetBinError(1)**2*res[srNJet][stb][htb][fitkey]['TT_AllPdg']['yield']**2 + \
                      res[srNJet][stb][htb][fitkey]['TT_AllPdg']['template'].GetBinContent(1)**2*res[srNJet][stb][htb][fitkey]['TT_AllPdg']['yieldVar']
          WPredPosPdg = res[srNJet][stb][htb][fitkey]['W_PosPdg']['template'].GetBinContent(1)*res[srNJet][stb][htb][fitkey]['W_PosPdg']['yield']
          WPredPosPdgVar = res[srNJet][stb][htb][fitkey]['W_PosPdg']['template'].GetBinError(1)**2*res[srNJet][stb][htb][fitkey]['W_PosPdg']['yield']**2 + \
                           res[srNJet][stb][htb][fitkey]['W_PosPdg']['template'].GetBinContent(1)**2*res[srNJet][stb][htb][fitkey]['W_PosPdg']['yieldVar']
          WPredNegPdg = res[srNJet][stb][htb][fitkey]['W_NegPdg']['template'].GetBinContent(1)*res[srNJet][stb][htb][fitkey]['W_NegPdg']['yield']
          WPredNegPdgVar = res[srNJet][stb][htb][fitkey]['W_NegPdg']['template'].GetBinError(1)**2*res[srNJet][stb][htb][fitkey]['W_NegPdg']['yield']**2 + \
                           res[srNJet][stb][htb][fitkey]['W_NegPdg']['template'].GetBinContent(1)**2*res[srNJet][stb][htb][fitkey]['W_NegPdg']['yieldVar']
          RestPredPosPdg = res[srNJet][stb][htb][fitkey]['Rest_PosPdg']['template'].GetBinContent(1)*res[srNJet][stb][htb][fitkey]['Rest_PosPdg']['yield']
          RestPredPosPdgVar = res[srNJet][stb][htb][fitkey]['Rest_PosPdg']['template'].GetBinError(1)**2*res[srNJet][stb][htb][fitkey]['Rest_PosPdg']['yield']**2 + \
                              res[srNJet][stb][htb][fitkey]['Rest_PosPdg']['template'].GetBinContent(1)**2*res[srNJet][stb][htb][fitkey]['Rest_PosPdg']['yieldVar']
          RestPredNegPdg = res[srNJet][stb][htb][fitkey]['Rest_NegPdg']['template'].GetBinContent(1)*res[srNJet][stb][htb][fitkey]['Rest_NegPdg']['yield']
          RestPredNegPdgVar = res[srNJet][stb][htb][fitkey]['Rest_NegPdg']['template'].GetBinError(1)**2*res[srNJet][stb][htb][fitkey]['Rest_NegPdg']['yield']**2 + \
                              res[srNJet][stb][htb][fitkey]['Rest_NegPdg']['template'].GetBinContent(1)**2*res[srNJet][stb][htb][fitkey]['Rest_NegPdg']['yieldVar']
    
          totalPredPosPdg = ttPred/2 + WPredPosPdg + RestPredPosPdg
          totalPredPosPdgVar = ttPredVar/4 + WPredPosPdgVar + RestPredPosPdgVar
    
          totalPredNegPdg = ttPred/2 + WPredNegPdg + RestPredNegPdg
          totalPredNegPdgVar = ttPredVar/4 + WPredNegPdgVar + RestPredNegPdgVar
    
          #fractions and errors
          ttPredPosFrac = ttPred/(2*totalPredPosPdg)
          ttPredPosFracVar = (ttPredVar/4)/totalPredPosPdg**2 + totalPredPosPdgVar*(ttPred/2)**2/totalPredPosPdg**4
    
          ttPredNegFrac = ttPred/(2*totalPredNegPdg)
          ttPredNegFracVar = (ttPredVar/4)/totalPredNegPdg**2 + totalPredNegPdgVar*(ttPred/2)**2/totalPredNegPdg**4
    
          WPredPosFrac = WPredPosPdg/totalPredPosPdg
          WPredPosFracVar = WPredPosPdgVar/totalPredPosPdg**2 + totalPredPosPdgVar*WPredPosPdg**2/totalPredPosPdg**4
    
          WPredNegFrac = WPredNegPdg/totalPredNegPdg
          WPredNegFracVar = WPredNegPdgVar/totalPredNegPdg**2 + totalPredNegPdgVar*WPredNegPdg**2/totalPredNegPdg**4
          RestPredPosFrac = RestPredPosPdg/totalPredPosPdg
          RestPredPosFracVar = RestPredPosPdgVar/totalPredPosPdg**2 + totalPredPosPdgVar*RestPredPosPdg**2/totalPredPosPdg**4
    
          RestPredNegFrac = RestPredNegPdg/totalPredNegPdg
          RestPredNegFracVar = RestPredNegPdgVar/totalPredNegPdg**2 + totalPredNegPdgVar*RestPredNegPdg**2/totalPredNegPdg**4
          
          frac_pos = {'tt':ttPredPosFrac, 'tt_var':ttPredPosFracVar, 'W':WPredPosFrac, 'W_var':WPredPosFracVar, 'Rest':RestPredPosFrac, 'Rest_var':RestPredPosFracVar}
          frac_neg = {'tt':ttPredPosFrac, 'tt_var':ttPredNegFracVar, 'W':WPredNegFrac, 'W_var':WPredNegFracVar, 'Rest':RestPredNegFrac, 'Rest_var':RestPredNegFracVar}
          res[srNJet][stb][htb].update({'bTagFit_fractions_'+keyName:{'pos':frac_pos, 'neg':frac_neg}})

path = '/afs/hephy.at/user/d/dspitzbart/www/Spring15/bTagFit_Fraction_Closure/'

if not os.path.exists(path):
  os.makedirs(path)

charges = ['pos','neg']
bkgs = ['W','tt','Rest']
keys = [['CR','bTagFit_fractions_CR'],['SR','bTagFit_fractions_SR']]


#varUp = []
#varDown = []
#signDown = 1
#signUp = 1
#
#Up_H  = ROOT.TH1F('Up_H','total Up',bins,0,bins)
#Down_H  = ROOT.TH1F('Down_H','total Down',bins,0,bins)
#b_Up_H  = ROOT.TH1F('b_Up_H','b Up',bins,0,bins)
#b_Down_H  = ROOT.TH1F('b_Down_H','b Down',bins,0,bins)
#light_Up_H  = ROOT.TH1F('light_Up_H','light Up',bins,0,bins)
#light_Down_H  = ROOT.TH1F('light_Down_H','light Down',bins,0,bins)
#
#max_H = ROOT.TH1F('max_H','total max',bins,0,bins)
#min_H = ROOT.TH1F('min_H','total min',bins,0,bins)
#zero_H = ROOT.TH1F('zero_H','zero',bins,0,bins)
#
#for keyName, fitkey in keys:
#  for charge in charges:
#    for bkg in bkgs:
#      i=1
#      b_varUp = []
#      b_varDown = []
#      b_signDown = 1
#      b_signUp = 1
#      light_varUp = []
#      light_varDown = []
#      light_signDown = 1
#      light_signUp = 1
#      varUp = []
#      varDown = []
#      signDown = 1
#      signUp = 1
#      for i_njb, srNJet in enumerate(sorted(signalRegions)):
#        for stb in sorted(signalRegions[srNJet]):
#          for htb in sorted(signalRegions[srNJet][stb]):
#            print
#            print '#############################################'
#            print 'bin: \t njet \t\t LT \t\t HT'
#            if len(str(srNJet))<7:
#              print '\t',srNJet,'\t\t',stb,'\t',htb
#            else:
#              print '\t',srNJet,'\t',stb,'\t',htb
#            print
#            light_upDiff   = (light_up[srNJet][stb][htb][fitkey][charge][bkg]-nominal[srNJet][stb][htb][fitkey][charge][bkg])/nominal[srNJet][stb][htb][fitkey][charge][bkg]
#            light_downDiff = (light_down[srNJet][stb][htb][fitkey][charge][bkg]-nominal[srNJet][stb][htb][fitkey][charge][bkg])/nominal[srNJet][stb][htb][fitkey][charge][bkg]
#            print 'light up, down:', light_upDiff, light_downDiff
#            b_upDiff   = (b_up[srNJet][stb][htb][fitkey][charge][bkg]-nominal[srNJet][stb][htb][fitkey][charge][bkg])/nominal[srNJet][stb][htb][fitkey][charge][bkg]
#            b_downDiff = (b_down[srNJet][stb][htb][fitkey][charge][bkg]-nominal[srNJet][stb][htb][fitkey][charge][bkg])/nominal[srNJet][stb][htb][fitkey][charge][bkg]
#            print 'b up, down:', b_upDiff, b_downDiff
#            if sign(b_upDiff) != sign(light_upDiff): print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11'
#            upDiff = sqrt(light_upDiff**2 + b_upDiff**2)
#            downDiff = sqrt(light_downDiff**2 + b_downDiff**2)
#            print 'total up, down:', upDiff, downDiff
#            Up_H.SetBinContent(i,sign(b_upDiff)*upDiff)
#            Up_H.GetXaxis().SetBinLabel(i,str(i))
#            Down_H.SetBinContent(i,sign(b_downDiff)*downDiff)
#            
#            b_Up_H.SetBinContent(i,b_upDiff)
#            b_Down_H.SetBinContent(i,b_downDiff)
#            light_Up_H.SetBinContent(i,light_upDiff)
#            light_Down_H.SetBinContent(i,light_downDiff)
#            
#            b_varUp.append(b_upDiff)
#            b_varDown.append(b_downDiff)
#            light_varUp.append(light_upDiff)
#            light_varDown.append(light_downDiff)
#            varUp.append(upDiff)
#            varDown.append(downDiff)
#            i += 1
#      can = ROOT.TCanvas('can','can',700,700)
#      
#      b_maxDown = max(map(abs,b_varDown))
#      if b_varDown[0]<0: b_signDown = -1
#      b_maxUp = max(map(abs,b_varUp))
#      if b_varUp[0]<0: b_signUp = -1
#      
#      light_maxDown = max(map(abs,light_varDown))
#      if light_varDown[0]<0: light_signDown = -1
#      light_maxUp = max(map(abs,light_varUp))
#      if light_varUp[0]<0: light_signUp = -1
#      
#      maxDown = max(map(abs,varDown))
#      maxUp = max(map(abs,varUp))
#      totalMax = max(map(abs,[maxDown,maxUp]))
#      print
#      print 'Max. change to nominal for b variation up:',b_maxUp*b_signUp
#      print 'Max. change to nominal for b variation down:',b_maxDown*b_signDown
#      print 'Max. change to nominal for light variation up:',light_maxUp*light_signUp
#      print 'Max. change to nominal for light variation down:',light_maxDown*light_signDown
#      print 'Max. change to nominal for total variation up:',maxUp*b_signUp
#      print 'Max. change to nominal for total variation down:',maxDown*b_signDown
#      
#      Up_H.GetXaxis().SetTitle('Signal Region #')
#      Up_H.GetXaxis().SetTitleSize(0.05)
#      Up_H.GetXaxis().SetTitleOffset(1.0)
#      Up_H.GetXaxis().SetLabelSize(0.08)
#      
#      Up_H.GetYaxis().SetTitle('#delta_{k}')
#      
#      Up_H.SetMinimum(-(2*totalMax))
#      Up_H.SetMaximum((2*totalMax))
#      Up_H.SetFillColor(ROOT.kGray)
#      Up_H.SetMarkerStyle(0)
#      Down_H.SetFillColor(ROOT.kGray)
#      Up_H.SetLineColor(ROOT.kBlack)
#      Up_H.SetLineWidth(2)
#      Down_H.SetLineColor(ROOT.kBlack)
#      Down_H.SetLineWidth(2)
#      b_Up_H.SetLineColor(ROOT.kOrange+8)
#      b_Up_H.SetMarkerStyle(0)
#      b_Up_H.SetLineWidth(2)
#      b_Down_H.SetLineColor(ROOT.kOrange+8)
#      b_Down_H.SetLineWidth(2)
#      light_Up_H.SetLineColor(ROOT.kBlue)
#      light_Up_H.SetMarkerStyle(0)
#      light_Up_H.SetLineWidth(2)
#      light_Down_H.SetLineColor(ROOT.kBlue)
#      light_Down_H.SetLineWidth(2)
#      
#      for i in range(1,bins+1):
#        max_H.SetBinContent(i,maxUp*b_signUp)
#        min_H.SetBinContent(i,maxDown*b_signDown)
#        zero_H.SetBinContent(i,0)
#      max_H.SetLineStyle(3)
#      min_H.SetLineStyle(3)
#      
#      Up_H.Draw()
#      Down_H.Draw('same')
#      b_Up_H.Draw('same')
#      b_Down_H.Draw('same')
#      light_Up_H.Draw('same')
#      light_Down_H.Draw('same')
#      max_H.Draw('same')
#      min_H.Draw('same')
#      zero_H.Draw('same')
#      can.RedrawAxis()
#      
#      leg = ROOT.TLegend(0.65,0.78,0.98,0.95)
#      leg.SetFillColor(ROOT.kWhite)
#      leg.SetShadowColor(ROOT.kWhite)
#      leg.SetBorderSize(1)
#      leg.SetTextSize(0.045)
#      leg.AddEntry(Up_H,'total')
#      leg.AddEntry(b_Up_H,'b/c var')
#      leg.AddEntry(light_Up_H,'light var')
#      leg.Draw()
#      can.Print(path+keyName+'_'+charge+'_'+bkg+'.png')
#      can.Print(path+keyName+'_'+charge+'_'+bkg+'.root')




#fitkey = 'fit_crNJet_lowDPhi'
#fitkey = 'fit_srNJet_lowDPhi'


for keyName, fitkey in keys:
  for charge in charges:
    for bkg in bkgs:
      print
      #print keyName, charge, bkg
      #print
      print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|}\\hline'
      print ' \\njet     & \ST & \HT     &\multicolumn{9}{c|}{'+bkg+' '+charge+' PDG}\\\%\hline'
      print ' & $[$GeV$]$ &$[$GeV$]$ & \multicolumn{3}{c}{data, 2015SF} & \multicolumn{3}{c}{data, 2012SF} & \multicolumn{3}{c|}{MC}  \\\\\hline'
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
            print ' & ' + getNumString(data1[srNJet][stb][htb][fitkey][charge][bkg], sqrt(data1[srNJet][stb][htb][fitkey][charge][bkg+'_var'])) \
                + ' & ' + getNumString(data2[srNJet][stb][htb][fitkey][charge][bkg],   sqrt(data2[srNJet][stb][htb][fitkey][charge][bkg+'_var'])) \
                + ' & ' + getNumString(mc1[srNJet][stb][htb][fitkey][charge][bkg], sqrt(mc1[srNJet][stb][htb][fitkey][charge][bkg+'_var'])) +'\\\\'

            if htb[1] == -1 : print '\\cline{2-12}'
      if keyName == 'CR': print '\\hline\end{tabular}}\end{center}\caption{Fractions of background obtained from a b-tag multiplicity fit for calculating W Rcs (3-4 jets) using MC (templates using b-tag weights) with varied SFs}\label{tab:fitFractions'+bkg+charge+keyName+'}\end{table}'
      if keyName == 'SR': print '\\hline\end{tabular}}\end{center}\caption{Fractions of background obtained from a b-tag multiplicity fit for obtaining the final background prediction using MC (templates using b-tag weights) with varied SFs}\label{tab:fitFractions'+bkg+charge+keyName+'}\end{table}'


#for keyName, fitkey in keys:
#  for charge in charges:
#    for bkg in bkgs:
#      print
#      #print keyName, charge, bkg
#      #print
#      print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|}\\hline'
#      print ' \\njet     & \ST & \HT     &\multicolumn{15}{c|}{'+bkg+' '+charge+' PDG}\\\%\hline'
#      print ' & $[$GeV$]$ &$[$GeV$]$ & \multicolumn{3}{c}{nominal} & \multicolumn{3}{c}{b/c Up} & \multicolumn{3}{c}{b/c Down} & \multicolumn{3}{c}{light Up}& \multicolumn{3}{c|}{light Down} \\\\\hline'
#      secondLine = False
#      for srNJet in sorted(signalRegions):
#        print '\\hline'
#        if secondLine: print '\\hline'
#        secondLine = True
#        print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
#        for stb in sorted(signalRegions[srNJet]):
#          print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
#          first = True
#          for htb in sorted(signalRegions[srNJet][stb]):
#            if not first: print '&'
#            first = False
#            print '&$'+varBin(htb)+'$'
#            print ' & ' + getNumString(nominal[srNJet][stb][htb][fitkey][charge][bkg], sqrt(nominal[srNJet][stb][htb][fitkey][charge][bkg+'_var'])) \
#                + ' & ' + getNumString(b_up[srNJet][stb][htb][fitkey][charge][bkg],    sqrt(b_up[srNJet][stb][htb][fitkey][charge][bkg+'_var'])) \
#                + ' & ' + getNumString(b_down[srNJet][stb][htb][fitkey][charge][bkg],  sqrt(b_down[srNJet][stb][htb][fitkey][charge][bkg+'_var'])) \
#                + ' & ' + getNumString(light_up[srNJet][stb][htb][fitkey][charge][bkg],   sqrt(light_up[srNJet][stb][htb][fitkey][charge][bkg+'_var'])) \
#                + ' & ' + getNumString(light_down[srNJet][stb][htb][fitkey][charge][bkg], sqrt(light_down[srNJet][stb][htb][fitkey][charge][bkg+'_var'])) +'\\\\'
#      
#            if htb[1] == -1 : print '\\cline{2-18}'
#      if keyName == 'CR': print '\\hline\end{tabular}}\end{center}\caption{Fractions of background obtained from a b-tag multiplicity fit for calculating W Rcs (3-4 jets) using MC (templates using b-tag weights) with varied SFs}\label{tab:fitFractions'+bkg+charge+keyName+'}\end{table}'
#      if keyName == 'SR': print '\\hline\end{tabular}}\end{center}\caption{Fractions of background obtained from a b-tag multiplicity fit for obtaining the final background prediction using MC (templates using b-tag weights) with varied SFs}\label{tab:fitFractions'+bkg+charge+keyName+'}\end{table}'

