#!/bin/sh
import subprocess
import os
from os.path import basename, splitext
from optparse import OptionParser


test=False ## True will only print the commands and not actually run them


verbose=True
#/dpm/oeaw.ac.at/home/cms/store/user//schoef/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test/150807_213157/0000/
sourceBaseDirDPMList=[
"DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
#"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8",
"QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8",
"ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"WWTo2L2Nu_13TeV-powheg",
"WZ_TuneCUETP8M1_13TeV-pythia8",
"ZJetsToNuNu_HT-200To400_13TeV-madgraph",
"ZJetsToNuNu_HT-400To600_13TeV-madgraph",
"ZJetsToNuNu_HT-600ToInf_13TeV-madgraph",
"ZZ_TuneCUETP8M1_13TeV-pythia8",
]
#sourceBaseDirDPMList=sourceBaseDirDPMList[0:2]






dpmDir                      = "/dpm/oeaw.ac.at/home/cms/store/user/"
userNameDPM                 ='schoef'
#sourceBaseDirDPM            =["DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]
targetBaseDirNFS            ="/cmgTuples/RunII/Spring15_v1/"
userNameNFS                 ='nrad'




################################################################################################################
################################################################################################################
####################################      DONT TOUCH               #############################################
####################################   (unless you have to!)       #############################################
################################################################################################################
################################################################################################################


parser = OptionParser()
(options, args) = parser.parse_args()


def getCMGHashedDirs(sourceDir):
  dirDict={}
  dirs=[]
  proc = subprocess.Popen(["dpns-ls", sourceDir],stdout=subprocess.PIPE)
  stdout = proc.stdout.readlines()
  if verbose: print "DPM Sample: ", sourceDir
  if proc.stderr:
    print "############# STDERR ################"
    for line in proc.stderr:
        print line
  else:
    nLines = len(stdout)
    #print "Number of Directories:", nLines
    if nLines > 50:
       print "#####################################################"
       print "Too many directories here! this could take some time!" 
       print "#####################################################"
    if nLines == 0:
       print "Directory not valid: ", sourceDir
       assert False 
    if nLines == 1:
      cmgHash=str([l.rsplit()[0] for l in stdout ][0])
      if cmgHash.replace("_","").isalnum():
        cmgHashedDir = sourceDir+"/"+cmgHash+"/"
        proc2 = subprocess.Popen(["dpns-ls", cmgHashedDir],stdout=subprocess.PIPE)
        cmg000s=[]
        ## checking the 0000 or 0001, etc, directories in the Hashed Dir
        for l in proc2.stdout.readlines():
          cmg000= l.rsplit()[0]
          if cmg000.isalnum() and len(cmg000)==4:
            #print cmg000
            dirs.append(cmgHashedDir+cmg000+"/")
          else:
             
            print "#####################################################"
            print cmgHash, "is not a cmgHash (0000 dir) or directory is not a CMG Hashed Dir:", cmgHashedDir
            print "#####################################################"
        #cmgHashedDir = sourceDir+"/"+cmgHash+"/0000/"
        #print "cmgHash:", cmgHash
        #print "cmgHashedDir:", cmgHashedDir 

        #dirs.append(cmgHashedDir)
        #return cmgHashedDir
        return dirs
      else:
        #print cmgHash.replace("_","")
        #print cmgHash.replace("_","").isalnum()
        #print str(cmgHash.replace("_","")).isalnum()
        #print type(cmgHash)
        #print cmgHash, "is not a cmgHash or directory is not a CMG output dir:", sourceDir
        #del cmgHash
        line = stdout[0].rsplit()[0]
        if verbose:
          print "Descending into directories:"
          print "        ", line
        dirs.append(getCMGHashedDirs(sourceDir+"/"+line)[0])
    else:
      print "Descending into directories:" 
      for line in stdout:
        print "        ", line
        #dirDict['l1'].append(line.rstrip())
        #dirDict['l1'].append()
        dirs.append(getCMGHashedDirs(sourceDir+"/"+line.rsplit()[0])[0]  )
  return dirs

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
                          "sourceDirDPM":dir.replace(dpmDir,"").replace(userNameDPM,""),
                          "targetDirNFS":targetBaseDirNFS+"/"+sampleName,
                          "userNameNFS":userNameNFS,
                          "userNameDPM":userNameDPM,
                         })

iJob=0
for optDict in allOptDicts:
  iJob+=1
  getOutputString = "getCMGCrabOutput.py     --userNameDPM={userNameDPM} --userNameNFS={userNameNFS} --source={sourceDirDPM} --target={targetDirNFS} --fileName='' --suffix=\".root .tgz\"".format(**optDict)
  unpackString=     "unpackCMGCrabOutput.py  --userNameNFS={userNameNFS}  --dir={targetDirNFS} --suffix=\".tgz\"".format(**optDict)

  #print "Job#", iJob
  #if iJob%4==0:paral=""
  #else: paral="&"
  #print iJob,paral  

  if test:
    print getOutputString
    print unpackString

  else:
    #os.system(getOutputString +";" + unpackString + paral)
    os.system(getOutputString)
    os.system(unpackString+" &")




