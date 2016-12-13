import ROOT
import pickle
import copy, os, sys

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/WPolarizationVariation.C+")
#ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
#ROOT.TH1F().SetDefaultSumw2()
#ROOT.setTDRStyle()
ROOT.gStyle.SetMarkerStyle(1)
ROOT.gStyle.SetOptTitle(0)

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.helpers import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_fromArtur import *
from Workspace.RA4Analysis.cmgTuples_data_25ns_fromArtur import *
from draw_helpers import *
from math import *
from Workspace.HEPHYPythonTools.user import username

picklePath = '/data/'+username+'/results2015/WPolarizationEstimation/'
picklePresel = '20151028_wjetsPolSys_pkl'

signalRegion = {(5, -1):{(250, -1): {(500, -1):   {'deltaPhi': 1.0}}},#Preselection
                (3, 4): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #3-4jets QCD and W+jets control region
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (4, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}, #4-5jets TTbar control region
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0},
                                      (500, -1):   {'deltaPhi': 0.75},
                                      (500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (5, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}},  #signal regions
                         (350, 450): {(500, -1):   {'deltaPhi': 1.0}},
                         (450, -1):  {(500, -1):   {'deltaPhi': 1.0}}},
                (6, 7): {(250, 350): {(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                         (350, 450): {(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                          (450, -1): {(500, 1000): {'deltaPhi': 0.75},
                                      (1000, -1):  {'deltaPhi': 0.75}}},
                (8, -1): {(250, 350):{(500, 750):  {'deltaPhi': 1.0},
                                      (750, -1):   {'deltaPhi': 1.0}},
                          (350, 450):{(500, -1):   {'deltaPhi': 0.75}},
                          (450, -1): {(500, -1):   {'deltaPhi': 0.75}}}
}

signalRegion = {(5, -1): {(250, -1): {(500, -1):   {'deltaPhi': 1.0}}}}
btreg = [(0,0)]#,(1,-1)]

targetLumi = 3000#pb-1
def getWeight(nEvents,targetLumi,sample=''):
  weight = targetLumi/nEvents
  return weight

def getGenWandLepton(c):
  genPartAll = [getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], j) for j in range(int(c.GetLeaf('nGenPart').GetValue()))]
  lepton = filter(lambda l:abs(l['pdgId']) in [11,13,15], genPartAll)
  #lepton = filter(lambda l:abs(l['pdgId']) == 13, genPartAll)
  #lepton = filter(lambda l:abs(l['pdgId']) == 11, genPartAll)
  if len(lepton)==0:
    print "no generated lepton found!"
    p4w=False
    p4lepton=False
    return p4w, p4lepton
  #lFromW = filter(lambda w:abs(w['motherId'])==24, lepton)
  lFromW = filter(lambda w:w['motherId']==(-24), lepton)
#  if len(lFromW)==0: #W->tau,nu->mu,nu||ele,nu
#    print 'W via tau'
#    lFromTau = filter(lambda w:abs(w['motherId'])==15, lepton)
#    if len(lFromTau)==1:
#      genTau = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], int(lFromTau[0]['motherIndex']))
#      if abs(genTau['motherId'])!=24: print '2)this should not have happened', genTau
#      genW = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], int(genTau['motherIndex']))
#      lep = ROOT.TLorentzVector()
#      lep.SetPtEtaPhiM(lFromTau[0]['pt'],lFromTau[0]['eta'],lFromTau[0]['phi'],lFromTau[0]['mass'])
#    elif len(lFromTau)>1:
#      print '1)this should not have happened', lFromTau
#      for j,l in enumerate(lFromTau):
#        genTau = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], int(l['motherIndex']))
#        if abs(genTau['motherId'])==24:
#          genW = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], int(genTau['motherIndex']))
#          lep = ROOT.TLorentzVector()
#          lep.SetPtEtaPhiM(l['pt'],l['eta'],l['phi'],l['mass'])
  if len(lFromW)==0:
    test = filter(lambda w:w['motherId']==24, lepton)
    if len(test)==0: print '2)this should not have happened'
    p4w=False
    p4lepton=False
    return p4w, p4lepton
  elif len(lFromW)>0:
    if len(lFromW)>1: print '3)this should not have happened'
    if abs(lFromW[0]['motherId'])!=24: print '4)this should not have happened'
    genW = getObjDict(c, 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], int(lFromW[0]['motherIndex']))
    lep = ROOT.TLorentzVector()
    lep.SetPtEtaPhiM(lFromW[0]['pt'],lFromW[0]['eta'],lFromW[0]['phi'],lFromW[0]['mass'])
  if abs(genW['pdgId'])!=24: '5)this should not have happened'
  W = ROOT.TLorentzVector()
  W.SetPtEtaPhiM(genW['pt'],genW['eta'],genW['phi'],genW['mass'])
  p4lepton = ROOT.LorentzVector(lep.Px(),lep.Py(),lep.Pz(),lep.E())
  p4w = ROOT.LorentzVector(W.Px(),W.Py(),W.Pz(),W.E())
  return p4w, p4lepton

