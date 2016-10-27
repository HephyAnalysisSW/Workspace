import ROOT
import pickle
import os
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
from Workspace.HEPHYPythonTools.xsecSMS import *
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
u_float = degTools.u_float

lumi = 12864.4

import Workspace.HEPHYPythonTools.xsecSMS as xsecSMS
stop_xsecs = xsecSMS.stop13TeV_NLONLL



import Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISpring16MiniAODv2_v3 as cmgTuples


samples = [
            cmgTuples.SMS_T2tt_dM_10to80_genHT_160_genMET_80 
        ]


withPuW = False

puWString = '(0.000488876427122 * (nTrueInt > 0.0 && nTrueInt <= 1.0) ) + (0.0151761562164 * (nTrueInt > 1.0 && nTrueInt <= 2.0) ) + (0.0183588773108 * (nTrueInt > 2.0 && nTrueInt <= 3.0) ) + (0.0333664659746 * (nTrueInt > 3.0 && nTrueInt <= 4.0) ) + (0.0483065573428 * (nTrueInt > 4.0 && nTrueInt <= 5.0) ) + (0.0402839565449 * (nTrueInt > 5.0 && nTrueInt <= 6.0) ) + (0.057229456542 * (nTrueInt > 6.0 && nTrueInt <= 7.0) ) + (0.185786803735 * (nTrueInt > 7.0 && nTrueInt <= 8.0) ) + (0.354258558515 * (nTrueInt > 8.0 && nTrueInt <= 9.0) ) + (0.63478267999 * (nTrueInt > 9.0 && nTrueInt <= 10.0) ) + (0.924729866345 * (nTrueInt > 10.0 && nTrueInt <= 11.0) ) + (1.28211894828 * (nTrueInt > 11.0 && nTrueInt <= 12.0) ) + (1.57418917522 * (nTrueInt > 12.0 && nTrueInt <= 13.0) ) + (1.71625399914 * (nTrueInt > 13.0 && nTrueInt <= 14.0) ) + (1.77500747401 * (nTrueInt > 14.0 && nTrueInt <= 15.0) ) + (1.6143356382 * (nTrueInt > 15.0 && nTrueInt <= 16.0) ) + (1.41243958433 * (nTrueInt > 16.0 && nTrueInt <= 17.0) ) + (1.41140446255 * (nTrueInt > 17.0 && nTrueInt <= 18.0) ) + (1.30200653416 * (nTrueInt > 18.0 && nTrueInt <= 19.0) ) + (1.33122481953 * (nTrueInt > 19.0 && nTrueInt <= 20.0) ) + (1.12053210702 * (nTrueInt > 20.0 && nTrueInt <= 21.0) ) + (0.97986467583 * (nTrueInt > 21.0 && nTrueInt <= 22.0) ) + (0.926955215044 * (nTrueInt > 22.0 && nTrueInt <= 23.0) ) + (0.883425521402 * (nTrueInt > 23.0 && nTrueInt <= 24.0) ) + (0.763767705156 * (nTrueInt > 24.0 && nTrueInt <= 25.0) ) + (0.721796242966 * (nTrueInt > 25.0 && nTrueInt <= 26.0) ) + (0.555326852123 * (nTrueInt > 26.0 && nTrueInt <= 27.0) ) + (0.472738437161 * (nTrueInt > 27.0 && nTrueInt <= 28.0) ) + (0.336529335244 * (nTrueInt > 28.0 && nTrueInt <= 29.0) ) + (0.254758566341 * (nTrueInt > 29.0 && nTrueInt <= 30.0) ) + (0.178877826996 * (nTrueInt > 30.0 && nTrueInt <= 31.0) ) + (0.12172745258 * (nTrueInt > 31.0 && nTrueInt <= 32.0) ) + (0.105837192589 * (nTrueInt > 32.0 && nTrueInt <= 33.0) ) + (0.0821827858547 * (nTrueInt > 33.0 && nTrueInt <= 34.0) ) + (0.0875271918878 * (nTrueInt > 34.0 && nTrueInt <= 35.0) ) + (0.109857294003 * (nTrueInt > 35.0 && nTrueInt <= 36.0) ) + (0.181669459093 * (nTrueInt > 36.0 && nTrueInt <= 37.0) ) + (0.20336544128 * (nTrueInt > 37.0 && nTrueInt <= 38.0) )'

getFilterPUDep=False

