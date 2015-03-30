import ROOT
from array import array
import pickle
from math import sqrt

from Workspace.HEPHYPythonTools.helpers import getObjDict

small = True
c = ROOT.TChain('Events')
#c.Add(' ~/data/ttJetsCSA1450ns_*.root')
c.Add('/data/schoef/convertedTuples_v26/copyInc/ttJetsCSA1450ns/histo_ttJetsCSA1450ns_from*.root')
def getVarValue(c, var, i=0):
  return c.GetLeaf(var).GetValue(i)


#boolean function for acceptance
def acceptance(lep):
  return lep['pt']>15 and abs(lep['eta'])<1.0
#boolean function for loose ID
def looseID(lep):
  return abs(lep['dxy'])<0.05 and abs(lep['dz'])<0.2 and lep['relIso03']<0.2 
def tightID(lep):
  return looseID(lep) and lep['relIso03']<0.12 and lep['tightId']

def deltaPhi( phi1, phi2):
  Pi = ROOT.TMath.Pi()
  dphi = phi2-phi1
  if  dphi > Pi:
    dphi -= 2.0*Pi
  if dphi <= -Pi:
    dphi += 2.0*Pi
  return abs(dphi)

def deltaR2(obj1, obj2):
  return deltaPhi(obj1['phi'], obj2['phi'])**2 + (obj1['eta'] - obj2['eta'])**2

def deltaRMatch(obj1, obj2):
  return deltaR2(obj1, obj2) < 0.05**2

def match(obj1, obj2):
  ptRel = obj1['pt']/obj2['pt']
  match = 0.7<ptRel and ptRel<1.5 and obj1['pdgId']==obj2['pdgId'] and deltaRMatch(obj1, obj2)
#  if match:
#    print sqrt(deltaR2(obj1, obj2)), ptRel, obj1['pdgId'], obj2['pdgId']
  return match
  
#get all gen muons in acceptance
def getGenMuonsInAcceptance(c):
  ngenLep = int(getVarValue(c, 'ngenLep'))
  gleps=[] 
  for i in range(ngenLep):
    glep = getObjDict(c, 'genLep_', ['pt','eta', 'pdgId'], i)
    if abs(glep['pdgId'])==13 and acceptance(glep):
      glep.update(getObjDict(c, 'genLep_', ['sourceId', 'phi'], i))
      gleps.append(glep)
  return gleps   

#get all loose reco muons in acceptance
def getLooseMuonsInAcceptance(c):
  nLepGood = int(getVarValue(c, 'nLepGood'))
  mus=[] 
  for i in range(nLepGood):
    mu = getObjDict(c, 'LepGood_', ['pt','eta', 'pdgId'], i)
    if abs(mu['pdgId'])==13 and acceptance(mu):
      mu.update(getObjDict(c, 'LepGood_', ['tightId', 'relIso03', 'dxy','dz', 'phi', 'jetPtRatio', 'jetBTagCSV', 'jetDR', 'mcMatchId', 'mcMatchAny'], i))
      mus.append(mu)
  return mus   

def getJets(c):
  nJet = int(getVarValue(c, 'nJet'))
  jets=[] 
  for i in range(nJet):
    jet = getObjDict(c, 'Jet_', ['pt','eta'], i)
    if True:
      jet.update(getObjDict(c, 'Jet_', ['phi', 'mcFlavour', 'mcMatchId', 'mcMatchFlav'], i))
    jets.append(jet)
  return jets   

##Calculate efficiencies
#ROOT.gStyle.SetOptStat(0)
##define efficiency histo
#ptBinsCoarse  = array('d', [float(x) for x in range(10, 20)+range(20,50,5)+range(50,100,20)+range(100,310,50)])
#etaBinsCoarse = array('d', [float(x)/10. for x in [-30,-25]+range(-21,22,6)+[25,30]])
#looseMuPtEta2DEff = ROOT.TProfile2D('muPtEta2DEff','muPtEta2DEff',len(ptBinsCoarse)-1,ptBinsCoarse, len(etaBinsCoarse)-1,etaBinsCoarse)
#cut = "Sum$(genLep_pt>15&&abs(genLep_eta)<2.1)>0" #Consider only events with at least one gen muon -> accelerates loop
#c.Draw(">>eList", cut, 'goff')
#eList = ROOT.gDirectory.Get('eList')
#nEvents = eList.GetN()
#nEvents = nEvents if not small else min(1000, nEvents)
#for nev in range(nEvents):
#  if nev%100000==0:
#    print nev,'/',nEvents
#  c.GetEntry(eList.GetEntry(nev))
#  genMuonsInAcceptance    = getGenMuonsInAcceptance(c) #get gen muons
#  if len(genMuonsInAcceptance)==0: continue #redundant with selection
#  looseMuonsInAcceptance  = getLooseMuonsInAcceptance(c)
#  for gLep in genMuonsInAcceptance:
#    matched = False
#    for mu in looseMuonsInAcceptance:
#      if match(gLep, mu): 
#        matched = True
#        break
#    looseMuPtEta2DEff.Fill(gLep['pt'], gLep['eta'], matched)
#del eList
#c1 = ROOT.TCanvas()
#looseMuPtEta2DEff.Draw('colz')
#c1.Print('/Users/robertschoefbeck/Desktop/looseMuPtEta2DEff.png')
#if not small:
#  pickle.dump(looseMuPtEta2DEff, file('/Users/robertschoefbeck/CloudStation/Workspace/RA4Analysis/plotsRobert/looseMuPtEta2DEff.pkl', 'w'))

