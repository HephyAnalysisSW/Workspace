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

