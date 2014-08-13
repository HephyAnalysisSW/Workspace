import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy, random
from datetime import datetime
#from helpers import getVarValue, deltaPhi, minAbsDeltaPhi,  deltaR, invMass,
from Workspace.HEPHYPythonTools.helpers import getVarValue, deltaPhi, minAbsDeltaPhi, invMassOfLightObjects, deltaR, closestMuJetDeltaR, invMass,  findClosestObjectDR
from objectSelection import getLooseEleStage1,getAllElectronsStage1, tightPOGEleID, vetoEleID, getLooseMuStage1, getAllMuonsStage1, tightPOGMuID, vetoMuID, getAllTausStage1, getTauStage1

from stage1Tuples import *

from Workspace.HEPHYPythonTools.xsec import xsec
xsec['testBin']=100.
xsec['ttbarCSA14']=100.
xsec['tmp']=100.

subDir = "convertedTuples_v23"

overwrite = True
target_lumi = 2000 #pb-1

from localInfo import username
outputDir = "/data/"+username+"/"+subDir+"/"

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--chmode", dest="chmode", default="copyInc", type="string", action="store", help="chmode: What to do.")
#parser.add_option("--jermode", dest="jermode", default="none", type="string", action="store", help="jermode: up/down/central/none")
#parser.add_option("--jesmode", dest="jesmode", default="none", type="string", action="store", help="jesmode: up/down/none")
parser.add_option("--samples", dest="allsamples", default="testSample", type="string", action="store", help="samples:Which samples.")
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")
parser.add_option("--fromPercentage", dest="fromPercentage", default="0", type="int", action="store", help="from (% of tot. events)")
parser.add_option("--toPercentage", dest="toPercentage", default="100", type="int", action="store", help="to (% of tot. events)")
parser.add_option("--keepPDFWeights", dest="keepPDFWeights", action="store_true", help="keep PDF Weights?")
 
(options, args) = parser.parse_args()
options.small=True
print "options: chmode",options.chmode, 'samples',options.allsamples
exec('allSamples=['+options.allsamples+']')

#def getPtISR(e):
#    sumtlv = ROOT.TLorentzVector(1.e-9,1.e-9,1.e-9,1.e-9)
#    for igp in range(e.ngp):
#        if(abs(e.gpPdg[igp])==1000021 and e.gpSta[igp]==3):
#            tlvaux = ROOT.TLorentzVector(0.,0.,0.,0.)
#            tlvaux.SetPtEtaPhiM(e.gpPt[igp],e.gpEta[igp],e.gpPhi[igp],e.gpM[igp])
#            sumtlv += tlvaux
#    return sumtlv.Pt()
  
def getGoodJets(c, crosscleanobjects):#, jermode=options.jermode, jesmode=options.jesmode):
  njets = getVarValue(c, 'nJets')   # jet.pt() > 10.
  res = []
  bres = []
  ht = 0.
  met_dx = 0.
  met_dy = 0.
