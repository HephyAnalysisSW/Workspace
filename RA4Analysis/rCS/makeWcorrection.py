import ROOT
import os,sys
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain

#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
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

cWJets  = getChain(WJetsHTToLNu_25ns,histname='',maxN=maxN)

from Workspace.HEPHYPythonTools.user import username
uDir = username[0]+'/'+username
subDir = 'Spring15/rCS/25ns/rCS_WjetfitNoCorr/'

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
#njreg = [(2,3),(4,4),(5,5),(6,7),(8,-1)]
njreg = [(3,4),(5,5),(6,7),(8,-1)]

#presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&Flag_EcalDeadCellTriggerPrimitiveFilter&&acos(cos(Jet_phi[0]-met_phi))>0.45&&acos(cos(Jet_phi[1]-met_phi))>0.45'
presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80'
prefix = presel.split('&&')[0]+'_'

h_nj = {}
h_nj_pos = {}
h_nj_neg = {}

rcsDict = {}
rcsDict_pos = {}
rcsDict_neg = {}

for srNJet in sorted(signalRegions):
  h_nj[srNJet] = {}
  h_nj_pos[srNJet] = {}
  h_nj_neg[srNJet] = {}
  rcsDict[srNJet] = {}
  rcsDict_pos[srNJet] = {}
  rcsDict_neg[srNJet] = {}
  for stb in sorted(signalRegions[srNJet]):
    h_nj[srNJet][stb] = {}
    h_nj_pos[srNJet][stb] = {}
    h_nj_neg[srNJet][stb] = {}
    rcsDict[srNJet][stb] = {}
    rcsDict_pos[srNJet][stb] = {}
    rcsDict_neg[srNJet][stb] = {}
    for htb in sorted(signalRegions[srNJet][stb]):
      h_nj[srNJet][stb][htb] = ROOT.TH1F("rcs_nj","",len(njreg),0,len(njreg))
      h_nj_pos[srNJet][stb][htb] = ROOT.TH1F("rcs_nj_pos","",len(njreg),0,len(njreg))
      h_nj_neg[srNJet][stb][htb] = ROOT.TH1F("rcs_nj_neg","",len(njreg),0,len(njreg))
      dPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
      rcsDict[srNJet][stb][htb] = {'deltaPhi':dPhiCut}
      rcsDict_pos[srNJet][stb][htb] = {'deltaPhi':dPhiCut}
      rcsDict_neg[srNJet][stb][htb] = {'deltaPhi':dPhiCut}
      for i_njb, njb in enumerate(njreg):
        cname, cut = nameAndCut(stb,htb,njb, btb=btreg ,presel=presel)
        rcs = getRCS(cWJets, cut, dPhiCut)
        rcs_pos = getRCS(cWJets, cut+'&&leptonPdg>0', dPhiCut)
        rcs_neg = getRCS(cWJets, cut+'&&leptonPdg<0', dPhiCut)
        print rcs, dPhiCut
        rcsDict[srNJet][stb][htb][njb] = rcs
        rcsDict_pos[srNJet][stb][htb][njb] = rcs_pos
        rcsDict_neg[srNJet][stb][htb][njb] = rcs_neg
        if not math.isnan(rcs['rCS']):
          if rcs['rCS']>0.:
            h_nj[srNJet][stb][htb].SetBinContent(i_njb+1,rcs['rCS'])
            h_nj[srNJet][stb][htb].SetBinError(i_njb+1,rcs['rCSE_sim'])
        if not math.isnan(rcs_pos['rCS']):
          if rcs_pos['rCS']>0.:
            h_nj_pos[srNJet][stb][htb].SetBinContent(i_njb+1,rcs_pos['rCS'])
            h_nj_pos[srNJet][stb][htb].SetBinError(i_njb+1,rcs_pos['rCSE_sim'])
        if not math.isnan(rcs_neg['rCS']):
          if rcs_neg['rCS']>0.:
            h_nj_neg[srNJet][stb][htb].SetBinContent(i_njb+1,rcs_neg['rCS'])
            h_nj_neg[srNJet][stb][htb].SetBinError(i_njb+1,rcs_neg['rCSE_sim'])
        
