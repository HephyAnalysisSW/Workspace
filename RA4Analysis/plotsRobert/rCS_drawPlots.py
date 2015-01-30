import ROOT
from array import array
from math import *
import os, copy, sys
from Workspace.RA4Analysis.helpers import nJetBinName, nBTagBinName, nameAndCut

#ROOT.TH1F().SetDefaultSumw2()
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks
import Workspace.HEPHYPythonTools.xsec as xsec
#from Workspace.RA4Analysis.simplePlotsCommon import *
from Workspace.RA4Analysis.helpers import *

from draw_helpers import *

from Workspace.RA4Analysis.cmgTuples_v5_Phys14 import WJetsToLNu_HT100to200_fromEOS, WJetsToLNu_HT200to400_fromEOS, WJetsToLNu_HT400to600_fromEOS, WJetsToLNu_HT600toInf_fromEOS, ttJets_fromEOS
ROOT_colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kCyan]
samples=[WJetsToLNu_HT100to200_fromEOS, WJetsToLNu_HT200to400_fromEOS, WJetsToLNu_HT400to600_fromEOS, WJetsToLNu_HT600toInf_fromEOS,ttJets_fromEOS]
totalYield=0
for s in samples:
  cs=getChunks(s, treeName="treeProducerSusySingleLepton")
  s.update(cs[0][0])
  s['chain']=ROOT.TChain('tree')
  s['chain'].Add(s['file'])
  s["weight"]=4000*xsec.xsec[s['dbsName']]/float(cs[1])
  nEntry=s['chain'].GetEntries()
  totalYield+=4000*xsec.xsec[s['dbsName']]/float(cs[1])*nEntry
  print s["name"],"xsec",xsec.xsec[s['dbsName']],"NSim",cs[1],"nEntry",nEntry, "yield:",4000*xsec.xsec[s['dbsName']]/float(cs[1])*nEntry
print "totalYield", totalYield

htb= (400)
stb= 250
prefix=None

leptonMinPt=25

#lepton="muon"; muMultiplicity=1; eleMultiplicity=0; minID=1; minRelIso=0.12
#lepton="electron"; muMultiplicity=0; eleMultiplicity=1; minID=3; minRelIso=0.14
#minRelIso=0.25

for lepton in ["electron", "muon"]:
  if lepton=="muon":
     muMultiplicity=1; eleMultiplicity=0; minID=1; minRelIso=0.12
  if lepton=="electron":
     muMultiplicity=0; eleMultiplicity=1; minID=3; minRelIso=0.14
  for htb in [(500,-1), (500,750), (750,-1), (750,1000), (1000,-1)]:
#  for htb in [(500,-1)]:
    for stb in [(250,350), (350,-1), (250,-1), (350,450), (450,-1)]:
#    for stb in [(250,-1)]:
      name = nameAndCut(stb, htb, njetb=None, btb=None)[0]
      fname="_".join(([prefix] if prefix else [])+[lepton,name])
      plots={}
      njet_bins = [(2,3), (4,4),(5,5),(6,-1)]
      nbtag_bins = [0,1,2,3,4,5]
      for njb in njet_bins: 
        #njb= 5

        cut= "&&".join([
            exactlyOneTightLepton(lepton=lepton, minPt=leptonMinPt, maxEta=2.4, minID=minID, minRelIso=minRelIso),\
            looseLeptonVeto(minPt=10, muMultiplicity=muMultiplicity, eleMultiplicity=eleMultiplicity), \
            nJetCut(njb=njb, minPt=30, maxEta=2.4), \
            htCut  (htb=htb, minPt=30, maxEta=2.4), \
            stCut(lepton=lepton, stb=stb, minPt=leptonMinPt, maxEta=2.4, minID=minID, minRelIso=minRelIso), \
            ])

        rCS_vs_nbtag = ROOT.TProfile('profile_rCS','', len(nbtag_bins)-1, array('d',nbtag_bins), 0, 1)
        print "lepton", lepton, "htb", htb, "stb", stb, "njb", njb, "cut:", cut
        #rCS_vs_nbtag.Reset()
        ttJets_fromEOS['chain'].Draw(dPhiCut(minDPhi=1, lepton=lepton,minPt=leptonMinPt, maxEta=2.4, minID=minID, minRelIso=minRelIso)+":"+nBTagStr(minPt=30, maxEta=2.4, minCMVATag=0.732)+'>>profile_rCS',cut,'goff') 
        plots[njb]=ROOT.gDirectory.Get('profile_rCS').Clone()

      opt=""
      c1 = ROOT.TCanvas()
      l=ROOT.TLegend(0.7,0.7,1.0,1.0)
      l.SetFillColor(ROOT.kWhite)
      l.SetShadowColor(ROOT.kWhite)
      l.SetBorderSize(1)
      for i_njb,njb in enumerate(njet_bins):
        ROOT.gStyle.SetOptStat(0)
        plots[njb].GetYaxis().SetRangeUser(0,0.2)
        plots[njb].SetLineColor(ROOT_colors[i_njb])
        plots[njb].Draw(opt)
        l.AddEntry(plots[njb], nJetBinName(njb))
        if opt=="":
          opt="same"

      l.Draw()
      c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngRCS/'+fname+'.png')

