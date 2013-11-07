import copy, pickle
import ROOT
from simplePlotsCommon import *
from math import *
import os, copy, array, xsec, sys, random
for path in [os.path.abspath(p) for p in ['../../HEPHYCommonTools/python/']]:
  if not path in sys.path:
      sys.path.insert(1, path)

from xsecSMS import gluino8TeV_NLONLL
from btagEff import getMCEff, getTagWeightDict, getSF

ROOT.gROOT.ProcessLine(".L polSys/WPolarizationVariation.C+")
ROOT.gROOT.ProcessLine(".L polSys/TTbarPolarization.C+")

small = False
outputDir = "/data/adamwo/convertedTuples_v15/"

def partonName (parton):
  if parton==5:  return 'b'
  if parton==4:  return 'c'
  return 'other'

mode = "Mu"
#mode = "Ele"

#mode = "HT"
#chmode = "copy"

overwrite = False

maxConsideredBTagWeight = 4

chmodes = [\
#      "chmode = 'copy6j'",
#      "chmode = 'copy4j'",

         "chmode = 'copyMET'",
#         "chmode = 'copyMET_JES+'",
#         "chmode = 'copyMET_JES-'",
#         "chmode = 'copyMET_separateBTagWeights'",

#         "chmode = 'copyMETmod2'",
#         "chmode = 'copy2JleptVeto'",
#         "chmode = 'copyTotal'",
#          "chmode = 'JER'",
#          "chmode = 'PDF_0'",
      ]


if len(sys.argv)>1:
  mode = sys.argv[1]
mNLow = 450
mNHigh = 475
if len(sys.argv)>3:
  mNLow = int(sys.argv[2])
  mNHigh = int(sys.argv[3])

# run root in batch mode
sys.argv.append("-b")

commoncf = "(-1)"
chainstring = "empty"

if mode == "Mu":
  from defaultMu2012Samples import *

if mode == "Ele":
  from defaultEle2012Samples import *

if mode == "HT":
  from defaultHad2012Samples import *

targetLumi = 20000.
print targetLumi

nvtxReweightingVar = "nTrueGenVertices"
if mode=="Ele" or mode=="Mu":
#  allSamples = [ttbarPowHeg, ttbar, dy, wjets, wjetsInc, stop, qcd]
  allSamples = [ wjetsInc ]
  for sample in allSamples:
    sample["reweightingHistoFile"]          = "PU/reweightingHisto_Summer2012-S7-Run2012ABC-PromptReco_JSONForSUSY_Sys0.root"
    sample["reweightingHistoFileSysPlus"]   = "PU/reweightingHisto_Summer2012-S7-Run2012ABC_60max_true_pixelcorr_SysPlus5.root"
    sample["reweightingHistoFileSysMinus"]  = "PU/reweightingHisto_Summer2012-S7-Run2012ABC_60max_true_pixelcorr_SysMinus5.root"
#  allSamples.append(data)
#  allSamples = [ data ]
#  allSamples = [ ]
  
##for sample in [ttbar, ttbarPowHeg]:
for sample in [ wjetsInc ]:
    sample["reweightingHistoFile"]          = "PU/reweightingHisto_Summer2012-S10-Run2012ABC-PromptReco_JSONForSUSY_Sys0.root"
    sample["reweightingHistoFileSysPlus"]   = "PU/reweightingHisto_Summer2012-S10-Run2012ABC_60max_true_pixelcorr_SysPlus5.root"
    sample["reweightingHistoFileSysMinus"]  = "PU/reweightingHisto_Summer2012-S10-Run2012ABC_60max_true_pixelcorr_SysMinus5.root"

if mode=="HT":
  allSamples = [HTdata, qcdHad]
  qcdHad["reweightingHistoFile"] = "PU/reweightingHisto_Summer2012-S10-Run2012ABC-PromptReco_JSONForSUSY.root" 

T1ttttSamples = []
T1tttt = {}
if mNLow>=0 and mNHigh>=0:
  print "Mode:",mode, "mNLow:",mNLow,"mNHigh",mNHigh
  for mN in range( mNLow, mNHigh, 25):
    for mgl in range(mN + 350, 2020, 25):
