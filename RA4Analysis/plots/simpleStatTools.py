import copy
from simplePlotsCommon import *
from math import *
import os, copy
#from PBayesianUpperLimit import BayesianUpperLimit

regions = ["A","B","C","D","All", "LB"]

def getErrQuotient(a,b,sigma_a, sigma_b):
  return [a*(1./b), sqrt(1./b**2*sigma_a**2 + a**2*1./b**4*sigma_b**2)]
def getErrProduct(a,b,sigma_a, sigma_b):
  return [a*b,sqrt(b*sigma_a**2+a*sigma_b**2)]

def getBkgSum(res, bins, lumiscaling = 1.0):
  thisresult={}
#  thesesamples = copy.deepcopy(bkgs)
#  if type(bkgs)==type(""):
#    thesesamples = [bkgs]
  for r in regions:
    thisresult[r]=0.
    for bin in bins:
#      thesebins = ""
#      if bins.has_key(bkg):
#        thesebins = bins[bkg]
#      else:
#        thesebins = [bkg]
#      for bin in thesebins:
      if not res.has_key(bin):
        print "getBkgSum: WARNING!! Bin",bin, "not in result!!"
      else:
        if res[bin]["Events"].has_key(r):
          thisresult[r]+=res[bin]["Events"][r]*lumiscaling
        else:
          print "getBkgSum: WARNING!! Bin",bin,"does not have region",r,". Regions found:",res[bin]["Events"].keys()
  return thisresult
 
def getErrSum(res, bins , lumiscaling = 1.0):
  thisSigma2={}
  for r in regions:
    thisSigma2[r]=0.
    for bin in bins:
      if not res.has_key(bin):
        print "getBkgSum: WARNING!! Bin",bin, "not in result!!"
      else:
        if res[bin]["Events"].has_key(r):
          thisSigma2[r]+=res[bin]["Entries"][r]*(res[bin]["weight"]*lumiscaling)**2
        else:
          print "getBkgSum: WARNING!! Bin",bin,"does not have region",r,". Regions found:",res[bin]["Events"].keys()
  thisSigma={}
  for key in thisSigma2.keys():
    thisSigma[key] = sqrt(thisSigma2[key])
  return thisSigma

def getBkgPred(events, sigmas):
  if events["A"]>0:
    sigma2pred = sigmas["C"]**2*(events["B"]/events["A"])**2 + sigmas["B"]**2*(events["C"]/events["A"])**2 + sigmas["A"]**2*(events["B"]*events["C"]/events["A"]**2)**2
    return [events["C"]*events["B"]/events["A"], sqrt(sigma2pred)]
  else:
    print "getBkgPred::Warning: Non-zero A!!"
    return [0,0]
  

def kappa(thisres):
  if thisres["B"]>0 and thisres["C"]>0:
    return thisres["A"]*thisres["D"]/(thisres["B"]*thisres["C"])
  else:
    return -1
def niceNum(num, dig = 2, signed = False):
  res=str(round(num,dig)).rjust(7).ljust(8)
  if signed and num>=0.:
    res = "+"+res
  return res
  

