import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_mAODv2_7412pass2 import *
from Workspace.DegenerateStopAnalysis.navidTools.Sample import Sample, Samples


#-------------------------


skim='presel'

mc_lumi   = 10000
data_lumi_unblinded = 139.63 #pb-1
data_lumi_blinded = 2245.386 #pb-1  (2.2 fb-1)

data_filters = '((\
                Flag_EcalDeadCellTriggerPrimitiveFilter) &&\
                (Flag_trkPOG_manystripclus53X) &&\
                 (Flag_trkPOG_logErrorTooManyClusters) &&\
                 (Flag_trkPOGFilters) && (Flag_ecalLaserCorrFilter) &&\
                 (Flag_trkPOG_toomanystripclus53X) &&\
                 (Flag_hcalLaserEventFilter) &&\
                 (Flag_CSCTightHaloFilter) &&\
                 (Flag_HBHENoiseFilter) &&\
                 (Flag_HBHENoiseIsoFilter) &&\
                 (Flag_goodVertices) &&\
                 (Flag_METFilters) &&\
                 (Flag_eeBadScFilter))'

#

colors ={
              'w':             ROOT.kSpring-5       , 
              'z':             ROOT.kOrange         ,#ROOT.kSpring+10       
              'tt':            ROOT.kAzure-5        , 
              'qcd':           ROOT.kViolet         , 
              'wtau':          ROOT.kSpring-2       ,
              'wnotau':        ROOT.kSpring+2       ,

              "s30":           ROOT.kRed+1          , 
              "s60FS":         ROOT.kOrange +7      , 
              "s30FS":         ROOT.kYellow -3       , 
              "s10FS":         ROOT.kAzure  +7      , 
              "t2tt30FS":      ROOT.kOrange-1       , 
            }




















def getWTauNoTau(WSample,Dir="/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_v4_012016_v2/RunIISpring15DR74_25ns/"):
    print "Creating a sample for the Tau and NonTau Components of WJets ... this might take some time"
    wtau    = WSample.CopyTree("Sum$(abs(GenPart_pdgId)==15)>=1")
    fWTau   = ROOT.TFile( '%s/wTau.root'%Dir, 'recreate' )
    wtau.Write()
    fWTau.Close() 

    wnotau  =   WSample.CopyTree("Sum$(abs(GenPart_pdgId)==15)==0")
    fWNoTau   = ROOT.TFile( '%s/wNoTau.root'%Dir, 'recreate' )
    wnotau.Write()
    fWNoTau.Close()
    return {'wtau': wtau , 'wnotau':wnotau }


def getSamples(wtau=False,sampleList=['w','tt','z','sig'], useHT=False, getData=False, blinded=True, skim='presel'):
    sampleDict = {}
    htString = "HT" if useHT else "Inc"
    if any( [x in sampleList for x in ["s30", "s30FS","s10FS","s60FS" , "t2tt30FS"]] ):
        sampleDict.update({
              "s30":            {'sample': T2DegStop_300_270[skim]                ,'name':'S300_270'        ,'color':colors["s30"     ]           , 'isSignal':1 ,'isData':0    ,"lumi":mc_lumi      },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
              "s60FS":          {'sample': T2DegStop_300_240_FastSim[skim]        ,'name':'S300_240Fast'      ,'color':colors["s60FS"   ]           , 'isSignal':1 ,'isData':0    ,"lumi":mc_lumi   ,"weight":"(weight*0.3520 )"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
              "s30FS":          {'sample': T2DegStop_300_270_FastSim[skim]        ,'name':'S300_270Fast'      ,'color':colors["s30FS"   ]           , 'isSignal':1 ,'isData':0    ,"lumi":mc_lumi   ,"weight":"(weight*0.2647 )"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
              "s10FS":          {'sample': T2DegStop_300_290_FastSim[skim]        ,'name':'S300_290Fast'      ,'color':colors["s10FS"   ]           , 'isSignal':1 ,'isData':0    ,"lumi":mc_lumi   ,"weight":"(weight*0.2546 )"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
              "t2tt30FS":       {'sample': T2tt_300_270_FastSim[skim]             ,'name':'T2tt300_270Fast'   ,'color':colors["t2tt30FS"]           , 'isSignal':1 ,'isData':0    ,"lumi":mc_lumi   ,"weight":"(weight*0.2783 )"   },# ,'sumWeights':T2Deg[1] ,'xsec':8.51615    },
                          })
    if "w" in sampleList:
        WJetsSample     = WJetsHT[skim] if useHT else WJetsInc[skim]
        sampleDict.update({
              #'w':              {'sample':WJetsSample         ,'name':'WJets%s'%htString           ,'color':colors['w']           , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
              'w':              {'sample':WJetsSample         ,'name':'WJets'           ,'color':colors['w']           , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
                            })
    if "z" in sampleList:
        sampleDict.update({
              'z':              {'sample':ZJetsHT[skim]         ,'name':'ZJetsInv'     ,'color':colors['z']              , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },# ,'sumWeights':WJets[1] ,'xsec':20508.9*3    },
                        })

    if "tt" in sampleList:
        sampleDict.update({
              'tt':             {'sample':TTJetsInc[skim]       ,'name':'TTJets'  ,'color':colors['tt']            , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
                        })

    if "qcd" in sampleList:
        sampleDict.update({
              'qcd':             {'sample':QCD[skim]            ,'name':'QCD'  ,'color':colors['qcd']            , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      },
                        })

    if "d" in sampleList or "dblind" in sampleList:
        if blinded:
          METDataOct05    = getChain(MET_Oct05[skim],histname='')
          METDataUnblind  = METDataOct05.CopyTree("run<=257599")
          METDataBlind    = getChain(MET_v4[skim],histname='')
          METDataBlind.Add(METDataOct05)
          sampleDict.update( {
              "d":     {'tree':METDataUnblind       ,"sample":MET_Oct05[skim]   ,'name':"DataUnblind"      , 'color':ROOT.kBlack            ,"triggers":"", "filters":data_filters     , 'isSignal':0 ,'isData':1    ,"weight":"(1)"  ,'lumi': data_lumi_unblinded  },
              "dblind":              {'tree':METDataBlind         ,"sample":MET_v4[skim]      ,'name':"DataBlind" , 'color':ROOT.kBlack     ,"triggers":"", "filters":data_filters     , 'isSignal':0 ,'isData':1    ,"weight":"(1)"  ,'lumi': data_lumi_blinded  },
                })
        else:
            assert False

    if wtau:
        print "Getting the Tau and Non-Tau components of WJets"
        WJetsTauSample       = WJetsTauHT[skim] if useHT else WJetsTauInc[skim]
        WJetsNoTauSample     = WJetsNoTauHT[skim] if useHT else WJetsNoTauInc[skim]
        
        sampleDict.update({
            'wtau':            {'sample':WJetsTauSample        ,'name':'WTau%s'%htString          ,'color':colors['wtau']          , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      } ,
            'wnotau':          {'sample':WJetsNoTauSample       ,'name':'WNoTau%s'%htString        ,'color':colors['wnotau']          , 'isSignal':0 ,'isData':0    ,"lumi":mc_lumi      }, 
            })
    
    sampleDict2 = {}
    for samp in sampleDict:
      sampleDict2[samp]=Sample(**sampleDict[samp])
    samples = Samples(**sampleDict2)

    return samples


