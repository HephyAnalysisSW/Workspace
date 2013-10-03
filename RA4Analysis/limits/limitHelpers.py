from optparse import OptionParser
import os, sys, pickle
import ROOT
ROOT.gROOT.ProcessLine(".L ../scripts/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)

ROOT.gROOT.ProcessLine(".L TriangularInterpolation.C+")
from interpolateContamination import interpolateContamination
path = os.path.abspath('../plots')
if not path in sys.path:
    sys.path.insert(1, path)

del path
from analysisHelpers import *
from xsecSMS import gluino8TeV_NLONLL
#ROOT.gROOT.ProcessLine(".L Chol.C+")
htb = [750, 2500]
doOnlyOneJob = []

from smsInfo import th2Binning

########### steering ############
writeModelFiles = True               #Whether to write model files to modelFiles_prefix (usually true, if false it tries to load from the directory. May be helpful to calc. asymptotic for an existing dir.)
writeGridDirectories = False           #Whether to write grid directories
calcAsymptotic = True                #Whether to calculate the asymptotic limit (writes into resultsAsymptotic_prefix)
correctSignalYieldForFastSim = True   #Whether to use acceptance corrections (should be true)

prefix =  "test"  #will be used in foldernames, etc.
useHT500_3b = True
if useHT500_3b:
  prefix=prefix+"_HT500"
unifiedLowHT = True
useHT1000Inconsistent = False
if useHT1000Inconsistent:
  prefix=prefix+"_useHT1000Inconsistent"
if not unifiedLowHT:
  prefix=prefix+"_splitLowHT"
estimationModifier=1.
#estimationModifier=0.9
if estimationModifier!=1.:
  prefix=prefix+"_estimationModifier_"+str(estimationModifier)
########### select SMS############
sms = "T1tttt-madgraph"  #
#sms = "T5tttt"
#sms = "T1t1t"
doOnlyOneJob = [1150,0] #For testing; comment for full run
##################################
if unifiedLowHT:
  templateFileName = "templateCard_3b_unifiedLowHT.txt"
else:
  templateFileName = "templateCard_3b.txt"

smsPrefix={}
#smsPrefix["T1tttt"] = ""
smsPrefix["T1tttt-madgraph"] = "T1tttt-madgraph_"
smsPrefix["T1t1t"] = "T1t1t_"
smsPrefix["T5tttt"] = "T5tttt_"

smoothingPostFixISR = {}
#smoothingPostFixISR["T1tttt"]           = "_smoothed"
smoothingPostFixISR["T1tttt-madgraph"]  = ""
smoothingPostFixISR["T1t1t"] = ""
smoothingPostFixISR["T5tttt"] = ""

smoothingPostFixPDF = {}
#smoothingPostFixPDF["T1tttt"] = "_smoothed"
smoothingPostFixPDF["T1tttt-madgraph"] = ""
smoothingPostFixPDF["T1t1t"] = ""
smoothingPostFixPDF["T5tttt"] = ""

modelDir = {}
modelDir["T1tttt"] = "/data/adamwo/convertedTuples_v16/copyMET/"
modelDir["T1tttt-madgraph"] = "/data/schoef/convertedTuples_v19/copyMET/"
modelDir["T5tttt"] = "/data/schoef/convertedTuples_v19/copyMET/"
modelDir["T1t1t"] =  "/data/schoef/convertedTuples_v19/copyMET/"

sigContRefmgl={}
sigContRefmgl["T1tttt"] = 1100
sigContRefmgl["T5tttt"] = 1100
sigContRefmgl["T1tttt-madgraph"] = 1100

sigContInDir={}
sigContInDir["T1tttt-madgraph"] = "/data/schoef/results2012/T1tttt-madgraph/sigCont/"
sigContInDir["T5tttt"] = "/data/schoef/results2012/T5tttt/sigCont/"
sigContInDir["T1t1t"] = "/data/schoef/results2012/T1t1t/sigCont/"

if sms=="T1tttt" or sms=="T1tttt-madgraph":
  varXmin = 400
  varXmax = 1525

if sms=="T1t1t":
  varXmin = 200 
  varXmax = 825

if sms=="T5tttt":
  varXmin = 800 
  varXmax = 1425

#modifyDeltaBetaAndClosure = False

doSigCont = True
dirname = prefix+"_"+sms

#if modifyDeltaBetaAndClosure:
#  dirname+="_modifiedDeltaBeta"

metbins = [[250,350],[350,450],[450,2500]]
lowHTBin = (400, 750)
lowHT500Bin = (500, 750)
lowHTmetbins = [[150,250],[250,2500]]

cData = getRefChain(mode = "Data")

def loadFromFileOrCanvas(file, obj,canv='c1'):
  res = getObjFromFile(file, obj) 
  if not res:
    ctmp = getObjFromFile(file, canv)
    res = ctmp.GetPrimitive(obj).Clone(obj)
    del ctmp
  return res

prec = 8
allFiles=[]
SpF         = pickle.load(file('../results/copyMET_fullMC_v19_GluSplitFixed_jackKnifeSpF.pkl'))
SpFJESPlus  = pickle.load(file('../results/copyMET_JES+_minimal_jackKnifeSpF.pkl'))
SpFJESMinus = pickle.load(file('../results/copyMET_JES-_minimal_jackKnifeSpF.pkl'))
SpFSysDataMC =pickle.load(file('../results/SpillFactorDataMCSys.pkl'))

#BTag and JES Systematics
btag_SFb_2b_sigsyshisto = {}
btag_SFl_2b_sigsyshisto = {}
btag_SFb_3b_sigsyshisto = {}
btag_SFl_3b_sigsyshisto = {}
jes_2b_sigsyshisto = {}
jes_3b_sigsyshisto = {}
PU_sigsyshisto={}
MuEff1_sigsyshisto={}
MuEff2_sigsyshisto={}
EleEff_sigsyshisto={}
sigCont_histo = {}
SpFJES_sys={}
SpFSFb_sys={}
SpFSFl_sys={}
SpFcFrac_sys={}
SpFgluSplit_sys={}
sigCont = {}
for metb in metbins+[(150,250)]:
  if not writeModelFiles:continue
  jes_2b_sigsyshisto[tuple(metb)] =       loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/JES//sigJESSys_'+smsPrefix[sms]+'bt2_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc') 
  jes_3b_sigsyshisto[tuple(metb)] =       loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/JES//sigJESSys_'+smsPrefix[sms]+'bt3p_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc') 
  btag_SFb_2b_sigsyshisto[tuple(metb)] =  loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/SFb/sigSFbSys_'+smsPrefix[sms]+'bt2_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc') 
  btag_SFb_3b_sigsyshisto[tuple(metb)] =  loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/SFb/sigSFbSys_'+smsPrefix[sms]+'bt3p_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc') 
  btag_SFl_2b_sigsyshisto[tuple(metb)] =  loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/SFl/sigSFlSys_'+smsPrefix[sms]+'bt2_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc') 
  btag_SFl_3b_sigsyshisto[tuple(metb)] =  loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/SFl/sigSFlSys_'+smsPrefix[sms]+'bt3p_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc') 
  MuEff1_sigsyshisto[tuple(metb)] =       loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/MuEff1/sigMuEff1Sys_'+smsPrefix[sms]+'ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc', 'c1_n2') 
  MuEff2_sigsyshisto[tuple(metb)] =       loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/MuEff2/sigMuEff2Sys_'+smsPrefix[sms]+'ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc', 'c1_n2') 
  EleEff_sigsyshisto[tuple(metb)] =       loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/EleEff/sigEleEffSys_'+smsPrefix[sms]+'ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc', 'c1_n2') 

  spfRef = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF']['3po2']['rForData']
  spfJESPlus = SpFJESPlus[tuple(htb)][tuple(metb)][(6,99)]['SF']['3po2']['rForData']
  spfJESMinus = SpFJESMinus[tuple(htb)][tuple(metb)][(6,99)]['SF']['3po2']['rForData']
  spfSFbPlus = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_b_Up']['3po2']['rForData']
  spfSFbMinus = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_b_Down']['3po2']['rForData']
  spfSFlPlus = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_light_Up']['3po2']['rForData']
  spfSFlMinus = SpF[tuple(htb)][tuple(metb)][(6,99)]['SF_light_Down']['3po2']['rForData']
  spfcFracPlus = SpF[tuple(htb)][tuple(metb)][(6,99)]['cFracUp']['3po2']['rForData']
  spfcFracMinus = SpF[tuple(htb)][tuple(metb)][(6,99)]['cFracDown']['3po2']['rForData']
  spfgluSplitPlus = SpF[tuple(htb)][tuple(metb)][(6,99)]['GluSplitUp']['3po2']['rForData']
  spfgluSplitMinus = SpF[tuple(htb)][tuple(metb)][(6,99)]['GluSplitDown']['3po2']['rForData']

  SpFJES_sys[tuple(metb)] = 0.5*(spfJESPlus - spfJESMinus)/spfRef
  SpFSFb_sys[tuple(metb)] = 0.5*(spfSFbPlus - spfSFbMinus)/spfRef
  SpFSFl_sys[tuple(metb)] = 0.5*(spfSFlPlus - spfSFlMinus)/spfRef
  SpFcFrac_sys[tuple(metb)]     = 0.5*(spfcFracPlus - spfcFracMinus)/spfRef
  SpFgluSplit_sys[tuple(metb)]  = 0.5*(spfgluSplitPlus - spfgluSplitMinus)/spfRef
  if doSigCont:
    sigCont_histo[tuple(metb)] = interpolateContamination(htb, metb, inDir = sigContInDir[sms], th2Binning = th2Binning[sms]) 

  PU_sigsyshisto[tuple(metb)] = loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/PU/sigPUSys_'+smsPrefix[sms]+'ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc', 'c1_n2') 
#  if not PU_sigsyshisto[tuple(metb)]:
#    ctmp = getObjFromFile('/data/schoef/results2012/'+sms+'/PU/sigPUSys_'+smsPrefix[sms]+'ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'c1_n2')
#    PU_sigsyshisto[tuple(metb)] = ctmp.GetPrimitive('hist2DSFunc').Clone('hist2DSFunc')
#    del ctmp

btaglowHT_SFb_3b_sigsyshisto = {}
btaglowHT_SFl_3b_sigsyshisto = {}
jeslowHT_3b_sigsyshisto = {}
PUlowHT_sigsyshisto={}
MuEff1lowHT_sigsyshisto={}
MuEff2lowHT_sigsyshisto={}
EleEfflowHT_sigsyshisto={}
sigContlowHT_histo = {}
EleEfflowHT_sigsys={}
SpFlowHTJES_sys={}
SpFlowHTSFb_sys={}
SpFlowHTSFl_sys={}
SpFlowHTcFrac_sys={}
SpFlowHTgluSplit_sys={}
sigContlowHT = {}
for metb in lowHTmetbins:
  if not writeModelFiles:continue
  jeslowHT_3b_sigsyshisto[tuple(metb)]      = loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/JES/sigJESSys_'+smsPrefix[sms]+'bt3p_ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc') 
  btaglowHT_SFb_3b_sigsyshisto[tuple(metb)] = loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/SFb/sigSFbSys_'+smsPrefix[sms]+'bt3p_ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc') 
  btaglowHT_SFl_3b_sigsyshisto[tuple(metb)] = loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/SFl/sigSFlSys_'+smsPrefix[sms]+'bt3p_ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc') 
  MuEff1lowHT_sigsyshisto[tuple(metb)]      = loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/MuEff1/sigMuEff1Sys_'+smsPrefix[sms]+'ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc', 'c1_n2')
  MuEff2lowHT_sigsyshisto[tuple(metb)]      = loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/MuEff2/sigMuEff2Sys_'+smsPrefix[sms]+'ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc', 'c1_n2')
  EleEfflowHT_sigsyshisto[tuple(metb)]      = loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/EleEff/sigEleEffSys_'+smsPrefix[sms]+'ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc', 'c1_n2') 

  spflowHTRef = SpF[tuple(lowHTBin)][tuple(metb)][(6,99)]['SF']['3po2']['rForData']
  spflowHTJESPlus = SpFJESPlus[tuple(lowHTBin)][tuple(metb)][(6,99)]['SF']['3po2']['rForData']
  spflowHTJESMinus = SpFJESMinus[tuple(lowHTBin)][tuple(metb)][(6,99)]['SF']['3po2']['rForData']
  spflowHTSFbPlus = SpF[tuple(lowHTBin)][tuple(metb)][(6,99)]['SF_b_Up']['3po2']['rForData']
  spflowHTSFbMinus = SpF[tuple(lowHTBin)][tuple(metb)][(6,99)]['SF_b_Down']['3po2']['rForData']
  spflowHTSFlPlus = SpF[tuple(lowHTBin)][tuple(metb)][(6,99)]['SF_light_Up']['3po2']['rForData']
  spflowHTSFlMinus = SpF[tuple(lowHTBin)][tuple(metb)][(6,99)]['SF_light_Down']['3po2']['rForData']
  spflowHTcFracPlus = SpF[tuple(lowHTBin)][tuple(metb)][(6,99)]['cFracUp']['3po2']['rForData']
  spflowHTcFracMinus = SpF[tuple(lowHTBin)][tuple(metb)][(6,99)]['cFracDown']['3po2']['rForData']
  spflowHTgluSplitPlus = SpF[tuple(lowHTBin)][tuple(metb)][(6,99)]['GluSplitUp']['3po2']['rForData']
  spflowHTgluSplitMinus = SpF[tuple(lowHTBin)][tuple(metb)][(6,99)]['GluSplitDown']['3po2']['rForData']

  SpFlowHTJES_sys[tuple(metb)] = 0.5*(spflowHTJESPlus - spflowHTJESMinus)/spflowHTRef
  SpFlowHTSFb_sys[tuple(metb)] = 0.5*(spflowHTSFbPlus - spflowHTSFbMinus)/spflowHTRef
  SpFlowHTSFl_sys[tuple(metb)] = 0.5*(spflowHTSFlPlus - spflowHTSFlMinus)/spflowHTRef
  SpFlowHTcFrac_sys[tuple(metb)]     = 0.5*(spflowHTcFracPlus - spflowHTcFracMinus)/spflowHTRef
  SpFlowHTgluSplit_sys[tuple(metb)]  = 0.5*(spflowHTgluSplitPlus - spflowHTgluSplitMinus)/spflowHTRef
  if doSigCont:
    sigContlowHT_histo[tuple(metb)] = interpolateContamination(lowHTBin, metb, inDir = sigContInDir[sms], th2Binning = th2Binning[sms]) 
  PUlowHT_sigsyshisto[tuple(metb)] = loadFromFileOrCanvas('/data/schoef/results2012/'+sms+'/PU/sigPUSys_'+smsPrefix[sms]+'ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'hist2DSFunc', 'c1_n2') 

PDF_sys = {}
PDF_3b_sys = {}
PDF_3b_lowHT_sys = {}
for metb in metbins:
  c = getObjFromFile('/data/schoef/results2012/'+sms+'/PDF/sigPDFSys_'+smsPrefix[sms]+'btb2_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixPDF[sms]+'.root', 'c1')
  PDF_sys[tuple(metb)] = c.GetPrimitive('hist2DSFunc').Clone()
for metb in metbins+[(150,250)]:
  c = getObjFromFile('/data/schoef/results2012/'+sms+'/PDF/sigPDFSys_'+smsPrefix[sms]+'btb3p_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixPDF[sms]+'.root', 'c1')
  PDF_3b_sys[tuple(metb)] = c.GetPrimitive('hist2DSFunc').Clone()
for metb in lowHTmetbins:
  c = getObjFromFile('/data/schoef/results2012/'+sms+'/PDF/sigPDFSys_'+smsPrefix[sms]+'btb3p_ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixPDF[sms]+'.root', 'c1')
  PDF_3b_lowHT_sys[tuple(metb)] = c.GetPrimitive('hist2DSFunc').Clone()

ISR_sys = {}
ISR_3b_sys = {}
ISR_3b_lowHT_sys = {}
if sms=="T1tttt":
  for metb in metbins:
    c = getObjFromFile('../results/sigISRSys_'+smsPrefix[sms]+'bt2_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixISR[sms]+'.root', 'c1')
    ISR_sys[tuple(metb)] = c.GetPrimitive('hSmooth').Clone()
  for metb in metbins+[(150,250)]:
    c = getObjFromFile('../results/sigISRSys_'+smsPrefix[sms]+'bt3p_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixISR[sms]+'.root', 'c1')
    ISR_3b_sys[tuple(metb)] = c.GetPrimitive('hSmooth').Clone()
  for metb in lowHTmetbins:
    c = getObjFromFile('../results/sigISRSys_'+smsPrefix[sms]+'bt3p_ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixISR[sms]+'.root', 'c1')
    ISR_3b_lowHT_sys[tuple(metb)] = c.GetPrimitive('hSmooth').Clone()
else:
  for metb in metbins:
    ISR_sys[tuple(metb)]          = getObjFromFile('/data/schoef/results2012/'+sms+'/ISR/sigISRSys_'+smsPrefix[sms]+'bt2_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixISR[sms]+'.root', 'hist2DSFunc')
  for metb in metbins+[(150,250)]:
    ISR_3b_sys[tuple(metb)]       = getObjFromFile('/data/schoef/results2012/'+sms+'/ISR/sigISRSys_'+smsPrefix[sms]+'bt3p_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixISR[sms]+'.root', 'hist2DSFunc')
  for metb in lowHTmetbins:
    ISR_3b_lowHT_sys[tuple(metb)] = getObjFromFile('/data/schoef/results2012/'+sms+'/ISR/sigISRSys_'+smsPrefix[sms]+'bt3p_ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixISR[sms]+'.root', 'hist2DSFunc')
    


os.system('mkdir -p modelFiles_'+dirname)
allJobs = []
for varX in range(varXmin,varXmax,25):
  if sms=="T1tttt" or sms=="T1tttt-madgraph":
    varYRange = range(0,varX-175,25) 
  if sms=="T1t1t":
    varYRange = range(100,varX-75,25) 
  if sms=="T5tttt":
    varYRange = range(200,varX-175,25)
 
  for varY in varYRange:
    if globals().has_key("doOnlyOneJob") and doOnlyOneJob!=[] and [varX,varY]!=doOnlyOneJob:
      continue
    if not writeModelFiles: continue
    infile = file(templateFileName)

    replacements = [["LUMI", 1.044]]
    #background predictions and signal yields
    signalYields2b = {}
    predYieldsAreOK = False

    highHTBin = htb 
    if useHT1000Inconsistent:
      highHTBin=[1000,2500]

    for metb in metbins:
      signalYields2b[tuple(metb)] = getSignalYield('2', highHTBin, metb, 'type1phiMet', 6, varX, varY, sms, dir = modelDir[sms] , weight = "weight", correctForFastSim = correctSignalYieldForFastSim)
      if signalYields2b[tuple(metb)]:
        predYieldsAreOK = True
    signalYields3b = {}
    for metb in metbins+[[150,250]]:
      signalYields3b[tuple(metb)] = getSignalYield('3', highHTBin, metb, 'type1phiMet', 6, varX, varY, sms, dir = modelDir[sms] , weight = "weight", correctForFastSim = correctSignalYieldForFastSim)
      if signalYields3b[tuple(metb)]:
        predYieldsAreOK = True
    signalYields3blowHT = {}
    if useHT500_3b:
      sig_and_bkgLowHTBin = lowHT500Bin
    else:
      sig_and_bkgLowHTBin = lowHTBin
      
    for metb in lowHTmetbins:
      if useHT500_3b:
        signalYields3blowHT[tuple(metb)] = getSignalYield('3', lowHT500Bin, metb, 'type1phiMet', 6, varX, varY, sms, dir = modelDir[sms] , weight = "weight", correctForFastSim = correctSignalYieldForFastSim)
      else: 
        signalYields3blowHT[tuple(metb)] = getSignalYield('3', lowHTBin, metb, 'type1phiMet', 6, varX, varY, sms, dir = modelDir[sms] , weight = "weight", correctForFastSim = correctSignalYieldForFastSim)

      if signalYields3blowHT[tuple(metb)]:
        predYieldsAreOK = True
    if not unifiedLowHT:
      if useHT500_3b:
        for metb in metbins:
          signalYields3blowHT[tuple(metb)] = getSignalYield('3', lowHT500Bin, metb, 'type1phiMet', 6, varX, varY, sms, dir = modelDir[sms] , weight = "weight", correctForFastSim =  correctSignalYieldForFastSim)
      else:
        for metb in metbins:
          signalYields3blowHT[tuple(metb)] = getSignalYield('3', lowHTBin, metb, 'type1phiMet', 6, varX, varY, sms, dir = modelDir[sms] , weight = "weight", correctForFastSim =  correctSignalYieldForFastSim)

    if not predYieldsAreOK:
      print "Problem with files! Skipping",sms, varX,varY
      continue
#    if useHT500_3b and unifiedLowHT:
#      sys = pickle.load(file('../results/systTableWithHT500.pkl'))
    if unifiedLowHT:
      sys = pickle.load(file('../results/systTableLargeBinning.pkl'))
    else:
      sys = pickle.load(file('../results/systTableLargeBinning_splitLowHT.pkl'))
    replacements += [\
      #2b, highHT, 250-350 
      ["OBS0", int(sys['observed'][tuple(highHTBin)][tuple(metbins[0])])],
      ["BKG0", round(estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[0])],4)],
      ["SIG0", round(signalYields2b[tuple(metbins[0])],4)],

      #2b, highHT, 350-450 
      ["OBS1", int(sys['observed'][tuple(highHTBin)][tuple(metbins[1])])],
      ["BKG1", round(estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[1])],4)],
      ["SIG1", round(signalYields2b[tuple(metbins[1])],4)],

      #2b, highHT, 450-2500 
      ["OBS2", int(sys['observed'][tuple(highHTBin)][tuple(metbins[2])])],
      ["BKG2", round(estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[2])],4)],
      ["SIG2", round(signalYields2b[tuple(metbins[2])],4)],

      #3b, highHT, 150-250 
      ["OBS3", int(getRefYield('3', tuple(highHTBin), [150, 250], 'type1phiMet', 6, cData))],
      ["BKG3", round(estimationModifier*sys['observed'][tuple(highHTBin)]['norm']*SpF[tuple(highHTBin)][(150,250)][(6,99)]['SF']['3po2']['rForData'],4)],
      ["SIG3", round(signalYields3b[(150,250)],4)],

      #3b, highHT, 250-350 
      ["OBS4", int(getRefYield('3', tuple(highHTBin), tuple(metbins[0]), 'type1phiMet', 6, cData))],
      ["BKG4", round(estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[0])]*SpF[tuple(highHTBin)][tuple(metbins[0])][(6,99)]['SF']['3po2']['rForData'],4)],
      ["SIG4", round(signalYields3b[tuple(metbins[0])],4)],

      #3b, highHT, 350-450 
      ["OBS5", int(getRefYield('3', tuple(highHTBin), tuple(metbins[1]), 'type1phiMet', 6, cData))],
      ["BKG5", round(estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[1])]*SpF[tuple(highHTBin)][tuple(metbins[1])][(6,99)]['SF']['3po2']['rForData'],4)],
      ["SIG5", round(signalYields3b[tuple(metbins[1])],4)],

      #3b, highHT, 450-2500 
      ["OBS6", int(getRefYield('3', tuple(highHTBin), tuple(metbins[2]), 'type1phiMet', 6, cData))],
      ["BKG6", round(estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[2])]*SpF[tuple(highHTBin)][tuple(metbins[2])][(6,99)]['SF']['3po2']['rForData'],4)],
      ["SIG6", round(signalYields3b[tuple(metbins[2])],4)],

      #3b, lowHT, 150-250 
      ["OBS7", int(getRefYield('3', tuple(sig_and_bkgLowHTBin), tuple(lowHTmetbins[0]), 'type1phiMet', 6, cData))],
      ["BKG7", round(estimationModifier*sys['observed'][tuple(sig_and_bkgLowHTBin)]['norm']*SpF[tuple(lowHTBin)][tuple(lowHTmetbins[0])][(6,99)]['SF']['3po2']['rForData'],4)],
      ["SIG7", round(signalYields3blowHT[tuple(lowHTmetbins[0])],4)]]

    if unifiedLowHT:
      replacements+=[\
        #3b, lowHT, 250-2500
        ["OBS8", int(getRefYield('3', tuple(sig_and_bkgLowHTBin), tuple(lowHTmetbins[1]), 'type1phiMet', 6, cData))],
        ["BKG8", round(estimationModifier*sys['predicted'][tuple(sig_and_bkgLowHTBin)][tuple(lowHTmetbins[1])]*SpF[tuple(lowHTBin)][tuple(lowHTmetbins[1])][(6,99)]['SF']['3po2']['rForData'],4)],
        ["SIG8", round(signalYields3blowHT[tuple(lowHTmetbins[1])],4)]]
    else:
      replacements+=[\
        #3b, lowHT, 250-350 
        ["OBS8", int(getRefYield('3', tuple(sig_and_bkgLowHTBin), tuple(metbins[0]), 'type1phiMet', 6, cData))],
        ["BKG8", round(sys['predicted'][tuple(sig_and_bkgLowHTBin)][tuple(metbins[0])]*SpF[tuple(lowHTBin)][tuple(metbins[0])][(6,99)]['SF']['3po2']['rForData'],4)],
        ["SIG8", round(signalYields3blowHT[tuple(metbins[0])],4)],

        #3b, lowHT, 350-450 
        ["OBS9", int(getRefYield('3', tuple(sig_and_bkgLowHTBin), tuple(metbins[1]), 'type1phiMet', 6, cData))],
        ["BKG9", round(sys['predicted'][tuple(sig_and_bkgLowHTBin)][tuple(metbins[1])]*SpF[tuple(lowHTBin)][tuple(metbins[1])][(6,99)]['SF']['3po2']['rForData'],4)],
        ["SIG9", round(signalYields3blowHT[tuple(metbins[1])],4)],

        #3b, lowHT, 450-2500 
        ["OBS10", int(getRefYield('3', tuple(sig_and_bkgLowHTBin), tuple(metbins[2]), 'type1phiMet', 6, cData))],
        ["BKG10", round(sys['predicted'][tuple(sig_and_bkgLowHTBin)][tuple(metbins[2])]*SpF[tuple(lowHTBin)][tuple(metbins[2])][(6,99)]['SF']['3po2']['rForData'],4)],
        ["SIG10", round(signalYields3blowHT[tuple(metbins[2])],4)]]


