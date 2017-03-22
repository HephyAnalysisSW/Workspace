# simulFakeRatePlot.py
# Simulteanous plot of tight-to-loose ratios
# Mateusz Zarucki 2017

import os
from fakeInfo import *

script = os.path.basename(__file__) #sys.argv[0]

#Arguments
args = fakeParser(script)

#Arguments
lep = args.lep
region = args.region
variable = args.variable
getData = args.getData
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

fakeInfo = fakeInfo(script, vars(args))

lepton =      fakeInfo['lepton']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

# Save
if save:
   savedir = fakeInfo['savedir']
   suffix =  fakeInfo['suffix']

   suffix2 = suffix + "_" + variable

   fakeRateDir = "%s/root/"%savedir

   savedir += "/simulFakeRatePlots"

   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

# Root file with fake rate

variables = {'pt':'lepPt', 'eta':'lepEta'}
fakeRate = {}
rootFile = {}
canv = {}

colors['djetBlind'] = colors['d1elBlind'] = colors['d1muBlind'] = colors['d1lepBlind'] = ROOT.kRed+1
colors['MC'] = ROOT.kOrange+1
colors['MC-EWK'] = ROOT.kViolet+1

fakeRate[variable] = {}
rootFile[variable] = {}

canv[variable] = ROOT.TCanvas("c1_"+variable, "Canvas " + variable, 1200, 1200)

if varBins: leg = makeLegend2(0.70,0.85,0.65,0.85) 
else:       leg = makeLegend2(0.15,0.3,0.65,0.85) 

if "measurement" in region:
   samplesList.extend(['MC', 'MC-EWK', 'data-EWK'])

for i, samp in enumerate(samplesList):
   fakeRateFile = "FakeRate_TightToLoose_%s%s_%s.root"%(variables[variable], suffix, samp)
   plot = "ratio_%s_%s"%(variable, samp)
   
   try:
      rootFile[variable][samp] = ROOT.TFile(fakeRateDir + fakeRateFile)
      fakeRate[variable][samp] = rootFile[variable][samp].Get("canv_%s"%variable).GetPrimitive("canv_%s_2"%variable).GetPrimitive(plot).Clone()
   except:
      AttributeError
      print "File", fakeRateFile, "not found. Continuing."
      continue

   canv[variable].cd()
   
   if i == 0: 
      dOpt = "P"
      fakeRate[variable][samp].SetTitle("%ss: Tight to Loose Ratio in %s Region"%(lepton, region.title()))
   else: dOpt = "Psame"

   if samp == "data-EWK":
      fakeRate[variable][samp].SetMarkerStyle(33)
      fakeRate[variable][samp].SetMarkerColor(1)
      fakeRate[variable][samp].SetMarkerSize(2)
      fakeRate[variable][samp].SetLineColor(1)
   else:
      fakeRate[variable][samp].SetMarkerColor(colors[samp])
      fakeRate[variable][samp].SetLineColor(colors[samp])
      
   fakeRate[variable][samp].SetMaximum(1) 
   fakeRate[variable][samp].Draw(dOpt) 
 
   ROOT.gPad.Modified()
   ROOT.gPad.Update()

   leg.AddEntry(plot, samp, "LP")

ROOT.gPad.Modified()
ROOT.gPad.Update()
leg.Draw()

ROOT.gPad.Modified()
ROOT.gPad.Update()
canv[variable].Modified()
canv[variable].Update()

if save:
   canv[variable].SaveAs("%s/simulFakeRatePlots%s.png"%(savedir, suffix2))
   canv[variable].SaveAs("%s/root/simulFakeRatePlots%s.root"%(savedir, suffix2))
   canv[variable].SaveAs("%s/pdf/simulFakeRatePlots%s.pdf"%(savedir, suffix2))
