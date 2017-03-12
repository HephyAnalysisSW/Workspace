# scanFakeRegions.py
# Mateusz Zarucki 2017

import os
from fakeInfo import *

script = os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

#Arguments
sample = args.sample
lep = args.lep
region = args.region
WP = args.WP
category = args.category
ptBin = args.ptBin
mva = args.mva
looseNotTight = args.looseNotTight
doYields = args.doYields
getData = args.getData
varBins = args.varBins
save = args.save
verbose = args.verbose

fakeInfo = fakeInfo(script, vars(args))

lepton =      fakeInfo['lepton']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
dataSample =  fakeInfo['dataSample']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

#Save
if save:
   savedir = fakeInfo['savedir']
   suffix =  fakeInfo['suffix']
   suffix2 = "%s_%s"%(suffix, sample)

if samples[sample].isData:
   sampType = 'data'
else:
   sampType = 'MC'

## Signal region
#region = {'SR':{}, 'looseCR':{}}
#
#region['SR']['total'] =  [selection[sampType]['tight']['cuts'], selection[sampType]['regDef']] 
#region['SR']['prompt'] = [selection[sampType]['tight']['cuts'], selection[sampType]['regDef'] + '_prompt'] 
#region['SR']['fake'] =   [selection[sampType]['tight']['cuts'], selection[sampType]['regDef'] + '_fake'] 
#
## Loose (not-Tight) CR
#if looseNotTight:
#   notTight = "_notTight"
#else:
#   notTight = ""
#
#region['looseCR']['total'] =  [selection[sampType]['loose']['cuts'], selection[sampType]['regDef'] + notTight] 
#region['looseCR']['prompt'] = [selection[sampType]['loose']['cuts'], selection[sampType]['regDef'] + notTight + '_prompt'] 
#region['looseCR']['fake'] =   [selection[sampType]['loose']['cuts'], selection[sampType]['regDef'] + notTight + '_fake' ] 

baseCutString = selection[sampType][WP][region][sample][0] 

weight = selection[sampType][WP][region][sample][1] 

if category == "total":
   cutString = baseCutString
elif category in ["prompt", "fake"]:
   cutString = combineCuts(baseCutString, selection[sampType][WP]['cuts'].cuts_dict[category]['cut'])

# Loose (not-Tight) CR
if WP == "loose" and looseNotTight:
   cutString = combineCuts(cutString, selection[sampType][WP]['cuts'].cuts_dict['notTight']['cut'])

if ptBin:
   lepPt = selection[sampType][WP]['cuts'].vars_dict_format['lepPt']
   cutString = combineCuts(cutString, "({lepPt} > {low}) && ({lepPt} < {high})".format(lepPt = lepPt, low = ptBin[0], high = ptBin[1]))

lepInd = selection[sampType][WP]['lepIndex']

# Scan
varGeneral = ["evt", weight, "nGenPart"]
varGenPart = ["pdgId", "pt", "eta", "phi", "motherId"]#, "motherIndex", "sourceId", "grandmotherId", "status", "isPromptHard"]
#varGenJet = ["pt","eta","phi"]
varLepGood = ["pdgId", "pt", "eta", "phi", "mt", "mcMatchId", "mcMatchAny", "mcMatchTau"] #"dxy", "dz", 
#varTauGood = ["pt", "eta"]

varGenPart = ["GenPart_"+x for x in varGenPart]
#varGenJet =  ["GenJet_"+x for x in varGenJet]
varLepGood = ["LepGood_%s[%s]"%(x,lepInd) for x in varLepGood]
#varTauGood = ["TauGood_"+x for x in varTauGood] #NOTE: adding these variables limits output of the TTree:Scan()

varExtra = ["met_pt", "met_phi", "met_genPt", "met_genPhi"]# "nJet_basJet_def"]
#varGenPart.insert(0, 'nGenPart')
#varLepGood.insert(0, 'nLepGood_{}_{}'.format(lep, WP).replace('tight', 'def'))

variables = ":".join(varGeneral+varGenPart+varLepGood+varExtra) #varGenJet+varTauGood

if verbose:
   print makeLine()
   print "Cut: ", cutString
   print makeLine()
   print "Variables: ", variables
   print makeLine()

t = samples[sample].tree

if save:
   t.SetScanField(0)
   t.GetPlayer().SetScanRedirect(True)
   t.GetPlayer().SetScanFileName(savedir + "/scan%s.txt"%suffix2)

t.Scan(variables, cutString)

