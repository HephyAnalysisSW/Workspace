import ROOT 
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy
from datetime import datetime

from defaultDiLeptonSamples import *
chmode = "Zmumu"

for p in ['../../MonoJetAnalysis/python', '../../HEPHYCommonTools/python']:
  path = os.path.abspath(p)
  if not path in sys.path:
      sys.path.insert(1, path)
  del path
from helpers import getVarValue, deltaR, invMassOfLightObjects

import xsec

subDir = "dileptonTuples_v1"

allSamples = [data_mumu]
#drellYan_mumu['bins']=drellYan_mumu['bins'][:1]
# from first parameter get mode, second parameter is sample type
if len(sys.argv)>=3:
  chmode = sys.argv[1]
  sampinp = sys.argv[2:]
  #steerable
  exec("allSamples = [" + ",".join(sampinp) + "]")

small  = False
overwrite = True
target_lumi = 19700 #pb-1

from localInfo import username
outputDir = "/data/"+username+"/"+subDir+"/"

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

def goodMuID(c, imu ):  
  isPF = getVarValue(c, 'muonsisPF', imu)
  isGlobal = getVarValue(c, 'muonsisGlobal', imu)
  isTracker = getVarValue(c, 'muonsisTracker', imu)
  pt = getVarValue(c, 'muonsPt', imu)
  dz = getVarValue(c, 'muonsDz', imu)
  eta=getVarValue(c, 'muonsEta', imu)
  relIso=getVarValue(c, 'muonsPFRelIso', imu)
  if isPF and (isGlobal or isTracker) and pt>20. and abs(eta)<2.1 and abs(dz)<0.5 and relIso<0.2:
    return {'pt':pt, 'phi':getVarValue(c, 'muonsPhi', imu), 'eta':eta, 'IsGlobal':isGlobal, 'IsTracker':isTracker, 'IsPF':isPF, 'relIso':getVarValue(c, 'muonsPFRelIso', imu), 'Dz':dz} 

def goodEleID(c, iele, eta = 'none'): # POG Ele veto https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaCutBasedIdentification
  if eta=='none':
    eta = getVarValue(c, 'elesEta', iele)
  sietaieta = getVarValue(c, 'elesSigmaIEtaIEta', iele)
  dphi = getVarValue(c, 'elesDPhi', iele)
  deta = getVarValue(c, 'elesDEta', iele)
  HoE  = getVarValue(c, 'elesHoE', iele)
  isEB = abs(eta) < 1.479
  isEE = abs(eta) > 1.479 and abs(eta) < 2.5
  relIso = getVarValue(c, 'elesPfRelIso', iele)
  pt = getVarValue(c, 'elesPt', iele)
  relIsoCut = 0.15
  return( isEE or isEB)\
    and ((isEB and dphi < 0.15) or (isEE and dphi < 0.1)) and ( (isEB and deta < 0.007) or (isEE and deta < 0.009) )\
    and ((isEB and sietaieta < 0.01 ) or (isEE and sietaieta < 0.03))\
    and (( isEB and HoE < 0.12 ) or ( isEE and HoE < 0.10 ))\
    and getVarValue(c, 'elesDxy', iele) < 0.02 and getVarValue(c, 'elesDz', iele) < 0.2 \
    and ( relIso < relIsoCut ) \
    and getVarValue(c, 'elesPassConversionRejection', iele)\
    and getVarValue(c, 'elesMissingHits', iele)<=1\
    and getVarValue(c, 'elesPt', iele)>20.

  # -------------------------------------------

def goodTauID_POG(c, itau ): 
  return getVarValue(c, 'tausisPF', itau) and \
         getVarValue(c, 'tausDecayModeFinding', itau) and \
         getVarValue(c, 'tausAgainstMuonLoose', itau) and \
         getVarValue(c, 'tausAgainstElectronLoose', itau) and \
         getVarValue(c, 'tausByLooseCombinedIsolationDBSumPtCorr', itau) and \
         getVarValue(c, 'tausPt', itau)>15.

def getAllMuons(c, nmuons ):
  res=[]
  for i in range(0, int(nmuons)):
    cand = goodMuID(c, i)
    if cand:
      for v in ['Pdg', 'Dxy', 'NormChi2', 'NValMuonHits', 'NumMatchedStations', 'PixelHits', 'NumtrackerLayerWithMeasurement']:
        cand[v] = getVarValue(c, 'muons'+v, i)
      res.append(cand)
