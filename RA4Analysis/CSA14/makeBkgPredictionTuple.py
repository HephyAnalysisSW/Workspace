import ROOT
import pickle
from array import array
from Workspace.RA4Analysis.objectSelection import getGenLepsWithMatchInfo,getGenLeps, getMuons, gTauAbsEtaBins, gTauPtBins, metParRatioBins, jetRatioBins
from Workspace.HEPHYPythonTools.helpers import findClosestObject,deltaR,getVarValue, getObjFromFile
from Workspace.RA4Analysis.objectSelection import getGoodJetsStage2,getLooseMuStage2, tightPOGMuID, vetoMuID
from math import sqrt, cos, sin, atan2
from Workspace.RA4Analysis.helpers import deltaPhi
from localInfo import username
from Workspace.RA4Analysis.stage2Tuples import *
c = ROOT.TChain('Events')
#for b in ttJetsCSA1450ns['bins']:
#  c.Add(ttJetsCSA1450ns['dirname']+'/'+b+'/histo_ttJetsCSA1450ns_from*.root')
#c.Add('/data/schoef/convertedTuples_v25/copyMET/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*.root')
#mode='dilep'
#c.Add('/data/schoef/convertedTuples_v24/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*')
c.Add('/data/schoef/convertedTuples_v26/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*.root')
mode='dilep'
relIso = 0.3
effUp = 1.1
effDown = 0.9
small = True
maxN=1000

