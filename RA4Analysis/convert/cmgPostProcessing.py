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

defSampleStr = "ttJetsCSA1450ns,WJetsToLNu_HT100to200,WJetsToLNu_HT200to400,WJetsToLNu_HT400to600,WJetsToLNu_HT600toInf"
#defSampleStr = "ttJetsCSA1450ns"

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--samples", dest="allsamples", default=defSampleStr, type="string", action="store", help="samples:Which samples.")
parser.add_option("--producerName", dest="producerName", default="treeProducerSusySingleLepton", type="string", action="store", help="samples:Which samples.")
parser.add_option("--targetDir", dest="targetDir", default="/data/schoef/cmgTuples/postProcessed_v0/", type="string", action="store", help="target directory.")
parser.add_option("--skim", dest="skim", default="met100", type="string", action="store", help="target directory.")

#parser.add_option("--small", dest="small", default = False, action="store_true", help="Just do a small subset.")
#parser.add_option("--overwrite", dest="overwrite", action="store_true", help="Overwrite?", default=True)
(options, args) = parser.parse_args()
if options.skim=='inc':
  skimCond = "(1)"
if options.skim.startswith('met'):
  skimCond = "met_pt>"+str(float(options.skim[3:]))

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
      inputFilename = sample['dir']+'/'+s['name']+'/'+options.producerName+'/'+options.producerName+'_tree.root'
      if os.path.isfile(inputFilename):
        print "Adding ",n,"events from chunk",s
        nTotEvents+=n
        allFiles.append(inputFilename)
        chunks[i]['file']=inputFilename
    except: print "Chunk",s,"could not be added"
  outDir = options.targetDir+'/'+"/".join([options.skim, sample['name']])
  tmpDir = outDir+'/tmp/'
  os.system('mkdir -p ' + outDir) 
  os.system('mkdir -p '+tmpDir)
  os.system('rm -rf '+tmpDir+'/*')

  newLeaves = 'weight/F'
  leafValues = array('f',[0.])
  lumiWeight = xsec[sample['dbsName']]*target_lumi/float(nTotEvents)
  leafValues[0]=lumiWeight
  filesForHadd=[]
  for j, s in enumerate(chunks):
    if not s.has_key('file'):continue
    rf = ROOT.TFile(s['file'])
    assert not rf.IsZombie()
    rf.cd()
    tc = rf.Get(options.producerName)
#    tc.Draw('>>eList', skimCond)
#    eList = ROOT.gDirectory.Get('eList')
#    tc.SetEventList(eList)
    ROOT.gDirectory.cd('PyROOT:/')
    t = tc.CopyTree(skimCond)
    rf.Close()
    t.SetName("Events")
    nEvents = t.GetEntries()
    newBranch = t.Branch( "weight" , leafValues, newLeaves )
    print "File",s['file'],'chunk',s['name'],"found", nEvents, '(skim:',options.skim,'cond:', skimCond,') with weight',lumiWeight, 'in Chain -> post processing...'
    for i in range(nEvents):
      newBranch.Fill()
    newFileName = sample['name']+'_'+s['name']+'.root'
    filesForHadd.append(newFileName)
    f = ROOT.TFile(tmpDir+'/'+newFileName, 'recreate')
    t.Write()
    f.Close()
    print "Written",tmpDir+'/'+newFileName
    del t
    del tc
#    del eList
  
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

