#!/bin/env python
import os, sys, uuid, subprocess
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--dpmDir", dest="dpmDir", default="/dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_140314", type="string", action="store", help="dpmDir: What to do.")
parser.add_option("--tmpDir", dest="tmpDir", default="/data/schoef/tmp/", type="string", action="store", help="tmpDir")
parser.add_option("--targetSize", dest="targetSize", default="1000", type="float", action="store", help="Target filesize in MB")
parser.add_option("--noPretend", dest="noPretend", action="store_true", default=False, help="Just pretend.")
parser.add_option("--onlyLocal", dest="onlyLocal", action="store_true", default=False, help="Dont delete original files.")
parser.add_option("--onlyHistos", dest="onlyHistos", action="store_true", default=True, help="Use only histo_ files.")

(options, args) = parser.parse_args()
print "dpmDir:",options.dpmDir, 'targetSize',options.targetSize

def readFileSize(f):
  p = subprocess.Popen(["dpns-ls -l "+ f], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  line=""
  for line in p.stdout.readlines():
    line = line[:-1]
  return int(line.split()[4])

files = []
p1 = os.popen("dpns-ls -l "+options.dpmDir+"/")
while 1:
  l=p1.readline()
  if not l:break
  if l.count('histo_') or not options.onlyHistos:
    files.append([int(l[:-1].split()[4])/1024.**2, l[:-1].split()[-1]])
p1.close()

jobs=[]

jobSize=0.
jobFiles=[]
for i, f in enumerate(files):
  jobSize+=f[0]
  jobFiles.append(f[1])
  if jobSize>options.targetSize or i+1==len(files):
    jobs.append([jobFiles, jobSize])
    jobSize=0.
    jobFiles=[]

for j, size in jobs:
  print j, '--> size', size
#  localFileName = 'root://hephyse.oeaw.ac.at/'+options.dpmDir+'/'+targetFileName
  localFile = str(uuid.uuid4())
  localFileList = options.tmpDir+'/'+localFile+'.txt'
#  localFileName = '/data/schoef/tmp/'+targetFileName
  localFileName = options.tmpDir+'/'+localFile+'.root'
#  targetFileName='histo_'
#  targetFileName+='_'.join([f.split('_')[1] for f in j])
#  targetFileName+='.root'
  targetFileName = localFile+'.root' 
  print localFileName, targetFileName
  list = file(localFileList, 'w')
  dpmSize=0
  for f in j:
    list.write('root://hephyse.oeaw.ac.at/'+options.dpmDir+'/'+f+'\n')
    dpmSize+=readFileSize(options.dpmDir+'/'+f)
  list.close()

#  os.system('edmCopyPickMerge inputFiles_load='+localFileList+' outputFile='+localFileName+' maxSize=-1  &>/dev/null')
  prefix=''
  if not options.noPretend:
    prefix='echo '
  os.system(prefix+'edmCopyPickMerge inputFiles_load='+localFileList+' outputFile='+localFileName+' maxSize=-1')
  if not options.onlyLocal:
    os.system(prefix+'rfcp '+localFileName+' '+options.dpmDir+'/'+targetFileName)
    os.system(prefix+'rm -f '+localFileName)
    os.system(prefix+'rm -f '+localFileList)
  if options.noPretend:
    finalSize=readFileSize(options.dpmDir+'/'+targetFileName)
  else:
    finalSize=dpmSize
  if finalSize/float(dpmSize)>0.2 and not options.onlyLocal:
    for f in j:
      os.system(prefix+'rfrm '+options.dpmDir+'/'+f)
