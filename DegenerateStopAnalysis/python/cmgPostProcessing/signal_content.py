import ROOT
import pickle
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
import Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2_mAODv2_v6 as cmgTuples
from Workspace.HEPHYPythonTools.xsecSMS import *

import pickle

dos={
      "get_sig_info":False,
      "get_chains":True,


    }



samples = [

            cmgTuples.SMS_T2_4bd_mStop_100_mLSP_20to90              ,
            cmgTuples.SMS_T2_4bd_mStop_125_mLSP_45to115             ,
            cmgTuples.SMS_T2_4bd_mStop_150_mLSP_70to140             ,
            cmgTuples.SMS_T2_4bd_mStop_175_mLSP_95to165             ,
            cmgTuples.SMS_T2_4bd_mStop_200_mLSP_120to190            ,
            cmgTuples.SMS_T2_4bd_mStop_225_mLSP_145to225            ,
            cmgTuples.SMS_T2_4bd_mStop_250_mLSP_170to240            ,
            cmgTuples.SMS_T2_4bd_mStop_275_mLSP_195to265            ,
            cmgTuples.SMS_T2_4bd_mStop_300_mLSP_220to290            ,
            cmgTuples.SMS_T2_4bd_mStop_325_mLSP_245to315            ,
            cmgTuples.SMS_T2_4bd_mStop_350_mLSP_270to340            ,
            cmgTuples.SMS_T2_4bd_mStop_375_mLSP_295to365            ,
            cmgTuples.SMS_T2_4bd_mStop_400_mLSP_320to390            ,
            cmgTuples.SMS_T2_4bd_mStop_425to475_mLSP_345to465       ,
            cmgTuples.SMS_T2_4bd_mStop_500to550_mLSP_420to540        ,
            cmgTuples.SMS_T2_4bd_mStop_550to600_mLSP_470to590        ,

        ]


def tryStopLSP(mass_dict, mstop, mlsp, def_val = 0):
    try:
        mass_dict[mstop]
    except KeyError:
        mass_dict[mstop]={}
    try:
        mass_dict[mstop][mlsp]
    except KeyError:
        mass_dict[mstop][mlsp]=def_val


output_dir = cmgTuples.sample_path

def getStopLSPInfo(sample):
    sample_name = sample["name"]
    print sample_name
    chunks = getChunks(sample, maxN=-1)
    chunk = chunks[0]
    chain = getChain(chunk, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1, treeName='tree')
    hist_name = "stop_lsp_%s"%sample_name
    mass_dict_sample={}
    mass_dict={}
    hist = ROOT.TH2D(hist_name, hist_name, 1000,0,1000, 1000 , 0, 1000)
    chain.Draw("GenSusyMNeutralino:GenSusyMStop>>%s"%hist_name)
    nBinsX = hist.GetNbinsX()
    nBinsY = hist.GetNbinsY()
    for xbin in xrange(nBinsX):
        for ybin in xrange(nBinsY):
            bin_cont = hist.GetBinContent(xbin,ybin)
            if bin_cont > 0.0000001:
                mstop = xbin -1
                mlsp = ybin -1
                print mstop, mlsp, bin_cont
                tryStopLSP(mass_dict_sample, mstop, mlsp, def_val= {"nEvents":0, "xSec":  stop13TeV_NLONLL[mstop]  } )
                mass_dict_sample[mstop][mlsp]['nEvents'] += bin_cont
                tryStopLSP(mass_dict, mstop, mlsp, def_val={"nEvents":0, "xSec":  stop13TeV_NLONLL[mstop] , "samples": set()    })
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

        pickle.dump(mass_dicts_samples_all, open(output_dir +"/mass_dict_samples.pkl","w") )
        pickle.dump(mass_dicts_all, open(output_dir +"/mass_dict.pkl","w") )


    if dos['get_chains']:
        chains={}
        for sample in samples:
            sample_name = sample["name"]
            print sample_name
            chunks = getChunks(sample, maxN=-1)
            chunk = chunks[0]
            chain = getChain(chunk, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1, treeName='tree')
            chains[sample_name]=chain




