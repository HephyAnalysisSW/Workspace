from Workspace.DegenerateStopAnalysis.cardFileWriter import cardFileWriter
from Workspace.DegenerateStopAnalysis.navidTools.FOM import get_float

import pickle

import glob
from os.path import basename, splitext

import ROOT






#pickleFiles = ["/afs/hephy.at/user/n/nrad/CMSSW/CMSSW_7_4_7/src/Workspace/DegenerateStopAnalysis/plotsNavid/analysis/pkl/SR1_r1_a.pkl"]


def getLimit(yld, sig=None , outDir ="./cards/", postfix = "", sys_uncorr=1.2, sys_corr = 1.06):
    c = cardFileWriter()
    c.defWidth=40
    c.maxUncNameWidth=40
    c.maxUncStrWidth=40
    c.precision=6
    c.addUncertainty("Sys", 'lnN')

    
    bins = yld.cutLegend[0][1:]
    bkgs = yld.bkgList
      
    if not sig:
        sig  = yld.sigList[0]
    elif sig in yld.sigList:
        pass
    else:
        assert False, "Signal %s not in the yield dictionary signal list:%s" %(sig, yld.sigList)
        
        

    processNames = { bkg:yld.yieldDict[bkg][0] for bkg in bkgs}
    #processNames.update(  { sig:yld.yieldDict[sig][0] } )
    #processNames.update(  { sig:'signal'} )
    processNames.update(  { 'signal':'signal'} )

 

    for iBin, bin in enumerate(bins,1):
        c.addBin(bin,[processNames[bkg] for bkg in bkgs],bin)
        c.specifyObservation(bin,int( get_float(yld.yieldDict["Total"][iBin]) ))
        sysName = "Sys_%s"%(bin)
        c.addUncertainty(sysName, 'lnN')
        c.addUncertainty(sysName+"_sig", 'lnN')
        for bkg in bkgs:
          c.specifyExpectation(bin,processNames[bkg],get_float(yld.yieldDict[bkg][iBin]))
          c.specifyUncertainty('Sys',bin,processNames[bkg],sys_corr)
          #sysName = "Sys_%s"%bkg
          c.specifyUncertainty(sysName,bin,processNames[bkg],sys_uncorr)
        c.specifyExpectation(bin,"signal",get_float(yld.yieldDict[sig][iBin]))
        c.specifyUncertainty(sysName+"_sig",bin,'signal',sys_uncorr)
        #c.specifyUncertainty('Sys',bin,"signal",sys_corr)
    badBins=[]
    #if True:
    #  return c
    print "--------debug-------------"
    print c.bins
    print c.processes
    print c.expectation
    print "--------debug-------------"


    for bin in c.bins:
        expectations = [c.expectation[( bin, process )] for process in c.processes[bin]] 
        bkgExpectations = [ c.expectation[(bin,processNames[process])] for process in bkgs]
        print bin, any(expectations), c.processes[bin], expectations
        if not any(expectations):
          print "############ no processes contributing to the bin %s, to make life easier the bin will be removed from card but make sure everything is ok"%bin
          print bin, c.processes[bin], expectations   
          badBins.append(bin)
          #print c.bins
        if not any(bkgExpectations):
          print "############ no background contributing to the bin %s, a small non zero value (0.001) has been assigned to the bin"%bin
          c.expectation[(bin,process[bkgs[0]])]=0.001
          print bin, c.processes[bin], expectations   
          
    for bin in badBins:
        c.bins.remove(bin)
    
    sigName  =  yld.yieldDict[sig][0]
    filename =  sigName + "_" + yld.tableName
    if postfix:
        if not postfix.startswith("_"):
            postfix = "_" + postfix
        filename += postfix

    
    cardName='%s.txt'%filename
    c.writeToFile('%s/%s'%(outDir,cardName))
    print "Card Written To: %s/%s"%(outDir,cardName)
    #limits=c.calcLimit("./output/%s"%cardName)
    limits=c.calcLimit()
    #print cardName,   "median:  ", limits['0.500']
    return (c, limits)






