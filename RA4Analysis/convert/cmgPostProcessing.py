import ROOT
import sys, os, copy, random, subprocess, datetime
from array import array
from Workspace.RA4Analysis.cmgTuples import *
from Workspace.RA4Analysis.cmgObjectSelection import cmgLooseLepIndices, cmgLooseLepID, cmgGoodLepID

from Workspace.HEPHYPythonTools.xsec import xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile
from Workspace.RA4Analysis.convertHelpers import compileClass, readVar, printHeader, typeStr, createClassString

subDir = "postProcessed_v0"
target_lumi = 1000 #pb-1

from localInfo import username

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

#defSampleStr = "WJetsToLNu_HT100to200,WJetsToLNu_HT200to400,WJetsToLNu_HT400to600,WJetsToLNu_HT600toInf"
#defSampleStr = "WJetsToLNu_HT200to400,WJetsToLNu_HT400to600,WJetsToLNu_HT600toInf"
#defSampleStr = "WJetsToLNu_HT600toInf"
#defSampleStr = "ttJetsCSA1450ns"
#defSampleStr = "T5Full_1200_1000_800,T5Full_1500_800_100"
defSampleStr = "T1qqqq_1400_325_300"
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--samples", dest="allsamples", default=defSampleStr, type="string", action="store", help="samples:Which samples.")
parser.add_option("--producerName", dest="producerName", default="treeProducerSusySingleLepton", type="string", action="store", help="samples:Which samples.")
parser.add_option("--targetDir", dest="targetDir", default="/data/"+username+"/cmgTuples/postProcessed_v0/", type="string", action="store", help="target directory.")
parser.add_option("--skim", dest="skim", default="singleLepton", type="string", action="store", help="target directory.")

#parser.add_option("--small", dest="small", default = False, action="store_true", help="Just do a small subset.")
#parser.add_option("--overwrite", dest="overwrite", action="store_true", help="Overwrite?", default=True)
(options, args) = parser.parse_args()
if options.skim=='singleLepton':
  skimCond = "(1)"
if options.skim.startswith('met'):
  skimCond = "met_pt>"+str(float(options.skim[3:]))

if sys.argv[0].count('ipython'):
  options.small=True

def getChunks(sample):
  chunks = [{'name':x} for x in os.listdir(sample['dir']) if x.startswith(sample['chunkString'])]
  nTotEvents=0
  allFiles=[]
  for i, s in enumerate(chunks):
    try:
      logfile = sample['dir']+'/'+s['name']+'/log.txt'
      line = [x for x in subprocess.check_output(["cat", logfile]).split('\n') if x.count('number of events processed')]
      assert len(line)==1,"Didn't find event number in file %s"%logfile
      n = int(line[0].split()[-1])
      inputFilename = sample['dir']+'/'+s['name']+'/'+options.producerName+'/'+options.producerName+'_tree.root'
      if os.path.isfile(inputFilename):
        nTotEvents+=n
        allFiles.append(inputFilename)
        chunks[i]['file']=inputFilename
    except: print "Chunk",s,"could not be added"
  print "Found",len(chunks),"chunks for sample",sample["name"]
  return chunks, nTotEvents

def getTreeFromChunk(c, skimCond):
  if not c.has_key('file'):return
  rf = ROOT.TFile(c['file'])
  assert not rf.IsZombie()
  rf.cd()
  tc = rf.Get(options.producerName)
  ROOT.gDirectory.cd('PyROOT:/')
  t = tc.CopyTree(skimCond)
  del tc
  rf.Close()
  return t
    
exec('allSamples=['+options.allsamples+']')
for isample, sample in enumerate(allSamples):
  chunks, nTotEvents = getChunks(sample)
  chunks = chunks
  outDir = options.targetDir+'/'+"/".join([options.skim, sample['name']])
  tmpDir = outDir+'/tmp/'
  os.system('mkdir -p ' + outDir) 
  os.system('mkdir -p '+tmpDir)
  os.system('rm -rf '+tmpDir+'/*')

  lumiWeight = xsec[sample['dbsName']]*target_lumi/float(nTotEvents)
  readVariables = []

  newVariables = ['weight/F']
  newVariables += ['nVetoMuons/I', 'nVetoElectrons/I', 'nGoodMuons/I', 'nGoodElectrons/I', 'singleMuonic/I', 'singleElectronic/I', 'singleLeptonic/I']
  newVariables.extend( ['leptonPt/F', 'leptonEta/F', 'leptonPhi/F', 'leptonPdg/I/0', 'leptonInd/I/-1', 'leptonMass/F'] )
  newVars = [readVar(v, allowRenaming=False, isWritten = True, isRead=False) for v in newVariables]

  aliases = ["st:leptonPt+met_pt", "met:met_pt", "metPhi:met_phi","genmet:met_genPt", "genmetPhi:met_genPhi"]

  readVectors = [\
    {'prefix':'LepGood',  'nMax':2, 'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'relIso03/F', 'tightId/I', 'mass/F']},
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
    print "File",chunk['file'],'chunk',chunk['name'],"found", nEvents, '(skim:',options.skim,'cond:', skimCond,') with weight',lumiWeight, 'in Chain -> post processing...'
    for i in range(nEvents):
      s.init()
      r.init()
      t.GetEntry(i)
      s.weight = lumiWeight
      vetoLepInd = cmgLooseLepIndices(r, ptCut=10, absEtaCut=2.4, relIso03Cut=0.3)
      s.nVetoMuons      = len(filter(lambda i : abs(r.LepGood_pdgId[i])==13, vetoLepInd))
      s.nVetoElectrons  = len(filter(lambda i : abs(r.LepGood_pdgId[i])==11, vetoLepInd))
      goodMuInd =  [i for i in vetoLepInd if abs(r.LepGood_pdgId[i])==13 and cmgGoodLepID(r, i, ptCut=15, absEtaCut=2.4, relIso03Cut=0.12)]
      goodEleInd = [i for i in vetoLepInd if abs(r.LepGood_pdgId[i])==11 and cmgGoodLepID(r, i, ptCut=15, absEtaCut=2.4, relIso03Cut=0.14)]
      s.nGoodMuons = len(goodMuInd) 
      s.nGoodElectrons = len(goodEleInd) 
      s.singleMuonic      = s.nGoodMuons==1 and s.nGoodElectrons==0
      s.singleElectronic  = s.nGoodMuons==0 and s.nGoodElectrons==1
      s.singleLeptonic    = s.singleMuonic or s.singleElectronic
      leadingLepInd = -1
      leadingLepInd = goodMuInd[0] if len(goodMuInd)>0 else -1
      leadingLepInd = goodEleInd[0] if len(goodEleInd)>0 and (leadingLepInd<0 or r.LepGood_pt[leadingLepInd]<r.LepGood_pt[goodEleInd[0]]) else leadingLepInd
      if leadingLepInd>=0:
        s.leptonPt  = r.LepGood_pt[leadingLepInd]
        s.leptonInd = leadingLepInd 
        s.leptonEta = r.LepGood_eta[leadingLepInd]
        s.leptonPhi = r.LepGood_phi[leadingLepInd]
        s.leptonPdg = r.LepGood_pdgId[leadingLepInd]
        s.leptonMass= r.LepGood_mass[leadingLepInd]
      for v in newVars:
        v['branch'].Fill()
    newFileName = sample['name']+'_'+chunk['name']+'.root'
    filesForHadd.append(newFileName)
    f = ROOT.TFile(tmpDir+'/'+newFileName, 'recreate')
    t.Write()
    f.Close()
    print "Written",tmpDir+'/'+newFileName
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

