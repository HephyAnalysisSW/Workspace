import copy, pickle
import ROOT
from simplePlotsCommon import *
from math import *
import os, copy, array, xsec, sys, random, itertools
from xsecSMS import stop8TeV_NLONLL
small = False
outputDir = "/data/schoef/convertedTuples_v13/"

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

def deltaR(l1, l2):
  return sqrt(deltaPhi(l1["phi"], l2["phi"])**2 + (l1["eta"] - l2["eta"])**2)

overwrite = True

doubleMuData={}
doubleMuData["name"]     = "doubleMuData";
doubleMuData["dirname"] = "/data/schoef/pat_120908/data8TeV/"
doubleMuData["bins"]    = [ 'DoubleMu-Run2012A-13Jul2012', 'DoubleMu-Run2012B-13Jul2012', 'DoubleMu-Run2012C-PromptReco', 'DoubleMu-Run2012C-PromptReco-v2']
doubleMuData["Chain"] = "Events"
doubleMuData["Counter"] = "bool_EventCounter_passed_PAT.obj"
doubleEleData={}
doubleEleData["name"]     = "doubleEleData";
doubleEleData["dirname"] = "/data/schoef/pat_120908/data8TeV/"
doubleEleData["bins"]    = [ 'DoubleElectron-Run2012A-13Jul2012', 'DoubleElectron-Run2012B-13Jul2012', 'DoubleElectron-Run2012C-PromptReco', 'DoubleElectron-Run2012C-PromptReco-v2']
doubleEleData["Chain"] = "Events"
doubleEleData["Counter"] = "bool_EventCounter_passed_PAT.obj"
eleMuData={}
eleMuData["name"]     = "eleMuData";
eleMuData["dirname"] = "/data/schoef/pat_120908/data8TeV/"
eleMuData["bins"]    = [ 'MuEG-Run2012A-13Jul2012', 'MuEG-Run2012B-13Jul2012', 'MuEG-Run2012C-PromptReco', 'MuEG-Run2012C-PromptReco-v2']
eleMuData["Chain"] = "Events"
eleMuData["Counter"] = "bool_EventCounter_passed_PAT.obj"

targetLumi = 9200.


def goodMuID(c, imu, cmode):
#  print abs(getVarValue(c, "muonsEta", imu)) , getVarValue(c, "muonsisPF", imu), getVarValue(c, "muonsisGlobal", imu), getVarValue(c, "muonsPFRelIso", imu), getVarValue(c, "muonsNormChi2", imu), getVarValue(c, "muonsNValMuonHits", imu), getVarValue(c, "muonsNumMatchedStadions", imu) , getVarValue(c, "muonsPixelHits", imu) , getVarValue(c, "muonsNumtrackerLayerWithMeasurement", imu) , getVarValue(c, "muonsDxy", imu) , getVarValue(c, "muonsDz", imu)  
#  print  abs(getVarValue(c, "muonsEta", imu)) < 2.4, getVarValue(c, "muonsisPF", imu)>0, getVarValue(c, "muonsisGlobal", imu)>0, getVarValue(c, "muonsPFRelIso", imu)<0.12, getVarValue(c, "muonsNormChi2", imu)<10., getVarValue(c, "muonsNValMuonHits", imu)>0, getVarValue(c, "muonsNumMatchedStadions", imu) > 1, getVarValue(c, "muonsPixelHits", imu) > 0, getVarValue(c, "muonsNumtrackerLayerWithMeasurement", imu) > 5, getVarValue(c, "muonsDxy", imu) < 0.2, getVarValue(c, "muonsDz", imu) < 0.5 
#  return  abs(getVarValue(c, "muonsEta", imu)) < 2.4 and getVarValue(c, "muonsisPF", imu)>0 and getVarValue(c, "muonsisGlobal", imu)>0 and getVarValue(c, "muonsPFRelIso", imu)<0.12 and getVarValue(c, "muonsNormChi2", imu)<10. and getVarValue(c, "muonsNValMuonHits", imu)>0 and getVarValue(c, "muonsNumMatchedStadions", imu) > 1 and getVarValue(c, "muonsPixelHits", imu) > 0 and getVarValue(c, "muonsNumtrackerLayerWithMeasurement", imu) > 5 and getVarValue(c, "muonsDxy", imu) < 0.2 and getVarValue(c, "muonsDz", imu) < 0.5 
  if cmode=="OSDL":  return  getVarValue(c, "muonsPt", imu)>10. and getVarValue(c, "muonsisPF", imu) and getVarValue(c, "muonsisGlobal", imu) and abs(getVarValue(c, "muonsEta", imu)) < 2.4  and getVarValue(c, "muonsPFRelIso", imu)<0.15 and getVarValue(c, "muonsNormChi2", imu)<10. and getVarValue(c, "muonsNValMuonHits", imu)>0 and getVarValue(c, "muonsNumMatchedStadions", imu) > 1 and getVarValue(c, "muonsPixelHits", imu) > 0 and getVarValue(c, "muonsNumtrackerLayerWithMeasurement", imu) > 5 and getVarValue(c, "muonsDxy", imu) < 0.02 and getVarValue(c, "muonsDz", imu) < 0.1 

