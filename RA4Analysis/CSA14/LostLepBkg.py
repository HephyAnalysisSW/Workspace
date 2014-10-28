import ROOT
import pickle
from array import array
from Workspace.RA4Analysis.objectSelection import gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getLooseMuStage2, tightPOGMuID, vetoMuID
from math import sqrt, cos, sin, atan2
from getmuon import getMu, getMuons, getGenLep , getGenLeps
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
maxN=50000

leptonEffMap = pickle.load(file('/data/'+username+'/results2014/muonTemplates/CSA14_TTJets_efficiencyMap_vetoMuIDPt15_ttJetsCSA1450ns_relIso'+str(relIso)+'.pkl'))
leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>15&&abs(muEta)<2.5&&abs(muDxy)<0.2&&abs(muDz)<0.5&&muRelIso<"+str(relIso) 

DoubleGenLeptonPreselection = "ngNuMuFromW==2&&ngNuEFromW==0"
#hadPresel="ht>500&&njets>=3"


copyVars  = ['event/l', 'njets/I','nbtags/F' ,'ht/F', 'met/F', 'metphi/F', 'nvetoMuons/F','ngoodMuons/F','nvetoElectrons/F','gTauPt/F','gTauEta/F','gTauNENu/I','gTauNMuNu/I','gTauNTauNu/I']

ofile ='/data/'+username+'/results2014/muonTuples/CSA14_TTJets_Lost_relIso'+str(relIso)+'.root'
GenVars   = ['GenWeight/F','GenMet/F', 'GenMetPhi/F', 'GenMt/F', 'GenPt/F','GenPtLost/F','TruthMuPhi/F','GenDeltaPhi/F']
vars      = copyVars+GenVars

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


c.Draw(">>eList", DoubleGenLeptonPreselection)
#c.Draw(">>eList", hadPresel)
eList = ROOT.gDirectory.Get("eList")
number_events = eList.GetN()

for i in range(number_events):
  c.GetEntry(eList.GetEntry(i))
  #print i,"/",number_events
  s.event = long(c.GetLeaf('event').GetValue())
  for v in copyVars[1:]:
    n=v.split('/')[0]
    #print n
    exec('s.'+n+'='+str(c.GetLeaf(n).GetValue()))
#  gLeps = getGenLeps(c)
#  muons = getMuons(c,relIso)
  nmuCount = int(c.GetLeaf('nmuCount').GetValue())
  ngoodMuons = c.GetLeaf('ngoodMuons').GetValue()
  nvetoMuons = c.GetLeaf('nvetoMuons').GetValue()
  nvetoElectrons = c.GetLeaf('nvetoElectrons').GetValue()
  njets = c.GetLeaf('njets').GetValue()
  met = c.GetLeaf('met').GetValue()
  genMet = c.GetLeaf('genMet').GetValue()
  ht = c.GetLeaf('ht').GetValue()
  metPhi = c.GetLeaf('metphi').GetValue()
  genMetPhi = c.GetLeaf('genMetPhi').GetValue()
  gLepCount = c.GetLeaf('ngLep').GetValue()
  ngNuMuFromW = c.GetLeaf('ngNuMuFromW').GetValue()
  ngNuEFromW = c.GetLeaf('ngNuEFromW').GetValue()
  ntmuons=0
  nlmuons=0
  muons=[]
  gLeps=[]
  #Get all genLeps
  for p in range(int(gLepCount)):
    genLep = getGenLep(c,p)
    if genLep:
      gLeps.append(genLep)
  for j in range(nmuCount):
    #muon=getMu(c,j)
    #muon=getLooseMuStage2(c,j)
    if muon:
      isTight=tightPOGMuID(muon)
      isLoose=vetoMuID(muon,relIso)
      muon['isTight'] = isTight
      muon['isLoose'] = isLoose
      if isTight: ntmuons+=1
      if isLoose: nlmuons+=1
      hasMatch = False
      for gl in gLeps:
        if gl['gLepInd']==j and gl['gLepDR']<0.4: hasMatch=True
      muon['hasMatch']=hasMatch
      muons.append(muon)
  lostGenLeps = filter(lambda gl:not(gl['gLepInd']>=0 and gl['gLepDR']<0.4) and gl['gLepPt']>15 and abs(gl['gLepEta'])<2.5, gLeps)
  lostnotloose = filter(lambda x:x['hasMatch'] and (not(x['isLoose'])), muons) 
  tightMatchedMuons = filter(lambda x:x['hasMatch'] and x['isTight'], muons)        
  tightMuons = filter(lambda x:x['isTight'], muons)
  LooseMuons = filter(lambda x:x['isLoose'], muons)

  print 'number of lost muons because no reconstruction at all:',len(lostGenLeps)
  print 'number of lost muons because there is reconstruction but the recomuons are not loose at all:', len(lostnotloose)
  nLostMuons = len(lostGenLeps) + len(lostnotloose) 
  print 'nLostMuons:', nLostMuons
  s.weight=c.GetLeaf('weight').GetValue()

  if len(muons)==2 or len(muons)==1:
    if len(tightMuons)==1 and len(LooseMuons)==1:
      if len(tightMatchedMuons)==1 and nLostMuons==1:
        if len(lostGenLeps)==1:
          lostGenMuon = lostGenLeps[0]
          s.GenPtLost=(lostGenMuon['gLepPt'])
        if len(lostnotloose)==1:
          lostGenMuon = lostnotloose[0]
          s.GenPtLost=(lostGenMuon['pt'])            
        if len(tightMatchedMuons) >1 : print "Warning"
        TightMatchedMuon = tightMatchedMuons[0]
        s.GenWeight = s.weight
        s.GenMt=(sqrt(2*s.met*TightMatchedMuon['pt']*(1-cos(TightMatchedMuon['phi']-s.metphi))))
        s.GenMet= s.met
        s.GenPt=(TightMatchedMuon['pt'])
        s.TruthMuPhi=(TightMatchedMuon['phi'])
        s.MetPhi=s.metphi
        s.GenDeltaPhi=(cos(TightMatchedMuon['phi']-s.metphi))
        t.Fill()

f.cd()
t.Write()
f.Close()
print "Written",f.GetName()
dir.cd()

