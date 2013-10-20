import copy, pickle
import ROOT
from simplePlotsCommon import *
from math import *
import os, copy, array, xsec, sys, random
from xsecSMS import gluino8TeV_NLONLL
from btagEff import getMCEff, getTagWeightDict, getSF
from random import randint
import eventShape

ROOT.gROOT.ProcessLine(".L polSys/WPolarizationVariation.C+")
ROOT.gROOT.ProcessLine(".L polSys/TTbarPolarization.C+")
ROOT.gROOT.ProcessLine(".L mt2w/mt2w_bisect.cpp+")
ROOT.gROOT.ProcessLine(".L alphaT/alphaT.C+")

mt2w = ROOT.mt2w(500, 499, 0.5)

small = False

mode = "Mu"
#mode = "Ele"
#mode = "HT"

targetLumi = 19400.
if targetLumi==19400.:
  outputDir = "/data/schoef/convertedTuples_v21/"

#mode = "HT"
#chmode = "copy"

overwrite = True

maxConsideredBTagWeight = 3

chmodes = [\
#      "chmode = 'copy6j'",
#      "chmode = 'copy4j'",

#         "chmode = 'copyMET50HT750'",
#         "chmode = 'copyMET50'",
         "chmode = 'copyMET'",
#         "chmode = 'copyHT'",
#        "chmode = 'copyMET_JES+'",
#         "chmode = 'copyMET_JES-'",
#         "chmode = 'copyMET_separateBTagWeights'",
#         "chmode = 'copyMETGenLep'",
#
#         "chmode = 'copyMETmod2'",
#         "chmode = 'copy6JleptVeto'",
#         "chmode = 'copyTotal'",
#          "chmode = 'JER'",
#          "chmode = 'PDF_0'",
      ]

sms = ""
mNLow = -1
mNHigh = -1
mglLow = -1
mglHigh = -1

if len(sys.argv)>4:
  sms = sys.argv[4]
  mode = sys.argv[1]
  if sms=="T1tttt":
    mNLow = int(sys.argv[2])
    mNHigh = int(sys.argv[3])
  if sms=="T1t1t":
    mNLow = int(sys.argv[2])
    mNHigh = int(sys.argv[3])
  if sms=="T5tttt":
    mglLow = int(sys.argv[2])
    mglHigh = int(sys.argv[3])

#sms = "T5tttt"
#mglLow = 1025
#mglHigh = 1050

commoncf = "(-1)"
chainstring = "empty"

print "Using lumi", targetLumi,"Run2012ABC(D)"

if mode == "Mu":
  from defaultMu2012Samples import *

if mode == "Ele":
  from defaultEle2012Samples import *

if mode == "HT":
  from defaultHad2012Samples import *

def partonName (parton):
  if parton==5:  return 'b'
  if parton==4:  return 'c'
  return 'other'

def topWeight(topPt):
  p0 = 1.18246e+00;
  p1 = 4.63312e+02;
  p2 = 2.10061e-06;

  if  topPt>p1 : topPt = p1;
  return  p0 + p2 * topPt * ( topPt - 2 * p1 );


nvtxReweightingVar = "nTrueGenVertices"
if mode=="Ele" or mode=="Mu":
  allSamples = [ttbarPowHeg, wjets, wjetsInc, wjetsCombined, ttbar, dy, stop, qcd, wbbjets, wbbjetsCombined]
  if targetLumi == 12000.:
    data["bins"] = data["bins"][:4]
    for sample in [ttbar, ttbarPowHeg, wjets, wjetsInc, wjetsCombined, wbbjets, wbbjetsCombined, dy, stop, qcd]:
        sample["reweightingHistoFile"]          = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S10-Run2012ABC_60max_true_pixelcorr_Sys0.root"
        sample["reweightingHistoFileSysPlus"]   = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S10-Run2012ABC_60max_true_pixelcorr_SysPlus5.root"
        sample["reweightingHistoFileSysMinus"]  = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S10-Run2012ABC_60max_true_pixelcorr_SysMinus5.root"
    print "Using only databins", data["bins"]
  if targetLumi == 20000. or targetLumi==19400.:
    for sample in [ttbarScaleDown, ttbarScaleUp, ttbarMatchingDown, ttbarMatchingUp, ttbar, ttbarPowHeg, wjets, wjetsInc, wjetsCombined, wbbjets, wbbjetsCombined, dy, stop, qcd, ttwJets, ttzJets,]:
        sample["reweightingHistoFile"]          = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_Sys0.root"
        sample["reweightingHistoFileSysPlus"]   = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_SysPlus5.root"
        sample["reweightingHistoFileSysMinus"]  = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_SysMinus5.root"

if mode=="HT":
#  allSamples = [zToNuNu]#, qcdHad,  
  allSamples = [zToNuNu, qcdHad, ttbarPowHeg, HTdata, wjets, wjetsInc, wjetsCombined, dy, stop]
  for sample in allSamples:
    sample["reweightingHistoFile"]   = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_Sys0.root"
  qcdHad["reweightingHistoFile"] = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_Sys0.root"
else:
  allSamples = [ttbarPowHeg, singleLeptonData, wjets, wjetsInc, wjetsCombined, dy, stop, qcd, data]

#allSamples = [ttbarPowHeg]
#allSamples = [ttbarPowHeg, wjetsCombined, dy, stop, qcd]
#allSamples = [wjetsCombined, dy, stop, qcd]

#allSamples = [ttbarPowHeg]
#allSamples = [wjets, wjetsInc, wjetsCombined,dy, stop, qcd, ttwJets, ttzJets]
allSamples = [data, singleLeptonData]

from smsInfo import getT1ttttMadgraphDirs, getT5ttttMadgraphDirs, nfsDirectories
def getT1ttttSample(mgl, mN):
  res= {}
#  res["bins"] = ["T1tttt-madgraph_"+str(mgl)+"_"+str(mN)]
#  res["dirname"] = getT1ttttMadgraphDirs(mgl, mN)
#  res["name"] = "T1tttt-madgraph_"+str(mgl)+"_"+str(mN)
  res["bins"] = ["T1tttt_"+str(mgl)+"_"+str(mN)]
  res["dirname"] = nfsDirectories["T1tttt"]
  res["name"] = "T1tttt_"+str(mgl)+"_"+str(mN)
  res["additionalCut"] = "(osetMgl=="+str(mgl)+"&&osetMN=="+str(max(1,mN))+")"
  res["reweightingHistoFile"]          = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_Sys0.root"
  res["reweightingHistoFileSysPlus"]   = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_SysPlus5.root"
  res["reweightingHistoFileSysMinus"]  = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_SysMinus5.root"
  res["Chain"] = "Events"
  return res

if sms=="T1tttt":
  T1ttttSamples = []
  T1tttt = {}
  print "SMS",sms,"Mode:",mode, "mNLow:",mNLow,"mNHigh",mNHigh
  for mN in range( mNLow, mNHigh, 25):
    for mgl in range(mN + 300, 2025, 25):
#    for mgl in range(mN + 200, 1025, 25):
#    for mgl in range(mN + 200, mN + 450, 25):
      if not T1tttt.has_key(mgl):
        T1tttt[mgl]={}
      T1tttt[mgl][mN]= getT1ttttSample(mgl, mN)
      T1ttttSamples.append(T1tttt[mgl][mN])
  allSamples = T1ttttSamples

#allSamples=[]
#T1tttt = {}
#for mgl, mN in [[1025, 425], [1200, 0], [1200, 600], [1300, 0], [1300, 600]]:
#  if not T1tttt.has_key(mgl):
#    T1tttt[mgl]={}
#  T1tttt[mgl][mN] = getT1ttttSample(mgl, mN)
#  allSamples.append(T1tttt[mgl][mN])

if sms=="T1t1t":
  T1t1tSamples = []
  T1t1t = {}
  print "SMS",sms,"Mode:",mode, "mNLow:",mNLow,"mNHigh",mNHigh
  for mN in range( mNLow, mNHigh, 25):
    for msq in range(mN + 100, 825, 25):
      if not T1t1t.has_key(mN):
        T1t1t[mN]={}
      T1t1t[mN][msq]= {}
      T1t1t[mN][msq]["bins"] = ["8TeV-T1t1t"]
      T1t1t[mN][msq]["dirname"] = ["/data/mhickel/pat_130426/8TeV-T1t1t_2J_mGo-1000_mStop-200to750_mLSP-100to650", \
                                   "/data/mhickel/pat_130426/8TeV-T1t1t_2J_mGo-1000_mStop-350to750_mLSP-100to500", \
                                   "/data/mhickel/pat_130426/8TeV-T1t1t_2J_mGo-1000_mStop-775to825_mLSP-575to725", \
                                   "/data/mhickel/pat_130426/8TeV-T1t1t_2J_mGo-1000_mStop-800to800_mLSP-100to550"]
      T1t1t[mN][msq]["name"] = "T1t1t_"+str(mN)+"_"+str(msq)
      T1t1t[mN][msq]["additionalCut"] = "(osetMN=="+str(mN)+"&&osetMsq=="+str(msq)+")"
      
      T1t1t[mN][msq]["reweightingHistoFile"]          = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_Sys0.root"
      T1t1t[mN][msq]["reweightingHistoFileSysPlus"]   = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_SysPlus5.root"
      T1t1t[mN][msq]["reweightingHistoFileSysMinus"]  = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_SysMinus5.root"

      T1t1t[mN][msq]["Chain"] = "Events"
      T1t1tSamples.append(T1t1t[mN][msq])
  allSamples = T1t1tSamples

