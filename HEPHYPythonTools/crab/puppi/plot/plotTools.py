from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import *
import ROOT
import os



steps = ['Step1','Step2','Step3','Step4', 'Step5', 'Step6']
compList = ['gen','puppi','pf']
defStep ='Step5'

samples=['TTJets', 'NuGun', 'ZToMuMu']

fileDict={\
    'TTJets':'/data/nrad/local/TTJets/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root',
    'ZToMuMu':'/data/nrad/local/ZToMuMu/Spring14dr_DYJetsToLL_M-50_13TeV-madgraph-pythia8-tauola_v2_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root',
    'NuGun':'/data/nrad/local//NuGun/Spring14dr_Neutrino_Pt-2to20_gun_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root',
      }

'''
fileDict={\
    'TTJets':'/afs/hephy.at/scratch/n/nrad/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/crab/puppi/Steps/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root',
    'ZToMuMu':'/afs/hephy.at/scratch/n/nrad/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/crab/puppi/ZToMuMu/Spring14dr_DYJetsToLL_M-50_13TeV-madgraph-pythia8-tauola_v2_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root',
    'NuGun':'/afs/hephy.at/scratch/n/nrad/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/crab/puppi/NuGun/Spring14dr_Neutrino_Pt-2to20_gun_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root',
      }
'''

##########   CUTS   ################

noNuFromW = 'ngNuMuFromW+ngNuEFromW+ngNuTauFromW==0'
nNuFromW='ngNuMuFromW+ngNuEFromW+ngNuTauFromW'




########## FUNCTINS ################

chainDict={}
def getChains(sample):
  filelist=[]
  chainDict.clear()
  print sample
  print fileDict[sample]
  for step in steps:
    filelist.append(fileDict[sample].replace('STEP',step))
    exec(\
       'c{0}= ROOT.TChain(\'Events\');\
        c{0}.Add(filelist[steps.index(step)])'.format(step))
    chainDict[('{0}'.format(step))]={}
    chainDict[('{0}'.format(step))]['tChain']=eval(('c{0}'.format(step)))
  return chainDict

def cap1stLet(varS):
  return varS.replace(varS[0],varS[0].capitalize())

def getPlot(c, varS, cutS,binT='',histTitle=''):
  if not histTitle: histTitle=varS+'{'+cutS+'}'
  c.Draw(varS+'>>hTMP{}'.format(binT),cutS, 'goff')
  h = ROOT.gDirectory.Get('hTMP')
  hret = h.Clone('{histTitle}'.format(histTitle=histTitle))
  hret.SetTitle(histTitle)
  ROOT.gDirectory.Delete('hTMP')
  del h
  return hret

def getProfile(c, varS, cutS,binT=(30,0,300,0,5),histTitle=''):
  if not histTitle: histTitle=varS+cutS
  tprTMP=ROOT.TProfile('tprTMP', 'tmpTMP', *binT )
  c.Draw(varS+'>>tprTMP',cutS, 'goff')
  tprRet= tprTMP.Clone('{histTitle}'.format(histTitle=histTitle))
  tprRet.SetTitle(histTitle)
  ROOT.gDirectory.Delete('tprTMP')
  del tprTMP
  return tprRet

def decorate(hist,color=1,width=1,histTitle=''):
  hist.SetLineColor(color)
  hist.SetLineWidth(width)
  hist.SetTitle(histTitle)
  return hist

def decorateAxis(hist,xAxisTitle='x title',yAxisTitle='y title',title=''):
  axis = hist.GetXaxis()
  axis.SetTitle(xAxisTitle)
#  axis.SetTitleOffSet(1)
  axis = hist.GetYaxis()
  axis.SetTitle(yAxisTitle)
#  axis.SetTitleOffSet(1)
#  axis.SetTitleFont(62) 
  if title:  hist.SetTitle(title)
  return hist

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