e_tight   = "(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<=2.5&&LepGood_miniRelIso<0.1&&LepGood_SPRING15_25ns_v1==4)" 
n_tight_e =  "(Sum$("+e_tight+"))"
e_veto    = "(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<=2.5&&!("+e_tight+"))"
n_veto_e  ="(Sum$("+e_veto+"))"
mu_tight = "(abs(LepGood_pdgId)==13&&LepGood_pt>=10&&abs(LepGood_eta)<=2.4&&LepGood_mediumMuonId==1&&LepGood_sip3d<4&&LepGood_miniRelIso<0.2)"
n_tight_mu = "(Sum$("+mu_tight+"))"
mu_veto  = "(abs(LepGood_pdgId)==13&&LepGood_pt>=10&&abs(LepGood_eta)<=2.5&&!("+mu_tight+"))"
n_veto_mu = "(Sum$("+mu_veto+"))"

##OneLep = "("+mu_tight+"+"+e_tight+"==1"+")"
#OneLep = "(Sum$("+n_tight_mu+"||"+n_tight_e+")==1)" 
OneLep = "("+n_tight_mu+"+"+n_tight_e+"==1)"
OneMu = "("+n_tight_mu+"==1"+")"
OneMu_lepveto = "("+n_veto_mu+"==0&&"+n_veto_e+"==0&&"+n_tight_e+"==0"+")"
OneE = "("+n_tight_e+"==1"+")"
OneE_lepveto = "("+n_veto_e+"==0&&"+n_veto_mu+"==0&&"+n_tight_mu+"==0"+")"
#lep_hard  = "LepGood_pt[0]>25"
lep_hard  = "((LepGood_pt>25)*"+"("+mu_tight+"||"+e_tight+"))"
OneLep_lepveto =  "(("+"abs(LepGood_pdgId)==11&&"+OneE_lepveto+")"+"||"+"("+"abs(LepGood_pdgId)==13&&"+OneMu_lepveto+"))"
presel = OneLep+'&&'+OneLep_lepveto+'&&'+lep_hard
#presel = OneMu+'&&'+OneMu_lepveto+'&&'+lep_hard
#presel = OneE+'&&'+OneE_lepveto+'&&'+lep_hard

dPhiStr = 'acos((LepGood_pt[0]+met_pt*cos(LepGood_phi[0]-met_phi))/sqrt(LepGood_pt[0]**2+met_pt**2+2*met_pt*LepGood_pt[0]*cos(LepGood_phi[0]-met_phi)))'
def getdPhi(c):
  metPt = c.GetLeaf('met_pt').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  lepPt = c.GetLeaf('LepGood_pt').GetValue(0)
  lepPhi = c.GetLeaf('LepGood_phi').GetValue(0)
  dp = acos((lepPt+metPt*cos(lepPhi-metPhi))/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))
  return dp

def stCut(stb):
  if type(stb)==type([]) or type(stb)==type(()):
    if len(stb)>1 and stb[1]>=0:
      return   "((LepGood_pt[0]+met_pt)>"+str(stb[0])+"&&"+"(LepGood_pt[0]+met_pt)<="+str(stb[1])+" )"
    else:
      return  stCut(stb=stb[0])
  else:
    return   "((LepGood_pt[0]+met_pt)>"+str(stb)+")"

