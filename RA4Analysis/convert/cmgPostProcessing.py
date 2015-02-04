import ROOT
import sys, os, copy, random, subprocess, datetime
from array import array
from Workspace.RA4Analysis.cmgObjectSelection import cmgLooseLepIndices, splitIndList

from Workspace.HEPHYPythonTools.xsec import xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getObjDict, getFileList
from Workspace.RA4Analysis.convertHelpers import compileClass, readVar, printHeader, typeStr, createClassString

subDir = "postProcessed_v4_PHYS14V1"
#from Workspace.RA4Analysis.cmgTuples_v3 import *
from Workspace.RA4Analysis.cmgTuples_v4_PHYS14 import *

target_lumi = 1000 #pb-1

from localInfo import username

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

#defSampleStr = "ttJets_PU20bx25"
defSampleStr = "ttWJets_PU20bx25,ttZJets_PU20bx25,ttHJets_PU20bx25"
defSampleStr = "ttH_PU20bx25"

branchKeepStrings = ["run", "lumi", "evt", "isData", "xsec", "puWeight", "nTrueInt", "genWeight", "rho", "nVert", "nJet25", "nBJetLoose25", "nBJetMedium25", "nBJetTight25", "nJet40", "nJet40a", "nBJetLoose40", "nBJetMedium40", "nBJetTight40", 
                     "nLepGood20", "nLepGood15", "nLepGood10",  
                     "GenSusyMScan1", "GenSusyMScan2", "GenSusyMScan3", "GenSusyMScan4", "GenSusyMGluino", "GenSusyMGravitino", "GenSusyMStop", "GenSusyMSbottom", "GenSusyMStop2", "GenSusyMSbottom2", "GenSusyMSquark", "GenSusyMNeutralino", "GenSusyMNeutralino2", "GenSusyMNeutralino3", "GenSusyMNeutralino4", "GenSusyMChargino", "GenSusyMChargino2", 
                     "htJet25", "mhtJet25", "htJet40j", "htJet40ja", "htJet40", "htJet40a", "mhtJet40", "mhtJet40a", "nSoftBJetLoose25", "nSoftBJetMedium25", "nSoftBJetTight25", 
                     "met_*", 
                     "nLepOther", "LepOther_*", "nLepGood", "LepGood_*", "ngenLep", "genLep_*", "nTauGood", "TauGood_*", 
                     "ngenPart", "genPart_*", "ngenTau", "genTau_*", "nJet", "Jet_*", "ngenLepFromTau", "genLepFromTau_*"]
#"nGenP6StatusThree", "GenP6StatusThree_*", "nGenTop", "GenTop_*"

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--samples", dest="allsamples", default=defSampleStr, type="string", action="store", help="samples:Which samples.")
parser.add_option("--inputTreeName", dest="inputTreeName", default="treeProducerSusySingleLepton", type="string", action="store", help="samples:Which samples.")
parser.add_option("--targetDir", dest="targetDir", default="/data/"+username+"/cmgTuples/"+subDir+'/', type="string", action="store", help="target directory.")
parser.add_option("--skim", dest="skim", default="", type="string", action="store", help="any skim condition?")
parser.add_option("--leptonSelection", dest="leptonSelection", default="hard", type="string", action="store", help="which lepton selection? 'soft' or 'hard' or 'none'?")

#parser.add_option("--small", dest="small", default = False, action="store_true", help="Just do a small subset.")
#parser.add_option("--overwrite", dest="overwrite", action="store_true", help="Overwrite?", default=True)
(options, args) = parser.parse_args()
if options.skim=='inc' or options.skim=="":
  skimCond = "(1)"
if options.skim.startswith('met'):
  skimCond = "met_pt>"+str(float(options.skim[3:]))

##In case a lepton selection is required, loop only over events where there is one 
if options.leptonSelection.lower()=='soft':
#  skimCond += "&&Sum$(LepGood_pt>5&&LepGood_pt<25&&(LepGood_relIso03*LepGood_pt<7.5)&&abs(LepGood_eta)<2.4)>=1"
  skimCond += "&&Sum$(LepGood_pt>5&&LepGood_pt<25&&LepGood_relIso03<0.4&&abs(LepGood_eta)<2.4)>=1"
