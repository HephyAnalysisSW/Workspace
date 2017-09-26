# fakesEstimation_finalTable.py 
# Mateusz Zarucki 2017

import os
import numpy as np
from fakeInfo import *

script = "fakeRate.py" #os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

lep = args.lep
region = args.region
doPlots = args.doPlots
#makeTables = args.makeTables
varBins = args.varBins
save = args.save
verbose = args.verbose

fakeInfo = fakeInfo(script, vars(args))

measurementType = 'data-EWK'
finalTag = "MR14"

lepton =      fakeInfo['lepton']
samples =     fakeInfo['samples']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

if save:
   baseDir =  fakeInfo['baseDir']
   saveTag =  fakeInfo['saveTag']

   tabledir = baseDir + "/tables/%s"%finalTag
   makeDir(tabledir)

   resultsDir = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final"
   resultsDir += "/%s/%s"%(saveTag, finalTag)

leptons = {'el':'Electron', 'mu':'Muon'}

leps = ['el', 'mu']
#regs = ['sr1ab', 'sr1c', 'sr2', 'sr2a', 'sr2b', 'sr2ab', 'sr2c']
regs = ['sr1a', 'sr1b', 'sr1ab', 'sr1c', 'sr2', 'sr2a', 'sr2b', 'sr2ab', 'sr2c']

# Estimate
LnT = {'el':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}, 'sr2a':{}, 'sr2b':{}, 'sr2ab':{}, 'sr2c':{}}, 
       'mu':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}, 'sr2a':{}, 'sr2b':{}, 'sr2ab':{}, 'sr2c':{}}}

fakesEstimate = {'el':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}, 'sr2a':{}, 'sr2b':{}, 'sr2ab':{}, 'sr2c':{}}, 
                 'mu':{'sr1':{}, 'sr1a':{}, 'sr1b':{}, 'sr1ab':{}, 'sr1c':{}, 'sr2':{}, 'sr2a':{}, 'sr2b':{}, 'sr2ab':{}, 'sr2c':{}}}

fakesEstimateFinal = {'el':{}, 'mu':{}, 'lep':{}}

# Open results pickle
yields = {}
for lep in leps:
   yields[lep] = {}
   for etaBin in ['eta_lt_1p5', 'eta_gt_1p5']:
      yields[lep][etaBin] = {}
   for reg in regs:
      if 'sr1' in reg:   etaBins = ['eta_lt_1p5']
      elif 'sr2' in reg: etaBins = ['eta_lt_1p5', 'eta_gt_1p5']
      for etaBin in etaBins:
         yields[lep][etaBin][reg] = pickle.load(open("%s/applicationRegions/application_%s/estimation/finalEstimate/SR/allBins/fakeTausConsidered/%s/LnotT/TL_%s/varBins/%s/fakesEstimationFinal_yields_%s_application_%s_%s.pkl"%(baseDir, reg, leptons[lep], measurementType, etaBin, lep, reg, measurementType), "r"))

TLratios = pickle.load(open("%s/tightToLooseRatios_%s_%s_stat.pkl"%(resultsDir, finalTag, measurementType), "r"))

for lep in leps:
   for reg in regs:
      if 'sr1' in reg:   etaBins = ['eta_lt_1p5']
      elif 'sr2' in reg: etaBins = ['eta_lt_1p5', 'eta_gt_1p5']

      for etaBin in etaBins:
         LnT[lep][reg][etaBin] = {}
         fakesEstimate[lep][reg][etaBin] = {}
         for ptBin in yields[lep][etaBin][reg]['looseCR']['prompt']:
            if ptBin == 1: continue
            binName = binMaps[lep][str(ptBin)] 

            LnT[lep][reg][etaBin][ptBin] = {'data' : yields[lep][etaBin][reg]['looseCR']['total'][ptBin],
                                          'prompt' : yields[lep][etaBin][reg]['looseCR']['prompt'][ptBin]}

            LnT[lep][reg][etaBin][ptBin]['data-prompt'] = (LnT[lep][reg][etaBin][ptBin]['data'] - LnT[lep][reg][etaBin][ptBin]['prompt'])

            # Estimate 
            TF = TLratios[lep][etaBin][binName]/(1-TLratios[lep][etaBin][binName].val)
            fakesEstimate[lep][reg][etaBin][ptBin] = TF*LnT[lep][reg][etaBin][ptBin]['data-prompt'] 

# SR2
#regs = ['sr2ab', 'sr2c']
regs_sr2 = ['sr2', 'sr2a', 'sr2b', 'sr2ab', 'sr2c']
for reg in regs_sr2:
   for lep in leps:
      fakesEstimate[lep][reg]['etaCombined'] = {} 
      for ptBin in yields[lep][etaBin][reg]['looseCR']['prompt']:
         if ptBin == 1: continue
         fakesEstimate[lep][reg]['etaCombined'][ptBin] = {} 
   
         # Estimate
         fakesEstimate[lep][reg]['etaCombined'][ptBin] = fakesEstimate[lep][reg]['eta_lt_1p5'][ptBin] + fakesEstimate[lep][reg]['eta_gt_1p5'][ptBin] 