def analyze(filename, mode, thisLumi = 0):
  if mode == "Ele":
    exec(file("defaultEleSamples.py","r").read())
  if mode == "Mu":
    exec(file("defaultMuSamples.py","r").read())
  print "Executing ",filename
  exec(file(filename,"r").read())
  lumiscaling = 1.0
  if thisLumi != 0:
    lumiscaling = thisLumi/targetLumi
    print "Rescaling! targetLumi = ",targetLumi," to ",thisLumi,"(",niceNum(lumiscaling),")"
  else:
    print "Using targetLumi ",targetLumi, "from file"
  
  data_2010_bins = []
  data_2011_bins = []
  for thisbin in data_bins:
    if thisbin.count("Run2011")>0:
      data_2011_bins.append(thisbin)
    else:
      data_2010_bins.append(thisbin)
      
  
  data_res      = getBkgSum(numbers, data_bins  )
  data_2010_res = getBkgSum(numbers, data_2010_bins)
  data_2011_res = getBkgSum(numbers, data_2011_bins)

  mc_bins = copy.deepcopy(QCD_Bins)
  mc_bins.extend(singleTop_Bins)
  mc_bins.extend(["TTJets"])
  mc_bins.extend(ZJets_Bins)
  mc_bins.extend(WJets_Bins)

  qcd_res = getBkgSum(numbers, QCD_Bins, lumiscaling)
  stop_res = getBkgSum(numbers, singleTop_Bins, lumiscaling)
  wjets_res = getBkgSum(numbers, WJets_Bins, lumiscaling)
  ttjets_res = getBkgSum(numbers, ["TTJets"], lumiscaling)
  dy_res = getBkgSum(numbers, ZJets_Bins, lumiscaling)
  totalBkg = getBkgSum(numbers, mc_bins, lumiscaling)
  LM9_res = getBkgSum(numbers, ["LM9"], lumiscaling)
  LM1_res = getBkgSum(numbers, ["LM1"], lumiscaling)

  data_res_err={}
  for key in data_res.keys():
    data_res_err[key] = sqrt(data_res[key])
  data_2010_res_err={}
  for key in data_2010_res.keys():
    data_2010_res_err[key] = sqrt(data_2010_res[key])
  data_2011_res_err={}
  for key in data_2011_res.keys():
    data_2011_res_err[key] = sqrt(data_2011_res[key])

  qcd_res_err = getErrSum(numbers, QCD_Bins, lumiscaling)
  stop_res_err = getErrSum(numbers, singleTop_Bins, lumiscaling)
  wjets_res_err = getErrSum(numbers, WJets_Bins, lumiscaling)
  dy_res_err = getErrSum(numbers, ZJets_Bins, lumiscaling)
  ttjets_res_err = getErrSum(numbers, ["TTJets"], lumiscaling)
  totalBkgErr = getErrSum(numbers, mc_bins, lumiscaling)
  LM9_res_err = getErrSum(numbers, ["LM9"], lumiscaling)
  LM1_res_err = getErrSum(numbers, ["LM1"], lumiscaling)

  qcd_pred = getBkgPred(qcd_res, qcd_res_err)
  stop_pred = getBkgPred(stop_res, stop_res_err)
  wjets_pred = getBkgPred(wjets_res, wjets_res_err)
  ttjets_pred = getBkgPred(ttjets_res, ttjets_res_err)
  dy_pred = getBkgPred(dy_res, dy_res_err)
  totBkg_pred = getBkgPred(totalBkg, totalBkgErr)
  data_pred = getBkgPred(data_res, data_res_err)
  data_2011_pred = getBkgPred(data_res, data_res_err)
  data_2010_pred = getBkgPred(data_res, data_res_err)

  kappaRelErr = sqrt( (totalBkgErr["A"]/totalBkg["A"])**2 + (totalBkgErr["B"]/totalBkg["B"])**2 + (totalBkgErr["C"]/totalBkg["C"])**2 + (totalBkgErr["D"]/totalBkg["D"])**2 )
  sigCont = {}
  for r in regions:
    sigCont[r]={}
    for s in ["LM9","LM1"]:
      sigCont[r][s] = (getBkgSum(numbers, [s], lumiscaling)[r] / (qcd_res[r] + wjets_res[r] + ttjets_res[r]))
  print "preSelection:",preSelectionROOTCut
  print "region-Cuts :",cuts
  print "########### Numbers ##############"
  print "tot. ABCD: total: "+niceNum(totalBkg["LB"])+"QCD:"+ niceNum(qcd_res["LB"])+"WJets"+ niceNum(wjets_res["LB"])+"TTJets"+ niceNum(ttjets_res["LB"])+"DY"+ niceNum(dy_res["LB"])+"sTop"+ niceNum(stop_res["LB"])+"LM9"+ niceNum(LM9_res["LB"])+"LM1"+niceNum(LM1_res["LB"])+"Data-2010"+ niceNum(data_2010_res["LB"])+"Data-2011"+ niceNum(data_2011_res["LB"])+"Data"+ niceNum(data_res["LB"])+"sC-LM9"+niceNum(sigCont["LB"]["LM9"])+"sC-LM1"+niceNum(sigCont["LB"]["LM1"])
  print "Bkg:     A total: "+niceNum(totalBkg["A"])+"QCD:"+ niceNum(qcd_res["A"] ) +"WJets"+ niceNum(wjets_res["A"] )+"TTJets"+ niceNum(ttjets_res["A"] )+"DY"+ niceNum(dy_res["A"] )+"sTop"+ niceNum(stop_res["A"] )+"LM9"+ niceNum(LM9_res["A"] )+"LM1"+niceNum(LM1_res["A"] )+"Data-2010"+ niceNum(data_2010_res["A"] )+"Data-2011"+ niceNum(data_2011_res["A"] )+"Data"+ niceNum(data_res["A"] )+"sC-LM9"+niceNum(sigCont["A"]["LM9"])+"sC-LM1"+niceNum(sigCont["A"]["LM1"])
  print "Bkg.     B total: "+niceNum(totalBkg["B"])+"QCD:"+ niceNum(qcd_res["B"] ) +"WJets"+ niceNum(wjets_res["B"] )+"TTJets"+ niceNum(ttjets_res["B"] )+"DY"+ niceNum(dy_res["B"] )+"sTop"+ niceNum(stop_res["B"] )+"LM9"+ niceNum(LM9_res["B"] )+"LM1"+niceNum(LM1_res["B"] )+"Data-2010"+ niceNum(data_2010_res["B"] )+"Data-2011"+ niceNum(data_2011_res["B"] )+"Data"+ niceNum(data_res["B"] )+"sC-LM9"+niceNum(sigCont["B"]["LM9"])+"sC-LM1"+niceNum(sigCont["B"]["LM1"])
  print "Bkg:     C total: "+niceNum(totalBkg["C"])+"QCD:"+ niceNum(qcd_res["C"] ) +"WJets"+ niceNum(wjets_res["C"] )+"TTJets"+ niceNum(ttjets_res["C"] )+"DY"+ niceNum(dy_res["C"] )+"sTop"+ niceNum(stop_res["C"] )+"LM9"+ niceNum(LM9_res["C"] )+"LM1"+niceNum(LM1_res["C"] )+"Data-2010"+ niceNum(data_2010_res["C"] )+"Data-2011"+ niceNum(data_2011_res["C"] )+"Data"+ niceNum(data_res["C"] )+"sC-LM9"+niceNum(sigCont["C"]["LM9"])+"sC-LM1"+niceNum(sigCont["C"]["LM1"])
  print "Sig.     D total: "+niceNum(totalBkg["D"])+"QCD:"+ niceNum(qcd_res["D"] ) +"WJets"+ niceNum(wjets_res["D"] )+"TTJets"+ niceNum(ttjets_res["D"] )+"DY"+ niceNum(dy_res["D"] )+"sTop"+ niceNum(stop_res["D"] )+"LM9"+ niceNum(LM9_res["D"] )+"LM1"+niceNum(LM1_res["D"] )+"Data-2010"+ niceNum(data_2010_res["D"] )+"Data-2011"+ niceNum(data_2011_res["D"] )+"Data"+ niceNum(data_res["D"] )+"SB-LM9"+niceNum(sigCont["D"]["LM9"])+"SB-LM1"+niceNum(sigCont["D"]["LM1"])
