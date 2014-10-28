from plotTools import *
#from plotAliases import *
#from plotChains import *
'''
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--sample", dest="sample", default="", type="string", action="store", help="infile:Which infile.")
args = parser.parse_args()
print args.sample
'''
AOD=1
getPlotIsOn=0


vetoList=( 1000022, 1000012, 1000014, 1000016, 2000012, 2000014, 2000016, 1000039, 5100039, 4000012, 4000014, 4000016, 9900012, 9900014, 9900016, 39, 12, 13, 14, 16)

vetoPdg='&'.join( ["(abs(genPdg)!="+str(p)+")" for p in vetoList])
#samples=['TTJets', 'NuGun', 'ZToMuMu']
sample=samples[2]

getChains(sample)
noNuFromW = 'ngNuMuFromW+ngNuEFromW+ngNuTauFromW==0'
nNuFromW='ngNuMuFromW+ngNuEFromW+ngNuTauFromW'
plotDir = '/afs/hephy.at/user/n/nrad/www/Puppi/{}/'.format(sample)




"""
################ Options  ##################

AOD=1
getPlotIsOn=0


print sample

'''
if parser.sample not in samples:
  print sample, ' not in' ,samples
  sample=samples[2]
else: sample=parser.sample
'''


################ Files  ##################

if AOD:
  if sample=='TTJets':
  #fileTemplate=['/data/nrad/local/PuppiSteps/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root']
  
    fileTemplate=['/afs/hephy.at/scratch/n/nrad/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/crab/puppi/Steps/Spring14dr_TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_AODSIM_PU_S14_POSTLS170_V6-v1PuppiSTEPMINIAODTupel_converted.root']
    noNuFromW = 'ngNuMuFromW+ngNuEFromW+ngNuTauFromW==0'
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

filelist=[]

now = datetime.datetime.now()
#plotDir = '/afs/hephy.at/user/n/nrad/www/tmp/{YEAR}-{MONTH}-{DAY}/'.format(YEAR=now.year, MONTH=now.month, DAY=now.day)

#plotDir = '/afs/hephy.at/user/n/nrad/www/AODvsMiniAOD/'
plotDir = '/afs/hephy.at/user/n/nrad/www/Puppi/{}/'.format(sample)


steps = ['Step1','Step2','Step3','Step4', 'Step5','Step6']
#steps = ['Step6']
compList = ['gen','puppi','pf']

chainDict={}
for step in steps:
  filelist.append(fileTemplate[0].replace('STEP',step))
  exec(\
     'c{0}= ROOT.TChain(\'Events\');\
      c{0}.Add(filelist[steps.index(step)])'.format(step))
  chainDict[('{0}'.format(step))]={}
  chainDict[('{0}'.format(step))]['tChain']=eval(('c{0}'.format(step)))
"""


ROOT.gROOT.Reset()
#ROOT.gStyle.SetOptTitle(0) 
ROOT.gStyle.SetOptStat ( 000000)



#### SETTING ALIASES

