import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain, getChunks

#from Workspace.HEPHYPythonTools.helpers import getChunksFromNFS, getChunksFromDPM, getChunks
#from Workspace.DegenerateStopAnalysis.cmgTuples_v1_Phys14 import *

from Workspace.DegenerateStopAnalysis.cmgTuples_Phys14_v1 import *
import os
import math


#from Workspace.RA4Analysis.cmgTuples_v5_Phys14 import ttJets_fromEOS, 

#from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_v6_Phys14V3 import WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600,  WJetsToLNu_HT600toInf, allSignals
from Workspace.DegenerateStopAnalysis.cmgTuplesPostProcessed_v1_Phys14V5 import *
from Workspace.DegenerateStopAnalysis.navidPlotTools import saveCanvas,decorate,decorateAxis


targetLumi = 4000. #pb-1
#lumiWeight = xsec[sample['dbsName']]*target_lumi/float(nTotEvents)

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

#a, nt=getChunks(T2DegStop_300_270,"treeProducerSusySingleLepton")


tableDir="/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/postProcessed_v4/tables/"
treeName="treeProducerSusySingleLepton"
ROOT.gStyle.SetOptStat ( 000000)






#sampleDict={
#            'TT':  {'tree':getChainFromChunks(ttJets_PU20bx25,treeName) , 'color':31    , 'isSignal':0 , 'isData':0       },
#            'W':  {'tree':getChainFromChunks([WJetsToLNu_HT100to200_PU20bx25,WJetsToLNu_HT200to400_PU20bx25,WJetsToLNu_HT400to600_PU20bx25,WJetsToLNu_HT600toInf_PU20bx25],treeName) , 'color':41    , 'isSignal':0 , 'isData':0       },
#            "T2Deg300_270": {'tree':getChainFromChunks(T2DegStop_300_270,treeName), 'color':ROOT.kRed     , 'isSignal':1 , 'isData':0 },
#            #'TTs': {'tree':getChain(ttJets['soft'],histname='') ,               'color':1    , 'isSignal':0 , 'isData':0       },            
#         }



try:
  sampleDict
except NameError:
  TTSample    = getChain(ttJets['none'],histname='') 
  T2DegSample = getChain(T2DegStop_300_270['none'],histname='')
  WSample     = getChain(WJetsHTToLNu['none'],histname='')

  sampleDict={
            'TTJets':             {'tree':TTSample    , 'color':31          ,'lineColor':1   , 'isSignal':0 , 'isData':0       },
            'WJets':              {'tree': WSample    , 'color':424         ,'lineColor':1   , 'isSignal':0 , 'isData':0       },
            "T2Deg300_270":       {'tree':T2DegSample , 'color':ROOT.kRed  , 'lineColor':1   , 'isSignal':1 , 'isData':0 },
            #'TTs': {'tree':getChain(ttJets['soft'],histname='') ,               'color':1    , 'isSignal':0 , 'isData':0       },            
         }



  #for s in sampleDict:
  #  sampleDict[s]['nEvents']=sampleDict[s]['tree'].GetEntries()
  #  sampleDict[s]['nEvents']=sampleDict[s]['tree'].GetEntries()
  #  sampleDict[s]['tree'].GetEntry(0)
  #  sampleDict[s]['xsec']=sampleDict[s]['tree'].GetLeaf('xsec').GetValue(0)
  #  sampleDict[s]['weight']= ( float(sampleDict[s]['xsec']) * targetLumi ) / float(sampleDict[s]['nTot'])
  #  print s, sampleDict[s]['weight']







###############################################################################
###############################################################################
##########################                      ###############################
########################    Cuts and Variables    #############################
##########################                      ###############################
###############################################################################
###############################################################################





###Cuts and Preselction
muPdg="(abs(LepGood_pdgId)==13)"
muId="(LepGood_mediumMuonId==1)"
muPt5_25="(LepGood_pt > 5 && LepGood_pt < 25)"
muEta="abs(LepGood_eta)<2.4"
muMiniIso="(LepGood_miniRelIso < 0.2 || LepGood_pt < 15)&&(LepGood_miniRelIso < 0.4 || LepGood_pt > 15)"


