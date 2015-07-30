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
def createClassString(className, vars, vectors, nameKey, typeKey, stdVectors=False):
  classString =  "#ifndef __"+className+"__\n#define __"+className+'__\n\n#include<vector>\n#include<TMath.h>\n\n'
  classString += "class "+className+"{\n"
  classString += "public:\n"
  for var in vars:
    classString+="  "+typeStr(var[typeKey])+" "+var[nameKey]+";\n"
  for v in vectors:
    for var in v['vars']:
      if stdVectors:
        classString+="  std::vector<"+edmVecTypes[var[typeKey]]+"> "+var[nameKey]+";\n"
      else:
        classString+="  "+typeStr(var[typeKey])+" "+var[nameKey]+"["+str(v['nMax'])+"];\n"
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
  newClassName = className+'_'+uniqueFilename.replace('-','_')
  f.write(classString.replace(className, newClassName))
  f.close()
  ROOT.gROOT.ProcessLine('.L '+tmpFileName+'+')
  print "new Class Name" , newClassName
  exec("from ROOT import "+newClassName)
  exec("s = "+newClassName+"()")
#  os.system('rm '+tmpFileName)
  print " -> done."
  return s

def readVar(v, allowRenaming, isWritten, isRead, makeVecType=False):
  assert allowRenaming or not v.count(":"), "Renaming syntax not allowed here (var: %s )"%v
  nSlash = v.count('/')
  assert nSlash>0 and nSlash<=2, "Found %i '/' characters->Don't know what to do with %s."%(nSlash, v)
  if not type(v)==type(""):
    print "Var",v
    raise Exception("Var not a string")
  res={}
  if isRead:
    if v.count(':'):
      stage1 = v.split(":")[0]
    else:
      stage1 = v
    assert stage1.count('/')==1, "Frow %s want to read %s but did not find a slash in stage1 part. Syntax: 'stage1/typeStage1[:stage2/typeStage2] or stage1/typeStage1[:stage2/typeStage2/default]"%(v, stage1)
    defString=None
    if stage1.count('/')==1:
      stage1Name, stage1Type = stage1.split('/')
    else:
      stage1Name, stage1Type, defString = stage1.split('/')
    res['stage1Type']=stage1Type
    if makeVecType:
      res['stage1Type']='vector<'+res['stage1Type']+'>'
    res['stage1Name']=stage1Name
    if defString:
      res['default']=defString
    else:
      res['default']=typeDefaults(stage1Type)
  if isWritten:
    if v.count(':'):
      stage2 = v.split(":")[1]
    else:
      stage2 = v
    assert stage2.count('/')==1 or stage2.count('/')==2, "Frow %s want to write %s but did not find one or two '/' in stage2part. Syntax: 'stage1/typestage1[:stage2/typeStage2] or stage1/typestage1[:stage2/typeStage2/default]"%(v, stage2)
    defString=None
    if stage2.count('/')==1:
      stage2Name, stage2Type = stage2.split('/')
    else:
      stage2Name, stage2Type, defString = stage2.split('/')
    res['stage2Type']=stage2Type
    res['stage2Name']=stage2Name
    if defString:
      res['default']=defString
    else:
      res['default']=typeDefaults(stage2Type)
  return res
  

def typeStr(t):
  assert type(t)==type("") and t.isalpha(), "Type '%s' not well formatted."%repr(t)
#  if t=='C':return 'TString' #Need to check this
#  if t=='B':return 'Char_t'
  if t=='b':return 'UChar_t'
  if t=='S':return 'Short_t'
  if t=='s':return 'UShort_t'
  if t=='I' or t=='int':return 'Int_t'
  if t=='i':return 'UInt_t'
  if t=='F' or t=='float':return 'Float_t'
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
  if s=='I' or s=='int':return '-1'
  if s=='i':return '0'
  if s=='F' or s=='float':return 'TMath::QuietNaN()'
  if s=='D':return 'TMath::QuietNaN()'
  if s=='L':return '-1'
  if s=='l':return '-1'
  if s=='O':return '0'
  raise Exception("Unknown type '"+s+"'.")

