import ROOT
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain

from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin
from rCShelpers import *
import math
import pickle
from Workspace.RA4Analysis.signalRegions import *

small = False
maxN = -1 if not small else 1

lepSel = 'hard'

cWJets  = getChain(WJetsHTToLNu[lepSel],histname='',maxN=maxN)
cTTJets = getChain(ttJets[lepSel],histname='',maxN=maxN)
cEWK = getChain([WJetsHTToLNu[lepSel],ttJets[lepSel],TTVH[lepSel],singleTop[lepSel],DY[lepSel]],histname='')


from localInfo import username
uDir = username[0]+'/'+username
subDir = 'PHYS14v3/ANplots/rCSbtagmultiCompleteCorrection/'

### DEFINE SR
regions = sideBand10fb.values()[0]

path = '/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'
if not os.path.exists(path):
  os.makedirs(path)

picklePath = '/data/'+username+'/PHYS14v3/withCSV/rCS_0b_10.0fbSlidingWcorrectionMuonChannel/'
if not os.path.exists(picklePath):
  os.makedirs(picklePath)

ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kAzure-1, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
dPhiStr = 'deltaPhi_Wl'
#no stat box
ROOT.gStyle.SetOptStat(0)

ROOT.TH1F().SetDefaultSumw2()

btreg = (0,0)
njreg = [(2,2),(3,3),(4,4),(5,5),(6,7),(8,-1)]#,(7,7),(8,8),(9,9)]
nbjreg = [(0,0),(1,1)]#,(2,2)]

presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80'
prefix = presel.split('&&')[0]+'_'