if mode=='had':
  leptonEffMap = pickle.load(file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_vetoLeptonEfficiencyMap.pkl'))
  #leptonEffMap = pickle.load(file('/data/easilar/results2014/tauTemplates/CSA14_TTJets_efficiencyMap_vetoMuIDPt15_ttJetsCSA1450ns_relIso0.3.pkl'))
  doubleLeptonPreselection = "ngoodMuons>=1&&nvetoMuons==2&&nvetoElectrons==0"
  templates = pickle.load(file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_genTau.pkl'))
  ofile =                      '/data/easilar/results2014/tauTuples/CSA14_TTJets_hadGenTauTryBtag110.root'
if mode=='lep':
  leptonEffMap = pickle.load(file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_vetoLeptonEfficiencyMap.pkl'))
  doubleLeptonPreselection = "ngoodMuons>=1&&nvetoMuons==2&&nvetoElectrons==0"
  templates = pickle.load(file('/data/schoef/results2014/tauTemplates/CSA14_TTJets_lepGenTau.pkl'))
  ofile =                      '/data/schoef/results2014/tauTuples/CSA14_TTJets_lepGenTau.root'
if mode=='dilep':
  leptonEffMap = pickle.load(file('/data/'+username+'/results2014/muonTemplates/CSA14_TTJets_efficiencyMap_v26_vetoMuIDPt15_ttJetsCSA1450ns_v26_relIso'+str(relIso)+'.pkl'))
  #leptonEffMap = pickle.load(file('/data/easilar/results2014/muonTemplates/CSA14_TTJets_efficiencyMap_vetoMuIDPt15_ttJetsCSA1450ns_relIso'+str(relIso)+'.pkl'))
  leptonID = "muIsPF&&(muIsGlobal||muIsTracker)&&muPt>15&&abs(muEta)<2.5&&abs(muDxy)<0.2&&abs(muDz)<0.5&&muRelIso<"+str(relIso)
  doubleLeptonPreselection = "gLepCount==2&&ngNuMuFromW==2&&ngNuEFromW==0" #&&ngoodMuons>=1&&Sum$("+leptonID+")==2&&nvetoElectrons==0"
  #ofile =                    '/data/easilar/results2014/muonTuples/CSA14_TTJets_diLep_v26_relIso'+str(relIso)+'.root'
  ofile =                    '/data/easilar/results2014/muonTuples/deneme_diLep.root'
  if small : ofile = '/data/easilar/results2014/muonTuples/CSA14_TTJets_diLep_Small_relIso'+str(relIso)+'.root'
if mode=='had' or mode=='lep':
  for ptk in templates.keys():
    for etak in templates[ptk].keys():
      templates[ptk][etak].Scale(1./templates[ptk][etak].Integral())
      res=[]
      for b in range(1, 1+templates[ptk][etak].GetNbinsX()):
        res.append({'frac':templates[ptk][etak].GetBinCenter(b), 'weight':templates[ptk][etak].GetBinContent(b)})
      templates[ptk][etak]=res

def getTwoMuons(c):
  nmuCount = int(getVarValue(c, 'muCount' ))
  res=[]
  nt=0
  nl=0
  for i in range(nmuCount):
    l=getLooseMuStage2(c, i)
    isTight=tightPOGMuID(l)
    isLoose=vetoMuID(l, relIso=relIso)
    l['isTight'] = isTight 
    l['isLoose'] = isLoose
    if isTight:nt+=1
    if isLoose:nl+=1
    if isTight or isLoose: res.append(l)
    if isTight and not isLoose:
      print "Warning!! Tight but not loose!!",l
  if len(res)!=2: print "Warning: found",len(res),'muons -> inconsistent with preselection!!'
  if not (nt>=1 and nl==2):print "Warning! Not >=1 tight and ==2 loose -> Inconsistent w/ preselection"
  return res

def getTypeStr(s):
  if s=='l': return 'ULong64_t'
  if s=='F': return 'Float_t'
  if s=='I': return 'Int_t'

copyVars  = ['event/l','nbtags/I', 'njets/I', 'ht/F', 'met/F', 'metPhi/F', 'nvetoMuons/I']
newVars   = ['njetsPred/I','lostRelIso/F','relIso/F',\
'eff/F','combFac/I' ,'lostPt/F','lostEta/F','lostPhi/F','htPred/F','pt/F','eta/F','phi/F','wPhi/F','wPt/F','st/F' ,'wPhiPred/F','wPtPred/F','stPred/F' ,'metPred/F', 'metPhiPred/F','weight/F', 'mT/F', 'mTPred/F', 'scaleLEff/F','scaleLEffUp/F','scaleLEffDown/F','deltaPhi/F','deltaPhiPred/F', \
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
'effTight/F'\
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
##muon Inc jets..
'jetIncMuPt[16]/F', \
'jetIncMuEta[16]/F', \
'jetIncMuPhi[16]/F', \
'bJetIncMuCSVMPt[16]/F', \
'bJetIncMuCSVMEta[16]/F', \
'bJetIncMuCSVMPhi[16]/F', \
'bJetIncMuCSVLPt[16]/F', \
'bJetIncMuCSVLEta[16]/F', \
'bJetIncMuCSVLPhi[16]/F', \
'nonbJetIncMuCSVMPt[16]/F', \
'nonbJetIncMuCSVMEta[16]/F', \
'nonbJetIncMuCSVMPhi[16]/F', \
'nonbJetIncMuCSVLPt[16]/F', \
'nonbJetIncMuCSVLEta[16]/F', \
'nonbJetIncMuCSVLPhi[16]/F', \

]

vars      = copyVars+newVars  

structString = "struct MyStruct{"
structString+= "".join([getTypeStr(v.split('/')[1])+" "+v.split('/')[0]+";" for v in vars])
structString+= "".join([getTypeStr(v.split('/')[1])+" "+v.split('/')[0]+";" for v in vectorVars])
structString+="}"   
print structString
ROOT.gROOT.ProcessLine(structString)
exec("from ROOT import MyStruct")
exec("s = MyStruct()")
dir=ROOT.gDirectory.func()

f=ROOT.TFile(ofile, 'recreate')
f.cd()
t = ROOT.TTree( "Events", "Events", 1 )
for v in vars:
 t.Branch(v.split('/')[0],   ROOT.AddressOf(s,v.split('/')[0]), v) 
for v in vectorVars:
  t.Branch(v.split('[')[0], ROOT.AddressOf(s,v.split('[')[0]),v)
dir.cd()

c.Draw(">>eList", doubleLeptonPreselection)
eList = ROOT.gDirectory.Get("eList")
number_events = eList.GetN()
if small:
  if number_events>maxN:
    number_events=maxN
number_events=min(number_events, eList.GetN())
countLeptons=0
for i in range(number_events):
  if (i%10000 == 0) and i>0 :
    print i,"/",number_events
  c.GetEntry(eList.GetEntry(i))
  s.event = long(c.GetLeaf('event').GetValue())
  if small: 
    print '**************'
    print s.event
  for v in copyVars[1:]:
    n=v.split('/')[0]
    exec('s.'+n+'='+str(c.GetLeaf(n).GetValue()))
  for v in newVars[:]:
   n=v.split('/')[0]
   exec('s.'+n+'='+str(-1000))
  for v in vectorVars[:]:
    n=v.split('[')[0]
    for i in range(16):
      exec('s.'+n+'['+str(i)+']='+str(-1000))

  #muons = getTwoMuons(c)

  #1.Get All gen Leps
  gLeps = getGenLepsWithMatchInfo(c,relIso) ##get All muons
  #1.1 Get all gen leps in acc
  gLepsInAcc = filter(lambda x:x['gLepPt']>=15 and abs(x['gLepEta'])<2.1, gLeps)
  #2.Get all reco muons
  allMuons = getMuons(c,relIso,gLeps)
  #2.1 Get loose muons
  looseMuons = filter(lambda x:x['isLoose'], allMuons) 
  #2.2 Get loose and tight matched muons
  looseMatchedMuons = filter(lambda x:x['isLoose'] and x['hasMatch'], allMuons) 
  tightMatchedMuons = filter(lambda x:x['isTight'] and x['hasMatch'], allMuons)

  ##Get Jets
  njets = getVarValue(c, 'njets')
  nbtags = getVarValue(c, 'nbtags')
  jets = getGoodJetsStage2(c)
  sorted(jets, key= lambda x: -x['pt'])
  if small: print 'ALL JETS: ', jets
  bjetsCSVM = filter(lambda j:j['btag']>0.679 and abs(j['eta'])<2.4, jets)
  sorted(bjetsCSVM, key=lambda x: -x['pt'])
  bjetsCSVL = filter(lambda j:j['btag']>0.246 and abs(j['eta'])<2.4, jets)
  sorted(bjetsCSVL, key=lambda x: -x['pt'])
  nonbjetsCSVM = filter(lambda j:not(j['btag']>0.679 and abs(j['eta'])<2.4), jets)
  sorted(nonbjetsCSVM, key=lambda x: -x['pt'])
  nonbjetsCSVL = filter(lambda j:not (j['btag']>0.246 and abs(j['eta'])<2.4), jets)
  sorted(nonbjetsCSVL, key=lambda x: -x['pt'])


  if small :
    print 'njets', len(jets)
    print 'nloosemuons' , len(looseMuons)
  #if len(looseMuons) >0: 
  #   jetsCleaned = [jet for jet in jets if min([deltaR(jet, muon) for muon in looseMuons])>0.4]
  #   if small: print 'number of cleaned jets', len(jetsCleaned)

  if (len(looseMatchedMuons)==2 and len(tightMatchedMuons)>=1 and len(gLepsInAcc)==2) :
    assert len(looseMatchedMuons)==2, "Problem in event "+str(int(c.GetLeaf('event').GetValue()))
    if looseMuons[0]['isTight'] and looseMuons[1]['isTight']:
      s.combFac = 0.5
    else:
      s.combFac = 1
    for perm in [looseMatchedMuons, reversed(looseMatchedMuons)]:
      m,m2 = perm
      if m2['isTight']:
#        print iperm, m['isTight'],m2['isTight']
#        print "pt",m['pt'],m['phi'],m['eta']
        abseta=abs(m['eta'])
        if abseta>2.5:continue

        s.weight=c.GetLeaf('weight').GetValue()
        lEffL = leptonEffMap.FindBin( m['pt'], m['eta'])
        lEffT = leptonEffMap.FindBin( m2['pt'], m2['eta'])
        lEffi = leptonEffMap.GetBinContent(lEffL)
        lEfft = leptonEffMap.GetBinContent(lEffT)
        if lEffi>0.5 and lEfft>0.5:
          lEffUp = max((lEffi*effUp)-(effUp-1),0)
          lEffDown = min((lEffi*effDown)+(1-effDown),1)
          lEff = lEffi
          if mode=='dilep':
            ##Jet Staff 

            if len(jets)>0:
              closestObj = findClosestObject(jets,m)
              closestJet = closestObj['obj']
              if small: print closestJet
              s.closestJetPt  = closestJet['pt']
              s.closestJetPdg = closestJet['pdg']
              s.closestJetPhi = closestJet['phi']
              s.closestJetEta = closestJet['eta']
              s.closestJetChef  = closestJet['chef']
              s.closestJetNhef  = closestJet['nhef']
              s.closestJetHFhef = closestJet['hFhef']
              s.closestJetHFeef = closestJet['hFeef']
              s.closestJetMuef  = closestJet['muef']
              s.closestJetElef  = closestJet['elef']
              s.closestJetPhef  = closestJet['phef']
              s.mindeltaRAllJets = sqrt(findClosestObject(jets,m2)['distance'])
              s.minlostdeltaRAllJets = sqrt(closestObj['distance'])
            if len(bjetsCSVM)>0:    s.mindeltaRBM          = sqrt(findClosestObject(bjetsCSVM,m2)['distance'])
            if len(bjetsCSVL)>0:    s.mindeltaRBL          = sqrt(findClosestObject(bjetsCSVL,m2)['distance'])
            if len(nonbjetsCSVM)>0: s.mindeltaRNonBM       = sqrt(findClosestObject(nonbjetsCSVM,m2)['distance'])
            if len(nonbjetsCSVL)>0: s.mindeltaRNonBL       = sqrt(findClosestObject(nonbjetsCSVL,m2)['distance'])
            if len(bjetsCSVM)>0:    s.minlostdeltaRBM      = sqrt(findClosestObject(bjetsCSVM,m)['distance'])
            if len(bjetsCSVL)>0:    s.minlostdeltaRBL      = sqrt(findClosestObject(bjetsCSVL,m)['distance'])
            if len(nonbjetsCSVM)>0: s.minlostdeltaRNonBM   = sqrt(findClosestObject(nonbjetsCSVM,m)['distance'])
            if len(nonbjetsCSVL)>0: s.minlostdeltaRNonBL   = sqrt(findClosestObject(nonbjetsCSVL,m)['distance'])

            for j in range(int(njets)):
              jet = jets[j]
              if jet:
                s.jetPt[j] = jet['pt']
                s.jetEta[j] = jet['eta']
                s.jetPhi[j] = jet['phi']
                s.jetPdg[j] = jet['pdg']
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


            ##Add loose muon to jet collections
            
            if m['pt'] > 30 :
              s.njetsPred = njets + 1
              s.htPred   = s.ht + m['pt']

            s.eff = lEff
            s.effTight = lEfft 
            s.scaleLEff = (1-lEff)/lEff
            s.scaleLEffUp = (1-lEffUp)/lEffUp
            s.scaleLEffDown = (1-lEffDown)/lEffDown 
            metx = s.met*cos(s.metPhi)+cos(m['phi'])*m['pt']
            mety = s.met*sin(s.metPhi)+sin(m['phi'])*m['pt']
            s.nbtags = s.nbtags
              
            s.pt     = m2['pt'] 
            s.eta    = m2['eta']
            s.phi    = m2['phi']
            s.lostPt    = m['pt']
            s.lostEta   = m['eta']
            s.lostPhi   = m['phi']
            s.weight = s.weight
            s.metPred = sqrt(metx**2+mety**2)
            s.metPhiPred = atan2(mety,metx)
            s.mTPred = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metPhiPred)))
            s.mT = sqrt(2.*s.met*m2['pt']*(1-cos(m2['phi']-s.metPhi)))
            wx = s.metPred*cos(s.metPhiPred) + m2['pt']*cos(m2['phi'])
            wy = s.metPred*sin(s.metPhiPred) + m2['pt']*sin(m2['phi'])
            wx_ = s.met*cos(s.metPhi) + m2['pt']*cos(m2['phi'])
            wy_ = s.met*sin(s.metPhi) + m2['pt']*sin(m2['phi'])
            s.wPhiPred     = atan2(wy,wx)
            s.wPhi     = atan2(wy_,wx_)
            s.wPtPred      = sqrt((wx)**2+(wy)**2)
            s.wPt    = sqrt((wx_)**2+(wy_)**2)
            s.stPred       = m2['pt'] + s.metPred 
            s.st       = m2['pt'] + s.met 
            s.deltaPhiPred = deltaPhi(s.wPhiPred,m2['phi'])
            s.deltaPhi = deltaPhi(s.wPhi,m2['phi'])
            s.relIso = m2['relIso']
            s.lostRelIso = m['relIso']
            t.Fill()
            if small:
              print 'metPred:' , s.metPred
              print 'nglep in acc:' , len(gLepsInAcc)
              print 'nloose matched muons:' , len(looseMatchedMuons)
              print 'generated leps in acc:', gLepsInAcc
              print 'loose matched muons:', looseMatchedMuons
              print '****'
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
#            if lEff>0:
            s.scaleLEff = 1./lEff