#    # build list of sigmas / correlations
#    ratioCovM = convertMatrixToRoot(sys['predCov'][tuple(htb)])
#    for i in range(len(metbins)): #FIXME
#      for j in range(len(metbins)):
#        ratioCovM[i][j] = ratioCovM[i][j]/(sys['predMean'][tuple(htb)][tuple(metbins[i])]*sys['predMean'][tuple(htb)][tuple(metbins[j])])

    ratioCovM = pickle.load(file('../results/Cholesky_3b_unifiedLowHT.pkl'))
    tdc = ROOT.TDecompChol(ratioCovM)
    print "Cholesky decomposition successful?",tdc.Decompose()
    U = ROOT.TMatrixD(ROOT.TMatrixD.kTransposed, tdc.GetU())
#    U.Print()
#    ratioCovM.Print()
#    ROOT.TMatrixD(U, ROOT.TMatrixD.kMult, ROOT.TMatrixD(ROOT.TMatrixD.kTransposed, U)).Print()

    for i in range(4):
      for j in range(4):
        if i<j:continue
        replacements.append(["CHOL"+str(i)+str(j), 1+round(U[i][j],4)])
    #highHT normalization region systematics
    normRegYieldHighHT = round(sys['observed'][tuple(highHTBin)]['norm'] , 0)
    replacements.append(["NREG",int(normRegYieldHighHT) ])
    replacements.append(["NRAT0",round(   estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[0])]/normRegYieldHighHT,4) ])
    replacements.append(["NRAT1",round(   estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[1])]/normRegYieldHighHT,4) ])
    replacements.append(["NRAT2",round(   estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[2])]/normRegYieldHighHT,4) ])
    replacements.append(["SpNRATn",round( estimationModifier*sys['observed'][tuple(highHTBin)]['norm']*SpF[tuple(highHTBin)][(150,250)][(6,99)]['SF']['3po2']['rForData']/normRegYieldHighHT,4) ])
    replacements.append(["SpNRAT0",round( estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[0])]*SpF[tuple(highHTBin)][tuple(metbins[0])][(6,99)]['SF']['3po2']['rForData']/normRegYieldHighHT,4) ])
    replacements.append(["SpNRAT1",round( estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[1])]*SpF[tuple(highHTBin)][tuple(metbins[1])][(6,99)]['SF']['3po2']['rForData']/normRegYieldHighHT,4) ])
    replacements.append(["SpNRAT2",round( estimationModifier*sys['predicted'][tuple(highHTBin)][tuple(metbins[2])]*SpF[tuple(highHTBin)][tuple(metbins[2])][(6,99)]['SF']['3po2']['rForData']/normRegYieldHighHT,4) ])

    #lowHT normalization region systematics
    normRegYieldLowHT = round(sys['observed'][sig_and_bkgLowHTBin]['norm'] , 0)
    replacements.append(["LNREG",int(normRegYieldLowHT) ])
    replacements.append(["LSpNRATn",round(estimationModifier* sys['observed'][tuple(sig_and_bkgLowHTBin)]['norm']*SpF[tuple(lowHTBin)][tuple(lowHTmetbins[0])][(6,99)]['SF']['3po2']['rForData']/normRegYieldLowHT,4) ])
    if unifiedLowHT:
      replacements.append(["LSpNRAT0",round(estimationModifier* sys['predicted'][tuple(sig_and_bkgLowHTBin)][tuple(lowHTmetbins[1])]*SpF[tuple(lowHTBin)][tuple(lowHTmetbins[1])][(6,99)]['SF']['3po2']['rForData']/normRegYieldLowHT,5) ])
    else:
      replacements.append(["LSpNRAT0",round(estimationModifier* sys['predicted'][tuple(sig_and_bkgLowHTBin)][tuple(metbins[0])]*SpF[tuple(lowHTBin)][tuple(metbins[0])][(6,99)]['SF']['3po2']['rForData']/normRegYieldLowHT,5) ])