if doYields:

   yld, err = getYieldFromChain(samples[sample].tree, cutString, weight = weight, returnError = True)
   
   if verbose:
      print makeLine() 
      print "Sample: ", sample
      print "Yield: ", yld, "+-", err
      print makeLine() 
  
   if save:
      yieldFile = "%s/fakeYields%s.txt"%(savedir, suffix) 
      if not os.path.isfile(yieldFile):
         outfile = open(yieldFile, "w")
         outfile.write("Fake Estimation Yields in %s\n"%region.title())
         outfile.write("Sample             Yield\n")

      with open(yieldFile, "a") as outfile:
         outfile.write(sample.ljust(10) + "%.2f+-%.2f\n"%(yld,err))
 
## Yields 
#if doYields:
#   yields = {'SR':{}, 'looseCR':{}}
#
#   for x in yields: 
#      yields[x]['total'] =  Yields(samples, samplesList, cutInst = None, cuts = region[x]['total'],  cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
#      yields[x]['prompt'] = Yields(samples, samplesList, cutInst = None, cuts = region[x]['prompt'], cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
#      yields[x]['fake'] =   Yields(samples, samplesList, cutInst = None, cuts = region[x]['fake'],   cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
#
#   if save:
#      if not os.path.isfile("%s/fakeYields_%s.txt"%(savedir, suffix)):
#         outfile = open("%s/fakeYields_%s.txt"%(savedir, suffix), "w")
#         outfile.write("Fake Estimation Yields in %s\n"%region.title())
#         outfile.write("Sample      Loose CR: Total         Loose CR: Prompt          Loose CR: Fakes          SR: Total              SR: Prompt               SR: Fakes\n") 
#
#      yieldsList = samplesList[:]
#      yieldsList.append('Total')
#
#      with open("%s/fakeYields_%s.txt"%(savedir, suffix), "a") as outfile:
#        for samp in yieldsList:
#            outfile.write(samp.ljust(10) +\
#            str(yields['looseCR']['total'].yieldDictFull[samp][selection[sampType]['regDef'] + notTight].round(2)).ljust(25) +\
#            str(yields['looseCR']['prompt'].yieldDictFull[samp][selection[sampType]['regDef'] + notTight + '_prompt'].round(2)).ljust(25) +\
#            str(yields['looseCR']['fake'].yieldDictFull[samp][selection[sampType]['regDef'] + notTight + '_fake'].round(2)).ljust(25) +\
#            str(yields['SR']['total'].yieldDictFull[samp][selection[sampType]['regDef']].round(2)).ljust(25) +\
#            str(yields['SR']['prompt'].yieldDictFull[samp][selection[sampType]['regDef'] + '_prompt'].round(2)).ljust(25) +\
#            str(yields['SR']['fake'].yieldDictFull[samp][selection[sampType]['regDef'] + '_fake'].round(2)) + "\n")# .ljust(18) +\

# GenPart variables
# nGenPart nGenPart/I : 0 at: 0x4fbf7b0
# GenPart_motherId  pdgId of the mother of the particle for Hard scattering particles, with ancestry and links : 0 at: 0x4fc3dd0
# GenPart_grandmotherId   pdgId of the grandmother of the particle for Hard scattering particles, with ancestry and links : 0 at: 0x4fc4450
# GenPart_sourceId  origin of the particle (heaviest ancestor): 6=t, 25=h, 23/24=W/Z for Hard scattering particles, with ancestry and links : 0 at: 0x4facaa0
# GenPart_charge charge for Hard scattering particles, with ancestry and links : 0 at: 0x4fad1a0
# GenPart_status status for Hard scattering particles, with ancestry and links : 0 at: 0x4fc1d00
# GenPart_isPromptHard isPromptHard for Hard scattering particles, with ancestry and links : 0 at: 0x4fc2330
# GenPart_pdgId  pdgId for Hard scattering particles, with ancestry and links : 0 at: 0x4faad20
# GenPart_pt  pt for Hard scattering particles, with ancestry and links : 0 at: 0x4fab380
# GenPart_eta eta for Hard scattering particles, with ancestry and links : 0 at: 0x4ce9c50
# GenPart_phi phi for Hard scattering particles, with ancestry and links : 0 at: 0x4cea2b0
# GenPart_mass   mass for Hard scattering particles, with ancestry and links : 0 at: 0x4fbe200
# GenPart_motherIndex  index of the mother in the generatorSummary for Hard scattering particles, with ancestry and links : 0 at: 0x4fbe860