#  if jesmode.lower()!="none":
#    if jesmode.lower()=='up':
#      sign=+1
#    if jesmode.lower()=='down':
#      sign=-1
#    delta_met_x_unclustered = getVarValue(c, 'deltaMETxUnclustered')
#    delta_met_y_unclustered = getVarValue(c, 'deltaMETyUnclustered')
#    met_dx+=0.1*delta_met_x_unclustered
#    met_dy+=0.1*delta_met_y_unclustered
  for i in range(int(njets)):
    eta = getVarValue(c, 'jetsEta', i)
    pt  = getVarValue(c, 'jetsPt', i)
    unc = getVarValue(c, 'jetsUnc', i)
    id =  getVarValue(c, 'jetsID', i)
    phi = getVarValue(c, 'jetsPhi', i)
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
      parton = int(abs(getVarValue(c, 'jetsParton', i)))
      jet = {'pt':pt, 'eta':eta,'phi':phi, 'pdg':parton,\
      'id':id,
      'chef':getVarValue(c, 'jetsChargedHadronEnergyFraction', i), 'nhef':getVarValue(c, 'jetsNeutralHadronEnergyFraction', i),\
      'ceef':getVarValue(c, 'jetsChargedEmEnergyFraction', i), 'neef':getVarValue(c, 'jetsNeutralEmEnergyFraction', i), 'id':id,\
      'hfhef':getVarValue(c, 'jetsHFHadronEnergyFraction', i), 'hfeef':getVarValue(c, 'jetsHFEMEnergyFraction', i),\
      'muef':getVarValue(c, 'jetsMuonEnergyFraction', i), 'elef':getVarValue(c, 'jetsElectronEnergyFraction', i), 'phef':getVarValue(c, 'jetsPhotonEnergyFraction', i),\
#      'jetCutBasedPUJetIDFlag':getVarValue(c, 'jetsCutBasedPUJetIDFlag', i),'jetMET53XPUJetIDFlag':getVarValue(c, 'jetsMET53XPUJetIDFlag', i),'jetFull53XPUJetIDFlag':getVarValue(c, 'jetsFull53XPUJetIDFlag', i), 
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


## helpers for GenParticle searching and matching
def find(x,lp):
  if x in lp:
    return lp.index(x)
  else:
    return -1


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
      prefix = ""
      if subdirname[0:5] != "/dpm/":
        filelist = os.listdir(subdirname)
      else:
        filelist = []
        p = subprocess.Popen(["dpns-ls "+ subdirname], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
          filelist.append(line[:-1])
#        allFiles = os.popen("rfdir %s | awk '{print $9}'" % (subdirname))
#        for file in allFiles.readlines():
#          print file
#          file = file.rstrip()
#          filelist.append(file)
        prefix = "root://hephyse.oeaw.ac.at/"#+subdirname
      if options.small: filelist = filelist[:1]
      for tfile in filelist:
#        print "Adding",subdirname+tfile
        sample['filenames'][bin].append(subdirname+tfile)
#    if options.allsamples.lower()=='sms':
#      c_ = ROOT.TChain(sample['Chain'])
#      for tfile in sample['filenames'][bin]:
#        print "Adding",prefix+tfile
#        c_.Add(prefix+tfile)
#      nevents = c_.GetEntries(sample['additionalCut'])
#      print nevents,'found with requirement', sample['additionalCut']
#      del c_
#    else:
#    d = ROOT.TChain('Runs')
#    for tfile in sample['filenames'][bin]:
#      d.Add(prefix+tfile)
#    nevents = 0
#    nruns = d.GetEntries()
#    for i in range(0, nruns):
#      d.GetEntry(i)
#      nevents += getVarValue(d,'uint_EventCounter_runCounts_PAT.obj')
#    del d
    c = ROOT.TChain('Events')
    for tfile in sample['filenames'][bin]:
      c.Add(prefix+tfile)
    nevents= c.GetEntries()
    del c
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
#if options.jermode.lower()!='none':
#  outSubDir = outSubDir+"_JER"+options.jermode.lower()
#if options.jesmode.lower()!='none':
#  outSubDir = outSubDir+"_JES"+options.jesmode.lower()
if not os.path.isdir(outputDir+"/"+outSubDir):
  os.system("mkdir "+outputDir+"/"+outSubDir)

nc = 0
for isample, sample in enumerate(allSamples):
  if not os.path.isdir(outputDir+"/"+outSubDir+"/"+sample["name"]):
    os.system("mkdir "+outputDir+"/"+outSubDir+"/"+sample["name"])
  else:
    print "Directory", outputDir+"/"+outSubDir, "already found"

  variables = ["weight", "run", "lumi", "ngoodVertices"]
  if not sample['name'].lower().count('data'):
    variables.extend(["nTrueGenVertices"])#, "puWeight", "puWeightSysPlus", "puWeightSysMinus"])
  extraVariables = ["ngoodMuons","nvetoMuons",'nvetoLeptons',"ngoodElectrons","nvetoElectrons","ngoodTaus","met","metphi","ht"] 
  extraVariables += ["leptonPt", 'leptonEta', 'leptonPhi', 'leptonPdg', 'singleMuonic', 'singleElectronic', 'singleLeptonic']
  extraVariables += ['pfMet', 'pfMetphi','genMet', 'genMetphi']
  jetvars = ["jetPt", "jetEta", "jetPhi", "jetPdg", "jetBtag", "jetChef", "jetNhef", "jetCeef", "jetNeef", "jetHFhef", "jetHFeef", "jetMuef", "jetElef", "jetPhef", "jetUnc"]#, "jetCutBasedPUJetIDFlag","jetFull53XPUJetIDFlag","jetMET53XPUJetIDFlag"
  muvars = ["muPt", "muEta", "muPhi", "muPdg", "muRelIso", "muDxy", "muDz", "muNormChi2", "muNValMuonHits", "muNumMatchedStations", "muPixelHits", "muNumtrackerLayerWithMeasurement", 'muIsGlobal', 'muIsTracker','muIsPF']
  elvars = ["elePt", "eleEta", "elePhi", "elePdg", "eleRelIso", "eleDxy", "eleDz", "eleOneOverEMinusOneOverP", "elePfRelIso", "eleSigmaIEtaIEta", "eleHoE", "eleDPhi", "eleDEta", "eleMissingHits", "elePassPATConversionVeto"]
  tavars = ["tauPt", "tauEta", "tauPhi", "tauPdg", 'tauJetInd', 'tauJetDR']
  if not sample['name'].lower().count('data'):
    extraVariables+=["ngNuEFromW","ngNuMuFromW","ngNuTauFromW"]
    genTauvars = ["gTauPdg", "gTauPt", "gTauEta", "gTauPhi", "gTauMetPar", "gTauMetPerp", "gTauNENu", "gTauNMuNu", 'gTauNTauNu', 'gTauJetInd', 'gTauJetDR', 'gTauTauDR', 'gTauTauInd']
    genLepvars = ["gLepPdg", "gLepPt", "gLepEta", "gLepPhi", 'gLepInd', 'gLepDR']
#  if options.allsamples.lower()=='sms':
#    variables+=['osetMgl', 'osetMN', 'osetMC', 'osetMsq', 'ptISR']
#  if not bin.lower().count('run') and maxConsideredBTagWeight>0:
#    btagVars=[]
#    for i in range(maxConsideredBTagWeight+1):
#      btagVars.append("weightBTag"+str(i)+"")
#      btagVars.append("weightBTag"+str(i)+"_SF")
#      btagVars.append("weightBTag"+str(i)+"_SF_b_Up")
#      btagVars.append("weightBTag"+str(i)+"_SF_b_Down")
#      btagVars.append("weightBTag"+str(i)+"_SF_light_Up")
#      btagVars.append("weightBTag"+str(i)+"_SF_light_Down")
#      if i>0:
#        btagVars.append("weightBTag"+str(i)+"p")
#        btagVars.append("weightBTag"+str(i)+"p_SF")
#        btagVars.append("weightBTag"+str(i)+"p_SF_b_Up")
#        btagVars.append("weightBTag"+str(i)+"p_SF_b_Down")
#        btagVars.append("weightBTag"+str(i)+"p_SF_light_Up")
#        btagVars.append("weightBTag"+str(i)+"p_SF_light_Down")
#    extraVariables+=btagVars
#  if sample['name'].lower().count('ttjets'):
#    extraVariables+=["top0Pt", "top1Pt"]#"topPtWeight"] 

  structString = "struct MyStruct_"+str(nc)+"_"+str(isample)+"{ULong64_t event;"
  structString+="Float_t "+",".join(variables+extraVariables)+";"
  structString +="Int_t nmu, nele, ntau, njets, nbtags,  njetsFailID;"
  structString +="Int_t njetCount, nmuCount, neleCount, ntauCount;"
  for var in jetvars:
    structString +="Float_t "+var+"[30];"
  for var in muvars:
    structString +="Float_t "+var+"[10];"
  for var in elvars:
    structString +="Float_t "+var+"[10];"
  for var in tavars:
    structString +="Float_t "+var+"[10];"
  if not sample['name'].lower().count('data'):
    structString +="Int_t ngTaus, ngLep;"
    for var in genTauvars:
      structString +="Float_t "+var+"[10];"
    for var in genLepvars:
      structString +="Float_t "+var+"[10];"
#  if options.keepPDFWeights:
#    structString +="Float_t cteqWeights[45];Float_t mstwWeights[41];Float_t nnpdfWeights[101];"

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
#  ofile = "histo_"+sample["name"]+postfix+".root"
  if os.path.isfile(ofile) and overwrite:
    print "Warning! will overwrite",ofile
  if os.path.isfile(ofile) and not overwrite:
    print ofile, "already there! Skipping!!!"
    continue
#  f = ROOT.TFile(ofile, "recreate")
  chain_gDir = ROOT.gDirectory.func()
  t = ROOT.TTree( "Events", "Events", 1 )
  t.Branch("event",   ROOT.AddressOf(s,"event"), 'event/l')
  for var in variables:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
  for var in extraVariables:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'/F')
  t.Branch("njets",   ROOT.AddressOf(s,"njets"), 'njets/I')
  t.Branch("nbtags",   ROOT.AddressOf(s,"nbtags"), 'nbtags/I')
  t.Branch("nmu",   ROOT.AddressOf(s,"nmu"), 'nmu/I')
  t.Branch("nele",   ROOT.AddressOf(s,"nele"), 'nele/I')
  t.Branch("ntau",   ROOT.AddressOf(s,"ntau"), 'ntau/I')
  t.Branch("njetsFailID",   ROOT.AddressOf(s,"njetsFailID"), 'njetsFailID/I')
  t.Branch("njetCount",   ROOT.AddressOf(s,"njetCount"), 'njetCount/I')
  t.Branch("neleCount",   ROOT.AddressOf(s,"neleCount"), 'neleCount/I')
  t.Branch("nmuCount",   ROOT.AddressOf(s,"nmuCount"), 'nmuCount/I')
  t.Branch("ntauCount",   ROOT.AddressOf(s,"ntauCount"), 'ntauCount/I')
  for var in jetvars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[njetCount]/F')
  for var in muvars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[nmuCount]/F')
  for var in elvars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[neleCount]/F')
  for var in tavars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[ntauCount]/F')
  if not sample['name'].lower().count('data'):
    t.Branch("ngTaus",   ROOT.AddressOf(s,"ngTaus"), 'ngTaus/I')
    t.Branch("ngLep",   ROOT.AddressOf(s,"ngLep"), 'ngLep/I')
    for var in genTauvars:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'[ngTaus]/F')
    for var in genLepvars:
      t.Branch(var,   ROOT.AddressOf(s,var), var+'[ngLep]/F')
