import ROOT, pickle

from Workspace.RA4Analysis.simplePlotsCommon import *
from math import *
from simpleStatTools import niceNum
subdir = "/afs/hephy.at/scratch/s/schoefbeck/CMS/CMSSW_4_2_8_patch7/src/Workspace/RA4Analysis/plots/pickle/"
#mode = "Mu"
#mode = "Ele"

computeUpperLimits = True
#computeUpperLimits = False
#writeYield = True
writeYield = False

if computeUpperLimits:
  from PBayesianUpperLimit import BayesianUpperLimit

binningHT =  [750, 1000]
binningMET = [250, 350, 450, 550]

bjetbins = {"inc":"(1)", \
#            "b0":"(!(btag0>1.74))",
#            "b1":"(btag0>1.74&&(!(btag1>1.74)))",
            "b1p":"(btag0>1.74)",
#            "b2":"(btag1>1.74)"
            } 

bjetbinsPy = {}
for bj in bjetbins.keys():
  bjetbinsPy[bj] = bjetbins[bj].replace("&&"," and ").replace("!", " not ")
commoncf = {}
commoncf["Mu"] = "jet2pt>40&&ht>750&&barepfmet>250&&singleMuonic&&nvetoMuons==1&&nvetoElectrons==0"  
commoncf["Ele"] = "jet2pt>40&&ht>750&&barepfmet>250&&singleElectronic&&nvetoElectrons==1&&nvetoMuons==0"  
  
if writeYield:
  print "Computing & saving Bkg and LM6-signal yield"
  bkg = {}
  sig = {}
  bkg["Mu"] = ROOT.TChain("Events")
  sig["Mu"] = ROOT.TChain("Events")
  bkg["Ele"] = ROOT.TChain("Events")
  sig["Ele"] = ROOT.TChain("Events")

  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/DYtoLL-M50/histo_DYtoLL-M50_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/TTJets/histo_TTJets_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/WJets-HT300/histo_WJets-HT300_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/T-s/histo_T-s_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/T-t/histo_T-t_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/T-tW/histo_T-tW_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/Tbar-s/histo_Tbar-s_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/Tbar-t/histo_Tbar-t_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/Tbar-tW/histo_Tbar-tW_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/QCD_Pt-120to150_MuPt5Enriched/histo_QCD_Pt-120to150_MuPt5Enriched_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/QCD_Pt-150_MuPt5Enriched/histo_QCD_Pt-150_MuPt5Enriched_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/QCD_Pt-20to30_MuPt5Enriched/histo_QCD_Pt-20to30_MuPt5Enriched_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/QCD_Pt-30to50_MuPt5Enriched/histo_QCD_Pt-30to50_MuPt5Enriched_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/QCD_Pt-50to80_MuPt5Enriched/histo_QCD_Pt-50to80_MuPt5Enriched_pf-3j40.root")
  bkg["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/QCD_Pt-80to120_MuPt5Enriched/histo_QCD_Pt-80to120_MuPt5Enriched_pf-3j40.root")
  sig["Mu"].Add("/data/schoef/convertedTuples_v6/copy/Mu/LM6/histo_LM6_pf-3j40.root")

  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/DYtoLL-M50/histo_DYtoLL-M50_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/TTJets/histo_TTJets_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/WJets-HT300/histo_WJets-HT300_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/T-s/histo_T-s_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/T-t/histo_T-t_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/T-tW/histo_T-tW_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/Tbar-s/histo_Tbar-s_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/Tbar-t/histo_Tbar-t_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/Tbar-tW/histo_Tbar-tW_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_BCtoE_Pt20to30/histo_QCD_BCtoE_Pt20to30_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_BCtoE_Pt30to80/histo_QCD_BCtoE_Pt30to80_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_BCtoE_Pt80to170/histo_QCD_BCtoE_Pt80to170_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_EMEnriched_Pt20to30/histo_QCD_EMEnriched_Pt20to30_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_EMEnriched_Pt30to80/histo_QCD_EMEnriched_Pt30to80_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_EMEnriched_Pt80to170/histo_QCD_EMEnriched_Pt80to170_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_Pt170to300/histo_QCD_Pt170to300_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_Pt300to470/histo_QCD_Pt300to470_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_Pt470to600/histo_QCD_Pt470to600_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_Pt600to800/histo_QCD_Pt600to800_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_Pt800to1000/histo_QCD_Pt800to1000_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_Pt1000to1400/histo_QCD_Pt1000to1400_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_Pt1400to1800/histo_QCD_Pt1400to1800_pf-3j40.root")
  bkg["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/QCD_Pt1800/histo_QCD_Pt1800_pf-3j40.root")

  sig["Ele"].Add("/data/schoef/convertedTuples_v6/copy3j/Ele/LM6/histo_LM6_pf-3j40.root")

  bkgYield = {}
  sigYield = {}
  for mode in ["Mu", "Ele"]: 
    bkgYield[mode] = {}
    sigYield[mode] = {}
    for bjb in bjetbins.keys():
      print "At mode",mode,bjb,bjetbins[bjb]
      bkg[mode].Draw(">>eListBkg", commoncf[mode]+"&&"+bjetbins[bjb])
      eListBkg = ROOT.gROOT.Get("eListBkg")
      bkgYield[mode][bjb] = {}

      for htcut in binningHT:
        bkgYield[mode][bjb][htcut] = {}
        for metcut in binningMET:
          bkgYield[mode][bjb][htcut][metcut] = 0.

      for n in range(eListBkg.GetN()):
        bkg[mode].GetEntry(eListBkg.GetEntry(n))
        ht = getValue(bkg[mode], "ht")
        met = getValue(bkg[mode], "barepfmet")
        weight = getValue(bkg[mode], "weight")
        for htcut in binningHT:
          if ht>htcut:
            for metcut in binningMET:
              if met > metcut:
                bkgYield[mode][bjb][htcut][metcut] += weight
      del eListBkg 

      sig[mode].Draw(">>eListSig", commoncf[mode]+"&&"+bjetbins[bjb])
      eListSig = ROOT.gROOT.Get("eListSig")
      sigYield[mode][bjb] = {}
      for htcut in binningHT:
        sigYield[mode][bjb][htcut] = {}
        for metcut in binningMET:
          sigYield[mode][bjb][htcut][metcut] = 0.

      for n in range(eListSig.GetN()):
        sig[mode].GetEntry(eListSig.GetEntry(n))
        ht = getValue(sig[mode], "ht")
        met = getValue(sig[mode], "barepfmet")
        weight = getValue(sig[mode], "weight")
        for htcut in binningHT:
          if ht>htcut:
            for metcut in binningMET:
              if met > metcut:
                sigYield[mode][bjb][htcut][metcut] += weight 
      del eListSig
  pickle.dump(bkgYield,  open(subdir+'/bkgYield.pkl', 'wb'))
  print "Written", subdir+"/bkgYield.pkl"
  pickle.dump(sigYield,  open(subdir+'/sigYield.pkl', 'wb'))
  print "Written", subdir+"/sigYield.pkl"