if sms=="T5tttt":
  T5ttttSamples = []
  T5tttt = {}
  print "SMS",sms,"Mode:",mode, "mglLow:",mglLow,"mglHigh",mglHigh
  for mgl in range( mglLow, mglHigh, 25):
    for msq in range(200, mgl-150, 25):
      if not T5tttt.has_key(mgl):
        T5tttt[mgl]={}
      T5tttt[mgl][msq]= {}
      T5tttt[mgl][msq]["bins"] = ["8TeV-T5tttt"]
      T5tttt[mgl][msq]["dirname"] = getT5ttttMadgraphDirs(mgl) 
      T5tttt[mgl][msq]["name"] = "T5tttt_"+str(mgl)+"_"+str(msq)
      T5tttt[mgl][msq]["additionalCut"] = "(osetMgl=="+str(mgl)+"&&osetMsq=="+str(msq)+")"
      T5tttt[mgl][msq]["reweightingHistoFile"]          = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_Sys0.root"
      T5tttt[mgl][msq]["reweightingHistoFileSysPlus"]   = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_SysPlus5.root"
      T5tttt[mgl][msq]["reweightingHistoFileSysMinus"]  = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_SysMinus5.root"
      T5tttt[mgl][msq]["Chain"] = "Events"
      T5ttttSamples.append(T5tttt[mgl][msq])
  allSamples = T5ttttSamples

#sms="T5tttt"
#
#T5ttttSamples = []
#T5tttt = {}
#print "SMS",sms,"Mode:",mode, "mglLow:",mglLow,"mglHigh",mglHigh
#for mgl in [1075]:
#  for msq in [575]:
#    if not T5tttt.has_key(mgl):
#      T5tttt[mgl]={}
#    T5tttt[mgl][msq]= {}
#    T5tttt[mgl][msq]["bins"] = ["8TeV-T5tttt"]
#    T5tttt[mgl][msq]["dirname"] = getT5ttttMadgraphDirs(mgl) 
#    T5tttt[mgl][msq]["name"] = "T5tttt_"+str(mgl)+"_"+str(msq)
#    T5tttt[mgl][msq]["additionalCut"] = "(osetMgl=="+str(mgl)+"&&osetMsq=="+str(msq)+")"
#    T5tttt[mgl][msq]["reweightingHistoFile"]          = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_Sys0.root"
#    T5tttt[mgl][msq]["reweightingHistoFileSysPlus"]   = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_SysPlus5.root"
#    T5tttt[mgl][msq]["reweightingHistoFileSysMinus"]  = "/data/schoef/results2012/PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_SysMinus5.root"
#    T5tttt[mgl][msq]["Chain"] = "Events"
#    T5ttttSamples.append(T5tttt[mgl][msq])
#allSamples = T5ttttSamples

def deltaPhi( phi1, phi2):
  dphi = phi2-phi1
  if  dphi > pi:
    dphi -= 2.0*pi
  if dphi <= -pi:
    dphi += 2.0*pi
  return abs(dphi)

def minAbsDeltaPhi(phi, phis):
  if len(phis)>0:
    return min([abs(deltaPhi(phi, x)) for x in phis])
  else: return float('inf')

def minAbsPiMinusDeltaPhi(phi, phis):
  if len(phis)>0:
    return min([abs(abs(deltaPhi(phi, x)) - pi) for x in phis])
  else: return float('inf')

def invMassOfLightObjects(p31, p32):
  [px1, py1, pz1] = p31
  [px2, py2, pz2] = p32
  px = px1+px2
  py = py1+py2
  pz = pz1+pz2
  p1 = sqrt(px1*px1+py1*py1+pz1*pz1)
  p2 = sqrt(px2*px2+py2*py2+pz2*pz2)
  p = sqrt(px*px+py*py+pz*pz)
  return   sqrt((p1 + p2)*(p1 + p2) - p*p)

def jerEtaBin(eta):
  feta = fabs(eta)
  if feta<=.5 : return 0
  if feta>.5 and feta<=1.1: return 1
  if feta>1.1 and feta<=1.7: return 2
  if feta>1.7 and feta<=2.3: return 3
  if feta>2.3 and feta<=5.0: return 4
  return -1

def jerDifferenceScaleFactor( jet, jermode = ""):
  if jermode=="": return 1.
  etab = jerEtaBin(jet["eta"])
  if jermode=="-1":
    if etab== 0: return 1.052 - 0.061
    if etab== 1: return 1.057 - 0.055
    if etab== 2: return 1.096 - 0.062
    if etab== 3: return 1.134 - 0.085
    if etab== 4: return 1.288 - 0.153
  if jermode=="0":
    if etab== 0: return 1.052
    if etab== 1: return 1.057
    if etab== 2: return 1.096
    if etab== 3: return 1.134
    if etab== 4: return 1.288
  if jermode=="1":
    if etab== 0: return 1.052 + 0.062
    if etab== 1: return 1.057 + 0.056
    if etab== 2: return 1.096 + 0.063
    if etab== 3: return 1.134 + 0.087
    if etab== 4: return 1.288 + 0.155
  return 1.


def getGoodJets(c, jes="0", jer=""):
  njets = getVarValue(c, "nsoftjets")
  res=[]
  resb=[]
  resl=[]
  delta_met_x = 0.
  delta_met_y = 0.
  deltaHT = 0.
  for i in range(int(njets)):
    eta = getVarValue(c, "jetsEta", i)
    pt  = getVarValue(c, "jetsPt", i)
    unscaledPt = pt
    if jes=="+":
      pt *= (1. + getVarValue(c, "jetsUnc", i))
    if jes=="-":
      pt *= (1. - getVarValue(c, "jetsUnc", i))
    if pt>40 and abs(eta)<2.4 and getVarValue(c, "jetsID", i) and getVarValue(c, "jetsEleCleaned", i) and getVarValue(c, "jetsMuCleaned", i):
      btag = getVarValue(c, "jetsBtag", i)
      btagged = btag>0.679
      phi = getVarValue(c, "jetsPhi", i)
      jet = {"pt":pt, "eta":eta,"phi":phi,"btag":btag}
      res.append(jet)
      if not jes=="0":
        delta_met_x += (- pt + unscaledPt)*cos(phi)
        delta_met_y += (- pt + unscaledPt)*sin(phi)
        deltaHT += pt - unscaledPt
      if btagged:
        resb.append(jet)
      else:
        resl.append(jet)
  res= sorted(res, key=lambda k: -k['pt'])
  resl= sorted(resl, key=lambda k: -k['pt'])
  resb= sorted(resb, key=lambda k: -k['btag'])
#  print res
  if not jes=="0":
    return res, resb, {"delta_met_x":delta_met_x, "delta_met_y":delta_met_y, "deltaHT":deltaHT}
  else:
    return res, resb, resl

def getJetArray(j):
  px = j['pt']*cos(j['phi'] )
  py = j['pt']*sin(j['phi'] )
  pz = j['pt']*sinh(j['eta'] )
  E = sqrt(px*px+py*py+pz*pz)
  return array.array('d', [E, px, py,pz])


def getMCEfficiencyForBTagSF(c, onlyLightJetSystem = False, sms=""):
  nsoftjets = int(getVarValue(c, "nsoftjets"))
  jets = [] 
  for i in range(nsoftjets):
    jPt     = getVarValue(c, "jetsPt", i)
    jEta    = getVarValue(c, "jetsEta", i)
    jParton = getVarValue(c, "jetsParton", i)
