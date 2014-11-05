import ROOT
import pickle
from array import array
from Workspace.RA4Analysis.objectSelection import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getGenLeps, getMuons, getLooseMuStage2, getGenLep ,tightPOGMuID, vetoMuID
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

relIso = 0.3
small = True
max =100

leptonEffMap = pickle.load(file('/data/'+username+'/results2014/muonTemplates/CSA14_TTJets_efficiencyMap_vetoMuIDPt15_ttJetsCSA1450ns_relIso'+str(relIso)+'.pkl'))
leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>15&&abs(muEta)<2.5&&abs(muDxy)<0.2&&abs(muDz)<0.5&&muRelIso<"+str(relIso) 

doubleLeptonPreselection = "ngLep==2&&ngNuMuFromW==2&&ngNuEFromW==0"
copyVars  = ['event/l', 'njets/I','nbtags/F' ,'ht/F', 'met/F', 'metphi/F', 'nvetoMuons/F','ngoodMuons/F','nvetoElectrons/F','gTauPt/F','gTauEta/F','gTauNENu/I','gTauNMuNu/I','gTauNTauNu/I']

ofile ='/data/'+username+'/results2014/muonTuples/CSA14_TTJets_Lost_New_New_relIso'+str(relIso)+'.root'
truthVars   = ['wPhiTruth/F','weightTruth/F','metTruth/F','wPtTruth/F','stTruth/F','htTruth/F','njetsTruth/I' ,'metPhiTruth/F', 'mTTruth/F', 'muPtTruth/F','ptLostTruth/F','muPhiTruth/F','deltaPhiTruth/F']
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
#eList = ROOT.TList()
c.Draw(">>eList", doubleLeptonPreselection)
#c.Draw(">>eList", hadPresel)
elist = ROOT.gDirectory.Get("eList")
number_events = elist.GetN()
if small: number_events = max
for i in range(number_events):
  c.GetEntry(elist.GetEntry(i))
  #if (i%10000 == 0) and i>0 :
    #print i,"/",number_events
  s.event = long(c.GetLeaf('event').GetValue())
  print s.event
  for v in copyVars[1:]:
    n=v.split('/')[0]
    #print n
    exec('s.'+n+'='+str(c.GetLeaf(n).GetValue()))
  gLeps = getGenLeps(c)
  muons = getMuons(c,relIso,gLeps)

  lostGenLeps = filter(lambda gl:not(gl['gLepInd']>=0 and gl['gLepDR']<0.4) and gl['gLepPt']>15 and abs(gl['gLepEta'])<2.5, gLeps)
  lostRecoMuons = filter(lambda x:x['hasMatch'] and (not(x['isLoose'])), muons)
  tightMatchedRecoMuons = filter(lambda x:x['hasMatch'] and x['isTight'], muons)        
  tightRecoMuons = filter(lambda x:x['isTight'], muons)
  looseRecoMuons = filter(lambda x:x['isLoose'], muons)
  #lostLeptons = filter(lambda x:not(x['hasMatch'] and x['isLoose']), muons)        
  #nLostMuons = len(lostLeptons)
  #if nLostMuons>0: print lostLeptons
  nLostMuons = len(lostGenLeps) + len(lostRecoMuons)
  if nLostMuons >0:
    print 'nLostMuons:', nLostMuons
    print 'number of lost muons because no reconstruction at all:',len(lostGenLeps)
    print 'number of lost muons because there is reconstruction but the recomuons are not loose at all:', len(lostRecoMuons)
  s.weight=c.GetLeaf('weight').GetValue()

  if len(muons)==2 or len(muons)==1:
    if len(tightMatchedRecoMuons)==1 and len(looseRecoMuons)==1:
      if not nLostMuons==1: continue
      if len(lostGenLeps)==1:
        #lostGenMuon = lostGenLeps[0]
        s.ptLostTruth =(lostGenLeps[0]['gLepPt'])
      if len(lostRecoMuons)==1:
        #lostGenMuon = lostRecoMuons[0]
        s.ptLostTruth = lostRecoMuons[0]['pt']
      if len(tightMatchedRecoMuons) >1 : print "Warning"
      print 'genLeps:' , gLeps
      print 'numebr of reco muons:', len(muons)
      print 'number of loose reco muons:', len(looseRecoMuons)
      print 'number of tight reco muons:' , len(tightRecoMuons)
      print 'n tight matched muons:', len(tightMatchedRecoMuons)
      print 'tight matched muons:', tightMatchedRecoMuons
      print 'lost gen leps:', lostGenLeps
      print 'lostRecoMuons:', lostRecoMuons 
      tightMatchedRecoMuon = tightMatchedRecoMuons[0]
      s.weightTruth = s.weight
      s.mTTruth=(sqrt(2*s.met*tightMatchedRecoMuon['pt']*(1-cos(tightMatchedRecoMuon['phi']-s.metphi))))
      wx = s.met*cos(s.metphi) + tightMatchedRecoMuon['pt']*cos(tightMatchedRecoMuon['phi'])
      wy = s.met*sin(s.metphi) + tightMatchedRecoMuon['pt']*sin(tightMatchedRecoMuon['phi'])
      s.wPhiTruth     = atan2(wy,wx)
      s.wPtTruth      = sqrt((wx)**2+(wy)**2) 
      s.stTruth       = sqrt((s.wPtTruth)**2+(s.mTTruth)**2)
      s.metTruth      = s.met
      s.htTruth       = s.ht
      s.njetsTruth    = s.njets
      s.muPtTruth     = (tightMatchedRecoMuon['pt'])
      s.muPhiTruth    = (tightMatchedRecoMuon['phi'])
      s.metPhiTruth   = s.metphi
      s.deltaPhiTruth = (deltaPhi(tightMatchedRecoMuon['phi'],s.wPhiTruth))
      t.Fill()

f.cd()
t.Write()
f.Close()
print "Written",f.GetName()
dir.cd()