#trigger and filters for real Data
trigger = "&&(HLT_EleHT350||HLT_MuHT350)"
filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter_fix&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_eeBadScFilter"

Bkg = [
       {'name':'WJetsToLNu_HT100to200_25ns', 'sample':WJetsToLNu_HT100to200_25ns, 'legendName':'W HT100-200', 'color':ROOT.kGreen+3, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT200to400_25ns', 'sample':WJetsToLNu_HT200to400_25ns, 'legendName':'W HT200-400', 'color':ROOT.kGreen, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT400to600_25ns', 'sample':WJetsToLNu_HT400to600_25ns, 'legendName':'W HT400-600', 'color':ROOT.kGreen-3, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT600to800_25ns', 'sample':WJetsToLNu_HT600to800_25ns, 'legendName':'W HT600-800', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT800to1200_25ns', 'sample':WJetsToLNu_HT800to1200_25ns, 'legendName':'W HT800-1200', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT1200to2500_25ns', 'sample':WJetsToLNu_HT1200to2500_25ns, 'legendName':'W HT1200-2500', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT2500toInf_25ns', 'sample':WJetsToLNu_HT2500toInf_25ns, 'legendName':'W HT2500-Inf', 'color':ROOT.kGreen-7, 'merge':'EWK'}
]

Data = [{'name':'SingleElectron_Run2015D', 'sample':SingleElectron_Run2015D_v4, 'LegendName':'Data', 'merge':'Data'}
        #{'name':'SingleMuon_Run2015D', 'sample':SingleMuon_Run2015D_v4, 'LegendName':'Data', 'merge':'Data'}
        #{'name':'JetHT_Run2015D', 'sample':JetHT_Run2015D_v4, 'LegendName':'Data', 'merge':'Data'}
]

for sample in Bkg:
  sample['chunks'], sample['norm'] = getChunks(sample['sample'], maxN=-1)
  sample['chain'] = ROOT.TChain('tree')
  for chunk in sample['chunks']:
    sample['chain'].Add(chunk['file'])

  sample['weight'] = getWeight(sample['norm'], targetLumi)

dataChain = ROOT.TChain('tree')
for sample in Data:
  sample['chunks'], sample['norm'] = getChunks(sample['sample'], maxN=-1)
  for chunk in sample['chunks']:
    dataChain.Add(chunk['file'])

bins = {}
for srNJet in signalRegion:
  bins[srNJet] = {}
  for stb in signalRegion[srNJet]:
    bins[srNJet][stb] = {}
    for htb in signalRegion[srNJet][stb]:
      bins[srNJet][stb][htb] = {}
      for btb in btreg:
        deltaPhiCut = signalRegion[srNJet][stb][htb]['deltaPhi']
        bins[srNJet][stb][htb][btb] = {}
        yNorm = 0.
        yNormVar = 0.
        y = 0.
        yVar = 0.
        yHighNorm = 0.
        yHighNormVar = 0.
        yHigh = 0.
        yHighVar = 0.
        yLowNorm = 0.
        yLowNormVar = 0.
        yLow = 0.
        yLowVar = 0.

        for sample in Bkg:
          cutname = nameAndCut(stb, srNJet, htb, btb, presel=presel, btagVar = 'nBJetMediumCMVA30')[0]
          cut = '('+presel+'&&'+stCut(stb)+'&&'+nJetCut(srNJet, minPt=30., maxEta=2.4)+'&&'+nBTagCut(btb, minPt=30, maxEta=2.4, minCSVTag=0.890)+'&&'+htCut(htb, minPt=30., maxEta=2.4, njCorr=0.)+'&&'+nJetCut(2, minPt=80., maxEta=2.4)+')'

          sample["chain"].Draw(">>eList",cut) #Get the event list 'eList' which has all the events satisfying the cut
          elist = ROOT.gDirectory.Get("eList")
          number_events = elist.GetN()
          print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
          #Event loop
          for i in range(number_events): #Loop over those events
