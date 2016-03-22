from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import makeStopLSPPlot, getTH2FbinContent, makeStopLSPRatioPlot 
from optparse import OptionParser
parser = OptionParser()
(options,args) = parser.parse_args()


import pickle
import os


#
# limit pickle file
#
import ROOT
import Workspace.DegenerateStopAnalysis.navidTools.limitTools as limitTools
#limit_pickle = args[0]


result_dict= {
                "8tev"      :   {    "pkl":"../../data/limits/8TeV/Full/limits.pkl"                 ,"savedir":"/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload/ExpLimit_8TeV.png" },
                "13tev_isr" :   {    "pkl":"../../data/limits/RunII_IsrWeight/limits.pkl"           ,"savedir":"/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload/ExpLimit_13TeV_IsrWeights.png" },
                "13tev_sys" :   {    "pkl":"../../data/limits/RunII_SysAdjust_IsrWeight/limits.pkl" ,"savedir":"/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload/ExpLimit_13TeV_IsrWeights_AdjustedSys.png" },
             }


bins8tev_dir  ="/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsNavid/data/cards/8TeV/Bins" 
import glob

bins8tev_pkls = glob.glob(bins8tev_dir+"/*.pkl")
bins8tev_savedir = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload/expected_limit/8tev/bins/"
bins8tev = [
            { "name":limitTools.get_filename(b) , "pkl":b, "savedir":bins8tev_savedir+"/%s.png"%limitTools.get_filename(b) } for b in bins8tev_pkls
           ]


bins13tev_dir  = "/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/plotsNavid/data/cards/13TeV/Reload_IsrWeight/Bins"    
bins13tev_pkls = glob.glob(bins13tev_dir+"/*.pkl")
bins13tev_savedir = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload/expected_limit/13tev/bins/"
bins13tev = [
            { "name":limitTools.get_filename(b) , "pkl":b, "savedir":bins13tev_savedir+"/%s.png"%limitTools.get_filename(b) } for b in bins13tev_pkls
           ]





#limit_pickle = "./pkl/RunII_Reload_Scan_Limits_2260.pkl"
#if not limit_pkl:
#    limit_pickle = "./pkl/limits_scan_isr_2200pbm1.pkl"


doStuff = True


if __name__ == "__main__":
    if doStuff:
        #for l in result_dict:
        #    limitTools.drawExpectedLimit(result_dict[l]  )
        for l in bins8tev:                                                                           
            limitTools.drawExpectedLimit(l)
        for l in bins13tev:
            limitTools.drawExpectedLimit(l)

