import os
import pickle
import math
from Workspace.HEPHYPythonTools import u_float

path = {}
EWKsys = {}
QCDest = {}

path['mu'] = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/muon/estimation/METloose/HT400MET300METloose200"
path['el'] = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/electron/ABCD6/estimation/METloose/HT400MET300METloose200"
path['combined'] = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/combined"

if not os.path.exists(path['combined']): os.makedirs(path['combined'])

QCDest['mu'] = pickle.load(open(path['mu'] +  "/QCDest_muon_HT400_MET300_METloose200.pkl", "r"))
EWKsys['mu'] = pickle.load(open(path['mu'] + "/EWKsys_muon_HT400_MET300_METloose200.pkl", "r"))

QCDest['el'] = pickle.load(open(path['el'] +  "/QCDest_ele_HT400_MET300_METloose200.pkl", "r"))
EWKsys['el'] = pickle.load(open(path['el'] + "/EWKsys_ele_HT400_MET300_METloose200.pkl", "r"))

regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

QCDsys = {}
for x in ['mu', 'el']:
   QCDsys[x] = {}
   for reg in regions:
      QCDsys[x][reg] = {}
      QCDsys[x][reg]['val'] = QCDest[x][reg].val
      QCDsys[x][reg]['stat'] = QCDest[x][reg].sigma
      QCDsys[x][reg]['sys'] = EWKsys[x][reg].val
      QCDsys[x][reg]['err'] = math.sqrt(QCDsys[x][reg]['stat']**2 + QCDsys[x][reg]['sys']**2) 

print QCDsys['mu']
print QCDsys['el']

QCDsys['combined'] = {}
      
for reg in regions:
   QCDsys['combined'][reg] = {}
   QCDsys['combined'][reg]['val'] = QCDsys['mu'][reg]['val'] + QCDsys['el'][reg]['val']
   QCDsys['combined'][reg]['stat'] = math.sqrt(QCDsys['mu'][reg]['stat']**2 + QCDsys['el'][reg]['stat']**2)
   QCDsys['combined'][reg]['sys'] = math.sqrt(QCDsys['mu'][reg]['sys']**2 + QCDsys['el'][reg]['sys']**2)
   QCDsys['combined'][reg]['err'] = math.sqrt(QCDsys['mu'][reg]['err']**2 + QCDsys['el'][reg]['err']**2)

print QCDsys['combined']

pickleFile1 = open("%s/QCDsystematics_muon.pkl"%(path['combined']), "w")
pickle.dump(QCDsys['mu'], pickleFile1)
pickleFile1.close()
 
pickleFile2 = open("%s/QCDsystematics_ele.pkl"%(path['combined']), "w")
pickle.dump(QCDsys['el'], pickleFile2)
pickleFile2.close()

pickleFile3 = open("%s/QCDsystematics_combined.pkl"%(path['combined']), "w")
pickle.dump(QCDsys['combined'], pickleFile3)
pickleFile3.close()
