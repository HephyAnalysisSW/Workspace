import ROOT 
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy, random, array
from datetime import datetime
from Workspace.HEPHYPythonTools.helpers import getVarValue, deltaPhi, minAbsDeltaPhi,  deltaR, invMass, findClosestJet
from defaultSamples import *

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/Thrust.C+")

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--chmode", dest="chmode", default="inc", type="string", action="store", help="chmode: What to do.")
parser.add_option("--samples", dest="allsamples", default="dy53X", type="string", action="store", help="samples:Which samples.")
parser.add_option("--fileNumbers", dest="fileNumbers", default="", type="string", action="store", help="which file numbers? parse e.g. 7,1,11 -> histo_X where X in 1,7,11")
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")
parser.add_option("--fromPercentage", dest="fromPercentage", default="0", type="int", action="store", help="from (% of tot. events)")
parser.add_option("--toPercentage", dest="toPercentage", default="100", type="int", action="store", help="to (% of tot. events)")


(options, args) = parser.parse_args()
print "options: chmode",options.chmode
exec("allSamples = [" +options.allsamples+ "]")

from Workspace.HEPHYPythonTools.xsec import xsec

subDir = "convertedMETTuples_v2"

overwrite = True
target_lumi = 19700 #pb-1

from localInfo import username
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
  
