import ROOT
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/WPolarizationVariation.C+")
ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.TH1F().SetDefaultSumw2()
from math import *
import os, copy, sys
from array import array

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.HEPHYPythonTools.xsec import *
from Workspace.HEPHYPythonTools.user import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_0l import *
from Workspace.RA4Analysis.helpers import *
from draw_helpers import *
from eleID_helper import *

#small = True
small = False

preprefix = 'WPolarizationEstimation'
wwwDir = '/afs/hephy.at/user/d/dhandl/www/RunII/Spring15_25ns/'+preprefix+'/'
prefix = 'W_cosTheta_'

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

WplusPresel = '(genPartAll_motherId==24&&abs(genPartAll_pdgId)>=11&&abs(genPartAll_pdgId)<=14)' #for Wplus
WminusPresel ='(genPartAll_motherId==(-24)&&abs(genPartAll_pdgId)>=11&&abs(genPartAll_pdgId)<=14)' #for Wminus
htreg = [(350,-1)]
ptWreg = [(10,100),(100,300),(300,500),(500,10000)]
absEtaW = [(0,1),(1,2),(2,5)]

#trigger and filters for real Data
#trigger = "&&(HLT_EleHT350||HLT_MuHT350)"
#filters = "&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilterMinZeroPatched&&Flag_goodVertices&&Flag_eeBadScFilter"

targetLumi = 3000 #pb-1
def getWeight(sample,nEvents,target_lumi):
  weight = xsec[sample['dbsName']] * target_lumi/nEvents
  return weight

def getGenWandLepton(c):
  genPartAll = [getObjDict(c, 'genPartAll_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex1'], j) for j in range(int(c.GetLeaf('ngenPartAll').GetValue()))]
  lepton = filter(lambda l:abs(l['pdgId']) in [11,13], genPartAll)
  lFromW = filter(lambda w:abs(w['motherId'])==24, lepton)
  if len(lFromW)>0:
    if len(lFromW)>1: print 'this should not have happened'
    if abs(lFromW[0]['motherId'])!=24: print 'this should not have happened'
    genW = getObjDict(c, 'genPartAll_', ['pt','eta','phi','mass','pdgId','motherId','motherIndex1'], int(lFromW[0]['motherIndex1']))
    if abs(genW['pdgId'])!=24: 'this should not have happened'
#    print lFromW
#    print genW
    lep = ROOT.TLorentzVector()
    lep.SetPtEtaPhiM(lFromW[0]['pt'],lFromW[0]['eta'],lFromW[0]['phi'],lFromW[0]['mass'])
    W = ROOT.TLorentzVector()
    W.SetPtEtaPhiM(genW['pt'],genW['eta'],genW['phi'],genW['mass'])
    p4lepton = ROOT.LorentzVector(lep.Px(),lep.Py(),lep.Pz(),lep.E())
    p4w = ROOT.LorentzVector(W.Px(),W.Py(),W.Pz(),W.E())
    return p4w, p4lepton

def doMyFit(hist,func):
  f = ROOT.TF1('myFit',func,-1,1)
  hist.Fit('myFit')
  fo=f.GetParameter(0)
  fL=f.GetParameter(1)
  fR=f.GetParameter(2)
  fo_err=f.GetParError(0)
  fL_err=f.GetParError(1)
  fR_err=f.GetParError(2)
  ftot=fo+fL+fR
  ftot_err=sqrt(fo_err**2+fL_err**2+fR_err**2)
  f0 = fo/ftot
  fl = fL/ftot
  fr = fR/ftot
  f0_err = f0*sqrt((fo_err/fo)**2+(ftot_err/ftot)**2)
  fl_err = fl*sqrt((fL_err/fL)**2+(ftot_err/ftot)**2)
  fr_err = fr*sqrt((fR_err/fR)**2+(ftot_err/ftot)**2)
  return f0,fl,fr,f0_err,fl_err,fr_err