'''
aliasDict={\
        'genMet':'genMet',
        'puppiMet':'sqrt( (Sum$((*)Pt*sin((*)Phi)) ) **2+ (Sum$((*)Pt*cos((*)Phi)) )**2)'.replace('(*)','puppi'),
        'pfMet':'sqrt( (Sum$((*)Pt*sin((*)Phi)) ) **2+ (Sum$((*)Pt*cos((*)Phi)) )**2)'.replace('(*)','pf'),
        'Met':'sqrt( (Sum$((*)Pt*sin((*)Phi)) ) **2+ (Sum$((*)Pt*cos((*)Phi)) )**2)',
        'SumEt':'Sum$((*)Pt):ngoodVertices',
#        'Eta':'(*)Eta',
#        'Pt':'(*)Pt',
#        'Multip':'(*)Count',
#        'MultipVsEta':'(*)Count:{0}Eta'
          }

####### GenMet is already defined so don't want to mess it up.
for chain in steps:
  for var in aliasDict:
    chainDict[chain]['tChain'].SetAlias(var,aliasDict[var])


#for chain in steps: setAliases(chainDict[chain]['tChain'],aliasDict)


Eta2='(abs((*)Eta)<2)'
Eta25='(abs((*)Eta)<2.5)'

genxMet='Sum$(genPt*cos(genPhi)*%s)'
genyMet='Sum$(genPt*sin(genPhi)*%s)'
#'Sum$(genMet*cos(genPhi)*(abs(genEta)>10))'

#'sqrt( (Sum$(puppiPt*sin(puppiPhi)*(abs(puppiEta)<2))+(Sum$(genMet*cos(genPhi))*(abs(genEta)<2))) **2+ (Sum$(puppiPt*cos(puppiPhi)*(abs(puppiEta)<2))+Sum$(genMet*sin(genPhi))*(abs(genEta)<2))**2)'


aliasDict.update({\
        'yMet':'Sum$((*)Pt*sin((*)Phi))',
        'xMet':'Sum$((*)Pt*cos((*)Phi))',
        'Met':'sqrt( (Sum$((*)Pt*sin((*)Phi)) ) **2+ (Sum$((*)Pt*cos((*)Phi)) )**2)',

        'SumEt1D':'Sum$((*)Pt)',

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

        'SumEt2':'Sum$((*)Pt*{ETABIN}):ngoodVertices'.format(ETABIN=Eta2),
        'SumEt25':'Sum$((*)Pt*{ETABIN}):ngoodVertices'.format(ETABIN=Eta25),
        'SumEt1D2':'Sum$((*)Pt*{ETABIN})'.format(ETABIN=Eta2),
        'SumEt1D25':'Sum$((*)Pt*{ETABIN})'.format(ETABIN=Eta25),

        'SumEtVsGen':'Sum$((*)Pt):Sum$(genPt)',



        })

'''
###################



if AOD:
  form='{}_AOD'.format(sample)
else:
  form='{}_MiniAOD'.format(sample)


######### PLOTTING ############

#for var in aliasDict.keys()
#  chainComp(chainDict,var,aliasDict[var],cutS=cut)




