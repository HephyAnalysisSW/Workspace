#! /usr/bin/env python
import sys, os

dirname = "/scratch/schoef/"
#if len(sys.argv)>0:
#  dirname += sys.argv[1]
#else:
dirname += "pat_101005/Mu/"
subdirnames = os.listdir(dirname)
toBeRemovedGlobal=[]
print subdirnames
for subdir in subdirnames:
  subdirname = dirname+"/"+subdir+"/"
  print  "At subdir ", subdirname
  filenames = os.listdir(subdirname)
  numbers=[]
  for file in filenames:
    sstring = file.split("_")
    if len(sstring)>1:
      numbers.append(int(sstring[1]))
  if len(numbers)>0:
    maxFileNumber = max(numbers)
  else:
    continue
  filesPerNumber={}
  for i in range(1,maxFileNumber+1):
    filesPerNumber[str(i)]=[]
    for file in filenames:
      if file.count("histo_"+str(i)+"_")>0:
        filesPerNumber[str(i)].append(file)
  for i in range(1,maxFileNumber+1):
    if len(filesPerNumber[str(i)])>1:
      toBeRemoved=[]
      for file in filesPerNumber[str(i)]:
        toBeRemoved.append(subdirname+"/"+file)
      print "Found duplicate Files!"
      toBeKept = ""
      maxSize = 0
      for file in filesPerNumber[str(i)]:
        filename = subdirname+"/"+file
        size = os.path.getsize(filename) 
        print filename, "size", size
        if size>maxSize:
          toBeKept = filename
          maxSize = size
      toBeRemoved.remove(toBeKept)
      print "Keep:", toBeKept, "Remove:", toBeRemoved
      toBeRemovedGlobal.extend(toBeRemoved)

#sample["filenames"][bin]=[]
#if small:
#  filelist=os.listdir(subdirname)
#  counter = 1   #Joining n files
#  for thisfile in filelist:
#    if os.path.isfile(subdirname+thisfile) and thisfile[-5:]==".root" and thisfile.count("histo")==1:
#      sample["filenames"][bin].append(subdirname+thisfile)
##          c.Add(sample["dirname"]+file)
#      if counter==0:
#        break
#      counter=counter-1

