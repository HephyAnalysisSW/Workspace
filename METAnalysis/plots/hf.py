import ROOT
from math import pi, sin, cos, sqrt
import numpy as np
import pickle, os
from scipy import optimize
from optparse import OptionParser
from localInfo import userName, nfsName

parser = OptionParser()
parser.add_option("--sample", dest="sample", default="dy53X", type="string", action="store", help="samples:Which samples.")
parser.add_option("--candRequ", dest="cut", default='candId==6&&candEta>0', type="string", action="store", help="")
parser.add_option("--postFix", dest="postFix", default='hHFPlus', type="string", action="store", help="")

(options, args) = parser.parse_args()

c = ROOT.TChain('Events')
if options.sample=='ttJets':
  c.Add('/data/schoef/convertedMETTuples_v2/inc/ttJets/histo_ttJets_from0To2.root')
if options.sample=='dy53X':
  c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from0To1.root')
  c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from1To2.root')
  c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from2To3.root')
  c.Add('/data/schoef/convertedMETTuples_v2/inc/dy53X/histo_dy53X_from3To4.root')
if options.sample=='minBiasSmall':
  c.Add('/data/schoef/convertedMETTuples_v2/inc/minBiasData/histo_minBiasData_small_from0To50.root')
postFix = '_'.join([options.sample, options.postFix])

#c.Add('/data/schoef/convertedMETTuples_v2/inc/DoubleMu-Run2012A-22Jan2013/histo_DoubleMu-Run2012A-22Jan2013_small_from0To50.root')
##c.Draw('sqrt(Sum$((candId==6)*candPt*cos(candPhi))**2+Sum$((candId==6)*candPt*sin(candPhi))**2)')
#c.Draw('atan2(Sum$((candId==6)*candPt*sin(candPhi)),Sum$((candId==6)*candPt*cos(candPhi)))>>(20,-pi,pi)')

hStart = ROOT.TH1F('hStart', 'hStart', 30, -pi, pi)
c.Draw('atan2(Sum$(('+options.cut+')*candPt*sin(candPhi)),Sum$(('+options.cut+')*candPt*cos(candPhi)))>>hStart','Sum$('+options.cut+')>0','goff')
yRange = [0, 1.2*hStart.GetBinContent(hStart.GetMaximumBin())]
hStart.GetYaxis().SetRangeUser(*yRange)
hStart.SetLineColor(ROOT.kRed)
history = [hStart]
iter=0
gifFile = '/afs/hephy.at/user/'+userName[0]+'/'+userName+'/www/pngHF/metPhiHF_'+postFix+'.gif'
os.system('rm -rf '+gifFile)

def getChi2Ndf(x, candRequ, verbose):
  global iter
  global history
  global c1
#  aprime=x[0]/1100.
#  phiHF=x[1]
  dx, dy = x
  if abs(x[0])>2. or abs(x[1])>2.: 
    print x
    return 10**9
#  f = 'atan2(Sum$(('+candRequ+')*candPt*sin(atan2(sin(candPhi)+'+str(aprime)+'*abs(sinh(candEta))*sin('+str(phiHF)+'), cos(candPhi)+'+str(aprime)+'*abs(sinh(candEta))*cos('+str(phiHF)+')))),Sum$(('+candRequ+')*candPt*cos(atan2(sin(candPhi)+'+str(aprime)+'*abs(sinh(candEta))*sin('+str(phiHF)+'), cos(candPhi)+'+str(aprime)+'*abs(sinh(candEta))*cos('+str(phiHF)+')))))'
  f = 'atan2(Sum$(('+candRequ+')*candPt*sin(atan2(sin(candPhi)+abs(sinh(candEta))*('+str(dy)+')/1100., cos(candPhi)+abs(sinh(candEta))*('+str(dx)+')/1100.))),'\
  +'Sum$(('+candRequ+')*candPt*cos(atan2(sin(candPhi)+abs(sinh(candEta))*('+str(dy)+')/1100., cos(candPhi)+abs(sinh(candEta))*('+str(dx)+')/1100.))))'

  if verbose:  print f
  h = ROOT.TH1F('hTMP', 'hTMP', 30, -pi, pi)
  c.Draw(f+'>>hTMP', 'Sum$('+options.cut+')>0', 'goff')
