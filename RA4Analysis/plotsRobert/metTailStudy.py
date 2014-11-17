import ROOT
from Workspace.RA4Analysis.stage1Tuples import *
from Workspace.HEPHYPythonTools.helpers import getFileList
#sample = WJetsToLNu25ns 
sample = WJetsHTToLNu
c = ROOT.TChain('Events')
for b in sample['bins']:
  fl = getFileList(b['dir']) 
  print "Adding ",len(fl),"files"
  for f in fl:
    c.Add(f)


