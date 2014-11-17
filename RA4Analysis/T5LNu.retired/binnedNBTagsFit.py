import ROOT
from ROOT import RooFit as rf

from Workspace.HEPHYPythonTools.helpers import getPlotFromChain,getCutYieldFromChain,getObjFromFile
from helpers import nameAndCut

cWJets=ROOT.TChain('Events')
cWJets.Add('/data/schoef/convertedTuples_v22/copy/WJetsHT150v2/histo_WJetsHT150v2*.root')
cTTJets=ROOT.TChain('Events')
cTTJets.Add('/data/schoef/convertedTuples_v22/copy/TTJetsPowHeg/histo_TTJetsPowHeg*.root')

cRest=ROOT.TChain('Events')
for s in['WW','ZZ','WZ','singleTop','DY','QCD20to600','QCD600to1000','QCD1000']:
  cRest.Add('/data/schoef/convertedTuples_v22/copy/'+s+'/histo_'+s+'*.root')

cData=ROOT.TChain('Events')
cData.Add('/data/schoef/convertedTuples_v22/copy/data/histo_data*.root')


metb=[150,350]
htb=[400,750]
njetb=[2,3]
lpdg=''
mTCut='mT>20&&mT<120'

template_WJets_PosPdg=getPlotFromChain(cWJets,'nbtags',[0,1,2,3],mTCut+'&&'+nameAndCut(metb,htb,njetb,'pos',btagRequirement='None')[1],'weight',binningIsExplicit=True,addOverFlowBin='upper')
template_WJets_NegPdg=getPlotFromChain(cWJets,'nbtags',[0,1,2,3],mTCut+'&&'+nameAndCut(metb,htb,njetb,'neg',btagRequirement='None')[1],'weight',binningIsExplicit=True,addOverFlowBin='upper')
template_TTJets=getPlotFromChain(cTTJets,'nbtags',[0,1,2,3],mTCut+'&&'+nameAndCut(metb,htb,njetb,'',btagRequirement='None')[1],'weight',binningIsExplicit=True,addOverFlowBin='upper')
template_Rest_PosPdg=getPlotFromChain(cRest,'nbtags',[0,1,2,3],mTCut+'&&'+nameAndCut(metb,htb,njetb,'pos',btagRequirement='None')[1],'weight',binningIsExplicit=True,addOverFlowBin='upper')
template_Rest_NegPdg=getPlotFromChain(cRest,'nbtags',[0,1,2,3],mTCut+'&&'+nameAndCut(metb,htb,njetb,'neg',btagRequirement='None')[1],'weight',binningIsExplicit=True,addOverFlowBin='upper')

print "Nominal yields TT:",template_TTJets.Integral(),'WJets_PosPdg',template_WJets_PosPdg.Integral(),'WJets_NegPdg',template_WJets_NegPdg.Integral()
print "Nominal yields:",'Rest_PosPdg',template_Rest_PosPdg.Integral(),'Rest_NegPdg',template_Rest_NegPdg.Integral()

#template_WJets_PosPdg.Scale(1./template_WJets_PosPdg.GetBinContent(1))
#template_WJets_NegPdg.Scale(1./template_WJets_NegPdg.GetBinContent(1))
#template_TTJets.Scale(1./template_TTJets.GetBinContent(1))

hData_PosPdg=getPlotFromChain(cData,'nbtags',[0,1,2,3],mTCut+'&&'+nameAndCut(metb,htb,njetb,'pos',btagRequirement='None')[1],'weight',binningIsExplicit=True,addOverFlowBin='upper')
hData_NegPdg=getPlotFromChain(cData,'nbtags',[0,1,2,3],mTCut+'&&'+nameAndCut(metb,htb,njetb,'neg',btagRequirement='None')[1],'weight',binningIsExplicit=True,addOverFlowBin='upper')


x=ROOT.RooRealVar("nbtags","nbtags",0.,3.)

