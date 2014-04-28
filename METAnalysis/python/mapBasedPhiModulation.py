import ROOT
import os
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import sqrt, sin, cos, atan2, pi, cosh
from Workspace.HEPHYPythonTools.helpers import getVarValue, getObjFromFile
#sample = 'minBiasData'
from commons import *

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/useNiceColorPalette.C")

ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
#ROOT.gStyle.SetPadRightMargin(0.10);
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()
ROOT.tdrStyle.SetPadRightMargin(0.18)
ROOT.useNiceColorPalette(255)

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--sample", dest="sample", default="dy53X", type="string", action="store", help="samples:Which samples.")
parser.add_option("--prefix", dest="prefix", default="", type="string", action="store", help="prefix:Which prefix.")
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")

(options, args) = parser.parse_args()
print "options: sample",options.sample#, 'maps', options.maps, 'prefix',options.prefix
#if options.maps=='all':
#  maps = allMaps
#else:
#  exec("maps = [" +options.maps+ "]")
prefix=""
if options.prefix!='':
  prefix = options.prefix+'_'

c = ROOT.TChain('Events')

if options.sample == 'dy53X':
#sample = 'MinimumBias-Run2012A-22Jan2013'
  if options.small:
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_from0To1.root')
  else:
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*.root')
if options.sample.lower().count('doublemu') or options.sample.lower().count('minimumbias'):
  if options.small:
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_0.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_1.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_2.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_3.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_4.root')
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*_5.root')
  else:
    c.Add('/data/schoef/convertedMETTuples_v2/inc/'+options.sample+'/histo_'+options.sample+'*.root')


c.SetBranchStatus("*", 0)
c.SetBranchStatus("candPt", 1)
c.SetBranchStatus("ht", 1)
c.SetBranchStatus("candPhi", 1)
c.SetBranchStatus("candEta", 1)
c.SetBranchStatus("candId", 1)

map = h
eb = energyBins[1]

ifile = '/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+options.sample+'_occ_'+map['name']+'_pt_'+str(eb[0])+'_'+str(eb[1])+'.root'
f = ROOT.TFile(ifile)
k = f.GetListOfKeys()[0].GetName()
f.Close()
canv = getObjFromFile(ifile, k)
occ = canv.GetPrimitive('occ_'+map['name']).Clone()

ifile = '/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+options.sample+'_en_'+map['name']+'_pt_'+str(eb[0])+'_'+str(eb[1])+'.root'
f = ROOT.TFile(ifile)
k = f.GetListOfKeys()[0].GetName()
f.Close()
canv = getObjFromFile(ifile, k)
en = canv.GetPrimitive('en_'+map['name']).Clone()

a = occ.GetXaxis()
etaBinning = [a.GetNbins(), a.GetXmin(),  a.GetXmax()]

projOcc={}
projEn={}
for i in range(1,1+etaBinning[0]):
  h=occ.ProjectionY('occ_'+str(i),i,i)
  integr = h.Integral()
  if integr>0:
    h.Scale(h.GetNbinsX()/integr)
  projOcc[i] = h
  h=en.ProjectionY('en_'+str(i),i,i)
  integr = h.Integral()
  if integr>0:
    h.Scale(h.GetNbinsX()/integr)
  projEn[i] = h

metPhi = ROOT.TH1F('metPhi','metPhi',30,-pi,pi)
metPhiCorr = ROOT.TH1F('metPhiCorr','metPhiCorr',30,-pi,pi)
metPhiCorrPt = ROOT.TH1F('metPhiCorrPt','metPhiCorrPt',30,-pi,pi)
met = ROOT.TH1F('met','met',100,0,100)
metCorr = ROOT.TH1F('metCorr','metCorr',100,0,100)
metCorrPt = ROOT.TH1F('metCorrPt','metCorrPt',100,0,100)
metx = ROOT.TH1F('metx','metx',100,-100,100)
metxCorr = ROOT.TH1F('metxCorr','metxCorr',100,-100,100)
metxCorrPt = ROOT.TH1F('metxCorrPt','metxCorrPt',100,-100,100)
mety = ROOT.TH1F('mety','mety',100,-100,100)
metyCorr = ROOT.TH1F('metyCorr','metyCorr',100,-100,100)
metyCorrPt = ROOT.TH1F('metyCorrPt','metyCorrPt',100,-100,100)

cut="(1)"
if options.prefix[:2] == 'ht':
  cut = 'ht>'+options.prefix[2:] 