#    replacements.append(["LSpNRAT1",round( sys['predicted'][tuple(lowHTBin)][tuple(metbins[1])]*SpF[tuple(lowHTBin)][tuple(metbins[1])][(6,99)]['SF']['3po2']['rForData']/normRegYieldLowHT,5) ])
#    replacements.append(["LSpNRAT2",round( sys['predicted'][tuple(lowHTBin)][tuple(metbins[2])]*SpF[tuple(lowHTBin)][tuple(metbins[2])][(6,99)]['SF']['3po2']['rForData']/normRegYieldLowHT,5) ])
#
    #BTag and JES Systematics
    btag_SFb_2b_sigsys = {}
    btag_SFl_2b_sigsys = {}
    btag_SFb_3b_sigsys = {}
    btag_SFl_3b_sigsys = {}
    jes_2b_sigsys = {}
    jes_3b_sigsys = {}
    PU_sigsys={}
    MuEff1_sigsys={}
    MuEff2_sigsys={}
    EleEff_sigsys={}
    for metb in metbins+[(150,250)]:
      if doSigCont and (sms=="T1tttt" or sms=="T5tttt" or sms=="T1tttt-madgraph"):
        sigCont[tuple(metb)] = 0.01*gluino8TeV_NLONLL[varX]/gluino8TeV_NLONLL[sigContRefmgl[sms]]*sigCont_histo[tuple(metb)].GetBinContent(sigCont_histo[tuple(metb)].FindBin(varX, varY))
      if doSigCont and (sms=="T1t1t"):
