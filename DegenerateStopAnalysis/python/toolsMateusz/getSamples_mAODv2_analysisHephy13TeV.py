#getSamples_mAODv2_analysisHephy13TeV.py

import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.tools.Sample import Sample, Samples
from Workspace.DegenerateStopAnalysis.tools.colors import colors
from Workspace.DegenerateStopAnalysis.toolsMateusz.cmgTuplesPostProcessed_mAODv2_analysisHephy13TeV import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.tools.weights import weights, def_weights, Weight

#import Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_mAODv2_scan as cmgTuplesPostProcessed
import os
import re
import glob
#-------------------------

lumis = { 
            #'lumi_mc':10000, 
            'lumi_target':2300., 
            'lumi_data_blinded':2245.386, 
            'lumi_data_unblinded':139.63,
        }

print makeLine()
for l in lumis: print l, ": ", lumis[l]
print makeLine()

import pickle
#mass_dict_pickle = "/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/cmgPostProcessing/mass_dict_all.pkl"
#mass_dict_pickle = "/data/nrad/cmgTuples/7412pass2_mAODv2_v6/RunIISpring15MiniAODv2//mass_dict.pkl"
#mass_dict = pickle.load(open(mass_dict_pickle,"r"))



def getSamples( wtau  = False, sampleList=['w','tt','z','sig'], 
                useHT = False, getData = False, blinded=True, scan=True, skim='presel', cmgPP=None, do8tev=False,
                weights = weights, def_weights = def_weights,
                #data_triggers = , data_flags = ,  
                #lumi_mc=10000, lumi_data_blinded=2245.386, lumi_data_unblinded=139.63):
                lumi_target=lumis["lumi_target"], lumi_data_blinded=lumis['lumi_data_blinded'], lumi_data_unblinded=lumis['lumi_data_unblinded']):

    #if not cmgPP:
    #    mc_path     = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/RunIISpring15DR74_25ns"
    #    signal_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/RunIISpring15DR74_25ns"
    #    data_path   = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/Data_25ns"
    #    cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)



    lumi_mc = cmgPP.lumi

    #data_filters = '((\
    #            Flag_EcalDeadCellTriggerPrimitiveFilter) &&\
    #            (Flag_trkPOG_manystripclus53X) &&\
    #             (Flag_trkPOG_logErrorTooManyClusters) &&\
    #             (Flag_trkPOGFilters) && (Flag_ecalLaserCorrFilter) &&\
    #             (Flag_trkPOG_toomanystripclus53X) &&\
    #             (Flag_hcalLaserEventFilter) &&\
    #             (Flag_CSCTightHaloFilter) &&\
    #             (Flag_HBHENoiseFilter) &&\
    #             (Flag_HBHENoiseIsoFilter) &&\
    #             (Flag_goodVertices) &&\
    #             (Flag_METFilters) &&\
    #             (Flag_eeBadScFilter))'

    data_filters = "Flag_METFilters && Flag_Veto_Event_List"
    data_triggers_MET = "HLT_PFMET90_PFMHT90_IDTight" #"HLT_PFMET170_JetIdCleaned"
    data_triggers_Mu = "HLT_IsoMu27"

    sampleDict = {}
    htString = "HT" if useHT else "Inc"
    if any( [x in sampleList for x in ["s30", "s30FS","s10FS","s60FS" , "t2tt30FS"]] ):
        sampleDict.update({
              "s30":            {'sample': cmgPP.T2DegStop_300_270[skim]                ,'name':'S300_270'        ,'color':colors["s30"     ]             , 'isSignal':2 ,'isData':0    ,"lumi":lumi_mc      },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },  "weight":weights.isrWeight(9.5e-5)
              "s60FS":          {'sample': cmgPP.T2DegStop_300_240_FastSim[skim]        ,'name':'S300_240Fast'      ,'color':colors["s60FS"   ]           , 'isSignal':2 ,'isData':0    ,"lumi":lumi_mc   ,"triggers":""   ,"filters":""  },  # ,"weight":"(weight*0.3520)"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
              "s30FS":          {'sample': cmgPP.T2DegStop_300_270_FastSim[skim]        ,'name':'S300_270Fast'      ,'color':colors["s30FS"   ]           , 'isSignal':2 ,'isData':0    ,"lumi":lumi_mc   ,"triggers":""   ,"filters":""  },  # ,"weight":"(weight*0.2647)"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
              "s10FS":          {'sample': cmgPP.T2DegStop_300_290_FastSim[skim]        ,'name':'S300_290Fast'      ,'color':colors["s10FS"   ]           , 'isSignal':2 ,'isData':0    ,"lumi":lumi_mc   ,"triggers":""   ,"filters":""  },  # ,"weight":"(weight*0.2546)"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
              "t2tt30FS":       {'sample': cmgPP.T2tt_300_270_FastSim[skim]             ,'name':'T2tt300_270Fast'   ,'color':colors["t2tt30FS"]           , 'isSignal':2 ,'isData':0    ,"lumi":lumi_mc   ,"triggers":""   ,"filters":""  },  # ,"weight":"(weight*0.2783)"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
                          })
    if "w" in sampleList:
        WJetsSample     = cmgPP.WJetsHT[skim] if useHT else cmgPP.WJetsInc[skim]
        sampleDict.update({
              #'w':              {'sample':WJetsSample         ,'name':'WJets%s'%htString           ,'color':colors['w']           , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
              'w':              {'sample':WJetsSample         ,'name':'WJets'           ,'color':colors['w']           , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
                            })
        #sampleDict.update({
        #      #'w':              {'sample':WJetsSample         ,'name':'WJets%s'%htString           ,'color':colors['w']           , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
        #      'winc':              {'sample':WJetsInc[skim]         ,'name':'WJets'           ,'color':colors['w']           , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
        #                    })
    if "z" in sampleList:
        sampleDict.update({
              'z':              {'sample':cmgPP.ZJetsHT[skim]         ,'name':'ZJetsInv'     ,'color':colors['z']              , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
                        })

    if "tt" in sampleList:

        if useHT:
            TTJetsHTLowChain    = getChain( cmgPP.TTJetsHTLow[skim], histname='')
            TTJetsHTHighChain    = getChain( cmgPP.TTJetsHTHigh[skim], histname='')
            TTJetsHTRestChain    = getChain( cmgPP.TTJetsHTRest[skim], histname='')
            TTJetsHTRestChain.Add(  TTJetsHTLowChain  )
            TTJetsHTRestChain.Add(  TTJetsHTHighChain )
            
            
            sampleDict.update({
                  'tt':             {'tree':TTJetsHTRestChain    , 'sample':cmgPP.TTJetsHTRest[skim]      ,'name':'TTJets'  ,'color':colors['tt']            , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },
                            })

        else:
            sampleDict.update({
                  'tt':             {'sample':cmgPP.TTJetsInc[skim]       ,'name':'TTJets'  ,'color':colors['tt']            , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },
                            })

    if "qcd" in sampleList:
        sampleDict.update({
              'qcd':             {'sample':cmgPP.QCD[skim]            ,'name':'QCD'  ,'color':colors['qcd']            , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },
              #'qcdem':             {'sample':cmgPP.QCDPT_EM[skim]            ,'name':'QCD'  ,'color':colors['qcdem']            , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },
              #'qcd':             {'sample':cmgPP.QCD[skim]            ,'name':'QCD'  ,'color':colors['qcd']            , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },
                        })

    if "d" in sampleList or "dblind" in sampleList:
      #if blinded:
      METDataOct05    = getChain(cmgPP.MET_Oct05[skim],histname='')
      METDataUnblind  = METDataOct05#.CopyTree("run<=257599")
      METDataBlind    = getChain(cmgPP.MET_v4[skim],histname='')
      METDataBlind.Add(METDataOct05)
      sampleDict.update( {
          "d":              {'tree':METDataUnblind       ,"sample":cmgPP.MET_Oct05[skim]   ,'name':"DataUnblind"      , 'color':ROOT.kBlack             , 'isSignal':0 ,'isData':1    ,"triggers":data_triggers_MET   ,"filters":data_filters    ,'lumi': lumi_data_unblinded, 'cut':"run<=257599"},
          "dblind":         {'tree':METDataBlind         ,"sample":cmgPP.MET_v4[skim]      ,'name':"DataBlind" , 'color':ROOT.kBlack          , 'isSignal':0 ,'isData':1              ,"triggers":data_triggers_MET   ,"filters":data_filters    ,'lumi': lumi_data_blinded  },
            })
      #else: assert False
      
    elif "d1mu" in sampleList or "d1muBlind" in sampleList:
      SingleMuDataOct05    = getChain(cmgPP.SingleMu_Oct05[skim],histname='')
      SingleMuDataUnblind  = SingleMuDataOct05#.CopyTree("run<=257599")
      SingleMuDataBlind    = getChain(cmgPP.SingleMu_v4[skim],histname='')
      SingleMuDataBlind.Add(SingleMuDataOct05)
      sampleDict.update( {
          "d1mu":              {'tree':SingleMuDataUnblind       ,"sample":cmgPP.SingleMu_Oct05[skim]   ,'name':"SingleMuDataUnblind"      , 'color':ROOT.kBlack             , 'isSignal':0 ,'isData':1    ,"triggers":data_triggers_Mu   ,"filters":data_filters    ,'lumi': lumi_data_unblinded, 'cut':"run<=257599"},
          "d1muBlind":         {'tree':SingleMuDataBlind         ,"sample":cmgPP.SingleMu_v4[skim]      ,'name':"SingleMuDataBlind" , 'color':ROOT.kBlack          , 'isSignal':0 ,'isData':1              ,"triggers":data_triggers_Mu   ,"filters":data_filters    ,'lumi': lumi_data_blinded  },
            })

    elif "d1el" in sampleList or "d1elBlind" in sampleList:
      SingleElDataOct05    = getChain(cmgPP.SingleEl_Oct05[skim],histname='')
      SingleElDataUnblind  = SingleElDataOct05#.CopyTree("run<=257599")
      SingleElDataBlind    = getChain(cmgPP.SingleEl_v4[skim],histname='')
      SingleElDataBlind.Add(SingleElDataOct05)
      sampleDict.update( {
          "d1el":              {'tree':SingleElDataUnblind       ,"sample":cmgPP.SingleEl_Oct05[skim]   ,'name':"SingleElDataUnblind"      , 'color':ROOT.kBlack             , 'isSignal':0 ,'isData':1    ,"triggers":data_triggers   ,"filters":data_filters    ,'lumi': lumi_data_unblinded, 'cut':"run<=257599"},
          "d1elBlind":         {'tree':SingleElDataBlind         ,"sample":cmgPP.SingleEl_v4[skim]      ,'name':"SingleElDataBlind" , 'color':ROOT.kBlack          , 'isSignal':0 ,'isData':1              ,"triggers":data_triggers   ,"filters":data_filters    ,'lumi': lumi_data_blinded  },
            })

    if "dy" in sampleList:
        DYJetsSample        = getChain(cmgPP.DYJetsM5to50HT[skim],histname='')
        sampleDict.update({
              #'dy5':               {'sample':cmgPP.DYJetsM5to50HT[skim]          ,'name':'DYJetsM5to50'  ,'color':colors['dy1']            , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },
              'dy50':              {'sample':cmgPP.DYJetsM50HT[skim]             ,'name':'DYJetsM50'  ,'color':colors['dy1']            , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },
              #'dyInv':             {'sample':cmgPP.DYJetsToNuNu[skim]            ,'name':'DYJetsInv'  ,'color':colors['dy1']            , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },
                        }) 

    if wtau:
        print "Getting the Tau and Non-Tau components of WJets"
        WJetsTauSample       = cmgPP.WJetsTauHT[skim] if useHT else cmgPP.WJetsTauInc[skim]
        WJetsNoTauSample     = cmgPP.WJetsNoTauHT[skim] if useHT else cmgPP.WJetsNoTauInc[skim]
        
        sampleDict.update({
            'wtau':            {'sample':WJetsTauSample        ,'name':'WTau%s'%htString          ,'color':colors['wtau']          , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      } ,
            'wnotau':          {'sample':WJetsNoTauSample       ,'name':'WNoTau%s'%htString        ,'color':colors['wnotau']          , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      }, 
            })

    if scan:
        icolor = 1
        #skim = "inc"
        #mass_dict = cmgPP.mass_dict
        #if not mass_dict: 
        #    raise Exception("No mass_dict available... Cannot create samples for mass scan")
        #for mstop in mass_dict:
        for mstop in range(100,601,25):
            #if mstop > 425 : continue
            #for mlsp in mass_dict[mstop]:
            for dm in range(10,81,10):
                mlsp = mstop - dm
                s = getattr(cmgPP,"SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp))[skim]
                if glob.glob(  "%s/%s/*.root"%(s['dir'],s['name'] ) ):
                    sampleDict.update({
                            #'s%s_%s'%(mstop,mlsp):      {'sample':eval("SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp))[skim]        ,'name':'T2_4bd%s_%s'%(mstop,mlsp)          ,'color': icolor         , 'isSignal':1 ,'isData':0    ,"lumi":lumi_mc      } ,
                            #'s%s_%s'%(mstop,mlsp):      {'sample':getattr(cmgPP,"SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp))[skim]        ,'name':'T2_4bd_%s_%s'%(mstop,mlsp)         , "weight":"(weight*(%s))"%weights.isrWeight(9.5e-5) ,'color': icolor         , 'isSignal':1 ,'isData':0    ,"lumi":lumi_mc      } ,
                             's%s_%s'%(mstop,mlsp):      {'sample':getattr(cmgPP,"SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp))[skim]        ,'name':'T2_4bd_%s_%s'%(mstop,mlsp)         ,'color': colors['s%s_%s'%(mstop,mlsp)]        , 'isSignal':1 ,'isData':0    ,"lumi":lumi_mc      } ,
                                            })
                else:
                    print "!!! Sample Not Found: %s, %s"%(mstop,mlsp)
#    if do8tev:
#        sampleDir_8tev = "/data/imikulec/monoJetTuples_v8/copyfiltered/"
#        get8TevSample = lambda mstop, mlsp : sampleDir_8tev  +"/"+"T2DegStop_{mstop}_{mlsp}/histo_T2DegStop_{mstop}_{mlsp}.root".format(mstop=mstop, mlsp=mlsp)
#        icolor = 1
#        #skim = "inc"
#        for mstop in mass_dict:
#            #if mstop > 300 : continue
#            for mlsp in mass_dict[mstop]:
#                        name = "T2Deg8TeV_%s_%s"%(mstop,mlsp)
#                        rootfile = get8TevSample(mstop,mlsp)
#                        if os.path.isfile( rootfile):
#                            sampleDict.update({
#                                 's8tev%s_%s'%(mstop,mlsp):      {'tree': getChain({'file': rootfile, 'name':name})       ,'name':name    ,'color': icolor         , 'isSignal':3 ,'isData':0    ,"lumi":19700      } ,
#                                               })
#
#
#        bkgDir_8tev = "/data/imikulec/monoJetTuples_v8/copy/"
#         
#        wjetDir = bkgDir_8tev+"/WJetsHT150v2/"
#        wfiles = wjetDir
#        sampleDict.update({
#              #'w':              {'sample':WJetsSample         ,'name':'WJets%s'%htString           ,'color':colors['w']           , 'isSignal':0 ,'isData':0    ,"lumi":lumi_mc      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
#              'w8tev':              {'tree': getChain({'file': wjetDir+"/*.root", 'name':"wjets"} )       ,'name':'WJets8TeV'           ,'color':colors['w']           , 'isSignal':0 ,'isData':0    ,"lumi":19700      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
#                            })
#    
#        ttjetDir = bkgDir_8tev+"/TTJetsPowHeg/"
#        sampleDict.update({
#              'tt8tev':             {'tree': getChain({'file': ttjetDir+"/*.root", 'name':"ttjets"} )    , 'name':'TTJets8TeV'           ,'color':colors['tt']            , 'isSignal':0 ,'isData':0    ,"lumi":19700      },
#                         })
    sampleDict2 = {}

    for samp in sampleDict:

        if weights.has_key(samp):
            sampleDict[samp]["weights"]  = weights[samp]
        elif scan and re.match("s\d\d\d_\d\d\d|s\d\d\d_\d\d|",samp).group():
            sampleDict[samp]["weights"] = weights["sigScan"]
        elif do8tev and re.match("s8tev\d\d\d_\d\d\d|s8tev\d\d\d_\d\d|",samp).group():                
            sampleDict[samp]["weights"] = weights["sigScan_8tev"]
        else:
            sampleDict[samp]["weights"] = Weight({}, def_weights)

        sampleDict2[samp] = Sample(**sampleDict[samp])
    samples = Samples(**sampleDict2)
    samples.set_lumis(lumi_target = lumi_target, lumi_data_blinded = lumi_data_blinded, lumi_data_unblinded = lumi_data_unblinded, lumi_mc = lumi_mc)

    #if "dblind" in samples: 
    #  print makeLine()
    #  print "Reweighting MC samples to blinded data luminosity of " + str(lumi_data_blinded) + " with factor: " + str(lumi_data_blinded/lumi_mc)
    #  print makeLine()
    #  samples.addWeight(lumi_data_blinded/lumi_mc) # scale to the target luminosity
    #elif "d" in samples: 
    #  print makeLine()
    #  print "Reweighting MC samples to unblinded data luminosity of " + str(lumi_data_unblinded) + " with factor: " + str(lumi_data_unblinded/lumi_mc)
    #  print makeLine()
    #  samples.addWeight(lumi_data_unblinded/lumi_mc) # scale to the target luminosity
    #else: 
    #  print makeLine()
    #  print "Reweighting to target luminosity of " + str(lumi_target) + " with factor: " + str(lumi_target/lumi_mc)
    #  print makeLine()
    #  samples.addWeight(lumi_target/lumi_mc) # scale to the target luminosity
    

    #samples.addLumiWeight( lumi_target = lumi_target, lumi_base = None , sampleList=[])         ## scale to the target luminosity
    #samples.addWeight( weights.isrWeightFunc(9.5e-5)  , sampleList=samples.privSigList() + samples.massScanList() )   ## apply isrWeight to the massScan

    #if do8tev:
    #    weight_8tev = "puWeight*wpts4X*(1.+7.5e-5*Max$(gpM*(gpPdg==1000006)))*(1.*(ptISR<120.)+0.95*(ptISR>=120.&&ptISR<150.)+0.9*(ptISR>=150.&&ptISR<250.)+0.8*(ptISR>=250.))"
    #    for samp in samples.otherSigList():
    #        samples[samp].weight = weight_8tev
    #        #samples[samp].weight = "(1)"
    #    #samples.addWeight( weight_8tev  , sampleList=samples.otherSigList()  )

    return samples