def getGoodJets(c, crosscleanobjects=[]):
  nSoftJets = getVarValue(c, 'nsoftjets')   # jet.pt() > 10.
  res = []
  bres = []
  ht = 0.
  nbtags = 0
  for i in range(int(nSoftJets)):
    eta = getVarValue(c, 'jetsEta', i)
    pt  = getVarValue(c, 'jetsPt', i)
    if abs(eta) <= 4.5:
      unc = getVarValue(c, 'jetsUnc', i)
      id =  getVarValue(c, 'jetsID', i)
      phi = getVarValue(c, 'jetsPhi', i)
  #      if max([jet['muef'],jet['elef']]) > 0.6 : print jet
      if pt>30:
        parton = int(abs(getVarValue(c, 'jetsParton', i)))
        jet = {'pt':pt, 'eta':eta,'phi':phi, 'Pdg':parton,\
        'id':id,
        'chef':getVarValue(c, 'jetsChargedHadronEnergyFraction', i), 'nhef':getVarValue(c, 'jetsNeutralHadronEnergyFraction', i),\
        'ceef':getVarValue(c, 'jetsChargedEmEnergyFraction', i), 'neef':getVarValue(c, 'jetsNeutralEmEnergyFraction', i), 'id':id,\
        'hfhef':getVarValue(c, 'jetsHFHadronEnergyFraction', i), 'hfeef':getVarValue(c, 'jetsHFEMEnergyFraction', i),\
        'muef':getVarValue(c, 'jetsMuonEnergyFraction', i), 'elef':getVarValue(c, 'jetsElectronEnergyFraction', i), 'phef':getVarValue(c, 'jetsPhotonEnergyFraction', i),\
#        'jetCutBasedPUJetIDFlag':getVarValue(c, 'jetsCutBasedPUJetIDFlag', i),'jetMET53XPUJetIDFlag':getVarValue(c, 'jetsMET53XPUJetIDFlag', i),'jetFull53XPUJetIDFlag':getVarValue(c, 'jetsFull53XPUJetIDFlag', i), 
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
  return {'jets':res}#,'met_dx':met_dx, 'met_dy':met_dy}


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
      if options.fileNumbers!="":
        exec("fileNumbers = ["+options.fileNumbers+"]")
        newList = []
        for f in filelist:
          for n in fileNumbers:
            if f.count('histo_'+str(n)+'_'):
              newList.append(f)
              break
        filelist = newList
        print "Doing only", newList
      if options.small: filelist = filelist[:10]
      for tfile in filelist:
          sample['filenames'][bin].append(subdirname+tfile)
    d = ROOT.TChain('Runs')
    for tfile in sample['filenames'][bin]:
      print "Adding",tfile
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
if not os.path.isdir(outputDir+"/"+outSubDir):
  os.system("mkdir "+outputDir+"/"+outSubDir)

nc = 0
for isample, sample in enumerate(allSamples):
  if not os.path.isdir(outputDir+"/"+outSubDir+"/"+sample["name"]):
    os.system("mkdir "+outputDir+"/"+outSubDir+"/"+sample["name"])
  else:
    print "Directory", outputDir+"/"+outSubDir, "already found"

  variables = ["weight", "run", "lumi", "ngoodVertices", 'patPFMet', 'patPFMetphi', 'patPFMetsumEt', 'patMETs', 'patMETsphi', 'patMETssumEt']
  if sample['name'].lower().count('run'):
    alltriggers =  [ "HLTL1ETM40", "HLTMET120", "HLTMET120HBHENoiseCleaned", "HLTMonoCentralPFJet80PFMETnoMu105NHEF0p95", "HLTMonoCentralPFJet80PFMETnoMu95NHEF0p95"]
    for trigger in alltriggers:
      variables.append(trigger)
      variables.append(trigger.replace("HLT", "pre") )
  else:
    variables.extend(["nTrueGenVertices", "genmet", "genmetphi", "puWeight", "puWeightSysPlus", "puWeightSysMinus"])
  candvars = ['candPt', 'candPhi', 'candEta', 'candE']
  jetvars = ["jetPt", "jetEta", "jetPhi", "jetPdg", "jetBtag", "jetChef", "jetNhef", "jetCeef", "jetNeef", "jetHFhef", "jetHFeef", "jetMuef", "jetElef", "jetPhef", "jetUnc"]
  muvars = ["muPt", "muEta", "muPhi", "muPdg", "muRelIso", "muDxy", "muDz", "muNormChi2", "muNValMuonHits", "muNumMatchedStations", "muPixelHits", "muNumtrackerLayerWithMeasurement", 'muIsGlobal', 'muIsTracker']
  elvars = ["elPt", "elEta", "elPhi", "elPdg","elSIEtaIEta", "elDPhi", "elDEta", "elHoE", "elOneOverEMinusOneOverP", "elConvRejection", "elMissingHits", "elIsEB", "elIsEE", "elRelIso", "elDxy", "elDz"]
  tavars = ["taPt", "taEta", "taPhi", "taPdg"]
  if not sample['name'].lower().count('run'):
    mcvars = ["gpPdg", "gpM", "gpPt", "gpEta", "gpPhi", "gpMo1", "gpMo2", "gpDa1", "gpDa2", "gpSta"]
  if options.allsamples.lower()=='sms':
    variables+=['osetMgl', 'osetMN', 'osetMC', 'osetMsq']
  extraVariables=["ht","nTightMuons", "nTightElectrons"]

  structString = "struct MyStruct_"+str(nc)+"_"+str(isample)+"{ULong64_t event;"
  structString+="Float_t "+",".join(variables+extraVariables)+";"
  structString +="Int_t nmu, nel, nta, njets, nbtags, njetFailID;"
  structString +="Int_t njetCount, nmuCount, nelCount, ntaCount, nCand;"
  for var in jetvars:
    structString +="Float_t "+var+"[10];"
  for var in muvars:
    structString +="Float_t "+var+"[10];"
  for var in elvars:
    structString +="Float_t "+var+"[10];"
  for var in tavars:
    structString +="Float_t "+var+"[10];"
  structString +="Int_t candId[100000];"
  structString +="Int_t candCharge[100000];"
  for var in candvars:
    structString +="Float_t "+var+"[100000];"
  if not sample['name'].lower().count('run'):
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
  if options.fileNumbers!="":
    postfix+='_'+options.fileNumbers.replace(',','_')
  if options.small:
    postfix+="_small"
  if options.fromPercentage!=0 or options.toPercentage!=100:
    postfix += "_from"+str(options.fromPercentage)+"To"+str(options.toPercentage)
  ofile = outputDir+"/"+outSubDir+"/"+sample["name"]+"/histo_"+sample["name"]+postfix+".root"
  print "Writing to file",ofile
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
  t.Branch("njetCount",   ROOT.AddressOf(s,"njetCount"), 'njetCount/I')
  t.Branch("nelCount",   ROOT.AddressOf(s,"nelCount"), 'nelCount/I')
  t.Branch("nmuCount",   ROOT.AddressOf(s,"nmuCount"), 'nmuCount/I')
  t.Branch("ntaCount",   ROOT.AddressOf(s,"ntaCount"), 'ntaCount/I')
  t.Branch("nCand",   ROOT.AddressOf(s,"nCand"), 'nCand/I')
  for var in jetvars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[njetCount]/F')
  for var in muvars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[nmuCount]/F')
  for var in elvars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[nelCount]/F')
  for var in tavars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[ntaCount]/F')
  t.Branch("candId",   ROOT.AddressOf(s,'candId'), 'candId[nCand]/I')
  t.Branch("candCharge",   ROOT.AddressOf(s,'candCharge'), 'candCharge[nCand]/I')
  for var in candvars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[nCand]/F')
  if not sample['name'].lower().count('run'):
    t.Branch("ngp",   ROOT.AddressOf(s,"ngp"), 'ngp/I')
    for var in mcvars:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'[ngp]/F')

  for bin_ in sample["bins"]:
    commoncf = ""
    if options.chmode[:4]=="inc":
      commoncf = "(1)"
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
    mclist = []
    for thisfile in sample["filenames"][bin]:
      mclist.append(prefix+thisfile)
    events = Events(mclist)
    pfhandle = Handle("vector<reco::PFCandidate>")
    pflabel = ("particleFlow")
    if not sample['name'].lower().count('run'):
      gphandle = Handle("vector<reco::GenParticle>")
      gplabel = ("genParticles")
    events.toBegin()
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
          events.to(elist.GetEntry(i))
          events.getByLabel(pflabel,pfhandle)
          pfcands = pfhandle.product()
          count=0
          for cand in pfcands:
            p4 = cand.p4()
            s.candPt[count]=p4.pt()
            s.candEta[count]=p4.eta()
            s.candPhi[count]=p4.phi()
            s.candE[count]=p4.E()
            s.candId[count]=cand.particleId()
            s.candCharge[count]=cand.charge()
            count+=1
          s.nCand = count
          if not sample['name'].lower().count('run'):
            events.getByLabel(gplabel,gphandle)
            gps = gphandle.product()
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
          if not sample['name'].lower().count('run'):
            vtxWeightSysPlus, nvtxWeightSysMinus, nvtxWeight = 1.,1.,1.
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


          jResult = getGoodJets(c)
          jetResult = jResult['jets']

          jets = filter(lambda j:j['id'] and j['isolated'], jetResult)
          s.ht = sum([ j['pt'] for j in jets])
          s.njets    = len(jets)
          lightJets, bJets = splitListOfObjects('btag', 0.679, jets) 
          s.nbtags  = len(filter(lambda j:j['btag']>0.679, jets))
          s.njetFailID = len(filter(lambda j:not j['id'] and j['isolated'], jetResult))
          
          s.nmu = len(allGoodMuons)
          s.nel = len(allGoodElectrons)
          s.nta = len(allGoodTaus)
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
