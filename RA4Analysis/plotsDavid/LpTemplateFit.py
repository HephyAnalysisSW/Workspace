import ROOT
import os, sys
from ROOT import RooFit as rf

from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName,nBTagBinName,varBinName
from Workspace.HEPHYPythonTools.user import username
from math import pi, sqrt

#def LpTemplateFit(LpTemplates, prefix="", printDir='/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCMG2/templateFit_Phys14V3/QCDestimation'):
def LpTemplateFit(LpTemplates, prefix="", printDir='/afs/hephy.at/user/'+username[0]+'/'+username+'/www/RunII/Spring15_25ns/QCDestimation/templateFit'):
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
  template_QCD   = histoQCDantiSel.Clone()
  template_QCD.Add(histoEWKantiSel)

#  template_WJets_PosPdg=getPlotFromChain(cWJets, nBTagVar, [0,1,2,3], 'leptonPdg>0&&'+cut, 'weight', binningIsExplicit=True,addOverFlowBin='upper')
#  template_WJets_NegPdg=getPlotFromChain(cWJets, nBTagVar, [0,1,2,3], 'leptonPdg<0&&'+cut, 'weight', binningIsExplicit=True,addOverFlowBin='upper')
#  template_TTJets=      getPlotFromChain(cTTJets,nBTagVar, [0,1,2,3], cut,                 'weight', binningIsExplicit=True,addOverFlowBin='upper')
#  template_Rest_PosPdg= getPlotFromChain(cRest,  nBTagVar, [0,1,2,3], 'leptonPdg>0&&'+cut, 'weight', binningIsExplicit=True,addOverFlowBin='upper')
#  template_Rest_NegPdg= getPlotFromChain(cRest,  nBTagVar, [0,1,2,3], 'leptonPdg<0&&'+cut, 'weight', binningIsExplicit=True,addOverFlowBin='upper')

  print "Nominal yields EWK:",template_EWK.Integral()#,'WJets_PosPdg',template_WJets_PosPdg.Integral(),'WJets_NegPdg',template_WJets_NegPdg.Integral()
  print "Nominal yields QCD:",template_QCD.Integral()
#  print "Nominal yields:",'Rest_PosPdg',template_Rest_PosPdg.Integral(),'Rest_NegPdg',template_Rest_NegPdg.Integral()

  #hData_PosPdg=getPlotFromChain(cData,nBTagVar,[0,1,2,3],mTCut+'&&'+nameAndCut(metb,htb,njetb,'pos',btagRequirement='None')[1],'weight',binningIsExplicit=True,addOverFlowBin='upper')
  #hData_NegPdg=getPlotFromChain(cData,nBTagVar,[0,1,2,3],mTCut+'&&'+nameAndCut(metb,htb,njetb,'neg',btagRequirement='None')[1],'weight',binningIsExplicit=True,addOverFlowBin='upper')
#  hData_PosPdg = template_TTJets.Clone()
#  hData_PosPdg.Scale(0.5)
#  hData_PosPdg.Add(template_WJets_PosPdg)
#  hData_PosPdg.Add(template_Rest_PosPdg)
#  hData_NegPdg = template_TTJets.Clone()
#  hData_NegPdg.Scale(0.5)
#  hData_NegPdg.Add(template_WJets_NegPdg)
#  hData_NegPdg.Add(template_Rest_NegPdg)
  hData = histoDATAsel.Clone()

  if template_EWK.Integral()>0:
    template_EWK.Scale(1./template_EWK.Integral())
  if template_QCD.Integral()>0:
    template_QCD.Scale(1./template_QCD.Integral())
#  template_WJets_PosPdg.Scale(1./template_WJets_PosPdg.Integral())
#  template_WJets_NegPdg.Scale(1./template_WJets_NegPdg.Integral())
#  y_Rest_PosPdg = template_Rest_PosPdg.Integral()
#  y_Rest_NegPdg = template_Rest_NegPdg.Integral()
#  template_Rest_PosPdg.Scale(1./template_Rest_PosPdg.Integral())
#  template_Rest_NegPdg.Scale(1./template_Rest_NegPdg.Integral())

  #Observable
  x=ROOT.RooRealVar('Lp','L_{P}',-0.5,2.5)

  #import the contents of 'data' ROOT histogram into a RooDataHist object 
  data=ROOT.RooDataHist("data","data",ROOT.RooArgList(x),hData)
