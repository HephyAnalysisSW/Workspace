import ROOT
from ROOT import RooFit as rf

import os, sys, copy
import pickle, operator

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()
from math import *
from array import array
from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *

from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2_postprocessed import *

from Workspace.HEPHYPythonTools.user import username

def makeWeight(lumi=4., sampleLumi=3.,debug=False):
  if debug:
    print 'No lumi-reweighting done!!'
    return 'weight', 'weight*weight'
  else:
    weight_str = '(((weight)/'+str(sampleLumi)+')*'+str(lumi)+')'
    weight_err_str = '('+weight_str+'*'+weight_str+')'
  return weight_str, weight_err_str

#25ns samples
WJETS = {'name':'WJets', 'chain':getChain(WJetsHTToLNu_25ns,histname=''), 'color':color('WJets'),'weight':'weight', 'niceName':'W Jets CB ID'}
TTJets = {'name':'TTJets', 'chain':getChain(TTJets_HTLO_25ns,histname=''), 'color':ROOT.kOrange,'weight':'weight', 'niceName':'t#bar{t} Jets HT bin'}

TTJets_semiLep = {'name':'TTJets', 'chain':getChain(TTJets_combined,histname=''), 'color':color('TTJets')-2,'weight':'weight', 'niceName':'t#bar{t} Jets 1l', 'cut':'((ngenLep+ngenTau)<2||(ngenLep+ngenTau)>2)'}
TTJets_diLep = {'name':'TTJets', 'chain':getChain(TTJets_combined,histname=''), 'color':color('TTJets'),'weight':'weight', 'niceName':'t#bar{t} Jets 2l', 'cut':'(ngenLep+ngenTau)==2'}

DY = {'name':'DY', 'chain':getChain(DY_25ns,histname=''), 'color':color('DY'),'weight':'weight', 'niceName':'Drell Yan'}
singleTop = {'name':'singleTop', 'chain':getChain(singleTop_25ns,histname=''), 'color':color('singleTop'),'weight':'weight', 'niceName':'single Top'}
QCD = {'name':'QCD', 'chain':getChain(QCDHT_25ns,histname=''), 'color':color('QCD'),'weight':'weight', 'niceName':'QCD'}
TTVH = {'name':'TTVH', 'chain':getChain(TTV_25ns,histname=''), 'color':color('TTV'),'weight':'weight', 'niceName':'TTVH'}
Rest = {'name':'TTVH', 'chain':getChain([TTV_25ns,singleTop_25ns,DY_25ns],histname=''), 'color':color('TTV'),'weight':'weight', 'niceName':'Rest EWK'}
RestPW = {'name':'Rest', 'chain':getChain([WJetsHTToLNu_25ns,TTV_25ns,singleTop_25ns,DY_25ns],histname=''), 'color':color('TTV'),'weight':'weight', 'niceName':'Rest EWK'}

samples = [TTJets_semiLep, TTJets_diLep, RestPW, QCD]#, diBoson]

TTandWJets = {'name':'TTJets', 'chain':getChain([TTJets_combined,WJetsHTToLNu_25ns],histname=''), 'color':color('TTJets')-2,'weight':'weight', 'niceName':'t#bar{t}+W Jets '}
TTandWJets_semiLep = {'name':'TTJets', 'chain':getChain([TTJets_combined,WJetsHTToLNu_25ns],histname=''), 'color':color('TTJets')-2,'weight':'weight', 'niceName':'t#bar{t} Jets 1l', 'cut':'((ngenLep+ngenTau)<2||(ngenLep+ngenTau)>2)'}


Data = {'name':'data', 'chain':getChain([single_mu_Run2015D, single_ele_Run2015D],histname=''), 'color':ROOT.kBlack,'weight':'weight', 'niceName':'data', 'cut':False}

lumi = 2.11
sampleLumi = 3.
weight_str, weight_err_str = makeWeight(lumi, sampleLumi)

dPhi = {'name':'deltaPhi_Wl', 'binning':[16,0,pi], 'titleX':'#Delta#Phi(W,l)', 'titleY':'Events', 'fileName':'dPhi'}