#                eff = 0.9-min(5,i)*0.1#getEfficiencyAndMistagRate(jPt, jEta, jParton )
    if jPt<=40. or abs(jEta)>=2.4 or (not getVarValue(c, "jetsEleCleaned", i)) or (not getVarValue(c, "jetsMuCleaned", i)) or (not getVarValue(c, "jetsID", i)):
      continue
    if onlyLightJetSystem and getVarValue(c, "jetsBtag", i)>0.679:
      continue
    if onlyLightJetSystem:
      jParton=1
    jets.append([jParton, jPt, jEta])
  if onlyLightJetSystem and len(jets)>0:
    nc = randint(0, len(jets)-1)
    jets[nc][0] = 4
  for jet in jets:
    jParton, jPt, jEta = jet
    r = getMCEff(parton=jParton, pt=jPt, eta=jEta, year=2012)#getEfficiencyAndMistagRate(jPt, jEta, jParton )
    jet.append(r)
#    print [j[0] for j in jets]
  mceffs = tuple()
  mceffs_SF = tuple()
  mceffs_SF_b_Up = tuple()
  mceffs_SF_b_Down = tuple()
  mceffs_SF_light_Up = tuple()
  mceffs_SF_light_Down = tuple()
  for jParton, jPt, jEta, r in jets:
    if sms!="":
      fsim_SF = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"mean",jEta)
      fsim_SF_up = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"up",jEta)
      fsim_SF_down = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"down",jEta)
    else:
      fsim_SF = 1.
      fsim_SF_up = 1.
      fsim_SF_down = 1.
    mceffs += (r["mcEff"],)
    mceffs_SF += (r["mcEff"]*r["SF"]*fsim_SF,)
    if abs(jParton)==5 or abs(jParton)==4:
      mceffs_SF_b_Up   += (r["mcEff"]*r["SF_up"]*fsim_SF_up,)
      mceffs_SF_b_Down += (r["mcEff"]*r["SF_down"]*fsim_SF_down,)
      mceffs_SF_light_Up   += (r["mcEff"]*r["SF"],)
      mceffs_SF_light_Down += (r["mcEff"]*r["SF"],)
    else:
      mceffs_SF_b_Up   += (r["mcEff"]*r["SF"],)
      mceffs_SF_b_Down += (r["mcEff"]*r["SF"],)
      mceffs_SF_light_Up   += (r["mcEff"]*r["SF_up"]*fsim_SF_up,)
      mceffs_SF_light_Down += (r["mcEff"]*r["SF_down"]*fsim_SF_down,)

  return {"mceffs":mceffs, "mceffs_SF":mceffs_SF, "mceffs_SF_b_Up":mceffs_SF_b_Up, "mceffs_SF_b_Down":mceffs_SF_b_Down, "mceffs_SF_light_Up":mceffs_SF_light_Up, "mceffs_SF_light_Down":mceffs_SF_light_Down}

for sample in allSamples:
  sample["filenames"]={}
  sample["weight"]={}
  sample["xsec"]={}
  for bin in sample["bins"]:
    sample["xsec"][bin] = -1.
    c = ROOT.TChain("Events")
    d = ROOT.TChain("Runs")
    sample["filenames"][bin]=[]

    if type(sample["dirname"])==type([]) and len(sample["bins"])==1:
      for dname in sample["dirname"]:
        if small:
          sample["filenames"][bin].append(dname+"/histo_10_*.root")
        else:
          sample["filenames"][bin].append(dname+"/*.root")
    else:
      subdirname = sample["dirname"]+"/"+bin+"/"
      if sample["bins"]==[""]:
        subdirname = sample["dirname"]+"/"
      if small:
        filelist=os.listdir(subdirname)
        counter = 3   #Joining n files
        for file in filelist:
          if os.path.isfile(subdirname+file) and file[-5:]==".root" and file.count("histo")==1:
            sample["filenames"][bin].append(subdirname+file)
            if counter==0:
              break
            counter=counter-1
      else:
        sample["filenames"][bin] = [subdirname+"/h*.root"]
    for file in sample["filenames"][bin]:
      c.Add(file)
      if not bin.count("redux"):
        d.Add(file)
    nevents = 0
    nruns = d.GetEntries()
    for i in range(0, nruns):
      d.GetEntry(i)
      nevents += getValue(d,"uint_EventCounter_runCounts_PAT.obj")
    weight = 1.
    if bin.count("T1tttt"):
      mgl = int(sample["name"].split("_")[1])
      mN = int(sample["name"].split("_")[2])
      xsec.xsec[bin] = gluino8TeV_NLONLL[mgl]
      nevents = c.GetEntries("osetMgl=="+str(mgl)+"&&osetMN=="+str(max(1,mN)))
      T1tttt[mgl][mN]["xsec"][bin] = xsec.xsec[bin]
      T1tttt[mgl][mN]["xsec"][bin] = xsec.xsec[bin]
      print "Using xsec",gluino8TeV_NLONLL[mgl],"for",bin,T1tttt[mgl][mN]["name"], "nevents", nevents
    if bin.count("T1t1t"):
      mN = int(sample["name"].split("_")[1])
      msq = int(sample["name"].split("_")[2])
      xsec.xsec[bin] = gluino8TeV_NLONLL[1000]
      nevents = c.GetEntries("osetMN=="+str(mN)+"&&osetMsq=="+str(msq))
      T1t1t[mN][msq]["xsec"][bin] = xsec.xsec[bin]
      T1t1t[mN][msq]["xsec"][bin] = xsec.xsec[bin]
      print "Using xsec",gluino8TeV_NLONLL[1000],"for",bin,T1t1t[mN][msq]["name"], "nevents", nevents
    if bin.count("T5tttt"):
      mgl = int(sample["name"].split("_")[1])
      msq = int(sample["name"].split("_")[2])
      xsec.xsec[bin] = gluino8TeV_NLONLL[mgl]
      nevents = c.GetEntries("osetMgl=="+str(mgl)+"&&osetMsq=="+str(msq))
      T5tttt[mgl][msq]["xsec"][bin] = xsec.xsec[bin]
      T5tttt[mgl][msq]["xsec"][bin] = xsec.xsec[bin]
      print "Using xsec",gluino8TeV_NLONLL[mgl],"for",bin,T5tttt[mgl][msq]["name"], "nevents", nevents
    if xsec.xsec.has_key(bin):
      if nevents>0:
        weight = xsec.xsec[bin]*targetLumi/nevents
        sample["xsec"][bin] = xsec.xsec[bin]
      else:
        weight = 0.
    print "Sample", sample["name"], "bin", bin, "n-events",nevents,"weight",weight
    sample["weight"][bin]=weight
    del c
    del d


def getVarValue(c, var, n=0):
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  else:
    return float('nan')

def getReweightingHisto(filename=""):
  if filename=="":
    return ""
  rf = ROOT.TFile(filename)
  htmp = rf.Get("ngoodVertices_Data")
  ROOT.gDirectory.cd("PyROOT:/")
  rwHisto = htmp.Clone()
  rf.Close()
  return rwHisto

eleEffSysEB = ROOT.TF1("eleEffSysEB", "0.916/(1+exp((6.3-x))/12)")
eleEffSysEE = ROOT.TF1("eleEffSysEE", "0.862/(1+exp((10.4-x))/14)")
muEffSys1   = ROOT.TF1("muEffSys1", "0.949/(1+exp((-16.1-x))/11)")
muEffSys2   = ROOT.TF1("muEffSys2", "1.01/(1+exp((-3.83-x))/14)")

#genmet_rwHist={}
#ifile = ROOT.TFile(mode+"_pythiaReweightingHistos.root")
#ifile.cd()
#htmp = ifile.Get("rwh_wjetsPlus").Clone()
#ROOT.gDirectory.cd("PyROOT:/")
#genmet_rwHist["W+"] = htmp.Clone()
#ifile.cd()
#htmp = ifile.Get("rwh_wjetsMinus").Clone()
#ROOT.gDirectory.cd("PyROOT:/")
#genmet_rwHist["W-"] = htmp.Clone()
#ifile.cd()
#htmp = ifile.Get("rwh_ttjets").Clone()
#ROOT.gDirectory.cd("PyROOT:/")
#genmet_rwHist["TT"] = htmp.Clone()
#ifile.Close()
#ROOT.gDirectory.cd("PyROOT:/")

