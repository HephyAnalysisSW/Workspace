import os
def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

for d in get_immediate_subdirectories('.'):
  #if d.count('Reco') or d.count('8TeV-') or d.count('Run2012'):
  if d.count('8TeV-WJetsToLNu'):
    for i in range(0, 2501, 500):
      if i==0:
        sstring= "crab -submit "+str(i+500)+" -c "+d
      else:
        sstring= "crab -submit "+str(i+1)+"-"+str(i+500)+" -c "+d
      print sstring
      os.system(sstring)