h_nbj = {}
for name, c in [["tt", cTTJets] , ["W",cWJets] ]:
  h_nbj[name] = {}
  for stb in regions:
    h_nbj[name][stb] = {}
    for i_htb, htb in enumerate(regions[stb]):
      h_nbj[name][stb][htb] = {}
      for i_nbjb, bjb in enumerate(nbjreg):
        h_nbj[name][stb][htb][bjb] = ROOT.TH1F("rcs_nbj","",len(njreg),0,len(njreg))
        for i_njb, njb in enumerate(njreg):
          cname, cut = nameAndCut(stb,htb,njb, btb=bjb ,presel=presel)
          dPhiCut = dynDeltaPhi(1.0,stb, htb, njb) #use the function and not the deltaPhi of the dict!
          if bjb == (1,1):
            rcs = getRCS(cEWK, cut, dPhiCut)
          else:
            rcs = getRCS(c, cut, dPhiCut)
          print rcs, dPhiCut
          res = rcs['rCS']
          resErrPred = rcs['rCSE_pred']
          resErr = rcs['rCSE_sim']
          #res, resErr = getRCS(c, cut,  dPhiCut)
          h_nbj[name][stb][htb][bjb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
          if not math.isnan(res):
            h_nbj[name][stb][htb][bjb].SetBinContent(i_njb+1, res)
            h_nbj[name][stb][htb][bjb].SetBinError(i_njb+1, resErr) #maybe should be changed to predicted error (estimated error for poisson distributed values)


correctionFactors = {}

for name, c in [["tt", cTTJets] , ["W",cWJets] ]:
  correctionFactors[name] = {}
  for stb in regions:
    correctionFactors[name][stb] = {}
    for i_htb, htb in enumerate(regions[stb]):
      correctionFactors[name][stb][htb] = {}
      c1 = ROOT.TCanvas('c1','c1',600,600)
      pad1 = ROOT.TPad('Pad','Pad',0.,0.0,1.,1.)
      pad1.SetLeftMargin(0.15)
      pad1.Draw()
      pad1.cd()
      first = True
      l = ROOT.TLegend(0.6,0.65,0.9,0.78)#right aligned legend
      l.SetFillColor(ROOT.kWhite)
      l.SetShadowColor(ROOT.kWhite)
      l.SetBorderSize(0)
      FitParList = {}
      FitParErrorList = {}
      for inbb, nbb in enumerate(reversed(nbjreg)):
        h_nbj[name][stb][htb][nbb].GetXaxis().SetLabelSize(0.06)
        h_nbj[name][stb][htb][nbb].GetYaxis().SetLabelSize(0.04)
        h_nbj[name][stb][htb][nbb].GetYaxis().SetTitleSize(0.04)
        h_nbj[name][stb][htb][nbb].GetYaxis().SetTitleOffset(1.5)
        h_nbj[name][stb][htb][nbb].GetYaxis().SetTitle('R_{CS}')
        h_nbj[name][stb][htb][nbb].SetLineColor(ROOT_colors[inbb])
        h_nbj[name][stb][htb][nbb].SetLineWidth(2)
        l.AddEntry(h_nbj[name][stb][htb][nbb], nBTagBinName(nbb))
        text=ROOT.TLatex()
        text.SetNDC()
        text.SetTextSize(0.04)
        text.SetTextAlign(11)
        text.DrawLatex(0.3,0.85,name+'+jets')
        text.DrawLatex(0.6,0.85,varBinName(htb, 'H_{T}'))
        text.DrawLatex(0.6,0.8,varBinName(stb, 'S_{T}'))
        if name == 'tt':
          h_nbj[name][stb][htb][nbb].SetMaximum(0.25)
          lowerFitBound = 2
          upperFitBound = 6
        elif name == 'W':
          h_nbj[name][stb][htb][nbb].SetMaximum(0.15)
          lowerFitBound = 0
          upperFitBound = 6
        h_nbj[name][stb][htb][nbb].Fit('pol0','','same',lowerFitBound,upperFitBound)
        FitFunc     = h_nbj[name][stb][htb][nbb].GetFunction('pol0')
        FitPar      = FitFunc.GetParameter(0)
        FitParError = FitFunc.GetParError(0)
        FitFunc.SetLineColor(ROOT_colors[inbb])
        FitFunc.SetLineStyle(2)
        FitFunc.SetLineWidth(2)
        FitParList.update({nbb:FitPar})
        FitParErrorList.update({nbb:FitParError})
        if first:
          first = False
          h_nbj[name][stb][htb][nbb].Draw()
        else:
          h_nbj[name][stb][htb][nbb].Draw('same')
        correctionFactors[name][stb][htb][nbb] = {'FitPar':FitPar, 'FitParError':FitParError}
        FitFunc.Draw("same")
      FitRatio = FitParList[(0,0)]/FitParList[(1,1)]
      FitRatioError = FitRatio*sqrt((FitParErrorList[(0,0)]/FitParList[(0,0)])**2+(FitParErrorList[(1,1)]/FitParList[(1,1)])**2)
      correctionFactors[name][stb][htb].update({'FitRatio':FitRatio, 'FitRatioError':FitRatioError})
      Etext=ROOT.TLatex()
      Etext.SetNDC()
      Etext.SetTextSize(0.04)
      Etext.SetTextAlign(11)
      Etext.DrawLatex(0.18,0.75,'Fit(0b/1b)='+str(round(FitRatio,3))+'#pm'+str(round(FitRatioError,4)))
      l.Draw()
      c1.Print(path+prefix+'_rCS_nbjet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".pdf")
      c1.Print(path+prefix+'_rCS_nbjet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".png")
      c1.Print(path+prefix+'_rCS_nbjet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=None, btb=btreg, presel=presel)[0]+".root")


rowsSt = {}
rows = 0
for stb in sorted(regions):
  rows += len(regions[stb])
  rowsSt[stb] = {'n':len(regions[stb])}
rowsNJet = {'nST':len(regions), 'n':rows}

print "Results"
print
print '\\begin{table}[ht]\\begin{center}\\begin{tabular}{|c|c|rrr|}\\hline'
print ' \ST & \HT     &\multicolumn{3}{c|}{$\kappa_{CS}$}\\\%\hline'
print ' $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c|}{0b/1b}\\\ '

for stb in sorted(regions):
  print '\\hline'
  print '\multirow{'+str(rowsSt[stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
  for htb in sorted(regions[stb]):
    print '&$'+varBin(htb)+'$'
    print ' & '+getNumString(correctionFactors['tt'][stb][htb]['FitRatio'], correctionFactors['tt'][stb][htb]['FitRatioError'])+'\\\\ '
print '\\hline\end{tabular}\end{center}\caption{Correction factors for \\ttJets background, 3$fb^{-1}$}\label{tab:0b_rcscorr_Wbkg}\end{table}'

pickle.dump(correctionFactors, file(picklePath+'correction_pkl','w'))
print "correction pkl written here :" , picklePath+'correction_pkl'
