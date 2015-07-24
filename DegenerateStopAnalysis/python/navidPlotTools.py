import ROOT
import os
import math




from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks

def saveCanvas(canv,name,plotDir="./",format=".gif"):
  canv.SaveAs(plotDir+"/"+name+format)

def decorate(hist,color='',width='',histTitle='',fillColor=''):
  if color: hist.SetLineColor(color)
  if width: hist.SetLineWidth(width)
  if histTitle: hist.SetTitle(histTitle)
  if fillColor: hist.SetFillColor(fillColor)
  return

def decorateAxis(hist,xAxisTitle='x title',yAxisTitle='y title',title=''):
  axis = hist.GetXaxis()
  axis.SetTitle(xAxisTitle)
#  axis.SetTitleOffSet(1)
  axis = hist.GetYaxis()
  axis.SetTitle(yAxisTitle)
#  axis.SetTitleOffSet(1)
#  axis.SetTitleFont(62) 
  if title:  hist.SetTitle(title)
  return 


def addToLeg(legend,hist,RMS=1,Mean=1,RMSError=0,MeanError=0,pName=''):
  if RMS:
    rmsString='  RMS={RMS:.2f}'.format(RMS=hist.GetRMS())
    if RMSError: rmsString += ' #pm {0:.2f}'.format(hist.GetRMSError())
  else: rmsString=''
  if Mean:
    meanString='  Mean={MEAN:.2f}'.format(MEAN=hist.GetMean())
    if MeanError: meanString += ' #pm {0:.2f}'.format(hist.GetMeanError())
  else: meanString=''
  if pName: nameString=pName

  else: nameString=hist.GetName()
  legString= nameString + rmsString + meanString
  legend.AddEntry(hist,legString)
  return legend



def getChainFromChunks( samples, treeName):
  c = ROOT.TChain("tree")
  if type(samples)!=type([]):
    sampleList=[0]
    sampleList[0]=samples
  else:
    sampleList=samples
  nTot=0
  for sample in sampleList:
    fList, niTot = getChunks(sample,treeName)
    for f in fList:
      c.Add(f['file'])
    #print fList
    nTot += niTot
    print c.GetEntries(), nTot, niTot
  return c, nTot 

def getChainFromDir( dir, treeName='tree'):
  c=ROOT.TChain(treeName)
  c.Add(dir+"/*.root")
  return c

def joinCutStrings(cutStringList):
  return "(" + " && ".join([ "("+c +")" for c in cutStringList])    +")"

def makeCutFlowList(cutList):
  cutFlowList=[]
  for cutName,cutString in cutList:
    cutFlowString = joinCutStrings( [cutList[i][1] for i in range(0, 1+cutList.index( [cutName,cutString]))] )
    cutFlowList.append( [cutName, cutFlowString ])
  return cutFlowList


getAllAlph = lambda str: ''.join(ch for ch in str if ch not in "Kl13@$%[]{}();'\"")

def getGoodPlotFromChain(c, var, binning,varName='', cutString='(1)', weight='weight', color='', lineWidth='',fillColor='',  binningIsExplicit=False, addOverFlowBin=''): 
  ret=  getPlotFromChain(c, var, binning, cutString=cutString, weight=weight, binningIsExplicit=binningIsExplicit, addOverFlowBin=addOverFlowBin) 
  if not varName:
    varName=getAllAlph(var)
    print varName
  ret.SetTitle(varName)
  ret.SetName(varName)
  if color:
    #ret.SetLineColor(color)
    ret.SetLineColor(color)
  if lineWidth:
    ret.SetLineWidth(lineWidth)
  if fillColor:
    ret.SetFillColor(fillColor)
    ret.SetLineColor(ROOT.kBlack)
  return ret

def getStackFromHists(histList):
  stk=ROOT.THStack()
  for h in histList:
    stk.Add(h)
  return stk

def matchListToDictKeys(List,Dict):
  if not List:
    List=Dict.keys()
  else:
    if type(List)==type([]) or  type(List)==type(()):
      pass
    else:
      List=List.rsplit()
    for l in List:
      if l not in Dict.keys():
        print "WARNING: Item \' %s \' will be ignored because it is not found in the dictionary keys:"%(l) , Dict.keys()
        List.pop(List.index(l))
  return List