#  def SoverSqrtB(bjb, ht, met):
#    if sigYield[bjb][ht][met] == bkgYield[bjb][ht][met] ==0:
#      return float('nan')
#    if bkgYield[bjb][ht][met]>0:
#      return sigYield[bjb][ht][met]/sqrt(bkgYield[bjb][ht][met])
#    else:
#      return float('inf')
#
#  for bjb in bjetbins:
#    results = []
#    for htcut in binningHT:
#      for metcut in binningMET:
#        results.append([SoverSqrtB(bjb, htcut, metcut), htcut, metcut, sigYield[bjb][htcut][metcut], bkgYield[bjb][htcut][metcut]])
#
#    results.sort()
#    print "###################",bjb,"########################"
#    for res in results:
#      SoverB = float('inf')
#      if res[4]>0:
#        SoverB = res[3]/res[4]
#      print "S/sqrt(B):", niceNum(res[0]), "HTcut", niceNum(res[1]),"MetCut",niceNum(res[2]),"S",niceNum(res[3]), "B",niceNum(res[4]), "S/B", niceNum(SoverB)

if not writeYield:
  print "Loading "+subdir+"/bkgYield.pkl"
  globals()["bkgYield"] = pickle.load(open(subdir+'/bkgYield.pkl'))
  print "Loading "+subdir+"/sigYield.pkl"
  globals()["sigYield"] = pickle.load(open(subdir+'/sigYield.pkl'))

