from Workspace.HEPHYPythonTools.helpers import getVarValue

gTauAbsEtaBins = [(0,0.5), (0.5,1),(1,1.5),(1.5,2.3)]
gTauPtBins = [(10,20), (20,30), (30,40), (40, 80), (80, 160), (160, 320), (320,-1)]
metParRatioBins = [x/10. for x in range(0,11)]
jetRatioBins = [0,0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.5,2.0,3.0]

def getLooseEleStage1(c, iele): # POG Ele veto https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaCutBasedIdentification
  eta = getVarValue(c, 'elesEta', iele)
  pdg = getVarValue(c, 'elesPdg', iele)
  sietaieta = getVarValue(c, 'elesSigmaIEtaIEta', iele)
  dphi = getVarValue(c, 'elesDPhi', iele)
  deta = getVarValue(c, 'elesDEta', iele)
  HoE  = getVarValue(c, 'elesHoE', iele)
  isEB = abs(eta) < 1.479
  isEE = abs(eta) > 1.479 and abs(eta) < 2.5
  relIso = getVarValue(c, 'elesPfRelIso', iele)
  pt = getVarValue(c, 'elesPt', iele)
  dxy = getVarValue(c, 'elesDxy', iele)
  dz = getVarValue(c, 'elesDz', iele)
  oneOverEMinusOneOverP = getVarValue(c, 'elesOneOverEMinusOneOverP', iele)
  convRej = getVarValue(c, 'elesPassPATConversionveto', iele)
  missingHits = getVarValue(c, 'elesMissingHits', iele)
  if ( isEE or isEB)\
    and ((isEB and dphi < 0.8) or (isEE and dphi < 0.7)) and ( (isEB and deta < 0.007) or (isEE and deta < 0.01) )\
    and ((isEB and sietaieta < 0.01 ) or (isEE and sietaieta < 0.03))\
    and ( isEB and HoE < 0.15 )\
    and abs(dxy) < 0.04 and abs(dz) < 0.2 \
    and ( relIso < 0.15 ) \
    and pt>10.:
    return {'pt':pt, 'phi':getVarValue(c, 'elesPhi', iele), 'Pdg':pdg, 'eta':eta, 'sIEtaIEta':sietaieta, 'DPhi':dphi, \
            'DEta':deta, 'HoE':HoE, 'OneOverEMinusOneOverP':oneOverEMinusOneOverP, 'ConvRejection':convRej, 'MissingHits':missingHits,\
            'isEB':isEB, 'isEE':isEE, 'relIso':relIso, 'Dxy':dxy, 'Dz':dz}

def getAllElectronsStage1(c, neles ):
  res=[]
  for i in range(0, int(neles)):
    cand =  getLooseEleStage1(c, i)
    if cand:
      res.append(cand)
  res = sorted(res, key=lambda k: -k['pt'])
  return res


def tightPOGEleID(ele):
  return ele['pt']>20 and abs(ele['eta'])<2.5 and ele['relIso']<0.15 and ele['ConvRejection'] and ele['MissingHits']<=1 and abs(ele['Dxy'])<0.02  and ele['OneOverEMinusOneOverP']<0.05\
    and abs(ele['Dz'])<0.1 and (\
    (ele['isEB'] and ele['DPhi']<0.06 and ele['DEta']<0.004 and ele['sIEtaIEta']<0.01 and ele['HoE']<0.12) or
    (ele['isEE'] and ele['DPhi']<0.03 and ele['DEta']<0.007 and ele['sIEtaIEta']<0.03)and ele['HoE']<0.10)

def vetoEleID(ele):
  return ele['pt']>15 and ele['relIso']<0.15 and  abs(ele['Dxy'])<0.04\
    and abs(ele['Dz'])<0.2 and (\
    (ele['isEB'] and ele['DPhi']<0.8 and ele['DEta']<0.007 and ele['sIEtaIEta']<0.01 and ele['HoE']<0.125) or
    (ele['isEE'] and ele['DPhi']<0.7 and ele['DEta']<0.01 and ele['sIEtaIEta']<0.03 ))

def getLooseMuStage1(c, imu ):
  isPF = getVarValue(c, 'muonsisPF', imu)
  isGlobal = getVarValue(c, 'muonsisGlobal', imu)
  isTracker = getVarValue(c, 'muonsisTracker', imu)
  pt = getVarValue(c, 'muonsPt', imu)
  dz = getVarValue(c, 'muonsDz', imu)
  eta=getVarValue(c, 'muonsEta', imu)
  if isPF and (isGlobal or isTracker) and pt>5. and abs(eta)<2.5 and abs(dz)<0.5:
    return {'pt':pt, 'phi':getVarValue(c, 'muonsPhi', imu), 'eta':eta, 'IsGlobal':isGlobal, 'IsTracker':isTracker, 'IsPF':isPF, 'relIso':getVarValue(c, 'muonsPFRelIso', imu), 'Dz':dz}


def tightPOGMuID(mu):
  return mu['IsGlobal'] and mu['IsPF'] and mu['pt']>20 and abs(mu['eta'])<2.1 and mu['relIso']<0.12 and mu['NormChi2']<=10 and mu['NValMuonHits']>0\
     and mu['NumMatchedStations']>1 and mu['PixelHits']>0 and mu['NumtrackerLayerWithMeasurement']>5 and abs(mu['Dxy'])<0.02 and abs(mu['Dz'])<0.5

def vetoMuID(mu):
  return (mu['IsTracker'] or mu['IsGlobal']) and mu['IsPF'] and mu['pt']>15 and abs(mu['eta'])<2.5 and mu['relIso']<0.2  and abs(mu['Dxy'])<0.2 and abs(mu['Dz'])<0.5


def getAllMuonsStage1(c, nmuons ):
  res=[]
  for i in range(0, int(nmuons)):
    cand = getLooseMuStage1(c, i)
    if cand:
      for v in ['Pdg', 'Dxy', 'NormChi2', 'NValMuonHits', 'NumMatchedStations', 'PixelHits', 'NumtrackerLayerWithMeasurement']:
        cand[v] = getVarValue(c, 'muons'+v, i)
      res.append(cand)
  res = sorted(res, key=lambda k: -k['pt'])
  return res


def getTauStage1(c, itau ):
#  print getVarValue(c, 'tausisPF', itau),          getVarValue(c, 'tausDecayModeFinding', itau),          getVarValue(c, 'tausAgainstMuonLoose', itau),          getVarValue(c, 'tausAgainstElectronLoose', itau),          getVarValue(c, '

#  return getVarValue(c, 'tausisPF', itau) and \
  return getVarValue(c, 'tausDecayModeFinding', itau) and \
         getVarValue(c, 'tausAgainstMuonLoose3', itau) and \
         getVarValue(c, 'tausAgainstElectronLooseMVA5', itau) and \
         getVarValue(c, 'tausByLooseCombinedIsolationDeltaBetaCorr3Hits', itau) and \
         getVarValue(c, 'tausPt', itau)>20. and \
         abs(getVarValue(c, 'tausEta', itau))<2.3

def getAllTausStage1(c, ntaus ):
  res=[]
  for i in range(0, int(ntaus)):
    if getTauStage1(c, i):
      res.append({'pt':getVarValue(c, 'tausPt', i),'eta':getVarValue(c, 'tausEta', i), 'phi':getVarValue(c, 'tausPhi', i),\
      'Pdg':getVarValue(c, 'tausPdg', i)})
  res = sorted(res, key=lambda k: -k['pt'])
  return res

