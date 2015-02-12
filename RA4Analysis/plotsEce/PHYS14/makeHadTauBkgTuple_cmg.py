import ROOT
import pickle
from array import array
from Workspace.RA4Analysis.objectSelection import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getLooseMuStage2, tightPOGMuID, vetoMuID
from Workspace.RA4Analysis.cmgObjectSelection import get_cmg_recoMuons , get_cmg_jets
from math import sqrt, cos, sin, atan2
from Workspace.RA4Analysis.helpers import deltaPhi
from Workspace.RA4Analysis.cmgTuplesPostProcessed_v3 import *
from Workspace.HEPHYPythonTools.helpers import getChain
from Workspace.RA4Analysis.stage2Tuples import *

#c = getChain(hard_ttJetsCSA1450ns)
ROOT.TH1F.SetDefaultSumw2()
c = ROOT.TChain('Events')
c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2/hard/TTJets/*.root')

mode='had'
relIso = 0.3

small = False
maxN=10000

if mode=='had':
  leptonEffMap = pickle.load(file('/afs/hephy.at/user/e/easilar/www/hadronicTau_PHYS14_inc/lepton_Efficiency_Results/CSA14_TTJet_LepEff_cmg_Large.pkl'))
  tauFrMap = pickle.load(file('/afs/hephy.at/user/e/easilar/www/hadronicTau_PHYS14_inc/fakeRate_Results/CSA14_TTJet_tauToBfakeRate_cmg_Phys14_inc.pkl'))
  #doubleLeptonPreselection = "ngoodMuons>=1&&nvetoMuons==2&&nvetoElectrons==0"
  doubleLeptonPreselection = "nLooseHardLeptons==2&&nTightHardLeptons>=1&&nLepGood==2\
  &&Sum$(abs(LepGood_pdgId)==13 && LepGood_tightId==1 && abs(LepGood_eta)<2.4 && LepGood_relIso03 < 0.3)==2\
  &&Sum$(abs(LepGood_pdgId)==13 && LepGood_tightId==1 && abs(LepGood_eta)<2.1 && LepGood_relIso03 < 0.12)>=1\
  &&Sum$(abs(LepGood_pdgId)==11)==0\
  &&nLepOther==0"
  gendoubleLeptonPreselection = "Sum$(abs(genPart_pdgId)==14&&abs(genPart_motherId)==24)==2&&Sum$(abs(genPart_pdgId)==12)==0&&Sum$(abs(genPart_pdgId)==16)==0"
  print doubleLeptonPreselection
  templates = pickle.load(file('/data/easilar/results2014/tauTemplates/CSA14_TTJets_genTau_cmg_PHYS14_inc.pkl'))
  ofile =                      '/data/easilar/results2014/tauTuples/CSA14_TTJets_hadTauEstimate_cmg_large_PHYS14_inc_new.root'

  #doubleLeptonPreselection = "ngoodMuons>=1&&nvetoMuons==2&&nvetoElectrons==0"
  #templates = pickle.load(file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_lepGenTau.pkl'))
  #ofile =                      '/data/schoef/results2014/tauTuples/CSA14_TTJets_lepGenTau.root'

if mode=='had' or mode=='lep':
  for ptk in templates.keys():
    for etak in templates[ptk].keys():
      templates[ptk][etak].Scale(1./templates[ptk][etak].Integral())
      res=[]
      for b in range(1, 1+templates[ptk][etak].GetNbinsX()):
        res.append({'frac':templates[ptk][etak].GetBinCenter(b), 'weight':templates[ptk][etak].GetBinContent(b)})
      templates[ptk][etak]=res
      #print res


def getTwoMuons(c):
  muons=get_cmg_recoMuons(c)
  #print muons
  if len(muons) ==2 : return muons
  if len(muons) !=2 : print 'problematic event'

def getTypeStr(s):
  if s=='l': return 'ULong64_t'
  if s=='F': return 'Float_t'
  if s=='I': return 'Int_t'

#copyVars  = ['event/l','nbtags/I', 'njets/I', 'ht/F', 'met/F', 'metPhi/F', 'nvetoMuons/I']
copyVars  = ['evt/l','xsec/I','lumi/I','nBJetMedium25/I', 'nBJetMedium40/I','nJet40a/I', 'htJet40ja/F','st/F','LepGood_pt/F','LepGood_phi/F','LepGood_eta/F', 'met_pt/F', 'met_phi/F','met_eta/F', 'nLepGood/I','nLepOther/I']
#newVars   = ['nbtagsPred/I','njetsPred/I','effTauToB/F','scaleLEffUp/F','scaleLEffDown/F', 'htPred/F', 'metPred/F', 'metphiPred/F','weightPred/F', 'mTPred/F', 'weight/F', 'scaleLEff/F','wPt/F','wPhi/F','deltaPhiPred/F']
newVars   = ['njets30Pred/I','nbtagsCMVAPred/I','nbtagsPred/I','njetsPred/I','effTauToB/F','scaleLEffUp/F','scaleLEffDown/F', 'htPred/F', 'metPred/F', 'metphiPred/F','weightPredOld/F','weightPred/F', 'mTPred/F', 'weight/F', 'scaleLEff/F','wPt/F','wPhi/F','deltaPhiPred/F']
vars      = copyVars+newVars  
#print vars
structString = "struct MyStruct{"
structString+= "".join([getTypeStr(v.split('/')[1])+" "+v.split('/')[0]+";" for v in vars])
structString+="}"   
ROOT.gROOT.ProcessLine(structString)
exec("from ROOT import MyStruct")
exec("s = MyStruct()")
dir=ROOT.gDirectory.func()
#print dir
f=ROOT.TFile(ofile, 'recreate')
f.cd()
t = ROOT.TTree( "Events", "Events", 1 )
for v in vars:
 t.Branch(v.split('/')[0],   ROOT.AddressOf(s,v.split('/')[0]), v) 
dir.cd()

c.Draw(">>eList", doubleLeptonPreselection+"&&"+gendoubleLeptonPreselection)
eList = ROOT.gDirectory.Get("eList")
number_events = eList.GetN()
#print number_events
if small:
  if number_events>maxN:
    number_events=maxN
#number_events=maxN
number_events=min(number_events, eList.GetN())
countLeptons=0
for i in range(number_events):
  #print i
  if (i%10000 == 0) and i>0 :
    print i,"/",number_events
  c.GetEntry(eList.GetEntry(i))
  #c.GetEntry(i)
  s.event = long(c.GetLeaf('evt').GetValue())
  #print s.event
  for v in copyVars[1:]:
    n=v.split('/')[0]
    exec('s.'+n+'='+str(c.GetLeaf(n).GetValue()))
  muons = getTwoMuons(c)
  jets = get_cmg_jets(c)
  nbtagCMVA = 0
  njet30 = 0
  for jet in jets :
    if jet:
      if jet['pt']>30 and abs(jet['eta'])<2.4 and jet['jetId'] and jet['btag']>0.732: nbtagCMVA = nbtagCMVA+1
      if jet['pt']>30 and abs(jet['eta'])<2.4 and jet['jetId'] : njet30 = njet30+1
  #print "nbtag CMVA" , nbtagCMVA
  #if len(muons) != 2 : continue
  #print muons
  #print 'len muons' , len(muons)
  assert len(muons)==2, "Problem in event "+str(int(c.GetLeaf('evt').GetValue()))
  if muons[0]['isTight'] and muons[1]['isTight']:
    combFac=0.5
  else:
    combFac=1.
  for perm in [muons, reversed(muons)]:
    m,m2 = perm
    if m2['isTight']:
#      #print iperm, m['isTight'],m2['isTight']
      #print "pt",m['pt'],m['phi'],m['eta']
      abseta=abs(m['eta'])
      if abseta>2.1 and m['pt']<10: continue
      countLeptons+=1
#      #print template 
      s.weight=c.GetLeaf('weight').GetValue()
      lEffb = leptonEffMap.FindBin( m['pt'], m['eta'])
      lEff = leptonEffMap.GetBinContent(lEffb)

      if mode=='had' or mode=='lep': 
        template=None
        for ptb in gTauPtBins:
          if m['pt']>=ptb[0] and (m['pt']<ptb[1] or ptb[1]<0):
            for etab in gTauAbsEtaBins:
              if abseta>=etab[0] and abseta<etab[1]:
                template=templates[ptb][etab]
                break
            if template:break
        assert template, "No template found for muon: %r" % repr(m)
        if lEff<0.5: continue
        s.scaleLEff = 1./lEff
        s.scaleLEffDown = 1./(lEff*1.1)
        s.scaleLEffUp = 1./(lEff*0.9)
        
#        else:
#          s.scaleLEff = 1.
        for p in template:
          metpar    = p['frac']*m['pt']
          mEx = s.met_pt*cos(s.met_phi)+cos(m['phi'])*metpar
          mEy = s.met_pt*sin(s.met_phi)+sin(m['phi'])*metpar
          wx = mEx+cos(m2['phi'])*m2['pt']
          wy = mEy+sin(m2['phi'])*m2['pt'] 
          if mode=='had':
  #          s.nvetoMuonsPred = s.nvetoMuons 
            jetpt =  (1.-p['frac'])*m['pt']
            s.metPred = sqrt(mEx**2+mEy**2)
            s.metphiPred = atan2(mEy,mEx)
            s.mTPred = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metphiPred)))
            s.wPt = sqrt(wx**2+wy**2)
            s.wPhi = atan2(wy,wx)
            s.deltaPhiPred = deltaPhi(s.wPhi,m2['phi'])
            s.effTauToB = tauFrMap.GetBinContent(tauFrMap.FindBin(jetpt))
            s.weightPredOld = p['weight']*s.weight
            if jetpt>30.:
              s.njetsPred = s.nJet40a+1
              s.njets30Pred = njet30 +1
              s.htPred   = s.htJet40ja+jetpt

              s.nbtagsPred = s.nBJetMedium40+1
              s.nbtagsCMVAPred = nbtagCMVA+1 
              s.weightPred = p['weight']*s.weight*s.effTauToB
              t.Fill()
              s.nbtagsPred = s.nBJetMedium40
              s.weightPred = p['weight']*s.weight*(1-s.effTauToB)
              t.Fill()
            else:
              s.weightPred = p['weight']*s.weight
              s.njetsPred = s.nJet40a
              s.njets30Pred = njet30
              s.nbtagsPred = s.nBJetMedium40
              s.nbtagsCMVAPred = nbtagCMVA
              s.htPred   = s.htJet40ja
              t.Fill()
          if mode=='lep':
            s.njetsPred = s.nJet40a
            s.htPred   = s.htJet40ja
            leppt =  (1.-p['frac'])*m['pt']
            if leppt>15.:
              nlEffb = leptonEffMap.FindBin(leppt, m['eta'])
              nlEff = leptonEffMap.GetBinContent(nlEffb) #Consider the event not contributing if the lepton from the tau hits the lepton veto
              weightFac = 1-nlEff
            else:
              weightFac = 1.
              
            s.weightPred = p['weight']*s.weight*weightFac
            MEx += leppt*cos(m['phi'])
            MEy += leppt*sin(m['phi'])
            s.metPred = sqrt(MEx**2+MEy**2)
            s.metphiPred = atan2(MEy,MEx)
            s.mTPred = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metphiPred)))
            t.Fill()
  #            #lepton reconstructed ->not filled
  ##            s.nvetoMuonsPred = s.nvetoMuons + 1 
  #            s.weightPred = p['weight']*s.weight*nlEff
  #            s.metPred = sqrt(MEx**2+MEy**2)
  #            s.metphiPred = atan2(MEy,MEx)
  #            s.mTPred = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metphiPred)))
  #            t.Fill()
              #lepton lost
  #            s.nvetoMuonsPred = s.nvetoMuons  


f.cd()
t.Write()
f.Close()
print "Written",f.GetName()
dir.cd()

