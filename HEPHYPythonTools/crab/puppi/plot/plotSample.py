from plotTools import *




###############
sample=samples[0]


for s in samples:
  exec('{S}=getChains(\"{S}\").copy()'.format(S=s))

sampleDict={}
for s in samples:
  sampleDict[s]=getChains(s).copy()
  for step in steps:
    setAliases(sampleDict[s][step]['tChain'],aliasDict1)

#getChains(sample)
###############
plotDir=''
cut=''
form=''

getPlotDict('')
#printChain(plotDict,sampleDict['TTJets'],varToPlot='gamma', algToPlot='pf',chainToPlot='Step1')

#chainComp(chainDict,'sumEt1D',aliasDict['SumEt1D'],cutS=cut,binT=(100,0,3500))
#printChainStack(chainDict,'sumEt1D','gen pf puppi',plotDir=plotDir,plotName='{}_Met'.format(form),xTitle='GeV',yTitle='nEvents',logY=1)


TTJetsPlotDict=getPlotDict(noNuFromW)
printChain(TTJetsPlotDict,sampleDict['TTJets'], varToPlot='gamma h_HFpt',algToPlot='pf',chainToPlot='Step1',debug=1)

legLoc1=(0.525,0.72,0.9,0.9)

