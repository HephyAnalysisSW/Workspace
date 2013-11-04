import ROOT
ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
from xsec import xsec

small = False                         #Steering for this script. Use True for development
variable = "met"                      #The variable to plot
cut = "singleMuonic&&ht>400&&met>100&&nbtags>=2" #The cut to use
binning = [50,100,1100]               #binning

def getVarValue(c, var, n=0):         #A general method to get the value of a variable from a chain after chain.GetEntry(i) has been called
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  else:
    return float('nan')

hString = "h*.root"                 #If small, chain only a few files
if small:
  hString = "histo_10_*.root"

cData = ROOT.TChain("Events")
cData.Add("/data/mhickel/pat_120927/data8TeV/MuHad-Run2012A-13Jul2012/histo_*.root")
cData.Add("/data/mhickel/pat_120927/data8TeV/MuHad-Run2012B-13Jul2012/histo_*.root")
targetLumi = 5000.

cTTbar = ROOT.TChain("Events")
dTTbar = ROOT.TChain("Runs")        #Now count number of MC events
for c in [cTTbar, dTTbar]:
  c.Add("/data/schoef/pat_120925/mc8TeV/8TeV-TTJets/histo_*.root")

nEventsTTbar = 0
nruns = dTTbar.GetEntries()
for i in range(0, nruns):
  dTTbar.GetEntry(i)
  nEventsTTbar += dTTbar.GetLeaf("uint_EventCounter_runCounts_PAT.obj").GetValue()

weightTTbar = xsec['8TeV-TTJets']*targetLumi / nEventsTTbar     #calculate weight for MC
print "Calculated weight:", weightTTbar

#Define two samples; I used dicts. Adapt as you need.
data  = {"name":"MuHad data", "chain":cData, "histo":ROOT.TH1F("metData",  "metData", *binning), "weight":1.0,         "color":ROOT.kBlack}
mc    = {"name":"TTJets MC",  "chain":cTTbar,"histo":ROOT.TH1F("metMC",    "metMC", *binning),   "weight":weightTTbar, "color":ROOT.kBlue}

allSamples = [data, mc] #For convinience

for sample in allSamples: #Loop over samples
  sample["chain"].Draw(">>eList", cut) #Get the event list 'eList' which has all the events satisfying the cut
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  print "Sample ",sample["name"],": Will loop over", number_events,"events" #Number of events satisfying the cut
  for i in range(number_events): #Loop over those events
    if i>0 and (i%10000)==0:
      print "Filled",i
    sample["chain"].GetEntry(elist.GetEntry(i))  #Set the chain to the current event (it's the i-th event of the eList). This is the central line in this file!
    varValue = getVarValue(sample["chain"], variable)   #Get the value of the variable
    sample["histo"].Fill(varValue, sample["weight"]) #Fill the histo
  del elist


#Draw the histograms ...

l = ROOT.TLegend(0.7,0.8,1.0,1.0)
l.SetFillColor(0)
l.SetShadowColor(ROOT.kWhite)
l.SetBorderSize(1)

for i, sample in enumerate(allSamples):
  sample["histo"].SetLineColor(sample["color"]) 
  sample["histo"].SetMarkerSize(0)
  sample["histo"].SetMarkerStyle(0)
  sample["histo"].GetXaxis().SetTitle(variable)
  sample["histo"].GetYaxis().SetTitle("Events / "+str( (binning[2] - binning[1])/binning[0])+" GeV")
  sample["histo"].GetXaxis().SetLabelSize(0.04)
  sample["histo"].GetYaxis().SetLabelSize(0.04)

  if i==0:
    sample["histo"].Draw()
  else:
    sample["histo"].Draw("same")
  l.AddEntry(sample["histo"], sample["name"])

l.Draw()
 