#            if getVarValue(sample['chain'], 'nLepGood')>1: 
#              print 'this should not have happened!'
#              x = getVarValue(sample['chain'],'nLepGood')
#              print x
#              for j in range(int(x)):print sample['chain'].GetLeaf('LepGood_pt').GetValue(j), sample['chain'].GetLeaf('LepGood_eta').GetValue(j),sample['chain'].GetLeaf('LepGood_pdgId').GetValue(j)
#              print [getObjDict(sample['chain'], 'GenPart_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex'], j) for j in range(int(sample['chain'].GetLeaf('nGenPart').GetValue()))]
            if i%10000==0:
              print "At %i of %i for sample %s"%(i,number_events,sample['name'])
            sample["chain"].GetEntry(elist.GetEntry(i))
            #find gen W
            p4w, p4lepton = getGenWandLepton(sample['chain'])
            weight = 1.
            if sample.has_key('weight'):
              if type(sample['weight'])==type(''):
                sampleWeight = getVarValue(sample['chain'], sample['weight'])
                genWeight = getVarValue(sample['chain'], 'genWeight')
                xsec = getVarValue(sample['chain'], 'xsec')
                weight = sampleWeight*genWeight*xsec
              else:
                genWeight = getVarValue(sample['chain'], 'genWeight')
                xsec = getVarValue(sample['chain'], 'xsec')
                weight = sample['weight']*genWeight*xsec

#            if sample['chain'].GetLeaf('LepGood_pdgId').GetValue(0)     
            if not p4w and not p4lepton: 
              y += weight
              yVar += (weight)**2
              yNorm += weight
              yNormVar += (weight)**2
              continue
            cosTheta = ROOT.WjetPolarizationAngle(p4w, p4lepton)
            normWeight = weight * (1.-0.1*(1.-cosTheta)**2) * 1./(1.-0.1*2./3.)
            yNorm += normWeight
            yNormVar += (normWeight)**2
            y += weight
            yVar += (weight)**2
#            dP = getdPhi(sample['chain'])
#            if dP > deltaPhiCut: 
#              yHighNorm += normWeight
#              yHighNormVar += (normWeight)**2
#              yHigh += weight
#              yHighVar += (weight)**2
#            else:
#              yLowNorm += normWeight
#              yLowNormVar += (normWeight)**2
#              yLow += weight
#              yLowVar += (weight)**2 
        try: u = abs(y-yNorm)/y
        except ZeroDivisionError: u = float('nan')
        try: uVar = u**2*((yVar+yNormVar)/(y-yNorm)**2 + yVar/y**2)
        except ZeroDivisionError: uVar = float('nan')
#        try: uLow = abs(yLow-yLowNorm)/yLow
#        except ZeroDivisionError: uLow = float('nan')
#        try: uLowVar = u**2*((yLowVar+yLowNormVar)/(yLow-yLowNorm)**2 + yLowVar/yLow**2)
#        except ZeroDivisionError: uLowVar = float('nan')
#        try: uHigh = abs(yHigh-yHighNorm)/yHigh
#        except ZeroDivisionError: uHigh = float('nan')
#        try: uHighVar = u**2*((yHighVar+yHighNormVar)/(yHigh-yHighNorm)**2 + yHighVar/yHigh**2)
#        except ZeroDivisionError: uHighVar = float('nan')

        bins[srNJet][stb][htb][btb].update({'yNorm':yNorm, 'yNormVar':yNormVar, 'y':y, 'yVar':yVar, 'uncertainty':u, 'uncertaintyVar':uVar\
#                                            'yLowNorm':yLowNorm, 'yLowNormVar':yLowNormVar, 'yLow':yLow, 'yLowVar':yLowVar, 'uncertaintyLow':uLow, 'uncertaintyLowVar':uLowVar,\
#                                            'yHighNorm':yHighNorm, 'yHighNormVar':yHighNormVar, 'yHigh':yHigh, 'yHighVar':yHighVar, 'uncertaintyHigh':uHigh, 'uncertaintyHighVar':uHighVar\
})
      print bins

#if not os.path.exists(picklePath):
#  os.makedirs(picklePath)
#pickle.dump(bins, file(picklePath+picklePresel,'w'))      
