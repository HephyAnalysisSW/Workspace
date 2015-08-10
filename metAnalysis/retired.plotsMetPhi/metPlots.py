import ROOT 
import os
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import sqrt, sin, cos, atan2, pi
from Workspace.HEPHYPythonTools.helpers import getVarValue

from commons import label, pfTypes, allMaps

c = ROOT.TChain('Events')

idir = '/data/schoef/convertedMETTuples_v2//inc/dy53X_dy53X_rwTo_flat/'
fl = os.listdir(idir)
filelist=[]
for f in fl:
  filelist.append(idir+'/'+f)

#filelist = ['/data/schoef/convertedMETTuples_v2//inc/dy53X_dy53X_rwTo_flat/histo_dy53X_small.root']


for f in filelist:
  c.Add(f)

#        prefix = "root://hephyse.oeaw.ac.at/"#+subdirname
#mapNames = ['map_'+m['name'] for m in allMaps]
#vars = [\
#      [ 'pfMet',   'pfMetRW',   'pfMet_R',                'pfMetRW_R',                [100,0,400]],
#      [ 'pfMetx',  'pfMetRWx',  'pfMetx_R',               'pfMetRWx_R',               [100,-100,100]],
#      [ 'pfMety',  'pfMetRWy',  'pfMety_R',               'pfMetRWy_R',               [100,-100,100]],
#      [ 'pfMetphi','pfMetRWphi','atan2(pfMety_R, pfMetx_R)','atan2(pfMetRWy_R, pfMetRWx_R)',[18,-pi,pi]],
#    ]
##cut='pfMetRWx>50'
#cut=''
#h = {}
#for m, mRW, var, varRW, binning in vars:
#  h[m] = ROOT.TH1F('h_'+m, 'h_'+m, *binning)
#  c.Draw(var.replace('_R','')+'>>h_'+m, cut)
#  h[mRW] = ROOT.TH1F('h_'+mRW, 'h_'+mRW, *binning)
#  c.Draw(varRW.replace('_R','')+'>>h_'+mRW, cut)
#  h[m+'_None'] = ROOT.TH1F('h_'+m+'_None', 'h_'+m+'_None', *binning)
#  c.Draw(var.replace('_R','_None')+'>>h_'+m+'_None', cut)
#for t in pfTypes+mapNames:
#  for m, mRW, var, varRW, binning in vars:
#    h[m+'_'+t] = ROOT.TH1F('h_'+m+'_'+t, 'h_'+m+'_'+t, *binning)
#    c.Draw(var.replace('_R','_'+t)+'>>h_'+m+'_'+t, cut)
#    h[mRW+'_'+t] = ROOT.TH1F('h_'+mRW+'_'+t, 'h_'+mRW+'_'+t, *binning)
#    c.Draw(varRW.replace('_R','_'+t)+'>>h_'+mRW+'_'+t, cut)
#for t in pfTypes:
#  for m, mRW, var, varRW, binning in vars:
#    h[m+'_'+t+'_None'] = ROOT.TH1F('h_'+m+'_'+t+'_None', 'h_'+m+'_'+t+'_None', *binning)
#    c.Draw(var.replace('_R','_'+t+'_None')+'>>h_'+m+'_'+t+'_None', cut)
#
#for m, mRW, var, varRW, binning in vars:
#  c1= ROOT.TCanvas()
#  h[m].Draw()
#  if m.lower().count('phi'):
#    c1.SetLogy(0)
#  else:
#    c1.SetLogy()
#  h[mRW].SetLineColor(ROOT.kRed)
#  h[mRW].Draw('same')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+m+".png")
#  h[m+'_None'].Draw()
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+m+'_None.png')
#for t in pfTypes+mapNames:
#  for m, mRW, var, varRW, binning in vars:
#    c1= ROOT.TCanvas()
#    h[m+'_'+t].Draw()
#    if m.lower().count('phi'):
#      c1.SetLogy(0)
#    else:
#      c1.SetLogy()
#    h[mRW+'_'+t].SetLineColor(ROOT.kRed)
#    h[mRW+'_'+t].Draw('same')
#    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+m+'_'+t+".png")
#for t in pfTypes:
#  for m, mRW, var, varRW, binning in vars:
#    c1= ROOT.TCanvas()
#    h[m+'_'+t+'_None'].Draw()
#    if m.lower().count('phi'):
#      c1.SetLogy(0)
#    else:
#      c1.SetLogy()
#    h[m+'_'+t+'_None'].Draw()
#    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+m+'_'+t+'_None.png')

#prefix="h"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx - pfMetx_h + pfMetRWx_h '

prefix="h0"
sumStr1x = 'pfMetx'
sumStr2x = 'pfMetx - pfMetx_h0 + pfMetRWx_h0'

#prefix="combined_h"
#sumStr1x = 'pfMetx_h'
#sumStr2x = 'pfMetRWx_h'
#
#prefix="combined_h0"
#sumStr1x = 'pfMetx_h0'
#sumStr2x = 'pfMetRWx_h0'

