import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy, random, subprocess, datetime
#from helpers import getVarValue, deltaPhi, minAbsDeltaPhi,  deltaR, invMass,
from Workspace.HEPHYPythonTools.helpers import getVarValue, deltaPhi, minAbsDeltaPhi, invMassOfLightObjects, deltaR, closestMuJetDeltaR, invMass,  findClosestObjectDR, getFileList
from objectSelection import getLooseEleStage1,getAllElectronsStage1, tightPOGEleID, vetoEleID, getLooseMuStage1, getAllMuonsStage1, tightPOGMuID, vetoMuID, getAllTausStage1, getTauStage1, hybridMuID, getGoodJetsStage1, isIsolated

from stage1Tuples import *

from Workspace.HEPHYPythonTools.xsec import xsec

subDir = "convertedTuples_v24"
newGenMet = False
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
parser.add_option("--samples", dest="allsamples", default="ttJetsCSA1450ns", type="string", action="store", help="samples:Which samples.")
parser.add_option("--DR", dest="DR", default="0.4", type="float", action="store", help="samples:Which samples.")
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")
parser.add_option("--fromPercentage", dest="fromPercentage", default="0", type="int", action="store", help="from (% of tot. events)")
parser.add_option("--toPercentage", dest="toPercentage", default="100", type="int", action="store", help="to (% of tot. events)")
parser.add_option("--keepPDFWeights", dest="keepPDFWeights", action="store_true", help="keep PDF Weights?")
 
(options, args) = parser.parse_args()
print "options: chmode",options.chmode, 'samples',options.allsamples,'DR',options.DR
exec('allSamples=['+options.allsamples+']')

#def getPtISR(e):
#    sumtlv = ROOT.TLorentzVector(1.e-9,1.e-9,1.e-9,1.e-9)
#    for igp in range(e.ngp):
#        if(abs(e.gpPdg[igp])==1000021 and e.gpSta[igp]==3):
#            tlvaux = ROOT.TLorentzVector(0.,0.,0.,0.)
#            tlvaux.SetPtEtaPhiM(e.gpPt[igp],e.gpEta[igp],e.gpPhi[igp],e.gpM[igp])
#            sumtlv += tlvaux
#    return sumtlv.Pt()