dPhiJet1Met = {'name':'acos(cos(Jet_phi[0]-met_phi))', 'binning':[16,0,pi], 'titleX':'#Delta#Phi(j_{1},#slash{E}_{T})', 'titleY':'Events', 'fileName':'dPhiJet1Met'}
mindPhiJetMet2 = {'name':'min(acos(cos(Jet_phi[0]-met_phi)),acos(cos(Jet_phi[1]-met_phi)))', 'binning':[16,0,pi], 'titleX':'min(#Delta#Phi(j_{1,2},#slash{E}_{T}))', 'titleY':'Events', 'fileName':'mindPhiJet12Met'}
mindPhiJetMet3 = {'name':'min(min(acos(cos(Jet_phi[0]-met_phi)),acos(cos(Jet_phi[1]-met_phi))),acos(cos(Jet_phi[2]-met_phi)))', 'binning':[16,0,pi], 'titleX':'min(#Delta#Phi(j_{1,2,3},#slash{E}_{T}))', 'titleY':'Events', 'fileName':'mindPhiJet123Met'}
mindPhiJetMet4 = {'name':'min(min(acos(cos(Jet_phi[0]-met_phi)),acos(cos(Jet_phi[1]-met_phi))),min(acos(cos(Jet_phi[2]-met_phi)),acos(cos(Jet_phi[3]-met_phi))))', 'binning':[16,0,pi], 'titleX':'min(#Delta#Phi(j_{1,2,3,4},#slash{E}_{T}))', 'titleY':'Events', 'fileName':'mindPhiJet1234Met'}

dPhiJet2Met = {'name':'acos(cos(Jet_phi[1]-met_phi))', 'binning':[16,0,pi], 'titleX':'#Delta#Phi(j_{2},#slash{E}_{T})', 'titleY':'Events', 'fileName':'dPhiJet2Met'}
dPhiJet3Met = {'name':'acos(cos(Jet_phi[2]-met_phi))', 'binning':[16,0,pi], 'titleX':'#Delta#Phi(j_{3},#slash{E}_{T})', 'titleY':'Events', 'fileName':'dPhiJet3Met'}
dPhiJet4Met = {'name':'acos(cos(Jet_phi[3]-met_phi))', 'binning':[16,0,pi], 'titleX':'#Delta#Phi(j_{4},#slash{E}_{T})', 'titleY':'Events', 'fileName':'dPhiJet4Met'}



triggers = "(HLT_EleHT350||HLT_MuHT350)"
filters = "Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_CSCTightHaloFilter && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter"
presel = "((!isData&&singleLeptonic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
#presel = "((!isData&&singleElectronic)||(isData&&"+triggers+"&&((muonDataSet&&singleMuonic)||(eleDataSet&&singleElectronic))&&"+filters+"))"
presel += "&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80&&st>250&&nJet30>2&&htJet30j>500"
newpresel = presel



#name, cut = nameAndCut((450,-1),(500,-1),(4,5),btb=(1,1),presel=newpresel)
#cut = {'name':name,'string':cut+'&&singleElectronic&&abs(leptonEta)<2.4&&'+filters,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}

#name, cut = nameAndCut((250,350),(500,-1),(3,4),btb=(0,0),presel=newpresel)
#cut2 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}
#
#name, cut = nameAndCut((250,-1),(500,-1),(4,5),btb=(1,1),presel=newpresel)
#cut3 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}
#
#name, cut = nameAndCut((350,450),(500,-1),(4,5),btb=(1,1),presel=newpresel)
#cut4 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}
#
#name, cut = nameAndCut((450,-1),(500,-1),(4,5),btb=(1,1),presel=newpresel)
#cut5 = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}


#binCut = cut
#varList = [dPhiJet1Met, dPhiJet2Met, dPhiJet3Met, dPhiJet4Met, mindPhiJetMet2, mindPhiJetMet3, mindPhiJetMet4]
varList = [dPhi]#, dPhiJet2Met, dPhiJet3Met, mindPhiJetMet2, mindPhiJetMet3]

