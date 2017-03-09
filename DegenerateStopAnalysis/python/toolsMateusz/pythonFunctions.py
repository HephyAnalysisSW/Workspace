#pythonFunctions.py

import os
import ROOT
import math

cmsbase = os.getenv("CMSSW_BASE")
ROOT.gROOT.ProcessLineSync(".L %s/src/Workspace/DegenerateStopAnalysis/python/tools/deltaR.C+"%cmsbase)

varSel = lambda x,sel: "Max$(%s*(%s))"%(x,sel)
sumSel1 = lambda sel: "Sum$(%s) == 1"%(sel)

less = lambda var,val: "(%s < %s)"%(var,val)
more = lambda var,val: "(%s > %s)"%(var,val)
btw = lambda var,minVal,maxVal: "(%s > %s && %s < %s)"%(var, min(minVal,maxVal), var, max(minVal,maxVal))

deltaPhiStr = lambda x,y : "acos(cos({x}-{y}))".format(x=x,y=y)
#deltaPhiStr = lambda x,y : "abs( atan2(sin({x}-{y}), cos({x}-{y}) ) )".format(x=x,y=y)

deltaRStr = lambda eta1,eta2,phi1,phi2: "sqrt( ({eta1}-{eta2})**2 - ({dphi})**2  )".format(eta1=eta1,eta2=eta2, dphi=deltaPhiStr(phi1,phi2) )

def combineCuts(*a):
   if len(a) == 1:
      print "At least 2 arguments required for combineCuts() function."
      return
   else:
      sel = ""
      for i in range(len(a)):
         if i == 0: sel = "(" + a[0] + ")"
         else: sel += " && (" + a[i] + ")"
   return "(" + sel + ")"

def joinCutStrings(cutStringList): #same (used in other functions)
  return "(" + " && ".join([ "("+c +")" for c in cutStringList])    +")"

def combineCutsList(a):
   if len(a) == 1:
      print "List of strings required as input."
      return
   else:
      sel = ""
      for i in range(len(a)):
         if i == 0: sel = "(" + a[0] + ")"
         else: sel += " && (" + a[i] + ")"
   return "(" + sel + ")"

def combineCutList(cutList):
  return joinCutStrings([x[1] for x in cutList if x[1]!="(1)"])

def btw(var,minVal,maxVal, rangeLimit=[0,0] ):
    greaterOpp = ">"
    lessOpp = "<"
    vals = [minVal, maxVal]
    minVal = min(vals)
    maxVal = max(vals)
    if rangeLimit[0]:
        greaterOpp += "="
    if rangeLimit[1]:
        lessOpp += "="
    return "(%s)"%" ".join(["%s"%x for x in [var,greaterOpp,minVal, "&&", var, lessOpp, maxVal ]])

def makeCutFlowList(cutList,baseCut=''):
  cutFlowList=[]
  for cutName,cutString in cutList:
    cutsToJoin=[] if not baseCut else [baseCut]
    cutsToJoin.extend( [ cutList[i][1] for i in range(0, 1+cutList.index( [cutName,cutString])) ] )
    cutFlowString = joinCutStrings( cutsToJoin   )
    cutFlowList.append( [cutName, cutFlowString ])
  return cutFlowList

def setErrSqrtN(hist):
   n = hist.GetNbinsX()

   val = {}
   err = {}
   newErr = {}

   for i in range(n):
      #a = int(hist.GetBinLowEdge(i+1))
      #w = int(hist.GetBinWidth(i+1))

      val[i] = hist.GetBinContent(i+1)
      err[i] = hist.GetBinError(i+1)

      #print "Bin: ", i
      #print "Value: ", val[i]
      #print "Error: ", err[i]

      newErr[i] = math.sqrt(val[i]) #sqrt(N)

      hist.SetBinError(i+1, newErr[i])

      #print "New error: ", hist.GetBinError(i+1)

   return
      #uFloat[i] = u_float.u_float(value[x][i], error[x][i]) 

def setErrZero(hist):
   n = hist.GetNbinsX()

   val = {}
   err = {}
   newErr = {}

   for i in range(n):
      #a = int(hist.GetBinLowEdge(i+1))
      #w = int(hist.GetBinWidth(i+1))

      val[i] = hist.GetBinContent(i+1)
      err[i] = hist.GetBinError(i+1)

      #print "Bin: ", i
      #print "Value: ", val[i]
      #print "Error: ", err[i]

      newErr[i] = 0. #sqrt(N)

      hist.SetBinError(i+1, newErr[i])

      #print "New error: ", hist.GetBinError(i+1)

   return

#from helpers.py
#def deltaPhi(phi1, phi2):
#  dphi = phi2-phi1
#  if  dphi > pi:
#    dphi -= 2.0*pi
#  if dphi <= -pi:
#    dphi += 2.0*pi
#  return abs(dphi)
#
#def deltaPhiNA(phi1, phi2):
#  dphi = phi2-phi1
#  if  dphi > pi:
#    dphi -= 2.0*pi
#  if dphi <= -pi:
#    dphi += 2.0*pi
#  return dphi
#
#def minAbsDeltaPhi(phi, phis):
#  if len(phis) > 0:
#    return min([abs(deltaPhi(phi, x)) for x in phis])
#  else: return float('inf')
#
#def minAbsPiMinusDeltaPhi(phi, phis):
#  if len(phis)>0:
#    return min([abs(abs(deltaPhi(phi, x)) - pi) for x in phis])
#  else: return float('inf')

#combineTwoCuts = lambda sel1,sel2: "((%s) && (%s))"%(sel1,sel2)