muonCutList= [

      ["muPdg", muPdg]  ,
      ["muId", muId],
      ["muPt5_25", muPt5_25],
      ["muEta", muEta],
      ["muMiniIso", muMiniIso],

            ]




muSelect= "(%s)"%" && ".join([muPdg,muId,muPt5_25,muEta,muMiniIso]) 

preMET="(met_pt>200)"
preHT="(htJet25 > 300)"
preISR="(Jet_pt[0]>110 && Jet_pt[1]>60)"
preSelection = "("+" && ".join([preMET,preISR  ]) + ")"

preSelection = joinCutStrings([preMET,preISR,preHT])
### Additional Variables:


mt0=80

####
####   Var Templates
####


invMassTemplate =  "sqrt(2*%(TYPE)s_pt*met_pt*(cosh(%(TYPE)s_phi-met_phi)-cos(%(TYPE)s_phi-met_phi)))"
mtTemplate      =  "sqrt(2*%(TYPE)s_pt*met_pt*(1-cos(%(TYPE)s_phi-met_phi)))"
QTemplate       =  "1-%(mt0)s^2/(2*met_pt*%(TYPE)s_pt)"



invMass   = invMassTemplate%{"TYPE":"LepGood"}
mt        = mtTemplate%{"TYPE":"LepGood"}
Q         = QTemplate%{"TYPE":"LepGood","mt0":mt0}
cos       = 'cos(met_phi-LepGood_phi)'
dmt       = Q+":"+cos

mtQline = lambda mt1: "-1*("+str(mt0)+"/"+str(mt1) +')^2*(1 - cos(met_phi-LepGood_phi))+1:cos(met_phi-LepGood_phi)'
#Qcut = lambda mt1: "-1*("+str(mt0)+"/"+str(mt1) +')^2*(cos(met_phi-LepGood_phi)):cos(met_phi-LepGood_phi)'
arbQcut = lambda m,b: ""+str(m)+'*cos(met_phi-LepGood_phi)+'+str(b)
arbQcutline = lambda m,b: arbQcut(m,b)+':cos(met_phi-LepGood_phi)'
arbQcutStr= lambda m, b: '('+Q+')>('+arbQcut(m,b)+')'



binEta=[100,-3,3]
binPT=[100,0,300]
binMT=binPT
binDMT=[40,1.5,-5,40,-1,1]




ht    =             "Sum$(Jet_pt)"
htCut = lambda htv: "(%s>%s)"%(ht,htv)
metCut = lambda met: "(met_pt>%s)"%met

###
###  Signal Regions 
###


SR1="(%s && met_pt>300 && Sum$(nBJetLoose40+nBJetMedium40+nBJetTight40)==0 && LepGood_pdgId==13 && abs(LepGood_eta)<1.5)"%(htCut(300))
SR1a=SR1+"&&(%s<60)"%mt
SR1b=SR1+"&&(%s>60)&&(%s<88)"%(mt,mt)
SR1c=SR1+"&&(%s>88)"%mt


SR1cutList=[
      ["noCut","(1)"],
      ["LepGood","LepGood_pt"],
      ["met300", metCut(300) ],
      ["ht300",htCut(300)],
      ["bVeto","Sum$(nBJetLoose40+nBJetMedium40+nBJetTight40)==0",],
      ["eta1.5","abs(LepGood_eta)<1.5"] ,
      ["ht+met", joinCutStrings([metCut(300),htCut(300) ])],
      ["ht+met+bVeto",joinCutStrings([ "Sum$(nBJetLoose40+nBJetMedium40+nBJetTight40)==0",metCut(300),htCut(300) ])],
      ["ht+met+bVeto+eta",joinCutStrings([ "Sum$(nBJetLoose40+nBJetMedium40+nBJetTight40)==0",metCut(300),htCut(300), "abs(LepGood_eta)<1.5"  ])],
      ["all",SR1],
      ]



