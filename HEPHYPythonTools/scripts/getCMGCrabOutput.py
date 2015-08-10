#!/bin/env python

import subprocess
import os

from optparse import OptionParser

parser = OptionParser()
parser.add_option("--userNameDPM", dest="userNameDPM", default="", type="string", action="store", help="username of DPM User")
parser.add_option("--userNameNFS", dest="userNameNFS", default="schoef", type="string", action="store", help="username on NFS disk /data/")
parser.add_option("--source", dest="source", default="pat_130418/8TeV-T1tttt-test", type="string", action="store", help="source directory in users dpm folder")
parser.add_option("--fileName", dest="fileName", default="histo_", type="string", action="store", help="which filenames")
parser.add_option("--suffix", dest="suffix", default=".root", type="string", action="store", help="file sufix. multiple sufix can be given seperated by space, i.e `.root .tgz` ")
parser.add_option("--target", dest="target", default="pat_130501/8TeV-T1tttt", type="string", action="store", help="target directory in users NFS folder")
parser.add_option("--dpmDir", dest="dpmStr", default="/dpm/oeaw.ac.at/home/cms/store/user/", type="string", action="store", help="default dpm string /dpm/oeaw.ac.at/home/cms/store/user/")
parser.add_option("--onlyUpdate", dest="onlyUpdate", action="store_false", help="Only update.") 

(options, args) = parser.parse_args()

dpmDir = options.dpmStr+'/'+options.userNameDPM+'/'+options.source
oDir = '/data/'+options.userNameNFS+'/'+options.target

suf = options.suffix
sufList = suf.split()

if not os.path.isdir(oDir):
  print "Creating ",oDir
  os.system("mkdir -p "+oDir)

lsNFS = os.listdir(oDir)

p = subprocess.Popen(["dpns-ls -l "+ dpmDir], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
lines=p.stdout.readlines()
print len(lines), "Files in Directory"
for line in lines:
   line = line[:-1]
   #print line
   filename = line.split(" ")[-1]
   size = int(line.split(" ")[-5]) 
   if "." in filename:
     sf = filename.split("_")
     tf = sf[0]+"_"+sf[1]+"_"
     if  filename.startswith(options.fileName) and any([filename.endswith(sufList[i]) for i in range(len(sufList))]) :
       if not size> 100:
         print "Skipping because file is too small (",filename, "size:", size,")"
         continue
       #print "Copying", dpmDir+"/"+filename, "to", oDir+"/"+filename
       if not options.onlyUpdate or not os.path.isfile(oDir+"/"+filename):
         #os.system("$LCG_LOCATION/bin/rfcp "+dpmDir+"/"+filename+" "+oDir+"/"+filename)
#         os.system("rfcp "+dpmDir+"/"+filename+" "+oDir+"/"+filename)
         os.system("/usr/bin/rfcp "+dpmDir+"/"+filename+" "+oDir+"/"+filename)
       else:
         print "Not overwriting",oDir+"/"+filename
    
retval = p.wait()

