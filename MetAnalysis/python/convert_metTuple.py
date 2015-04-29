import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import sys, os, copy, random, subprocess, datetime

from Workspace.RA4Analysis.convertHelpers import compileClass, readVar, printHeader, typeStr, createClassString

from Workspace.HEPHYPythonTools.helpers import bStr, wrapStr, getFileList, getVarValue
from Workspace.HEPHYPythonTools.helpers import deltaPhi, minAbsDeltaPhi, invMassOfLightObjects, deltaR 
from Workspace.RA4Analysis.objectSelection import getAllElectronsStage1, tightPOGEleID, vetoEleID, getAllMuonsStage1, tightPOGMuID, vetoMuID, getAllTausStage1, hybridMuID, getGoodJetsStage1, isIsolated

from Workspace.MetAnalysis.stage1Tuples import *

from Workspace.HEPHYPythonTools.xsec import xsec

subDir = "convertedMetTuples2_v1"
target_lumi = 4000 #pb-1

from localInfo import username
outputDir = "/data/"+username+"/"+subDir+"/"

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--chmode", dest="chmode", default="looseDoubleMu", type="string", action="store", help="chmode: What to do.")
parser.add_option("--samples", dest="allsamples", default="DYJetsToLL_HT", type="string", action="store", help="samples:Which samples.")
parser.add_option("--file", dest="file", default="", type="string", action="store", help="file:Which file.")
parser.add_option("--DR", dest="DR", default="0.4", type="float", action="store", help="samples:Which samples.")
parser.add_option("--small", dest="small", default = False, action="store_true", help="Just do a small subset.")
parser.add_option("--overwrite", dest="overwrite", action="store_true", help="Overwrite?", default=True)
parser.add_option("--fromPercentage", dest="fromPercentage", default="0", type="int", action="store", help="from (% of tot. events)")
parser.add_option("--toPercentage", dest="toPercentage", default="100", type="int", action="store", help="to (% of tot. events)")
 
(options, args) = parser.parse_args()
if sys.argv[0].count('ipython'):
  options.small=True

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
      if options.small: filelist = filelist[:1]
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

#  Variables and vectors to be loaded
  loadProducts = ["nmuons/int","neles/int", "nJets/int"]
  loadVectors = [\
#    {'prefix':'eles',  'vars':['Pt/float', 'Eta/float', 'Phi/float', 'Pdg/int', 'PfRelIso/float', 'Dxy/float', 'Dz/float', 'OneOverEMinusOneOverP/float',  'SigmaIEtaIEta/float', 'HoE/float', 'DPhi/float', 'DEta/float', 'MissingHits/int', 'PassPATConversionVeto/int']},
    {'prefix':'muons', 'vars':['Pt/float', 'Eta/float', 'Phi/float', 'Pdg/int', 'PFRelIso/float', 'Dxy/float', 'Dz/float', 'NormChi2/float', 'NValMuonHits/int', 'NumMatchedStations/int', 'PixelHits/int', 'NumtrackerLayerWithMeasurement/int', 'isGlobal/int', 'isTracker/int','isPF/int', 'Iso03sumChargedHadronPt/float', 'Iso03sumNeutralHadronEt/float', 'Iso03sumPhotonEt/float', 'Iso03sumPUChargedHadronPt/float']},
    {'prefix':'jets',  'vars':['Pt/float', 'Eta/float', 'Phi/float', 'Parton/int', 'Unc/float', 'ID/int', 'BTag/float', "ChargedHadronEnergyFraction/float", "NeutralHadronEnergyFraction/float", "ChargedEmEnergyFraction/float", "NeutralEmEnergyFraction/float", "HFHadronEnergyFraction/float", "HFEMEnergyFraction/float", "MuonEnergyFraction/float", "ElectronEnergyFraction/float", "PhotonEnergyFraction/float"]},
  ]
# edm collections to be loaded
  loadEDMCollections =[]
#  loadEDMCollections = [ {'name':'pfMet', 'label':("pfMet"), 'edmType':"vector<reco::PFMET>"} ]
#  loadEDMCollections.append({'name':'pf', 'label':("packedPFCandidates"), 'edmType':"vector<pat::PackedCandidate>"})
#  if not sample['isData']:
#    loadEDMCollections.append( {'name':'gps', 'label':("prunedGenParticles"), 'edmType':"vector<reco::GenParticle>"})
#  if not options.newGenMet:
#    loadEDMCollections.append({'name':'genMet', 'label':("genMetTrue"), 'edmType':"vector<reco::GenMET>"})

  #Anything that is copied from stage1 -> stage2. Syntax 'OldVar/Type:NewVar'. OldVar needs to be an alias.
