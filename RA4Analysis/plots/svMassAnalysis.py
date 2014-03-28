import copy, pickle
import ROOT
from Workspace.RA4Analysis.simplePlotsCommon import *
from math import *
import os, copy, array, xsec, sys, random
for path in [os.path.abspath(p) for p in ['../../HEPHYPythonTools/python/']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from xsecSMS import gluino8TeV_NLONLL
from btagEff import getMCEff, getTagWeightDict, getSF
from random import randint

small = True


overwrite = False

maxConsideredBTagWeight = 4


from defaultMu2012Samples import ttbarPowHeg as Mu_ttbarPowHeg
Mu_ttbarPowHeg["bins"]=["8TeV-TTJets-powheg-v1"] #FIXME
from defaultMu2012Samples import ttzJets as Mu_ttzJets
from defaultMu2012Samples import ttwJets as Mu_ttwJets
from defaultMu2012Samples import wjetsCombined as Mu_wjetsCombined
from defaultMu2012Samples import dy as Mu_dy
from defaultMu2012Samples import qcd as Mu_qcd
from defaultMu2012Samples import stop as Mu_stop
from defaultMu2012Samples import singleLeptonData as Mu_data
from defaultEle2012Samples import ttbarPowHeg as Ele_ttbarPowHeg
Ele_ttbarPowHeg["bins"]=["8TeV-TTJets-powheg-v1"]#FIXME
from defaultEle2012Samples import ttzJets as Ele_ttzJets
from defaultEle2012Samples import ttwJets as Ele_ttwJets
from defaultEle2012Samples import wjetsCombined as Ele_wjetsCombined
from defaultEle2012Samples import dy as Ele_dy
from defaultEle2012Samples import qcd as Ele_qcd
from defaultEle2012Samples import stop as Ele_stop
from defaultEle2012Samples import singleLeptonData as Ele_data
samples = {}
samples["Ele"] = {"mc":[Ele_ttbarPowHeg, Ele_ttzJets, Ele_ttwJets, Ele_wjetsCombined, Ele_dy, Ele_qcd, Ele_stop], "data": [Ele_data]}
samples["Mu"]  = {"mc":[Mu_ttbarPowHeg, Mu_ttzJets, Mu_ttwJets, Mu_wjetsCombined, Mu_dy, Mu_qcd, Mu_stop], "data": [Mu_data]}
if small:
  samples["Ele"] = {"mc":[Ele_ttbarPowHeg, Ele_ttzJets, Ele_ttwJets ], "data": [Ele_data]}
  samples["Mu"]  = {"mc":[Mu_ttbarPowHeg,  Mu_ttzJets, Mu_ttwJets   ], "data": [Mu_data]}

targetLumi = 12000.
samples["Ele"]["data"][0]["bins"] = ["SingleElectron-Run2012A-13Jul2012","SingleElectron-Run2012B-13Jul2012","SingleElectron-Run2012C-Aug24ReReco","SingleElectron-Run2012C-PromptReco-v2"]
samples["Mu"]["data"][0]["bins"] = ["SingleMu-Run2012A-13Jul2012","SingleMu-Run2012B-13Jul2012","SingleMu-Run2012C-Aug24ReReco","SingleMu-Run2012C-PromptReco-v2"]

nvtxReweightingVar = "nTrueGenVertices"
for s in samples["Ele"]["mc"]+samples["Mu"]["mc"]+samples["Ele"]["data"]+samples["Mu"]["data"]:
  s["dirname"] = "/data/schoef/pat_130517/"
for s in samples["Ele"]["mc"]+samples["Mu"]["mc"]:
  if targetLumi == 12000.:
    s["reweightingHistoFile"]          = "PU/reweightingHisto_Summer2012-S10-Run2012ABC_60max_true_pixelcorr_Sys0.root"
  if targetLumi == 19400:
    s["reweightingHistoFile"]          = "PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_Sys0.root"

print "Using lumi", targetLumi,"Run2012ABC(D)"


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
  res= sorted(res, key=lambda k: -k['pt'])
  resb= sorted(resb, key=lambda k: -k['btag'])
#  print res
  if not jes=="0":
    return res, resb, {"delta_met_x":delta_met_x, "delta_met_y":delta_met_y, "deltaHT":deltaHT}
  else:
    return res, resb


for sample in samples["Mu"]["mc"]+samples["Ele"]["mc"] + samples["Mu"]["data"] + samples["Ele"]["data"]:
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

hadronicCut =   "(type1phiMet>100&&type1phiMet<150.)&&njets==6&&nbtags>=2"

for mode in ["Mu", "Ele"]:
  commoncf = "-1"
  print "Mode:", mode

  if mode=="Mu":
    commoncf = hadronicCut+"&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0&&leptonPt>30."
  if mode=="Ele":
    commoncf = hadronicCut+"&&singleElectronic&&nvetoMuons==0&&nvetoElectrons==1&&leptonPt>30"

  for isample, sample in enumerate(samples[mode]["mc"] + samples[mode]["data"]):
    rwHisto=""
    if sample.has_key("reweightingHistoFile"):
      rwHisto=getReweightingHisto(sample["reweightingHistoFile"])

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
            nvtxWeight = 1.
            if rwHisto!="" and xsec.xsec.has_key(bin):
              nvtxWeight = rwHisto.GetBinContent(rwHisto.FindBin(getVarValue(c, nvtxReweightingVar)))
            scaleFac = 1.
            if sample.has_key("scaleFac"):
              if sample["scaleFac"].has_key(bin):
                scaleFac = sample["scaleFac"][bin]
            weight            = scaleFac*sample["weight"][bin]*nvtxWeight
            event = long(c.GetLeaf(c.GetAlias('event')).GetValue())
            targetLumi = targetLumi
            weightLumi = scaleFac*sample["weight"][bin]
            #xsec = sample["xsec"][bin]
            print event, targetLumi,weightLumi,weight

            jets, bjets = getGoodJets(c)
            print jets, bjets
#          if not separateBTagWeights:
#            t.Fill()
        del elist
      else:
        print "Zero entries in", bin, sample["name"]
      del c
#    if (not small):
#      f = ROOT.TFile(ofile, "recreate")
#      t.Write()
#      f.Close()
#      print "Written",ofile
#    else:
#      print "No saving when small!"
#    del t
