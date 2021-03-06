import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName

from makeTTPrediction import makeTTPrediction
from makeWPrediction import makeWPrediction
from Workspace.HEPHYPythonTools.user import username
from binnedNBTagsFit import binnedNBTagsFit
from rCShelpers import *
from math import pi, sqrt
from Workspace.RA4Analysis.signalRegions import *

from predictionConfig import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--nSR", dest="nSR", default=0, action="store", help="enter the number of SR you want to enter 0-27")
parser.add_option("--small", dest="test", action="store_true", help="enter the number of SR you want to enter 0-27")


(options, args) = parser.parse_args()


ROOT.TH1F().SetDefaultSumw2()

weight_str, weight_err_str = makeWeight(lumi, sampleLumi=sampleLumi, reWeight=MCweight)

samples={'W':cWJets, 'TT':cTTJets, 'Rest':cRest, 'Bkg':cBkg, 'Data': cData}

isData = False
#test = False

nSR = int(options.nSR)
prefix = prefix+"_"+str(nSR)
signalRegions = signalRegions_Moriond2017_onebyone[nSR]



#b = 1
test = False

n_bootstrap = 500
if test: n_bootstrap = 10
WSB = False

templateBootstrap = {}# {'TTJets':{},'TTJets_mu':{}, 'WJets_PosPdg':{}, 'WJets_NegPdg':{}, 'Rest_PosPdg':{}, 'Rest_NegPdg':{}}

