#!/usr/bin/env python
import sys,os
from Workspace.DegenerateStopAnalysis.tools.degTools import ArgParser, getHostName, makeDir

parser = ArgParser()
parser.add_argument('--cfg',                    action="store", help='config directory to load the cfg file from')
parser.add_argument('--cfg_path',               action="store", default="Workspace.DegenerateStopAnalysis.cfgs", help='Python Path for the config directory')
parser.add_argument('--small',                  action="store_true", help='Only Run over the first signal sample')
parser.add_argument('--interactive', '-i',      action="store_true", help='Use if you want to look at the cfg, samples, etc interactively')
parser.add_argument('--only_yields',            action="store_true", help='Only Calculate yields without calculating the limits ( can run jobs in parallel)')
parser.add_argument('--redo_yields',            action="store_true", help='Recalculate yields')
parser.add_argument('--redo_limit',             action="store_true", help='Recalculate limits')
parser.add_argument('--redo_eventLists',        action="store_true", help='Redo EventLists')

parser.add_argument('--lep',        default = 'lep',                action="store", help='')
parser.add_argument('--lepCol',     default = 'Lepton',             action="store", help='')
parser.add_argument('--jetCol',     default = 'JetClean',           action="store", help='')
parser.add_argument('--tauCol',     default = 'TauClean',           action="store", help='')
parser.add_argument('--task',       default = 'plots',              action="store", help='')
parser.add_argument('--cuts',       default = '',     nargs = "+",  action="store", help='')
parser.add_argument('--plot',       default = '',     nargs = "+",  action="store", help='')
parser.add_argument('--nMinus1',         action="store_true", help='Make nMinus1 Plot ')

parser.add_argument('--weights',    default = [],  nargs = "+", action="store", help='List of weights to apply')
parser.add_argument('--postFuncs',  default = '',  nargs = "+", action="store", help='')

parser.add_argument('--mcMatch',   default = '',                action="store_true", help='')

parser.add_argument('--nanoAOD',   default = '',                action="store_true", help='')
parser.add_argument("--year",      default = "2016",            action = "store", help = "Year")
parser.add_argument('--lepThresh', default = '',                action="store", help='')
parser.add_argument('--jetThresh', default = '',                action="store", help='')

parser.add_argument('--sigOpt',    default = 'NoSig',       action="store", help='BM= benchmark points only, NoSig=NoSignal , All=allsignal')
parser.add_argument('--bkgs',       nargs="+",      help='')

parser.add_argument('--getData',   default = '',                action="store_true", help='')
parser.add_argument('--dataset',   default = 'MET',      action="store", help='Dataset')
parser.add_argument('--ppSet',     default='nanoAOD_v6_0-0',          action="store", help='')
parser.add_argument('--nProc',     default=1,      type=int,    action="store" , help="Number of processes. if more than 1 multicores will be used")


parser.add_argument('--generalTag', default = '',             action="store", help='')
parser.add_argument('--sysTag',     default = 'AdjustedSys',             action="store", help='')
parser.add_argument('--skim',       default = 'preIncLep',             action="store", help='')

parser.add_argument('--fomplot',    default = '',     action="store_true", help='')

# MVA
parser.add_argument('--mvaId' ,        default = '',                         action="store", help='')
parser.add_argument('--bdtcut',        default = '',        type=str,        action="store", help='')
parser.add_argument('--step2',         default = '',        type=str,        action="store", help='')

parser.add_argument('--verbose',    action = "store_true", help = 'Verbose')

args = parser.parse(sys.argv, setdef = False)
   
# importing the cfg from arguments
if __name__=="__main__":
    cfgs_path = args.cfg_path
    cfg_dir   = cfgs_path + "." + args.cfg
    cfg_mod   = cfg_dir +".cfg"
    cfg_      = __import__(cfg_mod, fromlist = ['cfg'])
    cfg       = cfg_.cfg

    if "worker" in getHostName():
        args.nProc = 1

    args.nProc = min(args.nProc, 16) # NOTE: number of processess shouldn't be too much more than twice the number of cores (according to the internets)

    if args.interactive:
        raise Exception("Sorry to raise an exception, but you wanted to run interactively!")

    results = {}
    pool = {}
    task_ret = {}

    for task in cfg.taskList:
        pool[task] = {}
        results[task] = {}
        task_ret[task] = {}
        makeDir(cfg.saveDir)
        task_func = cfg.taskFuncs[task]

        print "Running Task: %s %s"%(task, task_func)
        print "\n=================================================================================\n"
        task_ret[task] = task_func(cfg, args)

#### a better way to import maybe(?)  
#### Stolen from http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
####import os, sys, inspect
#### # realpath() will make your script run, even if you symlink it :)
#### cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
#### if cmd_folder not in sys.path:
####     sys.path.insert(0, cmd_folder)
####
#### # use this if you want to include modules from a subfolder
#### cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
#### if cmd_subfolder not in sys.path:
####     sys.path.insert(0, cmd_subfolder)
