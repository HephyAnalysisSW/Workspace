import ROOT
from array import array
from math import *
import os, copy, sys

ROOT.TH1F().SetDefaultSumw2()

from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain
#from Workspace.RA4Analysis.simplePlotsCommon import *
from Workspace.RA4Analysis.helpers import *

sampleName = "WJets"

preselPHYS14 = "leptonPt>25&&singleMuonic&&nTightHardLeptons==1&&nLooseHardLeptons==1"
preselCSA14 =  "leptonPt>25&&singleMuonic&&nVetoMuons==1&&nVetoElectrons==0"
prefix = "lPt25_noWeight"
weight='(1)'

preselPHYS14 = "leptonPt>25&&singleMuonic&&nTightHardLeptons==1&&nLooseHardLeptons==1"
preselCSA14 =  "leptonPt>25&&singleMuonic&&nVetoMuons==1&&nVetoElectrons==0"
prefix = "lPt25"
weight='weight'

preselPHYS14 = "singleMuonic&&nTightHardLeptons==1&&nLooseHardLeptons==1"
preselCSA14 =  "singleMuonic&&nVetoMuons==1&&nVetoElectrons==0"
prefix = "orig"
weight='weight'

from Workspace.RA4Analysis.cmgTuplesPostProcessed_v4_Phys14V1 import WJetsHTToLNu as phys14_WJetsHTToLNu 
from Workspace.RA4Analysis.cmgTuplesPostProcessed import WJetsHTToLNu as csa14_WJetsHTToLNu

small = False
for i in range(-1,4):
  phys14_sample=  copy.deepcopy(phys14_WJetsHTToLNu['hard'])
  if i>=0:
    phys14_sample['bins']=phys14_WJetsHTToLNu['hard']['bins'][i:i+1]
  else:
    phys14_sample['bins']=phys14_WJetsHTToLNu['hard']['bins']
  if 'PHYS14' not in  phys14_sample['name']:phys14_sample['name']=phys14_sample['name']+"_PHYS14"
  csa14_sample=  copy.deepcopy(csa14_WJetsHTToLNu)
  if i>=0:
    csa14_sample['bins']=csa14_WJetsHTToLNu['bins'][i:i+1]
  else:
    csa14_sample['bins']=csa14_WJetsHTToLNu['bins']
  if 'CSA14' not in csa14_sample['name']:csa14_sample['name']=csa14_sample['name']+"_CSA14"

  #presel="singleMuonic&&nVetoMuons==1&&nVetoElectrons==0&&st>250&&htJet40ja>500&&nBJetMedium25>=1&&nJet40a>=4"

  phys14 = getChain(phys14_sample)
  csa14 = getChain(csa14_sample)

  for binning, var, name in [\
#     [[100,0,30000], 'met_pt', 'met_pt_wide'], [[100,0,30000], 'htJet40a', 'htJet40a_wide'], \
#     [[100,0,30000], 'met_genPt', 'met_genPt_wide']
     [[100,0,3000], 'met_pt', 'met_pt'], [[100,0,3000], 'htJet40a', 'htJet40a'], \
     [[100,0,3000], 'met_genPt', 'met_genPt'], 
     [[100,0,3000], 'leptonPt', 'leptonPt'], 
     [[100,0,100], 'leptonPt', 'leptonPt_zoom'], 
    ]:
    phys14.Draw(var+'>>h_phys14('+','.join([str(x) for x in binning])+')', '('+weight+')*('+preselPHYS14+')')
    h_phys14=ROOT.gDirectory.Get('h_phys14')
    csa14.Draw(var+'>>h_csa14('+','.join([str(x) for x in binning])+')', '('+weight+')*('+preselCSA14+')')
    h_csa14=ROOT.gDirectory.Get('h_csa14')
    h_phys14.SetLineColor(ROOT.kRed)
    c1=ROOT.TCanvas()
    h_phys14.Draw()
    h_csa14.Draw('same')
    c1.SetLogy()
  #  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPHYS14vsCSA14/WJets/draw_'+phys14_sample['bins'][i]+'_'+name+'.png')
    if i>=0:
      c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPHYS14vsCSA14/WJets/draw_'+prefix+'_'+csa14_WJetsHTToLNu['bins'][i]+'_'+name+'.png')
    else:
      c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPHYS14vsCSA14/WJets/draw_'+prefix+'_'+name+'.png')
