import os

from Workspace.DegenerateStopAnalysis.tools.TaskConfig import TaskConfig

## Specific cuts and weights for this config file
#from cuts import cuts


import Workspace.DegenerateStopAnalysis.tools.cfgFunctions as cfgFunctions
from Workspace.DegenerateStopAnalysis.tools.massPoints import MassPoints
from Workspace.DegenerateStopAnalysis.tools.degCuts_var import Cuts
CutVars = Cuts
from Workspace.DegenerateStopAnalysis.tools.degCuts import Cuts
from Workspace.DegenerateStopAnalysis.tools.degPlots import DegPlots
from Workspace.DegenerateStopAnalysis.scripts.degStop import args


#import Workspace.DegenerateStopAnalysis.tools.weights_pu as weights_pu
#import Workspace.DegenerateStopAnalysis.tools.weights_pu_teff as weights_pu_teff
#import Workspace.DegenerateStopAnalysis.tools.weights_pu2 as weights_pu2
#import Workspace.DegenerateStopAnalysis.tools.weights_wpt as weights_wpt
#import Workspace.DegenerateStopAnalysis.tools.weights_pu_wpt as weights_pu_wpt
#import Workspace.DegenerateStopAnalysis.tools.weights_pu_ttpt as weights_pu_ttpt
#import Workspace.DegenerateStopAnalysis.tools.weights_base as weights_base
from Workspace.DegenerateStopAnalysis.tools.weights import Weights
#import weights import weights_base

from copy import deepcopy

dmOpt = "allDM"
massPoints = MassPoints(dmOpt)
massPointsFull = MassPoints(dmOpt, (250,801,25))





bkgList = [ 'vv',  'qcd', 'st', 'z','dy', 'tt', 'w' ]
#bkgList = [  'w' ]
#bkgList = [ 'vv', 'qcd', 'st', 'dy', 'tt', 'w'  ]
#sigList = ['s60FS', 's30FS', 's10FS' , 's30']
#bkgList = ['vv']
#sigList = [ ] 
sigOpt = getattr(args,"sigOpt")

if sigOpt.lower() =='bm':
    sigList = ['s300_270','s300_220', 's300_290']
    #sigList = [ 's800_790', 's800_720','s800_750']
elif sigOpt.lower() == 'all': 
    sigList = massPointsFull.sigList
elif sigOpt.lower() == 'nosig':
    sigList = []
else:
    massPointsFull = MassPoints(dmOpt, (750,801,25))
    sigList = massPointsFull.sigList
    #sigList = [ 's800_790', 's800_720','s800_750']
print "Signal Opt: ", sigOpt
print "Signals to be used:", sigList
#signalList    = massPoints.sigList 
#mstop_lsps = massPoints.mstop_lsps
# 
#signalListFull  = massPointsFull.sigList
#mstop_lspsFull  = massPointsFull.mstop_lsps



#plotMStopLSPs   = [ (300,270), (300,290), (300,220)]
#plotSignalList  = ["s%s_%s"%(x[0],x[1]) for x in plotMStopLSPs]


plotMStopLSPs = []
plotSignalList = sigList



#sampleList = ['tt']

print args






lepCol = getattr( args, "lepCol", "LepAll")
lep    = getattr( args, "lep", "lep")

lepTag = lepCol+"_" + lep

btag   = getattr( args, 'btag', 'btag')

sr1c_opts = [ 
                "Reload" ,               #0 
                "MT95" ,                 #1   
                "MT95_IncCharge",        #2   
                "MT105_IncCharge_CT250"  #3       
            ]

sr1c_opt = sr1c_opts[2]


cuts     = Cuts(lepCol, lep, sr1c_opt = sr1c_opt, isrpt=100, btag = btag )

jc='jec_central'
cutvars = CutVars(lepCol, lep, sr1c_opt = sr1c_opt, isrpt=100, btag = btag , jc = jc)

jet_corrs=[ 'jec_up'         ,'jec_central'    ,'jec_down'       ,'jer_up'          ,'jer_central'     ,'jer_down'        ]

