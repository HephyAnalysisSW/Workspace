# getSamples.py

import os, sys
import re
import glob
import pprint as pp
import pickle
import ROOT

from Workspace.HEPHYPythonTools.helpers import getChain
from Workspace.DegenerateStopAnalysis.tools.colors import colors
from Workspace.DegenerateStopAnalysis.samples.Sample import Sample, Samples
from Workspace.DegenerateStopAnalysis.samples.samplesInfo import getCutWeightOptions, lumis, triggers, filters, sample_names, dataset_dict, dataset_info

cutWeightOptions = getCutWeightOptions()

def makeDataSample(eras, sample, tree, triggers, filters, settings = cutWeightOptions['settings'], dataset_dict = dataset_dict, niceName = None):

    eras = sorted(eras) 
    eras_name    = "".join(eras)
    if not niceName:
        niceName = "Data" + eras_name
    
    run_cut_list = []

    for era in eras:
        run_cut = "(run >= %s && run <= %s)"%dataset_dict[settings['year']][settings['dataset']][settings['campaign']][era]['runs']
        run_cut_list.append(run_cut)

    run_cuts = "(%s)"%(" || ".join(run_cut_list))

    total_lumi = sum([dataset_dict[settings['year']][settings['dataset']][settings['campaign']][era]['lumi'] for era in eras])

    data = {
     'name'     : niceName,
     'year'     : settings['year'],
     'campaign' : settings['campaign'],
     'sample'   : sample,
     'tree'     : tree,
     'color'    : ROOT.kBlack,
     'isSignal' : 0 ,
     'isData'   : 1,
     "triggers" : triggers,
     "filters"  : filters,
     'lumi'     : total_lumi,
     'cut'      : run_cuts,
     'dir'      : sample['dir']
    }

    return data, {niceName:total_lumi}
         
