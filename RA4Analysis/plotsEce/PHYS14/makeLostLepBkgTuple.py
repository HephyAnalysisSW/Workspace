import ROOT
import pickle
from array import array
from Workspace.RA4Analysis.objectSelection import getGoodJetsStage2,gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import findClosestObject, deltaR,getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getGenLepsWithMatchInfo,getGenLeps, getMuons, getLooseMuStage2, getGenLep ,tightPOGMuID, vetoMuID
from math import sqrt, cos, sin, atan2
from Workspace.RA4Analysis.stage2Tuples import *
from localInfo import username
from Workspace.RA4Analysis.helpers import deltaPhi

def getTypeStr(s):
  if s=='l': return 'ULong64_t'
  if s=='F': return 'Float_t'
  if s=='I': return 'Int_t'

c = ROOT.TChain('Events')
c.Add('/data/schoef/convertedTuples_v26/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*.root')

small = True
n_max = 1000
relIso = 0.3
doubleLeptonPreselection = "gLepCount==2&&ngNuMuFromW==2&&ngNuEFromW==0"

#leptonEffMap = pickle.load(file('/data/'+username+'/results2014/muonTemplates/CSA14_TTJets_efficiencyMap_vetoMuIDPt15_ttJetsCSA1450ns_relIso'+str(relIso)+'.pkl'))
leptonEffMap = pickle.load(file('/data/'+username+'/results2014/muonTemplates/CSA14_TTJets_efficiencyMap_v26_vetoMuIDPt15_ttJetsCSA1450ns_v26_relIso'+str(relIso)+'.pkl'))
leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>15&&abs(muEta)<2.5&&abs(muDxy)<0.2&&abs(muDz)<0.5&&muRelIso<"+str(relIso) 

#ofile ='/data/'+username+'/results2014/muonTuples/CSA14_TTJets_Lost_v26_looseMatchedMuons_relIso'+str(relIso)+'.root'
ofile ='/data/'+username+'/results2014/muonTuples/deneme.root'
#ofile ='/data/'+username+'/results2014/muonTuples/CSA14_TTJets_Lost_v26_relIso'+str(relIso)+'.root'
if small: ofile ='/data/'+username+'/results2014/muonTuples/CSA14_TTJets_Lost_small_relIso'+str(relIso)+'.root'

copyVars  = ['event/l','weight/F', 'njets/I','nbtags/F' ,'ht/F', 'met/F', 'metPhi/F', 'nvetoMuons/F','ngoodMuons/F','nvetoElectrons/F','gTauPt/F','gTauEta/F','gTauNENu/I','gTauNMuNu/I','gTauNTauNu/I']
truthVars   = ['wPhi/F', 'wPt/F','st/F','relIso/F', 'mT/F', 'pt/F','eta/F','lostPt/F','lostEta/F', \
'phi/F','lostPhi/F','deltaPhi/F', \
'mindeltaRBM/F', \
'mindeltaRBL/F', \
'mindeltaRNonBM/F', \
'mindeltaRNonBL/F', \
'mindeltaRAllJets/F', \
'minlostdeltaRBM/F', \
'minlostdeltaRBL/F', \
'minlostdeltaRNonBM/F', \
'minlostdeltaRNonBL/F', \
'minlostdeltaRAllJets/F', \
'closestJetPt/F', \
'closestJetPdg/F', \
'closestJetPhi/F', \
'closestJetEta/F', \
'closestJetChef/F', \
'closestJetNhef/F', \
'closestJetHFhef/F', \
'closestJetHFeef/F', \
'closestJetMuef/F', \
'closestJetElef/F', \
'closestJetPhef/F', \
'effTight/F',\
'effLost/F'\
]
vectorVars = [
'jetPt[16]/F', \
'jetEta[16]/F', \
'jetPhi[16]/F', \
'jetPdg[16]/F', \
'jetChef[16]/F', \
'jetNhef[16]/F', \
'jetHFhef[16]/F', \
'jetHFeef[16]/F', \
'jetMuef[16]/F', \
'jetElef[16]/F', \
'jetPhef[16]/F', \
'bJetCSVMPt[16]/F', \
'bJetCSVMEta[16]/F', \
'bJetCSVMPhi[16]/F', \
'bJetCSVMPdg[16]/F', \
'bJetCSVLPt[16]/F', \
'bJetCSVLEta[16]/F', \
'bJetCSVLPhi[16]/F', \
'bJetCSVLPdg[16]/F', \
'nonbJetCSVMPt[16]/F', \
'nonbJetCSVMEta[16]/F', \
'nonbJetCSVMPhi[16]/F', \
'nonbJetCSVMPdg[16]/F', \
'nonbJetCSVLPt[16]/F', \
'nonbJetCSVLEta[16]/F', \
'nonbJetCSVLPhi[16]/F', \
'nonbJetCSVLPdg[16]/F', \
]
vars      = copyVars+truthVars

