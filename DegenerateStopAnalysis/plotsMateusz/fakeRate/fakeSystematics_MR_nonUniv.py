# finalTL.py
# Mateusz Zarucki 2017

import os, sys
import ROOT
import pickle
from Workspace.HEPHYPythonTools import u_float
from Workspace.DegenerateStopAnalysis.tools.degTools import makeDir, makeSimpleLatexTable#, setup_style, 
from fakeInfo import binMaps, invBinMaps

save = True
doTable = True

if save:
   saveTag = "8025_mAODv2_v7/80X_postProcessing_v0"
   finalTag = "MR14"
   
   #baseDir =  fakeInfo['baseDir']
   #saveTag =  fakeInfo['saveTag']
   
   baseDir = "/afs/hephy.at/user/m/mzarucki/www/plots" 
   resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate"
   finalResultsDir = resultsDir + "/final"
   baseDir += "/%s/fakesEstimation"%saveTag
   
   resultsDir += "/" + saveTag
   finalResultsDir += "/%s/%s"%(saveTag, finalTag)

   tabledir = baseDir + "/measurementRegions/systematics/%s"%finalTag
   makeDir(tabledir)
 
MRs = [d for d in os.listdir(resultsDir) if os.path.isdir(os.path.join(resultsDir, d)) if 'measurement' in d]

etaBins = ['eta_lt_1p5', 'eta_gt_1p5'] # 'etaIncl'

savedir = finalResultsDir
makeDir(savedir) 

finalTLratios = pickle.load(open("%s/tightToLooseRatios_%s_data-EWK_stat.pkl"%(finalResultsDir, finalTag), "r"))

yields = {}
TLratios = {}
listTL = {}
TLdiff = {}
sys = {}

leps = ['el', 'mu']
bTagVars = ['central', 'bTag', 'bVeto', 'max', 'proposed']

for FR in ['MC', 'data-EWK']:#, 'MC-EWK']:
   listTL[FR] = {}
   TLdiff[FR] = {}
   sys[FR] = {}
   for etaBin in etaBins:
      listTL[FR][etaBin] = {}
      TLdiff[FR][etaBin] = {}
      sys[FR][etaBin] = {}
      for lep in leps:
         listTL[FR][etaBin][lep] = {}
         TLdiff[FR][etaBin][lep] = {}
         sys[FR][etaBin][lep] = {}
         for ptBin in binMaps[lep].keys(): 
            listTL[FR][etaBin][lep][ptBin] = []
         for bTagVar in bTagVars: 
            TLdiff[FR][etaBin][lep][bTagVar] = {}
            sys[FR][etaBin][lep][bTagVar] = {}

bTagVars.remove('max')
bTagVars.remove('proposed')

