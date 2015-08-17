#!/bin/env python
import subprocess
import os, re
import shutil

from optparse import OptionParser

parser = OptionParser()
parser.add_option("--source", dest="source", default="", type="string", action="store", help="source directory in users dpm folder")
parser.add_option("--usernameDPM", dest="usernameDPM", default="schoef", type="string", action="store", help="username on DPM")
parser.add_option("--usernameNFS", dest="usernameNFS", default="rschoefbeck", type="string", action="store", help="username on NFS")
parser.add_option("--treeFilename", dest="treeFilename", default="tree_", type="string", action="store", help="tree filename")
parser.add_option("--logFilename", dest="logFilename", default="output.log_", type="string", action="store", help="log file name")
parser.add_option("--targetDir", dest="targetDir", default=".", type="string", action="store", help="target directory in users NFS folder")
parser.add_option("--dpmDir", dest="dpmDir", default="/dpm/oeaw.ac.at/home/cms/store/user/", type="string", action="store", help="default dpm string /dpm/oeaw.ac.at/home/cms/store/user/")
parser.add_option("--overwrite", dest="overwrite", action="store_true", default=False, help="Overwrite chunks?") 
parser.add_option("--verbose", dest="verbose", action="store_true", default=False, help="verbose") 
parser.add_option("--suggest", dest="suggest", action="store_true", default=False, help="suggest copy commands by descending into subdirectories") 

(options, args) = parser.parse_args()

cpCMD="/usr/bin/rfcp"
pretend=False

def isNonEmptyDir(fileLine):
  try:
    lsplit = fileLine.split()
    return lsplit[4]=='0' and int(lsplit[1])>0
  except:
    return False
  return False

def isNonEmptyFile(fileLine):
  try:
    lsplit = fileLine.split()
    return int(lsplit[4])>0 and int(lsplit[1])==1
  except:
    return False
  return False

def filename(line):
  return line.split()[-1]

def isTreeFilename(fname):
  return fname.endswith('.root') and fname.split('/')[-1].startswith(options.treeFilename)
def isLogFilename(fname):
  return fname.endswith('.tgz') and fname.split('/')[-1].startswith(options.logFilename)

def getAbsDPMPath(relpath):
  return '/'.join([options.dpmDir,options.usernameDPM,relpath])
def getAbsNFSPath(relpath):
  return '/'.join(['/data',options.usernameNFS,relpath])

