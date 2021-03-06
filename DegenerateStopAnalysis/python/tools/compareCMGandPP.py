# compareCMGandPP.py
# Simple script used to compare CMG and Post-Processed Tuples
# Mateusz Zarucki 2016
 
import ROOT
import glob
import argparse
import sys, os
import importlib
from pprint import pprint
from Workspace.HEPHYPythonTools.helpers import getYieldFromChain # getChain, getPlotFromChain, getChunks
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeLine, makeDoubleLine
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_v10 import cmgTuplesPostProcessed, ppDir, mc_path, data_path, signal_path
from Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISummer16MiniAODv2_v10 import makeGetChainFunc
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--cmgLocation", dest = "cmgLocation",  help = "CMG location (AFS or DPM)", type = str, default = "DPM", choices = ["AFS", "DPM"])
parser.add_argument("--cmgUserDir", dest = "cmgUserDir",  help = "CMG user directory", type = str, default = "")
parser.add_argument("--ppUserDir", dest = "ppUserDir",  help = "PP user directory", type = str, default = "")
parser.add_argument("--cmgTag", dest = "cmgTag",  help = "CMG Tag", type = str, default = "8025_mAODv2_v10")
parser.add_argument("--ppTag", dest = "ppTag",  help = "PP Tag", type = str, default = "v0")
parser.add_argument("--parameterSet", dest = "parameterSet",  help = "Parameter set", type = str, default = "analysisHephy_13TeV_2016_v2_6")
parser.add_argument("--samples", dest = "samples",  help = "Samples", type = str, nargs = "+", default = [])
parser.add_argument("--signalScan", action = "store_true",  help = "Compare bins")
parser.add_argument("--getData", action = "store_true",  help = "Get data")
parser.add_argument("--dataset", dest = "dataset",  help = "Data", type = str, default = "dblind")
parser.add_argument("--useHT", dest = "useHT",  help = "Use HT", type = int, default = 1)
parser.add_argument("--skim", dest = "skim",  help = "Skim", type = str, default = "preIncLep")
parser.add_argument("--compareBins", action = "store_true",  help = "Compare bins")
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)

args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()

# Arguments
if isinstance(args.samples, list): samplesList  = args.samples
else: samplesList = [args.samples]
cmgLocation = args.cmgLocation
cmgUserDir = args.cmgUserDir
ppUserDir = args.ppUserDir
cmgTag = args.cmgTag
ppTag = args.ppTag
parameterSet = args.parameterSet
signalScan = args.signalScan
getData = args.getData
dataset = args.dataset
useHT = args.useHT
skim = args.skim
compareBins = args.compareBins

# CMG Tuples
cmgDict = {'tag':cmgTag, 'version':cmgTag.split('_')[2]}
  
#if not cmgUserDir: #directory taken from cmgTuples sample definition file 
cmg_MC_path =   'Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISummer16MiniAODv2_%s'%cmgDict['version']
cmg_data_path = 'Workspace.DegenerateStopAnalysis.samples.cmgTuples.Data2016_%s'%cmgDict['version']

cmg_MC = importlib.import_module(cmg_MC_path)
cmg_data = importlib.import_module(cmg_data_path)

cmgDict['dir'] =         cmg_MC.sample_path_base 
cmgDict['mc_path'] =     cmg_MC.sample_path 
cmgDict['data_path'] =   cmg_data.sample_path 
cmgDict['signal_path'] = cmgDict['mc_path'] 

allComponents = {'MC':cmg_MC.allComponents, 'data':cmg_data.allComponents}

