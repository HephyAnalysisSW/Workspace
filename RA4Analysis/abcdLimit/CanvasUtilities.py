import ROOT

def getObjectsFromCanvas(canvas,rootClass,name=None):
  result = [ ]
  for obj in canvas.GetListOfPrimitives():
    if obj.InheritsFrom(rootClass):
      if name==None or obj.GetName()==name:
        result.append(obj)
  return result

def getObjectsFromDirectory(dir,rootClass,name=None):
  result = [ ]
  ROOT.gROOT.cd()
  for key in dir.GetListOfKeys():
    obj = key.ReadObj()
    if obj.InheritsFrom(rootClass):
      if name==None or obj.GetName()==name:
        result.append(obj)
  return result

def getObjectsFromContainer(container,rootClass,name=None):
  if container.InheritsFrom(ROOT.TVirtualPad.Class()):
    return getObjectsFromCanvas(container,rootClass,name=name)
  elif container.InheritsFrom(ROOT.TDirectory.Class()):
    return getObjectsFromDirectory(container,rootClass,name=name)
  return [ ]

def getObjectsFromContainerRecursive(container,rootClass,name=None):
  result = [ ]
  stack = [ container ]
  while stack:
    c = stack.pop()
    result.extend(getObjectsFromContainer(c,rootClass,name=name))
    dirs = getObjectsFromContainer(c,ROOT.TDirectory.Class())
    stack.extend(dirs)
    cnvs = getObjectsFromContainer(c,ROOT.TVirtualPad.Class())
    stack.extend(cnvs)
  return result