#  if options.keepPDFWeights:
#    t.Branch('cteqWeights',   ROOT.AddressOf(s,'cteqWeights'), 'cteqWeights[45]/F')
#    t.Branch('mstwWeights',   ROOT.AddressOf(s,'mstwWeights'), 'mstwWeights[41]/F')
#    t.Branch('nnpdfWeights',   ROOT.AddressOf(s,'nnpdfWeights'), 'nnpdfWeights[101]/F')
  chain_gDir.cd()

  for bin_ in sample["bins"]:
    commoncf = ""
    if options.chmode=="copyMET":
      commoncf = "slimmedMETs>=100"
    if options.chmode[:7] == "copyInc":
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

    pfMetLabel = ("pfMet")
    pfMetHandle = Handle("vector<reco::PFMET>")

    genMetLabel = ("genMetTrue")
    genMetHandle = Handle("vector<reco::GenMET>")

#    gpLabel = ("packedGenParticles")
#    gpHandle = Handle("vector<pat::PackedGenParticle>")

    gpLabel = ("prunedGenParticles")
    gpHandle = Handle("vector<reco::GenParticle>")

    mclist = []
    for thisfile in sample["filenames"][bin]:
      mclist.append(prefix+thisfile)
    events = Events(mclist)
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
          events.to(elist.GetEntry(i))
          s.weight = sample["weight"][bin]
          for var in variables[1:]:
            getVar = var
            exec("s."+var+"="+str(getVarValue(c, getVar)).replace("nan","float('nan')"))
          s.event = long(c.GetLeaf(c.GetAlias('event')).GetValue())
