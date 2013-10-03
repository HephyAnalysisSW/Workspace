#!/env/python
import os, sys

for i in range(int(sys.argv[1]),int(sys.argv[2]), 25):
  os.system("python cloneSMSTree.py "+str(i)+" "+str(i+25))


