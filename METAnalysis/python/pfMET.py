import ROOT 
import os
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import sqrt, sin, cos, atan2
from Workspace.HEPHYPythonTools.helpers import getVarValue

idir = '/data/schoef/MET_240314/Mu-DYJetsToLL-M50/'
fl = os.listdir(idir)
filelist=[]
c = ROOT.TChain('Events')
for f in fl:
  filelist.append(idir+'/'+f)
  c.Add(idir+'/'+f)
#        prefix = "root://hephyse.oeaw.ac.at/"#+subdirname

events = Events(filelist)
pfhandle = Handle("vector<reco::PFCandidate>")
events.toBegin()
labelpf = ("particleFlow")
#labelpfmet = ("pfMet")
labelpfmet = ("patPFMet")
#pfMethandle = Handle("vector<reco::PFMET>")
pfMethandle = Handle("float")

pftypes = ["X", "h", "e", "mu", "gamma", "h0", "h_HF", "egamma_HF"]
label = {"X":0,"h":1, "e":2, "mu":3,"gamma":4, 'h0':5, 'h_HF':6, 'egamma_HF':7, 0:"X",1:"h", 2:"e", 3:"mu",4:"gamma", 5:'h0', 6:'h_HF', 7:'egamma_HF'}

categories = [\
  ["h_mE", "h", -3., -1.5  ],
  ["h_mB", "h", -1.5, 0.   ],
  ["h_pB", "h", 0., 1.5    ],
  ["h_pE", "h", 1.5, 3.0    ],
  ["h0_mE", "h0", -3., -1.4  ],
  ["h0_mB", "h0", -1.4, 0.   ],
  ["h0_pB", "h0", 0., 1.4    ],
  ["h0_pE", "h0", 1.4, 3.0    ],
  ["h_mHF", 'h_HF', -5., -3.],
  ["h_mpF", 'h_HF', 3., 5.],
  ["egamma_mHF", 'egamma_HF', -5., -3.],
  ["egamma_pHF", 'egamma_HF', 3., 5.],
]


h = {}
for t in pftypes+['all']:
  h[t+"_x"] = ROOT.TH1F(t+"_x", t+"_x", 200,-200,200)
  h[t+"_y"] = ROOT.TH1F(t+"_y", t+"_y", 200,-200,200)

def calcMet(pfCands):
  return - sum(vecs[:-1],vecs[-1])

nEvents = c.GetEntries()
for i in range(nEvents):
  c.GetEntry(i)
  if i%100==0:
    print "\nEvent",i, "/",nEvents 
  events.to(i)
  events.getByLabel(labelpf,pfhandle)
#  events.getByLabel(labelpfmet,pfMethandle)
  pfc = pfhandle.product()
#  met = pfMethandle.product()[0]
#  met = pfMethandle.product()
#  vec_x = - sum([ pf.p4().Et()*cos(pf.phi()) for pf in pfc])
#  vec_y = - sum([ pf.p4().Et()*sin(pf.phi()) for pf in pfc])
#  myEMet = sqrt(vec_x**2 + vec_y**2) 
#  myEMetphi = atan2(vec_y, vec_x) 
  vecs={}
  for t in pftypes:
    vecs[t] = [] 
  for p in pfc: 
    p4 = p.p4()
    Et = p4.Et()
    phi = p4.phi()
    vecs[label[p.particleId()]].append([Et*cos(phi), Et*sin(phi)])
#  vecs = [ pf.p4() for pf in filter(lambda p:p.particleId()==5, pfc)]
  fullMetx=0.
  fullMety=0.
  for t in pftypes:
    myMetx = -sum([v[0] for v in vecs[t]]) 
    myMety = -sum([v[1] for v in vecs[t]])
    h[t+"_x"].Fill(myMetx)
    h[t+"_y"].Fill(myMety)
    fullMetx+=myMetx 
    fullMety+=myMety 
  h["all_x"].Fill(fullMetx)
  h["all_y"].Fill(fullMety)
#    print sqrt(myMetx**2+myMety**2)
#  print vecs[-1].pt()
#  print met.pt(),met.phi()
#  met = getVarValue(c, 'patPFMet')
#  metphi = getVarValue(c, 'patPFMetphi')
#  print met, metphi 
#  print sqrt(fullMetx**2+fullMety**2) 
#  print myMet.pt(),myMet.phi()
#    print myEMet, myEMetphi

for t in pftypes+["all"]:
  c1= ROOT.TCanvas()
  h[t+"_x"].Draw()
  c1.SetLogy()
  h[t+"_y"].SetLineColor(ROOT.kRed)
  h[t+"_y"].Draw('same')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+t+".png")
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+t+".root")
  
