
from plotTools import *
import datetime


sample=samples[0]
getChains(sample)


for chain in steps:
  for var in aliasDict1:
    chainDict[chain]['tChain'].SetAlias(var,aliasDict[var])


print sample
form='{}_'.format(sample)

noNuFromW = 'ngNuMuFromW+ngNuEFromW+ngNuTauFromW==0'
nNuFromW='ngNuMuFromW+ngNuEFromW+ngNuTauFromW'
plotDir = '/afs/hephy.at/user/n/nrad/www/Puppi/{}/'.format(sample)



################# RESPONSE

plotDict['metRes']={'bin':(100,0,400),'cut':'',\
                      'xTitle':'genMet','yTitle':'PuppiResponse (GeV)', 'title':'','logX':0,'logY':0,'logZ':1 }
plotDict['metRes']['var']='(*)Met/genMet'

responseCut=nNuFromW+'==2'
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
'''

#### plot response and profile

def printResp():
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

def printRespStack():

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

  return ROOT.c1

###Response for eta<2
##chain.Draw('sqrt( (Sum$((*)Pt*sin((*)Phi)*(abs((*)Eta)<2))) **2+ (Sum$((*)Pt*cos((*)Phi)*(abs((*)Eta)<2)))**2)/(genMet*(abs(genEta)<2)):genMet'.replace('(*)','puppi'))


