from analysisHelpers import *
import os, sys, cPickle
from math import sqrt

def findSyst (name, var, allSysts):
  for syst in allSysts:
    if syst[0]==name and syst[1]==var:  return syst
  return None

metArgs = [ ]
if len(sys.argv)>1:
  metArgStrings = sys.argv[1].split(",")
  metArgInts = [ ]
  for metArgString in metArgStrings:
    metArgInts.append(int(metArgString))
  metArgInts.append(2500)
  for imet in range(len(metArgInts)-1):
    assert metArgInts[imet]<metArgInts[imet+1]
    metArgs.append( (metArgInts[imet],metArgInts[imet+1]) )

sys.argv.append("-b")

convDirBase = "/data/schoef/convertedTuples_v16"
minNJet = 6

btBin = '2'
#htBins = [ (400,750), (400,2500), (750,2500), (1000,2500) ]
#htBins = [ (750,2500) ]
#htBins = [ (400,750) ]
metNormBin = ( 150, 250 )
#metBins = [ (250,350), (350,450), (450,2500) ]
#htBins = [ (750,2500) ]
#metBins = [ (450,2500) ]
refVar = 'central'

regions = {
  (400,750) : [ (250,2500) ],
  (400,2500) : [ (250,350), (350,450), (450,2500) ],
  (750,2500) : [ (250,350), (350,450), (450,2500) ],
  (1000,2500) : [ (250,350), (350,450), (450,2500) ]
  }
htBins = sorted(regions.keys())
if len(metArgs)>0:
  for ht in htBins:
    if len(regions[ht])>1:
      regions[ht] = metArgs

systList = {
  "JES" : { "name" : "JES", "vars" : [ "Ref", "+", "-" ] },
  "DiLep" : { "name" : "DiLep", "vars" : [ "Ref", "+", "-" ] },
  "bSF" : { "name" : "BTag", "vars" : [ "Ref", "SF_b_Up", "SF_b_Down" ] },
  "lSF" : { "name" : "BTag", "vars" : [ "Ref", "SF_light_Up", "SF_light_Down" ] },
  "MET model" : { "name" : "model beta+/-0.047", "vars" : [ "Ref", "+", "-" ] },
  "Pileup" : { "name" : "PU", "vars" : [ "Ref", "+", "-" ] },
  "Tau" : { "name" : "Tau", "vars" : [ "Ref", "+", "-" ] },
  "TT polarization" : { "name" : "TTPol", "vars" : [ "Ref", "+", "-" ] },
  "TT cross section" : { "name" : "TT xsec", "vars" : [ "Ref", "+", "-" ] },
  "Wbb cross section" : { "name" : "W+bb", "vars" : [ "Ref", "+", "+" ] },
  "W+jets cross section" : { "name" : "W xsec", "vars" : [ "Ref", "+", "-" ] },
  "non-leading cross section" : { "name" : "Non leading xsec", "vars" : [ "Ref", "+", "-" ] },
  "MuEff1" : { "name" : "Mu Eff 1", "vars" : [ "Ref", "+", "+" ] },
  "MuEff2" : { "name" : "Mu Eff 2", "vars" : [ "Ref", "+", "+" ] },
  "EleEff" : { "name" : "Ele Eff", "vars" : [ "Ref", "+", "+" ] },
  "Erf nonlinearity ev0" : { "name" : "erf non lin 0", "vars" : [ "Ref", "+", "-" ] },
  "Erf nonlinearity ev1" : { "name" : "erf non lin 1", "vars" : [ "Ref", "+", "-" ] },
  "Erf data/MC" : { "name" : "erf data/mc 4j diff", "vars" : [ "Ref", "+", "+" ] },  
  "Closure" : { "name" : "closure", "vars" : [ "MC standard" ] }
  }
