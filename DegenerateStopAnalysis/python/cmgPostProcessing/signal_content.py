import ROOT
import pickle
import os
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
import Workspace.HEPHYPythonTools.xsecSMS as xsecSMS
import sys
import pickle
from functools import partial

#from Workspace.DegenerateStopAnalysis.tools.getGauginoXSec import getGauginoXSec, getHiggsinoXSec # FIXME

dos={
      "get_sig_info":True,
      "get_chains":False,
    }

#signal_name = "SMS_TChipmWW"
#signal_name = "SMS_TChiWZ_ZToLL"
#signal_name = "SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1"
#signal_name = "SMS_T2tt_dM_10to80_genHT_160_genMET_80"
#signal_name = "SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1"

import Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISummer16MiniAODv2_v10 as cmgTuples

#genFilterEff_file = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/filterEfficiency/T2tt_dM_10to80_genHT160_genMET80/filterEffs_genHT160_genMET80.pkl'
genFilterEff_file = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/filterEfficiency/{sample}/filterEffs_{sample}.pkl'

for comp in cmgTuples.allComponents:
    if comp.get("getChain"):
        comp.pop("getChain")


readFromDPM = True

if readFromDPM:
    
    from Workspace.DegenerateStopAnalysis.samples.heppy_dpm_samples import heppy_mapper
    cache_file = getattr(cmgTuples, "cache_file")
    if not cache_file:
        #raise Exception("Cache file not found in cmgTuples")
        print "Cache file not found in cmgTuples"
    ## one needs to make sure the proxy is availble at this stage
    from Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISummer16MiniAODv2_v10 import getHeppyMap
    heppySamples = getHeppyMap()
    #heppySamples = heppy_mapper(cmgTuples.allComponents, [], cache_file)
    if not heppySamples.heppy_sample_names:
        print "Something didn't work with the Heppy_sample_mapper.... no samples found"

    samps_to_get  = []

    for samp in cmgTuples.allComponents:
        samps_to_get.append(samp['cmgName'])
        exts = samp.get("ext")
        if exts:
            samps_to_get.extend(exts)

    for sampname in samps_to_get:
        samp_for_dpm = heppySamples.from_heppy_samplename(sampname)
        if not samp_for_dpm:
            print "No HeppyDPMSample was found for %s"%sampname
            print "Should be one of the samples in ", heppySamples.heppy_sample_names
        setattr(cmgTuples, sampname, samp_for_dpm)

    #allComponentsList = [ getattr(cmgTuples, samp['cmgName']) for samp in allComponentsList ]