if getPlotIsOn:

  chainComp(chainDict,'Met','(*)Met',cutS=cut,binT=(100,0,350))
  printChainStack(chainDict,'Met','gen pf puppi',plotDir=plotDir,plotName='{}_Met'.format(form),xTitle='GeV',yTitle='nEvents',logY=1)
  
  chainComp(chainDict,'Met2',aliasDict['Met2'],cutS=noNuFromW,binT=(100,0,350),)
  chainComp(chainDict,'Met25',aliasDict['Met25'],cutS=noNuFromW,binT=(100,0,350),)
  printChainStack(chainDict,'Met2','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_Met_Eta<2'.format(form))
  printChainStack(chainDict,'Met25','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_Met_Eta<2.5'.format(form))

  #printChainStack(chainDict,'Met','gen pf puppi',plotDir=plotDir,plotName='{}Met'.format(form),xTitle='GeV',yTitle='nEvents',logY=1)

  ####### X and Y Components of MET
  legLoc1=(0.525,0.72,0.9,0.9)
 
  chainComp(chainDict,'yMet',aliasDict['yMet'],cutS=cut,binT=(100,-200,200),)
  chainComp(chainDict,'xMet',aliasDict['xMet'],cutS=cut,binT=(100,-200,200),)

  chainComp(chainDict,'yMet25',aliasDict['yMet25'],cutS=cut,binT=(100,-200,200),)
  chainComp(chainDict,'xMet25',aliasDict['xMet25'],cutS=cut,binT=(100,-200,200),)
  chainComp(chainDict,'yMet2',aliasDict['yMet2'],cutS=cut,binT=(100,-200,200),)
  chainComp(chainDict,'xMet2',aliasDict['xMet2'],cutS=cut,binT=(100,-200,200),)

  printChainStack(chainDict,'yMet','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_Y_Met'.format(form),legLoc=legLoc1)
  printChainStack(chainDict,'xMet','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_X_Met'.format(form),legLoc=legLoc1)

  printChainStack(chainDict,'yMet25','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_Y_Met_Eta<2.5'.format(form),legLoc=legLoc1)
  printChainStack(chainDict,'xMet25','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_X_Met_Eta<2.5'.format(form),legLoc=legLoc1)
  printChainStack(chainDict,'yMet2','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_Y_Met_Eta<2'.format(form),legLoc=legLoc1)
  printChainStack(chainDict,'xMet2','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_X_Met_Eta<2'.format(form),legLoc=legLoc1)

 

  ####### X and Y Components with Gen Subtracted
  chainComp(chainDict,'yMet25gs',aliasDict['yMet25MinusGen'],cutS=cut,binT=(100,-200,200),)
  chainComp(chainDict,'xMet25gs',aliasDict['xMet25MinusGen'],cutS=cut,binT=(100,-200,200),)
  chainComp(chainDict,'yMet2gs',aliasDict['yMet2MinusGen'],cutS=cut,binT=(100,-200,200),)
  chainComp(chainDict,'xMet2gs',aliasDict['xMet2MinusGen'],cutS=cut,binT=(100,-200,200),)

  printChainStack(chainDict,'yMet25gs','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_Y_Met_Eta<25_GenMETSubtracted'.format(form),legLoc=legLoc1)
  printChainStack(chainDict,'xMet25gs','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_X_Met_Eta<25_GenMETSubtracted'.format(form),legLoc=legLoc1)
  printChainStack(chainDict,'yMet2gs','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_Y_Met_Eta<2_GenMETSubtracted'.format(form),legLoc=legLoc1)
  printChainStack(chainDict,'xMet2gs','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_X_Met_Eta<2_GenMETSubtracted'.format(form),legLoc=legLoc1)
  #############



  chainComp(chainDict,'Met2MinusGen',aliasDict['Met2MinusGen'],cutS=cut,binT=(100,0,350))
  chainComp(chainDict,'Met25MinusGen',aliasDict['Met25MinusGen'],cutS=cut,binT=(100,0,350))

  printChainStack(chainDict,'Met2MinusGen','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_Met_Eta<2_GenMETSubtracted'.format(form))
  printChainStack(chainDict,'Met25MinusGen','gen pf puppi',logY=1,plotDir=plotDir,plotName='{}_Met_Eta<25_GenMETSubtracted'.format(form))

  '''
  chainComp(chainDict,'Eta','(*)Eta',cutS=cut)
  printChainStack(chainDict,'Eta','gen pf puppi',plotDir=plotDir,plotName='{}Eta'.format(form),xTitle='Eta',yTitle='nEvents')
  '''

  '''
  chainComp(chainDict,'MetLP','(*)Met',cutS='ngoodVertices < 28 & {}'.format(cut),binT=(100,0,350))
  chainComp(chainDict,'MetHP','(*)Met',cutS='ngoodVertices >= 28 & {}'.format(cut),binT=(100,0,350))

  printChainStack(chainDict,'MetLP','gen pf puppi',plotDir=plotDir,plotName='{}MetLP'.format(form),xTitle='GeV',yTitle='nEvents',logY=1)
  printChainStack(chainDict,'MetHP','gen pf puppi',plotDir=plotDir,plotName='{}MetHP'.format(form),xTitle='GeV',yTitle='nEvents',logY=1)
  '''