systNames = [
  "lSF", 
  "bSF", 
  "DiLep", 
  "JES", 
  "Tau", 
  "MuEff1", 
  "MuEff2", 
  "EleEff", 
  "TT polarization", 
  "TT cross section", 
  "Wbb cross section", 
  "W+jets cross section", 
  "non-leading cross section", 
  "Pileup", 
  "MET model", 
  "Erf nonlinearity ev0", 
  "Erf nonlinearity ev1", 
  "Erf data/MC", 
  "Closure", 
  ]
systCombinations = {
  "\cPqb-quark jet identification" : [ "bSF", "lSF" ],
  "Lepton efficiencies" : [ "MuEff1", "MuEff2", "EleEff" ],
  "JES" : [ "JES" ],
  "Non-leading bkg cross sections" : [ "DiLep", "Tau", "Wbb cross section", "W+jets cross section", "non-leading cross section" ],
  "Error function parameters" : [ "Erf nonlinearity ev0", "Erf nonlinearity ev1", "Erf data/MC" ]
  }
systDoubleRatioOnly = [
#  "W+jets cross section"
  ]

countList = {
  "MC" : { "name" : "closure", "var" : "MC using btag weights" },
  "data" : { "name" : "closure", "var" : "Daten" }
  }
nomSystVarNames = [ 'Ref', '+', '-' ]

# cross checks
for syst in systNames:
  assert syst in systList
for groupName,group in systCombinations.iteritems():
  for syst in group:
    assert syst in systList
for syst in systDoubleRatioOnly:
  assert syst in systList

from systCsvList import allSysts

def getTrueYield (baseDir, htb, metb, btb):
  fitSummaryFile = baseDir+"/result_"+btb+".pkl"
  if os.path.exists(fitSummaryFile):
    htbs = [ htb ]
  else:
    htbs = getHtList(htb)
#    print "*** using ht list for getTrueYield ",baseDir,htb,metb,btb
  sumYieldLow = 0.
  sumYieldHigh = 0.
  sumYieldErr2 = 0.
  for htbb in htbs:
    fitSummaryFile = baseDir.replace("err_sampling_"+str(htb[0])+"_ht_"+str(htb[1]),
                                     "err_sampling_"+str(htbb[0])+"_ht_"+str(htbb[1]))
    fitSummaryFile += "/result_"+btb+".pkl"
    fitResultSummary = cPickle.load(file(fitSummaryFile))
    if not metb[0] in fitResultSummary:  return [ None, None ]
    trueYieldLow = fitResultSummary[metb[0]]['observ']
    trueYieldLowErr2 = fitResultSummary[metb[0]]['observ_error']
    if metb[1] != 2500:
      if not metb[1] in fitResultSummary: return [ None, None ]
      trueYieldHigh = fitResultSummary[metb[1]]['observ']
      trueYieldHighErr2 = fitResultSummary[metb[1]]['observ_error']
    else:
      trueYieldHigh = 0.
      trueYieldHighErr2 = 0.
    sumYieldLow += trueYieldLow
    sumYieldHigh += trueYieldHigh
    sumYieldErr2 += (trueYieldLowErr2-trueYieldHighErr2)
#  print 'True yields / errors = ',str(htb),str(metb),btb,(sumYieldLow-sumYieldHigh),sqrt(sumYieldErr2)
  return [ ( sumYieldLow - sumYieldHigh ), sqrt(sumYieldErr2) ]

result = { }

#
# counts & predictions
#
outDict = { }
outDict["observed"] = { }
outDict["predicted"] = { }
outDict["predFromPkl"] = { }
outDict["predBins"] = { }
outDict["predErr"] = { }
outDict["predCov"] = { }
outDict["predMean"] = { }
systData = findSyst(countList["data"]["name"],countList["data"]["var"],allSysts)
dataConvDir = convDirBase+"/"+systData[4]
#print "dataConvDir ",dataConvDir
if not os.path.exists(dataConvDir):
  print "Did not find directory ",dataConvDir
  sys.exit(1)