#  data_NegPdg=ROOT.RooDataHist("data","data",ROOT.RooArgList(x),hData_NegPdg)

#  dh_WJets_PosPdg=ROOT.RooDataHist("mcWJets","mcWJets",ROOT.RooArgList(x),template_WJets_PosPdg)
#  dh_WJets_NegPdg=ROOT.RooDataHist("mcWJets","mcWJets",ROOT.RooArgList(x),template_WJets_NegPdg)
  dh_EWK=ROOT.RooDataHist("mcEWK","mcEWK",ROOT.RooArgList(x),template_EWK)
  dh_QCD=ROOT.RooDataHist("QCD anti-selected","QCD anti-selected",ROOT.RooArgList(x),template_QCD)
#  dh_Rest_PosPdg=ROOT.RooDataHist("mcRest","mcRest",ROOT.RooArgList(x),template_Rest_PosPdg)
#  dh_Rest_NegPdg=ROOT.RooDataHist("mcRest","mcRest",ROOT.RooArgList(x),template_Rest_NegPdg)

  yield_EWK=ROOT.RooRealVar("EWK_yield","yieldEWK",0.1,0,10**9)
  yield_QCD=ROOT.RooRealVar("QCD_yield","yieldQCD",0.1,0,10**9)
#  yield_WJets_PosPdg = ROOT.RooRealVar("yield_WJets_PosPdg","yield_WJets_PosPdg",0.1,0,10**5)
#  yield_WJets_NegPdg = ROOT.RooRealVar("yield_WJets_NegPdg","yield_WJets_NegPdg",0.1,0,10**5)
#  yield_Rest_PosPdg = ROOT.RooRealVar("yield_Rest_PosPdg","yield_Rest_PosPdg",0.1,0,10**5)
#  yield_Rest_NegPdg = ROOT.RooRealVar("yield_Rest_NegPdg","yield_Rest_NegPdg",0.1,0,10**5)
#  yield_Rest_PosPdg = ROOT.RooRealVar("yield_Rest_PosPdg","yield_Rest_PosPdg",y_Rest_PosPdg,y_Rest_PosPdg,y_Rest_PosPdg)
#  yield_Rest_NegPdg = ROOT.RooRealVar("yield_Rest_NegPdg","yield_Rest_NegPdg",y_Rest_NegPdg,y_Rest_NegPdg,y_Rest_NegPdg)
#  yield_Rest_PosPdg.setConstant()
#  yield_Rest_NegPdg.setConstant()

  #MakePDFfromMChistograms
#  model_WJets_PosPdg=ROOT.RooHistPdf("model_WJets_PosPdg","model_WJets_PosPdg",ROOT.RooArgSet(x),dh_WJets_PosPdg)
#  model_WJets_NegPdg=ROOT.RooHistPdf("model_WJets_NegPdg","model_WJets_NegPdg",ROOT.RooArgSet(x),dh_WJets_NegPdg)
  model_EWK=ROOT.RooHistPdf("model_EWK","model_EWK",ROOT.RooArgSet(x),dh_EWK)
  model_QCD=ROOT.RooHistPdf("model_QCD","model_QCD",ROOT.RooArgSet(x),dh_QCD)
#  model_Rest_PosPdg=ROOT.RooHistPdf("model_Rest_PosPdg","model_Rest_PosPdg",ROOT.RooArgSet(x),dh_Rest_PosPdg)
#  model_Rest_NegPdg=ROOT.RooHistPdf("model_Rest_NegPdg","model_Rest_NegPdg",ROOT.RooArgSet(x),dh_Rest_NegPdg)

#  model_PosPdg=ROOT.RooAddPdf("model_PosPdg","model_PosPdg",ROOT.RooArgList(model_WJets_PosPdg, model_TTJets),ROOT.RooArgList(yield_WJets_PosPdg, yield_TTJets))
#  model_NegPdg=ROOT.RooAddPdf("model_NegPdg","model_NegPdg",ROOT.RooArgList(model_WJets_NegPdg, model_TTJets),ROOT.RooArgList(yield_WJets_NegPdg, yield_TTJets))
  model=ROOT.RooAddPdf("model","model",ROOT.RooArgList(model_EWK, model_QCD),ROOT.RooArgList(yield_EWK, yield_QCD))