def goodEleID(c, iele, cmode, eta = "none"):
  if eta=="none":
    eta = getVarValue(c, "elesEta", iele)
  sietaieta = getVarValue(c, "elesSigmaIEtaIEta", iele)
  dphi = getVarValue(c, "elesDPhi", iele)
  deta = getVarValue(c, "elesDEta", iele)
  HoE = getVarValue(c, "elesHoE", iele)
  isEB = abs(eta)<1.4442
  isEE = abs(eta)>1.566
  relIso = getVarValue(c, "elesPfRelIso", iele) 
  pt = getVarValue(c, "elesPt", iele)
  relIsoCut = 0.15
  if isEE and pt<20:
    relIsoCut = 0.10
#  print  getVarValue(c, "elesPt", iele), ( isEE or isEB),  getVarValue(c, "elesOneOverEMinusOneOverP", iele), getVarValue(c, "elesPfRelIso", iele), getVarValue(c, "elesPassConversionRejection", iele),\
#    HoE, sietaieta, getVarValue(c, "elesMissingHits", iele), dphi, deta, getVarValue(c, "elesDxy", iele), getVarValue(c, "elesDz", iele),"relIsoCut", relIsoCut
  if cmode=="OSDL": return  pt>10. and ( isEE or isEB) and getVarValue(c, "elesOneOverEMinusOneOverP", iele)< 0.05\
    and ( relIso<relIsoCut )  and getVarValue(c, "elesPassConversionRejection", iele)>0  and (abs(eta)<2.4)\
    and ( (isEB and HoE < 0.12 ) or (isEE and HoE < 0.10))\
    and ( (isEB and sietaieta < 0.01 ) or (isEE and sietaieta < 0.03)) and getVarValue(c, "elesMissingHits", iele) <=1\
    and ( (isEB and dphi<0.15) or (isEE and dphi<0.10)) and ( (isEB and deta<0.007) or (isEE and deta<0.009))  and getVarValue(c, "elesDxy", iele) < 0.02 and getVarValue(c, "elesDz", iele) < 0.1 

def getGoodMuons(c, nmuons, cmode):
  res=[]
  for i in range(0, int(nmuons)):
    if goodMuID(c, i, cmode):
      res.append({"pt":getVarValue(c, "muonsPt", i),"eta":getVarValue(c, "muonsEta", i), "phi":getVarValue(c, "muonsPhi", i), "pdg":getVarValue(c, "muonsPdg", i), "relIso":getVarValue(c, "muonsPFRelIso", i)})
  res = sorted(res, key=lambda k: -k['pt']) 
  return res

def getGoodElectrons(c, neles, cmode):
  res=[]
  for i in range(0, int(neles)):
    eta = getVarValue(c, "elesEta", i)
    if goodEleID(c, i, cmode, abs(eta)):
      res.append({"pt":getVarValue(c, "elesPt", i),"eta":eta, "phi":getVarValue(c, "elesPhi", i), "pdg":getVarValue(c, "elesPdg", i), "relIso":getVarValue(c, "elesPfRelIso", i)} )
  res = sorted(res, key=lambda k: -k['pt']) 
  return res

