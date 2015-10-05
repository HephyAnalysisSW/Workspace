import ROOT
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain

#from Workspace.RA4Analysis.cmgTuplesPostProcessed_Spring15_hard import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *

from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin
from rCShelpers import *
import math
import pickle
from Workspace.RA4Analysis.signalRegions import *

small = False
maxN = -1 if not small else 1

lepSel = 'hard'

#cWJets  = getChain(WJetsHTToLNu[lepSel],histname='',maxN=maxN)
#cTTJets = getChain(ttJets[lepSel],histname='',maxN=maxN)
#cEWK = getChain([WJetsHTToLNu[lepSel],ttJets[lepSel],singleTop[lepSel]],histname='')

cWJets  = getChain(WJetsHTToLNu_25ns,histname='',maxN=maxN)
cTTJets = getChain(TTJets_LO_25ns,histname='',maxN=maxN)
cEWK = getChain([WJetsHTToLNu_25ns,TTJets_LO_25ns,DY_25ns,singleTop_25ns],histname='')

from Workspace.HEPHYPythonTools.user import username
uDir = username[0]+'/'+username
subDir = 'Spring15/rCS/25ns/rCS/btagFitMoreBins/'

### DEFINE SR
signalRegions = signalRegion3fb

path = '/afs/hephy.at/user/'+uDir+'/www/'+subDir+'/'
if not os.path.exists(path):
  os.makedirs(path)

picklePath = '/data/'+username+'/Spring15/25ns/rCS_0b_3.0/'
if not os.path.exists(picklePath):
  os.makedirs(picklePath)

ROOT_colors = [ROOT.kBlack, ROOT.kRed-7, ROOT.kAzure-1, ROOT.kGreen+3, ROOT.kOrange+1,ROOT.kRed-3, ROOT.kAzure+6, ROOT.kCyan+3, ROOT.kOrange , ROOT.kRed-10]
dPhiStr = 'deltaPhi_Wl'
#no stat box
ROOT.gStyle.SetOptStat(0)

ROOT.TH1F().SetDefaultSumw2()

btreg = (0,0)
njreg = [(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,-1)]#,(7,7),(8,8),(9,9)]
nbjreg = [(0,0),(1,1)]#,(2,2)]


#presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&Flag_EcalDeadCellTriggerPrimitiveFilter&&acos(cos(Jet_phi[0]-met_phi))>0.45&&acos(cos(Jet_phi[1]-met_phi))>0.45'
presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80'

#presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80'
prefix = presel.split('&&')[0]+'_'

#samples = [["tt", cTTJets] , ["W",cWJets]]
samples = [["tt",cTTJets]]

h_nbj = {}
for name, c in samples:
  print
  print name
  h_nbj[name] = {}
  for srNJet in sorted(signalRegions):
    h_nbj[name][srNJet] = {}
    for stb in sorted(signalRegions[srNJet]):
      h_nbj[name][srNJet][stb] = {}
      for htb in sorted(signalRegions[srNJet][stb]):
        h_nbj[name][srNJet][stb][htb] = {}
        dPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
        print '                   njets     ST      HT'
        print 'Rcs values for SR:', srNJet, stb, htb
        for i_nbjb, bjb in enumerate(nbjreg):
          h_nbj[name][srNJet][stb][htb][bjb] = ROOT.TH1F("rcs_nbj","",len(njreg),0,len(njreg))
          for i_njb, njb in enumerate(njreg):
            cname, cut = nameAndCut(stb,htb,njb, btb=bjb ,presel=presel)
            if bjb == (1,1):
              rcs = getRCS(cEWK, cut, dPhiCut)
            else:
              rcs = getRCS(c, cut, dPhiCut)
            print 'nbjet, njet, deltaPhiCut:', bjb, njb, dPhiCut
            print rcs
            res = rcs['rCS']
            resErrPred = rcs['rCSE_pred']
            resErr = rcs['rCSE_sim']
            #res, resErr = getRCS(c, cut,  dPhiCut)
            h_nbj[name][srNJet][stb][htb][bjb].GetXaxis().SetBinLabel(i_njb+1, nJetBinName(njb))
            if not math.isnan(res):
              h_nbj[name][srNJet][stb][htb][bjb].SetBinContent(i_njb+1, res)
              h_nbj[name][srNJet][stb][htb][bjb].SetBinError(i_njb+1, resErr)

correctionFactors = {}