#          if options.allsamples.lower()=='sms':
#            s.ptISR = getPtISR(s)
#          for var in ['osetMgl', 'osetMN', 'osetMC', 'osetMsq']:
#            print s.event, var, eval('s.'+var)
#          if not sample['name'].lower().count('data'):
#            nvtxWeightSysPlus, nvtxWeightSysMinus, nvtxWeight = 1.,1.,1.
#            if sample.has_key('reweightingHistoFile'): 
#              s.puWeight = s.weight*sample['reweightingHistoFile'].GetBinContent(sample['reweightingHistoFile'].FindBin(s.nTrueGenVertices))
#            if sample.has_key('reweightingHistoFileSysPlus'): 
#              s.puWeightSysPlus = s.weight*sample['reweightingHistoFileSysPlus'].GetBinContent(sample['reweightingHistoFileSysPlus'].FindBin(s.nTrueGenVertices))
#            if sample.has_key('reweightingHistoFileSysMinus'): 
#              s.puWeightSysMinus = s.weight*sample['reweightingHistoFileSysMinus'].GetBinContent(sample['reweightingHistoFileSysMinus'].FindBin(s.nTrueGenVertices))
          for var in extraVariables:
            exec("s."+var+"=float('nan')")

          events.getByLabel(genMetLabel,genMetHandle)
          genMet =genMetHandle.product()
          s.genMet = genMet[0].pt()
          s.genMetphi = genMet[0].phi()
          events.getByLabel(pfMetLabel,pfMetHandle)
          pfMet =pfMetHandle.product()
          s.pfMet = pfMet[0].pt()
          s.pfMetphi = pfMet[0].phi()