data_PosPdg=ROOT.RooDataHist("data","data",ROOT.RooArgList(x),hData_PosPdg)
data_NegPdg=ROOT.RooDataHist("data","data",ROOT.RooArgList(x),hData_NegPdg)

dh_WJets_PosPdg=ROOT.RooDataHist("mcWJets","mcWJets",ROOT.RooArgList(x),template_WJets_PosPdg)
dh_WJets_NegPdg=ROOT.RooDataHist("mcWJets","mcWJets",ROOT.RooArgList(x),template_WJets_NegPdg)
dh_TTJets=ROOT.RooDataHist("mcTTJets","mcTTJets",ROOT.RooArgList(x),template_TTJets)
dh_Rest_PosPdg=ROOT.RooDataHist("mcRest","mcRest",ROOT.RooArgList(x),template_Rest_PosPdg)
dh_Rest_NegPdg=ROOT.RooDataHist("mcRest","mcRest",ROOT.RooArgList(x),template_Rest_NegPdg)

yield_WJets_PosPdg = ROOT.RooRealVar("yield_WJets_PosPdg","yield_WJets_PosPdg",0.1,0,10**5)
yield_WJets_NegPdg = ROOT.RooRealVar("yield_WJets_NegPdg","yield_WJets_NegPdg",0.1,0,10**5)
yield_TTJets=ROOT.RooRealVar("ttJets_yield","yieldTTJets",0.1,0,10**5)
yield_Rest_PosPdg = ROOT.RooRealVar("yield_Rest_PosPdg","yield_Rest_PosPdg",1,1,1)
yield_Rest_NegPdg = ROOT.RooRealVar("yield_Rest_NegPdg","yield_Rest_NegPdg",1,1,1)
yield_Rest_NegPdg.setConstant()
yield_Rest_PosPdg.setConstant()

#MakePDFfromMChistograms
model_WJets_PosPdg=ROOT.RooHistPdf("model_WJets_PosPdg","model_WJets_PosPdg",ROOT.RooArgSet(x),dh_WJets_PosPdg)
model_WJets_NegPdg=ROOT.RooHistPdf("model_WJets_NegPdg","model_WJets_NegPdg",ROOT.RooArgSet(x),dh_WJets_NegPdg)
model_TTJets=ROOT.RooHistPdf("model_TTJets","model_TTJets",ROOT.RooArgSet(x),dh_TTJets)
model_Rest_PosPdg=ROOT.RooHistPdf("model_Rest_PosPdg","model_Rest_PosPdg",ROOT.RooArgSet(x),dh_Rest_PosPdg)
model_Rest_NegPdg=ROOT.RooHistPdf("model_Rest_NegPdg","model_Rest_NegPdg",ROOT.RooArgSet(x),dh_Rest_NegPdg)

model_PosPdg=ROOT.RooAddPdf("model_PosPdg","model_PosPdg",ROOT.RooArgList(model_WJets_PosPdg, model_TTJets, model_Rest_PosPdg),ROOT.RooArgList(yield_WJets_PosPdg, yield_TTJets, yield_Rest_PosPdg))
model_NegPdg=ROOT.RooAddPdf("model_NegPdg","model_NegPdg",ROOT.RooArgList(model_WJets_NegPdg, model_TTJets, model_Rest_NegPdg),ROOT.RooArgList(yield_WJets_NegPdg, yield_TTJets, yield_Rest_NegPdg))
#CombinesmyMCsintoonePDFmodel


#Plottheimportedhistogram(s)
dframe=x.frame(rf.Title("Data"))
data_PosPdg.plotOn(dframe)
data_NegPdg.plotOn(dframe)

frame_WJets_PosPdg=x.frame(rf.Title("WJets PosPdg"))
model_WJets_PosPdg.plotOn(frame_WJets_PosPdg)
frame_WJets_NegPdg=x.frame(rf.Title("WJets NegPdg"))
model_WJets_NegPdg.plotOn(frame_WJets_NegPdg)

