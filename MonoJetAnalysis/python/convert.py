import ROOT 
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy, random
from datetime import datetime
from helpers import getVarValue, deltaPhi, minAbsDeltaPhi,  deltaR, invMass, findClosestJet
from defaultMETSamples_mc import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--chmode", dest="chmode", default="copy", type="string", action="store", help="chmode: What to do.")
parser.add_option("--jermode", dest="jermode", default="none", type="string", action="store", help="jermode: up/down/central/none")
parser.add_option("--jesmode", dest="jesmode", default="none", type="string", action="store", help="jesmode: up/down/none")
parser.add_option("--samples", dest="allsamples", default="copy", type="string", action="store", help="samples:Which samples.")
parser.add_option("--smsMsqRange", dest="smsMsqRangeString", default="None", type="string", action="store", help="What is the Msq range? Maximum is 100-425.")
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")
parser.add_option("--fromPercentage", dest="fromPercentage", default="0", type="int", action="store", help="from (% of tot. events)")
parser.add_option("--toPercentage", dest="toPercentage", default="100", type="int", action="store", help="to (% of tot. events)")

(options, args) = parser.parse_args()
print "options: chmode",options.chmode, "jermode",options.jermode, "jesmode",options.jesmode

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


path = os.path.abspath('../../HEPHYCommonTools/python')
if not path in sys.path:
    sys.path.insert(1, path)
del path
from helpers import getVarValue, deltaPhi, minAbsDeltaPhi, invMassOfLightObjects, deltaR, closestMuJetDeltaR
from monoJetFuncs import softIsolatedMT, pmuboost3d

from xsec import xsec

subDir = "monoJetTuples_v6"


if options.smsMsqRangeString!='None' and options.allsamples.lower()=='sms':
  from Workspace.HEPHYCommonTools.xsecSMS import stop8TeV_NLONLL
  allSamples=[]
  msqStart = int(options.smsMsqRangeString.split('-')[0])
  msqEnd = int(options.smsMsqRangeString.split('-')[1])
  msqVals = range(msqStart, msqEnd, 25)
  print "Converting Msq from",msqStart, 'to',msqEnd,'. Thats the following:',msqVals
  xsec = {}
  for msq in msqVals:

    b = None 
    if msq>=100 and msq<=150:
      b = "T2DegenerateStop_2J_mStop-100to150"
    if msq>=175 and msq<=225:
      b = "T2DegenerateStop_2J_mStop-175to225"
    if not b: 
      print "Don't know which bin on dpm for msq",msq
      continue

    for deltaM in range(0,110,10):
#    for deltaM in [100]:
      T2DegStop = {}  
      T2DegStop={}
      T2DegStop["dirname"] = "/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314/"
      T2DegStop['newMETCollection'] = True
      T2DegStop["Chain"] = "Events"
      name = "T2DegStop_"+str(msq)+"_"+str(msq-deltaM)
      T2DegStop["bins"] = [[name,[b]]]
      T2DegStop["name"] = name
      xsec[name] = stop8TeV_NLONLL[msq]
      T2DegStop["additionalCut"] = "osetMsq=="+str(msq)+"&&osetMC=="+str(msq-deltaM)
#      T2DegStop["additionalCut"] = "(1)"
      T2DegStop['reweightingHistoFile'] = S10rwHisto
      T2DegStop['reweightingHistoFileSysPlus'] = S10rwPlusHisto
      T2DegStop['reweightingHistoFileSysMinus'] = S10rwMinusHisto
      T2DegStop['reweightingHistoFile'] = S10rwHisto
      T2DegStop['reweightingHistoFileSysPlus'] = S10rwPlusHisto
      T2DegStop['reweightingHistoFileSysMinus'] = S10rwMinusHisto
      allSamples.append(T2DegStop)
      print "Added SMS",T2DegStop["name"]
else:
  exec("allSamples = [" +options.allsamples+ "]")

overwrite = False
target_lumi = 19700 #pb-1

from localInfo import username
outputDir = "/data/"+username+"/"+subDir+"/"

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

