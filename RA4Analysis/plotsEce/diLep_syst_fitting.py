import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.signalRegions import signalRegion3fb
from cutFlow_helper import *
from math import *
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)
lumi = 2250##pb
path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p3fb/diLep_syst_study_results/"
SR = signalRegion3fb

btagVarString = 'nBJetMediumCSV30'
p = {'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}','logy':False , 'var':'nJet30','varname':'nJet30', 'binlabel':1,  'bin':(6,3,9)}

bin = {}
for srNJet in sorted(SR):
  bin[srNJet]={}
  for stb in sorted(SR[srNJet]):
    bin[srNJet][stb] = {}
    for htb in sorted(SR[srNJet][stb]):
      bin[srNJet][stb][htb] = {}
      Name, bla_Cut = nameAndCut(stb, htb, srNJet, btb=(0,0), presel="(1)", btagVar =  btagVarString)
      print Name
      fratio_diLep = ROOT.TFile(path+Name+'_'+p['varname']+'_allWeights_diLep_4_Ratio.root')
      fratio_oneLep = ROOT.TFile(path+Name+'_'+p['varname']+'_allWeights_Ratio_4.root')
      cb = ROOT.TCanvas("cb","cb",800,800)
      cb.cd()
      latex = ROOT.TLatex()
      latex.SetNDC()
      latex.SetTextSize(0.04)
      latex.SetTextAlign(11) 
      h_ratio_diLep = fratio_diLep.Get("h_ratio")
      h_ratio_oneLep = fratio_oneLep.Get("h_ratio")
      h_double_ratio = h_ratio_diLep.Clone("h_double_ratio")
      h_double_ratio.Divide(h_ratio_oneLep)
      h_double_ratio.GetXaxis().SetLabelSize(0.1)
      h_double_ratio.GetXaxis().SetLabelSize(0.05)
      h_double_ratio.GetYaxis().SetLabelSize(0.05)
      h_double_ratio.GetYaxis().SetTitleSize(0.1)
      h_double_ratio.GetYaxis().SetTitleSize(0.05)
      h_double_ratio.Sumw2()
      h_double_ratio.Draw()
      func = ROOT.TF1("my","[0] + [1] * (x-"+str(format(h_double_ratio.GetMean(),'.3f'))+")",4,9)
      h_double_ratio.Fit(func)
      FitFunc     = h_double_ratio.GetFunction('my')
      latex.DrawLatex(0.6,0.85,"Fit:")
      latex.DrawLatex(0.6,0.8,"Constant:"+str(format(FitFunc.GetParameter(0),'.3f'))+"+-"+str(format(FitFunc.GetParError(0),'.3f')))
      latex.DrawLatex(0.6,0.75,"Slope:"+str(format(FitFunc.GetParameter(1),'.3f'))+"+-"+str(format(FitFunc.GetParError(1),'.3f')))
      latex.DrawLatex(0.6,0.7, "mean:"+str(format(h_ratio3.GetMean(),'.3f')))
      latex.DrawLatex(0.2,0.85,"(nJet+add lost)/(nJet)")
      bin[srNJet][stb][htb]["constant"] = sqrt(abs(1-FitFunc.GetParameter(0))**2+abs(FitFunc.GetParError(0))**2)
      bin[srNJet][stb][htb]["slope"] = sqrt(abs(0-abs(FitFunc.GetParameter(1)))**2+abs(FitFunc.GetParError(1))**2)
      bin[srNJet][stb][htb]["nJetMean"] = h_double_ratio.GetMean()
      print "mean:" , bin[srNJet][stb][htb]["nJetMean"]
      print "constant",abs(1-FitFunc.GetParameter(0)) ,"error", abs(FitFunc.GetParError(0)),"quad sum of constant:" , bin[srNJet][stb][htb]["constant"]
      print "slope",abs(0-abs(FitFunc.GetParameter(1))) ,"error", abs(FitFunc.GetParError(1)),"quad sum of constant:" , bin[srNJet][stb][htb]["slope"]
      cb.SaveAs(path+Name+'_'+p['varname']+'_allWeights_double_Ratio.root')
      cb.SaveAs(path+Name+'_'+p['varname']+'_allWeights_double_Ratio.png')
      cb.SaveAs(path+Name+'_'+p['varname']+'_allWeights_double_Ratio.pdf')
      #for f_ratio in [{'name':'diLep' , 'file':fratio_diLep} , {'name':'oneLep' , 'file':fratio_oneLep}]:
      #  cb = ROOT.TCanvas("cb","cb",800,800)
      #  cb.cd()
      #  latex = ROOT.TLatex()
      #  latex.SetNDC()
      #  latex.SetTextSize(0.04)
      #  latex.SetTextAlign(11)
      #  h_ratio = f_ratio['file'].Get("h_ratio")
      #  h_ratio.GetXaxis().SetLabelSize(0.1)
      #  h_ratio.GetXaxis().SetLabelSize(0.05)
      #  h_ratio.GetYaxis().SetLabelSize(0.05)
      #  h_ratio.GetYaxis().SetTitleSize(0.1)
      #  h_ratio.GetYaxis().SetTitleSize(0.05)
      #  h_ratio.GetXaxis().SetTitle("nJets")
      #  h_ratio.GetYaxis().SetNdivisions(510)
      #  h_ratio.Draw()
      #  func = ROOT.TF1("my","[0] + [1] * (x-"+str(format(h_ratio.GetMean(),'.3f'))+")",4,9)
      #  h_ratio.Fit('my')
      #  FitFunc     = h_ratio.GetFunction('my')
      #  latex.DrawLatex(0.6,0.85,"Fit:")
      #  latex.DrawLatex(0.6,0.8,"Constant:"+str(format(FitFunc.GetParameter(0),'.3f'))+"+-"+str(format(FitFunc.GetParError(0),'.3f')))
      #  latex.DrawLatex(0.6,0.75,"Slope:"+str(format(FitFunc.GetParameter(1),'.3f'))+"+-"+str(format(FitFunc.GetParError(1),'.3f')))
      #  latex.DrawLatex(0.6,0.7, "mean:"+str(format(h_ratio.GetMean(),'.3f')))
      #  latex.DrawLatex(0.3,0.85,"nJet")
      #  cb.SaveAs(path+Name+'_'+p['varname']+'_allWeights_'+f_ratio['name']+'_Ratio.root')
      #  cb.SaveAs(path+Name+'_'+p['varname']+'_allWeights_'+f_ratio['name']+'_Ratio.png')
      #  cb.SaveAs(path+Name+'_'+p['varname']+'_allWeights_'+f_ratio['name']+'_Ratio.pdf')



pickle.dump(bin,file('/data/easilar/Spring15/25ns/DL_syst_pkl','w'))
