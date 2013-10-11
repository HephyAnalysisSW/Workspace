#! /usr/bin/env python
import sys

h = eval(file(sys.argv[1],"r").read())
l = {}
hkeys=[]
for key in h.keys():
  hkeys.append(int(key))
print "Runrange before cut:",min(hkeys),max(hkeys)

lkeys=[]
if len(sys.argv)>3:
  lower = eval(sys.argv[2])
  upper = eval(sys.argv[3])
  for key in h.keys():
    if int(key)>=lower and int(key)<=upper:
      l[key]=h[key]
      lkeys.append(int(key))
  print "Runrange after cut: ",min(lkeys),max(lkeys)
if len(sys.argv)>4:
  outfile = file(sys.argv[4],"w")
  outfile.write(repr(l).replace("'",'"'))
  outfile.close()
