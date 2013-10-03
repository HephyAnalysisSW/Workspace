import ROOT
import copy, sys, os
import pickle
from math import *
from simplePlotsCommon import *

ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
#ROOT.gStyle.SetPadRightMargin(0.10);
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()

ROOT.tdrStyle.SetPadRightMargin(0.16)
if not ROOT.__dict__.has_key("useNiceColorPalette"):
  ROOT.gROOT.ProcessLine(".L ../scripts/useNiceColorPalette.C")

ROOT.useNiceColorPalette(255)

def dPhi(t1Phi, t2Phi):
  dphi = t2Phi - t1Phi
  if dphi > pi:
    dphi -= 2.0*pi
  elif dphi < -pi:
    dphi += 2.0*pi

  return abs(dphi)

def getLepVar(var):
  cvar =  "((top1WDaughter0Pdg>=10)*("+var.replace("topL", "top1").replace("topH", "top0")+")+(top0WDaughter0Pdg>=10)*("+var.replace("topL", "top0").replace("topH","top1")+"))"
#  print cvar
  return cvar

def matrixmult (A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    if cols_A != rows_B:
      print "Cannot multiply the two matrices. Incorrect dimensions."
      return
    C = [[0 for row in range(cols_B)] for col in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k]*B[k][j]
    return C

#doubleMuCut = "( abs(top0WDaughter0Pdg) + abs(top0WDaughter1Pdg) == 13 + 14 && abs(top1WDaughter0Pdg) + abs(top1WDaughter1Pdg) == 13 + 14)&&met>150&&ht>350"
#doubleMuCut = "( abs(top0WDaughter0Pdg) + abs(top0WDaughter1Pdg) == 13 + 14 && abs(top1WDaughter0Pdg) + abs(top1WDaughter1Pdg) == 13 + 14)&&met>100&&ht>100"

Cut = "(abs(top0WDaughter0Pdg)>=11&&abs(top0WDaughter0Pdg)<=14 && abs(top1WDaughter0Pdg)>=11&&abs(top1WDaughter0Pdg)<=14)&&ht>100" # get electrons and muons

c = ROOT.TChain("Events")
#c.Add("/data/schoef/pat_120925/mc8TeV/8TeV-TTJets/*.root")
#c.Add("/data/schoef/pat_120925/mc8TeV/8TeV-TTJets/histo_1*.root")
#c.Add("/data/schoef/pat_120925/mc8TeV/8TeV-TTJets-powheg-v1+2/histo_1*.root")
#c.Add("/data/schoef/pat_120925/mc8TeV/8TeV-TTJets-powheg-v1+2/*.root")

sampleDir = "/data/schoef/pat_120925/mc8TeV/8TeV-TTJets-powheg-v1+2/"
#sampleDir = '/data/mhickel/pat_120917/mc8TeV/8TeV-TTTo2L2Nu2B/' # big sample

outputPath = '/data/jkancsar/topDiLepton/fork/'

minF = 0
maxF = 3500 
if len(sys.argv)>2:
  minF = int(sys.argv[1])
  maxF = int(sys.argv[2])
  print "Adding ",sampleDir, "from >=", minF, "to <",maxF

filelist=os.listdir(sampleDir)

for thisfile in filelist:
 if os.path.isfile(sampleDir+thisfile) and thisfile[-5:]==".root":
    num = int(thisfile.split("_")[1])
    if num>=minF and num<maxF:
        c.Add(sampleDir+thisfile)
#        print "Added", sampleDir+thisfile

allEvents = []
Event = {}

#mW=79.8756213803
#mt=172.283184949
mW = 80.4
mW2 =mW**2
mt = 173.2
mt2=mt**2

swapBQuarks = False

def cosPhiBar(cosThetaYNu, cosThetaLNu, cosThetaYL):
  res=float('nan')
  try:
    res = (cosThetaYNu - cosThetaLNu *cosThetaYL)/(sqrt(1. - cosThetaYL*cosThetaYL)*sqrt(1. - cosThetaLNu*cosThetaLNu))
  except:
    pass
  if abs(res)>1:
    return float('nan')
  return res

def nNuPrime(cosThetaYNu, cosThetaLNu, cosThetaYL, sign):
  cPhiBar = cosPhiBar(cosThetaYNu, cosThetaLNu, cosThetaYL)
  if not cPhiBar<float('inf'):
    return [[float('nan')], [float('nan')], [float('nan')]]
  return [[cPhiBar*sqrt(1.-cosThetaLNu*cosThetaLNu)],[sign*sqrt(1.-cPhiBar*cPhiBar)*sqrt(1.-cosThetaLNu*cosThetaLNu)],[cosThetaLNu]]


n=50
#c.Draw(">>eList",doubleMuCut)
c.Draw(">>eList",Cut)
eList = ROOT.gDirectory.Get("eList")
nevents = eList.GetN() 
#chi2 = ROOT.TH2F("chi2", "chi2", n+1,-1-.5/n,1+.5/n,n+1,-1-.5/n,1+.5/n)

nEvents = 10
print 'Number of Events:', nevents

#for i in range(min(nEvents, nevents)):  #start
for i in range(0, nevents):  #start
  c.GetEntry(eList.GetEntry(i))
  t0d0pdg = getVarValue(c, "top0WDaughter0Pdg")
  t1d0pdg = getVarValue(c, "top1WDaughter0Pdg")
  l1ID=-1                                                   #Identify lepton daughter
  l2ID=-1
  if abs(t0d0pdg) == 13 or abs(t0d0pdg) == 11:  # if muon or electron
    l1ID=0
  else:
    l1ID=1
  if abs(t1d0pdg) == 13 or abs(t1d0pdg) == 11:
    l2ID=0
  else:
    l2ID=1

#  t0d1pdg = getVarValue(c, "top0WDaughter1Pdg")
#  t1d1pdg = getVarValue(c, "top1WDaughter1Pdg")
#  print 'W1 ', t0d0pdg, t0d1pdg, 'W2 ', t1d0pdg, t1d1pdg

  t1px = getVarValue(c, 'top0Px')
  t1py = getVarValue(c, 'top0Py')
  t1pz = getVarValue(c, 'top0Pz')
  t1p = sqrt(t1px*t1px + t1py*t1py + t1pz*t1pz)
  t1eta = acosh(t1p/sqrt(t1px*t1px + t1py*t1py))*t1pz/(sqrt(t1pz*t1pz))
  t1Phi = atan2(t1py, t1px)
  cosT1Theta = t1pz/t1p

  t2px = getVarValue(c, 'top1Px')
  t2py = getVarValue(c, 'top1Py')
  t2pz = getVarValue(c, 'top1Pz')
  t2p = sqrt(t2px*t2px + t2py*t2py + t2pz*t2pz)
  t2eta = acosh(t2p/sqrt(t2px*t2px + t2py*t2py))*t2pz/(sqrt(t2pz*t2pz))
  t2Phi = atan2(t2py, t2px)
  cosT2Theta = t2pz/t2p

  l1px = getVarValue(c, "top0WDaughter"+str(l1ID)+"Px")   #Get lepton and b components
  l1py = getVarValue(c, "top0WDaughter"+str(l1ID)+"Py")
  l1pz = getVarValue(c, "top0WDaughter"+str(l1ID)+"Pz")
  l1p = sqrt(l1px*l1px + l1py*l1py + l1pz*l1pz)           #calc. lepton and b 3 momenta abs. val.
  l1pt  = sqrt(l1px**2 + l1py**2)
  l1Phi = atan2(l1py, l1px)
  cosL1Phi = cos(l1Phi)
  sinL1Phi = sin(l1Phi)
  cosL1Theta = l1pz/l1p
  sinL1Theta = sqrt(1 - cosL1Theta**2)
  l1eta = acosh(l1p/sqrt(l1px**2 + l1py**2))*l1pz/(sqrt(l1pz**2))

  nu1pxTrue = getVarValue(c, "top0WDaughter"+str(1-l1ID)+"Px")   #Get lepton and b components
  nu1pyTrue = getVarValue(c, "top0WDaughter"+str(1-l1ID)+"Py")
  nu1pzTrue = getVarValue(c, "top0WDaughter"+str(1-l1ID)+"Pz")
  nu1pTrue = sqrt(nu1pxTrue*nu1pxTrue + nu1pyTrue*nu1pyTrue + nu1pzTrue*nu1pzTrue)
  nu1PhiTrue = atan2(nu1pyTrue, nu1pxTrue)
  cosNu1Phi = cos(nu1PhiTrue)
  sinNu1Phi = sin(nu1PhiTrue)
  cosNu1ThetaTrue = nu1pzTrue/nu1pTrue
  sinNu1ThetaTrue = sqrt(1 - cosNu1ThetaTrue**2)
  cosLNu1True = (nu1pxTrue*l1px + nu1pyTrue*l1py + nu1pzTrue*l1pz)/(l1p*nu1pTrue)

  l2px = getVarValue(c, "top1WDaughter"+str(l2ID)+"Px")
  l2py = getVarValue(c, "top1WDaughter"+str(l2ID)+"Py")
  l2pz = getVarValue(c, "top1WDaughter"+str(l2ID)+"Pz")
  l2p = sqrt(l2px*l2px + l2py*l2py + l2pz*l2pz)
  l2pt  = sqrt(l2px**2 + l2py**2)
  l2Phi = atan2(l2py, l2px)
  cosL2Phi = cos(l2Phi)
  sinL2Phi = sin(l2Phi)
  cosL2Theta = l2pz/l2p
  sinL2Theta = sqrt(1 - cosL2Theta*cosL2Theta)
  l2eta = acosh(l2p/sqrt(l2px**2 + l2py**2))*l2pz/(sqrt(l2pz**2))

  nu2pxTrue = getVarValue(c, "top1WDaughter"+str(1-l2ID)+"Px")   #Get lepton and b components
  nu2pyTrue = getVarValue(c, "top1WDaughter"+str(1-l2ID)+"Py")
  nu2pzTrue = getVarValue(c, "top1WDaughter"+str(1-l2ID)+"Pz")
  nu2pTrue = sqrt(nu2pxTrue*nu2pxTrue + nu2pyTrue*nu2pyTrue + nu2pzTrue*nu2pzTrue)
  nu2PhiTrue = atan2(nu2pyTrue, nu2pxTrue)
  cosNu2Phi = cos(nu2PhiTrue)
  sinNu2Phi = sin(nu2PhiTrue)
  cosNu2ThetaTrue = nu2pzTrue/nu2pTrue
  sinNu2ThetaTrue = sqrt(1 - cosNu2ThetaTrue**2)
  cosLNu2True = (nu2pxTrue*l2px + nu2pyTrue*l2py + nu2pzTrue*l2pz)/(l2p*nu2pTrue)

#  print getVarValue(c, "top0WDaughter"+str(1)+"Pdg"), getVarValue(c, "top0WDaughter"+str(1-l1ID)+"Pdg"),getVarValue(c, "top1WDaughter"+str(l2ID)+"Pdg"), getVarValue(c, "top1WDaughter"+str(1-l2ID)+"Pdg")

  bID = 0
  if swapBQuarks:
    bID=1
  b1px = getVarValue(c, "top"+str(bID)+"bPx")
  b1py = getVarValue(c, "top"+str(bID)+"bPy")
  b1pz = getVarValue(c, "top"+str(bID)+"bPz")
  b1p = sqrt(b1px*b1px + b1py*b1py + b1pz*b1pz)
  b2px = getVarValue(c, "top"+str(1-bID)+"bPx")
  b2py = getVarValue(c, "top"+str(1-bID)+"bPy")
  b2pz = getVarValue(c, "top"+str(1-bID)+"bPz")
  b2p = sqrt(b2px*b2px + b2py*b2py + b2pz*b2pz)
  #  print l1ID, l2ID, l1px, l1py, l1pz, l2px, l2py, l2pz 
  #  print b1px, b1py, b1pz, b2px, b2py, b2pz 

  MExGen = getVarValue(c, "genmetpx") 
  MEyGen = getVarValue(c, "genmetpy")
  MEx = getVarValue(c, "metpx") 
  MEy = getVarValue(c, "metpy")
  MExTrue = nu1pxTrue + nu2pxTrue 
  MEyTrue = nu1pyTrue + nu2pyTrue 

  METGen = sqrt(MExGen**2 + MEyGen**2)
  METTrue = sqrt(MExTrue**2 + MEyTrue**2)
  
  y1E  = l1p  + b1p 
  y1px = l1px + b1px
  y1py = l1py + b1py
  y1pz = l1pz + b1pz
  y1p = sqrt(y1px*y1px + y1py*y1py + y1pz*y1pz)           
  y1Phi = atan2(y1py, y1px)
  cosY1Phi = cos(y1Phi)
  sinY1Phi = sin(y1Phi)
  cosY1Theta = y1pz/y1p
  sinY1Theta = sqrt(1 - cosY1Theta*cosY1Theta) 
  y1sq =  y1E*y1E - y1px*y1px - y1py*y1py - y1pz*y1pz
  cosYNu1True = (nu1pxTrue*y1px + nu1pyTrue*y1py + nu1pzTrue*y1pz)/(y1p*nu1pTrue)

  y2E  = l2p  + b2p 
  y2px = l2px + b2px
  y2py = l2py + b2py
  y2pz = l2pz + b2pz
  y2p = sqrt(y2px*y2px + y2py*y2py + y2pz*y2pz)           
  y2Phi = atan2(y2py, y2px)
  cosY2Phi = cos(y2Phi)
  sinY2Phi = sin(y2Phi)
  cosY2Theta = y2pz/y2p
  sinY2Theta = sqrt(1-cosY2Theta*cosY2Theta) 
  y2sq =  y2E*y2E - y2px*y2px - y2py*y2py - y2pz*y2pz
  cosYNu2True = (nu2pxTrue*y2px + nu2pyTrue*y2py + nu2pzTrue*y2pz)/(y2p*nu2pTrue)

  mW2sys1 = (l1p+nu1pTrue)**2 - (l1px + nu1pxTrue)**2 - (l1py + nu1pyTrue)**2 - (l1pz + nu1pzTrue)**2
  mW2sys2 = (l2p+nu2pTrue)**2 - (l2px + nu2pxTrue)**2 - (l2py + nu2pyTrue)**2 - (l2pz + nu2pzTrue)**2
  mT2sys1 = (y1E+nu1pTrue)**2 - (y1px + nu1pxTrue)**2 - (y1py + nu1pyTrue)**2 - (y1pz + nu1pzTrue)**2
  mT2sys2 = (y2E+nu2pTrue)**2 - (y2px + nu2pxTrue)**2 - (y2py + nu2pyTrue)**2 - (y2pz + nu2pzTrue)**2
  
  W1ratio = sqrt(mW2sys1/mW2)
  W2ratio = sqrt(mW2sys2/mW2)
  T1ratio = sqrt(mT2sys2/mt2)
  T2ratio = sqrt(mT2sys2/mt2)

# ----------------- on-Shell +-10% ------------------------------------------------------------
#  if  (W1ratio > 1.1 or W1ratio < 0.9) or (W2ratio > 1.1 or W2ratio < 0.9):  # W off-shell
#    print 'Event', i, ':', '\tW:', round(W1ratio,3), round(W2ratio,3), '\tkicked'
#    continue
#  elif (T1ratio > 1.1 or T1ratio < 0.9) or (T2ratio > 1.1 or T2ratio < 0.9): # T off-shell
#    print 'Event', i, ':', '\tT:', round(T1ratio,3), round(T2ratio,3), '\tkicked'
#    continue
# ----------------------------------------------------------------------------------------------
  print 'Event', i, ':', '\tW:', round(sqrt(mW2sys1/mW2),3) , round(sqrt(mW2sys2/mW2), 3), '\tT:', round(sqrt(mT2sys1/mt2), 3), round(sqrt(mT2sys2/mt2), 3), '\tGenmet/TrueMet:', METGen/METTrue


  #  print .5*(mt**2 - y1sq) , .5*(mt**2 - y2sq)
  if y1sq > mt**2 or y2sq > mt**2:            #no real solutions possible in this case
    print "No real solution"
    continue

  cosYL1 = (y1px*l1px + y1py*l1py + y1pz*l1pz)/(y1p*l1p) 
  cosYL2 = (y2px*l2px + y2py*l2py + y2pz*l2pz)/(y2p*l2p)

  alpha1 = atan2(sinY1Theta*(cosY1Phi*sinL1Phi - cosL1Phi*sinY1Phi), ( - cosY1Theta*sinL1Theta + cosL1Theta*sinY1Theta*(cosL1Phi*cosY1Phi + sinL1Phi*sinY1Phi)))
#  if  - cosY1Theta*sinL1Theta + cosL1Theta*sinY1Theta*(cosL1Phi*cosY1Phi + sinL1Phi*sinY1Phi)<0:
#      tanAlpha1*=-1
  cosAlpha1 = cos(alpha1) 
  sinAlpha1 = sin(alpha1) 

  alpha2 = atan2(sinY2Theta*(cosY2Phi*sinL2Phi - cosL2Phi*sinY2Phi), ( - cosY2Theta*sinL2Theta + cosL2Theta*sinY2Theta*(cosL2Phi*cosY2Phi + sinL2Phi*sinY2Phi)))
#  if  - cosY2Theta*sinL2Theta + cosL2Theta*sinY2Theta*(cosL2Phi*cosY2Phi + sinL2Phi*sinY2Phi)<0:
#      tanAlpha2*=-1
  cosAlpha2 = cos(alpha2) 
  sinAlpha2 = sin(alpha2) 

  #  print sinAlpha1, sinAlpha2

  M1 =  [ [cosAlpha1*cosL1Theta*cosL1Phi + sinAlpha1*sinL1Phi, -(cosL1Phi*sinAlpha1) + cosAlpha1*cosL1Theta*sinL1Phi, -(cosAlpha1*sinL1Theta)],\
          [-(cosL1Theta*cosL1Phi*sinAlpha1) + cosAlpha1*sinL1Phi, -(cosAlpha1*cosL1Phi) - cosL1Theta*sinAlpha1*sinL1Phi, sinAlpha1*sinL1Theta], 
          [cosL1Phi*sinL1Theta, sinL1Theta*sinL1Phi, cosL1Theta ] ]
  M2 =  [ [cosAlpha2*cosL2Theta*cosL2Phi + sinAlpha2*sinL2Phi, -(cosL2Phi*sinAlpha2) + cosAlpha2*cosL2Theta*sinL2Phi, -(cosAlpha2*sinL2Theta)],\
          [-(cosL2Theta*cosL2Phi*sinAlpha2) + cosAlpha2*sinL2Phi, -(cosAlpha2*cosL2Phi) - cosL2Theta*sinAlpha2*sinL2Phi, sinAlpha2*sinL2Theta], 
          [cosL2Phi*sinL2Theta, sinL2Theta*sinL2Phi, cosL2Theta ] ]
#  print matrixmult(M1, [[sinL1Theta*cosL1Phi],[sinL1Theta*sinL1Phi],[cosL1Theta]]) 
#  print matrixmult(M1, [[sinY1Theta*cosY1Phi],[sinY1Theta*sinY1Phi],[cosY1Theta]]), sqrt(1.-cosYL1**2), cosYL1
#  print matrixmult(M2, [[sinL2Theta*cosL2Phi],[sinL2Theta*sinL2Phi],[cosL2Theta]]) 
#  print matrixmult(M2, [[sinY2Theta*cosY2Phi],[sinY2Theta*sinY2Phi],[cosY2Theta]]) , sqrt(1.-cosYL2**2), cosYL2
  M1Transposed = [\
      [cosAlpha1*cosL1Theta*cosL1Phi + sinAlpha1*sinL1Phi, -(cosL1Theta*cosL1Phi*sinAlpha1) + cosAlpha1*sinL1Phi, cosL1Phi*sinL1Theta],
      [-(cosL1Phi*sinAlpha1) + cosAlpha1*cosL1Theta*sinL1Phi,  -(cosAlpha1*cosL1Phi) - cosL1Theta*sinAlpha1*sinL1Phi, sinL1Theta*sinL1Phi],
      [-(cosAlpha1*sinL1Theta), sinAlpha1*sinL1Theta, cosL1Theta]]
  M2Transposed = [\
      [cosAlpha2*cosL2Theta*cosL2Phi + sinAlpha2*sinL2Phi, -(cosL2Theta*cosL2Phi*sinAlpha2) + cosAlpha2*sinL2Phi, cosL2Phi*sinL2Theta],
      [-(cosL2Phi*sinAlpha2) + cosAlpha2*cosL2Theta*sinL2Phi,  -(cosAlpha2*cosL2Phi) - cosL2Theta*sinAlpha2*sinL2Phi, sinL2Theta*sinL2Phi],
      [-(cosAlpha2*sinL2Theta), sinAlpha2*sinL2Theta, cosL2Theta]]
#  print matrixmult(M1, M1Transposed)
#  print matrixmult(M2, M2Transposed)

  #calculate the borders where cosLNuTheta1,2 is real
  a1 = (mt2 - y1sq)*(mt2 - y1sq)*l1p*l1p + y1E*mW2*mW2*y1p*cosYL1 - (mt2 - y1sq)*mW2*l1p*(y1E + y1p*cosYL1)
  b1 = float('nan')
  try:
    b1=mW*mW2*y1p*sqrt(-y1E*y1E*mW2 + 2*y1E*(mt2 - y1sq)*l1p + mW2*y1p*y1p - 2*(mt2 - y1sq)*l1p*y1p*cosYL1)*sqrt(1.-cosYL1*cosYL1)
  except:
    pass
    print "No real solution (b1)"
    continue
  den1 = (mt2 - y1sq)*(mt2 - y1sq)*l1p*l1p + mW2*mW2*y1p*y1p - 2*(mt2 - y1sq)*mW2*l1p*y1p*cosYL1

  a2 = (mt2 - y2sq)*(mt2 - y2sq)*l2p*l2p + y2E*mW2*mW2*y2p*cosYL2 - (mt2 - y2sq)*mW2*l2p*(y2E + y2p*cosYL2)
  b2 = float('nan')
  try:
    b2 = mW*mW2*y2p*sqrt(-y2E*y2E*mW2 + 2*y2E*(mt2 - y2sq)*l2p + mW2*y2p*y2p - 2*(mt2 - y2sq)*l2p*y2p*cosYL2)*sqrt(1.-cosYL2*cosYL2)
  except:
    pass
    print "No real solution (b2)"
    continue
  den2 = (mt2 - y2sq)*(mt2 - y2sq)*l2p*l2p + mW2*mW2*y2p*y2p - 2*(mt2 - y2sq)*mW2*l2p*y2p*cosYL2

  line1 = ROOT.TPolyLine(1)
  line2 = ROOT.TPolyLine(1)
  line3 = ROOT.TPolyLine(1)
  line4 = ROOT.TPolyLine(1)
  line1.SetPoint(0 , (a1+b1)/den1, -1)
  line1.SetPoint(1 , (a1+b1)/den1,  1)
  line2.SetPoint(0 , (a1-b1)/den1, -1)
  line2.SetPoint(1 , (a1-b1)/den1,  1)
  line3.SetPoint(0, -1,(a2+b2)/den2 ) 
  line3.SetPoint(1,  1,(a2+b2)/den2 )
  line4.SetPoint(0, -1,(a2-b2)/den2 )
  line4.SetPoint(1,  1,(a2-b2)/den2 )

  trueAngles = ROOT.TGraph(1)
  trueAngles.SetPoint(0, cosLNu1True, cosLNu2True )

  cosThetaLNu1Min = 0
  cosThetaLNu2Min = 0

  minText = ROOT.TLatex()
  minText.SetNDC(0)
  minText.SetTextSize(0.02)

  minAngles = ROOT.TGraph(1)

  fourEvents = []
  for sign1 in [+1, -1]:
    for sign2 in [+1, -1]:
      chi2Min = 10**4
      #chi2.Reset()
      for ith1 in range(n+1): #FIXME
        cosThetaLNu1 = -1 + 2.*ith1/float(n)  
        for ith2 in range(n): #FIXME
          cosThetaLNu2 = -1 + 2.*ith2/float(n)  
          cosThetaYNu1 = y1E/y1p*(1. - l1p*(mt**2 - y1sq)/(y1E*mW**2)*(1-cosThetaLNu1))
          cosThetaYNu2 = y2E/y2p*(1. - l2p*(mt**2 - y2sq)/(y2E*mW**2)*(1-cosThetaLNu2))
          chi2Value = float('nan')
          if abs(cosThetaYNu1)<=1. and abs(cosThetaLNu1)<=1. and abs(cosThetaYNu2)<1. and abs(cosThetaLNu2)<1.:
            nu1p = .5*mW**2/(l1p*(1. - cosThetaLNu1))
            nu2p = .5*mW**2/(l2p*(1. - cosThetaLNu2))
            nNu1Prime = nNuPrime(cosThetaYNu = cosThetaYNu1, cosThetaLNu = cosThetaLNu1, cosThetaYL = cosYL1, sign = sign1)
            nNu2Prime = nNuPrime(cosThetaYNu = cosThetaYNu2, cosThetaLNu = cosThetaLNu2, cosThetaYL = cosYL2, sign = sign2)
            nNu1 = matrixmult(M1Transposed, nNu1Prime) 
            nNu2 = matrixmult(M2Transposed, nNu2Prime)
#            print sign1, sign2
            rec_cosThetaLNu1 = (nNu1[0][0]*l1px + nNu1[1][0]*l1py + nNu1[2][0]*l1pz)/l1p
            rec_cosThetaYNu1 = (nNu1[0][0]*y1px + nNu1[1][0]*y1py + nNu1[2][0]*y1pz)/y1p
            rec_cosThetaLNu2 = (nNu2[0][0]*l2px + nNu2[1][0]*l2py + nNu2[2][0]*l2pz)/l2p
            rec_cosThetaYNu2 = (nNu2[0][0]*y2px + nNu2[1][0]*y2py + nNu2[2][0]*y2pz)/y2p
            if abs(rec_cosThetaLNu1 - cosThetaLNu1)>10**(-4):print rec_cosThetaLNu1, cosThetaLNu1
            if abs(rec_cosThetaYNu1 - cosThetaYNu1)>10**(-4):print rec_cosThetaYNu1, cosThetaYNu1
            if abs(rec_cosThetaLNu2 - cosThetaLNu2)>10**(-4):print rec_cosThetaLNu2, cosThetaLNu2
            if abs(rec_cosThetaYNu2 - cosThetaYNu2)>10**(-4):print rec_cosThetaYNu2, cosThetaYNu2
#            print "1", matrixmult(M1, [[y1px],[y1py],[y1pz]]), (nNu1[0][0]*y1px + nNu1[1][0]*y1py + nNu1[2][0]*y1pz)/y1p, cosThetaYNu1
#            print "2", matrixmult(M2, [[y2px],[y2py],[y2pz]]),(nNu2[0][0]*y2px + nNu2[1][0]*y2py + nNu2[2][0]*y2pz)/y2p, cosThetaYNu2
 
#            print nNu1Prime[2][0], cosThetaLNu1
#            print (nNu1Prime[0][0]*sqrt(1.-cosYL1*cosYL1) + nNu1Prime[2][0]*cosYL1), cosThetaYNu1
#            print nNu2Prime[2][0], cosThetaLNu2
#            print (nNu2Prime[0][0]*sqrt(1.-cosYL2*cosYL2) + nNu2Prime[2][0]*cosYL2), cosThetaYNu2
            chi2Value = sqrt((nu1p*nNu1[0][0] + nu2p*nNu2[0][0] - MEx)**2 + (nu1p*nNu1[1][0] + nu2p*nNu2[1][0] - MEy)**2)/mW
            if chi2Value<float('inf'):
              #chi2.Fill(cosThetaLNu1, cosThetaLNu2, chi2Value)
              if chi2Value < chi2Min:
                  chi2Min = chi2Value
                  cosThetaLNu1Min = cosThetaLNu1
                  cosThetaLNu2Min = cosThetaLNu2

                  nu1pMin = nu1p
                  nu1pxMin = nu1p*nNu1[0][0] 
                  nu1pyMin = nu1p*nNu1[1][0] 
                  nu1pzMin = nu1p*nNu1[2][0] 

                  nu2pMin = nu2p
                  nu2pxMin = nu2p*nNu2[0][0] 
                  nu2pyMin = nu2p*nNu2[1][0] 
                  nu2pzMin = nu2p*nNu2[2][0] 

# ------------------------------------------------------------------
      # save files here: Pickle

    # ---- MET----
      nu1ptMin  = sqrt(nu1pxMin**2 +  nu1pyMin**2)  # MET Nu 1
      nu2ptMin  = sqrt(nu2pxMin**2 +  nu2pyMin**2)
      nu1ptTrue = sqrt(nu1pxTrue**2 + nu1pyTrue**2)
      nu2ptTrue = sqrt(nu2pxTrue**2 + nu2pyTrue**2)
      nu1etaTrue = acosh(nu1pTrue/sqrt(nu1pxTrue**2 + nu1pyTrue**2))*nu1pzTrue/(sqrt(nu1pzTrue**2))
      nu2etaTrue = acosh(nu2pTrue/sqrt(nu2pxTrue**2 + nu2pyTrue**2))*nu2pzTrue/(sqrt(nu2pzTrue**2))
      nu1etaMin  = acosh(nu1pMin/ sqrt(nu1pxMin**2 +  nu1pyMin**2)) *nu1pzMin/ (sqrt(nu1pzMin**2))
      nu2etaMin  = acosh(nu2pMin/ sqrt(nu2pxMin**2 +  nu2pyMin**2)) *nu2pzMin/ (sqrt(nu2pzMin**2))

    # ---- HT ----
      ht = getVarValue(c, 'ht')
      ht1True = ht + l1pt + nu1ptTrue
      ht2True = ht + l2pt + nu2ptTrue
      ht1Min  = ht + l1pt + nu1ptMin
      ht2Min  = ht + l2pt + nu2ptMin

    # ---- Top True ----
      t1pxTrue = b1px + l1px + nu1pxTrue
      t1pyTrue = b1py + l1py + nu1pyTrue
      t1pzTrue = b1pz + l1pz + nu1pzTrue
      
      t2pxTrue = b2px + l2px + nu2pxTrue
      t2pyTrue = b2py + l2py + nu2pyTrue
      t2pzTrue = b2pz + l2pz + nu2pzTrue

      t1ptTrue = sqrt(t1pxTrue**2 + t1pyTrue**2)
      t1pTrue  = sqrt(t1pxTrue**2 + t1pyTrue**2 + t1pzTrue**2)
      t1etaTrue = acosh(t1pTrue/sqrt(t1pxTrue**2 + t1pyTrue**2))*t1pzTrue/(sqrt(t1pzTrue**2))
      t1PhiTrue = atan2(t1pyTrue, t1pxTrue)
      cosT1ThetaTrue = t1pzTrue/t1pTrue

      t2ptTrue = sqrt(t2pxTrue**2 + t2pyTrue**2)
      t2pTrue  = sqrt(t2pxTrue**2 + t2pyTrue**2 + t2pzTrue**2)
      t2etaTrue = acosh(t2pTrue/sqrt(t2pxTrue**2 + t2pyTrue**2))*t2pzTrue/(sqrt(t2pzTrue**2))
      t2PhiTrue = atan2(t2pyTrue, t2pxTrue)
      cosT2ThetaTrue = t2pzTrue/t2pTrue

    # ---- Top Min ----
      t1pxMin = b1px + l1px + nu1pxMin
      t1pyMin = b1py + l1py + nu1pyMin
      t1pzMin = b1pz + l1pz + nu1pzMin
      
      t2pxMin = b2px + l2px + nu2pxMin
      t2pyMin = b2py + l2py + nu2pyMin
      t2pzMin = b2pz + l2pz + nu2pzMin

      t1ptMin = sqrt(t1pxMin**2 + t1pyMin**2)
      t1pMin  = sqrt(t1pxMin**2 + t1pyMin**2 + t1pzMin**2)
      t1etaMin = acosh(t1pMin/sqrt(t1pxMin**2 + t1pyMin**2))*t1pzMin/(sqrt(t1pzMin**2))
      t1PhiMin = atan2(t1pyMin, t1pxMin)
      cosT1ThetaMin = t1pzMin/t1pMin

      t2ptMin = sqrt(t2pxMin**2 + t2pyMin**2)
      t2pMin = sqrt(t2pxMin**2 + t2pyMin**2 + t2pzMin**2)
      t2etaMin = acosh(t2pMin/sqrt(t2pxMin**2 + t2pyMin**2))*t2pzMin/(sqrt(t2pzMin**2))
      t2PhiMin = atan2(t2pyMin, t2pxMin)
      cosT2ThetaMin = t2pzMin/t2pMin
      
    # ---- TTBar True ----
      ttpxTrue = t1pxTrue + t2pxTrue
      ttpyTrue = t1pyTrue + t2pyTrue
      ttpzTrue = t1pzTrue + t2pzTrue

      ttptTrue = sqrt(ttpxTrue**2 + ttpyTrue**2)
      ttpTrue  = sqrt(ttpxTrue**2 + ttpyTrue**2 + ttpzTrue**2)
      ttetaTrue = acosh(ttpTrue/sqrt(ttpxTrue**2 + ttpyTrue**2))*ttpzTrue/(sqrt(ttpzTrue**2))
      ttPhiTrue = atan2(ttpyTrue, ttpxTrue)
      cosTTThetaTrue = ttpzTrue/ttpTrue

    # ---- TTBar Min ----
      ttpxMin = t1pxMin + t2pxMin
      ttpyMin = t1pyMin + t2pyMin
      ttpzMin = t1pzMin + t2pzMin

      ttptMin = sqrt(ttpxMin**2 + ttpyMin**2)
      ttpMin  = sqrt(ttpxMin**2 + ttpyMin**2 + ttpzMin**2)
      ttetaMin = acosh(ttpMin/sqrt(ttpxMin**2 + ttpyMin**2))*ttpzMin/(sqrt(ttpzMin**2))
      ttPhiMin = atan2(ttpyMin, ttpxMin)
      cosTTThetaMin = ttpzMin/ttpMin
    # ---- delta Phi ----
      deltaPhiTrue = dPhi(t1PhiTrue, t2PhiTrue)
      deltaPhiMin = dPhi(t1PhiMin, t2PhiMin)

    # --------------

      event = copy.deepcopy(Event)  # make copy of template
      event['dR'] =  sqrt((cosThetaLNu1Min - cosLNu1True)**2 + (cosThetaLNu2Min - cosLNu2True)**2)
      event['event'] = int(getVarValue(c, 'event'))
      event['run'] = getVarValue(c, 'run')
      event['lumi'] = getVarValue(c, 'lumi')
      
      event['ht'] = ht 
      event['ht1True'] = ht1True
      event['ht2True'] = ht2True
      event['ht1Min'] = ht1Min
      event['ht2Min'] = ht2Min

      event['MEx'] = MEx
      event['MEy'] = MEy
      
      event['sign1'] = sign1
      event['sign2'] = sign2
      event['chi2Min'] = chi2Min
      event['cosThetaLNu1Min'] = cosThetaLNu1Min
      event['cosThetaLNu2Min'] = cosThetaLNu2Min
      event['cosLNu1True'] = cosLNu1True
      event['cosLNu2True'] = cosLNu2True
      event['l1p'] = l1p
      event['l1pt'] = l1pt
      event['l1px'] = l1px
      event['l1py'] = l1py
      event['l1pz'] = l1pz
      event['cosL1Phi'] = cosL1Phi
      event['sinL1Phi'] = sinL1Phi
      event['cosL1Theta'] = cosL1Theta
      event['sinL1Theta'] = sinL1Theta
      event['l1eta'] = l1eta

      event['nu1pMin'] = nu1pMin
      event['nu1pTrue'] = nu1pTrue
      event['nu1pxTrue'] = nu1pxTrue
      event['nu1pyTrue'] = nu1pyTrue
      event['nu1pzTrue'] = nu1pzTrue
      event['nu1pxMin'] = nu1pxMin
      event['nu1pyMin'] = nu1pyMin
      event['nu1pzMin'] = nu1pzMin
      event['nu1etaTrue'] = nu1etaTrue
      event['nu1etaMin'] = nu1etaMin

      event['nu2pMin'] = nu2pMin
      event['nu2pTrue'] = nu2pTrue
      event['nu2pxTrue'] = nu2pxTrue
      event['nu2pyTrue'] = nu2pyTrue
      event['nu2pzTrue'] = nu2pzTrue
      event['nu2pxMin'] = nu2pxMin
      event['nu2pyMin'] = nu2pyMin
      event['nu2pzMin'] = nu2pzMin
      event['nu2etaTrue'] = nu2etaTrue
      event['nu2etaMin'] = nu2etaMin
      
      event['cosNu1Phi'] = cosNu1Phi
      event['sinNu1Phi'] = sinNu1Phi
      event['cosNu1ThetaTrue'] = cosNu1ThetaTrue
      event['sinNu1ThetaTrue'] = sinNu1ThetaTrue
      event['cosLNu1True'] = cosLNu1True
      event['l2p'] = l2p
      event['l2pt'] = l2pt
      event['l2px'] = l2px
      event['l2py'] = l2py
      event['l2pz'] = l2pz
      event['cosL2Phi'] = cosL2Phi
      event['sinL2Phi'] = sinL2Phi
      event['cosL2Theta'] = cosL2Theta
      event['sinL2Theta'] = sinL2Theta
      event['l2eta'] = l2eta

      event['cosNu2Phi'] = cosNu2Phi
      event['sinNu2Phi'] = sinNu2Phi
      event['cosNu2ThetaTrue'] = cosNu2ThetaTrue
      event['sinNu2ThetaTrue'] = sinNu2ThetaTrue
      event['cosLNu2True'] = cosLNu2True
      event['b1p'] = b1p
      event['b1px'] = b1px
      event['b1py'] = b1py
      event['b1pz'] = b1pz
      event['b2p'] = b2p
      event['b2px'] = b2px
      event['b2py'] = b2py
      event['b2pz'] = b2pz
      event['t1p'] = t1p
      event['t1px'] = t1px
      event['t1py'] = t1py
      event['t1pz'] = t1pz
      event['t1eta'] = t1eta
      event['t1Phi'] = t1Phi
      event['cosT1Theta'] = cosT1Theta
      event['t2p'] = t2p
      event['t2px'] = t2px
      event['t2py'] = t2py
      event['t2pz'] = t2pz
      event['t2eta'] = t2eta
      event['t2Phi'] = t2Phi
      event['cosT2Theta'] = cosT2Theta
      event['mW2sys1'] = mW2sys1
      event['mW2sys2'] = mW2sys2
      event['mT2sys1'] = mT2sys1
      event['mT2sys2'] = mT2sys2

    # MET
      event['nu1ptMin'] = nu1ptMin
      event['nu2ptMin'] = nu2ptMin
      event['nu1ptTrue'] = nu1ptTrue
      event['nu2ptTrue'] = nu2ptTrue

    # Top True
      event['t1etaTrue'] = t1etaTrue
      event['cosT1ThetaTrue'] = cosT1ThetaTrue
      event['t1PhiTrue'] = t1PhiTrue
      event['t1pxTrue'] = t1pxTrue
      event['t1pyTrue'] = t1pyTrue
      event['t1pzTrue'] = t1pzTrue
      event['t1pTrue'] = t1pTrue
      event['t1ptTrue'] = t1ptTrue

      event['t2etaTrue'] = t2etaTrue
      event['cosT2ThetaTrue'] = cosT2ThetaTrue
      event['t2PhiTrue'] = t2PhiTrue
      event['t2pxTrue'] = t2pxTrue
      event['t2pyTrue'] = t2pyTrue
      event['t2pzTrue'] = t2pzTrue
      event['t2pTrue'] = t2pTrue
      event['t2ptTrue'] = t2ptTrue

    # Top Min
      event['t1etaMin'] = t1etaMin
      event['cosT1ThetaMin'] = cosT1ThetaMin
      event['t1PhiMin'] = t1PhiMin
      event['t1pxMin'] = t1pxMin
      event['t1pyMin'] = t1pyMin
      event['t1pzMin'] = t1pzMin
      event['t1pMin'] = t1pMin
      event['t1ptMin'] = t1ptMin

      event['t2etaMin'] = t2etaMin
      event['cosT2ThetaMin'] = cosT2ThetaMin
      event['t2PhiMin'] = t2PhiMin
      event['t2pxMin'] = t2pxMin
      event['t2pyMin'] = t2pyMin
      event['t2pzMin'] = t2pzMin
      event['t2pMin'] = t2pMin
      event['t2ptMin'] = t2ptMin

    # TTBar True
      event['ttetaTrue'] = ttetaTrue
      event['cosTTThetaTrue'] = cosTTThetaTrue
      event['ttPhiTrue'] = ttPhiTrue
      event['ttpxTrue'] = ttpxTrue
      event['ttpyTrue'] = ttpyTrue
      event['ttpzTrue'] = ttpzTrue
      event['ttpTrue'] = ttpTrue
      event['ttptTrue'] = ttptTrue

    # TTBar Min
      event['ttetaMin'] = ttetaMin
      event['cosTTThetaMin'] = cosTTThetaMin
      event['ttPhiMin'] = ttPhiMin
      event['ttpxMin'] = ttpxMin
      event['ttpyMin'] = ttpyMin
      event['ttpzMin'] = ttpzMin
      event['ttpMin'] = ttpMin
      event['ttptMin'] = ttptMin
    
    # delta Phi
      event['deltaPhiTrue'] = deltaPhiTrue
      event['deltaPhiMin'] = deltaPhiMin

    # Ratios
      event['W1ratio'] = W1ratio
      event['W2ratio'] = W2ratio
      event['T1ratio'] = T1ratio
      event['T2ratio'] = T2ratio

      fourEvents.append(event)
    
  allEvents.append(fourEvents)
# ------------------------------------------------------------------
   #  outputPath = '/data/jkancsar/topDiLepton/fork/'
   #   filename = outputPath+"output/chi2_"+str(i)+"_"+str(sign1)+"_"+str(sign2)+".png"
   #   event['Filename'] = filename.rpartition('/')[2]  # no use if it is done by fork

#          print cosThetaLNu1, cosThetaLNu2, chi2Value
#      c1 = ROOT.TCanvas()
#      chi2.GetZaxis().SetRangeUser(10**-2,chi2.GetMaximum())
#      c1.SetLogz(1)
#      chi2.Draw("COLZ")
#      line1.Draw()
#      line2.Draw()
#      line3.Draw()
#      line4.Draw()
#      minAngles.SetPoint(0, cosThetaLNu1Min, cosThetaLNu2Min)
#      minAngles.SetLineColor(ROOT.kRed)
#      minAngles.Draw('*')
#      minText.DrawText(cosThetaLNu1Min,cosThetaLNu2Min + 0.01, str(round(chi2Min, 2)) )
#      trueAngles.SetLineColor(ROOT.kBlue)
#      trueAngles.Draw("*")
#      c1.Print(filename)

pickle.dump(allEvents, file(outputPath+'topDiLeptonEM_'+str(minF)+"_"+str(maxF)+"_nevents_"+str(nevents)+'.pkl', 'w'))
del eList
#
# EOF