dataChain = getRefChain(dir=dataConvDir,mode="data")
for htb in htBins:
  outDict["observed"][htb] = { }
  outDict["predicted"][htb] = { }
  outDict["predFromPkl"][htb] = { }
  outDict["predBins"][htb] = { }
  outDict["predErr"][htb] = [ ]
  outDict["predCov"][htb] = { }
  outDict["predMean"][htb] = { }
  fitBaseDir = systData[6]
  if not fitBaseDir.endswith("/"):  fitBaseDir += "/"
  fitDir = fitBaseDir + "err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])
  outDict["observed"][htb]["norm"] = getNormRegYield(fitDir,btBin,htb=list(htb))[0]
  for metb in regions[htb]:
    outDict["observed"][htb][metb] = getRefYield(btb=btBin, htb=list(htb), metb=list(metb), metvar='type1phiMet', minNJet = minNJet, chain = dataChain, weight = "1")
  metbs = [ ]
  for metb in regions[htb]:
    metbs.append(list(metb))
  print "fitBasedir = ",fitBaseDir,btBin,htb,metbs
  predictions =  getSampledMetYieldPrediction(fitBaseDir, btBin, htb=list(htb), metb=metbs, n=999999)# ['results'][metb][refVar]
  outDict["predBins"][htb] = metbs
  predCov = predictions['covMatrix']
  outDict["predCov"][htb] = predCov
  for imetb,metb in enumerate(metbs):
    outDict["predErr"][htb].append(sqrt(predCov[imetb][imetb]))
  resultsDictWK = { }
  resultsFile = fitDir+"/result_2.pkl"
  if os.path.exists(resultsFile):
    resultsDictWK = cPickle.load(file(resultsFile))
  else:
    print "did not find result file for ",resultsFile
  for metb in regions[htb]:
    outDict["predicted"][htb][metb] = predictions['results'][metb][refVar]
    outDict["predMean"][htb][metb] = predictions['results'][metb]["samplingMean"]
    if float(metb[0]) in resultsDictWK and ( float(metb[1]) in resultsDictWK or metb[1] == 2500 ):
      outDict["predFromPkl"][htb][metb] = resultsDictWK[float(metb[0])]['pred']
      if metb[1] != 2500:
        outDict["predFromPkl"][htb][metb] -= resultsDictWK[float(metb[1])]['pred']
    else:
      print "*** no prediction from results file for",htb,metb
#
# systematics
#
for htb in htBins:
  result[htb] = { }
  for systFullName in systList:
    if not "name" in systList[systFullName]: continue
    if not "vars" in systList[systFullName]: continue
    systName = systList[systFullName]["name"]
    systVars = systList[systFullName]["vars"]
#    print syst
#    print systName
    resPredYield = { }
    for metb in regions[htb]:
      if not metb in result[htb]:  result[htb][metb] = { }
      result[htb][metb][systFullName] = { }
      if len(systVars)==len(nomSystVarNames):
        for i,nomVarName in enumerate(nomSystVarNames):
          var = systVars[i]
#          print systName,var
          systCSV = findSyst(systName,var,allSysts)
          assert systCSV!=None
          fitBaseDir = systCSV[6]
          if not fitBaseDir.endswith("/"):  fitBaseDir += "/"
          fitDir = fitBaseDir + "err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])
          resPredYield[nomVarName] = getSampledMetYieldPrediction(fitBaseDir, btBin, htb=list(htb), metb=list(metb), n=999999)
          convDir = convDirBase+"/"+systCSV[4]
          if not os.path.exists(convDir):
            print "Did not find directory ",convDir
            sys.exit(1)
#          print "convDir = ",convDir
          chain = getRefChain(dir=convDir,mode="mc")
          wgt = systCSV[2]
          trueYieldAll = getTrueYield(fitDir,htb,metb,btBin)
          trueYield = trueYieldAll[0]
          if trueYield == None:
            trueYield = getRefYield(btb=btBin, htb=list(htb), metb=list(metb), metvar='type1phiMet', minNJet = minNJet, chain = chain, weight = wgt)
