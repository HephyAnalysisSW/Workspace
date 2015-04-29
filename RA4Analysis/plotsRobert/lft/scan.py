from smodels.theory import crossSection
import smodels.tools.modpyslha as pyslha
import os
import ROOT
import array
from xsecSMS import gluino13TeV_NLONLL, gluino8TeV_NLONLL
ROOT.gROOT.ProcessLine(".L ../../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C+")
ROOT.useNiceColorPalette(255)
gluinoXSec = gluino8TeV_NLONLL

from math import log

modelReaderXSecUnitConversion = 0.001
verbose=False

def matchIDs(id1, id2, ignoreCharges):
  if ignoreCharges:
    id1=[abs(i) for i in id1]
    id2=[abs(i) for i in id2]
  id1.sort()
  id2.sort()
  return id1==id2

def getXSec(xsec, pid, ignoreCharges=True):
  if ignoreCharges:
    pid=[abs(i) for i in pid]
  res=[]
  for x in xsec.xSections:
    pid2 = x.pid if not ignoreCharges else [ abs(p) for p in x.pid ]
    if matchIDs( pid, pid2, ignoreCharges=ignoreCharges):
      res.append([x.info.order, x]) 
  res.sort()
  if len(res)>0:
    return res[-1][1]
 
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

def scatterOnTH2(data, h, ofile, markerType, markerSize=1.):
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
  zmin, zmax = min(zmax*10**-1.5, max(zmin, zmax*10**-4)),zmax
  h.GetZaxis().SetRangeUser(zmin, zmax)
  c1.SetLogz()
  h.Draw("COLZ")
#  palette = h.GetListOfFunctions().FindObject("palette")
  c1.Update()
  stuff=[]
  for d in data:
    if d[0]>xmin*1.02 and d[0]<xmax*0.98 and d[1]>ymin*1.02 and d[1]<ymax*0.98:
      if d[2]>0: 
        e = ROOT.TMarker(d[0], d[1], markerType)
        zRatio = (log(d[2])-log(zmin))/(log(zmax) - log(zmin))
        color = ROOT.gStyle.GetColorPalette(int(round(zRatio*(ROOT.gStyle.GetNumberOfColors()-1))))
        e.SetMarkerColor(color)
        e.SetMarkerSize(markerSize)
        stuff.append(e)
#    h.Fill(d[0], d[1], 0) 
  for s in stuff:
    s.Draw()
  c1.Print(ofile)
  del h

dataPath = "/Users/robertschoefbeck//CloudStation/data/LFT/"

def readLimit(f):
  stringArg = "The highest r value is ="
  stringCMSSUS = "CMS-SUS-13-007"
  maxR=None
  cmsSUS_theoryT1tttt = None
  cmsSUS_experimentalLimit = None
  missingToposONs = ["[[[b,t],[W]],[[t,b],[W]]]","[[[b,t],[W]],[[b,t],[W]]]","[[[t,b],[W]],[[t,b],[W]]]"]
  missingToposONsXSecBR=0.
  missingToposOFFs = ["[[[b,t],[jet,jet]],[[t,b],[jet,jet]]]","[[[b,t],[jet,jet]],[[b,t],[jet,jet]]]","[[[t,b],[jet,jet]],[[t,b],[jet,jet]]]"]
  missingToposOFFsXSecBR=0.
  cmsSUS_r = 0.
  for l in file(f).readlines():
    if stringArg in l:
      maxR = float(l.split()[-1])
    if stringCMSSUS in l:
      cmsSUS_theoryT1tttt = float(l.split()[-3])
      cmsSUS_experimentalLimit = float(l.split()[-2])
      cmsSUS_r = float(l.split()[-1])
    for m in missingToposONs:
      if m in l:
        missingToposONsXSecBR+=float(l.split()[1])
    for m in missingToposOFFs:
      if m in l:
        missingToposOFFsXSecBR+=float(l.split()[1])
