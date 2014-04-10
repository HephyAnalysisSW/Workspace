import ROOT 
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy, random, array
from datetime import datetime
from Workspace.HEPHYPythonTools.helpers import getVarValue, deltaPhi, minAbsDeltaPhi,  deltaR, invMass, findClosestJet
from defaultSamples import *
from  Workspace.RA4Analysis import eventShape, mt2w

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/Thrust.C+")

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--chmode", dest="chmode", default="copy", type="string", action="store", help="chmode: What to do.")
parser.add_option("--jermode", dest="jermode", default="none", type="string", action="store", help="jermode: up/down/central/none")
parser.add_option("--jesmode", dest="jesmode", default="none", type="string", action="store", help="jesmode: up/down/none")
parser.add_option("--samples", dest="allsamples", default="copy", type="string", action="store", help="samples:Which samples.")
parser.add_option("--smsMglRange", dest="smsMglRangeString", default="None", type="string", action="store", help="What is the Mgl range? Maximum is 400-1425.")
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")
parser.add_option("--fromPercentage", dest="fromPercentage", default="0", type="int", action="store", help="from (% of tot. events)")
parser.add_option("--toPercentage", dest="toPercentage", default="100", type="int", action="store", help="to (% of tot. events)")

(options, args) = parser.parse_args()
print "options: chmode",options.chmode, "jermode",options.jermode, "jesmode",options.jesmode

def htFractionThrustSide(oPhi, thrustPhi, jets ):
  if cos(oPhi - thrustPhi)>0:
    sign = 1
  else:
    sign=-1
  htThrustObjSide = 0.
  for j in jets:
    if sign*cos(thrustPhi - j['phi'])>0:
      htThrustObjSide+=j['pt']
  ht = sum([j['pt'] for j in jets])
  if ht>0:
    return htThrustObjSide/ht
  else:
    return float('nan')

def getPtISR(e):
    sumtlv = ROOT.TLorentzVector(1.e-9,1.e-9,1.e-9,1.e-9)
    for igp in range(e.ngp):
        if(abs(e.gpPdg[igp])==1000006 and e.gpSta[igp]==3):
            tlvaux = ROOT.TLorentzVector(0.,0.,0.,0.)
            tlvaux.SetPtEtaPhiM(e.gpPt[igp],e.gpEta[igp],e.gpPhi[igp],e.gpM[igp])
            sumtlv += tlvaux
    return sumtlv.Pt()


def jerEtaBin(eta):
  feta = fabs(eta)
  if feta<=.5 : return 0
  if feta>.5 and feta<=1.1: return 1
  if feta>1.1 and feta<=1.7: return 2
  if feta>1.7 and feta<=2.3: return 3
  if feta>2.3 and feta<=5.0: return 4
  return -1

def jerDifferenceScaleFactor( eta, jermode = "none"): #https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution
  if jermode.lower()=="none": return 1.
  etab = jerEtaBin(eta)
  if jermode.lower()=="down":
    if etab== 0: return  1.0  
    if etab== 1: return  1.001 
    if etab== 2: return  1.032
    if etab== 3: return  1.042 
    if etab== 4: return  1.089 
  if jermode.lower()=="central":
    if etab== 0: return 1.052
    if etab== 1: return 1.057
    if etab== 2: return 1.096
    if etab== 3: return 1.134
    if etab== 4: return 1.288
  if jermode.lower()=="up":
    if etab== 0: return 1.115  
    if etab== 1: return 1.114 
    if etab== 2: return 1.161 
    if etab== 3: return 1.228 
    if etab== 4: return 1.488 
  return 1.


from Workspace.HEPHYPythonTools.xsec import xsec

subDir = "convertedTuples_v22"

if options.smsMglRangeString!='None' and options.allsamples.lower()=='sms':
  from Workspace.HEPHYPythonTools.xsecSMS import gluino8TeV_NLONLL
  allSamples=[]
  mglStart = int(options.smsMglRangeString.split('-')[0])
  mglEnd = int(options.smsMglRangeString.split('-')[1])
  mglVals = range(mglStart, mglEnd, 25)
  print "Converting Mgl from",mglStart, 'to',mglEnd,'. Thats the following:',mglVals
  xsec = {}
  for mgl in mglVals:
    for mn in range(0,mgl-75, 25):