for nc, m in enumerate(chmodes):
  commoncf = "-1"
  exec(m)
  print "Mode:", chmode, "for", mode
  presel = "None"
  prefixString = ""
  hadronicCut = "(jet2pt>40)"
  if chmode=="copy6j":
    hadronicCut = "(njets>=6)"
  if chmode=="copy4j":
    hadronicCut = "(njets>=4)"
  if chmode[:7]=="copyMET":
    hadronicCut =   "(met>100||genmet>100||type1phiMet>100)"
    if chmode=="copyMET50":
      hadronicCut = hadronicCut.replace("100", "50")
    if chmode=="copyMET50HT750":
      hadronicCut = hadronicCut.replace("100", "50")+"&&ht>750"
  if chmode=="copyMETmod2":
    hadronicCut =   "(event%2==1)&&(met>100||genmet>100)"
  if chmode=="copyInc":
    hadronicCut="(1)"

  if mode=="Mu":
    commoncf = hadronicCut+"&&ngoodMuons>0"
    if chmode[7:] == "GenLep":
      commoncf = hadronicCut+"&&antinuMu+nuMu>=1&&antinuE+nuE==0"
  if mode=="Ele":
    commoncf = hadronicCut+"&&ngoodElectrons>0"
    if chmode[7:] == "GenLep":
      commoncf = hadronicCut+"&&antinuMu+nuMu==0&&antinuE+nuE>=1"

  if mode=="HT":
    if chmode=="copy2JleptVeto":
      commoncf = "jet1pt>40&&nvetoMuons==0&&nvetoElectrons==0"
    if chmode=="copy6JleptVeto":
      commoncf = "njets>=6&&nvetoMuons==0&&nvetoElectrons==0"
    if chmode=="copyHT":
      commoncf =   "(ht>200)"
  if chmode[-5:] == "Total":
    commoncf = "(1)"
  if not os.path.isdir(outputDir+"/"+chmode):
    os.system("mkdir "+outputDir+"/"+chmode)
  pdfmeans = ""
  if chmode[:3]=="PDF":
    pdfMeans = pickle.load(open("pdfMeans.pkl"))
  if not os.path.isdir("mkdir "+outputDir+"/"+chmode+"/"+mode):
    os.system("mkdir "+outputDir+"/"+chmode+"/"+mode)
  else:
    print "Directory", outputDir+"/"+chmode+"/"+mode, "already found"


  for isample, sample in enumerate(allSamples):
    if not os.path.isdir("mkdir "+outputDir+"/"+chmode+"/"+mode+"/"+sample["name"]):
      os.system("mkdir "+outputDir+"/"+chmode+"/"+mode+"/"+sample["name"])
    else:
      print "Directory", outputDir+"/"+chmode+"/"+mode, "already found"

    variables = []
#    extraVariables=["mbb", "mbl", "phibb"]
    extraVariables=["alphaT"]
    extraVariables+=["S3D", "C3D", "C2D", "FWMT1", "FWMT2", "FWMT3", "FWMT4", "c2DLepMET", "FWMT1LepMET", "FWMT2LepMET", "FWMT3LepMET", "FWMT4LepMET"]
    if mode=="Ele" or mode=="Mu":
      variables = ["weight",  "weightPUSysPlus", "weightPUSysMinus", "targetLumi", "xsec", "weightLumi", "run", "lumi", "met", "type1phiMet", "type1phiMetpx", "type1phiMetpy", "metpx", "metpy", "metphi", "mT", "barepfmet" ,"ht", "btag0", "btag1", "btag2", "btag3","rawMetpx", "rawMetpy", "m3", "mht", "singleMuonic", "singleElectronic", \
      "leptonPt", "leptonEta", "leptonPhi", "leptonPdg", "njets", "nbtags", "nbjets", "jet0pt", "jet1pt", "jet2pt", "jet3pt", "jet0phi", "jet1phi","nvetoMuons", "nvetoElectrons", "ngoodMuons", "ngoodElectrons", "ngoodVertices", "nTrueGenVertices",
      "btag0pt", "btag1pt", "btag2pt", "btag3pt", "btag0eta", "btag1eta", "btag2eta", "btag3eta", "btag0Mass", "btag1Mass", "btag2Mass", "btag3Mass"]

      if chmode=="copyMET":
        extraVariables += ["weightEleEff", "weightMuEff1", "weightMuEff2", "probOneMoreBTag", "probOneMoreBTagSF", "mt2w", "minDeltaPhi", "htRatio"]
