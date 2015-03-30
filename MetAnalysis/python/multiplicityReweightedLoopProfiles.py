import os,sys,ROOT,pickle
from array import array
from math import sqrt, pi, cos, sin, atan2
#from localInfo import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getVarValue
from commons import *
sample = 'dy53X'
c = ROOT.TChain('Events')
#c.Add('/data/schoef/convertedMETTuples_v2//inc/dy53X_dy53X_rwTo_flat/histo_dy53X_from10To11.root')
c.Add('/data/schoef/convertedMETTuples_v2//inc/'+sample+'/histo_'+sample+'_*.root')
#c.Add('/data/schoef/convertedMETTuples_v2/inc/ttJets/histo_ttJets_from0To2.root')
c.GetEntries()

metx = ROOT.TProfile('metx','metx',50,0,50,-20,20)
metxCorr = ROOT.TProfile('metxCorr','metxCorr',50,0,50,-20,20)
mety = ROOT.TProfile('mety','mety',50,0,50,-20,20)
metyCorr = ROOT.TProfile('metyCorr','metyCorr',50,0,50,-20,20)

def getShiftCorr(sample, mapName):
  res = pickle.load(file('/data/schoef/tools/metPhiShifts/shift_'+sample+'_'+mapName+'.pkl'))
  return res

#for map in allMaps:
#  for k in ['fx', 'fy']:
#    sstring=""
#    for sample in ['MinimumBias-Run2012D-22Jan2013', 'DoubleMu-Run2012D-22Jan2013']:
##    for sample in ['dy53X', 'ttJets']:
##    for sample in ['dy53X', 'ttJets']:
#      res= getShiftCorr(sample, map['name'])
#      f=res[k]
#      if f.GetTitle().count('x^2'):
#        sstring+= ("("+"%2.2e"%f.GetParameter(0)+"+/-"+"%2.2e"%f.GetParError(0)+")*n^2 + ("+"%2.2e"%f.GetParameter(1)+'+/- '+"%2.2e"%f.GetParError(1)+")*n   ").rjust(60)
#      else:
#        sstring+= ("("+"%2.2e"%f.GetParameter(0)+"+/-"+"%2.2e"%f.GetParError(0)+")*n   ").rjust(30)
# 
#    print map['name'].rjust(30),k, sstring    

c.GetEntry(1)

def candBasedCorrFormula(sample):
#  lshifts = pickle.load(file(shiftFile))
  r={}
  r['countTTreeFormula'] = {}
  r['candCount'] = {}
  r['shifts'] = {}
  r['MExCorrFormula'] = {}
  r['MEyCorrFormula'] = {}
  for map in allMaps:
    res = getShiftCorr(sample, map['name'])
    r['shifts'][map['name']]=res
#    MEx_component = res['MEx'] 
#    MEy_component = res['MEy'] 
#    MEx_corr = '-'+res['param_x'] 
#    MEy_corr = '-'+res['param_y'] 
#ROOT.TTreeFormula("numBPartons", "Sum$(abs(jetsParton)==5&&jetsEleCleaned&&jetsMuCleaned&&jetsID)",c)
    r['countTTreeFormula'][map['name']] = ROOT.TTreeFormula("countFormula_"+map['name'], res['candCount'] ,c)
    r['candCount'][map['name']] = res['candCount'] 
    r['MExCorrFormula'][map['name']] = lambda c:-r['shifts'][map['name']]['fx'].Eval(r['countTTreeFormula'][map['name']].EvalInstance())
    r['MEyCorrFormula'][map['name']] = lambda c:-r['shifts'][map['name']]['fy'].Eval(r['countTTreeFormula'][map['name']].EvalInstance())
  return r


r = candBasedCorrFormula(sample)
MExFormula = ROOT.TTreeFormula("MExFormula", "-Sum$(candPt*cos(candPhi))" ,c)
MEyFormula = ROOT.TTreeFormula("MEyFormula", "-Sum$(candPt*sin(candPhi))" ,c)
#c.GetEntry(1)
#MExFormula.EvalInstance()
#MEyFormula.EvalInstance()

#prefix='highMetCorr_'
prefix=''
nEvents = min([100000, c.GetEntries()])
for i in range(nEvents):
  if i%100==0:print "At",i,"/",nEvents
  c.GetEntry(i)
  MExCorr={}
  MEyCorr={}
  for map in allMaps:
    r['countTTreeFormula'][map['name']].UpdateFormulaLeaves()
    count = r['countTTreeFormula'][map['name']].EvalInstance()
    MExCorr[map['name']] = -r['shifts'][map['name']]['fx'].Eval(count) 
    MEyCorr[map['name']] = -r['shifts'][map['name']]['fy'].Eval(count) 
  MExFormula.UpdateFormulaLeaves()
  MEyFormula.UpdateFormulaLeaves()

  mexUncorr = MExFormula.EvalInstance()
  meyUncorr = MEyFormula.EvalInstance()
  mexCorr = mexUncorr + sum(MExCorr.values())
  meyCorr = meyUncorr + sum(MEyCorr.values())
  metCorrVal = sqrt(mexCorr**2+meyCorr**2)
#  if metCorrVal<50:continue
  nvtx = c.GetLeaf('ngoodVertices').GetValue()
  metx.Fill(nvtx, mexUncorr)
  metxCorr.Fill(nvtx, mexCorr)
  mety.Fill(nvtx, meyUncorr)
  metyCorr.Fill(nvtx, meyCorr)


c1 = ROOT.TCanvas()
mety.SetLineColor(ROOT.kBlack)
mety.Draw()
metyCorr.SetLineColor(ROOT.kBlue)
metyCorr.Draw('same')
l=ROOT.TLine(0,0,50,0)
l.Draw()
#metx.SetLineColor(ROOT.kRed)
#metx.Draw('same')
#metxCorr.SetLineColor(ROOT.kGreen)
#metxCorr.Draw('same')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/nvtxProfile_'+prefix+sample+'.png')

