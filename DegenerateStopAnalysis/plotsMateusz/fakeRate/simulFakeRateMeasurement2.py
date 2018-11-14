# simulFakeRateMeasurement.py
# Simulteanous plot of tight-to-loose ratios in the measurement region 
# Mateusz Zarucki 2017

import os
from fakeInfo import *

#ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptStat(0)

script = "simulFakeRateMeasurement.py" #os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

#Arguments
lep = args.lep
measurementType = args.measurementType
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
   etaBin =  fakeInfo['etaBin']
   suffix =  fakeInfo['suffix']

   baseDir += "/prev2/measurementRegions"

   if considerFakeTaus:
      fakeTauDir = "fakeTausConsidered"
   else:
      fakeTauDir = "fakeTausNotConsidered"
   
   if varBins:
      binDir = "varBins"
   else:
      binDir = "fixedBins"

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
MRs = sorted(MRs)
#MRs.reverse()

if varBins: leg = makeLegend2(0.65,0.85,0.60,0.85) 
else:       leg = makeLegend2(0.15,0.3,0.65,0.85) 

canv[var][measurementType] = ROOT.TCanvas("c1_%s_%s"%(var, measurementType), "Canvas %s %s"%(var, measurementType), 1200, 1200)
fakeRate[var][measurementType] = {}
rootFile[var][measurementType] = {}

#MRs = MRs.reverse()

for i, MR in enumerate(MRs):

   if not 'measurement1' in MR and not 'measurement4' in MR: continue

   if lep == 'el' and 'measurement4' in MR: continue #FIXME
   if measurementType == "data-EWK" and 'measurement2' in MR: continue #FIXME

   if var == "eta" and lep == "mu" and "measurement4" in MR: continue #FIXME 

   fakeRateDir = "%s/%s/tightToLooseRatio/allBins/%s/%s/%s/%s/%s/log/root/"%(baseDir, MR, fakeTauDir, lepton, binDir, measurementType, etaBin)
   fakeRateFile = "FakeRate_TightToLoose_%s_%s_%s_%s.root"%(variables[var], lep, MR, measurementType)
   plotName = "ratio_%s_%s"%(var, measurementType)
   
   try:
      rootFile[var][measurementType][MR] = ROOT.TFile(fakeRateDir + fakeRateFile)
      fakeRate[var][measurementType][MR] = rootFile[var][measurementType][MR].Get('canv_%s'%var).GetPrimitive("canv_%s_2"%var).GetPrimitive(plotName).Clone()
   except:
      AttributeError
      print "File", fakeRateFile, "not found. Continuing."
      continue
   if var == "pt" and lep == 'mu' and 'measurement1' in MR: 
      #fakeRate[var][measurementType][MR].SetBinContent(6, -1)
      fakeRate[var][measurementType][MR].SetBinContent(7, -1)
      fakeRate[var][measurementType][MR].SetBinContent(8, -1)
  
   plotName = plotName + "_" + MR    
   fakeRate[var][measurementType][MR].SetName(plotName)

   canv[var][measurementType].cd()

   if i == 0: 
      dOpt = "P"
   else: dOpt = "same"
      
   fakeRate[var][measurementType][MR].SetTitle("")#Tight to Loose Ratios in {} for {}s".format(measurementType, lepton).replace('-EWK',''))

   if 'bTag' in MR:
      fakeRate[var][measurementType][MR].SetMarkerColor(4)
      fakeRate[var][measurementType][MR].SetLineColor(4)
   elif 'bVeto' in MR:
      fakeRate[var][measurementType][MR].SetMarkerColor(2)
      fakeRate[var][measurementType][MR].SetLineColor(2)
   else:
      fakeRate[var][measurementType][MR].SetMarkerColor(1)
      fakeRate[var][measurementType][MR].SetLineColor(1)

   #fakeRate[var][measurementType][MR].SetMarkerColor(9-i)
   #fakeRate[var][measurementType][MR].SetLineColor(9-i)
      
   fakeRate[var][measurementType][MR].SetMaximum(0.6) 
   fakeRate[var][measurementType][MR].Draw(dOpt) 

   ROOT.gPad.Modified()
   ROOT.gPad.Update()
 
   if i < 3:
      if 'bTag' in MR or 'bVeto' in MR: 
         leg.AddEntry(plotName, MR.split('_')[-1] + ' (' + measurementType.replace('-EWK','') + ')', "LP")
      else:   
         leg.AddEntry(plotName, 'Central' + ' (' + measurementType.replace('-EWK','') + ')', "LP")

ROOT.gPad.Modified()
ROOT.gPad.Update()
leg.Draw()

ROOT.gPad.Modified()
ROOT.gPad.Update()
canv[var][measurementType].Modified()
canv[var][measurementType].Update()

if save:
   suffix += "_" + variables[var]
   suffix += "_" + etaBin
   canv[var][measurementType].SaveAs("%s/simulFakeRateMeasurement%s.png"%(savedir, suffix))
   canv[var][measurementType].SaveAs("%s/root/simulFakeRateMeasurement%s.root"%(savedir, suffix))
   canv[var][measurementType].SaveAs("%s/pdf/simulFakeRateMeasurement%s.pdf"%(savedir, suffix))