def chainComp(chainDict, pName,pVar,cutS='' ,binT='',debugIsOn=0,histTitle=''):
  for chain in sorted(chainDict.keys()):
    if debugIsOn: print chain
    pDict = {}
    for i, st in enumerate(compList):
      if not histTitle: hTitle='{STEP}_{Alg}{NAME}'.format(STEP=chain,Alg=st,NAME=pName)
      else: hTitle=histTitle
      pCutModified = cutS.replace("(*)",st)
      pVarModified = pVar.replace("(*)",st)
      if debugIsOn: print pVarModified ,'  with Cut= ', pCutModified
      pDict[st] = getPlot(chainDict[chain]['tChain'],pVarModified,pCutModified,binT=binT,histTitle=hTitle  )
    if debugIsOn: print pDict
    chainDict[chain][pName]=pDict
  return 



canvasDict={}
def printChainStack(chainDict, varToPlot,algToPlot, chainToPlot='',plotDir='',plotName='',baseColor=40,logY=0,logX=0,\
                      legOpt=1,legLoc=(0.4,0.7,0.9,0.9),legRMS=1,legMean=1,legRMSEr=1,legMeanEr=0,cWidth=800,cHeight=800,xTitle=' ',yTitle=' '):
  debugIsOn=1
 # decorateAxis(chainDict['histos'][0],yAxisTitle=dict.get('yAxisTitle'),xAxisTitle=dict.get('xAxisTitle'),title=dict.get('title'))
  defStep=['Step1']
  for var in varToPlot.rsplit(): 
    cName='{}'.format(var)
    hs='{}Stack'.format(var)
    canvasDict[cName]= ROOT.TCanvas(cName,cName,cWidth,cHeight)
    canvasDict[cName].SetLogy(logY)
    canvasDict[cName].SetLogx(logX)
    canvasDict[hs]= ROOT.THStack(hs,plotName)
    if legOpt:
#      legLoc = (0.4,0.7,0.9,0.9)
      legName = 'leg{}'.format(var)
      canvasDict[legName] = ROOT.TLegend(*legLoc);
      canvasDict[legName].SetFillColor(0)
    #dOpt=''

  for alg in algToPlot.rsplit():
    if alg == 'pf':
      st = defStep
      iColor = 3
      print 'Drawing', alg, 'only for', st
    elif alg == 'gen':
      st = defStep
      iColor = 1
      print 'Drawing', alg, 'only for', st
    else:
      st = sorted(chainDict.keys())
      print 'Drawing', alg, 'for', st

    for chain in st:
      if chainToPlot and chain not in chainToPlot.rsplit(): continue 

      if alg == 'pf': iColor=3
      if alg == 'gen': iColor=1    
      if alg == 'puppi': iColor= sorted(chainDict.keys()).index(chain)*2 + baseColor

      print alg, chain, iColor
      histTitle='{CHAIN}_{ALG}_{VAR}'.format(CHAIN=chain, ALG=alg, VAR=var)
      decorate(chainDict[chain][var][alg],color=iColor, width=2,histTitle='{VAR}'.format(VAR=var))
      if legOpt: addToLeg(canvasDict[legName],chainDict[chain][var][alg], pName=histTitle,RMS=legRMS,Mean=legMean,RMSError=legRMSEr,MeanError=legMeanEr) #; print 'added to leg'
      canvasDict[hs].Add(chainDict[chain][var][alg])

    '''
        decorate(chainDict[defStep][var]['gen'],width=2,color=1)
        canvasDict[hs].Add(chainDict[defStep][var][alg])
        if legOpt: addToLeg(canvasDict[legName],chainDict[defStep][var][alg], pName=alg,RMS=legRMS,Mean=legMean,RMSError=legRMSEr,MeanError=legMeanEr)
        print 'drawing  chainDict[\'Step1\'][{var}][{alg}] seperately'.format(chain=chain,var=var,alg=alg)
      elif alg == 'pf':
        decorate(chainDict[defStep][var]['pf'],color=3,width=2)
        if legOpt: addToLeg(canvasDict[legName],chainDict[defStep][var][alg], pName=alg,RMS=legRMS,Mean=legMean,RMSError=legRMSEr,MeanError=legMeanEr)
        canvasDict[hs].Add(chainDict[defStep][var][alg])
        print 'drawing  chainDict[\'Step1\'][{var}][{alg}] seperately'.format(chain=chain,var=var,alg=alg)
    '''
    canvasDict[hs].Draw('nostack')
    canvasDict[legName].Draw() 
    decorateAxis(canvasDict[hs],xAxisTitle=xTitle,yAxisTitle=yTitle)
    if not plotName: plotName=cName 
    if plotDir: canvasDict[cName].Print('{0}/{1}.gif'.format(plotDir,plotName)) 
  return