#        if sms=="" and chmode[:7]=="copyMET":
#          extraVariables+= [ "numBPartons", "numCPartons"]
      if sample["name"]=="singleMuData" and mode=="Mu":
        variables+=["HLTIsoMu24eta2p1","HLTIsoMu30eta2p1","HLTIsoMu34eta2p1","HLTIsoMu40eta2p1",\
                    "preIsoMu24eta2p1","preIsoMu30eta2p1","preIsoMu34eta2p1","preIsoMu40eta2p1"]
        variables+= ["HLTPFHT350Mu15PFMET45", "HLTPFHT350Mu15PFMET50", "HLTPFHT400Mu5PFMET45", "HLTPFHT400Mu5PFMET50", "HLTPFNoPUHT350Mu15PFMET45", "HLTPFNoPUHT350Mu15PFMET50", "HLTPFNoPUHT400Mu5PFMET45", "HLTPFNoPUHT400Mu5PFMET50",\
                     "prePFHT350Mu15PFMET45", "prePFHT350Mu15PFMET50", "prePFHT400Mu5PFMET45", "prePFHT400Mu5PFMET50", "prePFNoPUHT350Mu15PFMET45", "prePFNoPUHT350Mu15PFMET50", "prePFNoPUHT400Mu5PFMET45", "prePFNoPUHT400Mu5PFMET50"]
      if sample["name"]=="singleEleData" and mode=="Ele":
        variables += ["HLTCleanPFHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45", "HLTCleanPFHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50", "HLTCleanPFHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45", "HLTCleanPFHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50", "HLTCleanPFNoPUHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45", "HLTCleanPFNoPUHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50", "HLTCleanPFNoPUHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45", "HLTCleanPFNoPUHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50", "HLTEle27WP80", "preCleanPFHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45", "preCleanPFHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50", "preCleanPFHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45", "preCleanPFHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50", "preCleanPFNoPUHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45", "preCleanPFNoPUHT300Ele15CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50", "preCleanPFNoPUHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET45", "preCleanPFNoPUHT350Ele5CaloIdTCaloIsoVLTrkIdTTrkIsoVLPFMET50", "preEle27WP80"]

      MC_variables =  ["genmet", "genmetpx","genmetpy", "btag0parton", "btag1parton", "btag2parton", "btag3parton",\
                       "antinuMu", "antinuE", "antinuTau", "nuMu", "nuE", "nuTau", "nuMuFromTausFromWs", "nuEFromTausFromWs", "nuTauFromTausFromWs", "weightTTPolPlus5", "weightTTPolMinus5", "weightTTxsecPlus30", "weightTTxsecMinus30",
                       "weightDiLepPlus15", "weightDiLepMinus15", "weightTauPlus15", "weightTauMinus15",  "weightWxsecPlus30", "weightWxsecMinus30" , "weightNonLeadingxsecPlus30", "weightNonLeadingxsecMinus30", "hasGluonSplitting", "numBPartons", "numCPartons"]
      if sms!="":
        MC_variables+=["gluino0Pt", "gluino0Eta", "gluino0Phi", "gluino0Pdg"]
        MC_variables+=["gluino1Pt", "gluino1Eta", "gluino1Phi", "gluino1Pdg"]
        MC_variables+=["osetMgl", "osetMN", "osetMsq"]
      if sample["name"].lower().count("ttjets"):
        MC_variables+= ["top0WDaughter0Pdg", "top0WDaughter0Px", "top0WDaughter0Py", "top0WDaughter0Pz"]
        MC_variables+= ["top0WDaughter1Pdg", "top0WDaughter1Px", "top0WDaughter1Py", "top0WDaughter1Pz"]
        MC_variables+= ["top1WDaughter0Pdg", "top1WDaughter0Px", "top1WDaughter0Py", "top1WDaughter0Pz"]
        MC_variables+= ["top1WDaughter1Pdg", "top1WDaughter1Px", "top1WDaughter1Py", "top1WDaughter1Pz"]
        MC_variables+= ["top0Px", "top1Px", "top0Py", "top1Py", "top0Pz", "top1Pz"]
      if sample["bins"][0].count("Run")==0:
        variables+=MC_variables
        extraVariables += ["weightWPol1Plus10","weightWPol1Minus10","weightWPol2PlusPlus5","weightWPol2PlusMinus5","weightWPol2MinusPlus5","weightWPol2MinusMinus5","weightWPol3Plus10","weightWPol3Minus10"]

    btagVars=[]
    separateBTagWeights = False
    if len(chmode.split("_"))>1 and chmode.split("_")[1]=="separateBTagWeights" :
      separateBTagWeights = True
      btagVars = ["weightBTag", "weightBTag_SF", "weightBTag_SF_b_Up", "weightBTag_SF_b_Down", "weightBTag_SF_light_Up", "weightBTag_SF_light_Down"]
      print "Storing separate btag weights!"
    else:
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
    extraVariables += btagVars

    if mode=="HT":
      variables = ["weight",  "weightPUSysPlus", "weightPUSysMinus", "targetLumi", "xsec", "weightLumi", "run", "lumi", "met", "type1phiMet", "type1phiMetpx", "type1phiMetpy", "metpx", "metpy", "metphi", "mT", "barepfmet" ,"ht", "btag0", "btag1", "btag2", "btag3","rawMetpx", "rawMetpy", "m3", "mht", "singleMuonic", "singleElectronic", \
      "leptonPt", "leptonEta", "leptonPhi", "leptonPdg", "njets", "nbtags", "nbjets", "jet0pt", "jet1pt", "jet2pt", "jet3pt", "jet0phi", "jet1phi","nvetoMuons", "nvetoElectrons", "ngoodMuons", "ngoodElectrons", "ngoodVertices", "nTrueGenVertices",
      "btag0pt", "btag1pt", "btag2pt", "btag3pt", "btag0eta", "btag1eta", "btag2eta", "btag3eta", "btag0Mass", "btag1Mass", "btag2Mass", "btag3Mass"]
      if sample["bins"][0].count("Run"):
        alltriggers =  [  "HLTHT200", "HLTHT250", "HLTHT300", "HLTHT350", "HLTHT400", "HLTHT450", "HLTHT500", "HLTHT550", "HLTHT600", "HLTHT650", "HLTHT700", "HLTHT750"]
        for trigger in alltriggers:
          variables.append(trigger)
          variables.append(trigger.replace("HLT", "pre") )
      else:
        variables+=["genmet","genmetpx","genmetpy"]

    print variables, extraVariables

    structString = "struct MyStruct_"+str(nc)+"_"+str(isample)+"{ULong64_t event;"
    for var in variables:
      structString +="Float_t "+var+";"
    for var in extraVariables:
      structString +="Float_t "+var+";"
    structString   +="};"
    ROOT.gROOT.ProcessLine(structString)

    exec("from ROOT import MyStruct_"+str(nc)+"_"+str(isample))
    exec("s = MyStruct_"+str(nc)+"_"+str(isample)+"()")

    t = ROOT.TTree( "Events", "Events", 1 )
    t.Branch("event",   ROOT.AddressOf(s,"event"), 'event/l')
    for var in variables:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
    for var in extraVariables:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
    ofile = outputDir+"/"+chmode+"/"+mode+"/"+sample["name"]+"/histo_"+sample["name"]+".root"
    if os.path.isfile(ofile) and overwrite:
      print "Warning! will overwrite",ofile
    if os.path.isfile(ofile) and not overwrite:
      print ofile, "already there! Skipping!!!"
      continue
    rwHistoSysPlus,rwHistoSysMinus,rwHisto = "","",""
    if sample.has_key("reweightingHistoFile"):
      rwHisto=getReweightingHisto(sample["reweightingHistoFile"])
    if sample.has_key("reweightingHistoFileSysPlus"):
      rwHistoSysPlus=getReweightingHisto(sample["reweightingHistoFileSysPlus"])
    if sample.has_key("reweightingHistoFileSysMinus"):
      rwHistoSysMinus=getReweightingHisto(sample["reweightingHistoFileSysMinus"])

    if rwHisto!="":
      print "Using reweightingHisto", sample["reweightingHistoFile"], rwHisto,"for sample",sample["name"]
    else:
      print "Using no reweightingHisto for sample",sample["name"]

    for bin in sample["bins"]:
      c = ROOT.TChain(sample["Chain"])
      for thisfile in sample["filenames"][bin]:
        c.Add(thisfile)
      ntot = c.GetEntries()
      if bin.count("Run")!=0: commoncf = commoncf.replace("||genmet>100", "")
      thiscommoncf = commoncf
      if sample.has_key("additionalCut"):
        if type(sample["additionalCut"])==type({}):
          if sample["additionalCut"].has_key(bin):
            thiscommoncf = commoncf+"&&"+sample["additionalCut"][bin]
        else:
          thiscommoncf = commoncf+"&&"+sample["additionalCut"]

      if ntot>0:
        c.Draw(">>eList", thiscommoncf)
        elist = ROOT.gDirectory.Get("eList")
        number_events = elist.GetN()
        if sample.has_key("scaleFac") and sample["scaleFac"].has_key(bin):
          print "Scaling by", sample["scaleFac"][bin],"!"
        print "Reading: ", sample["name"], bin, "with",number_events,"Events using cut", thiscommoncf
        if small:
          if number_events>1000:
            number_events=1000
        for i in range(0, number_events):
          if (i%10000 == 0) and i>0 :
            print i
    #      # Update all the Tuples
          if elist.GetN()>0 and ntot>0:
            c.GetEntry(elist.GetEntry(i))
            nvtxWeightSysPlus, nvtxWeightSysMinus, nvtxWeight = 1.,1.,1.
            if rwHisto!="" and xsec.xsec.has_key(bin):
              nvtxWeight = rwHisto.GetBinContent(rwHisto.FindBin(getVarValue(c, nvtxReweightingVar)))
            if rwHistoSysPlus!="" and xsec.xsec.has_key(bin):
              nvtxWeightSysPlus = rwHistoSysPlus.GetBinContent(rwHistoSysPlus.FindBin(getVarValue(c, nvtxReweightingVar)))
            if rwHistoSysMinus!="" and xsec.xsec.has_key(bin):
              nvtxWeightSysMinus = rwHistoSysMinus.GetBinContent(rwHistoSysMinus.FindBin(getVarValue(c, nvtxReweightingVar)))
            for var in variables[1:]:
              getVar = var
              if prefixString!="":
                getVar = prefixString+"_"+var
              exec("s."+var+"="+str(getVarValue(c, getVar)).replace("nan","float('nan')"))
            scaleFac = 1.
            if sample.has_key("scaleFac"):
              if sample["scaleFac"].has_key(bin):
                scaleFac = sample["scaleFac"][bin]
            s.weight            = scaleFac*sample["weight"][bin]*nvtxWeight
            s.weightPUSysPlus   = scaleFac*sample["weight"][bin]*nvtxWeightSysPlus
            s.weightPUSysMinus  = scaleFac*sample["weight"][bin]*nvtxWeightSysMinus
            if chmode=="copyMET_TopRW":
              if c.GetLeaf(c.GetAlias('top0Pdg')).GetValue()>0:
                topPt=sqrt(c.GetLeaf(c.GetAlias('top0Px')).GetValue()**2 + c.GetLeaf(c.GetAlias('top0Py')).GetValue()**2)
              else:
                topPt=sqrt(c.GetLeaf(c.GetAlias('top1Px')).GetValue()**2 + c.GetLeaf(c.GetAlias('top1Py')).GetValue()**2)
              s.weight*=topWeight(topPt)
              #print topPt,topWeight(topPt)
            s.event = long(c.GetLeaf(c.GetAlias('event')).GetValue())
            s.targetLumi = targetLumi
            s.weightLumi = scaleFac*sample["weight"][bin]
            s.xsec = sample["xsec"][bin]
#            print s.xsec, s.weightLumi, s.targetLumi
            if len(extraVariables)>0:
              for var in extraVariables:
                exec("s."+var+"=float('nan')")

            pxLep = s.leptonPt*cos( s.leptonPhi)
            pyLep = s.leptonPt*sin( s.leptonPhi)
            pzLep = s.leptonPt*sinh(s.leptonEta)
            ELep = sqrt(pxLep*pxLep + pyLep*pyLep + pzLep*pzLep)
            lep    =array.array('d',[ELep, pxLep, pyLep, pzLep] )
            pmiss  =array.array('d',[  0., s.type1phiMetpx, s.type1phiMetpy] )
            mt2w_values=[]
            jets, bjets, ljets = getGoodJets(c)
            metPhi = atan2(s.type1phiMetpy, s.type1phiMetpx)
            den=0
            num=0
            for j in jets:
              den+=j["pt"]
              if abs(deltaPhi(metPhi, j["phi"])) <= pi/2:
                num+=j["pt"]
            if len(jets)>0:
              s.htRatio = num/den
#            print jets         
            if 1<abs(den-s.ht):print "WARNING HT <> sum(JET-pt) DISAGREEMENT!!"
            if len(jets)>=2:
              s.alphaT =  ROOT.CalcAlphaT(array.array('d', [ j['pt'] for j in jets ]), array.array('d', [ j['eta'] for j in jets ]), array.array('d', [ j['phi'] for j in jets ]), len(jets) ) 