def getPtISR(e):
    sumtlv = ROOT.TLorentzVector(1.e-9,1.e-9,1.e-9,1.e-9)
    for igp in range(e.ngp):
        if(abs(e.gpPdg[igp])==1000006 and e.gpSta[igp]==3):
            tlvaux = ROOT.TLorentzVector(0.,0.,0.,0.)
            tlvaux.SetPtEtaPhiM(e.gpPt[igp],e.gpEta[igp],e.gpPhi[igp],e.gpM[igp])
            sumtlv += tlvaux
    return sumtlv.Pt()

def goodMuID(c, imu ):  
  isPF = getVarValue(c, 'muonsisPF', imu)
  isGlobal = getVarValue(c, 'muonsisGlobal', imu)
  isTracker = getVarValue(c, 'muonsisTracker', imu)
  pt = getVarValue(c, 'muonsPt', imu)
  dz = getVarValue(c, 'muonsDz', imu)
  eta=getVarValue(c, 'muonsEta', imu)
  if isPF and (isGlobal or isTracker) and pt>5. and abs(eta)<2.1 and abs(dz)<0.5:
    return {'pt':pt, 'phi':getVarValue(c, 'muonsPhi', imu), 'eta':eta, 'IsGlobal':isGlobal, 'IsTracker':isTracker, 'IsPF':isPF, 'relIso':getVarValue(c, 'muonsPFRelIso', imu), 'Dz':dz} 


# -------------------------------------------

def goodEleID_POG(c, iele, eta = 'none'): # POG Ele veto https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaCutBasedIdentification
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
    and ((isEB and dphi < 0.8) or (isEE and dphi < 0.7)) and ( (isEB and deta < 0.007) or (isEE and deta < 0.01) )\
    and ((isEB and sietaieta < 0.01 ) or (isEE and sietaieta < 0.03))\
    and ( isEB and HoE < 0.15 )\
    and getVarValue(c, 'elesDxy', iele) < 0.04 and getVarValue(c, 'elesDz', iele) < 0.2 \
    and ( relIso < relIsoCut ) \
    and getVarValue(c, 'elesPt', iele)>5.

  # -------------------------------------------

def goodTauID_POG(c, itau ): 
  return getVarValue(c, 'tausisPF', itau) and \
         getVarValue(c, 'tausDecayModeFinding', itau) and \
         getVarValue(c, 'tausAgainstMuonLoose', itau) and \
         getVarValue(c, 'tausAgainstElectronLoose', itau) and \
         getVarValue(c, 'tausByLooseCombinedIsolationDBSumPtCorr', itau) and \
         getVarValue(c, 'tausPt', itau)>5.

def getAllMuons(c, nmuons ):
  res=[]
  for i in range(0, int(nmuons)):
    cand = goodMuID(c, i)
    if cand:
      for v in ['Pdg', 'Dxy', 'NormChi2', 'NValMuonHits', 'NumMatchedStations', 'PixelHits', 'NumtrackerLayerWithMeasurement']:
        cand[v] = getVarValue(c, 'muons'+v, i)
      res.append(cand)
  res = sorted(res, key=lambda k: -k['pt'])
  return res

def getAllElectrons(c, neles ):
  res=[]
  for i in range(0, int(neles)):
    eta = getVarValue(c, 'elesEta', i)
    if goodEleID_POG(c, i, abs(eta)):
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
  