#######printChain (no stack)
def printChain(plotDict,chainDict,algToPlot='gen puppi pf',varToPlot='',chainToPlot='',dOpt='COLZ',plotDir='',plotPrefix='',debug=0):

  '''  
  for var in varToPlot.rsplit():
    if var not in plotDict.keys(): print var, "not in plotDict";
  for chain in chainToPlot.rsplit():
    if chain not in steps: print chain, "not in steps", steps;
  for alg in algToPlot.rsplit():
    if alg not in compList: print alg, "not in compList", compList;
  '''
#  if chainToPlot not in steps: print chain, "not in steps"; break
  for var in plotDict.keys():
    #if ( varToPlot and var in varToPlot.rsplit() ) or (not varToPlot):
    if not varToPlot or var in varToPlot: 
      if debug: print 'Plotting', var
      chainComp(chainDict,var,plotDict[var]['var'],binT=plotDict[var]['bin'], cutS=plotDict[var]['cut'])
      cTmp=ROOT.TCanvas('cTmp','cTmp',800,800)
      cTmp.Clear() 
#      if not ROOT.c1: c1=TCanvas('c1','c1',800,800)
#      else: ROOT.c1.Clear()    
      for chain in steps:
        if not chainToPlot or chain in chainToPlot.rsplit():
          if debug: print 'For with chain', chain
          for alg in algToPlot.rsplit():
            if debug: print 'Alg:', alg
            xT=plotDict[var]['xTitle'].replace('(*)',alg).replace('STEP',chain)
            yT=plotDict[var]['yTitle'].replace('(*)',alg).replace('STEP',chain)
            pT=plotDict[var]['title'].replace('(*)',alg).replace('STEP',chain)

            cTmp.SetLogx(plotDict[var]['logX'])
            cTmp.SetLogy(plotDict[var]['logY'])
            cTmp.SetLogz(plotDict[var]['logZ'])
            decorateAxis(chainDict[chain][var][alg],xAxisTitle=xT,yAxisTitle=yT,title=pT)            
            chainDict[chain][var][alg].Draw(dOpt)            
            if plotDir: cTmp.Print('{DIR}/{PREFIX}_{CHAIN}_{ALG}_{VAR}.gif'.format(DIR=plotDir,PREFIX=plotPrefix,CHAIN=chain,ALG=alg,VAR=var))
  return cTmp

    #setAliases(chain,**aliasDict)
############TESTING
#chainDict['Step1']['tChain'].Draw('puppiPt*cosh(puppiEta):puppiEta>>(120,-6,6,120,0,6)','abs(puppiPdg)==1 | abs(puppiPdg)==2','COLZ')
#chainComp(chainDict,'charged', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==211')
#chainComp(chainDict,'neutral', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==130' )
#chainComp(chainDict,'e', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==11') 
#chainComp(chainDict,'mu', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==13')
#chainComp(chainDict,'gamma', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==22')
#chainComp(chainDict,'h_HF', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==1')
#chainComp(chainDict,'egamma_HF', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==2')
#chainComp(chainDict,'h_HFpt', '(*)Pt:(*)Eta',binT=(60,-6,6,120,0,6), cutS='abs((*)Pdg)==1')
#chainComp(chainDict,'egamma_HFpt', '(*)Pt:(*)Eta',binT=(60,-6,6,120,0,6), cutS='abs((*)Pdg)==2')
#chainComp(chainDict,'SumEt1D','Sum$((*)Pt)',cutS=noNuFromW,debugIsOn=0)
#chainComp(chainDict,'Met',aliasDict['Met'],cutS=noNuFromW,binT=(100,0,500),debugIsOn=0)
#chainComp(chainDict,'Eta','(*)Eta',cutS=noNuFromW,debugIsOn=0)
#chainComp(chainDict,'EtaNeutral','(*)Eta',cutS=noNuFromW+'&abs((*)Pdg==130)',debugIsOn=0)
#chainComp(chainDict,'EtaCharged','(*)Eta',cutS=noNuFromW+'&abs((*)Pdg==211)',debugIsOn=0)