#    for mgl in range(mN + 350, mN+450, 25):
      if not T1tttt.has_key(mgl):
        T1tttt[mgl]={}
      T1tttt[mgl][mN]= {}
      T1tttt[mgl][mN]["bins"] = ["8-TeV-T1tttt"]
      T1tttt[mgl][mN]["dirname"] = "/data/mhickel/pat_121012/sms/"
      T1tttt[mgl][mN]["name"] = "T1tttt_"+str(mgl)+"_"+str(mN)
      T1tttt[mgl][mN]["filelist"] = "sms_"+T1tttt[mgl][mN]["bins"][0]+"_files.lis"
      T1tttt[mgl][mN]["elistfile"] = "sms_"+T1tttt[mgl][mN]["bins"][0]+"_entries.root"
      T1tttt[mgl][mN]["elistname"] = "T1tttt_"+str(mgl)+"_"+str(mN)
      T1tttt[mgl][mN]["additionalCut"] = "(osetMgl=="+str(mgl)+"&&osetMN=="+str(mN)+")"
      T1tttt[mgl][mN]["reweightingHistoFile"]          = "PU/reweightingHisto_Summer2012-S7-Run2012ABC-PromptReco_JSONForSUSY_Sys0.root"
      T1tttt[mgl][mN]["reweightingHistoFileSysPlus"]   = "PU/reweightingHisto_Summer2012-S7-Run2012ABC_60max_true_pixelcorr_SysPlus5.root"
      T1tttt[mgl][mN]["reweightingHistoFileSysMinus"]  = "PU/reweightingHisto_Summer2012-S7-Run2012ABC_60max_true_pixelcorr_SysMinus5.root"
#      T1tttt[mgl][mN]["reweightingHistoFile"] = ""#Don't want to loose stats
      T1tttt[mgl][mN]["Chain"] = "Events"
      T1ttttSamples.append(T1tttt[mgl][mN])
  allSamples = T1ttttSamples
 
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

for sample in allSamples:
  sample["filenames"]={}
  sample["weight"]={}
  sample["xsec"]={}
  print sample["bins"]
  for bin in sample["bins"]:
    sample["xsec"][bin] = -1.
    subdirname = sample["dirname"]+"/"+bin+"/"
    if sample["bins"]==[""]:
      subdirname = sample["dirname"]+"/"
    print "Starting with sample "+sample["name"]+" , "+subdirname
    c = ROOT.TChain("Events")
    d = ROOT.TChain("Runs")
    sample["filenames"][bin]=[]
    if small:
      filelist=os.listdir(subdirname)
      counter = 3   #Joining n files
      for fname in filelist:
        if os.path.isfile(subdirname+fname) and fname[-5:]==".root" and fname.count("histo")==1:
          sample["filenames"][bin].append(subdirname+fname)
#          c.Add(sample["dirname"]+fname)
          if counter==0:
            break
          counter=counter-1
    else:
      if "filelist" in sample:
        sample["filenames"][bin] = [ ]
#        print sample["filelist"]
        for line in file(sample["filelist"]):
          sample["filenames"][bin].append(line[:-1])
        print "Used filelist option, #files = ",len(sample["filenames"][bin])
      else:
        sample["filenames"][bin] = [subdirname+"/h*.root"]
    weight = 1.
    if bin == "8-TeV-T1tttt":
      mgl = int(sample["name"].split("_")[1])
      mN = int(sample["name"].split("_")[2])
      xsec.xsec[bin] = gluino8TeV_NLONLL[mgl]