#            if s.njets==3:
#              print "njets",s.njets, "met",s.met, "ht", s.ht, "alphaT", s.alphaT
            if len(bjets)==0 and len(ljets)>=3: #All combinations from the highest three light (or b-) jets
              b0=getJetArray(ljets[0])
              b1=getJetArray(ljets[1])
              b2=getJetArray(ljets[2])

              mt2w.set_momenta(lep, b0, b1, pmiss)
              mt2w_values.append(mt2w.get_mt2w()) 
              mt2w.set_momenta(lep, b1, b0, pmiss)
              mt2w_values.append(mt2w.get_mt2w())

              mt2w.set_momenta(lep, b0, b2, pmiss)
              mt2w_values.append(mt2w.get_mt2w()) 
              mt2w.set_momenta(lep, b2, b0, pmiss)
              mt2w_values.append(mt2w.get_mt2w())

              mt2w.set_momenta(lep, b2, b1, pmiss)
              mt2w_values.append(mt2w.get_mt2w()) 
              mt2w.set_momenta(lep, b1, b2, pmiss)
              mt2w_values.append(mt2w.get_mt2w())
            if len(bjets)==1 and len(ljets)>=2: #All combinations from one b and the highest two light jets
              b0=getJetArray(bjets[0])
              b1=getJetArray(ljets[0])
              b2=getJetArray(ljets[1])

              mt2w.set_momenta(lep, b0, b1, pmiss)
              mt2w_values.append(mt2w.get_mt2w()) 
              mt2w.set_momenta(lep, b1, b0, pmiss)
              mt2w_values.append(mt2w.get_mt2w())

              mt2w.set_momenta(lep, b0, b2, pmiss)
              mt2w_values.append(mt2w.get_mt2w()) 
              mt2w.set_momenta(lep, b2, b0, pmiss)
              mt2w_values.append(mt2w.get_mt2w())

            if len(bjets)==2:
              b0=getJetArray(bjets[0])
              b1=getJetArray(bjets[1])
#              print lep, pmiss, b0, b1
              mt2w.set_momenta(lep, b0, b1, pmiss)
              mt2w_values.append(mt2w.get_mt2w()) 
              mt2w.set_momenta(lep, b1, b0, pmiss)
              mt2w_values.append(mt2w.get_mt2w())
            if len(bjets)>=3: #All combinations from the highest three light (or b-) jets
        
              bjets= sorted(bjets, key=lambda k: -k['pt'])

              b0=getJetArray(bjets[0])
              b1=getJetArray(bjets[1])
              b2=getJetArray(bjets[2])

              mt2w.set_momenta(lep, b0, b1, pmiss)
              mt2w_values.append(mt2w.get_mt2w()) 
              mt2w.set_momenta(lep, b1, b0, pmiss)
              mt2w_values.append(mt2w.get_mt2w())

              mt2w.set_momenta(lep, b0, b2, pmiss)
              mt2w_values.append(mt2w.get_mt2w()) 
              mt2w.set_momenta(lep, b2, b0, pmiss)
              mt2w_values.append(mt2w.get_mt2w())

              mt2w.set_momenta(lep, b2, b1, pmiss)
              mt2w_values.append(mt2w.get_mt2w()) 
              mt2w.set_momenta(lep, b1, b2, pmiss)
              mt2w_values.append(mt2w.get_mt2w())
#            print len(bjets), len(ljets), len(jets), mt2w_values
            if len(mt2w_values)>0:
              s.mt2w = min(mt2w_values)
#            print s.mt2w
            s.minDeltaPhi = min(abs(deltaPhi(s.jet0phi, metPhi)), abs(deltaPhi(s.jet1phi, metPhi)))
#            print s.minDeltaPhi
            if len(jets)>1:
              s3D = eventShape.sphericity(jets)
              c3D = eventShape.circularity(s3D["eigenvalues"])
              c2D = eventShape.circularity2D(jets)
              foxwolfram = eventShape.foxWolframMoments(jets)
              s.S3D= s3D['sphericity']
              s.C3D= c3D
              s.C2D= c2D
              s.FWMT1= foxwolfram["FWMT1"]
              s.FWMT2= foxwolfram["FWMT2"]
              s.FWMT3= foxwolfram["FWMT3"]
              s.FWMT4= foxwolfram["FWMT4"]

              if mode=='Mu' or mode=='Ele': 
                metObj = {"pt":s.type1phiMet, "phi":metPhi}
                lepObj = {"pt":s.leptonPt, "phi":s.leptonPhi}
                c2DLepMET = eventShape.circularity2D(jets+[lepObj]+[metObj])
                foxwolfram = eventShape.foxWolframMoments(jets+[lepObj]+[metObj])
                s.c2DLepMET   =  c2DLepMET          
                s.FWMT1LepMET = foxwolfram["FWMT1"]
                s.FWMT2LepMET = foxwolfram["FWMT2"]
                s.FWMT3LepMET = foxwolfram["FWMT3"]
                s.FWMT4LepMET = foxwolfram["FWMT4"]


            if len(chmode.split("_"))>1 and chmode.split("_")[1][:3]=="JES":
#              print "\n",s.met, s.ht,s.njets,s.nbtags
              jesmode = chmode.split("_")[1][3]
              jets, bjets, changeDict = getGoodJets(c, jes = jesmode)
              s.njets = len(jets)
              s.nbtags = len(bjets)
              s.ht += changeDict["deltaHT"]
              s.metpx += changeDict["delta_met_x"]
              s.metpy += changeDict["delta_met_y"]
              s.met = sqrt(s.metpx**2 + s.metpy**2)
#              print s.met, s.ht,s.njets,s.nbtags
              for i in range(4):
                if i<len(jets):
                  exec("s.jet"+str(i)+"pt = "+str(jets[i]["pt"]))
                  exec("s.jet"+str(i)+"eta = "+str(jets[i]["eta"]))
                  exec("s.jet"+str(i)+"phi = "+str(jets[i]["phi"]))
                  exec("s.jet"+str(i)+"btag = "+str(jets[i]["btag"]))
                else:
                  exec("s.jet"+str(i)+"pt = float('nan')")
                  exec("s.jet"+str(i)+"phi = float('nan')")
                  exec("s.jet"+str(i)+"eta = float('nan')")
                  exec("s.jet"+str(i)+"btag = float('nan')")
              for i in range(4):
                if i<len(bjets):
                  exec("s.btag"+str(i)+" = "+str(bjets[i]["btag"]))
                  exec("s.btag"+str(i)+"pt = "+str(bjets[i]["pt"]))
                  exec("s.btag"+str(i)+"eta = "+str(bjets[i]["eta"]))
                  exec("s.btag"+str(i)+"phi = "+str(bjets[i]["phi"]))
                else:
                  exec("s.btag"+str(i)+" = float('nan')")
                  exec("s.btag"+str(i)+"pt = float('nan')")
                  exec("s.btag"+str(i)+"phi = float('nan')")
                  exec("s.btag"+str(i)+"eta = float('nan')")
#              print jets, bjets, changeDict

            if (not mode=="HT" ) and ("Run" not in bin ) and (sms==""):
#              if chmode[:7]=="copyMET":
#                numBPartons = ROOT.TTreeFormula("numBPartons", "Sum$(abs(jetsParton)==5&&jetsEleCleaned&&jetsMuCleaned&&jetsID)",c)
#                numCPartons = ROOT.TTreeFormula("numCPartons", "Sum$(abs(jetsParton)==4&&jetsEleCleaned&&jetsMuCleaned&&jetsID)",c)
#                s.numBPartons = numBPartons.EvalInstance()
#                s.numCPartons = numCPartons.EvalInstance()
#                del numBPartons, numCPartons
              if s.nuMu + s.antinuMu + s.nuE + s.antinuE==2:
                s.weightDiLepPlus15  = 1.15*s.weight
                s.weightDiLepMinus15 = 0.85*s.weight
              else:
                s.weightDiLepPlus15  = s.weight
                s.weightDiLepMinus15 = s.weight

              if s.nuTau+s.antinuTau>=1:
                s.weightTauPlus15  = 1.15*s.weight
                s.weightTauMinus15 = 0.85*s.weight
              else:
                s.weightTauPlus15  = s.weight
                s.weightTauMinus15 = s.weight
            if (not mode=="HT") and chmode=="copyMET":
              s.weightEleEff = s.weight
              s.weightMuEff1 = s.weight
              s.weightMuEff2 = s.weight
              if (s.singleMuonic):
                s.weightMuEff1 = muEffSys1(s.leptonPt)*s.weight
                s.weightMuEff2 = muEffSys2(s.leptonPt)*s.weight
              if (s.singleElectronic):
                if (abs(s.leptonEta)<1.4442):
                  s.weightEleEff = eleEffSysEB(s.leptonPt)*s.weight
                else:
                  s.weightEleEff = eleEffSysEE(s.leptonPt)*s.weight
