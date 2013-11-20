import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *

c = ROOT.TChain("Events")
c.Add('root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/schoef/MonoJetFullSim_SUSYTupelizer/stop300lsp270g200/histo_9_1_oEN.root')
n = c.GetEntries()
for i in range(n):
  c.GetEntry(i)
  met = c.GetLeaf(c.GetAlias('type1phiMet')).GetValue()
  if met>100:
    print "SUSY found! met=",met
  else:
    print "SUSY not found!"
