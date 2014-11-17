import ROOT
import pickle
from Workspace.RA4Analysis.stage2Tuples import ttJetsCSA1450ns #, ttJetsCSA1425ns
from array import array
from localInfo import username
import os, sys

c = ROOT.TChain('Events')
#for b in ttJetsCSA1450ns['bins']:
#  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/histo_ttJetsCSA1450ns_from*.root')
#c.Add('/data/schoef/convertedTuples_v25/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
#c.Add('/data/schoef/convertedTuples_v24/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
c.Add('/data/schoef/convertedTuples_v26/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
Lepton = {'muon':True,'electron': False, 'tau': False}

ROOT.gStyle.SetOptStat(0)

ptBins  = array('d', [float(x) for x in range(10, 20)+range(20,50,3)+range(50,100,10)+range(100,310,30)])
etaBins = array('d', [float(x)/10. for x in range(-30,32,2)])

ptBinsCoarse  = array('d', [float(x) for x in range(10, 20)+range(20,50,5)+range(50,100,20)+range(100,310,50)])
etaBinsCoarse = array('d', [float(x)/10. for x in [-30,-25]+range(-21,22,6)+[25,30]])


#hadPresel="ht>150&&njets>=3"    ##Met condition removed because for prediction I need Met<150 also.   
hadPresel=""    ##Met condition removed because for prediction I need Met<150 also.   
diLepSelection ="ngNuMuFromW==2&&ngNuEFromW==0"
#for relIso in [0.2,0.1,0.15,0.25,0.3,0.35]:
for relIso in [0.3]:
  ptCut=15
  leptonID = "muIsPF[gLepInd]&&(muIsGlobal[gLepInd]||muIsTracker[gLepInd])&&muPt[gLepInd]>"+str(ptCut)+"&&abs(muEta[gLepInd])<2.5"\
            +"&&abs(muDxy[gLepInd])<0.2&&abs(muDz[gLepInd])<0.5"\
            +"&&muRelIso[gLepInd]<"+str(relIso)
  prefix = 'vetoMuIDPt15_ttJetsCSA1450ns_v26_relIso'+str(relIso)
  print 'It is ok I am in the for statement'
  ##hybridLoose
  #ptCut=15
  #leptonID = "muIsPF[gLepInd]&&(muIsGlobal[gLepInd]||muIsTracker[gLepInd])&&muPt[gLepInd]>"+str(ptCut)+"&&abs(muEta[gLepInd])<2.1&&muRelIso[gLepInd]<0.2&&abs(muDxy[gLepInd])<0.02&&abs(muDz[gLepInd])<0.5"
  #prefix = 'vetoMuIDPt15'

  muPtPresEff = ROOT.TProfile('muPtPresEff','muPtPresEff', len(ptBins)-1,ptBins,-2,2)
  c.Draw('gLepInd>=0:gLepPt>>muPtPresEff','abs(gLepPdg)==13&&gLepPt>'+str(ptCut)+"&&abs(gLepEta)<2.5&&"+hadPresel+diLepSelection, 'goff')
  muPtIDEff = ROOT.TProfile('muPtIDEff','muPtIDEff', len(ptBins)-1,ptBins,-2,2)
  c.Draw('gLepDR<0.4&&abs(1-muPt[gLepInd]/gLepPt)<0.05&&'+leptonID+':gLepPt>>muPtIDEff','abs(gLepPdg)==13&&gLepPt>'+str(ptCut)+'&&abs(gLepEta)<2.5&&gLepInd>=0'+"&&"+hadPresel+diLepSelection, 'goff')
  muPtIDEff=muPtIDEff.ProjectionX()
  muPtIDEff.Multiply(muPtPresEff.ProjectionX())

  muEtaPresEff = ROOT.TProfile('muEtaPresEff','muEtaPresEff', len(etaBins)-1,etaBins,-2,2)
  c.Draw('gLepInd>=0:gLepEta>>muEtaPresEff','abs(gLepPdg)==13&&gLepPt>'+str(ptCut)+"&&"+hadPresel+diLepSelection, 'goff')
  muEtaIDEff = ROOT.TProfile('muEtaIDEff','muEtaIDEff', len(etaBins)-1,etaBins,-2,2)
  c.Draw('gLepDR<0.4&&abs(1-muPt[gLepInd]/gLepPt)<0.05&&'+leptonID+':gLepEta>>muEtaIDEff','abs(gLepPdg)==13&&gLepPt>'+str(ptCut)+'&&gLepInd>=0'+"&&"+hadPresel+diLepSelection, 'goff')
  muEtaIDEff=muEtaIDEff.ProjectionX()
  muEtaIDEff.Multiply(muEtaPresEff.ProjectionX())

  munVtxPresEff = ROOT.TProfile('munVtxPresEff','munVtxPresEff', 50,0,50,-2,2)
  c.Draw('gLepInd>=0:ngoodVertices>>munVtxPresEff','abs(gLepPdg)==13&&gLepPt>'+str(ptCut)+"&&abs(gLepEta)<2.5&&"+hadPresel+diLepSelection, 'goff')
  munVtxIDEff = ROOT.TProfile('munVtxIDEff','munVtxIDEff', 50,0,50,-2,2)
  c.Draw('gLepDR<0.4&&abs(1-muPt[gLepInd]/gLepPt)<0.05&&'+leptonID+':ngoodVertices>>munVtxIDEff','abs(gLepPdg)==13&&gLepPt>'+str(ptCut)+'&&abs(gLepEta)<2.5&&gLepInd>=0'+"&&"+hadPresel+diLepSelection, 'goff')
  munVtxIDEff=munVtxIDEff.ProjectionX()
  munVtxIDEff.Multiply(munVtxPresEff.ProjectionX())

  muPtEta2DPresEff = ROOT.TProfile2D('muPtEta2DPresEff','muPtEta2DPresEff',len(ptBinsCoarse)-1,ptBinsCoarse, len(etaBinsCoarse)-1,etaBinsCoarse)
  c.Draw('gLepInd>=0:gLepEta:gLepPt>>muPtEta2DPresEff','abs(gLepPdg)==13&&gLepPt>'+str(ptCut)+"&&"+hadPresel+diLepSelection, 'goff')
  muPtEta2DEff = ROOT.TProfile2D('muPtEta2DEff','muPtEta2DEff',len(ptBinsCoarse)-1,ptBinsCoarse, len(etaBinsCoarse)-1,etaBinsCoarse)
  c.Draw('gLepDR<0.4&&abs(1-muPt[gLepInd]/gLepPt)<0.05&&'+leptonID+':gLepEta:gLepPt>>muPtEta2DEff','abs(gLepPdg)==13&&gLepPt>'+str(ptCut)+'&&abs(gLepEta)<2.5&&gLepInd>=0'+"&&"+hadPresel+diLepSelection, 'goff')
  muPtEta2DEff=muPtEta2DEff.ProjectionXY()
  muPtEta2DEff.Multiply(muPtEta2DPresEff.ProjectionXY())

  PngPath = '/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/'
  if not os.path.exists(PngPath):
    os.makedirs(PngPath)
    
  c1 = ROOT.TCanvas()
  muPtIDEff.Draw()
  c1.Print(PngPath+'muPtIDEff_'+prefix+'.png')
#  muPtPresEff.Draw()
#  c1.Print(PngPath+'muPtPresEff_'+prefix+'.png')
  muEtaIDEff.Draw()
  c1.Print(PngPath+'muEtaIDEff_'+prefix+'.png')
#  muEtaPresEff.Draw()
#  c1.Print(PngPath+'muEtaPresEff_'+prefix+'.png')
  munVtxIDEff.Draw()
  c1.Print(PngPath+'munVtxIDEff_'+prefix+'.png')
#  munVtxPresEff.Draw()
#  c1.Print('/afs/hephy.at/user/s/'+username+'/www/pngCSA14/munVtxPresEff_'+prefix+'.png')

  #c1.SetLogz()
  muPtEta2DEff.Draw('COLZ')
  c1.Print(PngPath+'muPtEta2DEff_'+prefix+'.png')
  c1.Print(PngPath+'muPtEta2DEff_'+prefix+'.root')
#  muPtEta2DPresEff.Draw('COLZ')
#  c1.Print('/afs/hephy.at/user/'+username[0]+'/'+username+'/www/pngCSA14/muPtEta2DPresEff_'+prefix+'.png')
  for l in Lepton:
    if Lepton[l]:
      Path='/data/'+username+'/results2014/'+l+'Templates/'
      if not os.path.exists(Path):
        os.makedirs(Path)
      fname='CSA14_TTJets_efficiencyMap_v26_'+prefix+'.pkl'
      pickle.dump(muPtEta2DEff, file(Path+fname,'w'))
      print "Written",  Path+fname 
