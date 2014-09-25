from Workspace.HEPHYPythonTools.helpers import getVarValue, deltaR

gTauAbsEtaBins = [(0,0.5), (0.5,1),(1,1.5),(1.5,2.3)]
gTauPtBins = [(10,20), (20,30), (30,40), (40, 80), (80, 160), (160, 320), (320,-1)]
metParRatioBins = [x/10. for x in range(0,11)]
jetRatioBins = [0,0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.5,2.0,3.0]

#def getLooseEleStage1(c, iele): # POG Ele veto https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaCutBasedIdentification
#  eta = getVarValue(c, 'elesEta', iele)
#  pdg = getVarValue(c, 'elesPdg', iele)
#  sietaieta = getVarValue(c, 'elesSigmaIEtaIEta', iele)
#  dphi = getVarValue(c, 'elesDPhi', iele)
#  deta = getVarValue(c, 'elesDEta', iele)
#  HoE  = getVarValue(c, 'elesHoE', iele)
#  isEB = abs(eta) < 1.479
#  isEE = abs(eta) > 1.479 and abs(eta) < 2.5
#  relIso = getVarValue(c, 'elesPfRelIso', iele)
#  pt = getVarValue(c, 'elesPt', iele)
#  dxy = getVarValue(c, 'elesDxy', iele)
#  dz = getVarValue(c, 'elesDz', iele)
#  oneOverEMinusOneOverP = getVarValue(c, 'elesOneOverEMinusOneOverP', iele)
#  convRej = getVarValue(c, 'elesPassPATConversionveto', iele)
#  missingHits = getVarValue(c, 'elesMissingHits', iele)
#  if ( isEE or isEB)\
#    and ((isEB and dphi < 0.8) or (isEE and dphi < 0.7)) and ( (isEB and deta < 0.007) or (isEE and deta < 0.01) )\
#    and ((isEB and sietaieta < 0.01 ) or (isEE and sietaieta < 0.03))\
#    and ( isEB and HoE < 0.15 )\
#    and abs(dxy) < 0.04 and abs(dz) < 0.2 \
#    and ( relIso < 0.15 ) \
#    and pt>10.:
#    return {'pt':pt, 'phi':getVarValue(c, 'elesPhi', iele), 'Pdg':pdg, 'eta':eta, 'sIEtaIEta':sietaieta, 'DPhi':dphi, \
#            'DEta':deta, 'HoE':HoE, 'OneOverEMinusOneOverP':oneOverEMinusOneOverP, 'ConvRejection':convRej, 'MissingHits':missingHits,\
#            'isEB':isEB, 'isEE':isEE, 'relIso':relIso, 'Dxy':dxy, 'Dz':dz}
def getLooseEleStage1(s, iele): # POG Ele veto https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaCutBasedIdentification
  eta = s.elesEta[iele]#getVarValue(c, 'elesEta', iele)
  pdg = s.elesPdg[iele]#getVarValue(c, 'elesPdg', iele)
  sietaieta = s.elesSigmaIEtaIEta[iele]#getVarValue(c, 'elesSigmaIEtaIEta', iele)
  dphi = s.elesDPhi[iele]
  deta = s.elesDEta[iele]
  HoE  = s.elesHoE[iele]
  isEB = abs(eta) < 1.479
  isEE = abs(eta) > 1.479 and abs(eta) < 2.5
  relIso = s.elesPfRelIso[iele]
  pt =  s.elesPt[iele]
  dxy = s.elesDxy[iele]
  dz =  s.elesDz[iele]
  oneOverEMinusOneOverP = s.elesOneOverEMinusOneOverP[iele]
  convRej               = s.elesPassPATConversionVeto[iele]
  missingHits           = s.elesMissingHits[iele]
  if ( isEE or isEB)\
    and ((isEB and dphi < 0.8) or (isEE and dphi < 0.7)) and ( (isEB and deta < 0.007) or (isEE and deta < 0.01) )\
    and ((isEB and sietaieta < 0.01 ) or (isEE and sietaieta < 0.03))\
    and ( isEB and HoE < 0.15 )\
    and abs(dxy) < 0.04 and abs(dz) < 0.2 \
    and ( relIso < 0.15 ) \
    and pt>10.:
    return {'pt':pt, 'phi':s.elesPhi[iele], 'Pdg':pdg, 'eta':eta, 'sIEtaIEta':sietaieta, 'DPhi':dphi, \
            'DEta':deta, 'HoE':HoE, 'OneOverEMinusOneOverP':oneOverEMinusOneOverP, 'ConvRejection':convRej, 'MissingHits':missingHits,\
            'isEB':isEB, 'isEE':isEE, 'relIso':relIso, 'Dxy':dxy, 'Dz':dz}

