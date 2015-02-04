import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()
def getRCS(c, cut, dPhiCut):
  h = getPlotFromChain(c, "acos((leptonPt+met*cos(leptonPhi-metPhi))/sqrt(leptonPt**2+met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))", [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True)
  if h.GetBinContent(1)>0 and h.GetBinContent(2)>0:
    rcs = h.GetBinContent(2)/h.GetBinContent(1)
    rcsE = rcs*sqrt(h.GetBinError(2)**2/h.GetBinContent(2)**2 + h.GetBinError(1)**2/h.GetBinContent(1)**2)
    del h
    return rcs, rcsE
  del h
  return None, None


#ROOT.TH1F().SetDefaultSumw2()
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks
import Workspace.HEPHYPythonTools.xsec as xsec
#from Workspace.RA4Analysis.simplePlotsCommon import *
from Workspace.RA4Analysis.helpers import *

from Workspace.RA4Analysis.cmgTuplesPostProcessed_v5_Phys14V2 import *
c = getChain(ttJets['hard'],histname='') 
presel="singleMuonic&&nLooseSoftPt10Leptons==0&&nTightHardLeptons==1&&nLooseHardLeptons==1&&htJet40ja>500&&htJet40ja<750&&nJet40a>=4&&nJet40a<=5&&st>250&&st<350"
prefix = '4-5j_ht500-750_st250-350'
#prefix = '4j_ht500'

plots = [ \
    ['acos((leptonPt + met*cos(leptonPhi - metPhi))/sqrt(leptonPt**2 + met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))', [16,0,3.2], 'dphi'],
    ['met_pt', [30,0,800], "met"],
    ]

for var, binning, name in plots:
  c.Draw(var+'>>h_0_'+name+'('+','.join([str(x) for x in binning])+')', presel+"&&nBJetMedium25==0","goff")
  c.Draw(var+'>>h_1_'+name+'('+','.join([str(x) for x in binning])+')', presel+"&&nBJetMedium25==1","goff")
  c.Draw(var+'>>h_2_'+name+'('+','.join([str(x) for x in binning])+')', presel+"&&nBJetMedium25>1","goff")

  h_0=ROOT.gDirectory.Get("h_0_"+name)
  h_1=ROOT.gDirectory.Get("h_1_"+name)
  h_2=ROOT.gDirectory.Get("h_2_"+name)
  h_0.SetLineColor(ROOT.kBlack)
  h_1.SetLineColor(ROOT.kBlue)
  h_2.SetLineColor(ROOT.kRed)

  c1 = ROOT.TCanvas()
  h_2.Scale(h_0.Integral()/h_2.Integral())
  h_2.Draw()
  c1.SetLogy()
  h_1.Scale(h_0.Integral()/h_1.Integral())
  h_1.Draw("same")
  h_0.Draw("same")
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCMG/'+prefix+'_'+name+'.png')