#          if sample['name'].lower().count('ttjets') and len(tops)==2: #https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
#            s.top0Pt = tops[0].pt()
#            s.top1Pt = tops[1].pt()
#            s.topPtWeight = sqrt(exp( 0.156 - 0.00137*tops[0].pt())*exp( 0.156 - 0.00137*tops[1].pt()))
          nmuons = getVarValue(c, 'nmuons')   #Number of muons in Muon Vec
          neles  = getVarValue(c, 'neles')    #Number of eles in Ele Vec
          ntaus  = getVarValue(c, 'ntaus')    #Number of eles in Ele Vec
          allGoodElectrons = getAllElectronsStage1(c, neles)
          allGoodTaus = getAllTausStage1(c, ntaus)
          allGoodMuons = getAllMuonsStage1(c,nmuons) #Loose ID without relIso and Dxy<0.02
#          print "muons",nmuons, allGoodMuons, 
#          print "eles", neles, allGoodElectrons, 
#          print "taus", ntaus, allGoodTaus
          electrons = filter(lambda e:tightPOGEleID(e), allGoodElectrons)
          muons = filter(lambda e:tightPOGMuID(e), allGoodMuons)
          taus = allGoodTaus 
          vetoElectrons = filter(lambda e:vetoEleID(e), allGoodElectrons)
          vetoMuons = filter(lambda e:vetoMuID(e), allGoodMuons)
          
          leptons = sorted(electrons+muons, key=lambda k: -k['pt'])
          s.singleLeptonic = len(leptons)==1
          s.singleMuonic = len(leptons)==1 and abs(leptons[0]['Pdg'])==11
          s.singleElectronic = len(leptons)==1 and abs(leptons[0]['Pdg'])==13
          if len(leptons)>0:
            s.leptonPt=leptons[0]['pt']
            s.leptonPhi=leptons[0]['phi']
            s.leptonEta=leptons[0]['eta']
            s.leptonPdg=leptons[0]['Pdg']
 
          s.ngoodMuons = len(muons)
          s.nvetoMuons = len(vetoMuons)
          s.ngoodElectrons = len(electrons)
          s.nvetoElectrons=len(vetoElectrons)
          s.nvetoLeptons=s.nvetoElectrons+s.nvetoMuons
          s.ngoodTaus = len(taus)
          
          jResult = getGoodJets(c,muons+electrons)#, jermode=options.jermode, jesmode=options.jesmode)
          jetResult = jResult['jets']
          s.met = getVarValue(c, 'slimmedMETs')
          s.metphi = getVarValue(c, 'slimmedMETsPhi')