#  model_NegPdg=ROOT.RooAddPdf("model_NegPdg","model_NegPdg",ROOT.RooArgList(model_WJets_NegPdg, model_TTJets, model_Rest_NegPdg),ROOT.RooArgList(yield_WJets_NegPdg, yield_TTJets, yield_Rest_NegPdg))
  #CombinesmyMCsintoonePDFmodel

  #Plottheimportedhistogram(s)
  dframe=x.frame(rf.Title("Data"))
  data.plotOn(dframe)
#  data_NegPdg.plotOn(dframe)

#  frame_WJets_PosPdg=x.frame(rf.Title("WJets PosPdg"))
#  model_WJets_PosPdg.plotOn(frame_WJets_PosPdg)
#  frame_WJets_NegPdg=x.frame(rf.Title("WJets NegPdg"))
#  model_WJets_NegPdg.plotOn(frame_WJets_NegPdg)

  frame_EWK=x.frame(rf.Title("EWK"))
  model_EWK.plotOn(frame_EWK)
  frame_QCD=x.frame(rf.Title("QCD"))
  model_QCD.plotOn(frame_QCD)

#  frame_Rest_PosPdg=x.frame(rf.Title("Rest PosPdg"))
#  model_Rest_PosPdg.plotOn(frame_Rest_PosPdg)
#  frame_Rest_NegPdg=x.frame(rf.Title("Rest NegPdg"))
#  model_Rest_NegPdg.plotOn(frame_Rest_NegPdg)

#  c=ROOT.TCanvas("roofit_example","RooFitFractionFitExample",800,1200)
#  c.Divide(1,3)
#  ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
#  c.cd(1)
#  ROOT.gPad.SetLeftMargin(0.15)
#  dframe.GetYaxis().SetTitleOffset(1.4)
#  dframe.Draw()
#  c.cd(2)
#  ROOT.gPad.SetLeftMargin(0.15)
#  frame_WJets_PosPdg.GetYaxis().SetTitleOffset(1.4)
#  frame_WJets_PosPdg.Draw()
#  frame_WJets_NegPdg.Draw('same')
#  c.cd(3)
#  ROOT.gPad.SetLeftMargin(0.15)
#  frame_TTJets.GetYaxis().SetTitleOffset(1.4)
#  frame_TTJets.Draw()


  #nll=model.createNLL(data,rf.NumCPU(1))#Fromotherexample,lookslike
  ##pll_phi=nll.createProfile(ROOT.RooArgSet(mc1_yield))#anotherwayofdoingthefitTo
  #
  #ROOT.RooMinuit(nll).migrad()
  #ROOT.RooMinuit(nll).hesse()
  #ROOT.RooMinuit(nll).minos()#optional

  #model.fitTo(data)#ItisthisfitTocommandthatgivesthestatisticaloutput
  nllComponents = ROOT.RooArgList("nllComponents")
  nll=model.createNLL(data,rf.NumCPU(1))
#  nll_NegPdg=model_NegPdg.createNLL(data_NegPdg,rf.NumCPU(1))
  nllComponents.add(nll)
#  nllComponents.add(nll_NegPdg)

  #pll_phi=nll.createProfile(r.RooArgSet(mc1_yield))#anotherwayofdoingthefitTo
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

#  fitFrame_NegPdg=x.frame(rf.Bins(50),rf.Title("FitModel"))
#  model_NegPdg.paramOn(fitFrame_NegPdg,rf.Layout(0.42,0.9,0.9))
#  data_NegPdg.plotOn(fitFrame_NegPdg,rf.LineColor(ROOT.kRed))
#  model_NegPdg.plotOn(fitFrame_NegPdg,rf.LineStyle(ROOT.kDashed))
#  model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_WJets_NegPdg"),rf.LineColor(ROOT.kGreen))
#  model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_TTJets"),rf.LineColor(ROOT.kBlue))
#  model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_Rest_NegPdg"),rf.LineColor(ROOT.kOrange+7))
 
 
  c1=ROOT.TCanvas("c1","FitModel",600,600)
  ROOT.gROOT.SetStyle("Plain")
#  c1.Divide(1,2)
#  c1.cd(1)
  ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
  ROOT.gPad.SetLeftMargin(0.15)
  fitFrame.GetYaxis().SetTitleOffset(1.4)
  fitFrame.GetXaxis().SetTitle('L_{P}')
  fitFrame.Draw()

