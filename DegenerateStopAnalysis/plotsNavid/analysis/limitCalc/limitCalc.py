from cardFileWriter import cardFileWriter
import pickle

import glob
from os.path import basename, splitext


bkgs=["TTJets", "WJets"]
sig="T2Deg300_270"
sys_uncorr=1.20
sys_corr  =1.06




saveDir     = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/limits" 
pickleDir   =  "/afs/hephy.at/user/n/nrad/CMSSW/CMSSW_7_4_7/src/Workspace/DegenerateStopAnalysis/plotsNavid/analysis/cutbased/pkl/"
pickleFiles = glob.glob(pickleDir+"/*.pkl")


#pickleFiles = ["/afs/hephy.at/user/n/nrad/CMSSW/CMSSW_7_4_7/src/Workspace/DegenerateStopAnalysis/plotsNavid/analysis/pkl/SR1_r1_a.pkl"]


def getLimit(yld):
  c = cardFileWriter()
  c.defWidth=25
  c.maxUncNameWidth=45
  c.precision=6
  c.addUncertainty("Sys", 'lnN')

  filename= yld.tableName
  
  bins = yld.cutLegend[0][1:]
  bkgs = yld.bkgList
  sig  = yld.sigList[0]


  for iBin, bin in enumerate(bins,1):
    c.addBin(bin,bkgs,bin)
    c.specifyObservation(bin,int( float(yld.yieldDict["Total"][iBin]) ))
    sysName = "Sys_%s"%(bin)
    c.addUncertainty(sysName, 'lnN')
    c.addUncertainty(sysName+"_sig", 'lnN')
    for bkg in bkgs:
      c.specifyExpectation(bin,bkg,float(yld.yieldDict[bkg][iBin]))
      c.specifyUncertainty('Sys',bin,bkg,sys_corr)
      #sysName = "Sys_%s"%bkg
      c.specifyUncertainty(sysName,bin,bkg,sys_uncorr)
    c.specifyExpectation(bin,"signal",float(yld.yieldDict[sig][iBin]))
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
    expectations = [c.expectation[(bin,process)] for process in c.processes[bin]] 
    bkgExpectations = [c.expectation[(bin,process)] for process in bkgs]
    print bin, any(expectations), c.processes[bin], expectations
    if not any(expectations):
      print "############ no processes contributing to the bin %s, to make life easier the bin will be removed from card but make sure everything is ok"%bin
      print bin, c.processes[bin], expectations   
      badBins.append(bin)
      #print c.bins
    if not any(bkgExpectations):
      print "############ no background contributing to the bin %s, a small non zero value (0.001) has been assigned to the bin"%bin
      c.expectation[(bin,bkgs[0])]=0.001
      print bin, c.processes[bin], expectations   
      
  for bin in badBins:
    c.bins.remove(bin)
  
  cardName='%s.txt'%filename
  c.writeToFile('./cards/%s'%cardName)
  limits=c.calcLimit("./output/%s"%cardName)
  #print cardName,   "median:  ", limits['0.500']
  return (c, limits)






if len(pickleFiles)==0:
  print "############   WARNING    no pickle files found!  #####"
else:
  print "############ %s pickle files ound: "%len(pickleFiles),
  print pickleFiles

limitDict={}
yields={}

yieldInstPickleFiles = [x for x in pickleFiles if "YieldInstance" in x]
for pickleFile in yieldInstPickleFiles:
  filename = splitext(basename(pickleFile))[0].replace("YieldInstance_","")
  print "############ making a limit card for %s"%filename
  yields[filename]=pickle.load(open(pickleFile,"rb") )

  bins = yields[filename].cutLegend[0][1:]
    
 


  #yieldDict=pickle.load(open(pickleFile ,"rb"))
  #bins=[bin for bin in sorted(yieldDict['bkg'].keys()) if "Err" not in bin]
  #limitDict[filename] = getLimit(yieldDict,bins,sig,bkgs,filename)

import ROOT

#nLimits = len(limitDict)
#limitPlot = ROOT.TH1F("limitPlot","limitPlot",nLimits,0,nLimits)
#for i,fname in enumerate(sorted(limitDict),1):
#  limit=limitDict[fname]['0.500']
#  limitPlot.GetXaxis().SetBinLabel(i,fname)
#  limitPlot.SetBinContent(i,limit)
#
#limitPlot.GetYaxis().SetTitle("r")
#limitPlot.SetTitle("Median Expected Limits")
#limitPlot.Draw()
#ROOT.c1.SaveAs("/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/dmt/ExpectedLimits.png")
  