#          met_dx = jResult['met_dx']
#          met_dy = jResult['met_dy']
#          corrMetx = s.met*cos(s.metphi) + met_dx
#          corrMety = s.met*sin(s.metphi) + met_dy
#          s.met     = sqrt(corrMetx**2+corrMety**2)
#          s.metphi  = atan2(corrMety, corrMetx)

          idJets30 = filter(lambda j:j['id'] and j['isolated'], jetResult)
          s.ht = sum([ j['pt'] for j in idJets30])
          s.njets    = len(idJets30)
          s.njetsFailID = len(filter(lambda j:not j['id'] and j['isolated'], jetResult))
          s.nbtags      = len(filter(lambda j:j['btag']>0.679 and abs(j['eta'])<2.4, idJets30))
          s.nmu = len(allGoodMuons)
          s.nele = len(allGoodElectrons)
          s.ntau = len(allGoodTaus)
### MC specific part
          if not sample['name'].lower().count('data'):
            genTaus = []
            genLeps = []
            s.ngNuEFromW=0
            s.ngNuMuFromW=0
            s.ngNuTauFromW=0
            events.getByLabel(gpLabel,gpHandle)
            gps =gpHandle.product()
            lgps = list(gps)
            for igp,gp in enumerate(gps):
              pdgId = abs(gp.pdgId())
              if pdgId==12 or pdgId==14 or pdgId==16:
                if gp.numberOfMothers()>0 and abs(gp.mother(0).pdgId())==24:
                  if pdgId==12:s.ngNuEFromW+=1 
                  if pdgId==14:s.ngNuMuFromW+=1 
                  if pdgId==16:s.ngNuTauFromW+=1
              if pdgId==12 or pdgId==14:
                if not (gp.numberOfMothers()>0  and abs(gp.mother(0).pdgId())==24): continue
                lep = {'pt':gp.pt(),'phi':gp.phi(),'eta':gp.eta(),'Pdg':gp.pdgId(),}
                if pdgId==12:
                  rlep=findClosestObjectDR(allGoodElectrons, {'phi':lep['phi'], 'eta':lep['eta']})
                if pdgId==14:
                  rlep=findClosestObjectDR(allGoodMuons, {'phi':lep['phi'], 'eta':lep['eta']})
                if rlep:
                  lep['gLepDR'] = rlep['deltaR']
                  lep['gLepInd']= rlep['index']
                else:
                  lep['gLepDR'] = float('nan')
                  lep['gLepInd']= -1
                if pdgId==14: 
                  print "allGoodMuons", allGoodMuons
                  print "(g) lep", lep
                  print "r", rlep
                  print

                genLeps.append(lep)
        
              if pdgId==15:
                if not (gp.numberOfMothers()>0  and abs(gp.mother(0).pdgId())==24): continue
                tau = {'pt':gp.pt(),'phi':gp.phi(),'eta':gp.eta(),'Pdg':gp.pdgId(),'gTauNENu':0, 'gTauNMuNu':0, 'gTauNTauNu':0}
                if s.ngNuMuFromW==2:
                  print "Taus?" 
                MEx = 0.
                MEy = 0.
                justARadiation=False
#                tx=gp.px()
#                ty=gp.py() 
                cjet = findClosestObjectDR(idJets30, {'phi':tau['phi'], 'eta':tau['eta']})
                if cjet and cjet['index']<10:
#                  print cjet
                  tau['gTauJetInd']=cjet['index']
                  tau['gTauJetDR']=cjet['deltaR']
                else:
                  tau['gTauJetInd']=-1
                  tau['gTauJetDR']=float('nan')
                ctau = findClosestObjectDR(allGoodTaus, {'phi':tau['phi'], 'eta':tau['eta']})
                if ctau and ctau['index']<10:
                  tau['gTauTauInd']=ctau['index']
                  tau['gTauTauDR']=ctau['deltaR']
                else:
                  tau['gTauTauInd']=-1
                  tau['gTauTauDR']=float('nan')