if cmgLocation == "DPM":
    cache_file_MC =   getattr(cmg_MC, "cache_file")

    if not cache_file_MC:
        #raise Exception("Cache file not found in cmgTuples")
        print "Cache file not found in cmgTuples"

    ## one needs to make sure the proxy is availble at this stage
    heppy_MC = cmg_MC.getHeppyMap()

    if not heppy_MC.heppy_sample_names:
        print "Something didn't work with the Heppy_sample_mapper.... no MC samples found"

    samps_to_get_mc = []

    for samp in cmg_MC.allComponents:
        samps_to_get_mc.append(samp['cmgName'])
        exts = samp.get("ext")
        if exts:
            samps_to_get_mc.extend(exts)
    
    for sampname in samps_to_get_mc:
        samp_for_dpm_mc = heppy_MC.from_heppy_samplename(sampname)
        if not samp_for_dpm_mc:
            print "No HeppyDPMSample was found for %s"%sampname
            print "Should be one of the samples in ", heppy_MC.heppy_sample_names
        setattr(cmg_MC, sampname, samp_for_dpm_mc)
    
    allComponents['MC'] = [getattr(cmg_MC, samp['cmgName']) for samp in cmg_MC.allComponents]

    if getData:
        cache_file_data = getattr(cmg_data, "cache_file")

        if not cache_file_data:
            print "Cache file not found in cmgTuples"

        heppy_data = cmg_data.getHeppyMap()
    
        if not heppy_data.heppy_sample_names:
            print "Something didn't work with the Heppy_sample_mapper.... no data samples found"
    
        samps_to_get_data = []

        for samp in cmg_data.allComponents:
            samps_to_get_data.append(samp['cmgName'])
            exts = samp.get("ext")
            if exts:
                samps_to_get_data.extend(exts)

        for sampname in samps_to_get_data:
            samp_for_dpm_data = heppy_data.from_heppy_samplename(sampname)
            if not samp_for_dpm_data:
                print "No HeppyDPMSample was found for %s"%sampname
                print "Should be one of the samples in ", heppy_data.heppy_sample_names
            setattr(cmg_data, sampname, samp_for_dpm_data)

        allComponents['data'] = [getattr(cmg_data, samp['cmgName']) for samp in cmg_data.allComponents]

elif cmgUserDir: #directory taken from manual input
   if cmgLocation == "AFS": cmgDict['dir'] = "/afs/hephy.at/data/%s/cmgTuples/%s"%(cmgUserDir, cmgTag) #afs/hephy.at/data
   else:           cmgDict['dir'] = "/data/%s/cmgTuples/%s"%(cmgUserDir, cmgTag) #/data
   
   cmgDict['mc_path'] =     cmgDict['dir'] + "/RunIISummer16MiniAODv2"
   cmgDict['data_path'] =   cmgDict['dir'] + "/Data25ns"
   cmgDict['signal_path'] = cmgDict['mc_path'] 

# PP Tuples
ppDict = {'version':ppTag}

if not ppUserDir: #directory taken from PP tuples sample definition file
   ppDict['dir'] =         ppDir 
   ppDict['mc_path'] =     mc_path 
   ppDict['data_path'] =   data_path 
   ppDict['signal_path'] = signal_path
else: #directory taken from manual input
   ppDict['dir'] = "/afs/hephy.at/data/%s/cmgTuples/postProcessed_mAODv2/%s/80X_postProcessing_%s/%s/step1"%(ppUserDir, cmgDict['tag'], ppDict['version'], parameterSet)
   ppDict['mc_path'] =     ppDict['dir'] + "/RunIISummer16MiniAODv2_%s"%cmgDict['version']
   ppDict['data_path'] =   ppDict['dir'] + "/Data2016_%s"%cmgDict['version']
   ppDict['signal_path'] = ppDict['mc_path'] 

if 'all' in samplesList: samplesList = ['w', 'tt_1l', 'tt_2l', 'qcd', 'z', 'dy', 'dy5to50', 'st', 'vv', 'ttx']

if getData:  
   samplesList.append(dataset)

cmgPP = cmgTuplesPostProcessed(ppDict['mc_path'], ppDict['signal_path'], ppDict['data_path'])
samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = signalScan, useHT = useHT, getData = getData)