def getGoodJets(c, crosscleanobjects, jermode=options.jermode, jesmode=options.jesmode):
  njets = getVarValue(c, 'nsoftjets')   # jet.pt() > 10.
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
  for i in range(int(njets)):
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
      if pt>30:
        parton = int(abs(getVarValue(c, 'jetsParton', i)))
        jet = {'pt':pt, 'eta':eta,'phi':phi, 'pdg':parton,\
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

#if options.chmode == "incNoISRJetID":
#  def isrJetID(j):
#    return abs(j['eta']) < 2.4
#else:
def isrJetID(j):
  return j['id'] and j['chef'] > 0.2 and j['neef']<0.7 and j['nhef']<0.7 and j['ceef'] < 0.5 and abs(j['eta']) < 2.4

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
  if not os.path.isdir(outputDir+"/"+outSubDir+"/"+sample["name"]):
    os.system("mkdir "+outputDir+"/"+outSubDir+"/"+sample["name"])
  else:
    print "Directory", outputDir+"/"+outSubDir, "already found"

  variables = ["weight", "run", "lumi", "ngoodVertices"]
  if sample['newMETCollection']:
    variables+=["met", "metphi"]
  else:
    variables+=["type1phiMet", "type1phiMetphi"]
  if sample['name'].lower().count('data'):
    alltriggers =  [ "HLTL1ETM40", "HLTMET120", "HLTMET120HBHENoiseCleaned", "HLTMonoCentralPFJet80PFMETnoMu105NHEF0p95", "HLTMonoCentralPFJet80PFMETnoMu95NHEF0p95"]
    for trigger in alltriggers:
      variables.append(trigger)
      variables.append(trigger.replace("HLT", "pre") )
  else:
    variables.extend(["nTrueGenVertices", "genmet", "genmetphi", "puWeight", "puWeightSysPlus", "puWeightSysMinus", "ptISR"])
  
  jetvars = ["jetPt", "jetEta", "jetPhi", "jetPdg", "jetBtag", "jetCutBasedPUJetIDFlag","jetFull53XPUJetIDFlag","jetMET53XPUJetIDFlag", "jetChef", "jetNhef", "jetCeef", "jetNeef", "jetHFhef", "jetHFeef", "jetMuef", "jetElef", "jetPhef", "jetISRJetID", "jetUnc"]
  muvars = ["muPt", "muEta", "muPhi", "muPdg", "muRelIso", "muDxy", "muDz", "muNormChi2", "muNValMuonHits", "muNumMatchedStations", "muPixelHits", "muNumtrackerLayerWithMeasurement", 'muIsGlobal', 'muIsTracker']
  elvars = ["elPt", "elEta", "elPhi", "elPdg", "elRelIso", "elDxy", "elDz"]
  tavars = ["taPt", "taEta", "taPhi", "taPdg"]
  if not sample['name'].lower().count('data'):
    mcvars = ["gpPdg", "gpM", "gpPt", "gpEta", "gpPhi", "gpMo1", "gpMo2", "gpDa1", "gpDa2", "gpSta"]
  if options.allsamples.lower()=='sms':
    variables+=['osetMgl', 'osetMN', 'osetMC', 'osetMsq']
  extraVariables=["nbtags", "ht", "nSoftIsolatedMuons", "nHardMuons", "nHardMuonsRelIso02", "nSoftElectrons", "nHardElectrons", "nSoftTaus", "nHardTaus"]
  if sample['newMETCollection']:
    extraVariables+=["type1phiMet", "type1phiMetphi"]
  extraVariables += ["isrJetPt", "isrJetEta", "isrJetPhi", "isrJetPdg", "isrJetBtag", "isrJetChef", "isrJetNhef", "isrJetCeef", "isrJetNeef", "isrJetHFhef", "isrJetHFeef", "isrJetMuef", "isrJetElef", "isrJetPhef", "isrJetCutBasedPUJetIDFlag", "isrJetFull53XPUJetIDFlag", "isrJetMET53XPUJetIDFlag", "isrJetBTBVetoPassed", "isrJetUnc"]

  extraVariables += ["softIsolatedMuPt", "softIsolatedMuEta", "softIsolatedMuPhi", "softIsolatedMuPdg", "softIsolatedMuRelIso", "softIsolatedMuDxy", "softIsolatedMuDz",  'softIsolatedMuNormChi2', 'softIsolatedMuNValMuonHits', 'softIsolatedMuNumMatchedStations', 'softIsolatedMuPixelHits', 'softIsolatedMuNumtrackerLayerWithMeasurement', 'softIsolatedMuIsTracker', 'softIsolatedMuIsGlobal']
  extraVariables += ["softIsolatedMT", "closestMuJetDeltaR", "nHardbtags", "nSoftbtags"]
  if storeVectors: 
    extraVariables+=[ "softIsolatedpmuboost3d"]
    if sample['name'].lower().count('ttjets'):
      extraVariables+=["top0Pt", "top1Pt", "topPtWeight"] 
  structString = "struct MyStruct_"+str(nc)+"_"+str(isample)+"{ULong64_t event;"
  structString+="Float_t "+",".join(variables+extraVariables)+";"
#  for var in variables:
#    structString +="Float_t "+var+";"
#  for var in extraVariables:
#    structString +="Float_t "+var+";"
  structString +="Int_t nmu, nel, nta, njet, njet60, njet60FailID, njet30FailID, njet60FailISRJetID, njet30FailISRJetID;"
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
    if not sample['name'].lower().count('data'):
      structString +="Int_t ngp;"
      for var in mcvars:
        structString +="Float_t "+var+"[20];"
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
  t.Branch("njet",   ROOT.AddressOf(s,"njet"), 'njet/I')
  t.Branch("nmu",   ROOT.AddressOf(s,"nmu"), 'nmu/I')
  t.Branch("nel",   ROOT.AddressOf(s,"nel"), 'nel/I')
  t.Branch("nta",   ROOT.AddressOf(s,"nta"), 'nta/I')
  t.Branch("njet60",   ROOT.AddressOf(s,"njet60"), 'njet60/I')
  t.Branch("njet30FailID",   ROOT.AddressOf(s,"njet30FailID"), 'njet30FailID/I')
  t.Branch("njet30FailISRJetID",   ROOT.AddressOf(s,"njet30FailISRJetID"), 'njet30FailISRJetID/I')
  t.Branch("njet60FailID",   ROOT.AddressOf(s,"njet60FailID"), 'njet60FailID/I')
  t.Branch("njet60FailISRJetID",   ROOT.AddressOf(s,"njet60FailISRJetID"), 'njet60FailISRJetID/I')
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
    if not sample['name'].lower().count('data'):
      t.Branch("ngp",   ROOT.AddressOf(s,"ngp"), 'ngp/I')
      for var in mcvars:
        t.Branch(var,   ROOT.AddressOf(s,var), var+'[ngp]/F')

  for bin_ in sample["bins"]:
    commoncf = ""
    if options.chmode[:4]=="copy":
      commoncf = "type1phiMet>150"
    if options.chmode[:7] == "copyInc":
      commoncf = "(1)"
    if options.chmode[:7] == "copyMu":
      commoncf = "ngoodMuons==1"
    #  storeVectors = False
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
    if not sample['name'].lower().count('data'):
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
          if not sample['name'].lower().count('data'):
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
              s.ngp = min(len(lgp)+len(lgp2),20)
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
                if igp2 == 20:
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
          if options.allsamples.lower()=='sms':
            s.osetMN, s.osetMC = s.osetMC, s.osetMN# swap, because I misinterpreted the model string
            
#            for var in ['osetMgl', 'osetMN', 'osetMC', 'osetMsq']:
#              print s.event, var, getVarValue(c, var)
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
          if not sample['name'].lower().count('data'):
            s.ptISR = getPtISR(s)
          allGoodMuons = getAllMuons(c,nmuons)
          allGoodElectrons = getAllElectrons(c, neles)
          allGoodTaus = getAllTaus(c, ntaus)

          softMuons, hardMuons         = splitListOfObjects('pt', 20, allGoodMuons)
          softElectrons, hardElectrons = splitListOfObjects('pt', 20, allGoodElectrons)
          softTaus, hardTaus           = splitListOfObjects('pt', 20, allGoodTaus)
          
          hardMuonsRelIso02 = filter(lambda m:m['relIso']<0.2, hardMuons)
#            softMuons = sorted(softMuons, key=lambda k: -k['pt'])
#            s.nSoftMuons = len(softMuons)
          softIsolatedMuons = filter(lambda m:m['relIso']*m['pt']<10.0, softMuons)
          if options.chmode.lower().count('mudzid'):
            softIsolatedMuons = filter(lambda m:m['Dz']<0.2, softIsolatedMuons)

          s.nSoftIsolatedMuons = len(softIsolatedMuons)
          s.nHardMuons = len(hardMuons)
          s.nHardMuonsRelIso02 = len(hardMuonsRelIso02)
          s.nSoftElectrons = len(softElectrons)
          s.nHardElectrons = len(hardElectrons)
          s.nSoftTaus = len(softTaus)
          s.nHardTaus = len(hardTaus)

          if options.chmode.count("CleanedWithAllLeptons"):
            jResult = getGoodJets(c, allGoodMuons + allGoodElectrons, jermode=options.jermode, jesmode=options.jesmode)
          else:
            jResult = getGoodJets(c, hardMuonsRelIso02 + hardElectrons, jermode=options.jermode, jesmode=options.jesmode)
          jetResult = jResult['jets']
          met_dx = jResult['met_dx']
          met_dy = jResult['met_dy']
          corrMetx = s.type1phiMet*cos(s.type1phiMetphi) + met_dx
          corrMety = s.type1phiMet*sin(s.type1phiMetphi) + met_dy
          s.type1phiMet     = sqrt(corrMetx**2+corrMety**2)
          s.type1phiMetphi  = atan2(corrMety, corrMetx)

          idJets30 = filter(lambda j:j['id'] and j['isolated'], jetResult)
          for j in idJets30:
            j['isrJetID'] = isrJetID(j)
          idJets60 = filter(lambda j:j['id'] and j['isolated'] and j['pt']>60, jetResult)
          s.ht = sum([ j['pt'] for j in idJets30])
          s.njet    = len(idJets30)
          s.nbtags  = len(filter(lambda j:j['btag']>0.679, idJets30))
          s.nHardbtags  = len(filter(lambda j:j['pt']>=60 and j['btag']>0.679, idJets30))
          s.nSoftbtags  = len(filter(lambda j:j['pt']<60 and j['btag']>0.679, idJets30))
          s.njet60  = len(idJets60)
          s.njet60FailID = len(filter(lambda j:not j['id'] and j['isolated'], jetResult))
          s.njet30FailID = len(filter(lambda j:not j['id'] and j['isolated'] and j['pt']>60, jetResult))
          s.njet60FailISRJetID = len(filter(lambda j:not isrJetID(j) and j['isolated'], jetResult))
          s.njet30FailISRJetID = len(filter(lambda j:not isrJetID(j) and j['isolated'] and j['pt']>60, jetResult))
          if len( jetResult )>=1 and jetResult[0]['pt']>110 and isrJetID(jetResult[0]) and jetResult[0]['id'] and jetResult[0]['isolated']:
            leadingJet = jetResult[0]
            s.isrJetPt = leadingJet['pt']
            s.isrJetUnc = leadingJet['unc']
            s.isrJetEta = leadingJet['eta']
            s.isrJetPhi = leadingJet['phi']
            s.isrJetPdg = leadingJet['pdg']
            s.isrJetBtag = leadingJet['btag']
            s.isrJetChef = leadingJet['chef']
            s.isrJetNhef = leadingJet['nhef']
            s.isrJetCeef = leadingJet['ceef']
            s.isrJetNeef = leadingJet['neef']
            s.isrJetHFhef = leadingJet['hfhef']
            s.isrJetHFeef = leadingJet['hfeef']
            s.isrJetMuef = leadingJet['muef']
            s.isrJetElef = leadingJet['elef']
            s.isrJetPhef = leadingJet['phef']
            s.isrJetCutBasedPUJetIDFlag = leadingJet['jetCutBasedPUJetIDFlag']
            s.isrJetFull53XPUJetIDFlag = leadingJet['jetFull53XPUJetIDFlag']
            s.isrJetMET53XPUJetIDFlag = leadingJet['jetMET53XPUJetIDFlag']
            
            recoilJets = filter(lambda j:j['pt']>60 and j['id'] and j['isolated'] and deltaPhi(j['phi'], leadingJet['phi']) >=2.5, jetResult[1:])
            s.isrJetBTBVetoPassed = (len(recoilJets)==0)
          
          if len(softIsolatedMuons)>=1:
            s.softIsolatedMuPt                             = softIsolatedMuons[0]['pt']
            s.softIsolatedMuEta                            = softIsolatedMuons[0]['eta']
            s.softIsolatedMuPhi                            = softIsolatedMuons[0]['phi']
            s.softIsolatedMuPdg                            = softIsolatedMuons[0]['Pdg']
            s.softIsolatedMuRelIso                         = softIsolatedMuons[0]['relIso']
            s.softIsolatedMuDxy                            = softIsolatedMuons[0]['Dxy']
            s.softIsolatedMuDz                             = softIsolatedMuons[0]['Dz']
            s.softIsolatedMuNormChi2                       = softIsolatedMuons[0]['NormChi2']
            s.softIsolatedMuNValMuonHits                   = softIsolatedMuons[0]['NValMuonHits']
            s.softIsolatedMuNumMatchedStations             = softIsolatedMuons[0]['NumMatchedStations']
            s.softIsolatedMuPixelHits                      = softIsolatedMuons[0]['PixelHits']
            s.softIsolatedMuNumtrackerLayerWithMeasurement = softIsolatedMuons[0]['NumtrackerLayerWithMeasurement']
            s.softIsolatedMuIsGlobal                       = softIsolatedMuons[0]['IsGlobal']
            s.softIsolatedMuIsTracker                      = softIsolatedMuons[0]['IsTracker']
          if len(softIsolatedMuons)>=1:
            s.softIsolatedMT                               = sqrt(2.0*s.softIsolatedMuPt*s.type1phiMet*(1-cos(s.softIsolatedMuPhi - s.type1phiMetphi)))
            if len(idJets30)>0:
              cjet = findClosestJet(idJets30, {'phi':softIsolatedMuons[0]['phi'], 'eta':softIsolatedMuons[0]['eta']})
              s.closestMuJetDeltaR = cjet['deltaR']
              s.closestMuJetMass = invMass(cjet['jet'], {'phi':softIsolatedMuons[0]['phi'], 'pt':softIsolatedMuons[0]['pt'], 'eta':softIsolatedMuons[0]['eta']})
            s.softIsolatedpmuboost3d = pmuboost3d(idJets30, {'pt':s.type1phiMet, 'phi':s.type1phiMetphi}, {'phi':softIsolatedMuons[0]['phi'], 'pt':softIsolatedMuons[0]['pt'], 'eta':softIsolatedMuons[0]['eta']} )
             

          s.nmu = len(allGoodMuons)
          s.nel = len(allGoodElectrons)
          s.nta = len(allGoodTaus)
          if storeVectors:
            s.njetCount = min(10,s.njet)
            for i in xrange(s.njetCount):
              s.jetPt[i]    = idJets30[i]['pt']
              s.jetUnc[i]   = idJets30[i]['unc']
              s.jetEta[i]   = idJets30[i]['eta']
              s.jetPhi[i]   = idJets30[i]['phi']
              s.jetPdg[i]   = idJets30[i]['pdg']
              s.jetBtag[i]  = idJets30[i]['btag']
              s.jetChef[i]  = idJets30[i]['chef']
              s.jetNhef[i]  = idJets30[i]['nhef']
              s.jetCeef[i]  = idJets30[i]['ceef']
              s.jetNeef[i]  = idJets30[i]['neef']
              s.jetHFhef[i] = idJets30[i]['hfhef']
              s.jetHFeef[i] = idJets30[i]['hfeef']
              s.jetMuef[i]  = idJets30[i]['muef']
              s.jetElef[i]  = idJets30[i]['elef']
              s.jetPhef[i]  = idJets30[i]['phef']
              s.jetCutBasedPUJetIDFlag[i] = idJets30[i]['jetCutBasedPUJetIDFlag']
              s.jetFull53XPUJetIDFlag[i]  = idJets30[i]['jetFull53XPUJetIDFlag']
              s.jetMET53XPUJetIDFlag[i]   = idJets30[i]['jetMET53XPUJetIDFlag']
              s.jetISRJetID[i] = idJets30[i]['isrJetID']

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
#          print s.type1phiMet
          if s.type1phiMet<150:
            print "Warning!!"
          else:
            print "OK"
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