def getAllElectronsStage1(s, neles ):
  res=[]
  for i in range(0, int(neles)):
    cand =  getLooseEleStage1(s, i)
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

#def getLooseMuStage1(c, imu ):
#  isPF = getVarValue(c, 'muonsisPF', imu)
#  isGlobal = getVarValue(c, 'muonsisGlobal', imu)
#  isTracker = getVarValue(c, 'muonsisTracker', imu)
#  pt = getVarValue(c, 'muonsPt', imu)
#  dz = getVarValue(c, 'muonsDz', imu)
#  eta=getVarValue(c, 'muonsEta', imu)
#  if isPF and (isGlobal or isTracker) and pt>5. and abs(eta)<2.5 and abs(dz)<0.5:
#    return {'pt':pt, 'phi':getVarValue(c, 'muonsPhi', imu), 'eta':eta, 'IsGlobal':isGlobal, 'IsTracker':isTracker, 'IsPF':isPF, 'relIso':getVarValue(c, 'muonsPFRelIso', imu), 'Dz':dz}
def getLooseMuStage1(s, imu ):
  isPF = s.muonsisPF[imu]
  isGlobal = s.muonsisGlobal[imu]
  isTracker = s.muonsisTracker[imu]
  pt = s.muonsPt[imu]
  dz = s.muonsDz[imu]
  eta =s.muonsEta[imu]
  if isPF and (isGlobal or isTracker) and pt>5. and abs(eta)<2.5 and abs(dz)<0.5:
    return {'pt':pt, 'phi':s.muonsPhi[imu], 'eta':eta, 'IsGlobal':isGlobal, 'IsTracker':isTracker, 'IsPF':isPF, 'relIso':s.muonsPFRelIso[imu], 'Dz':dz}

def getAllMuonsStage1(s, nmuons ):
  res=[]
  for i in range(0, int(nmuons)):
    cand = getLooseMuStage1(s, i)
    if cand:
      cand["Pdg"]                            = s.muonsPdg[i]
      cand["Dxy"]                            = s.muonsDxy[i]
      cand["NormChi2"]                       = s.muonsNormChi2[i]
      cand["NValMuonHits"]                   = s.muonsNValMuonHits[i]
      cand["NumMatchedStations"]             = s.muonsNumMatchedStations[i]
      cand["PixelHits"]                      = s.muonsPixelHits[i]
      cand["NumtrackerLayerWithMeasurement"] = s.muonsNumtrackerLayerWithMeasurement[i]
      cand["Iso03sumChargedHadronPt"]        = s.muonsIso03sumChargedHadronPt[i]
      cand["Iso03sumNeutralHadronEt"]        = s.muonsIso03sumNeutralHadronEt[i]
      cand["Iso03sumPhotonEt"]               = s.muonsIso03sumPhotonEt[i]
      cand["Iso03sumPUChargedHadronPt"]      = s.muonsIso03sumPUChargedHadronPt[i]
      res.append(cand)
  res = sorted(res, key=lambda k: -k['pt'])
  return res