#  c1.cd(2)
#  ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
#  ROOT.gPad.SetLeftMargin(0.15)
#  fitFrame_NegPdg.GetYaxis().SetTitleOffset(1.4)
#  fitFrame_NegPdg.GetXaxis().SetTitle('nBJetCMVA')
#  fitFrame_NegPdg.Draw()

  c1.Print(printDir+'/'+prefix+'_TemplateFit.png')
  c1.Print(printDir+'/'+prefix+'_TemplateFit.pdf')
  c1.Print(printDir+'/'+prefix+'_TemplateFit.root')
  del c1
  del nllComponents

#  res = {'TT_AllPdg':{'template':template_TTJets, 'yield':2*yield_TTJets.getVal(), 'yield_high':2*(yield_TTJets.getVal()+yield_TTJets.getErrorHi()), 'yield_low':2*(yield_TTJets.getVal()+yield_TTJets.getErrorLo()), 
#                      'yieldVar':(yield_TTJets.getErrorHi()-yield_TTJets.getErrorLo())**2},
#         'W_PosPdg':{'template':template_WJets_PosPdg,'yield':yield_WJets_PosPdg.getVal(), 'yield_high':yield_WJets_PosPdg.getVal()+yield_WJets_PosPdg.getErrorHi(), 'yield_low':yield_WJets_PosPdg.getVal()+yield_WJets_PosPdg.getErrorLo(),
#                     'yieldVar':(0.5*(yield_WJets_PosPdg.getErrorHi()-yield_WJets_PosPdg.getErrorLo()))**2},
#         'W_NegPdg':{'template':template_WJets_NegPdg,'yield':yield_WJets_NegPdg.getVal(), 'yield_high':yield_WJets_NegPdg.getVal()+yield_WJets_NegPdg.getErrorHi(), 'yield_low':yield_WJets_NegPdg.getVal()+yield_WJets_NegPdg.getErrorLo(),
#                     'yieldVar':(0.5*(yield_WJets_NegPdg.getErrorHi()-yield_WJets_NegPdg.getErrorLo()))**2},
#         'Rest_PosPdg':{'template':template_Rest_PosPdg, 'yield':yield_Rest_PosPdg.getVal(), 'yield_high':yield_Rest_PosPdg.getVal()+yield_Rest_PosPdg.getErrorHi(), 'yield_low':yield_Rest_PosPdg.getVal()+yield_Rest_PosPdg.getErrorLo(),
#                     'yieldVar':(0.5*(yield_Rest_PosPdg.getErrorHi()-yield_Rest_PosPdg.getErrorLo()))**2},
#         'Rest_NegPdg':{'template':template_Rest_NegPdg, 'yield':yield_Rest_NegPdg.getVal(), 'yield_high':yield_Rest_NegPdg.getVal()+yield_Rest_NegPdg.getErrorHi(), 'yield_low':yield_Rest_NegPdg.getVal()+yield_Rest_NegPdg.getErrorLo(),
#                     'yieldVar':(0.5*(yield_Rest_NegPdg.getErrorHi()-yield_Rest_NegPdg.getErrorLo()))**2},
#        }
#  del model_NegPdg, model_PosPdg, data_PosPdg, sumNLL
  res = {'EWK':{'template':template_EWK, 'yield':yield_EWK.getVal(), 'yield_high':yield_EWK.getVal()+yield_EWK.getErrorHi(), 'yield_low':yield_EWK.getVal()+yield_EWK.getErrorLo(), 
                      'yieldVar':(yield_EWK.getErrorHi()-yield_EWK.getErrorLo())**2},
         'QCD':{'template':template_QCD,'yield':yield_QCD.getVal(), 'yield_high':yield_QCD.getVal()+yield_QCD.getErrorHi(), 'yield_low':yield_QCD.getVal()+yield_QCD.getErrorLo(),
                     'yieldVar':(yield_QCD.getErrorHi()-yield_QCD.getErrorLo())**2},
        }
  del model, data, sumNLL
  return res



#cWJets  = getChain(WJetsHTToLNu)
#cTTJets = getChain(ttJetsCSA1450ns)
#streg = [[(250, 350), 1.], [(350, -1), 1.]]
#htreg = [(400,500),(500,750),(750, -1)]
##njreg = [(2,2),(3,3),(4,4),(5,-1),(6,-1)]
#
#stb = streg[0][0]
#htb = htreg[1]
#njb = (2,3)
#
#presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0"
#cname, cut = nameAndCut(stb,htb,njb, btb=None, presel=presel)
#
#res = binnedNBTagsFit(cut, samples = {'W':cWJets, 'TT':cTTJets}, nBTagVar = 'nBJetMedium25', prefix=cname)