#      nevents = c.GetEntries("osetMgl=="+str(mgl)+"&&osetMN=="+str(mN))
      felist = ROOT.TFile(sample["elistfile"])
      elist = felist.Get("elist_"+str(mgl)+"_"+str(mN))
      nevents = elist.GetN()
      felist.Close()
      T1tttt[mgl][mN]["xsec"][bin] = xsec.xsec[bin] 
      T1tttt[mgl][mN]["xsec"][bin] = xsec.xsec[bin] 
      print "Using xsec",gluino8TeV_NLONLL[mgl],"for",bin,T1tttt[mgl][mN]["name"], "nevents", nevents
    else:
      for fname in sample["filenames"][bin]:
        d.Add(fname)
      nevents = 0
      nruns = d.GetEntries()
      for i in range(0, nruns):
        d.GetEntry(i)
        nevents += getValue(d,"uint_EventCounter_runCounts_PAT.obj")

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
    hadronicCut =   "(met>100||genmet>100)"
  if chmode=="copyMETmod2": 
    hadronicCut =   "(event%2==1)&&(met>100||genmet>100)"
  if chmode=="copyInc":
    hadronicCut="(1)"
  if mode=="Mu":
    commoncf = hadronicCut+"&&ngoodMuons>0"
  if mode=="Ele":
    commoncf = hadronicCut+"&&ngoodElectrons>0"
  if mode=="HT":
    if chmode=="copy2JleptVeto":
      commoncf = "jet1pt>40&&nvetoMuons==0&&nvetoElectrons==0"
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

  prevFiles = None
  prevElist = None
  c = None
  for isample, sample in enumerate(allSamples):
    if not os.path.isdir("mkdir "+outputDir+"/"+chmode+"/"+mode+"/"+sample["name"]):
      os.system("mkdir "+outputDir+"/"+chmode+"/"+mode+"/"+sample["name"])
    else:
      print "Directory", outputDir+"/"+chmode+"/"+mode, "already found"

    variables = []
    extraVariables=["mbb", "mbl", "phibb"]
    if mode=="Ele" or mode=="Mu":
      variables = ["weight",  "weightPUSysPlus", "weightPUSysMinus", "targetLumi", "xsec", "weightLumi", "run", "lumi", "met", "type1phiMet", "metpx", "metpy", "metphi", "mT", "barepfmet" ,"ht", "btag0", "btag1", "btag2", "btag3","rawMetpx", "rawMetpy", "m3", "mht", "singleMuonic", "singleElectronic", \
      "leptonPt", "leptonEta", "leptonPhi", "leptonPdg", "njets", "nbtags", "nbjets", "jet0pt", "jet1pt", "jet2pt", "jet3pt", "nvetoMuons", "nvetoElectrons", "ngoodMuons", "ngoodElectrons", "ngoodVertices",
      "btag0pt", "btag1pt", "btag2pt", "btag3pt", "btag0eta", "btag1eta", "btag2eta", "btag3eta"]
      MC_variables =  ["genmet", "genmetpx","genmetpy", "btag0parton", "btag1parton", "btag2parton", "btag3parton",\
                       "antinuMu", "antinuE", "antinuTau", "nuMu", "nuE", "nuTau", "nuMuFromTausFromWs", "nuEFromTausFromWs", "nuTauFromTausFromWs", "weightTTPolPlus5", "weightTTPolMinus5", "weightTTxsecPlus30", "weightTTxsecMinus30",
                       "weightDiLepPlus15", "weightDiLepMinus15", "weightTauPlus15", "weightTauMinus15"]
      if mNLow>=0 and mNHigh>=0:
        MC_variables += ["osetMgl", "osetMN"]
      if bin.count("Run")==0:
        variables+=MC_variables 
        if True or sample["name"].lower().count("wjets"):
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
      variables = ["weight",  "weightPUSysPlus", "weightPUSysMinus", "run", "lumi", "met", "metpx", "metpy" ,"ht", "btag0", "btag1", "btag2", "btags3", "nbtags", "njets", "jet0pt", "jet1pt", "jet2pt", "jet3pt", "ngoodVertices", "rawMetpx", "rawMetpy" , "nvetoMuons", "nvetoElectrons"]
      alltriggers =  [  "HLTHT200", "HLTHT250", "HLTHT300", "HLTHT350", "HLTHT400", "HLTHT450", "HLTHT500", "HLTHT550", "HLTHT600", "HLTHT650", "HLTHT700", "HLTHT750"]
      for trigger in alltriggers:
        variables.append(trigger)
        variables.append(trigger.replace("HLT", "pre") )
      extraVariables = []

    structString = "struct MyStruct_"+str(nc)+"_"+str(isample)+"{ULong64_t event;"
    for var in variables:
      structString +="Float_t "+var+";"
    for var in extraVariables:
      structString +="Float_t "+var+";"
    structString   +="};"
    ROOT.gROOT.ProcessLine(structString)

    exec("from ROOT import MyStruct_"+str(nc)+"_"+str(isample))
    exec("s = MyStruct_"+str(nc)+"_"+str(isample)+"()")

#    print "gDirectory 1"
#    ROOT.gDirectory.ls()
    t = ROOT.TTree( "Events", "Events", 1 )
#    print t.GetDirectory()
    t.Branch("event",   ROOT.AddressOf(s,"event"), 'event/l')
    for var in variables:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
    for var in extraVariables:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
#    print "gDirectory 2"
#    ROOT.gDirectory.ls()
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
      number_events = 0
      if prevFiles==None or prevFiles!=sample["filenames"][bin]:
        print "Creating new chains and elists"
        if prevElist!=None:  del prevElist
        if c!=None:  del c
        c = ROOT.TChain(sample["Chain"])
        for thisfile in sample["filenames"][bin]:
          c.Add(thisfile)
        if bin.count("T1tttt")>0:
          ntot = 999999999
        else:
          ntot = c.GetEntries()
        if bin.count("Run")!=0: commoncf = commoncf.replace("||genmet>100", "")
        thiscommoncf = commoncf