def getLooseMuStage2(c, imu ):
  isPF = True #FIXME->Should be added @stage1 anyways 
  isGlobal = getVarValue(c, 'muIsGlobal', imu)
  isTracker = getVarValue(c, 'muIsTracker', imu)
  pt = getVarValue(c, 'muPt', imu)
  dz = getVarValue(c, 'muDz', imu)
  eta=getVarValue(c, 'muEta', imu)
  cand={'pt':pt, 'phi':getVarValue(c, 'muPhi', imu), 'eta':eta, 'IsGlobal':isGlobal, 'IsTracker':isTracker, 'IsPF':isPF, 'relIso':getVarValue(c, 'muRelIso', imu), 'Dz':dz}
  for v in ['Pdg', 'Dxy', 'NormChi2', 'NValMuonHits', 'NumMatchedStations', 'PixelHits', 'NumtrackerLayerWithMeasurement']:
    cand[v] = getVarValue(c, 'mu'+v, imu)
  if isPF and (isGlobal or isTracker) and pt>5. and abs(eta)<2.5 and abs(dz)<0.5:
    return cand 

def tightPOGMuID(mu):
  return mu['IsGlobal'] and mu['IsPF'] and mu['pt']>20 and abs(mu['eta'])<2.1 and mu['relIso']<0.12 and mu['NormChi2']<=10 and mu['NValMuonHits']>0\
     and mu['NumMatchedStations']>1 and mu['PixelHits']>0 and mu['NumtrackerLayerWithMeasurement']>5 and abs(mu['Dxy'])<0.02 and abs(mu['Dz'])<0.5

def vetoMuID(mu, relIso=0.2):
  return (mu['IsTracker'] or mu['IsGlobal']) and mu['IsPF'] and mu['pt']>15 and abs(mu['eta'])<2.5 and mu['relIso']<relIso  and abs(mu['Dxy'])<0.2 and abs(mu['Dz'])<0.5


def hybridIso(m, wp):
  if wp=='loose':
    return  (m['pt']<25 and m['relIso']*m['pt']<10) or (m['pt']>=25 and m['relIso']<0.4)
  if wp=='medium':
    return  (m['pt']<25 and m['relIso']*m['pt']<5) or (m['pt']>=25 and m['relIso']<0.2)
  if wp=='tight':
    return  (m['pt']<25 and m['relIso']*m['pt']<3) or (m['pt']>=25 and m['relIso']<0.12)

def hybridMuID(mu, wp):
  return (mu['IsTracker'] or mu['IsGlobal']) and mu['IsPF'] and mu['pt']>10 and abs(mu['eta'])<2.5 and hybridIso(mu, wp)  and abs(mu['Dxy'])<0.2 and abs(mu['Dz'])<0.5

#def getTauStage1(c, itau ):
#  return getVarValue(c, 'tausDecayModeFinding', itau) and \
#         getVarValue(c, 'tausAgainstMuonLoose3', itau) and \
#         getVarValue(c, 'tausAgainstElectronLooseMVA5', itau) and \
#         getVarValue(c, 'tausByLooseCombinedIsolationDeltaBetaCorr3Hits', itau) and \
#         getVarValue(c, 'tausPt', itau)>20. and \
#         abs(getVarValue(c, 'tausEta', itau))<2.3
def getTauStage1(s, itau ):
  return s.tausDecayModeFinding[itau] and \
         s.tausAgainstMuonLoose3[itau] and \
         s.tausAgainstElectronLooseMVA5[itau] and \
         s.tausByLooseCombinedIsolationDeltaBetaCorr3Hits[itau] and \
         s.tausPt[itau]>20. and \
         abs(s.tausEta[itau])<2.3

def getAllTausStage1(s, ntaus ):
  res=[]
  for i in range(0, int(ntaus)):
    if getTauStage1(s, i):
      res.append({'pt':s.tausPt[i],'eta':s.tausEta[i], 'phi':s.tausPhi[i],\
      'Pdg':s.tausPdg[i]})
  res = sorted(res, key=lambda k: -k['pt'])
  return res

def splitListOfObjects(var, val, s):
  resLow = []
  resHigh = []
  for x in s:
    if x[var]<val:
      resLow.append(x)
    else:
      resHigh.append(x)
  return resLow, resHigh