def getSamples(wtau=False, sampleList=['w','tt','z','sig'], 
               useHT=False, getData=False, blinded=True, scan=True, massPoints=[], skim='skimPresel', PP=None, do8tev=False,
               triggers = triggers,
               mc_filters   = filters, 
               data_filters = filters, 
               kill_low_qcd_ht = False,
               applyMCTriggers = False, # "data_met",
               settings = cutWeightOptions['settings'],
               ):
    
    if not PP:
       print "PP not specified. Exiting."
       sys.exit()
   
    year = settings['year']
    lumis = settings['lumis']
    lumis["lumi_norm"] = PP.lumi
    
    htString = "HT" if useHT else "Inc"
    
    sampleDict = {}
    
    if getData:
        dataset  = settings['dataset']
        campaign = settings['campaign']

        if campaign:
            dataset_name = "%s_Run%s_%s"%(dataset, year, campaign)
        else:    
            dataset_name = dataset

        dataPP = getattr(PP, dataset_name)[skim]
        dataTree= getChain(dataPP, histname='')
    
        sampleDict.update({
              dataset_name:{'name':dataset_name, 'sample':dataPP, 'tree':dataTree, 'color':ROOT.kBlack, 'isSignal':0 , 'isData':1, "triggers":triggers[dataset], "filters":data_filters, 'lumi': lumis[year][dataset_name]}
           })

    if settings['year'] in dataset_dict:
        for shortName, data_sets, names in dataset_info[dataset]:
            d, l = makeDataSample(data_sets, dataPP, dataTree, triggers[dataset], data_filters, settings = settings, niceName = names['niceName'])
            sampleDict.update({shortName:d})
            lumis[year].update(l)
    
    if "w" in sampleList or any([x.startswith("w") for x in sampleList]):
       if "w_lo" in sampleList and hasattr(PP, "WJets_LO"):
              sampleDict.update({
                 'w_lo'  :{'name':'WJets_LO',   'sample':PP.WJets_LO[skim], 'color':colors['w']   , 'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]}
              })
    
       elif "w_nlo" in sampleList and hasattr(PP, "WJets_NLO"):
              sampleDict.update({
                 'w_nlo' :{'name':'WJets_NLO',  'sample':PP.WJets_NLO[skim], 'color':colors['w']   , 'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]}
              })
    
       elif useHT:
          WJetsSample     = PP.WJetsHT[skim]
          sampleDict.update({
             'w'     :{'name':sample_names['w']['shortName'],      'sample':WJetsSample, 'color':colors['w']   , 'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]},
             'wtau'  :{'name':'WJetsTau',   'sample':WJetsSample, 'color':colors['wtau'], 'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"] ,'cut':"Sum$(abs(GenPart_pdgId)==15)"},
             'wnotau':{'name':'WJetsNoTau', 'sample':WJetsSample, 'color':colors['wnotau'], 'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"] ,'cut':"Sum$(abs(GenPart_pdgId)==15)==0"},
          })
          
          wxsecs = [
                    1627.449951171875,
                    435.23699951171875,
                    59.18109893798828,
                    14.580499649047852,
                    6.656209945678711,
                    1.6080900430679321,
                    0.03891360014677048,
                   ]
    
          wxsecs.sort(reverse=True)
          
          if False:
             for ihtbin , xsec in enumerate(wxsecs,1):
               xseccut = "abs(xsec-%s)<1E-5"%xsec
               sampleDict['w%s'%ihtbin]={'name':'WJetsHT%s'%ihtbin, 'cut':xseccut   ,  'sample':WJetsSample, 'color':colors['w%s'%ihtbin]   , 'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]}
    
       else:
          WJetsSample     = PP.WJetsPt[skim] # PP.WJets_LO[skim] PP.WJetsInc[skim]
          sampleDict.update({
             'w_pt'     :{'name':'WJets',      'sample':WJetsSample, 'color':colors['w']   , 'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]},
          })
       
    if "tt" in sampleList or 'tt_pow' in sampleList or 'tt_1l' in sampleList or 'tt_2l' in sampleList:
       #if useHT:
       if False:
          TTJetsHTRestChain = getChain(PP.TTJetsHTRest[skim], histname='')
          TTJetsHTRestChain.Add(getChain(PP.TTJetsHTLow[skim], histname=''))
          TTJetsHTRestChain.Add(getChain(PP.TTJetsHTHigh[skim], histname=''))
          sampleDict.update({
             'tt':{'name':'TTJets', 'sample':PP.TTJetsHTRest[skim], 'tree':TTJetsHTRestChain, 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
          })
       #else:
       #if hasattr(PP, "TT_pow"):
       #   sampleDict.update({
       #         #'tt':{'name':'TTJets', 'sample':PP.TTJetsInc[skim], 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
       #         'tt_pow':{'name':'TT_pow', 'sample':PP.TT_pow[skim], 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
       #      })
       
       splitTT = True
    
       if splitTT:
          sampleDict.update({
                #'tt':{'name':'TTJets', 'sample':PP.TTJetsInc[skim], 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
                'tt_1l':{'name':sample_names['tt_1l']['shortName'], 'sample':PP.TTJets_SingleLepton[skim], 'color':colors['tt'] + 1, 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
                'tt_2l':{'name':sample_names['tt_2l']['shortName'], 'sample':PP.TTJets_DiLepton[skim],    'color':colors['tt'] - 3, 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
             })
       
          #TT splitting based on gen
          #
          #semiLep = "(Sum$((abs(GenPart_pdgId) == 13 || abs(GenPart_pdgId) == 11) && GenPart_isPromptHard) < 2)"
          #diLep =   "(Sum$((abs(GenPart_pdgId) == 13 || abs(GenPart_pdgId) == 11) && GenPart_isPromptHard) == 2)"
          #
          #sampleDict.update({ 
          #      'tt_1l':{'name':'TT_1l', 'sample':PP.TTJetsHTRest[skim], 'tree':TTJetsHTRestChain.Clone(), 'color':colors['tt'] + 2, 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"], 'cut': semiLep}, # NOTE: includes 0l # cloning tree is required 
          #      'tt_2l':{'name':'TT_2l', 'sample':PP.TTJetsHTRest[skim], 'tree':TTJetsHTRestChain.Clone(), 'color':colors['tt'] + 4, 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"], 'cut': diLep}, # cloning tree is required
          #   })
          #sampleDict.update({
       #      'ttInc_FS':{'name':'TTJets_FastSim', 'sample':PP.TTJetsInc_FS[skim], 'color':ROOT.kViolet+10, 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
       #   })
    
    if "z" in sampleList:
       sampleDict.update({
          'z':{'name':sample_names['z']['shortName'], 'sample':PP.ZJetsHT[skim], 'color':colors['z'], 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
       })
    
    if "qcd" in sampleList:
       if kill_low_qcd_ht:
          print "WARNING: Removing low HT QCD bins:" ,
          pp.pprint([x for x in  PP.QCD[skim]['bins'] if ("200to300" in x or "300to500" in x)])
          PP.QCD[skim]['bins'] = filter(lambda x: not ("200to300" in x or "300to500" in x), PP.QCD[skim]['bins'])    
          print "WARNING: Reducing QCD bins to:", 
          pp.pprint( PP.QCD[skim]['bins'] )
       
       sampleDict.update({
             'qcd':   {'name':sample_names['qcd']['shortName'],   'sample':PP.QCD[skim]     , 'color':colors['qcd'],   'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
       })
    
    if "dy" in sampleList or "dy5to50" in sampleList:
       #DYJetsSample = getChain(PP.DYJetsM5to50HT[skim],histname='')
       sampleDict.update({
             'dy':         {'name':sample_names['dy']['shortName'], 'sample':PP.DYJetsM50HT[skim],    'color':colors['dy'],         'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
             'dy5to50':    {'name':sample_names['dy5to50']['shortName'],     'sample':PP.DYJetsM5to50[skim], 'color':colors['dy5to50'],    'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
             #'dy5to50Inc':{'name':'DYJetsM5to50Inc',  'sample':PP.DYJetsM5to50[skim],   'color':colors['dy5to50Inc'], 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
             #'dyInv':     {'name':'DYJetsInv',        'sample':PP.DYJetsToNuNu[skim],   'color':colors['dyInv'],      'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
       }) 
    
    if "vv" in sampleList:
       sampleDict.update({
             'vv': {'name':sample_names['vv']['shortName'], 'sample':PP.VV[skim], 'color':colors['vv'], 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
    }) 
    
    if "ttx" in sampleList:
       sampleDict.update({
             'ttx': {'name':sample_names['ttx']['shortName'], 'sample':PP.TTX[skim], 'color':colors['ttx'], 'isSignal':0 , 'isData':0, 'lumi':lumis["lumi_norm"]},
    }) 
    
    if any (["st" in samp for samp in sampleList]):
       sampleDict.update({
             #'st_tch_lep':{'name':'ST_tch_lep',       'sample':PP.ST_tch_Lep[skim], 'color':colors['st_tch_lep'], 'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]},
             #'st_tch':    {'name':'ST_tch',           'sample':PP.ST_tch[skim],     'color':colors['st_tch'],     'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]},
             #'st_wch':    {'name':'ST_wch',           'sample':PP.ST_wch[skim],     'color':colors['st_wch'],     'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]},
             'st':        {'name':sample_names['st']['shortName'], 'sample':PP.ST[skim],         'color':colors['st'],         'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]},
             #'st_tch_lep':{'name':'ST_tch_lep',       'sample':PP.ST_tch_Lep[skim], 'color':colors['st_tch_lep'], 'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]},
       }) 
    
    if wtau:
       print "Getting the Tau and Non-Tau components of WJets"
       WJetsTauSample = PP.WJetsTauHT[skim] if useHT else PP.WJetsTauInc[skim]
       WJetsNoTauSample = PP.WJetsNoTauHT[skim] if useHT else PP.WJetsNoTauInc[skim]
       sampleDict.update({
           'wtau':  {'name':'WTau%s'%htString,   'sample':WJetsTauSample,   'color':colors['wtau'],   'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]},
           'wnotau':{'name':'WNoTau%s'%htString, 'sample':WJetsNoTauSample, 'color':colors['wnotau'], 'isSignal':0, 'isData':0, 'lumi':lumis["lumi_norm"]}, 
       })
    
    if any( [x in sampleList for x in ["s30", "s30FS","s10FS","s60FS" , "t2tt30FS"]] ):
       sampleDict.update({
          "s30":     {'name':'S300_270',        'sample':PP.T2DegStop_300_270[skim],         'color':colors["s30"],      'isSignal':2 , 'isData':0, 'lumi':lumis["lumi_norm"]},
          "s60FS":   {'name':'S300_240Fast',    'sample':PP.T2DegStop_300_240_FastSim[skim], 'color':colors["s60FS"],    'isSignal':2 , 'isData':0, 'lumi':lumis["lumi_norm"]},
          "s30FS":   {'name':'S300_270Fast',    'sample':PP.T2DegStop_300_270_FastSim[skim], 'color':colors["s30FS"],    'isSignal':2 , 'isData':0, 'lumi':lumis["lumi_norm"]},
          "s10FS":   {'name':'S300_290Fast',    'sample':PP.T2DegStop_300_290_FastSim[skim], 'color':colors["s10FS"],    'isSignal':2 , 'isData':0, 'lumi':lumis["lumi_norm"]},
          "t2tt30FS":{'name':'T2tt300_270Fast', 'sample':PP.T2tt_300_270_FastSim[skim],      'color':colors["t2tt30FS"], 'isSignal':2 , 'isData':0, 'lumi':lumis["lumi_norm"]},
       })
    
    # FullSim Signal Points 
    if any([x for x in sampleList if 'FullSim' in x]):
       sampleDict.update({
          "FullSim_275_205":{'name':'S275_205', 'sample':PP.SMS_T2_4bd_275_205_FullSim[skim], 'color':colors["s30"],   'isSignal':3 , 'isData':0, 'lumi':lumis["lumi_norm"]},
          "FullSim_350_330":{'name':'S350_330', 'sample':PP.SMS_T2_4bd_350_330_FullSim[skim], 'color':colors["s30FS"], 'isSignal':3 , 'isData':0, 'lumi':lumis["lumi_norm"]},
          "FullSim_400_350":{'name':'S400_350', 'sample':PP.SMS_T2_4bd_400_350_FullSim[skim], 'color':colors["s60FS"], 'isSignal':3 , 'isData':0, 'lumi':lumis["lumi_norm"]},
       })
          
       if 'allFullSim' in sampleList:
          allFullSim = getChain(PP.SMS_T2_4bd_275_205_FullSim[skim], histname='')
          allFullSim.Add(getChain(PP.SMS_T2_4bd_350_330_FullSim[skim], histname=''))
          allFullSim.Add(getChain(PP.SMS_T2_4bd_400_350_FullSim[skim], histname=''))
    
          sampleDict.update({
             'allFullSim':{'name':'allFullSim', 'sample':None, 'tree':allFullSim, 'color':colors['s30'], 'isSignal':3 , 'isData':0, 'lumi':lumis["lumi_norm"]},
          })
    
    if scan:
        
       icolor = 1
       signals_info = PP.signals_info
    
       for signal_name, signal_info in signals_info.items():
             #sampleId              = signal_info['scanId']
             signal_mass_dict      = signal_info['pkl']
             mass_template         = signal_info['mass_template']
             mass_dict_pickle_file = signal_info['mass_dict']
    
             if not os.path.isfile(mass_dict_pickle_file) and not massPoints: 
                 print 'No mass dict %s file found'%mass_dict_pickle_file
                 continue
             else:
                 mass_dict = pickle.load(file(mass_dict_pickle_file))
                 print 'Found mass dict', signal_name, mass_dict.keys() 
         
             mstops_mlsps_dict = {} 
             if not massPoints:
                mstops = mass_dict.keys()
                for mstop in mstops:
                   mstops_mlsps_dict[mstop] = mass_dict[mstop].keys()  
             else:
                mstops = [x[0] for x in massPoints]
    
                for mstop in mstops:
                    mstops_mlsps_dict[mstop] = [] 
                for x in massPoints:
                    mstops_mlsps_dict[x[0]].append(x[1]) 
             
             for mstop in mstops:
                mlsps = mstops_mlsps_dict[mstop]
    
                for mlsp in mlsps:
    
                   if '74' in PP.mc_path:
                       s = getattr(PP,"SMS_T2_4bd_mStop_%s_mLSP_%s"%(mstop,mlsp), None )
                       signal_cut  = "(1)"
                       sigPostFix  = "74X"
                   else:
                       #s = getattr(PP,"SMS_T2tt_mStop_%s_mLSP_%s"%(mstop,mlsp), None )
                       s = getattr(PP, mass_template%(mstop,mlsp), None )
                       signal_cut = "Flag_veto_event_fastSimJets"
                       sigPostFix = ""
                   
                   if s and glob.glob("%s/%s/*.root"%(s[skim]['dir'],s[skim]['name'])):
                       sampleDict.update({
                          signal_info['shortName']%(mstop,mlsp):{'name':signal_info['niceName']%(mstop,mlsp), 'sample':s[skim], 'cut':signal_cut , 'color':colors['%s_%s'%(mstop,mlsp)], 'isSignal':1 , 'isData':0, 'lumi':lumis["lumi_norm"]},
                        })
                   else: 
                       print "!!! Sample %s not found !!!"%mass_template%(mstop,mlsp)
       
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
          'w8tev':{'name':'WJets8TeV', 'tree':getChain({'file': wjetDir+"/*.root", 'name':"wjets"}), 'color':colors['w'], 'isSignal':0 , 'isData':0, 'lumi':19700},
       })
       
       ttjetDir = bkgDir_8tev+"/TTJetsPowHeg/"
       sampleDict.update({
          'tt8tev':{'name':'TTJets8TeV', 'tree':getChain({'file':ttjetDir+"/*.root", 'name':"ttjets"}), 'color':colors['tt'], 'isSignal':0 , 'isData':0, 'lumi':19700},
       })
    
    sampleDict2 = {}
    
    for samp in sampleDict:
       sampleDict2[samp] = Sample(**sampleDict[samp])
    
    samples = Samples(**sampleDict2)
    
    #applying filters
    for samp_name, sample in samples.iteritems():
        if not sample.isData:
           sample.filters = mc_filters 
        if applyMCTriggers and not sample.isData and not sample.isSignal:
           sample.triggers = triggers[applyMCTriggers] 
          
    return samples
