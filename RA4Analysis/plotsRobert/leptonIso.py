import ROOT
import pickle
from array import array
from objectSelection import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import getVarValue, getObjFromFile, findClosestObjectDR
from objectSelection import getLooseMuStage2, tightPOGMuID, vetoMuID, getGoodJetsStage2
from stage2Tuples import *
from math import sqrt, cos, sin, atan2

presel = 'ht>400&&met>150&&nmuCount>0'
small = True

sample = ttJetsCSA1450ns
prefix=''

c = ROOT.TChain('Events')
for b in sample['bins']:
  files=os.listdir(sample['dirname']+'/'+b)
  for f in files:
    if not 'small' in f:
      c.Add(sample['dirname']+'/'+b+'/'+f)

c.Draw("","abs(gLepPdg)==13&&gLepPt>15&&"+presel)

#c.Draw(">>eList", presel)
#eList = ROOT.gDirectory.Get("eList")
#number_events = eList.GetN()
#maxN=100000
#if small:
#  if number_events>maxN:
#    number_events=maxN
#number_events=min(number_events, eList.GetN())
#countLeptons=0
#dRTight = ROOT.TH1F('dR','dR',100,0,1)
#dRLoose = ROOT.TH1F('dR','dR',100,0,1)
#ptRatioTight = ROOT.TH1F('ptRatio','lep/jet',100,0,2)
#ptRatioLoose = ROOT.TH1F('ptRatio','lep/jet',100,0,2)
#muefNearTight = ROOT.TH1F('muef','muef',100,0,2)
#muefNearLoose = ROOT.TH1F('muef','muef',100,0,2)
#muefFarTight = ROOT.TH1F('muef','muef',100,0,2)
#muefFarLoose = ROOT.TH1F('muef','muef',100,0,2)
#for i in range(number_events):
#  if (i%10000 == 0) and i>0 :
#    print i,"/",number_events
#  c.GetEntry(eList.GetEntry(i))
#  jets = getGoodJetsStage2(c)
#  nmuCount = int(getVarValue(c, 'nmuCount' ))
#  for i in range(nmuCount):
#    l=getLooseMuStage2(c, i)
#    if vetoMuID(l) and l['pt']>30:
#      closestJet = findClosestObjectDR(jets, l)
#      jet = closestJet['obj']
#      dRLoose.Fill(closestJet['deltaR'])
#      if closestJet['deltaR']<0.4:
#        ptRatioLoose.Fill(l['pt']/jet['pt'])
#        muefNearLoose.Fill(jet['muef'])
#      else:
#        muefFarLoose.Fill(jet['muef'])
#      if tightPOGMuID(l):
#        dRTight.Fill(closestJet['deltaR'])
#        if closestJet['deltaR']<0.4:
#          ptRatioTight.Fill(l['pt']/jet['pt'])
#          muefNearTight.Fill(jet['muef'])
#        else:
#          muefFarTight.Fill(jet['muef'])
#c1=ROOT.TCanvas()
#c1.SetLogy()
#dRLoose.SetLineColor(ROOT.kRed)
#dRLoose.Draw()
#dRTight.Draw('same')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/dR_'+prefix+'.png')
#ptRatioLoose.SetLineColor(ROOT.kRed)
#ptRatioLoose.Draw()
#ptRatioTight.Draw('same')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/ptRatio_'+prefix+'.png')
#muefNearLoose.SetLineColor(ROOT.kRed)
#muefNearLoose.Draw()
#muefNearTight.Draw('same')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muefNear_'+prefix+'.png')
#muefFarLoose.SetLineColor(ROOT.kRed)
#muefFarLoose.Draw()
#muefFarTight.Draw('same')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/muefFar_'+prefix+'.png')