#          rYieldWgt = getRefYield(btb=btBin, htb=list(htb), metb=list(metb), metvar='type1phiMet', minNJet = minNJet, chain = chain, weight = wgt)
#          rYieldOne = getRefYield(btb=btBin, htb=list(htb), metb=list(metb), metvar='type1phiMet', minNJet = minNJet, chain = chain, weight = "1")
#          print "true yield ",nomVarName,metb,wgt,trueYieldAll,rYieldWgt,rYieldOne
          if i==0:
            resRef = resPredYield[nomVarName]["results"][metb][refVar]
            trueRef = trueYield
            print htb,metb,systName,nomVarName,wgt,trueRef,resRef
          else:
            resVar = resPredYield[nomVarName]["results"][metb][refVar]
            trueVar = trueYield
            prefix = ""
            if trueRef>1.e-6 and abs(trueVar/trueRef-1.)<0.00001:  prefix = "*** "
            print prefix,htb,metb,systName,nomVarName,wgt,trueVar,resVar
            sRes = resVar/resRef - 1.
            dRes = (resVar/trueVar)/(resRef/trueRef) - 1. if trueRef>1.e-6 else sRes
            # treat single-variation case
            if i==2 and ( var == systVars[1] ):
              print "Revert sign"
              sRes *= -1
              dRes *= -1
            result[htb][metb][systFullName][nomVarName] = ( sRes, dRes )
      elif systFullName=="Closure":
        systCSV = findSyst(systName,systVars[0],allSysts)
        closureBaseDir = systCSV[6]
        if not closureBaseDir.endswith("/"):  closureBaseDir += "/"
        closureDir = closureBaseDir + "err_sampling_"+str(htb[0])+"_ht_"+str(htb[1])
        closureYield =  getSampledMetYieldPrediction(closureBaseDir, btBin, htb=list(htb), metb=list(metb), n=999999)['results'][metb][refVar]
        convDir = convDirBase+"/"+systCSV[4]
        if not os.path.exists(convDir):
          print "Did not find directory ",convDir
          sys.exit(1)
#        chain = getRefChain(dir=convDir,mode="mc")
#        wgt = systCSV[2]
        trueYield = getTrueYield (closureDir,htb,metb,btBin)[0]
        if trueYield == None:
          print "Using true yield from getRefYield"
          trueYield = getRefYield(btb=btBin, htb=list(htb), metb=list(metb), metvar='type1phiMet', minNJet = minNJet, chain = chain, weight = wgt)
#        fitSummaryFile = closureDir+"/result_"+btBin+".pkl"
#        if os.path.exists(fitSummaryFile):
#          htbs = [ htb ]
#        else:
#          htbs = getHtList(htb)
#        sumYieldLow = 0.
#        sumYieldHigh = 0.
#        for htbb in htbs:
#          fitSummaryFile = closureDir.replace("err_sampling_"+str(htb[0])+"_ht_"+str(htb[1]),"err_sampling_"+str(htbb[0])+"_ht_"+str(htbb[1]))
#          fitSummaryFile += "/result_"+btBin+".pkl"
#          fitResultSummary = cPickle.load(file(fitSummaryFile))
#          trueYieldLow = fitResultSummary[metb[0]]['observ']
#          trueYieldHigh = fitResultSummary[metb[1]]['observ'] if ( metb[1] != 2500 )  else 0.
#          sumYieldLow += trueYieldLow
#          sumYieldHigh += trueYieldHigh
#        trueYield = sumYieldLow - sumYieldHigh
        print "Closure ",htb,metb,trueYield,closureYield
        result[htb][metb]["Closure"] = { }
        sRes = trueYield/closureYield - 1 # if trueYield>1.e-6 else float('nan')
        result[htb][metb]["Closure"][nomSystVarNames[1]] = ( sRes, sRes )
        result[htb][metb]["Closure"][nomSystVarNames[2]] = ( -sRes, -sRes )

    
#      break
#    break
#  break
      
