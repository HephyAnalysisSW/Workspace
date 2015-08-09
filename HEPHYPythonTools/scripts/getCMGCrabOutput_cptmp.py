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
print dpmDir
#oDir = '/data/'+options.userNameNFS+'/'+options.target
#oDir = '/afs/hephy.at/work/e/'+options.userNameNFS+'/'+options.target
oDir = '/tmp/'+options.userNameNFS+'/'+options.target

suf = options.suffix
sufList = suf.split()

if not os.path.isdir(oDir):
  print "Creating ",oDir
  os.system("mkdir -p "+oDir)

lsNFS = os.listdir(oDir)
print lsNFS
#p = subprocess.Popen(["dpns-ls -l "+ dpmDir], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
p = subprocess.Popen(["lcg-ls -v srm://hephyse.oeaw.ac.at/"+ dpmDir], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print p
for line in p.stdout.readlines():
   line = line[:-1]
   print "line", line
   filename = line.split(" ")[-1]
   print "filename" , filename
   #size = int(line.split(" ")[-5]) 
   if "." in filename:
     sf = filename.split("_")
     tf = sf[0]+"_"+sf[1]+"_"
     if  filename.startswith(options.fileName) and any([filename.endswith(sufList[i]) for i in range(len(sufList))]) :
       #if not size> 100:
       #  print "Skipping because file is too small (",filename, "size:", size,")"
       #  continue
       #print "Copying", dpmDir+"/"+filename, "to", oDir+"/"+filename
       final_file = filename.split("/")[-1]
       print "Copying", filename, "to", oDir+"/"+(filename.split(options.userNameDPM)[1]).split("/")[0]
       if not options.onlyUpdate or not os.path.isfile(oDir+"/"+filename):
         #os.system("$LCG_LOCATION/bin/rfcp "+dpmDir+"/"+filename+" "+oDir+"/"+filename)
         #os.system("/usr/bin/rfcp "+dpmDir+"/"+filename+" "+oDir+"/"+filename)
         #os.system("/usr/bin/rfcp "+filename+" "+oDir+"/"+(filename.split("easilar")[1]).split("/")[0])
         os.system("lcg-cp -v srm://hephyse.oeaw.ac.at///"+filename+" file:/"+oDir+"/"+(filename.split(options.userNameDPM)[1]).split("/")[0]+final_file)
       else:
         print "Not overwriting",oDir+"/"+filename
    
retval = p.wait()