frame_TTJets=x.frame(rf.Title("TTJets"))
model_TTJets.plotOn(frame_TTJets)

c=ROOT.TCanvas("roofit_example","RooFitFractionFitExample",800,1200)
c.Divide(1,3)
ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
c.cd(1)
ROOT.gPad.SetLeftMargin(0.15)
dframe.GetYaxis().SetTitleOffset(1.4)
dframe.Draw()
c.cd(2)
ROOT.gPad.SetLeftMargin(0.15)
frame_WJets_PosPdg.GetYaxis().SetTitleOffset(1.4)
frame_WJets_PosPdg.Draw()
frame_WJets_NegPdg.Draw('same')
c.cd(3)
ROOT.gPad.SetLeftMargin(0.15)
frame_TTJets.GetYaxis().SetTitleOffset(1.4)
frame_TTJets.Draw()


ROOT.gROOT.SetStyle("Plain")

#nll=model.createNLL(data,rf.NumCPU(1))#Fromotherexample,lookslike
##pll_phi=nll.createProfile(ROOT.RooArgSet(mc1_yield))#anotherwayofdoingthefitTo
#
#ROOT.RooMinuit(nll).migrad()
#ROOT.RooMinuit(nll).hesse()
#ROOT.RooMinuit(nll).minos()#optional

#model.fitTo(data)#ItisthisfitTocommandthatgivesthestatisticaloutput
nllComponents = ROOT.RooArgList("nllComponents")
nll_PosPdg=model_PosPdg.createNLL(data_PosPdg,rf.NumCPU(1))
nll_NegPdg=model_NegPdg.createNLL(data_NegPdg,rf.NumCPU(1))
nllComponents.add(nll_PosPdg)
nllComponents.add(nll_NegPdg)

#pll_phi=nll.createProfile(r.RooArgSet(mc1_yield))#anotherwayofdoingthefitTo
sumNLL = ROOT.RooAddition("sumNLL","sumNLL", nllComponents)

ROOT.RooMinuit(sumNLL).migrad()
ROOT.RooMinuit(sumNLL).hesse()
ROOT.RooMinuit(sumNLL).minos()#optional

fitFrame_PosPdg=x.frame(rf.Bins(50),rf.Title("FitModel"))
model_PosPdg.paramOn(fitFrame_PosPdg)
data_PosPdg.plotOn(fitFrame_PosPdg,rf.LineColor(ROOT.kRed))
model_PosPdg.plotOn(fitFrame_PosPdg,rf.LineStyle(ROOT.kDashed))
model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_WJets_PosPdg"),rf.LineColor(ROOT.kGreen))
model_PosPdg.plotOn(fitFrame_PosPdg,rf.Components("model_TTJets"),rf.LineColor(ROOT.kBlue))

fitFrame_NegPdg=x.frame(rf.Bins(50),rf.Title("FitModel"))
model_NegPdg.paramOn(fitFrame_NegPdg)
data_NegPdg.plotOn(fitFrame_NegPdg,rf.LineColor(ROOT.kRed))
model_NegPdg.plotOn(fitFrame_NegPdg,rf.LineStyle(ROOT.kDashed))
model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_WJets_NegPdg"),rf.LineColor(ROOT.kGreen))
model_NegPdg.plotOn(fitFrame_NegPdg,rf.Components("model_TTJets"),rf.LineColor(ROOT.kBlue))

c6=ROOT.TCanvas("c6","FitModel",800,1200)
c6.Divide(1,2)
c6.cd(1)
ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
ROOT.gPad.SetLeftMargin(0.15)
fitFrame_PosPdg.GetYaxis().SetTitleOffset(1.4)
fitFrame_PosPdg.Draw()

c6.cd(2)
ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
ROOT.gPad.SetLeftMargin(0.15)
fitFrame_NegPdg.GetYaxis().SetTitleOffset(1.4)
fitFrame_NegPdg.Draw()

#params=model_PosPdg.getParameters(ROOT.RooArgSet(x))


