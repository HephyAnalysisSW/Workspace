import ROOT
from math import pi, sin, cos, sqrt
import numpy as np
from scipy import optimize
c = ROOT.TChain('Events')
#postFix='ttJets'
#c.Add('/data/schoef/convertedMETTuples_v2/inc/ttJets/histo_ttJets_from0To2.root')

postFix='dy53X'
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from0To1.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from1To2.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from2To3.root')
c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from3To4.root')

#c.Add('/data/schoef/convertedMETTuples_v2/inc/minBiasData/histo_minBiasData_small_from0To50.root')
#postFix = 'MinBiasSmall'

#c.Add('/data/schoef/convertedMETTuples_v2/inc/DoubleMu-Run2012A-22Jan2013/histo_DoubleMu-Run2012A-22Jan2013_small_from0To50.root')
##c.Draw('sqrt(Sum$((candId==6)*candPt*cos(candPhi))**2+Sum$((candId==6)*candPt*sin(candPhi))**2)')
#c.Draw('atan2(Sum$((candId==6)*candPt*sin(candPhi)),Sum$((candId==6)*candPt*cos(candPhi)))>>(20,-pi,pi)')



candRequ='candId==6&&candEta>0'
def getChi2Ndf(x, candRequ, verbose):
#  aprime=x[0]/1100.
#  phiHF=x[1]
  dx, dy = x
  if abs(x[0])>2. or abs(x[1])>2.: 
    print x
    return 10**9
##  f = 'atan2(Sum$(('+candRequ+')*candPt*sin(atan2(sin(candPhi)+'+str(aprime)+'*abs(sinh(candEta))*sin('+str(phiHF)+'), cos(candPhi)+'+str(aprime)+'*abs(sinh(candEta))*cos('+str(phiHF)+')))),Sum$(('+candRequ+')*candPt*cos(atan2(sin(candPhi)+'+str(aprime)+'*abs(sinh(candEta))*sin('+str(phiHF)+'), cos(candPhi)+'+str(aprime)+'*abs(sinh(candEta))*cos('+str(phiHF)+')))))'
  f = 'atan2(Sum$(('+candRequ+')*candPt*sin(atan2(sin(candPhi)+abs(sinh(candEta))*('+str(dy)+')/1100., cos(candPhi)+abs(sinh(candEta))*('+str(dx)+')/1100.))),'\
  +'Sum$(('+candRequ+')*candPt*cos(atan2(sin(candPhi)+abs(sinh(candEta))*('+str(dy)+')/1100., cos(candPhi)+abs(sinh(candEta))*('+str(dx)+')/1100.))))'

  if verbose:  print f
  c.Draw(f+'>>h(30,-pi,pi)', '', 'goff')
  h=ROOT.gDirectory.Get('h')
#h.SetLineColor(ROOT.kRed)
#c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngHF/metPhiHF.png')
  s_c=0
  c_c=0
  n2=0
  for i in range(1, h.GetNbinsX()+1):
    phi = h.GetBinCenter(i)
    v = h.GetBinContent(i)
    s_c += v*sin(phi)
    c_c += v*cos(phi)
    n2  += v**2
  res = sqrt((s_c**2+c_c**2)/n2)
#  func = ROOT.TF1('pol0', '[0]+[1]*sin(x-[2])')
#  fRes=h.Fit('pol0','S')
#  res = func.GetParameter(1)
#  if verbose:print 'Chi2',fRes.Chi2(),fRes.Ndf(), 'Target:',res, 'at xHF/phiHF',x 
  if verbose:print 'Target:',res, 'at dx/dy',x 
  del h
  return res 
 
#Optimizing
bnds = ((-2, 2), (-2, 2))
x0 = np.array([0.5,0.5])
#res= optimize.anneal(lambda x:getChi2Ndf(x,candRequ, verbose=True), x0, T0=.0001, learn_rate=1.5)
res= optimize.fmin(lambda x:getChi2Ndf(x,candRequ, verbose=True), x0)
#optChi2 = optimize.minimize(lambda x:getChi2Ndf(x,candRequ, verbose=True), x0, bounds=bnds)
dx, dy = res
c1 = ROOT.TCanvas()
c.Draw('atan2(Sum$((candId==6)*candPt*sin(candPhi)),Sum$((candId==6)*candPt*cos(candPhi)))>>(20,-pi,pi)')
f = 'atan2(Sum$(('+candRequ+')*candPt*sin(atan2(sin(candPhi)+abs(sinh(candEta))*('+str(dy)+')/1100., cos(candPhi)+abs(sinh(candEta))*('+str(dx)+')/1100.))),'\
+'Sum$(('+candRequ+')*candPt*cos(atan2(sin(candPhi)+abs(sinh(candEta))*('+str(dy)+')/1100., cos(candPhi)+abs(sinh(candEta))*('+str(dx)+')/1100.))))'
c.Draw(f+'>>h(20,-pi,pi)', '', 'same')
h=ROOT.gDirectory.Get('h')
h.SetLineColor(ROOT.kRed)
h.Draw('same')

c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngHF/metPhiHF_'+postFix+'.png')
