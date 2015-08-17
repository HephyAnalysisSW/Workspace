#!/bin/sh

from copytools import *
import subprocess
import os
from os.path import basename, splitext
from optparse import OptionParser
from Workspace.HEPHYPythonTools.user import username

test=False              ## True will only print the commands and not actually run them
nParalJobs=4
verbose=True            
dpmDir                      = "/dpm/oeaw.ac.at/home/cms/store/user/"
userNameDPM                 = 'schoef'
#sourceBaseDirDPM            =["DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]
targetBaseDirNFS            =  "/cmgTuples/for_daniel"
userNameNFS                 =  username

sourceBaseDirDPMList=[
"WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",


#"DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
#"DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
#"DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
#"DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
#"DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
##DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",  #directory with one bad subdirectory is problematic! needs a fix
#"QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
##"QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8", #RECO 
#"QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8",
#"QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8",
#"ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
#"ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
#"ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
#"ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
#"TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
#"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
#"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
#"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
#"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
#"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
#"WWTo2L2Nu_13TeV-powheg",
#"WZ_TuneCUETP8M1_13TeV-pythia8",
#"ZJetsToNuNu_HT-200To400_13TeV-madgraph",
#"ZJetsToNuNu_HT-400To600_13TeV-madgraph",
#"ZJetsToNuNu_HT-600ToInf_13TeV-madgraph",
#"ZZ_TuneCUETP8M1_13TeV-pythia8",
]
#sourceBaseDirDPMList=sourceBaseDirDPMList[0:4]










################################################################################################################
################################################################################################################
####################################      DONT TOUCH BELOW HERE    #############################################
####################################      (unless you have to!)    #############################################
################################################################################################################
################################################################################################################


parser = OptionParser()
(options, args) = parser.parse_args()


try:
  allOptDicts
except NameError:
  allOptDicts=[]
  for sourceBaseDirDPM in sourceBaseDirDPMList:
    sourceDir=dpmDir+"/%s/"%userNameDPM  +sourceBaseDirDPM
    cmgHashedDirs = getCMGHashedDirs(sourceDir)
    for dir in cmgHashedDirs:
      #print "########################## copying #####################"
      #print dir
      dirSplit = dir.split("/")
      indxUsr = dirSplit.index(userNameDPM)
      #indxHash = dirSplit.index("0000")
      indxHash = -2
      sampleName= "_".join(dirSplit[indxUsr+1:indxHash-1])
      #print sampleName
      allOptDicts.append(  {
                            "dpmDir":dir,
                            "sourceDirDPM":dir.replace(dpmDir,"").replace(userNameDPM,""),
                            "sampleName":sampleName,
                            "targetDirNFS":targetBaseDirNFS+"/"+sampleName,
                            "userNameNFS":userNameNFS,
                            "userNameDPM":userNameDPM,
                           })

################################
## For Test:
if test:
  for iJob, optDict in enumerate(allOptDicts):
    iJob+=1
    getOutputString = "getCMGCrabOutput.py     --userNameDPM={userNameDPM} --userNameNFS={userNameNFS} --source={sourceDirDPM} --target={targetDirNFS} --fileName='' --suffix=\".root .tgz\"".format(**optDict)
    unpackString=     "unpackCMGCrabOutput.py  --userNameNFS={userNameNFS}  --dir={targetDirNFS} --suffix=\".tgz\"".format(**optDict)
    #print "Job#", iJob
    if iJob%nParalJobs==0:paral=""
    else: paral="&"
    print iJob,paral  
    print getOutputString
    print unpackString

################################

else:
### To Copy:
  for iJob, optDict in enumerate(allOptDicts):
    getOutputString = "getCMGCrabOutput.py     --userNameDPM={userNameDPM} --userNameNFS={userNameNFS} --source={sourceDirDPM} --target={targetDirNFS} --fileName='' --suffix=\".root .tgz\"".format(**optDict)
    #print "Job#", iJob
    if (iJob+1)%nParalJobs==0:paral=""
    else: paral="&"
    #print iJob,paral  
    #os.system(getOutputString +";" + unpackString + paral)
    #os.system(getOutputString)
    os.system(getOutputString + paral)
    #os.system(unpackString+" &")

  ################################
## To Unpack:
  for iJob, optDict in enumerate(allOptDicts):
    if (iJob+1)%nParalJobs==0:
      paral=""
    else: 
      paral=" &"
    unpackString=     "unpackCMGCrabOutput.py  --userNameNFS={userNameNFS}  --dir={targetDirNFS} --suffix=\".tgz\"".format(**optDict)
    #print "ijob:", iJob,paral  
    #os.system(getOutputString +";" + unpackString + paral)
    os.system(unpackString+ paral)