if options.leptonSelection.lower()=='hard':
  skimCond += "&&Sum$(LepGood_pt>25&&LepGood_relIso03<0.4&&abs(LepGood_eta)<2.4)>=1"

if sys.argv[0].count('ipython'):
  options.small=True

def getChunks(sample):
  if '/dpm/' in sample['dir']:
    return getChunksFromDPM(sample)
#  elif '/eoscms.cern.ch/' in sample['dir']:
#    return getSampleFromEOS(sample)
  else:
    return getChunksFromNFS(sample)
    

def getChunksFromNFS(sample):
  chunks = [{'name':x} for x in os.listdir(sample['dir']) if x.startswith(sample['chunkString']+'_Chunk') or x==sample['name']]
  nTotEvents=0
  allFiles=[]
  failedChunks=[]
  for i, s in enumerate(chunks):
#      logfile = sample['dir']+'/'+s['name']+'/log.txt'
#      line = [x for x in subprocess.check_output(["cat", logfile]).split('\n') if x.count('number of events processed')]
#      assert len(line)==1,"Didn't find event number in file %s"%logfile
#      n = int(line[0].split()[-1])
      logfile = sample['dir']+'/'+s['name']+'/skimAnalyzerCount/SkimReport.txt'
      if os.path.isfile(logfile):
        line = [x for x in subprocess.check_output(["cat", logfile]).split('\n') if x.count('All Events')]
        assert len(line)==1,"Didn't find event number in file %s"%logfile
        n = int(line[0].split()[2])
        inputFilename = sample['dir']+'/'+s['name']+'/'+options.inputTreeName+'/tree.root'
        if os.path.isfile(inputFilename):
          nTotEvents+=n
          allFiles.append(inputFilename)
          chunks[i]['file']=inputFilename
      else:failedChunks.append(chunks[i])
#    except: print "Chunk",s,"could not be added"
  print "Found",len(chunks),"chunks for sample",sample["name"],'with a total of',nTotEvents,"events. Failed for:",",".join([c['name'] for c in failedChunks]),"(",round(100*len(failedChunks)/float(len(chunks)),1),")%"
  return chunks, nTotEvents

def getChunksFromDPM(sample):
  fileList = getFileList(sample['dir'], minAgeDPM=0, histname='', xrootPrefix='root://hephyse.oeaw.ac.at/')
  chunks = [{'file':x,'name':x.split('/')[-1].replace('.root','')} for x in fileList]
  nTotEvents=0
  for c in chunks:
    c.update({'nEvents':int(c['name'].split('nEvents')[-1])})
    nTotEvents+=c['nEvents']
  print "Found",len(chunks),"chunks for sample",sample["name"]
  return chunks, nTotEvents

#def getSampleFromEOS(sample):
#  fn = sample['dir'].rstrip('/')+'/'+sample['name']+'/'+options.inputTreeName+'/tree.root'
#  chunks = [{'file':fn,'name':fn.split('/')[-1].replace('.root','')}]
#  nTotEvents=0
##  for c in chunks:
##    c.update({'nEvents':int(c['name'].split('nEvents')[-1])})
##    nTotEvents+=c['nEvents']
##  print "Found",len(chunks),"chunks for sample",sample["name"]
#  print chunks
#  return chunks, nTotEvents

def getTreeFromChunk(c, skimCond):
  if not c.has_key('file'):return
  rf = ROOT.TFile.Open(c['file'])
  assert not rf.IsZombie()
  rf.cd()
  tc = rf.Get("tree")
  ROOT.gDirectory.cd('PyROOT:/')
  t = tc.CopyTree(skimCond)
  tc.Delete()
  del tc
  rf.Close()
  del rf
  return t
   