#        print metb, varX, varY, sigCont_histo[tuple(metb)], sigCont_histo[tuple(metb)].FindBin(varX, varY), sigCont_histo[tuple(metb)].GetBinContent(sigCont_histo[tuple(metb)].FindBin(varX, varY))
        sigCont[tuple(metb)] = 0.01*sigCont_histo[tuple(metb)].GetBinContent(sigCont_histo[tuple(metb)].FindBin(varX, varY))

      h = PU_sigsyshisto[tuple(metb)]
      PU_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

      h = jes_2b_sigsyshisto[tuple(metb)]
      jes_2b_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))
      h = jes_3b_sigsyshisto[tuple(metb)]
      jes_3b_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

      h = btag_SFb_2b_sigsyshisto[tuple(metb)]
      btag_SFb_2b_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))
      h = btag_SFb_3b_sigsyshisto[tuple(metb)]
      btag_SFb_3b_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

      h = btag_SFl_2b_sigsyshisto[tuple(metb)]
      btag_SFl_2b_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))
      h = btag_SFl_3b_sigsyshisto[tuple(metb)]
      btag_SFl_3b_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

      h = MuEff1_sigsyshisto[tuple(metb)]
      MuEff1_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

      h = MuEff2_sigsyshisto[tuple(metb)]
      MuEff2_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

      h = EleEff_sigsyshisto[tuple(metb)]
      EleEff_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

    btaglowHT_SFb_3b_sigsys = {}
    btaglowHT_SFl_3b_sigsys = {}
    jeslowHT_3b_sigsys = {}
    PUlowHT_sigsys={}
    MuEff1lowHT_sigsys={}
    MuEff2lowHT_sigsys={}
    for metb in lowHTmetbins:
      if doSigCont and (sms=="T1tttt" or sms=="T5tttt" or sms=="T1tttt-madgraph"):
        sigContlowHT[tuple(metb)] = 0.01*gluino8TeV_NLONLL[varX]/gluino8TeV_NLONLL[sigContRefmgl[sms]]*sigContlowHT_histo[tuple(metb)].GetBinContent(sigContlowHT_histo[tuple(metb)].FindBin(varX, varY))
      if doSigCont and (sms=="T1t1t"):
        sigContlowHT[tuple(metb)] = 0.01*sigContlowHT_histo[tuple(metb)].GetBinContent(sigContlowHT_histo[tuple(metb)].FindBin(varX, varY))

      h = PUlowHT_sigsyshisto[tuple(metb)]
      PUlowHT_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

      h = jeslowHT_3b_sigsyshisto[tuple(metb)]
      jeslowHT_3b_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

      h = btaglowHT_SFb_3b_sigsyshisto[tuple(metb)]

      btaglowHT_SFb_3b_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))
      h = btaglowHT_SFl_3b_sigsyshisto[tuple(metb)]
      btaglowHT_SFl_3b_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

      h = MuEff1lowHT_sigsyshisto[tuple(metb)]
      MuEff1lowHT_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

      h = MuEff2lowHT_sigsyshisto[tuple(metb)]
      MuEff2lowHT_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

      h = EleEfflowHT_sigsyshisto[tuple(metb)]
      EleEfflowHT_sigsys[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))

    #ISR and PDF Uncertainty
    ISRSys = {}
    ISRSys_3b = {}
    ISRSys_3b_lowHT = {}
    PDFSys = {}
    PDFSys_3b = {}
    PDFSys_3b_lowHT = {}
    for metb in metbins:
      h = ISR_sys[tuple(metb)]
      ISRSys         [tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))
      h = PDF_sys[tuple(metb)]
      PDFSys         [tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))
    for metb in metbins+[(150,250)]:
      h = ISR_3b_sys[tuple(metb)]
      ISRSys_3b      [tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))
      h = PDF_3b_sys[tuple(metb)]
      PDFSys_3b      [tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))
    for metb in lowHTmetbins:
      h = ISR_3b_lowHT_sys[tuple(metb)]
      ISRSys_3b_lowHT[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY))
      h = PDF_3b_lowHT_sys[tuple(metb)]
      PDFSys_3b_lowHT[tuple(metb)] = h.GetBinContent(h.FindBin(varX, varY)) 

    #signal cont
    if doSigCont:
      replacements .append( [ "CONT0", round(sigCont[tuple(metbins[0])],4)])
      replacements .append( [ "CONT1", round(sigCont[tuple(metbins[1])],4)])
      replacements .append( [ "CONT2", round(sigCont[tuple(metbins[2])],4)])
      replacements .append( [ "CONT3", round(sigCont[(150,250)],4)])
      replacements .append( [ "CONT4", round(sigCont[tuple(metbins[0])],4)])
      replacements .append( [ "CONT5", round(sigCont[tuple(metbins[1])],4)])
      replacements .append( [ "CONT6", round(sigCont[tuple(metbins[2])],4)])
      replacements .append( [ "CONT7", round(sigContlowHT[tuple(lowHTmetbins[0])],4)])
      replacements .append( [ "CONT8", round(sigContlowHT[tuple(lowHTmetbins[1])],4)])
  #    replacements .append( [ "CONT8", round(sigContlowHT[tuple(metbins[0])],4)])
  #    replacements .append( [ "CONT9", round(sigContlowHT[tuple(metbins[1])],4)])
  #    replacements .append( [ "CONT10",round(sigContlowHT[tuple(metbins[2])],4)])
    else:
      replacements .append( [ "CONT0", 0.0]) 
      replacements .append( [ "CONT1", 0.0]) 
      replacements .append( [ "CONT2", 0.0]) 
      replacements .append( [ "CONT3", 0.0]) 
      replacements .append( [ "CONT4", 0.0]) 
      replacements .append( [ "CONT5", 0.0]) 
      replacements .append( [ "CONT6", 0.0]) 
      replacements .append( [ "CONT7", 0.0]) 
      replacements .append( [ "CONT8", 0.0]) 

    #SpF stat.
    replacements.append(["SpFstB3", round( 1.+SpF[tuple(htb)][(150,250)][(6,99)]['SF']['3po2']['sigmaForData'], 4)]) 
    replacements.append(["SpFstB4", round( 1.+SpF[tuple(htb)][tuple(metbins[0])][(6,99)]['SF']['3po2']['sigmaForData'], 4)]) 
    replacements.append(["SpFstB5", round( 1.+SpF[tuple(htb)][tuple(metbins[1])][(6,99)]['SF']['3po2']['sigmaForData'], 4)]) 
    replacements.append(["SpFstB6", round( 1.+SpF[tuple(htb)][tuple(metbins[2])][(6,99)]['SF']['3po2']['sigmaForData'], 4)]) 
    replacements.append(["SpFstB7", round( 1.+SpF[tuple(lowHTBin)][tuple(lowHTmetbins[0])][(6,99)]['SF']['3po2']['sigmaForData'], 4)]) 
    replacements.append(["SpFstB8", round( 1.+SpF[tuple(lowHTBin)][tuple(lowHTmetbins[1])][(6,99)]['SF']['3po2']['sigmaForData'], 4)]) 