for sample in allSamples:
  sample['filenames'] = {}
  sample['weight'] = {}
  for bin in sample['bins']:
    print "Looping over subdir",bin['dir']
    filelist = getFileList(bin['dir'], minAgeDPM=12, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/')
    if options.small: filelist = filelist[:1]
    bin['filenames'] = []
    for tfile in filelist:
      bin['filenames'] = filelist

    c = ROOT.TChain('Events')
    for f in bin['filenames']:
      c.Add(f)
    nevents= c.GetEntries()
    del c
    if bin['dbsName'] and  bin['dbsName'].lower().count('run'):
      weight = 1.
      print 'Sample', sample['name'], 'bin', bin, 'n-events',nevents,'weight',weight, '(is data!)'
    else:
      if nevents>0:
        if bin['dbsName']:
          weight = xsec[bin['dbsName']]*target_lumi/nevents
          bin['xsec']=xsec[bin['dbsName']]
        else:
          print "Warning! Sample ",sample['name'], 'bin',bin, 'has no dbsName! -> Use weight 1.'
          weight=1
          bin['xsec']=float('nan')
      else:
        weight=0
      print 'Sample', sample['name'], 'bin', bin['dbsName'], 'nevents:',nevents,'xsec',bin['xsec'], 'n-events',nevents,'weight',weight
    bin['weight']=weight


if not os.path.isdir(outputDir):
  os.system('mkdir -p '+outputDir)
outSubDir = options.chmode
#outSubDir+='_DR'+str(options.DR)
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
  extraVariables = ["ngoodMuons","nvetoMuons",'nHybridLooseMuons','nHybridMediumMuons', 'nHybridTightMuons','nvetoLeptons',"ngoodElectrons","nvetoElectrons","ngoodTaus","met","metphi","ht"] 
  extraVariables += ["leptonPt", 'leptonEta', 'leptonPhi', 'leptonPdg', 'singleMuonic', 'singleElectronic', 'singleLeptonic']
  extraVariables += ['pfMet', 'pfMetphi','genMet', 'genMetPhi']
  jetvars = ["jetPt", "jetEta", "jetPhi", "jetPdg", "jetBTag", "jetChef", "jetNhef", "jetCeef", "jetNeef", "jetHFhef", "jetHFeef", "jetMuef", "jetElef", "jetPhef", "jetUnc", 'jetId']#, "jetCutBasedPUJetIDFlag","jetFull53XPUJetIDFlag","jetMET53XPUJetIDFlag"
  muvars = ["muPt", "muEta", "muPhi", "muPdg", "muRelIso", "muDxy", "muDz", "muNormChi2", "muNValMuonHits", "muNumMatchedStations", "muPixelHits", "muNumtrackerLayerWithMeasurement", 'muIsGlobal', 'muIsTracker','muIsPF', "muIso03sumChargedHadronPt", "muIso03sumNeutralHadronEt", "muIso03sumPhotonEt", "muIso03sumPUChargedHadronPt"] 
  elvars = ["elePt", "eleEta", "elePhi", "elePdg", "eleRelIso", "eleDxy", "eleDz", "eleOneOverEMinusOneOverP", "elePfRelIso", "eleSigmaIEtaIEta", "eleHoE", "eleDPhi", "eleDEta", "eleMissingHits", "elePassPATConversionVeto"]
  tavars = ["tauPt", "tauEta", "tauPhi", "tauPdg", 'tauJetInd', 'tauJetDR']
  trackVars = ["trackPdg", "trackPt", "trackEta", "trackPhi", "trackRelIso","trackPassVetoMuSel","trackPassVetoEleSel","trackPassHybridLooseMuons","trackPassHybridMediumMuons","trackPassHybridTightMuons"]
  if not sample['name'].lower().count('data'):
    extraVariables+=["ngNuEFromW","ngNuMuFromW","ngNuTauFromW"]
    genTauvars = ["gTauPdg", "gTauPt", "gTauEta", "gTauPhi", "gTauMetPar", "gTauMetPerp", "gTauNENu", "gTauNMuNu", 'gTauNTauNu', 'gTauJetInd', 'gTauJetDR', 'gTauTauDR', 'gTauTauInd']
    genLepvars = ["gLepPdg", "gLepPt", "gLepEta", "gLepPhi", 'gLepInd', 'gLepDR', 'gLepMMass']
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
  structString +="Int_t njetCount, nmuCount, neleCount, ntauCount, ntrackCount;"
  for var in jetvars:
    structString +="Float_t "+var+"[30];"
  for var in muvars:
    structString +="Float_t "+var+"[10];"
  for var in elvars:
    structString +="Float_t "+var+"[10];"
  for var in tavars:
    structString +="Float_t "+var+"[10];"
  for var in trackVars:
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
  t.Branch("ntrackCount",   ROOT.AddressOf(s,"ntrackCount"), 'ntrackCount/I')
  for var in jetvars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[njetCount]/F')
  for var in muvars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[nmuCount]/F')
  for var in elvars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[neleCount]/F')
  for var in tavars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[ntauCount]/F')
  for var in trackVars:
    t.Branch(var,   ROOT.AddressOf(s,var), var+'[ntrackCount]/F')
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

  for bin in sample["bins"]:
    commoncf = ""
    if options.chmode=="copyMET":
      commoncf = "slimmedMETs>=100&&Sum$((muonsDz>0.05||muonsDxy>0.02)&&muonsPt>20)==0"
    if options.chmode[:7] == "copyInc":
      commoncf = "(1)"
    c = ROOT.TChain('Events')
    for f in bin['filenames']:
      c.Add(f)
    ntot = c.GetEntries()

    pfMetLabel = ("pfMet")
    pfMetHandle = Handle("vector<reco::PFMET>")

    if not newGenMet:
      genMetLabel = ("genMetTrue")
      genMetHandle = Handle("vector<reco::GenMET>")

#    gpLabel = ("packedGenParticles")
#    gpHandle = Handle("vector<pat::PackedGenParticle>")

    gpLabel = ("prunedGenParticles")
    gpHandle = Handle("vector<reco::GenParticle>")
    pfLabel = ("packedPFCandidates")
    pfHandle = Handle("vector<pat::PackedCandidate>")

    mclist = []
    for thisfile in bin["filenames"]:
      mclist.append(thisfile)
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
        if number_events>10001:
          number_events=10001
      start = int(options.fromPercentage/100.*number_events)
      stop  = int(options.toPercentage/100.*number_events)
      print "Reading: ", sample["name"], bin['dbsName'], "with",number_events,"Events using cut", commoncf
      print "Reading percentage ",options.fromPercentage, "to",options.toPercentage, "which is range",start,"to",stop,"of",number_events
      for i in range(start, stop):
        if (i%1000 == 0) and i>0 :
          print i
  #      # Update all the Tuples
        if elist.GetN()>0 and ntot>0:
          c.GetEntry(elist.GetEntry(i))
          events.to(elist.GetEntry(i))
          s.weight = bin['weight']
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

          if not newGenMet:
            events.getByLabel(genMetLabel,genMetHandle)
            genMet =genMetHandle.product()
            s.genMet = genMet[0].pt()
            s.genMetPhi = genMet[0].phi()
          else:
            s.genMet = getVarValue(c, 'genMet')
            s.genMetPhi = getVarValue(c, 'genMetPhi')
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
          vetoMuons = filter(lambda mu:vetoMuID(mu), allGoodMuons)
          hybridLooseMuons = filter(lambda mu:hybridMuID(mu, 'loose'), allGoodMuons)
          hybridMediumMuons = filter(lambda mu:hybridMuID(mu, 'medium'), allGoodMuons)
          hybridTightMuons = filter(lambda mu:hybridMuID(mu, 'tight'), allGoodMuons)
          
          leptons = sorted(electrons+muons, key=lambda k: -k['pt'])
          s.singleLeptonic = len(leptons)==1
          s.singleElectronic = len(leptons)==1 and abs(leptons[0]['Pdg'])==11
          s.singleMuonic = len(leptons)==1 and abs(leptons[0]['Pdg'])==13
          if len(leptons)>0:
            s.leptonPt=leptons[0]['pt']
            s.leptonPhi=leptons[0]['phi']
            s.leptonEta=leptons[0]['eta']
            s.leptonPdg=leptons[0]['Pdg']
 
          s.ngoodMuons = len(muons)
          s.nvetoMuons = len(vetoMuons)
          s.nHybridLooseMuons = len(hybridLooseMuons)
          s.nHybridMediumMuons = len(hybridMediumMuons)
          s.nHybridTightMuons = len(hybridTightMuons)
          s.ngoodElectrons = len(electrons)
          s.nvetoElectrons=len(vetoElectrons)
          s.nvetoLeptons=s.nvetoElectrons+s.nvetoMuons
          s.ngoodTaus = len(taus)
          
          jResult = getGoodJetsStage1(c,vetoMuons+vetoElectrons, options.DR)#, jermode=options.jermode, jesmode=options.jesmode)
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
          s.nmu  = len(allGoodMuons)
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
              if pdgId==11 or pdgId==13:
                if not (gp.numberOfMothers()>0  and abs(gp.mother(0).pdgId())==24): continue
                gpm = gp.mother(0)
                lep = {'pt':gp.pt(),'phi':gp.phi(),'eta':gp.eta(),'Pdg':gp.pdgId(), 'MMass':gpm.mass()}
                if pdgId==11:
                  rlep=findClosestObjectDR(allGoodElectrons, {'phi':lep['phi'], 'eta':lep['eta']})
                if pdgId==13:
                  rlep=findClosestObjectDR(allGoodMuons, {'phi':lep['phi'], 'eta':lep['eta']})
                if rlep:
                  lep['gLepDR'] = rlep['deltaR']
                  lep['gLepInd']= rlep['index']
                else:
                  lep['gLepDR'] = float('nan')
                  lep['gLepInd']= -1

                genLeps.append(lep)
 
              if pdgId==15:
                if not (gp.numberOfMothers()>0  and abs(gp.mother(0).pdgId())==24): continue
                tau = {'pt':gp.pt(),'phi':gp.phi(),'eta':gp.eta(),'Pdg':gp.pdgId(),'gTauNENu':0, 'gTauNMuNu':0, 'gTauNTauNu':0}
                if s.ngNuMuFromW==2:
                  print "Taus?" 
                MEx = 0.
                MEy = 0.
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
#                ind=0
                done=False
                while not done:
                  for id in range(gp.numberOfDaughters()):
                    if abs(gp.daughter(id).pdgId())==15:
                      gp = gp.daughter(id)
#                      ind+=1
                      break
                    done=True

                for id in range(gp.numberOfDaughters()):
                  gd = gp.daughter(id)
#                  tx-=gd.px()
#                  ty-=gd.py()
#                  print id, "d",gd.pdgId(),gd.pt()
                  dpdgId = abs(gd.pdgId())
#                  if dpdgId==15:
#                    justARadiation=True
#                    break
                  if dpdgId==12:tau['gTauNENu']+=1
                  if dpdgId==14:tau['gTauNMuNu']+=1
                  if dpdgId==16:tau['gTauNTauNu']+=1
                  if dpdgId==12 or dpdgId==14 or dpdgId==16:
                    MEx+=gd.px()
                    MEy+=gd.py()
                tau['gTauMetPar']=cos(tau['phi'])*MEx+sin(tau['phi'])*MEy
                tau['gTauMetPerp']=cos(tau['phi'])*MEy-sin(tau['phi'])*MEx
#                print tx, ty
#                if not justARadiation:
                genTaus.append(tau)
#              print genTaus
          events.getByLabel(pfLabel,pfHandle)
          pfcH =pfHandle.product()
          pfc = list(pfcH)
          isoCands = [{'c':cand,'iso':0.} for cand in filter(lambda c:c.pt()>10 and c.fromPV()==c.PVTight and abs(c.pdgId()) in [11, 13, 211], pfc)]
          for p in pfc:
#            if debug:
#              if p.pt()>100:
#                print s.event, p.pt(), p.pdgId() 
            phi=p.phi()
            eta=p.eta()
            for ic in isoCands:
              dR= deltaR({'phi':phi,'eta':eta},{'phi':ic['c'].phi(),'eta':ic['c'].eta()})
              if dR>0.02 and dR<0.3:
                ic['iso']+=p.pt()
          for ic in isoCands:
            ic['relIso']=ic['iso']/ic['c'].pt()
#          isoCands = filter(lambda c:c.pt()>10 and abs(c.dz())<0.1 and c.fromPV()==c.PVTight and abs(c.dxy())<0.02 and abs(c.pdgId()) in [11, 13, 211], pfc)
          isoCands=filter(lambda ic:ic['relIso']<0.2, isoCands)
#          for ic in isoCands:
#            print ic['c'].pdgId(), ic['c'].pt(), ic['relIso']
#          print "len",len(pfc), len(isoCands)
          s.ntrackCount=min(10,len(isoCands))
          for i in xrange(s.ntrackCount):
            s.trackPdg[i] = isoCands[i]['c'].pdgId()
            s.trackPt[i] = isoCands[i]['c'].pt()
            s.trackEta[i] = isoCands[i]['c'].eta()
            s.trackPhi[i] = isoCands[i]['c'].phi()
            s.trackRelIso[i] = isoCands[i]['relIso']
            s.trackPassVetoMuSel[i]=isIsolated({'phi':s.trackPhi[i],'eta':s.trackEta[i]}, vetoMuons, dR=0.1)
            s.trackPassVetoEleSel[i]=isIsolated({'phi':s.trackPhi[i],'eta':s.trackEta[i]}, vetoElectrons, dR=0.1)
            s.trackPassHybridLooseMuons[i]=isIsolated({'phi':s.trackPhi[i],'eta':s.trackEta[i]}, hybridLooseMuons, dR=0.1)
            s.trackPassHybridMediumMuons[i]=isIsolated({'phi':s.trackPhi[i],'eta':s.trackEta[i]}, hybridMediumMuons, dR=0.1)
            s.trackPassHybridTightMuons[i]=isIsolated({'phi':s.trackPhi[i],'eta':s.trackEta[i]}, hybridTightMuons, dR=0.1)
####################

          s.njetCount = min(30,s.njets)
          for i in xrange(s.njetCount):
            s.jetPt[i]    = idJets30[i]['pt']
            s.jetUnc[i]   = idJets30[i]['unc']
            s.jetEta[i]   = idJets30[i]['eta']
            s.jetPhi[i]   = idJets30[i]['phi']
            s.jetPdg[i]   = idJets30[i]['pdg']
            s.jetBTag[i]  = idJets30[i]['btag']
            s.jetChef[i]  = idJets30[i]['chef']
            s.jetNhef[i]  = idJets30[i]['nhef']
            s.jetCeef[i]  = idJets30[i]['ceef']
            s.jetNeef[i]  = idJets30[i]['neef']
            s.jetHFhef[i] = idJets30[i]['hfhef']
            s.jetHFeef[i] = idJets30[i]['hfeef']
            s.jetMuef[i]  = idJets30[i]['muef']
            s.jetElef[i]  = idJets30[i]['elef']
            s.jetPhef[i]  = idJets30[i]['phef']
            s.jetId[i]    = idJets30[i]['id']
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
            s.muIso03sumChargedHadronPt[i] = allGoodMuons[i]['Iso03sumChargedHadronPt']
            s.muIso03sumNeutralHadronEt[i] = allGoodMuons[i]['Iso03sumNeutralHadronEt']
            s.muIso03sumPhotonEt[i] = allGoodMuons[i]['Iso03sumPhotonEt']
            s.muIso03sumPUChargedHadronPt[i] = allGoodMuons[i]['Iso03sumPUChargedHadronPt']
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
              s.gLepMMass[i] = genLeps[i]['MMass']
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
