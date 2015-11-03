import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import *# getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName
#from Workspace.RA4Analysis.cmgTuplesPostProcessed_v8_Phys14V3_HT400ST200 import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_HT500ST250_postProcessed_fromArthur import *


from math import sqrt, pi, cosh
from array import array

def filterParticles(l, values, attribute):
  for a in l:
    for v in values:
      if abs(a[attribute])==v: yield a

def getWMass(c):
  para = ['pt','phi','eta','pdgId','motherId']
  genPartAll = [getObjDict(c, 'genPartAll_', para, j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  Neutrinos = []
  Leptons = []
  NeutrinosFromW = []
  NeutrinosFromTau = []
  LeptonsFromW = []
  LeptonsFromTau = []
  for Neutrino in filterParticles(genPartAll, [12,14], 'pdgId'):
    Neutrinos.append(Neutrino)
  for NeutrinoFromW in filterParticles(Neutrinos, [24], 'motherId'):
    NeutrinosFromW.append(NeutrinoFromW)
  #for NeutrinoFromTau in filterParticles(Neutrinos, [15], 'motherId'):
  #  NeutrinosFromTau.append(NeutrinoFromTau)
  for Lepton in filterParticles(genPartAll, [11,13], 'pdgId'):
    Leptons.append(Lepton)
  for LeptonFromW in filterParticles(Leptons, [24], 'motherId'):
    LeptonsFromW.append(LeptonFromW)
  #for LeptonFromTau in filterParticles(Leptons, [15], 'motherId'):
  #  LeptonsFromTau.append(LeptonFromTau)
  WMass = 0.
  if len(NeutrinosFromW)>0:
    if len(NeutrinosFromW)>1: print 'this should not have happened'
    if len(LeptonsFromW)>0:
      if len(LeptonsFromW)>1: print 'this should not have happened'
      LeptonPt = LeptonsFromW[0]['pt']
      LeptonPhi = LeptonsFromW[0]['phi']
      LeptonEta = LeptonsFromW[0]['eta']
      NeutrinoPt = NeutrinosFromW[0]['pt']
      NeutrinoPhi = NeutrinosFromW[0]['phi']
      NeutrinoEta = NeutrinosFromW[0]['eta']
      WMass = sqrt(2*LeptonPt*NeutrinoPt*(cosh(LeptonEta-NeutrinoEta)-cos(LeptonPhi-NeutrinoPhi)))
  #else: 
  #  print 'No promt neutrino found'
  #  if len(NeutrinosFromTau)>0:
  #    print 'But found', len(NeutrinosFromTau), 'neutrinos from tau'
  #    if len(NeutrinosFromTau)>1: print 'this should not have happened'
  #    if len(LeptonsFromTau)>0:
  #      if len(LeptonsFromTau)>1: print 'this should not have happened'
  #      LeptonPt =    LeptonsFromTau[0]['pt']
  #      LeptonPhi =   LeptonsFromTau[0]['phi']
  #      LeptonEta =   LeptonsFromTau[0]['eta']
  #      NeutrinoPt =  NeutrinosFromTau[0]['pt']
  #      NeutrinoPhi = NeutrinosFromTau[0]['phi']
  #      NeutrinoEta = NeutrinosFromTau[0]['eta']
  #      WMass = sqrt(2*LeptonPt*NeutrinoPt*(cosh(LeptonEta-NeutrinoEta)-cos(LeptonPhi-NeutrinoPhi)))
  #      print WMass
  if WMass < 1.:
    WMass = float('nan')
  return WMass

def getNeutrino(c):
  para = ['pt','phi','eta','pdgId','motherId']
  genPartAll = [getObjDict(c, 'genPartAll_', para, j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  #Neutrino = [i for i in genPartAll if (abs(i['pdgId'])==14 or abs(i['pdgId'])==12)]
  Neutrinos = []
  NeutrinosFromW = []
  for Neutrino in filterParticles(genPartAll, [12,14], 'pdgId'):
    Neutrinos.append(Neutrino)
  for NeutrinoFromW in filterParticles(Neutrinos, [24], 'motherId'):
    NeutrinosFromW.append(NeutrinoFromW)
  #Neutrino = filter(lambda w:(abs(w['pdgId'])==14 or abs(w['pdgId'])==12), genPartAll)
  #NeutrinoFromW = filter(lambda w:abs(w['motherId'])==24, Neutrino)
  metGenPhi = c.GetLeaf('met_genPhi').GetValue()
  metGenPt = c.GetLeaf('met_genPt').GetValue()
  if len(NeutrinosFromW)>0:
    if len(NeutrinosFromW)>1: print 'this should not have happened'
    NeutrinoPt = NeutrinosFromW[0]['pt']
    NeutrinoPhi = NeutrinosFromW[0]['phi']
    return NeutrinoPt, NeutrinoPhi, metGenPt
  else: return 0., 0.

lepSel = 'hard'

#WJETS  = getChain(WJetsHTToLNu[lepSel],histname='')
WJETS  = getChain(WJetsHT_25ns,histname='')

streg = [[(450,-1), 1.]]#, [(350, 450), 1.],  [(450, -1), 1.] ]
htreg = [(500,750)]#,(750,1000),(1000,-1)]#,(1000,1250),(1250,-1)]#,(1250,-1)]
btreg = (0,0)
njreg = [(2,2),(3,3),(4,4),(5,5),(6,7),(8,-1)]#,(7,7),(8,8),(9,9)]
nbjreg = [(0,0),(1,1),(2,2)]

presel='singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftPt10Leptons==0&&Jet_pt[1]>80&&(sqrt((-met_genPt*cos(met_genPhi)+met_pt*cos(met_phi))**2+(-met_genPt*sin(met_genPhi)+met_pt*sin(met_phi))**2)/met_genPt)<1'
colors = [ROOT.kBlue+2, ROOT.kBlue-7, ROOT.kCyan-9, ROOT.kCyan-2, ROOT.kGreen-6, ROOT.kOrange-4, ROOT.kOrange+8, ROOT.kRed+1]
first = True

can = ROOT.TCanvas('c1','c1',800,600)
can.SetLogy()
Whists = {}

newpresel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&st>250&&nJet30>=2&&htJet30j>500&&Jet_pt[1]>80"

stb = (250,-1)
htb = (500,-1)
njb = (3,-1)
btreg = (0,0)

cname, cut = nameAndCut(stb,htb,njb, btb=btreg ,presel=newpresel)
dPhiStr = 'deltaPhi_Wl'
WJETS.Draw('>>eList',cut)
elist = ROOT.gDirectory.Get("eList")
number_events = elist.GetN()

print 'Will loop over',number_events, 'events, patience please'

WmassHist = ROOT.TH1F('Whist_lowMass','low W mass',100,0,1000)
Whist_lowMass = ROOT.TH1F('Whist_lowMass','low W mass',16,0,3.2)
Whist_highMass = ROOT.TH1F('Whist_lowMass','low W mass',16,0,3.2)
Whist_lowMass.SetLineColor(ROOT.kBlue)
Whist_highMass.SetLineColor(ROOT.kRed)

for stb, dPhiCut in streg:
  Whists[stb] = {}
  for i_htb, htb in enumerate(htreg):
    Whists[stb][htb] = {}
    totalL = ROOT.TLegend(0.6,0.6,0.95,0.93)
    totalL.SetFillColor(ROOT.kWhite)
    totalL.SetShadowColor(ROOT.kWhite)
    totalL.SetBorderSize(1)
    for i_njb, njb in enumerate(njreg):
      print 'Processing njet',njb
      cname, cut = nameAndCut(stb,htb,njb, btb=btreg ,presel=presel)


for i in range(number_events):
  if i>0 and (i%10000)==0: print "Filled ",i
  WJETS.GetEntry(elist.GetEntry(i))
  weight = getVarValue(WJETS,"weight")
  deltaPhi = WJETS.GetLeaf(dPhiStr).GetValue()
  WMass = getWMass(WJETS)
  #print WMass
  WmassHist.Fill(WMass,weight)
  if WMass>100.:
    Whist_highMass.Fill(deltaPhi,weight)
  else:
    Whist_lowMass.Fill(deltaPhi,weight)

highMassYield = Whist_highMass.Integral()
lowMassYield  = Whist_lowMass.Integral()

Whist_lowMass.Scale(1/Whist_lowMass.Integral())
Whist_highMass.Scale(1/Whist_highMass.Integral())


#for stb, dPhiCut in streg:
#  Whists[stb] = {}
#  for i_htb, htb in enumerate(htreg):
#    Whists[stb][htb] = {}
#    totalL = ROOT.TLegend(0.6,0.6,0.95,0.93)
#    totalL.SetFillColor(ROOT.kWhite)
#    totalL.SetShadowColor(ROOT.kWhite)
#    totalL.SetBorderSize(1)
#    for i_njb, njb in enumerate(njreg):
#      print 'Processing njet',njb
#      cname, cut = nameAndCut(stb,htb,njb, btb=btreg ,presel=presel)
#      dPhiStr = 'deltaPhi_Wl'
#      WJETS.Draw('>>eList',cut)
#      elist = ROOT.gDirectory.Get("eList")
#      number_events = elist.GetN()
#      Whists[stb][htb][njb] = {'hist':ROOT.TH1F('h'+str(i_njb),str(njb),50,0,500)}
#      Whists[stb][htb][njb]['hist'].Sumw2()
#      counter = 0.
#      total = 0.
#      for i in range(number_events):
#        WJETS.GetEntry(elist.GetEntry(i))
#        weight = getVarValue(WJETS,"weight")
#        deltaPhi = WJETS.GetLeaf(dPhiStr).GetValue()
#        WMass = getWMass(WJETS)
#        deltaPhi = WJETS.GetLeaf(dPhiStr).GetValue()
#        if WMass>100.:
#          #print WMass, deltaPhi, weight
#          if deltaPhi>1.:
#            counter += weight
#          total += weight
#        #if abs(neutrinoPt-genMetPt)<5:
#        #  h.Fill(deltaPhi, weight)
#        Whists[stb][htb][njb]['hist'].Fill(WMass, weight)
#      Whists[stb][htb][njb]['hist'].SetLineColor(colors[i_njb])
#      totalL.AddEntry(Whists[stb][htb][njb]['hist'])
#      print 'Ratio of deltaPhi>1 in M(W)>100', counter/(total-counter)
#      if first:
#        Whists[stb][htb][njb]['hist'].Draw('hist')
#        first = False
#      else: Whists[stb][htb][njb]['hist'].Draw('hist same')
      