#        if sample.has_key("additionalCut"):
#          thiscommoncf = commoncf+"&&"+sample["additionalCut"]

        if ntot>0:
          c.Draw(">>eList", thiscommoncf)
          prevElist = ROOT.gDirectory.Get("eList")
          number_events = prevElist.GetN()
          print "Reading: ", sample["name"], bin, "with",number_events,"Events using cut", thiscommoncf

        prevFiles = sample["filenames"][bin]
      
#      print "gDirectory 3"
#      ROOT.gDirectory.ls()
#      for rfile in ROOT.gROOT.GetListOfFiles():
#        print "Root file ",rfile.GetName()
      if ntot>0:
        print sample.keys()
        if "elistfile" in sample:
          print "Found elistfile ",sample["elistfile"]
          tokens = sample["name"].split("_")
          ef = ROOT.TFile(sample["elistfile"])
          elistSMS = ef.Get("elist_"+tokens[1]+"_"+tokens[2])
          print "elistSMS nEntries = ",elistSMS.GetN()
#          elist = prevElist.Clone()
          elist = prevElist.Clone()
          elist.SetDirectory(ROOT.gROOT)
          print "elist nEntries (before) = ",elist.GetN()
          elist.Intersect(elistSMS)
          ef.Close()
          number_events = elist.GetN()
          print "elist nEntries (after) = ",elist.GetN()
        print type(elist),number_events
        if small:
          if number_events>1000:
            number_events=1000
        for i in range(0, number_events):
          if (i%1000 == 0) and i>0 :
            print "At event ",i," out of ",number_events
#            print "gDirectory 3"
#            ROOT.gDirectory.ls()
#            for rfile in ROOT.gROOT.GetListOfFiles():
#              print "Root file ",rfile.GetName()
#            print "          ---"
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
            s.weight  = sample["weight"][bin]*nvtxWeight
            s.weightPUSysPlus  = sample["weight"][bin]*nvtxWeightSysPlus
            s.weightPUSysMinus  = sample["weight"][bin]*nvtxWeightSysMinus
            s.event = long(c.GetLeaf(c.GetAlias('event')).GetValue())
            s.targetLumi = targetLumi
            s.weightLumi = sample["weight"][bin]
            s.xsec = sample["xsec"][bin]
#            print s.xsec, s.weightLumi, s.targetLumi
            if len(extraVariables)>0:
              for var in extraVariables:
                exec("s."+var+"=float('nan')")
              pxLep = s.leptonPt*cos( s.leptonPhi) 
              pyLep = s.leptonPt*sin( s.leptonPhi) 
              pzLep = s.leptonPt*sinh(s.leptonEta)
              bjets = []
              bjetPhis = []
              for i in range(int(s.njets)):
                if getVarValue(c, "jetsBtag",i)>=0.679:
                  jetPhi = getVarValue(c, "jetsPhi",i)
                  jetEta = getVarValue(c, "jetsEta",i)
                  jetPt = getVarValue(c, "jetsPt",i)
                  px = jetPt*cos(jetPhi);
                  py = jetPt*sin(jetPhi);
                  pz = jetPt*sinh(jetEta);
                  bjets.append([px, py, pz])
                  bjetPhis.append(jetPhi)
              if len(bjets)>0:
                s.mbl = invMassOfLightObjects(bjets[0], [pxLep, pyLep, pzLep]) #Mass of the hardest b-jet and the hardes lepton
              if len(bjets)>1:
                s.mbb = invMassOfLightObjects(bjets[0], bjets[1])
                s.phibb = deltaPhi(bjetPhis[0], bjetPhis[1])
  #            print len(bjets), s.mbl, s.mbb, s.phibb 
#            if s.njets < len(getGoodJets(c, "-")[0]):
#              print "\n"
#              print "WARNING"
#              print s.njets, len(getGoodJets(c, "0")[0]), len(getGoodJets(c, "+")[0]), len(getGoodJets(c, "-")[0])
#              print s.jet0pt, s.jet1pt, s.jet2pt, s.jet3pt, "\n",getGoodJets(c, "0"),"\n",getGoodJets(c, "+"),"\n",getGoodJets(c, "-")
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

            if chmode[:3]=="PDF":
              xbin = bin.replace('-pdf', '')
              n = int(chmode.split("_")[1])
              reweight = c.GetLeaf("floats_pfRA4Tupelizer_pdfWeights_PAT.obj").GetValue(n) / pdfMeans[xbin][mode][n]
              if reweight ==0.:
                print "Warning! found weight 0 in pdf reweighting. Wrong root version (GetValue(n) problem) ?"
              s.weight*=reweight