#    replacements.append(["SpFstB8", round( 1.+SpF[tuple(lowHTBin)][tuple(metbins[0])][(6,99)]['SF']['3po2']['sigmaForData'], 4)]) 
#    replacements.append(["SpFstB9", round( 1.+SpF[tuple(lowHTBin)][tuple(metbins[1])][(6,99)]['SF']['3po2']['sigmaForData'], 4)]) 
#    replacements.append(["SpFstB10",round( 1.+SpF[tuple(lowHTBin)][tuple(metbins[2])][(6,99)]['SF']['3po2']['sigmaForData'], 4)]) 
#
    #SFb
    replacements.append(["SFbS0",round( 1.+btag_SFb_2b_sigsys[tuple(metbins[0])]   ,4) ]) #FIXME
    replacements.append(["SFbS1",round( 1.+btag_SFb_2b_sigsys[tuple(metbins[1])]   ,4) ])
    replacements.append(["SFbS2",round( 1.+btag_SFb_2b_sigsys[tuple(metbins[2])]   ,4) ])
    replacements.append(["HSFbSn",round( 1.+btag_SFb_3b_sigsys[(150,250)]   ,4) ])
    replacements.append(["HSFbS0",round( 1.+btag_SFb_3b_sigsys[tuple(metbins[0])]   ,4) ]) #FIXME
    replacements.append(["HSFbS1",round( 1.+btag_SFb_3b_sigsys[tuple(metbins[1])]   ,4) ])
    replacements.append(["HSFbS2",round( 1.+btag_SFb_3b_sigsys[tuple(metbins[2])]   ,4) ])
    replacements.append(["LSFbSn",round( 1.+btaglowHT_SFb_3b_sigsys[tuple(lowHTmetbins[0])]   ,4) ])
    replacements.append(["LSFbS0",round( 1.+btaglowHT_SFb_3b_sigsys[tuple(lowHTmetbins[1])]   ,4) ])