signals={
            'SMS_T2tt_dM_10to80_genHT_160_genMET_80':
                    {
                        'xsec'        : xsecSMS.stop13TeV_NLONLL,
                        'genFilterEff': genFilterEff_file,
                        'cmgTuple'    : cmgTuples,
                        'samples'     : [ cmgTuples.SMS_T2tt_dM_10to80_genHT_160_genMET_80 ] ,
                        'massVars'    : [
                                            {'var':'GenSusyMStop', 'name':'mstop'},
                                            {'var':'GenSusyMNeutralino', 'name':'mlsp'},
                                        ]
                    },
            'SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1':
                    {
                        'xsec'        : xsecSMS.stop13TeV_NLONLL,
                        'genFilterEff': genFilterEff_file,
                        'cmgTuple'    : cmgTuples,
                        'samples'     : [ cmgTuples.SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1 ] ,
                        'massVars'    : [
                                            {'var':'GenSusyMStop', 'name':'mstop'},
                                            {'var':'GenSusyMNeutralino', 'name':'mlsp'},
                                        ]
                    },
            'SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1':
                    {
                        'xsec'        : xsecSMS.stop13TeV_NLONLL,
                        'genFilterEff': genFilterEff_file,
                        'cmgTuple'    : cmgTuples,
                        'samples'     : [ cmgTuples.SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1 ] ,
                        'massVars'    : [
                                            {'var':'GenSusyMStop'      , 'name':'mstop'},
                                            {'var':'GenSusyMNeutralino', 'name':'mlsp'},
                                        ]
                    },

            # FIXME
            #'SMS_TChiWZ_genHT_160_genMET_80_3p':
            #        {
            #            'xsec'        : partial( getGauginoXSec,"C1N2","wino" ),
            #            #'xsec'        : xsecSMS.stop13TeV_NLONLL,
            #            'genFilterEff': genFilterEff_file,
            #            'cmgTuple'    : cmgTuples,
            #            'samples'     : [ cmgTuples.SMS_TChiWZ_genHT_160_genMET_80_3p] ,
            #            'massVars'    : [
            #                                {'var':'GenSusyMChargino'  , 'name':'mChipm1'},
            #                                {'var':'GenSusyMNeutralino', 'name':'mlsp'},
            #                            ]
            #        },
            #'SMS_N2N1_higgsino_genHT_160_genMET_80_3p':
            #        {
            #            'xsec'        : partial( getGauginoXSec,"N1N2","hino" ),
            #            #'xsec'        : xsecSMS.n2n1_hino_13TeV,
            #            'genFilterEff': genFilterEff_file,
            #            'cmgTuple'    : cmgTuples,
            #            'samples'     : [ cmgTuples.SMS_N2N1_higgsino_genHT_160_genMET_80_3p ] ,
            #            'massVars'    : [
            #                             {'var':'GenSusyMNeutralino2', 'name':'mChi02'},
            #                             {'var':'GenSusyMNeutralino', 'name':'mLSP'},
            #                            ]
            #        },
            #'MSSM_higgsino_genHT_160_genMET_80_3p':
            #        {
            #            'xsec'        : getHiggsinoXSec,
            #            'genFilterEff': genFilterEff_file,
            #            'cmgTuple'    : cmgTuples,
            #            'samples'     : [ cmgTuples.MSSM_higgsino_genHT_160_genMET_80_3p ] ,
            #            'massVars'    : [
            #                             #   {'var':'GenSusyMStop', 'name':'mstop'},
            #                             #   {'var':'GenSusyMNeutralino', 'name':'mlsp'},
            #                            ]
            #        },
            #'SMS_C1N1_higgsino_genHT_160_genMET_80_3p':
            #        {
            #            'xsec'        : partial( getGauginoXSec,"C1N2" , "hino" ),
            #            #'xsec'        : xsecSMS.c1n1_hino_13TeV,
            #            'genFilterEff': genFilterEff_file,
            #            'cmgTuple'    : cmgTuples,
            #            'samples'     : [ cmgTuples.SMS_C1N1_higgsino_genHT_160_genMET_80_3p ] ,
            #            'massVars'    : [
            #                                {'var':'GenSusyMChargino'      , 'name':'mChipm1'},
            #                                {'var':'GenSusyMNeutralino', 'name':'mlsp'},
            #                            ]
            #        },
            #'SMS_C1C1_higgsino_genHT_160_genMET_80_3p':
            #        {
            #            'xsec'        : partial( getGauginoXSec,"C1C1","hino" ),
            #            #'xsec'        : xsecSMS.c1c1_hino_13TeV,
            #            'genFilterEff': genFilterEff_file,
            #            'cmgTuple'    : cmgTuples,
            #            'samples'     : [ cmgTuples.SMS_C1C1_higgsino_genHT_160_genMET_80_3p ] ,
            #            'massVars'    : [
            #                                {'var':'GenSusyMChargino', 'name':'mChipm1'},
            #                                {'var':'GenSusyMNeutralino', 'name':'mlsp'},
            #                            ]
            #        },
            #'SMS_N2C1_higgsino_genHT_160_genMET_80_3p':
            #        {
            #            'xsec'        : partial( getGauginoXSec,"C1N2","hino" ),
            #            'genFilterEff': genFilterEff_file,
            #            'cmgTuple'    : cmgTuples,
            #            'samples'     : [ cmgTuples.SMS_N2C1_higgsino_genHT_160_genMET_80_3p ] ,
            #            'massVars'    : [
            #                              {'var':'GenSusyMNeutralino2'  , 'name':'mChi01'},
            #                              {'var':'GenSusyMChargino'     , 'name':'mlsp'  },
            #                              #{'var':'GenSusyMNeutralino'     , 'name':'mlsp'},
            #                            ]
            #        },
        }