def getGoodLeptons(c, nmuons, neles, cmode):
  res={}
  res["muons"] = getGoodMuons(c,nmuons,cmode)
  res["electrons"] = getGoodElectrons(c, neles, cmode)
  leptons = res["muons"] + res["electrons"]
  res["leptons"] = leptons
  return res

def getBestLeptonPair(allLeptons, chmode):
  if len(allLeptons)<2:
    return [] 
  cands = list(itertools.combinations(allLeptons, 2))
  goodCands=[]
  for cand in cands:
    sumPt = cand[0]["pt"]+cand[1]["pt"]
    if chmode=="doubleMu"  and abs(cand[0]["pdg"])==13 and abs(cand[1]["pdg"])==13 and cand[0]["pdg"]+cand[1]["pdg"]==0:
      goodCands.append([cand, sumPt])
    if chmode=="doubleEle" and abs(cand[0]["pdg"])==11 and abs(cand[1]["pdg"])==11 and cand[0]["pdg"]+cand[1]["pdg"]==0:
      goodCands.append([cand, sumPt])
    if chmode=="eleMu"      and ( (abs(cand[0]["pdg"])==11 and abs(cand[1]["pdg"])==13) or (abs(cand[0]["pdg"])==13 and abs(cand[1]["pdg"])==11)) and abs(cand[0]["pdg"]+cand[1]["pdg"])==2:
      goodCands.append([cand, sumPt])
  goodCands = sorted(goodCands, key=lambda k: -k[1]) 
  if not len(goodCands)>0:
    return []
  goodCand = goodCands[0][0]
#  if len(goodCands)>1:
#    print "\n", c.GetLeaf(c.GetAlias('run')).GetValue(), c.GetLeaf(c.GetAlias('lumi')).GetValue(), long(c.GetLeaf(c.GetAlias('event')).GetValue())
#    print goodCands
#    print "selected:",sorted(goodCand, key=lambda k: -k['pt'])
  return sorted(goodCand, key=lambda k: -k['pt'])

def getGoodJets(c, crosscleanobjects):
  njets = getVarValue(c, "nsoftjets")
  res=[]
  ht = 0.
  nbtags = 0
  for i in range(int(njets)):
    eta = getVarValue(c, "jetsEta", i)
    pt  = getVarValue(c, "jetsPt", i)
    if abs(eta)<3.0 and getVarValue(c, "jetsID", i) and pt>40.:
      phi = getVarValue(c, "jetsPhi", i)
      jet = {"pt":pt, "eta":eta,"phi":phi}
      isolated = True
      for obj in crosscleanobjects:
        if deltaR(jet, obj)<0.4:
          isolated = False
#          print "Not this one!", jet, obj, deltaR(jet, obj)
          break
      if isolated:
        ht+=jet["pt"]
        btag = getVarValue(c, "jetsBtag", i)
        jet["btag"] = btag
        res.append(jet) 
        if btag>=0.679:
          nbtags = nbtags+1
  res= sorted(res, key=lambda k: -k['pt'])
#  print res
  return res, ht, nbtags


chainstring = "empty"
reweightingHistoFile = "reweightingHisto_Summer2012Private.root"
#reweightingHistoFile = "reweightingHisto_Summer2012-53X.root"

variables = ["weight", "run","lumi", "met",  "ht", "genmet", "genmetpx","genmetpy", \
  "njets", "nbtags",  "nvetoMuons", "nvetoElectrons", "ngoodMuons", "ngoodElectrons", "ngoodVertices",
  "metiso"]

extraVariables=[ "mLL", "jet0pt", "jet1pt", "jet2pt", "jet3pt", "deltaRLL", "ptZ", "jzb", "pdg1", "pdg2", "phi1", "phi2", "pt1", "pt2", "eta1", "eta2", "relIso1", "relIso2", "minLepMetIso", "mbb", "minJetsMetIso", "minbJetsMetIso", "mbl", "minLepbJetIso", "minLepJetIso", "deltaPhibb", "deltaRbb", "deltaEtabb", "deltaPhiLL", "deltaRLL", "deltaEtaLL", "minDeltaHT", "mbl1MinDeltaHT", "mbl2MinDeltaHT", "mllbb", "nLep", "btag0pt", "btag1pt", "type1met"]


