# compareCMGandPPS.py
# Simple script used to compare CMG and Post-Processed Tuples
# Mateusz Zarucki 2016
 
import ROOT
import glob
import argparse
import sys
import pprint as pp

from Workspace.HEPHYPythonTools.helpers import getYieldFromChain # getChain, getPlotFromChain, getChunks
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeLine, makeDoubleLine
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.tools.getSamples import getSamples

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--cmgUserDir", dest = "cmgUserDir",  help = "CMG user directory", type = str, default = "nrad")
parser.add_argument("--ppsUserDir", dest = "ppsUserDir",  help = "PPS user directory", type = str, default = "nrad01")
parser.add_argument("--cmgTag", dest = "cmgTag",  help = "CMG Tag", type = str, default = "8020_mAODv2_v0")
parser.add_argument("--ppsTag", dest = "ppsTag",  help = "PPS Tag", type = str, default = "v0")
parser.add_argument("--parameterSet", dest = "parameterSet",  help = "Parameter set", type = str, default = "analysisHephy_13TeV_2016_v2_0")
parser.add_argument("--samples", dest = "samples",  help = "Samples", type = str, nargs = "+", default = "all")
parser.add_argument("--signalScan", dest = "signalScan",  help = "Signal scan", type = int, default = 0)
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 0)
parser.add_argument("--dataset", dest = "dataset",  help = "Data", type = str, default = "dblind")
parser.add_argument("--useHT", dest = "useHT",  help = "Use HT", type = int, default = 1)
parser.add_argument("--skim", dest = "skim",  help = "Skim", type = str, default = "preIncLep")
parser.add_argument("--compareBins", dest = "compareBins",  help = "Compare bins", type = int, default = 0)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()

#Arguments
if isinstance(args.samples, list): samplesList  = args.samples
else: samplesList = [args.samples]
cmgUserDir = args.cmgUserDir
ppsUserDir = args.ppsUserDir
cmgTag = args.cmgTag
ppsTag = args.ppsTag
parameterSet = args.parameterSet
signalScan = args.signalScan
getData = args.getData
dataset = args.dataset
useHT = args.useHT
skim = args.skim
compareBins = args.compareBins

cmgDict = {'tag':cmgTag,
           'version':cmgTag.split('_')[2],
           'dir':"/data/%s/cmgTuples/%s"%(cmgUserDir, cmgTag)}
           #'dir':"/afs/hephy.at/data/%s01/cmgTuples/%s"%(cmgUserDir, cmgTag)}

cmgDict['mc_path'] =     cmgDict['dir'] + "/RunIISpring16MiniAODv2"
cmgDict['data_path'] =   cmgDict['dir'] + "/Data25ns"
cmgDict['signal_path'] = cmgDict['mc_path'] 

ppsDict = {'version':ppsTag}
ppsDict['dir'] = "/afs/hephy.at/data/%s/cmgTuples/postProcessed_mAODv2/%s/80X_postProcessing_%s/%s/step1"%(ppsUserDir, cmgDict['tag'], ppsDict['version'], parameterSet)
ppsDict['mc_path'] =     ppsDict['dir'] + "/RunIISpring16MiniAODv2_%s"%cmgDict['version']
ppsDict['data_path'] =   ppsDict['dir'] + "/Data2016_%s"%cmgDict['version']
ppsDict['signal_path'] = ppsDict['mc_path'] 

print makeDoubleLine()
print "Comparing CMG and PPS tuples"
print makeLine()
print "CMG tuples:"
print pp.pprint(cmgDict)
print makeLine()
print "PPS tuples:"
print pp.pprint(ppsDict)
print makeDoubleLine()

#Results written to file   
outfile = open("compareCMG__%s__andPPS_%s_%s.txt"%(cmgDict['tag'], ppsDict['version'], skim), "w")
outfile.write(makeDoubleLine() + "\n")
outfile.write("CMG tuples:\n")
for x in cmgDict.keys():
   outfile.write(\
      x + ":" + cmgDict[x] + "\n")
outfile.write(makeLine() + "\nPPS tuples:\n")
for x in ppsDict.keys():
   outfile.write(\
      x + ":" + ppsDict[x] + "\n")
outfile.write(makeDoubleLine() + "\n")

if samplesList[0] == "all": samplesList = ['w', 'tt', 'qcd', 'dy', 'st', 'vv'] #FIXME: Add LHE skim for tt+jets

if getData:  
   samplesList.append(dataset)

cmgPP = cmgTuplesPostProcessed(ppsDict['mc_path'], ppsDict['signal_path'], ppsDict['data_path'])

samples = getSamples(cmgPP = cmgPP, skim = skim, sampleList = samplesList, scan = signalScan, useHT = useHT, getData = getData)