#    vars = allSysts[systName][syst
#    print vars
#    resht =
#print " "
#print result
#
# add average and best values to dictionary
#
for systFullName in systNames:
  assert systFullName in systList
  systName = systList[systFullName]["name"] if "name" in systList[systFullName] else systFullName
  for htb in htBins:
    for metb in regions[htb]:
      sRatio = (result[htb][metb][systFullName]['+'][0]-result[htb][metb][systFullName]['-'][0])/2.
      dRatio = (result[htb][metb][systFullName]['+'][1]-result[htb][metb][systFullName]['-'][1])/2.
      result[htb][metb][systFullName]['singleRatio'] = sRatio
      result[htb][metb][systFullName]['doubleRatio'] = dRatio
      result[htb][metb][systFullName]['minRatio'] = dRatio
      if abs(sRatio)<abs(dRatio) and not ( systFullName in systDoubleRatioOnly ):
        result[htb][metb][systFullName]['minRatio'] = sRatio
        result[htb][metb][systFullName]['minRatioIsSingle'] = True
      sMean = (result[htb][metb][systFullName]['+'][0]+result[htb][metb][systFullName]['-'][0])/2.
      dMean = (result[htb][metb][systFullName]['+'][1]+result[htb][metb][systFullName]['-'][1])/2.
      result[htb][metb][systFullName]['singleMean'] = sMean
      result[htb][metb][systFullName]['doubleMean'] = dMean

outDict["systematics"] = { }
for systFullName in systList:
  systName = systList[systFullName]["name"] if "name" in systList[systFullName] else systFullName
  curDict = outDict["systematics"]
  if not systFullName in curDict:  curDict[systFullName] = { }
  for htb in htBins:
    curDict = outDict["systematics"][systFullName]
    if not htb in curDict:  curDict[htb] = { }
    for metb in regions[htb]:
      curDict = outDict["systematics"][systFullName][htb]
      curDict[metb] = result[htb][metb][systFullName]['minRatio']
#print outDict
outName = "systTable"
if len(metArgs)>0:
  outName += "_"
  outName += sys.argv[1].replace(",","-")
outDir = outName
if not os.path.isdir(outDir):
  os.mkdir(outDir)
outDir += "/"
outName = outDir+"systTable.pkl"
outFile = open(outName,"wb")
cPickle.dump(outDict,outFile)
outFile.close()

print " "
print "*** Average relative systematic error"
lenLabel = 30
lenMet = 20
for htb in htBins:
  print " "
  print "**  "+str(htb[0])+" < HT < "+str(htb[1])
  line = lenLabel*" "
  for metb in regions[htb]:
    label = str(metb[0])+"<MET<"+str(metb[1])
    fmt = '{0:^'+str(lenMet)+'}'
    line += fmt.format(label)
  print line
#  for systFullName in systList:  
  for systFullName in systNames:
    assert systFullName in systList
    fmt = '{0:'+str(lenLabel)+'}'
    line = fmt.format(systFullName)
    hasLine2 = False
    line2 = fmt.format("  (double ratio)")
    for metb in regions[htb]:
#      print result[htb][metb].keys()
      sRatio = result[htb][metb][systFullName]['singleRatio']
      dRatio = result[htb][metb][systFullName]['doubleRatio']
      fmt = '{0:'+str(lenMet-5)+'.1%}'
      if abs(sRatio)<abs(dRatio) and not ( systFullName in systDoubleRatioOnly ):
        line += fmt.format(sRatio)+5*" "
        line2 += fmt.format(dRatio)+5*" "
#        line += fmt.format(result[htb][metb][systFullName]['singleMean'])+5*" "
#        line2 += fmt.format(result[htb][metb][systFullName]['doubleMean'])+5*" "
        hasLine2 = True
      else:
        line += fmt.format(dRatio)+5*" "
#        line += fmt.format(dMean)+5*" "
        line2 += lenMet*" "
    print line
    if hasLine2:  print line2
      