def isIsolated(obj, objs, dR=0.4):
  if dR<0:return True
  isolated=True
  for o in objs:   #Jet cross-cleaning
    if deltaR(o, obj) < dR:
      isolated = False
      break
  return isolated

#def getGoodJetsStage1(c, crosscleanobjects, dR=0.4):#, jermode=options.jermode, jesmode=options.jesmode):
#  njets = getVarValue(c, 'nJets')   # jet.pt() > 10.
#  res = []
#  bres = []
#  ht = 0.
#  met_dx=0
#  met_dy=0.
#  for i in range(int(njets)):
#    eta = getVarValue(c, 'jetsEta', i)
#    pt  = getVarValue(c, 'jetsPt', i)
#    unc = getVarValue(c, 'jetsUnc', i)
#    id =  getVarValue(c, 'jetsID', i)
#    phi = getVarValue(c, 'jetsPhi', i)
###      if max([jet['muef'],jet['elef']]) > 0.6 : print jet
##    if jermode.lower()!="none":
##      c_jet = jerDifferenceScaleFactor(eta, jermode)
##      sigmaMCRel = jerSigmaMCRel(pt, eta)
##      sigma = sqrt(c_jet**2 - 1)*sigmaMCRel
##      scale = random.gauss(1,sigma)
##      met_dx+=(1-scale)*cos(phi)*pt
##      met_dy+=(1-scale)*sin(phi)*pt
##      pt*=scale
##    if jesmode.lower()!="none":
##      scale = 1. + sign*unc
##      met_dx+=(1-scale)*cos(phi)*pt
##      met_dy+=(1-scale)*sin(phi)*pt
##      pt*=scale
#    if pt>30 and abs(eta)<4.5:
#      parton = int(abs(getVarValue(c, 'jetsParton', i)))
#      jet = {'pt':pt, 'eta':eta,'phi':phi, 'pdg':parton,\
#      'id':id,
#      'chef':getVarValue(c, 'jetsChargedHadronEnergyFraction', i), 'nhef':getVarValue(c, 'jetsNeutralHadronEnergyFraction', i),\
#      'ceef':getVarValue(c, 'jetsChargedEmEnergyFraction', i), 'neef':getVarValue(c, 'jetsNeutralEmEnergyFraction', i), 'id':id,\
#      'hfhef':getVarValue(c, 'jetsHFHadronEnergyFraction', i), 'hfeef':getVarValue(c, 'jetsHFEMEnergyFraction', i),\
#      'muef':getVarValue(c, 'jetsMuonEnergyFraction', i), 'elef':getVarValue(c, 'jetsElectronEnergyFraction', i), 'phef':getVarValue(c, 'jetsPhotonEnergyFraction', i),\
##      'jetCutBasedPUJetIDFlag':getVarValue(c, 'jetsCutBasedPUJetIDFlag', i),'jetMET53XPUJetIDFlag':getVarValue(c, 'jetsMET53XPUJetIDFlag', i),'jetFull53XPUJetIDFlag':getVarValue(c, 'jetsFull53XPUJetIDFlag', i), 
#      'btag': getVarValue(c, 'jetsBTag', i), 'unc': unc
#      }
##      isolated = True
##      for obj in crosscleanobjects:   #Jet cross-cleaning
##        if deltaR(jet, obj) < 0.3:# and  obj['relIso']< relIsoCleaningRequ: #(obj['pt']/jet['pt']) > 0.4:  
##          isolated = False
###          print "Cleaned", 'deltaR', deltaR(jet, obj), 'maxfrac', max([jet['muef'],jet['elef']]), 'pt:jet/obj', jet['pt'], obj['pt'], "relIso",  obj['relIso'], 'btag',getVarValue(c, 'jetsBtag', i), "parton", parton
##  #          print 'Not this one!', jet, obj, deltaR(jet, obj)
##          break
#      jet['isolated'] = isIsolated(jet, crosscleanobjects, dR=dR)
#      res.append(jet)
#  res  = sorted(res,  key=lambda k: -k['pt'])
#  return {'jets':res,'met_dx':met_dx, 'met_dy':met_dy}
def getGoodJetsStage1(s, crosscleanobjects, dR=0.4):#, jermode=options.jermode, jesmode=options.jesmode):
  res = []
  bres = []
  ht = 0.
  met_dx=0
  met_dy=0.
  for i in range(s.nJets):
    eta = s.jetsEta[i]
    pt  = s.jetsPt[i]
    unc = s.jetsUnc[i]
    id =  s.jetsID[i]
    phi = s.jetsPhi[i]
