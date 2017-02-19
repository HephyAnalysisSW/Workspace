#!/usr/bin/env python
import sys,os
import pprint as pp
import shutil

import gc

import multiprocessing as mp

from    Workspace.DegenerateStopAnalysis.tools.degTools import *
#from    Workspace.DegenerateStopAnalysis.tools.limitCalc import  getLimit, plotLimits
#import  Workspace.DegenerateStopAnalysis.tools.limitTools as limitTools



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
####
## multiprocessing requires everything to be below
if True:

    parser = ArgParser()
    parser.add_argument('--cfg',                    action="store", help='config directory to load the cfg file from')
    parser.add_argument('--cfg_path',               action="store", default="Workspace.DegenerateStopAnalysis.cfgs", help='Python Path for the config directory')
    parser.add_argument('--small',                  action="store_true", help='Only Run over the first signal sample')
    parser.add_argument('-i','--interactive',       action="store_true", help='Use if you want to look at the cfg, samples, etc interactively')
    parser.add_argument('--only_yields',            action="store_true", help='Only Calculate yields without calculating the limits ( can run jobs in parallel)')
    parser.add_argument('--redo_yields',            action="store_true", help='Recalculate yields even if cfg says not to')
    parser.add_argument('--redo_limit',             action="store_true", help='Recalculate limits even if cfg says not to')
    parser.add_argument('--redo_eventLists',        action="store_true", help='Redo EventLists')

    parser.add_argument('--lep',        default = 'lep',                action="store", help='')
    parser.add_argument('--lepCol',     default = 'LepGood',            action="store", help='')
    parser.add_argument('--task',       default = 'plots',         action="store", help='')
    parser.add_argument('--cutInst',    default = '',     nargs = "+",  action="store", help='')
    parser.add_argument('--plot',       default = '',     nargs = "+",  action="store", help='')
    parser.add_argument('--nMinus1',         action="store_true", help='Make nMinus1 Plot ')
    
    parser.add_argument('--pu',         default = 'pu',                 action="store", help='choose between pu, pu_up, pu_down')
    parser.add_argument('--weight',     default = 'base',               action="store", help='')
    parser.add_argument('--btag',       default = 'btag',               action="store", help='')
    parser.add_argument('--mcMatch',     action="store_true", help='do mcMatch for lepton (should not be used with LepAll for now)')
    parser.add_argument('--postFuncs',    default = '',     nargs = "+",  action="store", help='')


    parser.add_argument('--lepThresh',        default = '',                action="store", help='')
    parser.add_argument('--jetThresh',        default = '',                action="store", help='')

    parser.add_argument('--sigOpt',    default='All',       action="store", help='BM= benchmark points only, NoSig=NoSignal , All=allsignal')
    parser.add_argument('--bkgs',       nargs="+",      help='')
    parser.add_argument('--data',      default="d",      help='')
    parser.add_argument('--ppSet',     default='80X',          action="store", help='')
    parser.add_argument('--nProc',     default=1,      type=int,    action="store" , help="Number of processes. if more than 1 multicores will be used" )


    parser.add_argument('--fomplot',    default = '',     action="store_true", help='')
    #MVA
    parser.add_argument('--mvaId' ,        default = '',                           action="store", help='')
    parser.add_argument('--bdtcut',        default = '',        type=str,        action="store", help='')
    parser.add_argument('--step2',         default = '',        type=str,        action="store", help='')


    args=parser.parse(sys.argv, setdef=False)
    
if __name__=="__main__":
    ## importing the cfg from arguments
    cfgs_path = args.cfg_path
    cfg_dir   = cfgs_path +"." + args.cfg
    cfg_mod   = cfg_dir +".cfg"
    cfg_      = __import__(cfg_mod, fromlist = ['cfg'] )
    cfg       = cfg_.cfg


    ## Setting UP TDR Style
    do_tdr = getattr(cfg,"tdr_style", True)
    if do_tdr:
        setup_style()

    try:
        samples  
        print "-------- reusing samples"
    except NameError:
        ### 
        samples    = getattr(cfg, "samples" )


    ##
    ##  Common Params amongst tasks
    ##
    
    cutInstList  = cfg.cutInstList
    sampleList   = getattr(cfg, "sampleList", cfg.samples.keys() )[:]
    cutName      = cfg.cutName
    fullTag = "%s_%s"%( cfg.runTag , cfg.htString )


    
    signalList = getattr( cfg, "signalList", [] )
    if args.small:
        signalList = signalList[:1]
    sampleList += signalList
    
    
    print " "
    print " . . . . . . . . . Running : . . . . . . . ." , "        ", cfg.runTag
    print " "

    
    if args.interactive:
        raise Exception("Sorry to raise an exception, but you wanted to run interactively!")

    write_tfile = False
    if write_tfile:
        print "Root File saved to:", cfg.saveDir+"/%s.root"%fullTag  
        tfile = ROOT.TFile(cfg.saveDir+"/%s.root"%fullTag ,"update")

    redo_eventLists = 'write' if args.redo_eventLists else 'read'

    ##
    ##  Common Params amongst tasks
    ##

    results = {}
    pool    = {}
    task_ret = {}
    for task in cfg.taskList:
        pool[task]={}
        results[task] = {}
        task_ret[task] = {}
        makeDir(cfg.saveDir)
        task_func      = cfg.taskFuncs[task]

        print "\n \n Now Running Task: %s -> %s \n \n "%(task, task_func)
        task_ret[task] = task_func( cfg, args )
        #if task == 'draw_plots':
        #    pass
        #elif task == "limit_calc":
        #    pass 
        #else:
        #    task_func = getattr(cfg,task,None)
        #    if not task_func:
        #        raise Exception("Config has no function attribute ( cfg.{task} ) for the user defined task {task})".format(task=task))
        #    else:


            #if getattr(cfg,"do_effMap", True):
            #    from Workspace.HEPHYPythonTools.xsecSMS import stop13TeV_NLONLL
            #    eff_map, yld_map = yields[cutName].getSignalEffMap( xsecs = stop13TeV_NLONLL )  
   
                 
    
