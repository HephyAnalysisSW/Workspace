import ROOT
import pickle
import copy, os, sys
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetMarkerStyle(1)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.signalRegions import *
from localInfo import username
from math import *

signalRegion = signalRegion3fb

target_lumi = 3000 #pb-1

preprefix = 'QCDestimation/ratioPlots'
wwwDir = '/afs/hephy.at/user/d/dhandl/www/pngCMG2/hard/Phys14V3/'+preprefix+'/'
presel = 'QCDratio_singleElectronic_'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

#add the path where the pickle files are located
path = '/data/'+username+'/results2015/rCS_0b/'

def getNumString(n,ne, acc=2):    ##For printing table 
  if type(n) is float and type(ne) is float:
    return str(round(n,acc))+'&$\pm$&'+str(round(ne,acc))
  #if type(n) is str and type(ne) is str: 
  else:
    return n +'&$\pm$&'+ ne

def getQCDfraction(Bkg, Bkg_err, QCD, QCD_err):
  if QCD>0 and Bkg>0:
    res = QCD/Bkg
    res_err = res*sqrt(Bkg_err**2/Bkg**2 + QCD_err**2/QCD**2)
  else:
    res = float('nan')
    res_err = float('nan')
  return res, res_err

controlRegion = [\
                  {'name':'lowST_inclHT', 'axisName':'low S_{T}, '+varBinName((500,-1),'H_{T}'), 'file':pickle.load(file('/data/dhandl/results2015/rCS_0b/QCDyieldFromTemplateFit_st250-350_ht500_njet3-4_nbtagEq0_pkl'))},\
                  {'name':'medST_inclHT', 'axisName':'medium S_{T}, '+varBinName((500,-1),'H_{T}'), 'file':pickle.load(file('/data/dhandl/results2015/rCS_0b/QCDyieldFromTemplateFit_st350-450_ht500_njet3-4_nbtagEq0_pkl'))},\
                  {'name':'highST_inclHT', 'axisName':'high S_{T}, '+varBinName((500,-1),'H_{T}'), 'file':pickle.load(file('/data/dhandl/results2015/rCS_0b/QCDyieldFromTemplateFit_st450_ht500_njet3-4_nbtagEq0_pkl'))},\
                  {'name':'lowST_lowHT', 'axisName':'low S_{T}, '+varBinName((500,750),'H_{T}'), 'file':pickle.load(file('/data/dhandl/results2015/rCS_0b/QCDyieldFromTemplateFit_st250-350_ht500-750_njet3-4_nbtagEq0_pkl'))},\
                  {'name':'lowST_medInclHT', 'axisName':'low S_{T}, '+varBinName((750,-1),'H_{T}'), 'file':pickle.load(file('/data/dhandl/results2015/rCS_0b/QCDyieldFromTemplateFit_st250-350_ht750_njet3-4_nbtagEq0_pkl'))},\
                  {'name':'medST_lowHT', 'axisName':'med S_{T}, '+varBinName((500,750),'H_{T}'), 'file':pickle.load(file('/data/dhandl/results2015/rCS_0b/QCDyieldFromTemplateFit_st350-450_ht500-750_njet3-4_nbtagEq0_pkl'))},\
                  {'name':'medST_medInclHT', 'axisName':'med S_{T}, '+varBinName((750,-1),'H_{T}'), 'file':pickle.load(file('/data/dhandl/results2015/rCS_0b/QCDyieldFromTemplateFit_st350-450_ht750_njet3-4_nbtagEq0_pkl'))},\
                  {'name':'highST_highHT', 'axisName':'high S_{T}, '+varBinName((500,1000),'H_{T}'), 'file':pickle.load(file('/data/dhandl/results2015/rCS_0b/QCDyieldFromTemplateFit_st450_ht500-1000_njet3-4_nbtagEq0_pkl'))},\
                  {'name':'highST_highInclHT', 'axisName':'high S_{T}, '+varBinName((1000,-1),'H_{T}'), 'file':pickle.load(file('/data/dhandl/results2015/rCS_0b/QCDyieldFromTemplateFit_st450_ht1000_njet3-4_nbtagEq0_pkl'))}\
]
for CR in controlRegion:
  res = CR['file']
  for htb in res:
    for stb in res[htb]:
        for njb in res[htb][stb]:
            for btb in res[htb][stb][njb]:
                CR['F_seltoantisel'] = res[htb][stb][njb][btb]['F_seltoantisel']
                CR['F_seltoantisel_err'] = res[htb][stb][njb][btb]['F_seltoantisel_err']
                CR['NQCDSelMC'] = res[htb][stb][njb][btb]['NQCDSelMC']
                CR['NQCDSelMC_err'] = res[htb][stb][njb][btb]['NQCDSelMC_err']
                CR['NQCD_fit'] = res[htb][stb][njb][btb]['QCD']['yield']
                CR['NQCD_fit_err'] = sqrt(res[htb][stb][njb][btb]['QCD']['yieldVar'])