def getPlots(sampleDict,plotDict,treeList='',varList='',cut=''):
  """Use: getPlots(sampleDict,plotDict,treeList='',varList='',cut=''):"""
  treeList  = matchListToDictKeys(treeList,sampleDict)
  varList   = matchListToDictKeys(varList,plotDict)
  print treeList
  print varList
  for s in treeList:
    if sampleDict[s].has_key("weight") and sampleDict[s]["weight"]:
      weight = str(sampleDict[s]["weight"])
      print "For sample %s, using weight in sampleDict, weight= %s"%(s,weight) 
    else: weight="weight"
    if not sampleDict[s].has_key('plots'):
      sampleDict[s]['plots']={}
    for p in varList:
      lineWidth=plotDict[p]['lineWidth']
      if plotDict[p]['color'] == type("") and plotDict[p]['color'].lower()=="fill" and not sampleDict[s]['isSignal']:
        #color = ROOT.kBlack
        color = sampleDict[s]['color']
        fcolor = sampleDict[s]['color']
      else:
        color  = sampleDict[s]['color']
        fcolor = 0 
        if sampleDict[s]['isSignal']:
          lineWidth=2
      if cut:
        cutString=cut
      else:
        cutString="(%s) && (%s)"%(plotDict[p]['presel'],plotDict[p]['cut'])
      print "Sample:" , s , "Getting Plot: ", p, "with cut:  " , cutString
      sampleDict[s]['plots'][p] = getGoodPlotFromChain(sampleDict[s]['tree'] , plotDict[p]['var'], plotDict[p]['bin'],\
                                                       varName     = p  ,
                                                       cutString   = cutString, 
                                                       color       = color,
                                                       fillColor   = fcolor,
                                                       lineWidth   = lineWidth,
                                                       weight      = weight
                                                       #weight      = str(sampleDict[s]['weight'])
                                                       )
  return

def getBkgSigStacks(sampleDict, plotDict, varList='',treeList=''):
  """Get stacks for signal and backgrounds. make vars in varlist are available in sampleDict. no stacks for 2d histograms.   """
  treeList  = matchListToDictKeys(treeList,sampleDict)
  varList   = matchListToDictKeys(varList,plotDict)
  #treeList=sampleDict.keys()
  #varList=plotDict.keys()
  #sampleDict=sampleDict
  bkgStackDict={}
  sigStackDict={}
  for v in varList:
    if len(plotDict[v]['bin'])!=6:
      bkgStackDict[v]=getStackFromHists([ sampleDict[t]['plots'][v] for t in treeList if not sampleDict[t]['isSignal']])
      sigStackDict[v]=getStackFromHists([ sampleDict[t]['plots'][v] for t in treeList if sampleDict[t]['isSignal']])
  return (bkgStackDict,sigStackDict)

def drawPlots(sampleDict,plotDict,varList='',treeList='',plotDir=''):
  treeList  = matchListToDictKeys(treeList,sampleDict)
  varList   = matchListToDictKeys(varList,plotDict)

  bkgStackDict, sigStackDict =  getBkgSigStacks(sampleDict,plotDict, varList=varList,treeList=treeList)
  for v in varList:
    if len(plotDict[v]['bin'])!=6:
      c1=ROOT.TCanvas("c1","c1")
      bkgStackDict[v].Draw()
      bkgStackDict[v].SetMinimum(1)
      sigStackDict[v].Draw("samenostack")
      decorateAxis(bkgStackDict[v],xAxisTitle=plotDict[v]['xLabel'],yAxisTitle=plotDict[v]['yLabel'])
    #plotDict[v]['yAxis']
      c1.SetLogy(plotDict[v]['yLog'])
      c1.SetLogx(plotDict[v]['xLog'])
      c1.Update()
      saveCanvas(c1,v,plotDir=plotDir)
      del c1
    ### 2D plots:
    elif len(plotDict[v]['bin'])==6:
      for t in treeList:
        c1=ROOT.TCanvas("c1","c1")
        sampleDict[t]['plots'][v].SetTitle(t+"_"+plotDict[v]['title'])
        sampleDict[t]['plots'][v].Draw("colz")
        decorateAxis(sampleDict[t]['plots'][v],xAxisTitle=plotDict[v]['xLabel'],yAxisTitle=plotDict[v]['yLabel'])
        c1.SetLogx(plotDict[v]['xLog'])
        c1.SetLogy(plotDict[v]['yLog'])
        c1.SetLogz(plotDict[v]['zLog'])
        saveCanvas(c1,v+"_"+t,plotDir=plotDir)
        del c1



###############################################################################
###############################################################################
##########################                    #################################
##########################      YIELDS        #################################
##########################                    #################################
###############################################################################
###############################################################################

def getYieldsFromCutDict(sampleDict,cutDict,treeList=''):


  if not treeList:
    treeList=sampleDict.keys()
  #varList=plotDict.keys()
  yieldDict={}
  for t in treeList:
    if sampleDict[t].has_key("weight"):
      print 'using weight value in sampleDict for:  ', t ,  sampleDict[t]['weight']
      weight = str(sampleDict[t]['weight'])
    else: weight= "weight"
    yieldDict[t]={}
    for cut in cutDict:
      cutName=cut.keys()[0]
      cutString=cut[cutName]
      #cutString = "(%s) && (%s)"%(plotDict[p]['presel'],plotDict[p]['cut'])
      yieldDict[t][cutName] = getYieldFromChain(sampleDict[t]['tree'],cutString,weight=weight)
  return yieldDict     


