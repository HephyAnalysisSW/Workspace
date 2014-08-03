#!/bin/env python
import subprocess
import os

from optparse import OptionParser

parser = OptionParser()
parser.add_option("--userNameDPM", dest="userNameDPM", default="", type="string", action="store", help="username of DPM User")
parser.add_option("--userNameNFS", dest="userNameNFS", default="schoef", type="string", action="store", help="username on NFS disk /data/")
parser.add_option("--source", dest="source", default="pat_130418/8TeV-T1tttt-test", type="string", action="store", help="source directory in users dpm folder")
parser.add_option("--target", dest="target", default="pat_130501/8TeV-T1tttt", type="string", action="store", help="target directory in users NFS folder")
parser.add_option("--dpmDir", dest="dpmStr", default="/dpm/oeaw.ac.at/home/cms/store/user/", type="string", action="store", help="default dpm string /dpm/oeaw.ac.at/home/cms/store/user/")
(options, args) = parser.parse_args()

dpmDir = options.dpmStr+'/'+options.userNameDPM+'/'+options.source
oDir = '/data/'+options.userNameNFS+'/'+options.target

if not os.path.isdir(oDir):
  print "Creating ",oDir
  os.system("mkdir -p "+oDir)

lsNFS = os.listdir(oDir)

p = subprocess.Popen(["dpns-ls -l "+ dpmDir], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    line = line[:-1]
    print line
    filename = line.split(" ")[-1]
    size = int(line.split(" ")[-5]) 
    if  filename[:6] == "histo_" and filename[-5:]==".root":
      sf = filename.split("_")
      print sf
      tf = sf[0]+"_"+sf[1]+"_"
      found = False
      for f in lsNFS:
        if f.count(tf): 
          print "Found ", f, "when looking for", tf,"(copying", filename,")"
          found = True
          break
      if found: continue
      else: 
        if not size> 1000:
          print "Skipping because file is too small (",filename, "size:", size,")"
          continue
        print "Copying", dpmDir+"/"+filename, "to", oDir+"/"+filename
        os.system("$LCG_LOCATION/bin/rfcp "+dpmDir+"/"+filename+" "+oDir+"/"+filename)
    
retval = p.wait()

