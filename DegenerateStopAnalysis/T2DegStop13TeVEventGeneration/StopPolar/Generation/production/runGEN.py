#!/usr/bin/env python

'''
Generate events from gridpacks stored locally, using the hephy batch system.
This script creates the txt file to be used with submitBatch.py
Gridpacks can be selected using a qualifier string.
A sandbox is created in the tmp_directory.
'''

import os
import uuid

CMSSW_BASE = os.path.expandvars("$CMSSW_BASE")
cfg_path = os.path.join(CMSSW_BASE, 'src/Workspace/DegenerateStopAnalysis/T2DegStop13TeVEventGeneration/StopPolar/Generation/production/')
#tmp_directory = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/generation_tmp/")
tmp_directory = os.path.expandvars("/afs/hephy.at/data/nrad01/tmp_/")

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--gridpack',           action='store',      default='/afs/hephy.at/data/nrad03/StopPolar/gridpacks/',          nargs='?', help="Where are the gridpacks?")
argParser.add_argument('--maxEvents',           action='store',      default=100000,          nargs='?', help="How many events?")
argParser.add_argument('--outDir',           action='store',      default='/afs/hephy.at/data/nrad03/StopPolar/genSamples/',                nargs='?', help="")

args = argParser.parse_args()

GENSCRIPT = cfg_path + "/GEN.py"
import glob

def runGEN( gridpack, outputDir, maxEvents):
    tmp_dir = "tmp_%s/"%uuid.uuid4()
    tmp_dir = os.path.abspath( tmp_dir )
    print "Working in tmp dir: %s"%tmp_dir
    os.makedirs( tmp_dir)
    commands = []
    if not os.path.isfile( GENSCRIPT ):
        raise Exception("GEN.py script was not found. Expected it at: %s"%GENSCRIPT )
    if not os.path.isfile( gridpack ):
        raise Exception("gridpack was not found. Expected it at: %s"%gridpack )
    commands = [
                  "cp %s %s/GEN.py"%(GENSCRIPT, tmp_dir),
                  "cd %s"%tmp_dir,
                  "cmsRun GEN.py gridpack={gridpack} maxEvents={maxEvents}".format(gridpack=gridpack, maxEvents=maxEvents),
               ]
    print commands
    os.system(';'.join(commands))
    if not os.path.isdir( outputDir): os.makedirs( outputDir )
    commands_finishup = [
                          "mv %s/events.root %s"%(tmp_dir, outputDir),
                          "rm -rf %s"%tmp_dir, 
                       ]
    os.system(';'.join(commands_finishup))
    command = "rm -rf %s"%tmp_dir
    print "Output moved to: %s"%outputDir

if __name__=='__main__':
    runGEN( args.gridpack, args.outDir, args.maxEvents )


if False:
    gridpacks = [ gp for gp in os.listdir(args.gridpackDir) if args.qualifier in gp ]
    
    baseDir = os.path.abspath('.')
    cfg     = os.path.join(cfg_path, args.cfg)
    
    with open(args.outFile, 'w') as f:
        for gp in gridpacks:
            gpName      = gp.replace(".tar.xz","").replace(".","p").replace("-","m")
            uniqueDir   = uuid.uuid4().hex
            uPath       = os.path.join(tmp_directory, uniqueDir)
            line        = "mkdir %s; cp %s %s; cd %s; cmsRun %s gridpack=%s/%s maxEvents=%s outputDir=%s/%s/; cd %s; rm -rf %s\n"%(uPath, cfg, uPath, uPath, args.cfg, args.gridpackDir, gp, args.maxEvents, args.outDir, gpName, baseDir, uPath)
            #print line
            f.write(line)
    
    print "Created submit file: %s"%args.outFile
    print "You can copy the content of 'forSamplesPY.txt' to your sample python file."
    print "Samples contained:"
    
    with open('forSamplesPY.txt', 'w') as f:
        for gp in gridpacks:
            gpName      = gp.replace(".tar.xz","").replace(".","p").replace("-","m")
            niceName    = gpName.replace("0000", "")
            line = '{:40}= FWLiteSample.fromFiles({:40} , texName="", files = ["{}/{}/events.root"])\n'.format(niceName, '"%s"'%niceName, args.outDir, gpName)
            print niceName
            f.write(line)
    
    with open('forPPSamplesPY.txt', 'w') as f:
        for gp in gridpacks:
            gpName      = gp.replace(".tar.xz","").replace(".","p").replace("-","m")
            niceName    = gpName.replace("0000", "")
            line = '{:40}= Sample.fromDirectory({:40}, directory = [os.path.join( gen_dir, "{}/")])\n'.format(niceName, '"%s"'%niceName, niceName)
            #print niceName
            f.write(line)
    
    