#            else:
#              s.scaleLEff = 1.
            for p in template:
              metpar    = p['frac']*m['pt']
              MEx = s.met*cos(s.metPhi)+cos(m['phi'])*metpar
              MEy = s.met*sin(s.metPhi)+sin(m['phi'])*metpar
              wx = MEx+cos(m2['phi'])*m2['pt']
              wy = MEy+sin(m2['phi'])*m2['pt'] 
              if mode=='had':
                s.weight = p['weight']*s.weight
    #            s.nvetoMuonsPred = s.nvetoMuons 
                jetpt =  (1.-p['frac'])*m['pt']
                if jetpt>30.:
                  s.njetsPred = s.njets+1
                  s.htPred    = s.ht+jetpt
                else:
                  s.njetsPred = s.njets
                  s.htPred    = s.ht
                s.metPred      = sqrt(MEx**2+MEy**2)
                s.metPhiPred   = atan2(MEy,MEx)
                s.mT       = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metPhiPred)))
                s.wPt      = sqrt(wx**2+wy**2)
                s.wPhi     = atan2(wy,wx)
                s.st       = sqrt((s.wPt)**2+(s.mT)**2)
                s.deltaPhi = deltaPhi(s.wPhi,m2['phi'])
                t.Fill()
              if mode=='lep':
                s.njetsPred = s.njets
                s.htPred   = s.ht
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
                s.metPhiPred = atan2(MEy,MEx)
                s.mT = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metPhiPred)))
                t.Fill()
    #                #lepton reconstructed ->not filled
    ##                s.nvetoMuonsPred = s.nvetoMuons + 1 
    #                s.weightPred = p['weight']*s.weight*nlEff
    #                s.metPred = sqrt(MEx**2+MEy**2)
    #                s.metPhiPred = atan2(MEy,MEx)
    #                s.mTPred = sqrt(2.*s.metPred*m2['pt']*(1-cos(m2['phi']-s.metPhiPred)))
    #                t.Fill()
                    #lepton lost
    #                s.nvetoMuonsPred = s.nvetoMuons  


f.cd()
t.Write()
f.Close()
print "Written",f.GetName()
dir.cd()

