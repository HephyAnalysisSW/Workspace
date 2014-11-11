import ROOT
import pickle
from array import array
from Workspace.RA4Analysis.objectSelection import getGoodJetsStage2,gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import deltaR,getVarValue, getObjFromFile
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
#for b in ttJetsCSA1450ns['bins']:
#  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/histo_ttJetsCSA1450ns_from*.root')
#c.Add('/data/easilar/convertedTuples_v23/copyMET/ttJetsCSA1450ns/*')
#c.Add('/data/schoef/convertedTuples_v24/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
c.Add('/data/schoef/convertedTuples_v26/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*.root')
small = False
n_max = 100
relIso = 0.3
doubleLeptonPreselection = "gLepCount==2&&ngNuMuFromW==2&&ngNuEFromW==0"

leptonEffMap = pickle.load(file('/data/'+username+'/results2014/muonTemplates/CSA14_TTJets_efficiencyMap_v26_vetoMuIDPt15_ttJetsCSA1450ns_v26_relIso'+str(relIso)+'.pkl'))
leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>15&&abs(muEta)<2.5&&abs(muDxy)<0.2&&abs(muDz)<0.5&&muRelIso<"+str(relIso) 

ofile ='/data/'+username+'/results2014/muonTuples/CSA14_TTJets_Lost_v26_2_relIso'+str(relIso)+'.root'
if small: ofile ='/data/'+username+'/results2014/muonTuples/CSA14_TTJets_Lost_small_relIso'+str(relIso)+'.root'

copyVars  = ['event/l','weight/F', 'njets/I','nbtags/F' ,'ht/F', 'met/F', 'metPhi/F', 'nvetoMuons/F','ngoodMuons/F','nvetoElectrons/F','gTauPt/F','gTauEta/F','gTauNENu/I','gTauNMuNu/I','gTauNTauNu/I']
truthVars   = ['htCalc/F','wPhi/F','lostminDeltaR/F','minDeltaR/F','hardestJetPt0/F','hardestJetPt1/F','hardestJetPt2/F','hardestJetPt3/F','wPt/F','st/F','relIso/F', 'mT/F', 'pt/F','eta/F','lostPt/F','lostEta/F','phi/F','lostPhi/F','deltaPhi/F', \
 'hardestJetEta0/F', \
 'hardestJetEta1/F', \
 'hardestJetEta2/F', \
 'hardestJetEta3/F', \
 'hardestJetPhi0/F', \
 'hardestJetPhi1/F', \
 'hardestJetPhi2/F', \
 'hardestJetPhi3/F', \
 'hardestbJetPt0/F', \
 'hardestbJetPt1/F', \
 'hardestbJetPt2/F', \
 'hardestbJetPt3/F', \

]
vars      = copyVars+truthVars

structString = "struct MyStruct{"
structString+= "".join([getTypeStr(v.split('/')[1])+" "+v.split('/')[0]+";" for v in vars])
structString+="}"
ROOT.gROOT.ProcessLine(structString)
exec("from ROOT import MyStruct")
exec("s = MyStruct()")
dir=ROOT.gDirectory.func()

f=ROOT.TFile(ofile, 'recreate')
f.cd()
t = ROOT.TTree( "Events", "Events", 1 )
for v in vars:
 t.Branch(v.split('/')[0],   ROOT.AddressOf(s,v.split('/')[0]), v)
