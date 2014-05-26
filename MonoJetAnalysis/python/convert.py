import ROOT 
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy, random
from datetime import datetime
#from helpers import getVarValue, deltaPhi, minAbsDeltaPhi,  deltaR, invMass,
from Workspace.HEPHYPythonTools.helpers import getVarValue, deltaPhi, minAbsDeltaPhi, invMassOfLightObjects, deltaR, closestMuJetDeltaR, invMass,  findClosestJet
from monoJetFuncs import softIsolatedMT, pmuboost3d

from Workspace.HEPHYPythonTools.btagEff import getMCEff, getTagWeightDict, getSF, partonName 
maxConsideredBTagWeight = 3 

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

sigmaMCDict =\
 {0:{'N':-0.34921, 'S':  0.29783, 'C':  0., 'm':  0.47112},
  1:{'N':-0.49974, 'S':  0.33639, 'C':  0., 'm':  0.43069},
  2:{'N':-0.56165, 'S':  0.42029, 'C':  0., 'm':  0.3924 },
  3:{'N':-1.12329, 'S':  0.65789, 'C':  0., 'm':  0.1396 },
  4:{'N': 1.04792, 'S':  0.46676, 'C':  0., 'm':  0.19314},
  5:{'N': 1.89961, 'S':  0.33432, 'C':  0., 'm':  0.36541},
  6:{'N': 1.66267, 'S':  0.3778 , 'C':  0., 'm':  0.43943},
  7:{'N': 1.50961, 'S':  0.22757, 'C':  0., 'm':  0.60094},
  8:{'N': 0.99052, 'S':  0.27026, 'C':  0., 'm':  0.46273},
  9:{'N': 1.37916, 'S':  0.28933, 'C':  0., 'm':  0.6123 }
  }
def sigmaMCParams(aeta):
  aeta=abs(aeta)
  return sigmaMCDict[min([int(aeta/0.5),9])]

def jerSigmaMCRel(pt, eta):
  p = sigmaMCParams(abs(eta))
  return sqrt(p['N']*abs(p['N'])/pt**2 + p['S']**2*pt**(p['m']-1) + p['C']**2)

from Workspace.HEPHYPythonTools.xsec import xsec

subDir = "monoJetTuples_v7"


if options.smsMsqRangeString!='None' and options.allsamples.lower()=='sms':
  from Workspace.HEPHYPythonTools.xsecSMS import stop8TeV_NLONLL
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
    if msq>=250 and msq<=300:
      b = "T2DegenerateStop_2J_mStop-250to300-4"
    if msq>=325 and msq<=375:
      b = "T2DegenerateStop_2J_mStop-325to375"
    if msq>=400:
      b = "T2DegenerateStop_2J_mStop-400-2"

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
      T2DegStop['isFastSim'] = True
      allSamples.append(T2DegStop)
      print "Added SMS",T2DegStop["name"]
else:
  exec("allSamples = [" +options.allsamples+ "]")

overwrite = True
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
    and abs(getVarValue(c, 'elesDxy', iele)) < 0.04 and abs(getVarValue(c, 'elesDz', iele)) < 0.2 \
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

def hybridIso(m, wp):
  if wp=='loose':
    return  (m['pt']<25 and m['relIso']*m['pt']<10) or (m['pt']>=25 and m['relIso']<0.4)
  if wp=='medium':
    return  (m['pt']<25 and m['relIso']*m['pt']<5) or (m['pt']>=25 and m['relIso']<0.2)
  if wp=='tight':
    return  (m['pt']<25 and m['relIso']*m['pt']<3) or (m['pt']>=25 and m['relIso']<0.12)

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
    unc = getVarValue(c, 'jetsUnc', i)
    id =  getVarValue(c, 'jetsID', i)
    phi = getVarValue(c, 'jetsPhi', i)
#      if max([jet['muef'],jet['elef']]) > 0.6 : print jet
    if jermode.lower()!="none":
      c_jet = jerDifferenceScaleFactor(eta, jermode)
      sigmaMCRel = jerSigmaMCRel(pt, eta)
      sigma = sqrt(c_jet**2 - 1)*sigmaMCRel
      scale = random.gauss(1,sigma)
      met_dx+=(1-scale)*cos(phi)*pt
      met_dy+=(1-scale)*sin(phi)*pt
      pt*=scale
    if jesmode.lower()!="none":
      scale = 1. + sign*unc
      met_dx+=(1-scale)*cos(phi)*pt
      met_dy+=(1-scale)*sin(phi)*pt
      pt*=scale
    if pt>30 and abs(eta)<4.5:
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

