import ROOT

#import ROOT; a  = ROOT.TChain("Events"); z= [ a.Add(f) for f in SMS_T2tt_dM_10to80_genHT_160_genMET_80.files ]

from DataFormats.FWLite import Events, Handle, Lumis
import DataFormats.FWLite as FWLite

import os


keys=[
"numEventsPassed"        ,
"numEventsTotal"        ,
"numEventsTried"        ,
"numPassNegativeEvents"        ,
"numPassPositiveEvents"        ,
"numTotalNegativeEvents"        ,
"numTotalPositiveEvents"        ,
"sumFailWeights"        ,
"sumFailWeights2"        ,
"sumPassWeights"        ,
"sumPassWeights2"        ,
"sumWeights"        ,
"sumWeights2"        ,
"filterEfficiency"        ,
"filterEfficiencyError"        ,
]

import CMGTools.RootTools.samples.samples_13TeV_signals as signals
import multiprocessing

fileList = signals.SMS_T2tt_dM_10to80_genHT_160_genMET_80.files


badfiles=[
"SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/00000/C4A453AF-6550-E611-845E-00259073E370.root",
"SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/20000/9CA8423F-7C52-E611-996F-00259074AEE6.root",
"SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/80000/E20B1BB0-AD51-E611-AAB7-0CC47A1DFE60.root",
"SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/90000/52E5EB56-4850-E611-B933-0CC47A1E0476.root",
"SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/90000/CCAC4322-4850-E611-A3AD-0090FAA581B4.root",
"SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/90000/DCFF8842-4850-E611-89EC-0CC47A1DF7F8.root",
]


for f in fileList:
    if any([badfile in f for badfile in badfiles]):
        fileList.pop( fileList.index(f) )
        print f

#fileList = ["root://cms-xrd-global.cern.ch//store/mc/RunIISpring16MiniAODv2/SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/00000/009E3FE0-C24B-E611-896E-002590E1E9B8.root"]

output_dir = "./model_info/"




import pickle
def getModelInfoFromFile(f):
    events =  Events(f)
    lumis  =  FWLite.Lumis(f)
    tree = ROOT.TChain("Events")
    #for f in fileList: tree.Add(f)
    for f in fileList: tree.Add(f)
    events.toBegin()
    print "number of Events: "
    nEvents = tree.GetEntries()
    print nEvents
    models = {}
    print "starting the loop:, "
    for ievt in xrange(nEvents):
        if ievt%100000 == 0 : print ievt 
        #tree.GetEntry(ievt)
        events.to(ievt)
        genLumiInfoHandle = Handle( "<GenLumiInfoHeader>" )
        lumis.getByLabel( "generator" , genLumiInfoHandle )
        genLumiInfo = genLumiInfoHandle.product()
        model = genLumiInfo.configDescription()
        #print model
        #genFilterInfoHandle = Handle("<GenFilterInfo>")
        #lumis.getByLabel( "genFilterEfficiencyProducer" , genFilterInfoHandle )
        #genFilterInfo = genFilterInfoHandle.product()
        if model in models:
            models[model]+=1
        else:
            models[model]=1
    filename= os.path.splitext(os.path.basename(f))[0]
    pickle.dump( models, open( output_dir +"/raw_models_evts%s.pkl"%filename,"w"))
    print models
    return models



if __name__ == '__main__':
    nProc = 20
    pool = multiprocessing.Pool(nProc)
    results = pool.map( getModelInfoFromFile ,  fileList)
    pool.close()
    pool.join()