#prefix="combined_h_h0"
#sumStr1x = 'pfMetx_h + pfMetx_h0'
#sumStr2x = 'pfMetRWx_h + pfMetRWx_h0'

#prefix="combined_h_h0_gamma"
#sumStr1x = 'pfMetx_h + pfMetx_h0 + pfMetx_gamma'
#sumStr2x = 'pfMetRWx_h + pfMetRWx_h0 + pfMetRWx_gamma'

#prefix="combined_h_h0_gamma_hHF_egammaHF_mu_e"
#sumStr1x = 'pfMetx_h + pfMetx_h0 + pfMetx_gamma+pfMetx_h_HF + pfMetx_egamma_HF+pfMetx_mu+pfMetx_e'
#sumStr2x = 'pfMetRWx_h + pfMetRWx_h0 + pfMetRWx_gamma+pfMetRWx_h_HF + pfMetRWx_egamma_HF+pfMetRWx_mu+pfMetRWx_e'

#prefix="h_h0"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx - pfMetx_h + pfMetRWx_h - pfMetx_h0 + pfMetRWx_h0'

#prefix="h_h0_gamma"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx - pfMetx_h + pfMetRWx_h - pfMetx_h0 + pfMetRWx_h0 - pfMetx_gamma + pfMetRWx_gamma'

#prefix="hHF_egammaHF"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx - pfMetx_h_HF + pfMetRWx_h_HF - pfMetx_egamma_HF + pfMetRWx_egamma_HF'
#
#prefix="combined_hHF_egammaHF"
#sumStr1x = 'pfMetx_h_HF + pfMetx_egamma_HF'
#sumStr2x = 'pfMetRWx_h_HF + pfMetRWx_egamma_HF'


#prefix="hHF"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx - pfMetx_h_HF + pfMetRWx_h_HF'

#prefix="egammaHF"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx - pfMetx_egamma_HF + pfMetRWx_egamma_HF'

#prefix="gamma"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx - pfMetx_gamma + pfMetRWx_gamma'


#prefix="noh"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx  - pfMetx_h0 + pfMetRWx_h0 - pfMetx_egamma_HF + pfMetRWx_egamma_HF- pfMetx_h_HF + pfMetRWx_h_HF- pfMetx_gamma + pfMetRWx_gamma'

#prefix="noh0"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx - pfMetx_h + pfMetRWx_h - pfMetx_egamma_HF + pfMetRWx_egamma_HF- pfMetx_h_HF + pfMetRWx_h_HF- pfMetx_gamma + pfMetRWx_gamma'

#prefix="noEgammaHF"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx - pfMetx_h + pfMetRWx_h - pfMetx_h0 + pfMetRWx_h0 - pfMetx_h_HF + pfMetRWx_h_HF- pfMetx_gamma + pfMetRWx_gamma'

#prefix="noHHF"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx - pfMetx_h + pfMetRWx_h - pfMetx_h0 + pfMetRWx_h0 - pfMetx_egamma_HF + pfMetRWx_egamma_HF- pfMetx_gamma + pfMetRWx_gamma'

#prefix="nogamma"
#sumStr1x = 'pfMetx'
#sumStr2x = 'pfMetx - pfMetx_h + pfMetRWx_h - pfMetx_h0 + pfMetRWx_h0 - pfMetx_egamma_HF + pfMetRWx_egamma_HF- pfMetx_h_HF + pfMetRWx_h_HF'

sumStr1y = sumStr1x.replace('x','y') 
sumStr2y = sumStr2x.replace('x','y') 

sumvars = [\
      [ 'sumComp_pfMetx',  'pfMetxSum',  sumStr1x, sumStr2x,               [100,-100,100]],
      [ 'sumComp_pfMety',  'pfMetySum',  sumStr1y, sumStr2y,               [100,-100,100]],
      [ 'sumComp_pfMet',  'pfMetSum',  'sqrt(('+sumStr1x+')**2+('+sumStr1y+')**2)', 'sqrt(('+sumStr2x+')**2+('+sumStr2y+')**2)',               [100,0,400]],
      [ 'sumComp_pfMetphi',  'pfMetphiSum',  'atan2('+sumStr1y+','+sumStr1x+')', 'atan2('+sumStr2y+','+sumStr2x+')',               [18,-pi,pi]],
    ]
h = {}
for m, m2, var, var2, binning in sumvars:
  h[m] = ROOT.TH1F('h_'+m, 'h_'+m, *binning)
  c.Draw(var+'>>h_'+m)
  h[m2] = ROOT.TH1F('h_'+m2, 'h_'+m2, *binning)
  c.Draw(var2+'>>h_'+m2)

for m, m2, var, var2, binning in sumvars:
  c1= ROOT.TCanvas()
  h[m].Draw()
  if m.lower().count('phi'):
    c1.SetLogy(0)
  else:
    c1.SetLogy()
  h[m2].SetLineColor(ROOT.kRed)
  h[m2].Draw('same')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+'_'+m+".png")
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+'_'+m+".root")



