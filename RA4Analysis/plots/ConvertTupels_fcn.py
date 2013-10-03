import array
import xsec
import math
import time, cPickle, os, copy
import ROOT
from array import array
import random
import btagEff.MCPfSSVHEMbcalc_snapshot, btagEff.MCPfSSVHEMccalc_snapshot, btagEff.MCPfSSVHEMlcalc_snapshot
import btagEff.MCPfSSVHEMbcalcJets_snapshot, btagEff.MCPfSSVHEMccalcJets_snapshot, btagEff.MCPfSSVHEMlcalcJets_snapshot
import btagEff.BTAGSSVHEM_snapshot, btagEff.MISTAGSSVHEM_snapshot

bold  = "\033[1m"
reset = "\033[0;0m"

def isNaN(x):
    return str(float(x)).lower() == 'nan'
  
def getArrValue(c, varname, i):
  alias = c.GetAlias(varname)
  if alias!="":
    return c.GetLeaf(alias).GetValue(i)
  else:
    if c.GetLeaf(varname):
      return c.GetLeaf(varname).GetValue(i)
    else:
      return float('nan')  
  
def loadEff(flavor, pt, eta):
  eff=0
  jetAbsEta=5; jetEt=2
  arr=loadEffArr(flavor); bins=arr[0]; results=arr[1]; effType=arr[2][0]; effErrType=arr[2][1]
  index=-1
  if flavor=="bcalc" and pt >=253: pt=250
  if flavor=="ccalc" and pt >=214: pt=210
  if flavor=="lcalc" and pt >=274: pt=270
  if flavor=="bcalcJets" and pt >=253: pt=250
  if flavor=="ccalcJets" and pt >=214: pt=210
  if flavor=="lcalcJets" and pt >=274: pt=270
  for i in range(0, len(bins)):  
    if bins[i][jetEt][0]<=pt<=bins[i][jetEt][1] and bins[i][jetAbsEta][0]<=abs(eta)<=bins[i][jetAbsEta][1]:
#      print "found bin", i, pt, eta, "bin", bins[i]
      index=i
      break
  if index>=0:  
    eff=results[effType][index]
    err=results[effErrType][index]
  else:
#    print flavor, i, pt, eta, "bin", bins[i]  
    print "no bin found"
  #if pt>240:
    #print "high pt", flavor, pt, eta, eff, 1-eff    
  return [eff, err]

def loadEffArr(flavor):
  bins= eval('btagEff.MCPfSSVHEM'+flavor+'_snapshot.MCPfSSVHEM'+flavor+'bins')
  results= eval('btagEff.MCPfSSVHEM'+flavor+'_snapshot.MCPfSSVHEM'+flavor+'results')
  effTypes=eval('btagEff.MCPfSSVHEM'+flavor+'_snapshot.MCPfSSVHEM'+flavor+'types')
#  print "loaded", flavor, bins, results, effTypes
  return [bins, results, effTypes]
    		       
def loadSFArr(file):
  if file[0]=="C":
    file=file[1:]
  bins= eval("btagEff."+file+'_snapshot.'+file+'bins')
  results= eval("btagEff."+file+'_snapshot.'+file+'results')
  effTypes=eval("btagEff."+file+'_snapshot.'+file+'types')
#  print "loaded", flavor, bins, results, effTypes
  return [bins, results, effTypes]
		       
def loadSF(file, pt, eta):
  eff=0
  jetAbsEta=5; jetEt=2
  arr=loadSFArr(file); bins=arr[0]; results=arr[1];
  effType=1013; effErrType=1014
  if "BTAG" in file:
    effType=1009
    effErrType=1010
  
  index=-1
  ptlarge=False
  if "BTAG" in file and pt >=240: 
    pt=200
    ptlarge=True
  if "MISTAG" in file and pt >=520: pt=515
  
  for i in range(0, len(bins)):  
    if bins[i][jetEt][0]<=pt<=bins[i][jetEt][1] and bins[i][jetAbsEta][0]<=abs(eta)<=bins[i][jetAbsEta][1]:
     #print "found bin", i, pt, eta, "bin", bins[i]
     index=i
     break
  if index>=0:
    sf=results[effType][index]
    sferr=results[effErrType][index]
    #print file, sf, sferr
    if "BTAG" in file and ptlarge: # and not file[0]=="C":
      sferr=0.15
    if "MISTAG" in file:
      sf=sf*1.04
      sferr=sferr*1.04
    elif file[0]=="C":  
      sferr=2*sferr
  else:
    print file, i, pt, eta, "bin", bins[i]  
    print "no bin found"
    sf=1; sferr=0
  #if pt>240:
    #print "high pt", flavor, pt, eta, eff, 1-eff    
  #print  "selected", pt, ptlarge, sf, sferr
  return [sf, sferr]    
    
def binomial(n, k, p):
  if k<=n and p <= 1:
    return noverk(n, k)*p**k*(1-p)**(n-k)
  else: return 0
  
def conv2bin(Njets, NtrueB, Ntag, effB, effL):
  NtrueL=Njets-NtrueB
  pdf_Ntag=0
  for i in range(0, min(Ntag, NtrueB)+1):
    pdf_Ntag+=binomial(NtrueB, i, effB)*binomial(NtrueL, Ntag-i, effL)
  return pdf_Ntag  

def block(n, k, i, d):
  arr=[]
  for j in range(i+1, (n-k)+d+1):
    #print "d:",d, "index", j
    if d<k:
      arr2=block(n, k, j, d+1)
      for l in range(0, len(arr2)):
	arr2[l]=str(j)+str(arr2[l])
      arr=arr+arr2	
    else:
      #print "ende Block", d
      arr.append(j)
      #print arr
  #print "lastd:",d, "lastindex", j
  return arr
  
def calcEff(arr, JetsArr):
  eff=0
  for elem in arr:
    eff+=getEff(elem, JetsArr)
    #print "tagged Jets", elem, "eff", getEff(elem, JetsArr), "currentSum", eff
  return eff
  
def getEff(elem, JetsArr):
  eff=1
  #print "elem", elem
  taggedJets=str(elem) #str(elem).replace(", ","").replace("[","").replace("]","")
  untaggedJets=""
  for i in range(1, len(JetsArr)+1):
     if str(i) not in taggedJets:
       untaggedJets+=str(i)
       eff=eff*JetsArr[i-1][1]
     else:
       eff=eff*JetsArr[i-1][0]
  #print "nlightJets, tag, untag", len(lightJetsArr), taggedJets, untaggedJets     
  return eff
     
def getEffTAG(elem, JetsArr, taggedJetsPt):
  eff=1
  #print "elem", elem
  taggedJets=str(elem) #str(elem).replace(", ","").replace("[","").replace("]","")
  untaggedJets=""
  for i in range(1, len(JetsArr)+1):
     if str(i) not in taggedJets:
       untaggedJets+=str(i)
       eff=eff*JetsArr[i-1][1]
     else:
       eff=eff*JetsArr[i-1][0]
       taggedJetsPt.append(JetsArr[i-1][2])
  #print "nJets", len(JetsArr), "taggedJets", taggedJets, "untaggedJets", untaggedJets, "calc Eff", eff     
  return eff     

  