#      res.append({'pt':getVarValue(c, 'muonsPt', i),'eta':getVarValue(c, 'muonsEta', i), 'phi':getVarValue(c, 'muonsPhi', i),\
#      'pdg':getVarValue(c, 'muonsPdg', i), 'relIso':getVarValue(c, 'muonsPFRelIso', i),\
#      'dxy':getVarValue(c, 'muonsDxy', i), 'dz':getVarValue(c, 'muonsDz', i)})
  res = sorted(res, key=lambda k: -k['pt'])
  return res

def getAllElectrons(c, neles ):
  res=[]
  for i in range(0, int(neles)):
    eta = getVarValue(c, 'elesEta', i)
    if goodEleID(c, i, abs(eta)):
      res.append({'pt':getVarValue(c, 'elesPt', i),'eta':eta, 'phi':getVarValue(c, 'elesPhi', i),\
      'pdg':getVarValue(c, 'elesPdg', i), 'relIso':getVarValue(c, 'elesPfRelIso', i),\
      'dxy':getVarValue(c, 'elesDxy', i), 'dz':getVarValue(c, 'elesDz', i)} )
  res = sorted(res, key=lambda k: -k['pt'])
  return res

def getAllTaus(c, ntaus ):
  res=[]
  for i in range(0, int(ntaus)):
    if goodTauID_POG(c, i):
      res.append({'pt':getVarValue(c, 'tausPt', i),'eta':getVarValue(c, 'tausEta', i), 'phi':getVarValue(c, 'tausPhi', i),\
      'pdg':getVarValue(c, 'tausPdg', i)})
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
  
def getGoodJets(c, crosscleanobjects):
  njets = getVarValue(c, 'nsoftjets')   # jet.pt() > 10.
  res = []
  bres = []
  ht = 0.
  nbtags = 0
  for i in range(int(njets)):
    eta = getVarValue(c, 'jetsEta', i)
    pt  = getVarValue(c, 'jetsPt', i)
    id =  getVarValue(c, 'jetsID', i)
    if abs(eta) <= 4.5 and pt >= 30. and id:
      phi = getVarValue(c, 'jetsPhi', i)
      parton = int(abs(getVarValue(c, 'jetsParton', i)))
      jet = {'pt':pt, 'eta':eta,'phi':phi, 'pdg':parton,\
      'id':id,
      'chef':getVarValue(c, 'jetsChargedHadronEnergyFraction', i), 'nhef':getVarValue(c, 'jetsNeutralHadronEnergyFraction', i),\
      'ceef':getVarValue(c, 'jetsChargedEmEnergyFraction', i), 'neef':getVarValue(c, 'jetsNeutralEmEnergyFraction', i), 'id':id,\
      'hfhef':getVarValue(c, 'jetsHFHadronEnergyFraction', i), 'hfeef':getVarValue(c, 'jetsHFEMEnergyFraction', i),\
      'muef':getVarValue(c, 'jetsMuonEnergyFraction', i), 'elef':getVarValue(c, 'jetsElectronEnergyFraction', i), 'phef':getVarValue(c, 'jetsPhotonEnergyFraction', i),\
      'jetCutBasedPUJetIDFlag':getVarValue(c, 'jetsCutBasedPUJetIDFlag', i),'jetMET53XPUJetIDFlag':getVarValue(c, 'jetsMET53XPUJetIDFlag', i),'jetFull53XPUJetIDFlag':getVarValue(c, 'jetsFull53XPUJetIDFlag', i), 
      'btag': getVarValue(c, 'jetsBtag', i)
      }
      isolated = True
  #      if max([jet['muef'],jet['elef']]) > 0.6 : print jet
      for obj in crosscleanobjects:   #Jet cross-cleaning
        if deltaR(jet, obj) < 0.3:# and  obj['relIso']< relIsoCleaningRequ: #(obj['pt']/jet['pt']) > 0.4:  
          isolated = False
#          print "Cleaned", 'deltaR', deltaR(jet, obj), 'maxfrac', max([jet['muef'],jet['elef']]), 'pt:jet/obj', jet['pt'], obj['pt'], "relIso",  obj['relIso'], 'btag',getVarValue(c, 'jetsBtag', i), "parton", parton
  #          print 'Not this one!', jet, obj, deltaR(jet, obj)
          break
      if  isolated:
        res.append(jet)
  res  = sorted(res,  key=lambda k: -k['pt'])
  return res 

def kin(o):
  return [o['pt'], o['eta'], o['phi']]

##################################################################################
storeVectors = True
commoncf = "(1)"

