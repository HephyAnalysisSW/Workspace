import ROOT
from math import pi, cos, sin, atan2, sqrt
c = ROOT.TChain('Events')
#ifile = '/data/schoef/convertedTuples_v22/copy/T5LNu_1000_0/histo_T5LNu_1000_0.root'
#name = 'T5LNu_1000_0'

ifile='/data/schoef/convertedTuples_v22/copy/WJetsHT150v2/histo_WJetsHT150v2_*.root'
name = 'WJetsHT150v2'

c.Add(ifile)
commoncf = "njets>=4&&ht>400&&nTightMuons+nTightElectrons==1&&nbtags==0&&(ht>750&&met>350)&&htThrustLepSideRatio>0.4"
c.Draw('>>eList', commoncf)
eList = ROOT.gDirectory.Get('eList')

n=100
for e in range(min([n, eList.GetN()])):
  stuff=[]
  c.GetEntry(eList.GetEntry(e))
  jets = [ [c.jetPt[i], c.jetPhi[i], ROOT.kRed]  for i in range(c.njets) ]
  lepton = [c.leptonPt, c.leptonPhi, ROOT.kBlue]
  met = [c.type1phiMet, c.type1phiMetphi, ROOT.kGreen]

  all = jets+[lepton, met]
  maxPt = max([p[0] for p in all])
  thrustPhi =  c.thrustPhi

  c1 = ROOT.TCanvas("c1", "c1", 0,0, 500, 500)
  c1.Range(-1.1, -1.1, 1.1, 1.1)
  ell = ROOT.TEllipse(0,0, 1)
  ell.Draw()

  if cos(thrustPhi-lepton[1])>0:
    shift=0
  else:
    shift=pi

  for p in all:
    phi = p[1]-thrustPhi+pi/2+shift
    pt = p[0]/maxPt
    l = ROOT.TArrow(0,0,pt*cos(phi),pt*sin(phi))
    l.SetLineColor(p[2])
    l.Draw()
    stuff.append(l)

  lines = [ [0.8, 0.15+0.8, "MET "+str(round(met[0],1))],\
            [0.8, 0.15+0.75, "l-pT "+str(round(lepton[0],1))],
            [0.8, 0.15+0.7, "ht "+str(round(c.ht,1))]
  ]


  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.04)
  latex.SetTextAlign(11) # align right
  for line in lines:
      latex.SetTextSize(0.04)
      latex.DrawLatex(line[0],line[1],line[2])

  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngT5LNu/Events/'+name+'_'+str(e)+'.png')