#looseMuPtEta2DEff = pickle.load(file('/Users/robertschoefbeck/CloudStation/Workspace/RA4Analysis/plotsRobert/looseMuPtEta2DEff.pkl'))
looseMuPtEta2DEff = pickle.load(file('/data/easilar/results2014/muonTemplates/CSA14_TTJets_efficiencyMap_vetoMuIDPt15_ttJetsCSA1450ns_relIso0.12.pkl'))
#prefix="njet4"

def matchCollections(coll1, coll2, matchId):
  for l1 in coll1:
    matched = False
    matchIndex = -1
    for il2, l2 in enumerate(coll2):
      if match(l1, l2): 
        matched = True
        matchIndex=il2
        break
    l1['match_'+matchId]=matched
    l1['match_'+matchId+'_index']=matchIndex
  #Find out whether two muons in coll1 match to the same object in coll2 (if so: matchingOverlap=True)
  indices = [l['match_'+matchId+'_index'] for l in coll1 if l['match_'+matchId]]
  matchingOverlap = len(indices)!=len(list(set(indices)))
  return coll1, matchingOverlap

def findClosestObject(obj, coll, returnComplement = False):
  l = sorted( [[deltaR2(obj, o), o] for o in coll] , key=lambda x:x[0])
  if len(l)>0:
    j=l[0][1]
    j['DR']=l[0][0]
    if returnComplement:
      complement = [p[1] for p in l[1:]]
      return j, complement
    else:
      return j
  if returnComplement: #protect unpacking in case of empty jet collection
    return None, None

def makeHisto(name,binning):
  return {\
  'prediction':          ROOT.TH1F(name+'_prediction','name',*binning),
  'prediction_noScaling': ROOT.TH1F(name+'_prediction_noScaling','name',*binning),
  'truth':         ROOT.TH1F(name+'_truth','name',*binning),
   'name':name
  }

h_met = makeHisto('met', [50,0,500])
h_ht  = makeHisto('ht', [50,0,2000])
h_nJet40  = makeHisto('nJet40', [10,0,10])
h_jet0pt  = makeHisto('jet0pt', [50,0,1000])
h_jet0pt_mu  = makeHisto('jet0pt_mu', [50,0,1000])

#h_lost_mcMatchAny = makeHisto('h_lost_mcMatchAny', [50,-25,25])  
#h_lost_mcMatchId  = makeHisto('h_lost_mcMatchId', [50,-25,25])
h_lost_jetDR      = makeHisto('h_lost_jetDR', [100,0,4])
h_lost_jetDR_next = makeHisto('h_lost_jetDR_next', [100,0,4])
#h_lost_jetPtRatio = makeHisto('h_lost_jetPtRatio', [50,-1,4])
#h_lost_jetBTagCSV = makeHisto('h_lost_jetBTagCSV', [50,-1,4])

h_closestJet_pt          =   makeHisto('closestJet_pt', [50,0,1000])
h_closestJet_mcFlavour   =   makeHisto('closestJet_mcFlavour', [60,-30,30])
h_closestJet_mcMatchId   =   makeHisto('closestJet_mcMatchId', [50,-25,25]) 
h_closestJet_mcMatchFlav =   makeHisto('closestJet_mcMatchFlav', [60,-30,30])


