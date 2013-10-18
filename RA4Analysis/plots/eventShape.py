import ROOT
from math import *

def px(obj):
  return obj['pt'] * cos(obj['phi'])

def py(obj):
  return obj['pt'] * sin(obj['phi'])

def pz(obj):
  return obj['pt'] * sinh(obj['eta'])

def psquare(x, y, z):
  return (x * x) + (y * y) + (z * z)


def sphericity(jets):
  msum = ROOT.TMatrixDSym(3)
  p2sum = 0

  for i in range(3):
    for j in range(3):
      msum[i][j] = 0

  for obj in jets:
    x = px(obj)
    y = py(obj)
    z = pz(obj)

    p2sum += psquare(x, y, z)

    msum[0][0] += x * x
    msum[0][1] += x * y
    msum[0][2] += x * z

    msum[1][0] += y * x 
    msum[1][1] += y * y
    msum[1][2] += y * z

    msum[2][0] += z * x
    msum[2][1] += z * y
    msum[2][2] += z * z
     
##    s = ROOT.TMatrixD(s,ROOT.kPlus,a)
#    for i in range(3):
#      for j in range(3):
#        msum[i][j] = msum[i][j] + a[i][j]

  for n in range(3):
    for m in range(3):
      msum[n][m] = msum[n][m] / p2sum

  eigenproblem = ROOT.TMatrixDSymEigen(msum)
  eigenvalue = eigenproblem.GetEigenValues()
  if len(jets)>2 and (eigenvalue[0] < 0 or eigenvalue[1] < 0 or eigenvalue[2] < 0):
    print '[Sphericity], Warning: eigenvalue < 0, len:',len(jets)
    print eigenvalue[0], eigenvalue[1] , eigenvalue[2]
  s = ((eigenvalue[2] + eigenvalue[1]) * 3) / 2

  return {'sphericity':s, "eigenvalues":eigenvalue}

def circularity(eigenvalues3D):
  c = (2 * eigenvalues3D[2]) / (eigenvalues3D[1] + eigenvalues3D[2])
  return c

def circularity2D(jets):
  msum = ROOT.TMatrixDSym(2)
  for i in range(2):
    for j in range(2):
      msum[i][j] = 0

  p2sum = 0

  for obj in jets:
    x = px(obj)
    y = py(obj)
    p2sum += (x * x) + (y * y) 
    msum[0][0] += x * x
    msum[0][1] += x * y
    msum[1][0] += y * x
    msum[1][1] += y * y

  for n in range(2):
    for m in range(2):
      msum[n][m] = msum[n][m] / p2sum

  eigenproblem = ROOT.TMatrixDSymEigen(msum)
  eigenvalue = eigenproblem.GetEigenValues()
  if eigenvalue[0] < 0 or eigenvalue[1] < 0:
    print '[Sphericity], Warning: eigenvalue < 0, len:',len(jets)
    print eigenvalue[0], eigenvalue[1] 
  c2D = (2 * eigenvalue[1]) / (eigenvalue[0] + eigenvalue[1])

  return c2D

#def WT(obj):
#  for i in obj[0]:
#    pt = obj[0][i]['pt']
#    psum += pt
#
#  for i in obj[0]:
#    pt1 = obj[0][i]['pt']
#    for j in obj[0]:
#      pt2 = obj[0][j]['pt']
#      wt = (pt1 * pt2) / (psum * psum)
#  return wt

#def theta(obj):
#  return 2 * atan(exp(-(obj['eta'])))

def foxWolframMoments(jets):
  psum = 0  
  for obj in jets:
    pt = obj['pt']
    psum += pt
    
#  ht0 = 0
  ht1 = 0
  ht2 = 0
  ht3 = 0
  ht4 = 0

  for obj1 in jets:
    pt1 = obj1['pt']
    for obj2 in jets:
      pt2 = obj2['pt']
      wt = (pt1 * pt2) / (psum * psum)
      ctheta = cos(obj1['phi'] - obj2['phi'])      
#      P0 = 1
      P1 = ctheta
      P2 = ((3 * ctheta * ctheta) - 1) / 2. 
      P3 = ((5 * ctheta * ctheta * ctheta) - (3 * ctheta)) / 2. 
      P4 = ((35 * ctheta * ctheta * ctheta * ctheta) - (30 * ctheta * ctheta) + 3) / 8.
 
#      ht0 += wt * P0
      ht1 += wt * P1
      ht2 += wt * P2
      ht3 += wt * P3
      ht4 += wt * P4

#  return  {"FWMT0":ht0,"FWMT1":ht1,"FWMT2":ht2,"FWMT3":ht3,"FWMT4":ht4}
  return  {"FWMT1":ht1,"FWMT2":ht2,"FWMT3":ht3,"FWMT4":ht4}


