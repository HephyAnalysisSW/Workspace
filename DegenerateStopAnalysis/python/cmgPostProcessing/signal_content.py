import ROOT
import pickle
import os
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
from Workspace.HEPHYPythonTools.xsecSMS import *

import pickle

dos={
      "get_sig_info":True,
      "get_chains":False,
    }


getGenFilterEff = True

import Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISpring16MiniAODv2_v3 as cmgTuples
samples = [
            #cmgTuples.SMS_T2tt_dM_10to80_2Lfilter
            cmgTuples.SMS_T2tt_dM_10to80_genHT_160_genMET_80 
        ]


genFilterEff_file = '$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/filterEfficiency/T2tt_dM_10to80_genHT160_genMET80/filterEffs_genHT160_genMET80.pkl'

if getGenFilterEff:
    genFilterEff_path = os.path.expandvars(genFilterEff_file)
    if os.path.isfile(genFilterEff_path):
       genFilterEff = pickle.load(open(genFilterEff_path)) 
    else:
        raise Exception("cannot find gen filter file! %s"%genFilterEff_path)
        

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
                tryStopLSP(mass_dict_sample, mstop, mlsp, def_val= {"nEvents":0, "xSec":  stop13TeV_NLONLL[mstop] , 'genFilterEff':genFilterEff[mstop][mlsp] } )
                mass_dict_sample[mstop][mlsp]['nEvents'] += bin_cont
                tryStopLSP(mass_dict, mstop, mlsp, def_val={"nEvents":0, "xSec":  stop13TeV_NLONLL[mstop] , "samples": set()  ,  'genFilterEff':genFilterEff[mstop][mlsp]  })
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

        print "Pickles dumped:",
        print output_dir +"/mass_dict_samples.pkl"
        print output_dir +"/mass_dict.pkl"

    if dos['get_chains']:
        chains={}
        for sample in samples:
            sample_name = sample["name"]
            print sample_name
            chunks = getChunks(sample, maxN=-1)
            chunk = chunks[0]
            chain = getChain(chunk, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1, treeName='tree')
            chains[sample_name]=chain