#  print "cmsSUS_experimentalLimit", cmsSUS_experimentalLimit
  newMaxR = (cmsSUS_theoryT1tttt + missingToposONsXSecBR)/cmsSUS_experimentalLimit if cmsSUS_experimentalLimit else 0.
  return {'maxR':maxR,\
          'cmsSUS_theoryT1tttt':cmsSUS_theoryT1tttt,\
          'cmsSUS_experimentalLimit':cmsSUS_experimentalLimit,\
          'missingToposONsXSecBR':missingToposONsXSecBR,\
          'missingToposOFFsXSecBR':missingToposOFFsXSecBR*(4./9.)**2,\
         'newMaxR':newMaxR, \
         'cmsSUS_r':cmsSUS_r,\
    }
 
def vec(res, key):
  return array.array('d', [r[key] for r in res])

files = os.listdir(dataPath+'/slha/')
#files = ['9902.txt']
#files = files[:10]
#prefix='mneu1_gr_70'
prefix='newExcl'
res=[]
for i, f in enumerate(files):
  if i%100==0:
    print i,'/',len(files)
  exclusions=readLimit(dataPath+'/smodelsOutputRun3/'+f)
#  exclR = exclusions['cmsSUS_r']
  exclR = exclusions['maxR']
  if exclR>1:
    continue
  if 'newExcl' in prefix and exclusions['newMaxR']>1:continue
#  print 'maxR',exclR, 'newMaxR',exclusions['newMaxR']
  slha=pyslha.readSLHAFile(dataPath+'/slha/'+f, ignoreblocks=['XSECTION'])
  mgl = slha.blocks['MASS'][1000021]
  xsecFromPythia=crossSection.getXsecFromSLHAFile(dataPath+'/slha/'+f)
  xsecFromPythia_gluinoPair= getXSec(xsecFromPythia, [1000021, 1000021])
#  xsecFromPythia_gluinoPair= xsecFromPythia_gluinoPair
  roundMgl= 5*int(round(mgl/5.))
  xsec_gluinoPair=gluinoXSec[roundMgl] if gluinoXSec.has_key(roundMgl) else 0
  if verbose:
    print "X-sec of gluino pair production (mgl=",roundMgl,"): 13 TeV:",gluino13TeV_NLONLL[roundMgl] if gluino13TeV_NLONLL.has_key(roundMgl) else None,\
          "(NLONLL) 8 TeV:", gluino8TeV_NLONLL[roundMgl] if gluino8TeV_NLONLL.has_key(roundMgl) else None, "(NLONNL)"
    print "X-sec of gluino pair production (",round(mgl,1),\
          ") Pythia 8 TeV: order:",xsecFromPythia_gluinoPair.value.asNumber()*modelReaderXSecUnitConversion if xsecFromPythia_gluinoPair else "n.c.",\
          "order",xsecFromPythia_gluinoPair.info.order if xsecFromPythia_gluinoPair else "n.c."

  mneu1 = abs(slha.blocks['MASS'][1000022])
  if 'mneu1_gr_70' in prefix and mneu1<70:continue
  if mgl<700:
    print f
    print exclusions['missingToposOFFsXSecBR']
  mcha1 = abs(slha.blocks['MASS'][1000024])
  mstop1 = abs(slha.blocks['MASS'][1000006])
  msbot1 = abs(slha.blocks['MASS'][1000005])
  br_gluinoToStop     = getBranching(slha, 1000021, [1000006, 6])
  br_stopToCha     = getBranching(slha, 1000006, [1000024, 5])

  br_sbotToCha     = getBranching(slha, 1000005, [1000024, 6])
  br_gluinoToSbottom  = getBranching(slha, 1000021, [1000005, 5])

  br_gluinoToCha     = getBranching(slha, 1000021, [1000024, 5, 6])
  br_ChaToNeu     = getTotalBranching(slha, 1000024, 1000022)
  if verbose:
    print 'BR: ~g to ~t_1 t',br_gluinoToStop, '~t_1->~chi^+_1 b',br_stopToCha
    print 'BR: ~g to ~b_1 b',br_gluinoToSbottom, '~b_1->~chi^+_1 t',br_sbotToCha
    print 'BR: ~g to ~chi^+_1 t b',br_gluinoToCha, 
    print '~chi^+_1 to ~chi^0_1', br_ChaToNeu
 
