import ROOT
import pickle
import os,sys,math
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()

from Workspace.HEPHYPythonTools.user import username
from rCShelpers import *
from math import pi, sqrt, isnan
from Workspace.RA4Analysis.signalRegions import *

from predictionConfig import *

colorList = [ROOT.kBlue+1, ROOT.kCyan-9, ROOT.kOrange-4, ROOT.kGreen+1, ROOT.kRed+1]

ROOT.TH1F().SetDefaultSumw2()

lumi = 1.26
predictionName = 'data_newSR_lep_SFtemplates'
pickleDir   = '/data/'+username+'/Results2015/Prediction_'+predictionName+'_'+str(lumi)+'/'

res = pickle.load(file(pickleDir+'singleLeptonic_Spring15__estimationResults_pkl'))

def divideRCSdict(a,b):
  if b['rCS']>0:
    kappa = a['rCS']/b['rCS']
  else:
    kappa = float('nan')
    kappaErrorPred = float('nan')
    kappaErrorSim = float('nan')
  if a['rCS']>0 and b['rCS']>0:
    kappaErrorPred = (a['rCS']/b['rCS'])*sqrt(a['rCSE_pred']**2/a['rCS']**2+b['rCSE_pred']**2/b['rCS']**2)
    kappaErrorSim = (a['rCS']/b['rCS'])*sqrt(a['rCSE_sim']**2/a['rCS']**2+b['rCSE_sim']**2/b['rCS']**2)
  elif b['rCS']>0:
    kappaErrorPred = float('nan')
    kappaErrorSim  = float('nan')
  return {'kappa':kappa, 'kappaE_pred':kappaErrorPred, 'kappaE_sim':kappaErrorSim}

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

rcs1bMC   = ROOT.TH1F('rcs1bMC','Rcs 1b MC',bins,0,bins)
rcs1bdata = ROOT.TH1F('rcs1bdata','Rcs 1b data',bins,0,bins)
rcs2bMC   = ROOT.TH1F('rcs2bMC','Rcs 2b MC',bins,0,bins)
rcs2bdata = ROOT.TH1F('rcs2bdata','Rcs 2b data',bins,0,bins)

rcs1bMC.SetLineColor(colorList[0])
rcs1bdata.SetLineColor(colorList[1])
rcs2bMC.SetLineColor(colorList[2])
rcs2bdata.SetLineColor(colorList[3])

rcs1bMC.SetMarkerStyle(0)
rcs1bdata.SetMarkerStyle(0)
rcs2bMC.SetMarkerStyle(0)
rcs2bdata.SetMarkerStyle(0)

rcs1bMC.SetLineWidth(2)
rcs1bdata.SetLineWidth(2)
rcs2bMC.SetLineWidth(2)
rcs2bdata.SetLineWidth(2)

rcs1bMC.SetMinimum(0.)
rcs1bMC.SetMaximum(0.25)


kappa01TT  = ROOT.TH1F('kappa01','tt(0b)/tt(1b)',bins,0,bins)
kappa12TT  = ROOT.TH1F('kappa12','tt(1b)/tt(2b)',bins,0,bins)
kappa0tt1EWK = ROOT.TH1F('kappa','tt(0b)/EWK(1b)',bins,0,bins)
kappa01EWK = ROOT.TH1F('kappa01ewk','EWK(0b)/EWK(1b)',bins,0,bins)
kappa12EWK = ROOT.TH1F('kappa12ewk','EWK(1b)/EWK(2b)',bins,0,bins)

kappa12data = ROOT.TH1F('kappa12data','data 1b/2b',bins,0,bins)

kappa01TT.SetLineColor(colorList[0])
kappa01TT.SetMinimum(0.)
kappa01TT.SetMaximum(2.)

kappa12TT.SetLineColor(colorList[1])
kappa0tt1EWK.SetLineColor(colorList[2])
kappa01EWK.SetLineColor(colorList[3])
kappa12EWK.SetLineColor(colorList[4])
kappa12data.SetLineColor(ROOT.kBlack)

kappa01TT.SetMarkerStyle(0)
kappa12TT.SetMarkerStyle(0)
kappa0tt1EWK.SetMarkerStyle(0)
kappa01EWK.SetMarkerStyle(0)
kappa12EWK.SetMarkerStyle(0)
kappa12data.SetMarkerStyle(0)

kappa01TT.SetLineWidth(2)
kappa12TT.SetLineWidth(2)
kappa0tt1EWK.SetLineWidth(2)
kappa01EWK.SetLineWidth(2)
kappa12EWK.SetLineWidth(2)
kappa12data.SetLineWidth(2)

i = 1
can = ROOT.TCanvas('c','c',700,700)

leg = ROOT.TLegend(0.6,0.7,0.98,0.95)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.035)

