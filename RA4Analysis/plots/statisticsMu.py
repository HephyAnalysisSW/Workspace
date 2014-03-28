
#from PBayesianUpperLimit import BayesianUpperLimit

import ROOT
from array import array
from math import *
import os, copy, fnmatch

from Workspace.RA4Analysis.simplePlotsCommon import *

from defaultMuSamples import *
from simpleStatTools import *

import xsec
small = False
mode = "ht"
#datapath = "/afs/hephy.at/scratch/s/schoefbeck/ABCDData/Mu-"+mode+"-kMs/2j80+1j50/"
datapath = "/afs/hephy.at/scratch/s/schoefbeck/ABCDData/Mu-"+mode+"-kMs/120_80_50/"
allSamples=[]

regions = ["A","B","C","D"]
 
var1 = "kinMetSig"
var2 = mode

#var1_cut1 = 3.5
#var1_cut2 = 8.
#var1_cut3 = 8.
#var2_cut1 = 150.
#var2_cut2 = 300.
#var2_cut3 = 400.
var1_cut1 = 3.5
var1_cut2 = 5.
var1_cut3 = 5.
var2_cut1 = 150.
var2_cut2 = 250.
var2_cut3 = 250.


def kappa (tbkg):
  if tbkg.has_key("A") and tbkg.has_key("B") and tbkg.has_key("C") and tbkg.has_key("D"):
    if tbkg["B"]*tbkg["C"]>0.:
      return (tbkg["A"]*tbkg["D"])/(tbkg["B"]*tbkg["C"])
  return -1.
#execfile(datapath+getABCDDataFileName(var1, var2, var1_cut1, var1_cut2, var1_cut3, var2_cut1, var2_cut2,var2_cut3))

syserr = 0.2

considerFiles = "*kinMetSig_2.5_*_ht_300_*.py"
#considerFiles = "*.py"
filelist=os.listdir(datapath)

exclusion = {}
counter=0
res_SoverSqrtB = []
res_SoverSig = []
res_SoverCombSig = []

backgrounds = mc["bins"]
print "Using background bins", backgrounds
print "datapath", datapath
for thisfile in filelist:
#  if counter>1:
#    break
  if fnmatch.fnmatch(thisfile, considerFiles) and thisfile[-3:]==".py"  and thisfile.count("MSUGRA")==0: #and thisfile.count("kinMetSig_2.5_5.0_5.0_")>0:
    numbers = 0
    exec(file(datapath+thisfile,"r").read())
    totalBkg = getBkgSum(numbers, backgrounds)   
    kappaVal = kappa(totalBkg)
    if cuts["ht"][0][1]==cuts["ht"][1][0] and cuts["kinMetSig"][0][1]==cuts["kinMetSig"][1][0] and kappaVal>0 and totalBkg["D"] < 3: #and fabs(1.-kappaVal)<.3: #and fabs(1.-kappaW)<0.1 and fabs(1.-kappaT)<0.1:
      wBkg = getBkgSum(numbers, WJets_Bins)
      tBkg = getBkgSum(numbers, ["TTJets"])
      qcdBkg = getBkgSum(numbers, QCD_Bins)
      kappaW = kappa(wBkg)
      kappaT = kappa(tBkg)
      totaltrueBkgA = tBkg["A"] + wBkg["A"] + qcdBkg["A"]
      totaltrueBkgB = tBkg["B"] + wBkg["B"] + qcdBkg["B"]
      totaltrueBkgC = tBkg["C"] + wBkg["C"] + qcdBkg["C"]
      totaltrueBkgD = tBkg["D"] + wBkg["D"] + qcdBkg["D"]

      kappa_rel_err = sqrt(1./totaltrueBkgA + 1./totaltrueBkgB + 1./totaltrueBkgC +1./totaltrueBkgD)
      totalBkgErr = getErrSum(numbers, mc["bins"])
      kappa_rel_err_mc = sqrt(totalBkgErr["A"]**2/totalBkg["A"]**2 + totalBkgErr["B"]**2/totalBkg["B"]**2 + totalBkgErr["C"]**2/totalBkg["C"]**2 + totalBkgErr["D"]**2/totalBkg["D"]**2)

      ttbar_res = getBkgSum(numbers, ["TTJets"])
      wjets_res = getBkgSum(numbers, WJets_Bins)
      cs_diff = (ttbar_res["A"]/ttbar_res["B"] - wjets_res["A"]/wjets_res["B"] ) /(ttbar_res["A"]/ttbar_res["B"] + wjets_res["A"]/wjets_res["B"] )

      totaltrueSigA =numbers["LM1"]["Events"]["A"] 
      totaltrueSigB =numbers["LM1"]["Events"]["B"] 
      totaltrueSigC =numbers["LM1"]["Events"]["C"] 
      totaltrueSigD =numbers["LM1"]["Events"]["D"] 
