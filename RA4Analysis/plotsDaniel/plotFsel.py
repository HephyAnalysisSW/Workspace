import ROOT, pickle, itertools
import os

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *

ROOT.gROOT.LoadMacro('../../HEPHYPythonTools/scripts/root/tdrstyle.C')
ROOT.setTDRStyle()


can = ROOT.TCanvas('can','can',600,600)
can.SetBottomMargin(0.22)
fitresFile = '/afs/hephy.at/data/dspitzbart01/RA4/Moriond2017/QCDEstimation/20170306_fitResult_Moriond17SR_v8_data35p9fb_multib'
fitres = pickle.load(file(os.path.expandvars(fitresFile)))

bins = len(fitres[(3,4)].keys())

fselH = ROOT.TH1F('Fsel','Fsel',bins,0,bins)

binNamesMultiB  = ['LTi_NJ34','LT12_NJ34','LT3_NJ34','LT4_NJ34','LT5i_NJ34']
binNamesZeroB   = ['LT1_NJ34','LT2_NJ34','LT3_NJ34','LT4_NJ34']

binNames = binNamesMultiB



plotFile = '/afs/hephy.at/user/d/dspitzbart/www/Results2016B/QCD/Moriond17/Fsel_multiB_update'
txtFile = plotFile + '.txt'

txt = open(txtFile,'w')

print '{:15}{:12}{:12}'.format('#Bin','F-ratio','Error')
txt.write('{:15}{:12}{:12}\n'.format('#Bin','F-ratio','Error'))


for i,lt in enumerate(sorted(fitres[(3,4)])):
  fsel      = fitres[(3,4)][lt][(500,-1)]['F_seltoantisel']
  fsel_err  = fitres[(3,4)][lt][(500,-1)]['F_seltoantisel_err']
  print '{:15}{:<12.4f}{:<12.4f}'.format(binNames[i],fsel,fsel_err)
  txt.write('{:15}{:<12.4f}{:<12.4f}\n'.format(binNames[i],fsel,fsel_err))
  #print i, lt,fsel
  fselH.SetBinContent(i+1,fsel)
  fselH.SetBinError(i+1,fsel_err)
  fselH.GetXaxis().SetBinLabel(i+1,varBinName(lt,'L_{T}'))
  
txt.close()
fselH.SetLineColor(ROOT.kAzure+9)
fselH.SetMarkerColor(ROOT.kAzure+9)
fselH.SetLineWidth(2)

fselH.SetMinimum(0)

fselH.GetYaxis().SetTitle('F_{sel-to-antisel}')
fselH.GetXaxis().SetTitle('L_{T} (GeV)')

fselH.Draw()
  
  
latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.16,0.96,'CMS #bf{#it{Preliminary}}')
latex1.DrawLatex(0.74,0.96,'35.9fb^{-1}#bf{(13TeV)}')

#can.SetLogy()
 
can.Print(plotFile+'.png')
can.Print(plotFile+'.pdf')
can.Print(plotFile+'.root')
  