Bkg = [
       {'name':'WJetsToLNu_HT100to200_25ns', 'sample':WJetsToLNu_HT100to200_25ns, 'legendName':'W HT100-200', 'color':ROOT.kGreen+3, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT200to400_25ns', 'sample':WJetsToLNu_HT200to400_25ns, 'legendName':'W HT200-400', 'color':ROOT.kGreen, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT400to600_25ns', 'sample':WJetsToLNu_HT400to600_25ns, 'legendName':'W HT400-600', 'color':ROOT.kGreen-3, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT600to800_25ns', 'sample':WJetsToLNu_HT600to800_25ns, 'legendName':'W HT600-800', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT800to1200_25ns', 'sample':WJetsToLNu_HT800to1200_25ns, 'legendName':'W HT800-1200', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT1200to2500_25ns', 'sample':WJetsToLNu_HT1200to2500_25ns, 'legendName':'W HT1200-2500', 'color':ROOT.kGreen-7, 'merge':'EWK'},
       {'name':'WJetsToLNu_HT2500toInf_25ns', 'sample':WJetsToLNu_HT2500toInf_25ns, 'legendName':'W HT2500-Inf', 'color':ROOT.kGreen-7, 'merge':'EWK'},
]

maxN=5 if small else -1

for sample in Bkg:
  sample['chunks'], sample['norm'] = getChunks(sample['sample'], maxN=maxN)
  sample['chain'] = ROOT.TChain('tree')
  for chunk in sample['chunks']:
    sample['chain'].Add(chunk['file'])

  sample['weight'] = getWeight(sample['sample'], sample['norm'], targetLumi)

h_Wminus_f0=ROOT.TH2F('h_Wminus_f0','h_Wminus_f0',4,0,4,3,0,3)
h_Wminus_fl=ROOT.TH2F('h_Wminus_fl','h_Wminus_fl',4,0,4,3,0,3)
h_Wminus_fr=ROOT.TH2F('h_Wminus_fr','h_Wminus_fr',4,0,4,3,0,3)
h_Wplus_f0=ROOT.TH2F('h_Wplus_f0','h_Wplus_f0',4,0,4,3,0,3)
h_Wplus_fl=ROOT.TH2F('h_Wplus_fl','h_Wplus_fl',4,0,4,3,0,3)
h_Wplus_fr=ROOT.TH2F('h_Wplus_fr','h_Wplus_fr',4,0,4,3,0,3)

histos = {} 
Wcharge = [
            {'name':'Wplus', 'fitFunc':'([0]*3./4.*(1-x*x)+[1]*3./8.*(1-x)*(1-x)+[2]*3./8.*(1+x)*(1+x))', 'cut':WplusPresel},
            {'name':'Wminus','fitFunc':'([0]*3./4.*(1-x*x)+[1]*3./8.*(1+x)*(1+x)+[2]*3./8.*(1-x)*(1-x))', 'cut':WminusPresel}
]

#f1 = ROOT.TFile(wwwDir+prefix+'ht'+str(htreg[0][0])+'_inclusive.root','recreate')
f1 = ROOT.TFile(wwwDir+prefix+'inclusive.root','recreate')
for wboson in Wcharge:
  histos[wboson['name']] = {}
  for i_htb, htb in enumerate(htreg):
#    histos[wboson['name']][htb] = {}
    histos[wboson['name']] = {}
    for ptw in ptWreg:
#      histos[wboson['name']][htb][ptw] = {}
      histos[wboson['name']][ptw] = {}
      for eta in absEtaW:
#        histos[wboson['name']][htb][ptw][eta] = ROOT.TH1F(wboson['name']+'_cosTheta_ht'+str(htb[0])+'-'+str(htb[1])+'_ptW'+str(ptw[0])+'-'+str(ptw[1])+'_absEtaW'+str(eta[0])+'-'+str(eta[1]),\
#                                                          wboson['name']+'_cosTheta_ht'+str(htb[0])+'-'+str(htb[1])+'_ptW'+str(ptw[0])+'-'+str(ptw[1])+'_absEtaW'+str(eta[0])+'-'+str(eta[1]),200,-1,1)  
        histos[wboson['name']][ptw][eta] = ROOT.TH1F(wboson['name']+'_cosTheta_ptW'+str(ptw[0])+'-'+str(ptw[1])+'_absEtaW'+str(eta[0])+'-'+str(eta[1]),\
                                                     wboson['name']+'_cosTheta_ptW'+str(ptw[0])+'-'+str(ptw[1])+'_absEtaW'+str(eta[0])+'-'+str(eta[1]),200,-1,1)  
  
    for sample in Bkg:
#      cutname = nameAndCut(None, htb, None, btb=None, presel=wboson['cut'], btagVar = 'nBJetMediumCMVA30')[0]
      cutname = nameAndCut(None, None, None, btb=None, presel=wboson['cut'], btagVar = 'nBJetMediumCMVA30')[0]
#      cut = '('+wboson['cut']+'&&'+htCut(htb, minPt=30, maxEta=2.4, njCorr=0.)+')'
      cut = '('+wboson['cut']+')'
  
      sample["chain"].Draw(">>eList",cut) #Get the event list 'eList' which has all the events satisfying the cut
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
  
      #Event loop
      for i in range(number_events): #Loop over those events
        if i%10000==0:
          print "At %i of %i for sample %s"%(i,number_events,sample['name'])
        sample["chain"].GetEntry(elist.GetEntry(i))
        p4w, p4lepton = getGenWandLepton(sample['chain'])
#        jets = cmgGetJets(sample['chain'], ptMin=25.) 
#        minDR = []
#        htjet30 = 0.
#        for i, j in enumerate(jets):
#          DR = sqrt(deltaPhi(p4lepton.Phi(),j['phi'])**2 + (p4lepton.Eta()-j['eta'])**2)
#          minDR.append((DR,j['pt'],j['eta']))
#          if (abs(j['eta'])<2.4) and (j['pt']>30.):
#            htjet30 += j['pt']
#        cleanJet = min(minDR,key=lambda x:x[0])
#        if (cleanJet[0]<0.4) and (cleanJet[1]>30.) and (abs(cleanJet[2])<2.4) and ((htjet30-cleanJet[1]) < htb[0]): print 'clean Jet:',cleanJet; continue
                
        weight = 1
        if sample.has_key('weight'):
          if type(sample['weight'])==type(''):
            sampleWeight = getVarValue(sample['chain'], sample['weight'])
            weight = sampleWeight
          else:
            genWeight = sample['chain'].GetLeaf('genWeight').GetValue()
            weight = sample['weight'] * genWeight
        
        for pt in ptWreg:
          for eta in absEtaW:
            if (abs(p4w.Eta())>eta[0]) and (abs(p4w.Eta())<eta[1]): etareg = eta
            if (p4w.Pt()>pt[0]) and (p4w.Pt()<pt[1]): ptreg = pt
            
        cosTheta = ROOT.WjetPolarizationAngle(p4w, p4lepton)
#        histos[wboson['name']][htb][ptreg][etareg].Fill(cosTheta,weight)
        histos[wboson['name']][ptreg][etareg].Fill(cosTheta,weight)
  
    for i_ptw,ptw in enumerate(ptWreg):
      for i_eta,eta in enumerate(absEtaW):
#        f0,fl,fr,f0_err,fl_err,fr_err = doMyFit(histos[wboson['name']][htb][ptw][eta],wboson['fitFunc'])
        f0,fl,fr,f0_err,fl_err,fr_err = doMyFit(histos[wboson['name']][ptw][eta],wboson['fitFunc'])
        if wboson['name']=='Wplus':
          h_Wplus_f0.SetBinContent(i_ptw+1,i_eta+1,f0)
          h_Wplus_fl.SetBinContent(i_ptw+1,i_eta+1,fl)
          h_Wplus_fr.SetBinContent(i_ptw+1,i_eta+1,fr)
          h_Wplus_f0.SetBinError(i_ptw+1,i_eta+1,f0_err)
          h_Wplus_fl.SetBinError(i_ptw+1,i_eta+1,fl_err)
          h_Wplus_fr.SetBinError(i_ptw+1,i_eta+1,fr_err)
        elif wboson['name']=='Wminus':
          h_Wminus_f0.SetBinContent(i_ptw+1,i_eta+1,f0)
          h_Wminus_fl.SetBinContent(i_ptw+1,i_eta+1,fl)
          h_Wminus_fr.SetBinContent(i_ptw+1,i_eta+1,fr)
          h_Wminus_f0.SetBinError(i_ptw+1,i_eta+1,f0_err)
          h_Wminus_fl.SetBinError(i_ptw+1,i_eta+1,fl_err)
          h_Wminus_fr.SetBinError(i_ptw+1,i_eta+1,fr_err)
#        histos[wboson['name']][htb][ptw][eta].Write()
        histos[wboson['name']][ptw][eta].Write()
  
    h_Wminus_f0.Write()
    h_Wminus_fl.Write()
    h_Wminus_fr.Write()
    h_Wplus_f0.Write()
    h_Wplus_fl.Write()
    h_Wplus_fr.Write()