#presel = singleMu_presel

for i_njb, njb in enumerate(sorted(signalRegions)):
  for stb in sorted(signalRegions[njb]):
    for htb in sorted(signalRegions[njb][stb]):
      print
      print '#############################################'
      print 'bin: \t njet \t\t LT \t\t HT'
      if len(str(njb))<7:
        print '\t',njb,'\t\t',stb,'\t',htb
      else:
        print '\t',njb,'\t',stb,'\t',htb
      print '#############################################'
      print
      dPhiCut = signalRegions[njb][stb][htb]['deltaPhi']
      #ttJets corrections
      cname2bCRtt, cut2bCRtt = nameAndCut(stb,htb,(4,5), btb=(2,-1) ,presel=presel)
      cname1bCRtt, cut1bCRtt = nameAndCut(stb,htb,(4,5), btb=(1,1) ,presel=presel)
      cname0bCRtt, cut0bCRtt = nameAndCut(stb,htb,(4,5), btb=(0,0) ,presel=presel)
      cnameCRtt, cutCRtt = nameAndCut(stb,htb,(4,5), btb=(0,-1) ,presel=presel)
      #rcs1bCRtt = getRCS(cEWK, cut1bCRtt, dPhiCut)
      #rcs0bCRtt = getRCS(cTTJets, cut0bCRtt, dPhiCut)
      samples0b = [{'chain':cWJets, 'cut':cutCRtt, 'weight':'weight*weightBTag0'}, {'chain':cTTJets, 'cut':cutCRtt, 'weight':'weight*weightBTag0'},{'chain':cDY, 'cut':cut0bCRtt, 'weight':'weight'},{'chain':cTTV, 'cut':cut0bCRtt, 'weight':'weight'},{'chain':csingleTop, 'cut':cut0bCRtt, 'weight':'weight'}]
      samples1b = [{'chain':cWJets, 'cut':cutCRtt, 'weight':'weight*weightBTag1_SF'}, {'chain':cTTJets, 'cut':cutCRtt, 'weight':'weight*weightBTag1_SF'},{'chain':cDY, 'cut':cut1bCRtt, 'weight':'weight'},{'chain':cTTV, 'cut':cut1bCRtt, 'weight':'weight'},{'chain':csingleTop, 'cut':cut1bCRtt, 'weight':'weight'}]
      samples2b = [{'chain':cWJets, 'cut':cutCRtt, 'weight':'weight*weightBTag2p_SF'}, {'chain':cTTJets, 'cut':cutCRtt, 'weight':'weight*weightBTag2p_SF'},{'chain':cDY, 'cut':cut2bCRtt, 'weight':'weight'},{'chain':cTTV, 'cut':cut2bCRtt, 'weight':'weight'},{'chain':csingleTop, 'cut':cut2bCRtt, 'weight':'weight'}]
      #rcs0bCRtt_btag_EWK = combineRCS(samples0b, dPhiCut)
      rcs1bCRtt_btag_EWK = combineRCS(samples1b, dPhiCut)
      rcs2bCRtt_btag_EWK = combineRCS(samples2b, dPhiCut)
      
      QCD1b_lowDPhi  = {'y':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi'],  'e':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_lowdPhi_err']}
      QCD1b_highDPhi = {'y':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_highdPhi'], 'e':QCDestimate[(4,5)][stb][htb][(1,1)][dPhiCut]['NQCDpred_highdPhi_err']}

      QCD2b_lowDPhi  = {'y':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi'],  'e':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_lowdPhi_err']}
      QCD2b_highDPhi = {'y':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_highdPhi'], 'e':QCDestimate[(4,5)][stb][htb][(2,-1)][dPhiCut]['NQCDpred_highdPhi_err']}
      
      QCD = [QCD1b_lowDPhi,QCD1b_highDPhi,QCD2b_lowDPhi,QCD2b_highDPhi]
      
      for q in QCD:
        if isnan(q['e']):
          print 'found nan error value', q['e'], 'going to set error to 100%'
          q['e'] = q['y']
      
      rcs1bCR_data = getRCS(cData, cut1bCRtt, dPhiCut, QCD_lowDPhi=QCD1b_lowDPhi, QCD_highDPhi=QCD1b_highDPhi)
      rcs2bCR_data = getRCS(cData, cut2bCRtt, dPhiCut, QCD_lowDPhi=QCD2b_lowDPhi, QCD_highDPhi=QCD2b_highDPhi)
      print rcs1bCR_data
      print rcs2bCR_data

      #rcs0bCRtt_btag = getRCS(cTTJets, cutCRtt, dPhiCut, weight = 'weight*weightBTag0')
      #rcs1bCRtt_btag = getRCS(cTTJets, cutCRtt, dPhiCut, weight = 'weight*weightBTag1')
      #rcs2bCRtt_btag = getRCS(cTTJets, cutCRtt, dPhiCut, weight = 'weight*weightBTag2')
      ##Kappa now calculated only in the SB bin (4,5) jets 1b allEWK MC vs 0b tt MC - no fit applied for the moment!
      #kappaTT01 = divideRCSdict(rcs0bCRtt_btag,rcs1bCRtt_btag)
      #kappaTT12 = divideRCSdict(rcs1bCRtt_btag,rcs2bCRtt_btag)

      #kappaTT01 = divideRCSdict(rcs0bCRtt_btag,rcs1bCRtt_btag)
      #kappaTT12 = divideRCSdict(rcs1bCRtt_btag,rcs2bCRtt_btag)

      #kappaEWK01 = divideRCSdict(rcs0bCRtt_btag_EWK,rcs1bCRtt_btag_EWK)
      #kappaEWK12 = divideRCSdict(rcs1bCRtt_btag_EWK,rcs2bCRtt_btag_EWK)

      #kappa0tt1ewk = divideRCSdict(rcs0bCRtt_btag,rcs1bCRtt_btag_EWK)

      #kappa_data = divideRCSdict(rcs1bCR_data,rcs2bCR_data)
      #kappa12data.SetBinContent(i,kappa_data['kappa'])
      #kappa12data.SetBinError(i,kappa_data['kappaE_pred'])

      #kappa01TT.SetBinContent(i,kappaTT01['kappa'])
      #kappa01TT.SetBinError(i,kappaTT01['kappaE_sim'])
      #kappa12TT.SetBinContent(i,kappaTT12['kappa'])
      #kappa12TT.SetBinError(i,kappaTT12['kappaE_sim'])

      #kappa0tt1EWK.SetBinContent(i,kappa0tt1ewk['kappa'])
      #kappa0tt1EWK.SetBinError(i,kappa0tt1ewk['kappaE_sim'])
      
      #kappa01EWK.SetBinContent(i,kappaEWK01['kappa'])
      #kappa01EWK.SetBinError(i,kappaEWK01['kappaE_sim'])
      #kappa12EWK.SetBinContent(i,kappaEWK12['kappa'])
      #kappa12EWK.SetBinError(i,kappaEWK12['kappaE_sim'])

      rcs1bMC.SetBinContent(i,rcs1bCRtt_btag_EWK['rCS'])
      rcs1bMC.SetBinError(i,rcs1bCRtt_btag_EWK['rCSE_sim'])
      rcs1bdata.SetBinContent(i,rcs1bCR_data['rCS'])
      rcs1bdata.SetBinError(i,rcs1bCR_data['rCSE_pred'])
      rcs2bMC.SetBinContent(i,rcs2bCRtt_btag_EWK['rCS'])
      rcs2bMC.SetBinError(i,rcs2bCRtt_btag_EWK['rCSE_sim'])
      rcs2bdata.SetBinContent(i,rcs2bCR_data['rCS'])
      rcs2bdata.SetBinError(i,rcs2bCR_data['rCSE_pred'])
      #print 'Total Electroweak'
      #print '0b/1b:', round(kappaEWK01['kappa'],2),'+/-',round(kappaEWK01['kappaE_sim'],2)
      #print '1b/2b:', round(kappaEWK12['kappa'],2),'+/-',round(kappaEWK12['kappaE_sim'],2)
      #print 'Data'
      #print '1b/2b:', round(kappa_data['kappa'],2),'+/-',round(kappa_data['kappaE_sim'],2)
      #print 'Kappa factor used'
      #print '0b/1b:', round(kappa0tt1ewk['kappa'],2),'+/-',round(kappa0tt1ewk['kappaE_sim'],2)
      i += 1

rcs1bMC.Draw('hist e1')
rcs1bdata.Draw('hist e1 same')
rcs2bMC.Draw('hist e1 same')
rcs2bdata.Draw('hist e1 same')


#kappa01TT.Draw('hist e1')
#kappa12TT.Draw('hist e1 same')
#kappa0tt1EWK.Draw('hist e1 same')
##kappa01EWK.Draw('hist e1 same')
#kappa12EWK.Draw('hist e1 same')
#kappa12data.Draw('hist e1 same')
#
#leg.AddEntry(kappa01TT)
#leg.AddEntry(kappa12TT)
#leg.AddEntry(kappa0tt1EWK)
#leg.AddEntry(kappa12EWK)
##leg.AddEntry(kappa01EWK)
#leg.AddEntry(kappa12data)
leg.AddEntry(rcs1bMC)
leg.AddEntry(rcs1bdata)
leg.AddEntry(rcs2bMC)
leg.AddEntry(rcs2bdata)


leg.Draw()

