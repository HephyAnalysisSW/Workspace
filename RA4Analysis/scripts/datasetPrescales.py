#! /usr/bin/env python
import sys
import os

#You have to give a JSON File as the first argument when executing from shell!
#you can also give the triggerpath as an optional third parameter, otherwise it will take the HLT path specified with trigger = "HLT_*".

if len(sys.argv) == 1:
  print "ERROR: You must give at least a JSON file as first argument!!"
  sys.exit()
elif len(sys.argv) > 1:
  h = eval(file(sys.argv[1],"r").read())
  hkeys=[]
  for key in h.keys():
    hkeys.append(int(key))
  hkeys.sort()
  if len(sys.argv) > 2:
    trigger = str(sys.argv[2])
  else:
    trigger = "HLT_HT100U"

i=0
ds = ["0"]
print "Searching for trigger: ", trigger
for run in hkeys:
  for dataset in ["MultiJet","Jet","JetMETTauMonitor","Electron","JetMETTau","EG","Mu","EGMonitor","MuMonitor"]:
    for path in os.popen('edmConfigFromDB --runNumber ' + str(run) + ' --format streams.list:A.'+dataset):
      if path.find(trigger) != -1:
        ds.append(dataset)
        if ds[i+1] != ds[i]:
          print "--------------------------------------------------------------------------"
          print "||  Run   || Primary Dataset    | | Prescales"
          print "--------------------------------------------------------------------------"
        i=i+1
        prescale = os.popen("edmConfigFromDB --runNumber "+ str(run) +" --format summary.ascii --paths "+path.rstrip()).readlines()
        print '|| %6d ||  %17s |' % (run, dataset), prescale[-4].rstrip()