def getVarValue(c, var, n=0):
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  else:
    return float('nan')

structString = "struct MyStruct{ULong_t event;"
for var in variables:
  structString +="Float_t "+var+";"

for var in extraVariables:
  structString +="Float_t "+var+";"

structString   +="};"
ROOT.gROOT.ProcessLine(structString)

from ROOT import MyStruct

s = MyStruct()

#rwHisto = ""
#if globals().has_key("reweightingHistoFile"):
#  if reweightingHistoFile!="":
#    rf = ROOT.TFile(reweightingHistoFile)
#    htmp = rf.Get("ngoodVertices_Data")
#    ROOT.gDirectory.cd("PyROOT:/")
#    rwHisto = htmp.Clone()
#    rf.Close()
#    print "Using reweightingHisto", reweightingHistoFile, rwHisto
#
#if rwHisto == "":
#  print "Don't use nvtx reweighting"

def getReweightingHisto(filename=""):
  if filename=="":
    return ""
  rf = ROOT.TFile(filename)
  htmp = rf.Get("ngoodVertices_Data")
  ROOT.gDirectory.cd("PyROOT:/")
  rwHisto = htmp.Clone()
  rf.Close()
  return rwHisto


#from defaultMu2012Samples import dy, dy_m20, wjetsInc, ttbar, ttbarS6,  stop, getSignal
#for sample in [dy, wjetsInc, ttbar, ttbarS6,  stop]:
#  sample["reweightingHistoFile"] = "reweightingHisto_Summer2012Private.root"
#ttbarS6["reweightingHistoFile"] = "reweightingHisto_Summer2012-S6.root"
#TMMe532Samples = []
#TMMe532 = {}
#for msq in [200, 300, 400, 500, 600, 700, 800]:
#  TMMe532[msq]= {}
#  for mN in [100]:
#    TMMe532[msq][mN]= {}
#    TMMe532[msq][mN]["bins"] = ["TMMe532_v6"]
#    TMMe532[msq][mN]["dirname"] = "/data/walten/excess/"
#    TMMe532[msq][mN]["name"] = "TMMe532_"+str(msq)+"_"+str(mN)
#    TMMe532[msq][mN]["additionalCut"] = "(msq=="+str(msq)+"&&mN=="+str(mN)+"&&mC=="+str(mN+70)+")"
#    TMMe532[msq][mN]["reweightingHistoFile"] = ""
#    TMMe532[msq][mN]["Chain"] = "Events"
#    TMMe532Samples.append(TMMe532[msq][mN])


#T6bbzzBv1Samples = []
#T6bbzzBv1 = {}
#for msq in [250, 300, 350, 400, 450]:
#  T6bbzzBv1[msq]= {}
#  for mN in [50, 100, 150, 200]:
##  for mN in [ 50,100,150,200,250,300]:
#    if msq - mN>= 100:
#      T6bbzzBv1[msq][mN]= {}
#      T6bbzzBv1[msq][mN]["bins"] = ["T6bbzzB_v1"]
#      T6bbzzBv1[msq][mN]["dirname"] = "/data/walten/excess/"
#      T6bbzzBv1[msq][mN]["name"] = "T6bbzzBv1_"+str(msq)+"_"+str(mN)
#      T6bbzzBv1[msq][mN]["additionalCut"] = "(msq=="+str(msq)+"&&mN=="+str(mN)+"&&mC=="+str(mN+70)+")"
#      T6bbzzBv1[msq][mN]["reweightingHistoFile"] = ""
#      T6bbzzBv1[msq][mN]["Chain"] = "Events"
#      T6bbzzBv1Samples.append(T6bbzzBv1[msq][mN])

T6bbzzEv2Samples = []
T6bbzzEv2 = {}
#for msq in [200, 250, 300, 350, 400, 450, 500, 550, 600]:
for msq in [175]:
  T6bbzzEv2[msq]= {}
