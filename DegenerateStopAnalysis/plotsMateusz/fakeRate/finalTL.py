# finalTL.py
# Mateusz Zarucki 2017

import os, sys
import ROOT
import pickle
from Workspace.HEPHYPythonTools import u_float
from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir #makeSimpleLatexTable, setup_style, 
from fakeInfo import binMaps

saveTag = "8025_mAODv2_v7/80X_postProcessing_v0"
finalTag = "MR14"

baseDir = "/afs/hephy.at/user/m/mzarucki/www/plots" 
resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate"
finalResultsDir = resultsDir + "/final"
baseDir += "/" + saveTag
resultsDir += "/" + saveTag
finalResultsDir += "/%s/%s"%(saveTag, finalTag)
   
MRs = [d for d in os.listdir(resultsDir) if os.path.isdir(os.path.join(resultsDir, d)) if 'measurement' in d]

etaBins = ['etaIncl', 'eta_lt_1p5', 'eta_gt_1p5']

for w in ['', '/noWttWeights']:
   savedir = finalResultsDir
   savedir += w
   makeDir(savedir) 
   
   yields = {}
   TLratios = {}
   
   for FR in ['data-EWK', 'MC', 'MC-EWK']:
      yields[FR] = {}
      TLratios[FR] = {}
      for MR in MRs:
         yields[FR][MR] = {}
         TLratios[FR][MR] = {}
         for etaBin in etaBins:
            yields[FR][MR][etaBin] = {}
            TLratios[FR][MR][etaBin] = {}
    
            for lep in ['el', 'mu']:
               if   lep == "el":  lepton = "Electron"
               elif lep == "mu":  lepton = "Muon"
               elif lep == "lep": lepton = "Lepton"
   
               pickleFile1 = "{}/{MR}/TL_{FR}/varBins/{etaBin}{}/tightToLooseRatios_{lep}_{MR}_{FR}.pkl".format(resultsDir, w, MR = MR, etaBin = etaBin, lep = lep, FR = FR)
   
               try:
                  TLratios[FR][MR][etaBin][lep] = pickle.load(open(pickleFile1, "r"))
               except:
                  IOError
                  print "File", pickleFile1, "not found. Continuing."
                  continue
               
               mcYldsDir = "{}/fakesEstimation/measurementRegions/{MR}/tightToLooseRatio/allBins/fakeTausConsidered/{lepton}/varBins/{FR}/{etaBin}{}/yields".format(baseDir, w, MR = MR, etaBin = etaBin, lepton = lepton, FR = FR)
               mcYlds = [d.split('_')[1] for d in os.listdir(mcYldsDir) if os.path.isfile(os.path.join(mcYldsDir, d)) and 'mcYields' in d and '.pkl' in d]
               
               yields[FR][MR][etaBin][lep] = {}
               for yldType in mcYlds:
                  pickleFile2 = "{}/mcYields_{}_{lep}_{MR}_{FR}.pkl".format(mcYldsDir, yldType, MR = MR, etaBin = etaBin, lep = lep, FR = FR)
                  
                  try:
                     yields[FR][MR][etaBin][lep].update(pickle.load(open(pickleFile2, "r")))
                  except:
                     IOError
                     print "File", pickleFile2, "not found. Continuing."
                     continue
               
               if 'data' in FR:    
                  yields[FR][MR][etaBin][lep]['data'] = {}
                  pickleFile3 = "{}/dataYields_total_{lep}_{MR}_{FR}.pkl".format(mcYldsDir, MR = MR, etaBin = etaBin, lep = lep, FR = FR)
      
                  try:
                     yields[FR][MR][etaBin][lep]['data'] = pickle.load(open(pickleFile3, "r"))['total']
                  except:
                     IOError
                     print "File", pickleFile3, "not found. Continuing."
                     continue
   
   
   yields_final = {}
   TLratios_final = {}
   
   baseMR = "measurement1" # baseline MR
   overwrite = False
   
   # replacing last three bins in muon channel by result from MR4
   combineMRs = True
   replaceMR = 'measurement4'
   replaceBins = [7, 8, 9]
  
 
   for measurementType in ['data-EWK', 'MC']:
      dictExists = True
      for lep in ['el', 'mu']: 
         try:
            ptBins = TLratios[measurementType][baseMR]['eta_lt_1p5'][lep]['ratio']
         except:
            KeyError
            print "No TL ratios for", measurementType, lep, etaBin, ". Continuing."
            dictExists = False 
            continue

         yields_final[lep] = {}
         TLratios_final[lep] = {}
         for etaBin in ['eta_lt_1p5', 'eta_gt_1p5']:
            yields_final[lep][etaBin] = {}
            TLratios_final[lep][etaBin] = {}

            for ptBin in ptBins: 
               TLratios_final[lep][etaBin][binMaps[lep][str(ptBin)]] = TLratios[measurementType][baseMR][etaBin][lep]['ratio'][ptBin] 
                     
               yields_final[lep][etaBin][binMaps[lep][str(ptBin)]] = {}
               for yldType in yields[measurementType][baseMR][etaBin][lep]:
                  yields_final[lep][etaBin][binMaps[lep][str(ptBin)]][yldType] = {}
                  if yields[measurementType][baseMR][etaBin][lep][yldType]['loose']:
                     yields_final[lep][etaBin][binMaps[lep][str(ptBin)]][yldType]['loose'] = yields[measurementType][baseMR][etaBin][lep][yldType]['loose']['pt'][ptBin]
                     yields_final[lep][etaBin][binMaps[lep][str(ptBin)]][yldType]['tight'] = yields[measurementType][baseMR][etaBin][lep][yldType]['tight']['pt'][ptBin]
   
      if combineMRs and dictExists:
         lep = 'mu' # NOTE: Muons only
         for etaBin in ['eta_lt_1p5', 'eta_gt_1p5']:
            for ptBin in replaceBins:
               TLratios_final[lep][etaBin][binMaps[lep][str(ptBin)]] = TLratios[measurementType][replaceMR][etaBin][lep]['ratio'][ptBin] 
                  
               for yldType in yields_final[lep][etaBin][binMaps[lep][str(ptBin)]]: 
                  if yields[measurementType][replaceMR][etaBin][lep][yldType]['loose']:
                     yields_final[lep][etaBin][binMaps[lep][str(ptBin)]][yldType]['loose'] = yields[measurementType][replaceMR][etaBin][lep][yldType]['loose']['pt'][ptBin]
                     yields_final[lep][etaBin][binMaps[lep][str(ptBin)]][yldType]['tight'] = yields[measurementType][replaceMR][etaBin][lep][yldType]['tight']['pt'][ptBin]
     
      #Pickle results 
      pickleFile4name = "%s/tightToLooseRatios_%s_%s_stat.pkl"%(savedir, finalTag, measurementType) 
      if os.path.isfile(pickleFile4name) and not overwrite:
         print "%s file exists. Set overwrite to True to overwrite."%pickleFile4name
      else:
         pickleFile4 = open(pickleFile4name, "w")
         pickle.dump(TLratios_final, pickleFile4)
         pickleFile4.close()
      
      pickleFile5name = "%s/yields_%s_%s.pkl"%(savedir, finalTag, measurementType) 
      if os.path.isfile(pickleFile5name) and not overwrite:
         print "%s file exists. Set overwrite to True to overwrite."%pickleFile5name
      else:
         pickleFile5 = open(pickleFile5name, "w")
         pickle.dump(yields_final, pickleFile5)
         pickleFile5.close()