dir.cd()
#cut = "&&".join([doubleLeptonPreselection, hadPresel])
c.Draw(">>eList", doubleLeptonPreselection)
#c.Draw(">>eList", hadPresel)
elist = ROOT.gDirectory.Get("eList")
number_events = elist.GetN()
if small : number_events = n_max
for i in range(number_events):
  c.GetEntry(elist.GetEntry(i))
  if (i%10000 == 0) and i>0 :
    print i,"/",number_events
  s.event = long(c.GetLeaf('event').GetValue())
  if small: print s.event
  for v in copyVars[1:]:
    n=v.split('/')[0]
    #print n
    exec('s.'+n+'='+str(c.GetLeaf(n).GetValue()))
  
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
  #4.1 get generated muon has no match to a reco muon
  lostGenMuons = filter(lambda x:not x['hasMatchInd'], gLeps)
  lostGenMuonsInAcc = filter(lambda x:x['gLepPt']>=15 and abs(x['gLepEta'])<2.1, lostGenMuons)
  #4.2 get reco muon has match but fails looseID
  lostRecoMuons = filter(lambda x:(not(x['isLoose']) and x['hasMatch']), allMuons)
  lostRecoMuonsInAcc = filter(lambda x:x['pt']>=15 and abs(x['eta'])<2.1, lostRecoMuons)

  ##Get Jets
  njets = getVarValue(c, 'njets')
  jets = getGoodJetsStage2(c)
  sorted(jets, key= lambda x: -x['pt'])
  bjets = filter(lambda j:j['btag']>0.679 and abs(j['eta'])<2.4, jets)
  sorted(bjets, key=lambda x: -x['pt'])
  nLostMuons = len(lostGenMuonsInAcc) + len(lostRecoMuonsInAcc)
  #if s.event == 26671039:

  if len(gLepsInAcc)==2 and  len(looseMuonsInAcc)==1 and len(tightMatchedMuons) == 1:

    tightMatchedMuon = tightMatchedMuons[0]
 
    ##take lost leptons:
    if len(lostGenMuonsInAcc)==1 :
      s.lostPt = lostGenMuonsInAcc[0]['gLepPt']
      s.lostEta = lostGenMuonsInAcc[0]['gLepEta']
      s.lostPhi =  lostGenMuonsInAcc[0]['gLepPhi']
    if len(lostRecoMuonsInAcc)==1 : 
      s.lostPt = lostRecoMuonsInAcc[0]['pt']
      s.lostEta = lostRecoMuonsInAcc[0]['eta']
      s.lostPhi = lostRecoMuonsInAcc[0]['phi']

    if small:
      print 'met:', s.met
      print 'number of all reco muons:', len(allMuons) 
      print 'number of all generated muons:', len(gLeps)
      print 'gLeps', gLeps
      print 'all muons', allMuons
      print 'relIso: ' , tightMatchedMuon['relIso']
      print 'lost reco muons fails loose ID:' , lostRecoMuonsInAcc
      print 'lost gen muons:' , lostGenMuonsInAcc
    ##Get hardest jet Pt
    jetsPt = []
    deltaRs = []
    lostDeltaRs = []
    for j in range(int(njets)):
      jet = jets[j]
      if jet:
        jetPt = jet['pt']
        jetsPt.append(jetPt)
        deltaRs.append(deltaR(tightMatchedMuon,jet))
        if len(lostGenMuonsInAcc)==1 : lostDeltaRs.append(deltaR({'phi':lostGenMuonsInAcc[0]['gLepPhi'],'eta':lostGenMuonsInAcc[0]['gLepEta']},jet))
        #if small: print 'lostDeltaRs:' , lostDeltaRs
        if len(lostRecoMuonsInAcc)==1 : lostDeltaRs.append(deltaR(lostRecoMuonsInAcc[0],jet))
        #if small: print 'lostDeltaRs:' , lostDeltaRs
    htCalc =  sum(jetsPt)    

    hardestJetPt0 = -1
    hardestJetPt1 = -1
    hardestJetPt2 = -1
    hardestJetPt3 = -1
    hardestJetEta0 = -100
    hardestJetEta1 = -100
    hardestJetEta2 = -100
    hardestJetEta3 = -100
    hardestJetPhi0 = -100
    hardestJetPhi1 = -100
    hardestJetPhi2 = -100
    hardestJetPhi3 = -100
    hardestbJetPt0 = -1
    hardestbJetPt1 = -1
    hardestbJetPt2 = -1
    hardestbJetPt3 = -1
    if njets>0: 
      hardestJetPt0 = jets[0]['pt']
      mindeltaR = min(deltaRs)
      hardestJetEta0 = jets[0]['eta']
      hardestJetPhi0 = jets[0]['phi']
      if s.nbtags > 0: hardestbJetPt0 = bjets[0]['pt']
      if nLostMuons>0 : lostmindeltaR = min(lostDeltaRs) 
      if njets >1:
        hardestJetPt1 = jets[1]['pt']
        hardestJetEta1 = jets[1]['eta']
        hardestJetPhi1 = jets[1]['phi']
        if s.nbtags > 1: hardestbJetPt1 = bjets[1]['pt']
        if njets >2:
          hardestJetPt2 = jets[2]['pt']
          hardestJetEta2 = jets[2]['eta']
          hardestJetPhi2 = jets[2]['phi']
          if s.nbtags > 2: hardestbJetPt2 = bjets[2]['pt']
          if njets>3:
            hardestJetPt3 = jets[3]['pt']
            hardestJetEta3 = jets[3]['eta']
            hardestJetPhi3 = jets[3]['phi']
            if s.nbtags > 3: hardestbJetPt3 = bjets[3]['pt']
    if small:
      print 'hardest Jet Pt:' , hardestJetPt0
      print 'min DeltaR:' , mindeltaR

    
    #jetsCleaned = [jet for jet in jets if min([deltaR(jet, muon) for muon in looseMuons])>0.4]
    #if small: print 'number of cleaned jets', len(jetsCleaned)
    s.njets = njets 
    s.mT=(sqrt(2*s.met*tightMatchedMuon['pt']*(1-cos(tightMatchedMuon['phi']-s.metPhi))))
    wx = s.met*cos(s.metPhi) + tightMatchedMuon['pt']*cos(tightMatchedMuon['phi'])
    wy = s.met*sin(s.metPhi) + tightMatchedMuon['pt']*sin(tightMatchedMuon['phi'])
    s.wPhi     = atan2(wy,wx)
    s.wPt      = sqrt((wx)**2+(wy)**2) 
#    s.st       = sqrt((s.wPt)**2+(s.mT)**2)
    s.st       = s.met + tightMatchedMuon['pt'] 
    s.pt     = (tightMatchedMuon['pt'])
    s.eta    = (tightMatchedMuon['eta'])
    s.phi    = (tightMatchedMuon['phi'])
    s.deltaPhi = (deltaPhi(tightMatchedMuon['phi'],s.wPhi))
    s.hardestJetPt0 = hardestJetPt0
    s.hardestJetPt1 = hardestJetPt1
    s.hardestJetPt2 = hardestJetPt2
    s.hardestJetPt3 = hardestJetPt3
    s.hardestJetEta0 = hardestJetEta0
    s.hardestJetEta1 = hardestJetEta1
    s.hardestJetEta2 = hardestJetEta2
    s.hardestJetEta3 = hardestJetEta3
    s.hardestJetPhi0 = hardestJetPhi0
    s.hardestJetPhi1 = hardestJetPhi1
    s.hardestJetPhi2 = hardestJetPhi2
    s.hardestJetPhi3 = hardestJetPhi3
    s.hardestbJetPt0 = hardestbJetPt0
    s.hardestbJetPt1 = hardestbJetPt1
    s.hardestbJetPt2 = hardestbJetPt2
    s.hardestbJetPt3 = hardestbJetPt3
    s.htCalc = htCalc
    s.minDeltaR = mindeltaR
    s.lostminDeltaR = lostmindeltaR  
    s.relIso = tightMatchedMuon['relIso']
    t.Fill()

f.cd()
t.Write()
f.Close()
print "Written",f.GetName()
dir.cd()