def _getLimit_delme(yld, sig=None ,  sys_uncorr=1.2, sys_corr = 1.06):
    c = cardFileWriter()
    c.defWidth=40
    c.maxUncNameWidth=40
    c.maxUncStrWidth=40
    c.precision=6
    c.addUncertainty("Sys", 'lnN')

    filename= yld.tableName
    
    bins = yld.cutLegend[0][1:]
    bkgs = yld.bkgList
      
    if not sig:
        sig  = yld.sigList[0]
    elif sig in yld.sigList:
        pass
    else:
        assert False, "Signal %s not in the yield dictionary signal list:%s" %(sig, yld.sigList)
        
        

    processNames = { bkg:yld.yieldDict[bkg][0] for bkg in bkgs}
    #processNames.update(  { sig:yld.yieldDict[sig][0] } )
    #processNames.update(  { sig:'signal'} )
    processNames.update(  { 'signal':'signal'} )

 

    for iBin, bin in enumerate(bins,1):
        c.addBin(bin,[processNames[bkg] for bkg in bkgs],bin)
        c.specifyObservation(bin,int( get_float(yld.yieldDict["Total"][iBin]) ))
        sysName = "Sys_%s"%(bin)
        c.addUncertainty(sysName, 'lnN')
        c.addUncertainty(sysName+"_sig", 'lnN')
        for bkg in bkgs:
          c.specifyExpectation(bin,processNames[bkg],get_float(yld.yieldDict[bkg][iBin]))
          c.specifyUncertainty('Sys',bin,processNames[bkg],sys_corr)
          #sysName = "Sys_%s"%bkg
          c.specifyUncertainty(sysName,bin,processNames[bkg],sys_uncorr)
        c.specifyExpectation(bin,"signal",get_float(yld.yieldDict[sig][iBin]))
        c.specifyUncertainty(sysName+"_sig",bin,'signal',sys_uncorr)
        #c.specifyUncertainty('Sys',bin,"signal",sys_corr)
    badBins=[]
    #if True:
    #  return c
    print "--------debug-------------"
    print c.bins
    print c.processes
    print c.expectation
    print "--------debug-------------"


    for bin in c.bins:
        expectations = [c.expectation[( bin, process )] for process in c.processes[bin]] 
        bkgExpectations = [ c.expectation[(bin,processNames[process])] for process in bkgs]
        print bin, any(expectations), c.processes[bin], expectations
        if not any(expectations):
          print "############ no processes contributing to the bin %s, to make life easier the bin will be removed from card but make sure everything is ok"%bin
          print bin, c.processes[bin], expectations   
          badBins.append(bin)
          #print c.bins
        if not any(bkgExpectations):
          print "############ no background contributing to the bin %s, a small non zero value (0.001) has been assigned to the bin"%bin
          c.expectation[(bin,process[bkgs[0]])]=0.001
          print bin, c.processes[bin], expectations   
          
    for bin in badBins:
        c.bins.remove(bin)
    
    cardName='%s.txt'%filename
    c.writeToFile('./cards/%s'%cardName)
    limits=c.calcLimit("./output/%s"%cardName)
    #print cardName,   "median:  ", limits['0.500']
    return (c, limits)









def try_int(s):
    "Convert to integer if possible."
    try: return int(s)
    except: return s

def natsort_key(s):
    "Used internally to get a tuple by which s is sorted."
    import re
    return map(try_int, re.findall(r'(\d+|\D+)', s))
 

def plotLimits(limitDict):
  nLimits = len(limitDict)
  limitPlot = ROOT.TH1F("limitPlot","limitPlot",nLimits,0,nLimits)
  for i,fname in enumerate(sorted(limitDict, key=natsort_key),1):
    limit=limitDict[fname][1]['0.500']
    limitPlot.GetXaxis().SetBinLabel(i,fname)
    limitPlot.SetBinContent(i,limit)

  limitPlot.GetYaxis().SetTitle("r")
  limitPlot.SetTitle("Median Expected Limits")
  return limitPlot





import subprocess

#def calcLimitFromCard(card="./cards/T2DegStop_300_270_cards.txt"): 
def calcLimitFromCard(card="./cards/T2DegStop_300_270_cards.txt", name="", mass=""):
    command = ['combine', '--saveWorkspace', '-M', 'Asymptotic'] 
    if name:
        command.extend(["--name", name])
    if mass:
        command.extend(["--mass, mass"])
    command.append(card)
    out = subprocess.Popen(command, stdout = subprocess.PIPE)
    start = False
    end   = False
    limit = {}
    ret = []
    for line in out.stdout.readlines():
        if "-- Asymptotic --" in line:
            start = True
            continue
        if not start:
            continue
        if line == "\n":
            break
        #print line
        for v in [":","%", "\n", "r <"]:
            line = line.replace(v,"")
        ret.append(line)
        limit_sig, limit_val = line.rsplit()[1:]
        if "limit" in limit_sig.lower(): # this should be the observed limit
            limit_sig = "-1"
        else:
            limit_sig = "%0.3f"%(float ( limit_sig ) / 100.)
        
        limit[limit_sig]=limit_val
    return limit









#if __name__==False:
if False:

  bkgs=["TTJets", "WJets"]
  sig="T2Deg300_270"
  saveDir     =  "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/dmt_regions/"
  pickleDir   =  "/afs/hephy.at/user/n/nrad/CMSSW/CMSSW_7_4_7/src/Workspace/DegenerateStopAnalysis/plotsNavid/analysis/cutbased/pkl/dmt_regions/r1/"
  pickleFiles = glob.glob(pickleDir+"/*.pkl")

  if len(pickleFiles)==0:
    print "############   WARNING    no pickle files found!  #####"
  else:
    print "############ %s ickle files ound: "%len(pickleFiles),
    print pickleFiles

  limitDict={}
  yields={}

  yieldInstPickleFiles = [x for x in pickleFiles if "YieldInstance" in x]
  for pickleFile in yieldInstPickleFiles:
    filename = splitext(basename(pickleFile))[0].replace("YieldInstance_","")
    print "############ making a limit card for %s"%filename
    yields[filename]=pickle.load(open(pickleFile,"rb") )
    bins = yields[filename].cutLegend[0][1:]
    limitDict[filename] = getLimit(yields[filename])

  import ROOT

  nLimits = len(limitDict)
  limitPlot = ROOT.TH1F("limitPlot","limitPlot",nLimits,0,nLimits)
  for i,fname in enumerate(sorted(limitDict),1):
    limit=limitDict[fname][1]['0.500']
    limitPlot.GetXaxis().SetBinLabel(i,fname)
    limitPlot.SetBinContent(i,limit)

  limitPlot.GetYaxis().SetTitle("r")
  limitPlot.SetTitle("Median Expected Limits")
  limitPlot.Draw()
  #ROOT.c1.SaveAs("/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/dmt_regions/ExpectedLimits.png")
  ROOT.c1.SaveAs(saveDir+"/ExpectedLimits.png")
    















