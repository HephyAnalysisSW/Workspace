import ROOT
from Workspace.HEPHYPythonTools.helpers import getVarValue, findClosestObject, deltaPhi, deltaR, deltaR2, getObjDict
from math import cos, sin, sqrt, acos, pi, atan2, cosh

def stage2MT(c):
  if c=="branches":return ['met_pt','leptonPt','met_phi','leptonPhi']
  met=c.GetLeaf('met').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  metphi=c.GetLeaf('met_phi').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  leptonPhi=c.GetLeaf('leptonPhi').GetValue()
  return sqrt(2.*leptonPt*met*(1.-cos(leptonPhi-metphi)))
def stage2DPhi(c):
  if c=="branches":return ['met_pt','met_phi','leptonPt','leptonPhi']
  met=c.GetLeaf('met').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  metphi=c.GetLeaf('met_phi').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  leptonPhi=c.GetLeaf('leptonPhi').GetValue()
  cdp  = cos(leptonPhi-metphi)
  return acos((leptonPt+met*cdp)/sqrt(leptonPt**2+met**2+2*met*leptonPt*cdp)) 

def cmgMT(c):
  if c=="branches":return ['met_pt','met_phi','leptonPt']
  met=c.GetLeaf('met_pt').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  metphi=c.GetLeaf('met_phi').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  leptonPhi=c.GetLeaf('leptonPhi').GetValue()
  return sqrt(2.*leptonPt*met*(1.-cos(leptonPhi-metphi)))
def cmgDPhi(c):
  if c=="branches":return ['met_pt','met_phi','leptonPt','leptonPhi']
  met=c.GetLeaf('met_pt').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  metphi=c.GetLeaf('met_phi').GetValue()
  leptonPhi=c.GetLeaf('leptonPhi').GetValue()
  cdp  = cos(leptonPhi-metphi)
  return acos((leptonPt+met*cdp)/sqrt(leptonPt**2+met**2+2*met*leptonPt*cdp)) 
def cmgST(c):
  if c=="branches":return ['leptonPt','met_phi']
  met=c.GetLeaf('met_pt').GetValue()
  leptonPt=c.GetLeaf('leptonPt').GetValue()
  return  met+leptonPt 

def cmgGetJets(c, ptMin=40., etaMax=999.):
  addJetVars =  ['phi', 'mcFlavour', 'mcMatchId', 'mcMatchFlav', 'btagCSV']
  if c=="branches":return ['nJet','Jet_pt','Jet_eta'] + ['Jet_'+x for x in addJetVars]
  nJet = int(getVarValue(c, 'nJet'))
  jets=[]
  for i in range(nJet):
    jet = getObjDict(c, 'Jet', ['pt','eta'], i)
    if jet['pt']>ptMin and abs(jet['eta']<etaMax):
      jet.update(getObjDict(c, 'Jet', addJetVars, i))
      jets.append(jet)
  return jets

def cmgMTClosestJetMET(c):
  if c=="branches":return cmgGetJets("branches")+['met_pt', 'met_phi'] 
  jets = cmgGetJets(c,  ptMin=40., etaMax=999.)
  met = {'pt':c.GetLeaf('met_pt').GetValue(), 'phi':c.GetLeaf('met_phi').GetValue()}
  closestJet = findClosestObject(jets, met, sortFunc=lambda o1, o2: deltaPhi(o1['phi'], o2['phi']))['obj']
  return sqrt(2.*met['pt']*closestJet['pt']*(1-cos(met['phi']-closestJet['phi'])))
def cmgMTClosestBJetMET(c):
  if c=="branches":return cmgGetJets("branches")+['met_pt', 'met_phi'] 
  bjets = filter(lambda j:j['btagCSV']>0.679, cmgGetJets(c,  ptMin=40., etaMax=999.))
  met = {'pt':c.GetLeaf('met_pt').GetValue(), 'phi':c.GetLeaf('met_phi').GetValue()}
  if len(bjets)>0:
    closestBJet = findClosestObject(bjets, met, sortFunc=lambda o1, o2: deltaPhi(o1['phi'], o2['phi']))['obj']
    return sqrt(2.*met['pt']*closestBJet['pt']*(1-cos(met['phi']-closestBJet['phi'])))
  else:
   return float('nan')
def cmgMinDPhiJet(c, nJets=3):
  if c=="branches":return cmgGetJets("branches")+['met_phi'] 
  leadingNJets = cmgGetJets(c,  ptMin=40., etaMax=999.)[:nJets]
  met = {'phi':c.GetLeaf('met_phi').GetValue()}
  closestJet = findClosestObject(leadingNJets, met, sortFunc=lambda o1,o2: deltaPhi(o1['phi'], o2['phi']))
  return closestJet['distance'] 
def cmgMinDPhiBJet(c):
  if c=="branches":return cmgGetJets("branches")+['met_phi'] 
  bjets = filter(lambda j:j['btagCSV']>0.679, cmgGetJets(c,  ptMin=40., etaMax=999.))
  met = {'phi':c.GetLeaf('met_phi').GetValue()}
  if len(bjets)>0:
    closestJet = findClosestObject(bjets, met, sortFunc=lambda o1,o2: deltaPhi(o1['phi'], o2['phi']))
    return closestJet['distance'] 
  else:
   return float('nan')