cutDict = [
      {"noCut": "(1)" } ,
      {"preSel": preSelection} ,
      {"muIndex": muSelect} ,
      {"preSel_muIndex": muSelect} ,
      {"SR1": SR1 } ,
      {"presel_SR1": "(%s&&%s)"%(preSelection,SR1) } ,
      {"presel_SR1a": "(%s&&%s)"%(preSelection,SR1a) } ,
      {"presel_SR1b": "(%s&&%s)"%(preSelection,SR1b) } ,
      {"presel_SR1c": "(%s&&%s)"%(preSelection,SR1c) } ,
           ]



cutList = [
      ["noCut", "(1)" ] ,
      ["preSel", preSelection] ,
      ["muIndex", muSelect] ,
      #["preSel_muIndex", "(%s&&%s)"%(muSelect, preSelection)] ,
      ["SR1", SR1 ] ,
      ["presel_SR1", "(%s&&%s)"%(preSelection,SR1) ] ,
      ["presel_SR1a", "(%s&&%s)"%(preSelection,SR1a) ] ,
      ["presel_SR1b", "(%s&&%s)"%(preSelection,SR1b) ] ,
      ["presel_SR1c", "(%s&&%s)"%(preSelection,SR1c) ] ,
           ]






plotDict = {


      #'lep_pt':  {'var':"LepGood_pt",    "presel":preSelection,              "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binPT,  "title":""    ,"xLabel":"lep_pt",    "yLabel":"",     "xLog":0, "yLog":1                  },
      #'lep_MT':     {'var':mt,           "presel":preSelection,              "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binMT,  "title":""    ,"xLabel":"lep_MT",    "yLabel":"",     "xLog":0, "yLog":1                  },
      #'lep_dmt':    {'var':dmt,          "presel":preSelection,              "cut":"(1)", "fillColor":"" ,"color":""     ,"lineWidth":1 , "bin":binDMT, "title":""    ,"xLabel":"cos(\phi)", "yLabel":"Q",    "xLog":0, "yLog":0    ,"zLog":1     },

      'mu_pt':  {'var':"LepGood_pt",    "presel":"(%s&&%s)"%( "(%s)"%" && ".join([muId,muEta,muMiniIso]) ,preSelection), "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binPT,  "title":"Muon P_{T}"    ,"xLabel":"mu_pt",     "yLabel":"",     "xLog":0, "yLog":1                  },
      'mu_MT':     {'var':mt,           "presel":"(%s&&%s)"%( "(%s)"%" && ".join([muId,muEta,muMiniIso]) ,preSelection), "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binMT,  "title":"MT"    ,"xLabel":"MT",        "yLabel":"",     "xLog":0, "yLog":1                  },
      #'mu_MT_presel':     {'var':mt,           "presel":"(%s)"%(preSelection), "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binMT,  "title":"MT"    ,"xLabel":"MT",        "yLabel":"",     "xLog":0, "yLog":1                  },
      'mu_dmt':    {'var':dmt,          "presel":joinCutStrings([preSelection]), "cut":"(1)", "fillColor":"" ,"color":""     ,"lineWidth":1 , "bin":binDMT, "title":"Deconstructed_MT"    ,"xLabel":"cos(\phi)", "yLabel":"Q",    "xLog":0, "yLog":0 ,"zLog":1        },
      'mu_eta':  {'var':"LepGood_eta",    "presel":preSelection, "cut":"(1)", "fillColor":"" ,"color":"fill" ,"lineWidth":1 , "bin":binEta,  "title":"Muon Eta"    ,"xLabel":"mu_eta",     "yLabel":"",     "xLog":0, "yLog":1                  },

      }



getAllAlph = lambda str: ''.join(ch for ch in str if ch not in "Kl13@$%[]{}();'\"")


### Move To PlotTools

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
    if not sampleDict[s].has_key('plots'):
      sampleDict[s]['plots']={}
    for p in varList:
      lineWidth=plotDict[p]['lineWidth']
      if plotDict[p]['color'].lower()=="fill" and not sampleDict[s]['isSignal']:
        #color = ROOT.kBlack
        color = sampleDict[s]['color']
        fcolor = sampleDict[s]['color']
      else:
        color  = sampleDict[s]['color']
        fcolor = 0 
        if sampleDict[s]['isSignal']:
          lineWidth=2
      print "Sample:" , s , "Getting Plot: ", p 
      sampleDict[s]['plots'][p] = getGoodPlotFromChain(sampleDict[s]['tree'] , plotDict[p]['var'], plotDict[p]['bin'],\
                                                       varName     = p  ,
                                                       cutString   = "(%s) && (%s)"%(plotDict[p]['presel'],plotDict[p]['cut']),                      
                                                       color       = color,
                                                       fillColor   = fcolor,
                                                       lineWidth   = lineWidth,
                                                       weight      = 'weight'
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



#muFromTau="mediumMuIndex>-1&&muIgpMatch[mediumMuIndex]>-1&&gpTag[muIgpMatch[mediumMuIndex]]==2"
#preselIvan="(type1phimet_pt>200.&&isrJetPt>110.&&ht>300.)"+"&&"+"(isrJetBTBVetoPassed)"+"&&"+"((nHardElectrons+nHardTaus)==0)"+"&&"+\
#             "(mediumMuIndex>-1&&(muPt[mediumMuIndex]<20.||nHardMuonsMediumWP==1))"+"&&"+"(njet60<3)"
#preselRobert="(type1phiMet>200.&&isrJetPt>110.&&ht>300.)"+"&&"+"(isrJetBTBVetoPassed)"+"&&"+"((nHardElectrons+nHardTaus)==0)"+"&&"+\
#             "(mediumMuIndex>-1&&(muPt[mediumMuIndex]<20.))"+"&&"+"(njet60<3)"
#preselection=preselRobert
#SR1="(ht>400.&&type1phiMet>300.)"+"&&"+"(nbtags==0)"+"&&"+"(abs(muEta[mediumMuIndex])<1.5)"+"&&"+"(muPdg[mediumMuIndex]>0)"
#SR1a=SR1+"&&"+"("+MT + "<60)"
#SR1b=SR1+"&&"+"("+MT + ">60)&&("+ MT + "< 88)"
#SR1c=SR1+"&&"+"("+MT + ">88)"
#SR2="(isrJetPt>325.&&type1phiMet>300.)"+"&&"+"(nHardbtags==0&&nSoftbtags>0)"
#mtcut = MT+">80"






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
  orderedYieldDictKeys=["TTJets","WJets","bkg","T2Deg300_270","fom_T2Deg300_270"]
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
    os.system("pdflatex -output-directory=%s %s"%(saveDir,outName))
  return




#plots = [
#          ['sqrt(2*leptonPt*met*(1-cos(metPhi-leptonPhi)))', [20,0,800], 'mt'],\
#          ['acos((leptonPt + met*cos(leptonPhi - metPhi))/sqrt(leptonPt**2 + met**2+2*met*leptonPt*cos(leptonPhi-metPhi)))', [16,0,3.2], 'd
#phi']
#    ]
#
#
#
#for var, binning, fname in plots:
#  c1 = ROOT.TCanvas() 
#  hPresel = getPlotFromChain(c, var, binning, presel, 'weight')
#  hPresel.SetLineColor(ROOT.kBlack)
#  hPresel.SetTitle("")
#  hPresel.GetYaxis().SetRangeUser(0.1, 1.5*hPresel.GetMaximum())
#  hPresel.Draw()
#
#  for sig in signals:
#    sig['hPresel'] = getPlotFromChain(sig['c'], var, binning, presel, 'weight')
#    sig['hPresel'].SetLineColor(sig['color'])
#    sig['hPresel'].SetLineWidth(2)
#    sig['hPresel'].SetTitle("")
#
#

#
#
#
#
#
#
#
#




#### WJET DMT

#h2=ROOT.TH2F("h2","h2",*binDMT)
#for w in ["W4", "W2", "W3", "W1"]:
#  sampleWDict[w]['tree'].Draw( plotDict['mu_dmt']['var'] + ">>+h2", "(" + str( sampleWDict[w]['weight'] ) +")*" +plotDict['mu_dmt']['presel'] , "COLZ")














#
