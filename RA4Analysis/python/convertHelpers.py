import ROOT

from Workspace.HEPHYPythonTools.helpers import wrapStr

def compileStruct(structName, structString, tmpDir):
  import uuid, os
  uniqueFilename = str(uuid.uuid4())
  tmpFileName = tmpDir+'/'+uniqueFilename+'.C'
  print "Compiling Struct",tmpFileName,
  f = file(tmpFileName,'w')
  f.write(structString)
  f.close()
  ROOT.gROOT.ProcessLine('.L '+tmpFileName)
  exec("from ROOT import "+structName)
  exec("s = "+structName+"()")
#  os.system('rm '+tmpFileName)
  print " -> done."
  return s

def printHeader(s):
  print
  print wrapStr()
  print wrapStr("".join(" " for i in range(len(s))))
  print wrapStr(s)
  print wrapStr("".join(" " for i in range(len(s))))
  print wrapStr()
  print 

def readVar(v):  
  if not type(v)==type(""):
    print "Var",v
    raise Exception("Var not a string")
  try:
    if v.count(':'):
      stage1, stage2Name = v.split(":")
      stage1Name, tp = stage1.split('/')
      assert stage2Name.count('/')==0, "Found '/' after : in %s"%v
    else:
      stage1Name, tp = v.split('/')
      stage2Name = stage1Name
  except:
    raise Exception( "Var '"+v+"' not of the form 'var/type' or 'varStage1/type:varStage2'" )
     
  return {'stage1Name':stage1Name,'stage2Name':stage2Name,'type':tp}

def typeStr(t):
  assert type(t)==type("") and t.isalpha(), "Type '%s' not well formatted."%repr(t)
#  if t=='C':return 'TString' #Need to check this
  if t=='B':return 'Char_t'
  if t=='b':return 'UChar_t'
  if t=='S':return 'Short_t'
  if t=='s':return 'UShort_t'
  if t=='I':return 'Int_t'
  if t=='i':return 'UInt_t'
  if t=='F':return 'Float_t'
  if t=='D':return 'Double_t'
  if t=='L':return 'Long64_t'
  if t=='l':return 'ULong64_t'
  if t=='O':return 'Bool_t'
  raise Exception("Unknown type '"+t+"'.")

