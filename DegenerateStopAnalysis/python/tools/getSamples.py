import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks
from Workspace.DegenerateStopAnalysis.tools.Sample import Sample, Samples
from Workspace.DegenerateStopAnalysis.tools.colors import colors
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from Workspace.DegenerateStopAnalysis.tools.weights import Weight , Weights
#from Workspace.DegenerateStopAnalysis.tools.weights_pu2_btag import weights, def_weights, Weight
import os
import re
import glob
import pprint as pp
#-------------------------


#skim='presel'


lumis = { 
            'target_lumi'         :   10000.   ,   
            'DataBlind_lumi'      :   12864.4  , 
            'DataUnblind_lumi'    :   4303.0    ,
        }

data_triggers_list = [
                         'HLT_PFMET100_PFMHT100_IDTight',
                         'HLT_PFMET110_PFMHT110_IDTight',  
                         'HLT_PFMET120_PFMHT120_IDTight',  
                         'HLT_PFMET90_PFMHT90_IDTight',
                     ]

data_mu_trigger = "HLT_IsoMu24"
data_el_trigger = "HLT_Ele27_WPTight_Gsf"

###Filters###
data_filters_list = [
                        'Flag_HBHENoiseFilter',
                        'Flag_HBHENoiseIsoFilter',
                        'Flag_EcalDeadCellTriggerPrimitiveFilter',
                        'Flag_goodVertices',
                        'Flag_eeBadScFilter',
                        'Flag_globalTightHalo2016Filter',
                        'Flag_badChargedHadronFilter',
                        'Flag_badMuonFilter',
                    ]

mc_filters_list = [
                      'Flag_badChargedHadronFilter',
                      'Flag_badMuonFilter',
                  ]


mc_filters_list = [ 'Flag_Filters']
data_filters = mc_filters_list 
import pickle
#mass_dict_pickle = "/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/cmgPostProcessing/mass_dict_all.pkl"
#mass_dict_pickle = "/data/nrad/cmgTuples/7412pass2_mAODv2_v6/RunIISpring15MiniAODv2//mass_dict.pkl"
#mass_dict = pickle.load(open(mass_dict_pickle,"r"))


weights_= Weights()
def_weights=weights_.def_weights
weights = weights_.weights


sample_names = {
                    'vv':"VV",
                    'z':r'#Z\rightarrow \nu\nu+jets',
                    'st':'Single top',
                    #'dy':r'#Z/\gamma^{*} \rightarrow \nu\nu+jets',
                    'dy':r'#Z/\gamma^{*} + jets',
                }

sample_names = {
                    "vv":"Diboson",
                    'z' :'ZJetsInv',
                    'st':'ST',
                    'dy':'DYJetsM50',
                }


