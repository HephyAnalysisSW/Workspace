import ROOT
import glob


from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_mAODv2 import *
from Workspace.DegenerateStopAnalysis.navidTools.getSamples_PP_mAODv2_7412pass2_scan import getSamples
from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import *

import pickle



mc_path     = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/RunIISpring15DR74_25ns"
signal_path = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/RunIISpring15DR74_25ns"
data_path   = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/Data_25ns"



#sample_dir = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/7412pass2_SMSScan_v3/RunIISpring15DR74_25ns/inc"
#samp_info={
#        "s30":          {"dir":"T2DegStop_300_270"                         },
#        "s30FS":        {"dir":"T2DegStop_300_270_FastSim"                 },
#        "s10FS":        {"dir":"T2DegStop_300_290_FastSim"                 } ,  
#        "s60FS":        {"dir":"T2DegStop_300_240_FastSim"                 },
#        }
#
#samples={}
#for samp in samp_info:
#    samples[samp]=ROOT.TChain("Events")
#    samples[samp].Add(sample_dir+"/"+samp_info[samp]['dir']+"/*.root")




isrweightOld = "(1.+7.5e-5*Max$(GenPart_mass[stopIndex1]))*(1.*(stops_pt<120.)+0.95*(stops_pt>=120.&&stops_pt<150.)+0.9*(stops_pt>=150.&&stops_pt<250.)+0.8*(stops_pt>=250.))"
isrWeight = lambda norm: '(1.+{norm}*Max$(GenPart_mass[stopIndex1]))*(1.*(stops_pt<120.)+0.95*(stops_pt>=120.&&stops_pt<150.)+0.9*(stops_pt>=150.&&stops_pt<250.)+0.8*(stops_pt>=250.))'.format(norm=norm)
isrw= isrWeight(11.686e-05)






cmgPP = cmgTuplesPostProcessed(mc_path, signal_path, data_path)
#samples = getSamples(scan=False,sampleList=['s30'], skim='inc',cmgPP=cmgPP)
samples = getSamples(scan=True,sampleList=[''], skim='inc',cmgPP=cmgPP)





#tree = samples['s30'].tree


def get_norm_factor( tree ):
    initial_yield = getYieldFromChain( tree, "(1)", "(1)" )
    weight_yield  = getYieldFromChain( tree, "(1)", isrWeight(0) )
    tree.GetEntry(1)
    stop_mass = tree.GetLeaf("GenSusyMStop").GetValue()
    norm_factor = (initial_yield/weight_yield  -1 )/stop_mass
    return norm_factor


mass_dict = pickle.load(  open("/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/cmgPostProcessing/mass_dict_all.pkl","r"))



norm_factor_dict={}
for stop_mass in mass_dict:
    norm_factor_dict[stop_mass]={}
    for lsp_mass in mass_dict[stop_mass]:
        tree = samples["s%s_%s"%(int(stop_mass),int(lsp_mass))].tree
        if tree.GetEntries():
            norm_factor = get_norm_factor(tree)
        else:
            norm_factor = 0

        norm_factor_dict[stop_mass][lsp_mass]=norm_factor

    

pl = makeStopLSPPlot("norm_factor", norm_factor_dict, title="ISR Weight Normalization Factor")
pl.Draw("COLZ")




