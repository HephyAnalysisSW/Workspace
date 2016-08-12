import os
import pickle
import math
from Workspace.HEPHYPythonTools import u_float

path = {}
EWKsys = {}
QCDest = {}
QCDyields = {} 

path1 = "/afs/hephy.at/user/m/mzarucki/public/Yields_12864pbm1_PreApp_Mt95_Inccharge_LepAll_lep_pu_SF_presel_BinsSummary.pkl"
path2 = "/afs/hephy.at/user/m/mzarucki/www/plots/QCD/combined/QCDsystematics_combined.pkl"

savedir = "/afs/hephy.at/user/m/mzarucki/public"
if not os.path.exists(savedir): os.makedirs(savedir)

allYields = pickle.load(open(path1, "r"))
QCDyields = pickle.load(open(path2, "r"))
regions = ['SR1a', 'SR1b', 'SR1c', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c']

for reg in regions:
   QCDyields[reg] = u_float.u_float(QCDyields[reg]['val'],QCDyields[reg]['err']).round(3)  
   allYields.yieldDictFull['qcd'][reg] = u_float.u_float(QCDyields[reg]['val'],QCDyields[reg]['err'])  

del QCDyields['SR1']

pickleFile1 = open("%s/Yields_12864pbm1_PreApp_Mt95_Inccharge_LepAll_lep_pu_SF_presel_BinsSummary_QCDest.pkl"%(savedir), "w")
pickle.dump(allYields, pickleFile1)
pickleFile1.close()
 
pickleFile2 = open("%s/QCDyields.pkl"%(savedir), "w")
pickle.dump(QCDyields, pickleFile2)
pickleFile2.close()

#pickleFile3 = open("%s/QCDsystematics_combined.pkl"%(path['combined']), "w")
#pickle.dump(QCDsys['combined'], pickleFile3)
#pickleFile3.close()