#chainComp(chainDict,'SumEt','Sum$((*)Pt)')

#metBin=(100,0,4000)
#a = compare(cStep1,'met','Sum$((*)Pt)',pBin=metBin)
#printStack(**a)
########################



def getPlots(pName,pVar,pCut='',binT='',**chainDict):

  pChain=chainDict['cStep1']
  print 'tchain', pChain
  print 'compare list', compList
  print 'binT', binT 

  legLoc = (0.4,0.7,0.9,0.9)
  legend = ROOT.TLegend(*legLoc);
  legend.SetFillColor(0)

  plotDict = {'name':pName, 'histos':[], 'color':'', 'title':'', 'xAxisTitle':'', 'yAxisTitle':'',\
              'legend':legend  }
  for i, st in enumerate(compList):
    pVarModified = pVar.replace("(*)",st)
    print pVarModified
    plotDict['histos'].insert(compList.index(st), getPlot(pChain,pVarModified,pCut,binT=binT))
    decorate(plotDict['histos'][i], color=eval(plotDict['color'] +'+'+ str(i+1)), width=2)
    plotDict['legend'].AddEntry(plotDict['histos'][i],'{PREFIX}{PLOTNAME}  RMS={RMS:.2f}, Mean={MEAN:.2f}'\
                            .format(PREFIX=st,PLOTNAME=pName, RMS=plotDict['histos'][i].GetRMS(),MEAN=plotDict['histos'][i].GetMean()))
  return plotDict

#p = getPlots('sumEt','Sum$((*)Pt)',**chainDict)


################# ALIAS DICTIONARY
def setAliases(chain,aliasdict,debug=0):
  for k in aliasdict.keys():
    for alg in compList:
      alias=''
      if alg in k: 
        alias = k
        if debug==2: print '1', k, alias
      #if '(*)' in k: 
      elif '(*)' in k:
        alias= k.replace('(*)',alg)
        if debug:print '2', k, alias
      if '(*)' not in k and alg not in k:
        case=''
        for alg2 in compList:
          case= alg2 in k 
          if case: 
            break
        if not case:
          alias = '{0}{1}'.format(alg,k)
          if debug:print '3', k , alias
      if alias:
        var='{}'.format(aliasdict[k].replace('(*)',alg))
        if debug: print 'key:',k,'alias:', alias, 'var:',var
        chain.SetAlias(alias,var)
#for chain in steps:
#  setAliases(chainDict[chain]['tChain'],aliasDict)
#################################

##This dict should be used in setAliases 
aliasDict1={\
        'genMet':'genMet',
        'puppiMet':'sqrt( (Sum$((*)Pt*sin((*)Phi)) ) **2+ (Sum$((*)Pt*cos((*)Phi)) )**2)'.replace('(*)','puppi'),
        'pfMet':'sqrt( (Sum$((*)Pt*sin((*)Phi)) ) **2+ (Sum$((*)Pt*cos((*)Phi)) )**2)'.replace('(*)','pf'),
#        'Eta':'(*)Eta',
#        'Pt':'(*)Pt',
#        'Multip':'(*)Count',
#        'MultipVsEta':'(*)Count:{0}Eta'
          }

Eta2='(abs((*)Eta)<2)'
Eta25='(abs((*)Eta)<2.5)'
genxMet='Sum$(genPt*cos(genPhi)*%s)'
genyMet='Sum$(genPt*sin(genPhi)*%s)'