for sample in allSamples:
  sample['filenames'] = {}
  sample['weight'] = {}
  for bin in sample['bins']:
    sample['filenames'][bin] = []
    nEvents = 0
    if sample.has_key('subDirs'):
      subDirsToAdd = sample['subDirs'][bin]
    else:
      subDirsToAdd = [bin]
    for subdir in subDirsToAdd:
      print "Sample",sample['name'], "Bin",bin,"adding",subdir
      subdirname = sample['dirname']+'/'+subdir+'/'
      if not bin.lower().count('run'):
        nEvents+=eventsInSample[subdir.replace('Mu-','').replace('Ele-','')]
      prefix = ""
      if subdirname[0:5] != "/dpm/":
        filelist = os.listdir(subdirname)
      else:
    # this is specific to rfio    
        filelist = []
        allFiles = os.popen("rfdir %s | awk '{print $9}'" % (subdirname))
        for file in allFiles.readlines():
          file = file.rstrip()
    #        if(file.find("histo_548_1_nmN") > -1): continue
          filelist.append(file)
        prefix = "root://hephyse.oeaw.ac.at/"#+subdirname
      if small: filelist = filelist[:10]
    ####
      for tfile in filelist:
    #      if os.path.isfile(subdirname+tfile) and tfile[-5:] == '.root' and tfile.count('histo') == 1:
        sample['filenames'][bin].append(subdirname+tfile)
    if not bin.lower().count('run'):
      weight = xsec.xsec[bin.replace("Ele-","8TeV-").replace("Mu-","8TeV-")]*target_lumi/nEvents
    else:
      weight = 1.
    print 'Sample', sample['name'], 'bin', bin, 'nEvents(only valid for MC)',nEvents,'weight',weight
    sample["weight"][bin]=weight


if not os.path.isdir(outputDir):
  os.system('mkdir -p '+outputDir)
if not os.path.isdir(outputDir+"/"+chmode):
  os.system("mkdir "+outputDir+"/"+chmode)

nc = 0
for isample, sample in enumerate(allSamples):
  if not os.path.isdir(outputDir+"/"+chmode+"/"+sample["name"]):
    os.system("mkdir "+outputDir+"/"+chmode+"/"+sample["name"])
  else:
    print "Directory", outputDir+"/"+chmode, "already found"

  variables = ["weight", "run", "lumi", "ngoodVertices", "type1phiMet", "type1phiMetphi"]
  if not sample['name'].lower().count('data'):