#  for mN in [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]:
  for mN in [0]:
    if msq - mN >= 100:
      T6bbzzEv2[msq][mN]= {}
      T6bbzzEv2[msq][mN]["bins"] = ["T6bbzzE_v2"]
      T6bbzzEv2[msq][mN]["dirname"] = "/data/walten/excess/"
      T6bbzzEv2[msq][mN]["name"] = "T6bbzzEv2_"+str(msq)+"_"+str(mN)
      T6bbzzEv2[msq][mN]["additionalCut"] = "(msq=="+str(msq)+"&&mN=="+str(mN)+"&&mC=="+str(mN+70)+")"
#      T6bbzzEv2[msq][mN]["additionalCut"] = "(1)"
      T6bbzzEv2[msq][mN]["reweightingHistoFile"] = ""
      T6bbzzEv2[msq][mN]["Chain"] = "Events"
      T6bbzzEv2Samples.append(T6bbzzEv2[msq][mN])

#for mode in ["lowMET", "highMET"]:
for mode in ["highMET", "lowMET"]:
  for cmode in ["OSDL"] :
#    for chmode in ["eleMu"]:
    for chmode in ["doubleMu", "doubleEle", "eleMu"]:
#      allSamples = [dy,  wjetsInc, ttbar, ttbarS6,   stop]
#      allSamples = []#T6bbzzEv2Samples
      allSamples = T6bbzzEv2Samples 
#      if chmode == "doubleMu":
#        allSamples.append(doubleMuData)
#      if chmode == "doubleEle":
#        allSamples.append(doubleEleData)
#      if chmode == "eleMu":
#        allSamples.append(eleMuData)
       

      for sample in allSamples:
        sample["filenames"]={}
        sample["weight"]={}
        for bin in sample["bins"]:
          subdirname = sample["dirname"]+"/"+bin+"/"
          if sample["bins"]==[""]:
            subdirname = sample["dirname"]+"/"
          c = ROOT.TChain("Events")
          d = ROOT.TChain("Runs")
          sample["filenames"][bin]=[]
          if small:
            filelist=os.listdir(subdirname)
            counter = 20   #Joining n files
            for tfile in filelist:
              if os.path.isfile(subdirname+tfile) and tfile[-5:]==".root" and tfile.count("histo")==1:
                sample["filenames"][bin].append(subdirname+tfile)
      #          c.Add(sample["dirname"]+tfile)
                if counter==0:
                  break
                counter=counter-1
          else:
            sample["filenames"][bin] = [subdirname+"/h*.root"]
          for tfile in sample["filenames"][bin]:
            c.Add(tfile)
            d.Add(tfile)
          nevents = 0
          nruns = d.GetEntries()
          for i in range(0, nruns):
            d.GetEntry(i)
            nevents += getValue(d,"uint_EventCounter_runCounts_PAT.obj")
          weight = 1.
          if bin == "T6bbzz_v5" or bin == "T6bbzzE_v2" or bin=="T6bbzzB_v1":
            msq = int(sample["name"].split("_")[1])
            mN = int(sample["name"].split("_")[2])
            xsec.xsec[bin] = stop8TeV_NLONLL[msq]
            nevents = c.GetEntries("msq=="+str(msq)+"&&mN=="+str(mN))
            print "Using xsec",stop8TeV_NLONLL[msq],"for",bin,T6bbzzEv2[msq][mN]["name"], "nevents", nevents
          xbin = bin.replace('-pdf', '')
          if xsec.xsec.has_key(xbin):
            if nevents>0:
              weight = xsec.xsec[xbin]*targetLumi/nevents
            else:
              weight = 0.
          print "Sample", sample["name"], "mode", mode, "cmode", cmode, "bin", bin, "n-events",nevents,"weight",weight
          sample["weight"][bin]=weight
          del c
          del d

      presel = "None"
      prefixString = ""
      commoncf = "0"
      if mode=="lowMET":
        commoncf =  "(barepfmet>100||met>100)"
      if mode=="highMET":
        commoncf =  "(barepfmet>150||met>150)"
      if chmode=="doubleMu":
        commoncf+="&&nmuons>=2"
      if chmode=="doubleEle":
        commoncf+="&&neles>=2"
      if chmode=="eleMu":
        commoncf+="&&neles+nmuons>=2"
      print "mode",mode, "cmode", cmode, "chmode", chmode, sample["name"], "commoncf", commoncf

      if not os.path.isdir(outputDir+"/"+cmode+"_"+chmode):
        os.system("mkdir "+outputDir+"/"+cmode+"_"+chmode)
      if not os.path.isdir("mkdir "+outputDir+"/"+cmode+"_"+chmode+"/"+mode):
        os.system("mkdir "+outputDir+"/"+cmode+"_"+chmode+"/"+mode)
      else:
        print "Directory", outputDir+"/"+cmode+"_"+chmode+"/"+mode, "already found"
      for sample in allSamples:
        if not os.path.isdir("mkdir "+outputDir+"/"+cmode+"_"+chmode+"/"+mode+"/"+sample["name"]):
          os.system("mkdir "+outputDir+"/"+cmode+"_"+chmode+"/"+mode+"/"+sample["name"])
        else:
          print "Directory", outputDir+"/"+cmode+"_"+chmode+"/"+mode, "already found"
        t = ROOT.TTree( "Events", "Events", 1 )
        t.Branch("event", ROOT.AddressOf(s, "event"), "event/l")
        for var in variables:
          t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
        for var in extraVariables:
          t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
        ofile = outputDir+"/"+cmode+"_"+chmode+"/"+mode+"/"+sample["name"]+"/histo_"+sample["name"]+".root"
        if os.path.isfile(ofile) and overwrite:
          print "Warning! will overwrite",ofile
        if os.path.isfile(ofile) and not overwrite:
          print ofile, "already there! Skipping!!!" 
          continue
        rwHisto = ""
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
          if ntot>0:
            thiscommoncf = commoncf
            if sample.has_key("additionalCut"):
              thiscommoncf = commoncf+"&&"+sample["additionalCut"]
            c.Draw(">>eList", thiscommoncf)
            elist = ROOT.gDirectory.Get("eList")
            number_events = elist.GetN()
            print "Reading: ", sample["name"], bin, "with",number_events,"Events using cut", thiscommoncf
            if small:
              if number_events>100000:
                number_events=100000
            for i in range(0, number_events):
              if (i%10000 == 0) and i>0:
                print i
        #      # Update all the Tuples
              if elist.GetN()>0 and ntot>0:
                c.GetEntry(elist.GetEntry(i))
                nvtxWeight = 1.
                if rwHisto!="" and xsec.xsec.has_key(bin):
                  nvtxWeight = rwHisto.GetBinContent(rwHisto.FindBin(getVarValue(c, "ngoodVertices")))
        #                print "nvtx:", c.GetLeaf( "ngoodVertices" ).GetValue(), "bin", rwHisto.FindBin(c.GetLeaf( "ngoodVertices" ).GetValue()),"weight",nvtxWeight
                for var in variables[1:]:
                  getVar = var
                  if prefixString!="":
                    getVar = prefixString+"_"+var
                  exec("s."+var+"="+str(getVarValue(c, getVar)).replace("nan","float('nan')"))
