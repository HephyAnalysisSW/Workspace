import ROOT
import pickle
from array import array
from Workspace.RA4Analysis.objectSelection import getGoodJetsStage2,gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import getVarValue, getObjFromFile
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
c.Add('/data/schoef/convertedTuples_v24/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
small = False
n_max = 100
relIso = 0.12
doubleLeptonPreselection = "ngLep==2&&ngNuMuFromW==2&&ngNuEFromW==0"

leptonEffMap = pickle.load(file('/data/'+username+'/results2014/muonTemplates/CSA14_TTJets_efficiencyMap_vetoMuIDPt15_ttJetsCSA1450ns_relIso'+str(relIso)+'.pkl'))
leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>15&&abs(muEta)<2.5&&abs(muDxy)<0.2&&abs(muDz)<0.5&&muRelIso<"+str(relIso) 

ofile ='/data/'+username+'/results2014/muonTuples/CSA14_TTJets_Lost_relIso'+str(relIso)+'.root'
if small: ofile ='/data/'+username+'/results2014/muonTuples/CSA14_TTJets_Lost_small_relIso'+str(relIso)+'.root'

copyVars  = ['event/l','weight/F', 'njets/I','nbtags/F' ,'ht/F', 'met/F', 'metphi/F', 'nvetoMuons/F','ngoodMuons/F','nvetoElectrons/F','gTauPt/F','gTauEta/F','gTauNENu/I','gTauNMuNu/I','gTauNTauNu/I']
truthVars   = ['wPhi/F','hardestJetPt/F','wPt/F','st/F','relIso/F', 'mT/F', 'pt/F','eta/F','lostPt/F','lostEta/F','phi/F','lostPhi/F','deltaPhi/F']
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
  looseMatchedMuons = filter(lambda x:x['isLoose'] and x['hasMatch'], allMuons)
  looseMuonsInAcc = filter(lambda x:x['pt']>=15 and abs(x['eta'])<2.1, looseMuons)
  #3. get tight muons that are matched
  tightMuons = filter(lambda x:x['isTight'], allMuons)
  tightMatchedMuons = filter(lambda x:x['isTight'] and x['hasMatch'], allMuons)
  #4. get Lost muons 
  #4.1 get generated muon has no match to a reco muon
  lostGenMuons = filter(lambda x:not x['hasMatchInd'], gLeps)
  lostGenMuonsInAcc = filter(lambda x:x['gLepPt']>=15 and abs(x['gLepEta'])<2.1, lostGenMuons)
  #4.2 get reco muon has match but fails looseID
  lostRecoMuons = filter(lambda x:(not(x['isLoose']) and x['hasMatch']), allMuons)
  lostRecoMuonsInAcc = filter(lambda x:x['pt']>=15 and abs(x['eta'])<2.1, lostRecoMuons)

  ##Get Jets
  njets = getVarValue(c, 'njetCount')
  jets = getGoodJetsStage2(c)
  ##Get hardest jet Pt 
  jetsPt = []
  for j in range(int(njets)):
    jetPt = jets[j]['pt']
    jetsPt.append(jetPt)
  if njets>0:   hardestJetPt = max(jetsPt)
  nLostMuons = len(lostGenMuons) + len(lostRecoMuons)
  #if s.event == 26671039:

  if len(gLepsInAcc)==2 and len(looseMuonsInAcc)==1 and len(tightMatchedMuons) == 1:

    ##take lost leptons:
    if len(lostGenMuonsInAcc)==1 :
      s.lostPt = lostGenMuonsInAcc[0]['gLepPt']
      s.lostEta = lostGenMuonsInAcc[0]['gLepEta']
      s.lostPhi =  lostGenMuonsInAcc[0]['gLepPhi']
    if len(lostRecoMuonsInAcc)==1 : 
      s.lostPt = lostRecoMuonsInAcc[0]['pt']
      s.lostEta = lostRecoMuonsInAcc[0]['eta']
      s.lostPhi = lostRecoMuonsInAcc[0]['phi']
    tightMatchedMuon = tightMatchedMuons[0]
    if small:
      print 'met:', s.met
      print 'number of all reco muons:', len(allMuons) 
      print 'number of all generated muons:', len(gLeps)
      print 'gLeps', gLeps
      print 'all muons', allMuons
      print 'relIso: ' , tightMatchedMuon['relIso']
      print 'lost reco muons fails loose ID:' , lostRecoMuonsInAcc
      print 'lost gen muons:' , lostGenMuonsInAcc
      print 'hardest Jet Pt:' , hardestJetPt
    s.mT=(sqrt(2*s.met*tightMatchedMuon['pt']*(1-cos(tightMatchedMuon['phi']-s.metphi))))
    wx = s.met*cos(s.metphi) + tightMatchedMuon['pt']*cos(tightMatchedMuon['phi'])
    wy = s.met*sin(s.metphi) + tightMatchedMuon['pt']*sin(tightMatchedMuon['phi'])
    s.wPhi     = atan2(wy,wx)
    s.wPt      = sqrt((wx)**2+(wy)**2) 
#    s.st       = sqrt((s.wPt)**2+(s.mT)**2)
    s.st       = s.met + tightMatchedMuon['pt'] 
    s.pt     = (tightMatchedMuon['pt'])
    s.eta    = (tightMatchedMuon['eta'])
    s.phi    = (tightMatchedMuon['phi'])
    s.deltaPhi = (deltaPhi(tightMatchedMuon['phi'],s.wPhi))
    s.hardestJetPt = hardestJetPt
    s.relIso = tightMatchedMuon['relIso']
    t.Fill()

f.cd()
t.Write()
f.Close()
print "Written",f.GetName()
dir.cd()