def ls(relpath):
  abspath = getAbsDPMPath(relpath) 
  p = subprocess.Popen(["dpns-ls -l "+ abspath], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  res=[]
  for line in p.stdout.readlines():
      line = line[:-1]
      fname = filename(line)
      if isNonEmptyDir(line):
        res.append({'isDir':True, 'isFile':False, 'path':relpath+'/'+fname, 'isLogFile':False, 'isTreeFile':False})
      elif isNonEmptyFile(line):
        res.append({'isDir':False, 'isFile':True, 'path':relpath+'/'+fname, 'isLogFile':isLogFilename(fname), 'isTreeFile':isTreeFilename(fname)})
      else:
        print "Skipping line:\n%s"%line
  return res 

def getDirs(res):
  return filter(lambda f:f['isDir'], res)

def isCMGOutputDirectory(res, verbose=options.verbose):
  treeFiles = len(filter(lambda f:f['isTreeFile'], res))
  logFiles = len(filter(lambda f:f['isLogFile'], res))
  isCMG = treeFiles>0 and logFiles>0
  if isCMG:
    if verbose or options.verbose: print "Found %i tree files and %i log files -> This is a cmg directory."%(treeFiles, logFiles)
  return isCMG

def suggestTargetDir(relpath):
  s = filter(lambda s:s!='',relpath.split('/'))
  if len(s)>0:
    if len(s[-1])==4 and s[-1].isdigit():  #last path in crab is /0000/, /0001/ -> remove it
      s=s[:-1]
  if len(s)>0:
    if '_' in s[-1] and False not in [x.isdigit() for x in s[-1].split('_')]: #last but one path is /data_time/ -> remove it
      s=s[:-1]
  return '_'.join(s)

def walkPath(relpath):
  res=ls(relpath)
  if isCMGOutputDirectory(res):
    if options.verbose:print "Found CMG dir: %s"%relpath
    print ' '.join(['getCMGFromDPM.py', '--usernameDPM='+options.usernameDPM, '--target='+suggestTargetDir(relpath), '--usernameNFS='+options.usernameNFS, '--source='+relpath ])
  else:
    dirs = getDirs(res)
    if len(dirs)>0:
      for f in getDirs(res):
        if options.verbose:print "Stepping into %s"%f['path']
        walkPath(f['path'])
    else:
      if options.verbose: print "Nothing found in %s"%relpath

def getN(f):
  if f['isFile']:
    s=f['path'].split('/')[-1]
    ints = map(int, re.findall(r'\d+', s))
    assert len(ints)>0, 'Couldn\'nt find number in %s'%f['path']
    assert len(ints)<=1, 'Found more than one number in  %s'%f['path']
    return ints[0] 

def copy(source, target, pretend=True):
  if not pretend:
    if options.verbose: subprocess.call(["echo", cpCMD, source, target])
    return subprocess.call([cpCMD, source, target])
  else:
    return subprocess.call(["echo", cpCMD, source, target])
  return 0

if options.suggest:
  walkPath(options.source)
else:
  res = ls(options.source)
  assert isCMGOutputDirectory(res, verbose=True), "This does not look like a cmg output directory: %s\ntree file: %s, log file: %s\ncontent: %s"%(options.source, options.treeFilename, options.logFilename, ', '.join([f['path'] for f in res]))
  treeFiles = {getN(f2):f2 for f2 in filter(lambda f:f['isTreeFile'], res)}
  logFiles = {getN(f2):f2 for f2 in filter(lambda f:f['isLogFile'], res)}
  pairs = {n:[logFiles[n], treeFiles[n]] for n in treeFiles.keys() if n in logFiles.keys()}
  print "Now working through %i pairs of log- and tree files."%len(pairs)

  for n, [logFile, treeFile] in pairs.iteritems():
    chunkDir = getAbsNFSPath(options.targetDir).rstrip('/')+'_Chunk_'+str(n)
    if os.path.exists(chunkDir):
      if options.overwrite:
        shutil.rmtree(chunkDir)
      else:
        print "Chunk directory %s found -> Skipping."%chunkDir
        continue
    os.makedirs(chunkDir)
    lf = getAbsDPMPath(logFile['path'])
    tlf = '/'.join([chunkDir, logFile['path'].split('/')[-1]]) 
    cp_lf=copy(lf, tlf, pretend=pretend)
    tf = getAbsDPMPath(treeFile['path'])
    if not cp_lf==0:
      print "Could not copy log file %s to %s! Cleaning %s."%(lf, tlf,chunkDir)
      shutil.rmtree(chunkDir)
      continue

    targetTreeFileName =  '_'.join(treeFile['path'].split('/')[-1].replace('.root','').split('_')[:-1])+'.root' #removing the _1 from tree_1.root
    ttf='/'.join([chunkDir, targetTreeFileName])
    cp_tf=copy(tf, ttf, pretend=pretend)
    if not cp_tf==0:
      print "Could not copy tree file %s to %s! Cleaning %s."%(tf, ttf,chunkDir)
      shutil.rmtree(chunkDir)
      continue

    if cp_lf==0 and cp_tf==0:
      print "Unpacking log: %s"%tlf
      tar_tlf = subprocess.call(['tar','-xzf', tlf, '-C', chunkDir, '--strip', '1'])
      if not tar_tlf==0:
        print "Could not untar %s! Cleaning %s."%(tlf, chunkDir)
        shutil.rmtree(chunkDir)
        continue

    preprocessorFile = chunkDir+'/cmsswPreProcessing.root' #remove preprocessor file
    if os.path.exists(preprocessorFile):os.remove(preprocessorFile)
    os.remove(tlf) #remove target log file
    print "... done."
  print "Done with copying %i files"%len(pairs)
