import ROOT
import os, sys
from ROOT import RooFit as rf

from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from Workspace.HEPHYPythonTools.user import username
from math import pi, sqrt

#def LpTemplateFit(LpTemplates, prefix="", printDir='/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCMG2/templateFit_Phys14V3/QCDestimation'):
def LpTemplateFit(LpTemplates, prefix="", printDir='/afs/hephy.at/user/'+username[0]+'/'+username+'/www/RunII/Spring15_25ns/QCDestimation/templateFit', storePlot = True):
  if not os.path.exists(printDir):
     os.makedirs(printDir) 
#  cWJets = samples['W']
#  cTTJets = samples['TT']
#  cQCD = samples['QCD']
  histoEWKantiSel = LpTemplates['EWKantiSel']
  histoEWKsel = LpTemplates['EWKsel']
  histoQCDantiSel = LpTemplates['QCDantiSel']
  histoQCDsel = LpTemplates['QCDsel']
  histoDATAantiSel = LpTemplates['DATAantiSel']
  histoDATAsel = LpTemplates['DATAsel']

#Clone histograms from LpTemplates: EWK selected and QCD anti-selected
  template_EWK   = histoEWKsel.Clone()
  template_QCD   = histoDATAantiSel.Clone()

  print "Nominal yields EWK:",template_EWK.Integral()#,'WJets_PosPdg',template_WJets_PosPdg.Integral(),'WJets_NegPdg',template_WJets_NegPdg.Integral()
  print "Nominal yields QCD:",template_QCD.Integral()

  hData = histoDATAsel.Clone()

  if template_EWK.Integral()>0:
    template_EWK.Scale(1./template_EWK.Integral())
  if template_QCD.Integral()>0:
    template_QCD.Scale(1./template_QCD.Integral())

  #Observable
  x=ROOT.RooRealVar('Lp','L_{P}',-0.5,0.5)

  #import the contents of 'data' ROOT histogram into a RooDataHist object 
  data=ROOT.RooDataHist("data","data",ROOT.RooArgList(x),hData)

  dh_EWK=ROOT.RooDataHist("mcEWK","mcEWK",ROOT.RooArgList(x),template_EWK)
  dh_QCD=ROOT.RooDataHist("QCD anti-selected","QCD anti-selected",ROOT.RooArgList(x),template_QCD)

  yield_EWK=ROOT.RooRealVar("EWK_yield","yieldEWK",0.1,0,10**9)
  yield_QCD=ROOT.RooRealVar("QCD_yield","yieldQCD",0.1,0,10**9)

  #MakePDFfromMChistograms
  model_EWK=ROOT.RooHistPdf("model_EWK","model_EWK",ROOT.RooArgSet(x),dh_EWK)
  model_QCD=ROOT.RooHistPdf("model_QCD","model_QCD",ROOT.RooArgSet(x),dh_QCD)
#  model=ROOT.RooAddPdf("model","model",ROOT.RooArgList(model_EWK),ROOT.RooArgList(yield_EWK))
  model=ROOT.RooAddPdf("model","model",ROOT.RooArgList(model_EWK, model_QCD),ROOT.RooArgList(yield_EWK, yield_QCD))
  #CombinesmyMCsintoonePDFmodel

  #Plottheimportedhistogram(s)
  dframe=x.frame(rf.Title("Data"))
  data.plotOn(dframe)

  frame_EWK=x.frame(rf.Title("EWK"))
  model_EWK.plotOn(frame_EWK)
  frame_QCD=x.frame(rf.Title("QCD"))
  model_QCD.plotOn(frame_QCD)

  nllComponents = ROOT.RooArgList("nllComponents")
  nll=model.createNLL(data,rf.NumCPU(1))
  nllComponents.add(nll)

  sumNLL = ROOT.RooAddition("sumNLL","sumNLL", nllComponents)

  ROOT.RooMinuit(sumNLL).migrad()
  ROOT.RooMinuit(sumNLL).hesse()
  ROOT.RooMinuit(sumNLL).minos()#optional

  fitFrame=x.frame(rf.Bins(50),rf.Title("Fit Model"))
  model.paramOn(fitFrame,rf.Layout(0.68,0.98,0.95))
  data.plotOn(fitFrame,rf.LineColor(ROOT.kBlack))
  model.plotOn(fitFrame,rf.LineColor(ROOT.kRed))
  model.plotOn(fitFrame,rf.Components("model_QCD"),rf.LineColor(ROOT.kGreen),rf.LineStyle(ROOT.kDashed))
  model.plotOn(fitFrame,rf.Components("model_EWK"),rf.LineColor(ROOT.kBlue),rf.LineStyle(ROOT.kDashed))

 
  if storePlot: 
    c1=ROOT.TCanvas("c1","FitModel",600,600)
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
    ROOT.gPad.SetLeftMargin(0.15)
    fitFrame.GetYaxis().SetTitleOffset(1.4)
    fitFrame.GetXaxis().SetTitle('L_{P}')
    fitFrame.Draw()
  
  
    c1.Print(printDir+'/'+prefix+'_TemplateFit.png')
    c1.Print(printDir+'/'+prefix+'_TemplateFit.pdf')
    c1.Print(printDir+'/'+prefix+'_TemplateFit.root')
    del c1
  del nllComponents