def cmgMTTopClosestJetMET(c):
  if c=="branches":return cmgGetJets("branches")+['met_phi','met_pt','leptonPt','leptonPhi','leptonEta'] 
  jets = cmgGetJets(c,  ptMin=40., etaMax=999.)
  met = {'pt':c.GetLeaf('met_pt').GetValue(), 'phi':c.GetLeaf('met_phi').GetValue()}
  lepton = {'pt':c.GetLeaf('leptonPt').GetValue(), 'phi':c.GetLeaf('leptonPhi').GetValue(), 'eta':c.GetLeaf('leptonEta').GetValue()}
  W = {'phi':atan2(met['pt']*sin(met['phi']) + lepton['pt']*sin(lepton['phi']), met['pt']*cos(met['phi']) + lepton['pt']*cos(lepton['phi']) )}
  closestJet = findClosestObject(jets, W, sortFunc=lambda o1,o2: deltaPhi(o1['phi'], o2['phi']))['obj']
  return sqrt(\
    2.*met['pt']*closestJet['pt']*(1-cos(met['phi']-closestJet['phi'])) +\
    2.*met['pt']*lepton['pt']*(1-cos(met['phi']-lepton['phi'])) + \
    2.*lepton['pt']*closestJet['pt']*(cosh(lepton['eta'] - closestJet['eta'])-cos(lepton['phi']-closestJet['phi']))\
    )
def cmgMTTopClosestBJetMET(c):
  if c=="branches":return cmgGetJets("branches")+['met_phi','met_pt','leptonPt','leptonPhi','leptonEta'] 
  bjets = filter(lambda j:j['btagCSV']>0.679, cmgGetJets(c,  ptMin=40., etaMax=999.))
  if len(bjets)>0:
    met = {'pt':c.GetLeaf('met_pt').GetValue(), 'phi':c.GetLeaf('met_phi').GetValue()}
    lepton = {'pt':c.GetLeaf('leptonPt').GetValue(), 'phi':c.GetLeaf('leptonPhi').GetValue(), 'eta':c.GetLeaf('leptonEta').GetValue()}
    W = {'phi':atan2(met['pt']*sin(met['phi']) + lepton['pt']*sin(lepton['phi']), met['pt']*cos(met['phi']) + lepton['pt']*cos(lepton['phi']) )}
    closestBJet = findClosestObject(bjets, W, sortFunc=lambda o1,o2: deltaPhi(o1['phi'], o2['phi']))['obj']
    return sqrt(\
      2.*met['pt']*closestBJet['pt']*(1-cos(met['phi']-closestBJet['phi'])) +\
      2.*met['pt']*lepton['pt']*(1-cos(met['phi']-lepton['phi'])) + \
      2.*lepton['pt']*closestBJet['pt']*(cosh(lepton['eta'] - closestBJet['eta'])-cos(lepton['phi']-closestBJet['phi']))\
      )
  else:
    return float('nan')

def nJetBinName(njb):
  n=str(list(njb)[0])+"#leq n_{jet}"
  if len(njb)>1 and njb[1]>-1:
    n+='#leq '+str(njb[1])
  return n
def nBTagBinName(btb):
  n=str(list(btb)[0])+"#leq n_{b-tag}"
  if len(btb)>1 and btb[1]>-1:
    n+='#leq '+str(btb[1])
  return n
def varBinName(vb, var):
  n=str(list(vb)[0])+"< "+var
  if len(vb)>1 and vb[1]>0:
    n+='< '+str(vb[1])
  return n
  

def nameAndCut(stb, htb, njetb, btb=None, presel="(1)", charge="", btagVar = 'nBJetMedium40'):
  cut=presel
  name=""
  if stb:
    cut+='&&st>='+str(stb[0])
    name+='st'+str(stb[0])
    if stb[1]>0:
      cut+='&&st<'+str(stb[1])
      name+='-'+str(stb[1])
  if htb:
    cut+='&&htJet40ja>='+str(htb[0])
    name+='_ht'+str(htb[0])
    if htb[1]>0:
      cut+='&&htJet40ja<'+str(htb[1])
      name+='-'+str(htb[1])
  if njetb:
    cut+='&&nJet40a>='+str(njetb[0])
    name+='_njet'+str(njetb[0])
    if len(njetb)>1 and njetb[1]>=0:
      cut+='&&nJet40a<='+str(njetb[1])
      name+='-'+str(njetb[1])
  if btb:
    cut+='&&'+btagVar+'>='+str(btb[0])
    name+='_nbtag'+str(btb[0])
    if len(btb)>1 and btb[1]>=0:
      cut+='&&'+btagVar+'<='+str(btb[1])
      name+='-'+str(btb[1])
  if charge.lower()=='pos':
    cut+='&&leptonPdg<0'
    name+='_posCharge'
  if charge.lower()=='neg':
    cut+='&&leptonPdg>0'
    name+='_negCharge'
  if name.startswith('_'):name=name[1:]
  return [name, cut]


#def wRecoPt(chain):
#  lPt = getVarValue(chain, "leptonPt")
#  lPhi = getVarValue(chain, "leptonPhi")
#  metphi = getVarValue(chain, "type1phiMetphi")
#  met = getVarValue(chain, "type1phiMet")
#  cosLepPhi = cos(lPhi)
#  sinLepPhi = sin(lPhi)
#  mpx = met*cos(metphi)
#  mpy = met*sin(metphi)
#  return sqrt((lPt*cosLepPhi + mpx)**2 + (lPt*sinLepPhi + mpy)**2)
#
#def wGenPt(c):
#  res=[]
#  for i in range(c.ngp):
#    if abs(c.gpPdg[i])==24:
#      res.append([c.gpM[i], c.gpPt[i]])
#  res.sort() 
#  if len(res)>0:
#    return res[0][1]
#  else:
#    return float('nan') 