def getMCEfficiencyForBTagSF(jets, isFastSim=False):
  for jet in jets:
    r = getMCEff(parton=jet['pdg'], pt=jet['pt'], eta=jet['eta'], year=2012)#getEfficiencyAndMistagRate(jPt, jEta, jParton )
    jet['effData']=r
#    print [j[0] for j in jets]
  mceffs = tuple()
  mceffs_SF = tuple()
  mceffs_SF_b_Up = tuple()
  mceffs_SF_b_Down = tuple()
  mceffs_SF_light_Up = tuple()
  mceffs_SF_light_Down = tuple()
  for jet in jets:
    if isFastSim:
      fsim_SF =       ROOT.getFastSimCorr(partonName(abs(jet['pdg'])),jet['pt'],"mean",jet['eta'])
      fsim_SF_up =    ROOT.getFastSimCorr(partonName(abs(jet['pdg'])),jet['pt'],"up",  jet['eta'])
      fsim_SF_down =  ROOT.getFastSimCorr(partonName(abs(jet['pdg'])),jet['pt'],"down",jet['eta'])
    else:
      fsim_SF = 1.
      fsim_SF_up = 1.
      fsim_SF_down = 1.
    mceffs += (jet['effData']["mcEff"],)
    mceffs_SF += (jet['effData']["mcEff"]*jet['effData']["SF"]*fsim_SF,)
    if abs(jet['pdg'])==5 or abs(jet['pdg'])==4:
      mceffs_SF_b_Up   += (jet['effData']["mcEff"]*jet['effData']["SF_up"]*fsim_SF_up,)
      mceffs_SF_b_Down += (jet['effData']["mcEff"]*jet['effData']["SF_down"]*fsim_SF_down,)
      mceffs_SF_light_Up   += (jet['effData']["mcEff"]*jet['effData']["SF"],)
      mceffs_SF_light_Down += (jet['effData']["mcEff"]*jet['effData']["SF"],)
    else:
      mceffs_SF_b_Up   += (jet['effData']["mcEff"]*jet['effData']["SF"],)
      mceffs_SF_b_Down += (jet['effData']["mcEff"]*jet['effData']["SF"],)
      mceffs_SF_light_Up   += (jet['effData']["mcEff"]*jet['effData']["SF_up"]*fsim_SF_up,)
      mceffs_SF_light_Down += (jet['effData']["mcEff"]*jet['effData']["SF_down"]*fsim_SF_down,)

  return {"mceffs":mceffs, "mceffs_SF":mceffs_SF, "mceffs_SF_b_Up":mceffs_SF_b_Up, "mceffs_SF_b_Down":mceffs_SF_b_Down, "mceffs_SF_light_Up":mceffs_SF_light_Up, "mceffs_SF_light_Down":mceffs_SF_light_Down}



#if options.chmode == "incNoISRJetID":
#  def isrJetID(j):
#    return abs(j['eta']) < 2.4
#else:
def isrJetID(j):
  return j['id'] and j['chef'] > 0.2 and j['neef']<0.7 and j['nhef']<0.7 and j['ceef'] < 0.5 and abs(j['eta']) < 2.4

# helpers for GenParticle searching and matching
def find(x,lp):
  if x in lp:
    return lp.index(x)
  else:
    return -1

def findSec1(gp):
  while gp.status() != 3:
    gp = gp.mother(0)
  return gp
  
def findSec2(gp):
  while gp.status() != 3:
    gp = gp.mother(max(gp.numberOfMothers()-1,0))
  return gp
  
def assignGpTag(gpmu,gpmo1,gpmo2,lgp):
# get primary and taus
  if gpmu.status() == 3: return 1
  if abs(gpmo1.pdgId()) == 13 and gpmo1.status() == 3: return 1
  if abs(gpmo1.pdgId()) == 15 and gpmo1.status() == 3: return 2
