import ROOT
import pickle
from array import array
##from helpers import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import getVarValue
from objectSelection import getLooseMuStage2, tightPOGMuID, vetoMuID
from stage2Tuples import ttJetsCSA14
from math import sqrt, cos, sin, atan2

htCut     = 400
metCut    = 150
minNJets  =   4

c = ROOT.TChain('Events')
for b in ttJetsCSA14['bins']:
  c.Add(ttJetsCSA14['dirname']+'/'+b+'/h*.root')

#small = False
#maxN=1001

doubleLeptonPreselection = "ngoodMuons>=1&&nvetoMuons==2"

ofile =                      '/data/schoef/results2014/tauTuples/CSA14_TTJets_genTau.root'

hMT = ROOT.TH1F('hMT', 'hMT',40,0,800)

c.Draw(">>eList", doubleLeptonPreselection)

c.Draw('sqrt(2.*met*leptonPt*(1-cos(leptonPhi-metphi)))>>hMT','weight*(''ht>'+str(htCut)+'&&njets>='+str(minNJets)+'&&met>'+str(metCut)+')')
#c.Draw('sqrt(2.*met*leptonPt*(1-cos(leptonPhi-metphi)))>>hMT')

##cPred = ROOT.TChain('Events')
#hMTPred = ROOT.TH1F('hMTPred', 'hMTPred',40,0,800)
##cPred.Add('/data/schoef/results2014/tauTuples/CSA14_TTJets_genTau.root')
##cPred.Draw('mTPred>>hMTPred','weight*(htPred>'+str(htCut)+'&&njetsPred>='+str(minNJets)+'&&metPred>'+str(metCut)+')','goff')
can = ROOT.TCanvas()
hMT.Draw()
##hMTPred.SetLineColor(ROOT.kRed)
##hMTPred.Draw('same')
can.Print()