#h.SetLineColor(ROOT.kRed)
#c1.Print('/afs/hephy.at/user/'+userName[0]+'/'+userName+'/www/pngHF/metPhiHF.png')
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
  h.SetLineColor(ROOT.kBlack)
  history.append(h.Clone('iter_'+str(iter)))
  del h
  history[0].Draw()
  history[0].GetYaxis().SetRangeUser(*yRange)
  for hist in history[-1:]:
    hist.GetYaxis().SetRangeUser(*yRange)
    hist.Draw('same')
  lines=[]
  lines.append([0.5, 0.4,  "#Delta x = "+str(round(dx,2))+" cm"])
  lines.append([0.5, 0.35, "#Delta y = "+str(round(dy,2))+" cm"])
  latex = ROOT.TLatex();
  latex.SetNDC();
  latex.SetTextSize(0.04);
  latex.SetTextAlign(11); # align right
  for line in lines:
    latex.SetTextSize(0.04)
    latex.DrawLatex(line[0],line[1],line[2])
  c1.Modified()
  c1.Update()
  c1.Print(gifFile+'+')

  iter+=1
  if verbose:print 'Target:',res, 'at dx/dy',x, 'sample', options.sample 
  return res 

print "All files:", c.GetListOfFiles().ls() 
print "nEvents:", c.GetEntries()

#Optimizing
bnds = ((-2, 2), (-2, 2))
x0 = np.array([0.5,0.5])
#res= optimize.anneal(lambda x:getChi2Ndf(x,candRequ, verbose=True), x0, T0=.0001, learn_rate=1.5)
c1 = ROOT.TCanvas()
res= optimize.fmin(lambda x:getChi2Ndf(x,options.cut, verbose=True), x0)
c1.Print(gifFile+'++')

del c1
#optChi2 = optimize.minimize(lambda x:getChi2Ndf(x,candRequ, verbose=True), x0, bounds=bnds)
dx, dy = res
candRequ=options.cut
c1 = ROOT.TCanvas()
hStart.GetYaxis().SetRangeUser(*yRange)
hStart.Draw()
f = 'atan2(Sum$(('+candRequ+')*candPt*sin(atan2(sin(candPhi)+abs(sinh(candEta))*('+str(dy)+')/1100., cos(candPhi)+abs(sinh(candEta))*('+str(dx)+')/1100.))),'\
+'Sum$(('+candRequ+')*candPt*cos(atan2(sin(candPhi)+abs(sinh(candEta))*('+str(dy)+')/1100., cos(candPhi)+abs(sinh(candEta))*('+str(dx)+')/1100.))))'
hAfter = ROOT.TH1F('hAfter', 'hAfter', 30, -pi, pi)
c.Draw(f+'>>hAfter', 'Sum$('+options.cut+')>0')
hAfter.Draw('same')

lines=[]
lines.append([0.5, 0.4,  "#Delta x = "+str(round(dx,2))+" cm"])
lines.append([0.5, 0.35, "#Delta y = "+str(round(dy,2))+" cm"])
latex = ROOT.TLatex();
latex.SetNDC();
latex.SetTextSize(0.04);
latex.SetTextAlign(11); # align right
for line in lines:
  latex.SetTextSize(0.04)
  latex.DrawLatex(line[0],line[1],line[2])


result = {'dx':dx, 'dy':dy, 'hStart':hStart, 'hAfter':hAfter, 'cut':options.cut, 'nEvents':c.GetEntries(), 'fileList':c.GetListOfFiles()}
c1.Print('/afs/hephy.at/user/'+userName[0]+'/'+userName+'/www/pngHF/metPhiHF_'+postFix+'.png')
c1.Print('/data/'+nfsName+'/results2014/HFFit//metPhiHF_'+postFix+'.png')
pickle.dump(result,file( '/data/'+nfsName+'/results2014/HFFit/metPhiHF_results_'+postFix+'.pkl', 'w'))