# try jets through mother
  tag1 = -1
  igpmo1 = find(gpmo1,lgp)
  if igpmo1>5:
    if abs(gpmo1.pdgId()) in [1,2,3,21]: tag1 = 3
    if abs(gpmo1.pdgId()) in [4,5]: tag1 = abs(gpmo1.pdgId())
  tag2 = -1
  igpmo2 = find(gpmo2,lgp)
  if igpmo2>5:
    if abs(gpmo2.pdgId()) in [1,2,3,21]: tag2 = 3
    if abs(gpmo2.pdgId()) in [4,5]: tag2 = abs(gpmo2.pdgId())
  if tag1>-1 and tag2>-1:
    dr1 = deltaR({'eta':gpmu.eta(),'phi':gpmu.phi()},{'eta':gpmo1.eta(),'phi':gpmo1.phi()})
    dr2 = deltaR({'eta':gpmu.eta(),'phi':gpmu.phi()},{'eta':gpmo2.eta(),'phi':gpmo2.phi()})
    return tag1 if dr1<dr2 else tag2
  else:
    return tag1 if tag1>-1 else tag2
# if not use dr matching
  drmin = 0.5
  tag = 0
  for igp,gp in enumerate(lgp):
    if igp<6: continue
    absId = abs(gp.pdgId())
    if absId in [1,2,3,4,5,21]:
      dr = deltaR({'eta':gpmu.eta(),'phi':gpmu.phi()},{'eta':gp.eta(),'phi':gp.phi()})
      if dr < drmin:
        drmin = dr
        tag = absId if absId in [4,5] else 3
  return tag
  
def assignMuIgp(i,s):
  drmin = 0.2
  igpmin = -1
  for igp in range(s.ngp):
    if not abs(s.gpPdg[igp])==13: continue
    dr = deltaR({'eta':s.muEta[i],'phi':s.muPhi[i]},{'eta':s.gpEta[igp],'phi':s.gpPhi[igp]})
    if dr < drmin:
      drmin = dr
      igpmin = igp
  return igpmin

##################################################################################
storeVectors = True

for sample in allSamples:
  if not sample.has_key('isFastSim'):
    sample['isFastSim']=False
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
  muvars = ["muPt", "muEta", "muPhi", "muPdg", "muRelIso", "muDxy", "muDz", "muNormChi2", "muNValMuonHits", "muNumMatchedStations", "muPixelHits", "muNumtrackerLayerWithMeasurement", 'muIsGlobal', 'muIsTracker', 'muWPt']
  muvars+= ["muMT", "muClosestJetDeltaR", "muClosestJetMass", "muPBoost3D", "muIgpMatch"]

  elvars = ["elPt", "elEta", "elPhi", "elPdg", "elRelIso", "elDxy", "elDz"]
  tavars = ["taPt", "taEta", "taPhi", "taPdg"]
  if not sample['name'].lower().count('data'):
    mcvars = ["gpPdg", "gpM", "gpPt", "gpEta", "gpPhi", "gpMo1", "gpMo2", "gpDa1", "gpDa2", "gpSta", "gpTag"]
  if options.allsamples.lower()=='sms':
    variables+=['osetMgl', 'osetMN', 'osetMC', 'osetMsq']
  extraVariables=["nbtags", "ht",  "nSoftElectrons", "nHardElectrons", "nSoftTaus", "nHardTaus"]
  if sample['newMETCollection']:
    extraVariables+=["type1phiMet", "type1phiMetphi"]
  extraVariables += ["isrJetPt", "isrJetEta", "isrJetPhi", "isrJetPdg", "isrJetBtag", "isrJetChef", "isrJetNhef", "isrJetCeef", "isrJetNeef", "isrJetHFhef", "isrJetHFeef", "isrJetMuef", "isrJetElef", "isrJetPhef", "isrJetCutBasedPUJetIDFlag", "isrJetFull53XPUJetIDFlag", "isrJetMET53XPUJetIDFlag", "isrJetBTBVetoPassed", "isrJetUnc"]