#      exclusion[thisfile] = ROOT.exclusion(totaltrueBkgA,totaltrueBkgB,totaltrueBkgC,totaltrueBkgD,totaltrueSigA,totaltrueSigB,totaltrueSigC,totaltrueSigD,2000);
      lm0 = numbers["LM9"]["Events"]["D"]
      lm1 = numbers["LM1"]["Events"]["D"]
      SoverB_lm0 = numbers["LM9"]["Events"]["D"]/totalBkg["D"]
      SoverB_lm1 = numbers["LM1"]["Events"]["D"]/totalBkg["D"]
      relstaterr = sqrt(1./totalBkg["A"] + 1./totalBkg["B"] + 1./totalBkg["C"])
      sigContB_lm0 = numbers["LM9"]["Events"]["B"]/totalBkg["B"]
      sigContC_lm0 = numbers["LM9"]["Events"]["C"]/totalBkg["C"]
      sigContB_lm1 = numbers["LM1"]["Events"]["B"]/totalBkg["B"]
      sigContC_lm1 = numbers["LM1"]["Events"]["C"]/totalBkg["C"]
      syserr_sc_lm0 = syserr + sigContB_lm0 + sigContC_lm0
      rel_err = sqrt(syserr*syserr+relstaterr*relstaterr)
      rel_err_sc = sqrt(syserr_sc_lm0*syserr_sc_lm0 +relstaterr*relstaterr)
      S_over_sigma = lm0/(rel_err*totalBkg["D"])
      S_over_sigma_sc_lm0 = lm0/(rel_err_sc*totalBkg["D"])
      pstring= "N. "+str(counter)+" kappa "+niceNum(kappaVal)+"("+niceNum(kappaW)+","+niceNum(kappaT)+") stat-rel-err "+niceNum(kappa_rel_err)+"mc-rel-err "+niceNum(kappa_rel_err_mc)+" yield lm1"+niceNum(lm1)+"true Bkg"+niceNum( totalBkg["D"])+"S/B"+niceNum(lm1/totalBkg["D"])+"S/sqrt-B"+niceNum(lm1/sqrt(totalBkg["D"]))+"tot-sig-cont."+niceNum(sigContB_lm1+sigContC_lm1)+thisfile
#      pstring= "N. "+str(counter)+" kappa "+niceNum(kappaVal)+"("+niceNum(kappaW)+","+niceNum(kappaT)+") stat-rel-err "+niceNum(kappa_rel_err)+" yield lm1"+niceNum(lm1)+"true Bkg"+niceNum( totalBkg["D"])+"S/B"+niceNum(lm1/totalBkg["D"])+"S/sqrt-B"+niceNum(lm1/sqrt(totalBkg["D"]))+"S/sig"+niceNum(lm1/(totalBkg["D"]*rel_err))+"cs_d"+niceNum(cs_diff)+"tot-sig-cont."+niceNum(sigContB_lm1+sigContC_lm1)+thisfile
      print pstring
#      if sigContB_lm0+sigContC_lm0 < 0.8:
      res_SoverSqrtB.append([lm0/sqrt(totalBkg["D"]), pstring, datapath+thisfile])
      res_SoverSig.append([lm0/(totalBkg["D"]*rel_err), pstring, datapath+thisfile])
      res_SoverCombSig.append([lm0/sqrt( totalBkg["D"] + totalBkg["D"]**2*rel_err**2), pstring, datapath+thisfile])

#      print " S_over_sigma"+niceNum(S_over_sigma)+" w/sc "+niceNum(S_over_sigma_sc_lm0)+" yield lm0 "+niceNum(lm0) +"totBkg D "+niceNum( totalBkg["D"]) +" sC-lm0"+niceNum(sigContB_lm0)+niceNum(sigContC_lm0) +"rel-err"+niceNum(rel_err)+"rel_err_sc"+niceNum(rel_err_sc)+"cs_diff"+niceNum(cs_diff) + datapath+thisfile
      #+"ex"+niceNum(exclusion[thisfile])
      counter=counter+1
#      analyze(datapath+thisfile)

print "\n\n---------Best results wrt. S/sqrt-B ----------\n"
res_SoverSqrtB.sort()
res_SoverSqrtB.reverse()
for s in res_SoverSqrtB[:20]:
  print s[1]
print
print "\n\n---------  Best results wrt. S/sig  ----------\n"
res_SoverSig.sort()
res_SoverSig.reverse()
for s in res_SoverSig[:20]:
  print s[1]
print
print "\n\n---------  Best results wrt. S/Combsig  ----------\n"
res_SoverCombSig.sort()
res_SoverCombSig.reverse()
for s in res_SoverCombSig[:20]:
  print s[1]

allFiles = []
for s in res_SoverSqrtB[:20]:
  allFiles.append(s[2])
for s in res_SoverSig[:20]:
  if allFiles.count(s[2])==0:
    allFiles.append(s[2])