exec('allSamples=['+options.allsamples+']')
for isample, sample in enumerate(allSamples):
  
  chunks, nTotEvents = getChunks(sample)
  chunks = chunks
  
  outDir = options.targetDir+'/'+"/".join([options.skim, options.leptonSelection, sample['name']])
  tmpDir = outDir+'/tmp/'
  os.system('mkdir -p ' + outDir) 
  os.system('mkdir -p '+tmpDir)
  os.system('rm -rf '+tmpDir+'/*')

  lumiWeight = xsec[sample['dbsName']]*target_lumi/float(nTotEvents)
  readVariables = ['met_pt/F']

  newVariables = ['weight/F']
  newVariables += ['nLooseSoftLeptons/I', 'nLooseSoftPt10Leptons/I', 'nLooseHardLeptons/I', 'nTightSoftLeptons/I', 'nTightHardLeptons/I']
  if options.leptonSelection.lower()!='none':
    newVariables.extend( ['st/F', 'leptonPt/F', 'leptonEta/F', 'leptonPhi/F', 'leptonPdg/I/0', 'leptonInd/I/-1', 'leptonMass/F', 'singleMuonic/I', 'singleElectronic/I', 'singleLeptonic/I'] )
  newVars = [readVar(v, allowRenaming=False, isWritten = True, isRead=False) for v in newVariables]

  aliases = [ "met:met_pt", "metPhi:met_phi","genMet:met_genPt", "genMetPhi:met_genPhi"]

  readVectors = [\
    {'prefix':'LepGood',  'nMax':8, 'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'relIso03/F', 'tightId/I', 'mass/F']},
  ]
  readVars = [readVar(v, allowRenaming=False, isWritten=False, isRead=True) for v in readVariables]
  for v in readVectors:
    readVars.append(readVar('n'+v['prefix']+'/I', allowRenaming=False, isWritten=False, isRead=True))
    v['vars'] = [readVar(v['prefix']+'_'+vvar, allowRenaming=False, isWritten=False, isRead=True) for vvar in v['vars']]

  printHeader("Compiling class to write")
  writeClassName = "ClassToWrite_"+str(isample)
  writeClassString = createClassString(className=writeClassName, vars= newVars, vectors=[], nameKey = 'stage2Name', typeKey = 'stage2Type')
#  print writeClassString
  s = compileClass(className=writeClassName, classString=writeClassString, tmpDir='/data/'+username+'/tmp/')

  readClassName = "ClassToRead_"+str(isample)
  readClassString = createClassString(className=readClassName, vars=readVars, vectors=readVectors, nameKey = 'stage1Name', typeKey = 'stage1Type', stdVectors=False)
  printHeader("Class to Read")
#  print readClassString
  r = compileClass(className=readClassName, classString=readClassString, tmpDir='/data/'+username+'/tmp/')

  filesForHadd=[]
  for chunk in chunks:
    t = getTreeFromChunk(chunk, skimCond)
    if not t:continue
    t.SetName("Events")
    nEvents = t.GetEntries()
    for v in newVars:
      v['branch'] = t.Branch(v['stage2Name'], ROOT.AddressOf(s,v['stage2Name']), v['stage2Name']+'/'+v['stage2Type'])
    for v in readVars:
      t.SetBranchAddress(v['stage1Name'], ROOT.AddressOf(r, v['stage1Name']))
    for v in readVectors:
      for var in v['vars']:
        t.SetBranchAddress(var['stage1Name'], ROOT.AddressOf(r, var['stage1Name']))
    for a in aliases:
      t.SetAlias(*(a.split(":")))
    print "File",chunk['file'],'chunk',chunk['name'],"found", nEvents, '(skim:',options.skim,') condition:', skimCond,' with weight',lumiWeight, 'in Chain -> post processing...'

    for i in range(nEvents):
      s.init()
      r.init()
      t.GetEntry(i)
      s.weight = lumiWeight

      #get all >=loose lepton indices
      looseLepInd = cmgLooseLepIndices(r, ptCuts=(10,5), absEtaCuts=(2.4,2.1), hybridIso03={'ptSwitch':0, 'absIso':0, 'relIso':0.4} )
      #split into soft and hard leptons
      looseSoftLepInd, looseHardLepInd = splitIndList(r.LepGood_pt, looseLepInd, 25.)
      #select soft leptons above 10 GeV (for vetoing in the hard lepton selection)
      looseSoftPt10LepInd = filter(lambda i:r.LepGood_pt[i]>10, looseSoftLepInd) 
      #select tight soft leptons (no special tight ID for now)
      tightSoftLepInd = looseSoftLepInd #No tight loose selection as of yet 
      #select tight hard leptons (use POG ID)
      tightHardLepInd = filter(lambda i:r.LepGood_tightId[i], looseHardLepInd)

      s.nLooseSoftLeptons = len(looseSoftLepInd)
      s.nLooseSoftPt10Leptons = len(looseSoftPt10LepInd)
      s.nLooseHardLeptons = len(looseHardLepInd)
      s.nTightSoftLeptons = len(tightSoftLepInd)
      s.nTightHardLeptons = len(tightHardLepInd)

      vars = ['pt', 'eta', 'phi', 'relIso03', 'pdgId']
      allLeptons = [getObjDict(t, 'LepGood', vars, i) for i in looseLepInd]
      looseSoftLep = [getObjDict(t, 'LepGood', vars, i) for i in looseSoftLepInd] 
      looseHardLep = [getObjDict(t, 'LepGood', vars, i) for i in looseHardLepInd]
      looseSoftPt10Lep = [getObjDict(t, 'LepGood', vars, i) for i in looseSoftPt10LepInd]
      tightSoftLep = [getObjDict(t, 'LepGood', vars, i) for i in tightSoftLepInd]
      tightHardLep =  [getObjDict(t, 'LepGood', vars, i) for i in tightHardLepInd]
      
      leadingLepInd = None
      if options.leptonSelection=='hard':
        if s.nTightHardLeptons>=1:
          leadingLepInd = tightHardLepInd[0]
          s.leptonPt  = r.LepGood_pt[leadingLepInd]
          s.leptonInd = leadingLepInd 
          s.leptonEta = r.LepGood_eta[leadingLepInd]
          s.leptonPhi = r.LepGood_phi[leadingLepInd]
          s.leptonPdg = r.LepGood_pdgId[leadingLepInd]
          s.leptonMass= r.LepGood_mass[leadingLepInd]
          s.st = r.met_pt + s.leptonPt
        s.singleLeptonic = s.nTightHardLeptons==1
        if s.singleLeptonic:
          s.singleMuonic      =  abs(s.leptonPdg)==13
          s.singleElectronic  =  abs(s.leptonPdg)==11
        else:
          s.singleMuonic      = False 
          s.singleElectronic  = False 

      if options.leptonSelection=='soft':
        #Select hardest tight lepton among soft leptons
        if s.nTightSoftLeptons>=1:

          leadingLepInd = tightSoftLepInd[0]
          s.leptonPt  = r.LepGood_pt[leadingLepInd]
          s.leptonInd = leadingLepInd 
          s.leptonEta = r.LepGood_eta[leadingLepInd]
          s.leptonPhi = r.LepGood_phi[leadingLepInd]
          s.leptonPdg = r.LepGood_pdgId[leadingLepInd]
          s.leptonMass= r.LepGood_mass[leadingLepInd]
          s.st = r.met_pt + s.leptonPt
        s.singleLeptonic = s.nTightSoftLeptons==1
        if s.singleLeptonic:
          s.singleMuonic      =  abs(s.leptonPdg)==13
          s.singleElectronic  =  abs(s.leptonPdg)==11
        else:
          s.singleMuonic      = False 
          s.singleElectronic  = False 

#      print "Selected",s.leptonPt

      for v in newVars:
        v['branch'].Fill()
    newFileName = sample['name']+'_'+chunk['name']+'.root'
    filesForHadd.append(newFileName)
    f = ROOT.TFile(tmpDir+'/'+newFileName, 'recreate')
    t.SetBranchStatus("*",0)
    for b in branchKeepStrings + [v['stage2Name'] for v in newVars] +  [v.split(':')[1] for v in aliases]:
      t.SetBranchStatus(b, 1)
    t2 = t.CloneTree()
    t2.Write()
    f.Close()
    print "Written",tmpDir+'/'+newFileName
    del f
    for v in newVars:
      del v['branch']
    del t2
    t.Delete()
    del t
  
  size=0
  counter=0
  files=[]
  for f in filesForHadd:
    size+=os.path.getsize(tmpDir+'/'+f)
    files.append(f)
    if size>10**9 or f==filesForHadd[-1]:
      ofile = outDir+'/'+sample['name']+'_'+str(counter)+'.root'
      print "Running hadd on", tmpDir, files
      os.system('cd '+tmpDir+';hadd -f '+ofile+' '+' '.join(files))
      print "Written", ofile
      size=0
      counter+=1
      files=[]
  os.system("rm -rf "+tmpDir)

