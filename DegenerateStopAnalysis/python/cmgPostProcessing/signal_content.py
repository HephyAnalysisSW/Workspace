import ROOT
import pickle
import os
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
import Workspace.HEPHYPythonTools.xsecSMS as xsecSMS

import pickle

dos={
      "get_sig_info":True,
      "get_chains":False,
    }


#signal_name = "SMS_TChipmWW"
signal_name = "SMS_TChiWZ_ZToLL"
signal_name = "SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1"
signal_name = "SMS_T2tt_dM_10to80_genHT_160_genMET_80"
signal_name = "SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1"

#getGenFilterEff = True

#import Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISpring16MiniAODv2_v3 as cmgTuples_v3

import Workspace.DegenerateStopAnalysis.samples.cmgTuples.MC_8020_mAODv2_OldJetClean_v2 as cmgTuplesOldJetClean

#import Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISpring16MiniAODv2_v0 as cmgTuples
#import Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISpring16MiniAODv2_v5 as cmgTuples
import Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISummer16MiniAODv2_v7 as cmgTuples
import Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISummer16MiniAODv2_v7_1 as cmgTuples

#genFilterEff_file = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/filterEfficiency/T2tt_dM_10to80_genHT160_genMET80/filterEffs_genHT160_genMET80.pkl'
genFilterEff_file = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/filterEfficiency/{sample}/filterEffs_{sample}.pkl'

for comp in cmgTuples.allComponents:
    if comp.get("getChain"):
        comp.pop("getChain")


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
            #'SMS_T2tt_dM_10to80_genHT_160_genMET_80':
            #        {
            #            'xsec'        : xsecSMS.stop13TeV_NLONLL,
            #            'genFilterEff': genFilterEff_file,
            #            'cmgTuple'    : cmgTuplesOldJetClean,
            #            'samples'     : [ cmgTuplesOldJetClean.SMS_T2tt_dM_10to80_genHT_160_genMET_80 ] ,
            #            'massVars'    : [
            #                                {'var':'GenSusyMStop', 'name':'mstop'},
            #                                {'var':'GenSusyMNeutralino', 'name':'mlsp'},
            #                            ]
            #        },
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
                                            {'var':'GenSusyMStop', 'name':'mstop'},
                                            {'var':'GenSusyMNeutralino', 'name':'mlsp'},
                                        ]
                    },
            #'SMS_TChipmWW':
            #        {
            #            'xsec'        : xsecSMS.c1c1_13TeV_NLONLL ,
            #            'cmgTuple'    : cmgTuples_v3_1,
            #            'samples'     : [cmgTuples_v3_1.SMS_TChipmWW],
            #            'massVars'    : [
            #                                {'var':'GenSusyMChargino', 'name':'mchi'},
            #                                {'var':'GenSusyMNeutralino', 'name':'mlsp'},
            #                            ]
            #        },
            #'SMS_TChiWZ_ZToLL':
            #        {
            #            'xsec'        : xsecSMS.c1n2_13TeV_NLONLL,
            #            'cmgTuple'    : cmgTuples_v3_1,
            #            'samples'     : [cmgTuples_v3_1.SMS_TChiWZ_ZToLL],
            #            'massVars'    : [
            #                                {'var':'GenSusyMChargino', 'name':'mchi'},
            #                                {'var':'GenSusyMNeutralino', 'name':'mlsp'},
            #                            ]
            #        }
        }


signal_info = signals[signal_name]
samples = signal_info['samples']
massVar1     = signal_info['massVars'][0]['var']
massVar1name = signal_info['massVars'][0]['name']
massVar2     = signal_info['massVars'][1]['var']
massVar2name = signal_info['massVars'][1]['name']
xsecs        = signal_info['xsec']

getGenFilterEff = signal_info.has_key("genFilterEff")

if getGenFilterEff:
    genFilterEff_path = os.path.expandvars(genFilterEff_file.format(sample=signal_name))
    if os.path.isfile(genFilterEff_path):
       genFilterEff = pickle.load(open(genFilterEff_path)) 
    else:
        raise Exception("cannot find gen filter file! %s"%genFilterEff_path)
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


output_dir = signal_info['cmgTuple'].sample_path

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
                def_dict = {"nEvents":0, "xSec":  xsecs[mstop]  }
                def_dict2= {"nEvents":0, "xSec":  xsecs[mstop] , "samples": set() }
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


if __name__ == "__main__":

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
