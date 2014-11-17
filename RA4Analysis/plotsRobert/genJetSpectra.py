import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from Workspace.HEPHYPythonTools.helpers import getFileList, getChain
fl = getFileList('/dpm/oeaw.ac.at/home/cms/store/user/schoef/T5Full_T5Full-1200-1000-800-Decay-MGMMatch50/T5Full_T5Full-1200-1000-800-Decay-MGMMatch50-Step0/42d2549c45b4fd5e74e09880357dd3d9/')[:100]
print "Adding ",len(fl),"files"
print ROOT.gDirectory.func()
h=ROOT.TH1F('pt','pt',300,0,300)
events=Events(fl)
nevents = events.size()
gjetsh=Handle("vector<reco::GenJet>")
for i in range(nevents):
#  print ROOT.gDirectory.func()
  if i%10000==0:
    print i,'/',nevents
  events.to(i)
  events.getByLabel(("ak4GenJets"),gjetsh)
  gjets = list(gjetsh.product())
  for j in gjets:
    h.Fill(j.pt())
c1 = ROOT.TCanvas()
h.Draw()
c1.SetLogy()
del events
   