if 0:
  chainComp(chainDict,'SumEt',aliasDict['SumEt'],cutS=cut,binT=(50,0,50))
  chainComp(chainDict,'SumEt2',aliasDict['SumEt2'],cutS=cut,binT=(50,0,50))
  chainComp(chainDict,'SumEt25',aliasDict['SumEt25'],cutS=cut,binT=(50,0,50))

  chainComp(chainDict,'SumEt1D',aliasDict['SumEt1D'],cutS=cut,binT=(100,0,3000))
  chainComp(chainDict,'SumEt1D2',aliasDict['SumEt1D2'],cutS=cut,binT=(100,0,3000))
  chainComp(chainDict,'SumEt1D25',aliasDict['SumEt1D25'],cutS=cut,binT=(100,0,3000))

  chainComp(chainDict,'charged', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==211')
  chainComp(chainDict,'neutral', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==130' )
  chainComp(chainDict,'e', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==11') 
  chainComp(chainDict,'mu', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==13')
  chainComp(chainDict,'gamma', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==22')

  #chainComp(chainDict,'h_HF', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==1')
  #chainComp(chainDict,'egamma_HF', '(*)Pt*cosh((*)Eta):(*)Eta',binT=(120,-6,6,120,0,6), cutS='abs((*)Pdg)==2')

  chainComp(chainDict,'h_HFpt', '(*)Pt:(*)Eta',binT=(60,-6,6,120,0,6), cutS='abs((*)Pdg)==1')
  chainComp(chainDict,'egamma_HFpt', '(*)Pt:(*)Eta',binT=(60,-6,6,120,0,6), cutS='abs((*)Pdg)==2')

'''
chainDict[step]['charged']['puppi'].Draw('COLZ')
'''

#chainComp(chainDict,'MetBarrel','(*)Met*(abs((*)Eta<2.5))',cutS=cut,binT=(100,0,350))
#chainComp(chainDict,'MetEndCaps','(*)Met*(abs((*)Eta>=2.5)*(abs((*)Eta<3)))',cutS=cut,binT=(100,0,350))
#chainComp(chainDict,'MetHF','(*)Met*(abs((*)Eta>3))',cutS=cut,binT=(100,0,350))

#printChainStack(chainDict,'MetBarrel','gen pf puppi',plotDir=plotDir,plotName='MetBarrel'.format(form),xTitle='GeV',yTitle='nEvents',logY=1)
#printChainStack(chainDict,'MetEndCaps','gen pf puppi',plotDir=plotDir,plotName='MetEndCaps'.format(form),xTitle='GeV',yTitle='nEvents',logY=1)
#printChainStack(chainDict,'MetHF','gen pf puppi',plotDir=plotDir,xTitle='GeV',yTitle='nEvents',logY=1)


'''
plotDict={}


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

'''

#chainComp(chainDict,'SumEt1D','Sum$((*)Pt)',cutS=cut,debugIsOn=0)
#chainComp(chainDict,'Met',aliasDict['Met'],cutS=cut,binT=(100,0,500),debugIsOn=0)
#chainComp(chainDict,'Eta','(*)Eta',cutS=cut,debugIsOn=0)
#chainComp(chainDict,'EtaNeutral','(*)Eta',cutS=cut+'&abs((*)Pdg==130)',debugIsOn=0)
#chainComp(chainDict,'EtaCharged','(*)Eta',cutS=cut+'&abs((*)Pdg==211)',debugIsOn=0)

'''
def printChain(plotDict,chainDict,algToPlot='gen puppi pf',varToPlot='',chainToPlot='',dOpt='COLZ',plotDir='',printPrefix=''):
  for var in plotDict.keys():
    if not varToPlot or var in varToPlot.rsplit(): 
      print 'dealing with', var
      chainComp(chainDict,var,plotDict[var]['var'],binT=plotDict[var]['bin'], cutS=plotDict[var]['cut'])

      cTmp=ROOT.TCanvas('cTmp','cTmp',800,800)
      cTmp.Clear() 
#      if not ROOT.c1: c1=TCanvas('c1','c1',800,800)
#      else: ROOT.c1.Clear()    

      for chain in steps:
        if not chainToPlot or chain in chainToPlot.rsplit():
          print 'also with chain', chain
          for alg in algToPlot.rsplit():
            print 'algs', alg
      
            xT=plotDict[var]['xTitle'].replace('(*)',alg).replace('STEP',chain)
            yT=plotDict[var]['yTitle'].replace('(*)',alg).replace('STEP',chain)
            pT=plotDict[var]['title'].replace('(*)',alg).replace('STEP',chain)

            cTmp.SetLogx(plotDict[var]['logX'])
            cTmp.SetLogy(plotDict[var]['logY'])
            cTmp.SetLogz(plotDict[var]['logZ'])
            decorateAxis(chainDict[chain][var][alg],xAxisTitle=xT,yAxisTitle=yT,title=pT)            
            chainDict[chain][var][alg].Draw(dOpt)            
            if plotDir and not noPrint: cTmp.Print('{DIR}/{FORM}_{CHAIN}_{ALG}_{VAR}.gif'.format(DIR=plotDir,FORM=plotPrefix,CHAIN=chain,ALG=alg,VAR=var))

  return cTmp
'''
#### USE LIKE THIS
#printChain(plotDict,chainDict,noPrint=0,algToPlot='pf',chainToPlot='Step1')
#printChain(plotDict,chainDict,noPrint=0,algToPlot='puppi')


    #else: print 'invalid var', var
            
            #chainDict[chain][var][alg].SetTitle(plotDict[var])
            #chainDict[chain][var][alg].Draw(dOpt)

  #        for var in 'SumEt'.rsplit():
  #          chainDict[chain][var]['puppi'].Draw('COLZ')























##############pdg ID
lookAtPdg=1

pfcDict={1:'h_HF',2:'egamma_HF',211:'h',130:'h0',22:'gamma',11:'e',13:'mu'}

if lookAtPdg:
  print lookAtPdg

pdgDict={}

def lookAtPdg():
  pdgDictRaw={}

  chainComp(chainDict,'pdgId','(*)Pdg',binT=(500,-250,250),histTitle='PdgID')
  

  for alg in 'gen puppi pf'.rsplit():
    pdgDictRaw[alg]={}
    pdgDict[alg]={}

    for chain in steps:
      pdgDictRaw[alg][chain]={}
      pdgDict[alg][chain]={}

      hist =  chainDict[chain]['pdgId'][alg]

      #print '##########', chain,'##########' 

      for i in range(0,500):
    #    print i, hist.GetBinLowEdge(i), hist.GetBinContent(i)
        if hist.GetBinContent(i):
          binEdge=int(hist.GetBinLowEdge(i))
          binVal=int(hist.GetBinContent(i))
          #print i, binEdge, binVal
          pdgDictRaw[alg][chain][binEdge]=binVal
          
          '''
          if pfcDict[abs(binEdge)] not in pdgDict[alg][chain]:
            pdgDict[alg][chain][pfcDict[abs(binEdge)]]=binVal
          else:
            pdgDict[alg][chain][pfcDict[abs(binEdge)]]+=binVal
          '''
  return pdgDictRaw


####Print Table

def pdgTable(alg,tOpt=0):
  ##tOpt=0 print all the values
  ##tOpt=1 print the first value, and ratios to the last value after that
  ##tOpt=2 print the first value as 1, and ratios to the last value after that
  print alg
  row_format ="{:>15}" * (len(steps) + 1)
  print row_format.format(alg, *steps)
  #for team, row in zip(teams_list, data):
  val=0
  for pdg in pfcDict.values():
    
    row=[]
    first=1
    for chain in steps:
      if first: 
        cN=chain
        if tOpt==1: val=pdgDict[alg][chain][pdg]
        if tOpt==2: val=pdgDict[alg][chain][pdg]/float(pdgDict[alg][cN][pdg])
      else:
        cL=cN
        cN=chain 
        if tOpt==1 or tOpt==2 :val=pdgDict[alg][cN][pdg]/float(pdgDict[alg][cL][pdg])
      if tOpt==0: row.append(pdgDict[alg][chain][pdg]) #use this if don't want the ratio
      if tOpt==1 or tOpt==2: row.append('%0.2f' % val)
      first=0
    print row_format.format(pdg,*row)



#####Use like this:   lookAtPdg(); pdgTable('puppi',tOpt=1)


#####
for chain in steps:
  for var in aliasDict1:
    chainDict[chain]['tChain'].SetAlias(var,aliasDict[var])
################# RESPONSE
"""
plotDict['metRes']={'bin':(100,0,400),'cut':'',\
                      'xTitle':'genMet','yTitle':'PuppiResponse (GeV)', 'title':'','logX':0,'logY':0,'logZ':1 }
plotDict['metRes']['var']='(*)Met/genMet'

responseCut=nNuFromW+'==1'
#responseCut=''
responseBin='(30,0,300,100,0,5)'
responseProfileBin= (35,0,350,0,3)


responseDict={}

for chain in steps:
  responseDict[chain]={}
  for alg in 'gen puppi pf'.rsplit():
    responseDict[chain][alg]={\
                              'res':getPlot(chainDict[chain]['tChain'],'{ALG}Met/genMet:genMet'.format(ALG=alg),responseCut,binT=responseBin,\
                                    histTitle='{CHAIN}_{ALG}_MET_Response_Dist'.format(FORM=form,CHAIN=chain,ALG=alg)),
                              'resProf':getProfile(chainDict[chain]['tChain'],'{ALG}Met/genMet:genMet'.format(ALG=alg),responseCut,binT=responseProfileBin,\
                                    histTitle='{CHAIN}_{ALG}_MET_ResponseCurve'.format(FORM=form,CHAIN=chain,ALG=alg))
                              }


'''
resPuppi1=getPlot(chainDict['Step1']['tChain'],'puppiMet/genMet:genMet',responseCut,binT=responseBin,histTitle='res')
resPuppi2=getPlot(chainDict['Step2']['tChain'],'puppiMet/genMet:genMet',responseCut,binT=responseBin,histTitle='res')
resPuppi3=getPlot(chainDict['Step3']['tChain'],'puppiMet/genMet:genMet',responseCut,binT=responseBin,histTitle='res')
resPuppi4=getPlot(chainDict['Step4']['tChain'],'puppiMet/genMet:genMet',responseCut,binT=responseBin,histTitle='res')
resPuppi5=getPlot(chainDict['Step5']['tChain'],'puppiMet/genMet:genMet',responseCut,binT=responseBin,histTitle='res')
resPuppi6=getPlot(chainDict['Step6']['tChain'],'puppiMet/genMet:genMet',responseCut,binT=responseBin,histTitle='res')


resPf=getPlot(chainDict['Step1']['tChain'],'pfMet/genMet:genMet',responseCut,binT=responseBin,histTitle='res')


'''
legLoc = (0.4,0.7,0.9,0.9)



plotDir= '/afs/hephy.at/user/n/nrad/www/Puppi/METResponse/'


responseLeg= ROOT.TLegend(*legLoc)
responseLeg.SetFillColor(0)
'''
for alg in 'gen pf'.rsplit():
  chain='Step1'
  responseDict[chain][alg]['res'].Draw('COLZ')
  responseDict[chain][alg]['resProf'].SetLineWidth(2)
  responseDict[chain][alg]['resProf'].Draw('same')
  addToLeg(responseLeg,responseDict[chain][alg]['resProf'], pName='Response',RMS=1,Mean=1,RMSError=1,MeanError=1)
  responseLeg.Draw()
  ROOT.c1.Print('{DIR}/METResponse_{TITLE}.gif'.format(DIR=plotDir,TITLE=responseDict[chain][alg]['res'].GetTitle()))
'''


#### plot response and profile
for alg in compList:
  if alg in 'gen pf'.rsplit():
    st=['Step1']
    print 'drawing only', st, 'for', alg
  if alg=='puppi':
    st=steps

  for chain in st:

    responseLeg= ROOT.TLegend(0.7,0.8,0.9,0.9)
    responseLeg.SetFillColor(0)

    responseDict[chain][alg]['res'].Draw('COLZ')
    responseDict[chain][alg]['resProf'].SetMarkerStyle(20)
    responseDict[chain][alg]['resProf'].SetMarkerColor(6)
    responseDict[chain][alg]['resProf'].SetLineColor(6)
    responseDict[chain][alg]['resProf'].SetLineWidth(1)
    
    decorateAxis(responseDict[chain][alg]['res'],xAxisTitle='genMet',yAxisTitle='{ALG}Met/{genMet}'.format(ALG=alg,genMet='{genMet}'))
    addToLeg(responseLeg,responseDict[chain][alg]['resProf'], pName='ResponseCurve',RMS=0,Mean=0,RMSError=0,MeanError=1)
    responseDict[chain][alg]['resProf'].Draw('same')
    responseLeg.Draw()
    ROOT.c1.Print('{DIR}METResponse_{TITLE}.gif'.format(DIR=plotDir,TITLE=responseDict[chain][alg]['res'].GetTitle()))
    #responseLeg.Clear()



######## Response Stack

respStack=ROOT.THStack('Response','resStack')
respStack.Clear()
iColor=1



legLoc=(0.7,0.6,0.9,0.9)
responseLeg= ROOT.TLegend(*legLoc)
responseLeg.SetFillColor(0)

compList=['puppi', 'gen', 'pf']

for alg in compList:
  if alg in 'pf gen'.rsplit():
    st=['Step1']
    print 'drawing only', st, 'for', alg
  if alg=='puppi':
    st=steps
  #if alg=='gen': continue
  for chain in st:

    if alg=='puppi': 
      iColor= st.index(chain)*2+42
      print chain, iColor
      addToLeg(responseLeg,responseDict[chain][alg]['resProf'], pName='{STEP}_{ALG}'.format(STEP=chain,ALG=alg),RMS=0,Mean=0,RMSError=1,MeanError=0)
    if alg=='gen':
      iColor=1
      addToLeg(responseLeg,responseDict[chain][alg]['resProf'], pName='{ALG}'.format(STEP=chain,ALG=alg),RMS=0,Mean=0,RMSError=1,MeanError=0)
    if alg=='pf':
      iColor=3
      #responseDict[chain][alg]['resProf'].SetMarkerStyle(26)
      #responseDict[chain][alg]['resProf'].SetMarkerSize(1)
      addToLeg(responseLeg,responseDict[chain][alg]['resProf'], pName='{ALG}'.format(STEP=chain,ALG=alg),RMS=0,Mean=0,RMSError=1,MeanError=0)

    responseDict[chain][alg]['resProf'].SetLineWidth(2)
    responseDict[chain][alg]['resProf'].SetLineColor(iColor)

    respStack.Add(responseDict[chain][alg]['resProf'])
    

respStack.Draw('noStack')
responseLeg.Draw()
respStack.SetTitle("Puppi MET Response")
respStack.GetXaxis().SetTitle('genMet')
respStack.GetYaxis().SetTitle('MET/genMet')
ROOT.c1.Print('{DIR}/METResponseProfile.gif'.format(DIR=plotDir,TITLE=responseDict[chain][alg]['res'].GetTitle()))


###Response for eta<2
##chain.Draw('sqrt( (Sum$((*)Pt*sin((*)Phi)*(abs((*)Eta)<2))) **2+ (Sum$((*)Pt*cos((*)Phi)*(abs((*)Eta)<2)))**2)/(genMet*(abs(genEta)<2)):genMet'.replace('(*)','puppi'))



"""