if computeUpperLimits:
  observedlimit = {}
  expectedlimit = {}
  totalSysUncert = {}
  totalSysUncert["Mu" ] = {}
  totalSysUncert["Ele"] = {}
  for bjb in bjetbins.keys():
    observedlimit[bjb]={}
    expectedlimit[bjb]={}
    totalSysUncert["Mu"][bjb] = {}
    totalSysUncert["Ele"][bjb] = {}
    for htcut in binningHT:
      observedlimit[bjb][htcut]={}
      expectedlimit[bjb][htcut]={}
      totalSysUncert["Mu" ][bjb][htcut] = {}
      totalSysUncert["Ele"][bjb][htcut] = {}
      for metcut in binningMET:
        observedlimit[bjb][htcut][metcut]=-1
        expectedlimit[bjb][htcut][metcut]=-1
        execfile("/afs/hephy.at/user/s/schoefbeck/www/systematicResults/systematics_htSig-"+str(htcut)+"_metSig-"+str(metcut)+".py")
        for mode in ["Mu", "Ele"]:
          totalSysUncert2 = 0. 
          for sys in largestAbsDoubleRatioDeviation.keys():
            uncert = min(largestAbsDoubleRatioDeviation[sys][mode][bjb], largestAbsSingleRatioDeviation[sys][mode][bjb])
            print mode, "DR.-Sys:", "htSig-"+str(htcut)+"_metSig-"+str(metcut),"sys",sys,"bjb",bjb,niceNum(largestAbsDoubleRatioDeviation[sys][mode][bjb]), "SR.-Sys:", niceNum(largestAbsSingleRatioDeviation[sys][mode][bjb]), "picked:",niceNum(uncert)
            totalSysUncert2+=uncert**2

          totalSysUncert[mode][bjb][htcut][metcut] = {"MC":sqrt(totalSysUncert2 + relStatErrMC[mode][bjb]**2), "Data":sqrt(totalSysUncert2 + relStatErrData[mode][bjb]**2)}
          print mode, "Total sys. uncert. for ","htSig-"+str(htcut)+"_metSig-"+str(metcut), "bjb",bjb,": MC", niceNum(totalSysUncert[mode][bjb][htcut][metcut]["MC"]),"Data:",niceNum(totalSysUncert[mode][bjb][htcut][metcut]["Data"]),"stat.uncert: MC:",niceNum(relStatErrMC[mode][bjb]),"Data:",niceNum(relStatErrData[mode][bjb])

        nSig = bkgYield["Mu"][bjb][htcut][metcut] + bkgYield["Ele"][bjb][htcut][metcut]
        epsilon = 0.2
        nSig_Err = sqrt((totalSysUncert["Mu"][bjb][htcut][metcut]["MC"]*bkgYield["Mu"][bjb][htcut][metcut])**2 + (totalSysUncert["Ele"][bjb][htcut][metcut]["MC"]*bkgYield["Ele"][bjb][htcut][metcut])**2)
#        precision = 0.008
        precision = 0.025
        cl = 0.95
        expectedlimit[bjb][htcut][metcut] = BayesianUpperLimit(int(nSig),epsilon,nSig,nSig_Err,cl,precision)

        nSigObserved = dataCount["Mu"][bjb] + dataCount["Ele"][bjb]
        nSigPredicted = dataPrediction["Mu"][bjb] + dataPrediction["Ele"][bjb]
        nSigPredicted_Err = sqrt((totalSysUncert["Mu"][bjb][htcut][metcut]["Data"]*dataPrediction["Mu"][bjb])**2 + (totalSysUncert["Ele"][bjb][htcut][metcut]["Data"]*dataPrediction["Ele"][bjb])**2)
        epsilon = 0.
        observedlimit[bjb][htcut][metcut] = BayesianUpperLimit(int(nSigObserved),epsilon,nSigPredicted,nSigPredicted_Err,cl,precision)

        print bjb,htcut,metcut,"Bkg:",niceNum(nSig),"+/-",niceNum(nSig_Err), "expected limit", niceNum(expectedlimit[bjb][htcut][metcut]), "obs:", nSigObserved,"Predicted:",nSigPredicted,"+/-",niceNum(nSigPredicted_Err), "observed limit:", niceNum(observedlimit[bjb][htcut][metcut])
  pickle.dump(expectedlimit,  open(subdir+'/expectedlimit.pkl', 'wb'))
  pickle.dump(observedlimit,  open(subdir+'/observedlimit.pkl', 'wb'))
  print "Written ", subdir+"/limit.pkl"

#if not computeUpperLimits:
#  print "Loading pickle/limit.pkl"
#  globals()["limit"] =  pickle.load(open(subdir+'/limit.pkl'))
#results=[]
#for bjb in bjetbins.keys():
#  for htcut in binningHT:
#    for metcut in binningMET:
#      if limit[bjb][htcut][metcut]>0:
#        results.append([sigYield[bjb][htcut][metcut] / limit[bjb][htcut][metcut], bjb, htcut, metcut, sigYield[bjb][htcut][metcut], bkgYield[bjb][htcut][metcut],limit[bjb][htcut][metcut]])
#results.sort()
#for res in results:
#  print "sig/limit:", niceNum(res[0]), "bjb",res[1],"HTcut", niceNum(res[2]),"MetCut",niceNum(res[3]),"S",niceNum(res[4]),"B", niceNum(res[5]), "L",niceNum(res[6])
