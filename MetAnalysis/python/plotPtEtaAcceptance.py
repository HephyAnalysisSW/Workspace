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
parser.add_option("--species", dest="species", default='all', type="string", action="store", help="samples:Which samples.")
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")

(options, args) = parser.parse_args()
print "options: sample",options.sample, 'prefix',options.prefix, 'species', options.species
if options.species=='all':
  species = allspecies
else:
  exec("species = [" +','.join(["'"+s+"'" for s in options.species.split(',')])+ "]")
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

acceptance = {}
for s in species:
  acceptance[s] = ROOT.TH2D('acc_'+s,'acc_'+s,60,-3,3,  45,0,1.5)
print species
#for k in pfTypes[1:]:
for s in species:
  cutString = '(candId=='+str(label[s])+')' 
  c1 = ROOT.TCanvas()
  c.Draw('candPt*cosh(candEta):candEta>>acc_'+s,cutString,'COLZ')#,"Sum$(candId=="+label(k)+")")
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_en_acc_'+s+'.png')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_en_acc_'+s+'.root')
  c.Draw('candPt:candEta>>acc_'+s,cutString,'COLZ')#,"Sum$(candId=="+label(k)+")")
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_pt_acc_'+s+'.png')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+prefix+options.sample+'_pt_acc_'+s+'.root')