#  extraVariables += ["looseMuIndex", "mediumMuIndex", "tightMuIndex"]
  extraVariables += ["nSoftMuonsLooseWP","nHardMuonsLooseWP","nSoftMuonsMediumWP","nHardMuonsMediumWP","nSoftMuonsTightWP","nHardMuonsTightWP"]
  extraVariables += ["nHardbtags", "nSoftbtags"]

  if not bin.lower().count('run'):
    btagVars=[]
    for i in range(maxConsideredBTagWeight+1):
      btagVars.append("weightBTag"+str(i)+"")
      btagVars.append("weightBTag"+str(i)+"_SF")
      btagVars.append("weightBTag"+str(i)+"_SF_b_Up")
      btagVars.append("weightBTag"+str(i)+"_SF_b_Down")
      btagVars.append("weightBTag"+str(i)+"_SF_light_Up")
      btagVars.append("weightBTag"+str(i)+"_SF_light_Down")
      if i>0:
        btagVars.append("weightBTag"+str(i)+"p")
        btagVars.append("weightBTag"+str(i)+"p_SF")
        btagVars.append("weightBTag"+str(i)+"p_SF_b_Up")
        btagVars.append("weightBTag"+str(i)+"p_SF_b_Down")
        btagVars.append("weightBTag"+str(i)+"p_SF_light_Up")
        btagVars.append("weightBTag"+str(i)+"p_SF_light_Down")
    extraVariables+=btagVars

#  extraVariables += ["softIsolatedMuPt", "softIsolatedMuEta", "softIsolatedMuPhi", "softIsolatedMuPdg", "softIsolatedMuRelIso", "softIsolatedMuDxy", "softIsolatedMuDz",  'softIsolatedMuNormChi2', 'softIsolatedMuNValMuonHits', 'softIsolatedMuNumMatchedStations', 'softIsolatedMuPixelHits', 'softIsolatedMuNumtrackerLayerWithMeasurement', 'softIsolatedMuIsTracker', 'softIsolatedMuIsGlobal']
  if storeVectors: 
#    extraVariables+=[ "softIsolatedpmuboost3d"]
    if sample['name'].lower().count('ttjets'):
      extraVariables+=["top0Pt", "top1Pt", "topPtWeight"] 
  structString = "struct MyStruct_"+str(nc)+"_"+str(isample)+"{ULong64_t event;"
  structString+="Float_t "+",".join(variables+extraVariables)+";"
#  for var in variables:
#    structString +="Float_t "+var+";"
#  for var in extraVariables:
#    structString +="Float_t "+var+";"
  structString +="Int_t nmu, nel, nta, njet, njet60, njet60FailID, njet30FailID, njet60FailISRJetID, njet30FailISRJetID, looseMuIndex, mediumMuIndex, tightMuIndex;"
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
        structString +="Float_t "+var+"[30];"
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
  t.Branch("looseMuIndex",ROOT.AddressOf(s,'looseMuIndex'),'looseMuIndex/I')
  t.Branch("mediumMuIndex",ROOT.AddressOf(s,'mediumMuIndex'),'mediumMuIndex/I')
  t.Branch("tightMuIndex",ROOT.AddressOf(s,'tightMuIndex'),'tightMuIndex/I')
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
              lgps = list(gps)
              for gp in gps:
                if abs(gp.pdgId()) == 6:
                  tops.append(gp)
                if gp.status() == 3:
                  lgp.append(gp)