def getSamples(wtau=False, sampleList=['w','tt','z','sig'], 
               useHT=False, getData=False, blinded=True, scan=True, massPoints=[], skim='preIncLep', cmgPP=None, do8tev=False,
               weights = weights, def_weights = def_weights,
               data_triggers = ' || '.join(data_triggers_list),
               data_filters  = ' && '.join(data_filters_list),  
               data_mu_trigger = data_mu_trigger, 
               data_el_trigger = data_el_trigger, 
               mc_filters    = ' && '.join(mc_filters_list),
               #signal_filters = ''
               kill_low_qcd_ht = False,
               lumis = lumis, 
               ):
   
   if not cmgPP:
      ppsDir = '/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8020_mAODv2_v0/80X_postProcessing_v0/analysisHephy_13TeV_2016_v2_0/step1'
      mc_path     = ppsDir + "/RunIISpring16MiniAODv2_v0"
      data_path   = ppsDir + "/Data2016_v0"
      signal_path = mc_path
      cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)
   
   mc_lumi = cmgPP.lumi
   
   lumis["mc_lumi"]     = mc_lumi
   lumi_data_unblinded  = lumis['DataUnblind_lumi']
   lumi_data_blinded    = lumis['DataBlind_lumi']
   
   sampleDict = {}
   htString = "HT" if useHT else "Inc"
   
   if getData:
      if "74" in cmgPP.data_path:
         MET = getChain(cmgPP.MET_v4[skim])
         sampleDict.update({
               "d":        {'name':"Data2015",         'sample':cmgPP.MET_v4[skim],         'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":"", "filters":"", 'lumi': lumi_data_unblinded, 'cut':""},
               #"dblind":   {'name':"DataBlind",           'sample':cmgPP.MET_v4[skim],      'tree':MET,                 'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":data_triggers, "filters":data_filters, 'lumi': lumi_data_blinded},
            })
      elif "d1mu" in sampleList or "d1muBlind" in sampleList:
         SingleMuDataBlind = getChain(cmgPP.SingleMu_v2[skim],histname='')
         SingleMuDataUnblind  = SingleMuDataBlind#.CopyTree("run<=274240") #instead cut on run # is applied
         sampleDict.update({
               "d1mu":     {'name':"SingleMuDataUnblind", 'sample':cmgPP.SingleMu_v2[skim], 'tree':SingleMuDataUnblind, 'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":data_mu_trigger, "filters":data_filters, 'lumi': lumi_data_unblinded, 'cut':"run<=275073"},
               "d1muBlind":{'name':"SingleMuDataBlind",   'sample':cmgPP.SingleMu_v2[skim], 'tree':SingleMuDataBlind,   'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":data_mu_trigger, "filters":data_filters, 'lumi': lumi_data_blinded},
            })

      elif "d1el" in sampleList or "d1elBlind" in sampleList:
         SingleElDataBlind = getChain(cmgPP.SingleEl_v2[skim],histname='')
         SingleElDataUnblind  = SingleElDataBlind#.CopyTree("run<=274240") #instead cut on run # is applied
         sampleDict.update({
               "d1el":     {'name':"SingleElDataUnblind", 'sample':cmgPP.SingleEl_v2[skim], 'tree':SingleElDataUnblind, 'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":data_el_trigger, "filters":data_filters, 'lumi': lumi_data_unblinded, 'cut':"run<=275073"},
               "d1elBlind":{'name':"SingleElDataBlind",   'sample':cmgPP.SingleEl_v2[skim], 'tree':SingleElDataBlind,   'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":data_el_trigger, "filters":data_filters, 'lumi': lumi_data_blinded},
            })
      else: # "d" in sampleList or "dblind" in sampleList:
         MET = getChain(cmgPP.MET_v2[skim],histname='')
         METDataUnblind  = MET#.CopyTree("run<=274240") #instead cut on run # is applied
         sampleDict.update({
               "d":        {'name':"DataUnblind",         'sample':cmgPP.MET_v2[skim],      'tree':METDataUnblind,      'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":data_triggers, "filters":data_filters, 'lumi': lumi_data_unblinded, 'cut':"run<=275073"},
               "dblind":   {'name':"DataBlind",           'sample':cmgPP.MET_v2[skim],      'tree':MET,                 'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":data_triggers, "filters":data_filters, 'lumi': lumi_data_blinded},
            })

   if "w" in sampleList:
      WJetsSample     = cmgPP.WJetsHT[skim] if useHT else cmgPP.WJetsInc[skim]
      sampleDict.update({
         'w':{'name':'WJets' , 'sample':WJetsSample, 'color':colors['w'], 'isSignal':0, 'isData':0, 'lumi':mc_lumi},
      })
   
   if "tt" in sampleList:
      if useHT:
      #if False:
         TTJetsHTRestChain = getChain(cmgPP.TTJetsHTRest[skim], histname='')
         TTJetsHTRestChain.Add(getChain(cmgPP.TTJetsHTLow[skim], histname=''))
         TTJetsHTRestChain.Add(getChain(cmgPP.TTJetsHTHigh[skim], histname=''))
         sampleDict.update({
            'tt':{'name':'TTJets', 'sample':cmgPP.TTJetsHTRest[skim], 'tree':TTJetsHTRestChain, 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':mc_lumi},
         })
      #else:
      sampleDict.update({
            'ttInc':{'name':'TTJets', 'sample':cmgPP.TTJetsInc[skim], 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':mc_lumi},
         })
   
   if "z" in sampleList:
      sampleDict.update({
         #'z':{'name':'ZJetsInv', 'sample':cmgPP.ZJetsHT[skim], 'color':colors['z'], 'isSignal':0 , 'isData':0, 'lumi':mc_lumi},
         'z':{'name':sample_names['z'], 'sample':cmgPP.ZJetsHT[skim], 'color':colors['z'], 'isSignal':0 , 'isData':0, 'lumi':mc_lumi},
      })
   
   if "qcd" in sampleList:
      if kill_low_qcd_ht:
         print "WARNING: Removing low HT QCD bins:" ,
         pp.pprint([x for x in  cmgPP.QCD[skim]['bins'] if ("200to300" in x or "300to500" in x)])
         cmgPP.QCD[skim]['bins'] = filter(lambda x: not ("200to300" in x or "300to500" in x), cmgPP.QCD[skim]['bins'])    
         print "WARNING: Reducing QCD bins to:", 
         pp.pprint( cmgPP.QCD[skim]['bins'] )
      
      sampleDict.update({
            'qcd':   {'name':'QCD',   'sample':cmgPP.QCD[skim]     , 'color':colors['qcd'],   'isSignal':0 , 'isData':0, 'lumi':mc_lumi},
            'qcdem': {'name':'QCDEM', 'sample':cmgPP.QCDPT_EM[skim], 'color':colors['qcdem'], 'isSignal':0 , 'isData':0, 'lumi':mc_lumi},
      })
   
   if "dy" in sampleList:
      #DYJetsSample = getChain(cmgPP.DYJetsM5to50HT[skim],histname='')
      sampleDict.update({
            'dy':         {'name':sample_names['dy'],       'sample':cmgPP.DYJetsM50HT[skim],    'color':colors['dy'],         'isSignal':0 , 'isData':0, 'lumi':mc_lumi},
            'dy5to50':    {'name':'DYJetsM5to50',    'sample':cmgPP.DYJetsM5to50[skim], 'color':colors['dy5to50'],    'isSignal':0 , 'isData':0, 'lumi':mc_lumi},
            #'dy5to50Inc':{'name':'DYJetsM5to50Inc', 'sample':cmgPP.DYJetsM5to50[skim],   'color':colors['dy5to50Inc'], 'isSignal':0 , 'isData':0, 'lumi':mc_lumi},
            #'dyInv':     {'name':'DYJetsInv',       'sample':cmgPP.DYJetsToNuNu[skim],   'color':colors['dyInv'],      'isSignal':0 , 'isData':0, 'lumi':mc_lumi},
      }) 
   
   if "vv" in sampleList:
      sampleDict.update({
            'vv': {'name':sample_names['vv'], 'sample':cmgPP.VV[skim], 'color':colors['vv'], 'isSignal':0 , 'isData':0, 'lumi':mc_lumi},
   }) 
   
   if any (["st" in samp for samp in sampleList]):
      sampleDict.update({
            'st_tch_lep':{'name':'ST_tch_lep', 'sample':cmgPP.ST_tch_Lep[skim], 'color':colors['st_tch_lep'], 'isSignal':0, 'isData':0, 'lumi':mc_lumi},
            'st_tch':    {'name':'ST_tch',     'sample':cmgPP.ST_tch[skim],     'color':colors['st_tch'],     'isSignal':0, 'isData':0, 'lumi':mc_lumi},
            'st_wch':    {'name':'ST_wch',     'sample':cmgPP.ST_wch[skim],     'color':colors['st_wch'],     'isSignal':0, 'isData':0, 'lumi':mc_lumi},
            'st':        {'name':sample_names['st'],         'sample':cmgPP.ST[skim],         'color':colors['st'],         'isSignal':0, 'isData':0, 'lumi':mc_lumi},
      }) 
   
   if wtau:
      print "Getting the Tau and Non-Tau components of WJets"
      WJetsTauSample = cmgPP.WJetsTauHT[skim] if useHT else cmgPP.WJetsTauInc[skim]
      WJetsNoTauSample = cmgPP.WJetsNoTauHT[skim] if useHT else cmgPP.WJetsNoTauInc[skim]
      sampleDict.update({
          'wtau':  {'name':'WTau%s'%htString,   'sample':WJetsTauSample,   'color':colors['wtau'],   'isSignal':0, 'isData':0, 'lumi':mc_lumi},
          'wnotau':{'name':'WNoTau%s'%htString, 'sample':WJetsNoTauSample, 'color':colors['wnotau'], 'isSignal':0, 'isData':0, 'lumi':mc_lumi}, 
      })
   
   if any( [x in sampleList for x in ["s30", "s30FS","s10FS","s60FS" , "t2tt30FS"]] ):
      sampleDict.update({
         "s30":     {'name':'S300_270',        'sample':cmgPP.T2DegStop_300_270[skim],         'color':colors["s30"],      'isSignal':2 , 'isData':0, 'lumi':mc_lumi},# ,'sumWeights':T2Deg[1], 'xsec':8.51615}, "weight":weights.isrWeight(9.5e-5)
         "s60FS":   {'name':'S300_240Fast',    'sample':cmgPP.T2DegStop_300_240_FastSim[skim], 'color':colors["s60FS"],    'isSignal':2 , 'isData':0, 'lumi':mc_lumi},# ,"weight":"(weight*0.3520)"},#, 'sumWeights':T2Deg[1], 'xsec':8.51615},
         "s30FS":   {'name':'S300_270Fast',    'sample':cmgPP.T2DegStop_300_270_FastSim[skim], 'color':colors["s30FS"],    'isSignal':2 , 'isData':0, 'lumi':mc_lumi},# ,"weight":"(weight*0.2647)"},#, 'sumWeights':T2Deg[1], 'xsec':8.51615},
         "s10FS":   {'name':'S300_290Fast',    'sample':cmgPP.T2DegStop_300_290_FastSim[skim], 'color':colors["s10FS"],    'isSignal':2 , 'isData':0, 'lumi':mc_lumi},# ,"weight":"(weight*0.2546)"},#, 'sumWeights':T2Deg[1], 'xsec':8.51615},
         "t2tt30FS":{'name':'T2tt300_270Fast', 'sample':cmgPP.T2tt_300_270_FastSim[skim],      'color':colors["t2tt30FS"], 'isSignal':2 , 'isData':0, 'lumi':mc_lumi},# ,"weight":"(weight*0.2783)"},#, 'sumWeights':T2Deg[1], 'xsec':8.51615},
      })
   
   if scan:
      icolor = 1
      signal_mass_dicts = cmgPP.signals_info


      for signal_name, signal_info in signal_mass_dicts.items():
            #sampleId              = signal_info['sampleId']
            signal_mass_dict      = signal_info['pkl']
            mass_template         = signal_info['mass_template']
            mass_dict_pickle_file = os.path.join(cmgPP.signal_path, signal_mass_dict)

            if not os.path.isfile(mass_dict_pickle_file) and not massPoints: 
                print '------------------------ skiping' , mass_dict_pickle_file
                #continue
            else:
                mass_dict = pickle.load(file(mass_dict_pickle_file))
                print 'found mass dict', mass_template, mass_dict.keys() 
        
            if not massPoints:
               mstops = range(250,800,25)
               dms = range(10,81,10)
            else:
               mstops = [x[0] for x in massPoints]
               dms = [x[0]-x[1] for x in massPoints]
            
            for mstop in mstops:
               for dm in dms:
                  mlsp = mstop - dm
                  #print cmgPP.__dict__.keys()

                  if '74' in cmgPP.mc_path:
                      s = getattr(cmgPP,"SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp), None )
                      signal_cut  = "(1)"
                      sigPostFix  = "74X"
                  else:
                      #s = getattr(cmgPP,"SMS_T2tt_mStop_%s_mLSP_%s"%(mstop,mlsp), None )
                      s = getattr(cmgPP, mass_template%(mstop,mlsp), None )
                      signal_cut = "Flag_veto_event_fastSimJets"
                      sigPostFix = ""

                  #s = getattr(cmgPP,"SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp))[skim]
                  if s and glob.glob("%s/%s/*.root"%(s[skim]['dir'],s[skim]['name'])):
                     #print signal_info['shortName']
                     #print signal_info['niceName']
                     sampleDict.update({
                        #'s%s_%s'%(mstop,mlsp):{'name':'T2_4bd_%s_%s'%(mstop,mlsp), 'sample':getattr(cmgPP,"SMS_T2tt_mStop_%s_mLSP_%s"%(mstop,mlsp))[skim], 'color':colors['s%s_%s'%(mstop,mlsp)], 'isSignal':1 , 'isData':0, 'lumi':mc_lumi},
                        #'s%s_%s'%(mstop,mlsp):{'name':'T2tt%s_%s_%s'%(sigPostFix, mstop,mlsp), 'sample':s[skim], 'cut':signal_cut , 'color':colors['s%s_%s'%(mstop,mlsp)], 'isSignal':1 , 'isData':0, 'lumi':mc_lumi},
                        signal_info['shortName']%(mstop,mlsp):{'name':signal_info['niceName']%(mstop,mlsp), 'sample':s[skim], 'cut':signal_cut , 'color':colors['%s_%s'%(mstop,mlsp)], 'isSignal':1 , 'isData':0, 'lumi':mc_lumi},
                      })
                  else: 
                      #print "%s/%s/*.root"%(s['dir'],s['name'])
                      print "!!! Sample Not Found:"  , mass_template%(mstop,mlsp)
   
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
                  's8tev%s_%s'%(mstop,mlsp):{'name':name, 'tree':getChain({'file':rootfile, 'name':name}), 'color':icolor, 'isSignal':3, 'isData':0, 'lumi':19700} ,
               })
      
      bkgDir_8tev = "/data/imikulec/monoJetTuples_v8/copy/"
      wjetDir = bkgDir_8tev+"/WJetsHT150v2/"
      wfiles = wjetDir
      sampleDict.update({
         'w8tev':{'name':'WJets8TeV', 'tree':getChain({'file': wjetDir+"/*.root", 'name':"wjets"}), 'color':colors['w'], 'isSignal':0 , 'isData':0, 'lumi':19700}, #'sumWeights':WJets[1] ,'xsec':20508.9*3},
      })
      
      ttjetDir = bkgDir_8tev+"/TTJetsPowHeg/"
      sampleDict.update({
         'tt8tev':{'name':'TTJets8TeV', 'tree':getChain({'file':ttjetDir+"/*.root", 'name':"ttjets"}), 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':19700},
      })
   
   sampleDict2 = {}
   #def_weights.update({'lumis':lumis})

   for samp in sampleDict:
      
      #if weights.has_key(samp):
      #   sampleDict[samp]["weights"] = Weight( weights[samp].weight_dict , def_weights )
      #elif scan and re.match("s\d\d\d_\d\d\d|s\d\d\d_\d\d|",samp).group() and weights.has_key('sigScan'):
      #   if not sampleDict[samp]['isSignal']: 
      #      assert False, "ISR weight was going to be applied to a non-signal! something is wrong!"
      #   sampleDict[samp]["weights"] = Weight( weights["sigScan"].weight_dict, def_weights)
      #elif do8tev and re.match("s8tev\d\d\d_\d\d\d|s8tev\d\d\d_\d\d|",samp).group():                
      #   sampleDict[samp]["weights"] = weights["sigScan_8tev"]
      #else:
      #   sampleDict[samp]["weights"] = Weight({}, def_weights)
      
      sampleDict2[samp] = Sample(**sampleDict[samp])
   
   samples = Samples(**sampleDict2)
   
   #applying mc_filters
   for samp_name, sample in samples.iteritems():
       if not sample.isData:
          sample.filters = mc_filters
        
   return samples
