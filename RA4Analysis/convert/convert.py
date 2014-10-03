import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy, random, subprocess, datetime
#from helpers import getVarValue, deltaPhi, minAbsDeltaPhi,  deltaR, invMass,

from Workspace.RA4Analysis.convertHelpers import compileClass, readVar, printHeader, typeStr, createClassString

from Workspace.HEPHYPythonTools.helpers import bStr, wrapStr, getFileList, getVarValue
from Workspace.HEPHYPythonTools.helpers import deltaPhi, minAbsDeltaPhi, invMassOfLightObjects, deltaR, closestMuJetDeltaR, invMass,  findClosestObjectDR
from Workspace.RA4Analysis.objectSelection import getLooseEleStage1,getAllElectronsStage1, tightPOGEleID, vetoEleID, getLooseMuStage1, getAllMuonsStage1, tightPOGMuID, vetoMuID, getAllTausStage1, getTauStage1, hybridMuID, getGoodJetsStage1, isIsolated

#def getVarValue(chain, bname):
#  return getattr(chain, bname)

from Workspace.RA4Analysis.stage1Tuples import *

from Workspace.HEPHYPythonTools.xsec import xsec

subDir = "convertedTuples_v24"
target_lumi = 2000 #pb-1

from localInfo import username
outputDir = "/data/"+username+"/"+subDir+"/"

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--chmode", dest="chmode", default="copyMET", type="string", action="store", help="chmode: What to do.")
#parser.add_option("--jermode", dest="jermode", default="none", type="string", action="store", help="jermode: up/down/central/none")
#parser.add_option("--jesmode", dest="jesmode", default="none", type="string", action="store", help="jesmode: up/down/none")
parser.add_option("--samples", dest="allsamples", default="T5Full_1200_1000_800", type="string", action="store", help="samples:Which samples.")
parser.add_option("--file", dest="file", default="", type="string", action="store", help="file:Which file.")
parser.add_option("--DR", dest="DR", default="0.4", type="float", action="store", help="samples:Which samples.")
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")
parser.add_option("--overwrite", dest="overwrite", action="store_true", help="Overwrite?", default=True)
parser.add_option("--puppi", dest="puppi", action="store_true", help="Just do a puppi subset.")
parser.add_option("--newGenMet", dest="newGenMet", action="store_true", help="new genmet?")
parser.add_option("--fromPercentage", dest="fromPercentage", default="0", type="int", action="store", help="from (% of tot. events)")
parser.add_option("--toPercentage", dest="toPercentage", default="100", type="int", action="store", help="to (% of tot. events)")
parser.add_option("--keepPDFWeights", dest="keepPDFWeights", action="store_true", help="keep PDF Weights?")
 
(options, args) = parser.parse_args()

if options.file:
  print "options: chmode",options.chmode, 'file',options.file, 'DR',options.DR
  allSamples = [{'name':'file', 'bins':[{'dbsName':None,'dir':None,'filenames':[options.file], 'xsec':-1, 'weight':1}], 'Chain':'Events'}]
