from math import *
import copy
import ROOT

#etabins = {
#  "0" :  [0.0, 0.5],
#  "0.5": [0.5, 1.0],
#  "1.0": [1.0, 1.5],
#  "1.5": [1.5, 2.0],
#  "2.0": [2.0, 2.5],
#  "2.5": [2.5, 3.0],
#  "3.0": [3.0, 5.0]
#}
#
#NVal = {
#  "0" : 3.97,
#  "0.5":3.55,
#  "1.0":4.54,
#  "1.5":4.63,
#  "2.0":2.53,
#  "2.5":-3.33,
#  "3.0":2.95
#}
#SVal = {
#  "0" : 0.183,
#  "0.5":0.240,
#  "1.0":0.227,
#  "1.5":0.237,
#  "2.0":0.343,
#  "2.5":0.733,
#  "3.0":0.116
#}
#mVal = {
#  "0" : 0.626,
#  "0.5":0.526,
#  "1.0":0.590,
#  "1.5":0.487,
#  "2.0":0.287,
#  "2.5":0.083,
#  "3.0":0.961
#}
#
#def getetaBinKey(etaval):
#  for kk in etabins.keys():
#    k = etabins[kk]
#    if (abs(etaval)>=k[0] or k[0]<0) and (abs(etaval)<k[1] or k[1]<0):
#      return kk
#
#def getConst(eta, const):
#  etaBin = getetaBinKey(abs(eta))
#  if const=="N":
#    return NVal[etaBin]
#  if const=="S":
#    return SVal[etaBin]
#  if const=="m":
#    return mVal[etaBin]
#
#def sigmaJetPt(ptval, etaval):
#  thisN = getConst(etaval, "N")
#  thisS = getConst(etaval, "S")
#  thism = getConst(etaval, "m")
#  return ptval*sqrt(thisN**3/(abs(thisN)*ptval**2) + thisS**2*ptval**(thism -1.0) ) #NSC formula

#loading templates
fullrootfilename = "resolutions_Spring10_AK5PF.root"
print "Loading ROOT file",fullrootfilename
tf = ROOT.TFile(fullrootfilename)
relResolutionPtEta={}
for pt in range(0,1001):
  relResolutionPtEta[pt] = {}
  for eta2 in range(0,10):
    eta = eta2/2.
    etastr = str(eta).replace(".0","")
    name = "res_pt_"+str(pt)+"_"+etastr
    relResolutionPtEta[pt][eta] = copy.deepcopy(tf.Get(name))
tf.Close()
print "... Done!"

fullrootfilename = "resolutions_Spring10_AK5PF_gaussian.root"
print "Loading ROOT file",fullrootfilename
tf = ROOT.TFile(fullrootfilename)
gaussian_relResolutionPtEta={}
for pt in range(0,1001):
  gaussian_relResolutionPtEta[pt] = {}
  for eta2 in range(0,10):
    eta = eta2/2.
    etastr = str(eta).replace(".0","")
    name = "res_pt_"+str(pt)+"_"+etastr
    gaussian_relResolutionPtEta[pt][eta] = copy.deepcopy(tf.Get(name))
tf.Close()
print "... Done!"
