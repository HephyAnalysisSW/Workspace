import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.tools.Sample import Sample, Samples
from Workspace.DegenerateStopAnalysis.tools.colors import colors
#import Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_mAODv2_scan as cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
#import Workspace.DegenerateStopAnalysis.weights as weights
from Workspace.DegenerateStopAnalysis.tools.weights import weights , def_weights , Weight
import os
import re
import glob
import pprint as pp
#-------------------------


#skim='presel'


lumis = { 
            #'mc_lumi':10000, 
            #'lumi_data_blinded':2245.386, 
            #'lumi_data_unblinded':139.63,
            'target_lumi'           :   2300.   ,   
            'DataBlind_lumi'      :   3990    , 
            'DataUnblind_lumi'    :   804.2   ,
        }



import pickle
#mass_dict_pickle = "/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/cmgPostProcessing/mass_dict_all.pkl"
#mass_dict_pickle = "/data/nrad/cmgTuples/7412pass2_mAODv2_v6/RunIISpring15MiniAODv2//mass_dict.pkl"
#mass_dict = pickle.load(open(mass_dict_pickle,"r"))



def getSamples( wtau  = False, sampleList=['w','tt','z','sig'], 
                useHT = False, getData = False, blinded=True, scan=True, massPoints=[] , skim='skimPresel', cmgPP=None, do8tev=False,
                weights = weights, def_weights = def_weights,
                data_triggers = 'HLT_PFMET100_PFMHT100_IDTight || HLT_PFMET110_PFMHT110_IDTight || HLT_PFMET120_PFMHT120_IDTight || HLT_PFMET90_PFMHT90_IDTight' , 
                data_filters  = "",  
                #mc_lumi=10000, lumi_data_blinded=2245.386, lumi_data_unblinded=139.63):
                kill_low_qcd_ht = True,
                lumis = lumis , 
                #lumi_target=lumis["lumi_target"], lumi_data_blinded=lumis['lumi_data_blinded'], lumi_data_unblinded=lumis['lumi_data_unblinded']):
               ):

    if not cmgPP:
        sample_path = '/afs/hephy.at/data/vghete02/cmgTuples/postProcessed_mAODv2/8011_mAODv2_v0/80X_postProcessing_v1/analysisHephy_13TeV_2016_v0/step1/'
        mc_path = sample_path +"/RunIISpring16MiniAODv2_v0/"
        signal_path =sample_path +"/RunIISpring16MiniAODv2_v0/"
        data_path =  sample_path +"/Data2016_v0/"

        cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)

    mc_lumi = cmgPP.lumi

    lumis["mc_lumi"]= mc_lumi
    lumi_data_unblinded = lumis['DataUnblind_lumi']
    lumi_data_blinded   = lumis['DataBlind_lumi']



    #data_filters  = ""
    #data_triggers = 'HLT_PFMET100_PFMHT100_IDTight || HLT_PFMET110_PFMHT110_IDTight || HLT_PFMET120_PFMHT120_IDTight || HLT_PFMET90_PFMHT90_IDTight'


    sampleDict = {}
    htString = "HT" if useHT else "Inc"
    if any( [x in sampleList for x in ["s30", "s30FS","s10FS","s60FS" , "t2tt30FS"]] ):
        sampleDict.update({
              "s30":            {'sample': cmgPP.T2DegStop_300_270[skim]                ,'name':'S300_270'        ,'color':colors["s30"     ]             , 'isSignal':2 ,'isData':0    ,"lumi":mc_lumi      },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },  "weight":weights.isrWeight(9.5e-5)
              "s60FS":          {'sample': cmgPP.T2DegStop_300_240_FastSim[skim]        ,'name':'S300_240Fast'      ,'color':colors["s60FS"   ]           , 'isSignal':2 ,'isData':0    ,"lumi":mc_lumi   ,"triggers":""   ,"filters":""  },  # ,"weight":"(weight*0.3520)"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
              "s30FS":          {'sample': cmgPP.T2DegStop_300_270_FastSim[skim]        ,'name':'S300_270Fast'      ,'color':colors["s30FS"   ]           , 'isSignal':2 ,'isData':0    ,"lumi":mc_lumi   ,"triggers":""   ,"filters":""  },  # ,"weight":"(weight*0.2647)"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
              "s10FS":          {'sample': cmgPP.T2DegStop_300_290_FastSim[skim]        ,'name':'S300_290Fast'      ,'color':colors["s10FS"   ]           , 'isSignal':2 ,'isData':0    ,"lumi":mc_lumi   ,"triggers":""   ,"filters":""  },  # ,"weight":"(weight*0.2546)"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
              "t2tt30FS":       {'sample': cmgPP.T2tt_300_270_FastSim[skim]             ,'name':'T2tt300_270Fast'   ,'color':colors["t2tt30FS"]           , 'isSignal':2 ,'isData':0    ,"lumi":mc_lumi   ,"triggers":""   ,"filters":""  },  # ,"weight":"(weight*0.2783)"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
                          })
    if "w" in sampleList:
        WJetsSample     = cmgPP.WJetsHT[skim] if useHT else cmgPP.WJetsInc[skim]
        sampleDict.update({
              'w':              {'sample':WJetsSample         ,'name':'WJets'           ,'color':colors['w']           , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
                            })
    if "z" in sampleList:
        sampleDict.update({
              'z':              {'sample':cmgPP.ZJetsHT[skim]         ,'name':'ZJetsInv'     ,'color':colors['z']              , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
                        })

    if "tt" in sampleList:

        if useHT:
            TTJetsHTRestChain    = getChain( cmgPP.TTJetsHTRest[skim], histname='')
            TTJetsHTRestChain.Add(  getChain( cmgPP.TTJetsHTLow[skim], histname='') )
            TTJetsHTRestChain.Add(  getChain( cmgPP.TTJetsHTHigh[skim], histname='') )
            sampleDict.update({
                  'tt':             {'tree':TTJetsHTRestChain    , 'sample':cmgPP.TTJetsHTRest[skim]      ,'name':'TTJets'  ,'color':colors['tt']            , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
                            })
        else:
            sampleDict.update({
                  'tt':             {'sample':cmgPP.TTJetsInc[skim]       ,'name':'TTJets'  ,'color':colors['tt']            , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
                            })

    if "qcd" in sampleList:
        if kill_low_qcd_ht:
            print "WARNING:     REMOVING QCD BINS:" ,
            pp.pprint([x for x in  cmgPP.QCD[skim]['bins'] if ("200to300" in x or "300to500" in x ) ] )
            cmgPP.QCD[skim]['bins'] = filter(lambda x: not ("200to300" in x or "300to500" in x ) , cmgPP.QCD[skim]['bins'] )    
            print "WARNING:     REDUCING QCD BINS TO:" , 
            pp.pprint( cmgPP.QCD[skim]['bins'] )
        sampleDict.update({
              'qcd':             {'sample':cmgPP.QCD[skim]            ,'name':'QCD'  ,'color':colors['qcd']            , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
              'qcdem':             {'sample':cmgPP.QCDPT_EM[skim]     ,'name':'QCD'  ,'color':colors['qcdem']            , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
              #'qcd':             {'sample':cmgPP.QCD[skim]            ,'name':'QCD'  ,'color':colors['qcd']            , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
                        })
    if getData:
        if blinded:
          MET    = getChain(cmgPP.MET_v2[skim],histname='')
          METDataUnblind  = MET.CopyTree("run<=274240")
          sampleDict.update( {
              "d":              {'tree':METDataUnblind       ,"sample":cmgPP.MET_v2[skim]   ,'name':"DataUnblind"      , 'color':ROOT.kBlack             , 'isSignal':0 ,'isData':1    ,"triggers":data_triggers   ,"filters":data_filters    ,'lumi': lumi_data_unblinded  },
              "dblind":         {       "sample":cmgPP.MET_v2[skim]      ,'name':"DataBlind" , 'color':ROOT.kBlack          , 'isSignal':0 ,'isData':1              ,"triggers":data_triggers   ,"filters":data_filters    ,'lumi': lumi_data_blinded  },
                })
        else:
            assert False

    if "dy" in sampleList:
        DYJetsSample        = getChain(cmgPP.DYJetsM5to50HT[skim],histname='')
        sampleDict.update({
              'dy':                {'sample':cmgPP.DYJetsM50HT[skim]             ,'name':'DYJetsM50'        ,'color':colors['dy']            , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
              'dy5to50':           {'sample':cmgPP.DYJetsM5to50HT[skim]          ,'name':'DYJetsM5to50'     ,'color':colors['dy5to50']            , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
              'dy5to50Inc':        {'sample':cmgPP.DYJetsM5to50[skim]            ,'name':'DYJetsM5to50Inc'  ,'color':colors['dy5to50Inc']            , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
              'dyInv':             {'sample':cmgPP.DYJetsToNuNu[skim]            ,'name':'DYJetsInv'        ,'color':colors['dyInv']            , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
                        }) 
    if wtau:
        print "Getting the Tau and Non-Tau components of WJets"
        WJetsTauSample       = cmgPP.WJetsTauHT[skim] if useHT else cmgPP.WJetsTauInc[skim]
        WJetsNoTauSample     = cmgPP.WJetsNoTauHT[skim] if useHT else cmgPP.WJetsNoTauInc[skim]
        sampleDict.update({
            'wtau':            {'sample':WJetsTauSample        ,'name':'WTau%s'%htString          ,'color':colors['wtau']          , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      } ,
            'wnotau':          {'sample':WJetsNoTauSample       ,'name':'WNoTau%s'%htString        ,'color':colors['wnotau']          , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      }, 
            })

    if scan:
        icolor = 1
        if not massPoints:
            mstops = range(100,601,25)
            dms  = range(10,81,10)
        else:
            mstops = [ x[0] for x in massPoints ]
            dms  = [ x[0]-x[1] for x in massPoints ]

        for mstop in mstops:
            for dm in dms:
                mlsp = mstop - dm
                s = getattr(cmgPP,"SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp))[skim]
                if glob.glob(  "%s/%s/*.root"%(s['dir'],s['name'] ) ):
                    sampleDict.update({
                             's%s_%s'%(mstop,mlsp):      {'sample':getattr(cmgPP,"SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp))[skim]        ,'name':'T2_4bd_%s_%s'%(mstop,mlsp)         ,'color': colors['s%s_%s'%(mstop,mlsp)]        , 'isSignal':1 ,'isData':0    ,"lumi":mc_lumi      } ,
                                            })
                else:
                    print "!!! Sample Not Found: %s, %s"%(mstop,mlsp)
    if do8tev:
        sampleDir_8tev = "/data/imikulec/monoJetTuples_v8/copyfiltered/"
        get8TevSample = lambda mstop, mlsp : sampleDir_8tev  +"/"+"T2DegStop_{mstop}_{mlsp}/histo_T2DegStop_{mstop}_{mlsp}.root".format(mstop=mstop, mlsp=mlsp)
        icolor = 1
        for mstop in mass_dict:
            for mlsp in mass_dict[mstop]:
                        name = "T2Deg8TeV_%s_%s"%(mstop,mlsp)
                        rootfile = get8TevSample(mstop,mlsp)
                        if os.path.isfile( rootfile):
                            sampleDict.update({
                                 's8tev%s_%s'%(mstop,mlsp):      {'tree': getChain({'file': rootfile, 'name':name})       ,'name':name    ,'color': icolor         , 'isSignal':3 ,'isData':0    ,"lumi":19700      } ,
                                               })

        bkgDir_8tev = "/data/imikulec/monoJetTuples_v8/copy/"
        wjetDir = bkgDir_8tev+"/WJetsHT150v2/"
        wfiles = wjetDir
        sampleDict.update({
              'w8tev':              {'tree': getChain({'file': wjetDir+"/*.root", 'name':"wjets"} )       ,'name':'WJets8TeV'           ,'color':colors['w']           , 'isSignal':0 ,'isData':0    ,"lumi":19700      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
                            })
    
        ttjetDir = bkgDir_8tev+"/TTJetsPowHeg/"
        sampleDict.update({
              'tt8tev':             {'tree': getChain({'file': ttjetDir+"/*.root", 'name':"ttjets"} )    , 'name':'TTJets8TeV'           ,'color':colors['tt']            , 'isSignal':0 ,'isData':0    ,"lumi":19700      },
                         })
    sampleDict2 = {}
    def_weights.update({'lumis':lumis})
    for samp in sampleDict:
        if weights.has_key(samp):
            sampleDict[samp]["weights"]  = Weight( weights[samp].weight_dict , def_weights )
        elif scan and re.match("s\d\d\d_\d\d\d|s\d\d\d_\d\d|",samp).group():
            sampleDict[samp]["weights"] = weights["sigScan"]
        elif do8tev and re.match("s8tev\d\d\d_\d\d\d|s8tev\d\d\d_\d\d|",samp).group():                
            sampleDict[samp]["weights"] = weights["sigScan_8tev"]
        else:
            sampleDict[samp]["weights"] = Weight({}, def_weights)

        sampleDict2[samp] = Sample(**sampleDict[samp])
    samples = Samples(**sampleDict2)
    return samples