#    replacements.append(["LSFbS1",round( 1.+btaglowHT_SFb_3b_sigsys[tuple(metbins[1])]   ,4) ])
#    replacements.append(["LSFbS2",round( 1.+btaglowHT_SFb_3b_sigsys[tuple(metbins[2])]   ,4) ])
    replacements.append(["SFbB0",round( 1.+sys['systematics']['bSF'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["SFbB1",round( 1.+sys['systematics']['bSF'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["SFbB2",round( 1.+sys['systematics']['bSF'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    replacements.append(["SpFbn",round( 1.+ SpFSFb_sys[(150,250)]   ,4) ])
    replacements.append(["SpFSFbB0", round( (1.+ SpFSFb_sys[tuple(metbins[0])])*(1.+sys['systematics']['bSF'][tuple(htb)][tuple(metbins[0])])   ,4) ])
    replacements.append(["SpFSFbB1", round( (1.+ SpFSFb_sys[tuple(metbins[1])])*(1.+sys['systematics']['bSF'][tuple(htb)][tuple(metbins[1])])   ,4) ])
    replacements.append(["SpFSFbB2", round( (1.+ SpFSFb_sys[tuple(metbins[2])])*(1.+sys['systematics']['bSF'][tuple(htb)][tuple(metbins[2])])   ,4) ])
    replacements.append(["LSpFbn",    round(  1.+ SpFlowHTSFb_sys[tuple(lowHTmetbins[0])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LSpFSFbB0", round( (1.+ SpFlowHTSFb_sys[tuple(lowHTmetbins[1])])*(1.+sys['systematics']['bSF'][tuple(lowHTBin)][tuple(lowHTmetbins[1])])   ,4) ])
    else:
      replacements.append(["LSpFSFbB0", round( (1.+ SpFlowHTSFb_sys[tuple(lowHTmetbins[1])])*(1.+sys['systematics']['bSF'][tuple(lowHTBin)][tuple(metbins[0])])   ,4) ])
#    replacements.append(["LSpFSFbB1", round( (1.+ SpFlowHTSFb_sys[tuple(metbins[1])])*(1.+sys['systematics']['bSF'][tuple(lowHTBin)][tuple(metbins[1])])   ,4) ])
#    replacements.append(["LSpFSFbB2", round( (1.+ SpFlowHTSFb_sys[tuple(metbins[2])])*(1.+sys['systematics']['bSF'][tuple(lowHTBin)][tuple(metbins[2])])   ,4) ])

    #SFl
    replacements.append(["SFlS0",round( 1.+btag_SFl_2b_sigsys[tuple(metbins[0])]   ,4) ])  #FIXME!
    replacements.append(["SFlS1",round( 1.+btag_SFl_2b_sigsys[tuple(metbins[1])]   ,4) ])
    replacements.append(["SFlS2",round( 1.+btag_SFl_2b_sigsys[tuple(metbins[2])]   ,4) ])
    replacements.append(["HSFlSn",round( 1.+btag_SFl_3b_sigsys[(150,250)]   ,4) ])
    replacements.append(["HSFlS0",round( 1.+btag_SFl_3b_sigsys[tuple(metbins[0])]   ,4) ])  #FIXME!
    replacements.append(["HSFlS1",round( 1.+btag_SFl_3b_sigsys[tuple(metbins[1])]   ,4) ])
    replacements.append(["HSFlS2",round( 1.+btag_SFl_3b_sigsys[tuple(metbins[2])]   ,4) ])
    replacements.append(["LSFlSn",round( 1.+btaglowHT_SFl_3b_sigsys[tuple(lowHTmetbins[0])]   ,4) ])
    replacements.append(["LSFlS0",round( 1.+btaglowHT_SFl_3b_sigsys[tuple(lowHTmetbins[1])]   ,4) ])
#    replacements.append(["LSFlS1",round( 1.+btaglowHT_SFl_3b_sigsys[tuple(metbins[1])]   ,4) ])
#    replacements.append(["LSFlS2",round( 1.+btaglowHT_SFl_3b_sigsys[tuple(metbins[2])]   ,4) ])
    replacements.append(["SFlB0",round( 1.+sys['systematics']['lSF'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["SFlB1",round( 1.+sys['systematics']['lSF'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["SFlB2",round( 1.+sys['systematics']['lSF'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    replacements.append(["SpFln",round( 1.+ SpFSFl_sys[(150,250)]   ,4) ])
    replacements.append(["SpFSFlB0", round( (1.+ SpFSFl_sys[tuple(metbins[0])])*(1.+sys['systematics']['lSF'][tuple(htb)][tuple(metbins[0])])   ,4) ])
    replacements.append(["SpFSFlB1", round( (1.+ SpFSFl_sys[tuple(metbins[1])])*(1.+sys['systematics']['lSF'][tuple(htb)][tuple(metbins[1])])   ,4) ])
    replacements.append(["SpFSFlB2", round( (1.+ SpFSFl_sys[tuple(metbins[2])])*(1.+sys['systematics']['lSF'][tuple(htb)][tuple(metbins[2])])   ,4) ])
    replacements.append(["LSpFln",    round(  1.+ SpFlowHTSFl_sys[tuple(lowHTmetbins[0])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LSpFSFlB0", round( (1.+ SpFlowHTSFl_sys[tuple(lowHTmetbins[1])])*(1.+sys['systematics']['lSF'][tuple(lowHTBin)][tuple(lowHTmetbins[1])])   ,4) ])
    else:
      replacements.append(["LSpFSFlB0", round( (1.+ SpFlowHTSFl_sys[tuple(lowHTmetbins[1])])*(1.+sys['systematics']['lSF'][tuple(lowHTBin)][tuple(metbins[0])])   ,4) ])
#    replacements.append(["LSpFSFlB1", round( (1.+ SpFlowHTSFl_sys[tuple(metbins[1])])*(1.+sys['systematics']['lSF'][tuple(lowHTBin)][tuple(metbins[1])])   ,4) ])
#    replacements.append(["LSpFSFlB2", round( (1.+ SpFlowHTSFl_sys[tuple(metbins[2])])*(1.+sys['systematics']['lSF'][tuple(lowHTBin)][tuple(metbins[2])])   ,4) ])
    #PU
    replacements.append(["SPUn",round( 1.+ PU_sigsys[(150,250)] ,4) ])
    replacements.append(["SPU0",round( 1.+ PU_sigsys[tuple(metbins[0])] ,4) ])
    replacements.append(["SPU1",round( 1.+ PU_sigsys[tuple(metbins[1])] ,4) ])
    replacements.append(["SPU2",round( 1.+ PU_sigsys[tuple(metbins[2])] ,4) ])
    replacements.append(["LSPUn",round( 1.+ PUlowHT_sigsys[tuple(lowHTmetbins[0])] ,4) ])
    replacements.append(["LSPU0",round( 1.+ PUlowHT_sigsys[tuple(lowHTmetbins[1])] ,4) ])
#    replacements.append(["LSPU1",round( 1.+ PUlowHT_sigsys[tuple(metbins[1])] ,4) ])
#    replacements.append(["LSPU2",round( 1.+ PUlowHT_sigsys[tuple(metbins[2])] ,4) ])
    replacements.append(["PU0",round( 1.+sys['systematics']['Pileup'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["PU1",round( 1.+sys['systematics']['Pileup'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["PU2",round( 1.+sys['systematics']['Pileup'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LPU0",round( 1.+sys['systematics']['Pileup'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LPU0",round( 1.+sys['systematics']['Pileup'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LPU1",round( 1.+sys['systematics']['Pileup'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LPU2",round( 1.+sys['systematics']['Pileup'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
    #JES
    replacements.append(["JESS0",round( 1.+jes_2b_sigsys[tuple(metbins[0])]   ,4) ])
    replacements.append(["JESS1",round( 1.+jes_2b_sigsys[tuple(metbins[1])]   ,4) ])
    replacements.append(["JESS2",round( 1.+jes_2b_sigsys[tuple(metbins[2])]   ,4) ])
    replacements.append(["HJESSn",round( 1.+jes_3b_sigsys[(150,250)]   ,4) ])
    replacements.append(["HJESS0",round( 1.+jes_3b_sigsys[tuple(metbins[0])]   ,4) ])
    replacements.append(["HJESS1",round( 1.+jes_3b_sigsys[tuple(metbins[1])]   ,4) ])
    replacements.append(["HJESS2",round( 1.+jes_3b_sigsys[tuple(metbins[2])]   ,4) ])
    replacements.append(["LJESSn",round( 1.+jeslowHT_3b_sigsys[tuple(lowHTmetbins[0])]   ,4) ])
    replacements.append(["LJESS0",round( 1.+jeslowHT_3b_sigsys[tuple(lowHTmetbins[1])]   ,4) ])
#    replacements.append(["LJESS1",round( 1.+jeslowHT_3b_sigsys[tuple(metbins[1])]   ,4) ])
#    replacements.append(["LJESS2",round( 1.+jeslowHT_3b_sigsys[tuple(metbins[2])]   ,4) ])
    replacements.append(["JESB0",round( 1.+sys['systematics']['JES'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["JESB1",round( 1.+sys['systematics']['JES'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["JESB2",round( 1.+sys['systematics']['JES'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    replacements.append(["SpFJn",round( 1.+ SpFJES_sys[(150,250)]   ,4) ])
    replacements.append(["SpFJESB0", round( (1.+ SpFJES_sys[tuple(metbins[0])])*(1.+sys['systematics']['JES'][tuple(htb)][tuple(metbins[0])])   ,4) ])
    replacements.append(["SpFJESB1", round( (1.+ SpFJES_sys[tuple(metbins[1])])*(1.+sys['systematics']['JES'][tuple(htb)][tuple(metbins[1])])   ,4) ])
    replacements.append(["SpFJESB2", round( (1.+ SpFJES_sys[tuple(metbins[2])])*(1.+sys['systematics']['JES'][tuple(htb)][tuple(metbins[2])])   ,4) ])
    replacements.append(["LSpFJn",round( 1.+ SpFlowHTJES_sys[tuple(lowHTmetbins[0])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LSpFJESB0", round( (1.+ SpFlowHTJES_sys[tuple(lowHTmetbins[1])])*(1.+sys['systematics']['JES'][tuple(lowHTBin)][tuple(lowHTmetbins[1])])   ,4) ])
    else:
      replacements.append(["LSpFJESB0", round( (1.+ SpFlowHTJES_sys[tuple(lowHTmetbins[1])])*(1.+sys['systematics']['JES'][tuple(lowHTBin)][tuple(metbins[0])])   ,4) ])
#    replacements.append(["LSpFJESB1", round( (1.+ SpFlowHTJES_sys[tuple(metbins[1])])*(1.+sys['systematics']['JES'][tuple(lowHTBin)][tuple(metbins[1])])   ,4) ])
#    replacements.append(["LSpFJESB2", round( (1.+ SpFlowHTJES_sys[tuple(metbins[2])])*(1.+sys['systematics']['JES'][tuple(lowHTBin)][tuple(metbins[2])])   ,4) ])

#    if not modifyDeltaBetaAndClosure:
    #Closure
    replacements.append(["CLOS0",round( 1.+sys['systematics']['Closure'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["CLOS1",round( 1.+sys['systematics']['Closure'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["CLOS2",round( 1.+sys['systematics']['Closure'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LCLOS0",round( 1.+sys['systematics']['Closure'][tuple(lowHTBin)][tuple(lowHTmetbins[1])],4) ])
    else:
      replacements.append(["LCLOS0",round( 1.+sys['systematics']['Closure'][tuple(lowHTBin)][tuple(metbins[0])],4) ])
#    #model beta
    replacements.append(["BETA0",round( 1.+sys['systematics']['MET model'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["BETA1",round( 1.+sys['systematics']['MET model'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["BETA2",round( 1.+sys['systematics']['MET model'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LBETA0",round( 1.+sys['systematics']['MET model'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LBETA0",round( 1.+sys['systematics']['MET model'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    else:
#      print "CLOSURE and MODEL Uncertainty added linearly!!!" #FIXME
#      #Closure
#      replacements.append(["CLOS0",round( 1. -  abs(sys['systematics']['Closure'][tuple(htb)][tuple(metbins[0])])          -abs(sys['systematics']['MET model'][tuple(htb)][tuple(metbins[0])]           )  ,4) ])
#      replacements.append(["CLOS1",round( 1. -  abs(sys['systematics']['Closure'][tuple(htb)][tuple(metbins[1])])          -abs(sys['systematics']['MET model'][tuple(htb)][tuple(metbins[1])]           )  ,4) ])
#      replacements.append(["CLOS2",round( 1. -  abs(sys['systematics']['Closure'][tuple(htb)][tuple(metbins[2])])          -abs(sys['systematics']['MET model'][tuple(htb)][tuple(metbins[2])]           )  ,4) ])
#      replacements.append(["LCLOS0",round( 1.- abs(sys['systematics']['Closure'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]) -abs(sys['systematics']['MET model'][tuple(lowHTBin)][tuple(lowHTmetbins[1])] )  ,4) ])
#  #    #model beta
#      replacements.append(["BETA0",round( 1.    ,4) ])
#      replacements.append(["BETA1",round( 1.    ,4) ])
#      replacements.append(["BETA2",round( 1.    ,4) ])
#      replacements.append(["LBETA0",round( 1.  ,4) ])

#    #TT x-sec
    replacements.append(["TTX0",round( 1.+sys['systematics']['TT cross section'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["TTX1",round( 1.+sys['systematics']['TT cross section'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["TTX2",round( 1.+sys['systematics']['TT cross section'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LTTX0",round( 1.+sys['systematics']['TT cross section'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LTTX0",round( 1.+sys['systematics']['TT cross section'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LTTX1",round( 1.+sys['systematics']['TT cross section'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LTTX2",round( 1.+sys['systematics']['TT cross section'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#
#    #TT Polarization
    replacements.append(["TTP0",round( 1.+sys['systematics']['TT polarization'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["TTP1",round( 1.+sys['systematics']['TT polarization'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["TTP2",round( 1.+sys['systematics']['TT polarization'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LTTP0",round( 1.+sys['systematics']['TT polarization'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LTTP0",round( 1.+sys['systematics']['TT polarization'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LTTP1",round( 1.+sys['systematics']['TT polarization'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LTTP2",round( 1.+sys['systematics']['TT polarization'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#    #W x-sec
    replacements.append(["WX0",round( 1.+sys['systematics']['W+jets cross section'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["WX1",round( 1.+sys['systematics']['W+jets cross section'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["WX2",round( 1.+sys['systematics']['W+jets cross section'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LWX0",round( 1.+sys['systematics']['W+jets cross section'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LWX0",round( 1.+sys['systematics']['W+jets cross section'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LWX1",round( 1.+sys['systematics']['W+jets cross section'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LWX2",round( 1.+sys['systematics']['W+jets cross section'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#    #Wbb x-sec
    replacements.append(["WBBX0",round( 1.+sys['systematics']['Wbb cross section'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["WBBX1",round( 1.+sys['systematics']['Wbb cross section'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["WBBX2",round( 1.+sys['systematics']['Wbb cross section'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LWBBX0",round( 1.+sys['systematics']['Wbb cross section'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LWBBX0",round( 1.+sys['systematics']['Wbb cross section'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LWBBX1",round( 1.+sys['systematics']['Wbb cross section'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LWBBX2",round( 1.+sys['systematics']['Wbb cross section'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#    #DiLep
    replacements.append(["DLEP0",round( 1.+sys['systematics']['DiLep'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["DLEP1",round( 1.+sys['systematics']['DiLep'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["DLEP2",round( 1.+sys['systematics']['DiLep'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LDLEP0",round( 1.+sys['systematics']['DiLep'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LDLEP0",round( 1.+sys['systematics']['DiLep'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LDLEP1",round( 1.+sys['systematics']['DiLep'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LDLEP2",round( 1.+sys['systematics']['DiLep'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#    #tau contr.
    replacements.append(["TAU0",round( 1.+sys['systematics']['Tau'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["TAU1",round( 1.+sys['systematics']['Tau'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["TAU2",round( 1.+sys['systematics']['Tau'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LTAU0",round( 1.+sys['systematics']['Tau'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LTAU0",round( 1.+sys['systematics']['Tau'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LTAU1",round( 1.+sys['systematics']['Tau'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LTAU2",round( 1.+sys['systematics']['Tau'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#    #non-leading x-sec
    replacements.append(["NONL0",round( 1.+sys['systematics']['non-leading cross section'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["NONL1",round( 1.+sys['systematics']['non-leading cross section'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["NONL2",round( 1.+sys['systematics']['non-leading cross section'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LNONL0",round( 1.+sys['systematics']['non-leading cross section'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LNONL0",round( 1.+sys['systematics']['non-leading cross section'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LNONL1",round( 1.+sys['systematics']['non-leading cross section'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LNONL2",round( 1.+sys['systematics']['non-leading cross section'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#
#    #Erf Data/MC
    replacements.append(["ERDM0",round( 1.+sys['systematics']['Erf data/MC'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["ERDM1",round( 1.+sys['systematics']['Erf data/MC'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["ERDM2",round( 1.+sys['systematics']['Erf data/MC'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    
    if unifiedLowHT:
      replacements.append(["LERDM0",round( 1.+sys['systematics']['Erf data/MC'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LERDM0",round( 1.+sys['systematics']['Erf data/MC'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LERDM1",round( 1.+sys['systematics']['Erf data/MC'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LERDM2",round( 1.+sys['systematics']['Erf data/MC'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#
#    #Erf NonLinear 1
    replacements.append(["ERF10",round( 1.+sys['systematics']['Erf nonlinearity ev0'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["ERF11",round( 1.+sys['systematics']['Erf nonlinearity ev0'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["ERF12",round( 1.+sys['systematics']['Erf nonlinearity ev0'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LERF10",round( 1.+sys['systematics']['Erf nonlinearity ev0'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LERF10",round( 1.+sys['systematics']['Erf nonlinearity ev0'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LERF11",round( 1.+sys['systematics']['Erf nonlinearity ev0'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LERF12",round( 1.+sys['systematics']['Erf nonlinearity ev0'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#
#    #Erf NonLinear 2
    replacements.append(["ERF20",round( 1.+sys['systematics']['Erf nonlinearity ev1'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["ERF21",round( 1.+sys['systematics']['Erf nonlinearity ev1'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["ERF22",round( 1.+sys['systematics']['Erf nonlinearity ev1'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LERF20",round( 1.+sys['systematics']['Erf nonlinearity ev1'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LERF20",round( 1.+sys['systematics']['Erf nonlinearity ev1'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LERF21",round( 1.+sys['systematics']['Erf nonlinearity ev1'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LERF22",round( 1.+sys['systematics']['Erf nonlinearity ev1'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#
#    #Mu Eff 1
    replacements.append(["SMEF1n",round( 1.+ MuEff1_sigsys[(150,250)] ,4) ])
    replacements.append(["SMEF10",round( 1.+ MuEff1_sigsys[tuple(metbins[0])] ,4) ])
    replacements.append(["SMEF11",round( 1.+ MuEff1_sigsys[tuple(metbins[1])] ,4) ])
    replacements.append(["SMEF12",round( 1.+ MuEff1_sigsys[tuple(metbins[2])] ,4) ])
    replacements.append(["LSMEF1n",round( 1.+ MuEff1lowHT_sigsys[tuple(lowHTmetbins[0])] ,4) ])
    replacements.append(["LSMEF10",round( 1.+ MuEff1lowHT_sigsys[tuple(lowHTmetbins[1])] ,4) ])
#    replacements.append(["LSMEF11",round( 1.+ MuEff1lowHT_sigsys[tuple(metbins[1])] ,4) ])
#    replacements.append(["LSMEF12",round( 1.+ MuEff1lowHT_sigsys[tuple(metbins[2])] ,4) ])
    replacements.append(["BMEF10",round( 1.+sys['systematics']['MuEff1'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["BMEF11",round( 1.+sys['systematics']['MuEff1'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["BMEF12",round( 1.+sys['systematics']['MuEff1'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LBMEF10",round( 1.+sys['systematics']['MuEff1'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LBMEF10",round( 1.+sys['systematics']['MuEff1'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LBMEF11",round( 1.+sys['systematics']['MuEff1'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LBMEF12",round( 1.+sys['systematics']['MuEff1'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#
#    #Mu Eff 2
    replacements.append(["SMEF2n",round( 1.+ MuEff2_sigsys[(150,250)] ,4) ])
    replacements.append(["SMEF20",round( 1.+ MuEff2_sigsys[tuple(metbins[0])] ,4) ])
    replacements.append(["SMEF21",round( 1.+ MuEff2_sigsys[tuple(metbins[1])] ,4) ])
    replacements.append(["SMEF22",round( 1.+ MuEff2_sigsys[tuple(metbins[2])] ,4) ])
    replacements.append(["LSMEF2n",round( 1.+ MuEff2lowHT_sigsys[tuple(lowHTmetbins[0])] ,4) ])
    replacements.append(["LSMEF20",round( 1.+ MuEff2lowHT_sigsys[tuple(lowHTmetbins[1])] ,4) ])
#    replacements.append(["LSMEF21",round( 1.+ MuEff2lowHT_sigsys[tuple(metbins[1])] ,4) ])
#    replacements.append(["LSMEF22",round( 1.+ MuEff2lowHT_sigsys[tuple(metbins[2])] ,4) ])
    replacements.append(["BMEF20",round( 1.+sys['systematics']['MuEff2'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["BMEF21",round( 1.+sys['systematics']['MuEff2'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["BMEF22",round( 1.+sys['systematics']['MuEff2'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LBMEF20",round( 1.+sys['systematics']['MuEff2'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LBMEF20",round( 1.+sys['systematics']['MuEff2'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LBMEF21",round( 1.+sys['systematics']['MuEff2'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LBMEF22",round( 1.+sys['systematics']['MuEff2'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#
#    #Ele Eff 2
    replacements.append(["SEEFFn",round( 1.+ EleEff_sigsys[(150,250)] ,4) ])
    replacements.append(["SEEFF0",round( 1.+ EleEff_sigsys[tuple(metbins[0])] ,4) ])
    replacements.append(["SEEFF1",round( 1.+ EleEff_sigsys[tuple(metbins[1])] ,4) ])
    replacements.append(["SEEFF2",round( 1.+ EleEff_sigsys[tuple(metbins[2])] ,4) ])
    replacements.append(["LSEEFFn",round( 1.+ EleEfflowHT_sigsys[tuple(lowHTmetbins[0])] ,4) ])
    replacements.append(["LSEEFF0",round( 1.+ EleEfflowHT_sigsys[tuple(lowHTmetbins[1])] ,4) ])
#    replacements.append(["LSEEFF1",round( 1.+ EleEfflowHT_sigsys[tuple(metbins[1])] ,4) ])
#    replacements.append(["LSEEFF2",round( 1.+ EleEfflowHT_sigsys[tuple(metbins[2])] ,4) ])
    replacements.append(["BEEFF0",round( 1.+sys['systematics']['EleEff'][tuple(htb)][tuple(metbins[0])]   ,4) ])
    replacements.append(["BEEFF1",round( 1.+sys['systematics']['EleEff'][tuple(htb)][tuple(metbins[1])]   ,4) ])
    replacements.append(["BEEFF2",round( 1.+sys['systematics']['EleEff'][tuple(htb)][tuple(metbins[2])]   ,4) ])
    if unifiedLowHT:
      replacements.append(["LBEEFF0",round( 1.+sys['systematics']['EleEff'][tuple(lowHTBin)][tuple(lowHTmetbins[1])]   ,4) ])
    else:
      replacements.append(["LBEEFF0",round( 1.+sys['systematics']['EleEff'][tuple(lowHTBin)][tuple(metbins[0])]   ,4) ])
#    replacements.append(["LBEEFF1",round( 1.+sys['systematics']['EleEff'][tuple(lowHTBin)][tuple(metbins[1])]   ,4) ])
#    replacements.append(["LBEEFF2",round( 1.+sys['systematics']['EleEff'][tuple(lowHTBin)][tuple(metbins[2])]   ,4) ])
#
#    #c-Frac
    replacements.append(["SpFCn",round( 1.+ SpFcFrac_sys[(150,250)] ,4) ])
    replacements.append(["SpFC0",round( 1.+ SpFcFrac_sys[tuple(metbins[0])] ,4) ])
    replacements.append(["SpFC1",round( 1.+ SpFcFrac_sys[tuple(metbins[1])] ,4) ])
    replacements.append(["SpFC2",round( 1.+ SpFcFrac_sys[tuple(metbins[2])] ,4) ])
    replacements.append(["LSpFCn",round( 1.+ SpFlowHTcFrac_sys[tuple(lowHTmetbins[0])] ,4) ])
    replacements.append(["LSpFC0",round( 1.+ SpFlowHTcFrac_sys[tuple(lowHTmetbins[1])] ,4) ])
#    replacements.append(["LSpFC1",round( 1.+ SpFlowHTcFrac_sys[tuple(metbins[1])] ,4) ])
#    replacements.append(["LSpFC2",round( 1.+ SpFlowHTcFrac_sys[tuple(metbins[2])] ,4) ])
#
#    #gluSplit
    replacements.append(["SpFgn",round( 1.+ SpFgluSplit_sys[(150,250)] ,4) ])
    replacements.append(["SpFg0",round( 1.+ SpFgluSplit_sys[tuple(metbins[0])] ,4) ])
    replacements.append(["SpFg1",round( 1.+ SpFgluSplit_sys[tuple(metbins[1])] ,4) ])
    replacements.append(["SpFg2",round( 1.+ SpFgluSplit_sys[tuple(metbins[2])] ,4) ])
    replacements.append(["LSpFgn",round( 1.+ SpFlowHTgluSplit_sys[tuple(lowHTmetbins[0])] ,4) ])
    replacements.append(["LSpFg0",round( 1.+ SpFlowHTgluSplit_sys[tuple(lowHTmetbins[1])] ,4) ])
#    replacements.append(["LSpFg1",round( 1.+ SpFlowHTgluSplit_sys[tuple(metbins[1])] ,4) ])
#    replacements.append(["LSpFg2",round( 1.+ SpFlowHTgluSplit_sys[tuple(metbins[2])] ,4) ])
#
#    #SpF nonclosure
    replacements.append(["SpFNn",round( 1.+ SpFSysDataMC[tuple(htb)][(150,250)] ,4) ])
    replacements.append(["SpFN0",round( 1.+ SpFSysDataMC[tuple(htb)][tuple(metbins[0])] ,4) ])
    replacements.append(["SpFN1",round( 1.+ SpFSysDataMC[tuple(htb)][tuple(metbins[1])] ,4) ])
    replacements.append(["SpFN2",round( 1.+ SpFSysDataMC[tuple(htb)][tuple(metbins[2])] ,4) ])
    replacements.append(["LSpFNn",round( 1.+ SpFSysDataMC[tuple(lowHTBin)][tuple(lowHTmetbins[0])] ,4) ])
    replacements.append(["LSpFN0",round( 1.+ SpFSysDataMC[tuple(lowHTBin)][tuple(lowHTmetbins[1])] ,4) ])
#    replacements.append(["LSpFN1",round( 1.+ SpFSysDataMC[tuple(lowHTBin)][tuple(metbins[1])] ,4) ])
#    replacements.append(["LSpFN2",round( 1.+ SpFSysDataMC[tuple(lowHTBin)][tuple(metbins[2])] ,4) ])
    #ISR
    replacements.append(["SISR0", round( 1.+ ISRSys         [tuple(metbins[0])] ,4) ])
    replacements.append(["SISR1", round( 1.+ ISRSys         [tuple(metbins[1])] ,4) ])
    replacements.append(["SISR2", round( 1.+ ISRSys         [tuple(metbins[2])] ,4) ])
    replacements.append(["HSISRn",round( 1.+ ISRSys_3b      [(150,250)] ,4) ])
    replacements.append(["HSISR0",round( 1.+ ISRSys_3b      [tuple(metbins[0])] ,4) ])
    replacements.append(["HSISR1",round( 1.+ ISRSys_3b      [tuple(metbins[1])] ,4) ])
    replacements.append(["HSISR2",round( 1.+ ISRSys_3b      [tuple(metbins[2])] ,4) ])
    replacements.append(["LSISRn",round( 1.+ ISRSys_3b_lowHT[tuple(lowHTmetbins[0])] ,4) ])
    replacements.append(["LSISR0",round( 1.+ ISRSys_3b_lowHT[tuple(lowHTmetbins[1])] ,4) ])
    #PDF
    replacements.append(["SPDF0", round( 1.+ PDFSys         [tuple(metbins[0])] ,4) ])
    replacements.append(["SPDF1", round( 1.+ PDFSys         [tuple(metbins[1])] ,4) ])
    replacements.append(["SPDF2", round( 1.+ PDFSys         [tuple(metbins[2])] ,4) ])
    replacements.append(["HSPDFn",round( 1.+ PDFSys_3b      [(150,250)] ,4) ])
    replacements.append(["HSPDF0",round( 1.+ PDFSys_3b      [tuple(metbins[0])] ,4) ])
    replacements.append(["HSPDF1",round( 1.+ PDFSys_3b      [tuple(metbins[1])] ,4) ])
    replacements.append(["HSPDF2",round( 1.+ PDFSys_3b      [tuple(metbins[2])] ,4) ])
    replacements.append(["LSPDFn",round( 1.+ PDFSys_3b_lowHT[tuple(lowHTmetbins[0])] ,4) ])
    replacements.append(["LSPDF0",round( 1.+ PDFSys_3b_lowHT[tuple(lowHTmetbins[1])] ,4) ])

    ofile = "modelFiles_"+dirname+'/model_'+str(varX)+"_"+str(varY)+'.txt'
    outfile = file(ofile,'w')
    while 1:
      line = infile.readline()
      if not line:break
      if len(line.lstrip())==0 or line.lstrip()[0]=='#':continue
      if line.count("#"):
        line = line.split("#")[0]+' \n'
      for r in replacements:
        s1 = ' '+('{0: >'+str(prec)+'}').format(r[1])+' '
        s0= ' '+''.join([" " for i in range(max(0, prec - len(r[0])))])+r[0]+' '
        pr = False
        if len(s0)!=len(s1):pr=True
        if len(s1)<len(s0):
          n=-len(s1)+len(s0)
          sadd = ''.join([" " for i in range(n)])
          s1 = sadd+s1
        line = line.replace(s0,s1) 
      print line[:-1]
      outfile.write(line)
    outfile.close()
    allJobs.append([varX, varY])
    allFiles.append(ofile)
    infile.close()

if not writeModelFiles:  #If they weren't written we load them
  print "Loading ",'modelFiles_'+dirname+'/'
  allFiles_ = os.listdir('modelFiles_'+dirname+'/')
  allFiles=[]
  allJobs=[]
  for f in allFiles_:
    if f[-4:]==".txt" and f[:6]=="model_":
      s = f.replace(".txt","").split("_")[1:3]
      job = [int(s[0]), int(s[1])]
      if doOnlyOneJob!=[]:
        if not job==doOnlyOneJob:continue
      allFiles.append('modelFiles_'+dirname+'/'+f)
      allJobs.append(job)
  print "Loaded ",len(allFiles),"files"

if writeGridDirectories:
  for i, ofile in enumerate(allFiles):
    print "Converting",i+1,'/',len(allFiles),ofile
    os.system('text2workspace.py '+ofile+' -o '+ofile.replace('txt','root'))
  print "Creating tar archives"
  os.system('cd modelFiles_'+dirname+';tar cvzf ../modelsText.tar *.txt')
  os.system('cd modelFiles_'+dirname+';tar cvzf ../models.tar *.root')

  import datetime
  now = datetime.datetime.now()
  dateStr = str(now.year)[2:]+(str(now.month).zfill(2))+(str(now.day).zfill(2))
  tDir = str(htb[0])+'_'+str(htb[1])
  #Write Grid directories
  dir_counter=0
  job_counter=0
  lisfile = file('m0m12.lis', 'w')
  for i, [varX, varY] in enumerate(allJobs):
  #  print i, varX, varY
    lisfile.write(str(varX)+' '+str(varY)+'\n')
    job_counter+=1
    if (i>0 and (i+1)%500==0) or i+1==len(allJobs):
      print "i",i,'jobs_counter',job_counter
      lisfile.close()
      crab_dirname = 'crab_'+dirname+"_"+tDir+"_part"+str(dir_counter)+'/'
      os.system('mkdir -p '+crab_dirname)
      os.system('cp m0m12.lis modelsText.tar models.tar '+crab_dirname)
      os.system('cp asymptotic.awk combine_HybridNew.cfg combine_HybridNew.sh combine '+crab_dirname)
      os.system('sed -i "s/NJOBS/'+str(job_counter)+'/" '+crab_dirname+'/combine_HybridNew.cfg')
      os.system('sed -i "s/SMS/'+sms+'/" '+crab_dirname+'/combine_HybridNew.cfg')
      os.system('sed -i "s/DATE/'+dateStr+'/" '+crab_dirname+'/combine_HybridNew.cfg')
      os.system('sed -i "s/COUNTER/'+str(dir_counter)+'/" '+crab_dirname+'/combine_HybridNew.cfg')
      os.system('cd '+crab_dirname+'; mv combine_HybridNew.cfg crab.cfg')
      lisfile = file('m0m12.lis', 'w')
      dir_counter+=1
      job_counter=0
  lisfile.close()
    

if calcAsymptotic:
  os.system('mkdir -p resultsAsymptotic_'+dirname)
  for i, [varX, varY] in enumerate(allJobs):
    print "Running asymptotic",sms,varX, varY
    opt = ""
    if (sms == "T1tttt" or sms=="T1tttt-madgraph") and varX<=950 and varY<=400: 
      opt = "--rMax 1.0"
    combCommand = 'cd modelFiles_'+dirname+'; combine -M Asymptotic model_'+str(varX)+'_'+str(varY)+'.txt'+" "+opt
    cpCommand = 'cp higgsCombineTest.Asymptotic.mH120.root ../resultsAsymptotic_'+dirname+'/higgsCombine_Asymptotic_'+str(varX)+'_'+str(varY)+'.root'
    os.system(combCommand+';'+cpCommand)

