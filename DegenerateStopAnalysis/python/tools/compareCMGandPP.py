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
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_Summer16 import cmgTuplesPostProcessed, ppDir, mc_path, data_path, signal_path
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--cmgUserDir", dest = "cmgUserDir",  help = "CMG user directory", type = str, default = "")
parser.add_argument("--cmgInAFS", dest = "cmgInAFS",  help = "cmgInAFS", type = int, default = 1)
parser.add_argument("--ppUserDir", dest = "ppUserDir",  help = "PP user directory", type = str, default = "")
parser.add_argument("--cmgTag", dest = "cmgTag",  help = "CMG Tag", type = str, default = "8025_mAODv2_v7")
parser.add_argument("--ppTag", dest = "ppTag",  help = "PP Tag", type = str, default = "v0")
parser.add_argument("--parameterSet", dest = "parameterSet",  help = "Parameter set", type = str, default = "analysisHephy_13TeV_2016_v2_3")
parser.add_argument("--samples", dest = "samples",  help = "Samples", type = str, nargs = "+", default = "all")
parser.add_argument("--signalScan", action = "store_true",  help = "Compare bins")
parser.add_argument("--getData", action = "store_true",  help = "Compare bins")
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
cmgUserDir = args.cmgUserDir
cmgInAFS = args.cmgInAFS
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
  
if not cmgUserDir: #directory taken from cmgTuples sample definition file 
   cmg_MC_path =   'Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISummer16MiniAODv2_%s'%cmgDict['version']
   cmg_data_path = 'Workspace.DegenerateStopAnalysis.samples.cmgTuples.Data2016_%s'%cmgDict['version']
   
   cmg_MC = importlib.import_module(cmg_MC_path)
   cmg_data = importlib.import_module(cmg_data_path)
   
   cmgDict['dir'] =         cmg_MC.sample_path_base 
   cmgDict['mc_path'] =     cmg_MC.sample_path 
   cmgDict['data_path'] =   cmg_data.sample_path 
   cmgDict['signal_path'] = cmgDict['mc_path'] 

else: #directory taken from manual input
   if cmgInAFS: cmgDict['dir'] = "/afs/hephy.at/data/%s/cmgTuples/%s"%(cmgUserDir, cmgTag) #afs/hephy.at/data
   else:        cmgDict['dir'] = "/data/%s/cmgTuples/%s"%(cmgUserDir, cmgTag) #/data
   
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

if samplesList[0] == "all": samplesList = ['w', 'tt', 'qcd', 'z', 'dy', 'st', 'vv']

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

outfile = open("compareCMG-%s-andPP-%s-%s-%s.txt"%(cmgDict['tag'], ppDict['version'], skim, i), "w")
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

if getData:  
   samplesList.append(dataset)

cmgPP = cmgTuplesPostProcessed(ppDict['mc_path'], ppDict['signal_path'], ppDict['data_path'])

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = signalScan, useHT = useHT, getData = getData)

#if 'tt' in samplesList and not useHT: 
#   samplesList.remove('tt')
#   samplesList.append('ttInc')

#FIXME: Add LHE skim for tt+jets

if skim == "preIncLep": 
    # branches for preselection (scalars or vectors) must be included in readVar or readVectors
    metCut = "(met_pt > 200)"
    leadingJet_pt = "((Max$(Jet_pt*(abs(Jet_eta) < 2.4 && Jet_id)) > 90 ) >= 1)"
    HTCut = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && Jet_id)) > 200)"

    skimString = "(%s)"%'&&'.join([metCut, leadingJet_pt, HTCut])

# lepton skimming
elif skim == 'oneLep':
    skimString = "(nLepGood >=1 || nLepOther >=1)"

elif skim == 'oneLepGood':
    skimString = "(nLepGood >=1)"

elif skim == 'oneLep20':
    skimString = "((nLepGood >=1 && LepGood_pt[0] > 20) || (nLepOther >=1 && LepOther_pt[0] > 20))"

elif skim == 'oneLepGood_HT800':
    skimString = "(nLepGood >=1 && (Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && (Jet_id))) > 800))"
elif skim == 'lt120':
    skimString = "(nLepGood >=1 && ((met_pt + LepGood_pt[0])>120))"

nBin = {'cmg':{}, 'pp':{}}

for samp in samplesList:
   outfile.write(makeDoubleLine() + "\n")
   print makeDoubleLine()
   print "Comparing sample", samples[samp]['name'], "with", skim, "skim:" 
   
   outfile.write(\
      makeLine() + "\n" +
      "Sample " + samp + " with " + skim + " skim: \n" +
      makeLine() + "\n")

   nCMG = 0
   nPP2 = 0 
 
   for bin in samples[samp].sample['bins']:
      if samples[samp].isData: 
         cmgPath = "%s/%s/%s_Chunk*/tree.root"%(cmgDict['data_path'], bin, bin)
      else:
         cmgPath = "%s/%s/%s_Chunk*/tree.root"%(cmgDict['mc_path'], bin, bin)

      files1 = glob.glob(cmgPath)
      
      t1 = ROOT.TChain("tree")
      
      for f1 in files1:
         t1.Add(f1)

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

   nPP = getYieldFromChain(samples[samp].tree, "1", "1")
      
   if compareBins: 
      for bin in samples[samp].sample['bins']:
         print makeLine()
         if nBin['cmg'][bin]: 
            if nBin['pp'][bin]/nBin['cmg'][bin] == 1: 
               #print "Number of CMG events in bin ", bin, ":", nBin['cmg'][bin] 
               #print "Number of PP events in bin ", bin, ":", nBin['pp'][bin] 
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
         #print "Total number of Events @ CMG: ", nCMG
         #print "Total number of Events @ PP: ", nPP, 
         #if compareBins: print "Total number of Events @ PP (x-check): ", nPP2  
         print samples[samp]['name'], "sample: Good with", nPP, " events!"
         outfile.write(samples[samp]['name'] + "sample: Good with " + str(nPP) + " events!\n")
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
   
print makeDoubleLine()
outfile.write(makeDoubleLine())
outfile.close()