# Signal
if signalScan:
    signalNames = []
    
    # CMG
    for s in allComponents['MC']:
        if s and 'isFastSim' in s:
            if s['isFastSim']:
                signalNames.append(s['name'])

    # PP
    combSignals = {}
    
    for sig in signalNames:
        simpName = sig.replace('-','_').split('_')[1]
        combSignals[simpName] = {}
        combSignals[simpName]['isSignal'] = 1
        combSignals[simpName]['isData'] = 0
        combSignals[simpName]['name'] = sig
        combSignals[simpName]['sample'] = {}
        combSignals[simpName]['sample']['name'] = sig
        combSignals[simpName]['sample']['bins'] = [sig]

        for samp in samples:
            if samples[samp].isSignal and "%s_%s"%(samples[samp]['sample']['name'].replace('-','_').split('_')[0],samples[samp]['sample']['name'].replace('-','_').split('_')[1]) in sig.replace('-','_'):
                if 'tree' not in combSignals[simpName]:
                    combSignals[simpName]['tree'] = samples[samp]['tree']
                else:
                    combSignals[simpName]['tree'].Add(samples[samp]['tree'])
        
        samplesList.append(simpName) 
    samples.update(combSignals)

print makeDoubleLine()
print "Comparing CMG and PP tuples:"
print "Samples: ", pprint(samplesList)
print makeLine()
print "CMG tuples:"
print pprint(cmgDict)
print makeLine()
print "PP tuples:"
print pprint(ppDict)
print makeDoubleLine()

#Results written to file   

i = 0
while os.path.exists("compareCMG-%s-andPP-%s-%s-%s.txt"%(cmgDict['tag'], ppDict['version'], skim, i)): # appends name by number if file exists
    i += 1

fileName = "compareCMG-%s-andPP-%s-%s-%s.txt"%(cmgDict['tag'], ppDict['version'], skim, i)

outfile = open(fileName, "w")
outfile.write(makeDoubleLine() + "\n")
outfile.write("Samples:")
for x in samplesList:
   outfile.write(" " + x)
outfile.write("\nCMG tuples:\n")
for x in cmgDict.keys():
   outfile.write(\
      x + " :" + cmgDict[x] + "\n")
outfile.write(makeLine() + "\nPP tuples:\n")
for x in ppDict.keys():
   outfile.write(\
      x + " :" + ppDict[x] + "\n")
outfile.close()

if skim == "preIncLep": 
   metCut = "(met_pt > 200)"
   leadingJet_pt = "((Max$(Jet_pt*(abs(Jet_eta) < 2.4 && Jet_id)) > 90 ) >= 1)"
   HTCut = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && Jet_id)) > 200)"

   skimString = "(%s)"%'&&'.join([metCut, leadingJet_pt, HTCut])

# lepton skimming
elif skim == 'oneLep':
   skimString = "(nLepGood >=1 || nLepOther >=1)"

elif skim == 'oneLep20':
   skimString = "((nLepGood >=1 && LepGood_pt[0] > 20) || (nLepOther >=1 && LepOther_pt[0] > 20))"

elif skim == 'oneLepGood':
   skimString = "(nLepGood >=1)"

elif skim == 'oneLepGood20':
   skimString = "(nLepGood >=1 && LepGood_pt[0] > 20)"

elif skim == 'oneLepGood20_ISR100':
   skimString = "((nLepGood >=1 && LepGood_pt[0] > 20) && (Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && (Jet_id))>100)))"

elif skim == 'oneLepGood_HT800':
   skimString = "(nLepGood >=1 && (Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && (Jet_id))) > 800))"

elif skim == 'lt120':
   skimString = "(nLepGood >=1 && ((met_pt + LepGood_pt[0])>120))"

elif skim == 'oneLepGood_HT100_MET40_MT30':
   skimString = "(Sum$( abs(LepGood_pdgId)==13 && LepGood_pt > 50 )>=1 && (Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && (Jet_id))>100)) && met_pt < 40 && Sum$( abs(LepGood_pdgId)==13 && LepGood_mt < 30 ) )"

elif skim == 'oneElGood50_ISR100_MET40_MT30':
   skimString = "(Sum$( abs(LepGood_pdgId)==11 && LepGood_pt > 50 )>=1 && (Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && (Jet_id))>100)) && met_pt < 40 && Sum$( abs(LepGood_pdgId)==11 && LepGood_mt < 30 ) )"

elif skim == 'met200':
   skimString = "(met_pt > 200)"

