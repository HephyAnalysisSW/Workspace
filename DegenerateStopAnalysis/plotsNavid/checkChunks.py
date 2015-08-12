#!/bin/sh
import subprocess
import os
from os.path import basename, splitext
from optparse import OptionParser

import glob


dirToCheck="/data/nrad/cmgTuples/RunII/Spring15_v1"




#mainDirProc = subprocess.Popen(["ls", dirToCheck],stdout=subprocess.PIPE)
#filesMainDir = [l.rsplit()[0] for l in mainDirProc.stdout.readlines()]

def checkWildCard(dir):
  if "*" in dir:
    return dir
  else:
    return dir+"/*"

def removeBasename(dir):
  return dir.replace("/"+basename(dir),"")

def checkForStrandedRootFiles(dir,filename="*",warn=False):
  strandedRootFiles=glob.glob(dir+"/%s.root"%filename)
  if warn and strandedRootFiles:
    print "There these stranded Rootfiles:", strandedRootFiles
  return strandedRootFiles

def getDirs(dir):
  dir = checkWildCard(dir)
  files = glob.glob(dir)
  dirs = [f for f in files if os.path.isdir(f)]
  return dirs

def getChunkNum(chunk):
  chunkString="Chunk"
  try:
    chunk = [x for x in chunk.rsplit("/") if "Chunk" in x][0]
    chunkNum= chunk[ chunk.index("Chunk")+5: ]
    if chunkNum.isalnum():
      return chunkNum
    else:
      print "##########################################"
      print "%s chunkNum is not Number"%chunkNum
      print chunk
      print "##########################################"
      return False
  except ValueError:
    return ""

def getTreeNum(chunk):
  string="tree"
  try:
    chunk = [x for x in chunk.rsplit("/") if string in x][0]
    chunk = splitext(chunk)[0]
    chunkNum= chunk[ chunk.index(string)+len(string)+1: ]
    if chunkNum.isalnum():
      return chunkNum
    else:
      print "##########################################"
      print "chunkNum is not Number"
      return False
  except ValueError:
    return ""

def getChunk(dir,chunkNum="*"):
  chunks = glob.glob(dir+"/"+basename(dir)+"_Chunk%s"%chunkNum)
  return chunks

def isGoodChunk(dir,chuckNum):
  chunk = getChunk(dir,chuckNum)
  return len(glob.glob(chunk+"/tree.root"))==1  

def isBadCMGDir(dir,warn=False):
  chunks = getChunk(dir)
  chunksWithRootFiles = [removeBasename(d) for d in glob.glob(dir+"/*/tree.root")]

  nChunks             = len( chunks)
  nChunksWithRootFile = len( chunksWithRootFiles )

  if nChunks == nChunksWithRootFile:
    return False
  else:
    if warn: print nChunks-nChunksWithRootFile , "Chunks are without rootfiles in Dir:", dir
    chunksWithoutRootFiles = [x for x in chunks if x not in chunksWithRootFiles]
    badChunkList = [getChunkNum(x) for x in chunksWithoutRootFiles] 
    return (chunksWithoutRootFiles,badChunkList)

subDirs= getDirs(dirToCheck)
strandedRootFilesDict={}
badCMGDirs=[]


print len(subDirs) , "Directories in ", dirToCheck
for subDir in subDirs:
  strandedRootFiles = checkForStrandedRootFiles(subDir,filename="tree*")
  badCMG = isBadCMGDir(subDir)

  if badCMG or strandedRootFiles:
    badCMGDir = {"sampleName":basename(subDir),"targetDir":subDir,"badChunks":"" ,"strandedRootFiles":strandedRootFiles }
    if isBadCMGDir(subDir):
      badCMGDir["badChunkDirs"] , badCMGDir["badChunks"]= isBadCMGDir(subDir)
    badCMGDirs.append(badCMGDir)
    if strandedRootFiles: 
      print len(strandedRootFiles),"(%"+"%0.2f)"%(1.*len(strandedRootFiles)/len(getChunk(subDir))*100),"stranded Root Files out of chunks in dir:"
      print "        ", subDir
      strandedRootFilesDict[subDir]=strandedRootFiles


sourceBaseDirDPMList=[
"DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
#"DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",  #directory with one bad subdirectory is problematic! needs a fix
"QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8",
"QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8",
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

dpmDir                      = "/dpm/oeaw.ac.at/home/cms/store/user/"
userNameDPM                 ='schoef'
#sourceBaseDirDPM            =["DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]
targetBaseDirNFS            ="/cmgTuples/RunII/Spring15_v1/"
userNameNFS                 ='nrad'
verbose=False


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
                            "targetDirNFS":targetBaseDirNFS+"/"+sampleName,
                            "sampleName":sampleName,
                            "userNameNFS":userNameNFS,
                            "userNameDPM":userNameDPM,
                           })






