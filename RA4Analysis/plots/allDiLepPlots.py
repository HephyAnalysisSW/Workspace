#! /usr/bin/env python
import os

#for msq in [200, 250, 300, 350, 400, 450, 500, 550, 600]:
#  for mN in [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]:
for msq in [175]:
  for mN in [0]:
    if msq - mN >= 100:
      os.system("python diLepPlots.py "+str(msq)+" "+str(mN)+"  pf-3j40-met100-mLL20-70-Run2012ABC")
      os.system("python diLepPlots.py "+str(msq)+" "+str(mN)+"  pf-3j40-met100-mLL20-Run2012ABC")
      os.system("python diLepPlots.py "+str(msq)+" "+str(mN)+"  pf-2j40-met150-mLL20-70-Run2012ABC")
      os.system("python diLepPlots.py "+str(msq)+" "+str(mN)+"  pf-2j40-met150-mLL20-Run2012ABC")
#msq=0;mN=0;
#os.system("python diLepPlots.py "+str(msq)+" "+str(mN)+"  pf-3j40-met100-mLL20-Run2012ABC")
#os.system("python diLepPlots.py "+str(msq)+" "+str(mN)+"  pf-3j40-met100-mLL20-70-Run2012ABC")