jet_corr_srs={}
jet_corr_cuts={}
for jet_corr in jet_corrs:
    jet_corr_cuts[jet_corr] = CutVars( lepCol, lep, sr1c_opt = sr1c_opt, isrpt=100, btag = btag , jc = jet_corr)
    #jet_corr_srs[jet_corr]  = jet_corr_cuts[jet_corr].srs_ptbin_sum
    jet_corr_srs[jet_corr]  = jet_corr_cuts[jet_corr].bins_sum
jet_corr_srs['central'] = cuts.bins_sum

#jet_corr_srs['central'] = cuts.srs_ptbin_sum

jet_corr_cutinsts = [ x for x in jet_corr_srs.itervalues()]

print jet_corr_cutinsts

met_vars = ['met','gen']
met_var_srs      =  {}
met_var_cuts     =  {}
for met_var  in met_vars:
    met_var_cuts[met_var] = CutVars( lepCol, lep, sr1c_opt = sr1c_opt, isrpt=100, btag = btag, jc='', met=met_var)  
    met_var_srs[met_var]  = met_var_cuts[met_var].bins_sum
met_var_cutinsts = [ x for x in met_var_srs.itervalues()]

plots = DegPlots( lepCol, lep)

limitCuts = cuts.bins 
plotCuts  = [ cuts.presel, cuts.sr1IncCharge , cuts.cr1IncCharge , cuts.sr1, cuts.cr1] #cuts.sr1, cuts.sr2, cuts.sr1a, cuts.sr1b, cuts.sr1c, cuts.cr1, cuts.cr2, cuts.crtt2 ]
flowCuts  = [ cuts.cutflow ]

crCuts = [ cuts.crs ] 

#bPlots = ["nBJets", "bJetPt", "bSoftJetPt", "bHardJetPt"]



tasks_info =  {
            'limits10fb':    {'taskList' : [ 'calc_sig_limit' ]  , 'sigList':  massPointsFull.sigList , 'massPoints':   massPointsFull.mstop_lsps   , 'cutInstList':  limitCuts    ,'plotList':plots.plots.keys()  , 'lumi_target' : 10000 }   ,
            'explimits':     {'taskList' : [ 'calc_sig_limit' ]  ,  'sigList':  massPointsFull.sigList , 'massPoints':   massPointsFull.mstop_lsps   , 'cutInstList':  limitCuts         ,'plotList':plots.plots.keys()                   },
            'bkg_est':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                        , 'cutInstList':  crCuts            ,'plotList':plots.plots.keys()           , 'data': True        },


            'met_var':     {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                      , 'cutInstList':  met_var_cutinsts ,'plotList':plots.plots.keys()              , 'data': True        },
            'met_met':     {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                      , 'cutInstList':  met_var_cutinsts[0:1] ,'plotList':plots.plots.keys()              , 'data': True        },
            'met_gen':     {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                      , 'cutInstList':  met_var_cutinsts[1:2] ,'plotList':plots.plots.keys()              , 'data': True        },
    

            'jec_est':     {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                       , 'cutInstList':  jet_corr_cutinsts ,'plotList':plots.plots.keys()              , 'data': False        },
            'jec_est1':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                      , 'cutInstList':  jet_corr_cutinsts[0:1],'plotList':plots.plots.keys()           , 'data': False        },
            'jec_est2':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                      , 'cutInstList':  jet_corr_cutinsts[1:2],'plotList':plots.plots.keys()           , 'data': False        },
            'jec_est3':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                      , 'cutInstList':  jet_corr_cutinsts[2:3],'plotList':plots.plots.keys()           , 'data': False        },
            'jec_est4':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                      , 'cutInstList':  jet_corr_cutinsts[3:4],'plotList':plots.plots.keys()           , 'data': False        },
            'jec_est5':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                      , 'cutInstList':  jet_corr_cutinsts[4:5],'plotList':plots.plots.keys()           , 'data': False        },
            'jec_est6':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                      , 'cutInstList':  jet_corr_cutinsts[5:6],'plotList':plots.plots.keys()           , 'data': False        },
            'jec_est7':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                      , 'cutInstList':  jet_corr_cutinsts[6:7],'plotList':plots.plots.keys()           , 'data': False        },

            'bkg_est_sr':    {'taskList' : [ 'bkg_est' ]  ,         'sigList': plotSignalList    , 'massPoints':   []                   , 'cutInstList':  cuts.srs_ptbin_sum     ,'plotList':plots.plots.keys()           , 'data': True        },

            'plots':     {'taskList' : [ 'draw_plots'  ]     , 'sigList':  plotSignalList     , 'massPoints':   plotMStopLSPs           , 'cutInstList':  plotCuts[:]       ,'plotList':plots.plots.keys()[:]                },
            'cutflow':   {'taskList' : [ 'cut_flow' ]        , 'sigList':  plotSignalList     , 'massPoints':   plotMStopLSPs           , 'cutInstList':  flowCuts          ,'plotList':plots.plots.keys()[:]             },
            'data':      {'taskList' : [ 'data_plots' ]      , 'sigList':  plotSignalList     , 'massPoints':   plotMStopLSPs           , 'cutInstList':  plotCuts[:]       ,'plotList': plots.plots.keys()[:]   , 'data':True},
            'limits2':    {'taskList' : [ 'calc_sig_limit' ]  , 'sigList':  massPoints.sigList , 'massPoints':   massPoints.mstop_lsps   , 'cutInstList':  limitCuts        ,'plotList':plots.plots.keys()[:]         , 'data':True},
              }
