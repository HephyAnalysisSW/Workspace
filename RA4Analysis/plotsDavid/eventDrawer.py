import ROOT
from math import pi, cos, sin, atan2, sqrt
from Workspace.HEPHYPythonTools.helpers import getChain
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v3 import *
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v6_Phys14V2_HT400_withDF import *

lepSel = 'hard'

#c = getChain(WJetsHTToLNu[lepSel],histname='')
#name = 'WJets'

c = getChain(ttJets[lepSel],histname='')
name = 'TTJets'

#c = getChain(SMS_T5qqqqWW_Gl1200_Chi1000_LSP800[lepSel],histname='')
#name = 'T5qqqqWW_Gl1200_Chi1000_LSP800'

#c = getChain(SMS_T5qqqqWW_Gl1500_Chi800_LSP100[lepSel],histname='')
#name = 'T5qqqqWW_Gl1500_Chi800_LSP100'

#  "T5qqqqWW_Gl_1400_LSP_300_Chi_315",
#  "T6qqWW_Sq_950_LSP_300_Chi_350",

#c = getChain(soft_T5qqqqWW_Gl_1400_LSP_300_Chi_315)
#name = 'T5qqqqWW_Gl_1400_LSP_300_Chi_315'

#c = getChain(soft_T6qqWW_Sq_950_LSP_300_Chi_350)
#name = 'soft_T6qqWW_Sq_950_LSP_300_Chi_350'



commoncf = "singleMuonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&htJet30j>400&&nBJetMediumCMVA30==0&&deltaPhi_Wl>1.0&&nJet30>=5"
#commoncf = "singleMuonic&&nLooseSoftLeptons==1&&nTightSoftLeptons==1&&nTightHardLeptons==0&&met>500&&htJet40ja>400&&nBJetMedium25==0&&nJet40a>=3"
c.Draw('>>eList', commoncf)
eList = ROOT.gDirectory.Get('eList')

n=100
for e in range(min([n, eList.GetN()])):
  stuff=[]
  c.GetEntry(eList.GetEntry(e))
  jets = [ [c.Jet_pt[i], c.Jet_phi[i], ROOT.kRed]  for i in range(c.nJet) if c.Jet_pt[i]>30 ]
  lepton = [c.leptonPt, c.leptonPhi, ROOT.kBlue]
  met = [c.met_pt, c.met_phi, ROOT.kGreen]

  all = jets+[lepton, met]
  maxPt = max([p[0] for p in all])
#  thrustPhi =  c.thrustPhi
  ref_phi = c.met_phi

  c1 = ROOT.TCanvas("c1", "c1", 0,0, 500, 500)
  c1.Range(-1.1, -1.1, 1.1, 1.1)
  ell = ROOT.TEllipse(0,0, 1)
  ell.Draw()

  if cos(ref_phi-lepton[1])>0:
    shift=0
  else:
    shift=pi

  for p in all:
    phi = p[1]-ref_phi+pi/2+shift
    pt = p[0]/maxPt
    l = ROOT.TArrow(0,0,pt*cos(phi),pt*sin(phi))
    l.SetLineColor(p[2])
    l.Draw()
    stuff.append(l)

  lines = [ [0.8, 0.15+0.8, "MET "+str(round(met[0],1))],\
            [0.8, 0.15+0.75, "l-pT "+str(round(lepton[0],1))],
            [0.8, 0.15+0.7, "ht "+str(round(c.htJet40ja,1))]
  ]
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.04)
  latex.SetTextAlign(11) # align right
  for line in lines:
      latex.SetTextSize(0.04)
      latex.DrawLatex(line[0],line[1],line[2])

  c1.Print('/afs/hephy.at/user/d/dhandl/www/pngEvents/'+name+'_'+str(e)+'.png')
