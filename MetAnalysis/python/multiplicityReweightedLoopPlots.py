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

metPhi = ROOT.TH1F('metPhi','metPhi',18,-pi,pi)
metPhiCorr = ROOT.TH1F('metPhiCorr','metPhiCorr',18,-pi,pi)
met = ROOT.TH1F('met','met',100,0,200)
metCorr = ROOT.TH1F('metCorr','metCorr',100,0,200)
metx = ROOT.TH1F('metx','metx',100,-100,100)
metxCorr = ROOT.TH1F('metxCorr','metxCorr',100,-100,100)
mety = ROOT.TH1F('mety','mety',100,-100,100)
metyCorr = ROOT.TH1F('metyCorr','metyCorr',100,-100,100)

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
nEvents = min([30000, c.GetEntries()])
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
  metPhi.Fill(atan2(meyUncorr, mexUncorr))
  metPhiCorr.Fill(atan2(meyCorr, mexCorr))
  met.Fill(sqrt(mexUncorr**2+meyUncorr**2))
  metCorr.Fill(sqrt(mexCorr**2+meyCorr**2))
  metx.Fill(mexUncorr)
  metxCorr.Fill(mexCorr)
  mety.Fill(meyUncorr)
  metyCorr.Fill(meyCorr)


c1 = ROOT.TCanvas()
metPhi.SetLineColor(ROOT.kBlue)
metPhi.Draw()
metPhiCorr.SetLineColor(ROOT.kRed)
metPhiCorr.Draw('same')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/metPhi_comparison_'+prefix+sample+'.png')

c1 = ROOT.TCanvas()
met.SetLineColor(ROOT.kBlue)
metCorr.SetLineColor(ROOT.kRed)
met.Draw()
c1.SetLogy()
metCorr.Draw('same')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/met_comparison_'+prefix+sample+'.png')

#c1 = ROOT.TCanvas()
#met.SetLineColor(ROOT.kBlue)
#metCorr.SetLineColor(ROOT.kRed)
#metCorr.Draw()
#c1.SetLogy()
#met.Draw('same')
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/met_comparison_'+prefix+sample+'.png')

c1 = ROOT.TCanvas()
metx.SetLineColor(ROOT.kBlue)
metx.Draw()
metxCorr.SetLineColor(ROOT.kRed)
metxCorr.Draw('same')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/metx_comparison_'+prefix+sample+'.png')

c1 = ROOT.TCanvas()
mety.SetLineColor(ROOT.kBlue)
mety.Draw()
metyCorr.SetLineColor(ROOT.kRed)
metyCorr.Draw('same')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/mety_comparison_'+prefix+sample+'.png')