for dir in badCMGDirs:
  sampleName = dir['sampleName']
  #print len(filter( lambda x: x['sampleName']==sampleName,allOptDicts ))
  assert (len(filter( lambda x: x['sampleName']==sampleName,allOptDicts )))==1
  dir['dpmDir']= filter( lambda x: x['sampleName']==sampleName,allOptDicts )[0]['dpmDir']





def fixBadCMGChunk(badCMGDirDict,attempt=0):

  if not isBadCMGDir(badCMGDirDict['targetDir']):
    print badCMGDirDict['sampleName'] ,"has no bad chunks"
  else:
    nBadChunks = len( badCMGDirDict["badChunkDirs"])
    dpmDir = badCMGDirDict['dpmDir']
    print nBadChunks ," Bad Chunks being fixed in:" , 
    print "        ", badCMGDirDict['targetDir']
    print "                Fixing Chunks:"
    for badChunk in badCMGDirDict["badChunkDirs"] :
      chunkNum = getChunkNum(badChunk)
      tree = dpmDir +"/tree_%s.root"%chunkNum
      missingTreeLs=subprocess.Popen(["dpns-ls" , tree],stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
      stdout      = [l for l in missingTreeLs.stderr.readlines()]
      if stdout:
        print "THERE IS SOMETHING WEIRD GOING ON"
        print stdout
        print "WILL SKIP THIS TREE"
        continue
      missingTree = [l.rsplit()[0] for l in missingTreeLs.stdout.readlines()][0]
      copyString = "/usr/bin/rfcp " + missingTree +"  " + badChunk+"/tree.root"
      os.system(copyString)
    fixed = isBadCMGDir(badCMGDirDict['targetDir'])      
    if not fixed:
      print "Chunks are all fixed!"
    elif attempt < 0:
      print "Still some missing chunks!"
      print "attempting to fix one more time!"
      print "attempt: %s"%attempt
      attempt +=1
      fixBadCMGChunk(badCMGDirDict,attempt=attempt)
    else:
      print "##################################"
      print "WARNING STILL CANT FIX DIRECTORY! LEAVE ME ALONE!!!!!"
      print "##################################"
    

def fixAllBadCMGChunks():
  for i in range(0,18): 
      print badCMGDirs[i]['sampleName']
      print "########################################"
      fixBadCMGChunk(badCMGDirs[i])
      print "########################################"


def fixStrandedRootFiles(badCMGDirDict,attempt=0,defaultOutput="output.log_"):
  nStranded =  len(badCMGDirDict['strandedRootFiles'])
  if nStranded == 0:
    print badCMGDirDict['sampleName'], "has no stranded root files!"
  else:
    dpmDir = badCMGDirDict['dpmDir']
    print nStranded ," Stranded Root Files being fixed in:" ,
    print "        ", badCMGDirDict['targetDir']
    print "                Fixing stranded root file:"
    for strandedRootFile in badCMGDirDict['strandedRootFiles']:
      commands = []
      treeNum = getTreeNum(strandedRootFile)
      chunkName = badCMGDirDict['sampleName']+"_Chunk"+treeNum
      cmgChunk  = badCMGDirDict['targetDir']+"/"+chunkName
      tarFileName = defaultOutput+treeNum+".tgz"
      sourceTarFile = dpmDir+tarFileName
      targetTarFile = badCMGDirDict['targetDir']+"/"+tarFileName

      #print sourceTarFile, chunkName, cmgChunk
      print treeNum ," :   " 

      missingTarfileLs =subprocess.Popen(["dpns-ls" , sourceTarFile ],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout      = [l for l in missingTarfileLs.stderr.readlines()]
      if stdout:
        print "THERE IS SOMETHING WEIRD GOING ON"
        print stdout
        print "WILL SKIP THIS TREE"
        continue
      missingTarfile = [l.rsplit()[0] for l in missingTarfileLs.stdout.readlines()][0]
      objs={"tarFileName":tarFileName, "sourceTarFile":sourceTarFile, "targetTarFile":targetTarFile, "cmgChunk":cmgChunk, "chunkName":chunkName, "treeNum":treeNum}
      commands= [
            "mkdir -p %s"%cmgChunk,
            "/usr/bin/rfcp %s %s"%(sourceTarFile,targetTarFile ),
            "tar -xf %s --directory=%s --strip-components=1"%(targetTarFile,cmgChunk),
            "mv %s %s"%(strandedRootFile,cmgChunk+"/tree.root"),
            "rm -rf %s"%(targetTarFile  ),
                ]
      for command in commands:
        print "                 ", command
        os.system(command)
      #return commands,objs

      #os.system("mkdir %s"%chunk)
      #os.system("tar -xf %s --directory=%s --strip-components=1"%(directory+"/"+filename,cmgChunks))
      #os.system( "mv %s %s"%(directory + '/' + rootFileName,cmgChunks+'/'+treeProducerName+'/'+finalTreeName))
      #os.system("rm -rf %s"%(directory+"/"+filename) )



