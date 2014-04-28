import ROOT 
import os
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import sqrt, sin, cos, atan2, pi
from Workspace.HEPHYPythonTools.helpers import getVarValue
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
parser.add_option("--maps", dest="maps", default='all', type="string", action="store", help="samples:Which samples.")
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")

(options, args) = parser.parse_args()
print "options: sample",options.sample, 'maps', options.maps, 'prefix',options.prefix
if options.maps=='all':
  maps = allMaps
else:
  exec("maps = [" +options.maps+ "]")
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

print "Entries", c.GetEntries()

c.SetBranchStatus("*", 0)
c.SetBranchStatus("candPt", 1)
#c.SetBranchStatus("candPdg", 1)
c.SetBranchStatus("candPhi", 1)
c.SetBranchStatus("candEta", 1)
c.SetBranchStatus("candId", 1)

occupancy = {}
energy = {}
for m in maps:
  k=m['name']
  m['occupancy'] = ROOT.TH2D('occ_'+k,'occ_'+k,  *(m['binning']))
  m['energy'] = ROOT.TH2D('en_'+k,'en_'+k,    *(m['binning']))

#for k in pfTypes[1:]:
for m in maps:
  cutString = '(candId=='+str(label[m['type']])+')' 
  c1 = ROOT.TCanvas()
  print m, cutString
  c.Draw('candPhi:candEta>>occ_'+m['name'],cutString,'COLZ')#,"Sum$(candId=="+label(k)+")")
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_occ_'+m['name']+'.png')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_occ_'+m['name']+'.root')
  c.Draw('candPhi:candEta>>en_'+m['name'],'cosh(candEta)*candPt*('+cutString+')','COLZ')#,"Sum$(candId=="+label(k)+")")
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_en_'+m['name']+'.png')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_en_'+m['name']+'.root')

  c.Draw('cosh(candEta)*candPt>>hTMP(200,0,100)','candEta>'+str(m['binning'][1])+'&&candEta<='+str(m['binning'][2])+'&&('+cutString+')')#,"Sum$(candId=="+label(k)+")")
  c1.SetLogx()
  c1.SetLogy()
  
  for eb in energyBins:
    name = "en_"+str(eb[0])
    enCut = "cosh(candEta)*candPt>="+str(eb[0])
    if eb[1]>0:
      name+="_"+str(eb[1])
      enCut += "&&cosh(candEta)*candPt<"+str(eb[1])
    c1 = ROOT.TCanvas()
    c.Draw('candPhi:candEta>>occ_'+m['name'],cutString+"&&"+enCut,'COLZ')#,"Sum$(candId=="+label(k)+")")
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_occ_'+m['name']+'_'+name+'.png')
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_occ_'+m['name']+'_'+name+'.root')
    c.Draw('candPhi:candEta>>en_'+m['name'],'cosh(candEta)*candPt*('+cutString+'&&'+enCut+')','COLZ')#,"Sum$(candId=="+label(k)+")")
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_en_'+m['name']+'_'+name+'.png')
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_en_'+m['name']+'_'+name+'.root')
     