#task = 'cutflow'
#task = 'limits10fb'
#task = 'plots'
#task = 'data'
#task = 'limits'

task = getattr( args, "task", "data")
task_info=tasks_info[task]

sampleList = bkgList + task_info['sigList']
#ppTag = "74X_postProcessing_v4"

ppSets = [
            ( "80X_postProcessing_v10" , "nrad01"   , '8012_mAODv2_v3'),
            ( "80X_postProcessing_v9" , "nrad01"   , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v8" , "nrad01"   , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v6" , "nrad01"   , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v7" , "nrad01"   , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v5" , "mzarucki01"   , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v4" , "nrad01"       , '8011_mAODv2_v1'),
            ( "80X_postProcessing_v3" , "nrad01"       , '8011_mAODv2_v1'),
         ]

ppSet  = 0 
ppTag  = ppSets[ppSet][0]
ppUser = ppSets[ppSet][1]
cmgTag = ppSets[ppSet][2]



def make_match_func(tothis):
    def match_func(x):
        ##      should use search instead, and then replace to make things less messy!
        ##      re.search( ".*%s"%(tothis.replace("(","\(").replace(")","\)").replace("*","\*")), x )
        ##
        return re.match( ".*%s"%(tothis.replace("(","\(").replace(")","\)").replace("*","\*")), x )
    return match_func



#from Workspace.DegenerateStopAnalysis.tools.btag_sf_map import BTagSFMap
#
#sf = 'sf' if btag=='btag' else btag
#
#btag_sf_map = BTagSFMap(sf)
#btag_to_sf = btag_sf_map.btag_to_sf
#sf_to_btag = btag_sf_map.sf_to_btag
#
#import re
#def_weights = {
#
#            "cuts": dict( [ (sf, (sf, make_match_func(sf))  )  for sf in sf_to_btag.keys()  ]) , 
#            "baseWeight":"puReweight*weight",
#            #"baseWeight":"puWeight2*weight",
#                }



lumis=              {
                            "mc_lumi"               :   10000   ,
                            'target_lumi'           :   12864.0   ,
                            'DataBlind_lumi'        :   12864.4    ,
                            'DataUnblind_lumi'      :   4303.0  ,
                    }


print "arg cut:", getattr(args, "cutInst", "False")
cutInstList = [] 
if hasattr(args,"cutInst") and args.cutInst:
    for cutInstName in args.cutInst:
        if hasattr(cuts, cutInstName):
            cutInstList.append( getattr(cuts,cutInstName))
        else:
            print args.cut ,"was not found as a attribute of cuts"
            cutInstList = task_info['cutInstList']
else:
    cutInstList = task_info['cutInstList']

plotList = []
if getattr(args,"plot",[]):
    for p in args.plot:
        if hasattr(plots.plots, p):
            plotList.append( p )
        else:
            print "Skipping plot: %s , not found in %s"%(p, plots.plots.keys() )
else:
    plotList = task_info['plotList']




#if hasattr(args,"plot") and args.plot:
#    if plots.plots.has_key( args.plot ):
#        plotList = [ args.plot ]
#    else:
#        print args.plot ,"was not found as a attribute of plots keys", plots.plots.keys()
#        plotList = task_info['plotList']
#else:
#    plotList    = task_info['plotList']






data_filters_list = [
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_goodVertices",
                        "Flag_eeBadScFilter",
                        "Flag_globalTightHalo2016Filter",
                        "Flag_badChargedHadronFilter",
                        "Flag_badMuonFilter",
                    ]
mc_filters_list   = [
                        "Flag_badChargedHadronFilter",
                        "Flag_badMuonFilter",
                    ]




#weights = {
#            'base': weights_base,
#            'pu_teff':   weights_pu_teff,
#            'pu':   weights_pu,
#            'pu2':   weights_pu2,
#            'wpt':  weights_wpt, 
#            'pu_wpt': weights_pu_wpt,
#            'pu_ttpt': weights_pu_ttpt,
#          }


weights_params = {
            'pu_teff':   {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':'puReweight'     , 'btag':btag, 'wpt':'', 'ttpt':'', 'isr':''},
            'pu':        {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':'puReweight'     , 'btag':btag, 'wpt':'', 'ttpt':'', 'isr':''},
            'pu_up':     {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':'puReweight_up'  , 'btag':btag, 'wpt':'', 'ttpt':'', 'isr':''},
            'pu_down':   {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':'puReweight_down', 'btag':btag, 'wpt':'', 'ttpt':'', 'isr':''},
            'wpt':       {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':''               , 'btag':btag, 'wpt':'wpt', 'ttpt':'', 'isr':''},
            'pu_wpt':    {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':'puReweight'     , 'btag':btag, 'wpt':'wpt', 'ttpt':'', 'isr':''},
            'pu_ttpt':   {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':'puReweight'     , 'btag':btag, 'wpt':'', 'ttpt':'ttpt', 'isr':''},
            'pu_noisr':    {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':'puReweight'     , 'btag':btag, 'wpt':'', 'ttpt':'', 'isr':'noisr'},

            'nopu':        {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':''    , 'btag':btag, 'wpt':'', 'ttpt':'', 'isr':''},
            'nopu_teff':   {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':''    , 'btag':btag, 'wpt':'', 'ttpt':'', 'isr':''},
            'nopu':        {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':''    , 'btag':btag, 'wpt':'', 'ttpt':'', 'isr':''},
            'nopu_noisr':  {'lumis':lumis  ,'lepCol':lepCol, 'lep':lep, 'pu':''    , 'btag':btag, 'wpt':'', 'ttpt':'', 'isr':'noisr'},

          }





lhe_weights = {
                0:  {'muR': 'central'     ,'muF':  'central'          } ,        ## <weight id="1001"> muR=1 muF=1 
                1:  {'muR': 'central'     ,'muF':  'up'               } ,        ## <weight id="1002"> muR=1 muF=2 
                2:  {'muR': 'central'     ,'muF':  'down'             } ,        ## <weight id="1003"> muR=1 muF=0.5 
                3:  {'muR': 'up'          ,'muF':  'central'          } ,        ## <weight id="1004"> muR=2 muF=1 
                4:  {'muR': 'up'          ,'muF':  'up'               } ,        ## <weight id="1005"> muR=2 muF=2 
                5:  {'muR': 'up'          ,'muF':  'down'             } ,        ## <weight id="1006"> muR=2 muF=0.5 
                6:  {'muR': 'down'        ,'muF':  'central'          } ,        ## <weight id="1007"> muR=0.5 muF=1 
                7:  {'muR': 'down'        ,'muF':  'up'               } ,        ## <weight id="1008"> muR=0.5 muF=2 
                8:  {'muR': 'down'        ,'muF':  'down'             } ,        ## <weight id="1009"> muR=0.5 muF=0.5 
              }

for lhe_weight_num, muR_muF in lhe_weights.iteritems():
    weights_param  = deepcopy(weights_params['pu'])
    weights_param['lhe'] = lhe_weight_num
    k = "pu_Q2" + muR_muF['muR'] + muR_muF['muF']
    weights_params[k] = weights_param

print weights_params



weight = getattr(args , "weight", "base") 
weight_tag = '' if weight == 'base' else "_%s"%weight


weight_params = weights_params[weight]
#weights_ = Weights(**weight_params)
task_weight = Weights(**weight_params)

#overalTag   = "SUS_16_031_v1"




cfg = TaskConfig(
                   runTag         =  os.path.basename(os.path.dirname(os.path.realpath(__file__)) ) + "_"  + sr1c_opt.title()  + "_"+lepTag + weight_tag + ( "_%s"%btag.upper() ),   ## should be the same as the name of the directory that the cfg is in
                   taskList       =  task_info['taskList'],
                   ppTag          =  ppTag , 
                   ppStep         =  'step1',    ## step1 for mva
                   ppUser         =  ppUser , 
                   cmgTag         =  cmgTag , 
                   #saveDirBase   =  "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2_v6/Studies_v1/" ,
                   saveDirBase    =  "%s/www/T2Deg13TeV/%s/%s/SUS_16_031_v1/"%(os.path.expandvars("$HOME"), cmgTag, ppTag) ,
                   #saveDirBase    =  "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/%s/%s/Studies_v0_puWeight_wptrwgt/"%(cmgTag, ppTag) ,
                   #saveDirBase    =  "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/%s/%s/Studies_v0_puWeight_wptrwgt/"%(cmgTag, ppTag) ,
                   cutInst        =  cutInstList,
                   plots          =  plots.plots         , 
                   plotList       =  plotList, 
                   nminus1s       =  plots.nminus1s, 
                   calc_sig_limit =  cfgFunctions.calc_sig_limit , 
                   cut_flow       =  cfgFunctions.cut_flow       ,
                   data_plots     =  cfgFunctions.data_plots , 
                   bkg_est        =  cfgFunctions.bkg_est , 
                   signalList     =  task_info['sigList']          ,
                   bkgList        =  bkgList , 
                
                   sys_pkl        =  "/data/nrad/results/systs/8TeVSysts.json"              ,
                   sample_info    =  {
                                        "sampleList"   :    sampleList  ,
                                        "wtau"         :    False       , 
                                        "useHT"        :    True        , 
                                        "skim"         :    'preIncLep', 
                                        "kill_low_qcd_ht":  False       ,
                                        "scan"         :    len(sigList)>0       ,
                                        #"massPoints"   :    task_info['massPoints']  ,
                                        "getData"      :    task_info.get("data",False)    ,
                                        "weights"      :    task_weight.weights     ,
                                        "def_weights"  :    task_weight.def_weights     ,
                                        "data_triggers":    'HLT_PFMET100_PFMHT100_IDTight || HLT_PFMET110_PFMHT110_IDTight || HLT_PFMET120_PFMHT120_IDTight || HLT_PFMET90_PFMHT90_IDTight'                ,
                                        "data_filters" :    ' && '.join(data_filters_list), 
                                        "mc_filters"   :    ' && '.join(mc_filters_list),
                                        'lumis'        :     task_weight.def_weights['lumis'],
                                      } , 
                   lumi_info       = task_weight.def_weights['lumis'],
                   #lumi_info      = task_info.get("lumi_info",{}),
                   nProc          =  15, 
                )

cfg.cuts = cuts
#cfg.cutvars = cutvars
cfg.met_var_srs  = met_var_srs
cfg.jet_corr_srs = jet_corr_srs

print "............................................"
print ""
print "RunTag:"  , cfg.runTag
print "Tasks:"   , cfg.taskList
print "sample tags:"   , ppUser, cmgTag, ppTag
print "cutInstList:"   , cutInstList
print "plotList:"      , plotList
print ""
print "............................................"






#tasks = [cfg, ]  submit multiple tasks TO BE IMPLEMENTED