#  print "########### Errors ##############"
#  print "tot. ABCD: total: "+niceNum(totalBkgErr["LB"])+"QCD:"+ niceNum(qcd_res_err["LB"])+"WJets"+ niceNum(wjets_res_err["LB"])+"TTJets"+ niceNum(ttjets_res_err["LB"])+"DY"+ niceNum(dy_res_err["LB"])+"sTop"+ niceNum(stop_res_err["LB"])+"LM9"+ niceNum(LM9_res_err["LB"])+"LM1"+niceNum(LM1_res_err["LB"])+"Data"+ niceNum(sqrt(data_res["LB"]))
#  print "Bkg:     A total: "+niceNum(totalBkgErr["A"])+"QCD:"+ niceNum(qcd_res_err["A"] ) +"WJets"+ niceNum(wjets_res_err["A"] )+"TTJets"+ niceNum(ttjets_res_err["A"] )+"DY"+ niceNum(dy_res_err["A"] )+"sTop"+ niceNum(stop_res_err["A"] )+"LM9"+ niceNum(LM9_res_err["A"] )+"LM1"+niceNum(LM1_res_err["A"] )+"Data"+ niceNum(sqrt(data_res["A"]) )
#  print "Bkg.     B total: "+niceNum(totalBkgErr["B"])+"QCD:"+ niceNum(qcd_res_err["B"] ) +"WJets"+ niceNum(wjets_res_err["B"] )+"TTJets"+ niceNum(ttjets_res_err["B"] )+"DY"+ niceNum(dy_res_err["B"] )+"sTop"+ niceNum(stop_res_err["B"] )+"LM9"+ niceNum(LM9_res_err["B"] )+"LM1"+niceNum(LM1_res_err["B"] )+"Data"+ niceNum(sqrt(data_res["B"]) )
#  print "Bkg:     C total: "+niceNum(totalBkgErr["C"])+"QCD:"+ niceNum(qcd_res_err["C"] ) +"WJets"+ niceNum(wjets_res_err["C"] )+"TTJets"+ niceNum(ttjets_res_err["C"] )+"DY"+ niceNum(dy_res_err["C"] )+"sTop"+ niceNum(stop_res_err["C"] )+"LM9"+ niceNum(LM9_res_err["C"] )+"LM1"+niceNum(LM1_res_err["C"] )+"Data"+ niceNum(sqrt(data_res["C"]) )
#  print "Sig.     D total: "+niceNum(totalBkgErr["D"])+"QCD:"+ niceNum(qcd_res_err["D"] ) +"WJets"+ niceNum(wjets_res_err["D"] )+"TTJets"+ niceNum(ttjets_res_err["D"] )+"DY"+ niceNum(dy_res_err["D"] )+"sTop"+ niceNum(stop_res_err["D"] )+"LM9"+ niceNum(LM9_res_err["D"] )+"LM1"+niceNum(LM1_res_err["D"] )+"Data"+ niceNum(sqrt(data_res["D"]) )
  print "#################################"
  print "kappa total", kappa(totalBkg),"+/-",kappaRelErr*kappa(totalBkg), "kappa WJets", kappa(wjets_res), "kappa TTJets", kappa(ttjets_res)
  print "true Bkg            :"+ niceNum(totalBkg["D"])
  print "                est.:"+niceNum(totalBkg["B"]*totalBkg["C"]/totalBkg["A"])
  print "Discovery: est.w/LM9:"+niceNum((totalBkg["B"] + LM9_res["B"])*(totalBkg["C"]+LM9_res["C"])/(totalBkg["A"]+LM9_res["A"]))+"tot. D"+niceNum(totalBkg["D"]+LM9_res["D"])+"est.w/LM1:"+niceNum((totalBkg["B"])) 
  diff_a = -1. 
  diff_b = -1. 
  diff_c = -1.   
  if totalBkg["A"] > LM9_res["A"]:
    diff_a = totalBkg["A"] - LM9_res["A"]
  else:
    print "More than 100% sig-cont in A"
  if totalBkg["B"] > LM9_res["B"]:
    diff_b = totalBkg["B"] - LM9_res["B"]
  else:
    print "More than 100% sig-cont in B" 
  if totalBkg["C"] > LM9_res["C"]:
    diff_c = totalBkg["C"] - LM9_res["C"]
  else:
    print "More than 100% sig-cont in C" 
  est_w_LM9=0.
  if diff_a>0. and diff_b > 0. and diff_c>0.:
    est_w_LM9 = diff_b*diff_c/diff_a
  totaltrueBkgA =totalBkg["A"] 
  totaltrueBkgB =totalBkg["B"] 
  totaltrueBkgC =totalBkg["C"] 
  stat_err =  sqrt( totaltrueBkgA * diff_b**2 * diff_c**2/diff_a**4 + totaltrueBkgB*diff_c**2/diff_a**2 + totaltrueBkgC*diff_b**2/diff_a**2 )
  sys_err = 0.2*est_w_LM9
  err = sqrt(sys_err*sys_err + stat_err*stat_err)
  print "Exclusion: est.w/LM9:"+niceNum(est_w_LM9)+"tot. D"+niceNum(totalBkg["D"]+LM9_res["D"])+"est.w/LM1:"+niceNum((totalBkg["B"] - LM1_res["B"])*(totalBkg["C"] - LM1_res["C"])/(totalBkg["A"] - LM1_res["A"])) 
  print "Errors: stat/sys/tot"+niceNum(stat_err)+niceNum(sys_err)+niceNum(err)
  if est_w_LM9 <0.01:
    print "Warning! Estimation of Bkg is zero!"