#              print "Mu1",s.weightMuEff1/s.weight, s.weightMuEff2/s.weight, s.weightEleEff/s.weight

              s.weightTTPolPlus5 = s.weight
              s.weightTTPolMinus5 = s.weight
              s.weightTTxsecPlus30  = s.weight
              s.weightTTxsecMinus30 = s.weight
              s.weightNonLeadingxsecPlus30  = s.weight
              s.weightNonLeadingxsecMinus30 = s.weight
              if not sample["name"].lower().count("ttjets") and not sample["name"].lower().count("wjets"):
                s.weightNonLeadingxsecPlus30  = 1.3*s.weight
                s.weightNonLeadingxsecMinus30 = 0.7*s.weight
              if sample["name"].lower().count("ttjets"):
                s.weightTTxsecPlus30 = 1.3* s.weight
                s.weightTTxsecMinus30 = 0.7* s.weight

                top0WDaughter0Pdg = abs(getVarValue(c, "top0WDaughter0Pdg"))
                top1WDaughter0Pdg = abs(getVarValue(c, "top1WDaughter0Pdg"))
                sLepTop = -1
                if top0WDaughter0Pdg>=10 and not (top1WDaughter0Pdg>=10):
                  sLepTop = 0
                if top1WDaughter0Pdg>=10 and not (top0WDaughter0Pdg>=10):
                  sLepTop = 1
                if sLepTop>=0:
                  if not 0==abs(getVarValue(c, "top"+str(sLepTop)+"WDaughter0Pdg"))%2:
                    lepDaughter = 0
                  else:
                    lepDaughter = 1
  #                print "top0WDaughter0Pdg",top0WDaughter0Pdg,"top1WDaughter0Pdg",top1WDaughter0Pdg, "sLepTop",sLepTop, "lepDaughter", lepDaughter
                  lpx = getVarValue(c, "top"+str(sLepTop)+"WDaughter"+str(lepDaughter)+"Px")
                  lpy = getVarValue(c, "top"+str(sLepTop)+"WDaughter"+str(lepDaughter)+"Py")
                  lpz = getVarValue(c, "top"+str(sLepTop)+"WDaughter"+str(lepDaughter)+"Pz")
                  lpE = sqrt(lpx**2 + lpy**2 + lpz**2)
                  neupx = getVarValue(c, "top"+str(sLepTop)+"WDaughter"+str(1-lepDaughter)+"Px")
                  neupy = getVarValue(c, "top"+str(sLepTop)+"WDaughter"+str(1-lepDaughter)+"Py")
                  neupz = getVarValue(c, "top"+str(sLepTop)+"WDaughter"+str(1-lepDaughter)+"Pz")
                  neuE = sqrt(neupx**2 + neupy**2 + neupz**2)
                  bpx = getVarValue(c, "top"+str(sLepTop)+"bPx")
                  bpy = getVarValue(c, "top"+str(sLepTop)+"bPy")
                  bpz = getVarValue(c, "top"+str(sLepTop)+"bPz")
                  bE = sqrt(bpx**2 + bpy**2 + bpz**2)
                  s.weightTTPolPlus5   = s.weight*ROOT.weightTTbarPolarization(bpx+lpx+neupx, bpy+lpy+neupy, bpz+lpz+neupz, bE+lpE+neuE, lpx+neupx, lpy+neupy, lpz+neupz, lpE+neuE, lpx, lpy, lpz, lpE, +5)
                  s.weightTTPolMinus5  = s.weight*ROOT.weightTTbarPolarization(bpx+lpx+neupx, bpy+lpy+neupy, bpz+lpz+neupz, bE+lpE+neuE, lpx+neupx, lpy+neupy, lpz+neupz, lpE+neuE, lpx, lpy, lpz, lpE, -5)
  #                print "Calculate TTJets pol. variation weight: ", s.weightTTPolPlus5, s.weightTTPolMinus5
                #genp4_lminus_.SetPxPyPzE(mc_doc_px->at(i),mc_doc_py->at(i),mc_doc_pz->at(i),mc_doc_energy->at(i))

              s.weightWPol1Plus10 = s.weight
              s.weightWPol1Minus10 = s.weight
              s.weightWPol2PlusPlus5 = s.weight
              s.weightWPol2PlusMinus5 = s.weight
              s.weightWPol2MinusPlus5 = s.weight
              s.weightWPol2MinusMinus5 = s.weight
              s.weightWPol3Plus10 = s.weight
              s.weightWPol3Minus10 = s.weight
              s.weightWxsecPlus30  = s.weight
              s.weightWxsecMinus30 = s.weight
              if sample["name"].lower().count("wjets"):
                s.weightWxsecPlus30 = 1.3*s.weight
                s.weightWxsecMinus30 = 0.7*s.weight

                if getVarValue(c, "genleptonmatch"):
                  plus = (s.leptonPdg<0)
                  minus = not plus
                  Wpx =getVarValue(c, "W0Px")
                  Wpy =getVarValue(c, "W0Py")
                  Weta = getVarValue(c, "W0Eta")
                  Wpz = sqrt(Wpx**2 + Wpy**2)*sinh(Weta)

                  lpx = s.leptonPt*cos(s.leptonPhi)
                  lpy = s.leptonPt*sin(s.leptonPhi)
                  lpz = s.leptonPt*sinh(s.leptonEta)
                  genp4_W_ = ROOT.TLorentzVector(Wpx, Wpy, Wpz, ROOT.sqrt(80.4**2 + Wpx**2 + Wpy**2 + Wpz**2))
                  genp4_l_ = ROOT.TLorentzVector(lpx, lpy, lpz, ROOT.sqrt(80.4**2 + lpx**2 + lpy**2 + lpz**2))
                  if plus:
                    WPol1Plus10_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,10,1);
                    WPol1Minus10_weight_flfr       = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,-10,1);
                    s.weightWPol1Plus10 = s.weight*WPol1Plus10_weight_flfr
                    s.weightWPol1Minus10 = s.weight*WPol1Minus10_weight_flfr
  #                    print "Wplus ", plus, chmode, Wplus_weight_flfr
                    WPol2PlusPlus5_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,5,1);
                    WPol2PlusMinus5_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,-5,1);
                    s.weightWPol2PlusPlus5= s.weight*WPol2PlusPlus5_weight_flfr
                    s.weightWPol2PlusMinus5= s.weight*WPol2PlusMinus5_weight_flfr
  #                    print "Wplus ", plus, chmode, Wplus_weight_flfr
                    WPol3Plus10_weight_flfr        = ROOT.GetWeightWjetsPolarizationF0(genp4_W_,genp4_l_,+10,1);
                    WPol3Minus10_weight_flfr        = ROOT.GetWeightWjetsPolarizationF0(genp4_W_,genp4_l_,-10,1);
                    s.weightWPol3Plus10=s.weight*WPol3Plus10_weight_flfr
                    s.weightWPol3Minus10=s.weight*WPol3Minus10_weight_flfr
  #                    print "Wplus ", plus, chmode, W_weight_flfr
                  if minus:
                    WPol1Plus10_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,10,0);
                    WPol1Minus10_weight_flfr       = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,-10,0);
                    s.weightWPol1Plus10 = s.weight*WPol1Plus10_weight_flfr
                    s.weightWPol1Minus10 = s.weight*WPol1Minus10_weight_flfr
  #                    print "Wplus ", plus, chmode, Wminus_weight_flfr
                    WPol2MinusPlus5_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,5,0);
                    WPol2MinusMinus5_weight_flfr        = ROOT.GetWeightWjetsPolarizationFLminusFR(genp4_W_,genp4_l_,-5,0);
                    s.weightWPol2MinusPlus5= s.weight*WPol2MinusPlus5_weight_flfr
                    s.weightWPol2MinusMinus5= s.weight*WPol2MinusMinus5_weight_flfr
  #                    print "Wplus ", plus, chmode, Wminus_weight_flfr
                    WPol3Plus10_weight_flfr        = ROOT.GetWeightWjetsPolarizationF0(genp4_W_,genp4_l_,+10,0);
                    WPol3Minus10_weight_flfr        = ROOT.GetWeightWjetsPolarizationF0(genp4_W_,genp4_l_,-10,0);
                    s.weightWPol3Plus10=s.weight*WPol3Plus10_weight_flfr
                    s.weightWPol3Minus10=s.weight*WPol3Minus10_weight_flfr
  #                    print "Wplus ", plus, chmode, W_weight_flfr

  #                print "weightWPol1Plus10      reweight", s.weightWPol1Plus10/s.weight
  #                print "weightWPol1Minus10     reweight", s.weightWPol1Minus10/s.weight
  #                print "weightWPol2PlusPlus5   reweight", s.weightWPol2PlusPlus5/s.weight
  #                print "weightWPol2PlusMinus5  reweight", s.weightWPol2PlusMinus5/s.weight
  #                print "weightWPol2MinusPlus5  reweight", s.weightWPol2MinusPlus5/s.weight
  #                print "weightWPol2MinusMinus5 reweight", s.weightWPol2MinusMinus5/s.weight
  #                print "weightWPol3Plus10      reweight", s.weightWPol3Plus10/s.weight
  #                print "weightWPol3Minus10     reweight", s.weightWPol3Minus10/s.weight
            if chmode=="copyMET":
              mceff = getMCEfficiencyForBTagSF(c, onlyLightJetSystem = True, sms="")
              s.probOneMoreBTag   = 1 - getTagWeightDict(mceff["mceffs"], 0)[0]
              s.probOneMoreBTagSF = 1 - getTagWeightDict(mceff["mceffs_SF"], 0)[0]