#  br_chaToNeu      = getBranching(slha, 1000024, [1000024, 6])
#  getBranching(slha, 1000006, [1000024, 6])
  BR_tbWtbW = ((br_gluinoToStop*br_stopToCha + br_gluinoToSbottom*br_sbotToCha + br_gluinoToCha)*br_ChaToNeu)**2
#  print mgl, mn, xsec_gluinoPair, exclR, "BR_gluinoPairToChaPair",BR_gluinoPairToChaPair
  res.append({'mgl':mgl, 'mneu1':mneu1, 'mcha1':mcha1, 'mstop1':mstop1, 'msbot1':msbot1,\
    'xsec_gluinoPair':xsec_gluinoPair, 
    'xsecBR_tbWtbW':xsec_gluinoPair*BR_tbWtbW,
    'BR_tbWtbW':BR_tbWtbW,
    'br_gluinoToStop':br_gluinoToStop,'br_gluinoToSbottom':br_gluinoToSbottom,'br_stopToCha':br_stopToCha,'br_sbotToCha':br_sbotToCha,'br_gluinoToCha':br_gluinoToCha,'br_ChaToNeu':br_ChaToNeu})


h = ROOT.TH1F('','',20,0,200)
for r in res:
  h.Fill(r['mcha1']-r['mneu1'])
c1 = ROOT.TCanvas()
h.Draw()
args=['dMEwkino']
if prefix!='':args=[prefix]+args
c1.Print('/Users/robertschoefbeck/Desktop/plots/'+'_'.join(args)+'.png')  

for zVar in [\
    'xsec_gluinoPair', 
    'xsecBR_tbWtbW', 'BR_tbWtbW', 'br_gluinoToStop', 'br_gluinoToSbottom', 'br_stopToCha', 'br_sbotToCha', 
#    'br_ChaToNeu'
    ]:
  allJobs = [ 
    {'firstVar':'mgl','firstBinning':[900,600,1500], 'secondBinning':[400,0,400], 'secondVar':'mneu1'}, 
    {'firstVar':'mgl','firstBinning':[900,600,1500], 'secondBinning':[400,0,400], 'secondVar':'mcha1'}, 
    {'firstVar':'mgl','firstBinning':[900,600,1500], 'secondBinning':[1000,250,1250], 'secondVar':'mstop1'}, 
    {'firstVar':'mgl','firstBinning':[900,600,1500], 'secondBinning':[1000,250,1250], 'secondVar':'msbot1'},
    {'secondVar':'mneu1','secondBinning':[400,0,400], 'firstBinning':[300,100,400], 'firstVar':'mcha1'},
  ]
  
  for job in allJobs:
    data = [(r[job['firstVar']], r[job['secondVar']], r[zVar]) for r in res if r[zVar]>0]
    if len(data)>0:
      data.sort(key=lambda x:x[2])
      h=ROOT.TH2F(zVar, '', *(job['firstBinning']+job['secondBinning']))
      h.Reset()
      h.GetXaxis().SetTitle("")
      h.GetYaxis().SetTitle("")
      ROOT.gStyle.SetOptStat(0)
      args=[job['firstVar'],job['secondVar'],zVar]
      if prefix!='':args=[prefix]+args
      scatterOnTH2(data, h, '/Users/robertschoefbeck/Desktop/plots/'+'_'.join(args)+'.png', 20, 0.5)
  
