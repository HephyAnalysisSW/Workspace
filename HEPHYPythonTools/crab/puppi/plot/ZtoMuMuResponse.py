from plotTools import *


plotDir='/hephy.at/user/n/nrad/www/Puppi/METResponse/ZToMuMu'

zPt='sqrt((muPt[0]*cos(muPhi[0])+muPt[1]*cos(muPhi[1]))**2+(muPt[0]*sin(muPhi[0])+muPt[1]*sin(muPhi[1]))**2)'
met='sqrt( (Sum$((*)Pt*sin((*)Phi))+(muPt[0]*sin(muPhi[0])+muPt[1]*sin(muPhi[1])) ) **2 +\
       (Sum$((*)Pt*cos((*)Phi))+(muPt[0]*cos(muPhi[0]) + muPt[1]*cos(muPhi[1])) )**2)'
pfMet=met.replace('(*)','pf')
puppiMet=met.replace('(*)','puppi')
#puppiMet='sqrt( (Sum$((*)Pt*sin((*)Phi)) ) **2+ (Sum$((*)Pt*cos((*)Phi)) )**2)'.replace('(*)','puppi')

#zxPt='(muPt[0]*cos(muPhi[0])+muPt[1]*cos(muPhi[1]))'
#xmet='(Sum$((*)Pt*cos((*)Phi)) + (muPt[0]*cos(muPhi[0]) + muPt[1]*cos(muPhi[1])))'
#pfxMet=xmet.replace('(*)','pf')
#puppixMet=xmet.replace('(*)','puppi')

#pfResponse= pfxMet+'/'+zxPt+':'+zxPt
#puppiResponse = puppixMet+'/'+zxPt+':'+zxPt



invMass ='sqrt(2*muPt[0]*muPt[1]*(cosh(muEta[0]-muEta[1])-cos(muPhi[0]-muPhi[1])))'

#realZPt='sqrt((muPt[0]*cos(muPhi[0])*'+invMassCut+'+muPt[1]*cos(muPhi[1])*'+invMassCut+')**2+(muPt[0]*sin(muPhi[0])*'+invMassCut+'+muPt[1]*sin(muPhi[1])*'+invMassCut+')**2)'

#'muPt[0]*sin(muPhi[0])+muPt[1]*sin(muPhi[1])'
#'muPt[0]*cos(muPhi[0])+muPt[1]*cos(muPhi[1])'


pfResponse= pfMet+'/'+zPt+':'+zPt
puppiResponse = puppiMet+'/'+zPt+':'+zPt


invMassCut = '('+invMass + '<= 95)&' + '('+invMass + '>=85)'
muPtCut= 'muPt[0]>20 & muPt[1]>20'


resCut = muPtCut +'&&'+ invMassCut
resCut =muPtCut 


steps=['Step1','Step2','Step3','Step4','Step5','Step6']

for step in steps:
  exec("c{STEP}= ROOT.TChain('Events')".format(STEP=step))
  exec("c{STEP}.Add('/afs/hephy.at/scratch/n/nrad/CMSSW_7_0_6_patch1/src/Workspace/HEPHYPythonTools/crab/puppi/ZToMuMu/Spring14dr_DYJetsToLL_M-50_13TeV-madgraph-pythia8-tauola_v2_AODSIM_PU_S14_POSTLS170_V6-v1Puppi{STEP}MINIAODTupel_converted.root')"\
        .format(STEP=step))


for step in steps:
  exec("puppiResDist{iSTEP}=getPlot(c{STEP},puppiResponse,resCut,binT='(30,0,300,100,0,5)',histTitle='Puppi{STEP}')"\
        .format(iSTEP=steps.index(step)+1,STEP=step))
  exec("puppiRes{iSTEP}=getProfile(c{STEP},puppiResponse,resCut,binT=(30,0,300,0,5),histTitle='Puppi{STEP}')"\
        .format(iSTEP=steps.index(step)+1,STEP=step))

pfResDist=getPlot(cStep1,pfResponse,resCut,binT='(30,0,300,100,0,5)',histTitle='pf')
pfRes=getProfile(cStep1,pfResponse,resCut,histTitle='pf')


### Print Response Stack

respStack=ROOT.THStack('Response','resStack')
legLoc=(0.7,0.6,0.9,0.9)
responseLeg= ROOT.TLegend(*legLoc)
responseLeg.SetFillColor(0)


for chain in steps:

  exec('pR=puppiRes{iSTEP}'.format(iSTEP=steps.index(chain)+1))
  iColor= steps.index(chain)*2+42
  print pR, iColor

  pR.SetLineColor(iColor)
  pR.SetLineWidth(2)
  addToLeg(responseLeg,pR, pName='Puppi_{STEP}'.format(STEP=chain),RMS=0,Mean=0,RMSError=1,MeanError=0)
  respStack.Add(pR)

pfRes.SetLineColor(3)
pfRes.SetLineWidth(2)
addToLeg(responseLeg,pfRes, pName='PF'.format(STEP=chain),RMS=0,Mean=0,RMSError=1,MeanError=0)
respStack.Add(pfRes)


respStack.Draw('noStack')
cStep1.Draw(zPt+'/'+zPt+':'+zPt,'','same')
responseLeg.Draw()
respStack.SetTitle("ZToMuMu Puppi MET Response")
respStack.GetXaxis().SetTitle('q_{T}^{Z}')
respStack.GetYaxis().SetTitle('MET/q_{T}^{Z}')
ROOT.c1.Print('{DIR}/METResponseProfile.gif'.format(DIR=plotDir,TITLE='ZtoMuMu_MET_Response'))