for s in res_SoverCombSig[:20]:
  if allFiles.count(s[2])==0:
    allFiles.append(s[2])
for f in allFiles:
  print "\""+f+"\","


#      print thisfile+ "kappa"+niceNum(kappaVal)+"W:"+kappaW+"T"+niceNum(kappaT)+"LM9"+ lm0+ "LM1"+ lm1+ "S/B LM9"+SoverB_lm0+"S/B LM1"+SoverB_lm1+ "sigContC"+ sigContB_lm1+ "sigContC"+ sigContC_lm1
#      if lm1>2 and SoverB>0.8 and sigContB<0.15 and sigContC<0.15: # and cuts["ht2"][0][0]>150:
#        print "Stat: kappa = ",kappaVal, "LM1:",numbers["LM1"]["Events"]["D"], datapath+thisfile
#        print "Stat: cuts:   ",cuts, "S/B", SoverB,"relstaterr",relstaterr, "sigcont: A",numbers["LM1"]["Events"]["A"]/totalBkg["A"], "B", numbers["LM1"]["Events"]["B"]/totalBkg["B"], "C", numbers["LM1"]["Events"]["C"]/totalBkg["C"]
#        cl=0.95  # compute 95 % confidence limit
##        nD=100   # number of observed events in D (integer)
#        nD = int(numbers["LM1"]["Events"]["D"])
#        nD_bg = totalBkg["B"]*totalBkg["C"]/totalBkg["A"]
#        sig_nD=nD_bg * sqrt(relstaterr**2 + 0.20**2)# uncertainty on the background estimate in D
#        epsilon=0. # acceptance error
#        precision=0.2 # integration step size
#
#        limit=BayesianUpperLimit(int(nD_bg),epsilon,nD_bg,sig_nD,cl,precision)
#        print "Stat: 1fb^-1:   We can exclude models at ",cl,"which predict >",limit,"signal events. nD/Limit = ", nD/limit
#        sig_nD=0.1*nD_bg * sqrt((sqrt(10)*relstaterr)**2 + 0.20**2)# uncertainty on the background estimate in D
#        limit=BayesianUpperLimit(int(0.1*nD_bg),epsilon,0.1*nD_bg,sig_nD,cl,precision)
#        print "Stat: 100pb^-1: We can exclude models at ",cl,"which predict >",limit,"signal events. LM1 exclusion at 100pb^-1?", (0.1*nD)/limit 
##        sig_nD=0.03*nD_bg * sqrt((sqrt(1/0.03)*relstaterr_1fb)**2 + syserr**2)# uncertainty on the background estimate in D
##        limit_30pb=BayesianUpperLimit(int(0.03*(nD_bg)),epsilon,0.03*nD_bg,sig_nD,cl,precision)
##        print "30pb^-1: With sig_nD",sig_nD,", we can exclude models at ",cl,"which predict >",limit_30pb,"signal events."
 
#http://wwwhephy.oeaw.ac.at/u3w/s/schoefbeck/www/ABCDData/ht2had/kinMetSig_3.0_7.0_7.0_ht2_150.0_300.0_300.0.py

#Candidates:
#0.971400766767 LM1: 53.94196755 /afs/hephy.at/user/s/schoefbeck/www/ABCDData/tightVetoRA4_ht2had/kinMetSig_2.0_5.0_7.0_ht2_150.0_300.0_300.0.py
#{'kinMetSig': [[2.0, 5.0], [7.0, -1]], 'ht2': [[150.0, 300.0], [300.0, -1]]} S/B 0.648042150407 relstaterr 0.0637017484046 sigcont: A 0.00156705745085 B 0.0201882995763 C 0.0903876595293
#1.01526035779 LM1: 27.5555920935 /afs/hephy.at/user/s/schoefbeck/www/ABCDData/tightVetoRA4_ht2had/kinMetSig_3.0_6.0_7.0_ht2_150.0_350.0_400.0.py
#{'kinMetSig': [[3.0, 6.0], [7.0, -1]], 'ht2': [[150.0, 350.0], [400.0, -1]]} S/B 1.18904695067 relstaterr 0.105061913756 sigcont: A 0.00384524178002 B 0.0765856024479 C 0.112882307072

#101005
#Stat: 100pb^-1: We can exclude models at  0.95 which predict > 8.09374607405 signal events.
#Stat: kappa =  0.992055132334 LM1: 29.6412217703 /afs/hephy.at/user/s/schoefbeck/www/ABCDData/101005_ht2had/kinMetSig_4.0_6.0_7.0_ht2_150.0_300.0_400.0.py
#Stat: cuts:    {'kinMetSig': [[4.0, 6.0], [7.0, -1]], 'ht2': [[150.0, 300.0], [400.0, -1]]} S/B 1.39406719343 relstaterr 0.138985518823 sigcont: A 0.00388719076221 B 0.113647086772 C 0.0987473625645
 