structString = "struct MyStruct{"
structString+= "".join([getTypeStr(v.split('/')[1])+" "+v.split('/')[0]+";" for v in vars])
structString+= "".join([getTypeStr(v.split('/')[1])+" "+v.split('/')[0]+";" for v in vectorVars])
structString+="}"
ROOT.gROOT.ProcessLine(structString)
exec("from ROOT import MyStruct")
exec("s = MyStruct()")
print structString
dir=ROOT.gDirectory.func()

f=ROOT.TFile(ofile, 'recreate')
f.cd()
t = ROOT.TTree( "Events", "Events", 1 )
for v in vars:
 t.Branch(v.split('/')[0],   ROOT.AddressOf(s,v.split('/')[0]), v)
for v in vectorVars:
  t.Branch(v.split('[')[0], ROOT.AddressOf(s,v.split('[')[0]),v) 
dir.cd()
#cut = "&&".join([doubleLeptonPreselection, hadPresel])
c.Draw(">>eList", doubleLeptonPreselection)
#c.Draw(">>eList", hadPresel)
elist = ROOT.gDirectory.Get("eList")
number_events = elist.GetN()
if small : number_events = n_max
for i in range(number_events):
#for i in range(80000,90000):
  c.GetEntry(elist.GetEntry(i))
  if (i%10000 == 0) and i>0 :
    print i,"/",number_events
  s.event = long(c.GetLeaf('event').GetValue())
  #if s.event == 73339641 or s.event == 78917005 : small = True
  if small: print s.event
  for v in copyVars[1:]:
    n=v.split('/')[0]
    #print n
    exec('s.'+n+'='+str(c.GetLeaf(n).GetValue()))
  for v in truthVars[:]:
   n=v.split('/')[0]
   exec('s.'+n+'='+str(-1000))
  for v in vectorVars[:]:
    n=v.split('[')[0]
    for i in range(16):
      exec('s.'+n+'['+str(i)+']='+str(-1000)) 

  #2 gen lep in acceptance
  #1 tight reco matched to a gen lepton
  #no further loose muon
  
  #1. get all gen leps:
  gLeps = getGenLepsWithMatchInfo(c,relIso)
  #1.1 get gen leps in acceptance:
  gLepsInAcc = filter(lambda x:x['gLepPt']>=15 and abs(x['gLepEta'])<2.1, gLeps)
  #2. get loose muons and match to gen-leps in acceptance
  allMuons = getMuons(c,relIso,gLeps)
  looseMuons = filter(lambda x:x['isLoose'], allMuons) 
  looseMatchedMuons = filter(lambda x:x['hasMatch'], looseMuons)
  looseMuonsInAcc = filter(lambda x:x['pt']>=15 and abs(x['eta'])<2.1, looseMuons)
  #3. get tight muons that are matched
  tightMuons = filter(lambda x:x['isTight'], allMuons)
  tightMatchedMuons = filter(lambda x:x['isTight'] and x['hasMatch'], looseMuons)
  #4. get Lost muons 
  lostGenMuons = filter(lambda x:not x['hasMatchInd'], gLeps)
  lostGenMuonsInAcc = filter(lambda x:x['gLepPt']>=15 and abs(x['gLepEta'])<2.1, lostGenMuons)

  nLostMuons = len(lostGenMuonsInAcc) 
  if small: print nLostMuons
  ##Get Jets
  njets = getVarValue(c, 'njets')
  nbtags = getVarValue(c, 'nbtags')
  jets = getGoodJetsStage2(c)
  sorted(jets, key= lambda x: -x['pt'])
  bjetsCSVM = filter(lambda j:j['btag']>0.679 and abs(j['eta'])<2.4, jets)
  sorted(bjetsCSVM, key=lambda x: -x['pt'])
  bjetsCSVL = filter(lambda j:j['btag']>0.246 and abs(j['eta'])<2.4, jets)
  sorted(bjetsCSVL, key=lambda x: -x['pt'])
  nonbjetsCSVM = filter(lambda j:not (j['btag']>0.679 and abs(j['eta'])<2.4), jets)
  sorted(nonbjetsCSVM, key=lambda x: -x['pt'])
  nonbjetsCSVL = filter(lambda j: not (j['btag']>0.246 and abs(j['eta'])<2.4), jets)
  sorted(nonbjetsCSVL, key=lambda x: -x['pt'])

  #if len(gLepsInAcc)==2 and  len(looseMuons)==1 and len(tightMatchedMuons) == 1:
  if len(gLepsInAcc)==2 and  len(looseMatchedMuons)==1 and len(tightMatchedMuons) == 1:
    if small:
      print nLostMuons
      print 'met:', s.met
      print 'number of all reco muons:', len(allMuons) 
      print 'number of all generated muons:', len(gLeps)
      print 'gLeps', gLeps
      print 'all muons', allMuons
      print 'lost gen muons:' , lostGenMuonsInAcc
      print 'n jets:' , len(jets)
      print 'n bjets:' , len(bjetsCSVM)
      print 'n non bjets' , len(nonbjetsCSVM)
      print 'ALL JETS:',jets
      print 'B JETS CSVM:', bjetsCSVM
      print 'Non B JETS CSVM:' , nonbjetsCSVM
    tightMatchedMuon = tightMatchedMuons[0]
    lostLep = lostGenMuonsInAcc[0] 
    lostLep_ = {'phi':lostLep['gLepPhi'],'eta':lostLep['gLepEta']} 

    ###Efficiency of tight muon:
    lEffT = leptonEffMap.FindBin( tightMatchedMuon['pt'], tightMatchedMuon['eta'])
    lEfft = leptonEffMap.GetBinContent(lEffT)
    lEffL = leptonEffMap.FindBin( lostLep['gLepPt'], lostLep['gLepEta'])
    lEffl = leptonEffMap.GetBinContent(lEffL)
    if lEfft<0.5 or lEffl<0.5: continue
    s.effTight = lEfft
    s.effLost = lEffl
    if small: print 'eff of tight muon:', s.effTight

    s.lostPt = lostLep['gLepPt']
    s.lostEta = lostLep['gLepEta']
    s.lostPhi =  lostLep['gLepPhi']
    #sortedList  = [[deltaR(lostLep_, jet), jet] for jet in jets]sort( key=lambda x:-x[0])

    if len(jets)>0:
      closestObj = findClosestObject(jets,lostLep_)
      closestJet = closestObj['obj']
      s.closestJetPt          = closestJet['pt']
      s.closestJetPdg         = closestJet['pdg']
      s.closestJetPhi         = closestJet['phi']
      s.closestJetEta         = closestJet['eta']
      s.closestJetChef        = closestJet['chef']
      s.closestJetNhef        = closestJet['nhef']
      s.closestJetHFhef       = closestJet['hFhef']
      s.closestJetHFeef       = closestJet['hFeef']
      s.closestJetMuef        = closestJet['muef']
      s.closestJetElef        = closestJet['elef']
      s.closestJetPhef        = closestJet['phef']
      s.minlostdeltaRAllJets  = sqrt(closestObj['distance'])
      if small: print 'min deltaR all jets:' , s.minlostdeltaRAllJets
      s.mindeltaRAllJets = sqrt(findClosestObjectDR(jets,tightMatchedMuon)['distance'])
    if len(bjetsCSVM)>0:    s.mindeltaRBM          =sqrt(findClosestObjectDR(bjetsCSVM,tightMatchedMuon)['distance'])
    if len(bjetsCSVL)>0:    s.mindeltaRBL          =sqrt(findClosestObjectDR(bjetsCSVL,tightMatchedMuon)['distance'])  
    if len(nonbjetsCSVM)>0: s.mindeltaRNonBM       =sqrt(findClosestObjectDR(nonbjetsCSVM,tightMatchedMuon)['distance'])
    if len(nonbjetsCSVL)>0: s.mindeltaRNonBL       =sqrt(findClosestObjectDR(nonbjetsCSVL,tightMatchedMuon)['distance'])
    if len(bjetsCSVM)>0:    
      s.minlostdeltaRBM      = sqrt(findClosestObjectDR(bjetsCSVM,lostLep_)['distance'] )
      if small: print 'min deltaR bjet:' , s.minlostdeltaRBM
      if s.minlostdeltaRBM < s.minlostdeltaRAllJets:  print 'ALERT ALERT', 'i:',i , 'event:', s.event
      if len(bjetsCSVM)==len(jets) and s.minlostdeltaRBM >s.minlostdeltaRAllJets :  print 'LOOK AT THIS EVENT!!!' , s.minlostdeltaRBM , 'event:' , s.event 
      if s.minlostdeltaRAllJets>0.4 and s.minlostdeltaRBM<0.4 :  print 'LOOK AT THIS EVENT!!!' , s.minlostdeltaRBM ,'i:',i, 'event:' , s.event 
    if len(bjetsCSVL)>0:    s.minlostdeltaRBL      = sqrt(findClosestObjectDR(bjetsCSVL,lostLep_)['distance'])
    if len(nonbjetsCSVM)>0:
      s.minlostdeltaRNonBM   = sqrt(findClosestObjectDR(nonbjetsCSVM,lostLep_)['distance'])
      if small: print 'min delta R non bjets:' , s.minlostdeltaRNonBM
      if s.minlostdeltaRNonBM < s.minlostdeltaRAllJets :  print 'ALERT ALERT', 'i:',i , 'event:', s.event
      if len(nonbjetsCSVM)==len(jets) and s.minlostdeltaRNonBM >s.minlostdeltaRAllJets :  print 'LOOK AT THIS EVENT!!!' , s.minlostdeltaRBM , 'event:' , s.event 
      if s.minlostdeltaRAllJets>0.4 and s.minlostdeltaRNonBM<0.4 :  print 'LOOK AT THIS EVENT!!!' , s.minlostdeltaRNonBM , 'i',i,'event:' , s.event 
    if len(nonbjetsCSVL)>0: s.minlostdeltaRNonBL = sqrt(findClosestObjectDR(nonbjetsCSVL,lostLep_)['distance'])
    if len(nonbjetsCSVM)>0 and len(bjetsCSVM)>0 and min(s.minlostdeltaRNonBM, s.minlostdeltaRBM) > s.minlostdeltaRAllJets : print 'ALERT !!!!'  , s.event 
    for j in range(int(njets)):
      jet = jets[j]
      if jet:
        s.jetPt[j] = jet['pt']
        s.jetEta[j] = jet['eta']
        s.jetPhi[j] = jet['phi']
        s.jetPdg[j] = jet['pdg']
        s.jetChef[j]  = jet['chef']
        s.jetNhef[j]  = jet['nhef']
        s.jetHFhef[j] = jet['hFhef']
        s.jetHFeef[j] = jet['hFeef']
        s.jetMuef[j]  = jet['muef']
        s.jetElef[j]  = jet['elef']
        s.jetPhef[j]  = jet['phef']
    for j in range(int(len(bjetsCSVM))):
      s.bJetCSVMPt[j]  = bjetsCSVM[j]['pt']
      s.bJetCSVMEta[j] = bjetsCSVM[j]['eta']
      s.bJetCSVMPhi[j] = bjetsCSVM[j]['phi']
      s.bJetCSVMPdg[j] = bjetsCSVM[j]['pdg']
    for j in range(int(len(bjetsCSVL))):
      s.bJetCSVLPt[j]  = bjetsCSVL[j]['pt']
      s.bJetCSVLEta[j] = bjetsCSVL[j]['eta']
      s.bJetCSVLPhi[j] = bjetsCSVL[j]['phi']
      s.bJetCSVLPdg[j] = bjetsCSVL[j]['pdg']
    for j in range(int(len(nonbjetsCSVM))):
      s.nonbJetCSVMPt[j]  = nonbjetsCSVM[j]['pt']
      s.nonbJetCSVMEta[j] = nonbjetsCSVM[j]['eta']
      s.nonbJetCSVMPhi[j] = nonbjetsCSVM[j]['phi']
      s.nonbJetCSVMPdg[j] = nonbjetsCSVM[j]['pdg']
    for j in range(int(len(nonbjetsCSVL))):
      s.nonbJetCSVLPt[j]  = nonbjetsCSVL[j]['pt']
      s.nonbJetCSVLEta[j] = nonbjetsCSVL[j]['eta']
      s.nonbJetCSVLPhi[j] = nonbjetsCSVL[j]['phi']
      s.nonbJetCSVLPdg[j] = nonbjetsCSVL[j]['pdg']

    #jetsCleaned = [jet for jet in jets if min([deltaR(jet, muon) for muon in looseMuons])>0.4]
    #if small: print 'number of cleaned jets', len(jetsCleaned)
    s.mT=(sqrt(2*s.met*tightMatchedMuon['pt']*(1-cos(tightMatchedMuon['phi']-s.metPhi))))
    wx = s.met*cos(s.metPhi) + tightMatchedMuon['pt']*cos(tightMatchedMuon['phi'])
    wy = s.met*sin(s.metPhi) + tightMatchedMuon['pt']*sin(tightMatchedMuon['phi'])
    s.wPhi     = atan2(wy,wx)
    s.wPt      = sqrt((wx)**2+(wy)**2) 
    s.st       = s.met + tightMatchedMuon['pt'] 
    s.pt     = (tightMatchedMuon['pt'])
    s.eta    = (tightMatchedMuon['eta'])
    s.phi    = (tightMatchedMuon['phi'])
    s.deltaPhi = (deltaPhi(tightMatchedMuon['phi'],s.wPhi))
    s.relIso = tightMatchedMuon['relIso']
    t.Fill()
f.cd()
t.Write()
f.Close()
print "Written",f.GetName()
dir.cd()