if __name__ == '__main__':
    signal_name = sys.argv[1]
    signal_info = signals[signal_name]
    samples = signal_info['samples']
    massVar1     = signal_info['massVars'][0]['var']
    massVar1name = signal_info['massVars'][0]['name']
    massVar2     = signal_info['massVars'][1]['var']
    massVar2name = signal_info['massVars'][1]['name']
    xsecs        = signal_info['xsec']
        
    output_dir = signal_info['cmgTuple'].sample_path + '/mass_dicts'
    if not os.path.exists(output_dir): os.makedirs(output_dir) 
    
    def getXSec( xsecs, mass):
        if hasattr(xsecs, "__call__"):
            return xsecs(mass)[0]
        else:
            return xsecs[mass]
    
    
    getGenFilterEff = signal_info.has_key("genFilterEff")
    
    if getGenFilterEff:
        genFilterEff_path = os.path.expandvars(genFilterEff_file.format(sample=signal_name))
        if os.path.isfile(genFilterEff_path):
           genFilterEff = pickle.load(open(genFilterEff_path)) 
        else:
            raise Exception("cannot find gen filter file! %s"%genFilterEff_path)
        roundMasses = True
        if roundMasses:
            roundedDict = {}
            print " I will round the masses in the genFilterDictionary!"
            for m1, effs in genFilterEff.iteritems():
                roundedDict[int(round(m1))]={}
                for m2, eff in effs.iteritems():
                    roundedDict[int(round(m1))][int(round(m2))]=eff
    
            genFilterEff = roundedDict
    
    else:
        genFilterEff = None
    
    def tryStopLSP(mass_dict, mstop, mlsp, def_val = 0):
        try:
            mass_dict[mstop]
        except KeyError:
            mass_dict[mstop]={}
        try:
            mass_dict[mstop][mlsp]
        except KeyError:
            mass_dict[mstop][mlsp]=def_val
    
    def getStopLSPInfo(sample):
        sample_name = sample["name"]
        print sample_name
        chunks = getChunks(sample, maxN=-1)
        chunk = chunks[0]
        chain = getChain(chunk, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1, treeName='tree')
        hist_name = "%s_%s_%s"%(massVar1name, massVar2name, sample_name)
        mass_dict_sample={}
        mass_dict={}
        hist = ROOT.TH2D(hist_name, hist_name, 1000,0,1000, 1000 , 0, 1000)
        #chain.Draw("GenSusyMNeutralino:GenSusyMStop>>%s"%hist_name)
        chain.Draw("%s:%s>>%s"%(massVar2, massVar1, hist_name))
        nBinsX = hist.GetNbinsX()
        nBinsY = hist.GetNbinsY()
        for xbin in xrange(nBinsX):
            for ybin in xrange(nBinsY):
                bin_cont = hist.GetBinContent(xbin,ybin)
                if bin_cont > 0.0000001:
                    mstop = xbin -1
                    mlsp = ybin -1
                    print mstop, mlsp, bin_cont
                    def_dict = {"nEvents":0, "xSec":  getXSec( xsecs, mstop )  }
                    def_dict2= {"nEvents":0, "xSec":  getXSec( xsecs, mstop )  , "samples": set() }
                    #def_dict = {"nEvents":0 }
                    #def_dict2= {"nEvents":0, "samples": set() }
                    if genFilterEff: 
                        def_dict['genFilterEff']=genFilterEff[mstop][mlsp] 
                        def_dict2['genFilterEff']=genFilterEff[mstop][mlsp]  
                    tryStopLSP(mass_dict_sample, mstop, mlsp, def_val = def_dict ) 
                    mass_dict_sample[mstop][mlsp]['nEvents'] += bin_cont
                    tryStopLSP(mass_dict, mstop, mlsp, def_val=def_dict2)
                    mass_dict[mstop][mlsp]['samples'].add(sample_name)
                    mass_dict[mstop][mlsp]['nEvents'] += mass_dict_sample[mstop][mlsp]['nEvents']
        return {"sample_name":sample_name, "mass_dict":mass_dict, "mass_dict_sample":mass_dict_sample}
    
    if True:
    
        if dos['get_sig_info']:
            import multiprocessing
            nProc = 10
            pool = multiprocessing.Pool(nProc)
            results = pool.map(getStopLSPInfo , samples)
            pool.close()
            pool.join()
    
            mass_dicts_samples_all={}
            mass_dicts_all={}
            for result in results:
                mass_dicts_samples_all[result['sample_name']] =  result['mass_dict_sample']
                mass_dicts_all.update(result['mass_dict'])
            pickle.dump(mass_dicts_samples_all, open(output_dir +"/%s_mass_dict_samples.pkl"%signal_name,"w") )
            pickle.dump(mass_dicts_all, open(output_dir +"/%s_mass_dict.pkl"%signal_name,"w") )
    
            print "Pickles dumped:",
            print output_dir +"/%s_mass_dict_samples.pkl"%signal_name
            print output_dir +"/%s_mass_dict.pkl"%signal_name
    
        if dos['get_chains']:
            chains={}
            for sample in samples:
                sample_name = sample["name"]
                print sample_name
                chunks = getChunks(sample, maxN=-1)
                chunk = chunks[0]
                chain = getChain(chunk, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1, treeName='tree')
                chains[sample_name]=chain