##      if max([jet['muef'],jet['elef']]) > 0.6 : print jet
#    if jermode.lower()!="none":
#      c_jet = jerDifferenceScaleFactor(eta, jermode)
#      sigmaMCRel = jerSigmaMCRel(pt, eta)
#      sigma = sqrt(c_jet**2 - 1)*sigmaMCRel
#      scale = random.gauss(1,sigma)
#      met_dx+=(1-scale)*cos(phi)*pt
#      met_dy+=(1-scale)*sin(phi)*pt
#      pt*=scale
#    if jesmode.lower()!="none":
#      scale = 1. + sign*unc
#      met_dx+=(1-scale)*cos(phi)*pt
#      met_dy+=(1-scale)*sin(phi)*pt
#      pt*=scale
    if pt>30 and abs(eta)<4.5:
      parton = s.jetsParton[i]
      jet = {'pt':pt, 'eta':eta,'phi':phi, 'pdg':parton,\
      'id':id,
      'chef':s.jetsChargedHadronEnergyFraction[i], 'nhef':s.jetsNeutralHadronEnergyFraction[i],\
      'ceef':s.jetsChargedEmEnergyFraction[i], 'neef':s.jetsNeutralEmEnergyFraction[i], 'id':id,\
      'hfhef':s.jetsHFHadronEnergyFraction[i], 'hfeef':s.jetsHFEMEnergyFraction[i],\
      'muef':s.jetsMuonEnergyFraction[i], 'elef':s.jetsElectronEnergyFraction[i], 'phef':s.jetsPhotonEnergyFraction[i],\
#      'jetCutBasedPUJetIDFlag':s.jetsCutBasedPUJetIDFlag[i],'jetMET53XPUJetIDFlag':getVarValue(c, 'jetsMET53XPUJetIDFlag', i),'jetFull53XPUJetIDFlag':getVarValue(c, 'jetsFull53XPUJetIDFlag', i), 
      'btag': s.jetsBTag[i], 'unc': unc
      }
#      isolated = True
#      for obj in crosscleanobjects:   #Jet cross-cleaning
#        if deltaR(jet, obj) < 0.3:# and  obj['relIso']< relIsoCleaningRequ: #(obj['pt']/jet['pt']) > 0.4:  
#          isolated = False
##          print "Cleaned", 'deltaR', deltaR(jet, obj), 'maxfrac', max([jet['muef'],jet['elef']]), 'pt:jet/obj', jet['pt'], obj['pt'], "relIso",  obj['relIso'], 'btag',getVarValue(c, 'jetsBtag', i), "parton", parton
#  #          print 'Not this one!', jet, obj, deltaR(jet, obj)
#          break
      jet['isolated'] = isIsolated(jet, crosscleanobjects, dR=dR)
      res.append(jet)
  res  = sorted(res,  key=lambda k: -k['pt'])
  return {'jets':res,'met_dx':met_dx, 'met_dy':met_dy}

def getGoodJetsStage2(c):#, jermode=options.jermode, jesmode=options.jesmode):
  njets = getVarValue(c, 'njetCount')   # jet.pt() > 10.
  res = []
  for i in range(int(njets)):
    res.append( {"eta":getVarValue(c, 'jetEta', i),\
          "pt" :getVarValue(c, 'jetPt', i),
          "phi":getVarValue(c, 'jetPhi', i), 
          'muef':getVarValue(c, 'jetMuef', i),
          'btag':getVarValue(c, 'jetBTag', i),
          'pdg':getVarValue(c, 'jetPdg', i)
      })
  
  return res 