#                if bin.count("Run"):
#                  if not checkLumi(s.run, s.lumi):
#  #                  print s.run, s.lumi
#                    continue
                s.weight  = sample["weight"][bin]*nvtxWeight
                s.met = c.GetLeaf(c.GetAlias('barepfmet')).GetValue()
                s.event = long(c.GetLeaf(c.GetAlias('event')).GetValue())

                for var in extraVariables:
                  exec("s."+var+"=float('nan')")

                s.type1met = c.GetLeaf(c.GetAlias('met')).GetValue()
                nmuons = getVarValue(c, "nmuons")
                neles = getVarValue(c, "neles")
                if (chmode=="doubleMu" and nmuons>=2) or (chmode=="doubleEle" and neles>=2) or (chmode=="eleMu" and nmuons>=1 and neles>=1):
                  allGoodLeptons = getGoodLeptons(c, nmuons, neles, cmode)
                  goodJets , s.ht, s.nbtags = getGoodJets(c, allGoodLeptons["leptons"])
#                  print s.ht, c.GetLeaf(c.GetAlias('ht')).GetValue(), s.nbtags, c.GetLeaf(c.GetAlias('nbtags')).GetValue()
                  s.njets = len(goodJets)
#                  print s.njets, s.nbtags, s.ht
                  mhtpx, mhtpy = 0., 0.
                  for j,jet in enumerate(goodJets):
                    mhtpx -= jet["pt"]*cos(jet["phi"])
                    mhtpy -= jet["pt"]*sin(jet["phi"])
                    if j<4:
                      exec("s.jet"+str(j)+"pt="+str(jet["pt"]))
                  s.mht = sqrt(mhtpx**2 + mhtpy**2)
                  leptonPair = []
                  if chmode=="doubleMu":  leptonPair = getBestLeptonPair(allGoodLeptons["muons"], chmode) 
                  if chmode=="doubleEle": leptonPair = getBestLeptonPair(allGoodLeptons["electrons"], chmode)
                  if chmode=="eleMu":     leptonPair = getBestLeptonPair(allGoodLeptons["leptons"], chmode)