#    for mn in [250]:
#    for deltaM in [100]:
      T5LNu={}
      T5LNu["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314/"
      T5LNu['newMETCollection'] = True
      T5LNu["Chain"] = "Events"
      name = "T5LNu_"+str(mgl)+"_"+str(mn)
      T5LNu["bins"] = [[name,["T5lnuPlusPlus_mGo-400to1400_mLSP_300to1300","T5lnuPlusPlus_mGo-400to1400_mLSP_300to1300_400_775"]]]
      T5LNu["name"] = name
      xsec[name] = gluino8TeV_NLONLL[mgl]
      T5LNu["additionalCut"] = "osetMgl=="+str(mgl)+"&&osetMN=="+str(mn)
#      T5LNu["additionalCut"] = "(1)"
      T5LNu['reweightingHistoFile'] = S10rwHisto
      T5LNu['reweightingHistoFileSysPlus'] = S10rwPlusHisto
      T5LNu['reweightingHistoFileSysMinus'] = S10rwMinusHisto
      T5LNu['reweightingHistoFile'] = S10rwHisto
      T5LNu['reweightingHistoFileSysPlus'] = S10rwPlusHisto
      T5LNu['reweightingHistoFileSysMinus'] = S10rwMinusHisto
      allSamples.append(T5LNu)
      print "Added SMS",T5LNu["name"]
else:
  exec("allSamples = [" +options.allsamples+ "]")

overwrite = True
target_lumi = 19700 #pb-1

from localConfig import username
outputDir = "/data/"+username+"/"+subDir+"/"

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

def getLooseMu(c, imu ):  
  isPF = getVarValue(c, 'muonsisPF', imu)
  isGlobal = getVarValue(c, 'muonsisGlobal', imu)
  isTracker = getVarValue(c, 'muonsisTracker', imu)
  pt = getVarValue(c, 'muonsPt', imu)
  dz = getVarValue(c, 'muonsDz', imu)
  eta=getVarValue(c, 'muonsEta', imu)
  if isPF and (isGlobal or isTracker) and pt>5. and abs(eta)<2.1 and abs(dz)<0.5:
    return {'pt':pt, 'phi':getVarValue(c, 'muonsPhi', imu), 'eta':eta, 'IsGlobal':isGlobal, 'IsTracker':isTracker, 'IsPF':isPF, 'relIso':getVarValue(c, 'muonsPFRelIso', imu), 'Dz':dz} 

# -------------------------------------------

def getVetoEle(c, iele): # POG Ele veto https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaCutBasedIdentification
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
  convRej = getVarValue(c, 'elesPassConversionRejection', iele)
  missingHits = getVarValue(c, 'elesMissingHits', iele)
  relIsoCut = 0.15
  if ( isEE or isEB)\
    and ((isEB and dphi < 0.8) or (isEE and dphi < 0.7)) and ( (isEB and deta < 0.007) or (isEE and deta < 0.01) )\
    and ((isEB and sietaieta < 0.01 ) or (isEE and sietaieta < 0.03))\
    and ( isEB and HoE < 0.15 )\
    and dxy < 0.04 and dz < 0.2 \
    and ( relIso < relIsoCut ) \
    and pt>5.:
    return {'pt':pt, 'phi':getVarValue(c, 'elesPhi', iele), 'Pdg':pdg, 'eta':eta, 'sIEtaIEta':sietaieta, 'DPhi':dphi, \
            'DEta':deta, 'HoE':HoE, 'OneOverEMinusOneOverP':oneOverEMinusOneOverP, 'ConvRejection':convRej, 'MissingHits':missingHits,\
            'isEB':isEB, 'isEE':isEE, 'relIso':relIso, 'Dxy':dxy, 'Dz':dz} 
def tightEleID(ele):
  return ele['pt']>20 and abs(ele['eta'])<2.5 and ele['relIso']<0.15 and ele['ConvRejection'] and ele['MissingHits']<=1 and ele['Dxy']<0.02 and ele['Dz']<0.1 and (\
    (ele['isEB'] and ele['DPhi']<0.06 and ele['DEta']<0.004 and ele['sIEtaIEta']<0.01) or
    (ele['isEE'] and ele['DPhi']<0.03 and ele['DEta']<0.007 and ele['sIEtaIEta']<0.03))

def goodTauID(c, itau ): 
  return getVarValue(c, 'tausisPF', itau) and \
         getVarValue(c, 'tausDecayModeFinding', itau) and \
         getVarValue(c, 'tausAgainstMuonLoose', itau) and \
         getVarValue(c, 'tausAgainstElectronLoose', itau) and \
         getVarValue(c, 'tausByLooseCombinedIsolationDBSumPtCorr', itau) and \
         getVarValue(c, 'tausPt', itau)>5.

def getAllMuons(c, nmuons ):
  res=[]
  for i in range(0, int(nmuons)):
    cand = getLooseMu(c, i)
    if cand:
      for v in ['Pdg', 'Dxy', 'NormChi2', 'NValMuonHits', 'NumMatchedStations', 'PixelHits', 'NumtrackerLayerWithMeasurement']:
        cand[v] = getVarValue(c, 'muons'+v, i)
      res.append(cand)
  res = sorted(res, key=lambda k: -k['pt'])
  return res

def tightMuID(mu):
  return mu['IsGlobal'] and mu['IsPF'] and mu['pt']>20 and abs(mu['eta'])<2.1 and mu['relIso']<0.12 and mu['NormChi2']<=10 and mu['NValMuonHits']>0\
     and mu['NumMatchedStations']>1 and mu['PixelHits']>0 and mu['NumtrackerLayerWithMeasurement']>5 and mu['Dxy']<0.02 and mu['Dz']<0.5

def getAllElectrons(c, neles ):
  res=[]
  for i in range(0, int(neles)):
    cand =  getVetoEle(c, i)
    if cand:
      res.append(cand)
  res = sorted(res, key=lambda k: -k['pt'])
  return res

def getAllTaus(c, ntaus ):
  res=[]
  for i in range(0, int(ntaus)):
    if goodTauID(c, i):
      res.append({'pt':getVarValue(c, 'tausPt', i),'eta':getVarValue(c, 'tausEta', i), 'phi':getVarValue(c, 'tausPhi', i),\
      'Pdg':getVarValue(c, 'tausPdg', i)})
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
  
def getGoodJets(c, crosscleanobjects, jermode=options.jermode, jesmode=options.jesmode):
  nSoftJets = getVarValue(c, 'nsoftjets')   # jet.pt() > 10.
  res = []
  bres = []
  ht = 0.
  nbtags = 0
  met_dx = 0.
  met_dy = 0.
  if jesmode.lower()!="none":
    if jesmode.lower()=='up':
      sign=+1
    if jesmode.lower()=='down':
      sign=-1
    delta_met_x_unclustered = getVarValue(c, 'deltaMETxUnclustered')
    delta_met_y_unclustered = getVarValue(c, 'deltaMETyUnclustered')
    met_dx+=0.1*delta_met_x_unclustered
    met_dy+=0.1*delta_met_y_unclustered
  for i in range(int(nSoftJets)):
    eta = getVarValue(c, 'jetsEta', i)
    pt  = getVarValue(c, 'jetsPt', i)
    if abs(eta) <= 4.5:
      unc = getVarValue(c, 'jetsUnc', i)
      id =  getVarValue(c, 'jetsID', i)
      phi = getVarValue(c, 'jetsPhi', i)
  #      if max([jet['muef'],jet['elef']]) > 0.6 : print jet
      if jermode.lower()!="none":
        c_jet = jerDifferenceScaleFactor(eta, jermode)
        sigma = sqrt(c_jet**2 - 1)*unc
        scale = random.gauss(1,sigma)
        met_dx+=(1-scale)*cos(phi)*pt
        met_dy+=(1-scale)*sin(phi)*pt
        pt*=random.gauss(1,sigma)
      if jesmode.lower()!="none":
        scale = 1. + sign*unc
        met_dx+=(1-scale)*cos(phi)*pt
        met_dy+=(1-scale)*sin(phi)*pt
        pt*=scale
      if pt>40:
        parton = int(abs(getVarValue(c, 'jetsParton', i)))
        jet = {'pt':pt, 'eta':eta,'phi':phi, 'Pdg':parton,\
        'id':id,
        'chef':getVarValue(c, 'jetsChargedHadronEnergyFraction', i), 'nhef':getVarValue(c, 'jetsNeutralHadronEnergyFraction', i),\
        'ceef':getVarValue(c, 'jetsChargedEmEnergyFraction', i), 'neef':getVarValue(c, 'jetsNeutralEmEnergyFraction', i), 'id':id,\
        'hfhef':getVarValue(c, 'jetsHFHadronEnergyFraction', i), 'hfeef':getVarValue(c, 'jetsHFEMEnergyFraction', i),\
        'muef':getVarValue(c, 'jetsMuonEnergyFraction', i), 'elef':getVarValue(c, 'jetsElectronEnergyFraction', i), 'phef':getVarValue(c, 'jetsPhotonEnergyFraction', i),\
        'jetCutBasedPUJetIDFlag':getVarValue(c, 'jetsCutBasedPUJetIDFlag', i),'jetMET53XPUJetIDFlag':getVarValue(c, 'jetsMET53XPUJetIDFlag', i),'jetFull53XPUJetIDFlag':getVarValue(c, 'jetsFull53XPUJetIDFlag', i), 
        'btag': getVarValue(c, 'jetsBtag', i), 'unc': unc 
        }
        isolated = True
        for obj in crosscleanobjects:   #Jet cross-cleaning
          if deltaR(jet, obj) < 0.3:# and  obj['relIso']< relIsoCleaningRequ: #(obj['pt']/jet['pt']) > 0.4:  
            isolated = False
  #          print "Cleaned", 'deltaR', deltaR(jet, obj), 'maxfrac', max([jet['muef'],jet['elef']]), 'pt:jet/obj', jet['pt'], obj['pt'], "relIso",  obj['relIso'], 'btag',getVarValue(c, 'jetsBtag', i), "parton", parton
    #          print 'Not this one!', jet, obj, deltaR(jet, obj)
            break
        jet['isolated'] = isolated
        res.append(jet)
  res  = sorted(res,  key=lambda k: -k['pt'])
  return {'jets':res,'met_dx':met_dx, 'met_dy':met_dy}


# helpers for GenParticle serching
def find(x,lp):
  for ip,p in enumerate(lp):
    if x == p:
      break
  if ip == len(lp)-1:
    ip = -1
  return ip

def findSec(x,lp):
  gp = x
  while gp.status() != 3:
    gp = gp.mother(0)
  return gp

##################################################################################
storeVectors = True

for sample in allSamples:
  sample['filenames'] = {}
  sample['weight'] = {}
  for bin_ in sample['bins']:
    if type(bin_) == type([]):
      bin = bin_[0]
      subdirs = bin_[1]
    else:
      subdirs = [bin_]
      bin=bin_
    sample['filenames'][bin] = []
    for dir in subdirs:
      subdirname = sample['dirname']+'/'+dir+'/'
      print "Looping over subdir",subdirname
      if sample['bins'] == ['']:
        subdirname = sample['dirname']+'/'
      prefix = ""
      if subdirname[0:5] != "/dpm/":
        filelist = os.listdir(subdirname)
      else:
        filelist = []
        allFiles = os.popen("rfdir %s | awk '{print $9}'" % (subdirname))
        for file in allFiles.readlines():
          file = file.rstrip()
          filelist.append(file)
        prefix = "root://hephyse.oeaw.ac.at/"#+subdirname
      if options.small: filelist = filelist[:10]
      for tfile in filelist:
          sample['filenames'][bin].append(subdirname+tfile)

    if options.allsamples.lower()=='sms':
      c = ROOT.TChain(sample['Chain'])
      for tfile in sample['filenames'][bin]:
        print "Adding",prefix+tfile
        c.Add(prefix+tfile)
      nevents = c.GetEntries(sample['additionalCut'])
      print nevents, sample['additionalCut']
      del c
    else:
      d = ROOT.TChain('Runs')
      for tfile in sample['filenames'][bin]:
        d.Add(prefix+tfile)
      nevents = 0
      nruns = d.GetEntries()
      for i in range(0, nruns):
        d.GetEntry(i)
        nevents += getVarValue(d,'uint_EventCounter_runCounts_PAT.obj')
      del d

    if not bin.lower().count('run'):
      if nevents>0:
        weight = xsec[bin]*target_lumi/nevents
      else:
        weight=0
      print 'Sample', sample['name'], 'bin', bin,'xsec',xsec[bin], 'n-events',nevents,'weight',weight
    else:
      weight = 1.
      print 'Sample', sample['name'], 'bin', bin, 'n-events',nevents,'weight',weight
    sample["weight"][bin]=weight

if not os.path.isdir(outputDir):
  os.system('mkdir -p '+outputDir)
outSubDir = options.chmode
if options.jermode.lower()!='none':
  outSubDir = outSubDir+"_JER"+options.jermode.lower()
if options.jesmode.lower()!='none':
  outSubDir = outSubDir+"_JES"+options.jesmode.lower()
if not os.path.isdir(outputDir+"/"+outSubDir):
  os.system("mkdir "+outputDir+"/"+outSubDir)

nc = 0
for isample, sample in enumerate(allSamples):
  isData = sample['name'].lower().count('data')
  if not os.path.isdir(outputDir+"/"+outSubDir+"/"+sample["name"]):
    os.system("mkdir "+outputDir+"/"+outSubDir+"/"+sample["name"])
  else:
    print "Directory", outputDir+"/"+outSubDir, "already found"

  variables = ["weight", "run", "lumi", "ngoodVertices"]
  if sample['newMETCollection']:
    variables+=["met", "metphi"]
  else:
    variables+=["type1phiMet", "type1phiMetphi"]
  if isData:
    alltriggers =  [ "HLTL1ETM40", "HLTMET120", "HLTMET120HBHENoiseCleaned", "HLTMonoCentralPFJet80PFMETnoMu105NHEF0p95", "HLTMonoCentralPFJet80PFMETnoMu95NHEF0p95"]
    for trigger in alltriggers:
      variables.append(trigger)
      variables.append(trigger.replace("HLT", "pre") )
  else:
    variables.extend(["nTrueGenVertices", "genmet", "genmetphi", "puWeight", "puWeightSysPlus", "puWeightSysMinus", "ptISR"])
    variables.extend(["antinuMu", "antinuE", "antinuTau", "nuMu", "nuE", "nuTau", "nuMuFromTausFromWs", "nuEFromTausFromWs", "nuTauFromTausFromWs"])

  jetvars = ["jetPt", "jetEta", "jetPhi", "jetPdg", "jetBtag", "jetCutBasedPUJetIDFlag","jetFull53XPUJetIDFlag","jetMET53XPUJetIDFlag", "jetChef", "jetNhef", "jetCeef", "jetNeef", "jetHFhef", "jetHFeef", "jetMuef", "jetElef", "jetPhef", "jetUnc"]
  muvars = ["muPt", "muEta", "muPhi", "muPdg", "muRelIso", "muDxy", "muDz", "muNormChi2", "muNValMuonHits", "muNumMatchedStations", "muPixelHits", "muNumtrackerLayerWithMeasurement", 'muIsGlobal', 'muIsTracker']
  elvars = ["elPt", "elEta", "elPhi", "elPdg","elSIEtaIEta", "elDPhi", "elDEta", "elHoE", "elOneOverEMinusOneOverP", "elConvRejection", "elMissingHits", "elIsEB", "elIsEE", "elRelIso", "elDxy", "elDz"]
  tavars = ["taPt", "taEta", "taPhi", "taPdg"]
  if not isData:
    mcvars = ["gpPdg", "gpM", "gpPt", "gpEta", "gpPhi", "gpMo1", "gpMo2", "gpDa1", "gpDa2", "gpSta"]
  if options.allsamples.lower()=='sms':
    variables+=['osetMgl', 'osetMN', 'osetMC', 'osetMsq']
  extraVariables=["ht","nTightMuons", "nTightElectrons"]
  if sample['newMETCollection']:
    extraVariables+=["type1phiMet", "type1phiMetphi"]
  extraVariables+=["thrust", "thrustPhi", "thrustEta", "htThrustLepSideRatio", "htThrustMetSideRatio", "htThrustWSideRatio"]
  extraVariables+=['mt2w', "S3D", "C3D", "C2D", "linS3D", "linC3D", "linC2D", "FWMT1", "FWMT2", "FWMT3", "FWMT4","linC2DLepMET", "c2DLepMET", "FWMT1LepMET", "FWMT2LepMET", "FWMT3LepMET", "FWMT4LepMET"]
  extraVariables+=["leptonPt", "leptonPhi", "leptonEta", "leptonPdg", "mT", 'WPt', 'WPhi', "cosDeltaPhi", "lepton2Pt", "lepton2Phi", "lepton2Eta", "lepton2Pdg"]

  if storeVectors: 
    if sample['name'].lower().count('ttjets'):
      extraVariables+=["top0Pt", "top1Pt", "topPtWeight"] 
  structString = "struct MyStruct_"+str(nc)+"_"+str(isample)+"{ULong64_t event;"
  structString+="Float_t "+",".join(variables+extraVariables)+";"
  structString +="Int_t nmu, nel, nta, njets, nbtags, njetFailID;"
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
    if not isData:
      structString +="Int_t ngp;"
      for var in mcvars:
        structString +="Float_t "+var+"[40];"
  structString   +="};"
#  print structString

  ROOT.gROOT.ProcessLine(structString)
  exec("from ROOT import MyStruct_"+str(nc)+"_"+str(isample))
  exec("s = MyStruct_"+str(nc)+"_"+str(isample)+"()")
  nc+=1
  postfix=""
  if options.small:
    postfix="_small"
  if options.fromPercentage!=0 or options.toPercentage!=100:
    postfix += "_from"+str(options.fromPercentage)+"To"+str(options.toPercentage)
  ofile = outputDir+"/"+outSubDir+"/"+sample["name"]+"/histo_"+sample["name"]+postfix+".root"
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
  t.Branch("nmu",   ROOT.AddressOf(s,"nmu"), 'nmu/I')
  t.Branch("nel",   ROOT.AddressOf(s,"nel"), 'nel/I')
  t.Branch("nta",   ROOT.AddressOf(s,"nta"), 'nta/I')
  t.Branch("njets",   ROOT.AddressOf(s,"njets"), 'njets/I')
  t.Branch("nbtags",   ROOT.AddressOf(s,"nbtags"), 'nbtags/I')
  t.Branch("njetFailID",   ROOT.AddressOf(s,"njetFailID"), 'njetFailID/I')
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
    if not isData:
      t.Branch("ngp",   ROOT.AddressOf(s,"ngp"), 'ngp/I')
      for var in mcvars:
        t.Branch(var,   ROOT.AddressOf(s,var), var+'[ngp]/F')

  for bin_ in sample["bins"]:
    commoncf = ""
    if options.chmode[:4]=="copy":
      commoncf = "type1phiMet>150"
    if type(bin_) == type([]):
      bin = bin_[0]
    else:
      bin=bin_
    c = ROOT.TChain(sample["Chain"])
    for thisfile in sample["filenames"][bin]:
      prefix = ""
      if thisfile[0:5] == "/dpm/":
#        prefix = "rfio:"
        prefix = "root://hephyse.oeaw.ac.at/"#+subdirname
      c.Add(prefix+thisfile)
    ntot = c.GetEntries()
    if not isData:
      mclist = []
      for thisfile in sample["filenames"][bin]:
        mclist.append(prefix+thisfile)
      events = Events(mclist)
      handle = Handle("vector<reco::GenParticle>")
      events.toBegin()
      label = ("genParticles")
    if sample.has_key("additionalCut"):
      if type(sample["additionalCut"])==type({}):
        if sample["additionalCut"].has_key(bin):
          commoncf = commoncf+"&&"+sample["additionalCut"][bin]
      else:
        commoncf = commoncf+"&&"+sample["additionalCut"]
    if sample['newMETCollection']:
      commoncf = commoncf.replace('type1phiMet', 'met')
    if ntot>0:
      c.Draw(">>eList", commoncf)
      elist = ROOT.gDirectory.Get("eList")
      number_events = elist.GetN()
      if options.small:
        if number_events>1001:
          number_events=1001
      start = int(options.fromPercentage/100.*number_events)
      stop  = int(options.toPercentage/100.*number_events)
      print "Reading: ", sample["name"], bin, "with",number_events,"Events using cut", commoncf
      print "Reading percentage ",options.fromPercentage, "to",options.toPercentage, "which is range",start,"to",stop,"of",number_events
      for i in range(start, stop):
        if (i%10000 == 0) and i>0 :
          print i
  #      # Update all the Tuples
        if elist.GetN()>0 and ntot>0:
          c.GetEntry(elist.GetEntry(i))
# MC specific part
          if not isData:
            events.to(elist.GetEntry(i))
            events.getByLabel(label,handle)
            gps = handle.product()
            if storeVectors: 
              lgp = []
              lgp2 = []
              tops = []
              igp = 0
              for gp in gps:
                if abs(gp.pdgId()) == 6:
                  tops.append(gp)
                if gp.status() == 3:
                  lgp.append(gp)
#                elif (abs(gp.pdgId())==11 or abs(gp.pdgId())==13) and gp.pt() > 3.:
                elif (abs(gp.pdgId())==11 or abs(gp.pdgId())==13 or abs(gp.pdgId())==15) and gp.pt() > 3.:
                  lgp2.append(gp)
              lgp2 = sorted(lgp2, key=lambda k: -k.pt())
              s.ngp = min(len(lgp)+len(lgp2),40)
              for igp,gp in enumerate(lgp):
                s.gpPdg[igp] = gp.pdgId()
                s.gpM[igp] = gp.mass()
                s.gpPt[igp] = gp.pt()
                s.gpEta[igp] = gp.eta()
                s.gpPhi[igp] = gp.phi()
                s.gpMo1[igp] = find(gp.mother(0),lgp)
                s.gpMo2[igp] = find(gp.mother(min(gp.numberOfMothers(),1)),lgp)
                s.gpDa1[igp] = find(gp.daughter(0),lgp)
                s.gpDa2[igp] = find(gp.daughter(min(gp.numberOfDaughters(),1)),lgp)
                s.gpSta[igp] = gp.status()
              for igp2,gp2 in enumerate(lgp2,igp+1):
                if igp2 == 40:
                  break
                gpm = findSec(gp2,gps)
                s.gpPdg[igp2] = gp2.pdgId()
                s.gpM[igp2] = gp2.mass()
                s.gpPt[igp2] = gp2.pt()
                s.gpEta[igp2] = gp2.eta()
                s.gpPhi[igp2] = gp2.phi()
                s.gpMo1[igp2] = find(gpm,lgp)
                s.gpMo2[igp2] = -2
                s.gpDa1[igp2] = -1
                s.gpDa2[igp2] = -1
                s.gpSta[igp2] = gp2.status()
###################
          s.weight = sample["weight"][bin]
          for var in variables[1:]:
            getVar = var
            exec("s."+var+"="+str(getVarValue(c, getVar)).replace("nan","float('nan')"))
#          if options.allsamples.lower()=='sms':
#            for var in ['osetMgl', 'osetMN', 'osetMC', 'osetMsq']:
#              print s.event, var, getVarValue(c, var)
          s.event = long(c.GetLeaf(c.GetAlias('event')).GetValue())
          if not isData:
            vtxWeightSysPlus, nvtxWeightSysMinus, nvtxWeight = 1.,1.,1.
            if sample.has_key('reweightingHistoFile'): 
              s.puWeight = s.weight*sample['reweightingHistoFile'].GetBinContent(sample['reweightingHistoFile'].FindBin(s.nTrueGenVertices))
            if sample.has_key('reweightingHistoFileSysPlus'): 
              s.puWeightSysPlus = s.weight*sample['reweightingHistoFileSysPlus'].GetBinContent(sample['reweightingHistoFileSysPlus'].FindBin(s.nTrueGenVertices))
            if sample.has_key('reweightingHistoFileSysMinus'): 
              s.puWeightSysMinus = s.weight*sample['reweightingHistoFileSysMinus'].GetBinContent(sample['reweightingHistoFileSysMinus'].FindBin(s.nTrueGenVertices))

          for var in extraVariables:
            exec("s."+var+"=float('nan')")
          if sample['newMETCollection']:
            s.type1phiMet=s.met
            s.type1phiMetphi=s.metphi

          if storeVectors and sample['name'].lower().count('ttjets') and len(tops)==2: #https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
            s.top0Pt = tops[0].pt()
            s.top1Pt = tops[1].pt()
            s.topPtWeight = sqrt(exp( 0.156 - 0.00137*tops[0].pt())*exp( 0.156 - 0.00137*tops[1].pt()))
          nmuons = getVarValue(c, 'nmuons')   #Number of muons in Muon Vec
          neles  = getVarValue(c, 'neles')    #Number of eles in Ele Vec
          ntaus  = getVarValue(c, 'ntaus')    #Number of eles in Ele Vec
          if not isData:
            s.ptISR = getPtISR(s)
          allGoodMuons = getAllMuons(c,nmuons)
          allGoodElectrons = getAllElectrons(c, neles)
          allGoodTaus = getAllTaus(c, ntaus)
          tightMuons = filter(lambda m: tightMuID(m), allGoodMuons)
          tightElectrons = filter(lambda m: tightEleID(m), allGoodElectrons)

          s.nTightMuons = len(tightMuons)
          s.nTightElectrons = len(tightElectrons)


          allTightLeptons = tightMuons + tightElectrons 
          allTightLeptons = sorted(allTightLeptons, key=lambda k: -k['pt'])
          if isData:
            if len(allTightLeptons)==0:continue
            if abs(allTightLeptons[0]['Pdg'])==11 and bin.count('MuHad'):continue 
            if abs(allTightLeptons[0]['Pdg'])==13 and bin.count('ElectronHad'):continue 
      

          jResult = getGoodJets(c, allTightLeptons , jermode=options.jermode, jesmode=options.jesmode)
          jetResult = jResult['jets']

          if len(allTightLeptons)>0:
            s.leptonPt = allTightLeptons[0]['pt']
            s.leptonEta = allTightLeptons[0]['eta']
            s.leptonPhi = allTightLeptons[0]['phi']
            s.leptonPdg = allTightLeptons[0]['Pdg']
            s.mT = sqrt(2.*s.type1phiMet*s.leptonPt*(1. - cos(s.leptonPhi - s.type1phiMetphi))) 
            s.WPt = sqrt((s.leptonPt*cos(s.leptonPhi) + s.type1phiMet*cos(s.type1phiMetphi))**2 + (s.leptonPt*sin(s.leptonPhi) + s.type1phiMet*sin(s.type1phiMetphi))**2)
            s.WPhi = atan2(s.type1phiMet*sin(s.type1phiMetphi) + s.leptonPt*sin(s.leptonPhi), s.type1phiMet*cos(s.type1phiMetphi) + s.leptonPt*cos(s.leptonPhi))
            s.cosDeltaPhi = ((s.leptonPt*cos(s.leptonPhi) + s.type1phiMet*cos(s.type1phiMetphi))*cos(s.leptonPhi) + (s.leptonPt*sin(s.leptonPhi) + s.type1phiMet*sin(s.type1phiMetphi))*sin(s.leptonPhi) )/s.WPt
          if len(allTightLeptons)>1:
            s.lepton2Pt = allTightLeptons[1]['pt']
            s.lepton2Eta = allTightLeptons[1]['eta']
            s.lepton2Phi = allTightLeptons[1]['phi']
            s.lepton2Pdg = allTightLeptons[1]['Pdg']

          met_dx = jResult['met_dx']
          met_dy = jResult['met_dy']
          corrMetx = s.type1phiMet*cos(s.type1phiMetphi) + met_dx
          corrMety = s.type1phiMet*sin(s.type1phiMetphi) + met_dy
          s.type1phiMet     = sqrt(corrMetx**2+corrMety**2)
          s.type1phiMetphi  = atan2(corrMety, corrMetx)

          jets = filter(lambda j:j['id'] and j['isolated'], jetResult)
          s.ht = sum([ j['pt'] for j in jets])
          s.njets    = len(jets)
          lightJets, bJets = splitListOfObjects('btag', 0.679, jets) 
          s.nbtags  = len(filter(lambda j:j['btag']>0.679, jets))
          s.njetFailID = len(filter(lambda j:not j['id'] and j['isolated'], jetResult))
          
          s.nmu = len(allGoodMuons)
          s.nel = len(allGoodElectrons)
          s.nta = len(allGoodTaus)
          if storeVectors:
            s.njetCount = min(10,s.njets)
            for i in xrange(s.njetCount):
              s.jetPt[i]    = jets[i]['pt']
              s.jetUnc[i]   = jets[i]['unc']
              s.jetEta[i]   = jets[i]['eta']
              s.jetPhi[i]   = jets[i]['phi']
              s.jetPdg[i]   = jets[i]['Pdg']
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
              s.elPdg[i] = allGoodElectrons[i]['Pdg']
              s.elSIEtaIEta[i] = allGoodElectrons[i]['sIEtaIEta']
              s.elDPhi[i] = allGoodElectrons[i]['DPhi']
              s.elDEta[i] = allGoodElectrons[i]['DEta']
              s.elHoE[i] = allGoodElectrons[i]['HoE']
              s.elOneOverEMinusOneOverP[i] = allGoodElectrons[i]['OneOverEMinusOneOverP']
              s.elConvRejection[i] = allGoodElectrons[i]['ConvRejection']
              s.elMissingHits[i] = allGoodElectrons[i]['MissingHits']
              s.elIsEB[i] = allGoodElectrons[i]['isEB']
              s.elIsEE[i] = allGoodElectrons[i]['isEE']
              s.elRelIso[i] = allGoodElectrons[i]['relIso']
              s.elDxy[i] = allGoodElectrons[i]['Dxy']
              s.elDz[i] = allGoodElectrons[i]['Dz']
#              print "Electron pt's:",i,allGoodElectrons[i]['pt']
            s.ntaCount = min(10,s.nta)
            for i in xrange(s.ntaCount):
              s.taPt[i] = allGoodTaus[i]['pt']
              s.taEta[i] = allGoodTaus[i]['eta']
              s.taPhi[i] = allGoodTaus[i]['phi']
              s.taPdg[i] = allGoodTaus[i]['Pdg']
          if len(jets)>1:
            s3D = eventShape.sphericity(jets)
            c3D = eventShape.circularity(s3D["ev"])
            linC3D = eventShape.circularity(s3D["linEv"])
            c2D = eventShape.circularity2D(jets)
            foxwolfram = eventShape.foxWolframMoments(jets)
            s.S3D= s3D['sphericity']
            s.linS3D= s3D['linSphericity']
            s.C3D= c3D
            s.linC3D= linC3D
            s.C2D= c2D["c2D"]
            s.linC2D= c2D["linC2D"]
            s.FWMT1= foxwolfram["FWMT1"]
            s.FWMT2= foxwolfram["FWMT2"]
            s.FWMT3= foxwolfram["FWMT3"]
            s.FWMT4= foxwolfram["FWMT4"]
            if s.leptonPt>0:
              metObj = {"pt":s.type1phiMet, "phi":s.type1phiMetphi}
              lepObj = {"pt":s.leptonPt, "phi":s.leptonPhi}
              c2DLepMET = eventShape.circularity2D(jets+[lepObj]+[metObj])
              foxwolfram = eventShape.foxWolframMoments(jets+[lepObj]+[metObj])
              s.c2DLepMET   =  c2DLepMET['c2D']
              s.linC2DLepMET=  c2DLepMET['linC2D']
              s.FWMT1LepMET = foxwolfram["FWMT1"]
              s.FWMT2LepMET = foxwolfram["FWMT2"]
              s.FWMT3LepMET = foxwolfram["FWMT3"]
              s.FWMT4LepMET = foxwolfram["FWMT4"]
          if s.leptonPt>0:
            px = [cos(s.leptonPhi)*s.leptonPt] + [s.type1phiMet*cos(s.type1phiMetphi)] + [cos(j['phi'])*j['pt'] for j in jets]
            py = [sin(s.leptonPhi)*s.leptonPt] + [s.type1phiMet*sin(s.type1phiMetphi)] + [sin(j['phi'])*j['pt'] for j in jets]
            thrust = ROOT.Thrust(2+len(jets), array.array('d', px), array.array('d', py))
            s.thrust = thrust.thrust()
            s.thrustPhi = thrust.thrustPhi()
            s.thrustEta = thrust.thrustEta()
            if s.thrustEta>0.1:
                print "transversal thrust.eta() not zero?", thrust.thrust(), s.njets, s.thrustPhi, s.thrustEta
            if cos(s.type1phiMetphi - s.thrustPhi)>0:
              sign = 1
            else:
              sign=-1
            htThrustMetSide = 0.
            for j in jets:
              if sign*cos(s.thrustPhi - j['phi'])>0:
                htThrustMetSide+=j['pt']
            s.htThrustMetSideRatio = htFractionThrustSide(s.type1phiMetphi, s.thrustPhi, jets)
            s.htThrustLepSideRatio = htFractionThrustSide(s.leptonPhi, s.thrustPhi, jets)
            s.htThrustWSideRatio    = htFractionThrustSide(s.WPhi, s.thrustPhi, jets)

            if len(jets)>=3 or len(bJets)>=2:
              s.mt2w = mt2w.mt2w(met = {'pt':s.type1phiMet, 'phi':s.type1phiMetphi}, l={'pt':s.leptonPt, 'phi':s.leptonPhi, 'eta':s.leptonEta}, ljets=lightJets, bjets=bJets)
              if not s.mt2w<float('inf') and len(jets)>0 and len(allTightLeptons)>0:
                print "Warning -> Why can't I compute mt2w?", s.mt2w, len(jets), len(bJets), len(allTightLeptons),lightJets,bJets, {'pt':s.type1phiMet, 'phi':s.type1phiMetphi}, {'pt':s.leptonPt, 'phi':s.leptonPhi, 'eta':s.leptonEta}

          tmpDir = ROOT.gDirectory.func()
          chain_gDir.cd()
          t.Fill()
          tmpDir.cd()
#          if s.type1phiMet<150:
#            print "Warning", s.type1phiMet
#          else:
#            print "OK",s.type1phiMet
      del elist
    else:
      print "Zero entries in", bin, sample["name"]
    del c
  if True or not options.small: #FIXME
    f = ROOT.TFile(ofile, "recreate")
    t.Write()
    f.Close()
    print "Written",ofile
  else:
    print "No saving when small!"
  del t