for i_njb, njb in enumerate(sorted(signalRegions)):
  templateBootstrap[njb] = {}

  for stb in sorted(signalRegions[njb]):
    templateBootstrap[njb][stb] = {}

    for htb in sorted(signalRegions[njb][stb]):
      templateBootstrap[njb][stb][htb] = {}

      print
      print '#############################################'
      print '## * njet:',njb
      print '## * LT:  ',stb
      print '## * HT:  ',htb
      print '#############################################'
      print
      dPhiCut = signalRegions[njb][stb][htb]['deltaPhi']
      srNJet = njb
      if WSB:
        srNJet = (3,4)
        presel += '&&abs(leptonPdg)==13'
      
      name, cut       = nameAndCut(stb, htb, srNJet, btb=None, presel=presel, btagVar = nBTagVar)
      WSBname, WSBcut = nameAndCut(stb, htb, (3,4), btb=None, presel=presel+'&&abs(leptonPdg)==13', btagVar = nBTagVar)

      fit     = binnedNBTagsFit(cut+"&&"+dPhiStr+"<"+str(dPhiCut), cut+"&&"+dPhiStr+"<"+str(dPhiCut), name+'_dPhi'+str(dPhiCut), samples = samples, prefix=name, nSR=nSR)
      fitWSB  = binnedNBTagsFit(WSBcut+"&&"+dPhiStr+"<"+str(dPhiCut), WSBcut+"&&"+dPhiStr+"<"+str(dPhiCut), WSBname+'_dPhi'+str(dPhiCut), samples = samples, prefix=WSBname, nSR=nSR)
      
      w_pos_max = fit['W_PosPdg']['yield_high']*fit['W_PosPdg']['template'].GetBinContent(1)*1.2
      w_pos_min = fit['W_PosPdg']['yield_low']*fit['W_PosPdg']['template'].GetBinContent(1)*0.8
      w_pos = ROOT.TH1F('w_pos','w_pos',100,w_pos_min,w_pos_max)
      
      w_neg_max = fit['W_NegPdg']['yield_high']*fit['W_NegPdg']['template'].GetBinContent(1)*1.2
      w_neg_min = fit['W_NegPdg']['yield_low']* fit['W_NegPdg']['template'].GetBinContent(1)*0.8
      w_neg = ROOT.TH1F('w_neg','w_neg',100,w_neg_min,w_neg_max)
      
      tt_max = fit['TT_AllPdg']['yield_high']*fit['TT_AllPdg']['template'].GetBinContent(1)*1.2
      tt_min = fit['TT_AllPdg']['yield_low']* fit['TT_AllPdg']['template'].GetBinContent(1)*0.8
      tt = ROOT.TH1F('tt','tt',100,tt_min,tt_max)
      
      tt_WSB_max = fitWSB['TT_AllPdg']['yield_high']*fitWSB['TT_AllPdg']['template'].GetBinContent(1)*1.2
      tt_WSB_min = fitWSB['TT_AllPdg']['yield_low']* fitWSB['TT_AllPdg']['template'].GetBinContent(1)*0.8
      tt_WSB = ROOT.TH1F('tt','tt',100,tt_WSB_min,tt_WSB_max)
      
      rest_pos_max = fit['Rest_PosPdg']['yield_high']*fit['Rest_PosPdg']['template'].GetBinContent(1)*1.2
      rest_pos_min = fit['Rest_PosPdg']['yield_low']* fit['Rest_PosPdg']['template'].GetBinContent(1)*0.8
      rest_pos = ROOT.TH1F('rest_pos','rest_pos',100,rest_pos_min,rest_pos_max)
      
      rest_neg_max = fit['Rest_NegPdg']['yield_high']*fit['Rest_NegPdg']['template'].GetBinContent(1)*1.2
      rest_neg_min = fit['Rest_NegPdg']['yield_low']* fit['Rest_NegPdg']['template'].GetBinContent(1)*0.8
      rest_neg = ROOT.TH1F('rest_neg','rest_neg',100,rest_neg_min,rest_neg_max)


      for i in range(n_bootstrap):
        'Bootstrapping now...', i
        fit     = binnedNBTagsFit(cut+"&&"+dPhiStr+"<"+str(dPhiCut), cut+"&&"+dPhiStr+"<"+str(dPhiCut), name+'_dPhi'+str(dPhiCut), samples = samples, prefix=name, bootstrap=True, nSR=nSR)
        fitWSB  = binnedNBTagsFit(WSBcut+"&&"+dPhiStr+"<"+str(dPhiCut), WSBcut+"&&"+dPhiStr+"<"+str(dPhiCut), WSBname+'_dPhi'+str(dPhiCut), samples = samples, prefix=WSBname, bootstrap=True, nSR=nSR)
        w_pos.Fill(fit['W_PosPdg']['template'].GetBinContent(1)*fit['W_PosPdg']['yield'])
        w_neg.Fill(fit['W_NegPdg']['template'].GetBinContent(1)*fit['W_NegPdg']['yield'])
        tt.Fill(fit['TT_AllPdg']['template'].GetBinContent(1)*fit['TT_AllPdg']['yield'])
        tt_WSB.Fill(fitWSB['TT_AllPdg']['template'].GetBinContent(1)*fitWSB['TT_AllPdg']['yield'])
        rest_pos.Fill(fit['Rest_PosPdg']['template'].GetBinContent(1)*fit['Rest_PosPdg']['yield'])
        rest_neg.Fill(fit['Rest_NegPdg']['template'].GetBinContent(1)*fit['Rest_NegPdg']['yield'])
      
      if tt.GetMean()>0:
        templateBootstrap[njb][stb][htb]['TTJets'] = tt.GetRMS()/tt.GetMean()
      if tt_WSB.GetMean()>0:
        templateBootstrap[njb][stb][htb]['TTJets_mu'] = tt_WSB.GetRMS()/tt_WSB.GetMean()
      if w_pos.GetMean()>0:
        templateBootstrap[njb][stb][htb]['WJets_PosPdg'] = w_pos.GetRMS()/w_pos.GetMean()
      if w_neg.GetMean()>0:
        templateBootstrap[njb][stb][htb]['WJets_NegPdg'] = w_neg.GetRMS()/w_neg.GetMean()
      if rest_pos.GetMean()>0:
        templateBootstrap[njb][stb][htb]['Rest_PosPdg'] = rest_pos.GetRMS()/rest_pos.GetMean()
      if rest_neg.GetMean()>0:
        templateBootstrap[njb][stb][htb]['Rest_NegPdg'] = rest_neg.GetRMS()/rest_neg.GetMean()
      
      #b += 1


pickle.dump(templateBootstrap, file('/afs/hephy.at/data/dspitzbart01/RA4/Moriond2017/bootstrap/bootstrap_unc_SR'+str(nSR)+'.pkl','w'))