aliasDict=aliasDict1.copy()


aliasDict.update({\
        'yMet':'Sum$((*)Pt*sin((*)Phi))',
        'xMet':'Sum$((*)Pt*cos((*)Phi))',
        #'Met':'sqrt( (Sum$((*)Pt*sin((*)Phi)) ) **2+ (Sum$((*)Pt*cos((*)Phi)) )**2)',

        'SumEt1D':'Sum$((*)Pt)',
        'SumEt':'Sum$((*)Pt):ngoodVertices',


        'yMet2':'Sum$((*)Pt*sin((*)Phi)*{ETABIN})'.format(ETABIN=Eta2),
        'yMet25':'Sum$((*)Pt*sin((*)Phi)*{ETABIN})'.format(ETABIN=Eta25),
        'xMet2':'Sum$((*)Pt*cos((*)Phi)*{ETABIN})'.format(ETABIN=Eta2),
        'xMet25':'Sum$((*)Pt*cos((*)Phi)*{ETABIN})'.format(ETABIN=Eta25),
        'Met2':'sqrt( (Sum$((*)Pt*sin((*)Phi)*{ETABIN})) **2+ (Sum$((*)Pt*cos((*)Phi)*{ETABIN}))**2)'.format(ETABIN=Eta2),
        'Met25':'sqrt( (Sum$((*)Pt*sin((*)Phi)*{ETABIN})) **2+ (Sum$((*)Pt*cos((*)Phi)*{ETABIN}))**2)'.format(ETABIN=Eta25),
        ##subtracing genMet
        'yMet2MinusGen':'Sum$((*)Pt*sin((*)Phi)*{ETABIN})-({GENY})'.format(ETABIN=Eta2, GENY=genyMet % Eta2.replace("(*)","gen")),
        'yMet25MinusGen':'Sum$((*)Pt*sin((*)Phi)*{ETABIN})-({GENY})'.format(ETABIN=Eta25, GENY=genyMet % Eta25.replace("(*)","gen")),
        'xMet2MinusGen':'Sum$((*)Pt*cos((*)Phi)*{ETABIN})-({GENX})'.format(ETABIN=Eta2,GENX=genxMet % Eta2.replace("(*)","gen")),
        'xMet25MinusGen':'Sum$((*)Pt*cos((*)Phi)*{ETABIN})-({GENX})'.format(ETABIN=Eta25,GENX=genxMet % Eta25.replace("(*)","gen")),

        'Met2MinusGen':'sqrt( (Sum$((*)Pt*sin((*)Phi)*{ETABIN})-({GENX})) **2+ (Sum$((*)Pt*cos((*)Phi)*{ETABIN})-{GENY})**2)'\
                            .format(ETABIN=Eta2,GENX=genxMet % Eta2.replace("(*)","gen") ,GENY=genyMet % Eta2.replace("(*)","gen")),
        'Met25MinusGen':'sqrt( (Sum$((*)Pt*sin((*)Phi)*{ETABIN})-({GENX})) **2+ (Sum$((*)Pt*cos((*)Phi)*{ETABIN})-{GENY})**2)'\
                            .format(ETABIN=Eta25,GENX=genxMet % Eta25.replace("(*)","gen") ,GENY=genyMet % Eta25.replace("(*)","gen")),
        ##
        'SumEt2':'Sum$((*)Pt*{ETABIN}):ngoodVertices'.format(ETABIN=Eta2),
        'SumEt25':'Sum$((*)Pt*{ETABIN}):ngoodVertices'.format(ETABIN=Eta25),
        'SumEt1D2':'Sum$((*)Pt*{ETABIN})'.format(ETABIN=Eta2),
        'SumEt1D25':'Sum$((*)Pt*{ETABIN})'.format(ETABIN=Eta25),
        ##
        'SumEtVsGen':'Sum$((*)Pt):Sum$(genPt)',
        })


#### plotDict:


plotDict={}

