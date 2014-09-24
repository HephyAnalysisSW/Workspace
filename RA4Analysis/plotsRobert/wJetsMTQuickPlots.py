import ROOT
from math import *
from Workspace.HEPHYPythonTools.helpers import getVarValue, getChain, getPlotFromChain
from Workspace.RA4Analysis.simplePlotHelpers import plot, stack, loopAndFill, drawNMStacks

from stage2Tuples import WJetsHTToLNu, WJetsToLNu25ns

#cInc = getChain(WJetsToLNu25ns)
c = getChain(WJetsHTToLNu)

binningFine = range(0,1000,20)
binningCoarse = [0,140,200,400,800]
binning = binningCoarse
c.Draw('sqrt(2.*leptonPt*met*(1-cos(leptonPhi-metphi)))','weight*(ht>400&&singleMuonic&&njets==5)')

ht=750
met=250
prefix = 'met'+str(met)+'-ht'+str(ht)

#h1.Draw('e')
#h1.SetLineColor(ROOT.kRed)
#h2.Scale(h1.Integral()/h2.Integral())
#h2.Draw('esame')
hGr4 =  getPlotFromChain(c, var='sqrt(2.*leptonPt*met*(1-cos(leptonPhi-metphi)))', binning=binning, cutString='met>'+str(met)+'&&ht>'+str(ht)+'&&singleMuonic&&njets>=4', weight='weight', binningIsExplicit=True)
h2To3 = getPlotFromChain(c, var='sqrt(2.*leptonPt*met*(1-cos(leptonPhi-metphi)))', binning=binning, cutString='met>'+str(met)+'&&ht>'+str(ht)+'&&singleMuonic&&njets>=2&&njets<4', weight='weight', binningIsExplicit=True)
h2 =    getPlotFromChain(c, var='sqrt(2.*leptonPt*met*(1-cos(leptonPhi-metphi)))', binning=binning, cutString='met>'+str(met)+'&&ht>'+str(ht)+'&&singleMuonic&&njets==2', weight='weight', binningIsExplicit=True)
h3 =    getPlotFromChain(c, var='sqrt(2.*leptonPt*met*(1-cos(leptonPhi-metphi)))', binning=binning, cutString='met>'+str(met)+'&&ht>'+str(ht)+'&&singleMuonic&&njets==3', weight='weight', binningIsExplicit=True)
#h4 =    getPlotFromChain(c, var='sqrt(2.*leptonPt*met*(1-cos(leptonPhi-metphi)))', binning=binning, cutString='met>'+str(met)+'&&ht>'+str(ht)+'&&singleMuonic&&njets==4', weight='weight', binningIsExplicit=True)

for h in [h2To4, h2, h3]:
  h.Scale(hGr5.Integral()/h.Integral())

pGr4 = plot.fromHisto(  hGr5  ,style={'legendText':'W + Jets, njets #geq 4 ',        'style':"l", 'lineThickNess':1, 'errorBars':True, 'color':ROOT.kRed, 'markerStyle':None, 'markerSize':None})
p2To3 = plot.fromHisto( h2To4 ,style={'legendText':'W + Jets, 2 #leq njets #leq 3',  'style':"l", 'lineThickNess':1, 'errorBars':True, 'color':ROOT.kBlack, 'markerStyle':None, 'markerSize':None})
p2 = plot.fromHisto(    h2    ,style={'legendText':'W + Jets, njets = 2',  'style':"l", 'lineThickNess':1, 'errorBars':True, 'color':ROOT.kGreen, 'markerStyle':None, 'markerSize':None})
p3 = plot.fromHisto(    h3,style={'legendText':'W + Jets, njets = 3',  'style':"l", 'lineThickNess':1, 'errorBars':True, 'color':ROOT.kMagenta, 'markerStyle':None, 'markerSize':None})
#p4 = plot.fromHisto(    h4,style={'legendText':'W + Jets, njets = 4',  'style':"l", 'lineThickNess':1, 'errorBars':True, 'color':ROOT.kAzure, 'markerStyle':None, 'markerSize':None})

plotLists = [[pGr4],[p2To3],\
  [p2],[p3]#,[p4]
]
labels={'x':'m_{T} (GeV)','y':'Number of Events / 10 GeV'}
ratioOps = {'yLabel':'#geq4 / 2#leq n#leq3', 'numIndex':0, 'denIndex':1 ,'yRange':None, 'logY':False, 'color':ROOT.kRed, 'yRange':(0.5,1.5)}
opt = {'fileName':'mTShape','labels':labels, 'logX':False, 'logY':True, 'yRange':[0.07, None], 'ratio':ratioOps}
opt['texLines'] = [{'pos':(0.15, 0.95),'text':'CMS Simulation',        'options':{'size':0.045}},\
                   {'pos':(0.7, 0.95), 'text':'L=2fb{}^{-1} (13 TeV)', 'options':{'size':0.045}}]
opt['legend'] = {'coordinates':[0.55,0.95 - len(plotLists)*0.10,.98,.93],'boxed':True}


stk = stack(plotLists, options = opt)
stuff=[]
stuff.append(drawNMStacks(1,1,[stk],         'pngTMP/'+prefix+'_'+stk.options['fileName']))