#  excl = BayesianUpperLimit(int(totalBkg["D"]), 0., est_w_LM9, err, 0.95, 0.02)
#  print "excl/LM9:",excl
  print

  print "$t\\bar t$       & $"+ niceNum(ttjets_res["A"] )+"\\pm"+niceNum(ttjets_res_err["A"] )+"$ & $"+ niceNum(ttjets_res["B"] )+"\\pm"+niceNum(ttjets_res_err["B"] )+"$ & $"+ niceNum(ttjets_res["C"] )+"\\pm"+niceNum(ttjets_res_err["C"] )+"$ & $"+ niceNum(ttjets_res["D"] )+"\\pm"+niceNum(ttjets_res_err["D"] )+"$ & $" +niceNum(ttjets_pred[0]  )+"\\pm"+niceNum( ttjets_pred[1])+"$\\\\"
  print "$W$ + jets      & $ "+ niceNum(wjets_res["A"] )+"\\pm"+niceNum(wjets_res_err["A"] )  +"$ & $"+ niceNum(wjets_res["B"] )+"\\pm" +niceNum(wjets_res_err["B"] ) +"$ & $"+ niceNum(wjets_res["C"] )+"\\pm"+niceNum(wjets_res_err["C"] )  +"$ & $"+ niceNum(wjets_res["D"] )+"\\pm"+niceNum(wjets_res_err["D"] )  +"$ & $" +niceNum(wjets_pred[0]  )+"\\pm"+niceNum( wjets_pred[1])  +"$\\\\"
  print "single top      & $ "+ niceNum(stop_res["A"] )+"\\pm"+niceNum(stop_res_err["A"] ) +   "$ & $"+ niceNum(stop_res["B"] )+"\\pm"  +niceNum(stop_res_err["B"] )  +"$ & $"+ niceNum(stop_res["C"] )+"\\pm"+niceNum(stop_res_err["C"] )    +"$ & $"+ niceNum(stop_res["D"] )+"\\pm"+niceNum(stop_res_err["D"] )    +"$ & $" +niceNum(stop_pred[0]   )+"\\pm"+niceNum( stop_pred[1])   +"$\\\\"
  print "Drell-Yan       & $ "+ niceNum(dy_res["A"] )+"\\pm"+niceNum(dy_res_err["A"] )   +     "$ & $"+ niceNum(dy_res["B"] )+"\\pm"    +niceNum(dy_res_err["B"] )   + "$ & $"+ niceNum(dy_res["C"] )+"\\pm"+niceNum(dy_res_err["C"] )        +"$ & $"+ niceNum(dy_res["D"] )+"\\pm"+niceNum(dy_res_err["D"] )        +"$ & $"+niceNum(dy_pred[0]     )+"\\pm"+niceNum( dy_pred[1])      +"$\\\\"
  print "QCD             & $ "+ niceNum(qcd_res["A"] )+"\\pm"+niceNum(qcd_res_err["A"] ) +     "$ & $"+ niceNum(qcd_res["B"] )+"\\pm"   +niceNum(qcd_res_err["B"] )   +"$ & $"+ niceNum(qcd_res["C"] )+"\\pm"+niceNum(qcd_res_err["C"] )      +"$ & $"+ niceNum(qcd_res["D"] )+"\\pm"+niceNum(qcd_res_err["D"] )      +"$ & $"+niceNum(qcd_pred[0]    )+"\\pm"+niceNum( qcd_pred[1])     +"$\\\\"
  print "total SM MC     & $ "+ niceNum(totalBkg["A"] )+"\\pm"+niceNum(totalBkgErr["A"] ) +    "$ & $"+ niceNum(totalBkg["B"] )+"\\pm"  +niceNum(totalBkgErr["B"] )   +"$ & $"+ niceNum(totalBkg["C"] )+"\\pm"+niceNum(totalBkgErr["C"] )     +"$ & $"+ niceNum(totalBkg["D"] )+"\\pm"+niceNum(totalBkgErr["D"] )     +"$ & $"+niceNum(totBkg_pred[0] )+"\\pm"+niceNum( totBkg_pred[1])+  "$\\\\ \\hline"
  print "data            & $ "+ niceNum(data_res["A"] )+   "$ & $"+ niceNum(data_res["B"] )+"$ & $"+ niceNum(data_res["C"]) +"$ & $"+ niceNum(data_res["D"] ) +"$ & $"+niceNum(data_pred[0]   )  +"$\\\\"