#  #alternative approach
#  
#  dataYield = hData.Integral()
#  histoEWKsel.Scale((yield_EWK.getVal()+yield_EWK.getErrorHi())/histoEWKsel.Integral(1,10))
#  EWKhigh = histoEWKsel.Integral()
#  
#  histoEWKsel.Scale((yield_EWK.getVal()+yield_EWK.getErrorLo())/histoEWKsel.Integral(1,10))
#  EWKlow = histoEWKsel.Integral()
#  
#  histoEWKsel.Scale(yield_EWK.getVal()/histoEWKsel.Integral(1,10))
#  EWKyield  = histoEWKsel.Integral()
#  QCDYield  = dataYield - EWKyield
#  QCDhigh   = dataYield - EWKlow
#  QCDlow    = dataYield - EWKhigh
#  
#  print 'Data yield', dataYield
#  print 'EWK yield', EWKyield
#  print 'QCD yield', QCDYield
#  
#  histoQCDsel.Scale(QCDYield/histoQCDsel.Integral())
#  
#  c2 = ROOT.TCanvas("c2","FitModel",600,600)
#  ROOT.gROOT.SetStyle("Plain")
#  ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
#  ROOT.gPad.SetLeftMargin(0.15)
#  histoEWKsel.SetLineColor(ROOT.kBlue)
#  histoEWKsel.Draw('hist')
#  totalH = histoEWKsel.Clone()
#  totalH.Add(histoQCDsel)
#  totalH.SetLineColor(ROOT.kRed)
#  histoQCDsel.SetLineColor(ROOT.kCyan)
#  histoQCDsel.Draw('hist same')
#  totalH.Draw('hist same')
#  histoDATAsel.Draw('e1p same')
#  c2.Print(printDir+'/'+prefix+'_TemplateFit_2.png')
#  c2.Print(printDir+'/'+prefix+'_TemplateFit_2.pdf')
#  c2.Print(printDir+'/'+prefix+'_TemplateFit_2.root')
#  del c2
  


  res = {'EWK':{'template':template_EWK, 'yield':yield_EWK.getVal(), 'yield_high':yield_EWK.getVal()+yield_EWK.getErrorHi(), 'yield_low':yield_EWK.getVal()+yield_EWK.getErrorLo(), 
                      'yieldVar':(yield_EWK.getErrorHi()-yield_EWK.getErrorLo())**2},
         'QCD':{'template':template_QCD,'yield':yield_QCD.getVal(), 'yield_high':yield_QCD.getVal()+yield_QCD.getErrorHi(), 'yield_low':yield_QCD.getVal()+yield_QCD.getErrorLo(),
                     'yieldVar':(yield_QCD.getErrorHi()-yield_QCD.getErrorLo())**2},
        }
  
#  res = {'EWK':{'template':template_EWK, 'yield':yield_EWK.getVal(), 'yield_high':yield_EWK.getVal()+yield_EWK.getErrorHi(), 'yield_low':yield_EWK.getVal()+yield_EWK.getErrorLo(), 
#                      'yieldVar':(yield_EWK.getErrorHi()-yield_EWK.getErrorLo())**2},
#         'QCD':{'template':template_QCD,'yield':QCDYield, 'yield_high':QCDhigh, 'yield_low':QCDlow,
#                     'yieldVar':(QCDhigh-QCDlow)**2},
#        }
  del model, data, sumNLL
  return res