else:
  print wrapStr()
  print "options: chmode",options.chmode, 'samples',options.allsamples,'DR',options.DR
  print wrapStr()

  printHeader("Calculating weights of all bins")

  exec('allSamples=['+options.allsamples+']')
  for sample in allSamples:
    print wrapStr(s="sample: "+bStr(sample['name']),maxL=110)
    sample['filenames'] = {}
    sample['weight'] = {}
    for bin in sample['bins']:
      print "Input files from:",bin['dir']
      filelist = getFileList(bin['dir'], minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/')
      if options.small: filelist = filelist[:2]
      bin['filenames'] = []
      for tfile in filelist:
        bin['filenames'] = filelist

      c = ROOT.TChain('Events')
      c.SetBranchStatus("*", 0)
      for f in bin['filenames']:
        c.Add(f)
      nevents= c.GetEntries()
      del c
      if not sample.has_key('isData'):
        sample['isData'] = (bin['dbsName'] and bin['dbsName'].lower().count('run')>0)
      else:
        assert sample['isData'] == (bin['dbsName'] and bin['dbsName'].lower().count('run')>0), \
          "Conflicting 'isData' condition in sample %s, was %i but bin %s suggests %i" \
          % (sample['name'], sample['isData'], repr(bin), bin['dbsName'].lower().count('run') )
      if sample['isData']:
        bin['weight'] = 1.
      else:   #Simulation
        if nevents>0:
          if bin['dbsName']:
            bin['weight'] = xsec[bin['dbsName']]*target_lumi/nevents
            bin['xsec']=xsec[bin['dbsName']]
          else:
            print "Warning! Sample ",sample['name'], 'bin',bin, 'has no dbsName! -> Use weight 1.'
            bin['weight']=1
            bin['xsec']=float('nan')
        else:
          bin['weight']=0
        print 'Sample', bStr(sample['name']), 'weight',bin['weight'], 'bin', bin['dbsName'], 'nevents:',nevents,'xsec',bin['xsec'], 'n-events',nevents
print wrapStr("Calculating weights of all samples: "+bStr("Done."), maxL=110)
print

print wrapStr("Creating directory if not present.")
if not os.path.isdir(outputDir):
  os.system('mkdir -p '+outputDir)
outSubDir = options.chmode
#outSubDir+='_DR'+str(options.DR)
#if options.jermode.lower()!='none':
#  outSubDir = outSubDir+"_JER"+options.jermode.lower()
#if options.jesmode.lower()!='none':
#  outSubDir = outSubDir+"_JES"+options.jesmode.lower()
os.system("mkdir -p "+outputDir+"/"+outSubDir)
print "directory:", outputDir+"/"+outSubDir
print wrapStr("Done creating directory.")

nc = 0
printHeader("Starting sample conversion")

for isample, sample in enumerate(allSamples):
  print wrapStr("Converting sample: "+bStr(sample['name']), maxL=110)
  if not os.path.isdir(outputDir+"/"+outSubDir+"/"+sample["name"]):
    os.system("mkdir -p "+outputDir+"/"+outSubDir+"/"+sample["name"])
    print "Subdir", outputDir+"/"+outSubDir, "created."
  else:
    print "Subdir", outputDir+"/"+outSubDir, "already found."

  #Variables that are needed but won't be written
  readVariables = ["nmuons/I","neles/I","ntaus/I", "nJets/I"]
  readVectors = [\
    {'prefix':'eles',  'nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'PfRelIso/F', 'Dxy/F', 'Dz/F', 'OneOverEMinusOneOverP/F',  'SigmaIEtaIEta/F', 'HoE/F', 'DPhi/F', 'DEta/F', 'MissingHits/I', 'PassPATConversionVeto/I']},
    {'prefix':'muons', 'nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'PFRelIso/F', 'Dxy/F', 'Dz/F', 'NormChi2/F', 'NValMuonHits/I', 'NumMatchedStations/I', 'PixelHits/I', 'NumtrackerLayerWithMeasurement/I', 'isGlobal/I', 'isTracker/I','isPF/I', 'Iso03sumChargedHadronPt/F', 'Iso03sumNeutralHadronEt/F', 'Iso03sumPhotonEt/F', 'Iso03sumPUChargedHadronPt/F']},
    {'prefix':'taus',  'nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'DecayModeFinding/I', 'AgainstMuonLoose3/I', 'AgainstElectronLooseMVA5/I', 'ByLooseCombinedIsolationDeltaBetaCorr3Hits/I']},
    {'prefix':'jets',  'nMax':30, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Parton/I', 'Unc/F', 'ID/I', 'BTag/F', "ChargedHadronEnergyFraction/F", "NeutralHadronEnergyFraction/F", "ChargedEmEnergyFraction/F", "NeutralEmEnergyFraction/F", "HFHadronEnergyFraction/F", "HFEMEnergyFraction/F", "MuonEnergyFraction/F", "ElectronEnergyFraction/F", "PhotonEnergyFraction/F"]},
  ]

  #Anything that is copied from stage1 -> stage2. Syntax 'OldVar/Type:NewVar'. OldVar needs to be an alias.
  copyVariables = [ 'event/l', 'run/I', 'lumi/I', 'ngoodVertices/I', 'bx/I:bunchCrossing', 'slimmedMETs/F:met', 'slimmedMETsPhi/F:metPhi']
  #new variables
  newVariables = ['weight/F'] 

  if options.newGenMet:
    copyVariables.extend(['genMet/F', 'genMetPhi/F'])
  if not sample['isData']:
    copyVariables.extend(['nTrueGenVertices/I'])

  newVariables.extend( ['pfMet/F', 'pfMetPhi/F'] )
  if not options.newGenMet:
    newVariables.extend(['genMet/F', 'genMetPhi/F'])
  newVariables.extend( ['leptonPt/F', 'leptonEta/F', 'leptonPhi/F', 'leptonPdg/I', 'singleMuonic/I', 'singleElectronic/I', 'singleLeptonic/I'] )
  newVariables.extend( ['ngoodMuons/I','nvetoMuons/I','nHybridLooseMuons/I','nHybridMediumMuons/I', 'nHybridTightMuons/I','nvetoLeptons/I','ngoodElectrons/I','nvetoElectrons/I','ngoodTaus/I'] )
  newVariables.extend( ['ht/F', 'njets/I' , 'njetsFailID/I', 'nbtags/I', 'nmu/I', 'nele/I', 'ntau/I'] ) 
  if not sample['isData']:
    newVariables+=['ngNuEFromW/I','ngNuMuFromW/I','ngNuTauFromW/I']
  #new vectors
  jetVec   = {'prefix':'jet',  'nMax':30, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'BTag/F', 'Chef/F', 'Nhef/F', 'Ceef/F', 'Neef/F', 'HFhef/F', 'HFeef/F', 'Muef/F', 'Elef/F', 'Phef/F', 'Unc/F', 'Id/F']}#, 'CutBasedPUIDFlag','Full53XPUIDFlag','MET53XPUIDFlag'
  muVec    = {'prefix':'mu',   'nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'RelIso/F', 'Dxy/F', 'Dz/F', 'NormChi2/F', 'NValMuonHits/I', 'NumMatchedStations/I', 'PixelHits/I', 'NumtrackerLayerWithMeasurement/I', 'IsGlobal/I', 'IsTracker/I','IsPF/I', 'Iso03sumChargedHadronPt/F', 'Iso03sumNeutralHadronEt/F', 'Iso03sumPhotonEt/F', 'Iso03sumPUChargedHadronPt/F']}
  eleVec   = {'prefix':'ele',  'nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'RelIso/F', 'Dxy/F', 'Dz/F', 'OneOverEMinusOneOverP/F',  'SigmaIEtaIEta/F', 'HoE/F', 'DPhi/F', 'DEta/F', 'MissingHits/I', 'PassPATConversionVeto/I']}
  tauVec   = {'prefix':'tau',  'nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'JetInd/I', 'JetDR/F']}
  trackVec = {'prefix':'track','nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'RelIso/F', 'PassVetoMuSel/I','PassVetoEleSel/I','PassHybridLooseMuons/I','PassHybridMediumMuons/I','PassHybridTightMuons/I']}
  newVectors = [jetVec, muVec, eleVec, tauVec, trackVec ]
  if not sample['isData']:
   gTauVec =  {'prefix':'gTau', 'nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'MetPar/F', 'MetPerp/F', 'NENu/I', 'NMuNu/I', 'NTauNu/I', 'JetInd/I', 'JetDR/F', 'TauDR/F', 'TauInd/I']}
   gLepVec =  {'prefix':'gLep', 'nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'Ind/I', 'DR/F', 'MMass/F']}
   newVectors+=[gTauVec, gLepVec]
  if options.puppi:
    puppiVec = {'prefix':'puppi', 'nMax':10000,  'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I']}
    pfVec =    {'prefix':'pf',    'nMax':10000,  'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I']}
    newVectors+= [puppiVec, pfVec]

  readVars = [readVar(v, allowRenaming=False, isWritten=False, isRead=True) for v in readVariables]
  for v in readVectors:
    v['vars'] = [readVar(v['prefix']+vvar, allowRenaming=False, isWritten=False, isRead=True) for vvar in v['vars']]

  copyVars   = [readVar(v, allowRenaming=True, isWritten=True, isRead=True) for v in copyVariables]
  for v in newVectors:
    v['varNameCount']  = v['prefix']+'Count'
    newVariables.append(v['varNameCount']+'/i')
    v['vars'] = [readVar(v['prefix']+vvar, allowRenaming=False, isWritten=True, isRead=False) for vvar in v['vars']]
  newVars = [readVar(v, allowRenaming=False, isWritten = True, isRead=False) for v in newVariables]

 
  writeClassName = "ClassToWrite_"+str(nc)+"_"+str(isample) 
  writeClassString = createClassString(className=writeClassName, vars=copyVars + newVars, vectors=newVectors, nameKey = 'stage2Name')
  printHeader("Class to Write")
#  print writeClassString
  s = compileClass(className=writeClassName, classString=writeClassString, tmpDir='/data/'+username+'/tmp/')

  readClassName = "ClassToRead_"+str(nc)+"_"+str(isample) 
  readClassString = createClassString(className=readClassName, vars=readVars, vectors=readVectors, nameKey = 'stage1Name', stdVectors=True)
  printHeader("Class to Read")
#  print readClassString
  r = compileClass(className=readClassName, classString=readClassString, tmpDir='/data/'+username+'/tmp/')

  nc+=1
  postfix=""
  if options.small:
    postfix="_small"
  if options.fromPercentage!=0 or options.toPercentage!=100:
    postfix += "_from"+str(options.fromPercentage)+"To"+str(options.toPercentage)
  ofile = outputDir+"/"+outSubDir+"/"+sample["name"]+"/histo_"+sample["name"]+postfix+".root"
  if options.file:
    ofile=options.file.replace('.root','_converted.root')
  if os.path.isfile(ofile) and options.overwrite:
    print "Warning! will overwrite",ofile
  if os.path.isfile(ofile) and not options.overwrite:
    print ofile, "already there! Skipping!!!"
    continue
  chain_gDir = ROOT.gDirectory.func()
  t = ROOT.TTree( "Events", "Events", 1 )
  for v in copyVars+newVars:
    t.Branch(v['stage2Name'], ROOT.AddressOf(s,v['stage2Name']), v['stage2Name']+'/'+v['type'])
  for v in newVectors:
    for var in v['vars']:
      t.Branch(var['stage2Name'], ROOT.AddressOf(s,var['stage2Name']), var['stage2Name']+'['+v['varNameCount']+']/'+var['type'])

  chain_gDir.cd()

  for bin in sample["bins"]:
    commoncf = ""
    if options.chmode=="copyMET":
      commoncf = "slimmedMETs>=100&&Sum$((muonsDz>0.05||muonsDxy>0.02)&&muonsPt>20)==0"
    if options.chmode[:7] == "copyInc":
      commoncf = "(1)"
    if sample.has_key("additionalCut"):
      if type(sample["additionalCut"])==type({}):
        if sample["additionalCut"].has_key(bin):
          commoncf = commoncf+"&&"+sample["additionalCut"][bin]
      else:
        commoncf = commoncf+"&&"+sample["additionalCut"]
    c = ROOT.TChain('Events')
    for f in bin['filenames']:
      c.Add(f)
    c.Draw(">>eList", commoncf)
    elist = ROOT.gDirectory.Get("eList")
    number_events = elist.GetN()
    ntot = c.GetEntries()
    if ntot==0:
      print "Zero entries in", bin, sample["name"]
      continue

    c.SetAutoDelete(1)
    c.SetMakeClass(1)
    c.SetBranchStatus("*", 0)
    c.GetEntry(0)
    for v in copyVars+readVars:
      c.SetBranchStatus(c.GetAlias(v['stage1Name']), 1)
    for v in copyVars:
      c.SetBranchAddress(c.GetAlias(v['stage1Name']), ROOT.AddressOf(s, v['stage2Name']))
    for v in readVars:
#      print c.GetAlias(v['stage1Name']), v['stage1Name']
      c.SetBranchAddress(c.GetAlias(v['stage1Name']), ROOT.AddressOf(r, v['stage1Name']))
    for v in readVectors:
      for var in v['vars']:
#        print var['stage1Name'], c.GetAlias(var['stage1Name'])
        c.SetBranchStatus(c.GetAlias(var['stage1Name']), 1)
#        print (c.GetAlias(var['stage1Name']), var['stage1Name'])
        c.SetBranchAddress(c.GetAlias(var['stage1Name']), ROOT.AddressOf(r, var['stage1Name']))

    pfMetLabel = ("pfMet")
    pfMetHandle = Handle("vector<reco::PFMET>")

    if not options.newGenMet:
      genMetLabel = ("genMetTrue")
      genMetHandle = Handle("vector<reco::GenMET>")

#    gpLabel = ("packedGenParticles")
#    gpHandle = Handle("vector<pat::PackedGenParticle>")

    gpLabel = ("prunedGenParticles")
    gpHandle = Handle("vector<reco::GenParticle>")
    pfLabel = ("packedPFCandidates")
    pfHandle = Handle("vector<pat::PackedCandidate>")
    puppiLabel = ("puppi","Puppi")
    puppiHandle = Handle("vector<reco::PFCandidate>")
    mclist = []
    for thisfile in bin["filenames"]:
      mclist.append(thisfile)
    print "Here1"
    events = Events(mclist)
    print "Here2"
    events.toBegin()
    print "Here3"
    print "Here4"
    if options.small:
      if number_events>11:
        number_events=11
    start = int(options.fromPercentage/100.*number_events)
    stop  = int(options.toPercentage/100.*number_events)
    print "Reading: ", sample["name"], bin['dbsName'], "with",number_events,"Events using cut", commoncf
    print "Reading percentage ",options.fromPercentage, "to",options.toPercentage, "which is range",start,"to",stop,"of",number_events
    for nev in range(start, stop):
      if (nev%1000 == 0) and nev>0 :
        print nev
#      # Update all the Tuples
      if elist.GetN()>0 and ntot>0:
        s.init()
        r.init()
#        print "Before", c.GetCurrentFile()
        c.GetEntry(elist.GetEntry(nev))
#        print "After", c.GetCurrentFile()
        
        events.to(elist.GetEntry(nev))
        s.weight = bin['weight']
        if not options.newGenMet:
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
        s.pfMetPhi = pfMet[0].phi()

        allGoodElectrons = getAllElectronsStage1(r, r.neles)
        allGoodTaus = getAllTausStage1(r, r.ntaus)
        allGoodMuons = getAllMuonsStage1(r, r.nmuons) 
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
        
        jResult = getGoodJetsStage1(r, vetoMuons+vetoElectrons, options.DR)#, jermode=options.jermode, jesmode=options.jesmode)
        jetResult = jResult['jets']
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
        s.trackCount=min(trackVec['nMax'],len(isoCands))
        for i in xrange(s.trackCount):
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
        if options.puppi:
          events.getByLabel(puppiLabel,puppiHandle)
          puppi = list(puppiHandle.product())
          s.puppiCount=min(puppiVec['nMax'], len(puppi))
          for i in range(s.puppiCount):
            s.puppiPt[i] = puppi[i].pt() 
            s.puppiEta[i] = puppi[i].eta() 
            s.puppiPhi[i] = puppi[i].phi() 
            s.puppiPdg[i] = puppi[i].pdgId() 
          s.pfCount=min(pfVec['nMax'], len(pfc))
          for i in range(s.pfCount):
            s.pfPt[i]  = pfc[i].pt() 
            s.pfEta[i] = pfc[i].eta() 
            s.pfPhi[i] = pfc[i].phi() 
            s.pfPdg[i] = pfc[i].pdgId() 
        s.jetCount = min(jetVec['nMax'],s.njets)
        for i in xrange(s.jetCount):
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
        s.muCount = min(muVec['nMax'],s.nmu)
        for i in xrange(s.muCount):
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
        s.eleCount = min(eleVec['nMax'],s.nele)
        for i in xrange(s.eleCount):
          s.elePt[i] = allGoodElectrons[i]['pt']
          s.eleEta[i] = allGoodElectrons[i]['eta']
          s.elePhi[i] = allGoodElectrons[i]['phi']
          s.elePdg[i] = allGoodElectrons[i]['Pdg']
          s.eleRelIso[i] = allGoodElectrons[i]['relIso']
          s.eleDxy[i] = allGoodElectrons[i]['Dxy']
          s.eleDz[i] = allGoodElectrons[i]['Dz']
          s.eleOneOverEMinusOneOverP[i] = allGoodElectrons[i]['OneOverEMinusOneOverP']
          s.eleSigmaIEtaIEta[i] = allGoodElectrons[i]['sIEtaIEta']
          s.eleHoE[i] = allGoodElectrons[i]['HoE']
          s.eleDPhi[i] = allGoodElectrons[i]['DPhi']
          s.eleDEta[i] = allGoodElectrons[i]['DEta']
          s.eleMissingHits[i] = allGoodElectrons[i]['MissingHits']
          s.elePassPATConversionVeto[i] = allGoodElectrons[i]['ConvRejection']

#              print "Electron pt's:",i,allGoodElectrons[i]['pt']
        s.tauCount = min(tauVec['nMax'],s.ntau)
        for i in xrange(s.tauCount):
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
          s.gTauCount = min(gTauVec['nMax'],len(genTaus))
          genTaus = sorted(genTaus, key=lambda k: -k['pt'])
          for i in xrange(s.gTauCount):
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
          s.gLepCount = min(gLepVec['nMax'],len(genLeps))
          genLeps = sorted(genLeps, key=lambda k: -k['pt'])
          for i in xrange(s.gLepCount):
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