for name, c in samples:
  correctionFactors[name] = {}
  for srNJet in sorted(signalRegions):
    correctionFactors[name][srNJet] = {}
    for stb in sorted(signalRegions[srNJet]):
      correctionFactors[name][srNJet][stb] = {}
      for i_htb, htb in enumerate(signalRegions[srNJet][stb]):
        correctionFactors[name][srNJet][stb][htb] = {}
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
          h_nbj[name][srNJet][stb][htb][nbb].GetXaxis().SetLabelSize(0.06)
          h_nbj[name][srNJet][stb][htb][nbb].GetYaxis().SetLabelSize(0.04)
          h_nbj[name][srNJet][stb][htb][nbb].GetYaxis().SetTitleSize(0.04)
          h_nbj[name][srNJet][stb][htb][nbb].GetYaxis().SetTitleOffset(1.5)
          h_nbj[name][srNJet][stb][htb][nbb].GetYaxis().SetTitle('R_{CS}')
          h_nbj[name][srNJet][stb][htb][nbb].SetLineColor(ROOT_colors[inbb])
          h_nbj[name][srNJet][stb][htb][nbb].SetLineWidth(2)
          l.AddEntry(h_nbj[name][srNJet][stb][htb][nbb], nBTagBinName(nbb))
          text=ROOT.TLatex()
          text.SetNDC()
          text.SetTextSize(0.04)
          text.SetTextAlign(11)
          text.DrawLatex(0.3,0.85,name+'+jets')
          text.DrawLatex(0.6,0.85,varBinName(htb, 'H_{T}'))
          text.DrawLatex(0.6,0.8,varBinName(stb, 'L_{T}'))
          h_nbj[name][srNJet][stb][htb][nbb].SetMinimum(0.)
          if name == 'tt':
            h_nbj[name][srNJet][stb][htb][nbb].SetMaximum(0.25)
            lowerFitBound = 1
            upperFitBound = 7
          elif name == 'W':
            h_nbj[name][srNJet][stb][htb][nbb].SetMaximum(0.15)
            lowerFitBound = 0
            upperFitBound = 7
          for a in range(lowerFitBound+1,upperFitBound+1):
            if h_nbj[name][srNJet][stb][htb][nbb].GetBinContent(a)<=0.:
              upperFitBound = a-1
              break
          h_nbj[name][srNJet][stb][htb][nbb].Fit('pol0','','same',lowerFitBound,upperFitBound)
          FitFunc     = h_nbj[name][srNJet][stb][htb][nbb].GetFunction('pol0')
          FitPar      = FitFunc.GetParameter(0)
          FitParError = FitFunc.GetParError(0)
          FitFunc.SetLineColor(ROOT_colors[inbb])
          FitFunc.SetLineStyle(2)
          FitFunc.SetLineWidth(2)
          FitParList.update({nbb:FitPar})
          FitParErrorList.update({nbb:FitParError})
          if first:
            first = False
            h_nbj[name][srNJet][stb][htb][nbb].Draw()
          else:
            h_nbj[name][srNJet][stb][htb][nbb].Draw('same')
          correctionFactors[name][srNJet][stb][htb][nbb] = {'FitPar':FitPar, 'FitParError':FitParError}
          FitFunc.Draw("same")
        FitRatio = FitParList[(0,0)]/FitParList[(1,1)]
        FitRatioError = FitRatio*sqrt((FitParErrorList[(0,0)]/FitParList[(0,0)])**2+(FitParErrorList[(1,1)]/FitParList[(1,1)])**2)
        correctionFactors[name][srNJet][stb][htb].update({'FitRatio':FitRatio, 'FitRatioError':FitRatioError})
        Etext=ROOT.TLatex()
        Etext.SetNDC()
        Etext.SetTextSize(0.04)
        Etext.SetTextAlign(11)
        Etext.DrawLatex(0.18,0.75,'Fit(0b/1b)='+str(round(FitRatio,3))+'#pm'+str(round(FitRatioError,4)))
        l.Draw()
        c1.Print(path+prefix+'_rCS_nbjet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=srNJet, btb=btreg, presel=presel)[0]+".pdf")
        c1.Print(path+prefix+'_rCS_nbjet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=srNJet, btb=btreg, presel=presel)[0]+".png")
        c1.Print(path+prefix+'_rCS_nbjet_'+name+'_'+nameAndCut(stb,htb=htb,njetb=srNJet, btb=btreg, presel=presel)[0]+".root")


rowsNJet = {}
rowsSt = {}
for srNJet in sorted(signalRegions):
  rowsNJet[srNJet] = {}
  rowsSt[srNJet] = {}
  rows = 0
  for stb in sorted(signalRegions[srNJet]):
    rows += len(signalRegions[srNJet][stb])
    rowsSt[srNJet][stb] = {'n':len(signalRegions[srNJet][stb])}
  rowsNJet[srNJet] = {'nST':len(signalRegions[srNJet]), 'n':rows}

print "Results"
print
print '\\begin{table}[ht]\\begin{center}\\begin{tabular}{|c|c|c|rrr|}\\hline'
print ' \\njet & \ST & \HT     &\multicolumn{3}{c|}{$\kappa_{CS}$}\\\%\hline'
print ' & $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c|}{0b/1b}\\\ '

secondLine = False
for srNJet in sorted(signalRegions):
  print '\\hline'
  if secondLine: print '\\hline'
  secondLine = True
  print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
  for stb in sorted(signalRegions[srNJet]):
    print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
    first = True
    for htb in sorted(signalRegions[srNJet][stb]):
      if not first: print '&'
      first = False
      print '&$'+varBin(htb)+'$'
      print ' & '+getNumString(correctionFactors['tt'][srNJet][stb][htb]['FitRatio'], correctionFactors['tt'][srNJet][stb][htb]['FitRatioError'])+'\\\\ '
print '\\hline\end{tabular}\end{center}\caption{Correction factors for \\ttJets background, 3$fb^{-1}$}\label{tab:0b_rcscorr_Wbkg}\end{table}'
print

pickle.dump(correctionFactors, file(picklePath+'correction_pkl','w'))
print "correction pkl written here :" , picklePath+'correction_pkl'