#    alltriggers =  [ "HLTL1ETM40", "HLTMET120", "HLTMET120HBHENoiseCleaned", "HLTMonoCentralPFJet80PFMETnoMu105NHEF0p95", "HLTMonoCentralPFJet80PFMETnoMu95NHEF0p95"]
#    for trigger in alltriggers:
#      variables.append(trigger)
#      variables.append(trigger.replace("HLT", "pre") )
    variables.extend(["nTrueGenVertices", "genmet", "genmetphi", "genmetChargedEM", "genmetChargedHad", "genmetMuonEt",  "genmetNeutralEM",  "genmetNeutralHad",  "genmetSumEt", "puWeight", "puWeightSysPlus", "puWeightSysMinus"])
  
  jetvars = ["jetPt", "jetEta", "jetPhi", "jetPdg", "jetBtag", "jetCutBasedPUJetIDFlag","jetFull53XPUJetIDFlag","jetMET53XPUJetIDFlag", "jetChef", "jetNhef", "jetCeef", "jetNeef", "jetHFhef", "jetHFeef", "jetMuef", "jetElef", "jetPhef"]
  muvars = ["muPt", "muEta", "muPhi", "muPdg", "muRelIso", "muDxy", "muDz", "muNormChi2", "muNValMuonHits", "muNumMatchedStations", "muPixelHits", "muNumtrackerLayerWithMeasurement", 'muIsGlobal', 'muIsTracker']
  elvars = ["elPt", "elEta", "elPhi", "elPdg", "elRelIso", "elDxy", "elDz"]
  tavars = ["taPt", "taEta", "taPhi", "taPdg"]
  for m in ["patMETs", "patPFMet", "patPFMetMVA", "patPFMetMVAUnity", "patPFMetNoPileUp", "patType1p2CorrectedPFMet"]:
    variables.append(m)
    variables.append(m+"phi")
    variables.append(m+"sumEt")
  for m in ["patPFMetJetEnDown","patPFMetJetEnUp","patPFMetMVAJetEnDown","patPFMetMVAJetEnDownUnity","patPFMetMVAJetEnUp","patPFMetMVAJetEnUpUnity","patPFMetMVAMuonEnDown","patPFMetMVAMuonEnDownUnity","patPFMetMVAMuonEnUp","patPFMetMVAMuonEnUpUnity","patPFMetMVAUnclusteredEnDown","patPFMetMVAUnclusteredEnDownUnity","patPFMetMVAUnclusteredEnUp","patPFMetMVAUnclusteredEnUpUnity","patPFMetMuonEnDown","patPFMetMuonEnUp","patPFMetNoPileUpJetEnDown","patPFMetNoPileUpJetEnUp","patPFMetNoPileUpMuonEnDown","patPFMetNoPileUpMuonEnUp","patPFMetNoPileUpUnclusteredEnDown","patPFMetNoPileUpUnclusteredEnUp","patPFMetUnclusteredEnDown","patPFMetUnclusteredEnUp","patType1CorrectedPFMet","patType1CorrectedPFMetJetEnDown","patType1CorrectedPFMetJetEnUp","patType1CorrectedPFMetMuonEnDown","patType1CorrectedPFMetMuonEnUp","patType1CorrectedPFMetUnclusteredEnDown","patType1CorrectedPFMetUnclusteredEnUp","patType1p2CorrectedPFMetJetEnDown","patType1p2CorrectedPFMetJetEnUp","patType1p2CorrectedPFMetMuonEnDown","patType1p2CorrectedPFMetMuonEnUp","patType1p2CorrectedPFMetUnclusteredEnDown","patType1p2CorrectedPFMetUnclusteredEnUp"]:
    variables.append(m)

  extraVariables=["nbtags", "ht", "Zm", "Zpt", "Zphi", "Zpz", "Zeta", "l0pt", "l0eta", "l0phi", "l0e", "l1pt", "l1eta", "l1phi", "l1e"]
  structString = "struct MyStruct_"+str(nc)+"_"+str(isample)+"{ULong64_t event;"
  for var in variables:
    structString +="Float_t "+var+";"
  for var in extraVariables:
    structString +="Float_t "+var+";"
  structString +="Int_t nmu, nel, nta, njet;"
  if storeVectors:
    structString +="Int_t njetCount, nmuCount, nelCount, ntaCount;"
    for var in jetvars:
      structString +="Float_t "+var+"[10];"
    for var in muvars:
      structString +="Float_t "+var+"[10];"
    for var in elvars:
      structString +="Float_t "+var+"[10];"
    for var in tavars:
      structString +="Float_t "+var+"[10];"
  structString   +="};"

  ROOT.gROOT.ProcessLine(structString)
  exec("from ROOT import MyStruct_"+str(nc)+"_"+str(isample))
  exec("s = MyStruct_"+str(nc)+"_"+str(isample)+"()")
  nc+=1
  postfix=""
  if small:
    postfix="_small"
  ofile = outputDir+"/"+chmode+"/"+sample["name"]+"/histo_"+sample["name"]+postfix+".root"
  if os.path.isfile(ofile) and overwrite:
    print "Warning! will overwrite",ofile
  if os.path.isfile(ofile) and not overwrite:
    print ofile, "already there! Skipping!!!"
    continue
  chain_gDir = ROOT.gDirectory.func() 
  t = ROOT.TTree( "Events", "Events", 1 )
  t.Branch("event",   ROOT.AddressOf(s,"event"), 'event/l')
  for var in variables:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
  for var in extraVariables:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
  t.Branch("njet",   ROOT.AddressOf(s,"njet"), 'njet/I')
  t.Branch("nmu",   ROOT.AddressOf(s,"nmu"), 'nmu/I')
  t.Branch("nel",   ROOT.AddressOf(s,"nel"), 'nel/I')
  t.Branch("nta",   ROOT.AddressOf(s,"nta"), 'nta/I')
  if storeVectors:
    t.Branch("njetCount",   ROOT.AddressOf(s,"njetCount"), 'njetCount/I')
    t.Branch("nelCount",   ROOT.AddressOf(s,"nelCount"), 'nelCount/I')
    t.Branch("nmuCount",   ROOT.AddressOf(s,"nmuCount"), 'nmuCount/I')
    t.Branch("ntaCount",   ROOT.AddressOf(s,"ntaCount"), 'ntaCount/I')
    for var in jetvars:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'[njetCount]/F')
    for var in muvars:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'[nmuCount]/F')
    for var in elvars:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'[nelCount]/F')
    for var in tavars:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'[ntaCount]/F')
  for bin in sample["bins"]:
    c = ROOT.TChain(sample["Chain"])
    for thisfile in sample["filenames"][bin]:
      prefix = ""
      if thisfile[0:5] == "/dpm/":
