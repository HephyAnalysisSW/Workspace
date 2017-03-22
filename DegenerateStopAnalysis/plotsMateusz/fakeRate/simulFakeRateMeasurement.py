# simulFakeRateMeasurement.py
# Simulteanous plot of tight-to-loose ratios in the measurement region 
# Mateusz Zarucki 2017

import os
from fakeInfo import *

script = os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

#Arguments
lep = args.lep
fakeRateMeasurement = args.fakeRateMeasurement
var = args.variable
getData = args.getData
varBins = args.varBins
considerFakeTaus = args.considerFakeTaus
logy = args.logy
save = args.save
verbose = args.verbose

fakeInfo = fakeInfo(script, vars(args))

lepton =      fakeInfo['lepton']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

#Save
if save:
   savedir = fakeInfo['savedir']
   baseDir = fakeInfo['baseDir']
   suffix =  fakeInfo['suffix']

   baseDir += "/measurementRegions"

   if considerFakeTaus:
      fakeTauDir = "fakeTausConsidered"
   else:
      fakeTauDir = "fakeTausNotConsidered"
   
   if varBins:
      binDir = "varBins"
   else:
      binDir = "fixedBins"

   suffix2 = suffix + "_%s"%var


variables = {'pt':'lepPt', 'eta':'lepEta'}
fakeRate = {}
rootFile = {}
canv = {}

colors['djetBlind'] = colors['d1elBlind'] = colors['d1muBlind'] = colors['d1lepBlind'] = ROOT.kRed+1
colors['MC'] = ROOT.kOrange
colors['MC-EWK'] = ROOT.kViolet

fakeRate[var] = {}
rootFile[var] = {}
canv[var] = {}

MRs = [d for d in os.listdir(baseDir) if os.path.isdir(os.path.join(baseDir, d)) and 'measurement' in d]

if varBins: leg = makeLegend2(0.70,0.85,0.65,0.85) 
else:       leg = makeLegend2(0.15,0.3,0.65,0.85) 

canv[var][fakeRateMeasurement] = ROOT.TCanvas("c1_%s_%s"%(var, fakeRateMeasurement), "Canvas %s %s"%(var, fakeRateMeasurement), 1200, 1200)
fakeRate[var][fakeRateMeasurement] = {}
rootFile[var][fakeRateMeasurement] = {}

if save: suffix_ = suffix2

for i, MR in enumerate(sorted(MRs)):

   fakeRateDir = "%s/%s/tightToLooseRatio/allBins/%s/%s/%s/root/"%(baseDir, MR, fakeTauDir, lepton, binDir)
   fakeRateFile = "FakeRate_TightToLoose_%s%s_%s_%s.root"%(variables[var], suffix, MR, fakeRateMeasurement)
   plotName = "ratio_%s_%s"%(var, fakeRateMeasurement)
   
   try:
      rootFile[var][fakeRateMeasurement][MR] = ROOT.TFile(fakeRateDir + fakeRateFile)
      fakeRate[var][fakeRateMeasurement][MR] = rootFile[var][fakeRateMeasurement][MR].Get('canv_%s'%var).GetPrimitive("canv_%s_2"%var).GetPrimitive(plotName).Clone()
   except:
      AttributeError
      print "File", fakeRateFile, "not found. Continuing."
      continue
  
   plotName = plotName + "_" + MR    
   fakeRate[var][fakeRateMeasurement][MR].SetName(plotName)

   canv[var][fakeRateMeasurement].cd()

   if i == 0: 
      dOpt = "P"
      fakeRate[var][fakeRateMeasurement][MR].SetTitle("%ss: Tight to Loose Ratio in the Measurement Regions"%lepton)
   else: dOpt = "same"

   fakeRate[var][fakeRateMeasurement][MR].SetMarkerColor(i+2)
   fakeRate[var][fakeRateMeasurement][MR].SetLineColor(i+2)
      
   fakeRate[var][fakeRateMeasurement][MR].SetMaximum(0.6) 
   fakeRate[var][fakeRateMeasurement][MR].Draw(dOpt) 

   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   leg.AddEntry(plotName, fakeRateMeasurement + "_" + MR.replace('measurement', 'MR'), "LP")

ROOT.gPad.Modified()
ROOT.gPad.Update()
leg.Draw()

ROOT.gPad.Modified()
ROOT.gPad.Update()
canv[var][fakeRateMeasurement].Modified()
canv[var][fakeRateMeasurement].Update()

if save:
   suffix_ += "_%s"%fakeRateMeasurement
   canv[var][fakeRateMeasurement].SaveAs("%s/simulFakeRateMeasurement%s.png"%(savedir, suffix_))
   canv[var][fakeRateMeasurement].SaveAs("%s/root/simulFakeRateMeasurement%s.root"%(savedir, suffix_))
   canv[var][fakeRateMeasurement].SaveAs("%s/pdf/simulFakeRateMeasurement%s.pdf"%(savedir, suffix_))