#                elif (abs(gp.pdgId())==11 or abs(gp.pdgId())==13) and gp.pt() > 3.:
                elif (abs(gp.pdgId())==11 or abs(gp.pdgId())==13 or abs(gp.pdgId())==15) and gp.pt() > 3.:
                  lgp2.append(gp)
              lgp2 = sorted(lgp2, key=lambda k: -k.pt())
              s.ngp = min(len(lgp)+len(lgp2),30)
              for igp,gp in enumerate(lgp):
                s.gpPdg[igp] = gp.pdgId()
                s.gpM[igp] = gp.mass()
                s.gpPt[igp] = gp.pt()
                s.gpEta[igp] = gp.eta()
                s.gpPhi[igp] = gp.phi()
                s.gpMo1[igp] = find(gp.mother(0),lgp)
                s.gpMo2[igp] = find(gp.mother(max(gp.numberOfMothers()-1,0)),lgp)
                s.gpDa1[igp] = find(gp.daughter(0),lgp)
                s.gpDa2[igp] = find(gp.daughter(max(gp.numberOfDaughters()-1,0)),lgp)
                s.gpSta[igp] = gp.status()
                s.gpTag[igp] = 1 if abs(gp.pdgId())==13 else -1
              for igp2,gp2 in enumerate(lgp2,igp+1):
                if igp2 == 30:
                  break
                gpm1 = findSec1(gp2)
                gpm2 = findSec2(gp2)
                s.gpPdg[igp2] = gp2.pdgId()
                s.gpM[igp2] = gp2.mass()
                s.gpPt[igp2] = gp2.pt()
                s.gpEta[igp2] = gp2.eta()
                s.gpPhi[igp2] = gp2.phi()
                s.gpMo1[igp2] = find(gpm1,lgp)
                s.gpMo2[igp2] = find(gpm2,lgp)
                s.gpDa1[igp2] = -1
                s.gpDa2[igp2] = -1
                s.gpSta[igp2] = gp2.status()
                s.gpTag[igp2] = assignGpTag(gp2,gpm1,gpm2,lgp) if abs(gp2.pdgId())==13 else -1
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
          allGoodElectrons = getAllElectrons(c, neles)
          allGoodTaus = getAllTaus(c, ntaus)
          allGoodMuons = getAllMuons(c,nmuons) #Loose ID without relIso and Dxy<0.02

          softElectrons, hardElectrons = splitListOfObjects('pt', 20, allGoodElectrons)
          softTaus, hardTaus           = splitListOfObjects('pt', 20, allGoodTaus)
          muCandidates = filter(lambda m:abs(m['Dxy'])<0.02, allGoodMuons)  #Apply Dxy<0.02
          softMuons, hardMuons = splitListOfObjects('pt', 20, muCandidates)
          hardMuonsMediumWP = filter(lambda m:hybridIso(m, 'medium'), hardMuons) #for crosscleaning

          s.nSoftMuonsLooseWP = len(filter(lambda m:hybridIso(m, 'loose'), softMuons)) 
          s.nHardMuonsLooseWP = len(filter(lambda m:hybridIso(m, 'loose'), hardMuons)) 
          s.nSoftMuonsMediumWP = len(filter(lambda m:hybridIso(m, 'medium'), softMuons)) 
          s.nHardMuonsMediumWP = len(hardMuonsMediumWP) 
          s.nSoftMuonsTightWP = len(filter(lambda m:hybridIso(m, 'tight'), softMuons)) 
          s.nHardMuonsTightWP = len(filter(lambda m:hybridIso(m, 'tight'), hardMuons)) 

          s.looseMuIndex = next((i for i in range(len(muCandidates)) if hybridIso(muCandidates[i], 'loose')), -1) 
          s.mediumMuIndex =next((i for i in range(len(muCandidates)) if hybridIso(muCandidates[i], 'medium')), -1) 
          s.tightMuIndex = next((i for i in range(len(muCandidates)) if hybridIso(muCandidates[i], 'tight')), -1) 

          s.nSoftElectrons = len(softElectrons)
          s.nHardElectrons = len(hardElectrons)
          s.nSoftTaus = len(softTaus)
          s.nHardTaus = len(hardTaus)

          if options.chmode.count("CleanedWithAllLeptons"):
            jResult = getGoodJets(c, allGoodMuons + allGoodElectrons, jermode=options.jermode, jesmode=options.jesmode)
          else:
            jResult = getGoodJets(c, hardMuonsMediumWP + hardElectrons, jermode=options.jermode, jesmode=options.jesmode)
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
          s.nbtags      = len(filter(lambda j:j['btag']>0.679 and abs(j['eta'])<2.4, idJets30))
          s.nHardbtags  = len(filter(lambda j:j['pt']>=60 and j['btag']>0.679 and abs(j['eta'])<2.4, idJets30))
          s.nSoftbtags  = len(filter(lambda j:j['pt']<60 and j['btag']>0.679 and abs(j['eta'])<2.4, idJets30))
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
              s.muMT[i]    = sqrt(2.0*s.muPt[i]*s.type1phiMet*(1-cos(s.muPhi[i] - s.type1phiMetphi)))
              if len(idJets30)>0:
                cjet = findClosestJet(idJets30, {'phi':s.muPhi[i], 'eta':s.muEta[i]})
                s.muClosestJetDeltaR[i] = cjet['deltaR']
                s.muClosestJetMass[i] = invMass(cjet['jet'], {'phi':s.muPhi[i], 'pt':s.muPt[i], 'eta':s.muEta[i]})
              else:
                s.muClosestJetDeltaR[i] =float('nan') 
                s.muClosestJetMass[i] =  float('nan') 
              s.muPBoost3D[i] = pmuboost3d(idJets30, {'pt':s.type1phiMet, 'phi':s.type1phiMetphi}, {'phi':s.muPhi[i], 'pt':s.muPt[i], 'eta':s.muEta[i]} )
              s.muWPt[i] = sqrt( (allGoodMuons[i]['pt']*cos(allGoodMuons[i]['phi']) + s.type1phiMet*cos(s.type1phiMetphi))**2\
                               + (allGoodMuons[i]['pt']*sin(allGoodMuons[i]['phi']) + s.type1phiMet*sin(s.type1phiMetphi))**2)
              s.muIgpMatch[i] = -1
