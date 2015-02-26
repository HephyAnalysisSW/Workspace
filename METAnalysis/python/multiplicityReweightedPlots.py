import ROOT
import pickle
from commons import label
from Workspace.HEPHYPythonTools.helpers import getVarValue
from math import pi, cos, sin, sqrt, atan2
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
sample = 'dy53X'
c = ROOT.TChain('Events')
c.Add('/data/schoef/convertedMETTuples_v2//inc/dy53X_dy53X_rwTo_flat/histo_dy53X_from10To11.root')
#c.Add('/data/schoef/convertedMETTuples_v2//inc/'+sample+'/histo_'+sample+'_*.root')
#c.Add('/data/schoef/convertedMETTuples_v2/inc/ttJets/histo_ttJets_from0To2.root')

def getShiftCorr(sample, mapName):
  res = pickle.load(file('/data/schoef/tools/metPhiShifts/shift_'+sample+'_'+mapName+'.pkl'))
  return res


from commons import *
  
prefix = 'candidateBased_comparison_'+sample
for map in allMaps:
  res = getShiftCorr(sample, map['name'])
  MEx_component = res['MEx'] 
  MEy_component = res['MEy'] 
  MEx_corr = '-('+res['param_x']+')' 
  MEy_corr = '-('+res['param_y']+')'

  sumStr1x = MEx_component 
  sumStr1y = MEy_component

  sumStr2x = MEx_component+MEx_corr 
  sumStr2y = MEy_component+MEy_corr

  sumvars = [\
        [ 'pfMetx_'+map['name'],    sumStr1x, sumStr2x,               [100,-100,100]],
        [ 'pfMety_'+map['name'],    sumStr1y, sumStr2y,               [100,-100,100]],
        [ 'pfMet_'+map['name'],    'sqrt(('+sumStr1x+')**2+('+sumStr1y+')**2)', 'sqrt(('+sumStr2x+')**2+('+sumStr2y+')**2)',               [100,0,200]],
        [ 'pfMetphi_'+map['name'],   'atan2('+sumStr1y+','+sumStr1x+')', 'atan2('+sumStr2y+','+sumStr2x+')',               [18,-pi,pi]],
      ]
  print sumStr1x
  print sumStr2x
  print sumStr1y
  print sumStr2y
  h1 = {}
  h2 = {}
  for m,  var, var2, binning in sumvars:
    h1[m] = ROOT.TH1F('h1_'+m, 'h1_'+m, *binning)
    c.Draw(var+'>>h1_'+m, res['candCount']+'>1')
    h2[m] = ROOT.TH1F('h2_'+m, 'h2_'+m, *binning)
    c.Draw(var2+'>>h2_'+m, res['candCount']+'>1')

  for m, var, var2, binning in sumvars:
    c1= ROOT.TCanvas()
    h1[m].Draw()
    if m.lower().count('phi'):
      c1.SetLogy(0)
    else:
      c1.SetLogy()
    h2[m].SetLineColor(ROOT.kRed)
    h2[m].Draw('same')
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+'_'+m+".png")
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+'_'+m+".root")

#def candBasedCorrFormula(sample):
##  lshifts = pickle.load(file(shiftFile))
#  sx = []
#  sy = []
#  for map in allMaps[10:13]:
#    res = getShiftCorr(sample, map['name'])
#    MEx_component = res['MEx'] 
#    MEy_component = res['MEy'] 
#    MEx_corr = '-'+res['param_x'] 
#    MEy_corr = '-'+res['param_y'] 
#    sx.append(MEx_corr)
#    sy.append(MEy_corr)
#  return '('+'+'.join(sx)+')', '('+'+'.join(sy)+')'

#prefix = 'candidateBased_comparison_'+sample
#MEx_corr, MEy_corr = candBasedCorrFormula(sample) 
#
#sumStr1x = 'Sum$(candPt*cos(candPhi))'
#sumStr1y = 'Sum$(candPt*sin(candPhi))'
#
#sumStr2x = 'Sum$(candPt*cos(candPhi))+'+MEx_corr 
#sumStr2y = 'Sum$(candPt*sin(candPhi))+'+MEy_corr
#
#sumvars = [\
#      [ 'pfMetx',    sumStr1x, sumStr2x,               [100,-100,100]],
#      [ 'pfMety',    sumStr1y, sumStr2y,               [100,-100,100]],
#      [ 'pfMet',    'sqrt(('+sumStr1x+')**2+('+sumStr1y+')**2)', 'sqrt(('+sumStr2x+')**2+('+sumStr2y+')**2)',               [100,0,200]],
#      [ 'pfMetphi',   'atan2('+sumStr1y+','+sumStr1x+')', 'atan2('+sumStr2y+','+sumStr2x+')',               [18,-pi,pi]],
#    ]
#print sumStr1x
#print sumStr2x
#print sumStr1y
#print sumStr2y
#c.Scan(':'.join([sumStr1x, sumStr2x, sumStr1y, sumStr2y]))
#h1 = {}
#h2 = {}
#for m,  var, var2, binning in sumvars:
#  h1[m] = ROOT.TH1F('h1_'+m, 'h1_'+m, *binning)
#  c.Draw(var+'>>h1_'+m)
#  h2[m] = ROOT.TH1F('h2_'+m, 'h2_'+m, *binning)
#  c.Draw(var2+'>>h2_'+m)
#
#for m, var, var2, binning in sumvars:
#  c1= ROOT.TCanvas()
#  h1[m].Draw()
#  if m.lower().count('phi'):
#    c1.SetLogy(0)
#  else:
#    c1.SetLogy()
#  h2[m].SetLineColor(ROOT.kRed)
#  h2[m].Draw('same')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+'_'+m+".png")
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+'_'+m+".root")