for srNJet in sorted(signalRegions):
  for stb in sorted(signalRegions[srNJet]):
    for htb in sorted(signalRegions[srNJet][stb]):
      upperbound = 0
      for i_njb, njb in enumerate(njreg):
        if h_nj[srNJet][stb][htb].GetBinContent(i_njb+1)>0.:
          upperbound = i_njb+1
        else:
          break
      h_nj[srNJet][stb][htb].Fit('pol1','','same',0,upperbound)
      FitFunc     = h_nj[srNJet][stb][htb].GetFunction('pol1')
      FitParD     = FitFunc.GetParameter(0)
      FitParDError = FitFunc.GetParError(0)
      FitParK = FitFunc.GetParameter(1)
      FitParKError = FitFunc.GetParError(1)
      rcsDict[srNJet][stb][htb].update({'D':FitParD, 'DErr':FitParDError, 'K':FitParK, 'Kerr':FitParKError})
      
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
      h_nj[srNJet][stb][htb].SetMaximum(0.08)
      h_nj[srNJet][stb][htb].SetMinimum(0.)
      h_nj[srNJet][stb][htb].GetXaxis().SetLabelSize(0.04)
      h_nj[srNJet][stb][htb].GetYaxis().SetLabelSize(0.04)
      h_nj[srNJet][stb][htb].GetYaxis().SetTitleSize(0.04)
      h_nj[srNJet][stb][htb].GetYaxis().SetTitleOffset(1.5)
      h_nj[srNJet][stb][htb].GetYaxis().SetTitle('R_{CS}')
      if first:
        first = False
        h_nj[srNJet][stb][htb].Draw()
      else:
        h_nj[srNJet][stb][htb].Draw('same')
      FitFunc.Draw("same")
      c1.Print(path+prefix+'_rCS_njet_'+nameAndCut(stb,htb=htb,njetb=srNJet, btb=btreg, presel=presel)[0]+".pdf")
      c1.Print(path+prefix+'_rCS_njet_'+nameAndCut(stb,htb=htb,njetb=srNJet, btb=btreg, presel=presel)[0]+".png")
      c1.Print(path+prefix+'_rCS_njet_'+nameAndCut(stb,htb=htb,njetb=srNJet, btb=btreg, presel=presel)[0]+".root")
      
      upperbound = 0
      for i_njb, njb in enumerate(njreg):
        if h_nj_pos[srNJet][stb][htb].GetBinContent(i_njb+1)>0.:
          upperbound = i_njb+1
        else:
          break
      h_nj_pos[srNJet][stb][htb].Fit('pol1','','same',0,upperbound)
      FitFunc     = h_nj_pos[srNJet][stb][htb].GetFunction('pol1')
      FitParD     = FitFunc.GetParameter(0)
      FitParDError = FitFunc.GetParError(0)
      FitParK = FitFunc.GetParameter(1)
      FitParKError = FitFunc.GetParError(1)
      rcsDict_pos[srNJet][stb][htb].update({'D':FitParD, 'DErr':FitParDError, 'K':FitParK, 'Kerr':FitParKError})

      upperbound = 0
      for i_njb, njb in enumerate(njreg):
        if h_nj_neg[srNJet][stb][htb].GetBinContent(i_njb+1)>0.:
          upperbound = i_njb+1
        else:
          break
      h_nj_neg[srNJet][stb][htb].Fit('pol1','','same',0,upperbound)
      FitFunc     = h_nj_neg[srNJet][stb][htb].GetFunction('pol1')
      FitParD     = FitFunc.GetParameter(0)
      FitParDError = FitFunc.GetParError(0)
      FitParK = FitFunc.GetParameter(1)
      FitParKError = FitFunc.GetParError(1)
      rcsDict_neg[srNJet][stb][htb].update({'D':FitParD, 'DErr':FitParDError, 'K':FitParK, 'Kerr':FitParKError})


pickle.dump(rcsDict_pos, file(picklePath+'correction_Wrcs_PosPdg_pkl','w'))
pickle.dump(rcsDict_neg, file(picklePath+'correction_Wrcs_NegPdg_pkl','w'))
pickle.dump(rcsDict, file(picklePath+'correction_Wrcs_pkl','w'))