#                if len(allGoodTaus)>0:
#                  print allGoodTaus, tau,ctau,justARadiation
#                  for id in range(gp.numberOfDaughters()):
#                    gd = gp.daughter(id)
#                    print id, gd.pdgId()
              
                for id in range(gp.numberOfDaughters()):
                  gd = gp.daughter(id)
#                  tx-=gd.px()
#                  ty-=gd.py()
#                  print id, "d",gd.pdgId(),gd.pt()
                  dpdgId = abs(gd.pdgId())
                  if dpdgId==15:
                    justARadiation=True
                    break
                  if dpdgId==12:tau['gTauNENu']+=1
                  if dpdgId==14:tau['gTauNMuNu']+=1
                  if dpdgId==16:tau['gTauNTauNu']+=1
                  if dpdgId==12 or dpdgId==14 or dpdgId==16:
                    MEx+=gd.px()
                    MEy+=gd.py()
                tau['gTauMetPar']=cos(tau['phi'])*MEx+sin(tau['phi'])*MEy
                tau['gTauMetPerp']=cos(tau['phi'])*MEy-sin(tau['phi'])*MEx
#                print tx, ty
                if not justARadiation:
                  genTaus.append(tau)
#              print genTaus
            if s.ngNuMuFromW==2:
              if len(genTaus)>0:print genTaus
####################

          s.njetCount = min(30,s.njets)
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
#            s.jetCutBasedPUJetIDFlag[i] = idJets30[i]['jetCutBasedPUJetIDFlag']
#            s.jetFull53XPUJetIDFlag[i]  = idJets30[i]['jetFull53XPUJetIDFlag']
#            s.jetMET53XPUJetIDFlag[i]   = idJets30[i]['jetMET53XPUJetIDFlag']
#
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
            s.muIsPF[i] = allGoodMuons[i]['IsPF']
#            s.muMT[i]    = sqrt(2.0*s.muPt[i]*s.met*(1-cos(s.muPhi[i] - s.metphi)))
#            if len(idJets30)>0:
#              cjet = findClosestObjectDR(idJets30, {'phi':s.muPhi[i], 'eta':s.muEta[i]})
#              s.muClosestJetDeltaR[i] = cjet['deltaR']
#              s.muClosestJetMass[i] = invMass(cjet['jet'], {'phi':s.muPhi[i], 'pt':s.muPt[i], 'eta':s.muEta[i]})
#            else:
#              s.muClosestJetDeltaR[i] =float('nan') 
#              s.muClosestJetMass[i] =  float('nan') 
#            s.muPBoost3D[i] = pmuboost3d(idJets30, {'pt':s.met, 'phi':s.metphi}, {'phi':s.muPhi[i], 'pt':s.muPt[i], 'eta':s.muEta[i]} )
#            s.muWPt[i] = sqrt( (allGoodMuons[i]['pt']*cos(allGoodMuons[i]['phi']) + s.met*cos(s.metphi))**2\
#                             + (allGoodMuons[i]['pt']*sin(allGoodMuons[i]['phi']) + s.met*sin(s.metphi))**2)
#            s.muIgpMatch[i] = -1
## MC specific part
#            if not sample['name'].lower().count('data'):
#              s.muIgpMatch[i] = assignMuIgp(i,s)
####################
#
          s.neleCount = min(10,s.nele)
          for i in xrange(s.neleCount):
            s.elePt[i] = allGoodElectrons[i]['pt']
            s.eleEta[i] = allGoodElectrons[i]['eta']
            s.elePhi[i] = allGoodElectrons[i]['phi']
            s.elePdg[i] = allGoodElectrons[i]['Pdg']
            s.eleRelIso[i] = allGoodElectrons[i]['relIso']
            s.eleDxy[i] = allGoodElectrons[i]['Dxy']
            s.eleDz[i] = allGoodElectrons[i]['Dz']
            s.eleOneOverEMinusOneOverP[i] = allGoodElectrons[i]['OneOverEMinusOneOverP']
            s.elePfRelIso[i] = allGoodElectrons[i]['relIso']
            s.eleSigmaIEtaIEta[i] = allGoodElectrons[i]['sIEtaIEta']
            s.eleHoE[i] = allGoodElectrons[i]['HoE']
            s.eleDPhi[i] = allGoodElectrons[i]['DPhi']
            s.eleDEta[i] = allGoodElectrons[i]['DEta']
            s.eleMissingHits[i] = allGoodElectrons[i]['MissingHits']
            s.elePassPATConversionVeto[i] = allGoodElectrons[i]['ConvRejection']

