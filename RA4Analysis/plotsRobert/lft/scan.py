from smodels.theory import crossSection
import smodels.tools.modpyslha as pyslha
import os
import ROOT
import array
from xsecSMS import gluino13TeV_NLONLL
from math import log

def matchIDs(id1, id2, ignoreCharges):
  if ignoreCharges:
    id1=[abs(i) for i in id1]
    id2=[abs(i) for i in id2]
  id1.sort()
  id2.sort()
  return id1==id2

def getBranching(slha, particle, finalState, sumCharges=True):
  dec=slha.decays[particle].decays
  totBR=0
  for d in dec:
    if matchIDs(d.ids, finalState, ignoreCharges=sumCharges): totBR+=d.br 
  return totBR
def getTotalBranching(slha, particle1, particle2, sumCharges=True):
  dec=slha.decays[particle1].decays
  if sumCharges:
    particle2=abs(particle2)
  totBR=0
  for d in dec:
    ids = [abs(i) for i in d.ids] if sumCharges else d.ids
    if particle2 in ids: totBR+=d.br 
  return totBR

def scatterOnTH2(data, h, ofile, markerType):
  assert type(h)==type(ROOT.TH2F()) or type(h)==type(ROOT.TH2D()), "Wrong type of histogram! %s" % repr(type(h))
  h.Reset()
  for d in data:
    h.Fill(d[0], d[1], 0) 
  c1 = ROOT.TCanvas()
  xmin = h.GetXaxis().GetXmin()
  xmax = h.GetXaxis().GetXmax()
  ymin = h.GetYaxis().GetXmin()
  ymax = h.GetYaxis().GetXmax()
  zvals = [d[2] for d in data] 
  zmin, zmax = min(zvals), max(zvals)
  h.GetZaxis().SetRangeUser(min(zmax*10**-1.5, max(zmin, zmax*10**-4)),zmax)
  c1.SetLogz()
  h.Draw("COLZ")
  c1.Update()
  zPaletteAxis=h.GetListOfFunctions().FindObject("palette")
  stuff=[]
  for d in data:
    if d[0]>xmin and d[0]<xmax and d[1]>ymin and d[1]<ymax:
      if d[2]>0: 
        e = ROOT.TMarker(d[0], d[1], markerType)
        e.SetMarkerColor(zPaletteAxis.GetValueColor(log(d[2],10))) 
        stuff.append(e)
#    h.Fill(d[0], d[1], 0) 
  for s in stuff:
    s.Draw()
  c1.Print(ofile)

dataPath = "/Users/robertschoefbeck//CloudStation/data/LFT/"

def getXSec(xsec, pid):
  for x in xsec.xSections:
    if False not in [ abs(p)==pid for p in x.pid ]:
      return x.value

def readLimit(f):
  lines=[]
  for l in file(f).readlines():
    if "The highest r value is" in l:lines.append(l)
  if len(lines)>0:
    return float(lines[0].split("=")[1])
  
def vec(res, key):
  return array.array('d', [r[key] for r in res])

files = os.listdir(dataPath+'/slha/')
res=[]
for i, f in enumerate(files):
  if i%100==0:
    print i,'/',len(files)
  exclR=readLimit(dataPath+'/smodelsOutputRun3/'+f)
  if exclR>1:
    continue
  slha=pyslha.readSLHAFile(dataPath+'/slha/'+f, ignoreblocks=['XSECTION'])
  mgl = slha.blocks['MASS'][1000021]
#  xsec=crossSection.getXsecFromSLHAFile(dataPath+'/slha/'+f)
#  xsec_gluinoPair= xsec_gluinoPair.asNumber()
#  xsec_gluinoPair= = getXSec(xsec, 1000021)
  roundMgl= 5*int(round(mgl/5.))
  xsec_gluinoPair=gluino13TeV_NLONLL[roundMgl] if gluino13TeV_NLONLL.has_key(roundMgl) else 0
  mn = abs(slha.blocks['MASS'][1000022])
  br_gluinoToStop     = getBranching(slha, 1000021, [1000006, 6])
  br_stopToCha     = getBranching(slha, 1000006, [1000024, 5])

  br_sbotToCha     = getBranching(slha, 1000005, [1000024, 6])
  br_gluinoToSbottom  = getBranching(slha, 1000021, [1000005, 5])

  br_gluinoToCha     = getBranching(slha, 1000021, [1000024, 5, 6])
  br_ChaToNeu     = getTotalBranching(slha, 1000024, 1000022)
  print 'gluino to stop',br_gluinoToStop,'gluino to sbottom', br_gluinoToSbottom, 'stop to cha1',br_stopToCha,'sbot to cha1', br_sbotToCha
  print 'br_gluinoToCha', br_gluinoToCha, 'br_ChaToNeu', br_ChaToNeu
 
#  br_chaToNeu      = getBranching(slha, 1000024, [1000024, 6])
#  getBranching(slha, 1000006, [1000024, 6])
  BR_gluinoPairToNeuPair = ((br_gluinoToStop*br_stopToCha + br_gluinoToSbottom*br_sbotToCha + br_gluinoToCha)*br_ChaToNeu)**2
#  print mgl, mn, xsec_gluinoPair, exclR, "BR_gluinoPairToChaPair",BR_gluinoPairToChaPair
  res.append({'mgl':mgl, 'mn':mn, 
    'xsec_gluinoPair':xsec_gluinoPair, 
    'xsecBR_gluinoPairToNeuPair':xsec_gluinoPair*BR_gluinoPairToNeuPair,
    'BR_gluinoPairToNeuPair':BR_gluinoPairToNeuPair,
    'br_gluinoToStop':br_gluinoToStop,'br_gluinoToSbottom':br_gluinoToSbottom,'br_stopToCha':br_stopToCha,'br_sbotToCha':br_sbotToCha,'br_gluinoToCha':br_gluinoToCha,'br_ChaToNeu':br_ChaToNeu})

for zVar in ['xsec_gluinoPair', 'xsecBR_gluinoPairToNeuPair', 'BR_gluinoPairToNeuPair', 'br_gluinoToStop', 'br_gluinoToSbottom', 'br_stopToCha', 'br_sbotToCha', 'br_ChaToNeu']:
  data = [(r['mgl'], r['mn'], r[zVar]) for r in res if r[zVar]>0]
  data.sort(key=lambda x:x[2])
  h=ROOT.TH2F(zVar, '', 1500-600,600,1500,500,0,500)
  h.Reset()
  h.GetXaxis().SetTitle("")
  h.GetYaxis().SetTitle("")
  ROOT.gStyle.SetOptStat(0)
  scatterOnTH2(data, h, '/Users/robertschoefbeck/Desktop/plots/'+zVar+'.png', 20)

  h=ROOT.TGraph2D('xsec', 'xsec', len(res), vec(res,'mgl'), vec(res, 'mn'), vec(res, zVar))
  c1=ROOT.TCanvas()
  h.Draw('COLZ')
  c1.SetLogz()
  c1.Print('/Users/robertschoefbeck/Desktop/plots/th2f_'+zVar+'.png')
  del h
#