#                  if len(allGoodLeptons) >=2 and ((mode=="highMET" and allGoodLeptons[0]["pt"]>20.) or (mode=="lowMET" and allGoodLeptons[1]["pt"]>20.))\
                  if len(leptonPair) >=2 and ((mode=="highMET" and leptonPair[0]["pt"]>20. and leptonPair[1]["pt"]>10.) or (mode=="lowMET" and leptonPair[1]["pt"]>20.)):
                    l1 = leptonPair[0]; l2 = leptonPair[1];
                    s.nLep = len(allGoodLeptons["leptons"])
                    s.deltaRLL = deltaR(l1, l2)
                    px1 = l1["pt"]*cos(l1["phi"]);  px2 = l2["pt"]*cos(l2["phi"])
                    py1 = l1["pt"]*sin(l1["phi"]);  py2 = l2["pt"]*sin(l2["phi"])
                    pz1 = l1["pt"]*sinh(l1["eta"]); pz2 = l2["pt"]*sinh(l2["eta"])
                    px = px1+px2 
                    py = py1+py2
                    pz = pz1+pz2
                    s.ptZ = sqrt(px*px + py* py)
                    p1 = sqrt(px1*px1+py1*py1+pz1*pz1)
                    p2 = sqrt(px2*px2+py2*py2+pz2*pz2)
                    p = sqrt(px*px+py*py+pz*pz) 
                    s.mLL = sqrt((p1 + p2)*(p1 + p2) - p*p)

                    s.jzb = getVarValue(c, "mht") - s.ptZ
                    s.pdg1 = l1["pdg"]
                    s.pdg2 = l2["pdg"]
                    s.phi1 = l1["phi"]
                    s.phi2 = l2["phi"]
                    s.eta1 = l1["eta"]
                    s.eta2 = l2["eta"]
                    s.pt1 = l1["pt"]
                    s.pt2 = l2["pt"]
                    s.relIso1 = l1["relIso"]
                    s.relIso2 = l2["relIso"]
                    metPhi = getVarValue(c, "rawMetphi")
                    s.deltaPhiLL = deltaPhi(l1["phi"], l2["phi"])
                    s.deltaEtaLL = l1["eta"] - l2["eta"] 
                    s.deltaRLL = sqrt(s.deltaPhiLL**2 + s.deltaEtaLL**2)
                    s.minLepMetIso = minAbsPiMinusDeltaPhi(metPhi,[l1["phi"], l2["phi"]])
                    jetPhis=[]
                    bjetPhis=[]
                    bjetEtas=[]
                    bjets3Vec = []
                    bjets = []
                    for jet in goodJets:
                      jetPhis.append(jet["phi"])
                      if jet["btag"]>=0.679:
                        bjetPhis.append(jet["phi"])
                        bjetEtas.append(jet["eta"])
                        px = jet["pt"]*cos(jet["phi"]); 
                        py = jet["pt"]*sin(jet["phi"]); 
                        pz = jet["pt"]*sinh(jet["eta"]);
                        bjets3Vec.append([px, py, pz])
                        bjets.append(jet)
                    if len(bjets)>0:
                      s.btag0pt = bjets[0]["pt"] 
                    if len(bjets)>1:
                      s.btagpt = bjets[1]["pt"] 
                    if len(bjets3Vec)>0:
                      s.mbl = invMassOfLightObjects(bjets3Vec[0], [px1, py1, pz1]) #Mass of the hardest b-jet and the hardes lepton
                    s.minLepbJetIso = min(minAbsDeltaPhi(l1["phi"], bjetPhis) , minAbsDeltaPhi(l2["phi"], bjetPhis))
                    s.minLepJetIso = min(minAbsDeltaPhi(l1["phi"], jetPhis) , minAbsDeltaPhi(l2["phi"], jetPhis))
                    if len(bjets3Vec)>1:
                      s.mbb = invMassOfLightObjects(bjets3Vec[0], bjets3Vec[1]) 
                      s.deltaPhibb = deltaPhi(bjetPhis[0], bjetPhis[1])
                      s.deltaEtabb = bjetEtas[0] - bjetEtas[1]
                      s.deltaRbb = sqrt(s.deltaPhibb**2 + s.deltaEtabb**2) 

                      pairL1B0 = True
                      deltaHT1 = abs((s.pt1 + sqrt(bjets3Vec[0][0]**2 + bjets3Vec[0][1]**2)) - (s.pt2 + sqrt(bjets3Vec[1][0]**2 + bjets3Vec[1][1]**2)))
                      deltaHT2 = abs((s.pt2 + sqrt(bjets3Vec[0][0]**2 + bjets3Vec[0][1]**2)) - (s.pt1 + sqrt(bjets3Vec[1][0]**2 + bjets3Vec[1][1]**2)))
                      s.minDeltaHT = deltaHT1
                      if deltaHT1>deltaHT2:
                        pairL1B0 = False
                        s.minDeltaHT = deltaHT2 
                      if pairL1B0:
                        s.mbl1MinDeltaHT = invMassOfLightObjects(bjets3Vec[0], [px1, py1, pz1]) 
                        s.mbl2MinDeltaHT = invMassOfLightObjects(bjets3Vec[1], [px2, py2, pz2])
                      else:
                        s.mbl1MinDeltaHT = invMassOfLightObjects(bjets3Vec[1], [px1, py1, pz1]) 
                        s.mbl2MinDeltaHT = invMassOfLightObjects(bjets3Vec[0], [px2, py2, pz2])
                      Ellbb = sqrt(bjets3Vec[0][0]**2 + bjets3Vec[0][1]**2 +  bjets3Vec[0][2]**2) + sqrt(bjets3Vec[1][0]**2 + bjets3Vec[1][1]**2 +  bjets3Vec[1][2]**2) + sqrt(px1**2 + py1**2 + pz1**2) + sqrt(px2**2 + py2**2 + pz2**2)
                      pxllbb = bjets3Vec[0][0] + bjets3Vec[1][0] + px1 + px2
                      pyllbb = bjets3Vec[0][1] + bjets3Vec[1][1] + py1 + py2
                      pzllbb = bjets3Vec[0][2] + bjets3Vec[1][2] + pz1 + pz2
                      s.mllbb = sqrt(Ellbb**2 - pxllbb**2 - pyllbb**2 - pzllbb**2) 
 
                    s.minJetsMetIso =   minAbsPiMinusDeltaPhi(metPhi, jetPhis) 
                    s.minbJetsMetIso =  minAbsDeltaPhi(metPhi, bjetPhis)
#                    print "mbb", s.mbb, "phibb", s.phibb, "minJetsMetIso", s.minJetsMetIso , "minbJetsMetIso", s.minbJetsMetIso, "mbl", s.mbl, "minLepbJetIso", s.minLepbJetIso, "minLepJetIso", s.minLepJetIso
#                      print s.deltaPhiLL, s.deltaEtaLL , s.deltaRLL, s.deltaPhibb, s.deltaEtabb, s.deltaRbb
                    
#                    print "allgoodmuons", allGoodLeptons
#                    print "s.ptZ", s.ptZ, "s.mLL", s.mLL, "s.jzb",s.jzb
          
                t.Fill() 
            del elist
          else:
            print "Zero entries in", bin, sample["name"]
          del c
        if not small:
          f = ROOT.TFile(ofile, "recreate")
          t.Write()
          f.Close()
          print "Written",ofile
        else:
          print "No saving when small!"
        del t
