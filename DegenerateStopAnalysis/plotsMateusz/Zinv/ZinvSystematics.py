import os
import pickle
import math
from Workspace.HEPHYPythonTools import u_float

path = {}
EWKsys = {}
QCDest = {}

path = "/afs/hephy.at/user/m/mzarucki/public/Yields_12864pbm1_PreApp_Mt95_Inccharge_LepAll_lep_pu_SF_presel_BinsSummary.pkl"

savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/Zinv/systematics"

if not os.path.exists(savedir): os.makedirs(savedir)

allYields = pickle.load(open(path, "r"))

regions = ['SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

R_el = u_float.u_float(0.95, math.sqrt(0.14**2 + 0.48**2))
R_mu = u_float.u_float(1.30, math.sqrt(0.11**2 + 0.65**2))

#allYields.yieldDictFull

#for reg in regions:
#   QCDsys[x][reg] = {}
#   QCDsys[x][reg]['val'] = QCDest[x][reg].val
#   QCDsys[x][reg]['stat'] = QCDest[x][reg].sigma
#   QCDsys[x][reg]['sys'] = EWKsys[x][reg].val
#   QCDsys[x][reg]['err'] = math.sqrt(QCDsys[x][reg]['stat']**2 + QCDsys[x][reg]['sys']**2) 

#pickleFile1 = open("%s/QCDsystematics_muon.pkl"%(path['combined']), "w")
#pickle.dump(QCDsys['mu'], pickleFile1)
#pickleFile1.close()
# 
#pickleFile2 = open("%s/QCDsystematics_ele.pkl"%(path['combined']), "w")
#pickle.dump(QCDsys['el'], pickleFile2)
#pickleFile2.close()
#
#pickleFile3 = open("%s/QCDsystematics_combined.pkl"%(path['combined']), "w")
#pickle.dump(QCDsys['combined'], pickleFile3)
#pickleFile3.close()