#        prefix = "rfio:"
        prefix = "root://hephyse.oeaw.ac.at/"#+subdirname
#      print "Chaining",prefix+thisfile

      c.Add(prefix+thisfile)
    ntot = c.GetEntries()
    if sample.has_key("additionalCut"):
      if type(sample["additionalCut"])==type({}):
        if sample["additionalCut"].has_key(bin):
          commoncf = commoncf+"&&"+sample["additionalCut"][bin]
      else:
        commoncf = commoncf+"&&"+sample["additionalCut"]

    if ntot>0:
      c.Draw(">>eList", commoncf)
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      print "Reading: ", sample["name"], bin, "with",number_events,"Events using cut", commoncf
      if small:
        if number_events>1000:
          number_events=1000
      for i in range(0, number_events):
        if (i%10000 == 0) and i>0 :
          print i
  #      # Update all the Tuples
        if elist.GetN()>0 and ntot>0:
          c.GetEntry(elist.GetEntry(i))
          s.weight = sample["weight"][bin]
          for var in variables[1:]:
            getVar = var
            exec("s."+var+"="+str(getVarValue(c, getVar)).replace("nan","float('nan')"))
          s.event = long(c.GetLeaf(c.GetAlias('event')).GetValue())

          if not sample['name'].lower().count('data'):
            nvtxWeightSysPlus, nvtxWeightSysMinus, nvtxWeight = 1.,1.,1.
            if sample.has_key('reweightingHistoFile'): 
              s.puWeight = s.weight*sample['reweightingHistoFile'].GetBinContent(sample['reweightingHistoFile'].FindBin(s.nTrueGenVertices))
            if sample.has_key('reweightingHistoFileSysPlus'): 
              s.puWeightSysPlus = s.weight*sample['reweightingHistoFileSysPlus'].GetBinContent(sample['reweightingHistoFileSysPlus'].FindBin(s.nTrueGenVertices))
            if sample.has_key('reweightingHistoFileSysMinus'): 
              s.puWeightSysMinus = s.weight*sample['reweightingHistoFileSysMinus'].GetBinContent(sample['reweightingHistoFileSysMinus'].FindBin(s.nTrueGenVertices))


          for var in extraVariables:
            exec("s."+var+"=float('nan')")
          nmuons = getVarValue(c, 'nmuons')   #Number of muons in Muon Vec
          neles  = getVarValue(c, 'neles')    #Number of eles in Ele Vec
          ntaus  = getVarValue(c, 'ntaus')    #Number of eles in Ele Vec
          allGoodMuons = getAllMuons(c,nmuons)
          allGoodElectrons = getAllElectrons(c, neles)
          allGoodTaus = getAllTaus(c, ntaus)

          if chmode=="Zee":
            if not len(allGoodElectrons)>=2: continue
            dilep = allGoodElectrons[:2]

          if chmode=="Zmumu":
            if not len(allGoodMuons)>=2: continue
            dilep = allGoodMuons[:2]
          Zpx= dilep[0]['pt']*cos(dilep[0]['phi']) + dilep[1]['pt']*cos(dilep[1]['phi'])
          Zpy= dilep[0]['pt']*sin(dilep[0]['phi']) + dilep[1]['pt']*sin(dilep[1]['phi'])
          Zpz= dilep[0]['pt']*sinh(dilep[0]['eta']) + dilep[1]['pt']*sinh(dilep[1]['eta'])
          Zpt=sqrt(Zpx**2 + Zpy**2)
          Ztheta = atan(Zpt/Zpz) 
          el0  = dilep[0]['pt']*cosh(dilep[0]['eta'])
          el1  = dilep[1]['pt']*cosh(dilep[1]['eta'])
          s.Zm  = sqrt((el0+el1)**2 - Zpx**2 - Zpy**2 - Zpz**2)
          s.Zpt = Zpt 
          s.Zphi = atan2(Zpy, Zpx)
          s.Zpz = Zpz
          sign = +1
          if Zpz<0: sign=-1
          s.Zeta = -log(abs(tan(Ztheta/2.)))*sign
          s.l0pt  = dilep[0]['pt']
          s.l0eta = dilep[0]['eta']
          s.l0phi = dilep[0]['phi']
          s.l0e   = el0
          s.l1pt  = dilep[1]['pt']
          s.l1eta = dilep[1]['eta']
          s.l1phi = dilep[1]['phi']
          s.l1e   = el1

          jets = getGoodJets(c, allGoodMuons + allGoodElectrons)
          s.ht = sum([ j['pt'] for j in jets])
          s.njet    = len(jets)
          s.nbtags  = len(filter(lambda j:j['btag']>0.679, jets))
          s.nmu = len(allGoodMuons)
          s.nel = len(allGoodElectrons)
          s.nta = len(allGoodTaus)
          
          if storeVectors:
            s.njetCount = min(10,s.njet)
            for i in xrange(s.njetCount):
              s.jetPt[i]    = jets[i]['pt']
              s.jetEta[i]   = jets[i]['eta']
              s.jetPhi[i]   = jets[i]['phi']
              s.jetPdg[i]   = jets[i]['pdg']
              s.jetBtag[i]  = jets[i]['btag']
              s.jetChef[i]  = jets[i]['chef']
              s.jetNhef[i]  = jets[i]['nhef']
              s.jetCeef[i]  = jets[i]['ceef']
              s.jetNeef[i]  = jets[i]['neef']
              s.jetHFhef[i] = jets[i]['hfhef']
              s.jetHFeef[i] = jets[i]['hfeef']
              s.jetMuef[i]  = jets[i]['muef']
              s.jetElef[i]  = jets[i]['elef']
              s.jetPhef[i]  = jets[i]['phef']
              s.jetCutBasedPUJetIDFlag[i] = jets[i]['jetCutBasedPUJetIDFlag']
              s.jetFull53XPUJetIDFlag[i]  = jets[i]['jetFull53XPUJetIDFlag']
              s.jetMET53XPUJetIDFlag[i]   = jets[i]['jetMET53XPUJetIDFlag']

            s.nmuCount = min(10,s.nmu)
            for i in xrange(s.nmuCount):
              s.muPt[i] = allGoodMuons[i]['pt']
              s.muEta[i] = allGoodMuons[i]['eta']
              s.muPhi[i] = allGoodMuons[i]['phi']
              s.muPdg[i] = allGoodMuons[i]['Pdg']
              s.muRelIso[i] = allGoodMuons[i]['relIso']
              s.muDxy[i] = allGoodMuons[i]['Dxy']
              s.muDz[i] = allGoodMuons[i]['Dz']
              s.muNormChi2[i] = allGoodMuons[i]['NormChi2']
              s.muNValMuonHits[i] = allGoodMuons[i]['NValMuonHits']
              s.muNumMatchedStations[i] = allGoodMuons[i]['NumMatchedStations']
              s.muPixelHits[i] = allGoodMuons[i]['PixelHits']
              s.muNumtrackerLayerWithMeasurement[i] = allGoodMuons[i]['NumtrackerLayerWithMeasurement']
              s.muIsGlobal[i] = allGoodMuons[i]['IsGlobal']
              s.muIsTracker[i] = allGoodMuons[i]['IsTracker']

            s.nelCount = min(10,s.nel)
            for i in xrange(s.nelCount):
              s.elPt[i] = allGoodElectrons[i]['pt']
              s.elEta[i] = allGoodElectrons[i]['eta']
              s.elPhi[i] = allGoodElectrons[i]['phi']
              s.elPdg[i] = allGoodElectrons[i]['pdg']
              s.elRelIso[i] = allGoodElectrons[i]['relIso']
              s.elDxy[i] = allGoodElectrons[i]['dxy']
              s.elDz[i] = allGoodElectrons[i]['dz']
#              print "Electron pt's:",i,allGoodElectrons[i]['pt']
            s.ntaCount = min(10,s.nta)
            for i in xrange(s.ntaCount):
              s.taPt[i] = allGoodTaus[i]['pt']
              s.taEta[i] = allGoodTaus[i]['eta']
              s.taPhi[i] = allGoodTaus[i]['phi']
              s.taPdg[i] = allGoodTaus[i]['pdg']
          tmpDir = ROOT.gDirectory.func()
          chain_gDir.cd()
          t.Fill()
          tmpDir.cd()
      del elist
    else:
      print "Zero entries in", bin, sample["name"]
    del c
  if True or not small: #FIXME
    f = ROOT.TFile(ofile, "recreate")
    t.Write()
    f.Close()
    print "Written",ofile
  else:
    print "No saving when small!"
  del t