cut = "Sum$(genLep_pt>15&&abs(genLep_eta)<2.1)==2" #Consider only events with exactly two generated leptons 
c.Draw(">>eList", cut, 'goff')
eList = ROOT.gDirectory.Get('eList')
nEvents = eList.GetN()
nEvents = nEvents if not small else min(100000, nEvents)
for nev in range(nEvents):
  if nev%10000==0:
    print nev,'/',nEvents
  c.GetEntry(eList.GetEntry(nev))
  genMuonsInAcceptance    = getGenMuonsInAcceptance(c) #get gen muons
  if len(genMuonsInAcceptance)!=2:continue #redundant with selection
  looseMuonsInAcceptance  = getLooseMuonsInAcceptance(c)
  if len(looseMuonsInAcceptance)>2:continue #Don't deal with multi-leptons
  #Add gen-matching info to loose muons
  looseMuonsInAcceptance, matchingOverlap = matchCollections(looseMuonsInAcceptance, genMuonsInAcceptance, 'gen')
  if matchingOverlap:
    print "Overlap in matching for event",nev,'\n','more info: looseMuonsInAcceptance, genMuonsInAcceptance',looseMuonsInAcceptance, genMuonsInAcceptance
    continue
  #Add loose-matching info to gen muons
  genMuonsInAcceptance, matchingOverlap = matchCollections(genMuonsInAcceptance, looseMuonsInAcceptance, 'loose')
  if matchingOverlap:
    print "Overlap in matching for event",nev,'\n','more info: looseMuonsInAcceptance, genMuonsInAcceptance',looseMuonsInAcceptance, genMuonsInAcceptance
    continue

  tightMatchedMuons = filter(lambda m:tightID(m) and m['match_gen'], looseMuonsInAcceptance)
  if not len(tightMatchedMuons)>=1:continue #Require at least one tight matched muon

  ht = getVarValue(c, 'htJet40j') 
  met = getVarValue(c, 'met_pt') 
  jet0pt = getVarValue(c, 'Jet_pt', 0) 
  weight = getVarValue(c, 'weight') 
  jets = getJets(c)
  jets40 = filter(lambda j:j['pt']>40, jets)
  nJet40 = len(jets40) 
  #'Prediction'
  if len(looseMuonsInAcceptance)==2:
    for m, m2 in [looseMuonsInAcceptance, reversed(looseMuonsInAcceptance)] :
      if not tightID(m2) and m2['match_gen']:continue #Require aloways 'the other' lepton be tight and matched
      eff = looseMuPtEta2DEff.GetBinContent(looseMuPtEta2DEff.FindBin(m['pt'], m['eta']))
      S_eff = (1-eff)/eff
      nJet40Pred = nJet40+1
#      if nJet40Pred<4:continue
      varList = [\
        [met, h_met], [ht, h_ht], [jet0pt, h_jet0pt], [jet0pt+m['pt'], h_jet0pt_mu], [nJet40Pred, h_nJet40]]
#        [m['mcMatchAny'], h_lost_mcMatchAny], 
#        [m['mcMatchId'], h_lost_mcMatchId], 
#        [m['jetPtRatio'], h_lost_jetPtRatio], 
#        [m['jetBTagCSV'], h_lost_jetBTagCSV]
      closestJet = findClosestObject(m, jets)
      if closestJet:
        varList.extend([\
        [closestJet['DR'], h_lost_jetDR], 
        [closestJet['DR'], h_lost_jetDR_next], 
        [closestJet['pt'], h_closestJet_pt],
        [closestJet['mcFlavour'], h_closestJet_mcFlavour],
        [closestJet['mcMatchId'], h_closestJet_mcMatchId],
        [closestJet['mcMatchFlav'], h_closestJet_mcMatchFlav],
          ])
      for var, h_var in varList:
        h_var['prediction'].Fill(var, weight*S_eff) 
        h_var['prediction_noScaling'].Fill(var, weight)

  #'Truth'
  if len(looseMuonsInAcceptance)==1:
    m=looseMuonsInAcceptance[0]
    assert tightID(m) and m['match_gen'],"Should never happen by construction!"
    lostGenLep = genMuonsInAcceptance[1-m['match_gen_index']]#This works because len(genMuonsInAcceptance)==2
#    if nJet40<4:continue
    varList = [\
      [met, h_met], [ht, h_ht], [jet0pt, h_jet0pt], [jet0pt, h_jet0pt_mu], [nJet40, h_nJet40]]
    if len(jets)>0:
      closestJet, complement = findClosestObject(lostGenLep, jets, returnComplement = True)
      if closestJet:
        varList.extend([\
        [closestJet['DR'], h_lost_jetDR], 
        [closestJet['pt'], h_closestJet_pt],
        [closestJet['mcFlavour'], h_closestJet_mcFlavour],
        [closestJet['mcMatchId'], h_closestJet_mcMatchId],
        [closestJet['mcMatchFlav'], h_closestJet_mcMatchFlav],
          ])
      secondClosestJet = findClosestObject(lostGenLep, complement, returnComplement = False)
      if secondClosestJet:
        varList.append([secondClosestJet['DR'], h_lost_jetDR_next])
    for var, h_var in varList:
      h_var['truth'].Fill(var, weight) 

c1 = ROOT.TCanvas()
ROOT.gStyle.SetOptStat(0)
         
for h in [h_met, h_ht, h_jet0pt,h_jet0pt_mu,\
          h_nJet40, h_lost_jetDR,h_lost_jetDR_next, 
          h_closestJet_pt,h_closestJet_mcFlavour,h_closestJet_mcMatchId,h_closestJet_mcMatchFlav]:
  h['prediction_noScaling'].SetLineColor(ROOT.kBlue)
  h['prediction_noScaling'].Draw()
  h['prediction'].SetLineColor(ROOT.kRed)
  h['prediction'].Draw('same')
  c1.SetLogy()
  h['prediction'].GetXaxis().SetTitle(h['name'])
  h['truth'].SetLineColor(ROOT.kBlack)
  h['truth'].Draw('same')
#  c1.Print('~/Desktop/plots/'+h['name']+'.png')
  c1.Print('/afs/hephy.at/user/e/easilar/www/pngCSA14/ClosureTest/RelIso0_12/'+h['name']+'.png')