#  copyVariables = ['event/ULong64_t:event/l', 'run/int:run/I', 'lumi/int:lumi/I', 'ngoodVertices/int:ngoodVertices/I', 'bx/int:bunchCrossing/I', 'slimmedMETs/float:met/F', 'slimmedMETsPhi/float:metPhi/F']
  copyVariables = ['run/int:run/I', 'lumi/int:lumi/I', 'ngoodVertices/int:ngoodVertices/I', 'bx/int:bunchCrossing/I']
  copyVariables+= ["genMet/float:genMet/F", "genMetPhi/float:genMetPhi/F", "slimmedMETs/float:t1MetPt/F", "slimmedMETsPhi/float:t1MetPhi/F", "slimmedMETsSumEt/float:t1MetSumEt/F", "slimmedRAWMETs/float:rawMetPt/F", "slimmedRAWMETsPhi/float:rawMetPhi/F", "slimmedRAWMETsSumEt/float:rawMetSumEt/F", "slimmedT1TxyMETs/float:t1TxyMetPt/F", "slimmedT1TxyMETsPhi/float:t1TxyMetPhi/F", "slimmedT1TxyMETsSumEt/float:t1TxyMetSumEt/F", "slimmedTxyMETs/float:txyMetPt/F", "slimmedTxyMETsPhi/float:txyMetPhi/F", "slimmedTxyMETsSumEt/float:txyMetSumEt/F"]
  #new variables
  newVariables = ['weight/F', 'event/l'] 
  newVariables += ['ptZ/F','phiZ/F', 'mll/F'] 

#  if options.newGenMet:
#    copyVariables.extend(['genMet/float:genMet/F', 'genMetPhi/float:genMetPhi/F'])
  if not sample['isData']:
    copyVariables.extend(['nTrueGenVertices/float:nTrueGenVertices/I'])