# MC specific part
              if not sample['name'].lower().count('data'):
                s.muIgpMatch[i] = assignMuIgp(i,s)
###################
             

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
            if not bin.lower().count('run'):
              zeroTagWeight = 1.
              bjetCandidates=filter(lambda j:abs(j['eta'])<2.4, idJets30)
              mceff = getMCEfficiencyForBTagSF(bjetCandidates, sample['isFastSim'])
              mceffW                = getTagWeightDict(mceff["mceffs"], maxConsideredBTagWeight)
              mceffW_SF             = getTagWeightDict(mceff["mceffs_SF"], maxConsideredBTagWeight)
              mceffW_SF_b_Up        = getTagWeightDict(mceff["mceffs_SF_b_Up"], maxConsideredBTagWeight)
              mceffW_SF_b_Down      = getTagWeightDict(mceff["mceffs_SF_b_Down"], maxConsideredBTagWeight)
              mceffW_SF_light_Up    = getTagWeightDict(mceff["mceffs_SF_light_Up"], maxConsideredBTagWeight)
              mceffW_SF_light_Down  = getTagWeightDict(mceff["mceffs_SF_light_Down"], maxConsideredBTagWeight)
#              print "mceffW                 ", mceffW
#              print "mceffW_SF              ", mceffW_SF
#              print "mceffW_SF_b_Up       ", mceffW_SF_b_Up
#              print "mceffW_SF_b_Down     ", mceffW_SF_b_Down
#              print "mceffW_SF_light_Up   ", mceffW_SF_light_Up
#              print "mceffW_SF_light_Down ", mceffW_SF_light_Down
#              print
              for i in range(1, maxConsideredBTagWeight+1):
                exec("s.weightBTag"+str(i)+"p=1")
                exec("s.weightBTag"+str(i)+"p_SF=1")
                exec("s.weightBTag"+str(i)+"p_SF_b_Up=1")
                exec("s.weightBTag"+str(i)+"p_SF_b_Down=1")
                exec("s.weightBTag"+str(i)+"p_SF_light_Up=1")
                exec("s.weightBTag"+str(i)+"p_SF_light_Down=1")
              for i in range(maxConsideredBTagWeight+1):
                exec("s.weightBTag"+str(i)+"="+str(mceffW[i]))
                exec("s.weightBTag"+str(i)+"_SF="+str(mceffW_SF[i]))
                exec("s.weightBTag"+str(i)+"_SF_b_Up="+str(mceffW_SF_b_Up[i]))
                exec("s.weightBTag"+str(i)+"_SF_b_Down="+str(mceffW_SF_b_Down[i]))
                exec("s.weightBTag"+str(i)+"_SF_light_Up="+str(mceffW_SF_light_Up[i]))
                exec("s.weightBTag"+str(i)+"_SF_light_Down="+str(mceffW_SF_light_Down[i]))
                for j in range(i+1, maxConsideredBTagWeight+1):
                  exec("s.weightBTag"+str(j)+"p               -="+str(mceffW[i]))
                  exec("s.weightBTag"+str(j)+"p_SF            -="+str(mceffW_SF[i]))
                  exec("s.weightBTag"+str(j)+"p_SF_b_Up       -="+str(mceffW_SF_b_Up[i]))
                  exec("s.weightBTag"+str(j)+"p_SF_b_Down     -="+str(mceffW_SF_b_Down[i]))
                  exec("s.weightBTag"+str(j)+"p_SF_light_Up   -="+str(mceffW_SF_light_Up[i]))
                  exec("s.weightBTag"+str(j)+"p_SF_light_Down -="+str(mceffW_SF_light_Down[i]))


          tmpDir = ROOT.gDirectory.func()
          chain_gDir.cd()
#          print s.type1phiMet
#          if s.type1phiMet<150:
#            print "Warning!!"
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