for FR in ['MC', 'data-EWK']:#, 'MC']:#, 'MC']:#, 'MC-EWK']:
   yields[FR] = {}
   TLratios[FR] = {}
   for MR in MRs:
      yields[FR][MR] = {}
      TLratios[FR][MR] = {}
      for etaBin in etaBins:
         yields[FR][MR][etaBin] = {}
         TLratios[FR][MR][etaBin] = {}
 
         for lep in leps:
            if   lep == "el":  lepton = "Electron"
            elif lep == "mu":  lepton = "Muon"
            elif lep == "lep": lepton = "Lepton"

            pickleFile = "{}/{MR}/TL_{FR}/varBins/{etaBin}/tightToLooseRatios_{lep}_{MR}_{FR}.pkl".format(resultsDir, MR = MR, etaBin = etaBin, lep = lep, FR = FR)

            try:
               TLratios[FR][MR][etaBin][lep] = pickle.load(open(pickleFile, "r"))
            except:
               IOError
               print "File", pickleFile, "not found. Continuing."
               continue
         
   comparisonMRs = ['measurement1']
   #for lep in ['el', 'mu']:
   #   if lep == 'mu': comparisonMRs.append('measurement4')
   #   for etaBin in etaBins:
   #      for compMR in comparisonMRs:
   #         for ptBin in TLratios[FR][compMR][etaBin][lep]['ratio']:
   #           if lep == 'mu' and ptBin >= 7 and "measurement1" in compMR: continue # ignore results from MR1 pT > 50 in muons
   #           if TLratios[FR][compMR][etaBin][lep]['ratio'][ptBin].val:
   #              listTL[FR][etaBin][lep][str(ptBin)].append(TLratios[FR][compMR][etaBin][lep]['ratio'][ptBin].val)

   for lep in leps:
      if lep == 'mu': comparisonMRs.append('measurement4')
      for etaBin in etaBins:
         for bTagVar in bTagVars:
            for ptBin in TLratios[FR]['measurement1'][etaBin][lep]['ratio']:
               if ptBin == 1: continue
               if lep == 'el' and ptBin == 2: continue
               if lep == 'mu' and ptBin >= 7:
                  baseMR = 'measurement4'
               else: 
                  baseMR = 'measurement1'
            
               MRvar = '{}_{}'.format(baseMR,bTagVar).replace('_central','')
              
               TLdiff[FR][etaBin][lep][bTagVar][str(ptBin)] = abs(finalTLratios[lep][etaBin][binMaps[lep][str(ptBin)]].val - TLratios[FR][MRvar][etaBin][lep]['ratio'][ptBin].val)
               #TLdiff_up =   abs(finalTLratios[lep][etaBin][binMaps[lep][str(ptBin)]].val - max(listTL[FR][etaBin][lep][str(ptBin)]))
               #TLdiff_down = abs(finalTLratios[lep][etaBin][binMaps[lep][str(ptBin)]].val - min(listTL[FR][etaBin][lep][str(ptBin)]))

               ## symmetrise by taking largest difference
               #if TLdiff_up > TLdiff_down:
               #   TLdiff[FR][etaBin][lep][str(ptBin)] = TLdiff_up
               #else:   
               #   TLdiff[FR][etaBin][lep][str(ptBin)] = TLdiff_down
   
               sys[FR][etaBin][lep][bTagVar][binMaps[lep][str(ptBin)]] = TLdiff[FR][etaBin][lep][bTagVar][str(ptBin)]/finalTLratios[lep][etaBin][binMaps[lep][str(ptBin)]].val 

   proposedSys = {}    
   proposedSys['el'] = {'0_3p5':0., 'ptVL':.2, 'ptL':.2, 'ptM':.2, 'ptH':.3, '30-50':.3, '50-80':.5, '80-200':.5, '>200':.5}
   proposedSys['mu'] = {'0_3p5':0., 'ptVL':.2, 'ptL':.2, 'ptM':.3, 'ptH':.3, '30-50':.3, '50-80':.5, '80-200':.7, '>200':1}
 
   if doTable:
      binNames = {}
      for lep in leps:
         binNames[lep] = [binMaps[lep][i] for i in binMaps[lep]]
         for etaBin in ['eta_lt_1p5', 'eta_gt_1p5']: #"etaIncl"
            rows = []
            listTitle = ['Bin', 'T-L Ratio: Final (Stat.)', 'TL Ratio: B-Veto',  'TL Ratio: B-Veto', '\% Diff. B-Veto', '\% Diff. B-Tag ', 'Max Sys. Unc. (\%)', 'Proposed Sys. Unc. (\%)']
            rows.append(listTitle)
            
            for ptBin in binNames[lep]:
               if ptBin == "0_5" or ptBin == "0_3p5": continue
               if lep == 'el' and ptBin == "ptVL": continue
               if lep == 'mu' and ptBin in ['>200', '80-200', '50-80']:
                  baseMR = 'measurement4'
               else: 
                  baseMR = 'measurement1'
               
               sys[FR][etaBin][lep]['max'][ptBin] = max(sys[FR][etaBin][lep]['bVeto'][ptBin], sys[FR][etaBin][lep]['bTag'][ptBin])
               sys[FR][etaBin][lep]['proposed'][ptBin] = proposedSys[lep][ptBin] 

               row = [ptBin,
               finalTLratios[lep][etaBin][ptBin].round(3),
               TLratios[FR][baseMR + '_bVeto'][etaBin][lep]['ratio'][int(invBinMaps[lep][ptBin])].round(3),
               TLratios[FR][baseMR + '_bTag'][etaBin][lep]['ratio'][int(invBinMaps[lep][ptBin])].round(3),
               "%.1f"%(sys[FR][etaBin][lep]['bVeto'][ptBin]*100),
               "%.1f"%(sys[FR][etaBin][lep]['bTag'][ptBin]*100),
               "%.1f"%(sys[FR][etaBin][lep]['max'][ptBin]*100),
               "%.1f"%(proposedSys[lep][ptBin]*100)]
               rows.append(row)
   
            makeSimpleLatexTable(rows, "TLnonUnivSysTable_%s_%s_%s"%(finalTag, lep, etaBin), tabledir)

   overwrite = False
   #Pickle results 
   pickleFileName = "%s/tightToLooseRatios_%s_%s_sys2.pkl"%(savedir, finalTag, FR) 
   if os.path.isfile(pickleFileName) and not overwrite:
      print "%s file exists. Set overwrite to True to overwrite."%pickleFileName
   else:
      pickleFile2 = open(pickleFileName, "w")
      pickle.dump(sys[FR], pickleFile2)
      pickleFile2.close()
