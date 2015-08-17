import subprocess
import os
from os.path import basename, splitext
from optparse import OptionParser

import glob


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


def getCMGHashedDirs(sourceDir,verbose=False):
  dirDict={}
  dirs=[]
  proc = subprocess.Popen(["dpns-ls", sourceDir],stdout=subprocess.PIPE)
  stdout = proc.stdout.readlines()
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
            if verbose: print "DPM Sample: ", sourceDir
            dirs.append(cmgHashedDir+cmg000+"/")
          else:
             
            print "#####################################################"
            print cmgHash, "is not a cmgHash (0000 dir) or directory is not a CMG Hashed Dir:", cmgHashedDir
            print "#####################################################"
        return dirs
      else:
        line = stdout[0].rsplit()[0]
        if verbose:
          print "Descending into directories:"
          print "        ", line
        dirs.append(getCMGHashedDirs(sourceDir+"/"+line)[0])
    else:
      print "Descending into directories:" 
      for line in stdout:
        print "        ", line
        dirs.append(getCMGHashedDirs(sourceDir+"/"+line.rsplit()[0])[0]  )
  return dirs




def getCMGHashedDirs2(sourceDir,verbose=True,_dirs=[]):
  dirDict={}
  dirs=[]
  proc = subprocess.Popen(["dpns-ls", sourceDir],stdout=subprocess.PIPE)
  lines = proc.stdout.readlines()
  if proc.stderr:
    print "############# STDERR ################"
    for line in proc.stderr:
        print line
  else:
    nLines = len(lines)
    #print "Number of Directories:", nLines
    if nLines > 50:
       print "#####################################################"
       print "Too many directories here! this could take some time!" 
       print "#####################################################"
    if nLines == 0:
       print "Directory not valid: ", sourceDir
       assert False 
    else: # nLines == 1:
      print "nLines: ", nLines
      print lines  
      for line in lines:
        line = line.rsplit()[0]
        print "dir: ", line 
        #cmgHash=str([l.rsplit()[0] for l in line ][0])
        cmgHash=line.rsplit()[0]
        print "CMGHASH?:",  cmgHash
        if cmgHash.replace("_","").isalnum():
          print "YES"
          cmgHashedDir = sourceDir+"/"+cmgHash+"/"
          proc2 = subprocess.Popen(["dpns-ls", cmgHashedDir],stdout=subprocess.PIPE)
          cmg000s=[]
          ## checking the 0000 or 0001, etc, directories in the Hashed Dir
          for l in proc2.stdout.readlines():
            cmg000= l.rsplit()[0]
            if cmg000.isalnum() and len(cmg000)==4:
              #print cmg000
              if verbose: print "DPM Sample Found: ", cmgHashedDir+cmg000+"/"
              dirs.append(cmgHashedDir+cmg000+"/")
            else:
              print "#####################################################"
              print cmgHash, "is not a cmgHash (0000 dir) or directory is not a CMG Hashed Dir:", cmgHashedDir
              print "#####################################################"
          return dirs
        else:
          print "NO"
          #print "$$$$", line
          #line = lines[0].rsplit()[0]
          #print "$$$$", line
          if verbose:
            print "Descending into directories:"
            print "        ", line
          dirs.append(getCMGHashedDirs2(sourceDir+"/"+line)[0])
    #else:
    #  print "Descending into directories:" 
    #  for line in stdout:
    #    print "        ", line
    #    dirs.append(getCMGHashedDirs(sourceDir+"/"+line.rsplit()[0])[0]  )
  return dirs





