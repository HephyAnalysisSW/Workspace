#!/usr/bin/env python

'''
Generate events from gridpacks stored locally, using the hephy batch system.
This script creates the txt file to be used with submitBatch.py
Gridpacks can be selected using a qualifier string.
A sandbox is created in the tmp_directory.
'''

import os
import uuid
import glob

CMSSW_BASE = os.path.expandvars("$CMSSW_BASE")
cfg_path = os.path.join(CMSSW_BASE, 'src/Workspace/DegenerateStopAnalysis/T2DegStop13TeVEventGeneration/StopPolar/Generation/production/')
#tmp_directory = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/generation_tmp/")
tmp_directory = os.path.expandvars("/afs/hephy.at/data/nrad01/tmp_/")

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--gridpackdir',           action='store',      default='/eos/user/n/nrad/gridpacks/StopPolar/',          nargs='?', help="Where are the gridpacks?")
argParser.add_argument('--pattern',             action='store',      default='*.tar.xz',          nargs='?', help="Where are the gridpacks?")
argParser.add_argument('--maxEvents',           action='store',      default=100000,          nargs='?', help="How many events?")
argParser.add_argument('--outDir',           action='store',      default='/eos/user/n/nrad/StopPolar/GEN/',                nargs='?', help="")

args = argParser.parse_args()


pattern   = args.pattern
gridpacks = glob.glob( args.gridpackdir +"/"+pattern )
outDir    = args.outDir 

commands = []
command_template = "python runGEN.py --gridpack=%s --outDir=%s --maxEvents=%s"
for gp in gridpacks:
    gpname   = os.path.basename( gp ).replace(".tar.xz","")
    niceName = gpname.split("_slc6")[0]
    command = command_template%( gp, outDir +"/" + niceName , args.maxEvents )
    commands.append(command)


for c in commands:
  print c