#            print bin, s.njets, s.probOneMoreBTag, s.probOneMoreBTagSF  
            if (not mode=="HT") and ("Run" not in bin):
              zeroTagWeight = 1.
              mceff = getMCEfficiencyForBTagSF(c, sms=sms)
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
              if not separateBTagWeights:
                for i in range(1, maxConsideredBTagWeight+1):
                  exec("s.weightBTag"+str(i)+"p=s.weight")
                  exec("s.weightBTag"+str(i)+"p_SF=s.weight")
                  exec("s.weightBTag"+str(i)+"p_SF_b_Up=s.weight")
                  exec("s.weightBTag"+str(i)+"p_SF_b_Down=s.weight")
                  exec("s.weightBTag"+str(i)+"p_SF_light_Up=s.weight")
                  exec("s.weightBTag"+str(i)+"p_SF_light_Down=s.weight")
                for i in range(maxConsideredBTagWeight+1):
                  exec("s.weightBTag"+str(i)+"="+str(mceffW[i]*s.weight))
                  exec("s.weightBTag"+str(i)+"_SF="+str(mceffW_SF[i]*s.weight))
                  exec("s.weightBTag"+str(i)+"_SF_b_Up="+str(mceffW_SF_b_Up[i]*s.weight))
                  exec("s.weightBTag"+str(i)+"_SF_b_Down="+str(mceffW_SF_b_Down[i]*s.weight))
                  exec("s.weightBTag"+str(i)+"_SF_light_Up="+str(mceffW_SF_light_Up[i]*s.weight))
                  exec("s.weightBTag"+str(i)+"_SF_light_Down="+str(mceffW_SF_light_Down[i]*s.weight))
                  for j in range(i+1, maxConsideredBTagWeight+1):
                    exec("s.weightBTag"+str(j)+"p               -="+str(mceffW[i]*s.weight))
                    exec("s.weightBTag"+str(j)+"p_SF            -="+str(mceffW_SF[i]*s.weight))
                    exec("s.weightBTag"+str(j)+"p_SF_b_Up       -="+str(mceffW_SF_b_Up[i]*s.weight))
                    exec("s.weightBTag"+str(j)+"p_SF_b_Down     -="+str(mceffW_SF_b_Down[i]*s.weight))
                    exec("s.weightBTag"+str(j)+"p_SF_light_Up   -="+str(mceffW_SF_light_Up[i]*s.weight))
                    exec("s.weightBTag"+str(j)+"p_SF_light_Down -="+str(mceffW_SF_light_Down[i]*s.weight))
  #                print "s.weightBTag"+str(i)+""              , eval("s.weightBTag"+str(i)+"")
  #                print "s.weightBTag"+str(i)+"_SF"           , eval("s.weightBTag"+str(i)+"_SF")
  #                print "s.weightBTag"+str(i)+"_SF_b_Up"      , eval("s.weightBTag"+str(i)+"_SF_b_Up")
  #                print "s.weightBTag"+str(i)+"_SF_b_Down"    , eval("s.weightBTag"+str(i)+"_SF_b_Down")
  #                print "s.weightBTag"+str(i)+"_SF_light_Up"  , eval("s.weightBTag"+str(i)+"_SF_light_Up")
  #                print "s.weightBTag"+str(i)+"_SF_light_Down", eval("s.weightBTag"+str(i)+"_SF_light_Down")
  #                if i>0:
  #                  print "s.weightBTag"+str(i)+"p"              , eval("s.weightBTag"+str(i)+"p")
  #                  print "s.weightBTag"+str(i)+"p_SF"           , eval("s.weightBTag"+str(i)+"p_SF")
  #                  print "s.weightBTag"+str(i)+"p_SF_b_Up"      , eval("s.weightBTag"+str(i)+"p_SF_b_Up")
  #                  print "s.weightBTag"+str(i)+"p_SF_b_Down"    , eval("s.weightBTag"+str(i)+"p_SF_b_Down")
  #                  print "s.weightBTag"+str(i)+"p_SF_light_Up"  , eval("s.weightBTag"+str(i)+"p_SF_light_Up")
  #                  print "s.weightBTag"+str(i)+"p_SF_light_Down", eval("s.weightBTag"+str(i)+"p_SF_light_Down")
                for i in range (int(s.njets)+1, maxConsideredBTagWeight+1):
                  exec("s.weightBTag"+str(i)+"= 0.")
                  exec("s.weightBTag"+str(i)+"_SF= 0.")
                  exec("s.weightBTag"+str(i)+"_SF_b_Up= 0.")
                  exec("s.weightBTag"+str(i)+"_SF_b_Down= 0.")
                  exec("s.weightBTag"+str(i)+"_SF_light_Up= 0.")
                  exec("s.weightBTag"+str(i)+"_SF_light_Down= 0.")
                  exec("s.weightBTag"+str(i)+"p              = 0.")
                  exec("s.weightBTag"+str(i)+"p_SF           = 0.")
                  exec("s.weightBTag"+str(i)+"p_SF_b_Up      = 0.")
                  exec("s.weightBTag"+str(i)+"p_SF_b_Down    = 0.")
                  exec("s.weightBTag"+str(i)+"p_SF_light_Up  = 0.")
                  exec("s.weightBTag"+str(i)+"p_SF_light_Down= 0.")
              if separateBTagWeights:
                inclusiveWeight = s.weight
                weightBTag4p  = inclusiveWeight
                weightBTag4p_SF  = inclusiveWeight
                weightBTag4p_SF_b_Up  = inclusiveWeight
                weightBTag4p_SF_b_Down  = inclusiveWeight
                weightBTag4p_SF_light_Up  = inclusiveWeight
                weightBTag4p_SF_light_Down  = inclusiveWeight
                for i in range(4):
                  s.nbtags = i
                  s.weightBTag = mceffW[i]*inclusiveWeight
                  s.weightBTag_SF = mceffW_SF[i]*inclusiveWeight
                  s.weightBTag_SF_b_Up = mceffW_SF_b_Up[i]*inclusiveWeight
                  s.weightBTag_SF_b_Down = mceffW_SF_b_Down[i]*inclusiveWeight
                  s.weightBTag_SF_light_Up = mceffW_SF_light_Up[i]*inclusiveWeight
                  s.weightBTag_SF_light_Down = mceffW_SF_light_Down[i]*inclusiveWeight
                  t.Fill()
                  weightBTag4p                -= mceffW[i]*inclusiveWeight
                  weightBTag4p_SF             -= mceffW_SF[i]*inclusiveWeight
                  weightBTag4p_SF_b_Up        -= mceffW_SF_b_Up[i]*inclusiveWeight
                  weightBTag4p_SF_b_Down      -= mceffW_SF_b_Down[i]*inclusiveWeight
                  weightBTag4p_SF_light_Up    -= mceffW_SF_light_Up[i]*inclusiveWeight
                  weightBTag4p_SF_light_Down  -= mceffW_SF_light_Down[i]*inclusiveWeight
                s.nbtags = 99
                s.weightBTag                = max(0., weightBTag4p              )
                s.weightBTag_SF             = max(0., weightBTag4p_SF           )
                s.weightBTag_SF_b_Up        = max(0., weightBTag4p_SF_b_Up      )
                s.weightBTag_SF_b_Down      = max(0., weightBTag4p_SF_b_Down    )
                s.weightBTag_SF_light_Up    = max(0., weightBTag4p_SF_light_Up  )
                s.weightBTag_SF_light_Down  = max(0., weightBTag4p_SF_light_Down)
                t.Fill()
#          print s.numBPartons, s.numCPartons
          if not separateBTagWeights:
            t.Fill()
        del elist
      else:
        print "Zero entries in", bin, sample["name"]
      del c
    if (not small):
      f = ROOT.TFile(ofile, "recreate")
      t.Write()
      f.Close()
      print "Written",ofile
    else:
      print "No saving when small!"
    del t