if getFilterPUDep:
    sample = cmgTuples.TTJets_LO
    sample_name = sample["name"]
    print sample_name
    chunks = getChunks(sample, maxN=-1)
    chunk ,nEvents = chunks
    chain = getChain(chunk, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1, treeName='tree')

    if withPuW:
        puW="puReweight"
        puWTag = ""
    else:
        puW="(1)"
        puWTag="_noPUW"
    
    chain.SetAlias(puW, puWString)


    puVar = "nTrueInt"
    puCuts = [ 15,20,25 ]
    puOps  = { 'gt':'>=', 'lt':'<' }
    lumiW  = sample['xsec'] * lumi /nEvents

    genHTVar = "Sum$(GenJet_pt*(GenJet_pt>30 && abs(GenJet_eta)<2.5 ))"
    genMETVar= "met_genPt"
    genHTCut = 160
    genMETCut= 80
    genFilterCut = "(( %s < %s  ) && (%s < %s))"%(genHTVar,genHTCut, genMETCut, genMETVar )

    puFiltDep = {}
    for puCut in puCuts:
        for puOpTag, puOp in puOps.iteritems():
            puCutString = '{puVar} {puOp} {puCut}'.format(puVar=puVar, puOp=puOp, puCut = puCut )
            tag = puOpTag+"%s"%puCut
            cutString = "(%s) && (%s)"%(genFilterCut, puCutString)
            weights   = " * ".join([" (%s) "%w for w in ["(1)", puW, lumiW]])
            print '---------', tag, "\n", 'cut:', cutString, '\n weight:', weights
            puFiltDep[tag+"_all"]    = u_float(* getYieldFromChain( chain, puCutString, weights , returnError=True) )
            puFiltDep[tag+"_filter"] = u_float(* getYieldFromChain( chain, cutString , weights , returnError=True) )

    puFiltDep["puInc_all"]    = u_float(* getYieldFromChain( chain, puCutString, weights , returnError=True) )
    puFiltDep["puInc_filter"] = u_float(* getYieldFromChain( chain, cutString , weights , returnError=True) )


    puFiltRatio = {}
    for puCut in puCuts:
        for puOpTag, puOp in puOps.iteritems():
            tag = puOpTag+"%s"%puCut
            puFiltRatio[tag] = puFiltDep[tag+"_filter"] / puFiltDep[tag+"_all"] 
    puFiltRatio['puInc'] = puFiltDep["puInc_filter"] / puFiltDep["puInc_all"]            

    pickle.dump( puFiltDep   , file( "puFiltDepTTJets%s.pkl"%puWTag   ,"w") )
    pickle.dump( puFiltRatio , file( "puFiltRatioTTJets%s.pkl"%puWTag ,"w") )

        
if __name__ == "__main__":

    def tryStopLSP(mass_dict, mstop, mlsp, def_val = 0):
        try:
            mass_dict[mstop]
        except KeyError:
            mass_dict[mstop]={}
        try:
            mass_dict[mstop][mlsp]
        except KeyError:
            mass_dict[mstop][mlsp]=def_val
    
    mass_dict_file = cmgTuples.signal_path + "/mass_dict.pkl"
    mass_dict = pickle.load(file(mass_dict_file))
    
    sample = samples[0]
    sample_name = sample["name"]
    print sample_name
    chunks = getChunks(sample, maxN=-1)
    chunk = chunks[0]
    chain = getChain(chunk, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1, treeName='tree')
    
    

    if withPuW:
        puW="puReweight"
        puWTag = ""
        chain.SetAlias(puW, puWString )
    else:
        puW="(1)"
        puWTag="_noPUW"




    #puW = '(1)' 
    
    def_weight = "((1) * (1) * ((7.279e-05 *(GenSusyMStop) + 1.108) * ( (nIsr==0) + (nIsr==1)*0.882  + (nIsr==2)*0.792  + (nIsr==3)*0.702  + (nIsr==4)*0.648  + (nIsr==5)*0.601  + (nIsr>=6)*0.515 ) ) * (1))"
    #def getPUYields(chain, mstop, mlsp):
    def getPUYields( (mstop, mlsp)):
        stop_lsp_cut = "(GenSusyMNeutralino==%s && GenSusyMStop==%s )"%(mlsp,mstop)
        chain.Draw(">>eList_%s_%s"%(mstop,mlsp),stop_lsp_cut)
        eList = getattr(ROOT,"eList_%s_%s"%(mstop,mlsp))
        chain.SetEventList(eList)
        nEvents = chain.GetEventList().GetN()
        print "nEvents for: mStop%s mLSP%s:"%(mstop, mlsp), nEvents
        puVar = "nTrueInt"
        puCuts = [ 15,20,25 ]
        #puCuts = [ 20 ]
        puOps  = { 'gt':'>=', 'lt':'<' } 
        res = {'nEvents':nEvents}
        lumiW = (stop_xsecs[mstop] * lumi)/(mass_dict[mstop][mlsp]['nEvents'])*mass_dict[mstop][mlsp]['genFilterEff']
        for puCut in puCuts:
            for puOpTag, puOp in puOps.iteritems():
                puCutString = '{puVar} {puOp} {puCut}'.format(puVar=puVar, puOp=puOp, puCut = puCut )
                tag = puOpTag+"%s"%puCut
                cutString = "(%s) && (%s)"%(stop_lsp_cut, puCutString)
                weights   = " * ".join([" (%s) "%w for w in [def_weight, puW, lumiW]])
                print '---------', tag, "\n", 'cut:', cutString, '\n weight:', weights
                res[tag] = u_float(* getYieldFromChain( chain, cutString, weights , returnError=True) )
        chain.SetEventList(0)
        return (mstop, mlsp) , res







    if True:

        res = {}
        #for mstop in mass_dict.keys():
        #    res[mstop]={}
        #    for mlsp in mass_dict[mstop].keys():
        #        res[mstop][mlsp] = getPUYields( (mstop, mlsp)) 
        

        import multiprocessing
        nProc = 30
        pool = multiprocessing.Pool(nProc)
        results = pool.map(getPUYields ,  [(mstop,mlsp) for mstop in mass_dict.keys() for mlsp in mass_dict[mstop].keys()] )
        pool.close()
        pool.join()
        
        for (mstop,mlsp), puylds in results:
            tryStopLSP(res, mstop, mlsp, puylds)

        pickle.dump(res, file("puTotYields%s.pkl"%puWTag,"w"))

    if False:


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

        chains={}
        for sample in samples:
            sample_name = sample["name"]
            print sample_name
            chunks = getChunks(sample, maxN=-1)
            chunk = chunks[0]
            chain = getChain(chunk, minAgeDPM=0, histname='histo', xrootPrefix='root://hephyse.oeaw.ac.at/', maxN=-1, treeName='tree')
            chains[sample_name]=chain
