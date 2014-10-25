import ROOT
import sys, os, copy, random, subprocess, datetime
from array import array
from Workspace.RA4Analysis.cmgTuples import *

from Workspace.HEPHYPythonTools.xsec import xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile

subDir = "postProcessed_v0"
target_lumi = 1000 #pb-1

from localInfo import username
outputDir = "/data/"+username+"/"+subDir+"/"

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--samples", dest="allsamples", default="ttJetsCSA1450ns", type="string", action="store", help="samples:Which samples.")
parser.add_option("--producerName", dest="producerName", default="treeProducerSusySingleLepton", type="string", action="store", help="samples:Which samples.")
parser.add_option("--targetDir", dest="targetDir", default="/data/schoef/cmgTuples/postProcessed_v0/", type="string", action="store", help="target directory.")
#parser.add_option("--small", dest="small", default = False, action="store_true", help="Just do a small subset.")
#parser.add_option("--overwrite", dest="overwrite", action="store_true", help="Overwrite?", default=True)

(options, args) = parser.parse_args()
if sys.argv[0].count('ipython'):
  options.small=True

exec('allSamples=['+options.allsamples+']')
for sample in allSamples:
  chunks = [{'name':x} for x in os.listdir(sample['dir']) if x.startswith(sample['chunkString'])]
  nTotEvents=0
  allFiles=[]
  for i, s in enumerate(chunks):
    try:
      logfile = sample['dir']+'/'+s['name']+'/log.txt'
      line = [x for x in subprocess.check_output(["cat", logfile]).split('\n') if x.count('number of events processed')]
      assert len(line)==1,"Didn't find event number in file %s"%logfile
      n = int(line[0].split()[-1])
      rootFile = sample['dir']+'/'+s['name']+'/'+options.producerName+'/'+options.producerName+'_tree.root'
      if os.path.isfile(rootFile):
        print "Adding ",n,"events from chunk",s
        nTotEvents+=n
        allFiles.append(rootFile)
        chunks[i]['file']=rootFile
    except: print "Chunk",s,"could not be added"
  os.system('mkdir -p '+options.targetDir+'/'+sample['name']) 
  newLeaves = 'weight/F'
  leafValues = array('f',[0.])
  lumiWeight = xsec[sample['dbsName']]*target_lumi/float(nTotEvents)
  leafValues[0]=lumiWeight
  filesForHadd=[]
  tmpDir = options.targetDir+'/'+sample['name']+'/tmp/'
  os.system('mkdir -p '+tmpDir)
  os.system('rm -rf '+tmpDir+'/*')
  for j, s in enumerate(chunks):
    if not s.has_key('file'):continue
    rf = ROOT.TFile(s['file'])
    assert not rf.IsZombie()
    rf.cd()
    tc = rf.Get(options.producerName)
    ROOT.gDirectory.cd('PyROOT:/')
    t = tc.CloneTree()
    rf.Close()
    t.SetName("Events")
    nEvents = t.GetEntries()
    newBranch = t.Branch( "weight" , leafValues, newLeaves )
    print "File",s['file'],'chunk',s['name'],"found", nEvents, ' with weight',lumiWeight, 'in Chain -> adding branches...'
    for i in range(nEvents):
      newBranch.Fill()
    newFileName = sample['name']+'_'+s['name']+'.root'
    filesForHadd.append(newFileName)
    f = ROOT.TFile(tmpDir+'/'+newFileName, 'recreate')
    t.Write()
    f.Close()
    print "Written",newFileName
    del t
    del tc
  
  size=0
  counter=0
  files=[]
  for f in filesForHadd:
    size+=os.path.getsize(tmpDir+'/'+f)
    files.append(f)
    if size>10**9 or f==filesForHadd[-1]:
      ofile = options.targetDir+'/'+sample['name']+'/'+sample['name']+'_'+str(counter)+'.root'
      print "Running hadd on", tmpDir, files
      os.system('cd '+tmpDir+';hadd -f '+ofile+' '+' '.join(files))
      print "Written",ofile
      size=0
      counter+=1
      files=[]
  os.system("rm -rf "+tmpDir)