for htb in htBins:
  texFile = open(outDir+"systTable-"+str(htb[0])+"_"+str(htb[1])+".tex","w")
  texFile.write(" "+"\n")
  texFile.write("\\begin{table}"+"\n")
  texFile.write("\\begin{center}"+"\n")
  texFile.write("\\caption{"+"\n")
  texFile.write("Systematic uncertainties for the background estimation in the signal regions defined for $"+str(htb[0])+" < \\HT < "+str(htb[1])+"\\GeV$."+"\n")
  texFile.write("}\\label{tab:BkgSyst_"+str(htb[0])+"}"+"\n")
  line = "\\begin{tabular}{c|"
  for metb in regions[htb]:  line += "|c"
  line += "}"
  texFile.write(line+"\n")
  line = " "
  for metb in regions[htb]:
    line += "& $"+str(metb[0])+" < \\ETmiss <"+str(metb[1])+" \\GeV$"
  line += " \\\\ \\hline"
  texFile.write(line+"\n")
  for systFullName in systNames:
    assert systFullName in systList
    line = systFullName
    for metb in regions[htb]:
#      print result[htb][metb].keys()
      sRatio = result[htb][metb][systFullName]['singleRatio']
      dRatio = result[htb][metb][systFullName]['doubleRatio']
      fmt = '{0:'+str(lenMet-5)+'.1%}'
      if abs(sRatio)<abs(dRatio) and not ( systFullName in systDoubleRatioOnly ):
        line += " & "+fmt.format(sRatio) #+" ("+fmt.format(dRatio)+")"
      else:
        line += " & "+fmt.format(dRatio)
    line += " \\\\"
    texFile.write(line.replace("%","\%")+"\n")
  texFile.write("\\end{tabular}"+"\n")
  texFile.write("\\end{center}"+"\n")
  texFile.write("\\end{table}"+"\n")
  texFile.close()


import ROOT
sys.argv.append('-b')

for groupName,group in systCombinations.iteritems():
  print "*** Group of systematics: "+str(group)
  for htb in htBins:
    print "**  "+str(htb[0])+" < HT < "+str(htb[1])
    m = ROOT.TMatrix(len(regions[htb]),len(group))
    for imet,metb in enumerate(regions[htb]):
      for isyst,syst in enumerate(group):
#        print imet,isyst
        m[imet][isyst] = result[htb][metb][syst]['minRatio']
#    for imet1,metb1 in enumerate(regions[htb]):
#      line = ""
#      for imet2,metb2 in enumerate(regions[htb]):
#        line += " " + str(m(imet1,imet2))
#      print line
    mt = ROOT.TMatrix(len(group),len(regions[htb]))
    mt.Transpose(m)
    cov = m*mt



    line = groupName
    for imet1,metb1 in enumerate(regions[htb]):
      line += " & "
      fmt = '{0:'+str(lenMet-5)+'.1%}'
      line += fmt.format(sqrt(cov(imet1,imet1)))+5*" "
    line += " \\\\"
    print line



    line = lenLabel*' '
    print " regions = ",regions[htb]
    for imet1,metb1 in enumerate(regions[htb]):
      label = str(metb1[0])+"<MET<"+str(metb1[1])
      fmt = '{0:^'+str(lenMet)+'}'
      line += fmt.format(label)
    print line
    for imet1,metb1 in enumerate(regions[htb]):
      label = str(metb1[0])+"<MET<"+str(metb1[1])
      fmt = '{0:^'+str(lenLabel)+'}'
      line = fmt.format(label)
      fmt1 = '{0:'+str(lenMet-5)+'.1%}'
      fmt2 = '{0:'+str(lenMet-5)+'.3f}'
      for imet2,metb2 in enumerate(regions[htb]):
        if imet2==imet1:
          line += fmt1.format(sqrt(cov(imet1,imet2)))+5*" "
        elif imet2<imet1:
          line += fmt2.format(cov(imet1,imet2)/sqrt(cov(imet1,imet1)*cov(imet2,imet2)))+5*" "
        else:
          line += (lenMet-5)*" "
      print line