#              print "Electron pt's:",i,allGoodElectrons[i]['pt']
          s.ntauCount = min(10,s.ntau)
          for i in xrange(s.ntauCount):
            s.tauPt[i] = allGoodTaus[i]['pt']
            s.tauEta[i] = allGoodTaus[i]['eta']
            s.tauPhi[i] = allGoodTaus[i]['phi']
            s.tauPdg[i] = allGoodTaus[i]['Pdg']
            cjet = findClosestObjectDR(idJets30, {'phi':s.tauPhi[i], 'eta':s.tauEta[i]})
            if cjet and cjet['index']<10:
              s.tauJetInd[i]=cjet['index']
              s.tauJetDR[i]=cjet['deltaR']
            else:
              s.tauJetInd[i]=-1
              s.tauJetDR[i]=float('nan')
          if not sample['name'].lower().count('data'):
            s.ngTaus = min(10,len(genTaus))
            genTaus = sorted(genTaus, key=lambda k: -k['pt'])
            for i in xrange(s.ngTaus):
              s.gTauPt[i]  = genTaus[i]['pt']
              s.gTauEta[i] = genTaus[i]['eta']
              s.gTauPhi[i] = genTaus[i]['phi']
              s.gTauPdg[i] = genTaus[i]['Pdg']
              s.gTauMetPar[i] = genTaus[i]['gTauMetPar'] 
              s.gTauMetPerp[i]= genTaus[i]['gTauMetPerp'] 
              s.gTauNENu[i]   = genTaus[i]['gTauNENu']
              s.gTauNMuNu[i]  = genTaus[i]['gTauNMuNu']
              s.gTauNTauNu[i] = genTaus[i]['gTauNTauNu']
              s.gTauJetInd[i]  = genTaus[i]['gTauJetInd']
              s.gTauJetDR[i]  = genTaus[i]['gTauJetDR']
              s.gTauTauInd[i]  = genTaus[i]['gTauTauInd']
              s.gTauTauDR[i]  = genTaus[i]['gTauTauDR']
            s.ngLep = min(10,len(genLeps))
            genLeps = sorted(genLeps, key=lambda k: -k['pt'])
            for i in xrange(s.ngLep):
              s.gLepPt[i]  = genLeps[i]['pt']
              s.gLepEta[i] = genLeps[i]['eta']
              s.gLepPhi[i] = genLeps[i]['phi']
              s.gLepPdg[i] = genLeps[i]['Pdg']
              s.gLepDR[i]  = genLeps[i]['gLepDR']
              s.gLepInd[i]  = genLeps[i]['gLepInd']
#          if options.keepPDFWeights:
#            for i in range(45):
#              s.cteqWeights[i]=getVarValue(c, 'cteqWeights',i)
#            for i in range(41):
#              s.mstwWeights[i]=getVarValue(c, 'mstwWeights',i)
#            for i in range(101):
#              s.nnpdfWeights[i]=getVarValue(c, 'nnpdfWeights',i)
          tmpDir = ROOT.gDirectory.func()
          chain_gDir.cd()
          t.Fill()
          tmpDir.cd()

#          dbf = ROOT.gDirectory.func()
#          f.cd()
#          print 'before',dbf,'now',ROOT.gDirectory.func(), 'go back to',pyroot_gDir
#          t.Fill()
#          pyroot_gDir.cd()
      del elist
    else:
      print "Zero entries in", bin, sample["name"]
    del c
  if True or not options.small: #FIXME
    f = ROOT.TFile(ofile, "recreate")
    t.Write()
    f.Close()
#    f.cd()
#    t.Write()
#    f.Close()
#    pyroot_gDir.cd()
#    if t:t.IsA().Destructor(t)
    print "Written",ofile
  else:
    print "No saving when small!"
  del t
