import ROOT

from Workspace.HEPHYPythonTools.helpers import wrapStr

def printHeader(s):
  print
  print wrapStr()
  print wrapStr("".join(" " for i in range(len(s))))
  print wrapStr(s)
  print wrapStr("".join(" " for i in range(len(s))))
  print wrapStr()
  print 

#def typeFromName(name):
#  assert type(name)==type(""), "Type of branchname is %s, should be string "%str(type(name))
#  try:
#    n=name.split('_')[0][:-1]
#    assert n=='float' or n=='int', "From branchname %s I deduce the type %s -> not understood."%(name, n)
#  except:
#    raise Exception("Can not find type from branchname "+name)
edmVecTypes = {'Float_t':'float', 'Int_t':'int', 'F':'float', 'I':'int'} 
def createClassString(className, vars, vectors, nameKey, stdVectors=False):
  classString =  "#ifndef __"+className+"__\n#define __"+className+'__\n\n#include<vector>\n#include<TMath.h>\n\n'
  classString += "class "+className+"{\n"
  classString += "public:\n"
  for var in vars:
    classString+="  "+typeStr(var['type'])+" "+var[nameKey]+";\n"
  for v in vectors:
    for var in v['vars']:
      if stdVectors:
        classString+="  std::vector<"+edmVecTypes[var['type']]+"> "+var[nameKey]+";\n"
      else:
        classString+="  "+typeStr(var['type'])+" "+var[nameKey]+"["+str(v['nMax'])+"];\n"
  classString +="\n  void init(){\n"
  for var in vars:
    classString+="    "+var[nameKey]+" = "+var['default']+";\n"
  if stdVectors:
    for v in vectors:
      for var in v['vars']:
        classString+="    "+var[nameKey]+".clear();\n"
  else:
    for v in vectors:
      classString+="    for(UInt_t i=0;i<"+str(v['nMax'])+";i++){\n"
      for var in v['vars']:
        classString+="      "+var[nameKey]+"[i]="+var['default']+";\n"
      classString+="    };\n"
  classString +="  };\n"
  classString +="};\n"
  classString +="#endif"
  return classString

def compileClass(className, classString, tmpDir):
  import uuid, os
  os.system('mkdir -p '+tmpDir)
  uniqueFilename = str(uuid.uuid4())
  tmpFileName = tmpDir+'/'+uniqueFilename+'.C'
  print "Compiling class",tmpFileName,
  f = file(tmpFileName,'w')
  f.write(classString)
  f.close()
  ROOT.gROOT.ProcessLine('.L '+tmpFileName+'+')
  exec("from ROOT import "+className)
  exec("s = "+className+"()")
#  os.system('rm '+tmpFileName)
  print " -> done."
  return s

def readVar(v, allowRenaming, isWritten, isRead):
  assert allowRenaming or not v.count(":"), "Renaming syntax not allowed here (var: %s )"%v
  nSlash = v.count('/')
  assert nSlash>0 and nSlash<=2, "Found %i '/' characters->Don't know what to do with %s."%(nSlash, v)
  if not type(v)==type(""):
    print "Var",v
    raise Exception("Var not a string")
  try:
    if v.count(':'):
      stage1, stage2Name = v.split(":")
      assert stage2Name.count('/')==0, "Found '/' after : in %s"%v
    else:
      stage1 = v
      stage2Name = None
    nSlash =  stage1.count('/')
    if nSlash ==2: 
      stage1Name, tp, defStr = stage1.split('/')
    elif nSlash == 1:
      stage1Name, tp = stage1.split('/')
      defStr = typeDefaults(tp)
    else:
      raise Exception("Should never happen :-). No '/' found.")
    if not stage2Name:stage2Name=stage1Name
  except:
    raise Exception( "Var '"+v+"' not of the form 'var/type', '/var/type/default', 'varStage1/type:varStage2, or  'varStage1/type/default:varStage2'" )
  res={'type':tp, 'default':defStr}
  if isWritten: 
    res['stage2Name']=stage2Name
  if isRead:
    res['stage1Name']=stage1Name
  return res
  

def typeStr(t):
  assert type(t)==type("") and t.isalpha(), "Type '%s' not well formatted."%repr(t)
#  if t=='C':return 'TString' #Need to check this
#  if t=='B':return 'Char_t'
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

def typeDefaults(s):
#  if t=='C':return 'TString' #Need to check this
#  if t=='B':return '' #Need to check this
  if s=='b':return '0'
  if s=='S':return '-1'
  if s=='s':return '0'
  if s=='I':return '-1'
  if s=='i':return '0'
  if s=='F':return 'TMath::QuietNaN()'
  if s=='D':return 'TMath::QuietNaN()'
  if s=='L':return '-1'
  if s=='l':return '-1'
  if s=='O':return '0'
  raise Exception("Unknown type '"+s+"'.")