elif 'HT300_ISR100' in skim:
   skimString = "((Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && (Jet_id))) > 300) && (Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && (Jet_id))>100)))"


nBin = {'cmg':{}, 'pp':{}}

for samp in samplesList:
   with open(fileName, "a") as outfile:
      outfile.write(makeDoubleLine() + "\n")
      print makeDoubleLine()
      print "Comparing sample", samples[samp]['name'], "with", skim, "skim:" 
      
      outfile.write(\
         makeLine() + "\n" +
         "Sample " + samp + " with " + skim + " skim: \n" +
         makeLine() + "\n")

      if samples[samp]['isData']:
         sampType = 'data'
      else:
         sampType = 'MC'

      if compareBins and ('bins' not in samples[samp]['sample'] or 'dir' not in samples[samp]):
          print "Either 'bins' or 'dir' entries missing in sample definition. Skipping bin comparison."
          compareBins = False

      nCMG = 0
      nPP2 = 0
 
      for bin in samples[samp]['sample']['bins']:
         for comp in allComponents[sampType]:
            if not comp: continue 
            if bin == comp['name']: 
               
               t1 = makeGetChainFunc(comp)() 
                
               nBin['cmg'][bin] = getYieldFromChain(t1, skimString, "1")

               nCMG += nBin['cmg'][bin] 
 
               if compareBins:
                  ppBinPath = "%s/%s/%s_Chunks*.root"%(samples[samp]['dir'], bin, bin)
                  files2 = glob.glob(ppBinPath)
                  
                  t2 = ROOT.TChain("Events")
                  
                  for f2 in files2:
                     t2.Add(f2)

                  nBin['pp'][bin] = getYieldFromChain(t2, "1", "1")

                  nPP2 += nBin['pp'][bin] 

      nPP = getYieldFromChain(samples[samp]['tree'], "1", "1")
         
      if compareBins:
         for bin in samples[samp]['sample']['bins']:
            print makeLine()
            if nBin['cmg'][bin]: 
               if nBin['pp'][bin]/nBin['cmg'][bin] == 1: 
                  print samples[samp]['name'], "bin", bin, ": Good with", nBin['pp'][bin], "events!"
                  outfile.write(samples[samp]['name'] + " bin " + bin + ": Good with " + str(nBin['pp'][bin]) + " events!\n")
               else:
                  print "!!! PP and CMG numbers do NOT correspond !!!"
                  print "Number of CMG events in bin", bin, ":", nBin['cmg'][bin] 
                  print "Number of PP events in bin", bin, ":", nBin['pp'][bin] 
                  outfile.write(\
                  "!!! PP and CMG numbers do NOT correspond !!!\n" +
                  "Number of CMG events in bin " + bin + ":" + str(nBin['cmg'][bin]) + "\n" +
                  "Number of PP events in bin " + bin + ":" + str(nBin['pp'][bin]) + "\n")
            else:
               print "Warning: nCMG = 0. CMG sample bin exists?"
               outfile.write("Warning: nCMG = 0. CMG sample bin exists?\n")
               
            print makeLine()
            outfile.write(makeLine() + "\n")
  
      if nCMG: 
         if nPP/nCMG == 1: 
            print samples[samp]['name'], "sample: Good with", nPP, " events!"
            outfile.write(samples[samp]['name'] + " sample: Good with " + str(nPP) + " events!\n")
         else: 
            print "!!! PP and CMG numbers do NOT correspond !!!"
            print "Total number of Events @ CMG:", nCMG
            print "Total number of Events @ PP:", nPP 
            outfile.write(\
             "!!! PP and CMG numbers do NOT correspond !!!\n" +
            "Total number of Events @ CMG: " + str(nCMG) + "\n" +
            "Total number of Events @ PP: " + str(nPP) + "\n")
            if compareBins: 
               print "Total number of Events @ PP (x-check):", nPP2  
               outfile.write("Total number of Events @ PP (x-check): " + str(nPP2) + "\n")

      else: 
         print "Warning: nCMG = 0. CMG sample exists?"
         outfile.write("Warning: nCMG = 0. CMG sample exists?\n")

   outfile.close()