specialName = ''

printDir = '/afs/hephy.at/user/d/dspitzbart/www/Spring15/25ns/dPhiFit_diLep/'
if not os.path.exists(printDir):
  os.makedirs(printDir)

inclTTSideBand = {(4,5): {(250, -1): {(500, -1): {'deltaPhi': 1.}}}}

#signalRegions = inclTTSideBand
signalRegions = signalRegion3fb

bins = {}

for srNJet in signalRegions:
  bins[srNJet] = {}
  for stb in signalRegions[srNJet]:
    bins[srNJet][stb] ={}
    for htb in signalRegions[srNJet][stb]:
      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      name, cut = nameAndCut(stb,htb,(4,5),btb=(2,2),presel=newpresel)
      nameInc, cutInc = nameAndCut(stb,htb,(4,5),btb=(0,-1),presel=newpresel)
      binCut = {'name':name,'string':cut,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}
      binCutInc = {'name':nameInc,'string':cutInc,'niceName':'L_{T} [250,350), H_{T} [500,-1)'}
      
      bins[srNJet][stb][htb] = {}

      for var in varList:
        template_TTJets_semiLep = getPlotFromChain(TTandWJets_semiLep['chain'], var['name'], var['binning'], binCut['string']+'&&'+TTJets_semiLep['cut'], weight_str)
        template_TTJets_diLep   = getPlotFromChain(TTJets_diLep['chain'], var['name'], var['binning'], binCut['string']+'&&'+TTJets_diLep['cut'], weight_str)
        
        template_QCD = getPlotFromChain(QCD['chain'], var['name'], var['binning'], binCut['string'], weight_str)
        
        template_Rest = getPlotFromChain(Rest['chain'], var['name'], var['binning'], binCut['string'], weight_str)
        
        hData = getPlotFromChain(Data['chain'], var['name'], var['binning'], binCut['string'])
        
        print 'Total MC truth yields:'
        print 'ttbar+Jets 1l:',template_TTJets_semiLep.Integral()
        print 'ttbar+Jets 2l:',template_TTJets_diLep.Integral()
        print 'Rest EWK:', template_Rest.Integral()
        print 'QCD:', template_QCD.Integral()
        
        
        y_TTJets_semiLep = template_TTJets_semiLep.Integral()
        y_TTJets_diLep = template_TTJets_diLep.Integral()
        y_QCD = template_QCD.Integral()
        y_Rest = template_Rest.Integral()
        y_Total = y_TTJets_semiLep + y_TTJets_diLep + y_QCD + y_Rest
        
        template_TTJets_semiLep.Scale(1./template_TTJets_semiLep.Integral())
        template_TTJets_diLep.Scale(1./template_TTJets_diLep.Integral())
        
        template_Rest.Scale(1./template_Rest.Integral())
        if template_QCD.Integral()>0: template_QCD.Scale(1./template_QCD.Integral())
        
        x=ROOT.RooRealVar(var['name'],var['name'],0.,pi)
        
        data=ROOT.RooDataHist("data","data",ROOT.RooArgList(x),hData)
        
        dh_TTJets_semiLep = ROOT.RooDataHist("mcTTJetsSemiLep","mcTTJetsSemiLep",ROOT.RooArgList(x),template_TTJets_semiLep)
        dh_TTJets_diLep = ROOT.RooDataHist("mcTTJetsDiLep","mcTTJetsDiLep",ROOT.RooArgList(x),template_TTJets_diLep)
        dh_Rest=ROOT.RooDataHist("mcRest","mcRest",ROOT.RooArgList(x),template_Rest)
        dh_QCD=ROOT.RooDataHist("mcQCD","mcQCD",ROOT.RooArgList(x),template_QCD)
        
        rooDataHist_arr = [data, dh_TTJets_diLep, dh_TTJets_semiLep , dh_Rest, dh_QCD]
        
        yield_TTJets_semiLep = ROOT.RooRealVar("ttJets_yield_semiLep","yieldTTJets_semiLep",0.1,0,10**5)
        yield_TTJets_diLep = ROOT.RooRealVar("ttJets_yield_diLep","yieldTTJets_diLep",0.1,0,10**5)
        yield_Rest=ROOT.RooRealVar("Rest_yield","yieldRest",y_Rest,y_Rest,y_Rest)
        #yield_Rest=ROOT.RooRealVar("Rest_yield","yieldRest",0.1,0,10**5)
        yield_QCD=ROOT.RooRealVar("QCD_yield","yieldQCD",0.1,0,10**5)
        
        model_TTJets_semiLep = ROOT.RooHistPdf("model_TTJets_semiLep","model_TTJets_semiLep",ROOT.RooArgSet(x),dh_TTJets_semiLep)
        model_TTJets_diLep = ROOT.RooHistPdf("model_TTJets_diLep","model_TTJets_diLep",ROOT.RooArgSet(x),dh_TTJets_diLep)
        
        model_Rest=ROOT.RooHistPdf("model_Rest","model_Rest",ROOT.RooArgSet(x),dh_Rest)
        
        model_QCD=ROOT.RooHistPdf("model_QCD","model_QCD",ROOT.RooArgSet(x),dh_QCD)
        
        model=ROOT.RooAddPdf("model","model",ROOT.RooArgList(model_TTJets_semiLep, model_TTJets_diLep, model_Rest, model_QCD),ROOT.RooArgList(yield_TTJets_semiLep, yield_TTJets_diLep, yield_Rest, yield_QCD))
        
        dframe=x.frame(rf.Title("Data"))
        #dframe_Pdg=x.frame(rf.Title("Data Charge split"))
        
        data.plotOn(dframe)
        
        frame_TTJets_semiLep=x.frame(rf.Title("TTJets_semiLep"))
        model_TTJets_semiLep.plotOn(frame_TTJets_semiLep)
        
        frame_TTJets_diLep=x.frame(rf.Title("TTJets_diLep"))
        model_TTJets_diLep.plotOn(frame_TTJets_diLep)
        
        frame_Rest=x.frame(rf.Title("Rest"))
        model_Rest.plotOn(frame_Rest)
        
        frame_QCD=x.frame(rf.Title("QCD"))
        model_QCD.plotOn(frame_QCD)
        
        print "starting to perform fit !!!!"
        
        #model.fitTo(data)#It is this fitTo command that gives the statistical output
        nllComponents = ROOT.RooArgList("nllComponents")
        nll=model.createNLL(data,rf.NumCPU(1))
        nllComponents.add(nll)
        
        #pll_phi=nll.createProfile(r.RooArgSet(mc1_yield))#anotherwayofdoingthefitTo
        sumNLL = ROOT.RooAddition("sumNLL","sumNLL", nllComponents)
        
        ROOT.RooMinuit(sumNLL).migrad()
        ROOT.RooMinuit(sumNLL).hesse()
        ROOT.RooMinuit(sumNLL).minos()#optional
        
        #myPdf->paramOn(frame,Layout(xmin,ymin,ymax))
        fitFrame=x.frame(rf.Bins(50),rf.Title("FitModel"))
        model.paramOn(fitFrame,rf.Layout(0.42,0.9,0.9))
        data.plotOn(fitFrame,rf.LineColor(ROOT.kRed))
        model.plotOn(fitFrame,rf.LineStyle(ROOT.kDashed))
        model.plotOn(fitFrame,rf.Components("model_TTJets_semiLep"),rf.LineColor(ROOT.kBlue))
        model.plotOn(fitFrame,rf.Components("model_TTJets_diLep"),rf.LineColor(ROOT.kBlue+2))
        model.plotOn(fitFrame,rf.Components("model_Rest"),rf.LineColor(ROOT.kOrange+7))
        model.plotOn(fitFrame,rf.Components("model_QCD"),rf.LineColor(color('QCD')))
        
        print "** Fit results **"
        print "yield_TTJets_semiLep:" , yield_TTJets_semiLep.getVal()
        print "yield_TTJets_diLep:" , yield_TTJets_diLep.getVal()
        print "yield_Rest:" , yield_Rest.getVal()
        print "yield_QCD:", yield_QCD.getVal()
        print
        fit_total = yield_TTJets_semiLep.getVal()+yield_TTJets_diLep.getVal()+yield_Rest.getVal()+yield_QCD.getVal()

        fit = {'TTJets_semiLep':yield_TTJets_semiLep.getVal(), 'TTJets_diLep':yield_TTJets_diLep.getVal(), 'Rest':yield_Rest.getVal(), 'QCD':yield_QCD.getVal()}
        fit_frac = {}
        for key in fit:
          fit_frac[key] = fit[key]/fit_total
        
        print
        print "** MC truth **"
        print "TTJets_semiLep:" , y_TTJets_semiLep
        print "TTJets_diLep:" , y_TTJets_diLep
        print "Rest:" , y_Rest
        print "QCD:", y_QCD
        print
        
        truth_total = y_TTJets_semiLep + y_TTJets_diLep + y_Rest + y_QCD
        
        truth = {'TTJets_semiLep':y_TTJets_semiLep, 'TTJets_diLep':y_TTJets_diLep, 'Rest':y_Rest, 'QCD':y_QCD}
        truth_frac = {}
        for key in truth:
          truth_frac[key] = truth[key]/truth_total
      
        bins[srNJet][stb][htb][var['fileName']] = {'MCtruth':truth, 'MCtruth_frac':truth_frac, 'fit':fit, 'fit_frac':fit_frac}
                
        c2=ROOT.TCanvas("c2","FitModel",650,500)
        ROOT.gROOT.SetStyle("Plain")
        ROOT.gROOT.SetStyle("Plain")#Removesgraybackgroundfromplots
        ROOT.gPad.SetLeftMargin(0.15)
        fitFrame.GetYaxis().SetTitleOffset(1.4)
        fitFrame.GetXaxis().SetTitle(var['titleX'])
        fitFrame.Draw()
        
        c3=ROOT.TCanvas("c3","templates",650,500)
        template_TTJets_semiLep.SetLineColor(color('ttjets')-2)
        template_TTJets_semiLep.SetMaximum(0.4)
        template_TTJets_diLep.SetLineColor(color('ttjets'))
        template_QCD.SetLineColor(color('qcd'))
        template_Rest.SetLineColor(color('wjets'))
        
        template_TTJets_semiLep.Draw('hist e1')
        template_TTJets_diLep.Draw('hist e1 same')
        template_QCD.Draw('hist e1 same')
        template_Rest.Draw('hist e1 same')
        
        
        ROOT.setTDRStyle()
        ROOT.gStyle.SetPalette(1)
        c4=ROOT.TCanvas("c4","correlation",650,500)
        res = model.fitTo(data, rf.Save())
        resH = res.correlationHist()
        resH.SetMarkerSize(2)
        
        pad1=ROOT.TPad("pad1","MyTitle",0.,0.,1.,1.)
        pad1.SetLeftMargin(0.15)
        pad1.SetBottomMargin(0.1)
        pad1.SetRightMargin(0.15)
        pad1.Draw()
        pad1.cd()
        
        resH.GetXaxis().SetBinLabel(1,'QCD')
        resH.GetXaxis().SetBinLabel(2,'W+jets')
        resH.GetXaxis().SetBinLabel(3,'t#bar{t}+jets')
        resH.GetXaxis().SetBinLabel(4,'Rest EWK')
        
        resH.GetYaxis().SetBinLabel(4,'QCD')
        resH.GetYaxis().SetBinLabel(3,'W+jets')
        resH.GetYaxis().SetBinLabel(2,'t#bar{t}+jets')
        resH.GetYaxis().SetBinLabel(1,'Rest EWK')
        resH.Draw('colz text')
        
        c2.Print(printDir+specialName+name+'_'+var['fileName']+'_fit.png')
        c3.Print(printDir+specialName+name+'_'+var['fileName']+'_templates.png')
        c4.Print(printDir+specialName+name+'_'+var['fileName']+'_correlation.png')