if 'tt' in samplesList and not useHT: 
   samplesList.remove('tt')
   samplesList.append('ttInc')

if skim == "preIncLep": 
    # branches for preselection (scalars or vectors) must be included in readVar or readVectors
    metCut = "(met_pt > 200)"
    leadingJet_pt = "((Max$(Jet_pt*(abs(Jet_eta) < 2.4 && Jet_id)) > 90 ) >= 1)"
    HTCut = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && Jet_id)) > 200)"

    skimString = "(%s)"%'&&'.join([metCut, leadingJet_pt, HTCut])

# lepton skimming
elif skim == 'oneLep':
    skimString = "(nLepGood >=1 || nLepOther >=1)"

elif skim == 'oneLep20':
    skimString = " ((nLepGood >=1 && LepGood_pt[0] > 20) || (nLepOther >=1 && LepOther_pt[0] > 20))"

elif skim == 'oneLepGood_HT800':
    skimString = " (nLepGood >=1 && (Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && (Jet_id))) > 800))"

nBin = {'cmg':{}, 'pps':{}}

for samp in samplesList:
   print "Comparing sample", samples[samp]['name'], "with", skim, "skim" 
   print makeDoubleLine()
   
   outfile.write(\
      makeLine() + "\n" +
      "Sample " + samp + " with " + skim + " skim: \n" +
      makeLine() + "\n")

   nCMG = 0
   nPPS2 = 0 
 
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
         ppsBinPath = "%s/%s/%s_Chunks*.root"%(samples[samp]['dir'], bin, bin)

         files2 = glob.glob(ppsBinPath)
         
         t2 = ROOT.TChain("Events")
         
         for f2 in files2:
            t2.Add(f2)

         nBin['pps'][bin] = getYieldFromChain(t2, "1", "1")

         nPPS2 += nBin['pps'][bin] 

   nPPS = getYieldFromChain(samples[samp].tree, "1", "1")
      
   if compareBins: 
      for bin in samples[samp].sample['bins']:
         print makeLine()
         if nBin['cmg'][bin]: 
            if nBin['pps'][bin]/nBin['cmg'][bin] == 1: 
               #print "Number of CMG events in bin ", bin, ":", nBin['cmg'][bin] 
               #print "Number of PPS events in bin ", bin, ":", nBin['pps'][bin] 
               print samples[samp]['name'], "bin", bin, ": Good with", nBin['pps'][bin], "events!"
               outfile.write(samples[samp]['name'] + " bin " + bin + " : Good with " + str(nBin['pps'][bin]) + " events!\n")
            else:
               print "!!! PPS and CMG numbers do NOT correspond !!!"
               print "Number of CMG events in bin", bin, ":", nBin['cmg'][bin] 
               print "Number of PPS events in bin", bin, ":", nBin['pps'][bin] 
               outfile.write(\
               "!!! PPS and CMG numbers do NOT correspond !!!\n" +
               "Number of CMG events in bin" + bin + ":" + str(nBin['cmg'][bin]) + "\n" +
               "Number of PPS events in bin" + bin + ":" + str(nBin['pps'][bin]) + "\n")
         else:
            print "Warning: nCMG = 0. CMG sample bin exists?"
            outfile.write("Warning: nCMG = 0. CMG sample bin exists?\n")
            
         print makeLine()
         outfile.write(makeLine() + "\n")
  
   if nCMG: 
      if nPPS/nCMG == 1: 
         #print "Total number of Events @ CMG: ", nCMG
         #print "Total number of Events @ PPS: ", nPPS, 
         #if compareBins: print "Total number of Events @ PPS (x-check): ", nPPS2  
         print samples[samp]['name'], "sample: Good with", nPPS, " events!"
         outfile.write(samples[samp]['name'] + "sample: Good with " + nPPS + " events!\n")
      else: 
         print "!!! PPS and CMG numbers do NOT correspond !!!"
         print "Total number of Events @ CMG:", nCMG
         print "Total number of Events @ PPS:", nPPS 
         outfile.write(\
          "!!! PPS and CMG numbers do NOT correspond !!!\n" +
         "Total number of Events @ CMG:" + str(nCMG) + "\n" +
         "Total number of Events @ PPS:" + str(nPPS) + "\n")
         if compareBins: 
            print "Total number of Events @ PPS (x-check):", nPPS2  
            outfile.write("Total number of Events @ PPS (x-check): " + str(nPPS2) + "\n")

   else: 
      print "Warning: nCMG = 0. CMG sample exists?"
      outfile.write("Warning: nCMG = 0. CMG sample exists?\n")

   print makeDoubleLine() 
   outfile.write(makeDoubleLine() + "\n")

outfile.close()