def getPlotDict(cut):
  plotDict['charged']={'var':'(*)Pt*cosh((*)Eta):(*)Eta','bin':(120,-6,6,120,0,6),'cut':'abs((*)Pdg)==211',\
                        'xTitle':'#eta','yTitle':'Energy (GeV)', 'title':'STEP_(*)Charged_Energy_Map','logX':0,'logY':0,'logZ':1 }
  plotDict['neutral']=plotDict['charged'].copy()
  plotDict['neutral'].update({'cut':'abs((*)Pdg)==130','title':'STEP_(*)Neutral_Energy_Map'})
  plotDict['e']=plotDict['charged'].copy()
  plotDict['e'].update({'cut':'abs((*)Pdg)==11','title':'STEP_(*)Electron_Energy_Map','logZ':0})
  plotDict['mu']=plotDict['charged'].copy()
  plotDict['mu'].update({'cut':'abs((*)Pdg)==13','title':'STEP_(*)Muon_Energy_Map','logZ':0})
  plotDict['gamma']=plotDict['charged'].copy()
  plotDict['gamma'].update({'cut':'abs((*)Pdg)==22','title':'STEP_(*)Photon_Energy_Map'})
  plotDict['h_HFpt']={'var':'(*)Pt:(*)Eta','bin':(60,-6,6,120,0,6),'cut':'abs((*)Pdg)==1',\
                        'xTitle':'#eta','yTitle':'P_{T} (GeV)', 'title':'STEP_(*)Hadron_HF_P_{T}_Map','logX':0,'logY':0,'logZ':1  }
  plotDict['egamma_HFpt']=plotDict['h_HFpt'].copy()
  plotDict['egamma_HFpt'].update({'cut':'abs((*)Pdg)==2','title':'e_gamma_HF_P_{T}_Map' })
  plotDict['SumEt']={'var':aliasDict['SumEt'],'bin':(50,0,50),'cut':cut,\
                        'xTitle':'NV','yTitle':'Energy (GeV)', 'title':'STEP_(*)SumEt','logX':0,'logY':0,'logZ':0  }
  plotDict['SumEt2']=plotDict['SumEt'].copy()
  plotDict['SumEt2'].update({'var':aliasDict['SumEt2'],'title':'STEP_(*)SumEt_#eta<2'})
  plotDict['SumEt25']=plotDict['SumEt'].copy()
  plotDict['SumEt25'].update({'var':aliasDict['SumEt25'],'title':'STEP_(*)SumEt_#eta<2.5'})
  plotDict['SumEtVsGen']=plotDict['SumEt'].copy()
  plotDict['SumEtVsGen'].update({'var':aliasDict['SumEtVsGen'],'title':'STEP_(*)SumEt vs. GenSumEt','xTitle':'GenSumEt','yTitle':'(*)SumEt' })
  return plotDict


###############################################
###############  CHAINS  ######################
###############################################


'''
if AOD:
  if sample=='TTJets':
  #fileTemplate=['/data/nrad/local/PuppiSteps/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root']
    fileTemplate=['/afs/hephy.at/scratch/n/nrad/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/crab/puppi/Steps/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root']
    cut=noNuFromW
  if sample=='ZToMuMu':
    fileTemplate=['/afs/hephy.at/scratch/n/nrad/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/crab/puppi/ZToMuMu/Spring14dr_DYJetsToLL_M-50_13TeV-madgraph-pythia8-tauola_v2_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root']
    cut=''
  if sample=='NuGun':
    fileTemplate=['/afs/hephy.at/scratch/n/nrad/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/crab/puppi/NuGun/Spring14dr_Neutrino_Pt-2to20_gun_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root']
    cut=''
  print 'running on AOD'
  print fileTemplate
else:
  #fileTemplate=['/data/nrad/local/MiniAODPuppiSteps/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1MINIAODPuppiSTEPTupel_converted.root']
  fileTemplate=['/data/nrad/local/MiniAODPuppiSteps/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1MINIAODPuppiSTEPTupel_converted.root']
  print 'running on MiniAOD'
  print fileTemplate
'''




