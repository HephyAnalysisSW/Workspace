from Workspace.RA4Analysis.signalRegions import *

def filterParticles(l, values, attribute):
  for a in l:
    for v in values:
      if abs(a[attribute])==v: yield a

def dictDepth(d, depth=0):
  if not isinstance(d, dict) or not d:
    return depth
  return max(dictDepth(v, depth+1) for k, v in d.iteritems())

def addKey(d, newDict='deltaPhiCut'):
  for k, v in d.iteritems():
    if k == newDict:
      d = {d[k]:d}
      return d
    elif isinstance(v, dict):
      d[k] = addKey(v, newDict)
  return d

def getValErrString(val,err, precision=3):
  return str(round(val,precision))+' +/- '+str(round(err,precision))

def sign(a):
  return (a > 0) - (a < 0)

def setNiceBinLabel(hist, signalRegions=signalRegion3fb):
  i = 1
  for njb in sorted(signalRegions):
    for stb in sorted(signalRegions[njb]):
      for htb in sorted(signalRegions[njb][stb]):
        hist.GetXaxis().SetBinLabel(i,'#splitline{'+signalRegions[njb][stb][htb]['njet']+'}{#splitline{'+signalRegions[njb][stb][htb]['LT']+'}{'+signalRegions[njb][stb][htb]['HT']+'}}')
        i += 1

def createDictFromHist(hist, signalRegions):
  i = 1
  d = {}
  for njb in sorted(signalRegions):
    d[njb] = {}
    for stb in sorted(signalRegions[njb]):
      d[njb][stb] = {}
      for htb in sorted(signalRegions[njb][stb]):
        d[njb][stb][htb] = hist.GetBinContent(i)
        i += 1
  
  return d

def addDPhiCutDict(res, signalRegions):
  for njb in sorted(signalRegions):
    for stb in sorted(signalRegions[njb]):
      for htb in sorted(signalRegions[njb][stb]):
        res[njb][stb][htb]['deltaPhiCut'] = signalRegions[njb][stb][htb]['deltaPhi']
  return res

def sign(a):
  return (a > 0) - (a < 0)

def printMatrix(matrix, name='MATRIX', precision=5):
  a = matrix.GetNrows()
  b = matrix.GetNcols()
  fmt = ''
  for i in range(b+1):
    fmt += '{'+str(i)+':<12}'
  #rows = []
  rows = name + '\n\n'
  tup = (' ',)
  for i in range(b):
    tup += ('p'+str(i),)
  exec('row=fmt.format'+str(tup))
  rows += row +'\n'
  #print row
  for i in range(a):
    tup = ()
    tup += ('p'+str(i),)
    for j in range(b):
      tup += ("%0.2e"%matrix(i,j),)
    exec('row=fmt.format'+str(tup))
    rows += row + '\n'
    #print row
  return rows