#  newVariables.extend( ['pfMet/F', 'pfMetPhi/F'] )
#  if not options.newGenMet:
#    newVariables.extend(['genMet/F', 'genMetPhi/F'])
#  newVariables.extend( ['leptonPt/F', 'leptonEta/F', 'leptonPhi/F', 'leptonPdg/I', 'singleMuonic/I', 'singleElectronic/I', 'singleLeptonic/I'] )
#  newVariables.extend( ['ngoodMuons/I','nvetoMuons/I','nHybridLooseMuons/I','nHybridMediumMuons/I', 'nHybridTightMuons/I','nvetoLeptons/I','ngoodElectrons/I','nvetoElectrons/I'] )
  newVariables.extend( ['ht/F', 'njets/I' , 'njetsFailID/I', 'nbtags/I', 'nmu/I'])#, 'nele/I'] ) 
  #new vectors
  jetVec   = {'prefix':'jet',  'nMax':30, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'BTag/F', 'Chef/F', 'Nhef/F', 'Ceef/F', 'Neef/F', 'HFhef/F', 'HFeef/F', 'Muef/F', 'Elef/F', 'Phef/F', 'Unc/F', 'Id/F']}#, 'CutBasedPUIDFlag','Full53XPUIDFlag','MET53XPUIDFlag'
  muVec    = {'prefix':'mu',   'nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'RelIso/F', 'Dxy/F', 'Dz/F', 'NormChi2/F', 'NValMuonHits/I', 'NumMatchedStations/I', 'PixelHits/I', 'NumtrackerLayerWithMeasurement/I', 'IsGlobal/I', 'IsTracker/I','IsPF/I', 'Iso03sumChargedHadronPt/F', 'Iso03sumNeutralHadronEt/F', 'Iso03sumPhotonEt/F', 'Iso03sumPUChargedHadronPt/F']}
#  eleVec   = {'prefix':'ele',  'nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'RelIso/F', 'Dxy/F', 'Dz/F', 'OneOverEMinusOneOverP/F',  'SigmaIEtaIEta/F', 'HoE/F', 'DPhi/F', 'DEta/F', 'MissingHits/I', 'PassPATConversionVeto/I']}
#  trackVec = {'prefix':'track','nMax':10, 'vars':['Pt/F', 'Eta/F', 'Phi/F', 'Pdg/I', 'RelIso/F', 'PassVetoMuSel/I','PassVetoEleSel/I','PassHybridLooseMuons/I','PassHybridMediumMuons/I','PassHybridTightMuons/I']}
  newVectors = [jetVec, muVec]#, eleVec, trackVec ]

  loadProds = [readVar(v, allowRenaming=True, isWritten=False, isRead=True) for v in loadProducts]
  for v in loadVectors:
    v['vars'] = [readVar(vvar, allowRenaming=False, isWritten=False, isRead=True, makeVecType=True) for vvar in v['vars']]

  copyVars   = [readVar(v, allowRenaming=True, isWritten=True, isRead=True) for v in copyVariables]
  for v in newVectors:
    v['varNameCount']  = v['prefix']+'Count'
    newVariables.append(v['varNameCount']+'/i')
    v['vars'] = [readVar(v['prefix']+vvar, allowRenaming=False, isWritten=True, isRead=False) for vvar in v['vars']]
  newVars = [readVar(v, allowRenaming=False, isWritten = True, isRead=False) for v in newVariables]
 
  printHeader("Compiling class")
  writeClassName = "ClassToWrite_"+str(nc)+"_"+str(isample) 
  writeClassString = createClassString(className=writeClassName, vars=copyVars + newVars, vectors=newVectors, nameKey = 'stage2Name', typeKey = 'stage2Type')
#  print writeClassString
  s = compileClass(className=writeClassName, classString=writeClassString, tmpDir='/data/'+username+'/tmp/')

#  readClassName = "ClassToRead_"+str(nc)+"_"+str(isample) 
#  readClassString = createClassString(className=readClassName, vars=readVars, vectors=readVectors, nameKey = 'stage1Name', stdVectors=True)
#  printHeader("Class to Read")
##  print readClassString
#  r = compileClass(className=readClassName, classString=readClassString, tmpDir='/data/'+username+'/tmp/')

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
    t.Branch(v['stage2Name'], ROOT.AddressOf(s,v['stage2Name']), v['stage2Name']+'/'+v['stage2Type'])
  for v in newVectors:
    for var in v['vars']:
      t.Branch(var['stage2Name'], ROOT.AddressOf(s,var['stage2Name']), var['stage2Name']+'['+v['varNameCount']+']/'+var['stage2Type'])

  chain_gDir.cd()

  for bin in sample["bins"]:
    commoncf = "Sum$((muonsDz>0.05||muonsDxy>0.02)&&muonsPt>20)==0"
    if options.chmode.startswith("looseDoubleMu"):
      commoncf += "&&Sum$(muonsDz<0.5&&muonsPt>15)==2"
    if 'HTGr200' in options.chmode:
      commoncf+="&&Sum$(jetsPt*(jetsPt>30))>=200"
    if 'HTSm200' in options.chmode:
      commoncf+="&&Sum$(jetsPt*(jetsPt>30))<200"
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
    del c

    handles={}
    products={} 
    for v in copyVars + loadProds:
      handles[v['stage1Name']] = Handle(v['stage1Type'])
    for v in loadEDMCollections:
      handles[v['name']] = Handle(v['edmType'])
    for v in loadVectors:
      for vvar in v['vars']:
        handles[v['prefix']+vvar['stage1Name']] = Handle(vvar['stage1Type'])

    events = Events(bin["filenames"])
    events.to(0)

    #Get Branch descriptions
    bds = events._event.getBranchDescriptions()
    labels={}
    for i in range(bds.size()):
      labels[bds[i].productInstanceName()] = tuple(bds[i].branchName().replace('.','').split('_')[1:3])
       
    if options.small:
      if number_events>1001:
        number_events=1001
    start = int(options.fromPercentage/100.*number_events)
    stop  = int(options.toPercentage/100.*number_events)
    print "Reading: ", sample["name"]
    print "bin    : ", bin['dbsName']
    print "with",number_events,"events using cut", commoncf
    print "Reading percentage ",options.fromPercentage, "to",options.toPercentage, "which is range",start,"to",stop,"of",number_events
    for nev in range(start, stop):
      if (nev%1000 == 0) and nev>0 :
        print nev
#      # Update all the Tuples
      if elist.GetN()>0 and ntot>0:
        s.init()
        events.to(elist.GetEntry(nev))
        s.weight = bin['weight']

        for v in loadEDMCollections:
          events.getByLabel(v['label'],handles[v['name']])
          products[v['name']] =handles[v['name']].product()

        for v in copyVars + loadProds:
          events.getByLabel(labels[v['stage1Name']], handles[v['stage1Name']])
          products[v["stage1Name"]]=handles[v['stage1Name']].product()[0]
        for v in loadVectors:
          products[v['prefix']]={}
          for vvar in v['vars']:
            events.getByLabel(labels[v['prefix']+vvar['stage1Name']], handles[v['prefix']+vvar['stage1Name']])
            products[v['prefix']][vvar["stage1Name"]]=handles[v['prefix']+vvar['stage1Name']].product()
            
        for v in copyVars:
          exec('s.'+v['stage2Name']+'=products[v["stage1Name"]]')
        s.event = events._event.id().event()

        allLooseMuons = getAllMuonsStage1(products['muons'], products['nmuons'])

#  nmuCount = int(getVarValue(c,'nmuCount'))
        muons = filter(lambda m:m['pt']>15 and m['relIso']<0.2 , allLooseMuons)
        if len(muons)==2:
          s.mll = sqrt(2.*muons[0]['pt']*muons[1]['pt']*(cosh(muons[0]['eta']-muons[1]['eta'])-cos(muons[0]['phi']-muons[1]['phi'])))
          if not abs(s.mll-90.1)<15:continue
          s.ptZ = sqrt((muons[0]['pt']*cos(muons[0]['phi'])+muons[1]['pt']*cos(muons[1]['phi']))**2+(muons[0]['pt']*sin(muons[0]['phi'])+muons[1]['pt']*sin(muons[1]['phi']))**2)
          s.phiZ = atan2( muons[0]['pt']*sin(muons[0]['phi'])+muons[1]['pt']*sin(muons[1]['phi']), muons[0]['pt']*cos(muons[0]['phi'])+muons[1]['pt']*cos(muons[1]['phi']) )
 
        jResult = getGoodJetsStage1(jets=products['jets'], njets = products['nJets'], crossCleanObjects = muons, dR = options.DR)#, jermode=options.jermode, jesmode=options.jesmode)
        jetResult = jResult['jets']

        idJets30 = filter(lambda j:j['id'] and j['isolated'], jetResult)
        s.ht = sum([ j['pt'] for j in idJets30])
        s.njets    = len(idJets30)
        s.njetsFailID = len(filter(lambda j:not j['id'] and j['isolated'], jetResult))
        s.nbtags      = len(filter(lambda j:j['btag']>0.679 and abs(j['eta'])<2.4, idJets30))
        s.nmu  = len(allLooseMuons)

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

        s.muCount = min(muVec['nMax'],s.nmu)
        for i in xrange(s.muCount):
          s.muPt[i] = allLooseMuons[i]['pt']
          s.muEta[i] = allLooseMuons[i]['eta']
          s.muPhi[i] = allLooseMuons[i]['phi']
          s.muPdg[i] = allLooseMuons[i]['Pdg']
          s.muRelIso[i] = allLooseMuons[i]['relIso']
          s.muDxy[i] = allLooseMuons[i]['Dxy']
          s.muDz[i] = allLooseMuons[i]['Dz']
          s.muNormChi2[i] = allLooseMuons[i]['NormChi2']
          s.muNValMuonHits[i] = allLooseMuons[i]['NValMuonHits']
          s.muNumMatchedStations[i] = allLooseMuons[i]['NumMatchedStations']
          s.muPixelHits[i] = allLooseMuons[i]['PixelHits']
          s.muNumtrackerLayerWithMeasurement[i] = allLooseMuons[i]['NumtrackerLayerWithMeasurement']
          s.muIsGlobal[i] = allLooseMuons[i]['IsGlobal']
          s.muIsTracker[i] = allLooseMuons[i]['IsTracker']
          s.muIsPF[i] = allLooseMuons[i]['IsPF']
          s.muIso03sumChargedHadronPt[i] = allLooseMuons[i]['Iso03sumChargedHadronPt']
          s.muIso03sumNeutralHadronEt[i] = allLooseMuons[i]['Iso03sumNeutralHadronEt']
          s.muIso03sumPhotonEt[i] = allLooseMuons[i]['Iso03sumPhotonEt']
          s.muIso03sumPUChargedHadronPt[i] = allLooseMuons[i]['Iso03sumPUChargedHadronPt']

        tmpDir = ROOT.gDirectory.func()
        chain_gDir.cd()
        t.Fill()
        tmpDir.cd()
    del events
#          dbf = ROOT.gDirectory.func()
#          f.cd()
#          print 'before',dbf,'now',ROOT.gDirectory.func(), 'go back to',pyroot_gDir
#          t.Fill()
#          pyroot_gDir.cd()
    del elist
  if True or not options.small: #FIXME
    print "Now writing",ofile
    f = ROOT.TFile(ofile, "recreate")
    t.Write()
    f.Close()
    print "Done with writing",ofile
  else:
    print "Results not written!"
  del t