for reg in regs:
   for lep in leps:
      for ptBin in yields[lep]['eta_lt_1p5'][reg]['looseCR']['prompt']:
         if ptBin == 1: continue
         binName = binMaps[lep][str(ptBin)] 

         if binName in ['ptVL', 'ptL', 'ptM', 'ptH']:
            regName = reg[:3] + binName.replace('pt', '').lower() + reg[3:]
         else:
            regName = reg.replace('s', 'c')
         
         if 'sr2' in reg:
            if 'cr' in regName: 
               fakesEstimateFinal[lep][regName] = fakesEstimate[lep][reg]['etaCombined'][int(invBinMaps[lep]['30-50'])] +  fakesEstimate[lep][reg]['etaCombined'][int(invBinMaps[lep]['50-80'])] +\
                                                  fakesEstimate[lep][reg]['etaCombined'][int(invBinMaps[lep]['80-200'])] + fakesEstimate[lep][reg]['etaCombined'][int(invBinMaps[lep]['>200'])]
            else: 
               fakesEstimateFinal[lep][regName] = fakesEstimate[lep][reg]['etaCombined'][ptBin] 
         else:
            if 'cr' in regName:   
               fakesEstimateFinal[lep][regName] = fakesEstimate[lep][reg]['eta_lt_1p5'][int(invBinMaps[lep]['30-50'])] +  fakesEstimate[lep][reg]['eta_lt_1p5'][int(invBinMaps[lep]['50-80'])] +\
                                                  fakesEstimate[lep][reg]['eta_lt_1p5'][int(invBinMaps[lep]['80-200'])] + fakesEstimate[lep][reg]['eta_lt_1p5'][int(invBinMaps[lep]['>200'])]
            else:
               fakesEstimateFinal[lep][regName] = fakesEstimate[lep][reg]['eta_lt_1p5'][ptBin] 

SR1s = ['sr1vla', 'sr1la', 'sr1ma', 'sr1ha', 'sr1vlb', 'sr1lb', 'sr1mb', 'sr1hb', 'sr1vlc', 'sr1lc', 'sr1mc', 'sr1hc']
SR2s = ['sr2vla', 'sr2la', 'sr2ma', 'sr2ha', 'sr2vlb', 'sr2lb', 'sr2mb', 'sr2hb', 'sr2vlc', 'sr2lc', 'sr2mc', 'sr2hc']
CRs =  ['cr1a', 'cr1b', 'cr1c', 'cr2a', 'cr2b', 'cr2c']
allRegions = SR1s + SR2s + CRs

allRegions.extend(['sr1vlab', 'sr1lab', 'sr1mab', 'sr1hab', 'sr1vlb', 'sr2vlab', 'sr2lab', 'sr2mab', 'sr2hab', 'sr2vlb', 'cr1ab', 'cr2ab'])

for regName in allRegions:
   if 'vl' in regName:
      fakesEstimateFinal['lep'][regName] = fakesEstimateFinal['mu'][regName]
   else: 
      fakesEstimateFinal['lep'][regName] = fakesEstimateFinal['el'][regName] + fakesEstimateFinal['mu'][regName] 

overwrite = True# False

#Pickle results 
pickleFileName = "%s/fakeEstimates_%s_%s_stat.pkl"%(resultsDir, finalTag, measurementType)
if os.path.isfile(pickleFileName) and not overwrite:
   print "%s file exists. Set overwrite to True to overwrite."%pickleFileName
else:
   pickleFile = open(pickleFileName, "w")
   pickle.dump(fakesEstimateFinal, pickleFile)
   pickleFile.close()

doPlots = 0 
makeTables = 1

if makeTables:
   rows = []
   listTitle = ['Region', 'Muon Fakes (Stat.)', 'Electron Fakes (Stat.)', 'Lepton Fakes (Stat.)']
   rows.append(listTitle)
   for regName in allRegions:
      if 'vl' in regName:
         row = [regName, fakesEstimateFinal['mu'][regName].round(3), "-", fakesEstimateFinal['lep'][regName].round(3)]
      else:
         row = [regName, fakesEstimateFinal['mu'][regName].round(3), fakesEstimateFinal['el'][regName].round(3), fakesEstimateFinal['lep'][regName].round(3)]
      rows.append(row)
            
   makeSimpleLatexTable(rows, "FRestTable_%s"%finalTag, tabledir, align_char = 'p{3cm}|')