text=ROOT.TLatex()
text.SetNDC()
text.SetTextSize(0.04)
text.SetTextAlign(11)

canv = ROOT.TCanvas('canv','canv',600,600)

Fhist=ROOT.TH1F('Fhist','Fhist',len(controlRegion),0,len(controlRegion))
Fhist.SetLineWidth(2)
for i_CR, CR in enumerate(controlRegion):
  Fhist.SetBinContent(i_CR+1,CR['F_seltoantisel'])
  Fhist.SetBinError(i_CR+1,CR['F_seltoantisel_err'])
  Fhist.GetXaxis().SetBinLabel(i_CR+1,CR['axisName'])
  Fhist.GetYaxis().SetTitle('F_{sel-to-antisel}')

Fhist.Draw('L')
text.DrawLatex(0.15,.96,"CMS Simulation")
text.DrawLatex(0.65,0.96,"L="+str(target_lumi/1000)+" fb^{-1} (13 TeV)")

#canv.Print(wwwDir+presel+'Fsa_usingFit_inCR.png')
#canv.Print(wwwDir+presel+'Fsa_usingFit_inCR.pdf')
#canv.Print(wwwDir+presel+'Fsa_usingFit_inCR.root')

canv2 = ROOT.TCanvas('canv2','canv2',600,600)

ClosureHist=ROOT.TH1F('ClosureHist','ClosureHist',len(controlRegion),0,len(controlRegion))
ClosureHist.SetLineWidth(2)
for i_CR, CR in enumerate(controlRegion):
  res, res_err = getQCDfraction(CR['NQCDSelMC'],CR['NQCDSelMC_err'],CR['NQCD_fit'],CR['NQCD_fit_err'])
  ClosureHist.SetBinContent(i_CR+1,res)
  ClosureHist.SetBinError(i_CR+1,res_err)
  ClosureHist.GetXaxis().SetBinLabel(i_CR+1,CR['axisName'])
  ClosureHist.GetYaxis().SetTitle('#frac{N^{fit}_{QCD}}{N^{MC}_{QCD}}')

ClosureHist.Draw('L')
text.DrawLatex(0.15,.96,"CMS Simulation")
text.DrawLatex(0.65,0.96,"L="+str(target_lumi/1000)+" fb^{-1} (13 TeV)")

line = ROOT.TLine()
line.SetY1(1.0)
line.SetX2(len(CR))
line.SetHorizontal()
line.SetLineColor(ROOT.kBlack)
line.SetLineStyle(ROOT.kDashed)
line.Draw()

#canv2.Print(wwwDir+presel+'FitClosure_inCR.png')
#canv2.Print(wwwDir+presel+'FitClosure_inCR.pdf')
#canv2.Print(wwwDir+presel+'FitClosure_inCR.root')