addSquareSum = lambda x: math.sqrt(sum(( e**2 for e in x   )))

def getYieldsFromCutList(sampleDict,cutList,treeList='',returnError=True):
  treeList  = matchListToDictKeys(treeList,sampleDict)
  print treeList

  if not treeList:
    treeList=sampleDict.keys()
  #varList=plotDict.keys()
  yieldDict={}
  for t in treeList:
    ##stupid wjets
    if t.startswith("W"):
      pass
    if sampleDict[t].has_key("weight"):
      print 'using weight value in sampleDict for:  ', t ,  sampleDict[t]['weight']
      weight = str(sampleDict[t]['weight'])
    else: weight= "weight"
    print weight
    yieldDict[t]={}
    for cutName,cutString in cutList:
      #cutName=cut[0]
      #cutString=cut[1]

      #cutString=cut[cutName]
      #cutString = "(%s) && (%s)"%(plotDict[p]['presel'],plotDict[p]['cut'])
      print cutName
      if returnError:
        yieldDict[t][cutName] , yieldDict[t][cutName +"_Err"]= getYieldFromChain(sampleDict[t]['tree'],cutString,weight=weight,returnError=True)
      else:
        yieldDict[t][cutName] = getYieldFromChain(sampleDict[t]['tree'],cutString,weight=weight,returnError=False)
  #########################################################
  ##   Getting Total Background and FOM for each Signal  ##
  #########################################################
  bkgList = [s for s in treeList if not sampleDict[s]['isSignal']]
  sigList = [s for s in treeList if sampleDict[s]['isSignal']]
  if len(bkgList) > 0:
    yieldDict['bkg']={}
    iBkg=0
    for cutName, cutString in cutList:
      yieldDict['bkg'][cutName] = sum([ yieldDict[bkg][cutName] for bkg in bkgList])
      yieldDict['bkg'][cutName+"_Err"] = addSquareSum([ yieldDict[bkg][cutName+"_Err"] for bkg in bkgList])
    iSig=0
    for sig in sigList:
      fomSig='fom_%s'%sig
      yieldDict[fomSig]={}
      for cut in cutList:
        cutName=cut[0]
        cutString=cut[1]
        yieldDict[fomSig][cutName] = yieldDict[sig][cutName]/ math.sqrt(yieldDict['bkg'][cutName])
        yieldDict[fomSig][cutName+"_Err"] = 0.0
    #print "added", iBkg+1 , "to bkg"
  return yieldDict     

def makeTableFromYieldDict(yieldDict,cutList,output="test",saveDir="./"):
  #orderedYieldDictKeys=["TTJets","WJets","bkg","T2Deg300_270","fom_T2Deg300_270"]
  orderedYieldDictKeys=["TTJets","bkg","T2Deg300_270","fom_T2Deg300_270"]
  orderedYieldDictKeys=["T2Deg"]
  #first_col= [ y for y in yieldDict.keys() ]
  first_col= [ y for y in orderedYieldDictKeys ]
  first_row= [ cut[0] for cut in cutList ]

  if not output.endswith(".tex"): output += ".tex"
  f2=open( output,'wb')
  f2.write( '\documentclass{article} \n\usepackage[english]{babel}\n \usepackage[margin=0.1in]{geometry}  \n\usepackage[T1]{fontenc}\n\\begin{document}\
              \n\\begin{center}\n\\begin{tabular}')
  f2.write(' { |c | '+ '|'.join( 'l' for icol in first_col ) +'| } \n' )
  f2.write('\\hline \n')
  f2.write( '      ' +' & '+ '&'.join(icol.replace("_","\_") for icol in first_col) + ' \\\ \hline \n' )
  for row in first_row:
    
    f2.write( '%s& '%row.replace("_","\_") + ' & '.join([ format(yieldDict[t][row],"0.2f") +" $\pm$ " + format(yieldDict[t][row+"_Err" ],"0.2f") for t in orderedYieldDictKeys     ]))
    f2.write('\\\ \hline \n')
  f2.write( '\end{tabular}\n\end{center}\n\end{document}')
  f2.close()
  print 'tex file written'
  if saveDir:
    os.system("pdflatex -output-directory=%s %s"%(saveDir,output))
  return


def getYieldTable(sampleDict,cutList,treeList='',returnError=False):
  yieldDict=getYieldsFromCutList(sampleDict,cutList,treeList=treeList, returnError=returnError)
  makeTableFromYieldDict(yieldDict,cutList,output=output,saveDir=saveDir)
  return yieldDict
  