#              print n, c.GetLeaf("floats_pfRA4Tupelizer_pdfWeights_PAT.obj").GetValue(n), pdfMeans[xbin][mode][n], reweight


            if "Run" not in bin:
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

              s.weightTTPolPlus5 = s.weight
              s.weightTTPolMinus5 = s.weight
              s.weightTTxsecPlus30  = s.weight
              s.weightTTxsecMinus30 = s.weight
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
              if sample["name"].lower().count("wjets"):
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
  #                if chmode[4]=="1":

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
            if "Run" not in bin:
#              trueBJets = getTrueBJets(c)
#              print trueBJets

              mceffs = tuple()
              mceffs_SF = tuple()
              mceffs_SF_b_Up = tuple()
              mceffs_SF_b_Down = tuple()
              mceffs_SF_light_Up = tuple()
              mceffs_SF_light_Down = tuple()
              zeroTagWeight = 1.
              for i in range(0, int(getVarValue(c, "nsoftjets"))):
                jPt     = getVarValue(c, "jetsPt", i) 
                jEta    = getVarValue(c, "jetsEta", i) 
                jParton = getVarValue(c, "jetsParton", i) 
#                eff = 0.9-min(5,i)*0.1#getEfficiencyAndMistagRate(jPt, jEta, jParton )
                if jPt<=40. or abs(jEta)>=2.4 or (not getVarValue(c, "jetsEleCleaned", i)) or (not getVarValue(c, "jetsMuCleaned", i)) or (not getVarValue(c, "jetsID", i)):
                  continue
                r = getMCEff(parton=jParton, pt=jPt, eta=jEta, year=2012)#getEfficiencyAndMistagRate(jPt, jEta, jParton )
                if bin.count("T1tttt")==0:
                  mceffs += (r["mcEff"],)
                  mceffs_SF += (r["mcEff"]*r["SF"],)
                  if abs(jParton)==5 or abs(jParton)==4:
                    mceffs_SF_b_Up   += (r["mcEff"]*r["SF_up"],)
                    mceffs_SF_b_Down += (r["mcEff"]*r["SF_down"],)
                    mceffs_SF_light_Up   += (r["mcEff"]*r["SF"],)
                    mceffs_SF_light_Down += (r["mcEff"]*r["SF"],)
                  else:
                    mceffs_SF_b_Up   += (r["mcEff"]*r["SF"],)
                    mceffs_SF_b_Down += (r["mcEff"]*r["SF"],)
                    mceffs_SF_light_Up   += (r["mcEff"]*r["SF_up"],)
                    mceffs_SF_light_Down += (r["mcEff"]*r["SF_down"],)
                else:
                  fsim_SF = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"mean",jEta)
                  fsim_SF_up = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"up",jEta)
                  fsim_SF_down = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"down",jEta)
#                  print "Correcting SF for jet pt ",jPt," , parton ",jParton," with ",fsim_SF,fsim_SF_up,fsim_SF_down
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
#              print
#              print "mceffs              ", mceffs
#              print "mceffs_SF           ", mceffs_SF
#              print "mceffs_SF_b_Up      ", mceffs_SF_b_Up
#              print "mceffs_SF_b_Down    ", mceffs_SF_b_Down
#              print "mceffs_SF_light_Up  ", mceffs_SF_light_Up
#              print "mceffs_SF_light_Down", mceffs_SF_light_Down
              mceffW                  = getTagWeightDict(mceffs, maxConsideredBTagWeight)
              mceffW_SF               = getTagWeightDict(mceffs_SF, maxConsideredBTagWeight)
              mceffW_SF_b_Up        = getTagWeightDict(mceffs_SF_b_Up, maxConsideredBTagWeight)
              mceffW_SF_b_Down      = getTagWeightDict(mceffs_SF_b_Down, maxConsideredBTagWeight)
              mceffW_SF_light_Up    = getTagWeightDict(mceffs_SF_light_Up, maxConsideredBTagWeight)
              mceffW_SF_light_Down  = getTagWeightDict(mceffs_SF_light_Down, maxConsideredBTagWeight)
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
          if not separateBTagWeights:
            t.Fill()
        del elist
      else:
        print "Zero entries in", bin, sample["name"]
#      del c
    if not small:
      f = ROOT.TFile(ofile, "recreate")
      t.Write()
      f.Close()
      print "Written",ofile
    else:
      print "No saving when small!"
    del t