c.Draw(">>eList", cut)
eList = ROOT.gDirectory.Get('eList')
n = eList.GetN()
print "cut",cut,"Entries", n

#nEvents = min([1000, n])
nEvents = min([30000, n])
for i in range(nEvents):
  c.GetEntry(eList.GetEntry(i))
  if i%100==0:print "At",i,"/",nEvents
  mexUncorr = 0.
  meyUncorr = 0.
  mexCorr = 0.
  meyCorr = 0.
  mexCorrPt = 0.
  meyCorrPt = 0.
  c.GetEntry(i)
  nCand = getVarValue (c, 'nCand')
  counter=0
  for j in range(int(nCand)):
    if label[getVarValue(c, 'candId', j)] == map['type']:
      eta = getVarValue (c, 'candEta', j)
      pt = getVarValue (c, 'candPt', j)
      en = pt*cosh(eta)
      if en>=eb[0] and en<eb[1]:
        if eta>=map['binning'][1] and eta<map['binning'][2]:
          counter+=1
          etaBin =  a.FindBin(eta)
          phi = getVarValue (c, 'candPhi', j)
          phiBin = projOcc[etaBin].FindBin(phi)
          resOcc = projOcc[etaBin].GetBinContent(phiBin)
          weightOcc=1.
          if resOcc>0:
            weightOcc=1./resOcc
          resEn = projEn[etaBin].GetBinContent(phiBin)
          weightEn=1.
          if resEn>0:
            weightEn=1./resEn
  #        print i,j,weight,'pt',pt,'eta',eta,'phi',phi
          cp = cos(phi)
          sp = sin(phi)
          dmx=cp*pt
          dmy=sp*pt
          mexUncorr-=dmx
          meyUncorr-=dmy
          mexCorr-=dmx*weightOcc
          meyCorr-=dmy*weightOcc
          mexCorrPt-=dmx*weightEn
          meyCorrPt-=dmy*weightEn
  if counter>0:
    metPhi.Fill(atan2(meyUncorr, mexUncorr))
    metPhiCorr.Fill(atan2(meyCorr, mexCorr))
    metPhiCorrPt.Fill(atan2(meyCorrPt, mexCorrPt))
    met.Fill(sqrt(mexUncorr**2+meyUncorr**2))
    metCorr.Fill(sqrt(mexCorr**2+meyCorr**2))
    metCorrPt.Fill(sqrt(mexCorrPt**2+meyCorrPt**2))
    metx.Fill(mexUncorr)
    metxCorr.Fill(mexCorr)
    metxCorrPt.Fill(mexCorrPt)
    mety.Fill(meyUncorr)
    metyCorr.Fill(meyCorr)
    metyCorrPt.Fill(meyCorrPt)

c1 = ROOT.TCanvas()
metPhi.SetLineColor(ROOT.kBlue)
metPhi.Draw()
metPhiCorr.SetLineColor(ROOT.kRed)
metPhiCorr.Draw('same')
metPhiCorrPt.SetLineColor(ROOT.kGreen)
metPhiCorrPt.Draw('same')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+'metPhi_comparison_'+options.sample+'_'+map['name']+'_pt_'+str(eb[0])+'_'+str(eb[1])+'.png')

c1 = ROOT.TCanvas()
met.SetLineColor(ROOT.kBlue)
met.Draw()
metCorr.SetLineColor(ROOT.kRed)
metCorr.Draw('same')
metCorrPt.SetLineColor(ROOT.kGreen)
metCorrPt.Draw('same')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+'met_comparison_'+options.sample+'_'+map['name']+'_pt_'+str(eb[0])+'_'+str(eb[1])+'.png')

c1 = ROOT.TCanvas()
metx.SetLineColor(ROOT.kBlue)
metx.Draw()
metxCorr.SetLineColor(ROOT.kRed)
metxCorr.Draw('same')
metxCorrPt.SetLineColor(ROOT.kGreen)
metxCorrPt.Draw('same')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+'metx_comparison_'+options.sample+'_'+map['name']+'_pt_'+str(eb[0])+'_'+str(eb[1])+'.png')

c1 = ROOT.TCanvas()
mety.SetLineColor(ROOT.kBlue)
mety.Draw()
metyCorrPt.SetLineColor(ROOT.kGreen)
metyCorrPt.Draw('same')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+'mety_comparison_'+options.sample+'_'+map['name']+'_pt_'+str(eb[0])+'_'+str(eb[1])+'.png')