def analyzeDir(datapath):
  all_bkg=[]
  all_bkg.extend(QCD_Bins)
  all_bkg.extend(WJets_Bins)
  all_bkg.extend(["TTJets"])
  filelist=os.listdir(datapath)
  for thisfile in filelist:
    if thisfile[-3:]==".py":
      filename = datapath+"/"+thisfile
      exec(file(filename,"r").read())
      totalBkg = {}
      for r in regions:
        totalBkg[r]=0.
        for bkg in  all_bkg:
          if numbers[bkg]["Events"].has_key(r):
            totalBkg[r]+=numbers[bkg]["Events"][r]
      kappaVal = kappa(totalBkg)
      if kappaVal>0 and fabs(1.-kappaVal)<0.07:
        lm9 = numbers["LM9"]["Events"]["D"]
        lm1 = numbers["LM1"]["Events"]["D"]
        SoverB_lm9 = numbers["LM9"]["Events"]["D"]/totalBkg["D"]
        SoverB_lm1 = numbers["LM1"]["Events"]["D"]/totalBkg["D"]
        relstaterr = sqrt(1./totalBkg["A"] + 1./totalBkg["B"] + 1./totalBkg["C"])
        sigContB_lm9 = numbers["LM9"]["Events"]["B"]/totalBkg["B"]
        sigContC_lm9 = numbers["LM9"]["Events"]["C"]/totalBkg["C"]
        sigContB_lm1 = numbers["LM1"]["Events"]["B"]/totalBkg["B"]
        sigContC_lm1 = numbers["LM1"]["Events"]["C"]/totalBkg["C"]
        if SoverB_lm9>1 and sigContB_lm9 + sigContC_lm9 < 0.55:
          print thisfile, "LM9", lm9, "LM1", lm1, "S/B LM9",SoverB_lm9,"S/B LM1",SoverB_lm1, "sigContC-LM9", sigContB_lm9, "sigContC-LM9", sigContC_lm9, "now analyzing ..."
          analyze(datapath+thisfile)
