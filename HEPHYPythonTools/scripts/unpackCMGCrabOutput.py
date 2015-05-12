#!/bin/env python

##Usage:
##python untarCrabOutput.py --dir=/data/nrad/cmgTuples/crab_ece_v1/test_runs/test2/test2 --suffix=".tgz" --sampleName="WJetsToLNu_HT100to200"

import subprocess
import os
import sys

from optparse import OptionParser

parser = OptionParser()
parser.add_option("--userNameNFS", dest="userNameNFS", default="schoef", type="string", action="store", help="username on NFS disk /data/")
parser.add_option("--dir", dest="dir", default="./_", type="string", action="store", help="which dir")
parser.add_option("--suffix", dest="suffix", default=".tgz", type="string", action="store", help="Suffix of tarfile")
parser.add_option("--untar", dest="untar", default=".tgz", type="string", action="store", help="what kind of tar file")
parser.add_option("--hadd", dest="hadd",default=False,action="store_true",help="adds chunks together.")
parser.add_option("--clean", dest="clean",default=False,action="store_true",help="move chunks to Chunks/ after processing. relevant only with --hadd")


#parser.add_option("--sampleName", dest="sampleName", default="TTJets", type="string", action="store", help="Name of sample name which will be used with chunks")
(options, args) = parser.parse_args()



directory= "/data/"+options.userNameNFS+'/'+options.dir

suf = options.suffix

print options.dir.split("/")

if not options.dir.endswith("/"):
  sampleName = options.dir.split("/")[-1]
elif not options.dir[:-1].endswith("/"):
  sampleName = options.dir.split("/")[-2]
else:
  print "can find sampleName in the dir", options.dir
  print "you should probably stop the code"



treeName="susySingleLepton"
finalTreeName="tree.root"
treeProducerName="treeProducerSusySingleLepton"
#if not os.path.isdir(oDir):
#  print "Creating ",oDir
#  os.system("mkdir -p "+oDir)

#lsNFS = os.listdir(oDir)
debug =0 
p = subprocess.Popen(["ls -l "+ directory], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)




print "Unpacking sample:  ", sampleName
#print "processing directories to: ", directory+"/../"+sampleName
print "To CMG Chunks:     ", directory+sampleName+"_Chunk*"
print "And root files in  ", directory+sampleName+"_Chunk*"+"/"+treeProducerName+"/"+finalTreeName



for line in p.stdout.readlines():
  linePart=line[:-1].split()
  #print "#### ", linePart
  if linePart[0]=='total':
    print line
    continue
  else: 
    if linePart[-1].endswith(suf):
      #print "##", line
      filename = linePart[-1]
      fileNum = filename[:-len(suf)].split("_")[1]
      cmgChunks = directory+'/'+sampleName +"_Chunk" + fileNum
      rootFileName=treeName+"_"+fileNum+'.root'
      #print "##", linePart[-5]
      #size = int(linePart[-5]) 
      os.system("mkdir %s"%cmgChunks)
      os.system("tar -xf %s --directory=%s --strip-components=1"%(directory+"/"+filename,cmgChunks))
      os.system( "mv %s %s"%(directory + '/' + rootFileName,cmgChunks+'/'+treeProducerName+'/'+finalTreeName))
      os.system("rm -rf %s"%(directory+"/"+filename) )
      if debug:
        print filename, fileNum , sampleName, cmgChunks #, size 
        print "mkdir %s"%cmgChunks     
        print "tar -xf %s --directory=%s --strip-components=1"%(directory+"/"+filename,cmgChunks)
        print "rm -rf %s"%(directory+"/"+filename) 
        print "mv %s %s"%(directory + '/' + rootFileName ,cmgChunks+'/'+treeProducerName+'/'+finalTreeName)
#os.system("mv %s %s"%(directory, directory+"/../"+sampleName))
#if debug:
#  print "mv %s %s"%(directory, directory+"/../"+sampleName)
if options.hadd:
  cleanstring=""
  if options.clean:
    cleanstring=" --clean"
  os.system( "haddChunks.py  %s %s"%(directory ,cleanstring))
  print ( "haddChunks.py  %s %s"%(directory ,cleanstring)  )
  #os.system( "mv %s %s"%(directory + '/' + rootFileName,cmgChunks+'/'+treeProducerName+'/'+finalTreeName))


retval = p.wait()

